"""Interfaz de los verificadores de consistencia π_i(H) ≈ y_i (ADR-0002).

En entornos sintéticos la implementa `organ.projections.VerificadorProyeccion`. En dominios
reales, `VerificadorLLM`: un modelo distinto del generador, una observación por llamada.
"""

import json
from typing import Protocol

from factory.config import ConfigRol
from factory.contracts.abduction import HipotesisCandidata
from factory.contracts.case import Relacion, Veredicto
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

Suponiendo que la hipótesis es verdadera, decide qué relación tiene con esta observación:
- "explica": la hipótesis hace esperable que este observador, desde su marco, reporte \
exactamente esto.
- "contradice": la hipótesis hace esperar que este observador reporte otra cosa; la observación \
es difícil de conciliar con ella.
- "neutral": la hipótesis no dice nada sobre lo que este observador reportaría; la observación \
sería igual de esperable con o sin ella.

Reglas:
- No juzgues si la hipótesis es plausible o probable; solo su relación con esta observación.
- Que la observación sea compatible con la hipótesis no basta para "explica": la hipótesis debe \
dar razones para esperarla. Si no las da y tampoco la vuelve improbable, es "neutral".
- Reserva "contradice" para cuando la hipótesis predice algo distinto de lo observado.
- Considera el marco del observador: lo que puede ver o medir desde su posición o método.
- Primero razona brevemente en 'justificacion' y luego da la relación."""


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
            relacion=Relacion(bruto.relacion),
            fuente=self.fuente,
            justificacion=bruto.justificacion,
        )
