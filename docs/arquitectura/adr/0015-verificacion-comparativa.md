# ADR-0015 — Verificación comparativa y parsimonia juzgada

**Estado:** aceptada (validación pendiente: [EXP-009](../../bitacora/EXP-009-verificacion-comparativa.md))

## Contexto

En el dominio abierto, el verificador por pares aceptó casi todo y P era autodeclarado ([EXP-008](../../bitacora/EXP-008-bench-motor-v01-v02.md)). Ver [13](../../marco-teorico/13-verificacion-comparativa.md).

## Decisión

1. **Verificación comparativa.** En dominios con `verificador: llm`, `VerificadorComparativo` reemplaza a `VerificadorLLM`. Hace una llamada por observación con todas las hipótesis vivas y una escala de cuatro niveles. `Veredicto` gana los campos `nivel` y `peso`, y la consiliencia ponderada usa ω·peso. Las calificaciones ya guardadas no se recalculan.
2. **Parámetro nuevo:** `pesos.peso_esperable`, por defecto 0.5, fijado a priori.
3. **Parsimonia juzgada.** Al registrar una hipótesis en un dominio con verificador LLM, el rol `verificador` lista sus postulados no observados. Se guardan en `HipotesisCandidata.entidades_juzgadas` y cuentan en P junto con los declarados.
4. **El margen en veredictos** usa el peso real de cada veredicto.

## Consecuencias

- **+** Menos llamadas por evaluación; discriminación explícita entre rivales; el acomodo ad hoc cuesta.
- **+** El dominio sintético no cambia.
- **−** Una llamada más por hipótesis (el juez). Las calificaciones dependen del conjunto presente cuando se emitieron.
- **−** Cambia el comportamiento de `finanzas-llm`. Sus comprobaciones se revisan en EXP-009, sin ajustar parámetros para que pasen.
