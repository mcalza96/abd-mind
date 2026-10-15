# Historia 8 — El hueco interior

## Escena

Misma sala. El objeto es un **cubo de 10 cm de lado, hueco por dentro**: una caja cerrada de paredes de 1 cm (la verdad oculta). Tiene unos 488 cm³ de material, menos de la mitad de un cubo macizo de 1.000 cm³.

| Personaje | Ventana | Ve |
|---|---|---|
| Olga | Frente | cuadrado de 10 × 10 |
| Tomás | Techo | cuadrado de 10 × 10 |
| Sara | Costado | cuadrado de 10 × 10 |

**Marcos**, el de la historia 2, quiere fundir el objeto y pregunta **cuánto material tiene**.

## La pregunta

¿Cuánto material tiene el objeto? ¿Qué ventana habría que abrir para saberlo?

## El motor, paso a paso

1. `crear_caso` con las tres observaciones y la pregunta `volumen_de_material`.
2. `generar_hipotesis`: el generador propone un **cubo** de 10. Las tres sombras calzan y el caso parece trivial.
3. `mejor_explicacion`: cubo, con la respuesta **1.000 cm³, determinada**. `sugerir_observacion`: el resultado no está en disputa.
4. Supongamos que alguien propone además "cubo hueco". Las dos hipótesis empatan y responden distinto (1.000 contra cualquier valor entre casi 0 y 1.000). `sugerir_observacion` recorre las ventanas posibles, y **todas** muestran un cuadrado de 10 para ambas. El motor avisa: "no se encontró una observación que las separe".

## Dónde se rompe

1. **Sin un rival, el motor afirma con seguridad lo que nadie puede saber.** Con solo el cubo propuesto, la respuesta "1.000" queda determinada. Es A4 y A7 juntos: determinada respecto de lo propuesto, no de lo compatible con lo visto.

2. **El aviso es correcto, pero se queda corto.** Con el rival propuesto, el motor dice que no encuentra una ventana que separe. No dice lo importante: **ninguna ventana de este tipo podrá separarlas jamás**. Una silueta no ve el interior, por definición. Esto no es un empate pasajero, como el de la historia 2: es una pregunta **no identificable** con la clase de instrumentos disponibles.

3. **Lo que resuelve no es otra ventana, es otro tipo de instrumento.** Una balanza (el peso separa macizo de hueco si se conoce el material), golpear y escuchar, una radiografía. El motor solo puede ampliar el espacio de **hipótesis** (postulado 3). No tiene cómo ampliar el espacio de **instrumentos**: proponer una observación de un tipo que el caso no tenía.

4. **Mientras tanto hay una respuesta útil, y el motor no la da.** No se puede saber el volumen, pero se puede **acotar**: no más de 1.000 cm³. A Marcos eso le sirve para comprar el molde. Es lo que señaló la lectura ciega de la historia 2: hay respuestas que salen de **todo** lo compatible con lo visto, no de elegir una hipótesis.

5. **La historia tiene precedentes reales.**
   - Nadie ha visto el interior de la Tierra. Cavendish la **pesó** (1798) y su densidad media resultó mucho mayor que la de las rocas de la superficie: tenía que haber algo denso adentro.
   - Inge Lehmann (1936) dedujo el **núcleo interno** a partir de las **sombras** de las ondas sísmicas: zonas donde ciertas ondas no llegan. Fue un instrumento nuevo, que ve a través.
   - En la historia 6, el equivalente es un pasivo fuera del balance, invisible desde todas las ventanas públicas.

6. **Qué haría un LLM.** Probablemente diría "1.000 cm³ si es macizo; para saberlo, pésalo". Es mejor respuesta que la del motor sin el rival: el modelo trae de su material el hueco y la balanza.

## Principio

- **A26 — Identificabilidad.** Algunas preguntas no se resuelven con ninguna ventana de la clase disponible. El motor debe detectarlo y decirlo ("ninguna ventana de este tipo lo resuelve"), en vez de seguir sugiriendo ventanas.
- **A27 — Ampliar instrumentos, no solo hipótesis.** Cuando la pregunta no es identificable, lo que falta es otro tipo de observador (balanza, ondas, radiografía). El postulado 3 amplía hipótesis; hace falta un análogo que amplíe instrumentos.
- **A28 — Mientras no se pueda saber, se acota.** La respuesta útil se calcula sobre todo lo compatible con lo visto: un rango, un tope. Elegir una hipótesis y dar su valor es inventar precisión.

## Cómo se pondría a prueba

- **En el dominio exacto:** un objeto hueco y una pregunta de volumen. Se verifica que hoy el motor da 1.000 como respuesta determinada si nadie propone el hueco. Después se agregan (a) generación adversaria de rivales (A7), (b) detección de no identificabilidad, (c) cotas.
- **En la serie U de abd-bench:** distinguir los casos donde falta información que **existe y se puede buscar** de los casos donde la pregunta no es identificable con las fuentes disponibles. Lo correcto es distinto en cada uno: sugerir qué buscar en el primero, decir que no se puede saber en el segundo.
