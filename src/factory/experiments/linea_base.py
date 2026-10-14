"""Línea base (D10): un modelo responde directamente, en una sola llamada y sin pipeline."""

from factory.config import ConfigRol
from factory.contracts.abduction import HipotesisCandidata
from factory.contracts.observation import Observacion, Observador
from factory.contracts.rules import ConjuntoReglas
from factory.transition.stochastic.contexto import describir_dominio, describir_observaciones
from factory.transition.stochastic.esquemas import RespuestaDirectaLLM, a_diccionario
from factory.transition.stochastic.llm_client import ClienteLLM

SISTEMA = "Responde la pregunta del usuario con tu mejor respuesta, de forma directa."


def respuesta_directa(
    cliente: ClienteLLM,
    rol: ConfigRol,
    dominio: ConjuntoReglas,
    observadores: dict[str, Observador],
    observaciones: list[Observacion],
) -> HipotesisCandidata:
    usuario = (
        f"{describir_dominio(dominio)}\n\n{describir_observaciones(observadores, observaciones)}"
        "\n\n¿Cuál es el estado real que describen estas observaciones? Da una única respuesta "
        "y fija en 'afirmaciones' las variables del dominio que la describen."
    )
    bruto = cliente.completar_json(rol, SISTEMA, usuario, RespuestaDirectaLLM)
    return HipotesisCandidata(
        id_hipotesis=f"base_{rol.modelo}",
        mecanismo_latente=bruto.respuesta,
        afirmaciones=a_diccionario(bruto.afirmaciones),
        origen=f"linea_base:{rol.modelo}",
    )
