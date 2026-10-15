# EXP-016 — ¿Los generadores recuperan la explicación verdadera en casos reales?

- **Fecha:** 2026-10-15 · **Estado:** registrado
- **Registro previo:** sí. Este commit va antes de preparar los datos y de generar.
- **Origen:** [generación §2 y §6](../marco-teorico/generacion.md); la sonda ciega de los [escenarios G1–G7](../experimentos-mentales/09-escenarios-generacion.md#lectura-ciega-2026-10-15-la-generación-libre-encontró-todo), donde un modelo fuerte encontró la verdad en los siete sin operadores.

## Pregunta

En casos reales recientes, y viendo solo lo que se sabía en su momento, ¿con qué frecuencia los generadores del motor incluyen el mecanismo documentado entre sus candidatas? **¿Es la generación el cuello de botella?**

Si casi siempre lo incluyen, construir operadores abductivos no se justifica para estos generadores, y el problema está en otra parte: encontrar la pista, conseguir la observación que falta o probar. Si rara vez lo incluyen, la premisa de la generación se sostiene.

## Diseño

### 1. Datos: conjunto R (15 casos, resueltos entre mayo y octubre de 2026)

Se parte de la [salida de la investigación 2](../../datasets/abd-bench/fuentes/investigacion-2/README.md). El saneamiento se hace con reglas fijadas aquí, antes de mirar las generaciones:

- **Se quita toda observación fechada el día de la resolución o después.** Por ejemplo, la de R06 del 20 de julio y las dos de R08 del 24 de septiembre.
- **Se quita toda observación cuya fuente tenga una fecha en la URL igual o posterior a la resolución.** Así cae, por ejemplo, la frase de R03 "nadie asociaba [el producto] con riesgo de explosión", tomada de un artículo de 2026.
- **El generador no ve el título del caso ni el nombre de quien estableció la resolución.** Los observadores se describen por su marco.
- **Se registra cada observación quitada.** Si a un caso le queda menos de dos observaciones, sale del análisis y se informa.

### 2. Verdad de referencia, fijada antes de generar

Un agente sin contexto, que no es ninguno de los generadores ni el juez, recibe **solo la resolución** de cada caso. Escribe de 2 a 4 **elementos clave** del mecanismo y marca uno como **núcleo**: el eslabón causal sin el cual la explicación es otra. Por ejemplo:

- en R04, el núcleo es "gas inflamable que retorna al fogón por abrir a la vez las válvulas de aislación";
- en R01, "sobrepeso en condiciones de engelamiento, con pérdida de sustentación".

Después, un segundo agente sin contexto recibe **las observaciones saneadas y los elementos clave**, sin la resolución completa, y califica la **inferibilidad** de cada elemento:

| Calificación | Significado |
|---|---|
| `sí` | Los hechos apuntan a él |
| `parcial` | Es compatible y se puede sugerir desde los hechos y el conocimiento del dominio |
| `no` | Requiere información ausente |

Con eso se forman dos grupos:

- **Análisis principal:** casos con núcleo `sí` o `parcial`.
- **Grupo aparte:** casos con núcleo `no`. Ahí acertar mide conocimiento del dominio o memoria, no inferencia desde los hechos.

**Casos triviales:** si las observaciones casi enuncian el mecanismo, el agente lo marca. Se informan aparte y no entran al criterio de decisión.

Todo esto se guarda en `datasets/abd-bench/recuperacion/` y se sube **antes** de generar.

### 3. Generación

| Factor | Niveles |
|---|---|
| Modelo | Muse 1.3 (respaldo 1.2, se registra cuál respondió) y DeepSeek V4.1 Flash. Son los generadores del motor |
| Pregunta | **Libre:** "propón las 10 explicaciones más probables del mecanismo, de más a menos probable". **Diversa:** lo mismo, "muy distintas entre sí, incluyendo hipótesis poco convencionales que un experto consideraría" |
| Corridas | 3 por combinación, temperatura 1,0 y sin caché, para medir la variación |

En total son 15 × 2 × 2 × 3 = 180 llamadas. Cada salida es una lista ordenada de 10 mecanismos, de una o dos frases cada uno. No se usa el motor: se mide solo la generación.

**Referencia (no decide):** un modelo fuerte de otra familia, el mismo tipo de agente que hizo la sonda de los escenarios, con la pregunta libre y una corrida.

### 4. Juez

Un agente sin contexto, de una familia distinta a los generadores, **ciego a la condición**: las listas se mezclan y se identifican con códigos. Para cada candidata y cada elemento clave decide si lo cubre (`sí`, `parcial` o `no`). La rúbrica exige el **eslabón causal**, no el tema: "una falla mecánica en el elevador" no cubre "el tapón del contrapeso se aflojó y trabó el elevador"; "un tapón o pieza suelta que trabó el elevador" sí lo cubre.

**Concordancia humana:** el usuario califica una muestra aleatoria de 20 pares (candidata, elemento), sin ver la decisión del juez. Se informa el acuerdo. La decisión del juez vale igual, pero si el acuerdo es menor a 70 %, el resultado se declara **no concluyente**.

### 5. Métricas

- **Primaria:** *núcleo@5*. Fracción de casos del análisis principal donde alguna de las 5 primeras candidatas cubre el núcleo con `sí`. Se promedia sobre las corridas y se informa por modelo.
- **Secundarias:**
  - *núcleo@1*, *núcleo@10*;
  - *núcleo en alguna corrida* (la unión de las tres);
  - *cobertura de elementos@10*;
  - las mismas métricas con `parcial`;
  - el grupo aparte (núcleo `no`);
  - los triviales;
  - el efecto de la pregunta diversa.
- **Incertidumbre:** con n tan chico se informan intervalos de Wilson y el detalle caso por caso.

## Expectativa y reglas de decisión (antes de correr)

**Regla de decisión,** sobre *núcleo@5* con la pregunta libre, en el análisis principal, promediando los dos modelos:

| Resultado | Decisión |
|---|---|
| **≥ 70 %** | La generación no es el cuello de botella para estos generadores en casos reales. Los operadores pasan a segundo plano; el foco va a encontrar la pista, buscar la observación que falta y probar |
| **≤ 40 %** | La premisa de la generación se sostiene: se justifica el experimento de operadores ([generación §6](../marco-teorico/generacion.md#6-cómo-se-mide)) |
| **Entre 40 % y 70 %** | No concluyente por sí solo. Si la pregunta diversa sube *núcleo@5* en 15 puntos o más, la diversidad barata podría bastar, y los operadores tendrían que superarla |

**Mi predicción,** para poder contrastarla después:

- *núcleo@5* libre de alrededor del 55 %, en la zona no concluyente;
- la pregunta diversa, unos 10 puntos más;
- Muse y DeepSeek parecidos;
- en el grupo con núcleo no inferible, alrededor del 30 %;
- la referencia fuerte, por encima de ambos generadores.

## Amenazas conocidas

- **n chico:** quizás 8 a 10 casos en el análisis principal. Esto es una medición piloto, no una prueba.
- **Contaminación:** los incidentes ocurrieron entre 2024 y 2025, y sus reportes preliminares eran públicos. La resolución es posterior a mayo de 2026, pero no conocemos la fecha de corte de entrenamiento de los generadores.
- **Calidad de la verdad:** las resoluciones vienen de una investigación externa. Solo R03 se verificó contra la fuente primaria.
- **El juez y los autores de los elementos clave son del mismo tipo de agente.** Puede haber sesgos compartidos; la concordancia humana es el control.
- **Las observaciones las seleccionó la investigación,** con su propio criterio de qué era relevante.

## Resultado

*(pendiente)*
