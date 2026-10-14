# Arquitectura — abd-mind

Este directorio define **cómo** se construye el sistema descrito en el [marco teórico](../marco-teorico/README.md). Si un documento de aquí contradice al marco teórico, prevalece el marco, salvo que un ADR diga explícitamente lo contrario.

## Índice

| Documento | Contenido |
|---|---|
| [Visión general](#visión-general) (este archivo) | Diagrama, responsabilidades, estructura del repo |
| [Contrato MCP](contrato-mcp.md) | Herramientas que el motor expone a Hermes: entradas, salidas, errores |
| [Interacción por Telegram](interaccion-telegram.md) | Cómo se ve un caso de punta a punta desde el chat |
| [Despliegue en el PC](despliegue-pc.md) | Instalación, configuración de Hermes, OpenCode Go y el servidor MCP |
| [Hoja de ruta](hoja-de-ruta.md) | Fases de construcción con criterios de término |
| [ADR](adr/) | Registro de decisiones de arquitectura |

### Decisiones (ADR)

| # | Decisión |
|---|---|
| [0001](adr/0001-acoplamiento-hermes-mcp.md) | Acoplarse a Hermes Agent mediante un servidor MCP |
| [0002](adr/0002-verificacion-interna.md) | La verificación de virtudes vive dentro del motor |
| [0003](adr/0003-generacion-hibrida.md) | Generación de hipótesis híbrida: Hermes + generadores propios |
| [0004](adr/0004-reglas-solo-lectura.md) | Las reglas del dominio son de solo lectura para el agente |
| [0005](adr/0005-transporte-stdio-y-http.md) | Transporte: stdio por defecto, HTTP como opción |
| [0006](adr/0006-experimentos-sin-hermes.md) | Los experimentos corren sin Hermes |
| [0007](adr/0007-persistencia-sqlite.md) | Persistencia de casos en SQLite |
| [0008](adr/0008-presupuestos-y-trabajos-largos.md) | Presupuestos por caso y trabajos largos |
| [0009](adr/0009-observadores-falibles.md) | Observadores falibles y atribución de error |
| [0010](adr/0010-subdeterminacion.md) | Subdeterminación y abducción activa |
| [0011](adr/0011-veredicto-ternario-y-explananda.md) | Veredicto de tres valores y explananda |
| [0012](adr/0012-pregunta-y-margen.md) | Pregunta del caso y margen de victoria |
| [0013](adr/0013-predicciones.md) | Predicciones y cierre del ciclo |

## Visión general

### Contexto de uso

- **Hermes Agent** corre en un PC del usuario.
- El usuario habla con Hermes por **Telegram** (gateway de mensajería de Hermes).
- Hermes y el motor abductivo usan **OpenCode Go** como proveedor de modelos (API compatible con OpenAI).
- El motor abductivo (**abd-mind**) corre en el mismo PC como servidor MCP. Opcionalmente, en otra máquina vía HTTP ([ADR-0005](adr/0005-transporte-stdio-y-http.md)).

### Diagrama

```
 Usuario ── Telegram ──┐
                       ▼
┌──────────────────────────── PC ─────────────────────────────┐
│ ┌──────────────────────── Hermes Agent ───────────────────┐ │
│ │ gateway Telegram · conversación · memoria · archivos    │ │
│ │ LLM agente (OpenCode Go, proveedor custom)              │ │
│ │ skill: razonamiento-abductivo                           │ │
│ └───────────────────────────┬─────────────────────────────┘ │
│                             │ MCP (stdio)                   │
│ ┌───────────────────────────▼─────────────────────────────┐ │
│ │ abd-mind (servidor MCP)                                 │ │
│ │  interfaces/   mcp_server · cli                         │ │
│ │  engine/       motor de casos (máquina de estados)      │ │
│ │  transition/   deterministic: IBE, árbol de estados     │ │
│ │                stochastic: córtex, generadores          │ │
│ │  organ/        motor de reglas, proyecciones, verificador│ │
│ │  contracts/    modelos Pydantic                         │ │
│ │  SQLite        casos, evidencia, auditoría              │ │
│ └───────────────────────────┬─────────────────────────────┘ │
└─────────────────────────────┼───────────────────────────────┘
                              ▼
                  OpenCode Go (API de modelos)
```

### Principio rector

> **Hermes orquesta, abd-mind decide.**

Hermes resuelve lo genérico de un agente: hablar con el usuario, recibir archivos, recordar contexto, decidir qué herramienta usar. abd-mind resuelve lo específico del razonamiento abductivo y es el único lugar donde se calculan virtudes, scores y derrotas. La frontera es un proceso aparte con un contrato MCP: el LLM de Hermes no tiene forma de alterar el cálculo.

### Responsabilidades

| Responsabilidad | Hermes | abd-mind |
|---|---|---|
| Canal Telegram, conversación, memoria | ✅ | |
| Recibir y leer documentos (PDF, texto) | ✅ | |
| Decidir que un problema requiere abducción | ✅ guiado por la skill | |
| Registrar observaciones con su observador | ✅ invoca | ✅ valida y persiste |
| Separar hechos de opiniones (córtex) | | ✅ |
| Proponer hipótesis | ✅ como un generador más | ✅ generadores propios diversos |
| Verificar $\pi_i(H) \approx y_i$ (→ $C$) | ❌ | ✅ |
| Contar entidades latentes (→ $P$) | ❌ | ✅ |
| Evaluar reglas (→ $K$) | ❌ | ✅ |
| Score, umbral, desempate, $H^*$ | ❌ | ✅ |
| Derrotar / reactivar hipótesis | ❌ | ✅ |
| Explicar el resultado al usuario | ✅ | entrega auditoría estructurada |
| Editar reglas del dominio | ❌ | ❌ (solo el humano, en el repo) |

### Capas de abd-mind

Las dependencias van solo hacia abajo. `contracts` no depende de nada; `transition/deterministic` y `organ/rule_engine` no importan ningún cliente LLM.

| Capa | Ruta | Depende de | IA |
|---|---|---|---|
| Interfaces | `src/factory/interfaces/` | engine | No |
| Motor de casos | `src/factory/engine/` | transition, organ, contracts, persistencia | Indirecta |
| Transición estocástica | `src/factory/transition/stochastic/` | contracts, cliente LLM | Sí |
| Transición determinista | `src/factory/transition/deterministic/` | contracts, organ (reglas, proyecciones) | **No** |
| Órganos | `src/factory/organ/` | contracts | Solo el verificador |
| Contratos | `src/factory/contracts/` | pydantic | No |

### Estructura del repositorio

```
abd-mind/
├── docs/
│   ├── marco-teorico/
│   └── arquitectura/
├── src/factory/
│   ├── config.py               # proveedor, modelos, roles, pesos, presupuestos
│   ├── contracts/
│   │   ├── abduction.py        # HipotesisCandidata, EvaluacionAbductiva
│   │   ├── observation.py      # Observer, Observation, Hecho, Opinion
│   │   └── case.py             # Caso, EstadoHipotesis, Veredicto
│   ├── organ/
│   │   ├── texto.py            # normalización de valores categóricos
│   │   ├── rule_engine.py      # K: reglas duras y blandas
│   │   ├── projections.py      # π computables (entornos sintéticos) y relación ≈
│   │   └── verifier.py         # interfaz Verificador y VerificadorLLM
│   ├── transition/
│   │   ├── deterministic/
│   │   │   ├── ibe_evaluator.py  # Score, umbral, desempate
│   │   │   └── state_tree.py     # derrotabilidad
│   │   └── stochastic/
│   │       ├── llm_client.py     # cliente OpenAI-compatible: chat/responses, SSE, caché
│   │       ├── esquemas.py       # salidas JSON que se piden a los modelos
│   │       ├── contexto.py       # descripción del dominio y del caso para los prompts
│   │       ├── cortex.py         # extracción hechos/opiniones
│   │       └── generator.py      # contrastivo, expansión
│   ├── engine/
│   │   ├── case_service.py     # casos de uso del motor
│   │   └── store.py            # SQLite
│   ├── experiments/            # cilindro, expansión, tercer observador, finanzas
│   └── interfaces/
│       ├── mcp_server.py       # FastMCP
│       └── cli.py              # experimentos, inspección de casos
├── rules/                      # reglas por dominio (YAML), versionadas
├── config/
│   └── abd-mind.example.yaml   # roles → modelos, pesos, presupuestos
├── hermes/
│   ├── skills/razonamiento-abductivo/SKILL.md
│   └── config.example.yaml
└── tests/
    ├── units/
    └── integration/
```

El paquete Python se llama `factory` (diseño `src/`), así que se importa como `from factory.contracts.abduction import ...`. Las instrucciones originales usaban `from src.factory...`; se evita porque convertir `src` en paquete es un antipatrón de empaquetado. Los nombres de módulo y clase son los de la especificación.

### Flujo de un caso

```
crear_caso ──► agregar_observacion (×m) ──► generar_hipotesis / proponer_hipotesis
                                                    │
                                                    ▼
                                                evaluar ──► mejor_explicacion
                                                    ▲              │
                    nueva_evidencia / retractar ────┘              ▼
                                                            auditoria
```

El detalle de cada herramienta está en el [contrato MCP](contrato-mcp.md); la experiencia desde el chat, en [interacción por Telegram](interaccion-telegram.md).

## Trazabilidad con el marco teórico

| Concepto teórico | Implementación |
|---|---|
| $y_i = \pi_{O_i}(S)$ (Postulado 1) | `Observation` exige `observer_id`; `Observer` guarda el marco |
| Invariantes $\mathcal{R}$ (Postulado 2) | `rules/*.yaml` + `organ/rule_engine.py` |
| Expansión ontológica (Postulado 3) | `generator.py` modo `expansion`, disparado por `case_service` |
| $\approx$ por observador (D5) | `organ/projections.py` y `organ/verifier.py` con tolerancia por observador |
| $C$ verificada (D1) | `verifier`/`projections` → `Veredicto` por par $(H, y_i)$ |
| $P$ contrastada (D2) | extracción de entidades + vocabulario $\mathcal{V}$ del caso |
| $K$ estructurada (D3, D4) | predicados estructurados en `rule_engine` |
| Derrotabilidad reversible (D6) | `state_tree.py` |
| Umbral y desempate (D7) | `ibe_evaluator.py` |
| Hechos ≠ opiniones (D8) | `cortex.py` → `Hecho` / `Opinion` |
| Modelos como configuración (D9) | `config/abd-mind.yaml`, `llm_client.py` |
| Línea base (D10) | `src/factory/experiments/` + `cli.py` ([ADR-0006](adr/0006-experimentos-sin-hermes.md)) |
