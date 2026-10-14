"""Esquemas de salida que se piden a los modelos. Planos y estrictos para json_schema."""

from typing import Literal

from pydantic import BaseModel, Field

from factory.contracts.abduction import Valor


class ParVariable(BaseModel):
    variable: str
    valor: str | float | bool


def a_diccionario(pares: list[ParVariable]) -> dict[str, Valor]:
    """Convierte pares a diccionario; los números enteros vuelven a ser int."""
    resultado: dict[str, Valor] = {}
    for p in pares:
        valor = p.valor
        if isinstance(valor, float) and valor.is_integer():
            valor = int(valor)
        resultado[p.variable] = valor
    return resultado


class HechoLLM(BaseModel):
    enunciado: str
    variables: list[ParVariable]


class ExtraccionLLM(BaseModel):
    hechos: list[HechoLLM]
    opiniones: list[str]
    dudas: list[str]


class PrediccionFuturaLLM(BaseModel):
    que: str
    horizonte: str
    esperado: str


class HipotesisLLM(BaseModel):
    mecanismo_latente: str
    entidades_latentes: list[str]
    afirmaciones: list[ParVariable]
    predicados_de_consistencia: list[str]
    observaciones_explicadas: list[str]
    predicciones: list[PrediccionFuturaLLM] = Field(default_factory=list)


class GeneracionLLM(BaseModel):
    hipotesis: list[HipotesisLLM]


class VeredictoLLM(BaseModel):
    justificacion: str
    relacion: Literal["explica", "neutral", "contradice"]


class RespuestaDirectaLLM(BaseModel):
    respuesta: str
    afirmaciones: list[ParVariable]


class PrediccionLLM(BaseModel):
    id_hipotesis: str
    prediccion: str


class ConsultaLLM(BaseModel):
    observador_sugerido: str
    marco: str
    que_observar: str
    predicciones: list[PrediccionLLM]


class ConsultasLLM(BaseModel):
    consultas: list[ConsultaLLM]


class CalificacionLLM(BaseModel):
    id_hipotesis: str
    justificacion: str
    nivel: Literal["muy_esperable", "esperable", "indiferente", "inesperado"]


class ComparacionLLM(BaseModel):
    calificaciones: list[CalificacionLLM]


class JuicioHipotesisLLM(BaseModel):
    id_hipotesis: str
    postulados: list[str]


class JuicioParsimoniaLLM(BaseModel):
    juicios: list[JuicioHipotesisLLM]
