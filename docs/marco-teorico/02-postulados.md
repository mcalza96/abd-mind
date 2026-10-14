# 02 — Postulados epistemológicos

Los tres postulados son los axiomas del sistema. No se demuestran: se asumen y se diseñan pruebas que fallarían si fueran falsos en un dominio dado.

## Postulado 1 — Principio de Mediación

> Toda observación $y_i$ es el resultado de un operador de proyección epistémica $\pi_{O_i}$ aplicado sobre el estado real $S$:
> $$y_i = \pi_{O_i}(S)$$

**Lectura.** La etiqueta supervisada no es el *ground truth* físico o biológico. Es lo que un observador concreto (un médico, un sensor, un analista, un anotador) puede registrar de $S$ dado su marco. Una proyección **pierde información**: es la sombra bidimensional de un objeto tridimensional.

**Implicación de diseño.** Cada observación del sistema se guarda junto con la identidad de su observador y, cuando se conoce, una descripción de su marco. Una observación sin observador no es admisible. Los modelos `Observer` y `Observation` lo reflejan.

**Matiz.** Dentro de un mismo marco puede existir ruido de medición ordinario. La forma completa es $y_i = \pi_{O_i}(S) + \eta_i$, donde $\eta_i$ es ruido *intra-marco*. El postulado afirma que la discrepancia *entre* observadores se explica principalmente por la diferencia entre $\pi_{O_i}$ y $\pi_{O_j}$, no por $\eta$.

**Corolario: el observador es falible (Duhem-Quine).** Además del ruido pequeño, un observador puede cometer errores groseros: $y_i = \pi_{O_i}(S) \oplus \eta_i$, con confiabilidad $\omega_i = \Pr(\eta_i = \varnothing)$. Una observación que contradice una hipótesis no la refuta por sí sola: refuta la conjunción de la hipótesis con "el observador reportó bien", y el sistema debe poder elegir cuál abandonar. La confiabilidad nunca se infiere del acuerdo con los demás observadores, porque eso reintroduciría el consenso. Desarrollo completo en [09 §9.1](09-robustez-epistemica.md#91-observadores-falibles-duhem-quine).

## Postulado 2 — Invariante Causal

> El proceso generativo que rige el fenómeno opera bajo leyes y restricciones estructurales **invariantes** respecto al marco de referencia del observador.

**Lectura.** Existe algo —$S$ y las leyes que lo gobiernan— que no cambia según quién mire. La meta del sistema es descubrir ese invariante, no reproducir el consenso ni el promedio inter-observador.

**Implicación de diseño.** Las leyes invariantes conocidas del dominio se expresan como **reglas explícitas** en un motor externo al LLM. Toda hipótesis debe ser compatible con ellas (coherencia $K$, ver [04](04-funcion-objetivo-ibe.md)). Una hipótesis que viola un invariante no es "menos probable": es inadmisible.

## Postulado 3 — Ampliación Abductiva

> El espacio de estados $S$ tiene dimensionalidad superior a cualquier proyección observable. Toda anomalía o contradicción inter-observador irreducible con las variables conocidas es manifestación de variables latentes no observadas, y obliga a expandir el espacio de hipótesis:
> $$S_{\text{nuevo}} = S_{\text{previo}} \cup \{v_{\text{latente}}\}$$

**Lectura.** Las anomalías no son ruido a suavizar. Son el **disparador obligatorio** para ampliar la ontología. Esto distingue la abducción peirceana (ampliativa: inventa conceptos nuevos) de la abducción como deducción inversa sobre una base de conocimiento cerrada.

**Implicación de diseño.** El generador de hipótesis tiene un modo explícito de expansión, que se activa cuando ninguna hipótesis del vocabulario actual reconcilia todas las observaciones. La expansión tiene un costo (parsimonia) para que no se use gratuitamente.

## Cómo se ponen a prueba

Un postulado útil debe poder fallar. Señales de que un postulado no se cumple en un dominio:

| Postulado | Falla si… | Señal observable |
|---|---|---|
| 1 | Las discrepancias son independientes de la identidad del observador | Permutar las etiquetas de observador no cambia el resultado |
| 2 | No hay invariante estable | Las hipótesis ganadoras cambian sin que cambie la evidencia relevante |
| 3 | Las anomalías son ruido puro | La expansión ontológica no mejora la consiliencia sobre datos nuevos |

En esos dominios el enfoque inductivo clásico es adecuado y este sistema no aporta ventaja. Es parte del trabajo experimental identificarlos.
