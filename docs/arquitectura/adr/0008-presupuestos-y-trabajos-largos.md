# ADR-0008 — Presupuestos por caso y trabajos largos

**Estado:** aceptada

## Contexto

En un dominio real, evaluar $n$ hipótesis contra $m$ observaciones cuesta $n \times m$ llamadas al verificador, más generación y extracción. Con 10 hipótesis y 8 observaciones son ~100 llamadas: minutos de latencia y costo no trivial. Además:

- Las llamadas a herramientas MCP tienen tiempo límite en el cliente.
- Por Telegram el usuario no ve progreso si una herramienta tarda minutos sin responder.

## Decisión

### Presupuestos

Cada caso tiene presupuestos configurables (con valores por defecto en `config/abd-mind.yaml`):

| Presupuesto | Por defecto (inicial) |
|---|---|
| Hipótesis por ronda de generación | 5 |
| Hipótesis vivas máximas por caso | 20 |
| Profundidad de expansión ontológica | 2 |
| Llamadas LLM por operación | 60 |
| Llamadas LLM por caso | 500 |

Al alcanzar un presupuesto, la operación termina con lo que tiene y lo informa (`presupuesto_agotado: true`), no falla en silencio.

### Trabajos largos

Las operaciones costosas (`generar_hipotesis`, `evaluar`, `nueva_evidencia`) aceptan `modo: "sincrono" | "asincrono"`:

- **síncrono** (por defecto en fase inicial): responde al terminar. Adecuado mientras los presupuestos mantengan la operación bajo el tiempo límite del cliente.
- **asíncrono**: responde de inmediato con `trabajo_id`; el progreso se consulta con `estado_trabajo(trabajo_id)`. Hermes informa al usuario por Telegram que está trabajando y consulta después.

Se implementa primero el modo síncrono con presupuestos ajustados; el asíncrono entra cuando un caso real lo necesite (ver [hoja de ruta](../hoja-de-ruta.md)).

## Consecuencias

- **+** Costo y latencia acotados y visibles.
- **+** Experiencia razonable por Telegram en casos grandes.
- **−** Un presupuesto bajo puede impedir encontrar la mejor hipótesis; la auditoría lo indica para que el usuario decida ampliarlo.
