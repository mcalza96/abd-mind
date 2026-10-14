# ADR-0010 — Subdeterminación y abducción activa

**Estado:** aceptada

## Contexto

Cuando varias hipótesis empatan, el motor elegía la de menor identificador (D7). En `finanzas-llm` cuatro hipótesis distintas quedaron con score 15.0 y se informó una como "la mejor explicación": certeza fingida. Ver [09 §9.2](../../marco-teorico/09-robustez-epistemica.md#92-subdeterminación-y-abducción-activa).

## Decisión

1. **Detección.** El árbol calcula el conjunto empatado $T$: hipótesis vivas y coherentes con score $\ge$ score máximo $- \delta$ (`pesos.delta_empate`, por defecto $10^{-6}$). Si $|T| \ge 2$, `h_estrella` es nulo y la evaluación informa `empatadas` y `subdeterminada: true`.
2. **El desempate por identificador** se conserva para ordenar el ranking, no para elegir. `IBEEvaluator.seleccionar_mejor_explicacion` (contrato de la especificación) no cambia; la detección vive en el árbol y en el motor de casos.
3. **Abducción activa.** Nueva operación `sugerir_observacion(caso_id)`:
   - dominios con proyección: recorre los marcos posibles que declara el dominio (`marcos_posibles` en el YAML) y devuelve los que separan a las hipótesis empatadas, con la predicción de cada una;
   - dominios con verificador LLM: un modelo propone consultas con la predicción de cada hipótesis; el motor descarta las consultas cuyas predicciones no difieren.
   Las consultas se ordenan por poder discriminante (número de clases en que parten a $T$).

## Consecuencias

- **+** El sistema no afirma más de lo que la evidencia permite.
- **+** Por Telegram la respuesta es accionable: qué observar para decidir.
- **−** En casos reales, los empates exactos son raros con verificador LLM; la tolerancia $\delta$ decide qué cuenta como "igual de bueno" y debe calibrarse.
- **−** `sugerir_observacion` cuesta una llamada LLM en dominios reales; no se ejecuta automáticamente.
