"""Valida campo/predicciones.csv antes de fusionar un PR (EXP-020).

Uso: python3 .github/scripts/validar_predicciones.py campo/predicciones.csv [--base main.csv]

Con --base compara contra la versión de main: lo ya predicho no se edita ni se borra.
Las filas con fecha >= CORTE deben cumplir además el formato de EXP-020.
Sale con código 1 y una línea por error si algo no cumple.
"""

import csv
import re
import sys
from datetime import date
from pathlib import Path

CORTE = date(2026, 10, 20)

COLUMNAS = [
    "id", "fecha", "nota", "dominio", "tipo", "afirmacion", "condicion", "fuente_resolucion",
    "probabilidad", "resolver_el", "familia", "comprobacion", "version_skill",
    "tasa_base", "tasa_base_fuente", "consenso",
    "resultado", "resuelta_el", "fuente_resultado",
]
RESOLUCION = {"resultado", "resuelta_el", "fuente_resultado"}

TIPOS = {"rebote-tras-caida", "evento-con-fecha", "nivel-a-plazo", "otro"}
FAMILIAS = {
    "obvia", "nada-que-explicar", "medicion", "seleccion", "mezcla", "tercero-comun",
    "decision", "tiempo", "umbral", "gemelo", "varias-causas",
}

# Una cláusula es «expresión operador valor»; las cláusulas se unen con Y u O en mayúscula.
CLAUSULA = re.compile(r"^(?P<izq>.+?)\s*(?:>=|<=|≥|≤|>|<|=)\s*(?:-?\d+(?:[.,]\d+)?%?|sí|no)$")
CONECTOR = re.compile(r"\s+(?:Y|O)\s+")
AMBIGUO = re.compile(r"\b(?:con|y|o|aprox\w*|alrededor|cerca)\b", re.IGNORECASE)


def fecha_iso(texto):
    try:
        return date.fromisoformat(texto)
    except ValueError:
        return None


def prob(texto):
    try:
        valor = float(texto)
    except ValueError:
        return None
    return valor if 0 <= valor <= 1 else None


def errores_condicion(condicion):
    if not condicion:
        return ["condicion vacía"]
    if condicion.count("(") != condicion.count(")"):
        return ["condicion con paréntesis desbalanceados"]
    errores = []
    for clausula in CONECTOR.split(condicion):
        clausula = clausula.strip()
        while clausula.startswith("(") and clausula.endswith(")"):
            clausula = clausula[1:-1].strip()
        m = CLAUSULA.match(clausula)
        if not m:
            errores.append(f"cláusula sin «expresión operador valor»: {clausula!r}")
        elif AMBIGUO.search(m["izq"]):
            errores.append(f"cláusula con conector o aproximación en palabras: {clausula!r}")
    return errores


def version_actual(raiz):
    texto = (raiz / "hermes/skills/abduccion/SKILL.md").read_text(encoding="utf-8")
    m = re.search(r"^version:\s*(\d+)\s*$", texto, re.MULTILINE)
    return int(m[1]) if m else None


def validar_fila(fila, raiz, version):
    e = []
    fecha = fecha_iso(fila["fecha"])
    if not re.fullmatch(r"P-\d{8}-\d{2}", fila["id"]):
        e.append("id no es P-AAAAMMDD-NN")
    if fecha is None:
        e.append("fecha no es AAAA-MM-DD")
    if not (raiz / fila["nota"]).is_file():
        e.append(f"nota no existe: {fila['nota']}")
    p = prob(fila["probabilidad"])
    if p is None or p in (0, 1):
        e.append("probabilidad fuera de (0, 1)")
    resolver = fecha_iso(fila["resolver_el"])
    if resolver is None or (fecha and resolver < fecha):
        e.append("resolver_el no es una fecha posterior a fecha")

    resuelta = fila["resultado"] != ""
    if fila["resultado"] not in ("", "0", "1", "anulada"):
        e.append("resultado no es 0, 1 ni anulada")
    if resuelta and (fecha_iso(fila["resuelta_el"]) is None or not fila["fuente_resultado"]):
        e.append("resuelta sin resuelta_el o sin fuente_resultado")
    if not resuelta and (fila["resuelta_el"] or fila["fuente_resultado"]):
        e.append("resuelta_el o fuente_resultado sin resultado")

    if fecha is None or fecha < CORTE:
        return e

    if fila["tipo"] not in TIPOS:
        e.append(f"tipo fuera de la lista: {sorted(TIPOS)}")
    if fila["familia"] not in FAMILIAS:
        e.append(f"familia fuera de la lista: {sorted(FAMILIAS)}")
    e += errores_condicion(fila["condicion"])
    for columna in ("fuente_resolucion", "comprobacion"):
        if not fila[columna]:
            e.append(f"{columna} vacía")
    if not fila["version_skill"].isdigit() or version is None or int(fila["version_skill"]) > version:
        e.append(f"version_skill no es una versión de la skill (actual: {version})")
    if fila["tasa_base"] and prob(fila["tasa_base"]) is None:
        e.append("tasa_base no es un número entre 0 y 1")
    if fila["tasa_base"] and not fila["tasa_base_fuente"]:
        e.append("tasa_base sin tasa_base_fuente")
    if fila["consenso"] and prob(fila["consenso"]) is None:
        e.append("consenso no es un número entre 0 y 1")
    return e


def leer(ruta):
    with open(ruta, newline="", encoding="utf-8") as f:
        lector = csv.DictReader(f)
        return lector.fieldnames, list(lector)


def validar(ruta, ruta_base=None):
    raiz = Path(ruta).resolve().parent.parent
    columnas, filas = leer(ruta)
    if columnas != COLUMNAS:
        return [f"encabezado distinto del esquema: {columnas}"]

    version = version_actual(raiz)
    errores, vistos = [], set()
    for fila in filas:
        if fila["id"] in vistos:
            errores.append(f"{fila['id']}: id repetido")
        vistos.add(fila["id"])
        errores += [f"{fila['id']}: {m}" for m in validar_fila(fila, raiz, version)]

    if ruta_base:
        columnas_base, filas_base = leer(ruta_base)
        actuales = {f["id"]: f for f in filas}
        comunes = [c for c in columnas_base if c in COLUMNAS and c not in RESOLUCION]
        for vieja in filas_base:
            nueva = actuales.get(vieja["id"])
            if nueva is None:
                errores.append(f"{vieja['id']}: se borró una predicción")
                continue
            errores += [
                f"{vieja['id']}: se editó lo predicho ({c})"
                for c in comunes if nueva[c] != vieja[c]
            ]
    return errores


if __name__ == "__main__":
    args = sys.argv[1:]
    base = args[args.index("--base") + 1] if "--base" in args else None
    errores = validar(args[0], base)
    for error in errores:
        print(error)
    print(f"{len(errores)} errores" if errores else "predicciones.csv válido")
    sys.exit(1 if errores else 0)
