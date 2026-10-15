"""Motor de reglas: coherencia externa K (docs/historico/marco-teorico/04, decisiones D3 y D4).

Dos mecanismos:
- `validar_predicados`: el simulador de la especificación, que busca palabras prohibidas en los
  predicados en texto libre. Se conserva como filtro barato.
- `evaluar`: reglas declarativas (rules/<dominio>.yaml) sobre las afirmaciones estructuradas de
  la hipótesis. Las reglas duras descartan la hipótesis; las blandas gradúan K.
"""

import operator
import os
from collections.abc import Callable, Iterable, Mapping
from enum import StrEnum
from pathlib import Path

import yaml
from pydantic import BaseModel, Field

from factory.contracts.abduction import HipotesisCandidata, Valor
from factory.contracts.rules import Comparacion, ConjuntoReglas, Implicacion, Regla
from factory.organ.texto import normalizar

# Frases que el simulador de la especificación considera contradicciones flagrantes.
PALABRAS_PROHIBIDAS: tuple[str, ...] = ("tasa negativa",)

_ORDEN: dict[str, Callable[[float, float], bool]] = {
    "<": operator.lt,
    "<=": operator.le,
    ">": operator.gt,
    ">=": operator.ge,
}


class ResultadoRegla(StrEnum):
    CUMPLE = "cumple"
    VIOLA = "viola"
    NO_APLICA = "no_aplica"


class EvaluacionRegla(BaseModel):
    regla_id: str
    tipo: str
    resultado: ResultadoRegla
    nota: str = ""


class ResultadoCoherencia(BaseModel):
    k: float = Field(
        description="1.0 sin reglas blandas aplicables; 0.0 si la hipótesis se descarta"
    )
    descartada: bool
    violaciones: list[str] = Field(default_factory=list)
    evaluaciones: list[EvaluacionRegla] = Field(default_factory=list)


def directorio_reglas() -> Path:
    """`ABD_MIND_RULES_DIR` o, por defecto, la carpeta `rules/` del repositorio."""
    env = os.environ.get("ABD_MIND_RULES_DIR")
    return Path(env) if env else Path(__file__).resolve().parents[3] / "rules"


def cargar_reglas(dominio: str, directorio: Path | None = None) -> ConjuntoReglas:
    ruta = (directorio or directorio_reglas()) / f"{dominio}.yaml"
    if not ruta.is_file():
        raise FileNotFoundError(f"no existe el archivo de reglas del dominio '{dominio}': {ruta}")
    with ruta.open(encoding="utf-8") as f:
        return ConjuntoReglas.model_validate(yaml.safe_load(f))


def _es_numero(v: object) -> bool:
    return isinstance(v, int | float) and not isinstance(v, bool)


def _igual(a: Valor, b: Valor) -> bool:
    if isinstance(a, str) and isinstance(b, str):
        return normalizar(a) == normalizar(b)
    return a == b


def _comparar(cmp: Comparacion, afirmaciones: Mapping[str, Valor]) -> tuple[ResultadoRegla, str]:
    if cmp.variable not in afirmaciones:
        return ResultadoRegla.NO_APLICA, f"la hipótesis no afirma '{cmp.variable}'"
    izquierda = afirmaciones[cmp.variable]

    if cmp.variable_ref is not None:
        if cmp.variable_ref not in afirmaciones:
            return ResultadoRegla.NO_APLICA, f"la hipótesis no afirma '{cmp.variable_ref}'"
        derecha: Valor | list[Valor] = afirmaciones[cmp.variable_ref]
    else:
        assert cmp.valor is not None  # garantizado por el validador de Comparacion
        derecha = cmp.valor

    if cmp.op in ("in", "not_in"):
        assert isinstance(derecha, list)
        pertenece = any(_igual(izquierda, d) for d in derecha)
        cumple = pertenece if cmp.op == "in" else not pertenece
    elif isinstance(derecha, list):
        return ResultadoRegla.NO_APLICA, "comparación con una lista sin operador 'in'"
    elif cmp.op in ("==", "!="):
        cumple = _igual(izquierda, derecha) == (cmp.op == "==")
    elif _es_numero(izquierda) and _es_numero(derecha):
        cumple = _ORDEN[cmp.op](float(izquierda), float(derecha))
    else:
        return ResultadoRegla.NO_APLICA, f"tipos no comparables con '{cmp.op}'"

    return (ResultadoRegla.CUMPLE if cumple else ResultadoRegla.VIOLA), ""


def evaluar_regla(regla: Regla, afirmaciones: Mapping[str, Valor]) -> EvaluacionRegla:
    cond = regla.condicion
    if isinstance(cond, Implicacion):
        antecedente, nota = _comparar(cond.si, afirmaciones)
        if antecedente is ResultadoRegla.CUMPLE:
            resultado, nota = _comparar(cond.entonces, afirmaciones)
        else:
            resultado = ResultadoRegla.NO_APLICA
            nota = nota or "no se cumple el antecedente"
    else:
        resultado, nota = _comparar(cond, afirmaciones)
    return EvaluacionRegla(regla_id=regla.id, tipo=regla.tipo, resultado=resultado, nota=nota)


class RuleEngine:
    def __init__(self, reglas: ConjuntoReglas | None = None) -> None:
        self.reglas = reglas or ConjuntoReglas(dominio="vacio", version=0, reglas=[])

    @property
    def invariantes(self) -> list[str]:
        return [r.descripcion for r in self.reglas.reglas]

    def validar_predicados(self, predicados: Iterable[str]) -> float:
        """Simulador de la especificación: 0.0 si algún predicado contiene una frase prohibida."""
        for predicado in predicados:
            texto = predicado.lower()
            if any(p in texto for p in PALABRAS_PROHIBIDAS):
                return 0.0
        return 1.0

    def evaluar(self, afirmaciones: Mapping[str, Valor]) -> ResultadoCoherencia:
        evaluaciones = [evaluar_regla(r, afirmaciones) for r in self.reglas.reglas]
        violaciones = [
            e.regla_id
            for e in evaluaciones
            if e.tipo == "dura" and e.resultado is ResultadoRegla.VIOLA
        ]
        if violaciones:
            return ResultadoCoherencia(
                k=0.0, descartada=True, violaciones=violaciones, evaluaciones=evaluaciones
            )
        blandas = [
            e
            for e in evaluaciones
            if e.tipo == "blanda" and e.resultado is not ResultadoRegla.NO_APLICA
        ]
        k = (
            sum(e.resultado is ResultadoRegla.CUMPLE for e in blandas) / len(blandas)
            if blandas
            else 1.0
        )
        return ResultadoCoherencia(k=k, descartada=False, evaluaciones=evaluaciones)

    def coherencia(self, hipotesis: HipotesisCandidata) -> ResultadoCoherencia:
        """K de una hipótesis: filtro textual de la especificación + reglas estructuradas."""
        resultado = self.evaluar(hipotesis.afirmaciones)
        if self.validar_predicados(hipotesis.predicados_de_consistencia) == 0.0:
            return resultado.model_copy(
                update={
                    "k": 0.0,
                    "descartada": True,
                    "violaciones": [*resultado.violaciones, "predicado_prohibido"],
                }
            )
        return resultado
