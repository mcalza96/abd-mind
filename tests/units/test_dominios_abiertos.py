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


# --- respuesta contrastiva y margen (11 §11.3–11.4, ADR-0012) -------------------------------

import itertools  # noqa: E402
import random  # noqa: E402

from factory.contracts.case import Pregunta  # noqa: E402

PREGUNTA = Pregunta(variable="clase", valores=["p", "q"])


def _arbol_pregunta(
    tabla: dict[tuple[str, str], Relacion], clases: dict[str, str], obs: list[str]
) -> ArbolHipotesis:
    arbol = ArbolHipotesis(
        IBEEvaluator(lambda_residuo=1.0), VerificadorTabla(tabla), set(), pregunta=PREGUNTA
    )
    arbol.agregar_observador(Observador(id="O", nombre="Fuente", confiabilidad=0.9))
    for o in obs:
        arbol.agregar_observacion(_obs(o), como_prueba=False)
    for h, clase in clases.items():
        arbol.agregar_hipotesis(
            HipotesisCandidata(
                id_hipotesis=h, mecanismo_latente=h, entidades_latentes=[h],
                afirmaciones={"clase": clase},
            )
        )  # fmt: skip
    return arbol


def _valor(tabla: dict[tuple[str, str], Relacion], clases: dict[str, str], obs: list[str]) -> str:
    r = _arbol_pregunta(tabla, clases, obs).evaluar().respuesta
    assert r is not None
    return r.valor if r.determinada and r.valor else "—"


def _margen_bruto(
    tabla: dict[tuple[str, str], Relacion], clases: dict[str, str], obs: list[str]
) -> int | None:
    """Mínimo de veredictos a cambiar (a cualquier relación) para que la respuesta cambie."""
    original = _valor(tabla, clases, obs)
    pares = sorted(tabla)
    for k in range(1, len(pares) + 1):
        for elegidos in itertools.combinations(pares, k):
            alternativas = [[r for r in Relacion if r is not tabla[p]] for p in elegidos]
            for nuevas in itertools.product(*alternativas):
                cambiada = {**tabla, **dict(zip(elegidos, nuevas, strict=True))}
                if _valor(cambiada, clases, obs) != original:
                    return k
    return None


def test_margen_voraz_coincide_con_fuerza_bruta() -> None:
    azar = random.Random(7)
    obs = ["y1", "y2", "y3"]
    clases = {"H1": "p", "H2": "p", "H3": "q"}
    probados = 0
    while probados < 25:
        tabla = {(h, o): azar.choice(list(Relacion)) for h in clases for o in obs}
        r = _arbol_pregunta(tabla, clases, obs).evaluar().respuesta
        if r is None or not r.determinada:
            continue
        assert r.margen_veredictos == _margen_bruto(tabla, clases, obs), tabla
        probados += 1


def test_empate_dentro_de_la_clase_no_bloquea_la_respuesta() -> None:
    tabla = {(h, "y1"): E for h in ["H1", "H2", "H3"]} | {
        ("H1", "y2"): E,
        ("H2", "y2"): E,
        ("H3", "y2"): N,
    }
    resultado = _arbol_pregunta(tabla, {"H1": "p", "H2": "p", "H3": "q"}, ["y1", "y2"]).evaluar()
    assert resultado.subdeterminada and resultado.h_estrella is None
    assert resultado.respuesta is not None
    assert resultado.respuesta.determinada and resultado.respuesta.valor == "p"


def test_hipotesis_sin_valor_no_cuenta_para_la_respuesta() -> None:
    tabla = {("H1", "y1"): E, ("H2", "y1"): E}
    arbol = _arbol_pregunta(tabla, {"H1": "p", "H2": "otra"}, ["y1"])
    respuesta = arbol.evaluar().respuesta
    assert respuesta is not None
    assert respuesta.valor == "p" and respuesta.sin_responder == ["H2"]
    assert respuesta.margen_veredictos is None  # no hay rival de otra clase


def test_proyeccion_no_tiene_margen_finito() -> None:
    from factory.experiments.cilindro import agregar_hipotesis_base
    from factory.experiments.solidos import arbol_cilindro

    arbol = arbol_cilindro()
    agregar_hipotesis_base(arbol)
    respuesta = arbol.evaluar().respuesta
    assert respuesta is not None and respuesta.valor == "h_cilindro"
    assert respuesta.margen_veredictos is None and not respuesta.fragil


def test_servicio_con_pregunta() -> None:
    from factory.engine.case_service import ServicioCasos
    from factory.engine.modelos import EntradaHipotesis, EntradaObservador
    from factory.engine.store import Store
    from factory.experiments.robustez import _config_sin_llm

    servicio = ServicioCasos(Store(":memory:"), _config_sin_llm())
    pregunta = Pregunta(variable="forma", valores=["redonda", "angulosa"])
    caso = servicio.crear_caso("¿forma?", "sintetico", pregunta=pregunta).caso_id
    assert servicio.estado_caso(caso).pregunta == pregunta
    servicio.agregar_observacion(
        caso,
        EntradaObservador(nombre="Cenital", parametros={"vista": "cenital"}),
        "círculo",
        valor="circulo",
    )
    hipotesis = [
        EntradaHipotesis(
            mecanismo=f"Es un {s}", afirmaciones={"solido": s, "dimension": 3, "forma": f}
        )
        for s, f in [("esfera", "redonda"), ("cilindro", "redonda"), ("cubo", "angulosa")]
    ]
    hipotesis.append(EntradaHipotesis(mecanismo="Es un cono", afirmaciones={"solido": "cono"}))
    avisos = servicio.proponer_hipotesis(caso, hipotesis, origen="usuario").avisos
    assert any("no fija 'forma'" in a for a in avisos)
    mejor = servicio.mejor_explicacion(caso)
    assert mejor.h_estrella is None  # esfera, cilindro y cono empatan en mecanismo
    assert mejor.respuesta is not None and mejor.respuesta.valor == "redonda"
    assert mejor.motivo.startswith("respuesta: redonda")
    # La respuesta está determinada por proyección: no hay nada que discriminar.
    assert servicio.sugerir_observacion(caso).consultas == []
