# 2026-10-19 · taller-mec · por qué 2 consultas hipot quedaron sin respuesta y 1 parcial

- **Agente y skills usadas:** Hermes (Bender), abduccion + red-abductiva
- **Pregunta:** causas de MTC2-041/042 sin respuesta y MTC2-043 parcial (hipot MT 6600 V, 13-10), para mejorar el flujo

## Lo sorprendente

Hernán preguntó lo mismo 3 veces con otras palabras (voltaje → tiempo → voltaje aconsejado).
Las respuestas correctas SÍ se dieron en el chat (14,2 kV fábrica / 8,5-10 terreno; 1 min; 10 kV).
Pero en el registro MTC2-041 y 042 quedaron `abierta` sin respuesta, y MTC2-043 quedó
`respondida` sin `Fuente:`. El conocimiento estaba; el trámite no se cerró.

## Hipótesis

| Hipótesis | Familia | Qué predecía distinto | Resultado de la comprobación |
|---|---|---|---|
| H-obvia: el agente respondió pero no cerró el trámite en el registro | una decisión (procedimiento) | el contenido existe en chat pero falta en el registro | CONFIRMADA: respuestas en sesión 20261013_142635_385a4b92, registro vacío |
| H-rival: falta de conocimiento (no sabía los valores) | nada que explicar / tasa base | los valores del chat serían inventados o errados | DESCARTADA: auditoría verificó 14,2 kV = D1 exacto, 8,5-10 envuelve 65 % reacondicionado (~9,2 kV) |
| H-rival: la fuente normativa no estaba disponible el 13-10 | la medición (instrumento ausente) | umbrales.md D1/D4/D6 creado después del 13-10 | DESCARTADA: `fichas-taller/umbrales.md` verificado textual 2026-10-08 (D1, D4, D6 con cita AR100) |
| H-rival: el gate de fuente bloqueó el registro | el umbral (regla que cambia el efecto) | 043/044 sin `Fuente:` porque el gate la exigía y no estaba a mano | PARCIAL: compatible con 043/044, pero no explica 041/042 abiertas (el `add` no exige fuente) |

## Evidencia

- Sesión `20261013_142635_385a4b92`: respuestas literales en chat —
  "Para 6600 V: hipot AC de fábrica 14,2 kV (2xUn+1 kV, 1 min). En terreno se usa 60-75% de eso,
  o sea unos 8,5 a 10 kV" ; "1 minuto a pleno voltaje" ; "Para ese motor en terreno: 10 kV AC
  por 1 minuto. Si es usado con aislación dudosa, baja a 8,5 kV."
- Registro: MTC2-041 `abierta` respuesta `""`; MTC2-042 `abierta` respuesta `""`;
  MTC2-043 `respondida` sin fuente; MTC2-044 `respondida` sin fuente.
- `fichas-taller/umbrales.md`: D1 (1000+2V, Tabla 4-4), D4 (65 % reacondicionado, §4.4.1.2),
  D6 (80 % post-rebobinado, §4.4.1.1), verificados 2026-10-08.
- MTC2-043 parcial: cifras certeras pero omitió condiciones (aprobación del cliente + IR
  antes/después, AR100 §4.2/§4.4) — error de completitud, no de valor.

## Conclusión

Causa: el agente contestó bien en el chat pero no ejecutó el cierre administrativo en el mismo
turno (responder + fuente). La tabla normativa existía desde 5 días antes, así que no fue falta
de fuente. Confianza alta (0,85). Lo que la cambiaría: evidencia de que el registro se editó o
truncó después (no hay indicios).

## Predicciones

- P-20261019-01

## Lo que aprendí del método

La familia "una decisión o un motivo" (paso 3 de abduccion) fue la que resolvió: el fallo no
estaba en el mundo (valores) ni en el instrumento (tabla), sino en el procedimiento del propio
agente. Faltó una comprobación explícita en la skill de registro: "responder en chat +
responder en registro son una sola transacción". Propuesta: agregar esa regla a la skill
`registro-consultas-taller-mec` (requiere OK del usuario).
