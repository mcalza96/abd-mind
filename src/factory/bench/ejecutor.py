"""Ejecutor de abd-bench (fase 7): corre el motor y la línea base sobre los casos.

Para cada caso:
- **Motor:** abre un caso en el dominio `abierto` con la pregunta `tipo_de_causa`, registra
  las observaciones tal como las vio cada observador (sin córtex: ya son hechos atómicos),
  genera hipótesis, evalúa, expande si el motor lo sugiere y pide la mejor explicación.
- **Línea base:** cada modelo de `roles.linea_base` responde en una sola llamada con la misma
  información y la misma pregunta (D10).

El motor nunca ve `solucion`, `verdad` ni `respuesta_inductiva_erronea`. La comparación con la
verdad la hace este módulo después, y solo cuenta para la precisión cuando la verdad está
`establecida` (docs/marco-teorico/12 §12.1). El resultado sirve para encontrar fallas, no
como puntaje (datasets/abd-bench/README.md).
"""

import functools
import time
from collections.abc import Callable
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from typing import Literal

from pydantic import BaseModel, Field

from factory.bench.casos import PREGUNTA_TIPO_CAUSA, Caso, TipoCausa
from factory.config import Config, ConfigRol
from factory.contracts.observation import Observacion, Observador
from factory.engine.case_service import ServicioCasos
from factory.engine.modelos import EntradaObservador, ErrorCaso
from factory.engine.store import Store
from factory.organ.rule_engine import cargar_reglas
from factory.organ.texto import normalizar
from factory.transition.deterministic.respuesta import clase_de
from factory.transition.stochastic.contexto import (
    describir_dominio,
    describir_observaciones,
    describir_pregunta,
)
from factory.transition.stochastic.llm_client import Cache, ClienteLLM, ErrorLLM, Transporte

DOMINIO = "abierto"

SISTEMA_BASE = "Responde la pregunta del usuario con tu mejor respuesta, de forma directa."


class RespuestaBaseLLM(BaseModel):
    tipo_de_causa: Literal[
        "entidad_nueva", "error_del_observador", "ley_incorrecta", "mecanismo_conocido"
    ]
    mecanismo: str


class ResultadoMotor(BaseModel):
    tipo: TipoCausa | None = Field(description="Respuesta a la pregunta, si quedó determinada")
    determinada: bool = False
    fragil: bool = False
    margen_veredictos: int | None = None
    mecanismo: str | None = Field(default=None, description="H*, o la líder de la clase ganadora")
    tipos_propuestos: list[TipoCausa] = Field(
        default_factory=list, description="Tipos de causa entre las hipótesis generadas"
    )
    hipotesis: int = 0
    expansion: bool = False
    llamadas: int = 0
    segundos: float = 0.0
    error: str | None = None


class ResultadoBase(BaseModel):
    modelo: str
    tipo: TipoCausa | None = None
    mecanismo: str | None = None
    error: str | None = None


class ResultadoCaso(BaseModel):
    id: str
    serie: str
    variante_de: str | None
    contaminacion: str
    estado_verdad: str
    tipo_verdad: TipoCausa
    tipo_secundario: TipoCausa | None
    motor: ResultadoMotor | None = None
    linea_base: list[ResultadoBase] = Field(default_factory=list)


def _observadores(caso: Caso) -> dict[str, EntradaObservador]:
    return {o.id: EntradaObservador(nombre=o.nombre, marco=o.marco) for o in caso.observadores}


def _contenido(caso: Caso, indice: int) -> str:
    o = caso.observaciones[indice]
    return f"[{o.momento}] {o.contenido}" if o.momento else o.contenido


def _tipo(valor: object) -> TipoCausa | None:
    clase = clase_de({"tipo_de_causa": valor}, PREGUNTA_TIPO_CAUSA)
    return TipoCausa(clase) if clase is not None else None


class EjecutorBench:
    def __init__(
        self,
        config: Config,
        directorio: Path,
        *,
        transporte: Transporte | None = None,
        cache: Cache | None = None,
        motor: bool = True,
        linea_base: bool = True,
    ) -> None:
        self.config = config
        self.directorio = directorio
        self.transporte = transporte
        self.cache = cache
        self.con_motor = motor
        self.con_linea_base = linea_base

    def ejecutar(
        self,
        casos: list[Caso],
        paralelo: int = 1,
        progreso: Callable[[ResultadoCaso], None] | None = None,
    ) -> list[ResultadoCaso]:
        self.directorio.mkdir(parents=True, exist_ok=True)

        def uno(caso: Caso) -> ResultadoCaso:
            resultado = self.ejecutar_caso(caso)
            if progreso is not None:
                progreso(resultado)
            return resultado

        if paralelo <= 1:
            return [uno(c) for c in casos]
        with ThreadPoolExecutor(max_workers=paralelo) as grupo:
            return list(grupo.map(uno, casos))

    def ejecutar_caso(self, caso: Caso) -> ResultadoCaso:
        resultado = ResultadoCaso(
            id=caso.id,
            serie=caso.serie,
            variante_de=caso.variante_de,
            contaminacion=caso.contaminacion,
            estado_verdad=caso.verdad.estado,
            tipo_verdad=caso.solucion.tipo_de_causa,
            tipo_secundario=caso.solucion.tipo_secundario,
        )
        if self.con_motor:
            resultado.motor = self._motor(caso)
        if self.con_linea_base:
            resultado.linea_base = [self._base(caso, rol) for rol in self.config.roles.linea_base]
        return resultado

    # --- motor ----------------------------------------------------------------------------

    def _motor(self, caso: Caso) -> ResultadoMotor:
        inicio = time.monotonic()
        ruta = self.directorio / f"{caso.id}.db"
        ruta.unlink(missing_ok=True)
        store = Store(ruta)
        resultado = ResultadoMotor(tipo=None)
        try:
            servicio = ServicioCasos(
                store, self.config, transporte=self.transporte, cache=self.cache
            )
            # La descripción no lleva el título: puede nombrar el caso histórico.
            caso_id = servicio.crear_caso(
                "Explicar por qué estos observadores reportan cosas que parecen incompatibles",
                DOMINIO,
                pregunta=PREGUNTA_TIPO_CAUSA,
            ).caso_id
            observadores = _observadores(caso)
            for i, o in enumerate(caso.observaciones):
                servicio.agregar_observacion(
                    caso_id,
                    observadores[o.observador],
                    _contenido(caso, i),
                    rol=o.rol,
                    extraer=False,
                )
            servicio.generar_hipotesis(caso_id, modo="contrastivo")
            evaluacion = servicio.evaluar(caso_id)
            if evaluacion.expansion_sugerida:
                resultado.expansion = True
                servicio.generar_hipotesis(caso_id, modo="expansion")
                servicio.evaluar(caso_id)
            mejor = servicio.mejor_explicacion(caso_id)
            auditoria = servicio.auditoria(caso_id)
            resultado.hipotesis = len(auditoria.hipotesis)
            resultado.tipos_propuestos = sorted(
                {
                    t
                    for h in auditoria.hipotesis
                    if (t := _tipo(h.afirmaciones.get("tipo_de_causa")))
                }
            )
            r = mejor.respuesta
            if r is not None:
                resultado.determinada = r.determinada
                resultado.fragil = r.fragil
                resultado.margen_veredictos = r.margen_veredictos
                if r.determinada and r.valor is not None:
                    resultado.tipo = TipoCausa(r.valor)
                lider = mejor.h_estrella.id_hipotesis if mejor.h_estrella else r.lider
                if lider is not None:
                    resultado.mecanismo = next(
                        h.mecanismo for h in auditoria.hipotesis if h.id_hipotesis == lider
                    )
            resultado.llamadas = servicio.estado_caso(caso_id).llamadas
        except (ErrorCaso, ErrorLLM) as e:
            resultado.error = str(e)
        finally:
            store.cerrar()
        resultado.segundos = round(time.monotonic() - inicio, 1)
        return resultado

    # --- línea base -----------------------------------------------------------------------

    def _base(self, caso: Caso, rol: ConfigRol) -> ResultadoBase:
        cliente = ClienteLLM(self.config, self.transporte, self.cache, max_llamadas=5)
        observadores = {
            o.id: Observador(id=o.id, nombre=o.nombre, marco=o.marco) for o in caso.observadores
        }
        observaciones = [
            Observacion(id=f"y{i}", observador_id=o.observador, contenido=_contenido(caso, i - 1))
            for i, o in enumerate(caso.observaciones, start=1)
        ]
        usuario = "\n\n".join(
            [
                describir_dominio(cargar_reglas(DOMINIO)),
                describir_observaciones(observadores, observaciones),
                describir_pregunta(PREGUNTA_TIPO_CAUSA),
                "Da una única respuesta: el tipo de causa y, en 'mecanismo', la explicación "
                "concreta en una o dos frases.",
            ]
        )
        try:
            bruto = cliente.completar_json(rol, SISTEMA_BASE, usuario, RespuestaBaseLLM)
            return ResultadoBase(
                modelo=rol.modelo, tipo=_tipo(bruto.tipo_de_causa), mecanismo=bruto.mecanismo
            )
        except ErrorLLM as e:
            return ResultadoBase(modelo=rol.modelo, error=str(e))


# --- informe -------------------------------------------------------------------------------


def acierto(tipo: TipoCausa | None, r: ResultadoCaso, aceptar_secundario: bool = False) -> bool:
    if tipo is None:
        return False
    return tipo is r.tipo_verdad or (aceptar_secundario and tipo is r.tipo_secundario)


def _celda(tipo: TipoCausa | None, r: ResultadoCaso) -> str:
    if tipo is None:
        return "—"
    marca = "✓" if acierto(tipo, r) else ("½" if acierto(tipo, r, True) else "✗")
    return f"{marca} {tipo.value}"


def informe_markdown(resultados: list[ResultadoCaso]) -> str:
    modelos = sorted({b.modelo for r in resultados for b in r.linea_base})
    lineas = ["# Resultados de abd-bench", ""]
    lineas += [
        "Precisión sobre el tipo de causa, solo con verdad `establecida`. ✓ acierta el tipo "
        "principal, ½ el secundario, ✗ falla, — sin respuesta determinada. Sirve para "
        "encontrar fallas, no como puntaje (datasets/abd-bench/README.md).",
        "",
    ]

    def precision(elegir: Callable[[ResultadoCaso], TipoCausa | None], grupo: str) -> str:
        validos = [
            r for r in resultados if r.estado_verdad == "establecida" and _en_grupo(r, grupo)
        ]
        if not validos:
            return "—"
        aciertos = sum(acierto(elegir(r), r) for r in validos)
        return f"{aciertos}/{len(validos)}"

    grupos = ["todos", "originales", "variantes", "contaminación alta", "contaminación baja"]
    cabecera = ["Grupo", "Motor", *modelos]
    lineas += ["| " + " | ".join(cabecera) + " |", "|" + "---|" * len(cabecera)]
    for g in grupos:
        fila = [g, precision(_tipo_motor, g)]
        for modelo in modelos:
            fila.append(precision(functools.partial(_tipo_base, modelo=modelo), g))
        lineas.append("| " + " | ".join(fila) + " |")

    con_motor = [r for r in resultados if r.motor is not None]
    if con_motor:
        propuso = sum(
            r.tipo_verdad in r.motor.tipos_propuestos for r in con_motor if r.motor is not None
        )
        frágiles = sum(1 for r in con_motor if r.motor is not None and r.motor.fragil)
        indeterminadas = sum(
            1 for r in con_motor if r.motor is not None and not r.motor.determinada
        )
        lineas += [
            "",
            f"- El generador propuso el tipo verdadero en {propuso}/{len(con_motor)} casos "
            "(si no lo propone, el motor no puede elegirlo: falla de generación, no de selección).",
            f"- Respuestas frágiles: {frágiles}; sin determinar: {indeterminadas}.",
        ]

    lineas += ["", "## Por caso", ""]
    cabecera = ["Caso", "Verdad", "Contam.", "Motor", "Margen", *modelos]
    lineas += ["| " + " | ".join(cabecera) + " |", "|" + "---|" * len(cabecera)]
    for r in resultados:
        mo = r.motor
        motor = "error" if mo and mo.error else (_celda(mo.tipo, r) if mo else "")
        if mo and mo.fragil and mo.determinada:
            motor += " (frágil)"
        margen = "∞" if mo and mo.determinada and mo.margen_veredictos is None else ""
        if mo and mo.margen_veredictos is not None:
            margen = str(mo.margen_veredictos)
        verdad = r.tipo_verdad.value + ("" if r.estado_verdad == "establecida" else " (no est.)")
        fila = [r.id, verdad, r.contaminacion, motor, margen]
        fila += [_celda(_tipo_base(r, mod), r) for mod in modelos]
        lineas.append("| " + " | ".join(fila) + " |")

    pares = [
        (r, o) for r in resultados if r.variante_de for o in resultados if o.id == r.variante_de
    ]
    if pares:
        lineas += ["", "## Originales frente a variantes", ""]
        lineas += ["| Variante | Original | Motor (var / orig) | Línea base (var / orig) |"]
        lineas.append("|---|---|---|---|")
        for v, o in pares:
            motor = f"{_celda(v.motor.tipo if v.motor else None, v)} / " + _celda(
                o.motor.tipo if o.motor else None, o
            )
            bases = "; ".join(
                f"{m}: {_celda(_tipo_base(v, m), v)} / {_celda(_tipo_base(o, m), o)}"
                for m in modelos
            )
            lineas.append(f"| {v.id} | {o.id} | {motor} | {bases} |")
        lineas += [
            "",
            "Si un sistema acierta el original y falla la variante, probablemente recuerda el "
            "caso en vez de razonarlo.",
        ]

    errores = [(r.id, r.motor.error) for r in resultados if r.motor and r.motor.error]
    errores += [
        (r.id, f"{b.modelo}: {b.error}") for r in resultados for b in r.linea_base if b.error
    ]
    if errores:
        lineas += ["", "## Errores", ""]
        lineas += [f"- {i}: {e}" for i, e in errores]
    return "\n".join(lineas) + "\n"


def _tipo_motor(r: ResultadoCaso) -> TipoCausa | None:
    return r.motor.tipo if r.motor else None


def _tipo_base(r: ResultadoCaso, modelo: str) -> TipoCausa | None:
    return next((b.tipo for b in r.linea_base if b.modelo == modelo), None)


def _en_grupo(r: ResultadoCaso, grupo: str) -> bool:
    return {
        "todos": True,
        "originales": r.serie != "V",
        "variantes": r.serie == "V",
        "contaminación alta": r.contaminacion == "alta",
        "contaminación baja": r.contaminacion == "baja",
    }[grupo]


def seleccionar(casos: list[Caso], ids: list[str] | None, series: list[str] | None) -> list[Caso]:
    """Filtra por id o serie. `pares` en ids agrega cada variante con su original."""
    elegidos = casos
    if series:
        elegidos = [c for c in elegidos if c.serie in series]
    if ids:
        pedidos = {normalizar(i).upper() for i in ids}
        if "PARES" in pedidos:
            originales = {c.variante_de for c in casos if c.variante_de}
            pedidos |= {c.id for c in casos if c.serie == "V"} | {o for o in originales if o}
        elegidos = [c for c in elegidos if c.id.upper() in pedidos]
    return elegidos
