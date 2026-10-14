"""Motor de casos: las operaciones del contrato MCP sobre casos persistidos (fase 4).

Cada operación reconstruye el árbol del caso reproduciendo sus eventos, aplica el cambio y
registra el evento nuevo solo si la operación termina bien. Los veredictos se guardan apenas se
obtienen, así que un caso se reconstruye sin volver a llamar al verificador.
"""

import hashlib
import uuid
from collections.abc import Iterator
from contextlib import contextmanager
from dataclasses import dataclass, field
from pathlib import Path

from factory.config import Config, ConfigPesos
from factory.contracts.abduction import HipotesisCandidata, Valor
from factory.contracts.case import EstadoHipotesis, ResultadoEvaluacion, Veredicto
from factory.contracts.observation import (
    EstadoObservacion,
    Observacion,
    Observador,
    RolObservacion,
)
from factory.contracts.rules import ConjuntoReglas
from factory.engine.modelos import (
    Auditoria,
    CodigoError,
    ConsultaDiscriminante,
    Descartada,
    EntradaHipotesis,
    EntradaObservador,
    EntradaRanking,
    ErrorCaso,
    HipotesisAuditada,
    HipotesisRegistrada,
    InfoCaso,
    ObservacionAuditada,
    ObservacionRegistrada,
    RegistroCaso,
    ResultadoEvaluacionCaso,
    ResultadoEvidencia,
    ResultadoHipotesis,
    ResultadoMejorExplicacion,
    ResultadoObservacion,
    ResultadoRetractacion,
    ResultadoSugerencias,
    ResumenHipotesis,
)
from factory.engine.store import CacheSQLite, Store, ahora
from factory.organ.projections import VerificadorProyeccion
from factory.organ.rule_engine import RuleEngine, cargar_reglas, directorio_reglas
from factory.organ.texto import normalizar
from factory.organ.verifier import Verificador, VerificadorLLM
from factory.transition.deterministic.ibe_evaluator import IBEEvaluator
from factory.transition.deterministic.state_tree import ArbolHipotesis
from factory.transition.stochastic.contexto import (
    describir_dominio,
    describir_hipotesis,
    describir_observaciones,
)
from factory.transition.stochastic.cortex import Cortex
from factory.transition.stochastic.esquemas import ConsultasLLM
from factory.transition.stochastic.generator import (
    ContextoGeneracion,
    Generador,
    ModoGeneracion,
)
from factory.transition.stochastic.llm_client import (
    Cache,
    ClienteLLM,
    ErrorLLM,
    PresupuestoAgotado,
    RespuestaInvalida,
    Transporte,
)

SISTEMA_CONSULTAS = """Eres el planificador de observaciones de un sistema de razonamiento \
abductivo. Varias hipótesis incompatibles explican igual de bien la evidencia disponible. \
Propón observaciones nuevas que las distingan: para cada una, quién debería observar, desde qué \
marco (perspectiva, instrumento o método), qué medir y qué resultado predice cada hipótesis. \
Una observación solo sirve si las predicciones difieren entre hipótesis. Prefiere observaciones \
factibles y concretas."""


def _hash_reglas(reglas: ConjuntoReglas) -> str:
    return hashlib.sha256(reglas.model_dump_json().encode()).hexdigest()[:16]


class _SinVerificador:
    """Para operaciones de solo lectura: verificar algo nuevo ahí sería un error de diseño."""

    def verificar(
        self, hipotesis: HipotesisCandidata, observacion: Observacion, observador: Observador
    ) -> Veredicto:
        raise RuntimeError("una operación de solo lectura intentó verificar")


class VerificadorPersistente:
    """Consulta primero los veredictos guardados; los nuevos se guardan al obtenerse."""

    def __init__(self, store: Store, caso_id: str, base: Verificador) -> None:
        self.store = store
        self.caso_id = caso_id
        self.base = base

    def verificar(
        self, hipotesis: HipotesisCandidata, observacion: Observacion, observador: Observador
    ) -> Veredicto:
        guardado = self.store.veredicto(self.caso_id, hipotesis.id_hipotesis, observacion.id)
        if guardado is not None:
            return guardado
        veredicto = self.base.verificar(hipotesis, observacion, observador)
        self.store.guardar_veredicto(self.caso_id, veredicto)
        return veredicto


@dataclass
class _Contexto:
    registro: RegistroCaso
    reglas: ConjuntoReglas
    arbol: ArbolHipotesis
    cliente: ClienteLLM | None
    opiniones: dict[str, list[str]] = field(default_factory=dict)
    grupos_observacion: int = 0
    avisos: list[str] = field(default_factory=list)


class ServicioCasos:
    def __init__(
        self,
        store: Store,
        config: Config,
        *,
        transporte: Transporte | None = None,
        cache: Cache | None = None,
        reglas_dir: Path | None = None,
    ) -> None:
        self.store = store
        self.config = config
        self.transporte = transporte
        self.cache = cache or CacheSQLite(store)
        self.reglas_dir = reglas_dir or directorio_reglas()

    # --- gestión de casos ----------------------------------------------------------------

    def listar_dominios(self) -> list[str]:
        return sorted(p.stem for p in self.reglas_dir.glob("*.yaml"))

    def listar_reglas(self, dominio: str) -> ConjuntoReglas:
        return self._reglas_de_archivo(dominio)

    def crear_caso(
        self, descripcion: str, dominio: str, pesos: ConfigPesos | None = None
    ) -> InfoCaso:
        reglas = self._reglas_de_archivo(dominio)
        numero = self.store.nuevo_numero()
        momento = ahora()
        registro = RegistroCaso(
            id=f"caso_{numero}",
            descripcion=descripcion,
            dominio=reglas.dominio,
            reglas_json=reglas.model_dump_json(),
            hash_reglas=_hash_reglas(reglas),
            pesos=pesos or self.config.pesos,
            sesion=f"abd-mind-{uuid.uuid4()}",
            creado=momento,
            actualizado=momento,
        )
        self.store.crear_caso(registro, numero)
        self.store.agregar_evento(
            registro.id,
            "caso_creado",
            {"descripcion": descripcion, "dominio": dominio, "version_reglas": reglas.version},
        )
        return self._info(registro)

    def listar_casos(self, estado: str | None = None, limite: int = 50) -> list[InfoCaso]:
        return [self._info(r) for r in self.store.listar_casos(estado, limite)]

    def estado_caso(self, caso_id: str) -> InfoCaso:
        return self._info(self._registro(caso_id))

    def cerrar_caso(self, caso_id: str) -> InfoCaso:
        registro = self._registro(caso_id)
        registro.estado = "cerrado"
        registro.actualizado = ahora()
        self.store.agregar_evento(caso_id, "caso_cerrado", {})
        self.store.guardar_caso(registro)
        return self._info(registro)

    # --- observaciones -------------------------------------------------------------------

    def agregar_observacion(
        self,
        caso_id: str,
        observador: EntradaObservador,
        contenido: str,
        *,
        fuente: str | None = None,
        valor: Valor | None = None,
        rol: RolObservacion = RolObservacion.EXPLANANDUM,
    ) -> ResultadoObservacion:
        """Registra lo que reportó un observador.

        Con `valor` el hecho se registra tal cual; si no, el córtex separa hechos de opiniones.
        Los hechos nuevos ponen a prueba a las hipótesis existentes (pueden derrotarlas).
        `rol`: explanandum (exige explicación) o evidencia (solo discrimina), ADR-0011.
        """
        with self._operacion(caso_id) as ctx:
            return self._agregar_observacion(ctx, observador, contenido, fuente, valor, rol)

    def corregir_observacion(
        self,
        caso_id: str,
        id_observacion: str,
        *,
        contenido: str | None = None,
        valor: Valor | None = None,
        es_opinion: bool = False,
    ) -> ResultadoObservacion:
        """Corrige un hecho mal extraído: lo retracta y registra la versión corregida.

        La versión corregida no se usa como prueba (no derrota hipótesis): es el mismo dato.
        Con `es_opinion` el enunciado pasa a ser una opinión del observador.
        """
        with self._operacion(caso_id) as ctx:
            original = ctx.arbol.observaciones.get(id_observacion)
            if original is None or original.estado is not EstadoObservacion.ACTIVA:
                raise ErrorCaso(
                    CodigoError.OBSERVACION_NO_ENCONTRADA,
                    f"no hay un hecho activo '{id_observacion}' en {caso_id}",
                )
            ctx.arbol.retractar_observacion(id_observacion)
            self.store.agregar_evento(
                caso_id, "observacion_retractada", {"id": id_observacion, "motivo": "correccion"}
            )
            texto = contenido or original.contenido
            if es_opinion:
                ctx.opiniones.setdefault(original.observador_id, []).append(texto)
                self.store.agregar_evento(
                    caso_id,
                    "opinion_registrada",
                    {"observador_id": original.observador_id, "contenido": texto},
                )
                return ResultadoObservacion(
                    caso_id=caso_id,
                    observador_id=original.observador_id,
                    hechos=[],
                    opiniones=[texto],
                )
            ctx.grupos_observacion += 1
            corregida = Observacion(
                id=f"o{ctx.grupos_observacion}",
                observador_id=original.observador_id,
                contenido=texto,
                valor=valor if valor is not None else original.valor,
                variables=original.variables,
                rol=original.rol,
            )
            ctx.arbol.agregar_observacion(corregida, como_prueba=False)
            self.store.agregar_evento(
                caso_id,
                "observacion_registrada",
                {
                    "grupo": corregida.id,
                    "observador_id": original.observador_id,
                    "contenido_original": texto,
                    "corrige": id_observacion,
                    "como_prueba": False,
                    "observaciones": [corregida.model_dump(mode="json")],
                    "opiniones": [],
                },
            )
            return ResultadoObservacion(
                caso_id=caso_id,
                observador_id=original.observador_id,
                hechos=[_registrada(corregida)],
                opiniones=[],
            )

    def nueva_evidencia(
        self,
        caso_id: str,
        observador: EntradaObservador,
        contenido: str,
        *,
        fuente: str | None = None,
        valor: Valor | None = None,
        rol: RolObservacion = RolObservacion.EXPLANANDUM,
    ) -> ResultadoEvidencia:
        with self._operacion(caso_id) as ctx:
            anterior = ctx.registro.resumen.h_estrella
            observacion = self._agregar_observacion(ctx, observador, contenido, fuente, valor, rol)
            evaluacion = self._evaluar(ctx, permitir_vacio=True)
            return ResultadoEvidencia(
                observacion=observacion, h_estrella_anterior=anterior, evaluacion=evaluacion
            )

    def retractar_evidencia(self, caso_id: str, id_observacion: str) -> ResultadoRetractacion:
        """Retira un hecho (`o3.h1`) o todos los de una observación (`o3`)."""
        with self._operacion(caso_id) as ctx:
            ids = [
                o.id
                for o in ctx.arbol.observaciones_activas()
                if o.id == id_observacion or o.id.startswith(f"{id_observacion}.")
            ]
            if not ids:
                raise ErrorCaso(
                    CodigoError.OBSERVACION_NO_ENCONTRADA,
                    f"no hay hechos activos '{id_observacion}' en {caso_id}",
                )
            reactivadas: list[str] = []
            for i in ids:
                reactivadas += ctx.arbol.retractar_observacion(i)
                self.store.agregar_evento(caso_id, "observacion_retractada", {"id": i})
            evaluacion = (
                self._evaluar(ctx, permitir_vacio=True)
                if ctx.arbol.observaciones_activas()
                else None
            )
            return ResultadoRetractacion(
                caso_id=caso_id,
                retractadas=ids,
                reactivadas=sorted(set(reactivadas)),
                evaluacion=evaluacion,
            )

    # --- hipótesis -----------------------------------------------------------------------

    def proponer_hipotesis(
        self, caso_id: str, hipotesis: list[EntradaHipotesis], origen: str = "hermes"
    ) -> ResultadoHipotesis:
        with self._operacion(caso_id) as ctx:
            self._exigir_cupo(ctx, len(hipotesis))
            avisos: list[str] = []
            nuevas = []
            for entrada in hipotesis:
                afirmaciones = dict(entrada.afirmaciones)
                if ctx.reglas.variables:
                    for nombre in sorted(set(afirmaciones) - set(ctx.reglas.variables)):
                        del afirmaciones[nombre]
                        avisos.append(f"se ignoró la variable desconocida '{nombre}'")
                h = HipotesisCandidata(
                    id_hipotesis=self._siguiente_id_hipotesis(ctx),
                    mecanismo_latente=entrada.mecanismo,
                    entidades_latentes=entrada.entidades_latentes,
                    afirmaciones=afirmaciones,
                    predicados_de_consistencia=entrada.predicados,
                    observaciones_explicadas=entrada.observaciones_explicadas,
                    origen=origen,
                )
                self._registrar_hipotesis(ctx, h)
                nuevas.append(h)
            return ResultadoHipotesis(
                caso_id=caso_id, hipotesis=[_hipotesis_registrada(h) for h in nuevas], avisos=avisos
            )

    def generar_hipotesis(
        self, caso_id: str, n: int | None = None, modo: str = "auto"
    ) -> ResultadoHipotesis:
        with self._operacion(caso_id) as ctx:
            if not ctx.arbol.observaciones_activas():
                raise ErrorCaso(CodigoError.SIN_OBSERVACIONES, "el caso no tiene observaciones")
            cupo = self._exigir_cupo(ctx, 1)
            n = min(n or self.config.presupuestos.hipotesis_por_ronda, cupo)
            resumen = ctx.registro.resumen
            if modo == "auto":
                vigente = resumen.evaluado_en_evento == self.store.contar_eventos(caso_id)
                expandir = vigente and resumen.expansion_sugerida
                modo_real = ModoGeneracion.EXPANSION if expandir else ModoGeneracion.CONTRASTIVO
            else:
                modo_real = ModoGeneracion(modo)
            assert ctx.cliente is not None
            generacion = Generador(ctx.cliente, self.config.roles.generadores).generar(
                ContextoGeneracion(
                    dominio=ctx.reglas,
                    observadores=ctx.arbol.observadores,
                    observaciones=ctx.arbol.observaciones_activas(),
                    existentes=ctx.arbol.todas_las_hipotesis(),
                    vocabulario=ctx.arbol.vocabulario,
                ),
                n,
                modo_real,
            )
            for h in generacion.hipotesis[:cupo]:
                self._registrar_hipotesis(ctx, h)
            avisos = [f"modo: {modo_real.value}", *generacion.avisos, *ctx.cliente.avisos]
            if len(generacion.hipotesis) > cupo:
                avisos.append(f"se descartaron {len(generacion.hipotesis) - cupo} por el límite")
            return ResultadoHipotesis(
                caso_id=caso_id,
                hipotesis=[_hipotesis_registrada(h) for h in generacion.hipotesis[:cupo]],
                avisos=avisos,
            )

    # --- evaluación ----------------------------------------------------------------------

    def evaluar(self, caso_id: str) -> ResultadoEvaluacionCaso:
        with self._operacion(caso_id) as ctx:
            return self._evaluar(ctx)

    def mejor_explicacion(self, caso_id: str) -> ResultadoMejorExplicacion:
        with self._operacion(caso_id) as ctx:
            evaluacion = self._evaluar(ctx)
            h = evaluacion.h_estrella
            por_id = {r.id_hipotesis: r for r in evaluacion.ranking}
            empatadas = [
                _resumen(ctx.arbol, ctx.arbol.evaluar_registro(i)) for i in evaluacion.empatadas
            ]
            if evaluacion.subdeterminada:
                motivo = (
                    f"subdeterminación: {len(empatadas)} hipótesis explican la evidencia igual de "
                    "bien; usar sugerir_observacion para saber qué observar"
                )
            elif h is not None:
                motivo = (
                    f"explica {h.consiliencia_c} de {evaluacion.m} observaciones, postula "
                    f"{h.parsimonia_p} entidades no verificadas y respeta las reglas del dominio"
                )
            elif not evaluacion.ranking:
                motivo = "ninguna hipótesis viva respeta las reglas del dominio"
            else:
                tau = ctx.registro.pesos.tau
                motivo = f"ninguna hipótesis alcanza el umbral de aceptación τ = {tau}"
            entrada = por_id[h.id_hipotesis] if h is not None else None
            if entrada is not None and entrada.sin_explicar:
                motivo += f"; deja sin explicar {', '.join(entrada.sin_explicar)}"
            residuo = entrada.atribuidas_a_error if entrada is not None else {}
            if residuo:
                motivo += f"; supone que {', '.join(sorted(residuo))} son errores de observación"
            if evaluacion.expansion_sugerida:
                motivo += "; conviene generar hipótesis en modo expansión"
            return ResultadoMejorExplicacion(
                caso_id=caso_id,
                h_estrella=h,
                empatadas=empatadas,
                atribuidas_a_error=residuo,
                motivo=motivo,
            )

    def sugerir_observacion(self, caso_id: str) -> ResultadoSugerencias:
        """Abducción activa (ADR-0010): qué observar para separar hipótesis empatadas."""
        with self._operacion(caso_id) as ctx:
            evaluacion = self._evaluar(ctx)
            if not evaluacion.subdeterminada:
                return ResultadoSugerencias(
                    caso_id=caso_id,
                    empatadas=[],
                    consultas=[],
                    avisos=["no hay hipótesis empatadas: no hace falta discriminar"],
                )
            empatadas = [ctx.arbol.hipotesis(i) for i in evaluacion.empatadas]
            if ctx.reglas.verificador == "proyeccion":
                consultas = self._consultas_por_proyeccion(ctx, empatadas)
            else:
                consultas = self._consultas_por_llm(ctx, empatadas)
            avisos = [] if consultas else ["no se encontró una observación que las separe"]
            return ResultadoSugerencias(
                caso_id=caso_id,
                empatadas=evaluacion.empatadas,
                consultas=sorted(consultas, key=lambda c: -c.clases),
                avisos=avisos,
            )

    # --- auditoría -----------------------------------------------------------------------

    def auditoria(self, caso_id: str) -> Auditoria:
        registro = self._registro(caso_id)
        ctx = self._cargar(registro, cliente=None)
        arbol = ctx.arbol
        return Auditoria(
            caso=self._info(registro),
            observadores=list(arbol.observadores.values()),
            opiniones=ctx.opiniones,
            observaciones=[
                ObservacionAuditada(**_registrada(o).model_dump(), observador_id=o.observador_id)
                for o in arbol.observaciones.values()
            ],
            hipotesis=[
                HipotesisAuditada(
                    id_hipotesis=h.id_hipotesis,
                    mecanismo=h.mecanismo_latente,
                    origen=h.origen,
                    entidades_latentes=h.entidades_latentes,
                    afirmaciones=h.afirmaciones,
                    estado=arbol.estado(h.id_hipotesis),
                    derrotada_por=arbol.derrotada_por(h.id_hipotesis),
                )
                for h in arbol.todas_las_hipotesis()
            ],
            veredictos=self.store.veredictos(caso_id),
            eventos=[
                {"id": e.id, "tipo": e.tipo, "momento": e.momento, **e.datos}
                for e in self.store.eventos(caso_id)
            ],
        )

    # --- interno: carga y operación ------------------------------------------------------

    def _reglas_de_archivo(self, dominio: str) -> ConjuntoReglas:
        try:
            return cargar_reglas(dominio, self.reglas_dir)
        except FileNotFoundError as e:
            disponibles = ", ".join(self.listar_dominios())
            raise ErrorCaso(
                CodigoError.DOMINIO_DESCONOCIDO,
                f"no existe el dominio '{dominio}'; disponibles: {disponibles}",
            ) from e

    def _registro(self, caso_id: str) -> RegistroCaso:
        registro = self.store.obtener_caso(caso_id)
        if registro is None:
            raise ErrorCaso(CodigoError.CASO_NO_ENCONTRADO, f"no existe el caso '{caso_id}'")
        return registro

    def _info(self, registro: RegistroCaso) -> InfoCaso:
        reglas = ConjuntoReglas.model_validate_json(registro.reglas_json)
        avisos = []
        try:
            actuales = cargar_reglas(registro.dominio, self.reglas_dir)
            if _hash_reglas(actuales) != registro.hash_reglas:
                avisos.append(
                    "las reglas del dominio cambiaron desde que se creó el caso; "
                    f"el caso sigue usando la versión {reglas.version}"
                )
        except FileNotFoundError:
            avisos.append("el archivo de reglas del dominio ya no existe")
        return InfoCaso(
            caso_id=registro.id,
            descripcion=registro.descripcion,
            dominio=registro.dominio,
            version_reglas=reglas.version,
            pesos=registro.pesos,
            estado=registro.estado,
            llamadas=registro.llamadas,
            resumen=registro.resumen,
            evaluacion_vigente=registro.resumen.evaluado_en_evento
            == self.store.contar_eventos(registro.id),
            actualizado=registro.actualizado,
            avisos=avisos,
        )

    def _nuevo_cliente(self, registro: RegistroCaso) -> ClienteLLM:
        presupuestos = self.config.presupuestos
        restantes = presupuestos.llamadas_por_caso - registro.llamadas
        if restantes <= 0:
            raise ErrorCaso(
                CodigoError.PRESUPUESTO_CASO_AGOTADO,
                f"el caso agotó su presupuesto de {presupuestos.llamadas_por_caso} llamadas",
            )
        return ClienteLLM(
            self.config,
            self.transporte,
            self.cache,
            sesion=registro.sesion,
            max_llamadas=min(presupuestos.llamadas_por_operacion, restantes),
        )

    def _cargar(self, registro: RegistroCaso, cliente: ClienteLLM | None) -> _Contexto:
        reglas = ConjuntoReglas.model_validate_json(registro.reglas_json)
        pesos = registro.pesos
        evaluador = IBEEvaluator(
            pesos.alpha,
            pesos.beta,
            pesos.gamma,
            pesos.tau,
            RuleEngine(reglas),
            lambda_residuo=pesos.lambda_residuo,
        )
        base: Verificador
        if reglas.verificador == "proyeccion":
            base = VerificadorProyeccion()
        elif cliente is not None:
            base = VerificadorLLM(cliente, self.config.roles.verificador)
        else:
            base = _SinVerificador()
        arbol = ArbolHipotesis(
            evaluador,
            VerificadorPersistente(self.store, registro.id, base),
            set(reglas.vocabulario),
            omega_derrota=pesos.omega_derrota,
            delta_empate=pesos.delta_empate,
        )
        ctx = _Contexto(registro=registro, reglas=reglas, arbol=arbol, cliente=cliente)

        for evento in self.store.eventos(registro.id):
            datos = evento.datos
            if evento.tipo == "observador_registrado":
                arbol.agregar_observador(Observador.model_validate(datos["observador"]))
            elif evento.tipo == "observacion_registrada":
                ctx.grupos_observacion += 1
                for o in datos["observaciones"]:
                    arbol.agregar_observacion(
                        Observacion.model_validate(o), como_prueba=datos.get("como_prueba", True)
                    )
                ctx.opiniones.setdefault(datos["observador_id"], []).extend(datos["opiniones"])
            elif evento.tipo == "opinion_registrada":
                ctx.opiniones.setdefault(datos["observador_id"], []).append(datos["contenido"])
            elif evento.tipo == "hipotesis_registrada":
                arbol.agregar_hipotesis(HipotesisCandidata.model_validate(datos["hipotesis"]))
            elif evento.tipo == "observacion_retractada":
                arbol.retractar_observacion(datos["id"])
        return ctx

    @contextmanager
    def _operacion(self, caso_id: str) -> Iterator[_Contexto]:
        registro = self._registro(caso_id)
        if registro.estado == "cerrado":
            raise ErrorCaso(CodigoError.CASO_CERRADO, f"el caso '{caso_id}' está cerrado")
        cliente = self._nuevo_cliente(registro)
        ctx = self._cargar(registro, cliente)
        try:
            yield ctx
        except PresupuestoAgotado as e:
            raise ErrorCaso(CodigoError.PRESUPUESTO_CASO_AGOTADO, str(e)) from e
        except RespuestaInvalida as e:
            raise ErrorCaso(CodigoError.RESPUESTA_LLM_INVALIDA, str(e)) from e
        except ErrorLLM as e:
            raise ErrorCaso(CodigoError.PROVEEDOR_LLM_NO_DISPONIBLE, str(e)) from e
        finally:
            # Las llamadas se cobran aunque la operación falle.
            registro.llamadas += cliente.uso.llamadas
            arbol = ctx.arbol
            todas = arbol.todas_las_hipotesis()
            vivas = [h for h in todas if arbol.estado(h.id_hipotesis) is EstadoHipotesis.VIVA]
            registro.resumen.n_observaciones = len(arbol.observaciones_activas())
            registro.resumen.n_hipotesis_vivas = len(vivas)
            registro.resumen.n_hipotesis_derrotadas = len(todas) - len(vivas)
            registro.actualizado = ahora()
            self.store.guardar_caso(registro)

    # --- interno: pasos ------------------------------------------------------------------

    def _registrar_observador(self, ctx: _Contexto, entrada: EntradaObservador) -> Observador:
        observador_id = normalizar(entrada.nombre)
        existente = ctx.arbol.observadores.get(observador_id)
        if existente is not None:
            return existente
        observador = Observador(
            id=observador_id,
            nombre=entrada.nombre,
            marco=entrada.marco,
            parametros=entrada.parametros,
            tolerancia=entrada.tolerancia,
            confiabilidad=entrada.confiabilidad or ctx.reglas.confiabilidad_por_defecto,
        )
        ctx.arbol.agregar_observador(observador)
        self.store.agregar_evento(
            ctx.registro.id,
            "observador_registrado",
            {"observador": observador.model_dump(mode="json")},
        )
        return observador

    def _agregar_observacion(
        self,
        ctx: _Contexto,
        entrada: EntradaObservador,
        contenido: str,
        fuente: str | None,
        valor: Valor | None,
        rol: RolObservacion = RolObservacion.EXPLANANDUM,
    ) -> ResultadoObservacion:
        observador = self._registrar_observador(ctx, entrada)
        grupo = f"o{ctx.grupos_observacion + 1}"
        avisos: list[str] = []
        if valor is not None:
            hechos = [
                Observacion(
                    id=grupo,
                    observador_id=observador.id,
                    contenido=contenido,
                    valor=valor,
                    rol=rol,
                )
            ]
            opiniones: list[str] = []
        else:
            assert ctx.cliente is not None
            extraccion = Cortex(ctx.cliente, self.config.roles.cortex).extraer(
                observador, contenido, ctx.reglas
            )
            hechos = extraccion.a_observaciones(observador.id, grupo, rol)
            opiniones = extraccion.opiniones
            avisos += [f"duda: {d}" for d in extraccion.dudas]
            if not hechos:
                avisos.append("no se extrajo ningún hecho; nada se agregó como evidencia")

        derrotadas: list[str] = []
        en_tension: list[str] = []
        for hecho in hechos:
            derrotadas += ctx.arbol.agregar_observacion(hecho)
            en_tension += ctx.arbol.en_tension(hecho.id)
        ctx.grupos_observacion += 1
        ctx.opiniones.setdefault(observador.id, []).extend(opiniones)
        self.store.agregar_evento(
            ctx.registro.id,
            "observacion_registrada",
            {
                "grupo": grupo,
                "observador_id": observador.id,
                "contenido_original": contenido,
                "fuente": fuente,
                "observaciones": [h.model_dump(mode="json") for h in hechos],
                "opiniones": opiniones,
            },
        )
        if ctx.cliente is not None:
            avisos += ctx.cliente.avisos
        return ResultadoObservacion(
            caso_id=ctx.registro.id,
            observador_id=observador.id,
            hechos=[_registrada(h) for h in hechos],
            opiniones=opiniones,
            derrotadas=sorted(set(derrotadas)),
            en_tension=sorted(set(en_tension)),
            avisos=avisos,
        )

    def _consultas_por_proyeccion(
        self, ctx: _Contexto, empatadas: list[HipotesisCandidata]
    ) -> list[ConsultaDiscriminante]:
        proyector = VerificadorProyeccion()
        consultas = []
        for marco in ctx.reglas.marcos_posibles:
            observador = Observador(
                id=normalizar(marco.nombre), nombre=marco.nombre, parametros=marco.parametros
            )
            predicciones = {
                h.id_hipotesis: str(proyector.proyeccion(h, observador) or "desconocido")
                for h in empatadas
            }
            clases = len({normalizar(p) for p in predicciones.values()})
            if clases >= 2:
                consultas.append(
                    ConsultaDiscriminante(
                        observador_sugerido=marco.nombre,
                        marco=marco.marco,
                        parametros=marco.parametros,
                        que_observar="silueta del objeto",
                        predicciones=predicciones,
                        clases=clases,
                    )
                )
        return consultas

    def _consultas_por_llm(
        self, ctx: _Contexto, empatadas: list[HipotesisCandidata]
    ) -> list[ConsultaDiscriminante]:
        assert ctx.cliente is not None
        usuario = "\n\n".join(
            [
                describir_dominio(ctx.reglas),
                describir_observaciones(ctx.arbol.observadores, ctx.arbol.observaciones_activas()),
                "Hipótesis empatadas (explican la evidencia igual de bien):\n"
                + "\n".join(describir_hipotesis(h) for h in empatadas),
                "Propón hasta 3 observaciones nuevas (quién debería observar, desde qué marco y "
                "qué medir) cuyo resultado sería distinto según cuál hipótesis es cierta. Para "
                "cada una, da la predicción de cada hipótesis por su id.",
            ]
        )
        bruto = ctx.cliente.completar_json(
            self.config.roles.generadores[0], SISTEMA_CONSULTAS, usuario, ConsultasLLM
        )
        ids = {h.id_hipotesis for h in empatadas}
        consultas = []
        for c in bruto.consultas:
            predicciones = {
                p.id_hipotesis: p.prediccion for p in c.predicciones if p.id_hipotesis in ids
            }
            clases = len({normalizar(p) for p in predicciones.values()})
            # Solo sirven las que dan una predicción por hipótesis y separan al menos dos.
            if set(predicciones) == ids and clases >= 2:
                consultas.append(
                    ConsultaDiscriminante(
                        observador_sugerido=c.observador_sugerido,
                        marco=c.marco,
                        que_observar=c.que_observar,
                        predicciones=predicciones,
                        clases=clases,
                    )
                )
        return consultas

    def _siguiente_id_hipotesis(self, ctx: _Contexto) -> str:
        existentes = {h.id_hipotesis for h in ctx.arbol.todas_las_hipotesis()}
        n = len(existentes) + 1
        while f"h{n}" in existentes:
            n += 1
        return f"h{n}"

    def _registrar_hipotesis(self, ctx: _Contexto, h: HipotesisCandidata) -> None:
        ctx.arbol.agregar_hipotesis(h)
        self.store.agregar_evento(
            ctx.registro.id, "hipotesis_registrada", {"hipotesis": h.model_dump(mode="json")}
        )

    def _exigir_cupo(self, ctx: _Contexto, pedidas: int) -> int:
        maximo = self.config.presupuestos.hipotesis_vivas_max
        vivas = sum(
            1
            for h in ctx.arbol.todas_las_hipotesis()
            if ctx.arbol.estado(h.id_hipotesis) is EstadoHipotesis.VIVA
        )
        cupo = maximo - vivas
        if cupo < pedidas:
            raise ErrorCaso(
                CodigoError.LIMITE_HIPOTESIS,
                f"el caso tiene {vivas} hipótesis vivas y el máximo es {maximo}",
            )
        return cupo

    def _evaluar(self, ctx: _Contexto, permitir_vacio: bool = False) -> ResultadoEvaluacionCaso:
        arbol = ctx.arbol
        if not permitir_vacio:
            if not arbol.observaciones_activas():
                raise ErrorCaso(CodigoError.SIN_OBSERVACIONES, "el caso no tiene observaciones")
            if not any(
                arbol.estado(h.id_hipotesis) is EstadoHipotesis.VIVA
                for h in arbol.todas_las_hipotesis()
            ):
                raise ErrorCaso(CodigoError.SIN_HIPOTESIS, "el caso no tiene hipótesis vivas")

        resultado = arbol.evaluar()
        ranking = [self._entrada_ranking(ctx, r) for r in resultado.ranking if not r.violaciones]
        descartadas = [
            Descartada(
                id_hipotesis=r.evaluacion.id_hipotesis,
                mecanismo=arbol.hipotesis(r.evaluacion.id_hipotesis).mecanismo_latente,
                reglas=r.violaciones,
            )
            for r in resultado.ranking
            if r.violaciones
        ]
        h_estrella = (
            _resumen(arbol, resultado.h_estrella) if resultado.h_estrella is not None else None
        )
        resumen = ctx.registro.resumen
        resumen.h_estrella = h_estrella
        resumen.expansion_sugerida = resultado.expansion_sugerida
        resumen.subdeterminada = resultado.subdeterminada
        resumen.empatadas = resultado.empatadas
        resumen.evaluado_en_evento = self.store.contar_eventos(ctx.registro.id)
        avisos = list(ctx.cliente.avisos) if ctx.cliente else []
        if resultado.expansion_sugerida:
            avisos.append(
                "lo que la mejor hipótesis deja sin explicar cuesta más que postular una entidad "
                "nueva: conviene generar hipótesis en modo expansión"
            )
        if resultado.subdeterminada:
            avisos.append(
                f"{len(resultado.empatadas)} hipótesis empatan ({', '.join(resultado.empatadas)}): "
                "no hay una mejor explicación; sugerir_observacion propone cómo distinguirlas"
            )
        return ResultadoEvaluacionCaso(
            caso_id=ctx.registro.id,
            m=resultado.m,
            ranking=ranking,
            descartadas_por_reglas=descartadas,
            h_estrella=h_estrella,
            expansion_sugerida=resultado.expansion_sugerida,
            subdeterminada=resultado.subdeterminada,
            empatadas=resultado.empatadas,
            avisos=avisos,
        )

    @staticmethod
    def _entrada_ranking(ctx: _Contexto, r: ResultadoEvaluacion) -> EntradaRanking:
        e = r.evaluacion
        h = ctx.arbol.hipotesis(e.id_hipotesis)
        return EntradaRanking(
            id_hipotesis=e.id_hipotesis,
            mecanismo=h.mecanismo_latente,
            origen=h.origen,
            consiliencia_c=e.consiliencia_c,
            parsimonia_p=e.parsimonia_p,
            coherencia_k=e.coherencia_k,
            score_final=e.score_final,
            atribuidas_a_error=r.atribuidas_a_error,
            sin_explicar=r.sin_explicar,
            veredictos=r.veredictos,
            declaradas_no_verificadas=r.declaradas_no_verificadas,
        )


def _registrada(o: Observacion) -> ObservacionRegistrada:
    return ObservacionRegistrada(
        id=o.id,
        contenido=o.contenido,
        valor=o.valor,
        variables=o.variables,
        estado=o.estado,
        rol=o.rol,
    )


def _hipotesis_registrada(h: HipotesisCandidata) -> HipotesisRegistrada:
    return HipotesisRegistrada(
        id_hipotesis=h.id_hipotesis,
        mecanismo=h.mecanismo_latente,
        entidades_latentes=h.entidades_latentes,
        afirmaciones=h.afirmaciones,
        origen=h.origen,
    )


def _resumen(arbol: ArbolHipotesis, r: ResultadoEvaluacion) -> ResumenHipotesis:
    e = r.evaluacion
    return ResumenHipotesis(
        id_hipotesis=e.id_hipotesis,
        mecanismo=arbol.hipotesis(e.id_hipotesis).mecanismo_latente,
        consiliencia_c=e.consiliencia_c,
        parsimonia_p=e.parsimonia_p,
        coherencia_k=e.coherencia_k,
        score_final=e.score_final,
    )
