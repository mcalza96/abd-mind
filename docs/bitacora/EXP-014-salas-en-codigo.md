# EXP-014 — Las historias 5, 7 y 8 en código, y la puntuación predictiva

- **Fecha:** 2026-10-15 · **Estado:** corrido
- **Registro previo:** sí (este commit va antes del código)
- **Origen:** [experimentos mentales](../experimentos-mentales/README.md), [16 §16.6](../historico/marco-teorico/16-fundamentos-desde-las-historias.md#166-próximos-pasos)

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

Código: `src/factory/experiments/salas.py`, ejecutable con `abd-mind experimento salas`. Sin LLM; corre en menos de un segundo.

### Parte A: el motor actual falla como dicen las historias

Las nueve expectativas se cumplen.

| Hipótesis (historia 5, ω = 0,95) | Score |
|---|---|
| Cilindro con lámpara cenital torcida (la verdad) | 13,27 |
| Cilindro elíptico con pantalla lateral distorsionada | 13,27 |
| Merlín | 13,27 |
| Objeto que se deforma desde arriba | 13,27 |
| Cilindro | 9,85 |
| Cilindro elíptico | 9,85 |

| Id | Resultado |
|---|---|
| A5a | ✅ Los rígidos empatan en 9,85 y se sugiere expandir |
| A5b | ✅ La verdad, la auxiliar simétrica, el monstruo y Merlín empatan en 13,27 |
| A5c | ✅ Con prestigio, gana el cilindro elíptico (11,30 contra 8,02) |
| A5d | ✅ Pedro repitiendo a Olga no rompe el empate (11,28 contra 11,28); repitiendo a Sara, gana el cilindro (11,28 contra 6,86). **La lectura ciega de la historia 5 se equivocó**, y esa parte de su variante quedó registrada en la historia sin verificar |
| A7a | ✅ Con datos consistentes, el cilindro supera a Merlín por un punto (14,28 contra 13,28) |
| A7b | ✅ Con la elipse de Tomás, gana Merlín |
| A7c | ✅ La observación nueva derrota al cilindro, nunca a Merlín |
| A8a | ✅ Solo con el cubo propuesto, "1000" queda determinada |
| A8b | ✅ Con el cubo hueco, queda sin determinar y ninguna vista separa |

### Parte B: la puntuación predictiva

| Hipótesis | Olga oculta | Sara oculta | Tomás oculto | Total |
|---|---|---|---|---|
| Cilindro con lámpara cenital torcida | 1,000 | 1,000 | 0,100 | **2,100** |
| Objeto que se deforma desde arriba | 1,000 | 1,000 | 0,007 | 2,007 |
| Cilindro | 1,000 | 1,000 | 0,000 | 2,000 |
| Cilindro elíptico con pantalla lateral distorsionada | 1,000 | 0,083 | 0,083 | 1,167 |
| Cilindro elíptico | 0,083 | 0,000 | 0,000 | 0,083 |
| Merlín | 0,007 | 0,007 | 0,007 | 0,021 |

| Id | Resultado |
|---|---|
| B1, Merlín | ✅ 0,021: cae al último lugar (con el motor actual estaba primero) |
| B1, monstruo | ❌ **Falla la expectativa:** 2,007, no bajo 0,1 |
| B2 | ❌ **Falla la expectativa:** las auxiliares no empatan (2,100 contra 1,167) |
| B3 | ✅ El cilindro elíptico queda en 0,083 |
| B4 | ✅ El objeto que se deforma (2,007) queda bajo la lámpara torcida (2,100) |
| B5 | ✅ Cubo y cubo hueco no son identificables con estas ventanas |
| B6 | No se probó: el prototipo ignora ω, así que no dice nada del prestigio ni de Pedro |

**La verdad queda primera.** La lámpara torcida gana sin que nadie le diga que es la verdad.

## Sorpresas y errores

1. **B1: la vaguedad solo se paga donde se es vago.** El objeto que se deforma es un cilindro rígido en el frente y el costado, y libre solo en el techo. Predice bien las dos primeras ventanas y paga solo en la tercera. Supera al cilindro simple porque el cilindro da probabilidad **cero** a la elipse de Tomás: no dice que Tomás puede equivocarse, simplemente se equivoca. Una versión honesta del cilindro tendría que repartir probabilidad para el error de Tomás según ω. Con ω = 0,95, eso daría unos 0,05/144 ≈ 0,0003 para la elipse, y el orden sería: lámpara (mecanismo específico), luego monstruo (vago), luego "Tomás se equivocó al azar". Es razonable, pero mi expectativa estaba mal planteada.

2. **B2: la coincidencia sí es evidencia. Esto corrige un axioma.** Supuse que culpar a Tomás o a Sara era simétrico ("uno contra uno, Olga no vota", A13). La puntuación predictiva dice que no:
   - Si el cuerpo es un cilindro, que Olga y Sara midan lo mismo (10) es **una consecuencia** de la hipótesis.
   - Si el cuerpo es elíptico, es **una coincidencia**: sus dos anchos son independientes.

   Por eso Olga **sí vota**, no sobre la medida en disputa, sino a través de la estructura de la hipótesis. Es el viejo argumento de que una buena explicación elimina coincidencias. Whewell lo llamaba consiliencia, y el motor actual no lo ve, porque cuenta coincidencias de valores, no coincidencias explicadas. El empate exacto de la Parte A (9,85 contra 9,85) es **un error del motor**, no una virtud.

3. **Una regla que el prototipo impone sin decirlo.** En la Parte A, las hipótesis llegan **ya ajustadas a los datos**, como las propone un generador después de mirar. En la Parte B son **familias con parámetros**, y el ajuste lo hace el motor. Esa diferencia es la que desarma a Merlín y a las auxiliares hechas a la medida. Si el generador entrega instancias ajustadas, la puntuación predictiva no tiene con qué trabajar.

## Lecciones

- Las historias 5, 7 y 8 estaban **bien contadas**: el motor falla exactamente como dicen. El costo de verificarlas fue mínimo.
- **Una lectura ciega también se equivoca** (Pedro de frente). Sus aportes se verifican igual que los míos.
- La puntuación predictiva corrige lo que prometía (Merlín, auxiliares hechas a la medida, el monstruo frente al mecanismo específico). Además encontró algo que no buscábamos: **la coincidencia como evidencia**, que corrige A13.
- Las dos expectativas fallidas eran mías, no del prototipo. Se registran sin ajustar el código para que pasen.

## Decisiones derivadas

- **A13 se corrige:** se cuentan evidencias por medida, pero un observador que no mide la cantidad en disputa vota a través de las hipótesis que ligan su medida con la disputada. Lo que sí vale de A13 es que repetir la **misma** ventana no son dos votos independientes.
- **Requisito para P3:** el generador debe entregar hipótesis como familias con parámetros, o al menos declarar qué ajustó a los datos.
- **Pendientes:**
  - el error del observador dentro de la probabilidad (mezcla según ω);
  - la misma prueba con ω distintos (prestigio) y con observadores repetidos;
  - llevar la puntuación predictiva al motor, detrás de una opción, comparando ambas en los experimentos existentes.
