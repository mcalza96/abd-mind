# Resultados de abd-bench

Precisión sobre el tipo de causa, solo con verdad `establecida`. ✓ acierta el tipo principal, ½ el secundario, ✗ falla, — sin respuesta determinada. Sirve para encontrar fallas, no como puntaje (datasets/abd-bench/README.md).

| Grupo | Motor | deepseek-v4.1-flash | muse-spark-1.2-contributor | muse-spark-1.3-contributor |
|---|---|---|---|---|
| todos | 0/2 | 1/2 | 2/2 | 2/2 |
| originales | — | — | — | — |
| variantes | 0/2 | 1/2 | 2/2 | 2/2 |
| contaminación alta | — | — | — | — |
| contaminación baja | 0/2 | 1/2 | 2/2 | 2/2 |

- El generador propuso el tipo verdadero en 2/2 casos (si no lo propone, el motor no puede elegirlo: falla de generación, no de selección).
- Respuestas frágiles: 2; sin determinar: 2.

## Por caso

| Caso | Verdad | Contam. | Motor | Margen | deepseek-v4.1-flash | muse-spark-1.2-contributor | muse-spark-1.3-contributor |
|---|---|---|---|---|---|---|---|
| V01 | entidad_nueva | baja | — | 0 | ✓ entidad_nueva | ✓ entidad_nueva | ✓ entidad_nueva |
| V02 | ley_incorrecta | baja | — | 0 | ✗ mecanismo_conocido | ✓ ley_incorrecta | ✓ ley_incorrecta |
