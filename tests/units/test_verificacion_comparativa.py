"""Verificación comparativa y parsimonia juzgada (13, ADR-0015)."""

import json
import re

from factory.config import ConfigRol
from factory.contracts.abduction import HipotesisCandidata
from factory.contracts.case import Relacion
from factory.contracts.observation import Observacion, Observador
from factory.experiments.reservado import VerificadorTabla
from factory.organ.verifier import VerificadorComparativo
from factory.transition.deterministic.ibe_evaluator import IBEEvaluator
from factory.transition.deterministic.state_tree import ArbolHipotesis
from factory.transition.stochastic.juez import juzgar_postulados
from factory.transition.stochastic.llm_client import ClienteLLM
from tests.units.falsos import JSON, TransporteFalso, config_prueba, ultimo_prompt

NIVELES = {"h1": "muy_esperable", "h2": "esperable", "h3": "indiferente", "h4": "inesperado"}


def _h(i: str) -> HipotesisCandidata:
    return HipotesisCandidata(id_hipotesis=i, mecanismo_latente=f"mecanismo {i}")


def _comparar(ruta: str, cuerpo: JSON) -> str:
    ids = re.findall(r"- (h\d+): mecanismo", ultimo_prompt(cuerpo))
    # h1 se omite a propósito si aparece junto a h9: prueba el caso de calificación faltante.
    return json.dumps(
        {
            "calificaciones": [
                {"id_hipotesis": i, "justificacion": "", "nivel": NIVELES.get(i, "esperable")}
                for i in ids
                if not (i == "h1" and "h9" in ids)
            ]
        }
    )


def test_una_llamada_califica_a_todas_y_no_recalifica() -> None:
    transporte = TransporteFalso(_comparar)
    vivas = [_h(i) for i in NIVELES]
    verificador = VerificadorComparativo(
        ClienteLLM(config_prueba(), transporte), ConfigRol(modelo="verif"), lambda: vivas
    )
    o = Observacion(id="y1", observador_id="O", contenido="hecho")
    obs = Observador(id="O", nombre="O")
    veredictos = {i: verificador.verificar(_h(i), o, obs) for i in NIVELES}
    assert len(transporte.llamadas) == 1
    assert {i: v.relacion for i, v in veredictos.items()} == {
        "h1": Relacion.EXPLICA,
        "h2": Relacion.EXPLICA,
        "h3": Relacion.NEUTRAL,
        "h4": Relacion.CONTRADICE,
    }
    assert veredictos["h1"].peso == 1.0 and veredictos["h2"].peso == 0.5

    # Una hipótesis nueva se califica con las anteriores como contexto; las viejas no cambian.
    vivas.append(_h("h9"))
    nueva = verificador.verificar(_h("h9"), o, obs)
    assert len(transporte.llamadas) == 2 and "h1" in ultimo_prompt(transporte.llamadas[1][1])
    assert nueva.relacion is Relacion.EXPLICA
    assert verificador.verificar(_h("h1"), o, obs) == veredictos["h1"]


def test_hipotesis_omitida_queda_neutral() -> None:
    verificador = VerificadorComparativo(
        ClienteLLM(config_prueba(), TransporteFalso(_comparar)),
        ConfigRol(modelo="verif"),
        lambda: [_h("h9")],
    )
    v = verificador.verificar(
        _h("h1"),
        Observacion(id="y", observador_id="O", contenido="x"),
        Observador(id="O", nombre="O"),
    )
    assert v.relacion is Relacion.NEUTRAL and v.nivel == "sin_calificar"


def test_consiliencia_ponderada_por_peso() -> None:
    vivas: list[HipotesisCandidata] = []
    verificador = VerificadorComparativo(
        ClienteLLM(config_prueba(), TransporteFalso(_comparar)),
        ConfigRol(modelo="verif"),
        lambda: vivas,
    )
    arbol = ArbolHipotesis(IBEEvaluator(lambda_residuo=1.0), verificador, set())
    arbol.agregar_observador(Observador(id="O", nombre="O", confiabilidad=0.9))
    arbol.agregar_observacion(Observacion(id="y1", observador_id="O", contenido="x"))
    for i in ["h1", "h2"]:
        vivas.append(_h(i))
        arbol.agregar_hipotesis(_h(i))
    s1 = arbol.evaluar_registro("h1").evaluacion.score_final
    s2 = arbol.evaluar_registro("h2").evaluacion.score_final
    assert abs((s1 - s2) - 1.5 * 0.9 * 0.5) < 1e-9  # "esperable" aporta la mitad


def test_juez_de_parsimonia_comparativo() -> None:
    def responder(ruta: str, cuerpo: JSON) -> str:
        prompt = ultimo_prompt(cuerpo)
        assert "ya juzgadas" in prompt and "h0" in prompt  # referencia de granularidad
        return json.dumps(
            {
                "juicios": [
                    {
                        "id_hipotesis": "h1",
                        "postulados": [
                            "Conexión clandestina",
                            "sin huella visual",
                            "conexion_clandestina",
                        ],
                    },
                    {"id_hipotesis": "h0", "postulados": ["no debe usarse"]},
                    {"id_hipotesis": "otra", "postulados": ["ignorada"]},
                ]
            }
        )

    referencia = _h("h0").model_copy(update={"entidades_juzgadas": ["falla_de_sensor"]})
    juicio = juzgar_postulados(
        ClienteLLM(config_prueba(), TransporteFalso(responder)),
        ConfigRol(modelo="verif"),
        [_h("h1"), _h("h2")],
        {"O": Observador(id="O", nombre="O")},
        [Observacion(id="y1", observador_id="O", contenido="x")],
        juzgadas=[referencia],
    )
    assert juicio == {"h1": ["conexion_clandestina", "sin_huella_visual"], "h2": []}
    arbol = ArbolHipotesis(IBEEvaluator(), VerificadorTabla({}), set())
    h = _h("h1").model_copy(
        update={"entidades_latentes": ["Conexión clandestina"], "entidades_juzgadas": juicio["h1"]}
    )
    assert arbol.parsimonia(h) == 2  # declarada y juzgada coinciden: no se cuenta dos veces


def test_parametros_de_razonamiento() -> None:
    from factory.transition.stochastic.llm_client import parametros_razonamiento

    assert parametros_razonamiento("responses", "bajo") == {"reasoning": {"effort": "low"}}
    assert parametros_razonamiento("responses", "desactivado") == {
        "reasoning": {"effort": "minimal"}
    }
    assert parametros_razonamiento("chat", "desactivado") == {"thinking": {"type": "disabled"}}
    assert parametros_razonamiento("chat", "alto") == {"reasoning_effort": "high"}


def test_precalificacion_en_paralelo_una_llamada_por_observacion() -> None:
    from factory.engine.case_service import ServicioCasos
    from factory.engine.modelos import EntradaHipotesis, EntradaObservador
    from factory.engine.store import Store

    def responder(ruta: str, cuerpo: JSON) -> str:
        prompt = ultimo_prompt(cuerpo)
        if "juez de parsimonia" in json.dumps(cuerpo, ensure_ascii=False):
            return json.dumps({"juicios": []})
        ids = re.findall(r"- (h\d+): ", prompt)
        return json.dumps(
            {
                "calificaciones": [
                    {"id_hipotesis": i, "justificacion": "", "nivel": "esperable"} for i in ids
                ]
            }
        )

    transporte = TransporteFalso(responder)
    servicio = ServicioCasos(Store(":memory:"), config_prueba(), transporte=transporte)
    caso = servicio.crear_caso("x", "abierto").caso_id
    for i in range(5):
        servicio.agregar_observacion(
            caso, EntradaObservador(nombre=f"O{i}"), f"hecho {i}", extraer=False
        )
    servicio.proponer_hipotesis(
        caso, [EntradaHipotesis(mecanismo=f"mecanismo {i}") for i in range(3)]
    )
    antes = len(transporte.llamadas)
    evaluacion = servicio.evaluar(caso)
    assert len(transporte.llamadas) - antes == 5  # una calificación por observación
    assert evaluacion.subdeterminada  # las tres empatan: todo "esperable"
