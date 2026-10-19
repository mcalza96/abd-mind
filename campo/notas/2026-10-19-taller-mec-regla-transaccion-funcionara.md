# 2026-10-19 · taller-mec · ¿funcionará la regla chat+registro como transacción única?

- **Agente y skills usadas:** Hermes (Bender), abduccion + red-abductiva
- **Pregunta:** ¿la mejora 1 (responder en chat + `responder --fuente` en el mismo turno) realmente
  evitará que se repitan MTC2-041/042/043?

## Lo sorprendente

La skill de registro YA dice "registrar siempre, en el mismo turno" (regla 3) y el script YA
rechaza `respondida` sin fuente (verificado: `responder --id MTC2-041 --respuesta "prueba"`
devuelve `ok:false`). Aun así, 041/042 quedaron abiertas y 043/044 sin fuente. La regla escrita
no bastó una vez; ¿por qué bastaría reescribirla?

## Hipótesis

| Hipótesis | Familia | Qué predecía distinto | Resultado de la comprobación |
|---|---|---|---|
| H-obvia: agregar la regla "transacción única" a la skill sí funcionará | — | las fallas son por falta de regla explícita | CONTRA: la regla ya existe (regla 3, "en el mismo turno") y falló igual. Agregar texto no cambia el mecanismo |
| H-rival: el fallo fue temporal, no estructural (el gate nació el 13-10, mismo día) | el tiempo (el orden no es el que parece) | fallas concentradas antes/después del gate, no después | A FAVOR: plugin creado 2026-10-13 15:10; las 4 consultas hipot son del 13-10 (sesión 14:26, pre-gate). Post-gate (045, 047): el audit muestra `accion: pasar` con fuente trazable. 0 fallas del mismo tipo desde el 16-10 |
| H-rival: lo que funciona no es la regla sino el mecanismo (script rechaza + gate retiene) | el umbral (la regla cambia el efecto) | con mecanismo activo, el registro se cierra solo o se bloquea; sin él, depende de memoria | A FAVOR: `responder` sin fuente → exit 1 verificado hoy. El gate retiene respuestas sin fuente antes de entregar. Doble red mecánica, no textual |
| H-rival: selección — solo vemos las fallas porque alguien auditó | la selección | habría más fallas no detectadas sin auditoría | A FAVOR parcial: 25/50 abiertas, pero 22 son del 02-10 (carga inicial histórica, no fallas de flujo). Las 2 del 13-10 sí son del flujo |
| H-rival: el agente futuro ignorará la skill igual que antes | una decisión | la skill no se lee en el turno | NEUTRA: no comprobable sin observar; pero el gate es código que corre siempre, no depende de lectura |

## Evidencia

- `registro-consultas-taller-mec` regla 3: "Registrar siempre, en el mismo turno" (ya existía).
- `responder --id MTC2-041 --respuesta "prueba"` → `{"ok": false, "error": "gate de fuente: ..."}`
  (mecanismo activo, verificado 2026-10-19).
- `fuente_gate_audit.jsonl`: MTC2-045 y 047 con `accion: pasar`, fuente trazable (post-gate ok).
- `plugin.yaml` del gate: 2026-10-13 15:10. Consultas hipot: 2026-10-13 14:26 (pre-gate).
- Stats: 25 abiertas, pero 22 son carga inicial del 02-10; solo 041/042 son fallas de flujo vigentes.

## Conclusión

La mejora 1 como "agregar regla a la skill" probablemente NO funcionará: la regla ya estaba escrita
y falló. Lo que sí funciona es el mecanismo (script rechaza + gate retiene), que nació el mismo
13-10 y desde entonces 0 fallas del mismo tipo. La mejora real no es texto nuevo sino cerrar el
hueco que el mecanismo no cubre: 041/042 quedaron `abierta` con respuesta vacía porque el `add`
inicial no exige respuesta — el agente respondió en chat y nunca llamó a `responder`. Confianza
media-alta (0,7): se apoya en solo 2 casos post-gate observados.

Qué la cambiaría: una falla nueva del mismo tipo (respuesta en chat sin `responder`) con el gate
activo; eso refutaría H-mecanismo.

## Predicciones

- P-20261019-14

## Lo que aprendí del método

La pregunta "¿qué otra cosa produciría exactamente estos mismos datos?" (paso 3) llevó a H-tiempo:
las fallas son pre-gate, no un problema vigente. La comprobación barata que más separó fue la fecha
del plugin vs la fecha de las consultas (paso 5). Sin ir a mirar eso, habría propuesto texto
redundante. Lección: ante "agregar regla", primero verificar si la regla ya existe y qué mecanismo
la respalda.
