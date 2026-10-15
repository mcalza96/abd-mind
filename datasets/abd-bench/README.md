# abd-bench — casos frontera

Casos para poner a prueba el motor abductivo. El esquema está en `src/factory/bench/casos.py`, y `tests/units/test_bench.py` valida cada archivo.

| Archivo | Casos | Origen |
|---|---|---|
| `casos-A.jsonl` | A01–A08 | Descubrimiento científico |
| `casos-B.jsonl` | B01–B08 | Postulados latentes que fracasaron |
| `casos-C.jsonl` | C01–C08 | Medicina, forense y accidentes |
| `casos-D.jsonl` | D01–D08 | Ciencias de la Tierra, historia e inteligencia |
| `casos-E.jsonl` | E01–E08 | Percepción y cognición |
| `variantes.jsonl` | V01–V10 | Variantes disfrazadas de casos reales |
| `perturbaciones.jsonl` | P01–P10 (8) | Variantes con un hecho decisivo cambiado: el tipo de causa correcto cambia ([EXP-012](../../docs/bitacora/EXP-012-bench-v2-perturbaciones-y-sin-respuesta.md)) |
| `sin-respuesta.jsonl` | U01–U10 | Variantes sin los hechos que discriminan: lo correcto es abstenerse |
| `fuentes/` | — | Notas originales de la investigación (sin modificar) |

## Cómo se usa

**No es un conjunto de etiquetas para medir aciertos ni para entrenar** ([12 §12.2](../../docs/historico/marco-teorico/12-verdad-y-entrenamiento.md#122-datos-sintéticos)). Sirve para encontrar dónde falla el motor.

Cada caso separa:

- **Lo que ve el motor:** `observadores`, `observaciones` (solo lo que cada observador reportó en su momento) y `pregunta`.
- **Lo que no ve:** `solucion`, `verdad` y `respuesta_inductiva_erronea`.

La `verdad` es una observación falible: tiene fuente, confiabilidad y estado (`establecida`, `tentativa` o `disputada`). En los casos A–E proviene de la historia documentada. En las variantes, de la construcción del caso.

**La pregunta es común a todos los casos:** `tipo_de_causa`. Sus valores son `entidad_nueva`, `error_del_observador`, `ley_incorrecta` y `mecanismo_conocido`. Mide qué clase de abducción hace falta y permite comparar casos de dominios distintos.

## Versión 2: perturbaciones y casos sin respuesta

La pregunta del tipo de causa resultó fácil para la línea base ([EXP-007](../../docs/bitacora/EXP-007-bench-linea-base.md)). La versión 2 mide dos cosas que un LLM en una sola llamada suele hacer mal:

- **Seguir la evidencia (serie P):** el mismo caso con uno o dos hechos cambiados, de modo que la respuesta correcta cambia.
- **Abstenerse (serie U):** el caso sin los hechos que permiten decidir. El campo `determinable` es falso y `tipos_compatibles` lista los tipos que quedan igual de sostenidos.

Para no comparar en desventaja, la línea base recibe en todos los casos la opción `indeterminado`.

Comando: `abd-mind bench --casos v2` corre P, U y las variantes de las que derivan.

## Contaminación

Casi todos los casos A–E son famosos, y los modelos que generan hipótesis conocen su solución. Por eso:

- cada caso tiene un campo `contaminacion` (alta, media o baja);
- las **variantes** (serie V) trasladan diez casos clave a otros dominios y épocas, y conservan la estructura y el tipo de causa;
- **lectura de resultados:** si el motor acierta mucho más en un original que en su variante, mide memoria, no abducción.

Pares de interés:

| Par | Qué prueba |
|---|---|
| V01 / V02 | Mismo dominio y misma forma superficial, respuestas opuestas: entidad nueva frente a ley incorrecta. Análogo de Neptuno frente a Vulcano |
| A01 / A06 / B01 | El par original |
| V03, V04, V10 | Postular algo nuevo sería un error: el problema está en el observador |

## Saneamiento

Las notas originales describen las observaciones sabiendo la respuesta. Al convertirlas se quitaron o reformularon las frases que revelaban la solución; el campo `saneamiento` de cada caso dice qué se cambió. La conversión la hizo un LLM y la revisó otro: puede quedar algún indicio. Si un caso resulta trivial para la línea base, conviene revisar primero su saneamiento.

## Composición

Son 50 casos: 40 reales y 10 variantes. Tipos de causa de los 40 reales:

| Tipo | Casos |
|---|---|
| `mecanismo_conocido` | 14 |
| `error_del_observador` | 11 |
| `entidad_nueva` | 10 |
| `ley_incorrecta` | 5 |

Contaminación: 29 alta, 8 media, 13 baja (las 10 variantes, D06, E07 y E08).

## Casos débiles

Lo señalaron los propios conversores. Conviene excluirlos o tratarlos aparte al leer resultados:

- **Se resuelven por memoria:** E01, E02 y E04, de una sola pieza y muy famosos.
- **Casi delatan la respuesta en la evidencia** (útiles como casos fáciles de control): A05, B02, B07, C01, C06, D06 y E05.
- **Imposibles de anonimizar dentro del caso original:** D07 y D08.
- **Tipo de causa discutible:** A08, B05, B06, C07 y D04. Por eso llevan `tipo_secundario`.
- **Verdad débil:** D01 (`tentativa`, 0,75). D02 y D03 tienen una parte de su verdad disputada.
- **Fuentes:** A08 conserva las URL de K–Ar aunque esa parte se dejó fuera. Varios casos tienen hechos agregados desde conocimiento general, sin URL; cada conversor los detalla en `saneamiento` o en su informe.
- **Caso pendiente:** el exceso de argón (K–Ar) podría formar un caso propio de `error_del_observador`.

## Limitaciones

- **URL:** las de la serie A y otras se copiaron de las notas sin verificar que funcionen.
- **Serie E:** es delgada (una sola fuente por caso) y aporta poco, salvo E07 y E08.
- **Dificultad:** no está calibrada.
- **Circularidad de las variantes:** las escribió el mismo asistente que diseñó el marco (12 §12.5). Su verdad es "por construcción" respecto de una estructura que él mismo eligió.
