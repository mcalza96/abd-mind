"""Oráculo de observaciones para la prueba A/B de agentes (EXP-017).

Servidor MCP neutral: lo tienen los dos agentes, con y sin abd-mind. Entrega los hechos de la
época de cada caso y responde a observaciones **concretas** con los hallazgos de la
investigación oficial. Una pregunta por la causa no obtiene nada: hay que decir qué mirar.

Todo queda en un registro JSONL con la hora, el agente (`ABD_ORACULO_AGENTE`) y la decisión
del oráculo, para evaluar después a ciegas.

El mundo (`mundo.b64`) va comprimido y en base64: no es secreto, pero no aparece en una
búsqueda de texto. Los agentes tienen prohibido leer archivos durante la prueba.
"""

import base64
import json
import os
import threading
import zlib
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from mcp.server.mcpserver import MCPServer
from mcp.server.mcpserver.exceptions import ToolError
from pydantic import BaseModel, Field

from factory.config import Config
from factory.transition.stochastic.llm_client import ClienteLLM, ErrorLLM

MAX_PEDIDOS = 8

SISTEMA_ORACULO = """Eres el archivo de una investigación. Un investigador pide mirar algo \
concreto. Tienes una lista de HALLAZGOS; cada uno indica qué hay que mirar para obtenerlo \
("que_mirar") y qué se encontró. Devuelve los ids de los hallazgos que esa solicitud obtendría.

Reglas:
- Entrega un hallazgo solo si la solicitud apunta a mirar eso concretamente: el mismo \
registro, objeto, ensayo, documento o persona, o uno equivalente que mostraría lo mismo.
- Preguntas por la causa, por conclusiones o por "todo lo que haya" no obtienen nada.
- Ante la duda, no entregues. Un investigador que pide mirar bien obtiene; uno que adivina, no.
- Puedes devolver una lista vacía."""

INSTRUCCIONES = """Oráculo de una prueba de investigación. Cada caso tiene hechos iniciales \
(ver_caso). Puedes pedir observaciones concretas (pedir_observacion: qué registro, objeto, \
ensayo o persona mirar); solo obtienes lo que pides mirar, como mucho 8 pedidos por caso. \
Cuando termines un caso, registra tu conclusión con concluir. No busques en la web ni leas \
archivos durante la prueba."""


class Seleccion(BaseModel):
    ids: list[str] = Field(default_factory=list)
    motivo: str = ""


class Hallazgo(BaseModel):
    contenido: str


class RespuestaObservacion(BaseModel):
    caso: str
    pedidos_usados: int
    pedidos_restantes: int
    hallazgos: list[Hallazgo]
    nota: str


def codificar_mundo(mundo: dict[str, Any]) -> str:
    crudo = json.dumps(mundo, ensure_ascii=False).encode("utf-8")
    return base64.b64encode(zlib.compress(crudo, 9)).decode("ascii")


def decodificar_mundo(texto: str) -> dict[str, Any]:
    return json.loads(zlib.decompress(base64.b64decode(texto)).decode("utf-8"))  # type: ignore[no-any-return]


def ruta_mundo_por_defecto() -> Path:
    return Path(__file__).resolve().parents[3] / "datasets" / "abd-bench" / "oraculo" / "mundo.b64"


class Oraculo:
    def __init__(
        self,
        mundo: dict[str, Any],
        config: Config,
        registro: Path,
        agente: str,
        cliente: ClienteLLM | None = None,
    ) -> None:
        self.casos: dict[str, dict[str, Any]] = {c["id"]: c for c in mundo["casos"]}
        self.config = config
        self.registro = registro
        self.agente = agente
        self.cliente = cliente or ClienteLLM(config.model_copy(update={"cache_dir": None}))
        self.candado = threading.Lock()
        registro.parent.mkdir(parents=True, exist_ok=True)

    def _anotar(self, tipo: str, **datos: Any) -> None:
        linea = {"momento": datetime.now(UTC).isoformat(), "agente": self.agente, "tipo": tipo}
        with self.candado, self.registro.open("a", encoding="utf-8") as f:
            f.write(json.dumps(linea | datos, ensure_ascii=False) + "\n")

    def _caso(self, caso: str) -> dict[str, Any]:
        if caso not in self.casos:
            raise ToolError(f"caso desconocido: {caso}. Casos: {', '.join(sorted(self.casos))}")
        return self.casos[caso]

    def _usados(self, caso: str) -> int:
        if not self.registro.exists():
            return 0
        lineas = self.registro.read_text(encoding="utf-8").splitlines()
        return sum(
            1
            for x in map(json.loads, lineas)
            if x["tipo"] == "pedido" and x["caso"] == caso and x["agente"] == self.agente
        )

    def listar(self) -> list[str]:
        return sorted(self.casos)

    def ver(self, caso: str) -> str:
        c = self._caso(caso)
        self._anotar("ver", caso=caso)
        lineas = [f"Caso {caso}. Hechos conocidos en su momento:"]
        lineas += [f"- [{o['fecha']}] ({o['marco']}): {o['contenido']}" for o in c["observaciones"]]
        return "\n".join(lineas)

    def pedir(self, caso: str, que_mirar: str) -> RespuestaObservacion:
        c = self._caso(caso)
        usados = self._usados(caso)
        if usados >= MAX_PEDIDOS:
            return RespuestaObservacion(
                caso=caso,
                pedidos_usados=usados,
                pedidos_restantes=0,
                hallazgos=[],
                nota="Agotaste los pedidos de este caso. Concluye con lo que tienes.",
            )
        lista = "\n".join(
            f"- {h['id']}: mirar «{h['que_mirar']}» → {h['contenido']}" for h in c["hallazgos"]
        )
        usuario = f"HALLAZGOS:\n{lista}\n\nSOLICITUD DEL INVESTIGADOR: {que_mirar}"
        rol = self.config.roles.verificador.model_copy(update={"temperatura": 0.0})
        try:
            seleccion = self.cliente.completar_json(rol, SISTEMA_ORACULO, usuario, Seleccion)
        except ErrorLLM as e:
            raise ToolError(f"el oráculo no pudo responder: {e}") from e
        validos = {h["id"]: h for h in c["hallazgos"]}
        entregados = [validos[i] for i in seleccion.ids if i in validos]
        self._anotar(
            "pedido",
            caso=caso,
            que_mirar=que_mirar,
            entregados=[h["id"] for h in entregados],
            motivo=seleccion.motivo,
        )
        return RespuestaObservacion(
            caso=caso,
            pedidos_usados=usados + 1,
            pedidos_restantes=MAX_PEDIDOS - usados - 1,
            hallazgos=[Hallazgo(contenido=h["contenido"]) for h in entregados],
            nota="" if entregados else "No hay información sobre eso. Pide mirar algo concreto.",
        )

    def concluir(
        self, caso: str, explicacion: str, confianza: float, alternativas: list[str]
    ) -> str:
        self._caso(caso)
        if not 0.0 <= confianza <= 1.0:
            raise ToolError("confianza debe estar entre 0 y 1")
        self._anotar(
            "conclusion",
            caso=caso,
            explicacion=explicacion,
            confianza=confianza,
            alternativas=alternativas,
        )
        return "Conclusión registrada."


def crear_servidor_oraculo(oraculo: Oraculo) -> MCPServer:
    servidor = MCPServer(
        name="abd-oraculo", title="Oráculo de observaciones", instructions=INSTRUCCIONES
    )

    @servidor.tool()
    def listar_casos() -> list[str]:
        """Casos de la prueba."""
        return oraculo.listar()

    @servidor.tool()
    def ver_caso(caso: str) -> str:
        """Hechos que se conocían en su momento sobre el caso."""
        return oraculo.ver(caso)

    @servidor.tool()
    def pedir_observacion(caso: str, que_mirar: str) -> RespuestaObservacion:
        """Pide mirar algo concreto (un registro, objeto, ensayo, documento o persona).

        Solo obtienes lo que pides mirar. Preguntar por la causa no obtiene nada. Máximo 8
        pedidos por caso.
        """
        return oraculo.pedir(caso, que_mirar)

    @servidor.tool()
    def concluir(caso: str, explicacion: str, confianza: float, alternativas: list[str]) -> str:
        """Registra tu conclusión final del caso.

        `explicacion`: el mecanismo causal concreto. `confianza`: de 0 a 1, qué tan seguro
        estás de que es correcta. `alternativas`: las otras explicaciones que sigues
        considerando posibles.
        """
        return oraculo.concluir(caso, explicacion, confianza, alternativas)

    return servidor


def oraculo_de_entorno(config: Config, mundo: Path | None = None) -> Oraculo:
    ruta = mundo or ruta_mundo_por_defecto()
    registro = Path(
        os.environ.get("ABD_ORACULO_REGISTRO", str(Path.home() / ".abd-mind" / "oraculo.jsonl"))
    )
    agente = os.environ.get("ABD_ORACULO_AGENTE", "sin-nombre")
    return Oraculo(decodificar_mundo(ruta.read_text(encoding="ascii")), config, registro, agente)
