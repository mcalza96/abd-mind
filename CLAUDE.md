# abd-mind — guía para agentes

**Qué es:** una familia de skills de pensamiento abductivo, la teoría de la que salen y el registro de lo que se aprende al usarlas. **Objetivo vigente:** que el agente (Hermes, que el usuario usa por Telegram) no se quede con la respuesta promedio: que tenga el **hábito** de buscar la explicación no obvia, comprobarla, y distinguirla de la rebuscada.

**Lo que se entrega al agente son instrucciones, no código:** las skills estables de [`hermes/skills/`](hermes/skills/) y las líneas siempre activas de [`hermes/instrucciones-permanentes.md`](hermes/instrucciones-permanentes.md). El motor abductivo y su servidor MCP se quitaron del repositorio ([ADR-0017](docs/historico/arquitectura/adr/0017-motor-como-investigacion-skills-como-producto.md)); el último commit con el motor es `44b51f694420cd3df004428e59c85fb000008c46`.

## Qué leer

1. [README.md](README.md): la organización y el ciclo del conocimiento (marco → skills → campo → patrones → experimento → marco).
2. [docs/marco-teorico/README.md](docs/marco-teorico/README.md): tesis, generación, principios y formalización. Es la referencia vigente; son cuatro documentos cortos. De aquí salen las skills.
3. [docs/bitacora/README.md](docs/bitacora/README.md): experimentos y lecciones transversales. **Revisar las lecciones antes de diseñar un experimento.** El experimento en curso es [EXP-018](docs/bitacora/EXP-018-fuera-de-la-caja-con-datos.md).
4. Para escribir en `campo/` o `taller/`: sus README tienen las plantillas y las reglas.
5. Solo si hace falta: [docs/experimentos-mentales/](docs/experimentos-mentales/README.md), las historias y axiomas de los que salen los principios.

**No leer para trabajar:** `docs/historico/` (marco anterior, arquitectura y ADRs del motor, skills anteriores) ni `datasets/abd-bench/fuentes/` (material crudo).

## Contribuir: PR del agente, revisión del usuario

Los agentes son **contribuidores**: todo aporte entra por un pull request que el usuario revisa. Nunca se escribe directo en `main`. Detalle en el [README](README.md#contribuir-los-agentes-abren-pr-el-usuario-revisa).

| Carpeta | Un agente abre PR por su cuenta para | Solo si el usuario lo pidió |
|---|---|---|
| `campo/` | Notas de campo, predicciones, resoluciones de predicciones vencidas, patrones `candidato` | Aceptar un patrón |
| `taller/` | Propuestas de skills | Crear un borrador, cambiar de estado una skill |
| `hermes/` | Nada | Todo: es lo que se instala |
| `docs/` y `datasets/` | Nada | Todo |

- **Una rama y un PR por tema**, con nombre `agente/<nombre-del-agente>/<tema>`, usando la [plantilla de PR](.github/pull_request_template.md).
- **Sin acceso de escritura:** se le entregan al usuario los archivos listos.

## Reglas del proyecto

- **Idioma:** español, en documentos y commits.
- **La teoría no se modifica sin pedido del usuario:** marco teórico, experimentos mentales, axiomas, histórico y bitácora.
- **Experimentos:** se registran en la bitácora **antes** de correrlos, con lo que contaría como fracaso. Cada cambio de parámetro hecho después de ver un resultado se declara. Las entradas no se reescriben: se agregan notas.
- **EXP-018 en curso:** la clave y los generadores de los casos los guarda el usuario. No los busques ni los reconstruyas; en el repositorio solo está su SHA-256. La skill `abduccion` y las instrucciones permanentes tienen su SHA-256 registrado: no se tocan hasta cerrar EXP-018, y no se instala nada del taller mientras corre.
- **Contra el sobreajuste:** un principio entra al marco solo si una historia o un experimento lo exige. Lo que llega de afuera (investigaciones, agentes, notas de campo) se verifica antes de usarlo. Ninguna skill se ajusta mirando los casos de su propia prueba.
- **Las skills son cortas:** una página como máximo. Extienden a `abduccion` sin repetirla. Lo que no cabe, va al marco.
- **El campo se agrega, no se reescribe:** una nota equivocada se corrige con otra que la enlaza. Lo predicho no se edita al resolver.
- **Entrega:** en una rama y con PR que revisa el usuario, nunca directo a `main`.
- **Documentación:** antes de crear un documento nuevo, se amplía uno de los vigentes.
- **Secretos y privacidad:** nunca se escriben claves en el repositorio (`.env` está ignorado), ni datos de terceros o posiciones del usuario sin su pedido.
