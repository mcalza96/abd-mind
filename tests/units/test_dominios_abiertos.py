"""Propiedades del veredicto de tres valores y de los explananda (11 §11.1–11.2, ADR-0011).

Se prueban invariancias generales con un verificador de tabla, no ganadores de un caso.
"""

from factory.contracts.abduction import HipotesisCandidata
from factory.contracts.case import EstadoHipotesis, Relacion, Veredicto
from factory.contracts.observation import Observacion, Observador, RolObservacion
from factory.transition.deterministic.ibe_evaluator import IBEEvaluator
from factory.transition.deterministic.state_tree import ArbolHipotesis

E, N, X = Relacion.EXPLICA, Relacion.NEUTRAL, Relacion.CONTRADICE


class VerificadorTabla:
    def __init__(self, tabla: dict[tuple[str, str], Relacion]) -> None:
        self.tabla = tabla

    def verificar(
        self, hipotesis: HipotesisCandidata, observacion: Observacion, observador: Observador
    ) -> Veredicto:
        return Veredicto(
            id_hipotesis=hipotesis.id_hipotesis,
            id_observacion=observacion.id,
            relacion=self.tabla[(hipotesis.id_hipotesis, observacion.id)],
            fuente="verificador:tabla",
        )


def _arbol(tabla: dict[tuple[str, str], Relacion], hipotesis: list[str]) -> ArbolHipotesis:
    arbol = ArbolHipotesis(IBEEvaluator(lambda_residuo=1.0), VerificadorTabla(tabla), set())
    arbol.agregar_observador(Observador(id="O", nombre="Fuente", confiabilidad=0.98))
    for h in hipotesis:
        arbol.agregar_hipotesis(
            HipotesisCandidata(id_hipotesis=h, mecanismo_latente=h, entidades_latentes=[h])
        )
    return arbol


def _obs(i: str, rol: RolObservacion = RolObservacion.EXPLANANDUM) -> Observacion:
    return Observacion(id=i, observador_id="O", contenido=i, rol=rol)


def _scores(arbol: ArbolHipotesis) -> dict[str, float]:
    return {r.evaluacion.id_hipotesis: r.evaluacion.score_final for r in arbol.evaluar().ranking}


TABLA = {
    ("A", "y1"): E,
    ("B", "y1"): E,
    ("A", "y2"): X,
    ("B", "y2"): N,
    ("A", "irrelevante"): N,
    ("B", "irrelevante"): N,
}


def test_veredicto_booleano_anterior_se_lee_como_explica_o_contradice() -> None:
    viejo = Veredicto.model_validate(
        {"id_hipotesis": "h", "id_observacion": "y", "explica": False, "fuente": "x"}
    )
    assert viejo.relacion is X and not viejo.explica
    assert Veredicto(id_hipotesis="h", id_observacion="y", relacion=E, fuente="x").explica


def test_hecho_irrelevante_no_cambia_el_ranking() -> None:
    for rol in RolObservacion:
        arbol = _arbol(TABLA, ["A", "B"])
        arbol.agregar_observacion(_obs("y1"))
        antes = _scores(arbol)
        assert arbol.agregar_observacion(_obs("irrelevante", rol)) == []
        assert _scores(arbol) == antes


def test_solo_contradecir_derrota() -> None:
    arbol = _arbol(TABLA, ["A", "B"])
    arbol.agregar_observacion(_obs("y1"))
    assert arbol.agregar_observacion(_obs("y2")) == ["A"]  # ω = 0.98 ≥ ω_d
    assert arbol.estado("B") is EstadoHipotesis.VIVA


def test_solo_lo_contradicho_entra_en_el_residuo() -> None:
    arbol = _arbol(TABLA, ["A", "B"])
    for o in ["y1", "y2"]:
        arbol.agregar_observacion(_obs(o), como_prueba=False)
    a, b = arbol.evaluar_registro("A"), arbol.evaluar_registro("B")
    assert list(a.atribuidas_a_error) == ["y2"] and a.sin_explicar == []
    assert b.atribuidas_a_error == {} and b.sin_explicar == ["y2"]


def test_explanandum_neutral_queda_sin_explicar_y_pide_expansion() -> None:
    arbol = _arbol(TABLA, ["B"])
    arbol.agregar_observacion(_obs("y1"))
    arbol.agregar_observacion(_obs("y2"))
    resultado = arbol.evaluar()
    assert resultado.h_estrella is not None
    assert resultado.h_estrella.sin_explicar == ["y2"]
    assert resultado.expansion_sugerida  # α·0.98 = 1.47 > γ


def test_evidencia_neutral_no_pide_expansion() -> None:
    arbol = _arbol(TABLA, ["B"])
    arbol.agregar_observacion(_obs("y1"))
    arbol.agregar_observacion(_obs("y2", RolObservacion.EVIDENCIA))
    resultado = arbol.evaluar()
    assert resultado.h_estrella is not None and resultado.h_estrella.sin_explicar == []
    assert not resultado.expansion_sugerida


def test_el_rol_se_persiste_y_sobrevive_a_la_correccion() -> None:
    from factory.engine.case_service import ServicioCasos
    from factory.engine.modelos import EntradaObservador
    from factory.engine.store import Store
    from factory.experiments.robustez import _config_sin_llm

    servicio = ServicioCasos(Store(":memory:"), _config_sin_llm())
    caso = servicio.crear_caso("rol", "sintetico").caso_id
    vista = EntradaObservador(nombre="Cenital", parametros={"vista": "cenital"})
    hecho = servicio.agregar_observacion(
        caso, vista, "círculo", valor="circulo", rol=RolObservacion.EVIDENCIA
    ).hechos[0]
    assert hecho.rol is RolObservacion.EVIDENCIA
    corregido = servicio.corregir_observacion(caso, hecho.id, valor="circulo").hechos[0]
    assert corregido.rol is RolObservacion.EVIDENCIA
    activas = [o for o in servicio.auditoria(caso).observaciones if o.estado.value == "activa"]
    assert [o.rol for o in activas] == [RolObservacion.EVIDENCIA]
