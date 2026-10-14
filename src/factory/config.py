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
    fallback: str | None = Field(
        default=None,
        description="Modelo a usar si el principal falla (error del proveedor o JSON inválido)",
    )
    temperatura: float | None = None
    max_tokens: int = Field(default=8000, gt=0)

    def modelos(self) -> list[str]:
        return [self.modelo, *([self.fallback] if self.fallback else [])]


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
    lambda_residuo: float = Field(
        default=1.0, ge=0.0, description="λ: peso del costo de atribuir hechos a error (09 §9.1)"
    )
    omega_derrota: float = Field(
        default=0.95, gt=0.0, le=1.0, description="ω mínimo para que un hecho derrote solo"
    )
    delta_empate: float = Field(
        default=1e-6, ge=0.0, description="δ: diferencia de score que cuenta como empate"
    )
    veredictos_fragil: int = Field(
        default=1,
        ge=0,
        description="k_f: la respuesta es frágil si cambiar k_f veredictos de LLM la invierte",
    )


class ConfigPresupuestos(_Estricto):
    hipotesis_por_ronda: int = Field(default=5, gt=0)
    hipotesis_vivas_max: int = Field(default=20, gt=0)
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
    base_datos: Path = Field(
        default=Path("~/.abd-mind/abd-mind.db"), description="SQLite de casos (ADR-0007)"
    )

    def modelo(self, nombre: str) -> ConfigModelo:
        return self.modelos.get(nombre, ConfigModelo())

    def avisos(self) -> list[str]:
        """Problemas de configuración que no impiden funcionar pero conviene corregir."""
        avisos = []
        generadores = {m for g in self.roles.generadores for m in g.modelos()}
        for modelo in self.roles.verificador.modelos():
            if modelo in generadores:
                avisos.append(
                    f"el verificador ({modelo}) también genera hipótesis: "
                    "se pierde la independencia generador/verificador (ADR-0002)"
                )
        if len({g.modelo for g in self.roles.generadores}) < 2:
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
    config.base_datos = config.base_datos.expanduser()
    return config
