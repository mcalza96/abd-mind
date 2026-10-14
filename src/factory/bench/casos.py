"""Esquema de los casos frontera de abd-bench (datasets/abd-bench).

Cada caso separa lo que el motor puede ver (`observadores`, `observaciones`, `pregunta`) de lo
que no debe ver (`solucion`, `verdad`, `respuesta_inductiva_erronea`). La verdad es una
observación falible con fuente y confiabilidad, no una etiqueta (docs/marco-teorico/12 §12.1).

La pregunta es la misma para todos los casos: qué *tipo* de causa explica la discrepancia.
Así el benchmark mide la clase de abducción (postular una entidad, culpar al observador,
revisar una ley o recombinar lo conocido), comparable entre dominios, además del mecanismo.
"""

import json
from enum import StrEnum
from pathlib import Path
from typing import Literal

from pydantic import BaseModel, Field, model_validator

from factory.contracts.case import Pregunta
from factory.contracts.observation import RolObservacion


class TipoCausa(StrEnum):
    ENTIDAD_NUEVA = "entidad_nueva"  # existe algo no observado ni conocido (Neptuno, neutrino)
    ERROR_DEL_OBSERVADOR = "error_del_observador"  # instrumento, filtro, sesgo o engaño (OPERA)
    LEY_INCORRECTA = "ley_incorrecta"  # la regla del marco es falsa o incompleta (Mercurio)
    MECANISMO_CONOCIDO = "mecanismo_conocido"  # entidades conocidas en una combinación nueva


PREGUNTA_TIPO_CAUSA = Pregunta(
    variable="tipo_de_causa",
    valores=[t.value for t in TipoCausa],
    descripcion=(
        "¿Qué explica que los observadores discrepen: una entidad aún no observada, un error o "
        "sesgo de algún observador, una ley del marco que es incorrecta, o un mecanismo con "
        "entidades ya conocidas?"
    ),
)


class Mecanismo(StrEnum):
    """Qué parte del marco pone a prueba el caso."""

    EXPANSION_JUSTIFICADA = "expansion_justificada"
    EXPANSION_INJUSTIFICADA = "expansion_injustificada"  # postular entidad sería un error
    SESGO_DEL_OBSERVADOR = "sesgo_del_observador"  # error sistemático, no ruido
    ENGANO = "engano"  # observador que oculta o falsea
    REVISION_DE_REGLA = "revision_de_regla"  # 12 §12.4
    CAMBIO_DE_MARCO = "cambio_de_marco"  # el observador no tiene el sensor o la resolución
    MAGNITUDES = "magnitudes"  # 10 B5: descomposición cuantitativa
    AUSENCIA_DE_EVIDENCIA = "ausencia_de_evidencia"
    COINCIDENCIA = "coincidencia"  # varias proyecciones débiles se vuelven una fuerte
    PRECEDENTE_ENGANOSO = "precedente_enganoso"  # inducir desde un caso parecido falla
    TEMPORALIDAD = "temporalidad"  # 9.4: la causa precede por mucho al efecto
    VERDAD_DISPUTADA = "verdad_disputada"
    DECISION_VS_EXPLICACION = "decision_vs_explicacion"
    CONSENSO_EQUIVOCADO = "consenso_equivocado"  # la mayoría o la autoridad estaba mal


class ObservadorCaso(BaseModel):
    id: str
    nombre: str
    marco: str = Field(description="Perspectiva, instrumento o método, sin la solución")


class ObservacionCaso(BaseModel):
    observador: str
    contenido: str = Field(description="Lo que el observador reportó en su momento")
    rol: RolObservacion = RolObservacion.EVIDENCIA
    momento: str | None = Field(default=None, description="Fecha o período, si importa")


class Solucion(BaseModel):
    """Oculta al motor. Lo que la historia terminó estableciendo."""

    tipo_de_causa: TipoCausa
    tipo_secundario: TipoCausa | None = None
    mecanismo: str
    entidades_nuevas: list[str] = Field(default_factory=list)
    mapeo: dict[str, str] = Field(
        description="Por observador: por qué, si H es cierta, reportó lo que reportó"
    )


class VerdadCaso(BaseModel):
    descripcion: str
    fuente: str = Field(description="Quién la estableció (no el agente que recopiló el caso)")
    confiabilidad: float = Field(gt=0.0, le=1.0)
    estado: Literal["establecida", "tentativa", "disputada"]


class Caso(BaseModel):
    id: str
    serie: Literal["A", "B", "C", "D", "E", "V"]
    titulo: str
    variante_de: str | None = Field(default=None, description="Caso real del que es variante")
    pregunta: Pregunta = PREGUNTA_TIPO_CAUSA
    observadores: list[ObservadorCaso] = Field(min_length=2)
    observaciones: list[ObservacionCaso] = Field(min_length=2)
    solucion: Solucion
    respuesta_inductiva_erronea: str
    verdad: VerdadCaso
    fuentes: list[str] = Field(default_factory=list)
    mecanismos: list[Mecanismo] = Field(min_length=1)
    contaminacion: Literal["alta", "media", "baja"]
    saneamiento: str = Field(
        default="", description="Qué se quitó de las observaciones por revelar la solución"
    )

    @model_validator(mode="after")
    def _coherente(self) -> "Caso":
        ids = {o.id for o in self.observadores}
        if len(ids) != len(self.observadores):
            raise ValueError(f"{self.id}: ids de observador repetidos")
        sin_observador = {o.observador for o in self.observaciones} - ids
        if sin_observador:
            raise ValueError(
                f"{self.id}: observaciones de observadores desconocidos {sin_observador}"
            )
        if not any(o.rol is RolObservacion.EXPLANANDUM for o in self.observaciones):
            raise ValueError(f"{self.id}: falta al menos un explanandum")
        if set(self.solucion.mapeo) - ids:
            raise ValueError(f"{self.id}: el mapeo nombra observadores desconocidos")
        if (self.serie == "V") != (self.variante_de is not None):
            raise ValueError(f"{self.id}: solo la serie V es variante, y siempre de un caso")
        return self


def cargar_casos(ruta: Path) -> list[Caso]:
    """Lee un archivo JSONL de casos (una línea por caso; líneas vacías se ignoran)."""
    casos = []
    for numero, linea in enumerate(ruta.read_text(encoding="utf-8").splitlines(), start=1):
        if linea.strip():
            try:
                casos.append(Caso.model_validate(json.loads(linea)))
            except ValueError as e:
                raise ValueError(f"{ruta.name}:{numero}: {e}") from e
    return casos
