"""Normalización de valores categóricos para comparaciones deterministas."""

import unicodedata


def normalizar(texto: str) -> str:
    """Minúsculas, sin tildes y con '_' en lugar de espacios: 'Rectángulo ' → 'rectangulo'."""
    sin_tildes = "".join(
        c for c in unicodedata.normalize("NFKD", texto) if not unicodedata.combining(c)
    )
    return "_".join(sin_tildes.casefold().split())
