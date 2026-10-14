"""Informe de auditoría en Markdown (para enviarlo como archivo por Telegram)."""

import json
import math

from factory.contracts.case import EstadoHipotesis
from factory.engine.modelos import Auditoria


def _score(valor: float) -> str:
    return "−∞" if valor == -math.inf else f"{valor:.2f}"


def auditoria_markdown(a: Auditoria) -> str:
    caso = a.caso
    lineas = [
        f"# Auditoría {caso.caso_id}",
        "",
        f"**Descripción:** {caso.descripcion}",
        f"**Dominio:** {caso.dominio} (reglas v{caso.version_reglas}) · **Estado:** {caso.estado}"
        f" · **Llamadas LLM:** {caso.llamadas}",
        f"**Pesos:** α={caso.pesos.alpha}, β={caso.pesos.beta}, γ={caso.pesos.gamma},"
        f" τ={caso.pesos.tau}",
    ]
    lineas += [f"> Aviso: {aviso}" for aviso in caso.avisos]

    h = caso.resumen.h_estrella
    lineas += ["", "## Mejor explicación", ""]
    if h is None:
        lineas.append("Sin explicación suficiente en la última evaluación.")
    else:
        lineas += [
            f"**{h.id_hipotesis}: {h.mecanismo}**",
            "",
            f"C = {h.consiliencia_c}, P = {h.parsimonia_p}, K = {h.coherencia_k:g},"
            f" score = {_score(h.score_final)}",
        ]
    if not caso.evaluacion_vigente:
        lineas.append("_Hubo cambios desde la última evaluación._")

    lineas += ["", "## Observadores", ""]
    for o in a.observadores:
        lineas.append(f"- **{o.nombre}** (`{o.id}`){f' — {o.marco}' if o.marco else ''}")
        for opinion in a.opiniones.get(o.id, []):
            lineas.append(f"  - opinión (no es evidencia): {opinion}")

    lineas += ["", "## Hechos", "", "| Id | Observador | Hecho | Estado |", "|---|---|---|---|"]
    for obs in a.observaciones:
        lineas.append(f"| {obs.id} | {obs.observador_id} | {obs.contenido} | {obs.estado.value} |")

    veredictos: dict[str, dict[str, bool]] = {}
    for v in a.veredictos:
        veredictos.setdefault(v.id_hipotesis, {})[v.id_observacion] = v.explica
    lineas += ["", "## Hipótesis", ""]
    for hip in a.hipotesis:
        estado = hip.estado.value
        if hip.estado is EstadoHipotesis.DERROTADA:
            estado += f" por {', '.join(hip.derrotada_por)}"
        explica = sorted(i for i, ok in veredictos.get(hip.id_hipotesis, {}).items() if ok)
        lineas += [
            f"### {hip.id_hipotesis} — {estado}",
            "",
            hip.mecanismo,
            "",
            f"- Origen: {hip.origen}",
            f"- Entidades latentes: {', '.join(hip.entidades_latentes) or '—'}",
            f"- Afirmaciones: `{json.dumps(hip.afirmaciones, ensure_ascii=False)}`",
            f"- Explica: {', '.join(explica) or '—'}",
            "",
        ]

    lineas += ["## Veredictos", "", "| Hipótesis | Hecho | Explica | Fuente | Justificación |"]
    lineas.append("|---|---|---|---|---|")
    for v in a.veredictos:
        justificacion = v.justificacion.replace("|", "\\|").replace("\n", " ")
        lineas.append(
            f"| {v.id_hipotesis} | {v.id_observacion} | {'sí' if v.explica else 'no'} "
            f"| {v.fuente} | {justificacion} |"
        )

    lineas += ["", "## Eventos", ""]
    for e in a.eventos:
        lineas.append(f"- {e['momento']} · {e['tipo']}")
    return "\n".join(lineas) + "\n"
