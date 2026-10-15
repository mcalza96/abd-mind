"""Ejecutor de abd-bench con modelos simulados."""

import json
import re
from pathlib import Path

from factory.bench.casos import TipoCausa, cargar_todos
from factory.bench.ejecutor import SISTEMA_BASE, EjecutorBench, informe_markdown, seleccionar
from tests.units.falsos import JSON, TransporteFalso, config_prueba
from tests.units.test_case_service import _sistema_y_usuario


def _responder(ruta: str, cuerpo: JSON) -> str:
    sistema, usuario = _sistema_y_usuario(cuerpo)
    if sistema.startswith(SISTEMA_BASE):
        return json.dumps({"tipo_de_causa": "entidad_nueva", "mecanismo": "algo oculto"})
    if "generador de hipótesis" in sistema:
        return json.dumps(
            {
                "hipotesis": [
                    {
                        "mecanismo_latente": "Error del instrumento de un observador",
                        "entidades_latentes": [],
                        "afirmaciones": [
                            {"variable": "tipo_de_causa", "valor": "error_del_observador"}
                        ],
                        "predicados_de_consistencia": [],
                        "observaciones_explicadas": [],
                    },
                    {
                        "mecanismo_latente": "Un objeto oculto produce la discrepancia",
                        "entidades_latentes": ["objeto_oculto"],
                        "afirmaciones": [{"variable": "tipo_de_causa", "valor": "entidad_nueva"}],
                        "predicados_de_consistencia": [],
                        "observaciones_explicadas": [],
                    },
                ]
            }
        )
    if "verificador independiente" in sistema:
        calificaciones = [
            {
                "id_hipotesis": m.group(1),
                "justificacion": "prueba",
                "nivel": "muy_esperable"
                if "Error del instrumento" in m.group(2)
                else "indiferente",
            }
            for m in re.finditer(r"^- (\w+): (.*?) \| afirmaciones", usuario, re.MULTILINE)
        ]
        return json.dumps({"calificaciones": calificaciones})
    if "juez de un sistema" in sistema:
        ids = re.findall(r"^- (h\d+): (.*?) \| afirmaciones", usuario, re.MULTILINE)
        orden = sorted((i for i, _ in ids), key=lambda i: "Error" not in dict(ids)[i])
        return json.dumps(
            {"justificacion": "prueba", "orden": orden, "decide": True, "confianza": "alta"}
        )
    if "juez de parsimonia" in sistema:
        return json.dumps({"juicios": []})
    raise AssertionError(f"petición inesperada: {sistema[:60]}")


def test_ejecutor_sobre_un_par(tmp_path: Path) -> None:
    casos = seleccionar(cargar_todos(), ["V03", "B04"], None)
    assert [c.id for c in casos] == ["B04", "V03"]
    transporte = TransporteFalso(_responder)
    resultados = EjecutorBench(config_prueba(), tmp_path, transporte=transporte).ejecutar(
        casos, paralelo=2
    )

    for r in resultados:
        assert r.motor is not None and r.motor.error is None, r.motor
        assert r.motor.tipo is TipoCausa.ERROR_DEL_OBSERVADOR and r.motor.determinada
        assert set(r.motor.tipos_propuestos) == {
            TipoCausa.ERROR_DEL_OBSERVADOR,
            TipoCausa.ENTIDAD_NUEVA,
        }
        assert [b.tipo for b in r.linea_base] == [TipoCausa.ENTIDAD_NUEVA]

    # El motor y la línea base nunca ven la solución, la verdad ni el título del caso.
    prompts = json.dumps([c for _, c, _ in transporte.llamadas], ensure_ascii=False)
    for caso in casos:
        for oculto in [
            caso.titulo,
            caso.solucion.mecanismo,
            caso.verdad.descripcion,
            caso.respuesta_inductiva_erronea,
        ]:
            assert oculto not in prompts, oculto

    informe = informe_markdown(resultados)
    assert "| reales (A–E) | 1/1 | 0/1 |" in informe
    assert "| variantes (V) | 1/1 | 0/1 |" in informe
    assert "| V03 | B04 |" in informe  # sección de casos derivados


def test_seleccion_de_pares() -> None:
    casos = seleccionar(cargar_todos(), ["pares"], None)
    ids = {c.id for c in casos}
    assert len([i for i in ids if i.startswith("V")]) == 10 and "A01" in ids and "A06" in ids


def test_seleccion_v2_y_abstencion() -> None:
    from factory.bench.ejecutor import ResultadoBase, ResultadoCaso, ResultadoMotor, correcta

    casos = seleccionar(cargar_todos(), ["v2"], None)
    series = {c.serie for c in casos}
    assert series == {"P", "U", "V"} and len([c for c in casos if c.serie == "U"]) == 10

    u = ResultadoCaso(
        id="U01",
        serie="U",
        variante_de="V01",
        contaminacion="baja",
        estado_verdad="establecida",
        tipo_verdad=TipoCausa.ENTIDAD_NUEVA,
        tipo_secundario=None,
        determinable=False,
        motor=ResultadoMotor(tipo=None, determinada=False),
        linea_base=[ResultadoBase(modelo="m", tipo=TipoCausa.ENTIDAD_NUEVA)],
    )
    from factory.bench.ejecutor import respuesta_base, respuesta_motor

    assert correcta(u, respuesta_motor(u))  # abstenerse es lo correcto
    assert not correcta(u, respuesta_base(u, "m"))  # elegir un tipo, no
