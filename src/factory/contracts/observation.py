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
    confiabilidad: float = Field(
        default=1.0,
        gt=0.0,
        le=1.0,
        description=(
            "ω_i: probabilidad de que un reporte no sea un error grosero (ADR-0009). "
            "Nunca se infiere del acuerdo con otros observadores"
        ),
    )


class EstadoObservacion(StrEnum):
    ACTIVA = "activa"
    RETRACTADA = "retractada"


class RolObservacion(StrEnum):
    """Qué papel juega el hecho en el caso (11 §11.2, ADR-0011)."""

    EXPLANANDUM = "explanandum"  # lo que el caso quiere entender: exige explicación
    EVIDENCIA = "evidencia"  # sirve para elegir entre explicaciones; no exige explicación


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
    confiabilidad: float | None = Field(
        default=None,
        gt=0.0,
        le=1.0,
        description="Confiabilidad de este hecho en particular; si no, la de su observador",
    )
    estado: EstadoObservacion = EstadoObservacion.ACTIVA
    rol: RolObservacion = RolObservacion.EXPLANANDUM


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

    def a_observaciones(
        self,
        observador_id: str,
        prefijo: str,
        rol: RolObservacion = RolObservacion.EXPLANANDUM,
    ) -> list[Observacion]:
        return [
            Observacion(
                id=f"{prefijo}.h{i}",
                observador_id=observador_id,
                contenido=h.enunciado,
                variables=h.variables,
                rol=rol,
            )
            for i, h in enumerate(self.hechos, start=1)
        ]
