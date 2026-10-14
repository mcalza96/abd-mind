# EXP-009 — Verificación comparativa y parsimonia juzgada

- **Fecha:** 2026-10-14 · **Estado:** registrado (expectativas escritas antes de implementar y correr)
- **Registro previo:** sí
- **Commit / artefactos:** teoría en [13](../marco-teorico/13-verificacion-comparativa.md), [ADR-0015](../arquitectura/adr/0015-verificacion-comparativa.md)

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
*(pendiente)*
