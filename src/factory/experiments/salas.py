"""Las historias 5, 7 y 8 en código (EXP-014). Sin LLM.

Parte A: el motor actual (`ArbolHipotesis`) sobre salas con siluetas medidas. Las hipótesis
llegan ya ajustadas a los datos, como las propondría un generador después de verlos.

Parte B: prototipo de puntuación predictiva (marco vigente: principios, P3). Cada hipótesis es una
familia con parámetros; cada observación se oculta, se ajustan los parámetros que satisfacen el
máximo de las restantes y se mide la probabilidad de la oculta. Merlín, que se acomoda a todo,
no predice nada.
"""

from collections.abc import Callable, Iterable
from itertools import product

from factory.contracts.abduction import HipotesisCandidata
from factory.contracts.case import Pregunta, Relacion, Veredicto
from factory.contracts.observation import Observacion, Observador
from factory.experiments.base import ResultadoExperimento, Tabla, formatear_score
from factory.organ.rule_engine import RuleEngine, cargar_reglas
from factory.transition.deterministic.ibe_evaluator import IBEEvaluator
from factory.transition.deterministic.state_tree import ArbolHipotesis

VISTAS = ("frontal", "lateral", "cenital")
MEDIDAS = range(1, 13)
LIBRE = "*"  # la hipótesis acepta cualquier silueta en esa vista

Silueta = tuple[str, ...]


def rect(ancho: int, alto: int) -> str:
    return f"rectangulo_{ancho}x{alto}"


def elipse(a: int, b: int) -> str:
    return f"circulo_{a}" if a == b else f"elipse_{a}x{b}"


# --- Parte A: siluetas fijas de cada hipótesis, ya ajustadas a los datos ------------------

SILUETAS_SALA: dict[str, dict[str, str]] = {
    "cilindro": {"frontal": rect(10, 10), "lateral": rect(10, 10), "cenital": elipse(10, 10)},
    "cilindro_eliptico": {
        "frontal": rect(10, 10),
        "lateral": rect(7, 10),
        "cenital": elipse(10, 7),
    },
    # Auxiliares de error ajustadas después de ver: reproducen justo lo observado.
    "cilindro_con_lampara_cenital_torcida": {
        "frontal": rect(10, 10),
        "lateral": rect(10, 10),
        "cenital": elipse(10, 7),
    },
    "eliptico_con_pantalla_lateral_distorsionada": {
        "frontal": rect(10, 10),
        "lateral": rect(10, 10),
        "cenital": elipse(10, 7),
    },
    "objeto_que_se_deforma_desde_arriba": {
        "frontal": rect(10, 10),
        "lateral": rect(10, 10),
        "cenital": LIBRE,
    },
    "merlin": {v: LIBRE for v in VISTAS},
    "cubo": {v: rect(10, 10) for v in VISTAS},
    "cubo_hueco": {v: rect(10, 10) for v in VISTAS},
}
CONOCIDOS = {"cilindro", "cilindro_eliptico", "cubo", "cubo_hueco"}


class VerificadorSala:
    """π exacta con medidas; `LIBRE` explica cualquier silueta."""

    fuente = "proyeccion"

    def verificar(
        self, hipotesis: HipotesisCandidata, observacion: Observacion, observador: Observador
    ) -> Veredicto:
        solido = str(hipotesis.afirmaciones["solido"])
        vista = str(observador.parametros["vista"])
        predicho = SILUETAS_SALA[solido][vista]
        explica = predicho in (LIBRE, observacion.valor)
        return Veredicto(
            id_hipotesis=hipotesis.id_hipotesis,
            id_observacion=observacion.id,
            relacion=Relacion.EXPLICA if explica else Relacion.CONTRADICE,
            fuente=self.fuente,
            justificacion=f"π({vista}) = {predicho} vs {observacion.valor}",
        )


def _hipotesis(solido: str, **afirmaciones: str) -> HipotesisCandidata:
    return HipotesisCandidata(
        id_hipotesis=solido,
        mecanismo_latente=solido.replace("_", " "),
        afirmaciones={"solido": solido, "dimension": 3, **afirmaciones},
        origen="experimento",
    )


def sala(
    observaciones: list[tuple[str, str, str, float]],
    hipotesis: Iterable[HipotesisCandidata],
    pregunta: Pregunta | None = None,
) -> ArbolHipotesis:
    """Observaciones (id, vista, silueta, ω) registradas antes que las hipótesis."""
    evaluador = IBEEvaluator(
        alpha=1.5,
        beta=10.0,
        gamma=1.0,
        lambda_residuo=1.0,
        rule_engine=RuleEngine(cargar_reglas("sintetico")),
    )
    arbol = ArbolHipotesis(evaluador, VerificadorSala(), CONOCIDOS, pregunta=pregunta)
    for id_, vista, silueta, omega in observaciones:
        arbol.agregar_observador(
            Observador(id=f"O_{id_}", nombre=id_, parametros={"vista": vista}, confiabilidad=omega)
        )
        arbol.agregar_observacion(
            Observacion(id=id_, observador_id=f"O_{id_}", contenido=silueta, valor=silueta)
        )
    for h in hipotesis:
        arbol.agregar_hipotesis(h)
    return arbol


def scores(arbol: ArbolHipotesis) -> dict[str, float]:
    return {r.evaluacion.id_hipotesis: r.evaluacion.score_final for r in arbol.evaluar().ranking}


HISTORIA_5 = [
    ("olga", "frontal", rect(10, 10), 0.95),
    ("sara", "lateral", rect(10, 10), 0.95),
    ("tomas", "cenital", elipse(10, 7), 0.95),
]


def _todas(*solidos: str) -> list[HipotesisCandidata]:
    return [_hipotesis(s) for s in solidos]


# --- Parte B: familias con parámetros y puntuación predictiva ------------------------------

Familia = Callable[[], Iterable[dict[str, str]]]
"""Cada parámetro posible, expresado directamente como su silueta en cada vista."""

TECHOS_LIBRES = sorted({elipse(a, b) for a in MEDIDAS for b in MEDIDAS})
PAREDES_LIBRES = sorted({rect(w, h) for w in MEDIDAS for h in MEDIDAS})


def f_cilindro() -> Iterable[dict[str, str]]:
    for d, h in product(MEDIDAS, MEDIDAS):
        yield {"frontal": rect(d, h), "lateral": rect(d, h), "cenital": elipse(d, d)}


def f_eliptico() -> Iterable[dict[str, str]]:
    for a, b, h in product(MEDIDAS, MEDIDAS, MEDIDAS):
        yield {"frontal": rect(a, h), "lateral": rect(b, h), "cenital": elipse(a, b)}


def f_lampara_torcida() -> Iterable[dict[str, str]]:
    """Cilindro; la lámpara cenital torcida acorta un eje del círculo (k ≤ d)."""
    for d, h in product(MEDIDAS, MEDIDAS):
        for k in range(1, d + 1):
            yield {"frontal": rect(d, h), "lateral": rect(d, h), "cenital": elipse(d, k)}


def f_pantalla_lateral() -> Iterable[dict[str, str]]:
    """Cilindro elíptico; la pantalla lateral distorsionada muestra un ancho cualquiera."""
    for a, b, h, s in product(MEDIDAS, MEDIDAS, MEDIDAS, MEDIDAS):
        yield {"frontal": rect(a, h), "lateral": rect(s, h), "cenital": elipse(a, b)}


def f_se_deforma() -> Iterable[dict[str, str]]:
    """Cilindro cuyo techo puede mostrar cualquier silueta: no dice cómo se deforma."""
    for d, h in product(MEDIDAS, MEDIDAS):
        for techo in TECHOS_LIBRES:
            yield {"frontal": rect(d, h), "lateral": rect(d, h), "cenital": techo}


def f_cubo() -> Iterable[dict[str, str]]:
    for s in MEDIDAS:
        yield {v: rect(s, s) for v in VISTAS}


def f_cubo_hueco() -> Iterable[dict[str, str]]:
    """Cubo de lado s con paredes de grosor t: las siluetas no ven el interior."""
    for s in MEDIDAS:
        for _t in range(1, s // 2 + 1):
            yield {v: rect(s, s) for v in VISTAS}


UNIVERSO = {"frontal": PAREDES_LIBRES, "lateral": PAREDES_LIBRES, "cenital": TECHOS_LIBRES}


def prob_oculta(
    familia: Familia | None, entrenamiento: list[tuple[str, str]], vista: str, valor: str
) -> float:
    """P(valor oculto | parámetros que satisfacen el máximo de las demás observaciones).

    `familia=None` es Merlín: cada vista es libre e independiente, así que reparte la
    probabilidad entre todas las siluetas posibles de esa vista.
    """
    if familia is None:
        return 1 / len(UNIVERSO[vista])
    mejor, ajustados = -1, []
    for parametros in familia():
        aciertos = sum(parametros[v] == y for v, y in entrenamiento)
        if aciertos > mejor:
            mejor, ajustados = aciertos, [parametros]
        elif aciertos == mejor:
            ajustados.append(parametros)
    return sum(p[vista] == valor for p in ajustados) / len(ajustados)


def puntaje_predictivo(
    familia: Familia | None, observaciones: list[tuple[str, str]]
) -> tuple[float, list[float]]:
    """Validación dejando una fuera: suma de las probabilidades de cada observación oculta."""
    partes = [
        prob_oculta(familia, observaciones[:i] + observaciones[i + 1 :], vista, valor)
        for i, (vista, valor) in enumerate(observaciones)
    ]
    return sum(partes), partes


FAMILIAS_5: dict[str, Familia | None] = {
    "cilindro": f_cilindro,
    "cilindro_eliptico": f_eliptico,
    "cilindro_con_lampara_cenital_torcida": f_lampara_torcida,
    "eliptico_con_pantalla_lateral_distorsionada": f_pantalla_lateral,
    "objeto_que_se_deforma_desde_arriba": f_se_deforma,
    "merlin": None,
}


def _identificable(familias: dict[str, Familia], observaciones: list[tuple[str, str]]) -> bool:
    """¿Alguna vista separa las predicciones de familias que calzan con lo observado?"""
    for vista in VISTAS:
        predicciones = []
        for familia in familias.values():
            calzan = [p for p in familia() if all(p[v] == y for v, y in observaciones)]
            predicciones.append({p[vista] for p in calzan})
        if any(a != predicciones[0] for a in predicciones[1:]):
            return True
    return False


# --- Experimento ---------------------------------------------------------------------------


def ejecutar() -> ResultadoExperimento:
    resultado = ResultadoExperimento(
        nombre="salas",
        descripcion=(
            "Historias 5, 7 y 8 (EXP-014): cómo falla el motor actual con siluetas medidas, y "
            "qué corrige un prototipo de puntuación predictiva."
        ),
    )
    _parte_a(resultado)
    _parte_b(resultado)
    return resultado


def _fila(nombre: str, valor: float) -> list[str]:
    return [nombre.replace("_", " "), formatear_score(valor) if valor > -1e9 else "-∞"]


def _parte_a(resultado: ResultadoExperimento) -> None:
    # Historia 5: rígidos, auxiliares y monstruo.
    arbol = sala(HISTORIA_5, _todas(*FAMILIAS_5))
    s = scores(arbol)
    resultado.tablas.append(
        Tabla(
            titulo="A. Motor actual, historia 5 (ω = 0,95)",
            columnas=["Hipótesis", "Score"],
            filas=[
                [k.replace("_", " "), f"{v:.2f}"]
                for k, v in sorted(s.items(), key=lambda kv: -kv[1])
            ],
        )
    )
    rigidos = sala(HISTORIA_5, _todas("cilindro", "cilindro_eliptico"))
    rs = scores(rigidos)
    resultado.comprobar(
        "A5a. Cilindro y cilindro elíptico empatan (9,85) y se sugiere expandir",
        abs(rs["cilindro"] - rs["cilindro_eliptico"]) < 1e-9
        and round(rs["cilindro"], 2) == 9.85
        and rigidos.evaluar().expansion_sugerida,
    )
    acomodan = [
        "cilindro_con_lampara_cenital_torcida",
        "eliptico_con_pantalla_lateral_distorsionada",
        "objeto_que_se_deforma_desde_arriba",
        "merlin",
    ]
    resultado.comprobar(
        "A5b. Verdad (lámpara torcida), auxiliar simétrica, monstruo y Merlín empatan en 13,27 "
        "sobre los rígidos: el score no distingue verdad de monstruo",
        len({round(s[h], 6) for h in acomodan}) == 1
        and round(s["merlin"], 2) == 13.27
        and s["merlin"] > s["cilindro"],
    )
    prestigio = sala(
        [
            HISTORIA_5[0],
            ("sara", "lateral", rect(10, 10), 0.8),
            ("tomas", "cenital", elipse(10, 7), 0.99),
        ],
        _todas("cilindro", "cilindro_eliptico"),
    )
    ps = scores(prestigio)
    resultado.comprobar(
        "A5c. Prestigio (Tomás 0,99, Sara 0,8): gana el cilindro elíptico, 11,30 contra 8,02",
        round(ps["cilindro_eliptico"], 2) == 11.30 and round(ps["cilindro"], 2) == 8.02,
    )
    pedro_frente = scores(
        sala(
            [*HISTORIA_5, ("pedro", "frontal", rect(10, 10), 0.95)],
            _todas("cilindro", "cilindro_eliptico"),
        )
    )
    pedro_costado = scores(
        sala(
            [*HISTORIA_5, ("pedro", "lateral", rect(10, 10), 0.95)],
            _todas("cilindro", "cilindro_eliptico"),
        )
    )
    resultado.comprobar(
        "A5d. Pedro repitiendo a Olga (frente) no rompe el empate; repitiendo a Sara, gana el "
        "cilindro (la lectura ciega se equivocó en la primera parte)",
        abs(pedro_frente["cilindro"] - pedro_frente["cilindro_eliptico"]) < 1e-9
        and pedro_costado["cilindro"] > pedro_costado["cilindro_eliptico"],
    )
    pf, pc = pedro_frente, pedro_costado
    resultado.notas.append(
        f"Pedro de frente: {pf['cilindro']:.2f} / {pf['cilindro_eliptico']:.2f}; "
        f"Pedro de costado: {pc['cilindro']:.2f} / {pc['cilindro_eliptico']:.2f}"
    )

    # Historia 7: Merlín con datos consistentes y con error.
    consistente = [*HISTORIA_5[:2], ("tomas", "cenital", elipse(10, 10), 0.95)]
    s7 = scores(sala(consistente, _todas("cilindro", "merlin")))
    resultado.comprobar(
        "A7a. Datos consistentes: el cilindro (14,27) supera a Merlín (13,27) por un punto",
        round(s7["cilindro"], 2) == 14.28 or round(s7["cilindro"], 2) == 14.27,
    )
    resultado.comprobar(
        "A7b. Con la elipse de Tomás, Merlín gana (13,27 contra 9,85)",
        s["merlin"] > s["cilindro"],
    )
    arbol7 = sala(consistente, _todas("cilindro", "merlin"))
    arbol7.agregar_observador(
        Observador(id="O_nueva", nombre="nueva", parametros={"vista": "frontal"}, confiabilidad=1.0)
    )
    derrotadas = arbol7.agregar_observacion(
        Observacion(id="nueva", observador_id="O_nueva", contenido="x", valor=rect(3, 9))
    )
    resultado.comprobar(
        "A7c. Una observación nueva (ω = 1) que contradice al cilindro lo derrota; a Merlín nunca",
        derrotadas == ["cilindro"],
    )

    # Historia 8: volumen y cubo hueco.
    pregunta = Pregunta(variable="volumen", valores=["1000", "menos_de_1000"])
    cubos = [
        ("olga", "frontal", rect(10, 10), 1.0),
        ("tomas", "cenital", rect(10, 10), 1.0),
        ("sara", "lateral", rect(10, 10), 1.0),
    ]
    solo_cubo = sala(cubos, [_hipotesis("cubo", volumen="1000")], pregunta).evaluar().respuesta
    resultado.comprobar(
        "A8a. Solo con el cubo propuesto, la respuesta '1000' queda determinada",
        solo_cubo is not None and solo_cubo.determinada and solo_cubo.valor == "1000",
    )
    ambos = (
        sala(
            cubos,
            [_hipotesis("cubo", volumen="1000"), _hipotesis("cubo_hueco", volumen="menos_de_1000")],
            pregunta,
        )
        .evaluar()
        .respuesta
    )
    separan = [v for v in VISTAS if SILUETAS_SALA["cubo"][v] != SILUETAS_SALA["cubo_hueco"][v]]
    resultado.comprobar(
        "A8b. Con el cubo hueco, la respuesta queda sin determinar y ninguna vista separa",
        ambos is not None and not ambos.determinada and separan == [],
    )


def _parte_b(resultado: ResultadoExperimento) -> None:
    obs = [(v, y) for _, v, y, _ in HISTORIA_5]
    puntajes = {}
    filas = []
    for nombre, familia in FAMILIAS_5.items():
        total, partes = puntaje_predictivo(familia, obs)
        puntajes[nombre] = total
        filas.append([nombre.replace("_", " "), *(f"{p:.3f}" for p in partes), f"{total:.3f}"])
    resultado.tablas.append(
        Tabla(
            titulo="B. Puntuación predictiva, historia 5 (probabilidad de cada observación oculta)",
            columnas=["Hipótesis", "Olga", "Sara", "Tomás", "Total"],
            filas=sorted(filas, key=lambda f: -float(f[-1])),
        )
    )
    p = puntajes
    resultado.notas.append(
        "Puntajes predictivos: " + ", ".join(f"{k} {v:.3f}" for k, v in p.items())
    )
    resultado.comprobar("B1-Merlín. Merlín queda bajo 0,1", p["merlin"] < 0.1)
    # EXP-014 esperaba B1 (monstruo < 0,1) y B2 (empate de auxiliares); ambas fallaron. Las
    # comprobaciones registran lo observado y la bitácora explica por qué.
    resultado.comprobar(
        "B1 (expectativa fallida). El objeto que se deforma no baja de 0,1: solo paga en la "
        "vista donde es vago, y supera al cilindro que da probabilidad 0 a la elipse",
        p["cilindro"]
        < p["objeto_que_se_deforma_desde_arriba"]
        < p["cilindro_con_lampara_cenital_torcida"],
    )
    resultado.comprobar(
        "B2 (expectativa fallida). Las auxiliares no empatan: la pantalla de Sara queda bajo la "
        "lámpara, porque con un cuerpo elíptico que Olga y Sara midan lo mismo es una coincidencia",
        p["eliptico_con_pantalla_lateral_distorsionada"]
        < p["cilindro"]
        < p["cilindro_con_lampara_cenital_torcida"],
    )
    resultado.comprobar("B3. El cilindro elíptico queda bajo 0,5", p["cilindro_eliptico"] < 0.5)
    resultado.comprobar(
        "B4. El objeto que se deforma queda bajo la lámpara torcida",
        p["objeto_que_se_deforma_desde_arriba"] < p["cilindro_con_lampara_cenital_torcida"],
    )
    cubos = [(v, rect(10, 10)) for v in VISTAS]
    resultado.comprobar(
        "B5. Cubo y cubo hueco no son identificables con estas ventanas",
        not _identificable({"cubo": f_cubo, "cubo_hueco": f_cubo_hueco}, cubos),
    )
