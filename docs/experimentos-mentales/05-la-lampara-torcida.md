# Historia 5 — La lámpara torcida

## Escena

Misma sala. El objeto es un **cilindro** de eje vertical, de 10 cm de diámetro y 10 cm de alto (la verdad oculta). Esta vez los observadores **miden** las siluetas con una regla sobre la pantalla.

| Personaje | Ventana | Ve |
|---|---|---|
| Olga | Frente | un rectángulo de **10 de ancho** × 10 de alto |
| Sara | Costado | un rectángulo de **10 de ancho** × 10 de alto |
| Tomás | Techo | una **elipse** de 10 de izquierda a derecha × **7** de adelante hacia atrás |

Lo que nadie sabe: **la lámpara del techo está torcida**. Proyecta el círculo en diagonal sobre la pantalla, y una sombra oblicua de un círculo es una elipse. Tomás mide bien lo que ve; lo que ve está deformado. Además, la lámpara siempre estuvo así: si Tomás mira cien veces, ve la misma elipse cien veces.

**La regla de la sala.** El objeto es rígido y las tres miradas son simultáneas. Entonces las sombras **comparten medidas**:
- el ancho que ve Olga es el largo de la sombra del techo de izquierda a derecha;
- el ancho que ve Sara es el largo de la sombra del techo de adelante hacia atrás.

## La pregunta

¿Qué hay en la sala? Y antes de eso: ¿quién se equivocó, si alguien se equivocó?

## El motor, paso a paso

1. `crear_caso` con las tres observaciones y sus medidas. Confiabilidad por defecto: ω = 0,95 para cada uno.
2. `proponer_hipotesis`:
   - **cilindro** de 10 × 10: produce el rectángulo de Olga y el de Sara, pero desde arriba un círculo de 10, no una elipse. **Contradice a Tomás.**
   - **cilindro elíptico** de 10 × 7: produce la elipse de Tomás y el rectángulo de Olga, pero de costado un rectángulo de **7** de ancho, no de 10. **Contradice a Sara.**
3. `evaluar`. **Ningún sólido rígido explica las tres sombras**: la elipse dice "7" de adelante hacia atrás y Sara dice "10". Es una contradicción geométrica, no una diferencia de puntos de vista.
4. Como ninguna hipótesis explica todo, **se dispara la expansión**. El generador propone algo que lo explique todo, por ejemplo **"un objeto que se deforma cuando se lo mira desde arriba"**: explica las tres sombras y postula una entidad nueva.
5. Puntuación con los pesos por defecto (α = 1,5, β = 10, γ = 1, λ = 1; c(ω) = −ln(1 − ω)):

   | Hipótesis | Explica | Contradice | Score |
   |---|---|---|---|
   | Cilindro | Olga, Sara | Tomás (c = 3,0) | 9,85 |
   | Cilindro elíptico | Olga, Tomás | Sara (c = 3,0) | 9,85 |
   | **Objeto que se deforma** | las tres | — (pero P = 1) | **13,27** |

   **Gana el monstruo.** Culpar a un observador cuesta 3,0; inventar una entidad cuesta 1,0.

## Dónde se rompe

1. **El monstruo gana porque la rigidez no está escrita como regla.** Si "el objeto es rígido" fuera una regla dura (K = 0 para quien la viole), el monstruo quedaría descartado sin apelación. Quedarían el cilindro y el cilindro elíptico **empatados**: cada uno culpa a un observador distinto. Ese empate es correcto. La teoría pide reglas duras ([postulado 2](../marco-teorico/02-postulados.md#postulado-2--invariante-causal)), pero si nadie las escribe, el motor premia acomodar el error.

2. **La mayoría es una ilusión.** La intuición dice: "Olga y Sara coinciden, Tomás está solo, el que se equivoca es Tomás". Pero Olga no opina sobre la medida en disputa (de adelante hacia atrás); solo Sara y Tomás la miden. Es **uno contra uno**. Contar observadores en vez de contar evidencias **por medida** fabrica un consenso que no existe. Aquí el principio D11 (la confiabilidad no sale del acuerdo) protege, aunque la intuición proteste.

3. **La reputación decide mal.** Variante: Tomás es un experto famoso (ω = 0,99) y Sara una novata (ω = 0,8). Ahora culpar a Tomás cuesta 4,6 y culpar a Sara 1,6. Gana el cilindro elíptico (11,30 contra 8,02). **El motor se equivoca por respetar el prestigio.** El ω salió de la fama, no de un registro de aciertos (historia 4).

4. **Repetir no detecta el error.** La lámpara torcida no se equivoca al azar: se equivoca siempre igual. Si Tomás mira cien veces, ve cien veces la misma elipse, y su "confiabilidad" parece perfecta. El modelo del motor, ω como probabilidad de un error ocasional, **no representa el error sistemático**, que es el más común en instrumentos reales: un sensor descalibrado, un sesgo de encuesta, una metodología contable.

5. **La ventana que hay que abrir apunta al instrumento.** Ninguna ventana nueva hacia el objeto resuelve el empate. Lo que lo resuelve es **mirar al observador**: poner en la sala una moneda redonda que todos conocen y ver qué dibuja la lámpara de Tomás. Si la moneda sale elíptica, el problema es la lámpara. `sugerir_observacion` solo propone observaciones del **objeto**. No sabe proponer una calibración.

6. **Variante Vulcano: ¿y si nadie se equivocó?** Supongamos que la lámpara está bien y el objeto **gira despacio**: Tomás miró en otro momento. Entonces la que falla es la **regla** (la simultaneidad), no un observador. La moneda saldría redonda, y eso descarta la lámpara y deja dos sospechosos: la regla o el objeto. Para separarlos, todos miran **en el mismo instante**. Son tres culpables posibles, y cada uno tiene su prueba:

   | Culpable | Ejemplo histórico | Prueba que lo separa |
   |---|---|---|
   | El instrumento | La lámpara de Tomás | Calibrar con un objeto conocido |
   | La regla (ley) | La simultaneidad; Vulcano y la mecánica de Newton | Repetir la medición cumpliendo la regla |
   | El objeto (entidad nueva) | Neptuno | Predecir dónde y cómo aparecería, y mirar |

7. **Qué haría un LLM en una llamada.** Probablemente diría "la vista de arriba está distorsionada", y en la versión base acertaría por frecuencia: las lámparas torcidas son más comunes que los objetos que se deforman. Esta historia no muestra que el motor supere al LLM. Muestra que el motor, tal como está, **puede quedar peor** (el monstruo, el prestigio) si le faltan reglas y calibración.

## Principio

- **A11 — La ley convierte la diferencia en contradicción.** Sin una regla que ligue las sombras (aquí, medidas compartidas), un desacuerdo es solo una diferencia de punto de vista. Con ella, es una contradicción que obliga a culpar a alguien. **Esto deriva el postulado 2:** el invariante es lo que hace detectable el error.
- **A12 — Ante una contradicción hay tres sospechosos: el instrumento, la ley y el objeto.** La consiliencia no elige entre ellos, porque acomodar el error siempre "explica más". Cada sospechoso se descarta con su propia prueba, no con la puntuación.
- **A13 — Se cuentan evidencias por medida, no observadores.** Un observador que no mide la cantidad en disputa no vota.
- **A14 — El error sistemático no se ve repitiendo: se ve calibrando contra algo conocido.** La confiabilidad sale de la calibración y del historial, nunca del prestigio.
- **A15 — Se puede observar al observador.** La observación que decide a veces apunta al instrumento, no al objeto.

## Cómo se pondría a prueba

- **Hoy, con el motor:** construir esta sala en el dominio con proyección exacta, sin la regla de rigidez y con ella. Se verifica que sin la regla gana el monstruo, y con la regla hay empate. Si no ocurre así, la historia está mal contada.
- **Componentes que faltan:**
  - observaciones de calibración, es decir, observaciones sobre un observador;
  - un modelo de error sistemático: un sesgo fijo del instrumento, no solo una probabilidad de fallo;
  - sugerencias que incluyan calibrar y repetir con la regla cumplida, no solo mirar el objeto.
- **En abd-bench:** los casos `error_del_observador` (V03, V04, V10) son esta historia en otros dominios. Habría que revisar si el motor perdió esos casos por las razones 1 a 4.

## Lectura ciega (2026-10-15)

Un agente sin contexto recibió la escena sin la verdad oculta (no sabía de la lámpara). Coincidió en la mayoría ilusoria ("es uno contra uno, Olga no participa"), en el empate correcto entre culpar a Tomás o a Sara, y en la calibración con un objeto conocido. Corrigió tres cosas de la historia:

1. **Ambigüedad, ya corregida.** La escena no decía en qué eje medía 7 la elipse, y de eso depende a quién se culpa. Ahora lo dice.
2. **"Gana el monstruo" depende del generador.** El análisis supuso que la expansión propone "un objeto que se deforma". El agente simuló otra cosa: el generador propone **"cilindro más pantalla del techo distorsionada"**, que es la verdad, con el mismo score (13,28). Pero propone con igual facilidad **"cilindro elíptico más pantalla de Sara distorsionada"**, también 13,28. El problema real no es el monstruo. Es que **cualquier contradicción se lava con una hipótesis auxiliar que cuesta 1 punto, cuando la contradicción costaba 3**: verdad y monstruo pagan lo mismo. Es el patrón que Lakatos describe en los programas degenerativos, ahora dentro de la fórmula.
3. **La regla también es una hipótesis.** "Comparten medidas" supone luz paralela y pantallas perpendiculares. Una pantalla inclinada o una lámpara cercana (sombra agrandada) violan el supuesto sin que nadie mida mal. Si la regla se escribe como regla dura, **mata justo la hipótesis verdadera**. Duhem-Quine, ahora bien aplicado: ante una contradicción, la regla también está en el banquillo.

Variantes que avergüenzan más al motor, propuestas por el agente:

- **Pedro repite a Olga.** Se agrega un cuarto observador en la ventana del frente, que repite el 10 de Olga. La consiliencia suma su observación, rompe el empate y culpa a Tomás con seguridad. Si la que se equivocó era Sara, el motor falla. Repetir una medida que no está en disputa compra votos (A6, A13).
- **Todos miden bien.** La lámpara del costado está más cerca y agranda la sombra (10/7). La regla escrita da K = 0 a la única hipótesis verdadera, y el motor no ve la pista: las dos discrepancias se explican por **un solo factor** (14,3/10 = 10/7).

Principios que el agente propuso y que se adoptan:

- **Diagnóstico por conflicto mínimo:** se identifica el conjunto mínimo de observaciones que no pueden ser ciertas a la vez, y quien no está en él queda exculpado. Es la técnica clásica de diagnóstico basado en modelos (Reiter; de Kleer y Williams). El motor no la tiene.
- **Una hipótesis auxiliar de error cuesta según la frecuencia de ese tipo de error**, no un punto fijo.

## Verificación en código (EXP-014, 2026-10-15)

[EXP-014](../bitacora/EXP-014-salas-en-codigo.md) construyó esta sala en código. Confirmó los puntajes de esta historia: 9,85 para los rígidos, 13,27 para el monstruo y las auxiliares, y la inversión por prestigio. Corrigió dos cosas:

1. **"La mayoría es una ilusión" (punto 2 de "Dónde se rompe") es solo parcialmente cierto.** Con una puntuación predictiva, Olga sí vota. Si el cuerpo es un cilindro, que Olga y Sara midan lo mismo es una consecuencia; si es elíptico, es una coincidencia. El cilindro supera al cilindro elíptico (2,0 contra 0,08), y la lámpara torcida supera a la pantalla de Sara (2,1 contra 1,2). El empate del motor actual es un defecto, no prudencia.
2. **La variante de Pedro de la lectura ciega era falsa en su primera forma.** Si Pedro repite a Olga (frente), el empate se mantiene, porque las dos hipótesis lo explican. Si repite a Sara (costado), gana el cilindro. Esa segunda versión sí ilustra el problema: el motor cuenta dos veces la misma ventana.
