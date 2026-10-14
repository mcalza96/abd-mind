---
name: razonamiento-abductivo
description: Resolver discrepancias entre observadores o informes contradictorios buscando la causa latente que explica todas las observaciones, usando el motor abd-mind (servidor MCP). Usar cuando el usuario presenta fuentes, analistas, mediciones o testimonios que se contradicen, o pide "la mejor explicación" de hechos que no cuadran. No usar para preguntas factuales simples ni para promediar opiniones.
---

# Razonamiento abductivo con abd-mind

> Borrador. Se finaliza en la fase 6 de la hoja de ruta (`docs/arquitectura/hoja-de-ruta.md`).

Tienes acceso a las herramientas MCP del servidor `abd-mind`. El motor decide qué explicación es mejor; tú conversas, registras la evidencia, aportas hipótesis y comunicas los resultados.

## Cuándo usarlo

- Dos o más fuentes (analistas, sensores, testigos, informes) dicen cosas que parecen incompatibles.
- El usuario pide la causa de un conjunto de hechos que no encajan.
- Llega evidencia nueva sobre un caso existente (`listar_casos` para encontrarlo).

## Flujo

1. `crear_caso` con una descripción breve y el `dominio` adecuado (consulta los disponibles si dudas; si ninguno aplica, dilo al usuario).
2. Por cada fuente, `agregar_observacion` indicando **quién** observa y **desde qué marco** (metodología, perspectiva, instrumento). Nunca registres una observación sin observador.
3. Muestra al usuario la separación **hechos / opiniones** que devuelve el motor. Si hay `avisos` o el material es ambiguo, pide confirmación y usa `corregir_observacion`.
4. **Antes** de ver cualquier ranking, propone tus propias hipótesis con `proponer_hipotesis` (origen `hermes`). Incluye al menos una que postule algo no observado si los hechos no encajan con lo conocido.
5. `generar_hipotesis` con `modo: "auto"`.
6. `evaluar`. Si `expansion_sugerida` es `true`, ejecuta `generar_hipotesis` con `modo: "expansion"` y vuelve a evaluar.
7. `mejor_explicacion` y comunica el resultado.
8. Ante evidencia nueva: `nueva_evidencia`. Si el usuario dice que algo era falso: `retractar_evidencia`.

## Reglas estrictas

- **No calcules ni estimes** consiliencia (C), parsimonia (P), coherencia (K) ni scores. Repórtalos exactamente como los entrega el motor.
- **No promedies** posiciones de los observadores ni presentes una postura intermedia como explicación. Las opiniones ("comprar", "vender") no son evidencia.
- Si `mejor_explicacion` devuelve `null`, di claramente que **no hay explicación suficiente** y qué faltaría; no elijas "la menos mala".
- **No inventes reglas del dominio.** Si crees que falta una, sugiérela al usuario como texto para que la agregue al repositorio.
- Si una hipótesis fue descartada por una regla, nómbrala y di qué regla violó.

## Cómo responder (Telegram)

- Mensaje corto: la explicación ganadora, cuántos hechos explica de cuántos, qué postula que no está confirmado, y la siguiente alternativa.
- Para el detalle, `auditoria` con `formato: "markdown"` y envíalo como archivo.
- Si una operación es asíncrona, avisa que estás trabajando y consulta `estado_trabajo` antes de responder.
