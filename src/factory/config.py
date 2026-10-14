"""Configuración de abd-mind: proveedor, modelos, roles, pesos y presupuestos (D9).

Se busca, en orden: `ABD_MIND_CONFIG`, `~/.abd-mind/config.yaml` y, por último, el ejemplo
versionado `config/abd-mind.example.yaml` del repositorio.
"""

import os
from pathlib import Path
from typing import Literal

import yaml
from pydantic import BaseModel, ConfigDict, Field

from factory import __version__

RUTA_EJEMPLO = Path(__file__).resolve().parents[2] / "config" / "abd-mind.example.yaml"
RUTA_USUARIO = Path.home() / ".abd-mind" / "config.yaml"


class _Estricto(BaseModel):
    model_config = ConfigDict(extra="forbid")


class ConfigProveedor(_Estricto):
    base_url: str = "https://opencode.ai/inference/go/v1"
    api_key_env: str | None = Field(
        default="OPENCODE_API_KEY",
        description=(
            "Variable de entorno con la clave. Si no está definida, no se envía Authorization "
            "(útil cuando un proxy agrega la clave)"
        ),
    )
    user_agent: str = f"abd-mind/{__version__}"
    timeout_s: float = 180.0
    reintentos_red: int = Field(default=2, ge=0)


class ConfigModelo(_Estricto):
    """Cómo se habla con un modelo concreto del proveedor."""

    api: Literal["chat", "responses"] = "chat"
    salida_json: Literal["json_schema", "json_object"] = "json_object"
    streaming: bool = Field(
        default=False,
        description="Recibir la respuesta por SSE; evita el corte de ~30 s de la pasarela",
    )


class ConfigRol(_Estricto):
    modelo: str
    temperatura: float | None = None
    max_tokens: int = Field(default=8000, gt=0)


class ConfigRoles(_Estricto):
    cortex: ConfigRol
    generadores: list[ConfigRol] = Field(min_length=1)
    verificador: ConfigRol
    linea_base: list[ConfigRol] = Field(default_factory=list)


class ConfigPesos(_Estricto):
    alpha: float = 1.5
    beta: float = 10.0
    gamma: float = 1.0
    tau: float | None = None


class ConfigPresupuestos(_Estricto):
    hipotesis_por_ronda: int = Field(default=5, gt=0)
    reintentos_json: int = Field(default=2, ge=0)
    llamadas_por_operacion: int = Field(default=60, gt=0)
    llamadas_por_caso: int = Field(default=500, gt=0)


class Config(_Estricto):
    proveedor: ConfigProveedor = Field(default_factory=ConfigProveedor)
    modelos: dict[str, ConfigModelo] = Field(default_factory=dict)
    roles: ConfigRoles
    pesos: ConfigPesos = Field(default_factory=ConfigPesos)
    presupuestos: ConfigPresupuestos = Field(default_factory=ConfigPresupuestos)
    cache_dir: Path | None = Field(
        default=None, description="Directorio de caché de respuestas LLM; None la desactiva"
    )

    def modelo(self, nombre: str) -> ConfigModelo:
        return self.modelos.get(nombre, ConfigModelo())

    def avisos(self) -> list[str]:
        """Problemas de configuración que no impiden funcionar pero conviene corregir."""
        avisos = []
        generadores = {g.modelo for g in self.roles.generadores}
        if self.roles.verificador.modelo in generadores:
            avisos.append(
                f"el verificador ({self.roles.verificador.modelo}) también genera hipótesis: "
                "se pierde la independencia generador/verificador (ADR-0002)"
            )
        if len(generadores) < 2:
            avisos.append("con un solo modelo generador hay menos diversidad de hipótesis")
        return avisos


def ruta_config() -> Path:
    env = os.environ.get("ABD_MIND_CONFIG")
    if env:
        return Path(env).expanduser()
    return RUTA_USUARIO if RUTA_USUARIO.is_file() else RUTA_EJEMPLO


def cargar_config(ruta: Path | None = None) -> Config:
    ruta = ruta or ruta_config()
    with ruta.open(encoding="utf-8") as f:
        config = Config.model_validate(yaml.safe_load(f))
    if config.cache_dir is not None:
        config.cache_dir = config.cache_dir.expanduser()
    return config
