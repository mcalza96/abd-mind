# EXP-013 — Selección holística en dominios abiertos (A)

- **Fecha:** 2026-10-14 · **Estado:** registrado (expectativas escritas antes de implementar y correr)
- **Registro previo:** sí
- **Origen:** [14](../marco-teorico/14-rumbo-estado-y-proyeccion.md), [ADR-0016](../arquitectura/adr/0016-seleccion-holistica-y-proyeccion.md)

## Pregunta
Con la selección holística (un juez ve todas las observaciones y todas las hipótesis), ¿el motor deja de rendir por debajo de la línea base en casos estáticos?

## Diseño
- Mismos 28 casos que EXP-012 (`--casos v2`).
- El juez es DeepSeek V4.1 Flash: de otra familia que el generador (ADR-0002) y el mismo modelo que una de las líneas base. La comparación directa es contra DeepSeek en una sola llamada.
- El juez puede declarar que la evidencia no alcanza (abstención).

## Expectativa (antes de correr)

| Id | Expectativa | Fracaso si… |
|---|---|---|
| G1 | En V + P, el motor acierta en un rango de ±2 casos respecto de DeepSeek (línea base: 10 de 18 en EXP-012) | Más de 2 casos por debajo de DeepSeek |
| G2 | En U, el motor se abstiene al menos tanto como DeepSeek (1 de 10 en EXP-012) | Menos que DeepSeek |
| G3 | Falsas abstenciones: 3 de 18 o menos | Más de 3 |
| G4 | No se espera que el motor supere a Muse 1.3: no es criterio de éxito | — |

Si se cumplen G1 a G3, A cumple su promesa mínima: el motor no degrada el juicio. El valor agregado se mide después, con casos secuenciales.

## Resultado
*(pendiente)*
