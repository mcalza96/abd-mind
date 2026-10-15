# EXP-001 — Línea base en el cilindro (fase 3)

- **Fecha:** 2026-10 (fase 3) · **Estado:** cerrado
- **Registro previo:** no (reconstruido)
- **Commit / artefactos:** `b9997b2`; experimentos `cilindro-llm`, `expansion-llm`

## Pregunta
¿Un LLM en una sola llamada cae en la "quimera estadística" (por ejemplo, "óvalo") ante las vistas frontal (rectángulo) y cenital (círculo)?

## Expectativa (antes de correr)
La tesis predecía que la decodificación directa promediaría las proyecciones.

## Diseño
Los tres modelos (Muse 1.3, Muse 1.2 y DeepSeek V4.1 Flash) responden en una llamada; el motor genera hipótesis con LLM y las verifica por proyección exacta.

## Resultado
Los tres modelos respondieron "cilindro" (C = 2/2). El motor también acierta.

## Sorpresas y errores
El caso canónico de la especificación no muestra la falla inductiva con modelos actuales. Es famoso y simple.

## Lecciones
Los casos canónicos sirven para probar que el código funciona, no para mostrar ventajas sobre un LLM.

## Decisiones derivadas
Encargar casos frontera más difíciles (prompt de investigación, después EXP-006 y abd-bench).
