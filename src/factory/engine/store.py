"""Persistencia de casos en SQLite (ADR-0007).

El estado de un caso se guarda como un registro de eventos append-only: el motor reconstruye el
árbol de hipótesis reproduciéndolos. Los veredictos se guardan aparte para que reconstruir un
caso nunca vuelva a llamar al LLM. También aloja la caché de respuestas LLM del motor.
"""

import json
import sqlite3
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from pydantic import BaseModel

from factory.contracts.case import Veredicto
from factory.engine.modelos import RegistroCaso

_ESQUEMA = """
CREATE TABLE IF NOT EXISTS casos (
    id TEXT PRIMARY KEY,
    numero INTEGER NOT NULL UNIQUE,
    datos TEXT NOT NULL,
    estado TEXT NOT NULL,
    actualizado TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS eventos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    caso_id TEXT NOT NULL REFERENCES casos(id),
    tipo TEXT NOT NULL,
    datos TEXT NOT NULL,
    momento TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS eventos_caso ON eventos(caso_id, id);
CREATE TABLE IF NOT EXISTS veredictos (
    caso_id TEXT NOT NULL REFERENCES casos(id),
    id_hipotesis TEXT NOT NULL,
    id_observacion TEXT NOT NULL,
    datos TEXT NOT NULL,
    PRIMARY KEY (caso_id, id_hipotesis, id_observacion)
);
CREATE TABLE IF NOT EXISTS llm_cache (
    clave TEXT PRIMARY KEY,
    texto TEXT NOT NULL
);
"""


def ahora() -> str:
    return datetime.now(UTC).isoformat(timespec="seconds")


class Evento(BaseModel):
    id: int
    caso_id: str
    tipo: str
    datos: dict[str, Any]
    momento: str


class Store:
    def __init__(self, ruta: Path | str) -> None:
        if isinstance(ruta, Path):
            ruta.parent.mkdir(parents=True, exist_ok=True)
        # Autocommit: cada escritura queda guardada al instante (los veredictos ya pagados no
        # se pierden si una operación falla a medio camino).
        self.conexion = sqlite3.connect(str(ruta), isolation_level=None)
        self.conexion.execute("PRAGMA foreign_keys = ON")
        self.conexion.executescript(_ESQUEMA)

    def cerrar(self) -> None:
        self.conexion.close()

    # --- casos ---------------------------------------------------------------------------

    def nuevo_numero(self) -> int:
        fila = self.conexion.execute("SELECT COALESCE(MAX(numero), 0) + 1 FROM casos").fetchone()
        return int(fila[0])

    def crear_caso(self, caso: RegistroCaso, numero: int) -> None:
        self.conexion.execute(
            "INSERT INTO casos (id, numero, datos, estado, actualizado) VALUES (?, ?, ?, ?, ?)",
            (caso.id, numero, caso.model_dump_json(), caso.estado, caso.actualizado),
        )

    def guardar_caso(self, caso: RegistroCaso) -> None:
        self.conexion.execute(
            "UPDATE casos SET datos = ?, estado = ?, actualizado = ? WHERE id = ?",
            (caso.model_dump_json(), caso.estado, caso.actualizado, caso.id),
        )

    def obtener_caso(self, caso_id: str) -> RegistroCaso | None:
        fila = self.conexion.execute("SELECT datos FROM casos WHERE id = ?", (caso_id,)).fetchone()
        return RegistroCaso.model_validate_json(fila[0]) if fila else None

    def listar_casos(self, estado: str | None = None, limite: int = 50) -> list[RegistroCaso]:
        consulta = "SELECT datos FROM casos"
        parametros: tuple[Any, ...] = ()
        if estado:
            consulta += " WHERE estado = ?"
            parametros = (estado,)
        consulta += " ORDER BY actualizado DESC, numero DESC LIMIT ?"
        filas = self.conexion.execute(consulta, (*parametros, limite)).fetchall()
        return [RegistroCaso.model_validate_json(f[0]) for f in filas]

    # --- eventos -------------------------------------------------------------------------

    def agregar_evento(self, caso_id: str, tipo: str, datos: dict[str, Any]) -> None:
        self.conexion.execute(
            "INSERT INTO eventos (caso_id, tipo, datos, momento) VALUES (?, ?, ?, ?)",
            (caso_id, tipo, json.dumps(datos, ensure_ascii=False), ahora()),
        )

    def eventos(self, caso_id: str) -> list[Evento]:
        filas = self.conexion.execute(
            "SELECT id, caso_id, tipo, datos, momento FROM eventos WHERE caso_id = ? ORDER BY id",
            (caso_id,),
        ).fetchall()
        return [
            Evento(id=f[0], caso_id=f[1], tipo=f[2], datos=json.loads(f[3]), momento=f[4])
            for f in filas
        ]

    def contar_eventos(self, caso_id: str) -> int:
        fila = self.conexion.execute(
            "SELECT COUNT(*) FROM eventos WHERE caso_id = ?", (caso_id,)
        ).fetchone()
        return int(fila[0])

    # --- veredictos ----------------------------------------------------------------------

    def veredicto(self, caso_id: str, id_hipotesis: str, id_observacion: str) -> Veredicto | None:
        fila = self.conexion.execute(
            "SELECT datos FROM veredictos "
            "WHERE caso_id = ? AND id_hipotesis = ? AND id_observacion = ?",
            (caso_id, id_hipotesis, id_observacion),
        ).fetchone()
        return Veredicto.model_validate_json(fila[0]) if fila else None

    def guardar_veredicto(self, caso_id: str, veredicto: Veredicto) -> None:
        self.conexion.execute(
            "INSERT OR REPLACE INTO veredictos (caso_id, id_hipotesis, id_observacion, datos) "
            "VALUES (?, ?, ?, ?)",
            (
                caso_id,
                veredicto.id_hipotesis,
                veredicto.id_observacion,
                veredicto.model_dump_json(),
            ),
        )

    def veredictos(self, caso_id: str) -> list[Veredicto]:
        filas = self.conexion.execute(
            "SELECT datos FROM veredictos WHERE caso_id = ? ORDER BY id_hipotesis, id_observacion",
            (caso_id,),
        ).fetchall()
        return [Veredicto.model_validate_json(f[0]) for f in filas]


class CacheSQLite:
    """Caché de respuestas LLM en la misma base de datos (implementa `llm_client.Cache`)."""

    def __init__(self, store: Store) -> None:
        self.store = store

    def leer(self, clave: str) -> str | None:
        fila = self.store.conexion.execute(
            "SELECT texto FROM llm_cache WHERE clave = ?", (clave,)
        ).fetchone()
        return str(fila[0]) if fila else None

    def guardar(self, clave: str, texto: str) -> None:
        self.store.conexion.execute(
            "INSERT OR REPLACE INTO llm_cache (clave, texto) VALUES (?, ?)", (clave, texto)
        )
