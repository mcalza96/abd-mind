"""Servidor MCP de abd-mind (fase 5, ADR-0001 y ADR-0005).

Expone las operaciones del motor de casos (docs/arquitectura/contrato-mcp.md) como
herramientas MCP. No calcula nada: cada herramienta delega en `ServicioCasos`, así que la
frontera estocástico/determinista es la misma que en la CLI y los experimentos.

- stdio: Hermes lanza el proceso. stdout es del protocolo; los registros van a stderr.
- HTTP (Streamable HTTP): exige `Authorization: Bearer <ABD_MIND_TOKEN>`.

Las herramientas son síncronas: el SDK las ejecuta en hilos. Un candado serializa el acceso
al motor (SQLite tiene un solo escritor, ADR-0007).
"""

import hmac
import json
import os
import threading
from collections.abc import Callable
from typing import Literal, TypeVar

from mcp.server.mcpserver import MCPServer
from mcp.server.mcpserver.exceptions import ToolError
from pydantic import BaseModel
from starlette.types import ASGIApp, Receive, Scope, Send

from factory import __version__
from factory.config import ConfigPesos
from factory.contracts.abduction import Valor
from factory.contracts.case import Pregunta
from factory.contracts.observation import RolObservacion
from factory.contracts.rules import ConjuntoReglas
from factory.engine.auditoria import auditoria_markdown
from factory.engine.case_service import ServicioCasos
from factory.engine.modelos import (
    Auditoria,
    EntradaHipotesis,
    EntradaObservador,
    EntradaVerdad,
    ErrorCaso,
    InfoCaso,
    ResultadoEvaluacionCaso,
    ResultadoEvidencia,
    ResultadoHipotesis,
    ResultadoMejorExplicacion,
    ResultadoObservacion,
    ResultadoRetractacion,
    ResultadoSugerencias,
)

VARIABLE_TOKEN = "ABD_MIND_TOKEN"

INSTRUCCIONES = """abd-mind es un motor de razonamiento abductivo: busca la causa latente que \
explica observaciones de distintos observadores que parecen contradecirse. El motor decide; \
tú registras evidencia, propones hipótesis y comunicas resultados.

Flujo típico: crear_caso (con 'pregunta' si el usuario pregunta entre alternativas) → \
agregar_observacion por fuente, con su observador y marco (rol 'explanandum' para lo que se \
quiere entender, 'evidencia' para lo que ayuda a decidir) → proponer_hipotesis y \
generar_hipotesis → evaluar → mejor_explicacion. Si la respuesta no está determinada o es \
frágil, sugerir_observacion. Evidencia nueva: nueva_evidencia; un hecho falso: \
retractar_evidencia.

Nunca calcules ni corrijas scores, C, P o K: repórtalos como los entrega el motor. Las \
opiniones no son evidencia. "No hay explicación suficiente" es una respuesta válida. La \
respuesta explica lo ocurrido; no es una recomendación de inversión ni de acción."""

T = TypeVar("T")


class ListaCasos(BaseModel):
    casos: list[InfoCaso]


class ListaDominios(BaseModel):
    dominios: list[str]


class InformeAuditoria(BaseModel):
    formato: Literal["json", "markdown"]
    markdown: str | None = None
    datos: Auditoria | None = None


def _error(e: ErrorCaso) -> ToolError:
    """Error con código estable (tabla del contrato) y mensaje legible."""
    return ToolError(
        json.dumps({"codigo": e.codigo.value, "mensaje": e.mensaje}, ensure_ascii=False)
    )


def crear_servidor(servicio: ServicioCasos) -> MCPServer:
    servidor = MCPServer(
        name="abd-mind",
        title="abd-mind — razonamiento abductivo",
        instructions=INSTRUCCIONES,
        version=__version__,
    )
    candado = threading.Lock()

    def llamar(operacion: Callable[[], T]) -> T:
        with candado:
            try:
                return operacion()
            except ErrorCaso as e:
                raise _error(e) from e

    # --- gestión de casos ----------------------------------------------------------------

    @servidor.tool()
    def listar_dominios() -> ListaDominios:
        """Dominios disponibles (archivos de reglas). Úsalo antes de crear_caso si dudas."""
        return llamar(lambda: ListaDominios(dominios=servicio.listar_dominios()))

    @servidor.tool()
    def listar_reglas(dominio: str) -> ConjuntoReglas:
        """Reglas, variables y vocabulario de un dominio (solo lectura)."""
        return llamar(lambda: servicio.listar_reglas(dominio))

    @servidor.tool()
    def crear_caso(
        descripcion: str,
        dominio: str,
        pregunta: Pregunta | None = None,
        pesos: ConfigPesos | None = None,
    ) -> InfoCaso:
        """Abre un caso abductivo.

        `pregunta`: si el usuario pregunta entre alternativas (p. ej. ¿estructural o
        transitoria?), declara la variable y sus valores; cada hipótesis deberá fijarla y la
        respuesta se decide entre esos valores. `pesos`: solo si el usuario lo pide.
        """
        return llamar(lambda: servicio.crear_caso(descripcion, dominio, pesos, pregunta))

    @servidor.tool()
    def listar_casos(
        estado: Literal["abierto", "cerrado"] | None = None, limite: int = 50
    ) -> ListaCasos:
        """Casos guardados, del más reciente al más antiguo."""
        return llamar(lambda: ListaCasos(casos=servicio.listar_casos(estado, limite)))

    @servidor.tool()
    def estado_caso(caso_id: str) -> InfoCaso:
        """Resumen del caso sin recalcular: pregunta, respuesta y H* de la última evaluación."""
        return llamar(lambda: servicio.estado_caso(caso_id))

    @servidor.tool()
    def cerrar_caso(caso_id: str, verdad: EntradaVerdad | None = None) -> InfoCaso:
        """Cierra el caso. `verdad`: lo que una fuente independiente reporta que ocurrió."""
        return llamar(lambda: servicio.cerrar_caso(caso_id, verdad))

    @servidor.tool()
    def registrar_verdad(caso_id: str, verdad: EntradaVerdad) -> InfoCaso:
        """Agrega lo que una fuente reporta que realmente ocurrió, aunque el caso esté cerrado.

        No borra versiones anteriores: si dos fuentes confiables discrepan, la verdad queda
        'disputada'. Indica la `fuente`, que debe ser independiente de los observadores del caso.
        """
        return llamar(lambda: servicio.registrar_verdad(caso_id, verdad))

    # --- observaciones -------------------------------------------------------------------

    @servidor.tool()
    def agregar_observacion(
        caso_id: str,
        observador: EntradaObservador,
        contenido: str,
        fuente: str | None = None,
        valor: Valor | None = None,
        rol: RolObservacion = RolObservacion.EXPLANANDUM,
        extraer: bool = True,
    ) -> ResultadoObservacion:
        """Registra lo que reportó un observador; el motor separa hechos de opiniones.

        Indica siempre quién observa y desde qué `marco` (metodología, perspectiva,
        instrumento). `confiabilidad` del observador solo si hay calibración independiente.
        `rol`: 'explanandum' (lo que se quiere entender) o 'evidencia' (ayuda a decidir).
        `valor`: solo para registrar un hecho ya estructurado, sin pasar por el córtex.
        `extraer=false`: el contenido ya es un único hecho atómico; no pasa por el córtex.
        """
        return llamar(
            lambda: servicio.agregar_observacion(
                caso_id,
                observador,
                contenido,
                fuente=fuente,
                valor=valor,
                rol=rol,
                extraer=extraer,
            )
        )

    @servidor.tool()
    def corregir_observacion(
        caso_id: str,
        id_observacion: str,
        contenido: str | None = None,
        valor: Valor | None = None,
        es_opinion: bool = False,
    ) -> ResultadoObservacion:
        """Corrige un hecho mal extraído o lo reclasifica como opinión (si el usuario lo pide)."""
        return llamar(
            lambda: servicio.corregir_observacion(
                caso_id, id_observacion, contenido=contenido, valor=valor, es_opinion=es_opinion
            )
        )

    @servidor.tool()
    def nueva_evidencia(
        caso_id: str,
        observador: EntradaObservador,
        contenido: str,
        fuente: str | None = None,
        valor: Valor | None = None,
        rol: RolObservacion = RolObservacion.EXPLANANDUM,
    ) -> ResultadoEvidencia:
        """Como agregar_observacion, y además reevalúa: informa derrotadas, en tensión y H*."""
        return llamar(
            lambda: servicio.nueva_evidencia(
                caso_id, observador, contenido, fuente=fuente, valor=valor, rol=rol
            )
        )

    @servidor.tool()
    def retractar_evidencia(caso_id: str, id_observacion: str) -> ResultadoRetractacion:
        """Retira un hecho (`o3.h1`) o toda una observación (`o3`); reactiva lo que derrotó."""
        return llamar(lambda: servicio.retractar_evidencia(caso_id, id_observacion))

    # --- hipótesis y evaluación ----------------------------------------------------------

    @servidor.tool()
    def proponer_hipotesis(
        caso_id: str,
        hipotesis: list[EntradaHipotesis],
        origen: Literal["hermes", "usuario"] = "hermes",
    ) -> ResultadoHipotesis:
        """Aporta hipótesis candidatas. Lo que declares que explican no se usa para puntuar.

        Si el caso tiene pregunta, fija su variable en `afirmaciones`. Agrega `predicciones`
        (qué se observaría, en qué plazo y con qué resultado) para saber qué vigilar.
        """
        return llamar(lambda: servicio.proponer_hipotesis(caso_id, hipotesis, origen))

    @servidor.tool()
    def generar_hipotesis(
        caso_id: str,
        n: int | None = None,
        modo: Literal["auto", "contrastivo", "expansion"] = "auto",
    ) -> ResultadoHipotesis:
        """Genera hipótesis con los modelos del motor. 'expansion' postula entidades nuevas.

        Puede tardar minutos en dominios con LLM.
        """
        return llamar(lambda: servicio.generar_hipotesis(caso_id, n, modo))

    @servidor.tool()
    def evaluar(caso_id: str) -> ResultadoEvaluacionCaso:
        """Verifica las hipótesis vivas contra los hechos y calcula el ranking y la respuesta.

        Puede tardar minutos en dominios con LLM (los veredictos se guardan y no se repiten).
        """
        return llamar(lambda: servicio.evaluar(caso_id))

    @servidor.tool()
    def mejor_explicacion(caso_id: str) -> ResultadoMejorExplicacion:
        """H*, la respuesta a la pregunta con su margen, el motivo y qué vigilar.

        h_estrella nulo es una respuesta válida (empate o explicación insuficiente).
        """
        return llamar(lambda: servicio.mejor_explicacion(caso_id))

    @servidor.tool()
    def sugerir_observacion(caso_id: str) -> ResultadoSugerencias:
        """Qué observar para separar a las candidatas cuando hay empate o el resultado es frágil."""
        return llamar(lambda: servicio.sugerir_observacion(caso_id))

    @servidor.tool()
    def auditoria(
        caso_id: str, formato: Literal["json", "markdown"] = "markdown"
    ) -> InformeAuditoria:
        """Historia completa del caso. 'markdown' sirve para enviarla como archivo."""

        def informe() -> InformeAuditoria:
            datos = servicio.auditoria(caso_id)
            if formato == "markdown":
                return InformeAuditoria(formato=formato, markdown=auditoria_markdown(datos))
            return InformeAuditoria(formato=formato, datos=datos)

        return llamar(informe)

    return servidor


# --- HTTP con token --------------------------------------------------------------------------


class ExigirToken:
    """Middleware ASGI: rechaza toda petición HTTP sin `Authorization: Bearer <token>`."""

    def __init__(self, app: ASGIApp, token: str) -> None:
        self.app = app
        self.esperado = f"Bearer {token}".encode()

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] == "http":
            recibido = dict(scope.get("headers") or []).get(b"authorization", b"")
            if not hmac.compare_digest(recibido, self.esperado):
                await send(
                    {
                        "type": "http.response.start",
                        "status": 401,
                        "headers": [
                            (b"content-type", b"application/json"),
                            (b"www-authenticate", b"Bearer"),
                        ],
                    }
                )
                await send({"type": "http.response.body", "body": b'{"error": "no autorizado"}'})
                return
        await self.app(scope, receive, send)


def app_http(servidor: MCPServer, token: str, host: str = "127.0.0.1") -> ASGIApp:
    """Aplicación ASGI Streamable HTTP (ruta /mcp) protegida por token."""
    if len(token) < 16:
        raise ValueError(f"{VARIABLE_TOKEN} debe tener al menos 16 caracteres")
    return ExigirToken(servidor.streamable_http_app(host=host), token)


def token_de_entorno() -> str:
    token = os.environ.get(VARIABLE_TOKEN, "")
    if not token:
        raise ValueError(f"el modo HTTP exige la variable de entorno {VARIABLE_TOKEN}")
    return token
