from factory.contracts.abduction import HipotesisCandidata
from factory.contracts.observation import Observacion, Observador
from factory.organ.projections import (
    RelacionConsistencia,
    VerificadorProyeccion,
    proyectar_solido,
)
from factory.organ.texto import normalizar


def _obs(vista: str) -> Observador:
    return Observador(id=vista, nombre=vista, parametros={"vista": vista})


def _hip(solido: str) -> HipotesisCandidata:
    return HipotesisCandidata(
        id_hipotesis=solido, mecanismo_latente=solido, afirmaciones={"solido": solido}
    )


def test_normalizar() -> None:
    assert normalizar("  Rectángulo ") == "rectangulo"
    assert normalizar("Tapón Universal") == "tapon_universal"


def test_proyeccion_del_cilindro() -> None:
    assert proyectar_solido(_hip("cilindro"), _obs("frontal")) == "rectangulo"
    assert proyectar_solido(_hip("Cilindro"), _obs("cenital")) == "circulo"


def test_proyeccion_desconocida() -> None:
    assert proyectar_solido(_hip("dodecaedro"), _obs("frontal")) is None
    assert proyectar_solido(_hip("cilindro"), Observador(id="x", nombre="x")) is None


def test_relacion_categorica_estricta_y_con_jerarquia() -> None:
    estricta = RelacionConsistencia()
    assert estricta.consistente("circulo", "Círculo")
    assert not estricta.consistente("cuadrado", "rectángulo")
    con_jerarquia = RelacionConsistencia({"cuadrado": ["rectángulo"]})
    assert con_jerarquia.consistente("cuadrado", "rectangulo")
    # La jerarquía no es simétrica: un rectángulo no es necesariamente un cuadrado.
    assert not con_jerarquia.consistente("rectangulo", "cuadrado")


def test_relacion_numerica_con_tolerancia() -> None:
    r = RelacionConsistencia()
    assert r.consistente(10.0, 10.4, tolerancia=0.5)
    assert not r.consistente(10.0, 10.6, tolerancia=0.5)
    assert not r.consistente(True, 1)
    assert not r.consistente("10", 10)


def test_verificador_produce_veredicto_justificado() -> None:
    v = VerificadorProyeccion()
    obs = Observacion(id="y1", observador_id="frontal", contenido="rectángulo", valor="rectángulo")
    si = v.verificar(_hip("cilindro"), obs, _obs("frontal"))
    no = v.verificar(_hip("esfera"), obs, _obs("frontal"))
    assert si.explica and si.fuente == "proyeccion"
    assert not no.explica and "circulo" in no.justificacion


def test_verificador_usa_contenido_si_no_hay_valor() -> None:
    obs = Observacion(id="y2", observador_id="cenital", contenido="círculo")
    assert VerificadorProyeccion().verificar(_hip("cono"), obs, _obs("cenital")).explica
