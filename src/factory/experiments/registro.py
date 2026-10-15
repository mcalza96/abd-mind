"""Experimentos disponibles desde la CLI (ADR-0006: corren sin Hermes)."""

from collections.abc import Callable

from factory.config import Config
from factory.experiments import (
    cilindro,
    comparacion_puntuacion,
    con_llm,
    expansion,
    finanzas,
    reservado,
    robustez,
    salas,
    tercer_observador,
)
from factory.experiments.base import ResultadoExperimento
from factory.transition.stochastic.llm_client import ClienteLLM

# Sin LLM: deterministas, corren en CI.
EXPERIMENTOS: dict[str, Callable[[], ResultadoExperimento]] = {
    "cilindro": cilindro.ejecutar,
    "expansion": expansion.ejecutar,
    "tercer-observador": tercer_observador.ejecutar,
    "errata": robustez.errata,
    "empate": robustez.empate,
    "reservado": reservado.ejecutar,
    "salas": salas.ejecutar,
    "puntuacion": comparacion_puntuacion.ejecutar,
}

# Con LLM: requieren proveedor configurado.
EXPERIMENTOS_LLM: dict[str, Callable[[Config, ClienteLLM], ResultadoExperimento]] = {
    "cilindro-llm": con_llm.cilindro_llm,
    "expansion-llm": con_llm.expansion_llm,
    "finanzas-llm": lambda config, cliente: finanzas.finanzas_llm(
        config, cliente.transporte, cliente.cache
    ),
}
