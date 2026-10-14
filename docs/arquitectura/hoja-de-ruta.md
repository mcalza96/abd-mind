# Hoja de ruta

Cada fase termina con algo que funciona y se puede probar. Ninguna fase depende de Hermes hasta la 5.

## Fase 0 — Base del proyecto

- `pyproject.toml` (Python 3.12, `uv`), pydantic, pytest, ruff, mypy.
- Estructura de carpetas según [README](README.md#estructura-del-repositorio).
- Comando `abd-mind` con subcomandos vacíos.

**Término:** `uv run pytest`, `ruff` y `mypy` pasan en CI.

## Fase 1 — Núcleo determinista

- `contracts/abduction.py` tal como la especificación.
- `organ/rule_engine.py` (versión de ejemplo de la especificación).
- `transition/deterministic/ibe_evaluator.py` con score, umbral $\tau$ y desempate (D7).
- `tests/units/test_ibe_evaluator.py`: gana el cilindro; $K=0 \Rightarrow -\infty$; desempate determinista; propiedad de $\beta$ ([04 §4.4](../marco-teorico/04-funcion-objetivo-ibe.md#44-propiedad-del-peso-de-coherencia)).

**Término:** tests de la especificación pasan sin ningún LLM.

## Fase 2 — Observadores, proyecciones y experimentos sintéticos

- `contracts/observation.py`, `contracts/case.py`.
- `organ/projections.py`: siluetas de sólidos por vista; relación $\approx$ por observador (D5).
- $C$ calculada por proyección, no declarada (D1).
- `transition/deterministic/state_tree.py`: derrota y reactivación (D6).
- `rules/sintetico.yaml`; motor de reglas con predicados estructurados (D3, D4).
- Experimentos 5.1, 5.2 (con hipótesis fijas) y 5.3 como tests.

**Término:** `abd-mind experimento cilindro|expansion|tercer-observador` reproduce las tablas de [05](../marco-teorico/05-experimentos-canonicos.md).

## Fase 3 — Roles LLM del motor (OpenCode Go)

- `transition/stochastic/llm_client.py`: cliente OpenAI-compatible, roles por configuración (D9), salida JSON validada con Pydantic, reintentos, caché.
- `cortex.py` (hechos/opiniones), `generator.py` (contrastivo, expansión), `organ/verifier.py`.
- `abd-mind modelos`, `abd-mind doctor`.

**Término:** el experimento del cilindro corre con hipótesis **generadas** por LLM y sigue eligiendo "cilindro"; la línea base (una llamada) se mide con el mismo verificador.

## Fase 4 — Motor de casos y persistencia

- `engine/store.py` (SQLite, [ADR-0007](adr/0007-persistencia-sqlite.md)), `engine/case_service.py`.
- Presupuestos ([ADR-0008](adr/0008-presupuestos-y-trabajos-largos.md)).
- `rules/finanzas.yaml`; experimento 5.4.

**Término:** un caso se crea, sobrevive a un reinicio, recibe evidencia nueva, derrota y reactiva hipótesis, y produce auditoría.

## Fase 5 — Servidor MCP

- `interfaces/mcp_server.py` con FastMCP, herramientas del [contrato](contrato-mcp.md), stdio y HTTP ([ADR-0005](adr/0005-transporte-stdio-y-http.md)).
- Tests de integración con un cliente MCP genérico en ambos transportes.

**Término:** el flujo completo del caso financiero funciona desde un cliente MCP de prueba.

## Fase 6 — Integración con Hermes

- `hermes/skills/razonamiento-abductivo/SKILL.md` final.
- `hermes/config.example.yaml`.
- Prueba de punta a punta por Telegram ([despliegue §5](despliegue-pc.md#5-prueba-de-punta-a-punta)).

**Término:** los dos ejemplos (cilindro y financiero) funcionan conversando con Hermes por Telegram.

## Fase 7 — Benchmarks y calibración

- Las cuatro pruebas del Plan Maestro ([05 §5.5](../marco-teorico/05-experimentos-canonicos.md#55-pruebas-que-derivan-de-estos-experimentos)) contra línea base.
- Sensibilidad a $\alpha$, $\gamma$, $\tau$.
- Métrica de racionalización (declarado vs. verificado) por modelo.
- Modo asíncrono si los casos reales lo requieren.

**Término:** informe con resultados reproducibles desde `experiments/`.
