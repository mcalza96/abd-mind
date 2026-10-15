# 15 — Forma y material: qué puede aportar un motor hecho de juicios de LLM

Revisión de la base del proyecto después de [EXP-001 a EXP-013](../bitacora/README.md). Surgió de dos objeciones del usuario:

1. **Delegar la variabilidad:** con la selección holística ([14](14-rumbo-estado-y-proyeccion.md)) la decisión la toma el modelo, no el motor.
2. **Los ladrillos blancos:** combinar más juicios del modelo (varios jueces, varias muestras) tampoco cambia nada de fondo: "con 100 ladrillos blancos la pared no será roja".

**Estado:** hipótesis de trabajo, sin validar. Este documento no deroga el 14; cuestiona su premisa.

## 15.1 Lo que muestran los experimentos

| Experimento | Resultado |
|---|---|
| EXP-001 (sintético) | El motor acierta, pero la línea base también: no se demostró aporte propio |
| EXP-002, 003, 005 | El motor cumple sus propiedades en casos construidos por nosotros (circular, 12 §12.5) |
| EXP-008 | En casos reales no decide: el verificador LLM acepta casi todo |
| EXP-010 | Decide, pero acierta 10 de 20; Muse 1.3 en una llamada, 18 de 19 |
| EXP-012 | Acierta menos que la línea base y no se abstiene más |
| EXP-013 | Con selección holística iguala al modelo que juzga |

1. **No hay un solo caso** en que el motor supere a un LLM en una sola llamada.
2. **Las correcciones convergieron hacia la línea base.** Cada una acercó el motor a "preguntarle todo junto a un LLM":
   - el veredicto de tres valores;
   - la verificación comparativa;
   - el juez de parsimonia;
   - la selección holística.

   Es la señal de un programa de investigación degenerativo (Lakatos): el núcleo se protege con hipótesis auxiliares en vez de revisarse.

## 15.2 Forma y material

Cien ladrillos blancos no hacen una pared roja, pero sí hacen un arco: ningún ladrillo suelto sostiene peso como un arco. La disposición crea propiedades, pero de dos clases distintas:

| Clase | Ejemplos | ¿Puede crearla la disposición? |
|---|---|---|
| **Forma** | Coherencia, trazabilidad, reglas duras, derrota, abstención explicada, verdad con historia | Sí |
| **Material (contenido)** | Saber algo del mundo que los componentes no saben | No: solo puede venir de los componentes o de fuera del sistema |

Los resultados calzan con esta división. El motor aportó forma: auditoría, derrota, abstención con su justificación. No aportó contenido: no supo del mundo más que el modelo que lo componía.

**Consecuencia:** no hay que preguntar cómo ordenar mejor los juicios del modelo. La pregunta es **qué material que no sea el modelo entra al sistema**. Por eso se descarta como respuesta de fondo medir la variabilidad entre modelos (autoconsistencia, varios jueces): sigue siendo material del mismo color. Puede mejorar la forma, por ejemplo una abstención mejor calibrada, pero no el contenido.

## 15.3 El LLM es un observador, no el razonador

Según el propio marco ([02](02-postulados.md), [09](09-robustez-epistemica.md)), un LLM es **un observador con un marco**. Su proyección es lo que el corpus humano tiende a decir sobre un caso así.

Ahí está la contradicción con la implementación:

- **La teoría:** la verdad aparece cuando observadores con **marcos distintos** discrepan y se busca la hipótesis que produce todas sus sombras.
- **La implementación:** hizo pasar **todas** las observaciones por un único marco, el del LLM que verifica (π en dominios abiertos, L2).

La implementación eliminó la pluralidad que la teoría necesita. Es Duhem-Quine aplicado al propio diseño: toda la evidencia se leyó a través de una sola teoría de fondo.

La frase "el LLM propone, un backend determinista decide" (README, punto 4) es falsa en dominios abiertos. Lo determinista es solo la suma. Cada término es un juicio del modelo, y ese juicio ("¿esta hipótesis produciría esta observación?") es la parte difícil de la abducción.

## 15.4 Un banco cerrado no puede medir abducción

La abducción es inferencia **ampliativa**: va más allá de los datos dados. Le Verrier no ganó por elegir la mejor explicación de la órbita de Urano. Ganó porque su hipótesis se comprometió con una posición en el cielo, y Galle miró. Con Vulcano el razonamiento fue el mismo y el telescopio dijo que no. Lo que distinguió ambos casos no fue la inferencia, fue **el contacto con el mundo después del compromiso**.

abd-bench es texto cerrado: todo lo que hay está en el enunciado. Lo mejor posible ahí es razonar bien sobre lo dado, y eso un LLM lo hace bien. **El diseño de la prueba excluía de antemano el aporte que se quería medir.** Esto no invalida los resultados: muestra qué miden y qué no.

Además, la evaluación usó una etiqueta inventada (`tipo_de_causa`), contra el primer principio del marco. Al menos dos errores de EXP-010 fueron de etiqueta (lección transversal 11).

## 15.5 La tesis original, releída

[01](01-problema-y-tesis.md) sostiene que el aprendizaje supervisado tiene un techo. El proyecto construyó una arquitectura hecha solo de modelos aprendidos de texto, y chocó con el techo de esos modelos.

**El fracaso es coherente con la tesis y refuta la implementación:** dentro del sistema no había material que no fuera corpus.

## 15.6 Fuentes de material que no es el modelo

1. **El mundo:** observaciones que el motor pide y la realidad responde (datos, precios, experimentos, búsquedas).
2. **El tiempo:** predicciones que se resuelven después.
3. **El cálculo sobre datos:** una descomposición de retornos, o una identidad contable, no es plausibilidad lingüística (C, [14 §14.3](14-rumbo-estado-y-proyeccion.md#143-c-proyección-calculable-en-dominios-reales)).
4. **El usuario:** lo que sabe y observa directamente.

**Objeción:** un agente con herramientas (Hermes con búsqueda web) también toca el mundo. Si el motor solo agrega acceso a datos, no aporta nada propio. La línea base justa deja de ser "un LLM en una llamada" y pasa a ser **"el mismo agente con las mismas herramientas, sin el motor"**.

## 15.7 Hipótesis: el aporte es el compromiso previo

Un agente con herramientas busca y después racionaliza: acomoda la hipótesis a lo que encontró (lección transversal 4). El conocimiento viene del **riesgo**, en el sentido de la severidad de Popper: una prueba vale en la medida en que la hipótesis probablemente fallaría si fuera falsa. Eso exige:

1. **Fijar la predicción antes de mirar.** Queda registrada, fechada e inmutable.
2. **Elegir la observación que más arriesga**, es decir, la que separa a las rivales (`sugerir_observacion`).
3. **No reinterpretar después:**
   - si la predicción falla, la hipótesis paga (derrota);
   - si se la quiere salvar, la modificación queda registrada como hipótesis auxiliar, con su costo.
4. **Llevar la cuenta.** Jueces, observadores y generadores se califican por predicciones resueltas, no por consenso (D11).

**Observación reflexiva:** es lo que mantuvo honesto a este mismo proyecto. Las hipótesis las proponía un LLM; lo que les dio contenido fue comprometerlas por escrito en la bitácora (registro previo) antes de que los resultados respondieran. El producto podría ser eso: **una máquina de registro previo para el razonamiento de un agente**, no un juez mejor.

## 15.8 Qué la falsaría

- **Prueba:** un agente con el motor (predice antes, mira después, paga por fallar) frente al mismo agente con las mismas herramientas y sin el motor.
- **Medida:** cuánto anticipan resultados reales que no se conocían al momento de razonar.
- **Fracaso:** no hay diferencia en calibración (puntaje de Brier sobre predicciones resueltas) ni en precisión. En ese caso, la hipótesis 15.7 se descarta.

**Dónde probarla:**

- **Conjunto F** de la segunda investigación: caídas de acciones con desenlace posterior a mayo de 2026.
- **Mundos sintéticos** donde el motor pueda pedir observaciones a un simulador cuya verdad se conoce por construcción (D21).

**Advertencia de sesgo:** esta reformulación es elegante y vuelve a salvar el proyecto, igual que las correcciones anteriores. Merece la misma desconfianza. La escribió el mismo asistente que diseñó el marco.

## 15.9 Qué cambia y qué no

- **Se conserva:** las etiquetas como proyecciones, los observadores falibles, la derrota, la verdad de cierre con historia, las reglas duras y la auditoría. Todo eso es forma, y la forma sí se puede construir.
- **Se abandona como promesa:** que el motor razone mejor que el modelo en dominios abiertos, o que una fórmula sobre juicios de un LLM decida mejor que el LLM.
- **Se suspende:** la elección del modelo juez y la optimización de la selección. Era optimizar la pieza equivocada.
- **Pendiente:** evaluación externa de este documento por un agente sin contexto, y una investigación de literatura relacionada.

## 15.10 Evaluación externa (2026-10-15)

Un agente sin contexto leyó solo este documento y lo evaluó de forma adversarial. Veredicto: **correcto en parte**. Se registra lo que aceptamos, sin reescribir las secciones anteriores (regla 3 de la bitácora).

**Aceptado:**

1. **Confusor de modelo en 15.1.** En EXP-010 y EXP-012 las piezas que deciden usan DeepSeek, y la línea base más fuerte es Muse 1.3. Contra el **mismo** modelo, la diferencia es menor:

   | Comparación (V + P) | Aciertos |
   |---|---|
   | DeepSeek en una llamada | 10/18 |
   | Motor con score (EXP-012) | 8/18 |
   | Motor holístico (EXP-013) | 10/18 |

   "Rinde por debajo de un LLM" vale sobre todo frente a un modelo más fuerte.
2. **Falta una línea base de igual cómputo.** El motor hace muchas llamadas. Hay que compararlo con autoconsistencia o best-of-n del mismo modelo y el mismo presupuesto.
3. **15.2 es demasiado fuerte.** La disposición puede **sacar a la superficie** contenido latente: la autoconsistencia y la descomposición mejoran el acierto en la literatura. Además, si la disposición pudo **restar** acierto (EXP-010), opera sobre el contenido. La versión defendible es más estrecha: *sin retroalimentación externa, combinar juicios del modelo no agrega conocimiento del mundo*. Hay que verificarla en la literatura.
4. **Contradicción entre 15.2 y 15.3.** Si la pluralidad de marcos es constitutiva, modelos de familias distintas son al menos pluralidad parcial. No se puede descartar y reclamar a la vez.
5. **Duhem-Quine está mal aplicado en 15.3.** Lo que se describe es carga teórica de la observación (Hanson, Kuhn) o un único punto de falla, no subdeterminación.
6. **15.4 exagera.** En Peirce, la abducción es la generación de hipótesis; un banco cerrado sí mide generación y selección. Lo que no mide es el ciclo de contrastación. Además, "excluía el aporte" explicaría un empate, no una derrota.
7. **15.5 inmuniza la tesis.** "El fracaso es coherente con la tesis" la vuelve irrefutable. Se retira como argumento.
8. **15.7 no es nuevo.** Ya existen pronóstico con LLMs puntuado con Brier, preregistro, diseño experimental bayesiano y agentes científicos con bitácora. El preregistro da credibilidad ante terceros, pero no mejora por sí solo el acierto de quien predice. Para eso hace falta un bucle de aprendizaje con lo resuelto, y 15.7 no lo especifica.
9. **La anécdota reflexiva se corrige.** La honestidad de esta revisión vino de un crítico externo (el usuario), no del registro previo.
10. **15.8 está mal especificado:**
    - no aísla qué se manipula (la línea base también debe emitir probabilidades antes de la resolución);
    - le falta un cálculo de potencia y un margen de equivalencia;
    - el conjunto F tiene poca señal, eventos correlados y riesgo de fuga por búsqueda retroactiva;
    - los mundos sintéticos propios reintroducen la circularidad.

**Siguientes pasos:**

1. **Análisis de errores caso a caso**, antes de seguir teorizando: en qué casos el motor falla y la llamada única acierta, y por qué (contexto perdido, verificador, agregación, etiqueta).
2. **Ablación con el mismo modelo e igual cómputo:** llamada única, autoconsistencia y motor.
3. **Investigación de literatura antes de construir** ([prompt](../investigacion/prompt-deep-research-3-literatura-relacionada.md)).
4. **Separar las dos propuestas de valor.** La forma (auditoría, trazabilidad) se evalúa con usuarios; el acierto, con bancos.
5. **Probar 15.7 primero en dominios con verificación externa rápida:** tests de software, datos retenidos o simuladores ajenos al proyecto.
