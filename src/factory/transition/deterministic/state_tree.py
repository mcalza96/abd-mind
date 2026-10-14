"""Árbol de hipótesis: consiliencia verificada, parsimonia contra vocabulario y derrotabilidad.

Implementa docs/marco-teorico/03 §3.5–3.6 y las decisiones D1, D2 y D6:
- C se cuenta con veredictos de un verificador, no con lo que declara la hipótesis.
- P cuenta las entidades latentes que no están en el vocabulario verificado V.
- Una observación que llega cuando ya hay hipótesis es una prueba: toda hipótesis que no la
  explica queda derrotada. Retractar esa observación reactiva a las que derrotó solo ella.
"""

from dataclasses import dataclass, field

from pydantic import BaseModel, Field

from factory.contracts.abduction import HipotesisCandidata
from factory.contracts.case import EstadoHipotesis, ResultadoEvaluacion, Veredicto
from factory.contracts.observation import EstadoObservacion, Observacion, Observador
from factory.organ.texto import normalizar
from factory.organ.verifier import Verificador
from factory.transition.deterministic.ibe_evaluator import IBEEvaluator, clave_ranking


class ResultadoArbol(BaseModel):
    m: int = Field(description="Número de observaciones activas")
    ranking: list[ResultadoEvaluacion]
    h_estrella: ResultadoEvaluacion | None
    expansion_sugerida: bool = Field(
        description="Ninguna hipótesis viva y coherente explica las m observaciones (§3.5)"
    )


@dataclass
class _Registro:
    hipotesis: HipotesisCandidata
    derrotada_por: set[str] = field(default_factory=set)

    @property
    def estado(self) -> EstadoHipotesis:
        return EstadoHipotesis.DERROTADA if self.derrotada_por else EstadoHipotesis.VIVA


class ArbolHipotesis:
    def __init__(
        self,
        evaluador: IBEEvaluator,
        verificador: Verificador,
        vocabulario: set[str] | None = None,
    ) -> None:
        self.evaluador = evaluador
        self.verificador = verificador
        self.vocabulario = {normalizar(v) for v in vocabulario or set()}
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

    def agregar_observacion(self, observacion: Observacion) -> list[str]:
        """Registra y_k y la usa como prueba de las hipótesis existentes.

        Devuelve los ids de las hipótesis vivas que quedaron derrotadas.
        """
        if observacion.id in self.observaciones:
            raise ValueError(f"la observación '{observacion.id}' ya existe")
        if observacion.observador_id not in self.observadores:
            raise ValueError(f"el observador '{observacion.observador_id}' no está registrado")
        self.observaciones[observacion.id] = observacion
        if observacion.estado is not EstadoObservacion.ACTIVA:
            return []

        derrotadas = []
        for registro in self._hipotesis.values():
            if self._veredicto(registro.hipotesis, observacion).explica:
                continue
            if registro.estado is EstadoHipotesis.VIVA:
                derrotadas.append(registro.hipotesis.id_hipotesis)
            registro.derrotada_por.add(observacion.id)
        return derrotadas

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
            if id_observacion in registro.derrotada_por:
                registro.derrotada_por.discard(id_observacion)
                if registro.estado is EstadoHipotesis.VIVA:
                    reactivadas.append(registro.hipotesis.id_hipotesis)
        return reactivadas

    def verificar_entidad(self, entidad: str) -> None:
        """Promueve una entidad latente al vocabulario verificado: deja de contar en P."""
        self.vocabulario.add(normalizar(entidad))

    # --- consulta -------------------------------------------------------------------------

    def estado(self, id_hipotesis: str) -> EstadoHipotesis:
        return self._hipotesis[id_hipotesis].estado

    def observaciones_activas(self) -> list[Observacion]:
        return [o for o in self.observaciones.values() if o.estado is EstadoObservacion.ACTIVA]

    def parsimonia(self, hipotesis: HipotesisCandidata) -> int:
        no_verificadas = {normalizar(e) for e in hipotesis.entidades_latentes} - self.vocabulario
        return len(no_verificadas)

    def evaluar_registro(self, id_hipotesis: str) -> ResultadoEvaluacion:
        registro = self._hipotesis[id_hipotesis]
        h = registro.hipotesis
        veredictos = [self._veredicto(h, o) for o in self.observaciones_activas()]
        explicadas = {v.id_observacion for v in veredictos if v.explica}
        evaluacion, coherencia = self.evaluador.evaluar_con_detalle(
            h, consiliencia=len(explicadas), parsimonia=self.parsimonia(h)
        )
        return ResultadoEvaluacion(
            evaluacion=evaluacion,
            estado=registro.estado,
            derrotada_por=sorted(registro.derrotada_por),
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
        mejor = self.evaluador.seleccionar(r.evaluacion for r in ranking)
        h_estrella = next(
            (r for r in ranking if mejor and r.evaluacion.id_hipotesis == mejor.id_hipotesis),
            None,
        )
        completa = any(r.evaluacion.consiliencia_c == m and not r.violaciones for r in ranking)
        return ResultadoArbol(
            m=m, ranking=ranking, h_estrella=h_estrella, expansion_sugerida=m > 0 and not completa
        )

    # --- interno --------------------------------------------------------------------------

    def _veredicto(self, hipotesis: HipotesisCandidata, observacion: Observacion) -> Veredicto:
        clave = (hipotesis.id_hipotesis, observacion.id)
        if clave not in self._veredictos:
            observador = self.observadores[observacion.observador_id]
            self._veredictos[clave] = self.verificador.verificar(hipotesis, observacion, observador)
        return self._veredictos[clave]
