"""Piezas comunes del entorno sintético de sólidos (docs/historico/marco-teorico/05 §5.1–5.3)."""

from factory.contracts.abduction import HipotesisCandidata
from factory.contracts.observation import Observacion, Observador
from factory.organ.projections import RelacionConsistencia, VerificadorProyeccion
from factory.organ.rule_engine import RuleEngine, cargar_reglas
from factory.transition.deterministic.ibe_evaluator import IBEEvaluator
from factory.transition.deterministic.state_tree import ArbolHipotesis

SOLIDOS_CONOCIDOS = {"esfera", "cubo", "cilindro", "cono", "elipsoide"}


def observador(id_: str, vista: str) -> Observador:
    return Observador(
        id=id_, nombre=f"Vista {vista}", marco=f"vista {vista}", parametros={"vista": vista}
    )


def observacion(id_: str, observador_id: str, silueta: str) -> Observacion:
    return Observacion(id=id_, observador_id=observador_id, contenido=silueta, valor=silueta)


def hipotesis_solido(
    id_: str,
    solido: str,
    mecanismo: str | None = None,
    *,
    latentes: list[str] | None = None,
    dimension: int = 3,
) -> HipotesisCandidata:
    return HipotesisCandidata(
        id_hipotesis=id_,
        mecanismo_latente=mecanismo or f"El objeto es un {solido}",
        entidades_latentes=latentes or [],
        afirmaciones={"solido": solido, "dimension": dimension},
        origen="experimento",
    )


def nuevo_arbol(
    vocabulario: set[str],
    *,
    alpha: float = 1.5,
    gamma: float = 1.0,
    jerarquia: dict[str, list[str]] | None = None,
) -> ArbolHipotesis:
    evaluador = IBEEvaluator(
        alpha=alpha, beta=10.0, gamma=gamma, rule_engine=RuleEngine(cargar_reglas("sintetico"))
    )
    verificador = VerificadorProyeccion(relacion=RelacionConsistencia(jerarquia))
    return ArbolHipotesis(evaluador, verificador, vocabulario)


def arbol_cilindro(
    vocabulario: set[str] | None = None,
    *,
    alpha: float = 1.5,
    gamma: float = 1.0,
    jerarquia: dict[str, list[str]] | None = None,
) -> ArbolHipotesis:
    """Dos observadores: frontal ve un rectángulo, cenital ve un círculo."""
    arbol = nuevo_arbol(
        SOLIDOS_CONOCIDOS if vocabulario is None else vocabulario,
        alpha=alpha,
        gamma=gamma,
        jerarquia=jerarquia,
    )
    arbol.agregar_observador(observador("O1", "frontal"))
    arbol.agregar_observador(observador("O2", "cenital"))
    arbol.agregar_observacion(observacion("y1", "O1", "rectángulo"))
    arbol.agregar_observacion(observacion("y2", "O2", "círculo"))
    return arbol
