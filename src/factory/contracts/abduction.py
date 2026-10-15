"""Contratos de la especificación: hipótesis candidata y su evaluación abductiva.

Ver docs/historico/marco-teorico/04-funcion-objetivo-ibe.md y docs/arquitectura/contrato-mcp.md.
"""

from pydantic import BaseModel, Field

# Valor atómico que puede tomar una variable observada o afirmada.
Valor = str | int | float | bool


class Prediccion(BaseModel):
    """Consecuencia futura observable que la hipótesis espera (11 §11.5, ADR-0013).

    No entra en el score: todavía no es una observación.
    """

    que: str = Field(description="Qué se observaría")
    horizonte: str = Field(description="En qué plazo (texto libre hasta implementar fechas)")
    esperado: str = Field(description="Qué resultado espera la hipótesis")


class HipotesisCandidata(BaseModel):
    id_hipotesis: str
    mecanismo_latente: str = Field(
        description="Descripción causal invariante de la entidad postulada"
    )
    entidades_latentes: list[str] = Field(
        default_factory=list,
        description="Nuevas entidades asumidas para calcular Parsimonia P",
    )
    entidades_juzgadas: list[str] = Field(
        default_factory=list,
        description="Postulados no observados según un juez independiente (ADR-0015); cuentan en P",
    )
    observaciones_explicadas: list[str] = Field(
        default_factory=list,
        description=(
            "IDs de observaciones que el generador declara resolver. Insumo de C solo en el "
            "evaluador básico; el árbol de hipótesis la usa como predicción auditable (D1)"
        ),
    )
    predicados_de_consistencia: list[str] = Field(
        default_factory=list,
        description="Reglas formales que deben validarse para Coherencia K",
    )
    afirmaciones: dict[str, Valor] = Field(
        default_factory=dict,
        description=(
            "Afirmaciones estructuradas variable → valor que evalúa el motor de reglas (D3)"
        ),
    )
    parametros_libres: dict[str, list[Valor]] = Field(
        default_factory=dict,
        description=(
            "Familia de hipótesis: variables que la hipótesis no fija y sus valores posibles. "
            "La puntuación predictiva las ajusta a los datos (16 P3, EXP-014)"
        ),
    )
    predicciones: list[Prediccion] = Field(
        default_factory=list, description="Consecuencias futuras que espera (no puntúan)"
    )
    origen: str = Field(
        default="desconocido",
        description="Quién propuso la hipótesis: motor:<modelo>, hermes, usuario, experimento",
    )


class EvaluacionAbductiva(BaseModel):
    id_hipotesis: str
    parsimonia_p: int
    consiliencia_c: int
    coherencia_k: float
    score_final: float
    score_predictivo: float | None = Field(
        default=None,
        description="Σ log p(y_i | y_−i, H) − γ·P, si el dominio permite proyectar (EXP-015)",
    )
