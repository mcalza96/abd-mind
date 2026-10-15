# abd-mind — guía para agentes

**Qué es:** un motor de razonamiento abductivo, servido por MCP a Hermes Agent, que el usuario usa por Telegram. **Objetivo vigente:** una IA a la que se le ocurran explicaciones no obvias y que sepa distinguirlas de las rebuscadas.

## Qué leer

1. [docs/marco-teorico/README.md](docs/marco-teorico/README.md): tesis, generación, principios y formalización. Es la referencia vigente; son cuatro documentos cortos.
2. [docs/bitacora/README.md](docs/bitacora/README.md): experimentos y lecciones transversales. **Revisar las lecciones antes de diseñar un experimento.**
3. Solo si hace falta:
   - [docs/arquitectura/](docs/arquitectura/README.md): MCP, ADRs, hoja de ruta;
   - [docs/experimentos-mentales/](docs/experimentos-mentales/README.md): las historias de las que salen los principios.

**No leer para trabajar:** `docs/historico/` (versiones anteriores) ni `datasets/abd-bench/fuentes/` (material crudo). Las referencias del código del tipo `NN §x` apuntan a `docs/historico/marco-teorico/`.

## Reglas del proyecto

- **Idioma:** español, en documentos, código y commits.
- **Experimentos:** se registran en la bitácora **antes** de correrlos, con lo que contaría como fracaso. Cada cambio de parámetro hecho después de ver un resultado se declara. Las entradas no se reescriben: se agregan notas.
- **Contra el sobreajuste:** un principio entra al marco solo si una historia o un experimento lo exige. Lo que llega de afuera (investigaciones, agentes) se verifica antes de usarlo.
- **Documentación:** antes de crear un documento nuevo, se amplía uno de los vigentes.
- **Secretos:** la clave del proveedor es `OPENCODE_API_KEY`, inyectada por el entorno. Nunca se escribe en el repositorio. `.env` está ignorado.

## Comandos

```bash
uv sync
uv run pytest
uv run ruff check && uv run ruff format --check && uv run mypy src
uv run abd-mind experimento todos        # experimentos deterministas, sin LLM
uv run abd-mind serve                    # servidor MCP por stdio
```
