# abd-mind

Investigación sobre razonamiento abductivo para agentes. **Desde el 2026-10-15** lo que recibe el agente (Hermes) son una skill y unas líneas siempre activas ([`hermes/`](hermes/), [ADR-0017](docs/arquitectura/adr/0017-motor-como-investigacion-skills-como-producto.md)); el motor y su servidor MCP quedan como investigación. **Objetivo:** una IA a la que se le ocurran explicaciones no obvias y que sepa distinguirlas de las rebuscadas ([tesis](docs/marco-teorico/tesis.md)). El motor mantiene el estado de cada caso, verifica, puntúa (por consiliencia o por predicción), detecta empates, sugiere qué observar y registra predicciones y verdades. La generación guiada por operadores abductivos está en diseño.

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

Estado: ver la [hoja de ruta](docs/arquitectura/hoja-de-ruta.md), fase 5c. La configuración de modelos está en [`config/abd-mind.example.yaml`](config/abd-mind.example.yaml).

## Documentación

- [Marco teórico](docs/marco-teorico/README.md): tesis, generación abductiva, principios y formalización (vigente).
- [Bitácora](docs/bitacora/README.md): experimentos, con su registro previo, y lecciones.
- [Arquitectura](docs/arquitectura/README.md): acoplamiento a Hermes Agent vía MCP, contrato de herramientas, interacción por Telegram, despliegue en el PC, ADRs y hoja de ruta.
