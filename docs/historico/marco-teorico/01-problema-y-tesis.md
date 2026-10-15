# 01 — Problema y tesis central

> **Nota (2026-10-15).** La tesis de §1.3 y el alcance de §1.5 ponen el peso en **seleccionar** de forma determinista. Los experimentos EXP-007 a EXP-015 mostraron que ese no es el cuello de botella: el problema que describe §1.4 (el LLM poda lo improbable) se resuelve **generando** de otra manera, no eligiendo mejor. El nuevo centro está en [17 — Generación abductiva](17-generacion-abductiva.md). Esta sección se conserva tal como se escribió.

## 1.1 El supuesto que se rechaza

El aprendizaje supervisado convencional descansa en un axioma de medición: la etiqueta humana $y$ es el estado real $S$ contaminado por ruido estocástico de media cero.

$$y = S + \varepsilon$$

De ese supuesto se siguen las prácticas habituales: voto mayoritario, modelos de confusión por anotador (Dawid–Skene), agregación por consenso. Si el desacuerdo es ruido, promediar lo reduce.

**La tesis del proyecto es que el supuesto es falso** en una clase amplia de problemas. Una etiqueta no es $S$ con ruido: es una *proyección* de $S$ a través del marco de referencia de un observador concreto —su perspectiva, su instrumental, sus convenciones—:

$$y_i = \pi_{O_i}(S)$$

## 1.2 Consecuencia: el techo del consenso

Si las etiquetas son proyecciones, entrenar para minimizar el error contra el consenso inter-observador optimiza la **imitación de convenciones**, no la captura del mecanismo causal. El rendimiento del modelo queda acotado por el marco de los observadores que lo etiquetaron.

Peor aún, cuando dos marcos son estructuralmente distintos, el promedio de sus proyecciones puede no corresponder a ningún estado posible del mundo: es una **quimera estadística**. El ejemplo canónico (ver [05](05-experimentos-canonicos.md)) es el de un cilindro visto de frente ("rectángulo") y desde arriba ("círculo"): el promedio semántico ("óvalo", "rectángulo redondeado") no es la respuesta correcta ni una aproximación a ella.

## 1.3 La tesis

> Superar ese techo exige un pipeline **abductivo** —Inferencia a la Mejor Explicación (IBE)— que trate las discordancias y anomalías no como ruido a promediar sino como **disparadores** para formular hipótesis latentes que unifiquen las observaciones bajo leyes causales invariantes.

Tres desplazamientos concretos:

| Enfoque inductivo | Enfoque abductivo (este proyecto) |
|---|---|
| El desacuerdo es ruido | El desacuerdo es información sobre la estructura de los marcos |
| Se estima $S$ como promedio de $y_i$ | Se busca $H$ tal que $\pi_{O_i}(H) \approx y_i$ para todo $i$ |
| El espacio de hipótesis es fijo | Una anomalía irreducible obliga a ampliar el espacio |
| La predicción se revisa reentrenando | La conclusión es derrotable en tiempo de ejecución |
| El modelo generativo decide | El modelo generativo propone; un evaluador determinista decide |

## 1.4 Por qué un LLM solo no basta

Un LLM autorregresivo maximiza la probabilidad condicional de cada token. Eso lo sesga hacia lo frecuente en su corpus: explicaciones convencionales, racionalizaciones plausibles, el consenso lingüístico. Las explicaciones abductivas valiosas suelen ser **de baja probabilidad a priori** —postulan una entidad no observada o un vínculo contraintuitivo— y la decodificación greedy, beam search o top-p tiende a podarlas temprano (ver [07, pilar 4](07-estado-del-arte.md#pilar-4--ibe-y-decodificación-en-modelos-generativos)).

Por eso la arquitectura usa el LLM para lo que hace bien —traducir lenguaje natural a estructura y **proponer** candidatos diversos— y saca de él la **decisión**, que pasa a una función objetivo explícita evaluada en código determinista.

## 1.5 Alcance

El proyecto no pretende resolver el problema teórico completo descrito en la literatura (optimización continua en un espacio latente de mecanismos, ver [07](07-estado-del-arte.md#el-vacío-formal)). Su objetivo es más acotado y verificable:

1. Construir un pipeline donde **la selección** de hipótesis sea determinista, auditable y separada de la verosimilitud del LLM.
2. Mostrar empíricamente, en entornos sintéticos controlados, que ese pipeline recupera la causa latente donde un LLM en decodificación directa produce la quimera.
3. Llevarlo a un dominio real (análisis de informes financieros contradictorios) con reglas invariantes explícitas.
