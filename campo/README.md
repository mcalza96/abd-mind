# Campo: lo que los agentes aprenden al usar las skills

Aquí escriben los agentes (Hermes y otros) mientras trabajan. Es la **entrada** del conocimiento del repositorio: material crudo, fechado y honesto, que después se cura. Nada de lo que está aquí es teoría ni cambia una skill por sí solo.

## El ciclo

```text
uso real ──► nota de campo ──► patrón ──► propuesta de skill o experimento ──► skill estable o marco
(agente)     (agente)          (agente propone,   (taller/ o bitácora)          (solo con OK del usuario)
                                usuario acepta)
     └──────► predicción ──► resolución ──► revisión periódica (¿acierta más que el consenso?)
```

| Paso | Quién escribe | Dónde | Regla |
|---|---|---|---|
| **Nota de campo** | El agente | `campo/notas/` | Una por análisis que valga la pena. Evidencia literal. Los fracasos también |
| **Predicción** | El agente | `campo/predicciones.csv` | Fechada, con probabilidad, antes de saber el resultado |
| **Resolución** | El agente, al llegar la fecha | La misma fila | Solo se completan las columnas de resolución; lo predicho no se toca |
| **Patrón** | El agente lo propone; el usuario lo acepta | `campo/patrones.md` | Al menos **3 notas independientes** que muestran lo mismo |
| **Propuesta de skill** | El agente | `taller/propuestas/` | Ver [taller](../taller/README.md) |
| **Cambio al marco teórico** | Solo el usuario lo pide | `docs/marco-teorico/` | Un principio entra solo si una historia o un experimento lo exige |

## Nota de campo

Archivo `campo/notas/AAAA-MM-DD-dominio-tema.md`:

```markdown
# AAAA-MM-DD · <dominio> · <tema en pocas palabras>

- **Agente y skills usadas:** <agente>, <skills>
- **Pregunta:** <lo que pidió el usuario, en una línea>

## Lo sorprendente
<qué hecho había que explicar y por qué ese>

## Hipótesis
| Hipótesis | Familia | Qué predecía distinto | Resultado de la comprobación |
|---|---|---|---|
| <la obvia> | | | |
| <rival> | | | |

## Evidencia
<cada cifra con su fuente o con la consulta y su salida literal; nada estimado de memoria>

## Conclusión
<la explicación, la confianza y qué la cambiaría>

## Predicciones
<ids de las filas agregadas a predicciones.csv, o "ninguna">

## Lo que aprendí del método
<qué funcionó, qué faltó en la skill, una familia de rivales o una comprobación que no estaba, un error propio. "Nada nuevo" también vale>
```

En «Resultado de la comprobación» usa solo `refutada` (lo predicho no se vio), `sobrevive` (lo predicho distinto de la obvia se vio), `no separada` (compatible pero no la distingue de otra, nómbrala) o `sin comprobar` (di qué dato falta), seguido de la cifra que lo decide; «apoya» solo no vale. Ejemplo: H1 predecía cierre sobre 3,00; cerró en 1,695 → `refutada`.

En «Conclusión», si combinas 2 o más causas, di cuánto aporta cada una y con qué comprobación lo estimaste (por ejemplo «CXMT ~1/3 de la caída; macro ~2/3, porque los no-memoria cayeron X %»); si no se puede estimar, escribe «aporte sin estimar» y qué haría falta.

**Cuándo no escribir:** respuestas triviales, o análisis sin sorpresa ni predicción. Una nota que no enseña nada es ruido.

## Predicciones

`campo/predicciones.csv`, una fila por predicción. Columnas:

| Columna | Contenido |
|---|---|
| `id` | `P-AAAAMMDD-NN` |
| `fecha` | Cuándo se hizo |
| `nota` | Archivo de la nota de campo |
| `dominio` | Por ejemplo `mercados`, `ventas`, `operaciones` |
| `afirmacion` | Algo que se pueda resolver sin discutir: qué, cuánto, para cuándo |
| `probabilidad` | Entre 0 y 1 |
| `resolver_el` | Fecha en que se sabrá |
| `tasa_base` | Probabilidad de referencia sin análisis, con su fuente, o vacía |
| `consenso` | Lo que implica la opinión mayoritaria, si existe, o vacía |
| `resultado` | `1` si ocurrió, `0` si no, `anulada` si dejó de poder resolverse; vacía hasta resolver |
| `resuelta_el` | Fecha de la resolución |
| `fuente_resultado` | De dónde sale el resultado |

Las comas dentro de un texto van entre comillas. **No decidir no exime de apostar** ([principios, P3](../docs/marco-teorico/principios.md#p3--riesgo)): una conclusión sin predicción no se puede calificar.

## Revisión periódica

Cada mes, o cada 20 predicciones resueltas, un agente:

1. Calcula el **puntaje de Brier** por dominio: promedio de (probabilidad − resultado)². Menos es mejor. Lo compara con el de la tasa base y con el del consenso sobre las mismas filas.
2. Lista los **patrones candidatos**: lo que se repite en "lo que aprendí del método".
3. Escribe el resumen en una nota `campo/notas/AAAA-MM-DD-revision.md` y se lo envía al usuario.

Con menos de 30 predicciones resueltas por dominio, el puntaje es solo una indicación, y la revisión lo dice.

## Reglas

- **Los agentes agregan; no reescriben.** Una nota equivocada se corrige con una nota nueva que la enlaza.
- **Nada privado sin permiso:** ni claves, ni datos de terceros, ni posiciones o montos del usuario, salvo que él lo pida.
- **Entrega por PR:** el agente es un contribuidor. Trabaja en una rama `agente/<nombre-del-agente>/<tema>` y abre un PR con la [plantilla](../.github/pull_request_template.md); el usuario lo revisa. Si no tiene acceso de escritura, le envía al usuario los archivos listos. Nunca a `main` directamente: la revisión del PR es la curaduría.
