# 05 — Experimentos canónicos

Los experimentos sirven a dos fines: **especificar** el comportamiento esperado (son la base de las pruebas automáticas) y **falsar** la tesis (si el pipeline no supera a la línea base en estos casos, algo en el marco está mal).

Todos los cálculos usan los pesos por defecto $\alpha = 1.5$, $\beta = 10$, $\gamma = 1$.

## 5.1 Cilindro latente

**Entorno.** Objeto real $S$ = cilindro con eje vertical.

| Observador | Marco | Observación |
|---|---|---|
| $O_1$ | Vista frontal | $y_1$ = "rectángulo" |
| $O_2$ | Vista cenital | $y_2$ = "círculo" |

Las proyecciones son siluetas geométricas, así que $\pi_1$ y $\pi_2$ son **computables**: en este entorno, $C$ se calcula sin ningún LLM.

**Falla inductiva esperada.** Un LLM en decodificación directa tiende a fusionar la semántica de las etiquetas y producir una quimera ("óvalo", "rectángulo redondeado"), que no es la proyección de ningún sólido compatible con ambas vistas.

**Resolución abductiva.**

| Hipótesis | $\pi_1$ (frontal) | $\pi_2$ (cenital) | $C$ | $P$ | $K$ | Score |
|---|---|---|---|---|---|---|
| $H_1$ Esfera | círculo ✗ | círculo ✓ | 1 | 0 | 1 | 11.5 |
| $H_2$ Cubo | cuadrado ✗ (*) | cuadrado ✗ | 0 | 0 | 1 | 10.0 |
| $H_3$ **Cilindro** | rectángulo ✓ | círculo ✓ | **2** | 0 | 1 | **13.0** |
| $H_q$ Quimera: elipsoide de revolución | elipse ✗ | círculo ✓ | 1 | 0 | 1 | 11.5 |

$H_3$ gana por máxima consiliencia, sin ser el promedio de nada.

(*) **Precisión sobre el cubo.** El documento de especificación asigna $C(H_2) = 1$, lo que solo es correcto si se acepta que "un cuadrado es un rectángulo". Con igualdad categórica estricta, $C(H_2) = 0$. El resultado de la selección no cambia, pero ilustra por qué $\approx$ debe estar definida explícitamente por observador ([03, §3.3](03-formalizacion.md#33-relación-de-consistencia)). Las pruebas fijan la variante estricta.

**Criterio de éxito.** El pipeline selecciona "cilindro". La línea base (LLM en decodificación greedy, una sola llamada, mismas observaciones) se evalúa con el mismo verificador: se espera $C_{\text{base}} < 2$ en una fracción significativa de corridas.

## 5.2 Expansión ontológica

Mismo entorno, pero el vocabulario inicial **no contiene** el cilindro: $\mathcal{V} = \{\text{esfera}, \text{cubo}, \text{cono}\}$.

| Hipótesis | $\pi_1$ | $\pi_2$ | $C$ | $P$ | Score |
|---|---|---|---|---|---|
| Esfera | círculo ✗ | círculo ✓ | 1 | 0 | 11.5 |
| Cubo | cuadrado ✗ | cuadrado ✗ | 0 | 0 | 10.0 |
| Cono | triángulo ✗ | círculo ✓ | 1 | 0 | 11.5 |

Ninguna alcanza $C = m = 2$: se cumple la condición de disparo de [03, §3.5](03-formalizacion.md#35-ampliación-ontológica). El sistema postula una entidad nueva, p. ej. *"sólido de revolución con perfil rectangular"*:

| Hipótesis | $C$ | $P$ | Score |
|---|---|---|---|
| $v_{\text{latente}}$: sólido de revolución de perfil rectangular | 2 | 1 | **12.0** |

Gana porque $\Delta C / \Delta P = 1 > \gamma/\alpha \approx 0.67$ ([04, §4.5](04-funcion-objetivo-ibe.md#45-el-intercambio-entre-parsimonia-y-consiliencia)).

**Criterio de éxito.** (a) La expansión se dispara solo cuando ninguna hipótesis del vocabulario alcanza $C = m$. (b) No se dispara en 5.1, donde no hace falta. (c) Con $\gamma/\alpha > 1$ la expansión deja de ganar: el comportamiento es sensible a los pesos de la forma prevista.

## 5.3 Derrotabilidad: el tercer observador

Partiendo del resultado de 5.1 ($H^*$ = cilindro), llega evidencia nueva:

| Observador | Marco | Observación |
|---|---|---|
| $O_3$ | Vista lateral (perpendicular a $O_1$) | $y_3$ = "triángulo" |

$\pi_3(\text{cilindro})$ = rectángulo $\not\approx$ triángulo, así que el cilindro queda **derrotado**. Se reevalúan todas las hipótesis vivas contra $y_3$; ninguna alcanza $C = 3$, y la expansión postula el sólido conocido como **tapón universal** (cilindro cortado por dos planos que forman una cuña): rectángulo de frente, círculo desde arriba, triángulo de lado.

| Hipótesis | $C$ | $P$ | Estado |
|---|---|---|---|
| Cilindro | 2 de 3 | 0 | `DERROTADA` por $y_3$ |
| Tapón universal | 3 de 3 | 1 | Nueva $H^*$ |

**Criterio de éxito.** (a) El cilindro pasa a `DERROTADA` y conserva el registro de qué evidencia lo derrotó. (b) La nueva ganadora explica las tres observaciones. (c) Si se retracta $y_3$, el cilindro vuelve a ser elegible. (d) Ningún paso reentrena un modelo.

## 5.4 Caso de dominio: informes financieros contradictorios

Es el caso de uso real del proyecto. $\pi_i$ no es computable: $\approx$ la decide un verificador independiente ([03, §3.3.1](03-formalizacion.md#331-proyecciones-no-computables)).

**Observaciones** (ya separadas por el córtex perceptivo en *hecho* y *opinión del observador*):

| Observador | Hecho reportado | Opinión (no entra en $C$) |
|---|---|---|
| $O_1$ Analista fundamental | El margen bruto cayó 4 pp en tres trimestres | "Vender" |
| $O_2$ Analista de ventas | El volumen de unidades creció 18 % | "Comprar" |
| $O_3$ Prensa sectorial | El principal competidor perdió cuota de mercado | — |

**Regla invariante relevante** ($\mathcal{R}$): *una reducción de precios sostenida comprime el margen bruto.*

| Hipótesis | Explica | $C$ | $P$ | $K$ | Score |
|---|---|---|---|---|---|
| $H_a$ La demanda del sector crece | $y_2$ | 1 | 0 | 1 | 11.5 |
| $H_b$ Suben los costos de insumos | $y_1$ | 1 | 0 | 1 | 11.5 |
| $H_c$ **Estrategia deliberada de reducción de precios para ganar cuota** | $y_1, y_2, y_3$ | **3** | 1 | 1 | **13.5** |
| $H_q$ Quimera: "situación neutral, mantener" | — | 0 | 0 | 1 | 10.0 |
| $H_x$ Dividendos extraordinarios por sobre la caja disponible | — | — | — | **0** | $-\infty$ |

- $H_c$ postula una entidad no verificada (la estrategia no está anunciada), por eso $P=1$, pero unifica las tres observaciones.
- $H_q$ es el "promedio" de las recomendaciones de los analistas: no explica ningún hecho.
- $H_x$ viola la regla "los dividendos pagados no pueden exceder la caja disponible" y se descarta sin importar su consiliencia.

**Derrotabilidad.** Si llega $y_4$: *"la empresa informa que sus precios de lista no cambiaron en 12 meses"*, $H_c$ queda derrotada y el sistema debe buscar otra hipótesis, por ejemplo un cambio de mezcla de ventas hacia productos de menor margen.

**Criterio de éxito.** (a) El córtex separa hecho de opinión. (b) El ranking coincide con el esperado bajo un panel de verificadores. (c) La regla de dominio descarta $H_x$.

## 5.5 Pruebas que derivan de estos experimentos

| Prueba (Plan Maestro) | Experimento | Qué mide |
|---|---|---|
| Unitaria de extracción | 5.4 | Precisión al separar hechos duros de opiniones en reportes ambiguos o contradictorios |
| "Tren de Einstein" | 5.1, 5.2 | Pipeline vs. LLM en decodificación greedy: tasa de recuperación de la causa latente |
| Estrés de contexto | 5.4 con $\lvert\mathcal{R}\rvert$ grande | Estabilidad del verificador y del motor de reglas con muchas reglas de fondo |
| Derrotabilidad | 5.3, 5.4 | Descarte de $H^*$ ante evidencia nueva y promoción de una alternativa sin reentrenar |

Métricas comunes: tasa de acierto de la hipótesis ganadora, $\hat{C}$ medio de la ganadora, tasa de quimeras, número de llamadas al LLM y costo, y concordancia entre lo que el generador declara explicar y lo que el verificador confirma (indicador de racionalización).
