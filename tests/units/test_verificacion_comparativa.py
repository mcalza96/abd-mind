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


def test_juez_de_parsimonia() -> None:
    def responder(ruta: str, cuerpo: JSON) -> str:
        return json.dumps(
            {
                "postulados": [
                    {"nombre": "Conexión clandestina", "descripcion": ""},
                    {"nombre": "sin huella visual", "descripcion": "cláusula de acomodo"},
                    {"nombre": "conexion_clandestina", "descripcion": "repetido"},
                ]
            }
        )

    postulados = juzgar_postulados(
        ClienteLLM(config_prueba(), TransporteFalso(responder)),
        ConfigRol(modelo="verif"),
        _h("h1"),
        {"O": Observador(id="O", nombre="O")},
        [Observacion(id="y1", observador_id="O", contenido="x")],
    )
    assert postulados == ["conexion_clandestina", "sin_huella_visual"]
    arbol = ArbolHipotesis(IBEEvaluator(), VerificadorTabla({}), set())
    h = _h("h1").model_copy(
        update={"entidades_latentes": ["Conexión clandestina"], "entidades_juzgadas": postulados}
    )
    assert arbol.parsimonia(h) == 2  # declarada y juzgada coinciden: no se cuenta dos veces
