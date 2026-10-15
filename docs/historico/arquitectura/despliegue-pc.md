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

Copiar `config/abd-mind.example.yaml` a `~/.abd-mind/config.yaml` (o apuntar `ABD_MIND_CONFIG` a otro archivo) y ajustar. Si no existe ninguno, se usa el ejemplo del repositorio. Lo que define:

- `proveedor`: `base_url` (`https://opencode.ai/inference/go/v1`) y la variable de entorno de la clave.
- `modelos`: por cada modelo, endpoint (`chat` o `responses`), modo de salida JSON (`json_schema` o `json_object`) y `streaming`. La tabla de endpoints está en la documentación de OpenCode Go.
- `roles`: córtex, generadores, verificador (distinto de los generadores, ADR-0002) y modelos de línea base.
- `pesos`, `presupuestos` y `cache_dir` (caché de respuestas para reproducir experimentos).

Particularidades de OpenCode Go que el cliente ya maneja:

- Exige un encabezado `x-opencode-session` estable por conversación y un user agent propio.
- La pasarela corta a los ~30 s las respuestas **sin streaming**: los modelos que razonan largo necesitan `streaming: true`.
- DeepSeek V4.1 Flash no acepta `json_schema`; usar `json_object`.
- Los modelos *Contributor* (p. ej. Muse Spark) **usan los datos para entrenamiento** y no tienen retención cero, según la tabla de privacidad de OpenCode Go. No enviarles información confidencial; para documentos sensibles, asignar esos roles a modelos sin entrenamiento.
- OpenCode Go está pensado para agentes de programación y monitorea el tráfico; el volumen del motor (muchas verificaciones cortas) puede requerir otro proveedor para benchmarks grandes.

Comprobar:

```bash
uv run abd-mind modelos      # lista modelos disponibles en OpenCode Go
uv run abd-mind doctor       # valida config, reglas y acceso a cada modelo configurado
uv run abd-mind experimento todos      # no usa LLM: cilindro, expansion, tercer-observador
uv run abd-mind experimento cilindro-llm   # hipótesis generadas por LLM + línea base
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

`hermes mcp test` debe listar 17 herramientas (de `crear_caso` a `auditoria`).

**Tiempo límite.** En dominios con LLM, `evaluar` y `generar_hipotesis` pueden tardar varios minutos: cada hipótesis se verifica contra cada hecho. Como referencia, el caso financiero completo hizo 42 llamadas en unos 5 minutos. Sube el tiempo límite de llamada a herramientas de Hermes para este servidor, por ejemplo a 600 s. Si es corto, Hermes corta la llamada, aunque el motor guarda los veredictos ya obtenidos y repetir la operación no los vuelve a pagar.

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
python3 -c "import secrets; print(secrets.token_urlsafe(32))"   # generar un token (≥ 16 caracteres)
ABD_MIND_TOKEN=<token> uv run abd-mind serve --transport http --host 127.0.0.1 --port 8765
```

Sin `ABD_MIND_TOKEN` el servidor no arranca. Toda petición sin `Authorization: Bearer <token>` recibe 401. El endpoint es `/mcp` (Streamable HTTP).

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
