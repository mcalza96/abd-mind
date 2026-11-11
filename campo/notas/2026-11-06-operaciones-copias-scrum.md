# 2026-11-06 · operaciones · origen de las copias de scrum-kanban-agents

- **Agente y skills usadas:** Codex; abduccion y red-abductiva.
- **Pregunta:** ¿Por qué hay tantas copias de la skill?
- **Alcance:** rutas de instalación bajo ~/.claude, ~/.agents, ~/.codex, ~/.opencode, ~/.config/opencode y ~/skills; adapters de portafolio-gestion, plugins de portafolio y consumidores de launchd. No es un inventario de todos los discos o respaldos.

## Lo sorprendente

Actualmente hay una instalación de la skill y un alias, pero hay réplicas divergentes de sus adapters dentro del proyecto. Un test de la app inspecciona una réplica distinta de la que ejecutan el plugin y launchd.

## Hipótesis y comprobaciones

| Hipótesis | Familia | Qué la separa | Resultado |
|---|---|---|---|
| Instalaciones completas independientes por agente | Instalación/decisión | Rutas reales y archivos distintos bajo .agents y .claude | Existieron históricamente según los mensajes de coordinación; no son dos instalaciones actuales: .agents es un enlace |
| Todas las copias son enlaces o artefactos equivalentes | Medición | Mismo inode o hashes iguales | Refutada para adapters del repo: cinco archivos comparados difieren |
| Se instalaron plugins copiando archivos y luego se mantuvieron réplicas manuales | Procedimiento | Instrucciones cp/copy, tickets de réplica y fuentes divergentes | Sostenida por README, CAL-25/26/30 y hashes actuales |
| La mudanza de gestión creó por sí sola las variantes | Tiempo | Las réplicas deberían nacer después de la mudanza | Refutada como origen único: ya hay instrucciones de copia anteriores; ORDEN-4/5 trasladó y conservó los archivos |

## Evidencia

1. `ls -ld ~/.agents/skills/scrum-kanban-agents` muestra enlace a `/Users/mcalzadilla/.claude/skills/scrum-kanban-agents`. Ambas rutas resuelven al inode `176483319`; nacimiento del enlace por `lstat`: `2026-11-04T11:15:44.961263-03:00`. No existe `~/.codex/skills/scrum-kanban-agents` en la inspección.
2. El reflog de la instalación canónica contiene literalmente:

```text
11365cf HEAD@{2026-10-21 15:12:05 -0300}: clone: from https://github.com/mcalza96/scrum-kanban-agents
```

3. `portafolio-gestion/inbox/archivo/Director-entrega-2026-11.md`, M-52 (3 de noviembre) reporta divergencia de 24 archivos entre las dos instalaciones; M-65 y M-96 (4 de noviembre) vuelven a pedir unificación. Es evidencia histórica de coordinación, no una remedición actual de esos 24 archivos. El commit canónico `748d4c8` se titula «Adaptador codex en la copia canónica».
4. `~/.claude/skills/scrum-kanban-agents/README.md:78` prescribe copiar inbox.js y guard.js a `.opencode/plugin/` y gestion.js a `.opencode/lib/`. `references/inbox.md:69` también prescribe copiar. CAL-25 y CAL-26 nombran skill y copias del proyecto como lugares de edición. CAL-30 documenta explícitamente replicar wake.py de skill a gestión.
5. Comparación de bytes por Python, abreviando SHA-256 a 16 caracteres:

```text
lanzar.py skill_sha256=c604b1a0d2f44e3a gestion_sha256=fe2d35d1ac611641 iguales=False
wake.py skill_sha256=0e5d985f564b3665 gestion_sha256=f7b9df395eda5154 iguales=False
inbox.js skill_sha256=d4acdb3264e626bf gestion_sha256=33c6676e415b594c iguales=False
guard.js skill_sha256=a1334fe8c79fa6a6 gestion_sha256=79cc192bf0ef466a iguales=False
control.sh skill_sha256=0fce1e72e5f08d82 gestion_sha256=7a52f85ace098f0e iguales=False
```

Los tres archivos instalados de la app (.opencode/plugin/inbox.js, .opencode/plugin/guard.js, .opencode/lib/gestion.js) sí son idénticos a sus fuentes canónicas al medir. La copia de lanzar.py en gestión conserva `MAX_PER_PM = 1` y `MAX_GLOBAL = 4`; la activa tiene máximo global diez sin tope por PM.

6. `portafolio/.opencode/plugin/inbox.js:30–33` resuelve SCRIPT, WAKE y LANZAR desde ~/.claude. `Library/LaunchAgents/cl.jitdata.portafolio.sweep.plist` también ejecuta ese wake.py. Pero `portafolio/lib/wake-bloqueo.test.ts:10` fija WAKE a `/Users/mcalzadilla/portafolio-gestion/adapters/opencode/wake.py`, y su prueba funcional importa ese mismo archivo. Las funciones M-140 que exige existen en la réplica y no aparecieron en la búsqueda del wake canónico. No se ejecutó el test ni se afirmó un incidente de producción: se demostró la diferencia de fuente entre prueba y ejecución.
7. Git de gestión registra importación de adapters en `c49659b` (5 de noviembre). Git de la app registra mudanzas `6c7df139` (ORDEN-4) y `28dc6735` (ORDEN-5); no equivalen a una nueva instalación de la skill.

## Conclusión

Confianza alta en el mecanismo: dos instalaciones históricas divergentes, luego unificadas por enlace, más una estrategia de instalación de adapters por copia y mantenimiento manual de réplicas que las mudanzas conservaron. No hay evidencia de que la ejecución actual cree clones completos nuevos. La divergencia se mantiene porque algunos consumidores ejecutan la fuente canónica mientras otros tests y tickets siguen tomando la réplica del proyecto como referencia.

No se identificó el comando original que creó la antigua instalación de .agents ni se atribuye su autoría. Una automatización de sincronización no inspeccionada o consumidores adicionales podrían cambiar el inventario; no cambian los hashes ni las rutas observadas en esta medición. No se modificaron instalaciones, consumidores ni pruebas durante este diagnóstico.

## Predicciones

Ninguna: la conclusión explica historia y estado observado; no proyecta una remediación todavía no acordada.

## Lo que aprendí del método

Contar carpetas daba una explicación equivocada: el enlace reduce dos rutas a una instalación. La comprobación que decide el riesgo es seguir desde el proceso y el test hasta el archivo real. Un test puede proteger una réplica obsoleta sin proteger el runtime; la igualdad de nombres no demuestra igualdad de código.
