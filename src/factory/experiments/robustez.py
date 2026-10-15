"""Experimentos de robustez epistémica (docs/historico/marco-teorico/09, fase 4b). Sin LLM."""

from factory.config import Config, ConfigRol, ConfigRoles
from factory.contracts.abduction import HipotesisCandidata
from factory.contracts.case import EstadoHipotesis
from factory.contracts.observation import Observacion, Observador
from factory.engine.case_service import ServicioCasos
from factory.engine.modelos import EntradaHipotesis, EntradaObservador
from factory.engine.store import Store
from factory.experiments.base import ResultadoExperimento, Tabla, formatear_score
from factory.experiments.cilindro import agregar_hipotesis_base
from factory.experiments.solidos import SOLIDOS_CONOCIDOS, hipotesis_solido
from factory.organ.projections import VerificadorProyeccion
from factory.organ.rule_engine import RuleEngine, cargar_reglas
from factory.transition.deterministic.ibe_evaluator import IBEEvaluator
from factory.transition.deterministic.state_tree import ArbolHipotesis

OMEGAS = [0.3, 0.6, 0.9, 1.0]


def _arbol_falible(omega_lateral: float) -> tuple[ArbolHipotesis, list[str]]:
    """Frontal y cenital calibrados (ω=0.99); un tercer observador lateral reporta un triángulo."""
    evaluador = IBEEvaluator(rule_engine=RuleEngine(cargar_reglas("sintetico")), lambda_residuo=1.0)
    arbol = ArbolHipotesis(evaluador, VerificadorProyeccion(), SOLIDOS_CONOCIDOS)
    for id_, vista, omega in [("O1", "frontal", 0.99), ("O2", "cenital", 0.99)]:
        arbol.agregar_observador(
            Observador(
                id=id_, nombre=f"Vista {vista}", parametros={"vista": vista}, confiabilidad=omega
            )
        )
    arbol.agregar_observador(
        Observador(
            id="O3",
            nombre="Vista lateral (escaneo)",
            parametros={"vista": "lateral"},
            confiabilidad=omega_lateral,
        )
    )
    arbol.agregar_observacion(
        Observacion(id="y1", observador_id="O1", contenido="rectangulo", valor="rectangulo")
    )
    arbol.agregar_observacion(
        Observacion(id="y2", observador_id="O2", contenido="circulo", valor="circulo")
    )
    agregar_hipotesis_base(arbol)
    derrotadas = arbol.agregar_observacion(
        Observacion(id="y3", observador_id="O3", contenido="triangulo", valor="triangulo")
    )
    return arbol, derrotadas


def _tapon() -> HipotesisCandidata:
    return hipotesis_solido(
        "h_tapon", "tapon_universal", "Cilindro cortado en cuña", latentes=["tapon_universal"]
    )


def errata() -> ResultadoExperimento:
    resultado = ResultadoExperimento(
        nombre="errata",
        descripcion=(
            "Frontal (rectángulo) y cenital (círculo) son observadores calibrados (ω=0.99). Llega "
            "un tercer reporte lateral, 'triángulo', de confiabilidad variable. ¿Error del "
            "observador o tapón universal?"
        ),
    )
    filas = []
    por_omega = {}
    for omega in OMEGAS:
        arbol, derrotadas = _arbol_falible(omega)
        antes = arbol.evaluar()
        arbol.agregar_hipotesis(_tapon())
        despues = arbol.evaluar()
        ganadora = despues.h_estrella.evaluacion if despues.h_estrella else None
        residuo = despues.h_estrella.atribuidas_a_error if despues.h_estrella else {}
        por_omega[omega] = (arbol, derrotadas, antes.expansion_sugerida, ganadora)
        filas.append(
            [
                f"{omega:g}",
                arbol.estado("h_cilindro").value
                + (" (en tensión)" if "h_cilindro" in arbol.en_tension("y3") else ""),
                "sí" if antes.expansion_sugerida else "no",
                ganadora.id_hipotesis if ganadora else "—",
                formatear_score(ganadora.score_final) if ganadora else "—",
                ", ".join(residuo) or "—",
            ]
        )
    resultado.tablas.append(
        Tabla(
            titulo="Decisión según la confiabilidad del observador lateral",
            columnas=[
                "ω lateral",
                "Cilindro tras y3",
                "¿Expandir?",
                "H* final",
                "Score",
                "Supone error en",
            ],
            filas=filas,
        )
    )

    arbol, derrotadas, expandir, ganadora = por_omega[0.3]
    resultado.comprobar(
        "ω=0.3: y3 no derrota al cilindro; queda en tensión",
        not derrotadas and "h_cilindro" in arbol.en_tension("y3"),
    )
    resultado.comprobar(
        "ω=0.3: no se sugiere expandir la ontología por una errata probable", not expandir
    )
    resultado.comprobar(
        "ω=0.3: el cilindro sigue siendo H* y supone que y3 es un error",
        ganadora is not None
        and ganadora.id_hipotesis == "h_cilindro"
        and list(arbol.evaluar_registro("h_cilindro").atribuidas_a_error) == ["y3"],
    )
    _, _, expandir, ganadora = por_omega[0.9]
    resultado.comprobar(
        "ω=0.9: el residuo cuesta más que una entidad: se sugiere expandir y gana el tapón",
        expandir and ganadora is not None and ganadora.id_hipotesis == "h_tapon",
    )
    arbol, derrotadas, _, _ = por_omega[1.0]
    resultado.comprobar(
        "ω=1 (infalible): y3 derrota al cilindro, como en la versión base",
        "h_cilindro" in derrotadas and arbol.estado("h_cilindro") is EstadoHipotesis.DERROTADA,
    )
    return resultado


def _config_sin_llm() -> Config:
    rol = ConfigRol(modelo="sin-llm")
    return Config(roles=ConfigRoles(cortex=rol, generadores=[rol], verificador=rol))


def empate() -> ResultadoExperimento:
    resultado = ResultadoExperimento(
        nombre="empate",
        descripcion=(
            "Un único observador cenital ve un círculo. Esfera, cilindro, cono y elipsoide lo "
            "explican igual de bien: el sistema no debe elegir, sino pedir la vista que separa."
        ),
    )
    store = Store(":memory:")
    servicio = ServicioCasos(store, _config_sin_llm())
    caso = servicio.crear_caso("Objeto visto solo desde arriba", "sintetico").caso_id
    servicio.agregar_observacion(
        caso,
        EntradaObservador(nombre="Cenital", marco="vista cenital", parametros={"vista": "cenital"}),
        "círculo",
        valor="circulo",
    )
    servicio.proponer_hipotesis(
        caso,
        [
            EntradaHipotesis(mecanismo=f"Es un {s}", afirmaciones={"solido": s, "dimension": 3})
            for s in ["esfera", "cilindro", "cono", "elipsoide"]
        ],
        origen="experimento",
    )
    mejor = servicio.mejor_explicacion(caso)
    sugerencias = servicio.sugerir_observacion(caso)
    resultado.tablas.append(
        Tabla(
            titulo="Observaciones sugeridas",
            columnas=["Marco", "Clases", "Predicciones"],
            filas=[
                [c.marco, str(c.clases), ", ".join(f"{k}: {v}" for k, v in c.predicciones.items())]
                for c in sugerencias.consultas
            ],
        )
    )
    resultado.notas.append(mejor.motivo)
    resultado.comprobar(
        "No hay H*: las cuatro hipótesis empatan",
        mejor.h_estrella is None and len(mejor.empatadas) == 4,
    )
    resultado.comprobar(
        "Se sugieren vistas que separan a las cuatro (4 clases), y no la cenital",
        bool(sugerencias.consultas)
        and sugerencias.consultas[0].clases == 4
        and all(c.marco != "vista cenital" for c in sugerencias.consultas),
    )
    primera = sugerencias.consultas[0] if sugerencias.consultas else None
    if primera:
        cilindro = next(i for i, p in primera.predicciones.items() if p == "rectangulo")
        servicio.agregar_observacion(
            caso,
            EntradaObservador(
                nombre=primera.observador_sugerido,
                marco=primera.marco,
                parametros=primera.parametros,
            ),
            "rectángulo",
            valor="rectangulo",
        )
        final = servicio.mejor_explicacion(caso)
        resultado.notas.append(f"tras observar {primera.marco}: {final.motivo}")
        resultado.comprobar(
            "Con la vista sugerida el empate se rompe a favor del cilindro",
            final.h_estrella is not None and final.h_estrella.id_hipotesis == cilindro,
        )
    store.cerrar()
    return resultado
