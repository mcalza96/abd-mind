"""Experimentos disponibles desde la CLI (ADR-0006: corren sin Hermes)."""

from collections.abc import Callable

from factory.config import Config
from factory.experiments import cilindro, con_llm, expansion, tercer_observador
from factory.experiments.base import ResultadoExperimento
from factory.transition.stochastic.llm_client import ClienteLLM

# Sin LLM: deterministas, corren en CI.
EXPERIMENTOS: dict[str, Callable[[], ResultadoExperimento]] = {
    "cilindro": cilindro.ejecutar,
    "expansion": expansion.ejecutar,
    "tercer-observador": tercer_observador.ejecutar,
}

# Con LLM: requieren proveedor configurado.
EXPERIMENTOS_LLM: dict[str, Callable[[Config, ClienteLLM], ResultadoExperimento]] = {
    "cilindro-llm": con_llm.cilindro_llm,
    "expansion-llm": con_llm.expansion_llm,
}
