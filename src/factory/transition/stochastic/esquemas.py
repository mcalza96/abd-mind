"""Esquemas de salida que se piden a los modelos. Planos y estrictos para json_schema."""

from pydantic import BaseModel

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


class HipotesisLLM(BaseModel):
    mecanismo_latente: str
    entidades_latentes: list[str]
    afirmaciones: list[ParVariable]
    predicados_de_consistencia: list[str]
    observaciones_explicadas: list[str]


class GeneracionLLM(BaseModel):
    hipotesis: list[HipotesisLLM]


class VeredictoLLM(BaseModel):
    justificacion: str
    explica: bool


class RespuestaDirectaLLM(BaseModel):
    respuesta: str
    afirmaciones: list[ParVariable]
