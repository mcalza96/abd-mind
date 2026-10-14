"""Entradas y salidas del motor de casos.

Son la base del contrato MCP (docs/arquitectura/contrato-mcp.md).
"""

from enum import StrEnum
from typing import Literal

from pydantic import BaseModel, Field

from factory.config import ConfigPesos
from factory.contracts.abduction import Valor
from factory.contracts.case import EstadoHipotesis, Veredicto
from factory.contracts.observation import EstadoObservacion, Observador


class CodigoError(StrEnum):
    CASO_NO_ENCONTRADO = "caso_no_encontrado"
    CASO_CERRADO = "caso_cerrado"
    DOMINIO_DESCONOCIDO = "dominio_desconocido"
    OBSERVACION_NO_ENCONTRADA = "observacion_no_encontrada"
    SIN_OBSERVACIONES = "sin_observaciones"
    SIN_HIPOTESIS = "sin_hipotesis"
    PRESUPUESTO_CASO_AGOTADO = "presupuesto_caso_agotado"
    LIMITE_HIPOTESIS = "limite_hipotesis"
    PROVEEDOR_LLM_NO_DISPONIBLE = "proveedor_llm_no_disponible"
    RESPUESTA_LLM_INVALIDA = "respuesta_llm_invalida"


class ErrorCaso(Exception):
    def __init__(self, codigo: CodigoError, mensaje: str) -> None:
        super().__init__(mensaje)
        self.codigo = codigo
        self.mensaje = mensaje


# --- registro persistido ------------------------------------------------------------------


class ResumenHipotesis(BaseModel):
    id_hipotesis: str
    mecanismo: str
    consiliencia_c: int
    parsimonia_p: int
    coherencia_k: float
    score_final: float


class ResumenCaso(BaseModel):
    n_observaciones: int = 0
    n_hipotesis_vivas: int = 0
    n_hipotesis_derrotadas: int = 0
    h_estrella: ResumenHipotesis | None = None
    expansion_sugerida: bool = False
    evaluado_en_evento: int | None = Field(
        default=None, description="Cantidad de eventos cuando se evaluó por última vez"
    )


class RegistroCaso(BaseModel):
    id: str
    descripcion: str
    dominio: str
    reglas_json: str = Field(description="Reglas con que se creó el caso (reproducibilidad)")
    hash_reglas: str
    pesos: ConfigPesos
    sesion: str = Field(description="x-opencode-session estable del caso")
    estado: Literal["abierto", "cerrado"] = "abierto"
    llamadas: int = 0
    resumen: ResumenCaso = Field(default_factory=ResumenCaso)
    creado: str
    actualizado: str


# --- entradas -----------------------------------------------------------------------------


class EntradaObservador(BaseModel):
    nombre: str
    marco: str | None = None
    parametros: dict[str, Valor] = Field(default_factory=dict)
    tolerancia: float = 0.0


class EntradaHipotesis(BaseModel):
    mecanismo: str
    entidades_latentes: list[str] = Field(default_factory=list)
    afirmaciones: dict[str, Valor] = Field(default_factory=dict)
    predicados: list[str] = Field(default_factory=list)
    observaciones_explicadas: list[str] = Field(default_factory=list)


# --- salidas ------------------------------------------------------------------------------


class InfoCaso(BaseModel):
    caso_id: str
    descripcion: str
    dominio: str
    version_reglas: int
    pesos: ConfigPesos
    estado: str
    llamadas: int
    resumen: ResumenCaso
    evaluacion_vigente: bool
    actualizado: str
    avisos: list[str] = Field(default_factory=list)


class ObservacionRegistrada(BaseModel):
    id: str
    contenido: str
    valor: Valor | None = None
    variables: dict[str, Valor] = Field(default_factory=dict)
    estado: EstadoObservacion = EstadoObservacion.ACTIVA


class ResultadoObservacion(BaseModel):
    caso_id: str
    observador_id: str
    hechos: list[ObservacionRegistrada]
    opiniones: list[str]
    derrotadas: list[str] = Field(
        default_factory=list, description="Hipótesis vivas que estos hechos derrotaron"
    )
    avisos: list[str] = Field(default_factory=list)


class HipotesisRegistrada(BaseModel):
    id_hipotesis: str
    mecanismo: str
    entidades_latentes: list[str]
    afirmaciones: dict[str, Valor]
    origen: str


class ResultadoHipotesis(BaseModel):
    caso_id: str
    hipotesis: list[HipotesisRegistrada]
    avisos: list[str] = Field(default_factory=list)


class EntradaRanking(BaseModel):
    id_hipotesis: str
    mecanismo: str
    origen: str
    consiliencia_c: int
    parsimonia_p: int
    coherencia_k: float
    score_final: float
    veredictos: list[Veredicto]
    declaradas_no_verificadas: list[str] = Field(
        default_factory=list, description="Declaró explicarlas y el verificador lo negó"
    )


class Descartada(BaseModel):
    id_hipotesis: str
    mecanismo: str
    reglas: list[str]


class ResultadoEvaluacionCaso(BaseModel):
    caso_id: str
    m: int
    ranking: list[EntradaRanking]
    descartadas_por_reglas: list[Descartada]
    h_estrella: ResumenHipotesis | None
    expansion_sugerida: bool
    avisos: list[str] = Field(default_factory=list)


class ResultadoMejorExplicacion(BaseModel):
    caso_id: str
    h_estrella: ResumenHipotesis | None
    motivo: str


class ResultadoEvidencia(BaseModel):
    observacion: ResultadoObservacion
    h_estrella_anterior: ResumenHipotesis | None
    evaluacion: ResultadoEvaluacionCaso


class ResultadoRetractacion(BaseModel):
    caso_id: str
    retractadas: list[str]
    reactivadas: list[str]
    evaluacion: ResultadoEvaluacionCaso | None


class HipotesisAuditada(BaseModel):
    id_hipotesis: str
    mecanismo: str
    origen: str
    entidades_latentes: list[str]
    afirmaciones: dict[str, Valor]
    estado: EstadoHipotesis
    derrotada_por: list[str]


class ObservacionAuditada(ObservacionRegistrada):
    observador_id: str


class Auditoria(BaseModel):
    caso: InfoCaso
    observadores: list[Observador]
    opiniones: dict[str, list[str]]
    observaciones: list[ObservacionAuditada]
    hipotesis: list[HipotesisAuditada]
    veredictos: list[Veredicto]
    eventos: list[dict[str, object]]
