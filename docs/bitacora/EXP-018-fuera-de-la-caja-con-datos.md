# EXP-018 — ¿El agente tiene el hábito de no quedarse con la respuesta promedio?

- **Fecha:** 2026-10-15 · **Estado:** registrado
- **Registro previo:** sí. Este commit va antes de construir los casos y de correr.
- **Origen:** la revisión de EXP-017 con el usuario. El oráculo medía si el agente sabe investigar, no si piensa fuera de la caja. **Objetivo, en palabras del usuario:** "que mis agentes no promedien respuestas, sino que tengan el hábito de pensar fuera de la caja". Fuente de casos elegida: datos con una causa no obvia plantada (opción b).

## Pregunta

Un agente con sus herramientas reales (código, archivos y, si las tiene, otras), que recibe una pregunta normal sobre unos datos, sin que se le pida pensar distinto:

1. ¿llega a una causa que **no** es la que daría un modelo respondiendo de una vez (la respuesta promedio)?
2. ¿lo hace sin volverse rebuscado cuando la respuesta obvia es la correcta?
3. ¿la skill y el MCP abd-mind forman ese hábito?

## Lo que dicen los experimentos anteriores (y orienta el diseño)

- En EXP-016, la causa verdadera aparecía casi siempre entre las cinco primeras candidatas cuando los hechos apuntaban a ella. El fallo estaba en **elegir**: quedarse con la candidata común, atender a la sorpresa equivocada o preferir un mecanismo físico a una decisión humana. El hábito que buscamos es, sobre todo, **no cerrar en lo obvio sin comprobar la rival**.
- En EXP-017, el agente llegó a causas que ningún modelo había encontrado razonando, porque fue a mirar (P6). Además, **no usó el MCP por iniciativa propia**. Por eso aquí el mensaje es natural y se mide la espontaneidad.

## Diseño

### 1. Casos (construidos por un agente sin contexto)

Un agente que no conoce el marco teórico ni los operadores de abd-mind construye **12 casos**. Cada caso tiene:

- **una pregunta realista** de alguien que pide ayuda, por ejemplo: "¿por qué cayeron las ventas en marzo?";
- **archivos de datos** (CSV y, si corresponde, registros de texto), generados por un script con semilla fija;
- **una causa verdadera plantada en los datos**, con una huella comprobable en ellos;
- **un señuelo**: la causa obvia que los datos apoyan a primera vista.

Del total:

- **9 casos "no obvios":** la causa obvia es falsa o incompleta;
- **3 casos de control:** la causa obvia es la verdadera. Sirven para medir lo rebuscado.

El constructor elige las causas en distintos dominios (comercio, operaciones, salud, educación, tráfico web, manufactura, finanzas, entre otros) y en distintos tipos (decisiones humanas, artefactos de medición, selección, cambios de régimen, interacciones, entre otros). **No** recibe la lista de operadores, para no ajustar los casos a nuestro método. Las preguntas no deben insinuar la respuesta.

**Secreto de la clave.** Los agentes pueden leer archivos, así que ni la clave ni los scripts generadores entran al repositorio antes de terminar las corridas. Se sube solo:

- la carpeta de cada caso, con la pregunta y los datos;
- el **SHA-256** de la clave y de los scripts, como compromiso de que no cambian después.

La clave y los scripts quedan con el usuario y se suben al terminar.

### 2. Comprobaciones de los casos (antes de cualquier corrida)

- **Huella:** un script independiente comprueba que la causa plantada se detecta en los datos con un análisis razonable.
- **Respuesta promedio:** DeepSeek recibe 10 veces, en una sola llamada y sin herramientas, la pregunta, la descripción de las columnas y las primeras 20 filas de cada archivo. Un agente sin contexto agrupa las 10 respuestas. Las causas que aparecen en 3 o más de las 10 forman la **respuesta promedio** del caso.
- **Filtro, fijado aquí:**
  - un caso no obvio en el que la causa verdadera esté en la respuesta promedio sale del análisis principal y se informa;
  - un caso de control en el que la causa obvia **no** esté en la respuesta promedio se informa como mal construido.
- Si quedan menos de 6 casos no obvios, se construyen más con el mismo procedimiento antes de correr.

### 3. Condiciones

Las tres usan el mismo modelo en Hermes, en una **sesión nueva y sin memoria** de las anteriores.

| Condición | Skill | MCP abd-mind |
|---|---|---|
| **S0** | Ninguna | No |
| **S1** | `razonamiento-abductivo-sin-mcp` | No |
| **S2** | `razonamiento-abductivo` | Sí |

### 4. Mensaje (el mismo en las tres, natural)

Por cada caso, el usuario envía la pregunta del caso y la ruta de su carpeta, más una sola regla: "Usa solo los archivos de esta carpeta; no busques el caso en internet." **No** se menciona la skill, el método, la creatividad ni las alternativas. Al terminar, el agente responde como respondería a esa persona. Después se le pide, por separado, el registro de herramientas.

### 5. Métricas

Las evalúa un juez ciego a la condición, con la clave y la rúbrica `sí / parcial / no` de EXP-016 aplicada a la causa plantada.

| Métrica | Definición |
|---|---|
| **Primaria: acierto fuera de la caja** | En los casos no obvios, la respuesta identifica la causa plantada (`sí`) |
| **Rebuscado** | En los casos de control, la respuesta rechaza o desplaza la causa obvia (verdadera) por otra con confianza alta. También cuenta, en los casos no obvios, afirmar con seguridad una causa que no es ni la plantada ni el señuelo y que los datos no muestran |
| **Hábito** | Según el registro de herramientas: el agente consideró al menos una causa distinta del señuelo **y la comprobó con los datos**, sin que se le pidiera |
| **Uso del MCP** (solo S2) | Si llamó a abd-mind y en qué momento |

### 6. Reglas de decisión (antes de correr)

Con 9 casos no obvios, solo una diferencia grande cuenta.

| Comparación | Resultado | Lectura |
|---|---|---|
| S1 frente a S0 | S1 acierta **3 o más** casos no obvios más, y no tiene más de 1 caso de control rebuscado adicional | La skill forma el hábito |
| S2 frente a S1 | S2 acierta **3 o más** más, con la misma condición sobre los controles | El MCP aporta además de la skill |
| Cualquiera | Diferencias de 2 o menos | Sin efecto detectable de esa intervención |
| Cualquiera | S1 o S2 aciertan más, pero son rebuscados en 2 o más controles adicionales | No es pensar fuera de la caja: es contrariar por sistema. Se revisa la skill |

**Fracaso del objetivo:** ni S1 ni S2 superan a S0 por 3 o más. En ese caso, nuestras instrucciones y herramientas no forman el hábito, y hay que replantear cómo se lo damos al agente.

**Predicción:** S0 acierta alrededor de 4 de 9, porque analizar datos ya revela algunas huellas; S1, alrededor de 6, y S2, alrededor de 6, porque el agente usará poco el MCP. Los controles salen bien en las tres condiciones.

## Amenazas

- **n pequeño y una corrida por condición:** es un piloto.
- **Casos sintéticos:** pueden tener rastros artificiales que delaten la causa. El constructor debe dar realismo y ruido, y las comprobaciones lo vigilan solo en parte.
- **El constructor es un LLM:** sus causas "no obvias" pueden ser las que a un LLM se le ocurren fácilmente. El filtro de la respuesta promedio lo detecta.
- **Memoria de Hermes:** si el agente recuerda casos o pruebas anteriores, se contamina. Las sesiones deben empezar sin memoria.
- **Un agente diligente** que analice todo exhaustivamente puede encontrar la huella sin pensar distinto. Lo aceptamos: el hábito también se ve en el registro de herramientas.
- **Mismo tipo de modelo** en la respuesta promedio, los agentes y el juez. El juez es de otra familia.

## Resultado

*(pendiente)*

## Nota 2026-10-15: dos condiciones en vez de tres (antes de correr)

A pedido del usuario, que tiene dos agentes Hermes, se corren solo **S0** (sin skill ni MCP) y **S2** (skill y MCP). S1 queda para después.

- **Regla de decisión:** S2 acierta 3 o más casos no obvios más que S0, sin más de 1 caso de control rebuscado adicional → nuestro paquete (skill y MCP juntos) forma el hábito. Si la diferencia es de 2 o menos, no hay efecto detectable.
- **Lo que se pierde:** si S2 gana, no se sabe si es por la skill o por el MCP. Eso lo respondería S1.
- **El usuario envía las preguntas** sin ver la clave, para no insinuar la respuesta.
