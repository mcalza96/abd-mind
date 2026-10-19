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
| Hipótesis | Familia | Qué predice distinto de la obvia (antes de mirar) | Resultado de la comprobación |
|---|---|---|---|
| <la obvia> | | | |
| <rival> | | | |

## Evidencia
<cada cifra con su fuente o con la consulta y su salida literal; nada estimado de memoria>

En «Evidencia» marca con **decisiva** la cifra o el hecho que decide la conclusión y dale su fuente primaria —el regulador, el filing, el operador del dato o el comunicado de la empresa— con URL; un resumen de buscador o de un LLM («grounding», «AI overview») sirve como pista, nunca como evidencia de una cifra **decisiva**. Si no se encontró la primaria, escribe «primaria no encontrada» y baja la confianza.

## Conclusión
<la explicación, la confianza y qué la cambiaría>

## Predicciones
<ids de las filas agregadas a predicciones.csv, o "ninguna">

## Lo que aprendí del método
<qué funcionó, qué faltó en la skill, una familia de rivales o una comprobación que no estaba, un error propio. "Nada nuevo" también vale>
```

En «Qué predice distinto de la obvia (antes de mirar)» escribe solo algo que la obvia prohíba o haga improbable, idealmente con número o fecha; si no hay nada así, escribe «nada distinto: sobra o es la misma» (cf. «Contra lo rebuscado»); lo que no distingue de la obvia se cierra como `no separada`, nunca como `sobrevive`. Ejemplo: SPRC H1 predice cierre sobre 3,00 frente a H2 que predice precio que gravita a 1,50.

En «Resultado de la comprobación» usa solo `refutada` (lo predicho no se vio), `sobrevive` (lo predicho distinto de la obvia se vio), `no separada` (compatible pero no la distingue de otra, nómbrala) o `sin comprobar` (di qué dato falta), seguido de la cifra que lo decide; «apoya» solo no vale. Ejemplo: H1 predecía cierre sobre 3,00; cerró en 1,695 → `refutada`.

En «Conclusión», si combinas 2 o más causas, di cuánto aporta cada una y con qué comprobación lo estimaste (por ejemplo «CXMT ~1/3 de la caída; macro ~2/3, porque los no-memoria cayeron X %»); si no se puede estimar, escribe «aporte sin estimar» y qué haría falta.

**Cuándo no escribir:** respuestas triviales, o análisis sin sorpresa ni predicción. Una nota que no enseña nada es ruido.

## Predicciones

`campo/predicciones.csv`, una fila por predicción. El formato lo fija [EXP-020](../docs/bitacora/EXP-020-calibracion-de-apuestas.md). Columnas:

| Columna | Contenido |
|---|---|
| `id` | `P-AAAAMMDD-NN` |
| `fecha` | Cuándo se hizo |
| `nota` | Archivo de la nota de campo |
| `dominio` | El activo o el área, por ejemplo `mercados-kospi`, `ventas`, `operaciones` |
| `tipo` | `rebote-tras-caida`, `evento-con-fecha`, `nivel-a-plazo` u `otro` |
| `afirmacion` | La apuesta en una frase, para leerla |
| `condicion` | La misma apuesta en forma resoluble (ver abajo) |
| `fuente_resolucion` | Dónde se va a mirar el resultado, nombrada antes |
| `probabilidad` | Mayor que 0 y menor que 1 |
| `resolver_el` | Fecha en que se sabrá |
| `familia` | Familia de la hipótesis que sostiene la apuesta, según la skill `abduccion`: `obvia`, `nada-que-explicar`, `medicion`, `seleccion`, `mezcla`, `tercero-comun`, `decision`, `tiempo`, `umbral`, `gemelo` o `varias-causas` |
| `comprobacion` | La comprobación que más pesó en la conclusión, en pocas palabras |
| `version_skill` | El `version` del frontmatter de `abduccion` que usaste |
| `tasa_base` | Probabilidad sin análisis, un número entre 0 y 1, o vacía |
| `tasa_base_fuente` | Datos, ventana y regla con que se calculó la tasa base, para que otro la reproduzca |
| `consenso` | Probabilidad que implica la opinión mayoritaria, un número entre 0 y 1, o vacía |
| `resultado` | `1` si ocurrió, `0` si no, `anulada` si dejó de poder resolverse; vacía hasta resolver |
| `resuelta_el` | Fecha de la resolución |
| `fuente_resultado` | De dónde sale el resultado |

**`condicion`:** cláusulas «expresión operador valor» unidas por `Y` u `O` en mayúscula. Operadores: `>=`, `<=`, `>`, `<`, `=`. El valor es un número (con coma o punto, con o sin `%`), `sí` o `no`. Sin «con», «aprox.», «cerca» ni conectores en palabras: si la apuesta tiene dos condiciones, se escriben las dos. Ejemplos:

```text
cierre(KOSPI,2026-10-16) >= 5554 Y (cierre(KOSPI,2026-10-16) - minimo(KOSPI,2026-10-16)) / minimo(KOSPI,2026-10-16) >= 0,02
recorta_guia(Samsung,2026-10-29) = no
```

Las comas dentro de un texto van entre comillas. **No decidir no exime de apostar** ([principios, P3](../docs/marco-teorico/principios.md#p3--riesgo)): una conclusión sin predicción no se puede calificar.

**Validador.** Cada PR que toca el CSV corre [`validar_predicciones.py`](../.github/scripts/validar_predicciones.py). En todas las filas revisa el formato y que lo predicho no se edite ni se borre respecto de `main`. En las filas desde el 2026-10-20 exige además las columnas nuevas. Para probarlo antes de abrir el PR:

```bash
python3 .github/scripts/validar_predicciones.py campo/predicciones.csv
```

## Revisión periódica

Cada mes, o cada 20 predicciones resueltas, un agente:

1. Calcula las métricas de [EXP-020](../docs/bitacora/EXP-020-calibracion-de-apuestas.md) por `tipo` y por `version_skill`, con los parámetros que fija ese registro: Brier skill score contra la tasa base y contra el consenso, y la brecha de calibración. Las 9 filas anteriores al 2026-10-20 son piloto y no entran.
2. Lista los **patrones candidatos**: lo que se repite en "lo que aprendí del método" y en las resoluciones.
3. Escribe el resumen en una nota `campo/notas/AAAA-MM-DD-revision.md` y se lo envía al usuario.

Con menos de 30 predicciones resueltas por tipo, las métricas son solo una indicación, y la revisión lo dice. **Un resultado no cambia la skill por sí solo:** un cambio se propone con el ciclo de siempre y se evalúa solo con las predicciones hechas después.

## Reglas

- **Los agentes agregan; no reescriben.** Una nota equivocada se corrige con una nota nueva que la enlaza.
- **Nada privado sin permiso:** ni claves, ni datos de terceros, ni posiciones o montos del usuario, salvo que él lo pida.
- **Entrega por PR:** el agente es un contribuidor. Trabaja en una rama `agente/<nombre-del-agente>/<tema>` y abre un PR con la [plantilla](../.github/pull_request_template.md); el usuario lo revisa. Si no tiene acceso de escritura, le envía al usuario los archivos listos. Nunca a `main` directamente: la revisión del PR es la curaduría.
