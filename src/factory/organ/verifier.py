"""Interfaz de los verificadores de consistencia π_i(H) ≈ y_i (ADR-0002).

En entornos sintéticos la implementa `organ.projections.VerificadorProyeccion`. En dominios
reales, `VerificadorComparativo` (ADR-0015): un modelo distinto del generador califica cada
observación contra todas las hipótesis rivales a la vez. `VerificadorLLM` (un par por llamada)
queda para comparaciones y experimentos.
"""

import json
from collections.abc import Callable
from typing import Protocol

from factory.config import ConfigRol
from factory.contracts.abduction import HipotesisCandidata
from factory.contracts.case import Relacion, Veredicto
from factory.contracts.observation import Observacion, Observador
from factory.transition.stochastic.contexto import describir_observador
from factory.transition.stochastic.esquemas import ComparacionLLM, VeredictoLLM
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


SISTEMA_COMPARATIVO = """Eres un verificador independiente en un sistema de razonamiento \
abductivo. Recibes UN observador con su marco, UNA observación de ese observador y VARIAS \
hipótesis rivales.

Para cada hipótesis, suponiendo que fuera la verdadera, califica cuán esperable sería que este \
observador, desde su marco, reportara exactamente esta observación:
- "muy_esperable": la hipótesis predice esta observación de forma específica; sin ella sería \
sorprendente.
- "esperable": la hipótesis la hace más probable que no, aunque no la predice específicamente.
- "indiferente": la observación sería igual de esperable sin la hipótesis, o la hipótesis solo \
la acomoda con una cláusula agregada para ese fin (por ejemplo, "no deja rastro").
- "inesperado": la hipótesis lleva a esperar que el observador reportara otra cosa.

Reglas:
- Compara las hipótesis entre sí: una observación que todas predicen igual no distingue a \
ninguna; reserva "muy_esperable" para las que la predicen mejor que sus rivales.
- No juzgues si la hipótesis es plausible; solo cuán esperable hace esta observación.
- Considera el marco del observador: lo que puede ver o medir desde su posición o método.
- Califica TODAS las hipótesis, una vez cada una, usando su id. Primero razona brevemente en \
'justificacion'."""

RELACION_DE_NIVEL = {
    "muy_esperable": Relacion.EXPLICA,
    "esperable": Relacion.EXPLICA,
    "indiferente": Relacion.NEUTRAL,
    "inesperado": Relacion.CONTRADICE,
}


class VerificadorComparativo:
    """Califica una observación contra todas las hipótesis vivas a la vez (13 §13.2, ADR-0015).

    `hipotesis_vivas` entrega el conjunto actual. La primera vez que se pide un par
    (hipótesis, observación) se califican juntas todas las hipótesis vivas sin calificación
    previa para esa observación; las ya calificadas van como contexto y no se recalifican.
    """

    def __init__(
        self,
        cliente: ClienteLLM,
        rol: ConfigRol,
        hipotesis_vivas: Callable[[], list[HipotesisCandidata]],
        peso_esperable: float = 0.5,
    ) -> None:
        self.cliente = cliente
        self.rol = rol
        self.hipotesis_vivas = hipotesis_vivas
        self.peso_esperable = peso_esperable
        self.fuente = f"verificador:{rol.modelo}"
        self._calificadas: dict[tuple[str, str], Veredicto] = {}

    def verificar(
        self, hipotesis: HipotesisCandidata, observacion: Observacion, observador: Observador
    ) -> Veredicto:
        clave = (hipotesis.id_hipotesis, observacion.id)
        if clave not in self._calificadas:
            self._calificar(hipotesis, observacion, observador)
        return self._calificadas[clave]

    def _calificar(
        self, pedida: HipotesisCandidata, observacion: Observacion, observador: Observador
    ) -> None:
        candidatas = {h.id_hipotesis: h for h in self.hipotesis_vivas()}
        candidatas[pedida.id_hipotesis] = pedida
        partes = [
            f"Observador: {describir_observador(observador)}",
            f"Observación: {observacion.contenido}",
        ]
        if observacion.valor is not None and observacion.valor != observacion.contenido:
            partes.append(f"Valor observado: {observacion.valor}")
        partes.append("Hipótesis rivales:")
        partes += [
            f"- {h.id_hipotesis}: {h.mecanismo_latente} | afirmaciones: "
            f"{json.dumps(h.afirmaciones, ensure_ascii=False)}"
            for h in candidatas.values()
        ]
        bruto = self.cliente.completar_json(
            self.rol, SISTEMA_COMPARATIVO, "\n".join(partes), ComparacionLLM
        )
        for c in bruto.calificaciones:
            clave = (c.id_hipotesis, observacion.id)
            if c.id_hipotesis not in candidatas or clave in self._calificadas:
                continue
            self._calificadas[clave] = Veredicto(
                id_hipotesis=c.id_hipotesis,
                id_observacion=observacion.id,
                relacion=RELACION_DE_NIVEL[c.nivel],
                nivel=c.nivel,
                peso=self.peso_esperable if c.nivel == "esperable" else 1.0,
                fuente=self.fuente,
                justificacion=c.justificacion,
            )
        clave = (pedida.id_hipotesis, observacion.id)
        if clave not in self._calificadas:
            # El modelo omitió la hipótesis pedida: se trata como sin juicio (neutral).
            self._calificadas[clave] = Veredicto(
                id_hipotesis=pedida.id_hipotesis,
                id_observacion=observacion.id,
                relacion=Relacion.NEUTRAL,
                nivel="sin_calificar",
                fuente=self.fuente,
                justificacion="el verificador no calificó esta hipótesis",
            )
