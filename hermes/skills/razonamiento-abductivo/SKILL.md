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

1. `crear_caso` con una descripción breve y el `dominio` adecuado (consulta los disponibles si dudas; si ninguno aplica, dilo al usuario). Si el usuario pregunta algo con alternativas ("¿estructural o transitoria?", "¿A o B?"), declara la `pregunta` con sus valores, incluido uno mixto si cabe.
2. Por cada fuente, `agregar_observacion` indicando **quién** observa y **desde qué marco** (metodología, perspectiva, instrumento). Nunca registres una observación sin observador. Marca con `rol: "explanandum"` lo que el usuario quiere entender (p. ej. la caída del precio) y con `rol: "evidencia"` lo que reúnes para decidir.
3. **Busca evidencia para cada alternativa**, no solo para la que parece obvia: antes de evaluar, intenta encontrar hechos que favorecerían a cada valor de la pregunta.
4. Muestra al usuario la separación **hechos / opiniones** que devuelve el motor. Si hay `avisos` o el material es ambiguo, pide confirmación y usa `corregir_observacion`.
5. **Antes** de ver cualquier ranking, propone tus propias hipótesis con `proponer_hipotesis` (origen `hermes`). Cada una debe fijar la variable de la pregunta y traer `predicciones` con horizonte. Incluye al menos una que postule algo no observado si los hechos no encajan con lo conocido.
6. `generar_hipotesis` con `modo: "auto"`.
7. `evaluar`. Si `expansion_sugerida` es `true`, ejecuta `generar_hipotesis` con `modo: "expansion"` y vuelve a evaluar.
8. `mejor_explicacion`. Si la respuesta no está determinada o es `fragil`, ejecuta `sugerir_observacion` y busca esas observaciones antes de concluir, o preséntalas al usuario.
9. Si hay `que_vigilar` con horizonte, ofrece programar una revisión (cron) para esa fecha. Al vencer, registra lo ocurrido con `nueva_evidencia`.
10. Ante evidencia nueva: `nueva_evidencia`. Si el usuario dice que algo era falso: `retractar_evidencia`. Cuando se sepa qué pasó realmente, `cerrar_caso` con `verdad`, indicando la `fuente`. Debe ser una fuente independiente de los observadores del caso; si no lo es, avísale al usuario. Si después aparece una versión distinta, `registrar_verdad`: no se borra la anterior.

## Reglas estrictas

- **No calcules ni estimes** consiliencia (C), parsimonia (P), coherencia (K) ni scores. Repórtalos exactamente como los entrega el motor.
- **No promedies** posiciones de los observadores ni presentes una postura intermedia como explicación. Las opiniones ("comprar", "vender") no son evidencia.
- Si `mejor_explicacion` devuelve `null`, di claramente que **no hay explicación suficiente** y qué faltaría; no elijas "la menos mala".
- **No inventes reglas del dominio.** Si crees que falta una, sugiérela al usuario como texto para que la agregue al repositorio.
- Si una hipótesis fue descartada por una regla, nómbrala y di qué regla violó.
- Si la respuesta es **frágil**, dilo: "depende de un solo juicio del verificador". No la presentes como conclusión firme.
- La respuesta explica lo ocurrido; **no es una recomendación de inversión ni de acción**. Si el usuario pregunta qué hacer, separa ambas cosas.

## Cómo responder (Telegram)

- Mensaje corto: la respuesta a la pregunta (y si está determinada o es frágil), la explicación ganadora, qué postula que no está confirmado, la alternativa principal y qué vigilar para cambiar de opinión.
- Para el detalle, `auditoria` con `formato: "markdown"` y envíalo como archivo.
- Si una operación es asíncrona, avisa que estás trabajando y consulta `estado_trabajo` antes de responder.
