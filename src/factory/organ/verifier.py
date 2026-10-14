"""Interfaz de los verificadores de consistencia π_i(H) ≈ y_i (ADR-0002).

En entornos sintéticos la implementa `organ.projections.VerificadorProyeccion`. En dominios
reales, `VerificadorLLM`: un modelo distinto del generador, una observación por llamada.
"""

import json
from typing import Protocol

from factory.config import ConfigRol
from factory.contracts.abduction import HipotesisCandidata
from factory.contracts.case import Veredicto
from factory.contracts.observation import Observacion, Observador
from factory.transition.stochastic.contexto import describir_observador
from factory.transition.stochastic.esquemas import VeredictoLLM
from factory.transition.stochastic.llm_client import ClienteLLM


class Verificador(Protocol):
    def verificar(
        self, hipotesis: HipotesisCandidata, observacion: Observacion, observador: Observador
    ) -> Veredicto: ...


SISTEMA_VERIFICADOR = """Eres un verificador independiente en un sistema de razonamiento \
abductivo. Recibes UNA hipótesis, UN observador con su marco y UNA observación de ese observador.

Decide si, suponiendo que la hipótesis es verdadera, este observador, desde su marco, habría \
reportado esta observación (explica = true) o no (explica = false).

Reglas:
- No juzgues si la hipótesis es plausible o probable; solo su consistencia con esta observación.
- Responde explica = false si la hipótesis contradice la observación o no da razones para \
esperarla.
- Considera el marco del observador: lo que puede ver o medir desde su posición o método.
- Primero razona brevemente en 'justificacion' y luego da el veredicto."""


class VerificadorLLM:
    """π_i aproximada por un modelo independiente del generador (03 §3.3.1, ADR-0002)."""

    def __init__(self, cliente: ClienteLLM, rol: ConfigRol) -> None:
        self.cliente = cliente
        self.rol = rol
        self.fuente = f"verificador:{rol.modelo}"

    def verificar(
        self, hipotesis: HipotesisCandidata, observacion: Observacion, observador: Observador
    ) -> Veredicto:
        afirmaciones = json.dumps(hipotesis.afirmaciones, ensure_ascii=False)
        partes = [
            f"Hipótesis: {hipotesis.mecanismo_latente}",
            f"Afirmaciones de la hipótesis: {afirmaciones}",
            f"Observador: {describir_observador(observador)}",
            f"Observación: {observacion.contenido}",
        ]
        if observacion.valor is not None:
            partes.append(f"Valor observado: {observacion.valor}")
        if observacion.variables:
            partes.append(
                f"Variables observadas: {json.dumps(observacion.variables, ensure_ascii=False)}"
            )
        bruto = self.cliente.completar_json(
            self.rol, SISTEMA_VERIFICADOR, "\n".join(partes), VeredictoLLM
        )
        return Veredicto(
            id_hipotesis=hipotesis.id_hipotesis,
            id_observacion=observacion.id,
            explica=bruto.explica,
            fuente=self.fuente,
            justificacion=bruto.justificacion,
        )
