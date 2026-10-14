"""Respuesta contrastiva y margen en veredictos (11 §11.3–11.4, ADR-0012). Sin IA.

La respuesta se decide entre clases de hipótesis: los valores de la pregunta del caso o, sin
pregunta, cada hipótesis por sí sola. El margen cuenta cuántos veredictos de LLM habría que
cambiar para que otra clase alcance a la ganadora; los veredictos por proyección no cuentan,
porque son deterministas.
"""

import math
from collections.abc import Callable, Mapping

from factory.contracts.case import (
    Pregunta,
    Relacion,
    Respuesta,
    ResultadoEvaluacion,
    Veredicto,
)
from factory.contracts.observation import Observacion
from factory.organ.texto import normalizar
from factory.transition.deterministic.ibe_evaluator import IBEEvaluator, costo_error


def es_juicio(v: Veredicto) -> bool:
    """Un veredicto que podría estar equivocado: lo emitió un modelo, no una proyección."""
    return v.fuente.startswith("verificador:")


def clase_de(afirmaciones: Mapping[str, object], pregunta: Pregunta) -> str | None:
    """Valor de la pregunta que afirma una hipótesis, con la grafía declarada; o None."""
    afirmado = afirmaciones.get(pregunta.variable)
    if afirmado is None:
        return None
    por_normal = {normalizar(v): v for v in pregunta.valores}
    return por_normal.get(normalizar(str(afirmado)))


class CalculoRespuesta:
    def __init__(
        self,
        evaluador: IBEEvaluator,
        observacion: Callable[[str], Observacion],
        confiabilidad: Callable[[Observacion], float],
        *,
        delta: float,
        veredictos_fragil: int,
    ) -> None:
        self.evaluador = evaluador
        self.observacion = observacion
        self.confiabilidad = confiabilidad
        self.delta = delta
        self.veredictos_fragil = veredictos_fragil

    def responder(
        self,
        coherentes: list[ResultadoEvaluacion],
        clases: dict[str, str | None],
    ) -> Respuesta | None:
        """`coherentes` en orden de ranking; `clases`: id de hipótesis → clase (None: no fija)."""
        if not coherentes:
            return None
        por_clase: dict[str, list[ResultadoEvaluacion]] = {}
        for r in coherentes:
            clase = clases.get(r.evaluacion.id_hipotesis)
            if clase is not None:
                por_clase.setdefault(clase, []).append(r)
        sin_responder = [
            r.evaluacion.id_hipotesis
            for r in coherentes
            if clases.get(r.evaluacion.id_hipotesis) is None
        ]
        scores = {c: rs[0].evaluacion.score_final for c, rs in por_clase.items()}
        orden = sorted(por_clase, key=lambda c: (-scores[c], c))
        if not orden:
            return Respuesta(valor=None, determinada=False, sin_responder=sin_responder)

        mejor = scores[orden[0]]
        tau = self.evaluador.tau
        if tau is not None and mejor < tau:
            return Respuesta(
                valor=None, determinada=False, scores_por_valor=scores, sin_responder=sin_responder
            )
        en_disputa = [c for c in orden if scores[c] >= mejor - self.delta]
        if len(en_disputa) > 1:
            return Respuesta(
                valor=None,
                determinada=False,
                scores_por_valor=scores,
                candidatas=[por_clase[c][0].evaluacion.id_hipotesis for c in en_disputa],
                margen_veredictos=0,
                fragil=True,
                sin_responder=sin_responder,
            )

        ganadora = orden[0]
        lider = por_clase[ganadora][0].evaluacion.id_hipotesis
        rival = por_clase[orden[1]][0].evaluacion.id_hipotesis if len(orden) > 1 else None
        margen = None
        if rival is not None:
            otras = [r for c in orden[1:] for r in por_clase[c]]
            margen = self._margen(por_clase[ganadora], otras)
        return Respuesta(
            valor=ganadora,
            determinada=True,
            scores_por_valor=scores,
            candidatas=[lider] + ([rival] if rival else []),
            lider=lider,
            rival=rival,
            margen_veredictos=margen,
            fragil=margen is not None and margen <= self.veredictos_fragil,
            sin_responder=sin_responder,
        )

    # --- margen ---------------------------------------------------------------------------

    def _impactos(self, r: ResultadoEvaluacion, subir: bool) -> list[float]:
        """Cuánto cambia el score al cambiar cada veredicto de LLM, de mayor a menor.

        Subir: el veredicto pasa a `explica`. Bajar: pasa a `contradice`.
        """
        alpha, lam = self.evaluador.alpha, self.evaluador.lambda_residuo
        impactos = []
        for v in r.veredictos:
            if not es_juicio(v):
                continue
            omega = self.confiabilidad(self.observacion(v.id_observacion))
            explicar, contradecir = alpha * omega, lam * costo_error(omega)
            if subir:
                cambio = {
                    Relacion.CONTRADICE: explicar + contradecir,
                    Relacion.NEUTRAL: explicar,
                    Relacion.EXPLICA: 0.0,
                }[v.relacion]
            else:
                cambio = {
                    Relacion.EXPLICA: explicar + contradecir,
                    Relacion.NEUTRAL: contradecir,
                    Relacion.CONTRADICE: 0.0,
                }[v.relacion]
            if cambio > 0:
                impactos.append(cambio)
        return sorted(impactos, reverse=True)

    @staticmethod
    def _cambios_para_bajar(score: float, objetivo: float, impactos: list[float]) -> float:
        """Mínimos cambios para que `score` quede en o bajo `objetivo` (inf si no alcanza)."""
        cambios = 0
        for impacto in impactos:
            if score <= objetivo:
                break
            score -= impacto
            cambios += 1
        return cambios if score <= objetivo else math.inf

    def _margen(
        self, lideres: list[ResultadoEvaluacion], rivales: list[ResultadoEvaluacion]
    ) -> int | None:
        bajar = {r.evaluacion.id_hipotesis: self._impactos(r, subir=False) for r in lideres}
        mejor = math.inf
        for rival in rivales:
            alcanzado = rival.evaluacion.score_final
            subidas = self._impactos(rival, subir=True)
            for t in range(len(subidas) + 1):
                if t:
                    alcanzado += subidas[t - 1]
                objetivo = alcanzado + self.delta
                total = t + sum(
                    self._cambios_para_bajar(
                        lider.evaluacion.score_final, objetivo, bajar[lider.evaluacion.id_hipotesis]
                    )
                    for lider in lideres
                )
                mejor = min(mejor, total)
        return None if math.isinf(mejor) else int(mejor)
