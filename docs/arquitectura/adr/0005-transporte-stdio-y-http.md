# ADR-0005 — Transporte MCP: stdio por defecto, HTTP como opción

**Estado:** aceptada

## Contexto

Hermes corre en un PC del usuario. El cliente MCP de Hermes admite servidores locales (stdio, Hermes lanza el proceso) y remotos (HTTP). El usuario quiere poder usar ambos.

## Decisión

El servidor se implementa con **FastMCP** (en el SDK oficial `mcp` 2.x se llama `MCPServer`) y un solo punto de entrada con dos modos:

```bash
abd-mind serve --transport stdio                  # por defecto
abd-mind serve --transport http --host 127.0.0.1 --port 8765
```

| Modo | Cuándo | Notas |
|---|---|---|
| **stdio** | abd-mind en el mismo PC que Hermes | Hermes gestiona el ciclo de vida del proceso. Sin puertos abiertos. Configuración por defecto |
| **HTTP** | abd-mind en otra máquina (servidor con más recursos, otro PC), o compartido entre varios clientes | Requiere token de acceso (`Authorization: Bearer`) y, fuera de la red local, TLS (proxy inverso). Nunca escuchar en `0.0.0.0` sin token |

El código de herramientas es idéntico en ambos modos; solo cambia el transporte. El estado de los casos está en SQLite ([ADR-0007](0007-persistencia-sqlite.md)), así que ambos modos pueden apuntar a la misma base si comparten disco.

## Consecuencias

- **+** Empezar simple (stdio) sin cerrar la puerta a separar el motor.
- **+** En modo HTTP, el motor puede atender trabajos largos sin depender de que Hermes mantenga vivo un proceso hijo.
- **−** Dos modos que probar. Los tests de integración del servidor corren en ambos.
- **−** En modo HTTP hay superficie de red: token obligatorio, *bind* a `127.0.0.1` por defecto.
