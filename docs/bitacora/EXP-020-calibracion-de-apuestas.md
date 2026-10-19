# EXP-020 — ¿Las apuestas de los agentes con la skill le ganan a la tasa base?

- **Fecha:** 2026-10-19 · **Estado:** registrado
- **Registro previo:** sí. Este commit va antes de que exista una sola predicción que cuente: rige para las filas con `fecha` desde el **2026-10-20**.
- **Origen:** pedido del usuario el 2026-10-19: mejorar los criterios de la skill con el acierto de las apuestas que ya registra en uso real, sin ajustar al ruido.
- **Commit / artefactos:** esquema de [`campo/predicciones.csv`](../../campo/README.md#predicciones), validador [`.github/scripts/validar_predicciones.py`](../../.github/scripts/validar_predicciones.py) y su [workflow](../../.github/workflows/predicciones.yml).

## Pregunta

1. ¿Las probabilidades que ponen los agentes con `abduccion` en sus predicciones le ganan a la **tasa base**, medida con el puntaje de Brier?
2. ¿Están **calibradas**, o son sobreconfiadas?
3. Cuando la skill cambia de versión, ¿la versión nueva lo hace mejor que la anterior, **en predicciones hechas después del cambio**?

## Por qué así

- **El resultado de una apuesta casi no enseña qué criterio falló.** En mercados es casi todo ruido, y la [tesis](../marco-teorico/tesis.md#límites) ya dice que ahí se espera disciplina, no ventaja. Por eso hay dos ciclos y no se mezclan:
  - **Ciclo rápido, de proceso:** las notas de resolución encuentran defectos de forma (P-20261015-01 juntó dos condiciones con un «con» y no dijo dónde se medía el rebote). Sirve con una sola nota. Con 3 notas que muestren el mismo defecto, se propone un patrón, y el patrón puede volverse una regla del validador o un cambio de la skill.
  - **Ciclo lento, de calibración:** este experimento. Dice **si** la skill sirve para apostar, no **qué** cambiar.
- **La tasa base no la puede elegir el que apuesta.** Si el agente fija la vara, puede hacer apuestas fáciles y parecer bueno. En el piloto ninguna `tasa_base` es un número: son frases («rebote técnico acotado»), así que hasta hoy el Brier contra la tasa base no se podía calcular.
- **Cambiar la skill después de ver resultados es la lección 2 de esta bitácora.** Cada predicción lleva la versión de la skill con que se hizo, y una versión se juzga solo con sus propias predicciones.
- **Los dominios por activo no llegan nunca a 30.** El piloto tiene 9 predicciones en 4 dominios, de 2 o 3 cada uno. Se evalúa por **tipo de apuesta**, una lista cerrada y corta; el activo queda en `dominio`.

## Diseño

### Unidad

Una fila de `campo/predicciones.csv` con `fecha` ≥ 2026-10-20, `tipo` distinto de `otro` y `resultado` en `0` o `1`. Las `anulada` se cuentan y se informan, pero no entran.

**Piloto, excluido:** las 9 filas anteriores (P-20261015-01 a -06 y P-20261019-01 a -03). Se resuelven igual, con las reglas de `campo/`, pero no cuentan.

### Tipos

| Tipo | Qué apuesta | Ejemplo |
|---|---|---|
| `rebote-tras-caida` | Si un precio recupera después de una caída fuerte, y cuánto | P-20261015-01 |
| `evento-con-fecha` | Si un hecho fechado ocurre o no (guía, resultado, presentación, decisión) | P-20261015-02 |
| `nivel-a-plazo` | Si un precio está sobre o bajo un nivel en una fecha | P-20261019-01 |
| `otro` | Lo demás. Se registra y se resuelve, pero no se evalúa | — |

### Lo que el validador exige a cada fila nueva

El validador corre en cada PR que toca el CSV. Para las filas desde el corte exige:

- `condicion`: la afirmación en forma resoluble, con cláusulas «expresión operador valor» unidas por `Y` u `O`, sin «con», «aprox.» ni conectores en palabras. Por ejemplo, `cierre(KOSPI,2026-10-16) >= 5554 Y (cierre(KOSPI,2026-10-16) - minimo(KOSPI,2026-10-16)) / minimo(KOSPI,2026-10-16) >= 0,02`. Un evento se escribe como `recorta_guia(Samsung,2026-10-29) = no`.
- `fuente_resolucion`: dónde se va a mirar el resultado, nombrada **antes**.
- `tipo` y `familia` de listas cerradas. `familia` es la de la hipótesis que sostiene la apuesta, según la skill `abduccion`, u `obvia`.
- `comprobacion`: la comprobación que más pesó en la conclusión, en pocas palabras.
- `version_skill`: el `version` del frontmatter de `abduccion` que usó el agente.
- `tasa_base` y `consenso`: un número entre 0 y 1, o vacío. Si hay `tasa_base`, `tasa_base_fuente` dice cómo se calculó.

En todas las filas, también las del piloto, el validador revisa que lo predicho no se edite ni se borre respecto de `main`.

### Tasa base

Una `tasa_base` cuenta para la métrica primaria solo si `tasa_base_fuente` permite que otro agente la reproduzca: **datos, ventana y regla**. Por ejemplo, «KOSPI diario 2000-2026, caídas de más de 7% en 3 sesiones; fracción que cerró 2% sobre el mínimo al día siguiente». La ventana y la regla se fijan al registrar la fila, no al resolverla. Quien resuelve la recalcula, y si no le da, la fila sale de la métrica primaria y se anota. Un script que la calcule es trabajo futuro: si se construye, lo reemplaza y se declara aquí con una nota.

### Métricas

Se calculan por tipo cuando el tipo llega a **30 filas resueltas que cuentan**. Antes, las revisiones mensuales de `campo/` informan los números como indicación y lo dicen.

- **Primaria:** Brier skill score contra la tasa base, sobre las filas con `tasa_base` reproducible: BSS = 1 − Brier(agente) / Brier(tasa base). Intervalo de 90% por bootstrap **por nota** (las predicciones de una misma nota no son independientes), 2.000 remuestreos, semilla `20261020`.
- **Secundaria, calibración:** confianza c = máx(p, 1 − p) y acierto = la opción elegida ocurrió. Brecha = promedio de c − tasa de acierto. Se informa también la tabla por cinco tramos de p.
- **Secundaria, consenso:** BSS contra `consenso`, donde sea un número. Es descriptiva: el consenso casi nunca tiene una probabilidad explícita.
- **Por versión:** cada versión de la skill con sus propias filas. Solo se comparan dos versiones si las dos tienen 30 o más filas en el mismo tipo.
- **Control de selección:** se informa qué fracción de las apuestas tiene p entre 0,4 y 0,6. Si pasa de la mitad, el BSS dice poco y la revisión lo declara.

### Veredicto, por tipo

- **Sirve:** el límite inferior del intervalo del BSS es mayor que 0.
- **Fracaso:** el BSS puntual es menor o igual que 0. Quiere decir que en ese tipo la skill no agrega valor predictivo a la tasa base. No dice nada del ciclo de proceso.
- **No concluyente:** lo demás.
- **Sobreconfianza:** se declara si la brecha pasa de 0,10, cualquiera sea el veredicto.

## Expectativa (antes de correr)

- **En los tres tipos de mercado, BSS cerca de 0, entre −0,05 y +0,05.** Lo dice la tesis: el mercado ya es el veredicto de muchos con información y dinero. Un BSS mayor que 0,10 me sorprendería y lo revisaría buscando una tasa base mal hecha antes de creerlo.
- **Sobreconfianza, brecha entre 0,05 y 0,15.** EXP-017 tuvo dos cierres prematuros con confianza de 0,7 o más en cada agente.
- **`evento-con-fecha` es donde más chance tiene la skill**, porque ahí sí hay información que leer, como guías, filings o calendarios, y el precio no la descuenta toda.
- **Fracaso del diseño, no de la skill:** que en seis meses ningún tipo llegue a 30 filas que cuentan, o que más de un tercio de las filas pierda su tasa base al recalcularla. Cualquiera de los dos obliga a revisar el diseño con el usuario, con una nota aquí.

## Amenazas

- **El agente elige qué apostar.** Se controla con la fracción de apuestas cerca de 0,5 y con la tasa base fijada al registrar.
- **Correlación:** varias predicciones sobre el mismo evento. Se controla con el bootstrap por nota.
- **Lectura litigable al resolver:** se controla con `condicion` y `fuente_resolucion` fijadas antes.
- **Ventana de la tasa base a conveniencia:** se fija al registrar, y quien resuelve la recalcula.
- **Cambiar estos parámetros después de ver datos:** cada cambio se declara con una nota fechada y se evalúa en filas posteriores al cambio.

## Resultado

*(pendiente)*
