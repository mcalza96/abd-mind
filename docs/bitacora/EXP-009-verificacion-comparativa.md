# EXP-009 — Verificación comparativa y parsimonia juzgada

- **Fecha:** 2026-10-14 · **Estado:** abortado (ver Resultado); continúa en [EXP-010](EXP-010-juez-comparativo.md)
- **Registro previo:** sí
- **Commit / artefactos:** teoría en [13](../historico/marco-teorico/13-verificacion-comparativa.md), [ADR-0015](../historico/arquitectura/adr/0015-verificacion-comparativa.md)

## Pregunta
¿La verificación comparativa y la parsimonia juzgada hacen que el motor decida cuando la evidencia lo permite, sin perder precisión y sin romper lo que ya funcionaba?

## Expectativa (antes de correr)

Conjunto de prueba: los 20 casos de `--casos pares`, es decir, las 10 variantes y sus originales. V01 y V02 motivaron la propuesta; los otros 18 no.

| Id | Expectativa | Fracaso si… |
|---|---|---|
| E1 | Los veredictos dejan de ser casi todos `explica`: al menos 15 % `indiferente` o `contradice` (en EXP-008 hubo 0 % `contradice`) | Menos de 5 % |
| E2 | El motor determina la respuesta en al menos 12 de 20 casos (en EXP-008, 0 de 2) | Menos de 8 de 20 |
| E3 | Entre las respuestas determinadas, el motor acierta al menos 60 % | Menos de 60 % |
| E4 | En los 18 casos que no motivaron el cambio, los resultados de E2 y E3 se mantienen en proporción | Las mejoras aparecen solo en V01 y V02 |
| E5 | El motor acierta en un rango de ±3 casos respecto de Muse 1.3 sobre los mismos 20 | Más de 3 casos por debajo |
| E6 | Los experimentos sintéticos dan salida idéntica y el caso reservado pasa | Cualquier diferencia |
| E7 | `finanzas-llm` en vivo: se registra qué comprobaciones pasan | No es criterio de fracaso. Si alguna cambia, se registra y no se ajustan parámetros para que pase |

**Parámetros fijados antes de correr:** `peso_esperable` = 0.5. Los demás pesos no cambian.

## Diseño
`abd-mind bench --casos pares`, con motor y línea base, en paralelo. Además, `abd-mind experimento todos` y `finanzas-llm`.

## Resultado

**Corrida abortada.** Implementación en `0ef9c1c`.

- **E6 se cumple:** los experimentos sintéticos dan salida idéntica y el caso reservado pasa.
- **La corrida de pares se detuvo a mano** después de 3 casos fallidos (A03, A06, B04) de 8 iniciados. Ninguno llegó a evaluar: todos fallaron al registrar hipótesis.
- **El juez de parsimonia falla de dos formas:**
  1. **Sobreconteo.** Lista en promedio 8,3 "postulados" por hipótesis (máximo 14; las hipótesis declaraban 0,3). Cuenta como postulados afirmaciones que solo reformulan las observaciones ("mediciones_halley_syowa_validas"), negaciones ("ausencia_de_perdida_real_de_ozono", "toms_es_correcto") y consecuencias. Con γ = 1, P habría dominado el score.
  2. **Truncamiento.** Enumerar tanto, con descripción por ítem, agota los 8000 tokens del rol `verificador`. La respuesta se corta y la operación falla.
- **E1–E5 no se pudieron medir.** El verificador comparativo no llegó a correr en ningún caso del bench.

## Sorpresas y errores

- **Error de diseño propio:** el juez repite el problema que se quería resolver. Sin punto de comparación, el LLM no tiene una granularidad estable, y en vez de ser indulgente (como el verificador en EXP-008) es exhaustivo. Es la lección transversal 3 aplicada a un rol nuevo.
- **Error de método:** no probé el juez con modelos reales sobre un caso antes de lanzar 20 en paralelo. Un caso de prueba habría mostrado el problema en un minuto y con menos llamadas.

## Lecciones

- Todo rol LLM nuevo se prueba primero en uno o dos casos reales antes de una corrida grande.
- Un juicio de cantidad (cuántas entidades) necesita la misma comparación entre rivales que el juicio de verosimilitud. Si no, la escala es arbitraria.

## Decisiones derivadas

[EXP-010](EXP-010-juez-comparativo.md): juez comparativo, registrado antes de implementar.
