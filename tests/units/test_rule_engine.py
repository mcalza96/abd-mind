from collections.abc import Mapping
from pathlib import Path

import pytest
from pydantic import ValidationError

from factory.contracts.abduction import HipotesisCandidata, Valor
from factory.contracts.rules import Comparacion, ConjuntoReglas
from factory.organ.rule_engine import ResultadoRegla, RuleEngine, cargar_reglas


@pytest.fixture
def finanzas() -> RuleEngine:
    return RuleEngine(cargar_reglas("finanzas"))


def _k(motor: RuleEngine, afirmaciones: Mapping[str, Valor]) -> tuple[float, list[str]]:
    r = motor.evaluar(afirmaciones)
    return r.k, r.violaciones


def test_validar_predicados_de_la_especificacion() -> None:
    motor = RuleEngine()
    assert motor.validar_predicados(["El margen cae por competencia"]) == 1.0
    assert motor.validar_predicados(["Requiere una Tasa Negativa"]) == 0.0


def test_reglas_de_finanzas_cargan(finanzas: RuleEngine) -> None:
    assert finanzas.reglas.dominio == "finanzas"
    assert "La tasa de descuento no puede ser negativa" in finanzas.invariantes


def test_comparacion_con_valor(finanzas: RuleEngine) -> None:
    assert _k(finanzas, {"tasa_descuento": 0.08}) == (1.0, [])
    assert _k(finanzas, {"tasa_descuento": -0.02}) == (0.0, ["tasa_descuento_no_negativa"])


def test_comparacion_entre_variables(finanzas: RuleEngine) -> None:
    assert _k(finanzas, {"dividendos_pagados": 50, "caja_disponible": 80})[0] == 1.0
    assert _k(finanzas, {"dividendos_pagados": 120, "caja_disponible": 80}) == (
        0.0,
        ["dividendos_bajo_caja"],
    )


def test_implicacion(finanzas: RuleEngine) -> None:
    viola = {"tendencia_precio": "baja_sostenida", "tendencia_margen_bruto": "alza"}
    cumple = {"tendencia_precio": "Baja sostenida", "tendencia_margen_bruto": "baja"}
    assert _k(finanzas, viola) == (0.0, ["reduccion_precio_comprime_margen"])
    assert _k(finanzas, cumple) == (1.0, [])
    # Sin el antecedente, la regla no aplica.
    assert _k(finanzas, {"tendencia_margen_bruto": "alza"}) == (1.0, [])


def test_variable_ausente_no_aplica(finanzas: RuleEngine) -> None:
    resultado = finanzas.evaluar({})
    assert not resultado.descartada
    assert all(e.resultado is ResultadoRegla.NO_APLICA for e in resultado.evaluaciones)


def test_tipos_no_comparables_no_aplican(finanzas: RuleEngine) -> None:
    resultado = finanzas.evaluar({"tasa_descuento": "alta"})
    assert not resultado.descartada


def test_reglas_blandas_gradúan_k() -> None:
    reglas = ConjuntoReglas.model_validate(
        {
            "dominio": "prueba",
            "version": 1,
            "reglas": [
                {
                    "id": "b1",
                    "tipo": "blanda",
                    "descripcion": "x>0",
                    "condicion": {"variable": "x", "op": ">", "valor": 0},
                },
                {
                    "id": "b2",
                    "tipo": "blanda",
                    "descripcion": "y>0",
                    "condicion": {"variable": "y", "op": ">", "valor": 0},
                },
            ],
        }
    )
    motor = RuleEngine(reglas)
    r = motor.evaluar({"x": 1, "y": -1})
    assert (r.k, r.descartada) == (0.5, False)
    r = motor.evaluar({"x": -1, "y": -1})
    assert (r.k, r.descartada) == (0.0, False)


def test_coherencia_combina_texto_y_estructura(finanzas: RuleEngine) -> None:
    h = HipotesisCandidata(
        id_hipotesis="h",
        mecanismo_latente="m",
        predicados_de_consistencia=["supone tasa negativa"],
        afirmaciones={"tasa_descuento": 0.05},
    )
    r = finanzas.coherencia(h)
    assert r.descartada and r.violaciones == ["predicado_prohibido"]


@pytest.mark.parametrize(
    "datos",
    [
        {"variable": "x", "op": "==", "valor": 1, "variable_ref": "y"},
        {"variable": "x", "op": "=="},
        {"variable": "x", "op": "in", "valor": 1},
        {"variable": "x", "op": "<", "valor": [1, 2]},
        {"variable": "x", "op": "~", "valor": 1},
    ],
)
def test_comparaciones_invalidas(datos: dict[str, object]) -> None:
    with pytest.raises(ValidationError):
        Comparacion.model_validate(datos)


def test_ids_repetidos_invalidos() -> None:
    regla = {
        "id": "r",
        "tipo": "dura",
        "descripcion": "d",
        "condicion": {"variable": "x", "op": "==", "valor": 1},
    }
    with pytest.raises(ValidationError):
        ConjuntoReglas.model_validate({"dominio": "d", "version": 1, "reglas": [regla, regla]})


def test_dominio_inexistente(tmp_path: Path) -> None:
    with pytest.raises(FileNotFoundError):
        cargar_reglas("no_existe", tmp_path)
