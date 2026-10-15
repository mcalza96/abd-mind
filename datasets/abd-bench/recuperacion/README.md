# Recuperación en casos reales (EXP-016)

Datos fijados **antes** de generar ([EXP-016](../../../docs/bitacora/EXP-016-recuperacion-en-casos-reales.md)):

- `casos.jsonl`: los 15 casos del conjunto R saneados con las reglas registradas. `quitadas` lista cada observación quitada y la razón; `fuera` marca los casos que quedaron con menos de dos observaciones.
- `elementos.json`: los elementos clave y el núcleo de cada mecanismo. Los escribió un agente sin contexto que solo vio la resolución.
- `inferibilidad.json`: qué tan inferible es cada elemento desde las observaciones, y si el caso es trivial. Lo calificó otro agente sin contexto, que vio las observaciones y los elementos, pero no la resolución.

Se agregan al correr:

- `generaciones.jsonl`: las listas de explicaciones.
- `juicios.jsonl`: las decisiones del juez ciego.
- `informe.md`: las métricas.
