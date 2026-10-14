"""Prueba de la especificación.

El sistema elige la hipótesis abductiva, no el promedio de opiniones, y rechaza de inmediato la
que viola el RuleEngine.
"""

import math

import pytest

from factory.contracts.abduction import HipotesisCandidata
from factory.transition.deterministic.ibe_evaluator import IBEEvaluator


def _h(
    id_: str,
    explicadas: list[str],
    latentes: list[str] | None = None,
    predicados: list[str] | None = None,
) -> HipotesisCandidata:
    return HipotesisCandidata(
        id_hipotesis=id_,
        mecanismo_latente=id_,
        entidades_latentes=latentes or [],
        observaciones_explicadas=explicadas,
        predicados_de_consistencia=predicados or [],
    )


@pytest.fixture
def evaluador() -> IBEEvaluator:
    return IBEEvaluator()


def test_elige_cilindro_y_no_el_promedio(evaluador: IBEEvaluator) -> None:
    candidatas = [
        _h("esfera", ["y2"]),
        _h("cubo", []),
        _h("cilindro", ["y1", "y2"]),
        _h("ovalo_promedio", []),
    ]
    mejor = evaluador.seleccionar_mejor_explicacion(candidatas)
    assert mejor is not None
    assert mejor.id_hipotesis == "cilindro"
    assert mejor.consiliencia_c == 2
    assert mejor.score_final == pytest.approx(1.5 * 2 + 10.0)


def test_score_es_la_formula(evaluador: IBEEvaluator) -> None:
    e = evaluador.evaluar_hipotesis(_h("h", ["y1", "y2", "y3"], latentes=["estrategia"]))
    assert (e.consiliencia_c, e.parsimonia_p, e.coherencia_k) == (3, 1, 1.0)
    assert e.score_final == pytest.approx(1.5 * 3 + 10.0 * 1 - 1.0 * 1)


def test_rechaza_inmediatamente_la_que_viola_reglas(evaluador: IBEEvaluator) -> None:
    violadora = _h("violadora", ["y1", "y2", "y3"], predicados=["Asume una tasa negativa"])
    e = evaluador.evaluar_hipotesis(violadora)
    assert e.coherencia_k == 0.0
    assert e.score_final == -math.inf

    mejor = evaluador.seleccionar_mejor_explicacion([violadora, _h("modesta", ["y1"])])
    assert mejor is not None and mejor.id_hipotesis == "modesta"


def test_nunca_selecciona_una_hipotesis_descartada(evaluador: IBEEvaluator) -> None:
    solo_violadoras = [_h("a", ["y1"], predicados=["tasa negativa"])]
    assert evaluador.seleccionar_mejor_explicacion(solo_violadoras) is None


def test_parsimonia_desempata_a_igual_consiliencia(evaluador: IBEEvaluator) -> None:
    mejor = evaluador.seleccionar_mejor_explicacion(
        [_h("ad_hoc", ["y1", "y2"], latentes=["x", "z"]), _h("simple", ["y1", "y2"])]
    )
    assert mejor is not None and mejor.id_hipotesis == "simple"


def test_desempate_determinista_no_depende_del_orden(evaluador: IBEEvaluator) -> None:
    a, b = _h("b_hip", ["y1"]), _h("a_hip", ["y1"])
    primero = evaluador.seleccionar_mejor_explicacion([a, b])
    segundo = evaluador.seleccionar_mejor_explicacion([b, a])
    assert primero is not None and segundo is not None
    assert primero.id_hipotesis == segundo.id_hipotesis == "a_hip"


def test_umbral_tau() -> None:
    candidatas = [_h("debil", ["y1"])]
    assert IBEEvaluator(tau=11.0).seleccionar_mejor_explicacion(candidatas) is not None
    assert IBEEvaluator(tau=12.0).seleccionar_mejor_explicacion(candidatas) is None


def test_beta_no_cambia_el_ranking_con_k_binario() -> None:
    candidatas = [_h("a", ["y1", "y2"], latentes=["x"]), _h("b", ["y1"]), _h("c", ["y1", "y2"])]
    rankings = [
        [e.id_hipotesis for e in ev.ordenar(ev.evaluar_hipotesis(h) for h in candidatas)]
        for ev in (IBEEvaluator(beta=1.0), IBEEvaluator(beta=100.0))
    ]
    assert rankings[0] == rankings[1]


def test_valores_verificados_reemplazan_lo_declarado(evaluador: IBEEvaluator) -> None:
    exagerada = _h("h", ["y1", "y2", "y3"], latentes=[])
    e = evaluador.evaluar_hipotesis(exagerada, consiliencia=1, parsimonia=2)
    assert (e.consiliencia_c, e.parsimonia_p) == (1, 2)


def test_sin_candidatas_es_error(evaluador: IBEEvaluator) -> None:
    with pytest.raises(ValueError):
        evaluador.seleccionar_mejor_explicacion([])


def test_pesos_deben_ser_positivos() -> None:
    with pytest.raises(ValueError):
        IBEEvaluator(gamma=0.0)
