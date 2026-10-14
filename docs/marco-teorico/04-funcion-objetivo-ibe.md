# 04 — Función objetivo abductiva (IBE)

## 4.1 Principio: desacoplar la decisión de la verosimilitud

Un LLM está diseñado para maximizar la probabilidad del consenso estadístico de su corpus. Si se le pide que *elija* la mejor explicación, hereda ese sesgo. Por eso la selección se hace con una función matemática explícita, evaluada en código determinista. El LLM aporta insumos; no puntúa ni elige.

La selección se basa en la **Inferencia a la Mejor Explicación** (Harman, Thagard), operacionalizada con tres virtudes explicativas.

## 4.2 Las tres virtudes

### Parsimonia — $P(H)$

Penaliza la complejidad ontológica: cuántas entidades nuevas, no verificadas, necesita postular $H$.

$$P(H) = \lvert L(H) \rvert = \lvert \{ v \in H \mid v \text{ es entidad latente postulada no verificada} \} \rvert$$

Menor es mejor. Una entidad que ya está en el vocabulario verificado $\mathcal{V}$ no cuenta.

### Consiliencia (poder unificador) — $C(H)$

Premia la capacidad de $H$ de reconciliar observaciones divergentes.

$$C(H) = \sum_{i=1}^{m} \mathbb{I}\big(\pi_i(H) \approx y_i\big)$$

con $\mathbb{I}$ la función indicadora y $\approx$ definida en [03, §3.3](03-formalizacion.md#33-relación-de-consistencia). Mayor es mejor; el máximo es $m$.

Variante normalizada, útil para comparar entre problemas con distinto número de observaciones: $\hat{C}(H) = C(H)/m \in [0,1]$.

### Coherencia externa — $K(H)$

Compatibilidad con las leyes invariantes del dominio $\mathcal{R}$, verificada por un motor de reglas externo:

$$K(H) = \begin{cases} 1 & \text{si } \Phi(H) \text{ no contradice ninguna regla de } \mathcal{R} \\ 0 & \text{si hay contradicción dura} \end{cases}$$

Actúa como **filtro** contra hipótesis que violan leyes establecidas, incluidas las alucinaciones.

## 4.3 El score abductivo

$$\text{Score}(H) = \alpha \cdot C(H) + \beta \cdot K(H) - \gamma \cdot P(H), \qquad \alpha, \beta, \gamma > 0$$

con la regla de descarte: si $K(H) = 0$, entonces $\text{Score}(H) = -\infty$.

**Selección.**

$$H^* = \arg\max_{H \in \mathcal{H}} \text{Score}(H) \quad \text{sujeto a} \quad \text{Score}(H^*) \ge \tau$$

donde $\tau$ es el umbral mínimo de aceptación. Si ninguna hipótesis lo alcanza, el sistema **no concluye**: genera más o amplía la ontología. "No hay explicación suficiente" es una salida válida.

**Desempate determinista.** Ante igualdad de score, se prefiere (1) mayor $C$, (2) menor $P$, (3) orden lexicográfico del identificador. El resultado no puede depender del orden de llegada.

Valores por defecto de la especificación de implementación: $\alpha = 1.5$, $\beta = 10$, $\gamma = 1$.

## 4.4 Propiedad del peso de coherencia

Si $K \in \{0, 1\}$ y $K = 0$ implica descarte, entonces toda hipótesis que sobrevive tiene $K = 1$ y recibe el mismo término $+\beta$. El orden entre sobrevivientes queda determinado solo por

$$\alpha \cdot C(H) - \gamma \cdot P(H)$$

Consecuencias:

- $\beta$ solo importa en relación con el umbral $\tau$: desplaza todos los scores por igual.
- Si en el futuro se quiere graduar la coherencia (p. ej., $K \in [0,1]$ como fracción de reglas blandas satisfechas, como sugiere uno de los documentos fuente), entonces sí hay que calibrar $\beta$ frente a $\alpha$ y $\gamma$. Las dos modalidades se distinguen en el código: **reglas duras** (gate, $K=0 \Rightarrow -\infty$) y **reglas blandas** (graduales, ponderadas por $\beta$).

## 4.5 El intercambio entre parsimonia y consiliencia

Comparemos una hipótesis $H_0$ con otra $H_1$ que postula $\Delta P$ entidades más y explica $\Delta C$ observaciones más (ambas coherentes). $H_1$ gana si y solo si

$$\alpha \cdot \Delta C > \gamma \cdot \Delta P \iff \frac{\Delta C}{\Delta P} > \frac{\gamma}{\alpha}$$

Es la **navaja de Occam cuantificada**: postular una entidad nueva solo vale la pena si explica al menos $\gamma/\alpha$ observaciones adicionales. Con los valores por defecto ($\gamma/\alpha = 2/3$), una entidad latente que explica una sola observación más ya se justifica.

Esto da criterio para calibrar:

| Si se quiere que… | Entonces |
|---|---|
| Una entidad nueva se justifique solo si explica ≥ 2 observaciones más | $1 < \gamma/\alpha < 2$ |
| La expansión ontológica sea muy conservadora | $\gamma/\alpha$ alto |
| El sistema postule latentes con facilidad | $\gamma/\alpha$ bajo (riesgo: hipótesis *ad hoc*) |

## 4.6 Riesgo: virtudes autodeclaradas

La fórmula es determinista, pero sus **insumos** pueden no serlo. Si $C$ se calcula contando la lista `observaciones_explicadas` que el propio LLM escribe, y $P$ contando `entidades_latentes` que el propio LLM declara, el generador se está puntuando a sí mismo: puede afirmar que explica todo y que no postula nada. El cálculo sería determinista; el resultado, no confiable.

Por eso el marco exige:

| Virtud | Fuente admisible del insumo |
|---|---|
| $C$ | Evaluación independiente de $\pi_i(H) \approx y_i$ por observación: función de proyección en dominios sintéticos, verificador separado en dominios reales ([03, §3.3.1](03-formalizacion.md#331-proyecciones-no-computables)) |
| $P$ | Extracción independiente de las entidades del mecanismo, contrastada contra $\mathcal{V}$. Lo que el generador declara se usa como referencia, y una discrepancia se registra |
| $K$ | Motor de reglas sobre predicados **estructurados**, no búsqueda de palabras clave en texto libre |

La lista autodeclarada por el generador sigue siendo útil como **predicción** que se puede auditar: si el generador dice explicar $y_3$ y el verificador dice que no, eso es una señal de racionalización.

## 4.7 Lo que la función no captura

Literatura de IBE computacional (ver [07](07-estado-del-arte.md)) identifica otras virtudes: profundidad de prueba, deriva conceptual, *hedging* (cobertura lingüística excesiva), circularidad. No se incluyen en la versión inicial para mantener la función mínima y auditable; quedan como extensiones candidatas, cada una con su término y peso propio.
