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
import threading
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
        "entidad_nueva",
        "error_del_observador",
        "ley_incorrecta",
        "mecanismo_conocido",
        "indeterminado",
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
    respondio: str | None = Field(default=None, description="Modelo que respondió (fallback)")
    abstuvo: bool = Field(default=False, description="Respondió 'indeterminado'")
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
    determinable: bool = True
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

        parcial = self.directorio / "resultados.parcial.jsonl"
        candado = threading.Lock()

        def uno(caso: Caso) -> ResultadoCaso:
            resultado = self.ejecutar_caso(caso)
            # Se guarda cada caso al terminar: una falla tardía no pierde la corrida.
            with candado, parcial.open("a", encoding="utf-8") as f:
                f.write(resultado.model_dump_json() + "\n")
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
            determinable=caso.determinable,
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
        except Exception as e:  # un caso que falla no debe tumbar la corrida (EXP-010)
            resultado.error = f"{type(e).__name__}: {e}"
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
                "concreta en una o dos frases. Si la evidencia no permite distinguir entre "
                "tipos de causa, responde 'indeterminado' y explica en 'mecanismo' qué falta.",
            ]
        )
        try:
            bruto, respondio = cliente.completar_json_con_modelo(
                rol, SISTEMA_BASE, usuario, RespuestaBaseLLM
            )
            return ResultadoBase(
                modelo=rol.modelo,
                respondio=respondio,
                tipo=_tipo(bruto.tipo_de_causa),
                abstuvo=bruto.tipo_de_causa == "indeterminado",
                mecanismo=bruto.mecanismo,
            )
        except ErrorLLM as e:
            return ResultadoBase(modelo=rol.modelo, error=str(e))
        except Exception as e:  # idem: se registra y la corrida sigue
            return ResultadoBase(modelo=rol.modelo, error=f"{type(e).__name__}: {e}")


# --- informe -------------------------------------------------------------------------------

ABSTENCION = "indeterminado"


def respuesta_motor(r: ResultadoCaso) -> str | None:
    """Tipo de causa, 'indeterminado' si el motor no decidió, o None si falló o no corrió."""
    m = r.motor
    if m is None or m.error:
        return None
    return m.tipo.value if m.tipo else ABSTENCION


def respuesta_base(r: ResultadoCaso, modelo: str) -> str | None:
    b = next((b for b in r.linea_base if b.modelo == modelo), None)
    if b is None or b.error:
        return None
    if b.abstuvo:
        return ABSTENCION
    return b.tipo.value if b.tipo else None


def correcta(r: ResultadoCaso, respuesta: str | None) -> bool:
    """En casos sin respuesta posible lo correcto es abstenerse; en los demás, el tipo verdadero."""
    if respuesta is None:
        return False
    if not r.determinable:
        return respuesta == ABSTENCION
    return respuesta == r.tipo_verdad.value


def _celda(r: ResultadoCaso, respuesta: str | None) -> str:
    if respuesta is None:
        return "error"
    if correcta(r, respuesta):
        return f"✓ {respuesta}"
    if r.tipo_secundario is not None and respuesta == r.tipo_secundario.value:
        return f"½ {respuesta}"
    return f"✗ {respuesta}"


GRUPOS: dict[str, Callable[[ResultadoCaso], bool]] = {
    "reales (A–E)": lambda r: r.serie in "ABCDE",
    "variantes (V)": lambda r: r.serie == "V",
    "perturbaciones (P)": lambda r: r.serie == "P",
    "sin respuesta (U): se abstiene": lambda r: r.serie == "U",
    "contaminación alta": lambda r: r.contaminacion == "alta" and r.determinable,
    "contaminación baja": lambda r: r.contaminacion == "baja" and r.determinable,
}


def informe_markdown(resultados: list[ResultadoCaso]) -> str:
    modelos = sorted({b.modelo for r in resultados for b in r.linea_base})
    hay_motor = any(r.motor is not None for r in resultados)
    sistemas: list[tuple[str, Callable[[ResultadoCaso], str | None]]] = []
    if hay_motor:
        sistemas.append(("Motor", respuesta_motor))
    sistemas += [(m, functools.partial(respuesta_base, modelo=m)) for m in modelos]

    lineas = ["# Resultados de abd-bench", ""]
    lineas += [
        "Respuestas correctas sobre el tipo de causa, solo con verdad `establecida`. En los "
        "casos sin respuesta posible (U) lo correcto es abstenerse ('indeterminado'). ✓ "
        "correcta, ½ acierta el tipo secundario, ✗ incorrecta. Sirve para encontrar fallas, no "
        "como puntaje (datasets/abd-bench/README.md).",
        "",
    ]
    cabecera = ["Grupo", *[n for n, _ in sistemas]]
    lineas += ["| " + " | ".join(cabecera) + " |", "|" + "---|" * len(cabecera)]
    for nombre, en_grupo in GRUPOS.items():
        validos = [r for r in resultados if r.estado_verdad == "establecida" and en_grupo(r)]
        if not validos:
            continue
        fila = [nombre]
        for _, responder in sistemas:
            fila.append(f"{sum(correcta(r, responder(r)) for r in validos)}/{len(validos)}")
        lineas.append("| " + " | ".join(fila) + " |")

    determinables = [r for r in resultados if r.determinable and r.estado_verdad == "establecida"]
    if determinables:
        lineas += ["", "Abstenciones en casos que sí tenían respuesta (falsas abstenciones):", ""]
        lineas += [
            f"- {n}: {sum(1 for r in determinables if f(r) == ABSTENCION)}/{len(determinables)}"
            for n, f in sistemas
        ]

    con_motor = [r for r in resultados if r.motor is not None and not r.motor.error]
    if con_motor:
        propuso = sum(
            r.tipo_verdad in r.motor.tipos_propuestos
            for r in con_motor
            if r.motor is not None and r.determinable
        )
        firmes = [
            r
            for r in con_motor
            if r.motor and r.determinable and r.motor.determinada and not r.motor.fragil
        ]
        fragiles = [
            r
            for r in con_motor
            if r.motor and r.determinable and r.motor.determinada and r.motor.fragil
        ]

        def tasa(grupo: list[ResultadoCaso]) -> str:
            if not grupo:
                return "—"
            return f"{sum(correcta(r, respuesta_motor(r)) for r in grupo)}/{len(grupo)}"

        lineas += [
            "",
            "## Motor",
            "",
            f"- El generador propuso el tipo verdadero en {propuso}/"
            f"{sum(1 for r in con_motor if r.determinable)} casos con respuesta (si no lo "
            "propone, el motor no puede elegirlo: falla de generación, no de selección).",
            f"- Respuestas firmes correctas: {tasa(firmes)}; respuestas frágiles correctas: "
            f"{tasa(fragiles)}. Si la fragilidad sirve, las firmes aciertan más.",
        ]

    lineas += ["", "## Por caso", ""]
    cabecera = ["Caso", "Verdad", "Contam.", "Margen", *[n for n, _ in sistemas]]
    lineas += ["| " + " | ".join(cabecera) + " |", "|" + "---|" * len(cabecera)]
    for r in resultados:
        mo = r.motor
        margen = ""
        if mo and mo.determinada:
            margen = "∞" if mo.margen_veredictos is None else str(mo.margen_veredictos)
            margen += " (frágil)" if mo.fragil else ""
        verdad = r.tipo_verdad.value if r.determinable else ABSTENCION
        if r.estado_verdad != "establecida":
            verdad += " (no est.)"
        fila = [r.id, verdad, r.contaminacion, margen]
        fila += [_celda(r, responder(r)) for _, responder in sistemas]
        lineas.append("| " + " | ".join(fila) + " |")

    por_id = {r.id: r for r in resultados}
    derivados = [(r, por_id[r.variante_de]) for r in resultados if r.variante_de in por_id]
    if derivados:
        lineas += ["", "## Casos derivados frente a su origen", ""]
        lineas += [
            "| Derivado | Origen | " + " | ".join(f"{n} (der. / orig.)" for n, _ in sistemas) + " |"
        ]
        lineas.append("|---|---|" + "---|" * len(sistemas))
        for d, o in derivados:
            celdas = [
                f"{_celda(d, responder(d))} / {_celda(o, responder(o))}"
                for _, responder in sistemas
            ]
            lineas.append(f"| {d.id} | {o.id} | " + " | ".join(celdas) + " |")
        lineas += [
            "",
            "- Variante (V): si un sistema acierta el original y falla la variante, "
            "probablemente recuerda el caso.",
            "- Perturbación (P): un sistema que da la misma respuesta en ambos no sigue la "
            "evidencia que cambió.",
            "- Sin respuesta (U): lo correcto es abstenerse.",
        ]

    errores = [(r.id, r.motor.error) for r in resultados if r.motor and r.motor.error]
    errores += [
        (r.id, f"{b.modelo}: {b.error}") for r in resultados for b in r.linea_base if b.error
    ]
    if errores:
        lineas += ["", "## Errores", ""]
        lineas += [f"- {i}: {e}" for i, e in errores]
    return "\n".join(lineas) + "\n"


def seleccionar(casos: list[Caso], ids: list[str] | None, series: list[str] | None) -> list[Caso]:
    """Filtra por id o serie. En ids, `pares` agrega cada variante con su original y `v2` las
    perturbaciones y casos sin respuesta con sus variantes."""
    elegidos = casos
    if series:
        elegidos = [c for c in elegidos if c.serie in series]
    if ids:
        pedidos = {normalizar(i).upper() for i in ids}
        if "PARES" in pedidos:
            variantes = [c for c in casos if c.serie == "V"]
            pedidos |= {c.id for c in variantes} | {
                c.variante_de for c in variantes if c.variante_de
            }
        if "V2" in pedidos:
            # Perturbaciones y casos sin respuesta, con las variantes de las que derivan.
            derivados = [c for c in casos if c.serie in ("P", "U")]
            pedidos |= {c.id for c in derivados} | {
                c.variante_de for c in derivados if c.variante_de
            }
        elegidos = [c for c in elegidos if c.id.upper() in pedidos]
    return elegidos
