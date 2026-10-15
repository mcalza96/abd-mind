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
| A9 | **El compromiso previo no hace acertar en un caso;** produce el registro para saber en quién confiar cuando falta la ventana. **No decidir no exime de apostar:** se declaran probabilidades antes de mirar, aunque no se decida | [4](04-el-sobre-cerrado.md) |
| A10 | **El registro sirve solo si es completo, graduado, independiente y extenso,** y se compara contra la tasa base, no contra el azar | [4](04-el-sobre-cerrado.md) |

## Postulados del documento 02 frente a las historias

| Postulado | Estado |
|---|---|
| 1 — Mediación | **Derivado** (A1). Su corolario de observador falible espera la historia 5 |
| 2 — Invariante causal | **Pendiente:** ninguna historia lo exige todavía. En la sala se da por supuesto (el objeto no cambia según quién mire) |
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
