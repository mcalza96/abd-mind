"""EXP-015: consiliencia frente a puntuación predictiva en los escenarios deterministas. Sin LLM.

Cada escenario se arma una vez y se evalúa con las dos puntuaciones (el árbol recalcula el score
según `arbol.puntuacion`). Las salas de EXP-014 entran como familias con parámetros.
"""

from collections.abc import Callable

from factory.contracts.abduction import HipotesisCandidata, Valor
from factory.contracts.case import Pregunta
from factory.contracts.observation import Observacion, Observador
from factory.experiments import expansion
from factory.experiments.base import ResultadoExperimento, Tabla
from factory.experiments.cilindro import agregar_hipotesis_base
from factory.experiments.robustez import _arbol_falible, _tapon
from factory.experiments.salas import HISTORIA_5, elipse, rect
from factory.experiments.solidos import (
    SOLIDOS_CONOCIDOS,
    arbol_cilindro,
    hipotesis_solido,
    nuevo_arbol,
    observacion,
    observador,
)
from factory.organ.projections import VerificadorProyeccion
from factory.organ.rule_engine import RuleEngine, cargar_reglas
from factory.transition.deterministic.ibe_evaluator import IBEEvaluator
from factory.transition.deterministic.state_tree import ArbolHipotesis, ResultadoArbol

MODOS = ("consiliencia", "predictiva")


def _ganadora(r: ResultadoArbol) -> str:
    if r.h_estrella is not None:
        return r.h_estrella.evaluacion.id_hipotesis
    if r.subdeterminada:
        return "empate: " + ", ".join(sorted(r.empatadas))
    return "—"


def _ambos(arbol: ArbolHipotesis) -> dict[str, ResultadoArbol]:
    resultados = {}
    for modo in MODOS:
        arbol.puntuacion = modo
        resultados[modo] = arbol.evaluar()
    arbol.puntuacion = "consiliencia"
    return resultados


# --- salas con medidas, como familias -------------------------------------------------------

MEDIDAS: list[Valor] = [4, 7, 10]
MEDIDAS_FINAS: list[Valor] = [2, 4, 7, 10, 12]


def paredes(medidas: list[Valor]) -> list[Valor]:
    return [rect(int(w), int(h)) for w in medidas for h in medidas]


def techos(medidas: list[Valor]) -> list[Valor]:
    return sorted({elipse(int(a), int(b)) for a in medidas for b in medidas})


IMPOSIBLE = "imposible"  # miembro fuera de la familia (p. ej. k > d): nunca calza


def proyectar_sala(h: HipotesisCandidata, observador: Observador) -> Valor | None:
    a = h.afirmaciones
    vista = str(observador.parametros["vista"])
    forma = a.get("solido")
    try:
        if forma == "cilindro":
            d, alto = int(a["d"]), int(a["h"])
            return {"frontal": rect(d, alto), "lateral": rect(d, alto), "cenital": elipse(d, d)}[
                vista
            ]
        if forma == "cilindro_eliptico":
            x, y, alto = int(a["a"]), int(a["b"]), int(a["h"])
            return {"frontal": rect(x, alto), "lateral": rect(y, alto), "cenital": elipse(x, y)}[
                vista
            ]
        if forma == "lampara_torcida":
            d, alto, k = int(a["d"]), int(a["h"]), int(a["k"])
            if k > d:
                return IMPOSIBLE
            return {"frontal": rect(d, alto), "lateral": rect(d, alto), "cenital": elipse(d, k)}[
                vista
            ]
        if forma == "pantalla_lateral":
            x, y, alto, s = int(a["a"]), int(a["b"]), int(a["h"]), int(a["s"])
            return {"frontal": rect(x, alto), "lateral": rect(s, alto), "cenital": elipse(x, y)}[
                vista
            ]
        if forma == "se_deforma":
            d, alto = int(a["d"]), int(a["h"])
            return {"frontal": rect(d, alto), "lateral": rect(d, alto), "cenital": a["techo"]}[
                vista
            ]
        if forma == "merlin":
            return a[vista]
        if forma in ("cubo", "cubo_hueco"):
            s = int(a["s"])
            return rect(s, s)
    except KeyError:
        return None  # familia sin ajustar: no proyecta
    return None


def _familia(id_: str, libres: dict[str, list[Valor]], **fijas: Valor) -> HipotesisCandidata:
    return HipotesisCandidata(
        id_hipotesis=id_,
        mecanismo_latente=id_.replace("_", " "),
        afirmaciones={"solido": id_, "dimension": 3, **fijas},
        parametros_libres=libres,
        origen="experimento",
    )


def familias_5(m: list[Valor]) -> list[HipotesisCandidata]:
    return [
        _familia("cilindro", {"d": m, "h": m}),
        _familia("cilindro_eliptico", {"a": m, "b": m, "h": m}),
        _familia("lampara_torcida", {"d": m, "h": m, "k": m}),
        _familia("pantalla_lateral", {"a": m, "b": m, "h": m, "s": m}),
        _familia("se_deforma", {"d": m, "h": m, "techo": techos(m)}),
        _familia("merlin", {"frontal": paredes(m), "lateral": paredes(m), "cenital": techos(m)}),
    ]


def universo_sala(m: list[Valor]) -> Callable[[Observacion, Observador], int]:
    def universo(_: Observacion, obs: Observador) -> int:
        return len(techos(m)) if obs.parametros["vista"] == "cenital" else len(paredes(m))

    return universo


def arbol_sala(
    observaciones: list[tuple[str, str, str, float]],
    familias: list[HipotesisCandidata],
    pregunta: Pregunta | None = None,
    medidas: list[Valor] = MEDIDAS,
) -> ArbolHipotesis:
    evaluador = IBEEvaluator(
        alpha=1.5, beta=10.0, gamma=1.0, rule_engine=RuleEngine(cargar_reglas("sintetico"))
    )
    proyector = VerificadorProyeccion(proyeccion=proyectar_sala)
    nombres = {"cilindro", "cilindro_eliptico", "cubo", "cubo_hueco"}
    nombres |= {"lampara_torcida", "pantalla_lateral", "se_deforma", "merlin"}
    arbol = ArbolHipotesis(
        evaluador,
        proyector,
        nombres,  # en la sala ninguna forma cuenta como entidad nueva: compite solo la predicción
        pregunta=pregunta,
        puntuacion="predictiva",
        universo=universo_sala(medidas),
    )
    for id_, vista, silueta, omega in observaciones:
        arbol.agregar_observador(
            Observador(id=f"O_{id_}", nombre=id_, parametros={"vista": vista}, confiabilidad=omega)
        )
        arbol.agregar_observacion(
            Observacion(id=id_, observador_id=f"O_{id_}", contenido=silueta, valor=silueta)
        )
    for h in familias:
        arbol.agregar_hipotesis(h)
    return arbol


# --- escenarios ---------------------------------------------------------------------------


def _cilindro() -> ArbolHipotesis:
    arbol = arbol_cilindro()
    agregar_hipotesis_base(arbol)
    return arbol


def _expansion(alpha: float, gamma: float) -> ArbolHipotesis:
    arbol = arbol_cilindro(expansion.VOCABULARIO, alpha=alpha, gamma=gamma)
    for solido in sorted(expansion.VOCABULARIO):
        arbol.agregar_hipotesis(hipotesis_solido(f"h_{solido}", solido))
    arbol.agregar_hipotesis(expansion._hipotesis_latente())
    return arbol


def _tercer_observador() -> ArbolHipotesis:
    arbol = _cilindro()
    arbol.agregar_observador(observador("O3", "lateral"))
    arbol.agregar_observacion(observacion("y3", "O3", "triángulo"))
    arbol.agregar_hipotesis(_tapon())
    return arbol


def _errata(omega: float) -> ArbolHipotesis:
    arbol, _ = _arbol_falible(omega)
    arbol.agregar_hipotesis(_tapon())
    return arbol


def _empate() -> ArbolHipotesis:
    arbol = nuevo_arbol(SOLIDOS_CONOCIDOS)
    arbol.agregar_observador(observador("O1", "cenital"))
    arbol.agregar_observacion(observacion("y1", "O1", "círculo"))
    for solido in ("esfera", "cilindro", "cono", "elipsoide"):
        arbol.agregar_hipotesis(hipotesis_solido(f"h_{solido}", solido))
    return arbol


ESCENARIOS: dict[str, Callable[[], ArbolHipotesis]] = {
    "E1 cilindro (5.1)": _cilindro,
    "E2 expansión (5.2), α=1,5 γ=1": lambda: _expansion(1.5, 1.0),
    "E2 expansión (5.2), α=1 γ=2": lambda: _expansion(1.0, 2.0),
    "E3 tercer observador (5.3)": _tercer_observador,
    "E4 errata ω=0,3": lambda: _errata(0.3),
    "E4 errata ω=0,6": lambda: _errata(0.6),
    "E4 errata ω=0,9": lambda: _errata(0.9),
    "E4 errata ω=1": lambda: _errata(1.0),
    "E5 empate": _empate,
}


def ejecutar() -> ResultadoExperimento:
    resultado = ResultadoExperimento(
        nombre="puntuacion",
        descripcion=(
            "EXP-015: consiliencia frente a puntuación predictiva (con error del observador) "
            "en los escenarios deterministas y en las salas de EXP-014 como familias."
        ),
    )
    filas = []
    g: dict[str, dict[str, str]] = {}
    for nombre, construir in ESCENARIOS.items():
        r = _ambos(construir())
        g[nombre] = {m: _ganadora(r[m]) for m in MODOS}
        filas.append([nombre, g[nombre]["consiliencia"], g[nombre]["predictiva"]])
    resultado.tablas.append(
        Tabla(
            titulo="H* según la puntuación",
            columnas=["Escenario", "Consiliencia", "Predictiva"],
            filas=filas,
        )
    )
    errata = _errata(0.3)
    detalle = {
        r.evaluacion.id_hipotesis: r.evaluacion.score_predictivo for r in errata.evaluar().ranking
    }
    resultado.notas.append(
        "Errata ω=0,3, score predictivo: "
        + ", ".join(f"{k} {v:.2f}" for k, v in detalle.items() if v is not None)
    )

    ordenes = {}
    for medidas in (MEDIDAS, MEDIDAS_FINAS):
        sala = arbol_sala(HISTORIA_5, familias_5(medidas), medidas=medidas)
        ranking = sala.evaluar_todas()
        etiqueta = ", ".join(str(x) for x in medidas)
        resultado.tablas.append(
            Tabla(
                titulo=f"E6 Historia 5 con familias (medidas {etiqueta}; ω = 0,95)",
                columnas=["Familia", "Score predictivo", "Olga", "Sara", "Tomás"],
                filas=[
                    [
                        r.evaluacion.id_hipotesis,
                        f"{r.evaluacion.score_final:.2f}",
                        *_por_obs(sala, r.evaluacion.id_hipotesis),
                    ]
                    for r in ranking
                ],
            )
        )
        ordenes[len(medidas)] = [r.evaluacion.id_hipotesis for r in ranking]
    orden = ordenes[len(MEDIDAS)]

    pregunta = Pregunta(variable="volumen", valores=["1000", "menos_de_1000"])
    cubos = [(n, v, rect(10, 10), 1.0) for n, v in [("olga", "frontal"), ("tomas", "cenital")]]
    cubos.append(("sara", "lateral", rect(10, 10), 1.0))
    hueco = arbol_sala(
        cubos,
        [
            _familia("cubo", {"s": MEDIDAS}, volumen="1000"),
            _familia("cubo_hueco", {"s": MEDIDAS, "t": [1, 2, 3]}, volumen="menos_de_1000"),
        ],
        pregunta,
    ).evaluar()

    _comprobar(resultado, g, orden, hueco)
    # Sensibilidad agregada después de ver E6 (no registrada antes): con más valores posibles,
    # no prohibir nada cuesta más, y Merlín se aleja del cilindro.
    fino = ordenes[len(MEDIDAS_FINAS)]
    resultado.comprobar(
        "E6b (posterior). Con 5 valores por medida el orden se mantiene y Merlín se aleja del "
        "cilindro",
        fino == orden and resultado.tablas[-1].filas[-2][0] == "merlin",
    )
    return resultado


def _por_obs(arbol: ArbolHipotesis, id_: str) -> list[str]:
    from factory.transition.deterministic.prediccion import puntuar

    h = arbol.hipotesis(id_)
    activas = arbol.observaciones_activas()
    assert arbol.proyector is not None
    p = puntuar(
        h,
        [(o, arbol.observadores[o.observador_id], arbol.confiabilidad(o)) for o in activas],
        arbol.proyector,
        arbol.universo,
    )
    return [f"{p.por_observacion[o.id]:.3f}" for o in activas]


def _comprobar(
    resultado: ResultadoExperimento,
    g: dict[str, dict[str, str]],
    orden: list[str],
    hueco: ResultadoArbol,
) -> None:
    def iguales(nombre: str, esperado: str) -> bool:
        return g[nombre]["consiliencia"] == g[nombre]["predictiva"] == esperado

    resultado.comprobar("E1. Ambas eligen el cilindro", iguales("E1 cilindro (5.1)", "h_cilindro"))
    resultado.comprobar(
        "E2. Ambas eligen la latente; con γ/α = 2 la consiliencia deja de elegirla y la "
        "predictiva no",
        iguales("E2 expansión (5.2), α=1,5 γ=1", "h_latente")
        and g["E2 expansión (5.2), α=1 γ=2"]["consiliencia"] != "h_latente"
        and g["E2 expansión (5.2), α=1 γ=2"]["predictiva"] == "h_latente",
    )
    resultado.comprobar(
        "E3. Ambas eligen el tapón", iguales("E3 tercer observador (5.3)", "h_tapon")
    )
    resultado.comprobar(
        "E4. Con ω = 0,3 difieren (consiliencia: cilindro; predictiva: tapón); con ω ≥ 0,6 "
        "ambas eligen el tapón",
        g["E4 errata ω=0,3"] == {"consiliencia": "h_cilindro", "predictiva": "h_tapon"}
        and all(iguales(f"E4 errata ω={w}", "h_tapon") for w in ("0,6", "0,9", "1")),
    )
    resultado.comprobar(
        "E5. Ambas declaran el empate",
        all(g["E5 empate"][m].startswith("empate") for m in MODOS),
    )
    # EXP-015 esperaba a Merlín último con medidas {4, 7, 10}; quedó penúltimo (ver bitácora).
    resultado.comprobar(
        "E6 (expectativa parcialmente fallida). Lámpara torcida primera y cilindro sobre "
        "cilindro elíptico; Merlín bajo el cilindro, pero el último es el cilindro elíptico, que "
        "predice con seguridad y se equivoca",
        orden[0] == "lampara_torcida"
        and orden.index("cilindro") < orden.index("merlin") < orden.index("cilindro_eliptico")
        and orden[-1] == "cilindro_eliptico",
    )
    resultado.comprobar(
        "E7. Cubo y cubo hueco empatan: la respuesta de volumen queda sin determinar",
        hueco.respuesta is not None and not hueco.respuesta.determinada,
    )
