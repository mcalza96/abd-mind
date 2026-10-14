# Bitácora de experimentos

Registro de cada experimento: qué esperábamos, qué pasó, qué errores cometimos y qué aprendimos. Sirve para no repetir errores y para detectar problemas en las propuestas y en las hipótesis de trabajo.

## Reglas

1. **Registrar antes de correr.** Las expectativas, y qué resultado contaría como fracaso, se escriben **antes** de ver los resultados; el commit lo deja fechado. Las entradas EXP-001 a EXP-008 se reconstruyeron después de los hechos y lo dicen.
2. **Los fracasos se registran igual que los éxitos.** Incluye los errores propios: de diseño, de código y de razonamiento.
3. **Una entrada no se reescribe.** Si después algo resulta falso, se agrega una nota fechada al final, con un enlace a la entrada que lo corrige.
4. **Cada cambio de parámetro hecho después de ver un resultado se declara**, aunque parezca justificado: es la forma más común de sobreajuste.

## Plantilla

```markdown
# EXP-NNN — Título

- **Fecha:** AAAA-MM-DD · **Estado:** registrado | corrido | cerrado
- **Registro previo:** sí | no (reconstruido)
- **Commit / artefactos:** ...

## Pregunta
## Expectativa (antes de correr)
Incluye qué resultado contaría como fracaso.
## Diseño
## Resultado
## Sorpresas y errores
## Lecciones
## Decisiones derivadas
```

## Índice

| Id | Experimento | Resultado en una línea |
|---|---|---|
| [EXP-001](EXP-001-linea-base-cilindro.md) | Línea base en el cilindro (fase 3) | Los tres modelos aciertan en una llamada: el caso es demasiado fácil |
| [EXP-002](EXP-002-finanzas-llm-fase4.md) | `finanzas-llm` (fase 4) | Funciona, pero 4 hipótesis empatan y H* se elige por el id |
| [EXP-003](EXP-003-robustez-fase4b.md) | Errata, empate y `finanzas-llm` (fase 4b) | La teoría se cumple; se ajustó un ω después de ver una falla |
| [EXP-004](EXP-004-ejercicio-caida-accion.md) | Ejercicio mental: caída de una acción | 12 brechas; una conclusión propia resultó equivocada |
| [EXP-005](EXP-005-fase4c-reservado.md) | Fase 4c: caso reservado y `finanzas-llm` | Cumple las propiedades; las hipótesis parciales compiten más cerca |
| [EXP-006](EXP-006-deep-research-1.md) | Primera investigación de casos frontera | Salida fuera de tema: no sirve |
| [EXP-007](EXP-007-bench-linea-base.md) | abd-bench: línea base sobre 50 casos | 36–39 de 49; las variantes no les resultan más difíciles |
| [EXP-008](EXP-008-bench-motor-v01-v02.md) | abd-bench: motor sobre V01/V02 | El motor no decide: el verificador acepta casi todo |
| [EXP-009](EXP-009-verificacion-comparativa.md) | Verificación comparativa y parsimonia juzgada | Registrado antes de correr |

## Lecciones transversales

Patrones de error que ya ocurrieron. Antes de diseñar un experimento, revisar esta lista.

1. **Casos demasiado fáciles** (EXP-001, EXP-007). Si la línea base acierta en una sola llamada, el caso no distingue el motor de un LLM.
2. **Ajustar un parámetro para que pase un test** (EXP-003: ω del comunicado). Si hace falta, se declara y se valida en casos que no motivaron el ajuste.
3. **El verificador LLM no es una proyección** (EXP-005, EXP-008). En el dominio sintético el verificador es exacto; en dominios abiertos es indulgente y casi todo "explica". Las garantías probadas en el dominio sintético no se trasladan solas.
4. **Las hipótesis se acomodan a la evidencia** (EXP-008). Un generador puede volver inmune una hipótesis ("sin huella visual") y el verificador lo premia.
5. **Autodeclaración** (EXP-008). Todo lo que la hipótesis declara de sí misma (entidades, hechos explicados) se puede manipular; D1 ya lo resolvió para C, pero P sigue autodeclarado en el dominio abierto.
6. **Etiquetas propias como verdad** (12, EXP-007). Las variantes y los casos convertidos los escribió un LLM; su "verdad" es una construcción o una fuente secundaria.
7. **Conclusiones propias apresuradas** (EXP-004 §B2). Una brecha que parece defecto puede ser una respuesta legítima. Antes de corregir la función objetivo, preguntar si lo "malo" podría ser verdad.
8. **Encargos a agentes externos sin verificar la salida** (EXP-006). Comprobar formato y tema antes de usar el resultado.
