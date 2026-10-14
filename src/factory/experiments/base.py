"""Resultado de un experimento: tablas para mostrar y comprobaciones que deciden el éxito."""

import math

from pydantic import BaseModel, Field

from factory.contracts.case import ResultadoEvaluacion


class Tabla(BaseModel):
    titulo: str
    columnas: list[str]
    filas: list[list[str]]


class Comprobacion(BaseModel):
    descripcion: str
    ok: bool


class ResultadoExperimento(BaseModel):
    nombre: str
    descripcion: str
    tablas: list[Tabla] = Field(default_factory=list)
    comprobaciones: list[Comprobacion] = Field(default_factory=list)
    notas: list[str] = Field(default_factory=list)

    @property
    def exito(self) -> bool:
        return all(c.ok for c in self.comprobaciones)

    def comprobar(self, descripcion: str, ok: bool) -> None:
        self.comprobaciones.append(Comprobacion(descripcion=descripcion, ok=ok))


def formatear_score(score: float) -> str:
    return "-∞" if score == -math.inf else f"{score:.1f}"


def tabla_hipotesis(
    titulo: str, resultados: list[ResultadoEvaluacion], m: int, nombres: dict[str, str]
) -> Tabla:
    filas = []
    for r in resultados:
        e = r.evaluacion
        filas.append(
            [
                nombres.get(e.id_hipotesis, e.id_hipotesis),
                f"{e.consiliencia_c}/{m}",
                str(e.parsimonia_p),
                f"{e.coherencia_k:g}",
                formatear_score(e.score_final),
                r.estado.value + (f" ({', '.join(r.derrotada_por)})" if r.derrotada_por else ""),
            ]
        )
    return Tabla(
        titulo=titulo, columnas=["Hipótesis", "C", "P", "K", "Score", "Estado"], filas=filas
    )


def renderizar(resultado: ResultadoExperimento) -> str:
    lineas = [f"== {resultado.nombre} ==", resultado.descripcion, ""]
    for tabla in resultado.tablas:
        anchos = [
            max(len(fila[i]) for fila in [tabla.columnas, *tabla.filas])
            for i in range(len(tabla.columnas))
        ]
        lineas.append(tabla.titulo)
        for fila in [tabla.columnas, *tabla.filas]:
            lineas.append("  " + "  ".join(c.ljust(a) for c, a in zip(fila, anchos, strict=True)))
        lineas.append("")
    if resultado.notas:
        lineas += ["Notas:", *(f"  - {n}" for n in resultado.notas), ""]
    for c in resultado.comprobaciones:
        lineas.append(f"  [{'OK' if c.ok else 'FALLA'}] {c.descripcion}")
    lineas.append(f"Resultado: {'ÉXITO' if resultado.exito else 'FALLA'}")
    return "\n".join(lineas)
