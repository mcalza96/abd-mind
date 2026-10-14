# Hoja de ruta

Cada fase termina con algo que funciona y se puede probar. Ninguna fase depende de Hermes hasta la 5.

## Estado

| Fase | Estado |
|---|---|
| 0 — Base del proyecto | ✅ |
| 1 — Núcleo determinista | ✅ |
| 2 — Observadores, proyecciones y experimentos sintéticos | ✅ |
| 3 — Roles LLM del motor | ✅ |
| 4 — Motor de casos y persistencia | Pendiente |
| 5 — Servidor MCP | Pendiente |
| 6 — Integración con Hermes | Pendiente |
| 7 — Benchmarks y calibración | Pendiente |

## Fase 0 — Base del proyecto

- `pyproject.toml` (Python 3.12, `uv`), pydantic, pytest, ruff, mypy.
- Estructura de carpetas según [README](README.md#estructura-del-repositorio).
- Comando `abd-mind` con `experimento`; los demás subcomandos avisan en qué fase llegan.

**Término:** `uv run pytest`, `ruff` y `mypy` pasan en CI.

## Fase 1 — Núcleo determinista

- `contracts/abduction.py` tal como la especificación.
- `organ/rule_engine.py` (versión de ejemplo de la especificación).
- `transition/deterministic/ibe_evaluator.py` con score, umbral $\tau$ y desempate (D7).
- `tests/units/test_ibe_evaluator.py`: gana el cilindro; $K=0 \Rightarrow -\infty$; desempate determinista; propiedad de $\beta$ ([04 §4.4](../marco-teorico/04-funcion-objetivo-ibe.md#44-propiedad-del-peso-de-coherencia)).

**Término:** tests de la especificación pasan sin ningún LLM.

Notas de implementación: `seleccionar_mejor_explicacion` devuelve `None` si ninguna hipótesis es coherente o alcanza $\tau$ (la especificación devolvía siempre la de mayor score, aunque fuera $-\infty$). El filtro textual de la especificación (`validar_predicados`) se conserva y se combina con las reglas estructuradas.

## Fase 2 — Observadores, proyecciones y experimentos sintéticos

- `contracts/observation.py`, `contracts/case.py`.
- `organ/projections.py`: siluetas de sólidos por vista; relación $\approx$ por observador (D5).
- $C$ calculada por proyección, no declarada (D1).
- `transition/deterministic/state_tree.py`: derrota y reactivación (D6).
- `rules/sintetico.yaml`; motor de reglas con predicados estructurados (D3, D4).
- Experimentos 5.1, 5.2 (con hipótesis fijas) y 5.3 como tests.
- `rules/finanzas.yaml` con las tres reglas de la especificación (adelantado desde la fase 4 para probar el motor de reglas).

**Término:** `abd-mind experimento cilindro|expansion|tercer-observador` reproduce las tablas de [05](../marco-teorico/05-experimentos-canonicos.md).

## Fase 3 — Roles LLM del motor (OpenCode Go)

- `transition/stochastic/llm_client.py`: cliente OpenAI-compatible, roles por configuración (D9), salida JSON validada con Pydantic, reintentos, caché.
- `cortex.py` (hechos/opiniones), `generator.py` (contrastivo, expansión), `organ/verifier.py`.
- `abd-mind modelos`, `abd-mind doctor`.

**Término:** el experimento del cilindro corre con hipótesis **generadas** por LLM y sigue eligiendo "cilindro"; la línea base (una llamada) se mide con el mismo verificador.

Notas de implementación:
- Roles por defecto (`config/abd-mind.example.yaml`): generador Muse Spark 1.3 Contributor con Muse Spark 1.2 Contributor como `fallback` si falla (endpoint `/responses`, salida `json_schema`); córtex y verificador DeepSeek V4.1 Flash (`/chat/completions`, salida `json_object`: no acepta `json_schema`). El verificador es de otra familia que los generadores (ADR-0002).
- OpenCode Go exige `x-opencode-session` y un user agent propio; la pasarela corta a los ~30 s las respuestas sin streaming, por eso los modelos se configuran con `streaming: true` (SSE).
- P cuenta también las entidades afirmadas en variables de tipo `entidad` del dominio (`rules/*.yaml` declara ahora sus variables), aunque el generador no las declare latentes (D2).
- Experimentos `cilindro-llm` y `expansion-llm`: la consiliencia se sigue calculando por proyección exacta, el LLM solo propone. `VerificadorLLM` queda listo para el dominio financiero (fase 4).

**Hallazgo.** En la primera corrida, los tres modelos de la línea base respondieron "cilindro" en una sola llamada (C = 2/2): el caso canónico es demasiado fácil para mostrar la falla inductiva con modelos actuales. La comparación con la línea base necesita casos más difíciles (fase 7).

## Fase 4 — Motor de casos y persistencia

- `engine/store.py` (SQLite, [ADR-0007](adr/0007-persistencia-sqlite.md)), `engine/case_service.py`.
- Presupuestos ([ADR-0008](adr/0008-presupuestos-y-trabajos-largos.md)).
- Experimento 5.4.

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

- Casos más difíciles que el cilindro, porque la línea base ya resuelve el caso canónico: dataset de casos frontera documentados (encargo de investigación en [docs/investigacion](../investigacion/prompt-deep-research-casos-frontera.md)), con controles negativos y variantes ofuscadas contra la memorización.
- Las cuatro pruebas del Plan Maestro ([05 §5.5](../marco-teorico/05-experimentos-canonicos.md#55-pruebas-que-derivan-de-estos-experimentos)) contra línea base.
- Sensibilidad a $\alpha$, $\gamma$, $\tau$.
- Métrica de racionalización (declarado vs. verificado) por modelo.
- Modo asíncrono si los casos reales lo requieren.

**Término:** informe con resultados reproducibles desde `experiments/`.
