# EXP-007 — abd-bench: línea base sobre los 50 casos

- **Fecha:** 2026-10-14 · **Estado:** corrido
- **Registro previo:** no (primera corrida exploratoria del ejecutor)
- **Commit / artefactos:** `76765b9`; `datasets/abd-bench/resultados/2026-10-14-linea-base/`

## Pregunta
¿Cuánto aciertan los modelos en una sola llamada el tipo de causa? ¿Les cuestan más las variantes disfrazadas?

## Diseño
Los 50 casos. Cada modelo de `linea_base` recibe los mismos observadores, observaciones y pregunta que recibiría el motor. Unas 150 llamadas, 7 minutos.

## Resultado
Sobre 49 casos con verdad `establecida`:

| Modelo | Aciertos |
|---|---|
| DeepSeek V4.1 Flash | 36 |
| Muse 1.2 | 39 |
| Muse 1.3 | 39 |

- Las variantes no les resultaron más difíciles (8–9 de 10).
- Fallan los tres en B03, E04 y V08.
- V08, la variante de GW150914, falla en los tres, mientras que los tres aciertan el original D07: es la señal más clara de memoria.

## Sorpresas y errores
- **Error del informe:** mostraba la columna del motor con 0/49 cuando el motor no se había corrido. Corregido.
- **Dos lecturas posibles de que las variantes sean igual de fáciles:** que los modelos razonan bien, o que las variantes (escritas por el asistente) delatan la respuesta. No se puede distinguir todavía.

## Lecciones
- La línea base ya es fuerte: la pregunta del tipo de causa, con cuatro valores, es fácil para modelos actuales.
- El valor del motor no puede estar en "acertar más" esta pregunta en casos de este tipo. Debe estar en lo que la línea base no da: margen, abducción activa, derrotabilidad y auditoría. O en casos más difíciles.

## Decisiones derivadas
- Revisar si las variantes delatan la respuesta.
- Buscar casos donde la línea base falle de forma sistemática.
