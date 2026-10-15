# Historia 2 — La ventana que nadie abrió

## Escena

Misma sala. El objeto es un **tapón universal** (la verdad oculta): un cilindro al que se le cortaron dos cuñas con planos inclinados, de modo que de costado se ve un triángulo. Es el sólido que pasa justo por un agujero redondo, uno cuadrado y uno triangular.

| Personaje | Ventana | Ve |
|---|---|---|
| Olga | Frente | un cuadrado |
| Tomás | Techo | un círculo |
| — | Costado | **nadie la ha abierto**: abrirla cuesta (hay que pagarle a la guardia) |

Hay dos clientes:

- **Clara** quiere encargar una **caja** para guardar el objeto y necesita saber sus medidas exteriores.
- **Marcos** quiere saber **cuánto material** tiene el objeto, porque lo va a fundir.

## La pregunta

¿Qué hay en la sala? Y la que importa de verdad: ¿qué le respondemos a Clara y qué a Marcos?

## El motor, paso a paso

1. `crear_caso` con las observaciones de Olga y Tomás.
2. `proponer_hipotesis`: **cilindro** (de altura igual al diámetro) y **tapón universal**. Supongamos que alguien propuso los dos.
3. `evaluar`: ambos producen un cuadrado de frente y un círculo desde arriba. C = 2 para los dos, misma parsimonia, misma coherencia. **Empate exacto.**
4. `mejor_explicacion` sin pregunta: no hay ganador, la respuesta queda sin determinar.
5. `sugerir_observacion`: el motor calcula qué ventana separa a las dos. **El costado**: el cilindro predice un cuadrado y el tapón, un triángulo.

Con pregunta (ADR-0012), cambia todo:

- **Pregunta de Clara** (*medidas exteriores de la caja*): las dos hipótesis predicen la misma caja, un cubo del lado del diámetro. La respuesta queda **determinada sin abrir la ventana**. `sugerir_observacion` responde que no hace falta discriminar.
- **Pregunta de Marcos** (*volumen*): el cilindro tiene más material que el tapón. La respuesta **no** queda determinada, y la ventana del costado pasa a valer lo que cuesta.

## Dónde se rompe

1. **El juez de un dominio abierto no empata.** En el dominio con proyección exacta, el motor declara el empate y pide la ventana. Un LLM que juzga ([EXP-013](../bitacora/EXP-013-seleccion-holistica.md)) casi siempre elige: "cilindro", porque es lo que más se ve en el mundo. Esa elección no sale de la evidencia: sale de la **frecuencia** con que aparecen cilindros en sus textos. Es una apuesta razonable, pero se presenta como una conclusión. En EXP-013 el juez se abstuvo solo en 3 de 10 casos que lo exigían.
2. **La frecuencia es inducción, no abducción.** Cuando la evidencia empata, decidir por "lo más común" es legítimo como **apuesta declarada**. Hoy el motor no tiene dónde declararla: ni la puntuación ni el juicio distinguen "lo vi" de "suele ser así".
3. **El motor ignora el costo de mirar.** `sugerir_observacion` dice qué ventana separa, pero no si vale la pena abrirla. Con Clara no vale nada, y lo resuelve la pregunta. Con Marcos depende de cuánto cuesta equivocarse con el metal frente a cuánto cuesta la guardia. Eso no está en el motor.
4. **Nuestra intuición.** Habría jurado que el empate es un defecto que hay que romper. La historia de Clara muestra que, a veces, el empate es la respuesta correcta y no importa.

## Principio

- **A3 — Empate empírico.** Cuando varias explicaciones dan cuenta de todo lo visto, razonar más no decide. Decide una observación en la que sus predicciones difieran.
- **A4 — La pregunta decide qué diferencia importa.** Un empate entre explicaciones solo es un problema si las explicaciones empatadas responden distinto a la pregunta. La ventana vale según lo que cambia en la respuesta y lo que cuesta abrirla.
- **A5 — La frecuencia es una apuesta, no una conclusión.** Lo que se use para elegir dentro de un empate (frecuencia, simplicidad, costumbre) debe quedar registrado como apuesta, separado de lo que dijo la evidencia.

## Cómo se pondría a prueba

- **Hoy:** en la serie U de abd-bench, contar cuántas veces el juez elige sin declarar que su elección vino de la frecuencia y no de la evidencia.
- **Construible:** salas sintéticas con objetos que comparten dos sombras. Se mide si el motor (a) se abstiene, (b) pide la ventana correcta, (c) no la pide cuando la pregunta no lo requiere.

## Lectura ciega (2026-10-15)

Un agente sin contexto leyó solo la escena y la pregunta. Coincidió en lo central: Clara queda resuelta sin la ventana, Marcos no, y el motor ignora el costo de mirar. Agregó tres cosas que la historia no veía:

1. **No son dos objetos, son infinitos.** Con un cuadrado de frente y un círculo arriba, también calzan el bicilindro (historia 3), un disco unido a una placa delgada y cualquier objeto con huecos interiores. La historia presenta un duelo cuando el conjunto compatible es enorme.
2. **"Determinada" significa "igual entre las hipótesis propuestas", no "igual entre todo lo compatible con lo visto".** Para Clara da lo mismo: las dos sombras fijan el cubo que contiene al objeto, sea cual sea. Para Marcos es grave: incluso con la ventana del costado abierta, un hueco interior no lo ve nadie, y el motor diría que el volumen está determinado.
3. **Lo que sí se puede decir sin elegir hipótesis.** A Marcos se le puede dar un tope: el objeto no tiene más material que el cilindro. Hay respuestas que salen de todo el conjunto compatible, sin pasar por la lista de candidatas.

Detalles menores: el triángulo del tapón es isósceles, no equilátero; la historia supone proyección paralela y un objeto alineado con las ventanas; las siluetas dan proporciones, no tamaño.

**Corrección de A4:** que una respuesta esté determinada depende de **todo lo compatible con lo visto**, no de las hipótesis que alguien propuso. Antes de comparar candidatas, hay que preguntar de qué depende la respuesta.
