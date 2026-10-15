"""Juicio holístico (14, ADR-0016): elige la mejor explicación viendo todo a la vez.

En dominios abiertos, sumar juicios por observación pierde los patrones entre hechos y queda a
merced del ruido de cada veredicto (EXP-010, EXP-012). Aquí un modelo ve todas las
observaciones y todas las hipótesis vivas y coherentes, las ordena y dice si la evidencia
alcanza para decidir. El motor registra el juicio como tal (no como un cálculo) y mantiene lo
que sí calcula: reglas duras, derrota, sugerencias y auditoría.
"""

from pydantic import BaseModel

from factory.config import ConfigRol
from factory.contracts.abduction import HipotesisCandidata
from factory.contracts.case import Pregunta
from factory.contracts.observation import Observacion, Observador
from factory.transition.stochastic.contexto import (
    describir_hipotesis,
    describir_observaciones,
    describir_pregunta,
)
from factory.transition.stochastic.esquemas import JuicioHolisticoLLM
from factory.transition.stochastic.llm_client import ClienteLLM

SISTEMA_JUICIO = """Eres el juez de un sistema de razonamiento abductivo. Recibes las \
observaciones de un caso (cada una reportada por un observador desde su marco) y varias \
hipótesis rivales que intentan explicarlas.

Ordena las hipótesis de la mejor a la peor explicación de TODAS las observaciones en conjunto:
- prefiere la que hace esperables más observaciones y sus relaciones entre sí, sin \
contradecir ninguna;
- desconfía de las hipótesis que acomodan hechos con cláusulas agregadas para ese fin;
- a igualdad de lo explicado, prefiere la que postula menos cosas no observadas;
- considera que cualquier observador puede equivocarse, pero suponer un error tiene un costo.

'decide' es false si la evidencia no permite preferir una explicación sobre las demás (o, si \
el caso tiene una pregunta, un valor de la respuesta sobre los demás): en ese caso, ordena igual \
y explica en 'justificacion' qué observación las separaría. No inventes certeza.
'confianza': alta, media o baja. 'orden': todos los ids, una vez cada uno."""


class Juicio(BaseModel):
    orden: list[str]
    decide: bool
    confianza: str
    justificacion: str
    modelo: str


def juzgar_explicaciones(
    cliente: ClienteLLM,
    rol: ConfigRol,
    hipotesis: list[HipotesisCandidata],
    observadores: dict[str, Observador],
    observaciones: list[Observacion],
    pregunta: Pregunta | None = None,
) -> Juicio:
    partes = [
        describir_observaciones(observadores, observaciones),
        "Hipótesis rivales:\n" + "\n".join(describir_hipotesis(h) for h in hipotesis),
    ]
    if pregunta is not None:
        partes.append(describir_pregunta(pregunta))
    bruto, modelo = cliente.completar_json_con_modelo(
        rol, SISTEMA_JUICIO, "\n\n".join(partes), JuicioHolisticoLLM
    )
    ids = [h.id_hipotesis for h in hipotesis]
    orden = [i for i in dict.fromkeys(bruto.orden) if i in ids]
    orden += [i for i in ids if i not in orden]  # las omitidas van al final
    return Juicio(
        orden=orden,
        decide=bruto.decide,
        confianza=bruto.confianza,
        justificacion=bruto.justificacion,
        modelo=modelo,
    )
