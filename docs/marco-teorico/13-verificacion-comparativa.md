# 13 — Verificación comparativa y parsimonia juzgada

Origen: [EXP-008](../bitacora/EXP-008-bench-motor-v01-v02.md). En el dominio abierto, el verificador LLM aceptó casi todo:

- 0 de 60 veredictos fueron `contradice`;
- 2 a 4 tipos de causa empataron y el motor no decidió;
- una hipótesis inmunizada ad hoc ("sin huella visual") recibió el mismo crédito que las demás;
- las hipótesis declaraban sus propias entidades, y casi todas declaraban cero.

**Advertencia:** la propuesta nace de dos casos. Se valida en los 18 casos del conjunto de pares que no la motivaron ([EXP-009](../bitacora/EXP-009-verificacion-comparativa.md)), con expectativas registradas antes de correr.

## 13.1 Por qué falla la verificación absoluta

El verificador recibía **una** hipótesis y **un** hecho, y respondía si el hecho "se explica". Eso tiene tres problemas:

1. **Sin punto de comparación.** Casi cualquier hecho es compatible con casi cualquier hipótesis bien redactada. Lo que discrimina es que una hipótesis haga el hecho **más esperable que sus rivales**: la verosimilitud relativa, o la explicación contrastiva de Lipton.
2. **La compatibilidad se confunde con la predicción.** Pedirle que distinga ambas en el prompt (11 §11.1) no bastó.
3. **Se premia el acomodo.** Una cláusula agregada solo para absorber un hecho ("no deja huella") lo vuelve compatible sin hacerlo esperable. Es la hipótesis auxiliar ad hoc de Popper y Lakatos.

## 13.2 Verificación comparativa

**Definición.** Para cada observación y, el verificador recibe **todas** las hipótesis vivas a la vez y califica, para cada H, cuán esperable es y si H es cierta, en una escala ordinal:

| Nivel | Relación | Peso en C |
|---|---|---|
| `muy_esperable`: H predice y específicamente | `explica` | 1 |
| `esperable`: H lo hace más probable que no, sin predecirlo de forma específica | `explica` | g = 0.5 |
| `indiferente`: y sería igual de esperable sin H, o H lo acomoda con una cláusula ad hoc | `neutral` | 0 |
| `inesperado`: H lleva a esperar otra cosa | `contradice` | — (residuo y derrota, como en 11.1) |

La consiliencia ponderada pasa a ser $\sum \omega_j \cdot g_j$ sobre lo explicado.

- **g = 0.5 es un valor a priori**, el punto medio, fijado antes de correr EXP-009 y sin calibrar.
- **Reducción:** una proyección produce solo `explica` con peso 1 o `contradice`. El dominio sintético no cambia.

**El contexto calibra el juicio, no el score.** Comparar rivales sirve para que el verificador use la escala con discriminación. El score de cada H sigue dependiendo solo de sus calificaciones, así que agregar una hipótesis no cambia el puntaje de las demás por sí mismo. Para mantener esa estabilidad, una calificación ya emitida no se recalcula: las hipótesis nuevas se califican en una llamada que incluye a las anteriores como contexto.

**Costo.** Es una llamada por observación por cada tanda de hipótesis nuevas, en lugar de una por par (hipótesis, observación). Con 5 hipótesis y 6 hechos, baja de 30 llamadas a 6.

## 13.3 Parsimonia juzgada

En el dominio sintético, P se contrasta con un vocabulario y con variables de tipo entidad (D2). En dominios con verificador LLM no hay vocabulario, y P dependía de lo que la hipótesis declaraba de sí misma: la misma debilidad que D1 corrigió para la consiliencia.

**Definición.** Al registrar una hipótesis en un dominio con verificador LLM, un juez independiente (el rol `verificador`, de otra familia que el generador) lista lo que la hipótesis **postula sin que esté observado**: entidades, agentes, eventos, condiciones ocultas o cláusulas auxiliares. No cuenta lo que ya está en las observaciones ni el conocimiento establecido del dominio.

- P = cantidad de postulados distintos, uniendo los juzgados y los declarados, menos los que estén en el vocabulario verificado.
- Los postulados juzgados se guardan con la hipótesis (`entidades_juzgadas`), así que reconstruir el caso no vuelve a llamar al juez.
- **Efecto buscado:** una cláusula de acomodo cuesta como un postulado más, y "una maniobra no registrada" cuenta como lo que es.

## 13.4 Qué no resuelve

- **El juez y el verificador siguen siendo LLM.** Pueden equivocarse de forma sistemática; el margen en veredictos (11 §11.4) sigue siendo la medida de cuánto depende el resultado de ellos.
- **La pregunta del tipo de causa ya es fácil para la línea base** ([EXP-007](../bitacora/EXP-007-bench-linea-base.md)). Esta propuesta busca que el motor decida cuando la evidencia lo permite, no ganarle a la línea base en esa pregunta.
