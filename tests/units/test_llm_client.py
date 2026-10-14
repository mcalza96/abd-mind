import json
from pathlib import Path

import pytest
from pydantic import BaseModel

from factory.config import ConfigModelo, ConfigRol, cargar_config
from factory.transition.stochastic.llm_client import (
    CacheArchivos,
    ClienteLLM,
    ErrorLLM,
    PresupuestoAgotado,
    RespuestaInvalida,
    esquema_estricto,
    reconstruir_responses,
)
from tests.units.falsos import (
    TransporteFalso,
    config_prueba,
    respuesta_chat,
    respuesta_responses,
)


class Figura(BaseModel):
    forma: str
    lados: int


CHAT = ConfigRol(modelo="gen-chat", temperatura=0.5, max_tokens=123)
RESPONSES = ConfigRol(modelo="gen-responses")


def _cliente(transporte: TransporteFalso, **kwargs: object) -> ClienteLLM:
    return ClienteLLM(config_prueba(), transporte, sesion="sesion-fija", **kwargs)  # type: ignore[arg-type]


def test_chat_json_object(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("OPENCODE_API_KEY", raising=False)
    t = TransporteFalso(lambda r, c: '{"forma": "triangulo", "lados": 3}')
    figura = _cliente(t).completar_json(CHAT, "sistema", "usuario", Figura)
    assert figura == Figura(forma="triangulo", lados=3)

    ruta, cuerpo, encabezados = t.llamadas[0]
    assert ruta == "/chat/completions"
    assert cuerpo["response_format"] == {"type": "json_object"}
    assert cuerpo["temperature"] == 0.5 and cuerpo["max_tokens"] == 123
    assert '"lados"' in cuerpo["messages"][0]["content"]  # el esquema va en el sistema
    assert encabezados["x-opencode-session"] == "sesion-fija"
    assert encabezados["User-Agent"].startswith("abd-mind/")
    assert "Authorization" not in encabezados


def test_clave_desde_entorno(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("OPENCODE_API_KEY", "secreto")
    assert _cliente(TransporteFalso()).encabezados()["Authorization"] == "Bearer secreto"


def test_responses_json_schema() -> None:
    t = TransporteFalso(lambda r, c: '{"forma": "cuadrado", "lados": 4}')
    assert _cliente(t).completar_json(RESPONSES, "sis", "usr", Figura).lados == 4
    ruta, cuerpo, _ = t.llamadas[0]
    assert ruta == "/responses"
    assert cuerpo["instructions"] == "sis"
    formato = cuerpo["text"]["format"]
    assert formato["type"] == "json_schema" and formato["strict"] is True
    assert "temperature" not in cuerpo


def test_reintenta_con_el_error_y_luego_falla() -> None:
    t = TransporteFalso(crudas=[respuesta_chat("no es json"), respuesta_chat('{"forma": "x"}')])
    t.responder = lambda r, c: '{"forma": "x", "lados": 1}'
    assert _cliente(t).completar_json(CHAT, "s", "u", Figura).lados == 1
    tercera = t.llamadas[2][1]["messages"]
    assert tercera[-1]["role"] == "user" and "no es válida" in tercera[-1]["content"]

    siempre_mal = TransporteFalso(lambda r, c: "nada")
    with pytest.raises(RespuestaInvalida):
        _cliente(siempre_mal).completar_json(CHAT, "s", "u", Figura)
    assert len(siempre_mal.llamadas) == 3  # 1 + reintentos_json


def test_quita_bloque_de_codigo() -> None:
    t = TransporteFalso(lambda r, c: '```json\n{"forma": "a", "lados": 2}\n```')
    assert _cliente(t).completar_json(CHAT, "s", "u", Figura).lados == 2


def test_cache_y_presupuesto(tmp_path: Path) -> None:
    t = TransporteFalso(lambda r, c: '{"forma": "a", "lados": 2}')
    cliente = _cliente(t, cache=CacheArchivos(tmp_path), max_llamadas=1)
    cliente.completar_json(CHAT, "s", "u", Figura)
    cliente.completar_json(CHAT, "s", "u", Figura)
    assert len(t.llamadas) == 1
    assert cliente.uso.de("gen-chat").desde_cache == 1
    with pytest.raises(PresupuestoAgotado):
        cliente.completar_json(CHAT, "s", "otra pregunta", Figura)


def test_respuestas_truncadas() -> None:
    truncada = TransporteFalso(crudas=[respuesta_chat("{", fin="length")])
    with pytest.raises(ErrorLLM, match="max_tokens"):
        _cliente(truncada).completar_json(CHAT, "s", "u", Figura)
    incompleta = TransporteFalso(crudas=[respuesta_responses("{", estado="incomplete")])
    with pytest.raises(ErrorLLM, match="incompleta"):
        _cliente(incompleta).completar_json(RESPONSES, "s", "u", Figura)


@pytest.mark.parametrize("rol", [CHAT, RESPONSES])
def test_streaming(rol: ConfigRol) -> None:
    config = config_prueba()
    config.modelos[rol.modelo] = config.modelos[rol.modelo].model_copy(update={"streaming": True})
    t = TransporteFalso(lambda r, c: '{"forma": "pentagono", "lados": 5}')
    cliente = ClienteLLM(config, t)
    assert cliente.completar_json(rol, "s", "u", Figura).lados == 5
    assert t.llamadas[0][1]["stream"] is True
    assert cliente.uso.de(rol.modelo).tokens_salida == 5


def test_stream_fallido() -> None:
    with pytest.raises(ErrorLLM, match="falló"):
        reconstruir_responses(
            [{"type": "response.failed", "response": {"error": {"message": "x"}}}]
        )
    with pytest.raises(ErrorLLM, match="sin respuesta final"):
        reconstruir_responses([{"type": "response.created"}])


def test_esquema_estricto() -> None:
    esquema = esquema_estricto(Figura)
    assert esquema["required"] == ["forma", "lados"]
    assert esquema["additionalProperties"] is False
    assert "title" not in json.dumps(esquema)


def test_listar_modelos() -> None:
    assert _cliente(TransporteFalso()).listar_modelos() == ["modelo-a", "modelo-b"]


def test_config_de_ejemplo_y_avisos() -> None:
    config = cargar_config(Path(__file__).resolve().parents[2] / "config/abd-mind.example.yaml")
    assert config.avisos() == []
    assert config.modelo("muse-spark-1.3-contributor").api == "responses"
    assert config.modelo("desconocido") == ConfigModelo()

    misma = config_prueba()
    misma.roles.verificador = ConfigRol(modelo="gen-chat")
    assert any("independencia" in a for a in misma.avisos())
