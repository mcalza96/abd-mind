# ADR-0002 — La verificación de virtudes vive dentro del motor

**Estado:** aceptada

## Contexto

Las decisiones D1 y D2 del marco teórico ([08](../../marco-teorico/08-decisiones-y-limitaciones.md)) exigen que la consiliencia $C$ y la parsimonia $P$ se calculen con una fuente **independiente del generador**. Con Hermes como agente, existe la tentación de pedirle al LLM de Hermes que diga qué observaciones explica cada hipótesis: sería más simple, pero el mismo modelo que propone estaría juzgando.

## Decisión

Toda verificación ocurre **dentro de abd-mind**:

- $C$: `organ/projections.py` cuando $\pi_i$ es computable; `organ/verifier.py` (LLM propio del motor, una tripleta $(H, O_i, y_i)$ por llamada, temperatura 0) en dominios reales.
- $P$: extracción de entidades del mecanismo por el motor, contrastada con el vocabulario $\mathcal{V}$ del caso.
- $K$: `organ/rule_engine.py`, sin LLM.

El rol `verificador` usa por configuración un modelo **distinto** a los roles `generador` y al modelo de Hermes. El motor emite una advertencia en la auditoría si la configuración no lo cumple.

Hermes puede **leer** los veredictos (vía `evaluar` y `auditoria`) pero no **escribirlos**. Ninguna herramienta MCP acepta valores de $C$, $P$, $K$ o score como entrada.

## Consecuencias

- **+** Se preserva la independencia generador/verificador aunque Hermes proponga hipótesis.
- **+** Los veredictos quedan registrados con justificación: se puede medir racionalización (declarado vs. verificado).
- **−** abd-mind necesita su propio acceso a OpenCode Go (misma clave, roles distintos).
- **−** Costo: una llamada por par (hipótesis, observación) en dominios reales. Se controla con presupuestos ([ADR-0008](0008-presupuestos-y-trabajos-largos.md)) y caché de veredictos.
