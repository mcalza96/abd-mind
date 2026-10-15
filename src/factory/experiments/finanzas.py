"""Experimento 5.4 — Informes financieros contradictorios (docs/historico/marco-teorico/05 §5.4).

Recorre el motor de casos completo con LLM real: el córtex separa hechos de opiniones, el
verificador LLM decide la consiliencia y las reglas del dominio descartan lo incoherente. Luego
llega evidencia que derrota a la mejor explicación y se generan alternativas.
"""

from factory.config import Config
from factory.engine.case_service import ServicioCasos
from factory.engine.modelos import EntradaHipotesis, EntradaObservador, ResultadoEvaluacionCaso
from factory.engine.store import Store
from factory.experiments.base import ResultadoExperimento, Tabla, formatear_score
from factory.transition.stochastic.llm_client import Cache, Transporte

INFORMES = [
    (
        EntradaObservador(nombre="Analista A", marco="análisis fundamental de estados financieros"),
        "En los últimos tres trimestres el margen bruto de la empresa X cayó 4 puntos "
        "porcentuales. Creemos que la compañía está perdiendo competitividad y recomendamos "
        "vender.",
    ),
    (
        EntradaObservador(nombre="Analista B", marco="análisis de ventas y canales"),
        "El volumen de unidades vendidas por la empresa X creció 18 % interanual. La demanda por "
        "sus productos es sólida: recomendamos comprar.",
    ),
    (
        EntradaObservador(nombre="Prensa sectorial", marco="cobertura periodística del sector"),
        "Durante el último año, el principal competidor de la empresa X perdió cuota de mercado.",
    ),
]

# Un comunicado oficial auditado tiene calibración propia: supera el umbral de derrota (0.95).
# Los analistas y la prensa usan la confiabilidad por defecto del dominio (0.9, ADR-0009).
EVIDENCIA_NUEVA = (
    EntradaObservador(
        nombre="Empresa X", marco="comunicado oficial auditado de la empresa", confiabilidad=0.98
    ),
    "La empresa X informa que sus precios de lista no han cambiado en los últimos 12 meses.",
)

HIPOTESIS = {
    "demanda": EntradaHipotesis(
        mecanismo="La demanda de todo el sector está creciendo",
        afirmaciones={"tendencia_volumen": "alza"},
    ),
    "costos": EntradaHipotesis(
        mecanismo="Suben los costos de los insumos de la empresa X",
        afirmaciones={"tendencia_margen_bruto": "baja"},
    ),
    "precios": EntradaHipotesis(
        mecanismo=(
            "La empresa X aplica una estrategia deliberada de reducción sostenida de precios "
            "para ganar cuota de mercado a costa de su margen"
        ),
        entidades_latentes=["estrategia_de_reduccion_de_precios"],
        afirmaciones={
            "tendencia_precio": "baja_sostenida",
            "tendencia_margen_bruto": "baja",
            "tendencia_volumen": "alza",
        },
    ),
    "quimera": EntradaHipotesis(
        mecanismo="La situación de la empresa X es neutral: lo prudente es mantener",
    ),
    "dividendos": EntradaHipotesis(
        mecanismo=(
            "La empresa X pagó dividendos extraordinarios superiores a su caja disponible, lo "
            "que la obliga a recortar márgenes"
        ),
        afirmaciones={"dividendos_pagados": 120, "caja_disponible": 80},
    ),
}


def _tabla(titulo: str, ev: ResultadoEvaluacionCaso) -> Tabla:
    filas = [
        [
            r.id_hipotesis,
            f"{r.consiliencia_c}/{ev.m}",
            str(r.parsimonia_p),
            formatear_score(r.score_final),
            r.origen.removeprefix("motor:"),
            r.mecanismo[:80],
        ]
        for r in ev.ranking
    ]
    filas += [
        [d.id_hipotesis, "—", "—", "-∞", f"descartada: {', '.join(d.reglas)}", d.mecanismo[:80]]
        for d in ev.descartadas_por_reglas
    ]
    return Tabla(
        titulo=titulo, columnas=["Id", "C", "P", "Score", "Origen", "Mecanismo"], filas=filas
    )


def finanzas_llm(
    config: Config,
    transporte: Transporte | None = None,
    cache: Cache | None = None,
) -> ResultadoExperimento:
    resultado = ResultadoExperimento(
        nombre="finanzas-llm",
        descripcion=(
            "Tres fuentes contradictorias sobre la empresa X; luego un comunicado que derrota "
            "a la mejor explicación."
        ),
    )
    store = Store(":memory:")
    servicio = ServicioCasos(store, config, transporte=transporte, cache=cache)
    caso = servicio.crear_caso("Informes contradictorios sobre la empresa X", "finanzas").caso_id

    opiniones: list[str] = []
    hechos: list[str] = []
    for observador, texto in INFORMES:
        r = servicio.agregar_observacion(caso, observador, texto)
        opiniones += r.opiniones
        hechos += [h.contenido for h in r.hechos]
        resultado.notas += [f"{observador.nombre}: {a}" for a in r.avisos]
    resultado.tablas.append(
        Tabla(
            titulo="Córtex: hechos y opiniones",
            columnas=["Tipo", "Enunciado"],
            filas=[["hecho", h] for h in hechos] + [["opinión", o] for o in opiniones],
        )
    )
    texto_hechos = " ".join(hechos).lower()
    resultado.comprobar(
        "Las recomendaciones (comprar/vender) quedan como opiniones, no como hechos",
        len(opiniones) >= 2 and "recomendamos" not in texto_hechos,
    )

    ids = {
        nombre: h.id_hipotesis
        for nombre, h in zip(
            HIPOTESIS,
            servicio.proponer_hipotesis(
                caso, list(HIPOTESIS.values()), origen="experimento"
            ).hipotesis,
            strict=True,
        )
    }
    evaluacion = servicio.evaluar(caso)
    resultado.tablas.append(_tabla("Evaluación inicial", evaluacion))
    por_id = {r.id_hipotesis: r for r in evaluacion.ranking}
    ganadora = evaluacion.h_estrella.id_hipotesis if evaluacion.h_estrella else None
    resultado.comprobar(
        "La mejor explicación es la estrategia de reducción de precios",
        ganadora == ids["precios"],
    )
    resultado.comprobar(
        "La hipótesis de dividendos se descarta por la regla dividendos_bajo_caja",
        any(
            d.id_hipotesis == ids["dividendos"] and "dividendos_bajo_caja" in d.reglas
            for d in evaluacion.descartadas_por_reglas
        ),
    )
    quimera = por_id.get(ids["quimera"])
    resultado.comprobar(
        "La postura intermedia ('mantener') no explica ningún hecho",
        quimera is not None and quimera.consiliencia_c == 0,
    )

    observador, texto = EVIDENCIA_NUEVA
    evidencia = servicio.nueva_evidencia(caso, observador, texto)
    resultado.comprobar(
        "El comunicado derrota a la hipótesis de reducción de precios",
        ids["precios"] in evidencia.observacion.derrotadas,
    )

    if evidencia.evaluacion.expansion_sugerida or evidencia.evaluacion.h_estrella is None:
        generacion = servicio.generar_hipotesis(caso, modo="expansion")
        resultado.notas += generacion.avisos
        final = servicio.evaluar(caso) if generacion.hipotesis else evidencia.evaluacion
    else:
        final = evidencia.evaluacion
    resultado.tablas.append(_tabla("Tras el comunicado (y generación si hizo falta)", final))
    h = final.h_estrella
    if h:
        resultado.notas.append(
            f"nueva mejor explicación: {h.id_hipotesis} — {h.mecanismo} "
            f"({h.consiliencia_c}/{final.m})"
        )
        if final.respuesta is not None:
            margen = final.respuesta.margen_veredictos
            resultado.notas.append(
                f"margen: {'∞' if margen is None else margen} veredictos"
                + (" (frágil)" if final.respuesta.fragil else "")
            )
    elif final.subdeterminada:
        resultado.notas.append(
            f"subdeterminación: empatan {', '.join(final.empatadas)}; se piden observaciones"
        )
        sugerencias = servicio.sugerir_observacion(caso)
        resultado.notas += sugerencias.avisos
        resultado.tablas.append(
            Tabla(
                titulo="Abducción activa: observaciones que separan a las empatadas",
                columnas=["Observador", "Qué observar", "Clases", "Predicciones"],
                filas=[
                    [
                        c.observador_sugerido[:40],
                        c.que_observar[:60],
                        str(c.clases),
                        "; ".join(f"{k}: {v[:40]}" for k, v in c.predicciones.items()),
                    ]
                    for c in sugerencias.consultas
                ],
            )
        )
    else:
        resultado.notas.append("sin explicación suficiente tras el comunicado")
    resultado.comprobar(
        "Tras el comunicado la mejor explicación ya no es la de reducción de precios",
        h is None or h.id_hipotesis != ids["precios"],
    )
    resultado.notas.append(f"llamadas LLM del caso: {servicio.estado_caso(caso).llamadas}")
    store.cerrar()
    return resultado
