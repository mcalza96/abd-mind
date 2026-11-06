# 2026-11-06 · operaciones · un lector de buzones no es su destinatario

- **Agente y skills:** Codex; abduccion, red-abductiva, scrum-kanban-agents.
- **Pregunta:** revisar wake, inbox y guard después de centralizar su implementación.

## Lo sorprendente

El runtime registraba despertares de varios PMs hacia una misma sesión titulada
PM-auditoria relevo. Leer o confirmar un mensaje no demostraba que hubiera llegado
al responsable correcto.

## Hipótesis

| Hipótesis | Familia | Predicción separadora | Resultado |
|---|---|---|---|
| El selector confunde lectura con identidad cuando falta TO | Mecanismo | Primer prompt Eres PM-auditoria reconocido como None; el mismo selector devuelve auditor para otras lanes | Confirmada |
| Solo están mal los logs | Medición | La consulta directa devolvería sesiones correctas | Refutada por find_session directo |
| Los IDs repetitivos prueban que eran fixtures de tests | Selección | No habría actividad real del modelo ni herramientas | No sustentada: los IDs no prueban origen; sí hay turnos y herramientas del runtime. No se afirma quién eligió esos IDs |
| Se decidió usar una sesión como varios PMs | Decisión | La identidad inicial sería múltiple o distinta del auditor | No sustentada por el primer prompt, que declara únicamente PM-auditoria |

## Evidencia

Primer texto del usuario, consultado en session_message de la DB real en modo
solo lectura:

```text
"Eres PM-auditoria. Ejecuta: python3 /Users/mcalzadilla/.claude/skills/scrum-kanban-agents/scripts/inbox.py read /Users/mcalzadilla/portafolio-gestion/inbox PM-auditoria"
```

La versión anterior solo reconocía TO al inicio y devolvía None para ese texto.
En una misma transacción de lectura, comparando selector anterior y corregido:

```text
PM-calidad: ses_eeeeeeeeeeeeeeeeeeeeeeee -> ses_bbbbbbbbbbbbbbbbbbbbbbbb
PM-nucleo: ses_eeeeeeeeeeeeeeeeeeeeeeee -> ses_cccccccccccccccccccc0001
PM-superficie: ses_eeeeeeeeeeeeeeeeeeeeeeee -> ses_111111111111111111111111
PM-auditoria: ses_eeeeeeeeeeeeeeeeeeeeeeee -> ses_eeeeeeeeeeeeeeeeeeeeeeee
PO: ses_e5e10e6feffeiWJXvJOn4JAusW -> ses_e5e10e6feffeiWJXvJOn4JAusW
```

El test nuevo de enrutamiento falla antes (`None != PM-auditoria`) y pasa después.
El cambio reconoce Eres PM, Director o PO únicamente al abrir el primer prompt;
no convierte menciones posteriores ni instrucciones de ejemplo en identidad.
Commit de skill: ad17dd3. El informe operativo conserva logs completos.

## Conclusión

Confianza alta en esta causa concreta: el primer prompt real reproduce el defecto,
y cambiar únicamente su reconocimiento cambia el destino en la misma DB sin
escribir en ella. No demuestra que todos los formatos posibles de identidad estén
cubiertos ni que la recepción implique una respuesta correcta del PM.

## Predicciones

Ninguna: conclusión sobre un defecto observado y comparación ejecutada; no se
predice el cumplimiento futuro de los agentes.

## Lo que aprendí del método

Un ID con apariencia artificial no basta para declarar contaminada la medición.
El dato decisivo fue el texto inicial real, junto con el selector ejecutado sobre
una misma instantánea. Tampoco basta probar identidad TO con fixtures cuando los
prompts de relevo operativos usan Eres: hay que contrastar las convenciones reales.
