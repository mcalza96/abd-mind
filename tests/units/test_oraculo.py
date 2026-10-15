"""Oráculo de observaciones de la prueba A/B (EXP-017), con el modelo simulado."""

import json
from pathlib import Path

import pytest
from mcp.server.mcpserver.exceptions import ToolError

from factory.bench.oraculo import (
    MAX_PEDIDOS,
    Oraculo,
    codificar_mundo,
    decodificar_mundo,
)
from factory.transition.stochastic.llm_client import ClienteLLM
from tests.units.falsos import JSON, TransporteFalso, config_prueba
from tests.units.test_case_service import _sistema_y_usuario

MUNDO = {
    "casos": [
        {
            "id": "R99",
            "observaciones": [
                {"fecha": "2025-01-01", "marco": "prensa", "contenido": "Algo falló."}
            ],
            "hallazgos": [
                {
                    "id": "h1",
                    "relevante": True,
                    "que_mirar": "registro de la válvula",
                    "contenido": "La válvula estaba abierta.",
                },
                {"id": "h2", "relevante": False, "que_mirar": "clima", "contenido": "Hacía sol."},
            ],
        }
    ]
}


def _responder(ruta: str, cuerpo: JSON) -> str:
    _, usuario = _sistema_y_usuario(cuerpo)
    pide_valvula = "válvula" in usuario.split("SOLICITUD DEL INVESTIGADOR:")[1]
    return json.dumps({"ids": ["h1", "h9"] if pide_valvula else [], "motivo": "prueba"})


def _oraculo(tmp_path: Path) -> Oraculo:
    config = config_prueba()
    cliente = ClienteLLM(config, TransporteFalso(_responder), cache=None)
    return Oraculo(MUNDO, config, tmp_path / "registro.jsonl", "A", cliente=cliente)


def test_mundo_codificado_ida_y_vuelta() -> None:
    texto = codificar_mundo(MUNDO)
    assert "válvula" not in texto and decodificar_mundo(texto) == MUNDO


def test_entrega_solo_lo_que_se_pide_mirar(tmp_path: Path) -> None:
    o = _oraculo(tmp_path)
    assert "Algo falló." in o.ver("R99")
    r = o.pedir("R99", "Quiero ver el registro de la válvula")
    assert [h.contenido for h in r.hallazgos] == ["La válvula estaba abierta."]  # h9 no existe
    vacio = o.pedir("R99", "¿Cuál fue la causa?")
    assert vacio.hallazgos == [] and "concreto" in vacio.nota
    assert vacio.pedidos_restantes == MAX_PEDIDOS - 2
    o.concluir("R99", "La válvula abierta", 0.8, ["error del sensor"])
    tipos = [json.loads(x)["tipo"] for x in (tmp_path / "registro.jsonl").read_text().splitlines()]
    assert tipos == ["ver", "pedido", "pedido", "conclusion"]


def test_limite_de_pedidos_y_errores(tmp_path: Path) -> None:
    o = _oraculo(tmp_path)
    for _ in range(MAX_PEDIDOS):
        o.pedir("R99", "clima")
    agotado = o.pedir("R99", "registro de la válvula")
    assert agotado.hallazgos == [] and agotado.pedidos_restantes == 0
    with pytest.raises(ToolError):
        o.ver("R00")
    with pytest.raises(ToolError):
        o.concluir("R99", "x", 1.5, [])
