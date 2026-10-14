"""Servidor MCP (fase 5): el flujo completo desde un cliente MCP genérico, en memoria, por stdio
y por HTTP con token."""

import json
import socket
import sys
import threading
import time
from collections.abc import Iterator
from pathlib import Path
from typing import Any

import httpx2
import pytest
import uvicorn
import yaml
from mcp import Client
from mcp.client.stdio import StdioServerParameters
from mcp.client.streamable_http import streamable_http_client

from factory.engine.case_service import ServicioCasos
from factory.engine.store import Store
from factory.experiments.finanzas import EVIDENCIA_NUEVA, HIPOTESIS, INFORMES
from factory.interfaces.cli import main
from factory.interfaces.mcp_server import VARIABLE_TOKEN, app_http, crear_servidor
from tests.units.falsos import TransporteFalso, config_prueba
from tests.units.test_case_service import responder

RAIZ = Path(__file__).resolve().parents[2]
TOKEN = "token-de-prueba-suficientemente-largo"

HERRAMIENTAS = {
    "listar_dominios",
    "listar_reglas",
    "crear_caso",
    "listar_casos",
    "estado_caso",
    "cerrar_caso",
    "registrar_verdad",
    "agregar_observacion",
    "corregir_observacion",
    "nueva_evidencia",
    "retractar_evidencia",
    "proponer_hipotesis",
    "generar_hipotesis",
    "evaluar",
    "mejor_explicacion",
    "sugerir_observacion",
    "auditoria",
}


@pytest.fixture
def anyio_backend() -> str:
    return "asyncio"


def _servicio(transporte: TransporteFalso | None = None) -> ServicioCasos:
    return ServicioCasos(Store(":memory:"), config_prueba(), transporte=transporte)


async def _llamar(cliente: Client, herramienta: str, **argumentos: Any) -> Any:
    resultado = await cliente.call_tool(herramienta, argumentos)
    assert not resultado.is_error, resultado.content
    return resultado.structured_content


def _vista(nombre: str, vista: str) -> dict[str, Any]:
    return {"nombre": nombre, "marco": f"vista {vista}", "parametros": {"vista": vista}}


async def _flujo_sintetico(cliente: Client) -> None:
    """Pregunta, empate de mecanismos, respuesta determinada, evidencia nueva, verdad."""
    nombres = {t.name for t in (await cliente.list_tools()).tools}
    assert nombres == HERRAMIENTAS

    caso = await _llamar(
        cliente,
        "crear_caso",
        descripcion="¿Qué objeto es?",
        dominio="sintetico",
        pregunta={"variable": "forma", "valores": ["redonda", "angulosa"]},
    )
    caso_id = caso["caso_id"]
    await _llamar(
        cliente,
        "agregar_observacion",
        caso_id=caso_id,
        observador=_vista("Cenital", "cenital"),
        contenido="círculo",
        valor="circulo",
    )
    await _llamar(
        cliente,
        "proponer_hipotesis",
        caso_id=caso_id,
        hipotesis=[
            {
                "mecanismo": f"Es un {s}",
                "afirmaciones": {"solido": s, "dimension": 3, "forma": f},
            }
            for s, f in [("esfera", "redonda"), ("cilindro", "redonda"), ("cubo", "angulosa")]
        ],
        origen="usuario",
    )
    mejor = await _llamar(cliente, "mejor_explicacion", caso_id=caso_id)
    assert mejor["h_estrella"] is None  # esfera y cilindro empatan en mecanismo...
    assert mejor["respuesta"]["valor"] == "redonda"  # ...pero la respuesta está determinada

    evidencia = await _llamar(
        cliente,
        "nueva_evidencia",
        caso_id=caso_id,
        observador=_vista("Frontal", "frontal"),
        contenido="rectángulo",
        valor="rectangulo",
    )
    assert evidencia["evaluacion"]["h_estrella"]["mecanismo"] == "Es un cilindro"

    informe = await _llamar(cliente, "auditoria", caso_id=caso_id)
    assert informe["markdown"].startswith(f"# Auditoría {caso_id}")
    cerrado = await _llamar(
        cliente,
        "cerrar_caso",
        caso_id=caso_id,
        verdad={"descripcion": "Era un cilindro", "valor": "redonda", "fuente": "metrología"},
    )
    assert cerrado["estado"] == "cerrado" and cerrado["estado_verdad"] == "establecida"

    # Errores con código estable del contrato.
    error = await cliente.call_tool("estado_caso", {"caso_id": "caso_999"})
    assert error.is_error
    texto = error.content[0].text  # type: ignore[union-attr]
    assert json.loads(texto[texto.index("{") :])["codigo"] == "caso_no_encontrado"


@pytest.mark.anyio
async def test_flujo_sintetico_en_memoria() -> None:
    async with Client(crear_servidor(_servicio())) as cliente:
        await _flujo_sintetico(cliente)


@pytest.mark.anyio
async def test_flujo_financiero_completo_desde_cliente_mcp() -> None:
    """Término de la fase 5: el caso financiero completo desde un cliente MCP de prueba."""
    async with Client(crear_servidor(_servicio(TransporteFalso(responder)))) as cliente:
        caso_id = (
            await _llamar(cliente, "crear_caso", descripcion="Empresa X", dominio="finanzas")
        )["caso_id"]
        for observador, texto in INFORMES:
            obs = await _llamar(
                cliente,
                "agregar_observacion",
                caso_id=caso_id,
                observador=observador.model_dump(exclude_none=True),
                contenido=texto,
            )
            assert all("recomend" not in h["contenido"].lower() for h in obs["hechos"])
        ids = {
            nombre: h["id_hipotesis"]
            for nombre, h in zip(
                HIPOTESIS,
                (
                    await _llamar(
                        cliente,
                        "proponer_hipotesis",
                        caso_id=caso_id,
                        hipotesis=[h.model_dump() for h in HIPOTESIS.values()],
                    )
                )["hipotesis"],
                strict=True,
            )
        }
        evaluacion = await _llamar(cliente, "evaluar", caso_id=caso_id)
        assert evaluacion["h_estrella"]["id_hipotesis"] == ids["precios"]
        assert [d["id_hipotesis"] for d in evaluacion["descartadas_por_reglas"]] == [
            ids["dividendos"]
        ]

        observador, texto = EVIDENCIA_NUEVA
        evidencia = await _llamar(
            cliente,
            "nueva_evidencia",
            caso_id=caso_id,
            observador=observador.model_dump(exclude_none=True),
            contenido=texto,
        )
        assert ids["precios"] in evidencia["observacion"]["derrotadas"]
        generadas = await _llamar(cliente, "generar_hipotesis", caso_id=caso_id, modo="expansion")
        assert generadas["hipotesis"]
        mejor = await _llamar(cliente, "mejor_explicacion", caso_id=caso_id)
        assert mejor["h_estrella"] is None or mejor["h_estrella"]["id_hipotesis"] != ids["precios"]


def _config(tmp_path: Path) -> Path:
    datos = yaml.safe_load((RAIZ / "config" / "abd-mind.example.yaml").read_text())
    datos["base_datos"] = str(tmp_path / "casos.db")
    datos["cache_dir"] = None
    ruta = tmp_path / "config.yaml"
    ruta.write_text(yaml.safe_dump(datos, allow_unicode=True))
    return ruta


@pytest.mark.anyio
async def test_flujo_por_stdio(tmp_path: Path) -> None:
    parametros = StdioServerParameters(
        command=sys.executable,
        args=["-m", "factory.interfaces.cli", "--config", str(_config(tmp_path)), "serve"],
        cwd=str(RAIZ),
    )
    async with Client(parametros) as cliente:
        await _flujo_sintetico(cliente)


def _puerto_libre() -> int:
    with socket.socket() as s:
        s.bind(("127.0.0.1", 0))
        return int(s.getsockname()[1])


@pytest.fixture
def servidor_http() -> Iterator[str]:
    puerto = _puerto_libre()
    app = app_http(crear_servidor(_servicio()), TOKEN)
    servidor = uvicorn.Server(
        uvicorn.Config(app, host="127.0.0.1", port=puerto, log_level="warning")
    )
    hilo = threading.Thread(target=servidor.run, daemon=True)
    hilo.start()
    for _ in range(100):
        if servidor.started:
            break
        time.sleep(0.05)
    yield f"http://127.0.0.1:{puerto}/mcp"
    servidor.should_exit = True
    hilo.join(timeout=5)


@pytest.mark.anyio
async def test_flujo_por_http_con_token(servidor_http: str) -> None:
    http = httpx2.AsyncClient(headers={"Authorization": f"Bearer {TOKEN}"})
    async with http, Client(streamable_http_client(servidor_http, http_client=http)) as cliente:
        await _flujo_sintetico(cliente)


def test_http_sin_token_responde_401(servidor_http: str) -> None:
    sin = httpx2.post(servidor_http, json={})
    malo = httpx2.post(servidor_http, json={}, headers={"Authorization": "Bearer otro-token-x"})
    assert sin.status_code == 401 and malo.status_code == 401


def test_serve_http_exige_token(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    monkeypatch.delenv(VARIABLE_TOKEN, raising=False)
    assert main(["serve", "--transport", "http"]) == 2
    assert VARIABLE_TOKEN in capsys.readouterr().err


def test_token_corto_se_rechaza() -> None:
    with pytest.raises(ValueError):
        app_http(crear_servidor(_servicio()), "corto")
