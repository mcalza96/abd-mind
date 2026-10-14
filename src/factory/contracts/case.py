"""Estado del razonamiento: veredictos por observación y resultado de evaluar una hipótesis."""

from enum import StrEnum
from typing import Any

from pydantic import BaseModel, Field, model_validator

from factory.contracts.abduction import EvaluacionAbductiva


class EstadoHipotesis(StrEnum):
    VIVA = "viva"
    DERROTADA = "derrotada"


class Relacion(StrEnum):
    """Relación entre una hipótesis y una observación (11 §11.1, ADR-0011)."""

    EXPLICA = "explica"  # si H es cierta, el observador reportaría y
    NEUTRAL = "neutral"  # H no dice qué reportaría el observador
    CONTRADICE = "contradice"  # si H es cierta, el observador reportaría otra cosa


class Veredicto(BaseModel):
    """Resultado de comprobar π_i(H) ≈ y_i para un par (hipótesis, observación)."""

    id_hipotesis: str
    id_observacion: str
    relacion: Relacion
    explica: bool = Field(default=False, description="Derivado: relacion == explica")
    fuente: str = Field(description="proyeccion o verificador:<modelo>")
    justificacion: str = ""

    @model_validator(mode="before")
    @classmethod
    def _completar(cls, datos: Any) -> Any:
        """Acepta veredictos booleanos (anteriores a ADR-0011) o solo la relación."""
        if isinstance(datos, dict):
            datos = dict(datos)
            if datos.get("relacion") is None:
                datos["relacion"] = (
                    Relacion.EXPLICA if datos.get("explica") else Relacion.CONTRADICE
                )
            datos["explica"] = Relacion(datos["relacion"]) is Relacion.EXPLICA
        return datos


class ResultadoEvaluacion(BaseModel):
    evaluacion: EvaluacionAbductiva
    estado: EstadoHipotesis
    derrotada_por: list[str] = Field(default_factory=list)
    en_tension_por: list[str] = Field(
        default_factory=list,
        description="Hechos nuevos que contradice, de observadores bajo el umbral de derrota",
    )
    atribuidas_a_error: dict[str, float] = Field(
        default_factory=dict,
        description="Residuo: hechos activos que contradice, con el costo c(ω) de suponerlos error",
    )
    sin_explicar: list[str] = Field(
        default_factory=list,
        description="Explananda ante los que la hipótesis es neutral (ADR-0011)",
    )
    veredictos: list[Veredicto] = Field(default_factory=list)
    violaciones: list[str] = Field(default_factory=list, description="Reglas duras violadas")
    declaradas_no_verificadas: list[str] = Field(
        default_factory=list,
        description=(
            "Observaciones que la hipótesis declaraba explicar y el verificador rechazó "
            "(indicador de racionalización)"
        ),
    )
