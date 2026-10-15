# EXP-005 — Fase 4c: caso reservado y `finanzas-llm`

- **Fecha:** 2026-10-14 · **Estado:** cerrado
- **Registro previo:** sí (11 §11.6, commit `30b0d8a`, antes de implementar)
- **Commit / artefactos:** `65d65ec`, `f473f7d`; experimento `reservado`

## Pregunta
¿El veredicto de tres valores, la pregunta del caso y el margen cumplen sus propiedades en un dominio que no los motivó?

## Expectativa (antes de correr)
Cinco propiedades del caso de la bomba industrial; experimentos anteriores idénticos.

## Resultado
- Las cinco propiedades se cumplen sin modificar el caso.
- Los experimentos anteriores dan salida idéntica.
- El margen voraz coincide con fuerza bruta en 25 casos aleatorios.
- `finanzas-llm`: 42 llamadas.

## Sorpresas y errores
Sin el residuo de lo neutral, las hipótesis parciales compiten más cerca de la ganadora: en `finanzas-llm`, la diferencia inicial bajó de 6.3 a 1.8.

## Lecciones
- El caso reservado lo escribió el mismo asistente que implementó (12 §12.5). Prueba coherencia, no validez.
- Era una señal temprana de lo que EXP-008 mostró de forma más grave: con verificador LLM, la discriminación es débil.

## Decisiones derivadas
Ninguna inmediata. Vigilar la cercanía de las hipótesis parciales con abd-bench.
