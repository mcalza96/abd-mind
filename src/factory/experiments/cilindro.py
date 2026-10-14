"""Experimento 5.1 — Cilindro latente (docs/marco-teorico/05-experimentos-canonicos.md)."""

from factory.experiments.base import ResultadoExperimento, tabla_hipotesis
from factory.experiments.solidos import arbol_cilindro, hipotesis_solido
from factory.transition.deterministic.state_tree import ArbolHipotesis

NOMBRES = {
    "h_esfera": "Esfera",
    "h_cubo": "Cubo",
    "h_cilindro": "Cilindro",
    "h_elipsoide": "Quimera: elipsoide",
    "h_ovalo": "Quimera: óvalo (figura plana)",
}

SCORES_ESPERADOS = {
    "h_cilindro": 13.0,
    "h_esfera": 11.5,
    "h_elipsoide": 11.5,
    "h_cubo": 10.0,
}


def agregar_hipotesis_base(arbol: ArbolHipotesis) -> None:
    arbol.agregar_hipotesis(hipotesis_solido("h_esfera", "esfera"))
    arbol.agregar_hipotesis(hipotesis_solido("h_cubo", "cubo"))
    arbol.agregar_hipotesis(hipotesis_solido("h_cilindro", "cilindro"))
    arbol.agregar_hipotesis(
        hipotesis_solido(
            "h_elipsoide", "elipsoide", "Un sólido intermedio: elipsoide de revolución"
        )
    )


def ejecutar() -> ResultadoExperimento:
    resultado = ResultadoExperimento(
        nombre="cilindro",
        descripcion=(
            "O1 (frontal) ve un rectángulo y O2 (cenital) un círculo. "
            "Se busca el sólido que proyecta ambas sombras, sin promediarlas."
        ),
    )

    arbol = arbol_cilindro()
    agregar_hipotesis_base(arbol)
    arbol.agregar_hipotesis(
        hipotesis_solido("h_ovalo", "ovalo", "Promedio de las etiquetas: un óvalo", dimension=2)
    )
    evaluacion = arbol.evaluar()
    resultado.tablas.append(
        tabla_hipotesis("Igualdad categórica estricta", evaluacion.ranking, evaluacion.m, NOMBRES)
    )

    por_id = {r.evaluacion.id_hipotesis: r for r in evaluacion.ranking}
    ganadora = evaluacion.h_estrella.evaluacion.id_hipotesis if evaluacion.h_estrella else None
    resultado.comprobar("La mejor explicación es el cilindro", ganadora == "h_cilindro")
    resultado.comprobar(
        "Los scores coinciden con la tabla de 05 §5.1",
        all(por_id[i].evaluacion.score_final == s for i, s in SCORES_ESPERADOS.items()),
    )
    resultado.comprobar(
        "La quimera plana se descarta por la regla objeto_tridimensional",
        por_id["h_ovalo"].violaciones == ["objeto_tridimensional"],
    )
    resultado.comprobar(
        "No se sugiere expansión ontológica: el cilindro explica todo",
        not evaluacion.expansion_sugerida,
    )

    # Variante: si se declara que un cuadrado es un rectángulo, el cubo explica y1.
    variante = arbol_cilindro(jerarquia={"cuadrado": ["rectangulo"]})
    agregar_hipotesis_base(variante)
    ev_variante = variante.evaluar()
    resultado.tablas.append(
        tabla_hipotesis(
            "Variante: cuadrado ⊂ rectángulo declarado", ev_variante.ranking, ev_variante.m, NOMBRES
        )
    )
    cubo = next(r for r in ev_variante.ranking if r.evaluacion.id_hipotesis == "h_cubo")
    ganadora_variante = (
        ev_variante.h_estrella.evaluacion.id_hipotesis if ev_variante.h_estrella else None
    )
    resultado.comprobar(
        "Con la jerarquía declarada el cubo sube a C=1 y el cilindro sigue ganando",
        cubo.evaluacion.consiliencia_c == 1 and ganadora_variante == "h_cilindro",
    )
    return resultado
