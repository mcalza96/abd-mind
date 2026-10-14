# EXP-003 — Errata, empate y `finanzas-llm` (fase 4b)

- **Fecha:** 2026-10 (fase 4b) · **Estado:** cerrado
- **Registro previo:** parcial (la tabla de 09 §9.1.6 fijaba las predicciones antes de implementar)
- **Commit / artefactos:** `6d30b91`; experimentos `errata`, `empate`, `finanzas-llm`

## Pregunta
¿Los observadores falibles y la detección de empates se comportan como predice 09?

## Expectativa (antes de correr)
- **errata:** con ω bajo el cilindro sobrevive y no se expande; con ω alto gana el tapón.
- **empate:** sin H*; se sugiere la vista que separa.

## Diseño
Experimentos sintéticos con proyección exacta, y `finanzas-llm` en vivo.

## Resultado
Los sintéticos coinciden con la tabla teórica. `finanzas-llm`: 46 llamadas, unos 7 minutos; 5 hipótesis empatadas y una consulta discriminante (el precio efectivo medio, que las separa en 4 clases).

## Sorpresas y errores
**Ajuste de un parámetro después de ver una falla.** Con la confiabilidad del dominio (ω = 0.9, por debajo de ω_d = 0.95), el comunicado ya no derrotaba a la hipótesis de precios y el test falló. Se le dio al comunicado oficial ω = 0.98, con el argumento de que es una fuente auditada. El argumento es razonable, pero el valor se eligió después de ver el resultado y para que el test pasara.

## Lecciones
- Es la primera instancia registrada de la lección transversal 2.
- Todas las confiabilidades del dominio son suposiciones (L7).

## Decisiones derivadas
L7 en 08; calibrar ω con casos cerrados con verdad `establecida` (ADR-0014) y con mundos sintéticos (12 §12.2).
