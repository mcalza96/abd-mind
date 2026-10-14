"""Córtex perceptivo: separa hechos de opiniones en una observación cruda (D8)."""

from factory.config import ConfigRol
from factory.contracts.observation import ExtraccionObservacion, HechoExtraido, Observador
from factory.contracts.rules import ConjuntoReglas
from factory.transition.stochastic.contexto import describir_dominio, describir_observador
from factory.transition.stochastic.esquemas import ExtraccionLLM, a_diccionario
from factory.transition.stochastic.llm_client import ClienteLLM

SISTEMA = """Eres el córtex perceptivo de un sistema de razonamiento abductivo. Recibes lo que \
reportó un observador y lo separas en:

- hechos: lo que el observador afirma haber visto, medido o registrado. Un hecho por elemento, \
atómico y verificable, con las palabras del observador. Si un hecho fija explícitamente el valor \
de una variable del dominio, inclúyela en 'variables'; si no, deja 'variables' vacío.
- opiniones: juicios, recomendaciones, predicciones, valoraciones o interpretaciones causales del \
observador (por ejemplo "recomienda vender", "la empresa está en problemas").
- dudas: enunciados que no puedes clasificar con seguridad.

Reglas:
- No agregues hechos que el texto no contiene ni infieras causas.
- No conviertas una opinión en hecho ni al revés.
- No uses variables que no estén en la lista del dominio.
- Responde en el idioma del texto."""


class Cortex:
    def __init__(self, cliente: ClienteLLM, rol: ConfigRol) -> None:
        self.cliente = cliente
        self.rol = rol

    def extraer(
        self, observador: Observador, contenido: str, dominio: ConjuntoReglas
    ) -> ExtraccionObservacion:
        usuario = (
            f"{describir_dominio(dominio)}\n\nObservador: {describir_observador(observador)}\n\n"
            f"Texto reportado:\n<<<\n{contenido}\n>>>"
        )
        bruto = self.cliente.completar_json(self.rol, SISTEMA, usuario, ExtraccionLLM)

        hechos = []
        dudas = list(bruto.dudas)
        for h in bruto.hechos:
            variables = a_diccionario(h.variables)
            desconocidas = sorted(set(variables) - set(dominio.variables))
            for nombre in desconocidas:
                del variables[nombre]
                dudas.append(f"variable '{nombre}' no pertenece al dominio (en: {h.enunciado})")
            hechos.append(HechoExtraido(enunciado=h.enunciado, variables=variables))
        return ExtraccionObservacion(hechos=hechos, opiniones=bruto.opiniones, dudas=dudas)
