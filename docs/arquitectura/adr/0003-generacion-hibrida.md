# ADR-0003 — Generación de hipótesis híbrida

**Estado:** aceptada

## Contexto

La limitación L1 del marco teórico reconoce que solo puede ganar una hipótesis que alguien llegó a proponer. La diversidad de fuentes es la principal defensa ([06 §6.4](../../marco-teorico/06-arquitectura.md#64-generación-aproximar-una-búsqueda-no-guiada-por-verosimilitud)). Hermes tiene contexto que el motor no tiene: la conversación con el usuario, su memoria, los documentos que leyó, búsquedas web.

## Decisión

Hay dos vías de entrada al mismo conjunto $\mathcal{H}$ del caso:

1. **`generar_hipotesis`** — generadores propios del motor: varios modelos, muestreo contrastivo, modo de expansión ontológica.
2. **`proponer_hipotesis`** — Hermes (o el usuario a través de Hermes) aporta candidatas.

Todas las hipótesis registran su `origen` (`motor:<modelo>`, `hermes`, `usuario`) y pasan por **exactamente la misma** evaluación. El origen no da ventaja ni penalización en el score; se usa solo para análisis (¿qué fuente produce las ganadoras?).

Los campos `observaciones_explicadas` y `entidades_latentes` que traiga una hipótesis propuesta se guardan como **declaración**, nunca como insumo del score ([ADR-0002](0002-verificacion-interna.md)).

## Consecuencias

- **+** Más diversidad de hipótesis; el contexto conversacional de Hermes entra al razonamiento.
- **+** El usuario puede sugerir su propia explicación y verla competir en igualdad de condiciones.
- **−** Hermes ve los scores de las hipótesis existentes cuando propone nuevas: podría sesgarse hacia variantes de la ganadora. Se mitiga en la skill (proponer antes de mirar el ranking) y, si hace falta, ocultando scores en `estado_caso` hasta que se pida `evaluar`.
