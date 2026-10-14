"""Contratos de la especificación: hipótesis candidata y su evaluación abductiva.

Ver docs/marco-teorico/04-funcion-objetivo-ibe.md y docs/arquitectura/contrato-mcp.md.
"""

from pydantic import BaseModel, Field

# Valor atómico que puede tomar una variable observada o afirmada.
Valor = str | int | float | bool


class HipotesisCandidata(BaseModel):
    id_hipotesis: str
    mecanismo_latente: str = Field(
        description="Descripción causal invariante de la entidad postulada"
    )
    entidades_latentes: list[str] = Field(
        default_factory=list,
        description="Nuevas entidades asumidas para calcular Parsimonia P",
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
