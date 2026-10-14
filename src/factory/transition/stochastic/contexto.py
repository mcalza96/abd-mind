"""Descripción textual del dominio y del caso para los prompts."""

import json

from factory.contracts.abduction import HipotesisCandidata
from factory.contracts.observation import Observacion, Observador
from factory.contracts.rules import ConjuntoReglas


def describir_dominio(dominio: ConjuntoReglas) -> str:
    lineas = [f"Dominio: {dominio.dominio}"]
    if dominio.descripcion:
        lineas.append(dominio.descripcion)
    if dominio.variables:
        lineas.append("\nVariables del dominio (usa solo estas en 'afirmaciones' y 'variables'):")
        for nombre, v in dominio.variables.items():
            valores = f" Valores admitidos: {', '.join(map(str, v.valores))}." if v.valores else ""
            lineas.append(f"- {nombre} ({v.tipo}): {v.descripcion}.{valores}")
    if dominio.reglas:
        lineas.append("\nLeyes invariantes del dominio (una hipótesis que las viola se descarta):")
        lineas += [f"- {r.descripcion}" for r in dominio.reglas]
    return "\n".join(lineas)


def describir_observador(o: Observador) -> str:
    partes = [f"{o.id} — {o.nombre}"]
    if o.marco:
        partes.append(f"marco: {o.marco}")
    if o.parametros:
        partes.append(f"parámetros: {json.dumps(o.parametros, ensure_ascii=False)}")
    return "; ".join(partes)


def describir_observaciones(
    observadores: dict[str, Observador], observaciones: list[Observacion]
) -> str:
    lineas = ["Observadores:"]
    lineas += [f"- {describir_observador(o)}" for o in observadores.values()]
    lineas.append("\nObservaciones (cada una es un hecho reportado por su observador):")
    for obs in observaciones:
        extra = f" [valor: {obs.valor}]" if obs.valor is not None else ""
        lineas.append(f"- {obs.id} (observador {obs.observador_id}): {obs.contenido}{extra}")
    return "\n".join(lineas)


def describir_hipotesis(h: HipotesisCandidata) -> str:
    afirmaciones = json.dumps(h.afirmaciones, ensure_ascii=False)
    return f"- {h.id_hipotesis}: {h.mecanismo_latente} | afirmaciones: {afirmaciones}"
