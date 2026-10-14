# Despliegue en el PC

Guía para instalar abd-mind junto a Hermes Agent en el PC del usuario. Los comandos de abd-mind existirán cuando se implemente la fase correspondiente de la [hoja de ruta](hoja-de-ruta.md).

> **Verificar contra la versión instalada de Hermes.** La configuración de Hermes cambia entre versiones (en particular, cómo se pasa la clave a un proveedor personalizado). Después de cada cambio, ejecutar `hermes doctor`. Los fragmentos de configuración de Hermes de este documento son orientativos.

## 1. Requisitos

- Python 3.12 y [`uv`](https://docs.astral.sh/uv/).
- Hermes Agent instalado y funcionando con el gateway de Telegram.
- Una clave de **OpenCode Go**.

## 2. Instalar abd-mind

```bash
git clone https://github.com/mcalza96/abd-mind.git
cd abd-mind
uv sync
```

## 3. Configurar abd-mind

### Secretos

`~/.abd-mind/.env` (fuera del repositorio; **nunca** se versiona):

```bash
OPENCODE_API_KEY=...
```

### Configuración

Copiar `config/abd-mind.example.yaml` a `~/.abd-mind/config.yaml`:

```yaml
proveedor:
  base_url: https://opencode.ai/zen/go/v1   # verificar con GET /v1/models
  api_key_env: OPENCODE_API_KEY

roles:                       # nombres reales: consultar `abd-mind modelos`
  cortex:       { modelo: "<modelo-barato>",  temperatura: 0.0 }
  generadores:
    - { modelo: "<modelo-A>", temperatura: 1.0 }
    - { modelo: "<modelo-B>", temperatura: 1.0 }
  verificador:  { modelo: "<modelo-C>",       temperatura: 0.0 }   # distinto de generadores (ADR-0002)

pesos: { alpha: 1.5, beta: 10.0, gamma: 1.0, tau: 11.0 }   # tau provisional: se calibra en la fase 7

presupuestos:
  hipotesis_por_ronda: 5
  hipotesis_vivas_max: 20
  profundidad_expansion: 2
  llamadas_por_operacion: 60
  llamadas_por_caso: 500

almacenamiento:
  sqlite: ~/.abd-mind/abd-mind.db

reglas_dir: ./rules
```

Comprobar:

```bash
uv run abd-mind modelos      # lista modelos disponibles en OpenCode Go
uv run abd-mind doctor       # valida config, clave, reglas y base de datos
uv run abd-mind experimento cilindro   # no usa LLM: debe elegir "cilindro"
```

## 4. Configurar Hermes

### Modelo del agente vía OpenCode Go

Con el asistente interactivo:

```bash
hermes model    # elegir "custom endpoint", base URL https://opencode.ai/zen/go/v1
```

O editando `~/.hermes/config.yaml` (orientativo):

```yaml
model:
  provider: custom
  base_url: https://opencode.ai/zen/go/v1
  default: "<modelo-agente>"   # uno bueno siguiendo herramientas
```

y la clave en `~/.hermes/.env`. Según la versión, Hermes puede exigir que el bloque `model:` referencie explícitamente la variable de entorno de la clave; `hermes doctor` lo indica.

Se recomienda que el modelo del agente sea **distinto** del verificador de abd-mind.

### Registrar el servidor MCP (stdio, recomendado)

```bash
hermes mcp add abd-mind --command "uv --directory /ruta/a/abd-mind run abd-mind serve --transport stdio"
hermes mcp test abd-mind
```

Equivalente en `~/.hermes/config.yaml` (orientativo):

```yaml
mcp_servers:
  abd-mind:
    command: uv
    args: ["--directory", "/ruta/a/abd-mind", "run", "abd-mind", "serve", "--transport", "stdio"]
```

### Alternativa: servidor HTTP

En la máquina del motor:

```bash
ABD_MIND_TOKEN=<token-largo> uv run abd-mind serve --transport http --host 127.0.0.1 --port 8765
```

En Hermes:

```bash
hermes mcp add abd-mind --url http://127.0.0.1:8765/mcp
```

con el encabezado `Authorization: Bearer <token>` según admita la versión de Hermes. Si el motor está en otra máquina, exponerlo detrás de TLS (proxy inverso o túnel) y nunca sin token ([ADR-0005](adr/0005-transporte-stdio-y-http.md)).

### Instalar la skill

Copiar `hermes/skills/razonamiento-abductivo/` al directorio de skills de Hermes (habitualmente `~/.hermes/skills/`) y reiniciar Hermes.

## 5. Prueba de punta a punta

Por Telegram:

> Tengo dos observaciones de un objeto: de frente se ve un rectángulo, desde arriba un círculo. Usa el dominio sintético. ¿Qué objeto es?

Resultado esperado: Hermes abre un caso en el dominio `sintetico`, registra dos observaciones, genera y evalúa, y responde **cilindro** con C=2, sin proponer "óvalo".

## 6. Operación

| Tarea | Comando |
|---|---|
| Ver casos | `uv run abd-mind casos` |
| Exportar auditoría | `uv run abd-mind auditoria <caso_id> --formato markdown` |
| Respaldar | copiar `~/.abd-mind/abd-mind.db` |
| Actualizar reglas | editar `rules/<dominio>.yaml`, commit, `abd-mind doctor` |
| Logs | stderr del proceso MCP (Hermes los registra en modo stdio) |
