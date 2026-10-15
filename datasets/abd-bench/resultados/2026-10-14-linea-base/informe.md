# Resultados de abd-bench

Precisión sobre el tipo de causa, solo con verdad `establecida`. ✓ acierta el tipo principal, ½ el secundario, ✗ falla, — sin respuesta determinada. Sirve para encontrar fallas, no como puntaje (datasets/abd-bench/README.md).

| Grupo | deepseek-v4.1-flash | muse-spark-1.2-contributor | muse-spark-1.3-contributor |
|---|---|---|---|
| todos | 36/49 | 39/49 | 39/49 |
| originales | 28/39 | 30/39 | 31/39 |
| variantes | 8/10 | 9/10 | 8/10 |
| contaminación alta | 23/29 | 24/29 | 26/29 |
| contaminación baja | 10/13 | 12/13 | 10/13 |

## Por caso

| Caso | Verdad | Contam. | Motor | Margen | deepseek-v4.1-flash | muse-spark-1.2-contributor | muse-spark-1.3-contributor |
|---|---|---|---|---|---|---|---|
| A01 | entidad_nueva | alta |  |  | ✓ entidad_nueva | ✓ entidad_nueva | ✓ entidad_nueva |
| A02 | entidad_nueva | alta |  |  | ✓ entidad_nueva | ✓ entidad_nueva | ✓ entidad_nueva |
| A03 | error_del_observador | alta |  |  | ✓ error_del_observador | ✓ error_del_observador | ✓ error_del_observador |
| A04 | entidad_nueva | alta |  |  | ✓ entidad_nueva | ✓ entidad_nueva | ✓ entidad_nueva |
| A05 | entidad_nueva | alta |  |  | ✓ entidad_nueva | ✗ mecanismo_conocido | ✓ entidad_nueva |
| A06 | ley_incorrecta | alta |  |  | ✓ ley_incorrecta | ✓ ley_incorrecta | ✓ ley_incorrecta |
| A07 | entidad_nueva | alta |  |  | ✓ entidad_nueva | ✓ entidad_nueva | ✓ entidad_nueva |
| A08 | entidad_nueva | alta |  |  | ✓ entidad_nueva | ✗ ley_incorrecta | ✓ entidad_nueva |
| B01 | ley_incorrecta | alta |  |  | ✓ ley_incorrecta | ✓ ley_incorrecta | ✓ ley_incorrecta |
| B02 | error_del_observador | alta |  |  | ✓ error_del_observador | ✓ error_del_observador | ✓ error_del_observador |
| B03 | error_del_observador | media |  |  | ✗ mecanismo_conocido | ✗ mecanismo_conocido | ✗ mecanismo_conocido |
| B04 | error_del_observador | alta |  |  | ✓ error_del_observador | ✓ error_del_observador | ✓ error_del_observador |
| B05 | ley_incorrecta | alta |  |  | ✗ entidad_nueva | ✓ ley_incorrecta | ✓ ley_incorrecta |
| B06 | ley_incorrecta | alta |  |  | ✓ ley_incorrecta | ✓ ley_incorrecta | ✓ ley_incorrecta |
| B07 | error_del_observador | alta |  |  | ✗ mecanismo_conocido | ✓ error_del_observador | ✓ error_del_observador |
| B08 | error_del_observador | alta |  |  | ✓ error_del_observador | ✓ error_del_observador | ✓ error_del_observador |
| C01 | mecanismo_conocido | alta |  |  | ✓ mecanismo_conocido | ✓ mecanismo_conocido | ✓ mecanismo_conocido |
| C02 | mecanismo_conocido | alta |  |  | ✓ mecanismo_conocido | ✓ mecanismo_conocido | ✓ mecanismo_conocido |
| C03 | mecanismo_conocido | alta |  |  | ✓ mecanismo_conocido | ✓ mecanismo_conocido | ✓ mecanismo_conocido |
| C04 | mecanismo_conocido | alta |  |  | ✓ mecanismo_conocido | ✓ mecanismo_conocido | ✓ mecanismo_conocido |
| C05 | entidad_nueva | alta |  |  | ✗ mecanismo_conocido | ✓ entidad_nueva | ✓ entidad_nueva |
| C06 | entidad_nueva | alta |  |  | ✓ entidad_nueva | ✗ mecanismo_conocido | ✗ mecanismo_conocido |
| C07 | ley_incorrecta | alta |  |  | ✗ mecanismo_conocido | ✓ ley_incorrecta | ✓ ley_incorrecta |
| C08 | entidad_nueva | alta |  |  | ✓ entidad_nueva | ✓ entidad_nueva | ✓ entidad_nueva |
| D01 | mecanismo_conocido (no est.) | media |  |  | ✓ mecanismo_conocido | ✓ mecanismo_conocido | ✓ mecanismo_conocido |
| D02 | error_del_observador | media |  |  | ½ mecanismo_conocido | ½ mecanismo_conocido | ½ mecanismo_conocido |
| D03 | mecanismo_conocido | alta |  |  | ✓ mecanismo_conocido | ✓ mecanismo_conocido | ✓ mecanismo_conocido |
| D04 | mecanismo_conocido | media |  |  | ✓ mecanismo_conocido | ✓ mecanismo_conocido | ✓ mecanismo_conocido |
| D05 | mecanismo_conocido | media |  |  | ✓ mecanismo_conocido | ✓ mecanismo_conocido | ✓ mecanismo_conocido |
| D06 | mecanismo_conocido | baja |  |  | ✓ mecanismo_conocido | ✓ mecanismo_conocido | ✓ mecanismo_conocido |
| D07 | entidad_nueva | alta |  |  | ✓ entidad_nueva | ✓ entidad_nueva | ✓ entidad_nueva |
| D08 | mecanismo_conocido | alta |  |  | ✓ mecanismo_conocido | ✓ mecanismo_conocido | ✓ mecanismo_conocido |
| E01 | error_del_observador | alta |  |  | ½ mecanismo_conocido | ½ mecanismo_conocido | ½ mecanismo_conocido |
| E02 | mecanismo_conocido | alta |  |  | ✓ mecanismo_conocido | ✓ mecanismo_conocido | ✓ mecanismo_conocido |
| E03 | error_del_observador | media |  |  | ½ mecanismo_conocido | ½ mecanismo_conocido | ½ mecanismo_conocido |
| E04 | error_del_observador | alta |  |  | ✗ mecanismo_conocido | ✗ mecanismo_conocido | ✗ mecanismo_conocido |
| E05 | mecanismo_conocido | media |  |  | ✓ mecanismo_conocido | ✓ mecanismo_conocido | ✓ mecanismo_conocido |
| E06 | error_del_observador | media |  |  | ½ mecanismo_conocido | ½ mecanismo_conocido | ½ mecanismo_conocido |
| E07 | mecanismo_conocido | baja |  |  | ✗ entidad_nueva | ✓ mecanismo_conocido | ✗ entidad_nueva |
| E08 | mecanismo_conocido | baja |  |  | ✓ mecanismo_conocido | ✓ mecanismo_conocido | ✓ mecanismo_conocido |
| V01 | entidad_nueva | baja |  |  | ✓ entidad_nueva | ✓ entidad_nueva | ✓ entidad_nueva |
| V02 | ley_incorrecta | baja |  |  | ✗ mecanismo_conocido | ✓ ley_incorrecta | ✓ ley_incorrecta |
| V03 | error_del_observador | baja |  |  | ✓ error_del_observador | ✓ error_del_observador | ✓ error_del_observador |
| V04 | error_del_observador | baja |  |  | ✓ error_del_observador | ✓ error_del_observador | ✓ error_del_observador |
| V05 | mecanismo_conocido | baja |  |  | ✓ mecanismo_conocido | ✓ mecanismo_conocido | ✓ mecanismo_conocido |
| V06 | entidad_nueva | baja |  |  | ✓ entidad_nueva | ✓ entidad_nueva | ✓ entidad_nueva |
| V07 | error_del_observador | baja |  |  | ✓ error_del_observador | ✓ error_del_observador | ✓ error_del_observador |
| V08 | entidad_nueva | baja |  |  | ✗ mecanismo_conocido | ✗ mecanismo_conocido | ✗ mecanismo_conocido |
| V09 | mecanismo_conocido | baja |  |  | ✓ mecanismo_conocido | ✓ mecanismo_conocido | ✓ mecanismo_conocido |
| V10 | error_del_observador | baja |  |  | ✓ error_del_observador | ✓ error_del_observador | ✗ mecanismo_conocido |

## Originales frente a variantes

| Variante | Original | Motor (var / orig) | Línea base (var / orig) |
|---|---|---|---|
| V01 | A01 | — / — | deepseek-v4.1-flash: ✓ entidad_nueva / ✓ entidad_nueva; muse-spark-1.2-contributor: ✓ entidad_nueva / ✓ entidad_nueva; muse-spark-1.3-contributor: ✓ entidad_nueva / ✓ entidad_nueva |
| V02 | A06 | — / — | deepseek-v4.1-flash: ✗ mecanismo_conocido / ✓ ley_incorrecta; muse-spark-1.2-contributor: ✓ ley_incorrecta / ✓ ley_incorrecta; muse-spark-1.3-contributor: ✓ ley_incorrecta / ✓ ley_incorrecta |
| V03 | B04 | — / — | deepseek-v4.1-flash: ✓ error_del_observador / ✓ error_del_observador; muse-spark-1.2-contributor: ✓ error_del_observador / ✓ error_del_observador; muse-spark-1.3-contributor: ✓ error_del_observador / ✓ error_del_observador |
| V04 | B02 | — / — | deepseek-v4.1-flash: ✓ error_del_observador / ✓ error_del_observador; muse-spark-1.2-contributor: ✓ error_del_observador / ✓ error_del_observador; muse-spark-1.3-contributor: ✓ error_del_observador / ✓ error_del_observador |
| V05 | D06 | — / — | deepseek-v4.1-flash: ✓ mecanismo_conocido / ✓ mecanismo_conocido; muse-spark-1.2-contributor: ✓ mecanismo_conocido / ✓ mecanismo_conocido; muse-spark-1.3-contributor: ✓ mecanismo_conocido / ✓ mecanismo_conocido |
| V06 | C05 | — / — | deepseek-v4.1-flash: ✓ entidad_nueva / ✗ mecanismo_conocido; muse-spark-1.2-contributor: ✓ entidad_nueva / ✓ entidad_nueva; muse-spark-1.3-contributor: ✓ entidad_nueva / ✓ entidad_nueva |
| V07 | A03 | — / — | deepseek-v4.1-flash: ✓ error_del_observador / ✓ error_del_observador; muse-spark-1.2-contributor: ✓ error_del_observador / ✓ error_del_observador; muse-spark-1.3-contributor: ✓ error_del_observador / ✓ error_del_observador |
| V08 | D07 | — / — | deepseek-v4.1-flash: ✗ mecanismo_conocido / ✓ entidad_nueva; muse-spark-1.2-contributor: ✗ mecanismo_conocido / ✓ entidad_nueva; muse-spark-1.3-contributor: ✗ mecanismo_conocido / ✓ entidad_nueva |
| V09 | C02 | — / — | deepseek-v4.1-flash: ✓ mecanismo_conocido / ✓ mecanismo_conocido; muse-spark-1.2-contributor: ✓ mecanismo_conocido / ✓ mecanismo_conocido; muse-spark-1.3-contributor: ✓ mecanismo_conocido / ✓ mecanismo_conocido |
| V10 | B08 | — / — | deepseek-v4.1-flash: ✓ error_del_observador / ✓ error_del_observador; muse-spark-1.2-contributor: ✓ error_del_observador / ✓ error_del_observador; muse-spark-1.3-contributor: ✗ mecanismo_conocido / ✓ error_del_observador |

Si un sistema acierta el original y falla la variante, probablemente recuerda el caso en vez de razonarlo.
