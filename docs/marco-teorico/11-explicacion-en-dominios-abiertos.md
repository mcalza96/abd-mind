# 11 — Explicación en dominios abiertos

El ejercicio de [10](10-validacion-caida-accion.md) mostró que el marco se diseñó con tres supuestos que solo valen en el dominio sintético:

1. "No explica" equivale a "contradice".
2. Todo lo observado hay que explicarlo.
3. La pregunta es el mecanismo.

Este documento reemplaza esos supuestos por definiciones generales. Cada una se reduce exactamente al marco anterior en el dominio sintético.

## 11.0 Protocolo contra el sobreajuste

Las brechas salieron de un solo caso. Para no ajustar el marco a ese caso:

1. **No se tocan los pesos** (α, β, γ, λ, ω_d). Ningún cambio se justifica porque haga ganar a cierta hipótesis en el caso de la acción.
2. **Cada cambio viene de la teoría, no del caso:** explicación contrastiva (Lipton), relevancia evidencial (Good, Hempel) y robustez.
3. **Reducción:** con un verificador que solo responde "explica" o "contradice", y con todas las observaciones como explananda, el comportamiento es idéntico al de la fase 4b. Todos los experimentos anteriores deben dar los mismos números.
4. **Las pruebas son propiedades, no ganadores.** Por ejemplo: "agregar un hecho al que todas las hipótesis son neutrales no cambia el ranking". Nunca: "en el caso de la acción gana H4".
5. **Caso reservado:** antes de implementar se fija un caso de otro dominio ([§11.6](#116-caso-reservado)) con las propiedades que debe cumplir. No se modifica después de ver los resultados.
6. **Validación externa:** el dataset de casos frontera (`boundary_cases.jsonl`) será la prueba final. Ningún parámetro se ajusta con él sin separar antes un subconjunto de prueba.

### Corrección a 10 §B2

La hipótesis "cajón de sastre" (H7 = estructural + transitoria + sectorial) gana por el diseño de D14: si un componente explica un hecho más que el resto, justifica su entidad. **No se corrige cambiando la función objetivo.** Corregirla así sería sobreajuste: "una parte es estructural y otra transitoria" puede ser la respuesta verdadera. Lo que faltaba era otra cosa:

- que la hipótesis declare qué responde a la pregunta (§11.3); así "mixta" queda explícita como respuesta;
- que los hechos neutrales no cuesten (§11.1); en el caso, esos costos eran los que empujaban a sumar componentes.

## 11.1 Veredicto de tres valores

**Definición.** Para una hipótesis H y una observación y del observador O:

| Relación | Significado | En términos de verosimilitud |
|---|---|---|
| `explica` | Si H es cierta, O reportaría y: H la hace esperable | P(y \| H) alta |
| `contradice` | Si H es cierta, O reportaría otra cosa | P(y \| H) baja |
| `neutral` | H no dice qué reportaría O | P(y \| H) ≈ P(y) |

Una proyección determinista es total cuando puede calcularse: solo produce `explica` o `contradice`. Si la hipótesis no permite proyectar (le falta la variable que la proyección necesita), el veredicto es `neutral`.

**Consecuencias en el score** ([09 §9.1.4](09-robustez-epistemica.md#914-función-objetivo-extendida)):

- C suma ω sobre lo que H **explica**.
- El residuo cobra c(ω) solo sobre lo que H **contradice**. Suponer que un hecho es un error solo hace falta si H lo contradice; si H no habla de él, no hay nada que atribuir a error.
- La derrota (y la tensión, si ω < ω_d) solo ocurre por `contradice`.

**Propiedad (invarianza ante evidencia irrelevante).** Si todas las hipótesis son neutrales respecto de un hecho, agregarlo no cambia ningún score ni el ranking. En la fase 4b esto no se cumplía: un hecho neutral de fuente calibrada derrotaba a todas.

## 11.2 Explanandum y evidencia

**Definición.** Cada observación tiene un rol:

- **Explanandum:** lo que el caso quiere entender (la caída del precio).
- **Evidencia:** sirve para elegir entre explicaciones; nadie está obligado a explicarla.

El valor por defecto es *explanandum*, que es la semántica anterior.

El rol solo cambia el tratamiento del veredicto `neutral`:

| | `explica` | `neutral` | `contradice` |
|---|---|---|---|
| Explanandum | +α·ω | queda **sin explicar**: no suma | −λ·c(ω) |
| Evidencia | +α·ω | nada | −λ·c(ω) |

Un explanandum sin explicar no suma ni cuesta en el score, pero cuenta para el disparo de expansión: si la mejor hipótesis deja explananda sin explicar, conviene buscar una que sí lo haga. La pérdida que se compara contra γ es:

$$L(H) = \sum_{j \in \text{contradichas}} \big(\alpha\,\omega_j + \lambda\,c(\omega_j)\big) + \sum_{j \in \text{explananda neutrales}} \alpha\,\omega_j$$

Con un verificador de dos valores y todo explanandum, L es la de 9.1.7.

## 11.3 La pregunta del caso

Lipton: toda explicación es **contrastiva**: "¿por qué P y no Q?". El usuario no pregunta qué mecanismo produjo la caída, sino "¿estructural o transitoria?".

**Definición.** Un caso puede declarar una pregunta: una variable con valores posibles, por ejemplo `persistencia ∈ {estructural, transitoria, mixta}`. Cada hipótesis afirma un valor. Si no lo afirma, se considera *indeterminada* respecto de la pregunta.

**Respuesta.** Para cada valor v, S(v) es el mejor score entre las hipótesis vivas y coherentes que afirman v. La respuesta es el v con mayor S(v):

- **Determinada:** S(v₁) − S(v₂) > δ. Puede haber un empate de mecanismos dentro de v₁ (subdeterminación del mecanismo) sin que la respuesta lo esté.
- **Subdeterminada:** la diferencia entre las dos mejores clases es ≤ δ.

Si el caso no declara pregunta, la respuesta es H* (comportamiento anterior).

`sugerir_observacion` prioriza las consultas que separan **clases de la pregunta** antes que mecanismos de la misma clase.

## 11.4 Margen de victoria

Una diferencia de score no dice cuán fácil sería invertir el resultado. En dominios con verificador LLM, el error unitario es un veredicto mal juzgado.

**Definición.** El **margen en veredictos** k es la mínima cantidad de veredictos de LLM que habría que cambiar para que el resultado deje de ser el mismo. Hay dos formas de lograrlo:

- **subir a un rival:** un veredicto suyo pasa a `explica`;
- **bajar a los líderes:** un veredicto pasa a `contradice`. Si hay varias hipótesis de la clase ganadora por encima del rival, hay que bajarlas a todas.

El cálculo combina ambas formas: para cada rival y cada cantidad t de cambios a su favor (los de mayor impacto primero), suma lo mínimo necesario para bajar a cada líder que siga por encima. Como el score es aditivo por veredicto, cada paso voraz es exacto. Los veredictos por proyección no cuentan, porque son deterministas: en el dominio sintético k = ∞. Es una aproximación en un punto: no considera que un cambio a `contradice` podría además derrotar al líder.

- Con pregunta, el líder y el rival son los mejores de las dos mejores clases. Sin pregunta, son H* y la segunda.
- El resultado es **frágil** si k ≤ k_f (`pesos.veredictos_fragil`, por defecto 1): un solo veredicto erróneo lo invertiría.
- Un resultado frágil se informa como tal, y `sugerir_observacion` también funciona en ese caso, no solo con empate.

## 11.5 Predicciones y cierre del ciclo

IBE elige la mejor explicación de lo ocurrido. Si la pregunta del usuario es sobre el futuro, hace falta derivar lo que **cada** hipótesis espera.

**Definición.** Una hipótesis puede declarar predicciones: `{que, horizonte, esperado}`. Las predicciones **no entran en el score**: todavía no son observaciones. Sirven para tres cosas:

1. **Qué vigilar:** las predicciones en que el líder y el rival difieren son las señales que cambiarían la respuesta.
2. **Cierre del ciclo:** al vencer el horizonte, Hermes registra lo ocurrido con `nueva_evidencia`. Las predicciones cumplidas o fallidas se vuelven observaciones como cualquier otra.
3. **Calibración:** `cerrar_caso` puede registrar la respuesta verdadera cuando se conoce, como observación falible con historial ([12 §12.1](12-verdad-y-entrenamiento.md#121-la-verdad-de-cierre-es-una-observación)). Los casos cerrados con verdad son el insumo para calibrar ω, δ y k_f (L7). La calibración misma queda para después.

## 11.6 Caso reservado

Este caso se fija antes de implementar y no se modifica después. Su dominio es distinto del financiero: diagnóstico de fallas de una bomba industrial.

Pregunta: `causa ∈ {desgaste, desalineacion, cavitacion}`.

| Hecho | Rol | ω |
|---|---|---|
| e1: la vibración aumentó 3× en dos semanas | explanandum | 0.99 |
| e2: la temperatura del rodamiento está normal | evidencia | 0.98 |
| e3: la presión de succión está bajo el mínimo | evidencia | 0.98 |
| e4: hubo un cambio de turno de operadores | evidencia | 0.9 |

Hipótesis (veredictos fijados de antemano):

- **A** (desgaste): explica e1, contradice e2, neutral ante e3 y e4.
- **B** (desalineación): explica e1, neutral ante e2, e3 y e4.
- **C** (cavitación): explica e1 y e3, neutral ante e2 y e4.
- **C′** (cavitación por obstrucción): igual a C.

Propiedades que debe cumplir:

1. e4, neutral para todas, no cambia ningún score.
2. Agregar e2 cuando A ya existe derrota a A (ω ≥ ω_d), y no derrota a B ni a C.
3. C y C′ empatan en mecanismo, pero la respuesta "cavitacion" queda **determinada**.
4. Si e3 se retracta, la respuesta queda subdeterminada entre las clases de B y C. `sugerir_observacion` debe considerar el caso, porque hay empate entre clases.
5. Si los veredictos vienen del verificador LLM, el margen de la respuesta "cavitacion" es de 1 veredicto, y el resultado se informa como frágil.

Todas las hipótesis postulan una entidad (P = 1). La propiedad 5 se evalúa con los pesos por defecto. La diferencia entre las clases es α·0.98 = 1.47. Bajar la clase "cavitacion" exige cambiar dos veredictos, el de C y el de C′. En cambio, basta uno para subir a B: su veredicto sobre e3 pasa de `neutral` a `explica` y empata. Por eso k = 1.
