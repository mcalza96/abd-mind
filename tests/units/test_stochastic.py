import json

from factory.config import ConfigRol
from factory.contracts.abduction import HipotesisCandidata
from factory.contracts.observation import Observacion, Observador
from factory.experiments.con_llm import cilindro_llm
from factory.experiments.solidos import arbol_cilindro, hipotesis_solido
from factory.organ.rule_engine import cargar_reglas
from factory.organ.verifier import VerificadorLLM
from factory.transition.stochastic.cortex import Cortex
from factory.transition.stochastic.generator import (
    ContextoGeneracion,
    Generador,
    ModoGeneracion,
)
from factory.transition.stochastic.llm_client import ClienteLLM
from tests.units.falsos import JSON, TransporteFalso, config_prueba, ultimo_prompt


def _hip(solido: str, latentes: list[str] | None = None, **extra: object) -> JSON:
    return {
        "mecanismo_latente": f"Es un {solido}",
        "entidades_latentes": latentes or [],
        "afirmaciones": [
            {"variable": "solido", "valor": solido},
            {"variable": "dimension", "valor": 3},
            *[{"variable": k, "valor": v} for k, v in extra.items()],
        ],
        "predicados_de_consistencia": [],
        "observaciones_explicadas": ["y1", "y2"],
    }


def _contexto() -> ContextoGeneracion:
    arbol = arbol_cilindro()
    return ContextoGeneracion(
        dominio=cargar_reglas("sintetico"),
        observadores=arbol.observadores,
        observaciones=arbol.observaciones_activas(),
        existentes=[hipotesis_solido("h1", "esfera")],
        vocabulario=arbol.vocabulario,
    )


def test_cortex_separa_hechos_y_opiniones() -> None:
    respuesta = {
        "hechos": [
            {
                "enunciado": "El margen bruto cayó 4 pp",
                "variables": [
                    {"variable": "tendencia_margen_bruto", "valor": "baja"},
                    {"variable": "inventada", "valor": 1},
                ],
            }
        ],
        "opiniones": ["Recomienda vender"],
        "dudas": [],
    }
    t = TransporteFalso(lambda r, c: json.dumps(respuesta))
    cortex = Cortex(ClienteLLM(config_prueba(), t), ConfigRol(modelo="verif"))
    observador = Observador(id="A", nombre="Analista A", marco="fundamental")
    extraccion = cortex.extraer(observador, "texto del informe", cargar_reglas("finanzas"))

    assert extraccion.opiniones == ["Recomienda vender"]
    assert extraccion.hechos[0].variables == {"tendencia_margen_bruto": "baja"}
    assert "inventada" in extraccion.dudas[0]
    obs = extraccion.a_observaciones("A", "obs1")
    assert obs[0].id == "obs1.h1" and obs[0].observador_id == "A"
    assert "texto del informe" in ultimo_prompt(t.llamadas[0][1])


def test_generador_ids_origen_duplicados_y_errores() -> None:
    def responder(ruta: str, cuerpo: JSON) -> str:
        if ruta == "/responses":
            return json.dumps({"hipotesis": [_hip("cilindro"), _hip("esfera"), _hip("cono", x=1)]})
        return json.dumps({"hipotesis": [_hip("cilindro"), _hip("tapon_universal", ["tapon"])]})

    t = TransporteFalso(responder)
    config = config_prueba()
    # Un tercer rol que repite el segundo modelo: todo lo que proponga ya existe.
    roles = [*config.roles.generadores, ConfigRol(modelo="gen-chat")]
    generador = Generador(ClienteLLM(config, t), roles)
    resultado = generador.generar(_contexto(), 3, ModoGeneracion.CONTRASTIVO)

    solidos = [h.afirmaciones["solido"] for h in resultado.hipotesis]
    assert solidos == ["cilindro", "cono", "tapon_universal"]
    assert [h.id_hipotesis for h in resultado.hipotesis] == ["h2", "h3", "h4"]
    assert resultado.hipotesis[0].origen == "motor:gen-responses"
    assert resultado.hipotesis[0].afirmaciones["dimension"] == 3  # entero, no 3.0
    assert any("repetir" in a for a in resultado.avisos)  # esfera y cilindro duplicados
    assert any("'x'" in a for a in resultado.avisos)  # variable desconocida
    # El segundo modelo ve lo que propuso el primero.
    assert "cilindro" in ultimo_prompt(t.llamadas[1][1])


def test_generador_sigue_si_un_modelo_falla() -> None:
    def responder(ruta: str, cuerpo: JSON) -> str:
        return "no json" if ruta == "/responses" else json.dumps({"hipotesis": [_hip("cilindro")]})

    config = config_prueba()
    resultado = Generador(
        ClienteLLM(config, TransporteFalso(responder)), config.roles.generadores
    ).generar(_contexto(), 1, ModoGeneracion.EXPANSION)
    assert len(resultado.hipotesis) == 1
    assert any("gen-responses" in a for a in resultado.avisos)


def test_verificador_llm() -> None:
    t = TransporteFalso(
        lambda r, c: '{"justificacion": "un cilindro de frente es un rectángulo", "explica": true}'
    )
    verificador = VerificadorLLM(ClienteLLM(config_prueba(), t), ConfigRol(modelo="verif"))
    veredicto = verificador.verificar(
        hipotesis_solido("h1", "cilindro"),
        Observacion(id="y1", observador_id="O1", contenido="rectángulo"),
        Observador(id="O1", nombre="Frontal", marco="vista frontal"),
    )
    assert veredicto.explica and veredicto.fuente == "verificador:verif"
    prompt = ultimo_prompt(t.llamadas[0][1])
    assert "vista frontal" in prompt and "rectángulo" in prompt


def test_parsimonia_cuenta_entidades_afirmadas() -> None:
    arbol = arbol_cilindro({"esfera"})
    oculta = HipotesisCandidata(
        id_hipotesis="h", mecanismo_latente="m", afirmaciones={"solido": "Cilindro", "dimension": 3}
    )
    assert arbol.parsimonia(oculta) == 1  # no la declaró latente, pero no está en V


def test_experimento_cilindro_llm_con_transporte_falso() -> None:
    def responder(ruta: str, cuerpo: JSON) -> str:
        prompt = ultimo_prompt(cuerpo)
        if "estado real que describen" in prompt:  # línea base
            return json.dumps(
                {
                    "respuesta": "Un óvalo",
                    "afirmaciones": [{"variable": "solido", "valor": "ovalo"}],
                }
            )
        return json.dumps({"hipotesis": [_hip("esfera"), _hip("cilindro")]})

    config = config_prueba(cache_dir=None)
    resultado = cilindro_llm(config, ClienteLLM(config, TransporteFalso(responder)))
    assert resultado.exito, [c.descripcion for c in resultado.comprobaciones if not c.ok]
    base = resultado.tablas[1].filas[0]
    assert base[1] == "ovalo" and base[2] == "0/2"


def test_origen_registra_el_modelo_que_respondio() -> None:
    def responder(ruta: str, cuerpo: JSON) -> str:
        if cuerpo["model"] == "gen-responses":
            return "no json"
        return json.dumps({"hipotesis": [_hip("cilindro")]})

    config = config_prueba()
    rol = ConfigRol(modelo="gen-responses", fallback="gen-chat")
    resultado = Generador(ClienteLLM(config, TransporteFalso(responder)), [rol]).generar(
        _contexto(), 1, ModoGeneracion.CONTRASTIVO
    )
    assert [h.origen for h in resultado.hipotesis] == ["motor:gen-chat"]
