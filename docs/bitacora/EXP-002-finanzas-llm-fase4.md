# EXP-002 — `finanzas-llm` (fase 4)

- **Fecha:** 2026-10 (fase 4) · **Estado:** cerrado
- **Registro previo:** no (reconstruido)
- **Commit / artefactos:** `cf746f6`; experimento `finanzas-llm`

## Pregunta
¿El motor completo funciona con modelos reales: córtex, verificador LLM, reglas, derrota y expansión?

## Expectativa (antes de correr)
Ganaría la estrategia de reducción de precios; el comunicado la derrotaría; la expansión encontraría una alternativa.

## Diseño
Tres informes contradictorios y cinco hipótesis propuestas. Después llega un comunicado y se pide expansión.

## Resultado
21 llamadas. Todo lo esperado ocurrió. Después de la expansión, 4 hipótesis distintas quedaron empatadas (score 15.0) y H* se eligió **por el identificador**.

## Sorpresas y errores
- **Error de código:** el generador descartaba como duplicadas hipótesis distintas que afirmaban las mismas variables ("demanda" y "mezcla"). Lo encontraron los tests y se corrigió incluyendo el mecanismo en la firma.
- **Certeza fingida:** el sistema presentaba como "mejor explicación" un empate resuelto por orden alfabético.

## Lecciones
Un desempate determinista sirve para ordenar, no para afirmar.

## Decisiones derivadas
ADR-0010 (subdeterminación y abducción activa).
