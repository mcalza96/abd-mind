"""Experimento 5.3 — Derrotabilidad: el tercer observador (docs/marco-teorico/05)."""

from factory.contracts.case import EstadoHipotesis
from factory.experiments.base import ResultadoExperimento, tabla_hipotesis
from factory.experiments.cilindro import NOMBRES as NOMBRES_CILINDRO
from factory.experiments.cilindro import agregar_hipotesis_base
from factory.experiments.solidos import arbol_cilindro, hipotesis_solido, observacion, observador

NOMBRES = {**NOMBRES_CILINDRO, "h_tapon": "Latente: tapón universal"}


def ejecutar() -> ResultadoExperimento:
    resultado = ResultadoExperimento(
        nombre="tercer-observador",
        descripcion=(
            "Partiendo del cilindro como mejor explicación, llega O3 (vista lateral) y ve un "
            "triángulo. Luego esa observación se retracta."
        ),
    )

    arbol = arbol_cilindro()
    agregar_hipotesis_base(arbol)
    inicial = arbol.evaluar()
    ganadora_inicial = inicial.h_estrella.evaluacion.id_hipotesis if inicial.h_estrella else None
    resultado.comprobar(
        "Antes de y3 la mejor explicación es el cilindro", ganadora_inicial == "h_cilindro"
    )

    arbol.agregar_observador(observador("O3", "lateral"))
    derrotadas = arbol.agregar_observacion(observacion("y3", "O3", "triángulo"))
    tras_y3 = arbol.evaluar()
    resultado.comprobar(
        "y3 derrota al cilindro (π_lateral = rectángulo ≉ triángulo)", "h_cilindro" in derrotadas
    )
    resultado.comprobar(
        "Sin hipótesis vivas no hay H* y se sugiere expansión",
        tras_y3.h_estrella is None and tras_y3.expansion_sugerida,
    )

    arbol.agregar_hipotesis(
        hipotesis_solido(
            "h_tapon",
            "tapon_universal",
            "Cilindro cortado en cuña: rectángulo de frente, círculo arriba, triángulo de lado",
            latentes=["tapon_universal"],
        )
    )
    con_tapon = arbol.evaluar()
    resultado.tablas.append(
        tabla_hipotesis("Tras y3 y la expansión", arbol.evaluar_todas(), con_tapon.m, NOMBRES)
    )
    tapon = con_tapon.h_estrella
    resultado.comprobar(
        "El tapón universal explica las 3 observaciones y es la nueva H*",
        tapon is not None
        and tapon.evaluacion.id_hipotesis == "h_tapon"
        and tapon.evaluacion.consiliencia_c == 3,
    )
    cilindro = arbol.evaluar_registro("h_cilindro")
    resultado.comprobar(
        "El cilindro conserva el registro de qué evidencia lo derrotó",
        cilindro.estado is EstadoHipotesis.DERROTADA and cilindro.derrotada_por == ["y3"],
    )

    reactivadas = arbol.retractar_observacion("y3")
    tras_retractar = arbol.evaluar()
    resultado.tablas.append(
        tabla_hipotesis("Tras retractar y3", arbol.evaluar_todas(), tras_retractar.m, NOMBRES)
    )
    ganadora_final = (
        tras_retractar.h_estrella.evaluacion.id_hipotesis if tras_retractar.h_estrella else None
    )
    resultado.comprobar(
        "Al retractar y3 el cilindro vuelve a estar vivo y recupera H*",
        "h_cilindro" in reactivadas and ganadora_final == "h_cilindro",
    )
    return resultado
