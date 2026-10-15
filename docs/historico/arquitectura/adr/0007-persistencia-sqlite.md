# ADR-0007 — Persistencia de casos en SQLite

**Estado:** aceptada

## Contexto

Un caso abductivo vive más que una llamada: se crea, se agregan observaciones a lo largo de una conversación (o de días, por Telegram), llega evidencia nueva, se retracta evidencia. Hermes puede reiniciar el proceso MCP en cualquier momento (modo stdio). La derrotabilidad reversible (D6) y la auditoría exigen guardar historia, no solo el estado actual.

## Decisión

SQLite en un archivo local (por defecto `~/.abd-mind/abd-mind.db`, configurable). Modelo de datos inicial:

| Tabla | Contenido |
|---|---|
| `casos` | id, descripción, dominio, versión de reglas, configuración (pesos, τ), estado, fechas |
| `observadores` | id, caso, nombre, marco (descripción), tolerancia $\varepsilon_i$ |
| `observaciones` | id, caso, observador, contenido crudo, hechos extraídos, opiniones, estado (`activa`/`retractada`), fecha |
| `hipotesis` | id, caso, mecanismo, entidades declaradas, predicados, origen, estado (`viva`/`derrotada`), derrotada_por |
| `veredictos` | hipótesis, observación, resultado ($\approx$ sí/no), fuente (`proyeccion`/`verificador:<modelo>`), justificación |
| `evaluaciones` | hipótesis, $C$, $P$, $K$, score, momento |
| `eventos` | registro append-only de todo lo que pasa en el caso (para auditoría y reproducción) |
| `llm_cache` | hash de (modelo, prompt, parámetros) → respuesta |

Los veredictos se cachean por (hipótesis, observación, versión del verificador): agregar una observación nueva solo requiere verificar esa observación contra las hipótesis vivas, no todo de nuevo.

## Consecuencias

- **+** Sin servicios adicionales que instalar en el PC.
- **+** Un caso se puede inspeccionar, exportar o reproducir con la CLI.
- **+** La caché de LLM abarata repetir experimentos.
- **−** Un solo escritor a la vez; suficiente para un usuario. Si el motor pasa a ser multiusuario vía HTTP, se reevalúa (PostgreSQL).
