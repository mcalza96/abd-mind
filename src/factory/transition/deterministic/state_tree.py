"""Árbol de hipótesis: consiliencia verificada, parsimonia contra vocabulario y derrotabilidad.

Implementa docs/marco-teorico/03 §3.5–3.6 y las decisiones D1, D2 y D6:
- C se cuenta con veredictos de un verificador, no con lo que declara la hipótesis.
- P cuenta las entidades (declaradas o afirmadas en variables de tipo entidad) que no están en
  el vocabulario verificado V.
- Una observación que llega cuando ya hay hipótesis es una prueba: toda hipótesis que no la
  explica queda derrotada. Retractar esa observación reactiva a las que derrotó solo ella.

Con observadores falibles (09 §9.1–9.2, ADR-0009 y ADR-0010):
- Solo derrota una observación con confiabilidad ω ≥ ω_d; las demás dejan la hipótesis en
  tensión y entran en su residuo.
- El score pondera lo explicado por ω y cobra c(ω) por cada hecho no explicado.
- La expansión se sugiere si el residuo de la mejor hipótesis cuesta más que una entidad nueva.
- Si varias hipótesis empatan (diferencia ≤ δ) no hay H*: el caso está subdeterminado.
"""

from dataclasses import dataclass, field

from pydantic import BaseModel, Field

from factory.contracts.abduction import HipotesisCandidata
from factory.contracts.case import EstadoHipotesis, ResultadoEvaluacion, Veredicto
from factory.contracts.observation import EstadoObservacion, Observacion, Observador
from factory.organ.texto import normalizar
from factory.organ.verifier import Verificador
from factory.transition.deterministic.ibe_evaluator import (
    IBEEvaluator,
    clave_ranking,
    costo_error,
)


class ResultadoArbol(BaseModel):
    m: int = Field(description="Número de observaciones activas")
    ranking: list[ResultadoEvaluacion]
    h_estrella: ResultadoEvaluacion | None
    expansion_sugerida: bool = Field(
        description="El residuo de la mejor hipótesis coherente cuesta más que una entidad nueva"
    )
    subdeterminada: bool = Field(
        default=False, description="Varias hipótesis empatan: no se elige ninguna (ADR-0010)"
    )
    empatadas: list[str] = Field(default_factory=list)


@dataclass
class _Registro:
    hipotesis: HipotesisCandidata
    derrotada_por: set[str] = field(default_factory=set)
    en_tension_por: set[str] = field(default_factory=set)

    @property
    def estado(self) -> EstadoHipotesis:
        return EstadoHipotesis.DERROTADA if self.derrotada_por else EstadoHipotesis.VIVA


class ArbolHipotesis:
    def __init__(
        self,
        evaluador: IBEEvaluator,
        verificador: Verificador,
        vocabulario: set[str] | None = None,
        *,
        omega_derrota: float = 0.95,
        delta_empate: float = 1e-6,
    ) -> None:
        self.evaluador = evaluador
        self.verificador = verificador
        if vocabulario is None:
            vocabulario = set(evaluador.rule_engine.reglas.vocabulario)
        self.vocabulario = {normalizar(v) for v in vocabulario}
        self.omega_derrota = omega_derrota
        self.delta_empate = delta_empate
        self.observadores: dict[str, Observador] = {}
        self.observaciones: dict[str, Observacion] = {}
        self._hipotesis: dict[str, _Registro] = {}
        self._veredictos: dict[tuple[str, str], Veredicto] = {}

    # --- registro -------------------------------------------------------------------------

    def agregar_observador(self, observador: Observador) -> None:
        if observador.id in self.observadores:
            raise ValueError(f"el observador '{observador.id}' ya existe")
        self.observadores[observador.id] = observador

    def agregar_hipotesis(self, hipotesis: HipotesisCandidata) -> None:
        if hipotesis.id_hipotesis in self._hipotesis:
            raise ValueError(f"la hipótesis '{hipotesis.id_hipotesis}' ya existe")
        self._hipotesis[hipotesis.id_hipotesis] = _Registro(hipotesis)

    def agregar_observacion(self, observacion: Observacion, como_prueba: bool = True) -> list[str]:
        """Registra y_k y la usa como prueba de las hipótesis existentes.

        Devuelve los ids de las hipótesis vivas que quedaron derrotadas. Si el observador no
        alcanza ω_d, las que no explican y_k quedan en tensión (ver `en_tension`). Con
        `como_prueba=False` (p. ej. al corregir un hecho mal transcrito) solo se registra.
        """
        if observacion.id in self.observaciones:
            raise ValueError(f"la observación '{observacion.id}' ya existe")
        if observacion.observador_id not in self.observadores:
            raise ValueError(f"el observador '{observacion.observador_id}' no está registrado")
        self.observaciones[observacion.id] = observacion
        if observacion.estado is not EstadoObservacion.ACTIVA or not como_prueba:
            return []

        derrota = self.confiabilidad(observacion) >= self.omega_derrota
        derrotadas = []
        for registro in self._hipotesis.values():
            if self._veredicto(registro.hipotesis, observacion).explica:
                continue
            if not derrota:
                registro.en_tension_por.add(observacion.id)
                continue
            if registro.estado is EstadoHipotesis.VIVA:
                derrotadas.append(registro.hipotesis.id_hipotesis)
            registro.derrotada_por.add(observacion.id)
        return derrotadas

    def en_tension(self, id_observacion: str) -> list[str]:
        """Hipótesis que no explican la observación pero no quedaron derrotadas por ella."""
        return [i for i, r in self._hipotesis.items() if id_observacion in r.en_tension_por]

    def retractar_observacion(self, id_observacion: str) -> list[str]:
        """Retira y_k. Devuelve los ids de las hipótesis que vuelven a estar vivas."""
        observacion = self.observaciones.get(id_observacion)
        if observacion is None:
            raise KeyError(f"la observación '{id_observacion}' no existe")
        if observacion.estado is EstadoObservacion.RETRACTADA:
            return []
        self.observaciones[id_observacion] = observacion.model_copy(
            update={"estado": EstadoObservacion.RETRACTADA}
        )
        reactivadas = []
        for registro in self._hipotesis.values():
            registro.en_tension_por.discard(id_observacion)
            if id_observacion in registro.derrotada_por:
                registro.derrotada_por.discard(id_observacion)
                if registro.estado is EstadoHipotesis.VIVA:
                    reactivadas.append(registro.hipotesis.id_hipotesis)
        return reactivadas

    def verificar_entidad(self, entidad: str) -> None:
        """Promueve una entidad latente al vocabulario verificado: deja de contar en P."""
        self.vocabulario.add(normalizar(entidad))

    # --- consulta -------------------------------------------------------------------------

    def hipotesis(self, id_hipotesis: str) -> HipotesisCandidata:
        return self._hipotesis[id_hipotesis].hipotesis

    def todas_las_hipotesis(self) -> list[HipotesisCandidata]:
        return [r.hipotesis for r in self._hipotesis.values()]

    def estado(self, id_hipotesis: str) -> EstadoHipotesis:
        return self._hipotesis[id_hipotesis].estado

    def derrotada_por(self, id_hipotesis: str) -> list[str]:
        return sorted(self._hipotesis[id_hipotesis].derrotada_por)

    def confiabilidad(self, observacion: Observacion) -> float:
        """ω de un hecho: la suya si la declara; si no, la de su observador."""
        if observacion.confiabilidad is not None:
            return observacion.confiabilidad
        return self.observadores[observacion.observador_id].confiabilidad

    def observaciones_activas(self) -> list[Observacion]:
        return [o for o in self.observaciones.values() if o.estado is EstadoObservacion.ACTIVA]

    def entidades(self, hipotesis: HipotesisCandidata) -> set[str]:
        """Entidades que usa H: las declaradas y los valores de variables de tipo entidad."""
        variables_entidad = self.evaluador.rule_engine.reglas.variables_entidad()
        afirmadas = {
            v
            for k, v in hipotesis.afirmaciones.items()
            if k in variables_entidad and isinstance(v, str)
        }
        return {normalizar(e) for e in [*hipotesis.entidades_latentes, *afirmadas]}

    def parsimonia(self, hipotesis: HipotesisCandidata) -> int:
        """P: entidades de H que no están en el vocabulario verificado (D2).

        Las entidades afirmadas en variables de tipo entidad cuentan aunque el generador no las
        declare como latentes.
        """
        return len(self.entidades(hipotesis) - self.vocabulario)

    def evaluar_registro(self, id_hipotesis: str) -> ResultadoEvaluacion:
        registro = self._hipotesis[id_hipotesis]
        h = registro.hipotesis
        activas = self.observaciones_activas()
        veredictos = [self._veredicto(h, o) for o in activas]
        explicadas = {v.id_observacion for v in veredictos if v.explica}
        residuo = {
            o.id: costo_error(self.confiabilidad(o)) for o in activas if o.id not in explicadas
        }
        evaluacion, coherencia = self.evaluador.evaluar_con_detalle(
            h,
            consiliencia=len(explicadas),
            parsimonia=self.parsimonia(h),
            consiliencia_ponderada=sum(
                self.confiabilidad(o) for o in activas if o.id in explicadas
            ),
            residuo=sum(residuo.values()),
        )
        return ResultadoEvaluacion(
            evaluacion=evaluacion,
            estado=registro.estado,
            derrotada_por=sorted(registro.derrotada_por),
            en_tension_por=sorted(registro.en_tension_por),
            atribuidas_a_error=residuo,
            veredictos=veredictos,
            violaciones=coherencia.violaciones,
            declaradas_no_verificadas=sorted(
                {i for i in h.observaciones_explicadas if i in self.observaciones} - explicadas
            ),
        )

    def evaluar_todas(self) -> list[ResultadoEvaluacion]:
        """Evaluación de todas las hipótesis, vivas y derrotadas, en orden de ranking."""
        return sorted(
            (self.evaluar_registro(i) for i in self._hipotesis),
            key=lambda r: clave_ranking(r.evaluacion),
        )

    def evaluar(self) -> ResultadoArbol:
        """Ranking de las hipótesis vivas, H* y si corresponde ampliar la ontología."""
        m = len(self.observaciones_activas())
        ranking = sorted(
            (
                self.evaluar_registro(i)
                for i, r in self._hipotesis.items()
                if r.estado is EstadoHipotesis.VIVA
            ),
            key=lambda r: clave_ranking(r.evaluacion),
        )
        coherentes = [r for r in ranking if not r.violaciones]

        # Empate (ADR-0010): todas las coherentes a menos de δ del mejor score.
        empatadas: list[str] = []
        h_estrella = None
        if coherentes:
            mejor = coherentes[0].evaluacion.score_final
            tau = self.evaluador.tau
            if tau is None or mejor >= tau:
                empatadas = [
                    r.evaluacion.id_hipotesis
                    for r in coherentes
                    if r.evaluacion.score_final >= mejor - self.delta_empate
                ]
                if len(empatadas) == 1:
                    h_estrella = coherentes[0]
                    empatadas = []

        # Expansión (09 §9.1.7): ¿el residuo de la mejor coherente cuesta más que una entidad?
        perdida_minima = min((self._perdida_residuo(r) for r in coherentes), default=float("inf"))
        return ResultadoArbol(
            m=m,
            ranking=ranking,
            h_estrella=h_estrella,
            expansion_sugerida=m > 0 and perdida_minima > self.evaluador.gamma,
            subdeterminada=bool(empatadas),
            empatadas=empatadas,
        )

    # --- interno --------------------------------------------------------------------------

    def _perdida_residuo(self, r: ResultadoEvaluacion) -> float:
        """L(H) = Σ_{j∈R(H)} (α·ω_j + λ·c(ω_j)): lo que se gana si se explicara el residuo."""
        return sum(
            self.evaluador.alpha * self.confiabilidad(self.observaciones[j])
            + self.evaluador.lambda_residuo * costo
            for j, costo in r.atribuidas_a_error.items()
        )

    def _veredicto(self, hipotesis: HipotesisCandidata, observacion: Observacion) -> Veredicto:
        clave = (hipotesis.id_hipotesis, observacion.id)
        if clave not in self._veredictos:
            observador = self.observadores[observacion.observador_id]
            self._veredictos[clave] = self.verificador.verificar(hipotesis, observacion, observador)
        return self._veredictos[clave]
