# Historia 6 — La acción que cae

Las historias 1 a 5 ocurren en una sala donde el objeto es rígido, las ventanas son independientes y la geometría liga las sombras. Esta historia lleva todo a la pregunta que motivó el proyecto ([10](../marco-teorico/10-validacion-caida-accion.md)): ¿la caída de una acción es estructural o vendrá un rebote? El objetivo es ver qué sobrevive fuera de la sala.

## Escena

**Bombas Andinas** es una empresa mediana, ficticia, que fabrica bombas industriales para minería. Su acción cayó un 35 % en dos meses; el índice del sector cayó un 8 %. Un usuario le pregunta a su agente si la caída es estructural o si vendrá un rebote.

| Observador | Instrumento | Lo que reporta |
|---|---|---|
| Analista fundamental | Estados financieros del último trimestre | El margen bruto cayó 3 puntos; las ventas subieron un 2 % |
| Empresa | Comunicado oficial | Mantiene su proyección de ventas del año; atribuye el margen a "costos de acero transitorios" |
| Prensa | Un medio especializado, con fuentes anónimas | "Bombas Andinas habría perdido a su principal cliente minero". La empresa lo desmiente |
| Analista técnico | Precio y volumen diarios | Volumen 4 veces lo normal durante seis semanas, con muchas operaciones en bloques grandes; rompió su mínimo de dos años |
| Registro de propiedad | Declaraciones trimestrales de fondos, publicadas con 45 días de desfase | Hace un trimestre, el fondo Cóndor tenía el 12 % de la empresa |
| Directores | Registro de transacciones de ejecutivos | Dos directores compraron acciones la semana pasada |
| Consenso de analistas | Promedio de estimaciones | Bajaron un 8 % la ganancia esperada del año, después de la caída |

## La pregunta

¿La caída es estructural o vendrá un rebote? ¿Y qué debería vigilar el usuario?

## Lo que sabe el narrador (la verdad oculta)

- **El fondo Cóndor** enfrenta rescates de sus inversionistas y está vendiendo todas sus posiciones pequeñas, sin mirar la empresa. Esas son las ventas grandes y constantes. Su próxima declaración, dentro de un mes, mostrará que vendió casi todo.
- **El margen** cayó de verdad por un alza puntual del acero, que ya revirtió. El próximo trimestre se recupera a medias.
- **El rumor del cliente es falso**, pero el cliente sí está renegociando precios, y el contrato se renovará con un descuento del 5 %.
- **A doce meses**, la acción sube un 15 % desde el mínimo. El sector, en cambio, cae otro 20 % por el precio del cobre. Contra el sector, la recuperación es fuerte; en valor absoluto, apenas recupera una parte de lo perdido.

## El motor, paso a paso

1. `crear_caso` en el dominio abierto, con la pregunta `tipo_de_caida` ∈ {estructural, transitoria}.
2. `agregar_observacion` para las siete fuentes. El comunicado y el desmentido son **opiniones** del observador interesado; según D8, solo cuenta como hecho que la empresa mantuvo su proyección.
3. `generar_hipotesis`:
   - **H1:** pérdida del cliente principal (estructural);
   - **H2:** venta forzada de un fondo (transitoria);
   - **H3:** costo puntual del acero (transitoria);
   - **H4:** deterioro del ciclo minero (estructural);
   - **H5:** combinaciones de las anteriores.
4. `evaluar`: el verificador (un LLM) califica cada observación contra cada hipótesis. **Casi nada contradice a nadie.** El volumen alto calza con H1 (los informados venden) y con H2 (vende un fondo). La compra de los directores calza con H2 y H3, pero no refuta H1 (los directores pueden equivocarse o querer dar una señal). La proyección mantenida contradice a H1, salvo que la empresa no lo sepa todavía o lo oculte.
5. `mejor_explicacion`: el juez holístico elige, casi seguro, **H5** ("una combinación de presión vendedora y márgenes; vigilar el cliente"). Es razonable y casi no arriesga nada.
6. `que_vigilar`: el próximo trimestre, la próxima declaración del fondo y la renovación del contrato.

## Dónde se rompe

1. **No hay ley, así que no hay contradicción.** En la sala, la geometría convertía las diferencias en contradicciones (A11). Aquí casi ninguna regla liga las sombras, y casi todo es compatible con casi todo. Estamos en la historia 2 con un conjunto infinito de explicaciones, sin la ventana que decide. Las pocas leyes que hay son contables (ventas × margen = utilidad bruta) o legales (una empresa no puede mantener una proyección que sabe falsa sin arriesgar una demanda). **Esas pocas leyes son la única parte donde el motor puede calcular en vez de opinar** (C, [14 §14.3](../marco-teorico/14-rumbo-estado-y-proyeccion.md#143-c-proyección-calculable-en-dominios-reales)).

2. **Las ventanas son ecos.** El analista técnico no mira la empresa: mira a quienes compran y venden. El consenso bajó sus estimaciones **después** de la caída, así que en parte lee el precio. La prensa publica lo que circula en el mercado. Tres de los siete observadores miran, al menos en parte, a los otros observadores. Contarlos como evidencia independiente es la historia 3 a gran escala (A6).

3. **La tercera ventana existe, pero se abre tarde.** La observación que separa H1 de H2 es la próxima declaración del fondo Cóndor, que aparece en un mes. La que separa H3 es el próximo trimestre, en tres meses. En la sala abrir una ventana costaba dinero; aquí cuesta **tiempo**, y mientras tanto el usuario tiene que decidir. El tiempo es la ventana del mercado, y llega en cuotas.

4. **El desenlace es una sombra borrosa.** En la sala, abrir la ventana revelaba el objeto. Aquí, el precio a doce meses mezcla la causa con todo lo que pasó después: el cobre, las tasas, el sector. Con la verdad oculta de esta historia, ¿hubo "rebote"? Contra el sector, sí; en valor absoluto, a medias. Quien acertó la causa (H2 + H3) pudo perder la apuesta sobre el precio, y quien apostó a H1 pudo "acertar" que no volvería a su nivel anterior por la razón equivocada. **Calificar a los jueces por el precio (historia 4) mezcla razonamiento con suerte**, y para separar ambas cosas hacen falta muchos casos.

5. **La pregunta mezcla dos preguntas.** "¿Estructural o rebote?" pregunta por la **causa** (¿cambió algo permanente en la empresa?) y por el **precio** (¿subirá?). No son lo mismo. Una caída estructural que ya está en el precio puede rebotar, y una caída transitoria puede no rebotar si llega otra mala noticia. Es la taxonomía ambigua de EXP-010 otra vez, y además es lo que el usuario realmente pregunta.

6. **El mercado son los cien jueces, pero con dinero y con información distinta.** A diferencia de la historia 3, los participantes no se formaron igual y pierden plata si se equivocan. El precio ya contiene casi toda la información pública. Todas las fuentes del motor son públicas, así que **el motor compite contra un juez que ya vio lo mismo**. Solo aportaría contenido con información que no está en el precio: privada (ilegal o cara), más rápida o mejor calculada. Lo honesto es suponer que no la tiene.

7. **El observador cambia el objeto.** Si muchos usuarios corren el mismo motor y concluyen "transitoria", compran, y eso produce el rebote. En la sala, mirar no movía el objeto; aquí sí. Es la reflexividad de Soros, y debilita el postulado 2: el invariante del mercado cambia en parte porque la gente lo estudia.

8. **Un LLM en una llamada diría casi lo mismo que el motor:** una historia equilibrada, "probablemente una mezcla", y una lista de cosas que vigilar. La diferencia no está en la conclusión.

## Lo que sí sobrevive

Lo que el motor puede aportar aquí, honestamente, no es ventaja sobre el mercado:

- **Separar la pregunta de causa de la pregunta de precio**, y responder cada una por separado.
- **Las predicciones intermedias, fechadas y concretas (el sobre de la historia 4), apuntando a las sombras del mecanismo y no al precio:**
  - "si es H2, la próxima declaración de Cóndor mostrará una venta mayor al 8 % y el volumen se normalizará en un mes";
  - "si es H1, la empresa recortará su proyección en el próximo trimestre".

  Estas sombras están más cerca de la causa que el precio y se resuelven antes.
- **Las pocas leyes del dominio, calculadas:** identidades contables, la descomposición del retorno en parte del sector y parte propia. Aquí se ve que la caída fue del 35 % contra un 8 % del sector: casi toda es propia de la empresa.
- **Que las fuentes eco cuenten como una.**
- **El historial del usuario:** qué tesis tuvo, qué predijo, qué pasó. Sirve para que el usuario sepa cuánto confiar en su propio juicio, no para ganarle al mercado.

## Principio

- **A17 — La causa y el desenlace son preguntas distintas.** Responder una no responde la otra, y una pregunta que las mezcla se separa antes de razonar.
- **A18 — Se predicen las sombras del mecanismo, no solo el desenlace.** El desenlace mezcla la causa con todo lo que pasa después; las sombras intermedias se resuelven antes y señalan mejor la causa.
- **A19 — Un observador que lee a otros observadores es un eco, no una ventana.** Su acuerdo no suma evidencia (amplía A6).
- **A20 — Un dominio sin leyes no produce contradicciones.** Antes de prometer algo en un dominio, hay que medir cuánta ley tiene: ahí, y solo ahí, el motor puede calcular.
- **A21 — Cuando el objeto es el veredicto de otros jueces con información distinta y dinero en juego (un mercado), solo aporta contenido lo que no está en ese veredicto.** Si no se tiene, el valor del motor es disciplina, no ventaja.

## Cómo se pondría a prueba

- **Conjunto F** (segunda investigación): caídas con mínimo entre mayo y octubre de 2025 y desenlace posterior a mayo de 2026. Se evalúan las predicciones intermedias (A18) y no solo el precio, y se compara contra la tasa base de rebote del conjunto, no contra el azar.
- **Mercados simulados ajenos al proyecto**, con causa conocida por construcción y sin la circularidad de los mundos propios. Por ejemplo, un simulador de mercado basado en agentes como ABIDES, donde se puede introducir un fondo con rescates o un shock de costos.
- **Medir cuánta ley tiene el dominio `mercado`:** en los casos F, qué fracción de las observaciones puede chocar con una identidad o regla calculable. Si es casi cero, C no tiene dónde operar.

## Lectura ciega (2026-10-15)

Un agente sin contexto, con conocimientos de finanzas y de filosofía de la ciencia, recibió la escena sin la verdad oculta ni el análisis. Su conclusión coincide con la historia: el motor no da ventaja predictiva, y lo único real que aporta es disciplina y memoria (un registro fechado que impide racionalizar después). Agregó cinco cosas que la historia no tenía.

1. **Una hipótesis que faltaba, y la más peligrosa.** H6: **Cóndor vende porque sabe lo del cliente.** No es una venta forzada sino informada. El análisis presentó la venta del fondo como opuesta a la pérdida del cliente; pueden ser la misma historia. El agente propuso además una hipótesis que nadie mencionó: una venta mecánica por otra causa, como la salida de un índice o una exigencia de garantías. Como alguna hipótesis siempre "explica todo", **la expansión nunca se activa** y esta hipótesis no aparece. Es A7 en un caso real.

2. **Una ventana disponible hoy, que el análisis no vio.** Para separar la venta forzada de la venta informada no hace falta esperar 45 días: basta mirar **las otras posiciones de Cóndor**. Si todas muestran el mismo patrón de volumen, el fondo está liquidando todo y no apostando contra esta empresa. Es una observación sobre el observador hecha **en otros objetos**, y es transversal, no temporal. Corrige el punto 3 de "Dónde se rompe": el tiempo no es la única ventana del mercado.

3. **El objeto de la pregunta no es la empresa.** Es la **diferencia entre el estado de la empresa y lo que el precio ya descuenta**. Si el 35 % ya descuenta la pérdida del cliente, la caída puede ser estructural y aun así rebotar. Abducir la causa no basta: hay que estimar también qué creen los demás.

4. **Las causas se suman.** En la sala, el objeto tiene una sola forma. Aquí la venta del fondo, el acero y la renegociación ocurren a la vez y se combinan. Por consiliencia, la hipótesis compuesta "explica todo" y gana siempre, y su castigo por parsimonia lo decide una constante arbitraria.

5. **La historia está arreglada en parte.** El 12 % de Cóndor está puesto como pista. "Ventas grandes y constantes" suponía que se puede identificar al vendedor en la cinta, y eso normalmente no se puede; la escena ahora dice "operaciones en bloques grandes". Faltan además la cronología, el horizonte de la pregunta y la situación del usuario. Varias observaciones (el consenso, "rompió el mínimo") salen del propio precio y no aportan evidencia nueva (A19).

**Riesgo que señala:** puntuaciones que dan una **apariencia de rigor que el dominio no permite**. Es la misma advertencia del documento 15, ahora desde el caso concreto.
