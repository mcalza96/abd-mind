"""Caso reservado (docs/historico/marco-teorico/11 §11.6): diagnóstico de una bomba industrial.

Se fijó antes de implementar la fase 4c y no se modifica para hacerlo pasar. Prueba
propiedades generales del veredicto de tres valores, la respuesta contrastiva y el margen, en
un dominio distinto del que motivó los cambios. Los veredictos están fijados de antemano en una
tabla y se marcan como juicios del verificador (no proyecciones).
"""

from factory.contracts.abduction import HipotesisCandidata
from factory.contracts.case import EstadoHipotesis, Pregunta, Relacion, Veredicto
from factory.contracts.observation import Observacion, Observador, RolObservacion
from factory.experiments.base import ResultadoExperimento, Tabla, formatear_score
from factory.transition.deterministic.ibe_evaluator import IBEEvaluator
from factory.transition.deterministic.state_tree import ArbolHipotesis

E, N, X = Relacion.EXPLICA, Relacion.NEUTRAL, Relacion.CONTRADICE


class VerificadorTabla:
    """Veredictos fijados de antemano; la fuente los marca como juicios de un verificador."""

    fuente = "verificador:tabla"

    def __init__(self, tabla: dict[tuple[str, str], Relacion]) -> None:
        self.tabla = tabla

    def verificar(
        self, hipotesis: HipotesisCandidata, observacion: Observacion, observador: Observador
    ) -> Veredicto:
        return Veredicto(
            id_hipotesis=hipotesis.id_hipotesis,
            id_observacion=observacion.id,
            relacion=self.tabla[(hipotesis.id_hipotesis, observacion.id)],
            fuente=self.fuente,
        )


PREGUNTA = Pregunta(
    variable="causa",
    valores=["desgaste", "desalineacion", "cavitacion"],
    descripcion="¿Qué causa el aumento de vibración de la bomba?",
)

HECHOS = {
    "e1": ("La vibración aumentó 3× en dos semanas", RolObservacion.EXPLANANDUM, 0.99),
    "e2": ("La temperatura del rodamiento está normal", RolObservacion.EVIDENCIA, 0.98),
    "e3": ("La presión de succión está bajo el mínimo", RolObservacion.EVIDENCIA, 0.98),
    "e4": ("Hubo un cambio de turno de operadores", RolObservacion.EVIDENCIA, 0.9),
}

HIPOTESIS = {
    "A": ("Desgaste de rodamientos", "desgaste", "rodamiento_desgastado"),
    "B": ("Desalineación del acople", "desalineacion", "acople_desalineado"),
    "C": ("Cavitación por baja presión de succión", "cavitacion", "cavitacion"),
    "C2": ("Cavitación por obstrucción parcial de la succión", "cavitacion", "obstruccion"),
}

TABLA: dict[tuple[str, str], Relacion] = {
    ("A", "e1"): E, ("A", "e2"): X, ("A", "e3"): N, ("A", "e4"): N,
    ("B", "e1"): E, ("B", "e2"): N, ("B", "e3"): N, ("B", "e4"): N,
    ("C", "e1"): E, ("C", "e2"): N, ("C", "e3"): E, ("C", "e4"): N,
    ("C2", "e1"): E, ("C2", "e2"): N, ("C2", "e3"): E, ("C2", "e4"): N,
}  # fmt: skip


def _hecho(i: str) -> Observacion:
    contenido, rol, omega = HECHOS[i]
    return Observacion(
        id=i, observador_id="planta", contenido=contenido, rol=rol, confiabilidad=omega
    )


def arbol_reservado() -> ArbolHipotesis:
    """e1 y e3 registrados; las cuatro hipótesis propuestas."""
    arbol = ArbolHipotesis(
        IBEEvaluator(lambda_residuo=1.0), VerificadorTabla(TABLA), set(), pregunta=PREGUNTA
    )
    arbol.agregar_observador(Observador(id="planta", nombre="Sensores y bitácora de planta"))
    arbol.agregar_observacion(_hecho("e1"))
    arbol.agregar_observacion(_hecho("e3"))
    for id_, (mecanismo, causa, entidad) in HIPOTESIS.items():
        arbol.agregar_hipotesis(
            HipotesisCandidata(
                id_hipotesis=id_,
                mecanismo_latente=mecanismo,
                entidades_latentes=[entidad],
                afirmaciones={"causa": causa},
            )
        )
    return arbol


def _scores(arbol: ArbolHipotesis) -> dict[str, float]:
    return {r.evaluacion.id_hipotesis: r.evaluacion.score_final for r in arbol.evaluar().ranking}


def ejecutar() -> ResultadoExperimento:
    resultado = ResultadoExperimento(
        nombre="reservado",
        descripcion=(
            "Caso fijado antes de implementar la fase 4c (11 §11.6): ¿desgaste, desalineación "
            "o cavitación? Veredictos de tres valores, explananda, respuesta contrastiva y margen."
        ),
    )
    arbol = arbol_reservado()

    # 1. Un hecho al que todas son neutrales no cambia nada.
    antes = _scores(arbol)
    derrotadas_e4 = arbol.agregar_observacion(_hecho("e4"))
    resultado.comprobar(
        "1. e4 (neutral para todas) no cambia ningún score ni derrota a nadie",
        _scores(arbol) == antes and not derrotadas_e4,
    )

    # 2. Solo contradecir derrota.
    derrotadas_e2 = arbol.agregar_observacion(_hecho("e2"))
    resultado.comprobar(
        "2. e2 derrota a A (lo contradice, ω ≥ ω_d) y no a B ni a C (neutrales)",
        derrotadas_e2 == ["A"] and arbol.estado("B") is EstadoHipotesis.VIVA,
    )

    # 3 y 5. Respuesta determinada aunque el mecanismo empate; margen de un veredicto.
    evaluacion = arbol.evaluar()
    respuesta = evaluacion.respuesta
    resultado.tablas.append(
        Tabla(
            titulo="Ranking con e1–e4",
            columnas=["Hipótesis", "Causa", "Score", "Contradice", "Sin explicar"],
            filas=[
                [
                    r.evaluacion.id_hipotesis,
                    str(arbol.clase(r.evaluacion.id_hipotesis)),
                    formatear_score(r.evaluacion.score_final),
                    ", ".join(r.atribuidas_a_error) or "—",
                    ", ".join(r.sin_explicar) or "—",
                ]
                for r in arbol.evaluar_todas()
            ],
        )
    )
    resultado.comprobar(
        "3. C y C2 empatan en mecanismo (no hay H*), pero la respuesta 'cavitacion' está "
        "determinada",
        evaluacion.subdeterminada
        and set(evaluacion.empatadas) == {"C", "C2"}
        and respuesta is not None
        and respuesta.determinada
        and respuesta.valor == "cavitacion",
    )
    resultado.comprobar(
        "5. El margen es de 1 veredicto (subir a B en e3) y la respuesta se informa frágil",
        respuesta is not None and respuesta.margen_veredictos == 1 and respuesta.fragil,
    )
    if respuesta is not None:
        resultado.notas.append(
            f"respuesta: {respuesta.valor}; scores por clase: "
            + ", ".join(f"{k} {v:.2f}" for k, v in respuesta.scores_por_valor.items())
            + f"; margen: {respuesta.margen_veredictos}"
        )

    # 4. Sin e3, la respuesta queda subdeterminada entre clases.
    arbol.retractar_observacion("e3")
    sin_e3 = arbol.evaluar().respuesta
    resultado.comprobar(
        "4. Sin e3 la respuesta queda subdeterminada entre desalineacion y cavitacion",
        sin_e3 is not None
        and not sin_e3.determinada
        and {arbol.clase(i) for i in sin_e3.candidatas} == {"desalineacion", "cavitacion"},
    )
    return resultado
