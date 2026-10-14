"""Experimentos sintéticos con hipótesis generadas por LLM y comparación con la línea base.

La consiliencia se sigue calculando por proyección exacta: el LLM solo propone. Así se mide la
calidad de la generación sin mezclarla con errores de verificación.
"""

from factory.config import Config
from factory.contracts.abduction import HipotesisCandidata
from factory.experiments.base import ResultadoExperimento, Tabla, formatear_score
from factory.experiments.linea_base import respuesta_directa
from factory.experiments.solidos import SOLIDOS_CONOCIDOS, arbol_cilindro
from factory.transition.deterministic.state_tree import ArbolHipotesis
from factory.transition.stochastic.generator import (
    ContextoGeneracion,
    Generador,
    ModoGeneracion,
)
from factory.transition.stochastic.llm_client import ClienteLLM, ErrorLLM


def _nuevo_arbol(config: Config, vocabulario: set[str]) -> ArbolHipotesis:
    return arbol_cilindro(vocabulario, alpha=config.pesos.alpha, gamma=config.pesos.gamma)


def _solido(h: HipotesisCandidata) -> str:
    return str(h.afirmaciones.get("solido", "?"))


def _tabla_pipeline(titulo: str, arbol: ArbolHipotesis) -> Tabla:
    m = len(arbol.observaciones_activas())
    filas = []
    for r in arbol.evaluar_todas():
        e = r.evaluacion
        h = arbol.hipotesis(e.id_hipotesis)
        filas.append(
            [
                e.id_hipotesis,
                _solido(h),
                h.origen.removeprefix("motor:"),
                f"{e.consiliencia_c}/{m}",
                str(e.parsimonia_p),
                f"{e.coherencia_k:g}",
                formatear_score(e.score_final),
                h.mecanismo_latente[:70],
            ]
        )
    return Tabla(
        titulo=titulo,
        columnas=["Id", "Sólido", "Origen", "C", "P", "K", "Score", "Mecanismo"],
        filas=filas,
    )


def _ejecutar(
    nombre: str,
    descripcion: str,
    vocabulario: set[str],
    config: Config,
    cliente: ClienteLLM,
    solido_esperado: str | None,
) -> ResultadoExperimento:
    resultado = ResultadoExperimento(nombre=nombre, descripcion=descripcion)
    arbol = _nuevo_arbol(config, vocabulario)
    dominio = arbol.evaluador.rule_engine.reglas
    generador = Generador(cliente, config.roles.generadores)
    n = config.presupuestos.hipotesis_por_ronda

    def ronda(modo: ModoGeneracion) -> None:
        contexto = ContextoGeneracion(
            dominio=dominio,
            observadores=arbol.observadores,
            observaciones=arbol.observaciones_activas(),
            existentes=arbol.todas_las_hipotesis(),
            vocabulario=arbol.vocabulario,
        )
        generacion = generador.generar(contexto, n, modo)
        resultado.notas += generacion.avisos
        for h in generacion.hipotesis:
            arbol.agregar_hipotesis(h)

    ronda(ModoGeneracion.CONTRASTIVO)
    evaluacion = arbol.evaluar()
    if evaluacion.expansion_sugerida:
        resultado.notas.append("ninguna hipótesis explicó todo: se ejecutó una ronda de expansión")
        ronda(ModoGeneracion.EXPANSION)
        evaluacion = arbol.evaluar()
    resultado.tablas.append(_tabla_pipeline("Pipeline (generación + evaluación)", arbol))

    h_estrella = evaluacion.h_estrella
    ganadora = arbol.hipotesis(h_estrella.evaluacion.id_hipotesis) if h_estrella else None
    resultado.comprobar(
        "El pipeline encuentra una H* que explica todas las observaciones (C = m)",
        h_estrella is not None and h_estrella.evaluacion.consiliencia_c == evaluacion.m,
    )
    if solido_esperado:
        resultado.comprobar(
            f"H* es el {solido_esperado}",
            ganadora is not None and _solido(ganadora) == solido_esperado,
        )

    filas = []
    for rol in config.roles.linea_base:
        try:
            h = respuesta_directa(
                cliente, rol, dominio, arbol.observadores, arbol.observaciones_activas()
            )
        except ErrorLLM as error:
            resultado.notas.append(f"línea base {rol.modelo}: {error}")
            continue
        aislado = _nuevo_arbol(config, vocabulario)
        aislado.agregar_hipotesis(h)
        e = aislado.evaluar_registro(h.id_hipotesis).evaluacion
        filas.append(
            [
                rol.modelo,
                _solido(h),
                f"{e.consiliencia_c}/{evaluacion.m}",
                str(e.parsimonia_p),
                formatear_score(e.score_final),
                h.mecanismo_latente[:70],
            ]
        )
    resultado.tablas.append(
        Tabla(
            titulo="Línea base (una llamada, mismo verificador)",
            columnas=["Modelo", "Sólido", "C", "P", "Score", "Respuesta"],
            filas=filas,
        )
    )

    for modelo, uso in sorted(cliente.uso.por_modelo.items()):
        resultado.notas.append(
            f"uso {modelo}: {uso.llamadas} llamadas, {uso.desde_cache} desde caché, "
            f"{uso.tokens_entrada} tokens de entrada, {uso.tokens_salida} de salida"
        )
    return resultado


def cilindro_llm(config: Config, cliente: ClienteLLM) -> ResultadoExperimento:
    return _ejecutar(
        "cilindro-llm",
        "Experimento 5.1 con hipótesis generadas por los modelos configurados.",
        SOLIDOS_CONOCIDOS,
        config,
        cliente,
        solido_esperado="cilindro",
    )


def expansion_llm(config: Config, cliente: ClienteLLM) -> ResultadoExperimento:
    return _ejecutar(
        "expansion-llm",
        "Experimento 5.2 con hipótesis generadas: el vocabulario solo conoce esfera, cubo y cono.",
        {"esfera", "cubo", "cono"},
        config,
        cliente,
        solido_esperado=None,
    )
