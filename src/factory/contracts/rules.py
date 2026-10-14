"""Esquema de las reglas invariantes del dominio (rules/<dominio>.yaml). Ver ADR-0004."""

from typing import Literal, Self

from pydantic import BaseModel, ConfigDict, model_validator

from factory.contracts.abduction import Valor

Operador = Literal["==", "!=", "<", "<=", ">", ">=", "in", "not_in"]


class Comparacion(BaseModel):
    """Compara una variable con un valor fijo o con otra variable."""

    model_config = ConfigDict(extra="forbid")

    variable: str
    op: Operador
    valor: Valor | list[Valor] | None = None
    variable_ref: str | None = None

    @model_validator(mode="after")
    def _validar(self) -> Self:
        if (self.valor is None) == (self.variable_ref is None):
            raise ValueError("una comparación necesita exactamente uno de 'valor' o 'variable_ref'")
        if self.op in ("in", "not_in") and not isinstance(self.valor, list):
            raise ValueError(f"el operador '{self.op}' requiere una lista en 'valor'")
        if self.op not in ("in", "not_in") and isinstance(self.valor, list):
            raise ValueError(f"el operador '{self.op}' no admite una lista en 'valor'")
        return self


class Implicacion(BaseModel):
    """Si se cumple 'si', debe cumplirse 'entonces'."""

    model_config = ConfigDict(extra="forbid")

    si: Comparacion
    entonces: Comparacion


Condicion = Comparacion | Implicacion


class Regla(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: str
    tipo: Literal["dura", "blanda"]
    descripcion: str
    condicion: Condicion


class ConjuntoReglas(BaseModel):
    model_config = ConfigDict(extra="forbid")

    dominio: str
    version: int
    reglas: list[Regla]

    @model_validator(mode="after")
    def _ids_unicos(self) -> Self:
        ids = [r.id for r in self.reglas]
        repetidos = sorted({i for i in ids if ids.count(i) > 1})
        if repetidos:
            raise ValueError(f"ids de regla repetidos: {repetidos}")
        return self
