# Axiomas derivados de las historias

Cada axioma cita la historia que lo exige. Son **candidatos**: siguen en pie mientras ninguna historia ni ningún experimento los rompa.

| Id | Axioma | Historia |
|---|---|---|
| A1 | **Mediación.** Nadie ve el objeto, solo proyecciones a través de un instrumento | [1](01-el-cilindro.md) |
| A2 | **Consiliencia, no promedio.** El desacuerdo entre proyecciones es información; una explicación debe producir cada proyección | [1](01-el-cilindro.md) |
| A3 | **Empate empírico.** Si varias explicaciones dan cuenta de todo lo visto, razonar más no decide; decide una observación en la que difieran | [2](02-la-ventana-que-nadie-abrio.md) |
| A4 | **La pregunta decide qué diferencia importa.** Una respuesta está determinada si es la misma para **todo lo compatible con lo visto**, no solo para las hipótesis propuestas. La ventana vale lo que cambia en la respuesta frente a lo que cuesta (corregido tras la lectura ciega) | [2](02-la-ventana-que-nadie-abrio.md) |
| A5 | **La frecuencia es apuesta, no conclusión.** Lo que decida dentro de un empate se registra como apuesta, separado de la evidencia | [2](02-la-ventana-que-nadie-abrio.md) |
| A6 | **El acuerdo no es evidencia si los errores están correlacionados.** Jueces con la misma formación cuentan como uno | [3](03-los-cien-jueces.md) |
| A7 | **Explicar todo no es señal de verdad.** Buscar rivales es obligatorio también cuando nada falla | [3](03-los-cien-jueces.md) |
| A8 | **Diversidad para generar, observación para decidir** | [3](03-los-cien-jueces.md) |
| A11 | **La ley convierte la diferencia en contradicción.** El invariante es lo que hace detectable el error (deriva el postulado 2) | [5](05-la-lampara-torcida.md) |
| A12 | **Ante una contradicción hay tres sospechosos: instrumento, ley y objeto,** y cada uno se descarta con su propia prueba. Se diagnostica por el conjunto mínimo de conflicto: quien no está en él queda exculpado. La regla también es sospechosa | [5](05-la-lampara-torcida.md) |
| A13 | **Se cuentan evidencias por medida, no observadores.** Quien no mide la cantidad en disputa no vota; repetir una medida no disputada no compra votos | [5](05-la-lampara-torcida.md) |
| A14 | **El error sistemático no se ve repitiendo: se ve calibrando.** La confiabilidad sale de la calibración y del historial, no del prestigio | [5](05-la-lampara-torcida.md) |
| A15 | **Se puede observar al observador.** La observación que decide a veces apunta al instrumento | [5](05-la-lampara-torcida.md) |
| A16 | **Las hipótesis auxiliares pagan según lo frecuentes que son.** Si absorber una contradicción con una entidad ad hoc cuesta menos que la contradicción, todo conflicto se lava | [5](05-la-lampara-torcida.md) |
| A17 | **La causa y el desenlace son preguntas distintas;** una pregunta que las mezcla se separa antes de razonar | [6](06-la-accion-que-cae.md) |
| A18 | **Se predicen las sombras del mecanismo, no solo el desenlace** | [6](06-la-accion-que-cae.md) |
| A19 | **Un observador que lee a otros observadores es un eco, no una ventana** | [6](06-la-accion-que-cae.md) |
| A20 | **Un dominio sin leyes no produce contradicciones:** antes de prometer algo, se mide cuánta ley tiene | [6](06-la-accion-que-cae.md) |
| A21 | **Donde el objeto es el veredicto de otros jueces con información y dinero (un mercado), solo aporta contenido lo que no está en ese veredicto;** sin eso, el valor es disciplina | [6](06-la-accion-que-cae.md) |
| A22 | **Las causas pueden sumarse.** Cuando no son excluyentes, la compuesta siempre explica todo; compararlas exige estimar cuánto aporta cada una, no solo si está | [6](06-la-accion-que-cae.md) |
| A23 | **Antes de esperar, buscar la ventana transversal:** el mismo observador visto en otros objetos (amplía A15) | [6](06-la-accion-que-cae.md) |
| A9 | **El compromiso previo no hace acertar en un caso;** produce el registro para saber en quién confiar cuando falta la ventana. **No decidir no exime de apostar:** se declaran probabilidades antes de mirar, aunque no se decida | [4](04-el-sobre-cerrado.md) |
| A10 | **El registro sirve solo si es completo, graduado, independiente y extenso,** y se compara contra la tasa base, no contra el azar | [4](04-el-sobre-cerrado.md) |

## Postulados del documento 02 frente a las historias

| Postulado | Estado |
|---|---|
| 1 — Mediación | **Derivado** (A1). Su corolario de observador falible, también (historia 5), pero ω como probabilidad de error al azar no representa el error sistemático (A14) |
| 2 — Invariante causal | **Derivado** por la historia 5 (A11), con una corrección: la regla también es falible (A12) y no siempre puede ser dura sin matar a la hipótesis verdadera |
| 3 — Ampliación abductiva | **Corregido** por A7: buscar rivales no puede depender de que haya una anomalía |

## Qué dicen sobre el motor actual

| Ya lo hace | Le falta |
|---|---|
| Calcula sombras y empates en el dominio exacto (A2, A3) | Declarar empates en dominios abiertos: el juez LLM elige por frecuencia sin decirlo (A5) |
| Pide la ventana que separa (`sugerir_observacion`) | El costo de abrirla (A4) |
| La pregunta del caso decide qué empate importa (A4) | Buscar rivales cuando nada falla (A7) |
| Registra predicciones de hipótesis (`que_vigilar`) | Registrar apuestas fechadas por juez y calificarlas (A9, A10) |
| — | Tratar como uno a los jueces con la misma formación (A6) |
| — | Responder desde todo lo compatible, no desde la lista de candidatas: topes, "ninguna ventana resuelve esto" (A4) |
| Se abstiene ante un empate (A3) | Apostar aunque se abstenga: hoy, al no decidir, se comporta como Berta (A9) |
| Penaliza contradecir a un observador (residuo c(ω)) | Diagnóstico por conflicto mínimo; costo de las hipótesis auxiliares según su frecuencia (A12, A16) |
| — | Observaciones de calibración, error sistemático, sugerir calibrar (A14, A15) |
| — | No sumar repeticiones de una medida no disputada (A13) |
| — | Separar causa y desenlace; estimar lo que el precio ya descuenta (A17, A21) |
| — | Hipótesis que se suman, con aporte estimado (A22) |
| — | Sugerir observaciones transversales que estén disponibles hoy, no solo esperar (A23) |
