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
    variables: dict[str, Valor] = Field(
        default_factory=dict, description="Variables del dominio que el hecho fija explícitamente"
    )
    estado: EstadoObservacion = EstadoObservacion.ACTIVA


class HechoExtraido(BaseModel):
    enunciado: str
    variables: dict[str, Valor] = Field(default_factory=dict)


class ExtraccionObservacion(BaseModel):
    """Salida del córtex perceptivo: hechos (evidencia) separados de opiniones (D8)."""

    hechos: list[HechoExtraido] = Field(default_factory=list)
    opiniones: list[str] = Field(default_factory=list)
    dudas: list[str] = Field(
        default_factory=list, description="Enunciados de clasificación incierta o descartados"
    )

    def a_observaciones(self, observador_id: str, prefijo: str) -> list[Observacion]:
        return [
            Observacion(
                id=f"{prefijo}.h{i}",
                observador_id=observador_id,
                contenido=h.enunciado,
                variables=h.variables,
            )
            for i, h in enumerate(self.hechos, start=1)
        ]
