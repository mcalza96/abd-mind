# ADR-0017 — El motor queda como investigación; lo que recibe el agente son skills

**Estado:** aceptada (decisión del usuario, 2026-10-15). Reemplaza el rumbo de producto de [ADR-0001](0001-acoplamiento-hermes-mcp.md) y [ADR-0003](0003-generacion-hibrida.md), sin derogar su contenido técnico.

## Contexto

El objetivo es que el agente no se quede con la respuesta promedio: que tenga el **hábito** de buscar la explicación no obvia y comprobarla ([tesis](../../../marco-teorico/tesis.md)). La pregunta del usuario fue: ¿qué agrega el motor que el agente con sus herramientas no pueda hacer?

Lo que dicen los experimentos:

| Lo que el motor ofrece | Evidencia |
|---|---|
| Verificar con exactitud | Solo en el dominio sintético. En dominios abiertos, el verificador es un LLM indulgente ([EXP-008](../../../bitacora/EXP-008-bench-motor-v01-v02.md)) |
| Puntuar y elegir | En dominios abiertos iguala a un LLM en una llamada o queda debajo ([EXP-010](../../../bitacora/EXP-010-juez-comparativo.md), [EXP-012](../../../bitacora/EXP-012-bench-v2-perturbaciones-y-sin-respuesta.md), [EXP-013](../../../bitacora/EXP-013-seleccion-holistica.md)) |
| Generar candidatas | Los modelos ya generan la causa verdadera cuando los hechos apuntan a ella; fallan al elegir ([EXP-016](../../../bitacora/EXP-016-recuperacion-en-casos-reales.md)) |
| Diversidad de modelos | Hoy hay un solo modelo ([ADR-0002](0002-verificacion-interna.md)) |
| Ser usado por un agente | El agente con el MCP no lo llamó ([EXP-017](../../../bitacora/EXP-017-ab-agente-con-y-sin-mcp.md)). Cuando se le pidió, tardó ~45 min y 99 llamadas para llegar a lo mismo que el agente sin MCP en 2 min ([EXP-018, nota 4](../../../bitacora/EXP-018-fuera-de-la-caja-con-datos.md)) |

Lo que falta no es una capacidad: es una costumbre. Y lo que mejor funcionó fue un agente que, con sus herramientas, puso a prueba la rival por su cuenta.

## Decisión

1. **El motor queda como investigación.** El código, los experimentos, el servidor MCP y sus tests se conservan y siguen pasando. No se desarrollan funciones nuevas para el producto.
2. **La teoría queda intacta.** El marco teórico, los experimentos mentales, los axiomas, los principios, la formalización, el histórico y la bitácora no se modifican por esta decisión. Son la fuente de la que sale el producto.
3. **Lo que recibe el agente son instrucciones:** una skill corta (`hermes/skills/abduccion/`) y unas líneas siempre activas (`hermes/instrucciones-permanentes.md`), destiladas del marco.
4. **Se prueba antes de afirmarlo:** EXP-018 compara el agente sin nada (S0) con el agente con la skill y las líneas siempre activas (S1).

## Consecuencias

- **+** Nada que instalar fuera de Hermes; sin costo de tiempo ni de llamadas; funciona con las herramientas del agente.
- **+** Lo aprendido (disparadores, operadores, contacto, no cerrar sin comprobar la rival) llega al agente en la forma en que puede usarlo.
- **−** Se pierde lo que el motor podría obligar: una skill se puede ignorar. Si EXP-018 muestra que las instrucciones no forman el hábito, se revisa esta decisión (por ejemplo, con un segundo agente que revise antes de responder).
- **−** La parte formal (verificación exacta, puntuación predictiva) deja de estar en el camino del producto. Sigue disponible para investigación.
