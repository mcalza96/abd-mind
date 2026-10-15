# Historia 4 — El sobre cerrado

## Escena

Ya no hay una sala, sino **veinte**, y en cada una hay un objeto distinto. En todas pasa lo de la historia 2: las ventanas del frente y del techo muestran sombras que **dos** objetos explican por igual, y la ventana del costado decide.

Dos investigadoras, **Ana** y **Berta**, recorren las veinte salas con la misma información:

- **Ana**, antes de abrir la ventana del costado, escribe en un **sobre cerrado** qué sombra cree que verá. Lo firma y lo entrega a un notario.
- **Berta** abre la ventana, mira y explica: "claro, era de esperar, por esto y esto".

Al terminar, Berta "acertó" en las veinte. Los sobres de Ana acertaron en catorce.

En la sala veintiuno, **la ventana del costado está tapiada**, y alguien tiene que decidir qué hay adentro.

## La pregunta

¿A quién le preguntas en la sala veintiuno? ¿Qué compró el sobre?

## El motor, paso a paso

En cada sala:

1. `crear_caso` y las dos hipótesis, como en la historia 2.
2. `mejor_explicacion`: empate. El motor registra las predicciones de cada hipótesis para la ventana del costado (`que_vigilar`).
3. Se abre la ventana: `nueva_evidencia`. Una hipótesis queda derrotada.
4. `cerrar_caso` con la verdad.

El motor guarda **qué predijo cada hipótesis**. Lo que **no** guarda es qué apostó **cada juez** antes de mirar, y por lo tanto no puede calificarlos al final.

## Dónde se rompe

1. **El sobre no hizo acertar a Ana en ninguna sala.** En cada sala, la ventana dio la misma respuesta con sobre y sin sobre. El sobre no agrega conocimiento al caso. Esto confirma la crítica de la evaluación externa: el compromiso previo no mejora por sí solo el acierto de quien predice.
2. **Lo que compró el sobre es saber en quién confiar.** El veinte de veinte de Berta no informa nada: explicar después siempre "acierta". El catorce de veinte de Ana es la **única** información sobre la calidad de un juicio cuando falta la ventana. En la sala veintiuno, el sobre es lo único que separa a Ana de una moneda.
3. **Catorce de veinte es casi nada.** Con dos rivales por sala, el azar acierta diez de veinte. Catorce o más le sale a una moneda alrededor de 6 de cada 100 veces. Veinte salas no alcanzan para distinguir con seguridad a Ana del azar. Hacen falta muchos casos: es el problema de potencia que señaló la evaluación externa, ahora a la vista.
4. **El sobre se puede hacer trampa.** Si Ana escribe sobre solo cuando está segura, su porcentaje se infla. El compromiso tiene que ser **en todas las salas**, con su grado de confianza, incluso "no sé, cincuenta y cincuenta". Así funciona la puntuación de Brier.
5. **Las salas tienen que ser independientes.** Si las veinte salas salieron de la misma fábrica, acertar en una casi garantiza acertar en las demás, y los veinte casos valen como pocos.
6. **El motor tiene el sobre, pero no el notario.** `que_vigilar` registra predicciones de **hipótesis**, no apuestas fechadas de **jueces** ni de fuentes. No existe una cuenta acumulada de quién acertó.

## Principio

- **A9 — El compromiso previo no hace acertar en un caso: produce el registro para saber en quién confiar.** Su valor aparece entre casos, no dentro de uno, y solo cuando falta la ventana que decide.
- **A10 — El registro sirve solo si es completo, graduado e independiente.** Hay que apostar en todos los casos (no elegir cuáles), con un grado de confianza, y sobre casos que no se copian entre sí. Y hacen falta muchos.

## Cómo se pondría a prueba

- **Componente que falta:** un registro de apuestas por juez (modelo, prompt, persona, fuente), fechado antes de la resolución, con puntuación de Brier acumulada.
- **Prueba:** muchos casos con resolución conocida después. Primero salas sintéticas, que se resuelven al instante; después casos reales con fecha. Se mide si elegir al juez según su registro mejora las decisiones en los casos **sin** ventana, frente a elegirlo al azar o por fama.
- **Cálculo previo:** cuántos casos hacen falta para separar un 70 % de acierto del 50 % del azar con una seguridad razonable. Se fija antes de correr.

## Lectura ciega (2026-10-15)

El agente sin contexto coincidió: preguntarle a Ana, porque es la única cuyo método se midió, y 14 de 20 no es significativo (p ≈ 0,058). Agregó cuatro puntos, uno de ellos grave para el diseño del motor:

1. **El motor se comporta como Berta.** Ante un empate no decide, así que nunca se juega, nunca acumula historial y nunca puede ser calificado. Peor todavía:
   - la expansión ("genera algo que lo explique todo") es exactamente el procedimiento de Berta;
   - el juez que ve todo junto racionaliza si la observación decisiva ya entró.
2. **Tensión entre A3 y A9.** Abstenerse de decidir es correcto (A3). Abstenerse de apostar impide el registro (A9). La salida es separarlas: **el motor puede no decidir, pero siempre declara probabilidades antes de mirar**.
3. **Lo que mide el sobre de Ana es su prior, no su abducción.** Con dos objetos igual de compatibles, Ana desempata por lo que cree frecuente. Además, la línea base justa no es la moneda: si un objeto aparece en el 70 % de las salas, apostar siempre a él también da 14 de 20.
4. **Berta también debería sellar sobres**, y la sala 21 tiene que venir de la misma población que las veinte anteriores. Si no, el registro no se traslada.

**Ajuste de A10:** el registro se compara contra la tasa base (apostar siempre a lo más frecuente), no contra el azar.
