# Hoja de ruta

Cada fase termina con algo que funciona y se puede probar. Ninguna fase depende de Hermes hasta la 5.

## Estado

| Fase | Estado |
|---|---|
| 0 — Base del proyecto | ✅ |
| 1 — Núcleo determinista | ✅ |
| 2 — Observadores, proyecciones y experimentos sintéticos | ✅ |
| 3 — Roles LLM del motor | ✅ |
| 4 — Motor de casos y persistencia | ✅ |
| 4b — Robustez epistémica | ✅ |
| 4c — Explicación en dominios abiertos | ✅ |
| 5 — Servidor MCP | ✅ |
| 5b — Rumbo A + C | Parcial: A1 hecha (EXP-013); el resto queda subordinado a la fase 5c |
| 5c — Generación abductiva | Marco teórico hecho; el motor queda como investigación ([ADR-0017](adr/0017-motor-como-investigacion-skills-como-producto.md)) |
| **6 — Integración con Hermes** | **Replanteada: skill y líneas siempre activas, probadas en EXP-018** |
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
- `tests/units/test_ibe_evaluator.py`: gana el cilindro; $K=0 \Rightarrow -\infty$; desempate determinista; propiedad de $\beta$ ([04 §4.4](../historico/marco-teorico/04-funcion-objetivo-ibe.md#44-propiedad-del-peso-de-coherencia)).

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

**Término:** `abd-mind experimento cilindro|expansion|tercer-observador` reproduce las tablas de [05](../historico/marco-teorico/05-experimentos-canonicos.md).

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

Notas de implementación:
- El estado de un caso es un registro de eventos append-only; el árbol se reconstruye reproduciéndolo. Los veredictos se guardan aparte, así que reconstruir o reevaluar no vuelve a llamar al verificador. Cada caso guarda una copia de sus reglas: cambiar el YAML no altera casos existentes (solo genera un aviso).
- Cada dominio declara su verificador (`proyeccion` o `llm`). La detección de hipótesis duplicadas considera el mecanismo en dominios con verificador LLM.
- `corregir_observacion` retracta el hecho y registra la versión corregida sin usarla como prueba.

**Resultado de `finanzas-llm`** (21 llamadas): el córtex separó hechos de opiniones; ganó la estrategia de reducción de precios (C=3/3); la regla de dividendos descartó su hipótesis; la postura intermedia obtuvo C=0; el comunicado derrotó a la ganadora. Después, la expansión produjo **cuatro hipótesis empatadas** (C=4/4, P=1, score 15.0) y H* se eligió por el id: un caso real de subdeterminación que el sistema todavía no reconoce (ver la fase 4b).

## Fase 4b — Robustez epistémica

Implementa [09 §9.1–9.2](../historico/marco-teorico/09-robustez-epistemica.md), antes del servidor MCP porque cambia el contrato.

- Observadores falibles ([ADR-0009](adr/0009-observadores-falibles.md)): confiabilidad por observador y por dominio, score con consiliencia ponderada y residuo, derrota graduada, nuevo disparo de expansión, `atribuidas_a_error` en la evaluación.
- Subdeterminación ([ADR-0010](adr/0010-subdeterminacion.md)): detección de empates, sin $H^*$ cuando los hay, operación `sugerir_observacion`.
- Experimentos: errata de un observador poco confiable (no debe derrotar ni disparar expansión) y empate sintético (el sistema debe pedir la vista que separa).

**Término:** los experimentos sintéticos anteriores no cambian; los nuevos pasan; `finanzas-llm` informa el empate en lugar de elegir por id.

Resultados:
- `errata`: con ω = 0.3 el triángulo lateral queda como error del observador (el cilindro sigue vivo, en tensión, y no se expande la ontología); con ω ≥ 0.6 postular el tapón universal sale más barato que culpar al observador; con ω = 1 la derrota es inmediata, como en la versión base. Coincide con la tabla de [09 §9.1.6](../historico/marco-teorico/09-robustez-epistemica.md#916-culpar-al-observador-o-ampliar-la-ontología).
- `empate`: con solo la vista cenital, esfera, cilindro, cono y elipsoide empatan; el sistema no elige y sugiere la vista frontal o lateral (4 clases); al agregarla gana el cilindro.
- `finanzas-llm` (46 llamadas, ~7 min): los analistas usan ω = 0.9 del dominio y el comunicado oficial ω = 0.98, que sí derrota. Tras la expansión, cinco hipótesis empatan; el sistema lo informa y propone medir la evolución del precio efectivo medio, que las separa en 4 clases.

Después (propuestos en 09 §9.3–9.5): observadores correlacionados, observaciones con fecha y alerta de revisión de reglas.

## Fase 4c — Explicación en dominios abiertos

Origen: el ejercicio mental de [10](../historico/marco-teorico/10-validacion-caida-accion.md). Teoría en [11](../historico/marco-teorico/11-explicacion-en-dominios-abiertos.md); ADR-0011 a ADR-0013.

1. Veredicto de tres valores y rol de la observación (B1, B2).
2. Pregunta del caso, respuesta contrastiva y margen en veredictos (B3, B10).
3. Predicciones, `que_vigilar` y `cerrar_caso` con verdad (B4).

**Criterio de cierre** (protocolo de 11 §11.0):
- los experimentos anteriores dan los mismos números;
- se cumplen las propiedades de invarianza;
- el caso reservado (11 §11.6) cumple sus cinco propiedades sin modificarlo;
- `finanzas-llm` corre en vivo con el verificador de tres valores.

**Resultado:** criterio cumplido.
- Los cinco experimentos anteriores dan salida idéntica, carácter por carácter.
- El caso reservado (`experimento reservado`) cumple sus cinco propiedades sin modificarlo.
- El margen voraz coincide con fuerza bruta en 25 casos aleatorios.
- `finanzas-llm` en vivo: 42 llamadas, ~5 min. El verificador real distingue lo neutral de lo contradicho, y el comunicado sigue derrotando a la hipótesis de precios porque la contradice.

Efecto visible: las hipótesis de un solo hecho (demanda, costos) ya no pagan residuo por los hechos que no tratan. En la evaluación inicial, la diferencia con la ganadora baja de 6.3 a 1.8 puntos (c(0.9) = 2.3 por cada hecho no tratado).

### Complemento: verdad de cierre falible

[12](../historico/marco-teorico/12-verdad-y-entrenamiento.md) y ADR-0014: la verdad de cierre tiene fuente, ω e historial, y su estado puede ser `sin_verdad`, `tentativa`, `establecida` o `disputada`. Pendientes para después de la fase 5: mundos sintéticos con observadores sesgados, registro de anomalías de reglas y vocabulario retractable.

## Fase 5 — Servidor MCP

- `interfaces/mcp_server.py` con FastMCP, herramientas del [contrato](contrato-mcp.md), stdio y HTTP ([ADR-0005](adr/0005-transporte-stdio-y-http.md)).
- Tests de integración con un cliente MCP genérico en ambos transportes.

**Término:** el flujo completo del caso financiero funciona desde un cliente MCP de prueba.

**Resultado:** término cumplido. `abd-mind serve --transport stdio|http` expone 17 herramientas con el SDK oficial `mcp` 2.3 (`MCPServer`, el antiguo FastMCP). Tests de integración con el cliente genérico del SDK:
- flujo sintético en memoria, por stdio (subproceso real) y por HTTP con token;
- flujo financiero completo en memoria con LLM simulado;
- HTTP sin token o con token incorrecto: 401.

Notas:
- **Ejecución:** las herramientas son síncronas. El SDK las ejecuta en hilos, y un candado serializa el acceso al motor, porque SQLite admite un solo escritor.
- **Errores:** `isError` con `{codigo, mensaje}`.
- **Operaciones asíncronas** (`estado_trabajo`, ADR-0008): pendientes hasta que el tiempo límite de Hermes lo exija. Mientras tanto se sube ese límite (despliegue-pc §4).

### Complemento: abd-bench

`datasets/abd-bench/` reúne 40 casos frontera de la investigación, convertidos con separación entre lo que ve el motor y la solución, más 10 variantes disfrazadas. El esquema está en `src/factory/bench/casos.py`. Todavía no hay un ejecutor que corra el motor sobre los casos; queda para la fase 7, junto con la línea base y la comparación entre originales y variantes.

## Fase 5b — Rumbo A + C

Decisión de [14](../historico/marco-teorico/14-rumbo-estado-y-proyeccion.md) y [ADR-0016](adr/0016-seleccion-holistica-y-proyeccion.md), después de EXP-010 y EXP-012.

1. **A:** selección holística en dominios abiertos. Se comprueba en abd-bench que no degrada respecto de la línea base (experimento registrado).
2. **A:** casos secuenciales para medir anclaje y revisión. Primero sintéticos derivados de las variantes; después, el conjunto S de la segunda investigación.
3. **C:** verificación híbrida por variables y dominio `mercado`, validado con el conjunto F.
4. **Comunicación:** README y skill de Hermes dejan de prometer más precisión que un LLM en dominios abiertos.

## Fase 5c — Generación abductiva (nuevo centro)

Decisión del 2026-10-15: el objetivo es una IA a la que se le ocurran explicaciones no obvias ([17](../historico/marco-teorico/17-generacion-abductiva.md)). La fase 5b no se descarta: sus piezas pasan a ser el filtro y la prueba de lo que se genera (17 §17.8).

1. **Marco teórico:** documento 17, alineado con 01, el README, 16 y el glosario. Lectura ciega.
2. **Escenarios:** un experimento mental por operador o grupo de operadores, cada uno con su lectura ciega. Cada escenario debe poder mostrar que el operador **no** ayuda.
3. **Plan del MCP:** detección de disparadores, generación guiada por operadores, medición de novedad y de recuperación, y calificación de operadores por resultados resueltos.
4. **Experimento central** (registrado antes de correr): generación libre frente a generación guiada, con el mismo modelo y el mismo cómputo, en las salas, el conjunto R y las perturbaciones P (17 §17.7).

## Fase 6 — Integración con Hermes

**Desde el 2026-10-15 ([ADR-0017](adr/0017-motor-como-investigacion-skills-como-producto.md)):** lo que se integra es `hermes/skills/abduccion/` y `hermes/instrucciones-permanentes.md`. **Término:** EXP-018 muestra que el agente con ellas supera al agente sin nada en los casos no obvios, sin volverse rebuscado. Lo que sigue es el plan anterior, con el motor.

- `hermes/skills/razonamiento-abductivo/SKILL.md` final.
- `hermes/config.example.yaml`.
- Prueba de punta a punta por Telegram ([despliegue §5](despliegue-pc.md#5-prueba-de-punta-a-punta)).

**Término:** los dos ejemplos (cilindro y financiero) funcionan conversando con Hermes por Telegram.

## Fase 7 — Benchmarks y calibración

- Casos más difíciles que el cilindro, porque la línea base ya resuelve el caso canónico: dataset de casos frontera documentados (encargo de investigación en [docs/investigacion](../investigacion/prompt-deep-research-casos-frontera.md)), con controles negativos y variantes ofuscadas contra la memorización.
- Las cuatro pruebas del Plan Maestro ([05 §5.5](../historico/marco-teorico/05-experimentos-canonicos.md#55-pruebas-que-derivan-de-estos-experimentos)) contra línea base.
- Sensibilidad a $\alpha$, $\gamma$, $\tau$.
- Métrica de racionalización (declarado vs. verificado) por modelo.
- Modo asíncrono si los casos reales lo requieren.

**Término:** informe con resultados reproducibles desde `experiments/`.
