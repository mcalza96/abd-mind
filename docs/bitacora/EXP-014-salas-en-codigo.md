# EXP-014 — Las historias 5, 7 y 8 en código, y la puntuación predictiva

- **Fecha:** 2026-10-15 · **Estado:** registrado
- **Registro previo:** sí (este commit va antes del código)
- **Origen:** [experimentos mentales](../experimentos-mentales/README.md), [16 §16.6](../marco-teorico/16-fundamentos-desde-las-historias.md#166-próximos-pasos)

## Pregunta

1. ¿El motor actual falla **exactamente** como dicen las historias 5, 7 y 8? Si no, las historias están mal contadas.
2. ¿Una puntuación por predicción (validación dejando una observación fuera, P3) corrige esas fallas, y cuáles no?

Sin LLM: sala con proyección exacta y siluetas **con medidas**.

## Diseño

**Parte A: motor actual.** Se usa `ArbolHipotesis` con los pesos por defecto (α = 1,5, β = 10, γ = 1, λ = 1), un verificador de siluetas con medidas y las observaciones registradas antes que las hipótesis, como en un caso real. Las hipótesis son las que un generador propondría **después de ver los datos**, así que sus parámetros ya están ajustados: el cilindro elíptico ya es de 10 × 7, y la lámpara torcida ya produce exactamente 10 × 7.

**Parte B: prototipo predictivo.** Cada hipótesis es una **familia con parámetros**:

| Familia | Parámetros |
|---|---|
| Cilindro | diámetro, alto |
| Cilindro elíptico | ejes a, b, alto |
| Cilindro con lámpara cenital torcida | diámetro, alto y el eje acortado k ≤ diámetro |
| Cilindro elíptico con pantalla lateral distorsionada | — |
| Objeto que se deforma desde arriba | cilindro con techo libre |
| Merlín | una silueta libre por ventana |

- Cada medida va de 1 a 12, enteros.
- Para cada observación: se oculta, se ajustan los parámetros que satisfacen el **máximo número** de las restantes y se calcula la probabilidad de la observación oculta, repartida por igual entre los parámetros ajustados.
- **Puntaje** = suma de esas probabilidades.

## Expectativa (antes de correr)

**Parte A, el motor actual:**

| Id | Expectativa | Fracaso de la historia si… |
|---|---|---|
| A5a | Historia 5: cilindro y cilindro elíptico empatan en 9,85; se sugiere expandir | No empatan o no se sugiere expandir |
| A5b | El objeto que se deforma, la lámpara torcida (verdad) y la pantalla de Sara distorsionada empatan en 13,27 y superan a los rígidos: el puntaje no distingue verdad de monstruo | Alguna difiere |
| A5c | Prestigio (Tomás ω = 0,99, Sara 0,8): gana el cilindro elíptico, 11,30 contra 8,02 | Gana el cilindro |
| A5d | Pedro repite la medida de **Olga** (frente): **no** rompe el empate, porque ambas hipótesis lo explican. La lectura ciega de la historia 5 afirmó lo contrario; aquí se prueba. Si Pedro repite la medida de **Sara**, gana el cilindro | Pedro-frente rompe el empate |
| A7a | Historia 7 con datos consistentes (techo: círculo de 10): el cilindro (14,27) supera a Merlín (13,27) por un punto | Merlín gana o empata |
| A7b | Con la elipse de Tomás, Merlín gana: 13,27 contra 9,85 | El cilindro gana |
| A7c | Una observación nueva con ω = 1 que contradice a todo sólido rígido derrota al cilindro y **nunca** a Merlín | Merlín queda derrotado |
| A8a | Historia 8 con solo el cubo propuesto y pregunta de volumen: respuesta "1000" determinada | No queda determinada |
| A8b | Con el cubo hueco agregado: la respuesta queda sin determinar y **ninguna** de las tres vistas separa | Alguna vista separa |

**Parte B, la puntuación predictiva (historia 5 con la elipse de Tomás):**

| Id | Expectativa | Fracaso si… |
|---|---|---|
| B1 | Merlín y el objeto que se deforma quedan por debajo de 0,1; el cilindro llega a 2 | Merlín supera al cilindro |
| B2 | La lámpara torcida y la pantalla de Sara distorsionada **empatan** (≈ 2,1) y quedan levemente sobre el cilindro (2,0): la auxiliar específica cuesta casi lo mismo que culpar al observador. Ya no hay salto de 3,4 puntos | La auxiliar supera al cilindro por más de 0,5, o las dos auxiliares no empatan (sería una asimetría introducida por mí) |
| B3 | El cilindro elíptico queda muy por debajo del cilindro (< 0,5) | Supera al cilindro |
| B4 | El objeto que se deforma (cualquier techo) queda por debajo de la lámpara torcida (techo con un solo eje acortado): la hipótesis que dice **cómo** depende prohíbe más y gana (A25) | No queda por debajo |
| B5 | Historia 8: cubo y cubo hueco hacen la misma predicción en todas las vistas; se detecta como no identificable con estas ventanas | Alguna vista los separa |
| B6 | **Limitaciones declaradas:** la puntuación predictiva no corrige el prestigio (A5c) ni a Pedro repitiendo a Sara (A5d). Eso corresponde a P1 (calibración e instrumentos), no a P3 | — |

## Resultado

*(pendiente)*
