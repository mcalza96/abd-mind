# EXP-017 — ¿El MCP ayuda a un agente a pensar abductivamente? (A/B con dos Hermes)

- **Fecha:** 2026-10-15 · **Estado:** cerrado (parcial)
- **Registro previo:** sí. Este commit va antes de preparar los hallazgos ocultos y de correr.
- **Origen:** la evaluación de alineación del 2026-10-15. Todos los experimentos anteriores midieron el motor contra un LLM en una sola llamada sobre texto cerrado; el objetivo es otro: **un agente con herramientas que investiga**. Decisiones del usuario: casos resueltos y abiertos (1c); el control recibe el mismo método sin herramientas (2b).

## Pregunta

Un agente Hermes con el MCP abd-mind, frente al mismo agente con las mismas instrucciones de método pero sin el MCP: ¿llega más veces a la causa, pide mejores observaciones, cierra menos veces antes de tiempo y está mejor calibrado?

## Condiciones

| | Agente A (con MCP) | Agente B (control) |
|---|---|---|
| Modelo de Hermes | El mismo en ambos. El usuario lo confirma antes de correr | Igual |
| Instrucciones de método | Skill `razonamiento-abductivo` (con herramientas) | Skill `razonamiento-abductivo-sin-mcp`: el mismo método, con las acciones hechas a mano |
| MCP abd-mind | Sí | No |
| MCP oráculo (abajo) | Sí | Sí |
| Búsqueda web y lectura de archivos del repositorio | **Desactivadas o prohibidas** durante la prueba | Igual |

## Parte rápida: casos resueltos, con oráculo

**Casos:** los 11 casos R que quedaron de [EXP-016](EXP-016-recuperacion-en-casos-reales.md), con sus observaciones saneadas de la época.

**Hallazgos ocultos.** Para cada caso, un agente sin contexto escribe de 3 a 6 **hallazgos** a partir de la resolución. Cada hallazgo es una **observación**, no una conclusión: lo que mostraría un registro, una inspección, un ensayo o una entrevista concretos. Por ejemplo: "los registros de control muestran que las dos válvulas de aislación del horno 5 se abrieron con 2 segundos de diferencia". Se agregan además 2 hallazgos **irrelevantes pero verdaderos** por caso, para que pedir de todo no sea gratis.

**El oráculo** es un servidor MCP neutral (`abd-mind oraculo`) con tres herramientas:

| Herramienta | Qué hace |
|---|---|
| `ver_caso` | Entrega los hechos de la época |
| `pedir_observacion(caso, que_mirar)` | Devuelve los hallazgos que responden **a esa observación concreta**, o "no hay información sobre eso". Una pregunta por la causa ("¿qué pasó?") no obtiene nada: hay que pedir qué mirar. Lo decide DeepSeek, sin ver qué agente pregunta. Máximo 8 pedidos por caso |
| `concluir(caso, explicacion, confianza, alternativas)` | Registra la conclusión final, su confianza (0–1) y las rivales que el agente sigue considerando |

Todo queda registrado con su hora.

**Procedimiento.** El usuario envía a cada agente el mismo mensaje: resolver los 11 casos del oráculo uno por uno, sin web ni archivos, pidiendo las observaciones que crea necesarias y concluyendo cada caso.

### Métricas

| Métrica | Definición |
|---|---|
| **Primaria: acierto** | La explicación final cubre el núcleo del mecanismo, según un juez ciego con la rúbrica de EXP-016 y los elementos clave ya fijados |
| Acierto por grupo | Casos principales, y R04 y R10, donde el núcleo **no** es inferible de los hechos iniciales: ahí solo se llega pidiendo observaciones |
| Observaciones útiles | Pedidos que obtuvieron un hallazgo relevante, sobre el total de pedidos |
| Cierre prematuro | Conclusión equivocada con confianza ≥ 0,7 |
| Calibración | Puntaje de Brier de la confianza frente al acierto |
| Apertura | La causa verdadera está entre las alternativas declaradas, cuando la conclusión es otra |

### Reglas de decisión (antes de correr)

Con 11 casos, la diferencia tiene que ser grande para contar.

| Resultado | Lectura |
|---|---|
| A acierta **3 o más casos** más que B y no tiene peor calibración | Indicio de que el MCP aporta **como herramienta**. Se pasa a la parte definitiva |
| La diferencia es de 2 o menos | Sin diferencia detectable: el valor, si existe, está en las instrucciones. Una skill bastaría, y hay que replantear qué hace el MCP |
| B acierta más | El MCP estorba: carga, distrae o ancla. Se revisa antes de seguir |

**Predicción:** A aciertos y B aciertos parecidos en los casos principales. A algo mejor en R04 y R10, porque `sugerir_observacion` empuja a pedir la observación que separa las hipótesis. A mejor calibrado. Diferencia total: alrededor de 2 casos, es decir, **sin diferencia detectable**.

## Parte definitiva: casos abiertos

Son casos cuya respuesta todavía no existe, analizados con web por los dos agentes. Se registran sus conclusiones, su confianza y lo que cada uno dice que hay que vigilar. Se evalúan cuando se resuelvan. Los casos se eligen con el usuario después de la parte rápida, y entonces se agrega a esta entrada un registro previo propio.

## Amenazas

- **n = 11 y una sola corrida por agente:** es un piloto.
- **Lectura de archivos:** el repositorio clonado contiene las resoluciones. Si un agente lee archivos, el resultado se invalida. Se pide revisar los registros de herramientas de Hermes.
- **El oráculo es otro LLM:** puede entregar de más o de menos. Sus decisiones quedan registradas y se revisan.
- **Mismo modelo en todo:** agentes, oráculo y juez son DeepSeek o del mismo tipo. El juez es un agente de otra familia, ciego a la condición.
- **La skill del agente A** todavía dice "el motor decide qué explicación es mejor". Se corrige antes de correr, sin cambiar el método.

## Resultado

*(pendiente)*

## Nota 2026-10-15: cerrado como parcial

Solo corrió el agente A. Desviaciones: el modelo de Hermes fue `muse-spark-1.2-contributor`, no DeepSeek, y **A no llamó a ninguna herramienta de abd-mind**. Hizo 81 pedidos al oráculo; 36 obtuvieron un hallazgo. B y A2 no se corren.

Motivo del cierre: el diseño medía si el agente sabe investigar con un oráculo, no si piensa fuera de la caja, que es el objetivo del usuario. Lo reemplaza [EXP-018](EXP-018-fuera-de-la-caja-con-datos.md).

Dos hallazgos, sin juez ciego y por lo tanto preliminares:

1. **Comprobar resuelve lo que razonar no alcanza.** A llegó a R04 (las válvulas) y a R14 (la tripulación insistió en aterrizar), que ningún modelo encontró en EXP-016, porque pidió mirar los registros. Apoya P6.
2. **El agente no usa el MCP por iniciativa propia**, aunque tenga la skill instalada.

El informe de A no se sube al repositorio, porque trae los hallazgos ocultos del oráculo.
