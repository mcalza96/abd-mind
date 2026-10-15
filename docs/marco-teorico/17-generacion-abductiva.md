# 17 — Generación abductiva: cómo se le ocurre a una IA lo no obvio

**Estado:** nuevo centro del marco. Decisión tomada con el usuario el 2026-10-15: el objetivo es **una IA a la que se le ocurran explicaciones no obvias**. Lo construido no se descarta: se reordena alrededor de este documento (§17.8).

## 17.1 La desviación y el regreso

[01 §1.4](01-problema-y-tesis.md#14-por-qué-un-llm-solo-no-basta) ya lo decía al inicio. Un LLM está sesgado hacia lo frecuente en su corpus, y las explicaciones abductivas valiosas suelen tener baja probabilidad a priori, así que la decodificación las poda. La arquitectura respondió **sacando la decisión del LLM**, y casi todo el trabajo posterior (documentos 04, 09, 11, 13 y 16, y EXP-007 a EXP-015) se dedicó a **elegir** entre hipótesis.

Esa respuesta no atacaba el problema que el propio 1.4 había descrito. Si la explicación verdadera nunca se genera, ninguna selección la encuentra. La historia 3 lo mostró sin ambigüedad: con solo el cilindro propuesto, el motor se equivoca con todas sus garantías intactas.

En términos de Peirce, la abducción tiene tres momentos:

1. **La sorpresa:** "se observa el hecho sorprendente C".
2. **La conjetura:** "pero si A fuera verdad, C sería cosa corriente".
3. **La razón para seguir A:** cuál conjetura vale la pena probar y cómo.

El proyecto trabajó casi solo el tercero. **El pensamiento abductivo vive en el segundo**, y depende del primero.

## 17.2 Qué es "no obvio"

Sea $G$ un generador (un LLM) que, ante los hechos $F$ y una manera de preguntar $q$, propone hipótesis con probabilidad $p_G(H \mid F, q)$.

- **Obvia:** $p_G(H \mid F, q_0)$ es alta con la pregunta habitual $q_0$ ("¿qué explica esto?"). Es lo primero que se le ocurre.
- **No obvia:** $p_G(H \mid F, q_0)$ es baja, **pero**, una vez propuesta, hace que los hechos sean "cosa corriente": su puntuación predictiva ([EXP-015](../bitacora/EXP-015-puntuacion-predictiva-en-el-motor.md)) es alta.
- **Rebuscada:** $p_G$ es baja **y** la puntuación predictiva también. Merlín, las conspiraciones, los parámetros libres que acomodan todo ([historia 7](../experimentos-mentales/07-el-objeto-que-cambia.md)).

Lo que se busca está en una sola esquina: **baja probabilidad para el generador, alta capacidad predictiva una vez dicha.**

**La conclusión más importante del documento 15 y de la historia 3:** pedir más muestras con la misma pregunta $q_0$ produce más de lo mismo. Cien jueces de igual formación dicen "cilindro" cien veces. Muestrear más no mueve la distribución; **cambiar la pregunta sí.**

## 17.3 Tesis

> **La creatividad abductiva es un cambio de marco, no un muestreo.** Una explicación no obvia aparece cuando se le hace al generador una pregunta distinta, bajo la cual esa explicación se vuelve probable: $p_G(H^* \mid F, q_o) \gg p_G(H^* \mid F, q_0)$. Esas preguntas se pueden catalogar. Las llamamos **operadores abductivos**.

Esto resuelve una contradicción que el documento 15 dejó abierta (§15.10, punto 4). El marco necesita **pluralidad de marcos de observación**, y la implementación los colapsó en uno. Un operador abductivo es exactamente **un marco distinto aplicado al mismo modelo**. La pluralidad se puede producir a voluntad, y además se puede combinar con modelos de distinta formación (A8: diversidad para generar).

**Límite honesto (P6, [16 §16.1](16-fundamentos-desde-las-historias.md#p6--contacto-el-contenido-nuevo-entra-por-observaciones)):** un operador **saca a la superficie** lo que el modelo sabe y no dice. No agrega conocimiento del mundo. Si el modelo nunca supo de bicilindros, ninguna pregunta se lo hará proponer. La recombinación de lo conocido en una configuración nueva sí está a su alcance, y Peirce sostenía que de eso está hecha la mayoría de las ideas nuevas. No prometemos más que eso.

## 17.4 Los disparadores: cuándo hay algo que explicar

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

El **ajuste demasiado bueno** es el disparador que corrige al postulado 3 (A7): que todo calce **también** obliga a buscar.

## 17.5 Catálogo inicial de operadores abductivos

Cada operador es una pregunta que cambia el marco del generador. Se aplica cuando aparece cierto disparador y tiene un riesgo propio, es decir, lo que produce cuando se usa mal.

| Id | Operador | La pregunta | Disparador típico | De dónde sale | Riesgo |
|---|---|---|---|---|---|
| O1 | **Reconciliar** | ¿Qué tendría que ser verdad para que **todos** tengan razón? | Contradicción | El cilindro (1) | Quimeras que nadie produce |
| O2 | **Gemelo observacional** | ¿Qué **otra** cosa produciría **exactamente** lo mismo? | Ajuste demasiado bueno | Ada y el bicilindro (3), el tapón (2) | Gemelos rebuscados sin fin |
| O3 | **Explicar la coincidencia** | ¿Por qué coinciden **estos** dos valores? | Coincidencia | Olga y Sara (EXP-014), Wegener | Ver causas en el azar |
| O4 | **Sospechar del instrumento** | ¿Y si el error está en **cómo** se mira? | Contradicción, residuo | La lámpara torcida (5); los neutrinos "más rápidos que la luz" de OPERA (2011), que eran un cable de fibra mal conectado | Culpar al observador para salvar la hipótesis |
| O5 | **Sospechar de la ley** | ¿Y si la regla que liga las observaciones es falsa? | Contradicción persistente | Vulcano, y el perihelio de Mercurio explicado por la relatividad | Abandonar leyes buenas por una anomalía |
| O6 | **Entidad oculta** | ¿Qué cosa **no vista** produciría la anomalía? | Residuo | Neptuno | Vulcanos: entidades que nunca aparecen |
| O7 | **Motivo del observador** | ¿Qué sabe o qué gana quien reporta esto? | Regularidad sin mecanismo | El fondo que vende porque sabe (6) | Conspiraciones |
| O8 | **Selección** | ¿Qué hizo que viéramos **justo estos** casos? | Ajuste demasiado bueno, regularidad | Los aviones de Wald: reforzar donde **no** volvían con agujeros | Negar todo patrón real |
| O9 | **Causa común** | ¿Hay un tercero que produce ambas cosas? | Coincidencia, regularidad | La bomba de Broad Street (Snow, 1854) | Terceros inventados |
| O10 | **Invertir la causalidad** | ¿Y si el efecto produce la causa? | Regularidad | La reflexividad de los mercados (6) | Circularidad |
| O11 | **Cambiar de instrumento** | ¿Qué tipo de observación vería lo que ninguna ve? | Pregunta sin resolver | La balanza (8); el núcleo terrestre de Lehmann (1936), deducido de sombras sísmicas | Proponer instrumentos imposibles |
| O12 | **Ausencia significativa** | ¿Qué debería estar y no está? | Ausencia | El perro que no ladró | Leer demasiado en lo que falta |
| O13 | **Composición** | ¿Y si son varias causas sumadas? | Residuo, ajuste parcial | La acción que cae (6) | La compuesta que siempre gana (A22) |
| O14 | **Tiempo** | ¿Y si no fue simultáneo, o el objeto cambió? | Contradicción | Las lámparas encendidas a la vez (7); el objeto que gira | Historias de cambio sin evidencia |

**Este catálogo es inicial.** Su fuente son ocho historias y algunos casos célebres, y está sujeto a lo mismo que todo lo demás: un operador entra cuando un escenario lo exige y sale cuando no produce nada que la selección acepte.

## 17.6 Qué separa lo no obvio de lo rebuscado

Un operador produce hipótesis improbables a propósito. Sin un filtro, eso sería una fábrica de conspiraciones. **El filtro ya existe, y es lo que se construyó hasta ahora:**

- **Puntuación predictiva** ([EXP-015](../bitacora/EXP-015-puntuacion-predictiva-en-el-motor.md)). La explicación no obvia tiene que hacer que los hechos sean "cosa corriente": predecirlos, explicar las coincidencias, prohibir algo (A24). Merlín y las conspiraciones fallan aquí.
- **Prior de entidades nuevas.** Una entidad postulada paga (A5, A16). Neptuno pagó y ganó; Vulcano pagó y perdió.
- **La observación que separa** (A3, A15, A23). Cada hipótesis no obvia debe decir qué la confirmaría y qué la refutaría. El valor de proponerla depende de lo barato que sea esa prueba: es la "economía de la investigación" de Peirce.

Se definen tres medidas de una hipótesis:

| Medida | Definición | Qué busca |
|---|---|---|
| **Novedad** | $-\log p_G(H \mid F, q_0)$, en la práctica: no estaba entre lo que la generación libre propuso | Que no sea lo obvio |
| **Valor explicativo** | Su puntuación predictiva | Que no sea rebuscada |
| **Costo de prueba** | Qué observación la separa de sus rivales y cuánto cuesta | Que valga la pena seguirla |

## 17.7 Cómo se mide

La pregunta deja de ser "¿acierta la etiqueta?" y pasa a ser:

> **Cuando la explicación verdadera no es la obvia, ¿aparece entre las candidatas?**

- **Casos:** aquellos donde la explicación verdadera **no** está entre lo que el generador libre propone. Así, "no obvia" queda definida operativamente respecto de una línea base, no por mi opinión.
- **Comparación justa:** el mismo modelo con el mismo número de llamadas. De un lado, generación libre con N muestras; del otro, generación guiada por operadores con N llamadas.
- **Métricas:**
  1. *Recuperación:* ¿la verdadera aparece entre las candidatas? La compara un juez independiente con la resolución documentada.
  2. *Novedad útil:* fracción de candidatas que la generación libre no propuso y que sobreviven a la puntuación predictiva.
  3. *Costo en pistas falsas:* cuántas candidatas rebuscadas produce cada operador.
- **Bancos:**
  - **las salas**, con proyección exacta: bicilindro, tapón, cubo hueco y lámpara son verdades no obvias, y la verificación no depende de un LLM;
  - **el conjunto R**, casos posteriores a mayo de 2026 que el modelo no puede recordar;
  - **las perturbaciones P de abd-bench**.
- **Qué falsaría la tesis:** con igual cómputo, la generación guiada por operadores no recupera más verdades no obvias que la libre, o las recupera solo a costa de muchas más pistas falsas.

## 17.8 Qué pasa con lo construido

Nada se tira. Cambia su lugar en el ciclo:

```text
disparador ──► operadores ──► hipótesis no obvias ──► filtro ──► observación que separa ──► registro
 (17.4)          (17.5)          (familias)            (17.6)       (A3, A15, A23)         (P3, A9)
```

| Pieza existente | Nuevo papel |
|---|---|
| Postulados y principios (02, 16) | Siguen siendo la epistemología: mediación, ley, riesgo, subdeterminación, pregunta y contacto |
| Expansión ontológica (postulado 3) | Pasa a ser **un** operador (O6), y se dispara también por ajuste demasiado bueno |
| Consiliencia y puntuación predictiva (04, EXP-015) | El **filtro**: separan lo no obvio de lo rebuscado |
| Verificación, derrota, sugerencia de observación | La **prueba** de la conjetura |
| Selección holística (ADR-0016) | Sigue disponible donde no hay proyección |
| Predicciones, verdad, registro (11, 12, historia 4) | Dicen, con el tiempo, **qué operadores** producen conjeturas que resultan ciertas |
| Experimentos mentales | Fuente de operadores y de escenarios de prueba |
| abd-bench, conjunto R | Bancos para medir la recuperación de verdades no obvias |

**El último punto es nuevo.** El registro de predicciones resueltas, que antes servía para calificar jueces, sirve también para **calificar operadores**: cuáles producen conjeturas que después se confirman y en qué dominios. A largo plazo, eso es lo más parecido a que el sistema **aprenda a pensar abductivamente**.

## 17.9 Antecedentes

Ninguna de las piezas es nueva. Hay que revisarlas antes de construir:

- **Heurísticas de descubrimiento:** Pólya (*Cómo plantear y resolver problemas*); los 40 principios inventivos de TRIZ (Altshuller), que son un catálogo de operadores para inventar; Lakatos (heurística positiva y negativa); Hanson (*Patrones de descubrimiento*).
- **Descubrimiento científico computacional:** BACON (Langley, Simon y colaboradores); la filosofía computacional de la ciencia de Thagard.
- **Técnicas recientes para hacer preguntar distinto a un LLM:** retroceder a la pregunta general antes de responder (*step-back prompting*, Zheng y colaboradores, 2023); componer una estructura de razonamiento a partir de módulos (*Self-Discover*, Zhou y colaboradores, 2024); el razonamiento por analogía.
- **Abducción y generación de hipótesis con LLM:** pendiente de la investigación de literatura ([prompt 3](../investigacion/prompt-deep-research-3-literatura-relacionada.md)). Conviene agregarle una pregunta específica sobre operadores y diversidad de hipótesis.

**Lo que podría ser propio:** un catálogo de operadores **anclado en disparadores**, con un **filtro predictivo** que separa lo no obvio de lo rebuscado, y una **calificación de operadores** por resultados resueltos. Hay que verificarlo.

## 17.10 Próximos pasos acordados

1. **Alinear la documentación:** 01, el README, 16, el glosario y la hoja de ruta.
2. **Escenarios:** un experimento mental por operador o grupo de operadores, con el mismo método que las historias 1 a 8, incluida la lectura ciega. Cada escenario debe poder mostrar que el operador **no** ayuda.
3. **Plan del MCP:** qué herramientas cambian y cuáles se agregan (disparadores, operadores, generación guiada, medición de novedad).
