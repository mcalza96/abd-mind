# abd-mind

Investigación sobre pensamiento abductivo para agentes de IA. **Objetivo:** que un agente no se quede con la respuesta promedio, sino que busque la explicación no obvia, la compruebe y la distinga de la rebuscada ([tesis](docs/marco-teorico/tesis.md)).

## Qué se le da al agente

- [`hermes/skills/abduccion/SKILL.md`](hermes/skills/abduccion/SKILL.md): el método, en una página.
- [`hermes/instrucciones-permanentes.md`](hermes/instrucciones-permanentes.md): siete líneas para las instrucciones siempre activas de Hermes. Son las que buscan volverlo un hábito.

Se prueba en [EXP-018](docs/bitacora/EXP-018-fuera-de-la-caja-con-datos.md): el mismo agente con y sin estas instrucciones, ante preguntas con datos donde la explicación obvia suele estar equivocada.

**El motor abductivo** (verificación, puntuación y servidor MCP) se construyó y se midió, pero no agregaba nada que un agente con sus herramientas no pudiera hacer, y se quitó ([ADR-0017](docs/historico/arquitectura/adr/0017-motor-como-investigacion-skills-como-producto.md)). Último commit con el motor: `44b51f694420cd3df004428e59c85fb000008c46`.

## Documentación

- [Marco teórico](docs/marco-teorico/README.md): tesis, generación abductiva, principios y formalización (vigente).
- [Bitácora](docs/bitacora/README.md): experimentos, con su registro previo, y lecciones.
- [Experimentos mentales](docs/experimentos-mentales/README.md): las historias y axiomas de los que salen los principios.
- [Histórico](docs/historico/README.md): el marco anterior, la arquitectura y los ADRs del motor, y las skills anteriores.
- [Datos](datasets/abd-bench/README.md): los conjuntos usados en los experimentos.
