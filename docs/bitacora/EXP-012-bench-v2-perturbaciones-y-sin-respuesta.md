# EXP-012 — abd-bench v2: perturbaciones y casos sin respuesta posible

- **Fecha:** 2026-10-14 · **Estado:** corrido
- **Registro previo:** sí
- **Origen:** [EXP-007](EXP-007-bench-linea-base.md). La línea base acierta alrededor de 80 % en la pregunta del tipo de causa; ese banco no distingue el motor de un LLM.

## Pregunta

¿El motor hace algo que la línea base no hace? Concretamente:

1. Cambiar la respuesta cuando cambia un hecho decisivo.
2. Abstenerse cuando la evidencia no alcanza.

## Diseño

Casos nuevos derivados de las variantes V01 a V10. Su verdad es por construcción y su contaminación, baja. Los escribe el asistente, con la circularidad declarada en 12 §12.5.

- **Serie P (perturbación):** el mismo caso con uno o dos hechos decisivos cambiados para que el tipo de causa correcto cambie. Son 8, porque V07 y V09 no admiten una perturbación limpia que cambie el tipo.
- **Serie U (sin respuesta posible):** el mismo caso sin los hechos que discriminan, de modo que al menos dos tipos de causa quedan igual de sostenidos. Son 10. La respuesta correcta es **abstenerse**.
- **Lo que se mide:**
  - **Motor:** se abstiene si su respuesta queda sin determinar.
  - **Línea base:** recibe en **todos** los casos la opción explícita `indeterminado`, para no compararla en desventaja. Por eso se vuelve a correr también sobre los 20 casos de pares, porque la opción nueva puede cambiar sus resultados.

## Expectativa (antes de correr)

| Id | Expectativa | Fracaso de la hipótesis "el motor aporta algo" si… |
|---|---|---|
| F1 | **U:** el motor se abstiene en al menos 6 de 10 | El motor se abstiene en menos de 4 de 10 |
| F2 | **U:** la línea base se abstiene en 3 de 10 o menos, aunque tenga la opción | La línea base se abstiene tanto o más que el motor |
| F3 | **P:** el motor acierta al menos 5 de 8 | El motor acierta menos que la mejor línea base |
| F4 | **Pares:** el motor se abstiene en 6 de 20 o menos (no se abstiene por sistema) | Más de 8 de 20 |
| F5 | Las respuestas firmes del motor (determinadas y no frágiles) aciertan más que las frágiles | Las frágiles aciertan igual o más |

Si F1 y F2 se cumplen y F4 no fracasa, el motor aporta saber cuándo no sabe. Si no, se registra que en estos casos no aporta.

**Configuración fijada:** la de `config/abd-mind.example.yaml` al momento de correr. Línea base: Muse 1.3 (con Muse 1.2 de respaldo) y DeepSeek.

## Nota agregada antes de correr (después de EXP-010)

EXP-010 mostró que la etiqueta del tipo de causa es ambigua: el motor puede elegir el mecanismo correcto con otra etiqueta. Para las series V y P se guardan y se revisan los mecanismos elegidos, y los errores se clasifican en "de etiqueta" o "de razonamiento". F1 y F2, que miden la abstención en U, no dependen de la etiqueta. Las expectativas no cambian.

## Resultado

**Corrida:** `--casos v2 --paralelo 5`, 28 casos (8 P, 10 U, 10 V), unos 45 minutos sin incidentes. Resultados en `datasets/abd-bench/resultados/2026-10-14-exp012/`.

| | Motor | Muse 1.3 | DeepSeek |
|---|---|---|---|
| Variantes (V) correctas | 3/10 | 9/10 | 6/10 |
| Perturbaciones (P) correctas | 5/8 | 7/8 | 4/8 |
| Sin respuesta (U): se abstiene | 1/10 | 2/10 | 1/10 |
| Falsas abstenciones en casos con respuesta | 2/18 | 0/18 | 0/18 |

| Id | Resultado | ¿Se cumple? |
|---|---|---|
| F1 | El motor se abstiene en 1 de 10 casos U | ❌ (umbral de fracaso: menos de 4) |
| F2 | La línea base se abstiene poco (Muse 2, DeepSeek 1), pero Muse se abstiene más que el motor | ❌ (la condición de fracaso se cumple) |
| F3 | El motor acierta 5 de 8 en P, frente a 7 de 8 de Muse | ❌ (por debajo de la mejor línea base) |
| F4 | 2 falsas abstenciones de 18 | ✅ |
| F5 | Firmes correctas 2 de 3; frágiles correctas 6 de 13 | ✅ en dirección, pero con muy pocos casos |

**Veredicto registrado:** en estos casos el motor **no** aporta saber cuándo no sabe. La hipótesis que motivó EXP-012 fracasa.

## Sorpresas y errores

- **Casi todo es frágil.** El motor decide con margen de 1 veredicto en 21 de 26 decisiones, tanto en casos con respuesta como sin ella. La fragilidad no separa los casos que se pueden responder de los que no. Si "frágil" contara como abstención, el motor se abstendría en 9 de 10 U, pero también en 13 de 16 casos con respuesta.
- **Inestabilidad.** El motor responde distinto que en EXP-010 en varias variantes (V06, V09, V10). Los mismos casos dan resultados distintos entre corridas: el resultado depende del camino que toma la generación.
- **La perturbación sí la sigue cuando acierta.** P04, P06, P08 y P10 aciertan aunque su variante original fallara: el motor no repite la respuesta del caso de origen. La línea base también los acierta.

## Lecciones (interpretación hecha después de ver los resultados)

1. **La suma por observación pierde las relaciones entre hechos.** El score suma juicios de cada observación por separado: supone, en la práctica, evidencia independiente. Muchas abducciones dependen de **patrones entre hechos**, como el intercambio de etiquetas que solo tiene sentido junto con la cata ciega, o las excepciones del mapa del cólera. Un LLM que ve todo junto los capta; el motor, al descomponer, los pierde. Es una hipótesis de trabajo y hay que registrarla y probarla, no darla por cierta.
2. **Con verificación LLM, las diferencias de score son del orden de un veredicto.** Los empates casi exactos son la norma, y el resultado depende del ruido de cada juicio. La abstención por δ = 10⁻⁶ nunca se activa; la fragilidad se activa casi siempre. Ninguna de las dos es una señal útil.
3. **En dominios abiertos, el motor actual rinde por debajo de un LLM en una sola llamada en todo lo medido:** precisión, seguimiento de la evidencia y abstención. Su valor demostrado sigue limitado al dominio con proyección exacta, más la auditoría y la derrotabilidad, que no se midieron aquí.

## Decisiones derivadas

Pendientes de discutir con el usuario: es una decisión de rumbo, no de parámetros.
