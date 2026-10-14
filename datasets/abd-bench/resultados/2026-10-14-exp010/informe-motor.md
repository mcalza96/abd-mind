# Resultados de abd-bench

Respuestas correctas sobre el tipo de causa, solo con verdad `establecida`. En los casos sin respuesta posible (U) lo correcto es abstenerse ('indeterminado'). ✓ correcta, ½ acierta el tipo secundario, ✗ incorrecta. Sirve para encontrar fallas, no como puntaje (datasets/abd-bench/README.md).

| Grupo | Motor |
|---|---|
| reales (A–E) | 6/10 |
| variantes (V) | 3/10 |
| contaminación alta | 5/9 |
| contaminación baja | 4/11 |

Abstenciones en casos que sí tenían respuesta (falsas abstenciones):

- Motor: 2/20

## Motor

- El generador propuso el tipo verdadero en 20/20 casos con respuesta (si no lo propone, el motor no puede elegirlo: falla de generación, no de selección).
- Respuestas firmes correctas: 3/5; respuestas frágiles correctas: 6/13. Si la fragilidad sirve, las firmes aciertan más.

## Por caso

| Caso | Verdad | Contam. | Margen | Motor |
|---|---|---|---|---|
| A01 | entidad_nueva | alta | 1 (frágil) | ✗ error_del_observador |
| A03 | error_del_observador | alta | 1 (frágil) | ✓ error_del_observador |
| A06 | ley_incorrecta | alta | 2 | ✓ ley_incorrecta |
| B02 | error_del_observador | alta | 1 (frágil) | ✓ error_del_observador |
| B04 | error_del_observador | alta | 2 | ✓ error_del_observador |
| B08 | error_del_observador | alta | 2 | ✓ error_del_observador |
| C02 | mecanismo_conocido | alta | 1 (frágil) | ✗ entidad_nueva |
| C05 | entidad_nueva | alta | 2 | ✗ mecanismo_conocido |
| D06 | mecanismo_conocido | baja | 1 (frágil) | ✓ mecanismo_conocido |
| D07 | entidad_nueva | alta | 1 (frágil) | ✗ mecanismo_conocido |
| V01 | entidad_nueva | baja | 1 (frágil) | ✓ entidad_nueva |
| V02 | ley_incorrecta | baja | 1 (frágil) | ✓ ley_incorrecta |
| V03 | error_del_observador | baja |  | ✗ indeterminado |
| V04 | error_del_observador | baja |  | ✗ indeterminado |
| V05 | mecanismo_conocido | baja | 1 (frágil) | ✓ mecanismo_conocido |
| V06 | entidad_nueva | baja | 2 | ✗ mecanismo_conocido |
| V07 | error_del_observador | baja | 1 (frágil) | ½ mecanismo_conocido |
| V08 | entidad_nueva | baja | 1 (frágil) | ✗ error_del_observador |
| V09 | mecanismo_conocido | baja | 1 (frágil) | ½ error_del_observador |
| V10 | error_del_observador | baja | 1 (frágil) | ✗ ley_incorrecta |

## Casos derivados frente a su origen

| Derivado | Origen | Motor (der. / orig.) |
|---|---|---|
| V01 | A01 | ✓ entidad_nueva / ✗ error_del_observador |
| V02 | A06 | ✓ ley_incorrecta / ✓ ley_incorrecta |
| V03 | B04 | ✗ indeterminado / ✓ error_del_observador |
| V04 | B02 | ✗ indeterminado / ✓ error_del_observador |
| V05 | D06 | ✓ mecanismo_conocido / ✓ mecanismo_conocido |
| V06 | C05 | ✗ mecanismo_conocido / ✗ mecanismo_conocido |
| V07 | A03 | ½ mecanismo_conocido / ✓ error_del_observador |
| V08 | D07 | ✗ error_del_observador / ✗ mecanismo_conocido |
| V09 | C02 | ½ error_del_observador / ✗ entidad_nueva |
| V10 | B08 | ✗ ley_incorrecta / ✓ error_del_observador |

- Variante (V): si un sistema acierta el original y falla la variante, probablemente recuerda el caso.
- Perturbación (P): un sistema que da la misma respuesta en ambos no sigue la evidencia que cambió.
- Sin respuesta (U): lo correcto es abstenerse.
