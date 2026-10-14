# EXP-012 — abd-bench v2: perturbaciones y casos sin respuesta posible

- **Fecha:** 2026-10-14 · **Estado:** registrado (expectativas escritas antes de construir los casos y correr)
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

## Resultado
*(pendiente)*
