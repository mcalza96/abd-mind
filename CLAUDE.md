# abd-mind — guía para agentes

**Qué es:** investigación sobre pensamiento abductivo para agentes de IA. **Objetivo vigente:** que el agente (Hermes, que el usuario usa por Telegram) no se quede con la respuesta promedio: que tenga el **hábito** de buscar la explicación no obvia, comprobarla, y distinguirla de la rebuscada.

**Lo que se entrega al agente son instrucciones, no código:** la skill [`hermes/skills/abduccion/`](hermes/skills/abduccion/SKILL.md) y las líneas siempre activas de [`hermes/instrucciones-permanentes.md`](hermes/instrucciones-permanentes.md). El motor abductivo y su servidor MCP se quitaron del repositorio ([ADR-0017](docs/historico/arquitectura/adr/0017-motor-como-investigacion-skills-como-producto.md)); el último commit con el motor es `44b51f694420cd3df004428e59c85fb000008c46`.

## Qué leer

1. [docs/marco-teorico/README.md](docs/marco-teorico/README.md): tesis, generación, principios y formalización. Es la referencia vigente; son cuatro documentos cortos. De aquí sale la skill.
2. [docs/bitacora/README.md](docs/bitacora/README.md): experimentos y lecciones transversales. **Revisar las lecciones antes de diseñar un experimento.** El experimento en curso es [EXP-018](docs/bitacora/EXP-018-fuera-de-la-caja-con-datos.md).
3. Solo si hace falta: [docs/experimentos-mentales/](docs/experimentos-mentales/README.md), las historias y axiomas de los que salen los principios.

**No leer para trabajar:** `docs/historico/` (marco anterior, arquitectura y ADRs del motor, skills anteriores) ni `datasets/abd-bench/fuentes/` (material crudo).

## Reglas del proyecto

- **Idioma:** español, en documentos y commits.
- **La teoría no se modifica sin pedido del usuario:** marco teórico, experimentos mentales, axiomas, histórico y bitácora.
- **Experimentos:** se registran en la bitácora **antes** de correrlos, con lo que contaría como fracaso. Cada cambio de parámetro hecho después de ver un resultado se declara. Las entradas no se reescriben: se agregan notas.
- **EXP-018 en curso:** la clave y los generadores de los casos los guarda el usuario. No los busques ni los reconstruyas; en el repositorio solo está su SHA-256.
- **Contra el sobreajuste:** un principio entra al marco solo si una historia o un experimento lo exige. Lo que llega de afuera (investigaciones, agentes) se verifica antes de usarlo. La skill no se ajusta mirando los casos de prueba.
- **La skill es corta:** una página como máximo. Lo que no cabe, va al marco.
- **Documentación:** antes de crear un documento nuevo, se amplía uno de los vigentes.
- **Secretos:** nunca se escriben claves en el repositorio. `.env` está ignorado.
