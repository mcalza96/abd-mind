# Prueba A/B (EXP-017): instrucciones

Hay dos agentes Hermes en contenedores separados. Deben usar **el mismo modelo**.

| | Agente A | Agente B |
|---|---|---|
| MCP abd-mind | Sí (ya instalado) | **No** |
| MCP abd-oraculo | Sí | Sí |
| Skill | `razonamiento-abductivo` (con el MCP) | `razonamiento-abductivo-sin-mcp`, instalada con el nombre `razonamiento-abductivo` |

Diseño completo: [docs/bitacora/EXP-017](../../bitacora/EXP-017-ab-agente-con-y-sin-mcp.md).

---

## 1. Preparación del agente A (ya tiene abd-mind)

Pégale esto:

> Actualiza abd-mind y agrega el servidor MCP del oráculo para una prueba:
>
> 1. `cd ~/abd-mind && git pull && uv sync`
> 2. Reinstala la skill actualizada: copia `~/abd-mind/hermes/skills/razonamiento-abductivo/` sobre tu skill `razonamiento-abductivo`.
> 3. Registra un segundo servidor MCP llamado `abd-oraculo`, en modo stdio:
>    - comando: `uv --directory <ruta a abd-mind> run abd-mind oraculo`
>    - variables de entorno: `OPENCODE_API_KEY` (desde el entorno, nunca escrita en el archivo) y `ABD_ORACULO_AGENTE=A`
>    - tiempo límite: 600 s
> 4. `hermes mcp test abd-oraculo` debe listar 4 herramientas: `listar_casos`, `ver_caso`, `pedir_observacion` y `concluir`.
> 5. Si es posible, **desactiva tus herramientas de búsqueda web** mientras dure la prueba.
> 6. Reinicia y dime: el modelo que usas, el resultado de los dos `hermes mcp test` y si la web quedó desactivada.

## 2. Preparación del agente B (sin abd-mind)

Pégale esto:

> Prepara el entorno para una prueba de investigación. **No** registres el servidor MCP `abd-mind`: solo el oráculo.
>
> 1. Si no tienes `uv`: `curl -LsSf https://astral.sh/uv/install.sh | sh`.
> 2. `git clone https://github.com/mcalza96/abd-mind.git ~/abd-mind && cd ~/abd-mind && uv sync`
> 3. `mkdir -p ~/.abd-mind && cp config/abd-mind.example.yaml ~/.abd-mind/config.yaml`
> 4. Instala la skill de control con el nombre `razonamiento-abductivo`: copia `~/abd-mind/hermes/skills/razonamiento-abductivo-sin-mcp/SKILL.md` a tu directorio de skills, en `razonamiento-abductivo/SKILL.md`.
> 5. Registra un servidor MCP llamado `abd-oraculo`, en modo stdio:
>    - comando: `uv --directory <ruta a abd-mind> run abd-mind oraculo`
>    - variables de entorno: `OPENCODE_API_KEY` (desde el entorno, nunca escrita en el archivo) y `ABD_ORACULO_AGENTE=B`
>    - tiempo límite: 600 s
> 6. `hermes mcp test abd-oraculo` debe listar 4 herramientas.
> 7. Si es posible, **desactiva tus herramientas de búsqueda web** mientras dure la prueba.
> 8. Reinicia y dime: el modelo que usas, el resultado del `hermes mcp test` y si la web quedó desactivada.

**Antes de seguir:** confirma que los dos agentes usan el mismo modelo.

## 3. La prueba

Envía **exactamente el mismo mensaje** a los dos agentes:

> Prueba de investigación. Usa el servidor `abd-oraculo`. Para cada caso de `listar_casos`, en ese orden:
>
> 1. Lee los hechos con `ver_caso`.
> 2. Investiga la causa aplicando tu método de razonamiento abductivo.
> 3. Pide las observaciones que necesites con `pedir_observacion`, diciendo **qué mirar en concreto**: un registro, una inspección, un ensayo, un documento o una persona. Tienes 8 pedidos por caso. Preguntar por la causa no da información.
> 4. Cuando termines el caso, registra con `concluir`:
>    - el mecanismo causal concreto;
>    - tu confianza de 0 a 1;
>    - las alternativas que sigues considerando posibles.
>
> **Reglas:** no busques en la web, no leas archivos del disco y no mires otras fuentes. Solo usa lo que te entregue el oráculo y tu razonamiento. Trabaja los 11 casos sin pedirme confirmación entre uno y otro. Al final, envíame un resumen de una línea por caso.

## 4. Al terminar

Pídele a cada agente:

> Envíame el archivo `~/.abd-mind/oraculo.jsonl` y, si puedes, el registro de las herramientas que usaste durante la prueba.

Si el agente A usó abd-mind, conviene también:

> Ejecuta `uv run abd-mind casos` y envíame la salida.

Después, pásame los archivos para la evaluación ciega.
