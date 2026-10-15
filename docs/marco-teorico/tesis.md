# Tesis

## Objetivo

**Una IA a la que se le ocurran explicaciones no obvias**, y que sepa distinguirlas de las rebuscadas. La decisión es del 2026-10-15 y reemplaza a la tesis original, que se conserva en [histórico, 01](../historico/marco-teorico/01-problema-y-tesis.md).

## El problema

Una observación no es la verdad: es una **proyección** del estado real a través del marco de un observador, $y_i = \pi_{O_i}(S)$. Cuando dos observadores discrepan, promediar produce quimeras. Hay que buscar la hipótesis que **produce** todas las sombras. Por ejemplo, el cilindro que de frente se ve como rectángulo y desde arriba como círculo.

Un LLM propone lo frecuente en su corpus. Las explicaciones valiosas suelen ser improbables antes de ser dichas: un planeta no visto, un instrumento mal calibrado, un vendedor que sabe algo. Por eso el LLM las descarta. Si la explicación verdadera nunca se genera, ningún criterio de selección la encuentra.

## Qué aprendimos (EXP-001 a EXP-015)

- **Elegir mejor no era el cuello de botella.** Un motor que decide sumando juicios de un LLM no superó a un LLM en una sola llamada. Contra el mismo modelo, solo empató.
- **Lo que el motor sí aporta es forma, no contenido:** estado del caso, reglas que no se negocian, derrota, abstención explicada y registro.
- **Más muestras de lo mismo no ayudan:** cien jueces con la misma formación se equivocan juntos ([historia 3](../experimentos-mentales/03-los-cien-jueces.md)).
- **Una pregunta distinta sí ayuda.** La explicación no obvia aparece cuando alguien pregunta "¿qué otra cosa daría exactamente estas sombras?".
- **La puntuación por predicción** separa lo no obvio de lo rebuscado: pone primera a la verdad y última a la hipótesis que acomoda todo ([EXP-014](../bitacora/EXP-014-salas-en-codigo.md), [EXP-015](../bitacora/EXP-015-puntuacion-predictiva-en-el-motor.md)).

## La tesis

En los tres momentos de la abducción según Peirce:

1. **Sorpresa:** se detecta qué hay que explicar. Una contradicción, pero también una coincidencia, un residuo, una ausencia o un ajuste demasiado bueno.
2. **Conjetura:** **operadores abductivos**, preguntas que cambian el marco del generador, llevan probabilidad hacia explicaciones que con la pregunta habitual quedan en la cola.
3. **Razón para seguirla:** un filtro con hechos reservados separa lo no obvio de lo rebuscado. Cada conjetura dice qué observación la pondría a prueba, y queda registrada antes de mirar.

El detalle está en [generación](generacion.md). Que los operadores le ganen a las formas baratas de diversidad es una **afirmación empírica**, que todavía hay que demostrar.

## Límites

- **Un operador saca a la superficie lo que el modelo sabe y no dice. No agrega conocimiento del mundo.** Eso solo entra por observaciones nuevas, instrumentos nuevos o el paso del tiempo ([principios, P6](principios.md#p6--contacto)).
- **Donde no hay proyección exacta ni hechos reservados, el filtro es el juicio de otro modelo,** y la auditoría lo dice.
- **En dominios donde el objeto ya es el veredicto de muchos con información y dinero, como un mercado,** el aporte esperable es disciplina, no ventaja.
