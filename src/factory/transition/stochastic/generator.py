"""Generador de hipótesis: muestreo contrastivo y expansión ontológica (06 §6.4)."""

from enum import StrEnum

from pydantic import BaseModel, Field

from factory.config import ConfigRol
from factory.contracts.abduction import HipotesisCandidata, Valor
from factory.contracts.observation import Observacion, Observador
from factory.contracts.rules import ConjuntoReglas
from factory.organ.texto import normalizar
from factory.transition.stochastic.contexto import (
    describir_dominio,
    describir_hipotesis,
    describir_observaciones,
)
from factory.transition.stochastic.esquemas import GeneracionLLM, HipotesisLLM, a_diccionario
from factory.transition.stochastic.llm_client import ClienteLLM, ErrorLLM

SISTEMA = """Eres un generador de hipótesis abductivas. Distintos observadores reportan cosas \
que parecen incompatibles. Cada observación es una proyección del mismo estado real del mundo \
a través del marco de su observador (su perspectiva, instrumento o método), no ruido.

Tu tarea es proponer hipótesis sobre el estado real o mecanismo causal que, si fuera cierto, \
haría esperables TODAS las observaciones, cada una desde el marco de su observador.

Reglas:
- No promedies ni mezcles las observaciones: una postura intermedia no es una explicación.
- Las hipótesis deben ser mutuamente excluyentes entre sí y distintas de las ya existentes.
- Incluye alternativas poco convencionales; no te limites a la más obvia.
- En 'afirmaciones' fija las variables del dominio que la hipótesis determina (solo variables \
de la lista; para variables de tipo entidad usa el nombre en minúsculas, sin tildes y con \
guiones bajos).
- En 'entidades_latentes' declara toda entidad o mecanismo que postulas y que NO está en el \
vocabulario conocido. Cada entidad nueva tiene un costo: postúlala solo si hace falta.
- En 'observaciones_explicadas' lista los ids de las observaciones que la hipótesis explica.
- En 'predicados_de_consistencia' enuncia las condiciones que la hipótesis asume."""

INSTRUCCION_MODO = {
    "contrastivo": (
        "Propón {n} hipótesis. Prioriza las que expliquen todas las observaciones con el "
        "vocabulario conocido."
    ),
    "expansion": (
        "Ninguna hipótesis formulada con el vocabulario conocido explica todas las "
        "observaciones. Propón {n} hipótesis que postulen al menos una entidad, objeto o "
        "mecanismo NUEVO (fuera del vocabulario conocido) capaz de explicarlas todas, y "
        "declárala en 'entidades_latentes'."
    ),
}


class ModoGeneracion(StrEnum):
    CONTRASTIVO = "contrastivo"
    EXPANSION = "expansion"


class ContextoGeneracion(BaseModel):
    dominio: ConjuntoReglas
    observadores: dict[str, Observador]
    observaciones: list[Observacion]
    existentes: list[HipotesisCandidata] = Field(default_factory=list)
    vocabulario: set[str] = Field(default_factory=set)


class ResultadoGeneracion(BaseModel):
    hipotesis: list[HipotesisCandidata] = Field(default_factory=list)
    avisos: list[str] = Field(default_factory=list)


def _firma(afirmaciones: dict[str, Valor]) -> frozenset[tuple[str, str]]:
    return frozenset((normalizar(k), normalizar(str(v))) for k, v in afirmaciones.items())


class Generador:
    def __init__(self, cliente: ClienteLLM, roles: list[ConfigRol]) -> None:
        self.cliente = cliente
        self.roles = roles

    def generar(
        self, contexto: ContextoGeneracion, n_por_modelo: int, modo: ModoGeneracion
    ) -> ResultadoGeneracion:
        resultado = ResultadoGeneracion()
        firmas = {
            _firma(h.afirmaciones): h.id_hipotesis for h in contexto.existentes if h.afirmaciones
        }
        ids = {h.id_hipotesis for h in contexto.existentes}

        for rol in self.roles:
            # Cada modelo ve también lo que propusieron los anteriores en esta ronda.
            vistas = [*contexto.existentes, *resultado.hipotesis]
            try:
                bruto = self.cliente.completar_json(
                    rol, SISTEMA, self._prompt(contexto, vistas, n_por_modelo, modo), GeneracionLLM
                )
            except ErrorLLM as e:
                resultado.avisos.append(f"{rol.modelo}: {e}")
                continue
            for propuesta in bruto.hipotesis:
                h, avisos = self._convertir(propuesta, rol.modelo, contexto.dominio, ids)
                resultado.avisos += avisos
                firma = _firma(h.afirmaciones)
                if h.afirmaciones and firma in firmas:
                    resultado.avisos.append(
                        f"{rol.modelo}: hipótesis descartada por repetir las afirmaciones de "
                        f"{firmas[firma]} ({h.mecanismo_latente})"
                    )
                    continue
                if h.afirmaciones:
                    firmas[firma] = h.id_hipotesis
                ids.add(h.id_hipotesis)
                resultado.hipotesis.append(h)
        return resultado

    @staticmethod
    def _prompt(
        contexto: ContextoGeneracion,
        vistas: list[HipotesisCandidata],
        n: int,
        modo: ModoGeneracion,
    ) -> str:
        partes = [
            describir_dominio(contexto.dominio),
            describir_observaciones(contexto.observadores, contexto.observaciones),
            "Vocabulario conocido (entidades verificadas): "
            + (", ".join(sorted(contexto.vocabulario)) or "(vacío)"),
        ]
        if vistas:
            partes.append(
                "Hipótesis ya existentes (no las repitas):\n"
                + "\n".join(describir_hipotesis(h) for h in vistas)
            )
        partes.append(INSTRUCCION_MODO[modo].format(n=n))
        return "\n\n".join(partes)

    @staticmethod
    def _convertir(
        propuesta: HipotesisLLM, modelo: str, dominio: ConjuntoReglas, ids: set[str]
    ) -> tuple[HipotesisCandidata, list[str]]:
        avisos = []
        afirmaciones = a_diccionario(propuesta.afirmaciones)
        if dominio.variables:
            for nombre in sorted(set(afirmaciones) - set(dominio.variables)):
                del afirmaciones[nombre]
                avisos.append(f"{modelo}: se ignoró la variable desconocida '{nombre}'")
        n = len(ids) + 1
        while f"h{n}" in ids:
            n += 1
        return (
            HipotesisCandidata(
                id_hipotesis=f"h{n}",
                mecanismo_latente=propuesta.mecanismo_latente,
                entidades_latentes=propuesta.entidades_latentes,
                observaciones_explicadas=propuesta.observaciones_explicadas,
                predicados_de_consistencia=propuesta.predicados_de_consistencia,
                afirmaciones=afirmaciones,
                origen=f"motor:{modelo}",
            ),
            avisos,
        )
