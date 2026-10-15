# Experimentos mentales

Historias concretas para construir la teoría **desde abajo**: de la situación al principio, no al revés. Cuando un principio se escribe primero y después se ilustra, el caso se elige para que el principio quede bien. Cuando la historia va primero, obliga a aceptar un principio, o muestra dónde falla el sentido común (y el nuestro).

Origen: conversación del 2026-10-15, después del [documento 15](../marco-teorico/15-forma-y-material.md). El caso del cilindro aclaró más que cualquier formalización; la idea es repetir ese ejercicio.

## Método

Cada historia tiene la misma estructura:

1. **Escena:** un mundo mínimo con una **verdad oculta que conoce el narrador**. La verdad está fijada por construcción, no es una etiqueta de un modelo (12 §12.2).
2. **Personajes con instrumentos explícitos:** qué ve cada uno y por qué.
3. **La pregunta.**
4. **El motor, paso a paso:** la historia ejecutada a mano con las herramientas reales del servidor MCP (`crear_caso`, `proponer_hipotesis`, `mejor_explicacion`, `sugerir_observacion`…).
5. **Dónde se rompe:** el momento en que el motor, el LLM o nuestra intuición se equivocan.
6. **El principio que la historia obliga a aceptar.** Va a [axiomas.md](axiomas.md) citando la historia.
7. **Cómo se pondría a prueba de verdad.**

## Reglas

1. **Un axioma entra solo si una historia lo exige.** Los postulados del [documento 02](../marco-teorico/02-postulados.md) se vuelven a derivar; los que ninguna historia exija quedan marcados como pendientes.
2. **Cada historia tiene que poder avergonzarnos.** Si en todas el motor sale bien parado, están mal elegidas.
3. **Lectura ciega:** un agente sin contexto lee la escena y la pregunta y dice qué se rompe **antes** de ver nuestro análisis. Su lectura queda registrada al final de la historia.
4. **Todas ocurren en el mismo mundo**, la sala del cilindro, que se complica de a poco. Así cada principio nuevo se apoya en los anteriores.

## La sala

Una sala cerrada con un objeto sólido. Hay ventanas en el techo, al frente y al costado, perpendiculares entre sí. Por cada ventana, una lámpara proyecta la **silueta** del objeto sobre una pantalla. Quien mira por una ventana ve solo esa silueta. Nadie entra a la sala.

## Índice

| # | Historia | Principio que fuerza | Estado |
|---|---|---|---|
| 1 | [El cilindro](01-el-cilindro.md) | Nadie ve el objeto; el desacuerdo entre sombras es información | escrita |
| 2 | [La ventana que nadie abrió](02-la-ventana-que-nadie-abrio.md) | Cuando varias explicaciones dan cuenta de todo, razonar más no decide | escrita |
| 3 | [Los cien jueces](03-los-cien-jueces.md) | El acuerdo entre jueces de igual formación no es evidencia; explicar todo no significa que no haya rivales | escrita |
| 4 | [El sobre cerrado](04-el-sobre-cerrado.md) | El compromiso previo no hace acertar en un caso: produce el registro para saber en quién confiar | escrita |
| 5 | [La lámpara torcida](05-la-lampara-torcida.md) | Ante una contradicción hay tres sospechosos: instrumento, ley y objeto; las hipótesis auxiliares tienen que pagar | escrita |
| 6 | [La acción que cae](06-la-accion-que-cae.md) | Fuera de la sala casi no hay leyes ni ventanas independientes; lo que sobrevive es disciplina, no ventaja | escrita |
| 7 | El objeto que cambia según quién mira | Una hipótesis infalsable tiene consiliencia máxima: ¿qué la descarta? | pendiente (propuesta en la lectura ciega) |
| 8 | El hueco interior | Una pregunta que ninguna ventana resuelve: el motor debe decirlo, no sugerir qué mirar | pendiente (propuesta en la lectura ciega) |

La historia 5 tiene ahora una forma concreta, propuesta por la lectura ciega: Tomás reporta "círculo", pero su ventana está oblicua y en realidad ve una elipse. Ninguna hipótesis explica todo, así que el motor expande y premia una forma monstruosa que acomoda el error, en vez de dudar del dato.
