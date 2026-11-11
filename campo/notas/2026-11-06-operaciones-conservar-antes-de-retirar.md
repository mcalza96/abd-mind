# 2026-11-06 · operaciones · comprobar el guardado antes de retirar

- **Agente y skills:** Codex; abduccion, red-abductiva, scrum-kanban-agents.
- **Pregunta:** revisar archivar, stale_worktrees y gestion sin sobreingeniería.

## Lo sorprendente

Una rama conserva/... creada con éxito no demostraba que contuviera los archivos
nuevos del worktree. Un test con fallo de git add retiraba el entorno y anunciaba
guardado, aunque el archivo nuevo no estaba en el árbol conservado.

## Hipótesis

| Hipótesis | Familia | Predicción separadora | Resultado |
|---|---|---|---|
| Se ignora un fallo previo al guardado | Mecanismo | Con add fallido, write-tree puede devolver HEAD y branch puede tener éxito | Confirmada con fixture real Git y fallo de add inyectado |
| Es solo un mensaje de salida incorrecto | Medición | El archivo seguiría presente o conservado | Refutada: desaparece del worktree y no se añadió al árbol |
| Git pierde archivos aun con comandos correctos | Instrumento | Todos los códigos serían cero antes de la pérdida | No explica la reproducción: add devuelve 128 y no se valida |
| El archivo se excluye por decisión de ignorados | Decisión | Estaría bajo una regla de .gitignore | Refutada en el fixture: nuevo.txt no está ignorado |

## Evidencia

Antes del fix, test_error_al_guardar_no_borra_el_worktree falla; la salida de reap:

```text
removed .../fallo-guardado (dirty) saved as conserva/wt-fallo-guardado ...
```

La línea anterior muestra solo la forma del mensaje; las rutas y hashes literales
están en el artefacto primario:
`/Users/mcalzadilla/portafolio-gestion/epic-calidad/reports/evidencia-archivado-seguro/worktrees-antes.log`.
La assertion comprueba la existencia del archivo y resulta False. No se afirma que
haya ocurrido una pérdida histórica en el repo operativo.

En otra reproducción determinista, un archivador reescribe una instantánea antigua
mientras otro escritor agrega un ticket, directiva o línea de log: la nueva entrada
no sobrevive en archivo vivo ni archivado. Un rename atómico no resolvería esa
actualización perdida. El dueño decidió dejar STATUS/focus como archivado manual;
los escritores conocidos del log comparten flock.

Commit de skill instalado: 825ef07. Suite final: 186 tests, OK. El informe operativo
conserva reproducciones, resultados previos y posteriores, decisión y límites.

## Conclusión

Alta confianza en estos mecanismos reproducidos. El último paso exitoso de una
cadena no certifica los pasos previos. Hay que inspeccionar la postcondición que
importa —archivo recuperable— y no solo la existencia de una rama o un exit final.

## Predicciones

Ninguna: se documentan defectos y comprobaciones ejecutadas, sin pronóstico futuro.

## Lo que aprendí del método

Una falla inyectada permite separar pérdida posible de incidente histórico: muestra
el mecanismo sin inventar evidencia de que ya ocurrió. Para los editores concurrentes,
el problema necesitó una decisión de política del dueño, no otro candado unilateral.
