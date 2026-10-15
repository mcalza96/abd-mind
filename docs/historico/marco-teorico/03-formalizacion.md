# 03 — Formalización

Esta sección fija la notación y las definiciones que el código implementa. Donde los documentos fuente dejaban algo implícito (en particular la relación $\approx$), aquí se define.

## 3.1 Espacios y observadores

| Símbolo | Significado |
|---|---|
| $\mathcal{S}$ | Espacio de mecanismos y estados causales latentes (el "mundo"). Abierto: puede crecer (§3.5). |
| $\mathcal{V} \subset \mathcal{S}$ | Vocabulario actual: variables, entidades y relaciones que el sistema sabe nombrar. |
| $O = \{O_1, \dots, O_m\}$ | Conjunto de observadores con marcos de referencia diferenciados. |
| $\mathcal{Y}_i$ | Espacio de observación local del observador $O_i$. |
| $\pi_{O_i} : \mathcal{S} \to \mathcal{Y}_i$ | Operador de proyección del observador $O_i$. Abreviado $\pi_i$. |
| $Y = \{y_1, \dots, y_m\}$ | Observaciones recolectadas, con $y_i \in \mathcal{Y}_i$. |
| $\mathcal{R}$ | Conjunto de reglas invariantes del dominio (Postulado 2). |

**Ecuación de la observación** (Postulado 1):

$$y_i = \pi_i(S) + \eta_i$$

con $\eta_i$ ruido intra-marco. El aprendizaje clásico asume $\pi_i = \text{id}$ para todo $i$ y atribuye toda discrepancia a $\eta$. Aquí $\pi_i$ es en general **no inyectiva** (pierde información) y **distinta** para cada observador.

Un observador puede emitir varias observaciones. Cuando haga falta distinguirlas, se indexan como $y_{i,j}$; para simplificar, en lo que sigue cada $y_i$ es una observación atómica con su observador asociado.

## 3.2 Hipótesis

Una hipótesis $H$ es una descripción de un estado o mecanismo de $\mathcal{S}$ que tiene tres componentes:

- $\text{mec}(H)$: el mecanismo causal propuesto (descripción en lenguaje natural o estructura).
- $L(H) \subseteq \mathcal{S} \setminus \mathcal{V}$: las **entidades latentes nuevas** que $H$ postula, es decir, las que no están en el vocabulario verificado.
- $\Phi(H)$: los **predicados de consistencia** que $H$ afirma y que deben ser compatibles con $\mathcal{R}$.

## 3.3 Relación de consistencia

Los documentos fuente usan $\pi_i(H) \approx y_i$ sin definirla. Se define por observador como un predicado booleano:

$$\pi_i(H) \approx y_i \iff d_i\big(\pi_i(H),\, y_i\big) \le \varepsilon_i$$

donde $d_i$ es una medida de discrepancia apropiada a $\mathcal{Y}_i$ y $\varepsilon_i \ge 0$ una tolerancia que absorbe el ruido intra-marco $\eta_i$. Casos según el tipo de observación:

| Tipo de $\mathcal{Y}_i$ | $d_i$ | $\varepsilon_i$ |
|---|---|---|
| Categórico cerrado ("círculo", "rectángulo") | $0$ si iguales, $1$ si no (o una jerarquía explícita: ver nota) | $0$ |
| Numérico | $\lvert a - b \rvert$ o error relativo | Precisión del instrumento |
| Lenguaje natural | Veredicto de un verificador (§3.3.1) | — |

**Nota sobre jerarquías.** Si el dominio admite que "cuadrado" es un caso de "rectángulo", eso debe estar escrito en la definición de $d_i$, no decidido caso a caso. La elección cambia los resultados (ver el ejemplo del cubo en [05](05-experimentos-canonicos.md#51-cilindro-latente)).

### 3.3.1 Proyecciones no computables

En dominios sintéticos, $\pi_i$ es una función programable (p. ej., la silueta geométrica de un sólido vista desde un ángulo). En dominios reales no existe una fórmula: $\pi_i$ es "lo que este analista, con su metodología, habría reportado si $H$ fuera cierta".

En ese caso $\approx$ se aproxima con un **verificador** que recibe una sola tripleta $(H, O_i, y_i)$ y emite un veredicto booleano. Requisitos:

1. Evalúa **una observación por llamada**, sin ver las demás ni el score.
2. No es el mismo proceso que generó $H$ (idealmente otro modelo).
3. Su veredicto queda registrado con su justificación para auditoría.

Esto es una aproximación, no una proyección exacta; se reconoce como limitación en [08](08-decisiones-y-limitaciones.md).

## 3.4 El problema inverso (abducción)

Dado $Y$, el operador abductivo $\mathcal{A}$ busca las hipótesis que hacen esperables **todas** las observaciones:

$$H_{\text{cand}} = \{\, H \in \mathcal{S} \;\mid\; \pi_i(H) \approx y_i \;\; \forall i \,\}$$

Si dos observadores dicen cosas opuestas, el sistema no promedia: busca qué $H$ proyecta exactamente esas dos sombras desde esos dos ángulos.

En la práctica $\mathcal{S}$ no se recorre entero. Un generador produce un conjunto finito $\mathcal{H} = \{H_1, \dots, H_n\}$ y se trabaja con la versión **relajada**: en lugar de exigir consistencia con todas las observaciones, se mide cuántas explica (consiliencia, [04](04-funcion-objetivo-ibe.md)) y se elige la mejor. $H_{\text{cand}}$ es el subconjunto de $\mathcal{H}$ con consiliencia máxima $C(H) = m$.

## 3.5 Ampliación ontológica

**Condición de disparo.** Si ninguna hipótesis formulable con el vocabulario actual reconcilia todas las observaciones coherentes con las reglas,

$$\nexists\, H \in \mathcal{H}_{\mathcal{V}} : \big(C(H) = m \,\wedge\, K(H) = 1\big)$$

el sistema ejecuta una expansión postulando una variable latente no observada:

$$\mathcal{S}_{\text{nuevo}} = \mathcal{S}_{\text{previo}} \cup \{v_{\text{latente}}\}$$

y genera nuevas hipótesis que la usan.

**Costo.** Cada entidad postulada suma 1 a la parsimonia $P(H)$ y resta $\gamma$ al score. Por eso la expansión solo gana si compra suficiente consiliencia; la condición exacta se deriva en [04, §4.5](04-funcion-objetivo-ibe.md#45-el-intercambio-entre-parsimonia-y-consiliencia).

**Promoción.** Una entidad latente postulada deja de contar en $P$ cuando es **verificada** de forma independiente (por evidencia nueva o una fuente externa) y pasa a $\mathcal{V}$. Hasta entonces, es una deuda ontológica de la hipótesis.

> Con observadores falibles, el disparo de la expansión compara el costo del residuo de la mejor hipótesis con el de una entidad nueva: ver [09 §9.1.7](09-robustez-epistemica.md#917-disparo-de-la-expansión-ontológica).

## 3.6 Derrotabilidad (no monotonía)

Sea $H^*$ la hipótesis ganadora actual y llega una observación nueva $y_k$ del observador $O_k$:

- Si $\pi_k(H^*) \approx y_k$: $H^*$ sobrevive y gana robustez. $C(H^*) \leftarrow C(H^*) + 1$.
- Si $\pi_k(H^*) \not\approx y_k$: $H^*$ queda **derrotada**. Su estado pasa a `DERROTADA` y deja de ser elegible.

Tres precisiones respecto a los documentos fuente:

1. **Todas** las hipótesis vivas se reevalúan contra $y_k$, no solo $H^*$. La "siguiente mejor" también debe pasar la prueba de $y_k$ antes de ser promovida.
2. La derrota se aplica con la misma relación $\approx$ (con tolerancia), no con igualdad estricta. Si no, cualquier ruido intra-marco derrotaría hipótesis correctas.
3. Una hipótesis derrotada **no se borra**: queda registrada con la evidencia que la derrotó. Si esa evidencia se retracta, la hipótesis puede volver a ser elegible. Esto es un registro de mantenimiento de verdad, no un descarte irreversible.

Si tras la reevaluación no queda ninguna hipótesis viva que supere el umbral de aceptación, se vuelve a §3.4 (generar) y, si es necesario, a §3.5 (ampliar).

Nada de esto requiere reentrenar pesos: el estado del razonamiento vive en el árbol de hipótesis, no en el modelo.

> Con observadores falibles, solo una observación de confiabilidad $\omega_k \ge \omega_d$ derrota por sí sola; las demás dejan a la hipótesis *en tensión* ([09 §9.1.8](09-robustez-epistemica.md#918-derrota-graduada)). Si varias hipótesis quedan empatadas, no se elige ninguna ([09 §9.2](09-robustez-epistemica.md#92-subdeterminación-y-abducción-activa)).

## 3.7 Ciclo completo

```
Y ──► generar 𝓗 ──► evaluar Score ──► ¿existe H con C=m, K=1, Score ≥ τ?
          ▲                                  │ sí                │ no
          │                                  ▼                   ▼
          │                         H* = argmax Score     ampliar 𝓢 (§3.5)
          │                                  │                   │
          │        nueva evidencia y_k ──────┤                   │
          │                                  ▼                   │
          │                      reevaluar todas (§3.6)          │
          └──────────────────────────────────┴───────────────────┘
```
