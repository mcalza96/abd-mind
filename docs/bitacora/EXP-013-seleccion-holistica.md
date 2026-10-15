# EXP-013 — Selección holística en dominios abiertos (A)

- **Fecha:** 2026-10-14 · **Estado:** corrido
- **Registro previo:** sí
- **Origen:** [14](../historico/marco-teorico/14-rumbo-estado-y-proyeccion.md), [ADR-0016](../arquitectura/adr/0016-seleccion-holistica-y-proyeccion.md)

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

**Corrida:** motor solo, reutilizando generación y veredictos de EXP-012 desde la caché; solo el juez es nuevo. Prueba de humo previa en U01: el juez se abstuvo y dijo qué observación separaría las hipótesis. Resultados en `datasets/abd-bench/resultados/2026-10-14-exp013/`.

| | Motor con selección holística | Motor con score (EXP-012) | DeepSeek, una llamada (EXP-012) | Muse 1.3, una llamada (EXP-012) |
|---|---|---|---|---|
| V + P correctas | 10/18 | 8/18 | 10/18 | 16/18 |
| U: se abstiene | 3/10 | 1/10 | 1/10 | 2/10 |
| Falsas abstenciones | 2/18 | 2/18 | 0/18 | 0/18 |

| Id | Resultado | ¿Se cumple? |
|---|---|---|
| G1 | 10 de 18 en V + P, igual que DeepSeek | ✅ |
| G2 | Se abstiene en 3 de 10 casos U, más que DeepSeek (1) y que Muse (2) | ✅ |
| G3 | 2 falsas abstenciones (V03 y V08) | ✅ |
| G4 | Muse 1.3 sigue siendo mejor en V + P (16 frente a 10) | No era criterio de éxito |

**Incidente:** V01 falló por truncamiento. Después de la expansión tiene unas 10 hipótesis, y alguna llamada (juez, verificador o generador) superó su límite de tokens. Cuenta como error.

## Lecciones

- **A cumple su promesa mínima:** el motor deja de rendir por debajo del juicio del mismo modelo, y se abstiene algo más. Su techo es el modelo juez: con DeepSeek como juez, el motor no supera a Muse.
- **La abstención sigue siendo baja** (3 de 10), aunque el juez tiene la opción explícita y la justifica bien cuando la usa.
- **Los casos grandes necesitan límites de tokens acordes al número de hipótesis**, o un juicio por tandas.

## Decisiones derivadas

- El valor agregado de A se mide con casos secuenciales: primero sintéticos, luego el conjunto S de la investigación.
- **Elección del juez (pendiente, a decidir con el usuario):** Muse 1.3 juzga mejor, pero también genera las hipótesis. Usarlo de juez rompe la independencia de ADR-0002.
