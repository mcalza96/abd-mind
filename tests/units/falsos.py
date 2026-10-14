"""Transporte LLM simulado para probar sin red."""

import json
from collections.abc import Callable
from typing import Any

from factory.config import Config, ConfigModelo, ConfigRol, ConfigRoles

JSON = dict[str, Any]
Responder = Callable[[str, JSON], str]


def respuesta_chat(texto: str, fin: str = "stop") -> JSON:
    return {
        "choices": [{"message": {"content": texto}, "finish_reason": fin}],
        "usage": {"prompt_tokens": 10, "completion_tokens": 5},
    }


def respuesta_responses(texto: str, estado: str = "completed") -> JSON:
    return {
        "status": estado,
        "output": [
            {"type": "reasoning"},
            {"type": "message", "content": [{"type": "output_text", "text": texto}]},
        ],
        "usage": {"input_tokens": 10, "output_tokens": 5},
    }


class TransporteFalso:
    """Responde con `responder(ruta, cuerpo) -> texto` o con respuestas crudas en cola."""

    def __init__(self, responder: Responder | None = None, crudas: list[JSON] | None = None):
        self.responder = responder
        self.crudas = list(crudas or [])
        self.llamadas: list[tuple[str, JSON, dict[str, str]]] = []

    def _respuesta(self, ruta: str, cuerpo: JSON) -> JSON:
        if self.crudas:
            return self.crudas.pop(0)
        assert self.responder is not None
        texto = self.responder(ruta, cuerpo)
        return respuesta_responses(texto) if ruta == "/responses" else respuesta_chat(texto)

    def post(self, ruta: str, cuerpo: JSON, encabezados: dict[str, str]) -> JSON:
        self.llamadas.append((ruta, cuerpo, encabezados))
        return self._respuesta(ruta, cuerpo)

    def post_eventos(self, ruta: str, cuerpo: JSON, encabezados: dict[str, str]) -> list[JSON]:
        self.llamadas.append((ruta, cuerpo, encabezados))
        respuesta = self._respuesta(ruta, cuerpo)
        if ruta == "/responses":
            return [
                {"type": "response.created"},
                {"type": "response.completed", "response": respuesta},
            ]
        texto = respuesta["choices"][0]["message"]["content"]
        mitad = len(texto) // 2
        return [
            {"choices": [{"delta": {"content": texto[:mitad]}, "finish_reason": None}]},
            {"choices": [{"delta": {"content": texto[mitad:]}, "finish_reason": "stop"}]},
            {"choices": [], "usage": respuesta["usage"]},
        ]

    def get(self, ruta: str, encabezados: dict[str, str]) -> JSON:
        return {"data": [{"id": "modelo-b"}, {"id": "modelo-a"}]}


def config_prueba(**cambios: Any) -> Config:
    config = Config(
        modelos={
            "gen-responses": ConfigModelo(api="responses", salida_json="json_schema"),
            "gen-chat": ConfigModelo(api="chat", salida_json="json_object"),
            "verif": ConfigModelo(api="chat", salida_json="json_object"),
        },
        roles=ConfigRoles(
            cortex=ConfigRol(modelo="verif", temperatura=0.0),
            generadores=[ConfigRol(modelo="gen-responses"), ConfigRol(modelo="gen-chat")],
            verificador=ConfigRol(modelo="verif", temperatura=0.0),
            linea_base=[ConfigRol(modelo="gen-chat")],
        ),
    )
    return config.model_copy(update=cambios)


def ultimo_prompt(cuerpo: JSON) -> str:
    """Texto de usuario de una petición, para decidir qué responder."""
    mensajes = cuerpo.get("messages") or cuerpo.get("input") or []
    return json.dumps(mensajes, ensure_ascii=False)
