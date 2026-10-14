import pytest

from factory.contracts.abduction import HipotesisCandidata
from factory.contracts.case import EstadoHipotesis
from factory.experiments.solidos import arbol_cilindro, hipotesis_solido, observacion, observador
from factory.transition.deterministic.state_tree import ArbolHipotesis


@pytest.fixture
def arbol() -> ArbolHipotesis:
    a = arbol_cilindro()
    a.agregar_hipotesis(hipotesis_solido("h_cilindro", "cilindro"))
    a.agregar_hipotesis(hipotesis_solido("h_esfera", "esfera"))
    return a


def test_consiliencia_se_verifica_no_se_declara(arbol: ArbolHipotesis) -> None:
    mentirosa = HipotesisCandidata(
        id_hipotesis="h_mentirosa",
        mecanismo_latente="Es una esfera y explica todo",
        observaciones_explicadas=["y1", "y2"],
        afirmaciones={"solido": "esfera", "dimension": 3},
    )
    arbol.agregar_hipotesis(mentirosa)
    r = arbol.evaluar_registro("h_mentirosa")
    assert r.evaluacion.consiliencia_c == 1
    assert r.declaradas_no_verificadas == ["y1"]


def test_parsimonia_contra_vocabulario(arbol: ArbolHipotesis) -> None:
    h = hipotesis_solido("h_x", "cilindro", latentes=["cilindro", "fuerza_oculta", "Fuerza oculta"])
    arbol.agregar_hipotesis(h)
    assert arbol.parsimonia(h) == 1  # 'cilindro' ya es conocido; las otras dos son la misma
    arbol.verificar_entidad("fuerza oculta")
    assert arbol.parsimonia(h) == 0


def test_observaciones_iniciales_no_derrotan() -> None:
    a = arbol_cilindro()
    a.agregar_hipotesis(hipotesis_solido("h_esfera", "esfera"))
    assert a.estado("h_esfera") is EstadoHipotesis.VIVA


def test_evidencia_nueva_derrota_y_retractar_reactiva(arbol: ArbolHipotesis) -> None:
    arbol.agregar_observador(observador("O3", "lateral"))
    derrotadas = arbol.agregar_observacion(observacion("y3", "O3", "triangulo"))
    assert sorted(derrotadas) == ["h_cilindro", "h_esfera"]
    assert arbol.evaluar().ranking == []

    assert sorted(arbol.retractar_observacion("y3")) == ["h_cilindro", "h_esfera"]
    assert arbol.retractar_observacion("y3") == []
    resultado = arbol.evaluar()
    assert resultado.m == 2
    assert resultado.h_estrella is not None
    assert resultado.h_estrella.evaluacion.id_hipotesis == "h_cilindro"


def test_derrota_multiple_requiere_retractar_todo(arbol: ArbolHipotesis) -> None:
    arbol.agregar_observador(observador("O3", "lateral"))
    arbol.agregar_observacion(observacion("y3", "O3", "triangulo"))
    arbol.agregar_observacion(observacion("y4", "O3", "triangulo"))
    arbol.retractar_observacion("y3")
    assert arbol.estado("h_cilindro") is EstadoHipotesis.DERROTADA
    assert arbol.retractar_observacion("y4") == ["h_cilindro", "h_esfera"]


def test_errores_de_registro(arbol: ArbolHipotesis) -> None:
    with pytest.raises(ValueError):
        arbol.agregar_hipotesis(hipotesis_solido("h_cilindro", "cilindro"))
    with pytest.raises(ValueError):
        arbol.agregar_observacion(observacion("y9", "O_inexistente", "x"))
    with pytest.raises(ValueError):
        arbol.agregar_observacion(observacion("y1", "O1", "x"))
    with pytest.raises(KeyError):
        arbol.retractar_observacion("no_existe")


def test_sin_observaciones_no_sugiere_expansion() -> None:
    from factory.experiments.solidos import nuevo_arbol

    a = nuevo_arbol(set())
    a.agregar_hipotesis(hipotesis_solido("h", "cubo"))
    assert not a.evaluar().expansion_sugerida
