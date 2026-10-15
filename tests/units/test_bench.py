"""Validación de los casos de abd-bench (datasets/abd-bench)."""

from collections import Counter
from pathlib import Path

from factory.bench.casos import Caso, TipoCausa, cargar_casos

DIRECTORIO = Path(__file__).resolve().parents[2] / "datasets" / "abd-bench"


def _todos() -> list[Caso]:
    return [c for ruta in sorted(DIRECTORIO.glob("*.jsonl")) for c in cargar_casos(ruta)]


def test_casos_validos_e_ids_unicos() -> None:
    casos = _todos()
    repetidos = [i for i, n in Counter(c.id for c in casos).items() if n > 1]
    assert casos and not repetidos


def test_variantes_apuntan_a_casos_existentes() -> None:
    casos = _todos()
    ids = {c.id for c in casos}
    for c in casos:
        if c.variante_de is not None:
            assert c.variante_de in ids, c.id
        if c.serie == "V" and c.variante_de is not None:
            original = next(o for o in casos if o.id == c.variante_de)
            # La variante conserva la estructura: el mismo tipo de causa que su original.
            assert c.solucion.tipo_de_causa is original.solucion.tipo_de_causa, c.id


def test_variantes_cubren_todos_los_tipos_de_causa() -> None:
    tipos = {c.solucion.tipo_de_causa for c in _todos() if c.serie == "V"}
    assert tipos == set(TipoCausa)
