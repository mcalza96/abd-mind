"""Estado del razonamiento: veredictos por observación y resultado de evaluar una hipótesis."""

from enum import StrEnum

from pydantic import BaseModel, Field

from factory.contracts.abduction import EvaluacionAbductiva


class EstadoHipotesis(StrEnum):
    VIVA = "viva"
    DERROTADA = "derrotada"


class Veredicto(BaseModel):
    """Resultado de comprobar π_i(H) ≈ y_i para un par (hipótesis, observación)."""

    id_hipotesis: str
    id_observacion: str
    explica: bool
    fuente: str = Field(description="proyeccion o verificador:<modelo>")
    justificacion: str = ""


class ResultadoEvaluacion(BaseModel):
    evaluacion: EvaluacionAbductiva
    estado: EstadoHipotesis
    derrotada_por: list[str] = Field(default_factory=list)
    veredictos: list[Veredicto] = Field(default_factory=list)
    violaciones: list[str] = Field(default_factory=list, description="Reglas duras violadas")
    declaradas_no_verificadas: list[str] = Field(
        default_factory=list,
        description=(
            "Observaciones que la hipótesis declaraba explicar y el verificador rechazó "
            "(indicador de racionalización)"
        ),
    )
