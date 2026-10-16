"""EXP-019: sorteo de los 10 controles.

Universo: tickets archivados de portafolio con Rebotes 0, con una sección de
verificación, revisión o cierre del PM, y cuyo Estado no dice que se retiró o
quedó sin efecto. Uso: python3 sorteo.py <ruta a docs/tickets>
"""
import random
import re
import sys
from pathlib import Path

SEMILLA = 20261015
N = 10
REBOTES_0 = re.compile(r"\*\*Rebotes\*\*[^0-9]*0")
SECCION_PM = re.compile(r"^## (Verificación|Revisión|Cierre)( en producción)? (del )?PM", re.I | re.M)
EXCLUIR = re.compile(r"retirad|sin efecto|defer|cancel|descart|reemplaz", re.I)


def estado(texto):
    m = re.search(r"^\| \*\*Estado\*\* \|(.*)$", texto, re.M)
    return m.group(1) if m else ""


def universo(tickets):
    ids = []
    for f in sorted((tickets / "archivo").glob("*/*.md")):
        t = f.read_text()
        if REBOTES_0.search(t) and SECCION_PM.search(t) and not EXCLUIR.search(estado(t)):
            ids.append(f.stem)
    return sorted(ids)


if __name__ == "__main__":
    u = universo(Path(sys.argv[1]))
    sorteados = sorted(random.Random(SEMILLA).sample(u, N))
    print(f"universo ({len(u)}): {' '.join(u)}")
    print(f"semilla {SEMILLA}, {N} controles: {' '.join(sorteados)}")
    resto = [x for x in u if x not in sorteados]
    print(f"control del piloto (semilla {SEMILLA + 1}, entre {len(resto)}): {random.Random(SEMILLA + 1).choice(resto)}")
