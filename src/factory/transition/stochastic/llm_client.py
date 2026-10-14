"""Cliente LLM compatible con OpenAI, con roles por configuración (D9).

- Habla con dos tipos de endpoint: `/chat/completions` y `/responses`.
- Exige salida JSON y la valida con Pydantic; si no es válida, reintenta indicando el error.
- Envía un `x-opencode-session` estable por cliente y un user agent propio (requisitos de
  OpenCode Go).
- Usa streaming (SSE) en los modelos que lo requieren: la pasarela corta a los ~30 s las
  respuestas sin streaming, y un modelo que razona largo no alcanza a responder.
- Cachea respuestas por cuerpo de petición para que los experimentos sean reproducibles.
- Cuenta llamadas y tokens, y corta al agotar el presupuesto (ADR-0008).
"""

import hashlib
import json
import os
import re
import time
import urllib.error
import urllib.request
import uuid
from collections.abc import Callable, Iterable
from pathlib import Path
from typing import Any, Protocol

from pydantic import BaseModel, Field, ValidationError

from factory.config import Config, ConfigRol

JSON = dict[str, Any]


class ErrorLLM(Exception):
    """Error al obtener una respuesta útil de un modelo."""


class ErrorProveedor(ErrorLLM):
    def __init__(self, estado: int, detalle: str) -> None:
        super().__init__(f"el proveedor respondió {estado}: {detalle}")
        self.estado = estado


class RespuestaInvalida(ErrorLLM):
    """El modelo no devolvió JSON válido para el esquema tras los reintentos."""


class PresupuestoAgotado(ErrorLLM):
    """Se alcanzó el máximo de llamadas permitido."""


# --- transporte ----------------------------------------------------------------------------


class Transporte(Protocol):
    def post(self, ruta: str, cuerpo: JSON, encabezados: dict[str, str]) -> JSON: ...

    def post_eventos(self, ruta: str, cuerpo: JSON, encabezados: dict[str, str]) -> list[JSON]:
        """POST con streaming (SSE): devuelve los eventos `data:` decodificados."""
        ...

    def get(self, ruta: str, encabezados: dict[str, str]) -> JSON: ...


class TransporteHTTP:
    """HTTP con la biblioteca estándar. Respeta HTTPS_PROXY y el almacén de certificados."""

    def __init__(self, base_url: str, timeout_s: float, reintentos: int) -> None:
        self.base_url = base_url.rstrip("/")
        self.timeout_s = timeout_s
        self.reintentos = reintentos

    def post(self, ruta: str, cuerpo: JSON, encabezados: dict[str, str]) -> JSON:
        datos = json.dumps(cuerpo).encode()
        resultado: JSON = self._enviar(
            "POST", ruta, datos, {**encabezados, "Content-Type": "application/json"}, json.load
        )
        return resultado

    def post_eventos(self, ruta: str, cuerpo: JSON, encabezados: dict[str, str]) -> list[JSON]:
        datos = json.dumps(cuerpo).encode()
        encabezados = {
            **encabezados,
            "Content-Type": "application/json",
            "Accept": "text/event-stream",
        }
        eventos: list[JSON] = self._enviar("POST", ruta, datos, encabezados, _leer_eventos)
        return eventos

    def get(self, ruta: str, encabezados: dict[str, str]) -> JSON:
        resultado: JSON = self._enviar("GET", ruta, None, encabezados, json.load)
        return resultado

    def _enviar(
        self,
        metodo: str,
        ruta: str,
        datos: bytes | None,
        encabezados: dict[str, str],
        leer: Callable[[Any], Any],
    ) -> Any:
        for intento in range(self.reintentos + 1):
            peticion = urllib.request.Request(
                self.base_url + ruta, data=datos, method=metodo, headers=encabezados
            )
            try:
                with urllib.request.urlopen(peticion, timeout=self.timeout_s) as respuesta:
                    return leer(respuesta)
            except urllib.error.HTTPError as e:
                detalle = e.read().decode(errors="replace")[:500]
                if e.code < 500 or intento == self.reintentos:
                    raise ErrorProveedor(e.code, detalle) from e
            except (urllib.error.URLError, TimeoutError) as e:
                if intento == self.reintentos:
                    raise ErrorLLM(f"no se pudo contactar al proveedor: {e}") from e
            time.sleep(2**intento)
        raise AssertionError("inalcanzable")


def _leer_eventos(respuesta: Iterable[bytes]) -> list[JSON]:
    eventos = []
    for linea in respuesta:
        texto = linea.decode("utf-8").strip()
        if not texto.startswith("data:"):
            continue
        dato = texto.removeprefix("data:").strip()
        if dato == "[DONE]":
            break
        eventos.append(json.loads(dato))
    return eventos


def reconstruir_responses(eventos: list[JSON]) -> JSON:
    """La respuesta final de /responses viaja completa en el evento de cierre."""
    for evento in reversed(eventos):
        tipo = evento.get("type")
        if tipo == "response.failed":
            error = (evento.get("response") or {}).get("error") or {}
            raise ErrorLLM(f"el modelo falló: {error.get('message', error)}")
        if tipo in ("response.completed", "response.incomplete"):
            respuesta: JSON = evento["response"]
            return respuesta
        if tipo == "error":
            raise ErrorLLM(f"error en el stream: {evento.get('message', evento)}")
    raise ErrorLLM("el stream terminó sin respuesta final")


def reconstruir_chat(eventos: list[JSON]) -> JSON:
    """Une los fragmentos `delta` de /chat/completions en una respuesta completa."""
    contenido: list[str] = []
    fin: str | None = None
    uso: JSON = {}
    for evento in eventos:
        if evento.get("usage"):
            uso = evento["usage"]
        for opcion in evento.get("choices") or []:
            contenido.append((opcion.get("delta") or {}).get("content") or "")
            fin = opcion.get("finish_reason") or fin
    return {
        "choices": [{"message": {"content": "".join(contenido)}, "finish_reason": fin}],
        "usage": uso,
    }


# --- caché ---------------------------------------------------------------------------------


class Cache(Protocol):
    def leer(self, clave: str) -> str | None: ...

    def guardar(self, clave: str, texto: str) -> None: ...


class CacheArchivos:
    """Un archivo JSON por respuesta, nombrado por el hash de la petición."""

    def __init__(self, directorio: Path) -> None:
        self.directorio = directorio

    def _ruta(self, clave: str) -> Path:
        return self.directorio / clave[:2] / f"{clave}.json"

    def leer(self, clave: str) -> str | None:
        ruta = self._ruta(clave)
        if not ruta.is_file():
            return None
        texto = json.loads(ruta.read_text(encoding="utf-8"))["texto"]
        return str(texto)

    def guardar(self, clave: str, texto: str) -> None:
        ruta = self._ruta(clave)
        ruta.parent.mkdir(parents=True, exist_ok=True)
        ruta.write_text(json.dumps({"texto": texto}, ensure_ascii=False), encoding="utf-8")


# --- esquemas ------------------------------------------------------------------------------


def esquema_estricto(modelo: type[BaseModel]) -> JSON:
    """JSON Schema apto para salida estricta: sin títulos ni defaults, todo requerido y cerrado."""

    def limpiar(nodo: Any) -> Any:
        if isinstance(nodo, dict):
            nodo = {k: limpiar(v) for k, v in nodo.items() if k not in ("title", "default")}
            if nodo.get("type") == "object" and "properties" in nodo:
                nodo["required"] = list(nodo["properties"])
                nodo["additionalProperties"] = False
            return nodo
        if isinstance(nodo, list):
            return [limpiar(v) for v in nodo]
        return nodo

    resultado: JSON = limpiar(modelo.model_json_schema())
    return resultado


_BLOQUE_CODIGO = re.compile(r"^\s*```(?:json)?\s*(.*?)\s*```\s*$", re.DOTALL)


def extraer_json(texto: str) -> str:
    """Quita un bloque de código Markdown alrededor del JSON, si lo hay."""
    m = _BLOQUE_CODIGO.match(texto)
    return m.group(1) if m else texto.strip()


# --- cliente -------------------------------------------------------------------------------


class UsoModelo(BaseModel):
    llamadas: int = 0
    desde_cache: int = 0
    tokens_entrada: int = 0
    tokens_salida: int = 0


class Uso(BaseModel):
    por_modelo: dict[str, UsoModelo] = Field(default_factory=dict)

    def de(self, modelo: str) -> UsoModelo:
        return self.por_modelo.setdefault(modelo, UsoModelo())

    @property
    def llamadas(self) -> int:
        return sum(u.llamadas for u in self.por_modelo.values())


ESFUERZO = {
    "desactivado": "minimal",
    "minimo": "minimal",
    "bajo": "low",
    "medio": "medium",
    "alto": "high",
}


def parametros_razonamiento(api: str, nivel: str) -> JSON:
    """Parámetros de razonamiento según la API (probados contra OpenCode Go, ver EXP-011).

    /responses (Muse): `reasoning.effort`, sin opción de apagarlo (lo mínimo es "minimal").
    /chat/completions (DeepSeek): `reasoning_effort`, o `thinking: disabled` para apagarlo.
    """
    if api == "responses":
        return {"reasoning": {"effort": ESFUERZO[nivel]}}
    if nivel == "desactivado":
        return {"thinking": {"type": "disabled"}}
    return {"reasoning_effort": "low" if nivel == "minimo" else ESFUERZO[nivel]}


class ClienteLLM:
    def __init__(
        self,
        config: Config,
        transporte: Transporte | None = None,
        cache: Cache | None = None,
        *,
        sesion: str | None = None,
        max_llamadas: int | None = None,
    ) -> None:
        self.config = config
        proveedor = config.proveedor
        self.transporte = transporte or TransporteHTTP(
            proveedor.base_url, proveedor.timeout_s, proveedor.reintentos_red
        )
        if cache is None and config.cache_dir is not None:
            cache = CacheArchivos(config.cache_dir)
        self.cache = cache
        self.sesion = sesion or f"abd-mind-{uuid.uuid4()}"
        self.max_llamadas = max_llamadas
        self.uso = Uso()
        self.avisos: list[str] = []

    def encabezados(self) -> dict[str, str]:
        encabezados = {
            "User-Agent": self.config.proveedor.user_agent,
            "x-opencode-session": self.sesion,
        }
        variable = self.config.proveedor.api_key_env
        clave = os.environ.get(variable) if variable else None
        if clave:
            encabezados["Authorization"] = f"Bearer {clave}"
        return encabezados

    def listar_modelos(self) -> list[str]:
        respuesta = self.transporte.get("/models", self.encabezados())
        return sorted(str(m["id"]) for m in respuesta.get("data", []))

    def completar_json[T: BaseModel](
        self, rol: ConfigRol, sistema: str, usuario: str, esquema: type[T]
    ) -> T:
        """Pide al modelo del rol un JSON que cumpla `esquema` y lo devuelve validado."""
        return self.completar_json_con_modelo(rol, sistema, usuario, esquema)[0]

    def completar_json_con_modelo[T: BaseModel](
        self, rol: ConfigRol, sistema: str, usuario: str, esquema: type[T]
    ) -> tuple[T, str]:
        """Como `completar_json`, y además informa qué modelo respondió.

        Si el modelo principal falla y el rol tiene `fallback`, se reintenta con ese modelo.
        Un presupuesto agotado no activa el fallback.
        """
        try:
            return self._completar_json(rol, sistema, usuario, esquema), rol.modelo
        except PresupuestoAgotado:
            raise
        except ErrorLLM as e:
            if not rol.fallback:
                raise
            self.avisos.append(f"{rol.modelo} falló ({e}); se usó el fallback {rol.fallback}")
            respaldo = rol.model_copy(update={"modelo": rol.fallback, "fallback": None})
            return self._completar_json(respaldo, sistema, usuario, esquema), rol.fallback

    def _completar_json[T: BaseModel](
        self, rol: ConfigRol, sistema: str, usuario: str, esquema: type[T]
    ) -> T:
        modo = self.config.modelo(rol.modelo).salida_json
        if modo == "json_object":
            esquema_json = json.dumps(esquema_estricto(esquema), ensure_ascii=False)
            sistema = (
                f"{sistema}\n\nResponde únicamente con un objeto JSON que cumpla este JSON "
                f"Schema, sin texto adicional:\n{esquema_json}"
            )
        conversacion = [{"role": "user", "content": usuario}]
        ultimo_error = ""
        for _ in range(self.config.presupuestos.reintentos_json + 1):
            texto = self._completar(rol, sistema, conversacion, esquema)
            try:
                return esquema.model_validate_json(extraer_json(texto))
            except ValidationError as e:
                ultimo_error = str(e)[:1500]
                conversacion += [
                    {"role": "assistant", "content": texto},
                    {
                        "role": "user",
                        "content": (
                            "Tu respuesta no es válida para el esquema pedido:\n"
                            f"{ultimo_error}\nDevuelve solo el JSON corregido."
                        ),
                    },
                ]
        raise RespuestaInvalida(
            f"{rol.modelo} no devolvió JSON válido para {esquema.__name__}: {ultimo_error}"
        )

    # --- interno ---------------------------------------------------------------------------

    def _completar(
        self,
        rol: ConfigRol,
        sistema: str,
        conversacion: list[dict[str, str]],
        esquema: type[BaseModel],
    ) -> str:
        modelo = self.config.modelo(rol.modelo)
        if modelo.api == "responses":
            ruta = "/responses"
            cuerpo: JSON = {
                "model": rol.modelo,
                "instructions": sistema,
                "input": conversacion,
                "max_output_tokens": rol.max_tokens,
            }
            if modelo.salida_json == "json_schema":
                cuerpo["text"] = {"format": self._formato_esquema(esquema)}
            else:
                cuerpo["text"] = {"format": {"type": "json_object"}}
        else:
            ruta = "/chat/completions"
            cuerpo = {
                "model": rol.modelo,
                "messages": [{"role": "system", "content": sistema}, *conversacion],
                "max_tokens": rol.max_tokens,
            }
            if modelo.salida_json == "json_schema":
                cuerpo["response_format"] = {
                    "type": "json_schema",
                    "json_schema": self._formato_esquema(esquema),
                }
            else:
                cuerpo["response_format"] = {"type": "json_object"}
        if rol.temperatura is not None:
            cuerpo["temperature"] = rol.temperatura
        if rol.razonamiento is not None:
            cuerpo.update(parametros_razonamiento(modelo.api, rol.razonamiento))

        clave = hashlib.sha256(
            json.dumps(
                [self.config.proveedor.base_url, ruta, cuerpo], sort_keys=True, ensure_ascii=False
            ).encode()
        ).hexdigest()
        uso = self.uso.de(rol.modelo)
        if self.cache is not None:
            guardado = self.cache.leer(clave)
            if guardado is not None:
                uso.desde_cache += 1
                return guardado

        if self.max_llamadas is not None and self.uso.llamadas >= self.max_llamadas:
            raise PresupuestoAgotado(f"se alcanzó el máximo de {self.max_llamadas} llamadas")
        uso.llamadas += 1
        if modelo.streaming:
            cuerpo_stream = {**cuerpo, "stream": True}
            if ruta == "/chat/completions":
                cuerpo_stream["stream_options"] = {"include_usage": True}
            eventos = self.transporte.post_eventos(ruta, cuerpo_stream, self.encabezados())
            respuesta = (
                reconstruir_responses(eventos)
                if ruta == "/responses"
                else reconstruir_chat(eventos)
            )
        else:
            respuesta = self.transporte.post(ruta, cuerpo, self.encabezados())
        texto = self._texto(ruta, respuesta, uso)
        if self.cache is not None:
            self.cache.guardar(clave, texto)
        return texto

    @staticmethod
    def _formato_esquema(esquema: type[BaseModel]) -> JSON:
        return {
            "type": "json_schema",
            "name": esquema.__name__,
            "schema": esquema_estricto(esquema),
            "strict": True,
        }

    @staticmethod
    def _texto(ruta: str, respuesta: JSON, uso: UsoModelo) -> str:
        consumo = respuesta.get("usage") or {}
        if ruta == "/responses":
            uso.tokens_entrada += int(consumo.get("input_tokens", 0))
            uso.tokens_salida += int(consumo.get("output_tokens", 0))
            if respuesta.get("status") == "incomplete":
                motivo = (respuesta.get("incomplete_details") or {}).get("reason", "desconocido")
                raise ErrorLLM(f"respuesta incompleta ({motivo}); aumentar max_tokens del rol")
            textos = [
                c.get("text", "")
                for item in respuesta.get("output", [])
                if item.get("type") == "message"
                for c in item.get("content", [])
                if c.get("type") == "output_text"
            ]
            return "".join(textos)

        uso.tokens_entrada += int(consumo.get("prompt_tokens", 0))
        uso.tokens_salida += int(consumo.get("completion_tokens", 0))
        opciones = respuesta.get("choices") or [{}]
        if opciones[0].get("finish_reason") == "length":
            raise ErrorLLM("respuesta truncada por max_tokens; aumentar max_tokens del rol")
        return str((opciones[0].get("message") or {}).get("content") or "")
