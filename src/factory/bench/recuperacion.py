"""EXP-016: ¿los generadores recuperan la explicación verdadera en casos reales (conjunto R)?

Tres pasos, separados para que la verdad de referencia quede fijada antes de generar:

1. `preparar`: sanea los casos con las reglas registradas (sin observaciones fechadas el día de
   la resolución o después, ni de fuentes posteriores) y escribe `casos.jsonl`.
2. `generar`: pide a cada generador 10 explicaciones ordenadas, con la pregunta libre y la
   diversa, en varias corridas sin caché. Guarda cada respuesta al llegar (se puede reanudar).
3. `medir`: con los juicios del juez ciego, calcula núcleo@k y la cobertura de elementos.
"""

import json
import math
import re
import threading
from collections.abc import Iterable
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from typing import Any

from pydantic import BaseModel, Field

from factory.config import Config, ConfigRol
from factory.transition.stochastic.llm_client import ClienteLLM, ErrorLLM

PREGUNTAS = {
    "libre": (
        "Propón las 10 explicaciones más probables del mecanismo que causó lo ocurrido, "
        "ordenadas de más a menos probable."
    ),
    "diversa": (
        "Propón 10 explicaciones del mecanismo que causó lo ocurrido, muy distintas entre sí, "
        "incluyendo hipótesis poco convencionales que un experto consideraría. Ordénalas de más "
        "a menos probable."
    ),
}

SISTEMA = """Recibes observaciones de distintas fuentes sobre un incidente, tal como se \
reportaron en su momento, con su fecha. Cada explicación debe ser un mecanismo causal concreto \
(qué pasó y por qué produjo lo observado), en una o dos frases. No repitas explicaciones."""


class ListaExplicaciones(BaseModel):
    explicaciones: list[str] = Field(min_length=5, max_length=15)


# --- 1. preparar ------------------------------------------------------------------------------

_FECHA_URL = re.compile(r"/(20\d\d)[/-](\d\d)(?:[/-](\d\d))?(?:[/-]|$)")


def fecha_de_url(url: str) -> str | None:
    """Fecha que aparece en la ruta de una URL (AAAA-MM o AAAA-MM-DD), si la hay."""
    m = _FECHA_URL.search(url)
    if not m:
        return None
    anio, mes, dia = m.groups()
    return f"{anio}-{mes}-{dia}" if dia else f"{anio}-{mes}"


def posterior_o_igual(fecha: str, referencia: str) -> bool:
    """Compara con la precisión de la fecha más corta (mes o día)."""
    n = min(len(fecha), len(referencia))
    return fecha[:n] >= referencia[:n]


def sanear(caso: dict[str, Any]) -> tuple[list[dict[str, Any]], list[dict[str, str]]]:
    resolucion = caso["resolucion"]["fecha"]
    quedan, quitadas = [], []
    for o in caso["observaciones"]:
        url = fecha_de_url(o.get("fuente") or "")
        if posterior_o_igual(o["fecha"], resolucion):
            quitadas.append(
                {"contenido": o["contenido"], "razon": "fechada en o tras la resolución"}
            )
        elif url is not None and posterior_o_igual(url, resolucion):
            quitadas.append({"contenido": o["contenido"], "razon": f"fuente fechada {url}"})
        else:
            quedan.append(o)
    return quedan, quitadas


def preparar(origen: Path, destino: Path) -> list[dict[str, Any]]:
    casos = []
    for linea in origen.read_text(encoding="utf-8").splitlines():
        if not linea.strip():
            continue
        crudo = json.loads(linea)
        if crudo["conjunto"] != "R":
            continue
        quedan, quitadas = sanear(crudo)
        marcos = {o["id"]: o["marco"] for o in crudo["observadores"]}
        casos.append(
            {
                "id": crudo["id"],
                "observaciones": [
                    {
                        "observador": o["observador"],
                        "marco": marcos.get(o["observador"], ""),
                        "fecha": o["fecha"],
                        "contenido": o["contenido"],
                    }
                    for o in sorted(quedan, key=lambda o: o["fecha"])
                ],
                "quitadas": quitadas,
                "resolucion": crudo["resolucion"]["mecanismo"],
                "fecha_resolucion": crudo["resolucion"]["fecha"],
                "fuera": len({o["observador"] for o in quedan}) < 1 or len(quedan) < 2,
            }
        )
    destino.mkdir(parents=True, exist_ok=True)
    with (destino / "casos.jsonl").open("w", encoding="utf-8") as f:
        for c in casos:
            f.write(json.dumps(c, ensure_ascii=False) + "\n")
    return casos


def describir(caso: dict[str, Any]) -> str:
    """Lo que ve el generador: observaciones con su fecha y el marco de cada fuente."""
    lineas = ["Observaciones (tal como se reportaron en su momento):"]
    for o in caso["observaciones"]:
        lineas.append(f"- [{o['fecha']}] Fuente {o['observador']} ({o['marco']}): {o['contenido']}")
    return "\n".join(lineas)


# --- 2. generar -------------------------------------------------------------------------------


def _leer_jsonl(ruta: Path) -> list[dict[str, Any]]:
    if not ruta.exists():
        return []
    return [json.loads(x) for x in ruta.read_text(encoding="utf-8").splitlines() if x.strip()]


def generar(
    config: Config,
    roles: list[ConfigRol],
    casos: list[dict[str, Any]],
    destino: Path,
    corridas: int = 3,
    paralelo: int = 4,
) -> None:
    ruta = destino / "generaciones.jsonl"
    hechas = {(g["caso"], g["modelo"], g["pregunta"], g["corrida"]) for g in _leer_jsonl(ruta)}
    sin_cache = config.model_copy(update={"cache_dir": None})
    tareas = [
        (c, r, p, k)
        for c in casos
        if not c["fuera"]
        for r in roles
        for p in PREGUNTAS
        for k in range(1, corridas + 1)
        if (c["id"], r.modelo, p, k) not in hechas
    ]
    candado = threading.Lock()

    def una(tarea: tuple[dict[str, Any], ConfigRol, str, int]) -> None:
        caso, rol, pregunta, corrida = tarea
        cliente = ClienteLLM(sin_cache, cache=None, max_llamadas=4)
        usuario = f"{describir(caso)}\n\n{PREGUNTAS[pregunta]}"
        registro: dict[str, Any] = {
            "caso": caso["id"],
            "modelo": rol.modelo,
            "pregunta": pregunta,
            "corrida": corrida,
        }
        try:
            lista, respondio = cliente.completar_json_con_modelo(
                rol, SISTEMA, usuario, ListaExplicaciones
            )
            registro |= {"respondio": respondio, "explicaciones": lista.explicaciones[:10]}
        except ErrorLLM as e:
            registro |= {"error": str(e)[:500]}
        except Exception as e:  # se registra y la corrida sigue
            registro |= {"error": f"{type(e).__name__}: {e}"[:500]}
        with candado, ruta.open("a", encoding="utf-8") as f:
            f.write(json.dumps(registro, ensure_ascii=False) + "\n")

    with ThreadPoolExecutor(max_workers=paralelo) as pool:
        list(pool.map(una, tareas))


# --- 3. medir ---------------------------------------------------------------------------------


def wilson(exitos: float, n: int, z: float = 1.96) -> tuple[float, float]:
    if n == 0:
        return (0.0, 0.0)
    p = exitos / n
    centro = (p + z * z / (2 * n)) / (1 + z * z / n)
    margen = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / (1 + z * z / n)
    return (max(0.0, centro - margen), min(1.0, centro + margen))


def nucleo_en(juicios: Iterable[dict[str, str]], k: int, aceptar: set[str]) -> bool:
    """¿Alguna de las k primeras candidatas cubre el núcleo? `juicios` en orden de la lista."""
    return any(j["nucleo"] in aceptar for j in list(juicios)[:k])


# --- juez ciego -------------------------------------------------------------------------------

RUBRICA = """Eres un juez ciego. Para cada caso tienes los ELEMENTOS CLAVE del mecanismo \
documentado y varias LISTAS de explicaciones candidatas, identificadas con códigos (no sabes \
quién ni cómo las generó). Para cada candidata y cada elemento decide si la candidata lo cubre:
- "si": la candidata afirma ese mismo eslabón causal (puede usar otras palabras, pero el \
mecanismo concreto es el mismo).
- "parcial": apunta a la misma zona o pieza pero sin el eslabón concreto (p. ej. "falla en el \
sistema de control del elevador" frente a "el tapón suelto trabó el elevador").
- "no": no lo menciona, o afirma algo distinto.
Cubrir el tema no basta: se exige el eslabón causal. Juzga cada candidata por sí sola."""


def preparar_juez(
    destino: Path, referencia: dict[str, list[str]] | None, grupos: int, semilla: int = 16
) -> list[Path]:
    """Mezcla las listas con códigos opacos y escribe una entrada por grupo de casos.

    La clave código → condición queda en `clave_juez.json`, que el juez no ve.
    """
    import random

    rng = random.Random(semilla)
    casos = {c["id"]: c for c in _leer_jsonl(destino / "casos.jsonl") if not c["fuera"]}
    elementos = {
        c["id"]: c["elementos"]
        for c in json.loads((destino / "elementos.json").read_text(encoding="utf-8"))["casos"]
    }
    listas: dict[str, list[tuple[dict[str, Any], list[str]]]] = {i: [] for i in casos}
    for g in _leer_jsonl(destino / "generaciones.jsonl"):
        if g.get("explicaciones") and g["caso"] in listas:
            condicion = {k: g[k] for k in ("modelo", "pregunta", "corrida")}
            listas[g["caso"]].append((condicion, g["explicaciones"]))
    for caso_id, explicaciones in (referencia or {}).items():
        if caso_id in listas:
            condicion = {"modelo": "referencia", "pregunta": "libre", "corrida": 1}
            listas[caso_id].append((condicion, explicaciones[:10]))
    clave: dict[str, Any] = {}
    ids = sorted(listas)
    rng.shuffle(ids)
    rutas = []
    for n in range(grupos):
        partes = [RUBRICA, ""]
        partes.append(
            'Responde SOLO con JSON: {"listas": [{"codigo": "...", "juicios": '
            '[{"pos": 1, "e1": "si|parcial|no", "e2": "..."}]}]}, con un juicio por candidata, '
            "en el orden de la lista."
        )
        for caso_id in ids[n::grupos]:
            partes.append(f"\n## Caso {caso_id}\nElementos clave:")
            partes += [f"- {e['id']}: {e['texto']}" for e in elementos[caso_id]]
            mezcla = listas[caso_id][:]
            rng.shuffle(mezcla)
            for condicion, explicaciones in mezcla:
                codigo = f"{caso_id}-{rng.randrange(16**6):06x}"
                clave[codigo] = {"caso": caso_id, **condicion}
                partes.append(f"\n### Lista {codigo}")
                partes += [f"{i}. {texto}" for i, texto in enumerate(explicaciones, start=1)]
        ruta = destino / f"juez-entrada-{n + 1}.md"
        ruta.write_text("\n".join(partes), encoding="utf-8")
        rutas.append(ruta)
    (destino / "clave_juez.json").write_text(
        json.dumps(clave, ensure_ascii=False, indent=1), encoding="utf-8"
    )
    return rutas


def medir(destino: Path) -> str:
    """Informe en Markdown a partir de los juicios y la clave."""
    clave = json.loads((destino / "clave_juez.json").read_text(encoding="utf-8"))
    nucleo = {
        c["id"]: next(e["id"] for e in c["elementos"] if e["nucleo"])
        for c in json.loads((destino / "elementos.json").read_text(encoding="utf-8"))["casos"]
    }
    inferencia = {
        c["id"]: c
        for c in json.loads((destino / "inferibilidad.json").read_text(encoding="utf-8"))["casos"]
    }

    def grupo(caso: str) -> str:
        inf = inferencia[caso]
        nivel = next(e["inferible"] for e in inf["elementos"] if e["id"] == nucleo[caso])
        if inf.get("trivial"):
            return "trivial"
        return "principal" if nivel in ("si", "parcial") else "no inferible"

    filas: list[dict[str, Any]] = []
    for linea in _leer_jsonl(destino / "juicios.jsonl"):
        cond = clave[linea["codigo"]]
        orden = sorted(linea["juicios"], key=lambda j: j["pos"])
        n = nucleo[cond["caso"]]
        elementos = [k for k in orden[0] if k != "pos"] if orden else []
        filas.append(
            {
                **cond,
                "grupo": grupo(cond["caso"]),
                "pos_si": next((j["pos"] for j in orden if j.get(n) == "si"), None),
                "pos_parcial": next(
                    (j["pos"] for j in orden if j.get(n) in ("si", "parcial")), None
                ),
                "cobertura10": (
                    sum(any(j.get(e) == "si" for j in orden[:10]) for e in elementos)
                    / len(elementos)
                    if elementos
                    else 0.0
                ),
            }
        )
    return _informe(filas)


def _informe(filas: list[dict[str, Any]]) -> str:
    def tasa(sel: list[dict[str, Any]], k: int, campo: str = "pos_si") -> str:
        if not sel:
            return "—"
        ok = sum(1 for f in sel if f[campo] is not None and f[campo] <= k)
        bajo, alto = wilson(ok, len(sel))
        return f"{ok}/{len(sel)} = {ok / len(sel):.0%} [{bajo:.0%}–{alto:.0%}]"

    lineas = ["# EXP-016 — Informe", ""]
    condiciones = sorted({(f["modelo"], f["pregunta"]) for f in filas})
    for nombre_grupo in ("principal", "no inferible", "trivial"):
        sel_g = [f for f in filas if f["grupo"] == nombre_grupo]
        if not sel_g:
            continue
        casos = sorted({f["caso"] for f in sel_g})
        lineas += [
            f"## Grupo {nombre_grupo} ({len(casos)} casos: {', '.join(casos)})",
            "",
            "| Modelo | Pregunta | núcleo@1 | núcleo@5 | núcleo@10 | núcleo@5 (con parcial) |"
            " Cobertura@10 |",
            "|---|---|---|---|---|---|---|",
        ]
        for modelo, pregunta in condiciones:
            sel = [f for f in sel_g if f["modelo"] == modelo and f["pregunta"] == pregunta]
            if not sel:
                continue
            cobertura = sum(f["cobertura10"] for f in sel) / len(sel)
            lineas.append(
                f"| {modelo} | {pregunta} | {tasa(sel, 1)} | {tasa(sel, 5)} | {tasa(sel, 10)} | "
                f"{tasa(sel, 5, 'pos_parcial')} | {cobertura:.0%} |"
            )
        lineas += ["", "Posición del núcleo por caso (`si`; — si no aparece):", ""]
        lineas += ["| Caso | " + " | ".join(f"{m} / {p}" for m, p in condiciones) + " |"]
        lineas += ["|---|" + "---|" * len(condiciones)]
        for caso in casos:
            celdas = []
            for modelo, pregunta in condiciones:
                pos = [
                    f["pos_si"]
                    for f in sel_g
                    if f["caso"] == caso and f["modelo"] == modelo and f["pregunta"] == pregunta
                ]
                celdas.append(", ".join("—" if p is None else str(p) for p in pos) or " ")
            lineas.append(f"| {caso} | " + " | ".join(celdas) + " |")
        lineas.append("")
    return "\n".join(lineas)
