"""Tronco determinista: Score(H) = α·C + β·K − γ·P (docs/marco-teorico/04-funcion-objetivo-ibe.md).

Sin IA. Por defecto C y P se toman de lo que declara la hipótesis, como en la especificación; el
árbol de hipótesis inyecta en su lugar los valores verificados (decisiones D1 y D2).

Con observadores falibles (09 §9.1, ADR-0009) el árbol entrega además la consiliencia ponderada
por confiabilidad y el residuo: Score = α·Σω + β·K − γ·P − λ·Σc(ω). Con λ = 0 y ω = 1 es la
función de la especificación.
"""

import math
from collections.abc import Iterable

from factory.contracts.abduction import EvaluacionAbductiva, HipotesisCandidata
from factory.organ.rule_engine import ResultadoCoherencia, RuleEngine

OMEGA_MAX = 0.999


def costo_error(omega: float) -> float:
    """c(ω) = −ln(1 − ω): costo de suponer que un observador de confiabilidad ω se equivocó."""
    return -math.log(1 - min(omega, OMEGA_MAX))


def clave_ranking(e: EvaluacionAbductiva) -> tuple[float, int, int, str]:
    """Orden determinista (D7): mayor score, luego mayor C, menor P e id."""
    return (-e.score_final, -e.consiliencia_c, e.parsimonia_p, e.id_hipotesis)


class IBEEvaluator:
    def __init__(
        self,
        alpha: float = 1.5,
        beta: float = 10.0,
        gamma: float = 1.0,
        tau: float | None = None,
        rule_engine: RuleEngine | None = None,
        lambda_residuo: float = 0.0,
    ) -> None:
        if min(alpha, beta, gamma) <= 0:
            raise ValueError("los pesos α, β y γ deben ser positivos")
        if lambda_residuo < 0:
            raise ValueError("el peso λ del residuo no puede ser negativo")
        self.lambda_residuo = lambda_residuo  # Peso del residuo atribuido a error
        self.alpha = alpha  # Peso Consiliencia
        self.beta = beta  # Peso Coherencia
        self.gamma = gamma  # Peso Parsimonia
        self.tau = tau  # Umbral mínimo de aceptación (None: sin umbral)
        self.rule_engine = rule_engine or RuleEngine()

    def score(
        self, c: float, k: float, p: int, descartada: bool = False, residuo: float = 0.0
    ) -> float:
        if descartada:
            return -math.inf
        return (self.alpha * c) + (self.beta * k) - (self.gamma * p) - self.lambda_residuo * residuo

    def evaluar_con_detalle(
        self,
        hipotesis: HipotesisCandidata,
        *,
        consiliencia: int | None = None,
        parsimonia: int | None = None,
        consiliencia_ponderada: float | None = None,
        residuo: float = 0.0,
    ) -> tuple[EvaluacionAbductiva, ResultadoCoherencia]:
        """`consiliencia_ponderada` (Σω de lo explicado) reemplaza a C en el score si se da;
        `residuo` es Σc(ω) de lo no explicado."""
        # 1. Parsimonia (P): entidades latentes postuladas
        p = len(hipotesis.entidades_latentes) if parsimonia is None else parsimonia
        # 2. Consiliencia (C): observaciones explicadas
        c = len(hipotesis.observaciones_explicadas) if consiliencia is None else consiliencia
        # 3. Coherencia (K): validación externa
        coherencia = self.rule_engine.coherencia(hipotesis)

        evaluacion = EvaluacionAbductiva(
            id_hipotesis=hipotesis.id_hipotesis,
            parsimonia_p=p,
            consiliencia_c=c,
            coherencia_k=coherencia.k,
            score_final=self.score(
                c if consiliencia_ponderada is None else consiliencia_ponderada,
                coherencia.k,
                p,
                coherencia.descartada,
                residuo,
            ),
        )
        return evaluacion, coherencia

    def evaluar_hipotesis(
        self,
        hipotesis: HipotesisCandidata,
        *,
        consiliencia: int | None = None,
        parsimonia: int | None = None,
    ) -> EvaluacionAbductiva:
        evaluacion, _ = self.evaluar_con_detalle(
            hipotesis, consiliencia=consiliencia, parsimonia=parsimonia
        )
        return evaluacion

    def ordenar(self, evaluaciones: Iterable[EvaluacionAbductiva]) -> list[EvaluacionAbductiva]:
        return sorted(evaluaciones, key=clave_ranking)

    def seleccionar(
        self, evaluaciones: Iterable[EvaluacionAbductiva]
    ) -> EvaluacionAbductiva | None:
        """H*: la mejor evaluación coherente que alcanza τ, o None si ninguna lo hace."""
        for e in self.ordenar(evaluaciones):
            if e.score_final == -math.inf:
                return None
            return e if self.tau is None or e.score_final >= self.tau else None
        return None

    def seleccionar_mejor_explicacion(
        self, candidatas: list[HipotesisCandidata]
    ) -> EvaluacionAbductiva | None:
        if not candidatas:
            raise ValueError("no hay hipótesis candidatas que evaluar")
        return self.seleccionar(self.evaluar_hipotesis(h) for h in candidatas)
