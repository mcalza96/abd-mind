# Generación abductiva

Cómo se le ocurre a una IA lo no obvio: disparadores, operadores abductivos, el filtro entre lo no obvio y lo rebuscado, y cómo se mide. Es el centro del marco ([tesis](tesis.md)). La versión con su historia completa y la evaluación externa está en [histórico, 17](../historico/marco-teorico/17-generacion-abductiva.md).

## 1. Qué es "no obvio"

Sea $G$ un generador (un LLM) que, ante los hechos $F$ y una manera de preguntar $q$, propone hipótesis con probabilidad $p_G(H \mid F, q)$.

- **Obvia:** $p_G(H \mid F, q_0)$ es alta con la pregunta habitual $q_0$ ("¿qué explica esto?"). Es lo primero que se le ocurre.
- **No obvia:** $p_G(H \mid F, q_0)$ es baja, **pero**, una vez propuesta, hace que los hechos sean "cosa corriente": su puntuación predictiva ([EXP-015](../bitacora/EXP-015-puntuacion-predictiva-en-el-motor.md)) es alta.
- **Rebuscada:** $p_G$ es baja **y** la puntuación predictiva también. Merlín, las conspiraciones, los parámetros libres que acomodan todo ([historia 7](../experimentos-mentales/07-el-objeto-que-cambia.md)).

Lo que se busca está en una sola esquina: **baja probabilidad para el generador, alta capacidad predictiva una vez dicha.**

**Qué hay que declarar para que la definición sea operativa:**

- **Las condiciones:** el generador, la pregunta base $q_0$, la decodificación, el número de muestras N y el juez que decide si dos hipótesis son la misma.
- **Varias corridas independientes:** "no estaba en la generación libre" cambia con la semilla, así que se mide con semillas distintas a las usadas para elegir los casos.
- **Una aproximación declarada como tal:** con modelos por API, $-\log p_G$ no se puede observar, y en la práctica se aproxima por frecuencia de aparición.

**La conclusión más importante del documento 15 y de la historia 3:** pedir más muestras con la misma pregunta $q_0$ produce más de lo mismo. Cien jueces de igual formación dicen "cilindro" cien veces. Muestrear más no mueve la distribución; **cambiar la pregunta sí.**

## 2. Tesis

> **Una pregunta distinta encuentra lo que más muestras no encuentran.** Condicionar al generador con una pregunta que cambia su marco, $p_G(H \mid F, q_o)$, lleva probabilidad hacia explicaciones que con la pregunta habitual están en la cola. Llegar ahí subiendo la temperatura o pidiendo más muestras es muy ineficiente. Esas preguntas se pueden catalogar: son los **operadores abductivos**.

Tres precisiones, que salen de la lectura ciega (§10):

1. **No es "cambio de marco *en vez de* muestreo".** Aplicar un operador sigue siendo muestrear, pero de otra distribución. La tesis es **empírica**: hay que mostrar que los operadores superan a las formas baratas de diversidad (temperatura alta, "propón hipótesis muy distintas entre sí", personas, *step-back*), no darlo por hecho.
2. **Los operadores son genéricos.** Para cualquier H* existe una pregunta que la vuelve probable ("¿y si fuera H*?"). La tesis solo tiene contenido si cada operador **no depende de la respuesta** y se elige **sin conocerla**, a partir del disparador. Si no, es trampa.
3. **Respecto de quién es "no obvio".** De un generador declarado, con una pregunta base, una decodificación y un número de muestras declarados (§1). Una explicación no obvia para un LLM puede ser obvia para un experto, y al revés.

Esto resuelve una contradicción que dejó abierta la revisión de la base (histórico 15 §15.10). El marco necesita **pluralidad de marcos de observación**, y la implementación los colapsó en uno. Un operador abductivo es exactamente **un marco distinto aplicado al mismo modelo**. La pluralidad se puede producir a voluntad, y además se puede combinar con modelos de distinta formación (A8: diversidad para generar).

**Límite honesto (P6, [principios, P6](principios.md#p6--contacto)):** un operador **saca a la superficie** lo que el modelo sabe y no dice. No agrega conocimiento del mundo. Si el modelo nunca supo de bicilindros, ninguna pregunta se lo hará proponer. La recombinación de lo conocido en una configuración nueva sí está a su alcance, y Peirce sostenía que de eso está hecha la mayoría de las ideas nuevas. No prometemos más que eso.

## 3. Los disparadores: cuándo hay algo que explicar

Una abducción empieza con una sorpresa. Hoy el motor reconoce una sola: "ninguna hipótesis explica todo" (postulado 3). Las historias mostraron que hay más, y que la más peligrosa es la que **no parece sorpresa**:

| Disparador | Qué se nota | Historia o ejemplo |
|---|---|---|
| **Contradicción** | Dos reportes no pueden ser ciertos a la vez | El cilindro (1), la lámpara torcida (5) |
| **Coincidencia** | Dos valores coinciden sin razón aparente | Olga y Sara miden lo mismo ([EXP-014](../bitacora/EXP-014-salas-en-codigo.md)); las costas de África y Sudamérica (Wegener) |
| **Residuo** | Un hecho queda sin explicar, o se lo atribuye a un error | El triángulo del tercer observador (5.3) |
| **Ausencia** | Falta algo que debería estar | El perro que no ladró (Conan Doyle) |
| **Ajuste demasiado bueno** | Todo calza y todos coinciden | Los cien jueces (3); el cubo "macizo" (8) |
| **Regularidad sin mecanismo** | Algo se repite y nadie sabe por qué | Las rachas, los ciclos, los patrones sin causa conocida |
| **Pregunta sin resolver** | Las hipótesis empatan y responden distinto | La ventana que nadie abrió (2) |
| **Fallo de predicción** | Lo que una hipótesis aceptada predijo no ocurrió | Distinto de la contradicción entre reportes: la sorpresa es contra una expectativa propia |
| **Cambio de régimen** | Una relación estable se rompe en un momento | Discontinuidades, cambios de tendencia |
| **Anomalía de magnitud** | El fenómeno es esperable, pero no de ese tamaño | El 35 % contra el 8 % del sector (6) |

El **ajuste demasiado bueno** es el disparador que corrige al postulado 3 (A7): que todo calce **también** obliga a buscar.

**Los disparadores se detectan de forma automática y se evalúan por separado.** Si los marca un humano, o quien escribió el caso, la información sobre la respuesta se filtra por ahí.

## 4. Catálogo de operadores abductivos

### Principio de construcción

La primera versión listaba 14 operadores sacados de ocho historias: una muestra de conveniencia, con solapamientos y huecos. Ahora el catálogo se deriva del **esquema de una explicación**. Toda explicación postula:

- entidades;
- leyes que las rigen;
- un grafo causal entre ellas;
- un modelo de cómo se observan;
- un tiempo;
- una población o escala;
- una parte que es azar.

**Un operador perturba un componente.** Así se puede comprobar si el catálogo está completo: cada componente tiene que tener al menos un operador. Se agrega una fuente que no perturba ningún componente: traer la estructura de **otro dominio**, es decir, la analogía.

Los ids de la primera versión se conservan.

| Componente | Id | Operador | La pregunta | Ejemplo | Riesgo |
|---|---|---|---|---|---|
| **Entidades** | O6 | Entidad oculta | ¿Qué cosa no vista produciría la anomalía? | Neptuno | Vulcanos |
| | O2 | Gemelo observacional | ¿Qué **otra** cosa produciría exactamente lo mismo? | El bicilindro (3), el tapón (2) | Gemelos rebuscados |
| | O15 | Identidad | ¿Son dos cosas que parecen una, o una que parece dos? | — | Multiplicar o fusionar sin evidencia |
| **Leyes** | O5 | Sospechar de la ley | ¿Y si la regla que liga las observaciones es falsa? | Vulcano y la relatividad | Abandonar leyes buenas |
| | O16 | Umbral o no linealidad | ¿Y si el efecto cambia de naturaleza pasado cierto punto? | — | Ajustar curvas a voluntad |
| | O17 | Simetría | ¿Qué debería conservarse y no se conserva, o al revés? | — | Simetrías decorativas |
| **Grafo causal** | O9 | Causa común | ¿Hay un tercero que produce ambas cosas? | La bomba de Broad Street (Snow) | Terceros inventados |
| | O10 | Invertir o retroalimentar | ¿Y si el efecto produce la causa, o se refuerzan entre sí? | La reflexividad (6) | Circularidad |
| | O13 | Composición | ¿Y si son varias causas sumadas? | La acción que cae (6) | La compuesta que siempre gana (A22) |
| | O1 | Reconciliar | ¿Qué estructura haría que **todos** tengan razón? | El cilindro (1) | Quimeras |
| **Observación** | O4 | Sospechar del instrumento | ¿Y si el error está en cómo se mira? | La lámpara (5); los neutrinos de OPERA, un cable mal conectado | Culpar al observador para salvar la hipótesis |
| | O8 | Selección | ¿Qué hizo que viéramos justo estos casos? | Los aviones de Wald | Negar patrones reales |
| | O7 | Motivo del observador | ¿Qué sabe o qué gana quien reporta? | El fondo que vende porque sabe (6) | Conspiraciones |
| | O12 | Ausencia significativa | ¿Qué debería estar y no está? | El perro que no ladró | Leer demasiado en lo que falta |
| **Tiempo** | O14 | Tiempo | ¿Y si no fue simultáneo, o el objeto cambió? | Las lámparas a la vez (7) | Historias de cambio sin evidencia |
| **Población o escala** | O18 | Heterogeneidad | ¿Y si son subpoblaciones que se comportan distinto? | La paradoja de Simpson | Partir los datos hasta encontrar algo |
| | O19 | Cambio de nivel | ¿Y si el fenómeno es de otro nivel (micro o macro, emergente)? | — | Saltos de nivel sin puente |
| **Azar** | O20 | **Nulo** | ¿Y si no hay nada que explicar: azar, regresión a la media, tasa base? | — | Descartar señales reales |
| **Otro dominio** | O21 | Analogía | ¿Dónde se vio una estructura así, en otro campo? | Darwin leyendo a Malthus | Analogías superficiales |
| | O3 | Explicar la coincidencia | ¿Por qué coinciden **estos** dos valores? | Olga y Sara (EXP-014), Wegener | Apofenia |

**El nulo (O20) es obligatorio** cada vez que se aplica O3, O9 u O18. Sin él, el catálogo empuja a ver patrones donde no los hay.

**Lo que salió del catálogo:** O11 ("cambiar de instrumento") no genera explicaciones: diseña pruebas. Pasa al tercer momento de Peirce, junto con la sugerencia de observación (A27).

**Lo que falta definir:** la **política**, es decir, qué operadores aplicar ante qué disparador, en qué orden, cómo combinarlos (por ejemplo O6 con O14), con qué presupuesto y cuándo parar. Es la "economía de la investigación" de Peirce, y está por diseñar. Por ahora el catálogo dice qué preguntas existen, no cuáles hacer.

## 5. Qué separa lo no obvio de lo rebuscado

Un operador produce hipótesis improbables a propósito. Sin un filtro, eso sería una fábrica de conspiraciones. La primera versión decía que el filtro ya existía. Era cierto solo en parte: el filtro tiene cuatro problemas, y aquí se rediseña.

1. **Se evalúa con hechos que la hipótesis no vio.** Una conspiración o Merlín tienen verosimilitud **alta** sobre los hechos que acomodan. Si la puntuación usa los mismos hechos que generaron la hipótesis, cuenta dos veces. El filtro usa:
   - **hechos reservados:** se generan hipótesis con parte de los hechos, y se puntúan con el resto (la novedad de uso de Worrall y Lakatos);
   - **o la validación dejando una fuera con familias** ([EXP-015](../bitacora/EXP-015-puntuacion-predictiva-en-el-motor.md)), que penaliza la flexibilidad.
2. **No hay rechazo binario: existe el estado *prometedora*.** Wegener esperó cuarenta años porque no tenía mecanismo. Copérnico no predecía mejor al principio. Una conjetura no obvia que todavía no predice mejor, pero que tampoco está refutada, no se descarta. Queda **prometedora**, con la observación que la separaría de sus rivales y lo que costaría hacerla. Es la tolerancia de Lakatos con los programas que todavía no progresan.
3. **Las entidades nuevas pagan, y las auxiliares según su frecuencia** (A5, A16). Neptuno pagó y ganó; Vulcano pagó y perdió.
4. **En dominios sin proyección exacta, el filtro lo hace un modelo.** Si es el mismo que generó la hipótesis, el sistema es circular. La exigencia mínima es un juez de otra familia, que no vea qué operador produjo cada hipótesis. Aun así es un juicio, no un cálculo, y la auditoría lo dice. **El filtro fuerte solo existe donde hay proyección o hechos reservados.** Eso define dónde se puede validar primero esta teoría: en las salas y en casos con hechos reservados.

Se definen tres medidas de una hipótesis:

| Medida | Definición | Qué busca |
|---|---|---|
| **Novedad** | Frecuencia de aparición en la generación de referencia (§1), medida con semillas independientes | Que no sea lo obvio |
| **Valor explicativo** | Puntuación sobre hechos reservados, o predictiva con familias | Que no sea rebuscada |
| **Costo de prueba** | Qué observación la separa de sus rivales y cuánto cuesta | Que valga la pena seguirla |

**Riesgo de Goodhart:** si se optimiza la novedad, el sistema produce rarezas que pasan un filtro débil. Por eso la novedad nunca se premia sola: solo cuenta si viene con valor explicativo.

## 6. Cómo se mide

La pregunta deja de ser "¿acierta la etiqueta?" y pasa a ser:

> **Cuando la explicación verdadera no es la obvia, ¿aparece entre las candidatas?**

La primera versión de este diseño permitía que cualquier resultado positivo se explicara por artefactos. Se blinda así:

1. **Se separan los bancos de desarrollo y de prueba.**
   - Los operadores salieron de las historias 1 a 8, así que esas salas son el banco de **desarrollo**, no de prueba.
   - **El catálogo se congela antes** de escribir los casos de prueba.
   - Los casos de prueba los escribe **otro autor que no conoce el catálogo**: un agente sin contexto, con la instrucción de construir salas con una verdad oculta no obvia.
2. **Selección de casos sin regresión a la media.** Los casos se eligen porque la generación libre no encontró la verdad con ciertas semillas, y se evalúan con **otras semillas, independientes**. Además se reporta el resultado sobre **todos** los casos, no solo sobre los elegidos.
3. **Igual cómputo de verdad:** se iguala el número de candidatas k y los tokens, no solo el número de llamadas. La métrica es la recuperación con k candidatas (recall@k), porque recuperar más es trivial si se generan más.
4. **Líneas base fuertes:**
   - generación libre;
   - temperatura alta;
   - "propón hipótesis muy distintas entre sí";
   - muestreo verbalizado (pedir hipótesis con su probabilidad);
   - personas variadas;
   - *step-back*;
   - Self-Discover.
5. **Placebo de operadores.** Preguntas con la misma forma, pero sin contenido heurístico, y operadores asignados al azar sin relación con el disparador. **Solo el placebo separa el efecto del contenido del operador del efecto de la mera diversidad.**
6. **Juez ciego.**
   - No sabe qué condición produjo cada candidata.
   - Usa una rúbrica que exige coincidencia de **mecanismo**: "algo hueco" no es "cubo hueco".
   - En una submuestra se mide su concordancia con un humano, el usuario.
7. **Disparadores automáticos**, medidos por separado.
8. **Preregistro** de los umbrales: cuánto más tiene que recuperar para contar como "más", y cuántas pistas falsas son "demasiadas".

**Bancos:**

| Banco | Para qué |
|---|---|
| **Salas nuevas**, de un autor ciego, con proyección exacta | El filtro fuerte existe; la verdad es por construcción |
| **Conjunto R**, casos posteriores a mayo de 2026 | Casos reales. Advertencia: n pequeño, y la fecha no garantiza que el patrón explicativo no esté en el preentrenamiento |
| **Perturbaciones P de abd-bench** | Casos donde la respuesta cambió por un hecho decisivo |
| **Casos científicos** (pendiente) | Contra el **sesgo de género**: las salas y casi todo abd-bench son acertijos detectivescos. Una IA que resuelve adivinanzas no es todavía una IA que genera explicaciones científicas |

**Qué falsaría la tesis:** con igual cómputo, la generación guiada por operadores no recupera más verdades no obvias que **la mejor línea base y que el placebo**, o las recupera solo a costa de más pistas falsas de las preregistradas.

## 7. Qué pasa con lo construido

Nada se tira. Cambia su lugar en el ciclo:

```text
disparador ──► operadores ──► hipótesis no obvias ──► filtro ──► observación que separa ──► registro
 (17.4)          (17.5)          (familias)            (17.6)       (A3, A15, A23)         (P3, A9)
```

| Pieza existente | Nuevo papel |
|---|---|
| Postulados y principios ([principios](principios.md)) | Siguen siendo la epistemología: mediación, ley, riesgo, subdeterminación, pregunta y contacto |
| Expansión ontológica (postulado 3) | Pasa a ser **un** operador (O6), y se dispara también por ajuste demasiado bueno |
| Consiliencia y puntuación predictiva ([formalización](formalizacion.md)) | El **filtro**: separan lo no obvio de lo rebuscado |
| Verificación, derrota, sugerencia de observación | La **prueba** de la conjetura |
| Selección holística (ADR-0016) | Sigue disponible donde no hay proyección |
| Predicciones, verdad, registro ([formalización](formalizacion.md), historia 4) | Dicen, con el tiempo, **qué operadores** producen conjeturas que resultan ciertas |
| Experimentos mentales | Fuente de operadores y de escenarios de prueba |
| abd-bench, conjunto R | Bancos para medir la recuperación de verdades no obvias |

**El último punto es nuevo.** El registro de predicciones resueltas, que antes servía para calificar jueces, sirve también para **calificar operadores**: cuáles producen conjeturas que después se confirman y en qué dominios. A largo plazo, eso es lo más parecido a que el sistema **aprenda a pensar abductivamente**.

**Advertencia:** calificar operadores por resultados es un problema de bandido con recompensa escasa y muy demorada. Antes de prometerlo hay que estimar cuántos casos resueltos hacen falta para distinguir un operador útil de uno inútil. Hasta entonces, la calificación viene de los experimentos (§6), no del uso.

## 8. Antecedentes

Ninguna de las piezas es nueva. Hay que revisarlas antes de construir:

- **Patrones de abducción:** Schurz (2008, *Patterns of abduction*) distingue la abducción selectiva de la creativa y clasifica la abducción factual, la de leyes, la de modelo teórico y la de segundo orden. **Es el antecedente más cercano**, y el catálogo debe compararse explícitamente con él. También Magnani (la cognición abductiva) y los métodos de Mill.
- **Heurísticas de descubrimiento:** Pólya (*Cómo plantear y resolver problemas*); los 40 principios inventivos de TRIZ (Altshuller), que son un catálogo de operadores para inventar; Lakatos (heurística positiva y negativa); Hanson (*Patrones de descubrimiento*).
- **Descubrimiento científico computacional:** BACON (Langley, Simon y colaboradores); la filosofía computacional de la ciencia de Thagard.
- **Técnicas recientes para hacer preguntar distinto a un LLM:** retroceder a la pregunta general antes de responder (*step-back prompting*, Zheng y colaboradores, 2023); componer una estructura de razonamiento a partir de módulos (*Self-Discover*, Zhou y colaboradores, 2024); el razonamiento por analogía.
- **Diversidad y generación de hipótesis con LLM:** el colapso de modo de los modelos alineados y las técnicas para mitigarlo (muestreo verbalizado); la generación de hipótesis a partir de datos (HypoGeniC); la novedad de las ideas de investigación generadas por LLM (Si y colaboradores, 2024). Las referencias exactas están por verificar.
- **Abducción y generación de hipótesis con LLM, en general:** pendiente de la investigación de literatura ([prompt 3](../investigacion/prompt-deep-research-3-literatura-relacionada.md)). Conviene agregarle una pregunta específica sobre operadores y diversidad de hipótesis.

**Lo que podría ser propio:**

- operadores derivados del **esquema de una explicación** y **acoplados a disparadores** detectados de forma automática;
- un filtro sobre **hechos reservados**, con el estado *prometedora*;
- la **calificación de operadores** por resultados resueltos.

Hay que verificarlo contra Schurz y contra la literatura reciente antes de afirmarlo.

