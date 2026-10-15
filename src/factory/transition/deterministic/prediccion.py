"""Puntuación predictiva (docs/historico/marco-teorico/16 P3, EXP-014, EXP-015). Sin IA.

Una hipótesis vale lo que predice de lo no visto, no lo que acomoda de lo visto. Para cada
observación y_i se la oculta, se ajustan los parámetros libres de la hipótesis con las demás y se
mide la probabilidad que le daba a y_i:

    score(H) = Σ_i log p(y_i | y_−i, H) − γ·P(H)
    p(y_i | y_−i, H) = Σ_θ w_θ ℓ_i(θ),   w_θ ∝ Π_{j≠i} ℓ_j(θ)   (prior uniforme sobre θ)
    ℓ_j(θ) = ω_j·[π_j(θ) ≈ y_j] + (1 − ω_j)/|Y_j|

El segundo término de ℓ es el error del observador: con probabilidad 1 − ω reporta cualquier
valor de su universo Y_j. Si H no proyecta lo que vería el observador, ℓ_j = 1/|Y_j|.

Solo aplica donde π es computable. Una hipótesis fija (sin parámetros libres) es una familia de
un solo miembro: su puntaje es su log-verosimilitud.
"""

import math
from collections.abc import Callable, Iterator
from itertools import product
from typing import Protocol

from pydantic import BaseModel, Field

from factory.contracts.abduction import HipotesisCandidata, Valor
from factory.contracts.observation import Observacion, Observador
from factory.transition.deterministic.ibe_evaluator import OMEGA_MAX

MAX_MIEMBROS = 50_000


class Proyector(Protocol):
    def predecir(self, hipotesis: HipotesisCandidata, observador: Observador) -> Valor | None: ...

    def consistente(
        self, predicho: Valor, observacion: Observacion, observador: Observador
    ) -> bool: ...


class PuntajePredictivo(BaseModel):
    total: float = Field(description="Σ log p(y_i | y_−i, H), sin el prior de parsimonia")
    por_observacion: dict[str, float] = Field(
        description="p(y_i | y_−i, H) de cada observación oculta"
    )
    miembros: int = Field(description="Tamaño de la familia (combinaciones de parámetros)")


def miembros(hipotesis: HipotesisCandidata) -> Iterator[HipotesisCandidata]:
    """Cada asignación de los parámetros libres, como hipótesis fija."""
    libres = hipotesis.parametros_libres
    if not libres:
        yield hipotesis
        return
    nombres = sorted(libres)
    for valores in product(*(libres[n] for n in nombres)):
        yield hipotesis.model_copy(
            update={
                "afirmaciones": {
                    **hipotesis.afirmaciones,
                    **dict(zip(nombres, valores, strict=True)),
                },
                "parametros_libres": {},
            }
        )


def tamano_familia(hipotesis: HipotesisCandidata) -> int:
    return math.prod(len(v) for v in hipotesis.parametros_libres.values())


def _logsumexp(valores: list[float]) -> float:
    m = max(valores)
    if m == -math.inf:
        return -math.inf
    return m + math.log(sum(math.exp(v - m) for v in valores))


def puntuar(
    hipotesis: HipotesisCandidata,
    observaciones: list[tuple[Observacion, Observador, float]],
    proyector: Proyector,
    universo: Callable[[Observacion, Observador], int],
) -> PuntajePredictivo:
    """`observaciones`: (observación activa, su observador, ω)."""
    n = tamano_familia(hipotesis)
    if n > MAX_MIEMBROS:
        raise ValueError(
            f"la familia '{hipotesis.id_hipotesis}' tiene {n} miembros (máximo {MAX_MIEMBROS}): "
            "declare menos parámetros libres o menos valores"
        )
    # log ℓ_j(θ) para cada miembro θ y cada observación j.
    tabla: list[list[float]] = []
    for miembro in miembros(hipotesis):
        fila = []
        for observacion, observador, omega in observaciones:
            omega = min(omega, OMEGA_MAX)
            base = 1 / max(universo(observacion, observador), 1)
            predicho = proyector.predecir(miembro, observador)
            if predicho is None:
                verosimilitud = base
            else:
                acierta = proyector.consistente(predicho, observacion, observador)
                verosimilitud = omega * acierta + (1 - omega) * base
            fila.append(math.log(verosimilitud))
        tabla.append(fila)

    totales = [sum(fila) for fila in tabla]
    por_observacion: dict[str, float] = {}
    for i, (observacion, _, _) in enumerate(observaciones):
        sin_i = [t - fila[i] for t, fila in zip(totales, tabla, strict=True)]
        log_p = _logsumexp(totales) - _logsumexp(sin_i)
        por_observacion[observacion.id] = math.exp(log_p)
    total = sum(math.log(p) if p > 0 else -math.inf for p in por_observacion.values())
    return PuntajePredictivo(total=total, por_observacion=por_observacion, miembros=n)
