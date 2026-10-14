"""Experimento 5.2 — Expansión ontológica (docs/marco-teorico/05-experimentos-canonicos.md)."""

from factory.contracts.abduction import HipotesisCandidata
from factory.experiments.base import ResultadoExperimento, tabla_hipotesis
from factory.experiments.solidos import arbol_cilindro, hipotesis_solido
from factory.transition.deterministic.state_tree import ArbolHipotesis

VOCABULARIO = {"esfera", "cubo", "cono"}
# El generador nombra el sólido nuevo; al afirmarlo en 'solido' cuenta en P aunque no se declare.
LATENTE = "cilindro"

NOMBRES = {
    "h_esfera": "Esfera",
    "h_cubo": "Cubo",
    "h_cono": "Cono",
    "h_latente": "Latente: sólido de revolución de perfil rectangular (cilindro)",
}


def _hipotesis_conocidas(arbol: ArbolHipotesis) -> None:
    for solido in sorted(VOCABULARIO):
        arbol.agregar_hipotesis(hipotesis_solido(f"h_{solido}", solido))


def _hipotesis_latente() -> HipotesisCandidata:
    return hipotesis_solido(
        "h_latente",
        "cilindro",
        "Existe un sólido no catalogado: de revolución, con perfil rectangular",
        latentes=[LATENTE],
    )


def ejecutar() -> ResultadoExperimento:
    resultado = ResultadoExperimento(
        nombre="expansion",
        descripcion=(
            "Mismas observaciones que el cilindro, pero el vocabulario solo conoce "
            "esfera, cubo y cono. Ninguna hipótesis conocida explica ambas vistas."
        ),
    )

    arbol = arbol_cilindro(VOCABULARIO)
    _hipotesis_conocidas(arbol)
    antes = arbol.evaluar()
    resultado.tablas.append(tabla_hipotesis("Vocabulario inicial", antes.ranking, antes.m, NOMBRES))
    resultado.comprobar(
        "Se sugiere expansión: ninguna hipótesis conocida alcanza C = m", antes.expansion_sugerida
    )

    arbol.agregar_hipotesis(_hipotesis_latente())
    despues = arbol.evaluar()
    resultado.tablas.append(
        tabla_hipotesis("Tras postular la entidad latente", despues.ranking, despues.m, NOMBRES)
    )
    latente = next(r for r in despues.ranking if r.evaluacion.id_hipotesis == "h_latente")
    ganadora = despues.h_estrella.evaluacion.id_hipotesis if despues.h_estrella else None
    resultado.comprobar(
        "La hipótesis latente gana con C=2, P=1, score 12.0",
        ganadora == "h_latente"
        and (latente.evaluacion.consiliencia_c, latente.evaluacion.parsimonia_p) == (2, 1)
        and latente.evaluacion.score_final == 12.0,
    )
    resultado.comprobar("Tras la expansión ya no se sugiere otra", not despues.expansion_sugerida)

    # Sensibilidad: con γ/α > 1, explicar una observación más no compensa una entidad nueva.
    conservador = arbol_cilindro(VOCABULARIO, alpha=1.0, gamma=2.0)
    _hipotesis_conocidas(conservador)
    conservador.agregar_hipotesis(_hipotesis_latente())
    ev_conservador = conservador.evaluar()
    resultado.tablas.append(
        tabla_hipotesis("Sensibilidad: α=1, γ=2", ev_conservador.ranking, ev_conservador.m, NOMBRES)
    )
    ganadora_conservador = (
        ev_conservador.h_estrella.evaluacion.id_hipotesis if ev_conservador.h_estrella else None
    )
    resultado.comprobar(
        "Con γ/α = 2 la expansión deja de ganar", ganadora_conservador != "h_latente"
    )
    return resultado
