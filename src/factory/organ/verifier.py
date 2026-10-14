"""Interfaz de los verificadores de consistencia π_i(H) ≈ y_i (ADR-0002).

En entornos sintéticos la implementa `organ.projections.VerificadorProyeccion`. En dominios
reales la implementará un verificador basado en LLM, independiente del generador (fase 3).
"""

from typing import Protocol

from factory.contracts.abduction import HipotesisCandidata
from factory.contracts.case import Veredicto
from factory.contracts.observation import Observacion, Observador


class Verificador(Protocol):
    def verificar(
        self, hipotesis: HipotesisCandidata, observacion: Observacion, observador: Observador
    ) -> Veredicto: ...
