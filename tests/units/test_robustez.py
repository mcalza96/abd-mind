import json
import math
from pathlib import Path
from typing import Any

import pytest

from factory.contracts.abduction import HipotesisCandidata
from factory.contracts.case import EstadoHipotesis
from factory.contracts.observation import Observacion, Observador
from factory.engine.case_service import ServicioCasos
from factory.engine.modelos import EntradaHipotesis, EntradaObservador
from factory.engine.store import Store
from factory.experiments.solidos import SOLIDOS_CONOCIDOS, hipotesis_solido
from factory.organ.projections import VerificadorProyeccion
from factory.organ.rule_engine import RuleEngine, cargar_reglas
from factory.transition.deterministic.ibe_evaluator import IBEEvaluator, costo_error
from factory.transition.deterministic.state_tree import ArbolHipotesis
from tests.units.falsos import JSON, TransporteFalso, config_prueba
from tests.units.test_case_service import responder as responder_base


def test_costo_error() -> None:
    assert costo_error(0.9) == pytest.approx(2.302585, rel=1e-5)
    assert costo_error(1.0) == costo_error(0.999)  # tope: nunca infinito
    assert costo_error(0.5) < costo_error(0.9)


def test_score_extendido_se_reduce_al_original() -> None:
    h = HipotesisCandidata(id_hipotesis="h", mecanismo_latente="m")
    base = IBEEvaluator().evaluar_hipotesis(h, consiliencia=2, parsimonia=1)
    extendido = IBEEvaluator(lambda_residuo=0.0).evaluar_con_detalle(
        h, consiliencia=2, parsimonia=1, consiliencia_ponderada=2.0, residuo=5.0
    )[0]
    assert base.score_final == extendido.score_final == pytest.approx(1.5 * 2 + 10 - 1)

    con_residuo = IBEEvaluator(lambda_residuo=2.0).evaluar_con_detalle(
        h, consiliencia=2, parsimonia=1, consiliencia_ponderada=1.8, residuo=0.5
    )[0]
    assert con_residuo.score_final == pytest.approx(1.5 * 1.8 + 10 - 1 - 2.0 * 0.5)
    with pytest.raises(ValueError):
        IBEEvaluator(lambda_residuo=-1)


def _arbol(omega_y3: float, **kwargs: Any) -> ArbolHipotesis:
    evaluador = IBEEvaluator(rule_engine=RuleEngine(cargar_reglas("sintetico")), lambda_residuo=1.0)
    arbol = ArbolHipotesis(evaluador, VerificadorProyeccion(), SOLIDOS_CONOCIDOS, **kwargs)
    for i, vista in [("O1", "frontal"), ("O2", "cenital"), ("O3", "lateral")]:
        arbol.agregar_observador(Observador(id=i, nombre=i, parametros={"vista": vista}))
    arbol.agregar_observacion(Observacion(id="y1", observador_id="O1", contenido="rectangulo"))
    arbol.agregar_observacion(Observacion(id="y2", observador_id="O2", contenido="circulo"))
    arbol.agregar_hipotesis(hipotesis_solido("h_cil", "cilindro"))
    arbol.agregar_observacion(
        Observacion(id="y3", observador_id="O3", contenido="triangulo", confiabilidad=omega_y3)
    )
    return arbol


def test_derrota_graduada_y_tension() -> None:
    debil = _arbol(0.5)
    assert debil.estado("h_cil") is EstadoHipotesis.VIVA
    assert debil.en_tension("y3") == ["h_cil"]
    r = debil.evaluar_registro("h_cil")
    assert r.en_tension_por == ["y3"]
    assert r.atribuidas_a_error == pytest.approx({"y3": costo_error(0.5)})
    # La consiliencia ponderada excluye lo no explicado; el residuo lo cobra.
    assert r.evaluacion.score_final == pytest.approx(1.5 * 2 + 10 - costo_error(0.5))

    debil.retractar_observacion("y3")
    assert debil.en_tension("y3") == []

    fuerte = _arbol(0.97)
    assert fuerte.estado("h_cil") is EstadoHipotesis.DERROTADA

    umbral_alto = _arbol(0.97, omega_derrota=0.99)
    assert umbral_alto.estado("h_cil") is EstadoHipotesis.VIVA


def test_disparo_de_expansion_segun_el_residuo() -> None:
    assert not _arbol(0.3).evaluar().expansion_sugerida  # L = 0.45 + 0.36 < γ
    assert _arbol(0.9).evaluar().expansion_sugerida  # L = 1.35 + 2.30 > γ


def test_empate_no_elige() -> None:
    evaluador = IBEEvaluator(rule_engine=RuleEngine(cargar_reglas("sintetico")))
    arbol = ArbolHipotesis(evaluador, VerificadorProyeccion(), SOLIDOS_CONOCIDOS)
    arbol.agregar_observador(Observador(id="O", nombre="O", parametros={"vista": "cenital"}))
    arbol.agregar_observacion(Observacion(id="y", observador_id="O", contenido="circulo"))
    for s in ["esfera", "cilindro", "cubo"]:
        arbol.agregar_hipotesis(hipotesis_solido(f"h_{s}", s))
    r = arbol.evaluar()
    assert r.h_estrella is None and r.subdeterminada
    assert r.empatadas == ["h_cilindro", "h_esfera"]  # el cubo no explica: no empata

    tolerante = ArbolHipotesis(
        evaluador, VerificadorProyeccion(), SOLIDOS_CONOCIDOS, delta_empate=2
    )
    tolerante.agregar_observador(arbol.observadores["O"])
    tolerante.agregar_observacion(arbol.observaciones["y"])
    for h in arbol.todas_las_hipotesis():
        tolerante.agregar_hipotesis(h)
    assert len(tolerante.evaluar().empatadas) == 3  # con δ=2 el cubo (−1.5) también empata


def test_tau_sin_ganadora_no_es_empate() -> None:
    evaluador = IBEEvaluator(tau=100.0, rule_engine=RuleEngine(cargar_reglas("sintetico")))
    arbol = ArbolHipotesis(evaluador, VerificadorProyeccion(), SOLIDOS_CONOCIDOS)
    arbol.agregar_observador(Observador(id="O", nombre="O", parametros={"vista": "cenital"}))
    arbol.agregar_observacion(Observacion(id="y", observador_id="O", contenido="circulo"))
    arbol.agregar_hipotesis(hipotesis_solido("h", "esfera"))
    r = arbol.evaluar()
    assert r.h_estrella is None and not r.subdeterminada


def _responder(ruta: str, cuerpo: JSON) -> str:
    sistema = cuerpo["messages"][0]["content"] if "messages" in cuerpo else cuerpo["instructions"]
    if "planificador de observaciones" in sistema:
        return json.dumps(
            {
                "consultas": [
                    {
                        "observador_sugerido": "Auditor",
                        "marco": "facturas a distribuidores",
                        "que_observar": "precio neto facturado",
                        "predicciones": [
                            {"id_hipotesis": "h1", "prediccion": "baja"},
                            {"id_hipotesis": "h2", "prediccion": "estable"},
                        ],
                    },
                    {
                        "observador_sugerido": "Nadie",
                        "marco": "x",
                        "que_observar": "algo que no separa",
                        "predicciones": [
                            {"id_hipotesis": "h1", "prediccion": "igual"},
                            {"id_hipotesis": "h2", "prediccion": "igual"},
                        ],
                    },
                ]
            }
        )
    return responder_base(ruta, cuerpo)


def test_servicio_confiabilidad_y_sugerencias_llm(tmp_path: Path) -> None:
    servicio = ServicioCasos(
        Store(tmp_path / "c.db"), config_prueba(), transporte=TransporteFalso(_responder)
    )
    caso = servicio.crear_caso("x", "finanzas").caso_id
    servicio.agregar_observacion(caso, EntradaObservador(nombre="A"), "El margen bruto cayó.")
    auditoria = servicio.auditoria(caso)
    assert auditoria.observadores[0].confiabilidad == 0.9  # por defecto del dominio

    servicio.proponer_hipotesis(
        caso,
        [
            EntradaHipotesis(mecanismo="Suben los costos de insumos"),
            EntradaHipotesis(mecanismo="Suben los costos logísticos"),
        ],
    )
    evaluacion = servicio.evaluar(caso)
    assert evaluacion.subdeterminada and evaluacion.empatadas == ["h1", "h2"]
    assert evaluacion.h_estrella is None

    sugerencias = servicio.sugerir_observacion(caso)
    assert [c.observador_sugerido for c in sugerencias.consultas] == ["Auditor"]
    assert sugerencias.consultas[0].clases == 2

    # Un analista sin calibración (ω=0.9 < 0.95) no derrota: deja las hipótesis en tensión.
    r = servicio.agregar_observacion(
        caso, EntradaObservador(nombre="B"), "El volumen de ventas creció."
    )
    assert r.derrotadas == [] and r.en_tension == ["h1", "h2"]
    mejor = servicio.mejor_explicacion(caso)
    assert mejor.h_estrella is None and len(mejor.empatadas) == 2
    assert math.isclose(
        servicio.evaluar(caso).ranking[0].atribuidas_a_error["o2.h1"], costo_error(0.9)
    )


def test_sugerir_sin_empate(tmp_path: Path) -> None:
    servicio = ServicioCasos(
        Store(tmp_path / "c.db"), config_prueba(), transporte=TransporteFalso(_responder)
    )
    caso = servicio.crear_caso("x", "sintetico").caso_id
    servicio.agregar_observacion(
        caso,
        EntradaObservador(nombre="F", parametros={"vista": "frontal"}),
        "r",
        valor="rectangulo",
    )
    servicio.proponer_hipotesis(
        caso, [EntradaHipotesis(mecanismo="c", afirmaciones={"solido": "cilindro", "dimension": 3})]
    )
    assert servicio.sugerir_observacion(caso).consultas == []
