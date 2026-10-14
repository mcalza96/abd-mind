# ADR-0001 — Acoplarse a Hermes Agent mediante un servidor MCP

**Estado:** aceptada

## Contexto

Construir desde cero un agente conversacional (bucle de herramientas, memoria, manejo de archivos, canal de mensajería, reintentos, programación de tareas) es costoso y no es el aporte del proyecto. El usuario ya opera **Hermes Agent** (Nous Research) en un PC y se comunica con él por Telegram.

Hermes admite varias vías de extensión: herramientas propias, skills (estándar agentskills), plugins y servidores **MCP** (stdio o HTTP, con descubrimiento automático de herramientas).

El marco teórico exige que la selección de hipótesis ocurra fuera del LLM ([06 §6.3](../../marco-teorico/06-arquitectura.md#63-frontera-estocástico--determinista)).

## Decisión

abd-mind se implementa como **servidor MCP independiente**. Hermes lo registra como un servidor MCP más y usa sus herramientas. Una **skill** de Hermes le enseña cuándo y cómo usarlas.

## Alternativas consideradas

| Alternativa | Por qué no |
|---|---|
| Orquestador propio desde cero | Duplica lo que Hermes ya resuelve; el valor del proyecto está en el motor, no en el agente |
| Plugin o herramienta nativa de Hermes (código Python cargado en su proceso) | Acopla el motor a la API interna de Hermes, que cambia entre versiones; el LLM y el cálculo determinista comparten proceso; no reutilizable desde otros agentes ni desde los benchmarks |
| Solo una skill (instrucciones) sin motor | El LLM de Hermes haría todo, incluido puntuar: viola el principio central del marco |

## Consecuencias

- **+** La frontera estocástico/determinista es una frontera de proceso: el LLM de Hermes no puede alterar el cálculo.
- **+** El motor es reutilizable por cualquier cliente MCP (otro agente, un IDE, scripts) y por la CLI de experimentos.
- **+** Las actualizaciones de Hermes rara vez rompen la integración: MCP es un protocolo estable.
- **−** Dos componentes que instalar y configurar en el PC.
- **−** El estado de un caso no puede vivir en memoria del proceso MCP (Hermes puede reiniciarlo): requiere persistencia ([ADR-0007](0007-persistencia-sqlite.md)).
- **−** La calidad del flujo depende del modelo que use Hermes como agente; debe ser bueno siguiendo herramientas.
