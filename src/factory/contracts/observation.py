"""Observadores y observaciones (Postulado 1: y_i = π_{O_i}(S)).

Toda observación pertenece a un observador; el marco del observador condiciona su proyección.
"""

from enum import StrEnum

from pydantic import BaseModel, Field

from factory.contracts.abduction import Valor


class Observador(BaseModel):
    id: str
    nombre: str
    marco: str | None = Field(
        default=None, description="Perspectiva, metodología o instrumento del observador"
    )
    parametros: dict[str, Valor] = Field(
        default_factory=dict,
        description="Parámetros del marco que usa la proyección (p. ej. vista: frontal)",
    )
    tolerancia: float = Field(
        default=0.0, ge=0.0, description="ε_i: tolerancia de la relación ≈ (D5)"
    )


class EstadoObservacion(StrEnum):
    ACTIVA = "activa"
    RETRACTADA = "retractada"


class Observacion(BaseModel):
    """Observación atómica y_i: un hecho reportado por un observador."""

    id: str
    observador_id: str
    contenido: str = Field(description="Enunciado del hecho tal como se reportó")
    valor: Valor | None = Field(
        default=None, description="Valor estructurado del hecho, si se conoce"
    )
    estado: EstadoObservacion = EstadoObservacion.ACTIVA
