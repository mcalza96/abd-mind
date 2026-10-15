# ADR-0009 — Observadores falibles y atribución de error

**Estado:** aceptada

## Contexto

El motor trata cada observación como una proyección fiel salvo una tolerancia pequeña. Un error grosero (una errata, una etiqueta corrupta) produce sobreajuste ontológico —se inventan entidades para justificarlo— y derrotas espurias de hipótesis sólidas. Ver [09 §9.1](../../historico/marco-teorico/09-robustez-epistemica.md#91-observadores-falibles-duhem-quine).

## Decisión

1. **Confiabilidad por observador.** `Observador.confiabilidad` $\omega \in (0, 1]$, con valor por defecto del dominio (`confiabilidad_por_defecto` en `rules/<dominio>.yaml`; 1.0 si no se declara). Una `Observacion` puede declarar la suya. El motor **nunca** calcula $\omega$ a partir del acuerdo entre observadores.
2. **Score extendido** en `IBEEvaluator`: $\alpha \sum_{E} \omega_i + \beta K - \gamma P - \lambda \sum_{R} c(\omega_j)$, con $c(\omega) = -\ln(1 - \min(\omega, 0.999))$. El evaluador recibe consiliencia ponderada y residuo ya calculados por el árbol; con $\lambda = 0$ y $\omega = 1$ el resultado es idéntico al de la especificación.
3. **Residuo explícito.** Cada hipótesis evaluada informa `atribuidas_a_error`: las observaciones que no explica, con su costo. El residuo lo calcula el motor; no lo declara el generador (D1).
4. **Derrota graduada.** Una observación nueva derrota solo si $\omega \ge \omega_d$ (`pesos.omega_derrota`, por defecto 0.95). Si no, la hipótesis queda *en tensión*, registrada para auditoría.
5. **Expansión.** `expansion_sugerida` es verdadero si el menor $L(H) = \sum_{R(H)} (\alpha\omega_j + \lambda c(\omega_j))$ entre las hipótesis coherentes supera $\gamma$.

Pesos nuevos en `ConfigPesos`: `lambda_residuo` (por defecto 1.0 en la configuración del motor, 0.0 en `IBEEvaluator` para conservar la especificación) y `omega_derrota` (0.95).

## Consecuencias

- **+** Un error tipográfico de un observador poco confiable no derriba una hipótesis ni dispara la expansión.
- **+** El usuario ve qué datos supone erróneos la explicación ganadora y puede revisarlos.
- **+** Los experimentos sintéticos no cambian ($\omega = 1$).
- **−** Los resultados dependen del $\omega$ por defecto del dominio mientras no haya historial (L7).
- **−** Un observador sistemáticamente sesgado no se corrige con $\omega$: hay que modelar su marco.
