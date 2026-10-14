"""Experimentos disponibles desde la CLI (ADR-0006: corren sin Hermes)."""

from collections.abc import Callable

from factory.experiments import cilindro, expansion, tercer_observador
from factory.experiments.base import ResultadoExperimento

EXPERIMENTOS: dict[str, Callable[[], ResultadoExperimento]] = {
    "cilindro": cilindro.ejecutar,
    "expansion": expansion.ejecutar,
    "tercer-observador": tercer_observador.ejecutar,
}
