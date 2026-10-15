# ADR-0012 — Pregunta del caso y margen de victoria

**Estado:** aceptada

## Contexto

El usuario pregunta algo contrastivo ("¿estructural o transitoria?"), no "¿qué mecanismo?". Un empate de mecanismos que dan la misma respuesta bloqueaba la respuesta. Además, una victoria por un solo veredicto LLM se presentaba igual que una victoria amplia. Ver [11 §11.3–11.4](../../marco-teorico/11-explicacion-en-dominios-abiertos.md).

## Decisión

1. `crear_caso` acepta `pregunta: {variable, valores, descripcion?}`, que se guarda en el registro del caso. Los generadores reciben la pregunta y deben afirmar la variable.
2. La evaluación agrega `respuesta`:
   - `valor`: el valor que la responde, o nulo;
   - `determinada`: si la respuesta quedó establecida;
   - `scores_por_valor`;
   - `margen_veredictos`: k; nulo si es infinito;
   - `fragil`: k ≤ `pesos.veredictos_fragil`, por defecto 1.

   Sin pregunta, los mismos campos describen a H* (`valor` = su id).
3. `sugerir_observacion` funciona cuando hay empate **o** fragilidad. Con pregunta, propone consultas que separan clases.

## Consecuencias

- **+** Por Telegram la respuesta puede decir "transitoria, aunque no sabemos el mecanismo exacto".
- **+** La fragilidad se informa en vez de esconderse.
- **−** El parámetro k_f es nuevo y sin calibrar. El valor 1 se justifica porque un veredicto es la unidad de error del verificador, no por ningún caso concreto.
