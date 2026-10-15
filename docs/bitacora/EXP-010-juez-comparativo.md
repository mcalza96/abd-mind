# EXP-010 — Juez de parsimonia comparativo

- **Fecha:** 2026-10-14 · **Estado:** corrido (ver Resultado)
- **Registro previo:** sí
- **Origen:** [EXP-009](EXP-009-verificacion-comparativa.md), abortado por el juez

## Pregunta
Las mismas de EXP-009, con un juez que no sobrecuente: ¿la verificación comparativa y la parsimonia juzgada hacen que el motor decida cuando la evidencia lo permite?

## Cambio respecto de EXP-009
1. **Juez comparativo.** Una sola llamada califica el lote de hipótesis nuevas, con las ya registradas como contexto (con sus postulados ya juzgados), para usar **la misma granularidad** en todas.
2. **Definición más estrecha de postulado:** una entidad, agente o evento independiente cuya existencia la hipótesis afirma y que ninguna observación registra. **No cuentan:**
   - reformulaciones de observaciones;
   - negaciones o ausencias;
   - afirmaciones sobre qué observación es correcta;
   - pasos o consecuencias de otro postulado (si solo existen juntos, cuentan como uno);
   - conocimiento establecido.
3. **Salida mínima:** solo nombres, sin descripción, para no agotar tokens.
4. **Prueba de humo obligatoria** antes de la corrida grande: un caso real (V02) con inspección manual de los postulados y los niveles del verificador. Lo que se observe en la prueba de humo se registra aquí antes de la corrida grande.

No se cambia ningún peso ni `peso_esperable`.

## Expectativa (antes de correr)
Se mantienen E1 a E7 de EXP-009 sin cambios, más:

| Id | Expectativa | Fracaso si… |
|---|---|---|
| E8 | El juez cuenta en promedio entre 0,5 y 4 postulados por hipótesis | Promedio mayor que 4 o igual a 0 |
| E9 | Ninguna operación falla por respuesta truncada | Una o más fallas por truncamiento |

## Diseño
Prueba de humo con `--casos V02`; después `--casos pares --paralelo 5`.

## Prueba de humo (V02, antes de la corrida grande)

**Primer intento: falla.** El juez comparativo ya cuenta bien (0 a 3 postulados por hipótesis), pero el verificador comparativo se trunca. DeepSeek V4.1 Flash razona antes de responder, y esos tokens cuentan en la salida. Una calificación de 5 hipótesis usó 11 608 tokens, por encima del límite de 8000.

**Cambio de ingeniería, declarado:** `max_tokens` del rol `verificador` sube de 8000 a 32 000, y la justificación se limita a una frase. No es un parámetro epistémico: no cambia ningún peso ni umbral.

**Segundo intento:** 7 llamadas, unos 4 minutos.

- **Postulados juzgados por hipótesis:** 0, 2, 1, 1 y 3. La hipótesis de la derivación clandestina recibe 3, incluido "informante_que_avisa_inspecciones".
- **Niveles del verificador:** ahora hay `indiferente` e `inesperado`. La derivación clandestina queda `indiferente` en 5 de 6 hechos e `inesperado` en el ensayo de laboratorio.
- **Resultado:** el motor responde **ley_incorrecta**, que es la correcta, con margen de 1 veredicto (frágil). DeepSeek, como línea base, falla.

V02 motivó la propuesta, así que esto **no** cuenta como validación; solo confirma que la mecánica funciona.

## Resultado

**Corrida:** `--casos pares --paralelo 5`, unos 90 minutos.

**Incidente:** en el último caso (V10), el proveedor cortó una conexión a mitad de respuesta. Esa excepción no estaba contemplada y tumbó la corrida antes de escribir `resultados.jsonl`. Se corrigió:

- el transporte reintenta también las conexiones cortadas;
- el ejecutor guarda cada caso al terminar.

**Cómo se reconstruyeron los resultados:**

- **Motor:** se volvió a correr, reutilizando la caché. Coincidió con la corrida original en 18 casos.
- **V10:** se completó en esa misma pasada.
- **V06 dio otra respuesta en la repetición:** `mecanismo_conocido` en lugar de `entidad_nueva`. No acertó la caché y siguió otro camino. Su respuesta no es estable entre corridas.
- **Línea base:** se toma del log de la corrida original. Muse 1.2 se excluye, porque dejó de ser modelo principal.

| Id | Resultado | ¿Se cumple? |
|---|---|---|
| E1 | 25 % de los veredictos son `indiferente` o `inesperado` (en EXP-008 no hubo ningún `contradice`) | ✅ |
| E2 | El motor determina la respuesta en 18 de 20 casos (en EXP-008, 0 de 2) | ✅ |
| E3 | Acierta 10 de 18 determinadas (56 %); con la repetición de V06, 9 de 18 | ❌ (umbral 60 %) |
| E4 | En los 18 casos que no motivaron el cambio: 16 de 18 determinadas, 8 de 16 aciertos (50 %). V01 y V02, que motivaron el cambio, aciertan ambos | Parcial: la mejora en decidir se generaliza; el acierto, no |
| E5 | Motor 10 de 20, frente a Muse 1.3 con 18 de 19 | ❌ (8 casos por debajo) |
| E6 | Experimentos sintéticos idénticos; el caso reservado pasa | ✅ |
| E7 | `finanzas-llm`: 6 de 6 comprobaciones, con 10 llamadas (antes 42) | ✅ |
| E8 | El juez cuenta en promedio 1,87 postulados por hipótesis (máximo 4) | ✅ |
| E9 | Ninguna falla por truncamiento | ✅ (hubo una falla de red, ya corregida) |

## Diagnóstico de los errores (hecho después de ver los resultados)

1. **La etiqueta del tipo de causa es ambigua.** En D07 y C05 el motor eligió el mecanismo correcto, pero el generador lo etiquetó con otro tipo:
   - D07: "fusión real de dos agujeros negros" quedó como `mecanismo_conocido`; la verdad dice `entidad_nueva`.
   - C05: "el pozo se contamina con heces de un enfermo de cólera" quedó como `mecanismo_conocido`; la verdad dice `entidad_nueva`.

   Las dos lecturas son defendibles. La pregunta del tipo de causa mide, en parte, acuerdo entre la convención de quien etiquetó el caso y la del generador: una proyección del marco del etiquetador, justo lo que critica la tesis (01). **Al menos 2 de los 8 errores son de etiqueta, no de razonamiento.**
2. **La parsimonia decide en contra de lo nuevo** (A01 y C05). La hipótesis de entidad nueva tiene veredictos iguales o mejores, pero paga más postulados:
   - A01: Neptuno pierde por 1 punto frente a "errores sistemáticos de catálogo" (P = 2 contra 1).
   - C05: la partícula viva paga P = 5, incluida la cláusula "no deja rastro en el agua", que el juez castiga como acomodo.
3. **El generador etiqueta hipótesis distintas con el mismo tipo,** y el motor responde la etiqueta de la ganadora. Sin una definición operativa compartida, el tipo depende de cómo lo nombró el generador.

## Lecciones

- **La verificación comparativa cumplió su objetivo:** el motor ahora decide. El cuello de botella pasó de "no decide" a "decide mal". El motor queda muy por debajo de la línea base en este banco.
- **Evaluar con una taxonomía ambigua repite el error de tomar etiquetas como verdad** (lección transversal 6). Una medición que dependa de la etiqueta necesita definiciones operativas o una evaluación por mecanismo, con un juez independiente que tiene sus propios sesgos.
- **No se ajusta γ después de ver estos resultados** (lección transversal 2). Si la parsimonia está mal calibrada para dominios abiertos, se prueba con un experimento registrado que compare con y sin P juzgada.

## Decisiones derivadas

- Antes de correr EXP-012, se agrega una nota a su registro: el tipo de causa puede ser ambiguo; para P se guardan los mecanismos y se revisan.
- Experimento por registrar: P juzgada frente a P declarada sobre los mismos casos, y evaluación por mecanismo con un juez independiente.
