# Resultados de abd-bench

Respuestas correctas sobre el tipo de causa, solo con verdad `establecida`. En los casos sin respuesta posible (U) lo correcto es abstenerse ('indeterminado'). ✓ correcta, ½ acierta el tipo secundario, ✗ incorrecta. Sirve para encontrar fallas, no como puntaje (datasets/abd-bench/README.md).

| Grupo | Motor | deepseek-v4.1-flash | muse-spark-1.3-contributor |
|---|---|---|---|
| variantes (V) | 3/10 | 6/10 | 9/10 |
| perturbaciones (P) | 5/8 | 4/8 | 7/8 |
| sin respuesta (U): se abstiene | 1/10 | 1/10 | 2/10 |
| contaminación baja | 8/18 | 10/18 | 16/18 |

Abstenciones en casos que sí tenían respuesta (falsas abstenciones):

- Motor: 2/18
- deepseek-v4.1-flash: 0/18
- muse-spark-1.3-contributor: 0/18

## Motor

- El generador propuso el tipo verdadero en 18/18 casos con respuesta (si no lo propone, el motor no puede elegirlo: falla de generación, no de selección).
- Respuestas firmes correctas: 2/3; respuestas frágiles correctas: 6/13. Si la fragilidad sirve, las firmes aciertan más.

## Por caso

| Caso | Verdad | Contam. | Margen | Motor | deepseek-v4.1-flash | muse-spark-1.3-contributor |
|---|---|---|---|---|---|---|
| P01 | error_del_observador | baja | 1 (frágil) | ½ mecanismo_conocido | ½ mecanismo_conocido | ✓ error_del_observador |
| P02 | entidad_nueva | baja | 1 (frágil) | ✗ ley_incorrecta | ✗ mecanismo_conocido | ✗ mecanismo_conocido |
| P03 | mecanismo_conocido | baja | 1 (frágil) | ✗ error_del_observador | ✓ mecanismo_conocido | ✓ mecanismo_conocido |
| P04 | mecanismo_conocido | baja | 1 (frágil) | ✓ mecanismo_conocido | ✓ mecanismo_conocido | ✓ mecanismo_conocido |
| P05 | error_del_observador | baja | 2 | ✓ error_del_observador | ✗ mecanismo_conocido | ✓ error_del_observador |
| P06 | mecanismo_conocido | baja | 1 (frágil) | ✓ mecanismo_conocido | ✗ error_del_observador | ✓ mecanismo_conocido |
| P08 | mecanismo_conocido | baja | 1 (frágil) | ✓ mecanismo_conocido | ✓ mecanismo_conocido | ✓ mecanismo_conocido |
| P10 | mecanismo_conocido | baja | 2 | ✓ mecanismo_conocido | ✓ mecanismo_conocido | ✓ mecanismo_conocido |
| U01 | indeterminado | baja |  | ✓ indeterminado | ✗ error_del_observador | ✗ entidad_nueva |
| U02 | indeterminado | baja | 1 (frágil) | ✗ ley_incorrecta | ✗ mecanismo_conocido | ✗ ley_incorrecta |
| U03 | indeterminado | baja | 2 | ✗ error_del_observador | ✗ error_del_observador | ✗ error_del_observador |
| U04 | indeterminado | baja | 1 (frágil) | ✗ error_del_observador | ✗ error_del_observador | ✗ error_del_observador |
| U05 | indeterminado | baja | 1 (frágil) | ✗ error_del_observador | ✗ mecanismo_conocido | ✗ mecanismo_conocido |
| U06 | indeterminado | baja | 1 (frágil) | ✗ ley_incorrecta | ✗ mecanismo_conocido | ✓ indeterminado |
| U07 | indeterminado | baja | 1 (frágil) | ½ mecanismo_conocido | ½ mecanismo_conocido | ½ mecanismo_conocido |
| U08 | indeterminado | baja | 1 (frágil) | ✗ mecanismo_conocido | ✗ mecanismo_conocido | ✗ entidad_nueva |
| U09 | indeterminado | baja | 1 (frágil) | ✗ mecanismo_conocido | ✗ mecanismo_conocido | ✗ mecanismo_conocido |
| U10 | indeterminado | baja | 1 (frágil) | ✗ ley_incorrecta | ✓ indeterminado | ✓ indeterminado |
| V01 | entidad_nueva | baja | 1 (frágil) | ✓ entidad_nueva | ✓ entidad_nueva | ✓ entidad_nueva |
| V02 | ley_incorrecta | baja | 1 (frágil) | ✓ ley_incorrecta | ✗ mecanismo_conocido | ✓ ley_incorrecta |
| V03 | error_del_observador | baja |  | ✗ indeterminado | ✓ error_del_observador | ✓ error_del_observador |
| V04 | error_del_observador | baja |  | ✗ indeterminado | ✗ mecanismo_conocido | ✓ error_del_observador |
| V05 | mecanismo_conocido | baja | 1 (frágil) | ✓ mecanismo_conocido | ✓ mecanismo_conocido | ✓ mecanismo_conocido |
| V06 | entidad_nueva | baja | 2 | ✗ mecanismo_conocido | ✓ entidad_nueva | ✓ entidad_nueva |
| V07 | error_del_observador | baja | 1 (frágil) | ½ mecanismo_conocido | ½ mecanismo_conocido | ✓ error_del_observador |
| V08 | entidad_nueva | baja | 1 (frágil) | ✗ error_del_observador | ✗ mecanismo_conocido | ✗ mecanismo_conocido |
| V09 | mecanismo_conocido | baja | 1 (frágil) | ½ error_del_observador | ✓ mecanismo_conocido | ✓ mecanismo_conocido |
| V10 | error_del_observador | baja | 1 (frágil) | ✗ ley_incorrecta | ✓ error_del_observador | ✓ error_del_observador |

## Casos derivados frente a su origen

| Derivado | Origen | Motor (der. / orig.) | deepseek-v4.1-flash (der. / orig.) | muse-spark-1.3-contributor (der. / orig.) |
|---|---|---|---|---|
| P01 | V01 | ½ mecanismo_conocido / ✓ entidad_nueva | ½ mecanismo_conocido / ✓ entidad_nueva | ✓ error_del_observador / ✓ entidad_nueva |
| P02 | V02 | ✗ ley_incorrecta / ✓ ley_incorrecta | ✗ mecanismo_conocido / ✗ mecanismo_conocido | ✗ mecanismo_conocido / ✓ ley_incorrecta |
| P03 | V03 | ✗ error_del_observador / ✗ indeterminado | ✓ mecanismo_conocido / ✓ error_del_observador | ✓ mecanismo_conocido / ✓ error_del_observador |
| P04 | V04 | ✓ mecanismo_conocido / ✗ indeterminado | ✓ mecanismo_conocido / ✗ mecanismo_conocido | ✓ mecanismo_conocido / ✓ error_del_observador |
| P05 | V05 | ✓ error_del_observador / ✓ mecanismo_conocido | ✗ mecanismo_conocido / ✓ mecanismo_conocido | ✓ error_del_observador / ✓ mecanismo_conocido |
| P06 | V06 | ✓ mecanismo_conocido / ✗ mecanismo_conocido | ✗ error_del_observador / ✓ entidad_nueva | ✓ mecanismo_conocido / ✓ entidad_nueva |
| P08 | V08 | ✓ mecanismo_conocido / ✗ error_del_observador | ✓ mecanismo_conocido / ✗ mecanismo_conocido | ✓ mecanismo_conocido / ✗ mecanismo_conocido |
| P10 | V10 | ✓ mecanismo_conocido / ✗ ley_incorrecta | ✓ mecanismo_conocido / ✓ error_del_observador | ✓ mecanismo_conocido / ✓ error_del_observador |
| U01 | V01 | ✓ indeterminado / ✓ entidad_nueva | ✗ error_del_observador / ✓ entidad_nueva | ✗ entidad_nueva / ✓ entidad_nueva |
| U02 | V02 | ✗ ley_incorrecta / ✓ ley_incorrecta | ✗ mecanismo_conocido / ✗ mecanismo_conocido | ✗ ley_incorrecta / ✓ ley_incorrecta |
| U03 | V03 | ✗ error_del_observador / ✗ indeterminado | ✗ error_del_observador / ✓ error_del_observador | ✗ error_del_observador / ✓ error_del_observador |
| U04 | V04 | ✗ error_del_observador / ✗ indeterminado | ✗ error_del_observador / ✗ mecanismo_conocido | ✗ error_del_observador / ✓ error_del_observador |
| U05 | V05 | ✗ error_del_observador / ✓ mecanismo_conocido | ✗ mecanismo_conocido / ✓ mecanismo_conocido | ✗ mecanismo_conocido / ✓ mecanismo_conocido |
| U06 | V06 | ✗ ley_incorrecta / ✗ mecanismo_conocido | ✗ mecanismo_conocido / ✓ entidad_nueva | ✓ indeterminado / ✓ entidad_nueva |
| U07 | V07 | ½ mecanismo_conocido / ½ mecanismo_conocido | ½ mecanismo_conocido / ½ mecanismo_conocido | ½ mecanismo_conocido / ✓ error_del_observador |
| U08 | V08 | ✗ mecanismo_conocido / ✗ error_del_observador | ✗ mecanismo_conocido / ✗ mecanismo_conocido | ✗ entidad_nueva / ✗ mecanismo_conocido |
| U09 | V09 | ✗ mecanismo_conocido / ½ error_del_observador | ✗ mecanismo_conocido / ✓ mecanismo_conocido | ✗ mecanismo_conocido / ✓ mecanismo_conocido |
| U10 | V10 | ✗ ley_incorrecta / ✗ ley_incorrecta | ✓ indeterminado / ✓ error_del_observador | ✓ indeterminado / ✓ error_del_observador |

- Variante (V): si un sistema acierta el original y falla la variante, probablemente recuerda el caso.
- Perturbación (P): un sistema que da la misma respuesta en ambos no sigue la evidencia que cambió.
- Sin respuesta (U): lo correcto es abstenerse.
