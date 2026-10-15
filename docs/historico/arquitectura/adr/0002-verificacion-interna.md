# ADR-0002 — La verificación de virtudes vive dentro del motor

**Estado:** aceptada; independencia de modelos **suspendida** desde el 2026-10-15 (ver la nota al final)

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

## Nota (2026-10-15): un solo modelo

Por decisión del usuario, todos los roles usan DeepSeek V4.1 Flash. Muse, de otra familia, es un modelo *contributor*: entrena con los prompts y su acceso quedó bloqueado. **La verificación sigue ocurriendo dentro del motor**, pero el modelo que propone y el que juzga son el mismo.

**Consecuencias:**

- El sesgo de autoconfirmación puede volver.
- Los juicios del verificador y del juez holístico valen como juicios del mismo observador, no de uno independiente (principio P1).
- Donde hay proyección exacta, nada cambia.

**Para volver a la independencia:** un verificador o un generador de otra familia que no sea *contributor*. En el plan hay candidatos, como Qwen, Kimi y GLM.

