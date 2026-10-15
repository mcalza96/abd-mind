# Resultados de abd-bench

Respuestas correctas sobre el tipo de causa, solo con verdad `establecida`. En los casos sin respuesta posible (U) lo correcto es abstenerse ('indeterminado'). ✓ correcta, ½ acierta el tipo secundario, ✗ incorrecta. Sirve para encontrar fallas, no como puntaje (datasets/abd-bench/README.md).

| Grupo | Motor |
|---|---|
| variantes (V) | 4/10 |
| perturbaciones (P) | 6/8 |
| sin respuesta (U): se abstiene | 3/10 |
| contaminación baja | 10/18 |

Abstenciones en casos que sí tenían respuesta (falsas abstenciones):

- Motor: 2/18

## Motor

- El generador propuso el tipo verdadero en 17/17 casos con respuesta (si no lo propone, el motor no puede elegirlo: falla de generación, no de selección).
- Respuestas firmes correctas: 10/15; respuestas frágiles correctas: —. Si la fragilidad sirve, las firmes aciertan más.

## Por caso

| Caso | Verdad | Contam. | Margen | Motor |
|---|---|---|---|---|
| P01 | error_del_observador | baja | ∞ | ½ mecanismo_conocido |
| P02 | entidad_nueva | baja | ∞ | ✗ mecanismo_conocido |
| P03 | mecanismo_conocido | baja | ∞ | ✓ mecanismo_conocido |
| P04 | mecanismo_conocido | baja | ∞ | ✓ mecanismo_conocido |
| P05 | error_del_observador | baja | ∞ | ✓ error_del_observador |
| P06 | mecanismo_conocido | baja | ∞ | ✓ mecanismo_conocido |
| P08 | mecanismo_conocido | baja | ∞ | ✓ mecanismo_conocido |
| P10 | mecanismo_conocido | baja | ∞ | ✓ mecanismo_conocido |
| U01 | indeterminado | baja |  | ✓ indeterminado |
| U02 | indeterminado | baja | ∞ | ✗ ley_incorrecta |
| U03 | indeterminado | baja | ∞ | ✗ error_del_observador |
| U04 | indeterminado | baja |  | ✓ indeterminado |
| U05 | indeterminado | baja | ∞ | ✗ mecanismo_conocido |
| U06 | indeterminado | baja | ∞ | ✗ mecanismo_conocido |
| U07 | indeterminado | baja | ∞ | ½ mecanismo_conocido |
| U08 | indeterminado | baja | ∞ | ✗ mecanismo_conocido |
| U09 | indeterminado | baja | ∞ | ✗ mecanismo_conocido |
| U10 | indeterminado | baja |  | ✓ indeterminado |
| V01 | entidad_nueva | baja |  | error |
| V02 | ley_incorrecta | baja | ∞ | ✓ ley_incorrecta |
| V03 | error_del_observador | baja |  | ✗ indeterminado |
| V04 | error_del_observador | baja | ∞ | ✓ error_del_observador |
| V05 | mecanismo_conocido | baja | ∞ | ✓ mecanismo_conocido |
| V06 | entidad_nueva | baja | ∞ | ✗ mecanismo_conocido |
| V07 | error_del_observador | baja | ∞ | ✗ entidad_nueva |
| V08 | entidad_nueva | baja |  | ✗ indeterminado |
| V09 | mecanismo_conocido | baja | ∞ | ✓ mecanismo_conocido |
| V10 | error_del_observador | baja | ∞ | ✗ ley_incorrecta |

## Casos derivados frente a su origen

| Derivado | Origen | Motor (der. / orig.) |
|---|---|---|
| P01 | V01 | ½ mecanismo_conocido / error |
| P02 | V02 | ✗ mecanismo_conocido / ✓ ley_incorrecta |
| P03 | V03 | ✓ mecanismo_conocido / ✗ indeterminado |
| P04 | V04 | ✓ mecanismo_conocido / ✓ error_del_observador |
| P05 | V05 | ✓ error_del_observador / ✓ mecanismo_conocido |
| P06 | V06 | ✓ mecanismo_conocido / ✗ mecanismo_conocido |
| P08 | V08 | ✓ mecanismo_conocido / ✗ indeterminado |
| P10 | V10 | ✓ mecanismo_conocido / ✗ ley_incorrecta |
| U01 | V01 | ✓ indeterminado / error |
| U02 | V02 | ✗ ley_incorrecta / ✓ ley_incorrecta |
| U03 | V03 | ✗ error_del_observador / ✗ indeterminado |
| U04 | V04 | ✓ indeterminado / ✓ error_del_observador |
| U05 | V05 | ✗ mecanismo_conocido / ✓ mecanismo_conocido |
| U06 | V06 | ✗ mecanismo_conocido / ✗ mecanismo_conocido |
| U07 | V07 | ½ mecanismo_conocido / ✗ entidad_nueva |
| U08 | V08 | ✗ mecanismo_conocido / ✗ indeterminado |
| U09 | V09 | ✗ mecanismo_conocido / ✓ mecanismo_conocido |
| U10 | V10 | ✓ indeterminado / ✗ ley_incorrecta |

- Variante (V): si un sistema acierta el original y falla la variante, probablemente recuerda el caso.
- Perturbación (P): un sistema que da la misma respuesta en ambos no sigue la evidencia que cambió.
- Sin respuesta (U): lo correcto es abstenerse.

## Errores

- V01: respuesta truncada por max_tokens; aumentar max_tokens del rol
