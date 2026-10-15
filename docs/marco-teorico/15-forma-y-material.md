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
