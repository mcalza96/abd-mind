# abd-mind

Motor de razonamiento abductivo: un pipeline que separa percepción (LLM), generación de hipótesis (LLM), selección por virtudes explicativas (determinista) y verificación externa, para encontrar la causa latente que reconcilia observaciones contradictorias en lugar de promediarlas.

## Uso rápido

Requiere Python 3.12 y [`uv`](https://docs.astral.sh/uv/).

```bash
uv sync
uv run abd-mind experimento todos   # experimentos canónicos (sin LLM)
uv run abd-mind doctor              # valida configuración y acceso a los modelos
uv run abd-mind experimento cilindro-llm   # con LLM (requiere OPENCODE_API_KEY)
uv run abd-mind serve               # servidor MCP por stdio (para Hermes); --transport http con ABD_MIND_TOKEN
uv run pytest                        # tests
uv run ruff check && uv run mypy     # lint y tipos
```

Estado: fases 0–3 de la [hoja de ruta](docs/arquitectura/hoja-de-ruta.md): núcleo determinista, experimentos sintéticos y roles LLM (córtex, generadores, verificador) sobre OpenCode Go. La configuración de modelos está en [`config/abd-mind.example.yaml`](config/abd-mind.example.yaml).

## Documentación

- [Marco teórico](docs/marco-teorico/README.md): problema, postulados, formalización, función objetivo IBE, experimentos canónicos, arquitectura, estado del arte y decisiones de diseño.
- [Arquitectura](docs/arquitectura/README.md): acoplamiento a Hermes Agent vía MCP, contrato de herramientas, interacción por Telegram, despliegue en el PC, ADRs y hoja de ruta.
