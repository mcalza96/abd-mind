# Historia 7 — El objeto que cambia según quién mira

## Escena

Misma sala, mismas ventanas que en la historia 5. El objeto es un **cilindro** de 10 × 10. La lámpara del techo está torcida, así que Tomás ve una elipse de 10 × 7.

| Personaje | Ventana | Ve |
|---|---|---|
| Olga | Frente | rectángulo de 10 × 10 |
| Sara | Costado | rectángulo de 10 × 10 |
| Tomás | Techo | elipse de 10 × 7 |

Llega **Merlín**, que propone: *"El objeto adopta, ante cada ventana, la forma que se ve por esa ventana."*

## La pregunta

¿Qué vale la hipótesis de Merlín? ¿Cómo se la descarta, si es que se puede?

## Lo que sabe el narrador

El objeto es un cilindro rígido y no sabe quién lo mira. Pero existen objetos que sí cambian al ser observados: los sistemas cuánticos al medirlos, las personas que se saben estudiadas (efecto Hawthorne) y los mercados (historia 6).

## El motor, paso a paso

1. `crear_caso` con las tres observaciones. `proponer_hipotesis`: cilindro, cilindro elíptico y la hipótesis de Merlín.
2. `evaluar` (α = 1,5, β = 10, γ = 1; ω = 0,95):

   | Hipótesis | Explica | Contradice | P | Score |
   |---|---|---|---|---|
   | Cilindro | Olga, Sara | Tomás (c = 3,0) | 0 | 9,85 |
   | Cilindro elíptico | Olga, Tomás | Sara (c = 3,0) | 0 | 9,85 |
   | **Merlín** | las tres | — | 1 | **13,27** |

3. `mejor_explicacion`: **Merlín**.
4. Llega una cuarta observación por una ventana nueva, sea cual sea. Merlín la explica también: **nunca puede ser derrotado.**

Incluso sin el error de Tomás, Merlín pierde contra el cilindro por un solo punto de parsimonia (13,27 contra 14,27). Con cualquier error de un observador, gana.

## Dónde se rompe

1. **La consiliencia premia a quien no prohíbe nada.** La hipótesis de Merlín "explica" todo porque no dice nada antes de mirar. El motor cuenta lo que una hipótesis explica de lo ya visto, no lo que **prohíbe** de lo que falta ver. Es la objeción de Popper a las teorías que todo lo explican, y la fórmula la ignora.

2. **Merlín ya apareció en los experimentos reales.** En EXP-008, el generador volvió inmune una hipótesis con "sin huella visual" (lección transversal 4). En la historia 6, "una combinación de factores" explica todo. Son versiones suaves de Merlín: no dicen que el objeto cambia, pero se acomodan a cualquier sombra.

3. **No se lo puede prohibir sin más.** A veces Merlín tiene razón: medir altera un sistema cuántico, una persona observada cambia su conducta y un mercado responde a quien lo estudia. Una regla dura que descarte "el objeto depende del observador" eliminaría justo esas verdades.

4. **Lo que distingue al Merlín legítimo del vacío es si dice *cómo* depende.** "La forma cambia según quién mire" no prohíbe nada. "El objeto se deforma solo cuando una lámpara lo ilumina de frente" sí prohíbe algo. Y se prueba mirando **sin que el objeto lo sepa**: una cámara oculta, una medición que el objeto no puede detectar. Es la lógica del doble ciego.

5. **El sobre de la historia 4 desarma a Merlín.** Si cada hipótesis debe escribir **antes** qué sombra verá la próxima ventana, Merlín no puede escribir nada, o escribe "cualquiera", que es apostar a todo con probabilidad repartida. En un registro de Brier, quien no se compromete con nada saca un puntaje mediocre siempre. **El compromiso previo convierte en costo lo que la consiliencia premiaba.**

6. **Qué haría un LLM.** Probablemente descartaría a Merlín por sentido común y culparía a Tomás. Un LLM no premia a Merlín; el motor sí. Es un caso donde la fórmula empeora al modelo.

## Principio

- **A24 — Una hipótesis vale lo que prohíbe.** La consiliencia sobre lo ya visto premia a quien no prohíbe nada. Una hipótesis debe declarar, antes de mirar, qué verá cada ventana no abierta. Si no puede, no compite en igualdad.
- **A25 — "Depende de quién mire" es admisible solo si dice cómo.** Entonces prohíbe algo, y se prueba mirando sin que el objeto lo sepa.

## Cómo se pondría a prueba

- **En el dominio exacto:** agregar la hipótesis de Merlín a la sala de la historia 5 y verificar que hoy gana. Después exigir a cada hipótesis su predicción para las ventanas no abiertas: Merlín no puede darla y queda fuera, o queda con una predicción repartida que pierde en el registro.
- **En abd-bench:** contar cuántas hipótesis ganadoras de EXP-010 a EXP-013 no prohíben nada observable. Por ejemplo, las que no dejan una predicción concreta en `que_vigilar`.

## Lectura ciega (2026-10-15)

El agente sin contexto llegó al mismo diagnóstico: Merlín no prohíbe nada. Su verosimilitud queda repartida entre todos los datos posibles, como pasa con "Dios lo quiso así". Calculó el mismo puntaje (Merlín gana por unos 4 puntos) y agregó cuatro cosas que vale la pena registrar:

1. **Una prueba que no se había visto: encender las tres lámparas a la vez.** Un solo cuerpo no puede tener tres formas en el mismo instante. También se puede cambiar a los observadores de ventana, porque "según quién mira" y "según la ventana" son hipótesis distintas.
2. **El empate sin salida.** Si los datos fueran consistentes, Merlín y el cilindro empatarían (con P = 0), y el motor sugeriría mirar más. Pero **ninguna observación los separa**, porque Merlín se acomoda a cualquiera: el motor quedaría en un bucle sin fin. Es la historia 8 vista desde el lado de la hipótesis.
3. **Los grados de libertad ajustados también son entidades.** Merlín ajusta una forma libre por cada ventana, así que su complejidad real crece con los datos. Contar entidades sintácticas no lo ve: "f = la silueta" tiene cero parámetros escritos. Hay que medirlo con una prueba predictiva, no contando.
4. **Un remedio concreto: puntuar por predicción, no por explicación.**
   - Se oculta una ventana, se predice desde las otras y se repite con cada ventana: validación dejando una fuera.
   - El cilindro acota la sombra oculta; Merlín no predice nada y obtiene la peor puntuación.
   - Se puntúa por log-verosimilitud predictiva, no por "explica sí o no".

   Esto unifica A9 (comprometerse antes), A16 (las auxiliares pagan) y A24 (vale lo que prohíbe) en un solo mecanismo.

**Riesgos del remedio**, señalados por el propio agente:

- Penaliza fenómenos que de verdad dependen del observador cuando todavía no traen un mecanismo.
- La hipótesis "el testigo se equivocó" puede volverse un comodín simétrico al de Merlín. Hay que limitarla: que diga qué medición falló, cómo comprobarlo y con qué frecuencia ocurre (A16).
- En dominios abiertos, un LLM estima mal las verosimilitudes.

**La versión legítima de Merlín** trae dos cosas:

- **un canal causal identificable:** un sensor, el calor de la lámpara, el tiempo entre mediciones, la conciencia de ser observado;
- **una función de dependencia fijada de antemano**, que arriesga predicciones. Por ejemplo, que la forma cambie al tapar el sensor.

Precisa A25.

**Problema de la historia:** como en la 5, los datos son imposibles para cualquier sólido rígido con proyección paralela, así que la escena fabrica la situación en que el acomodo gana. Es deliberado, porque eso es lo que ocurre con un observador que se equivoca. Pero hay que decirlo.
