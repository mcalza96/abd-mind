# 09 — Robustez epistémica

Extensiones al marco para los casos de borde donde la versión base ([03](03-formalizacion.md), [04](04-funcion-objetivo-ibe.md)) colapsa. Todas se reducen exactamente a la versión base en el caso límite de observadores infalibles (§9.1.5), así que los experimentos sintéticos ([05](05-experimentos-canonicos.md)) no cambian.

| § | Problema | Estado |
|---|---|---|
| 9.1 | Observadores falibles: ¿anomalía latente o error del observador? | Especificado; se implementa en la fase 4b |
| 9.2 | Subdeterminación: hipótesis empíricamente indistinguibles | Especificado; se implementa en la fase 4b |
| 9.3 | Observadores correlacionados (sesgo de rebaño) | Propuesto |
| 9.4 | Asincronía temporal | Propuesto |
| 9.5 | Reglas falibles | Propuesto |
| 9.6 | Parsimonia y realidad compleja | Analizado: no se cambia la función |

## 9.1 Observadores falibles (Duhem-Quine)

### 9.1.1 El problema

La versión base trata cada observación como proyección fiel: $y_i = \pi_{O_i}(S) + \eta_i$, con $\eta_i$ ruido pequeño absorbido por la tolerancia $\varepsilon_i$ ([03 §3.3](03-formalizacion.md#33-relación-de-consistencia)). Un **error grosero** —un cero de más, una etiqueta corrupta, un sensor averiado— no es ruido pequeño y produce dos patologías:

1. **Sobreajuste ontológico.** Si ninguna hipótesis explica el dato erróneo, el sistema amplía la ontología e inventa entidades latentes para justificar una errata.
2. **Derrota espuria.** Una hipótesis sólida queda derrotada por una sola observación falsa ([03 §3.6](03-formalizacion.md#36-derrotabilidad-no-monotonía)).

La tesis de Duhem-Quine lo formula así: una observación que contradice una teoría no la refuta aisladamente; refuta la conjunción de la teoría con las **hipótesis auxiliares**, entre ellas "el observador reportó correctamente". El sistema debe poder elegir cuál de las dos abandonar.

### 9.1.2 Observación con canal de error

$$y_i = \pi_{O_i}(S) \oplus \eta_i, \qquad \eta_i \in \{\varnothing\} \cup \mathcal{E}$$

$\eta_i = \varnothing$ significa que el reporte es fiel (salvo la tolerancia $\varepsilon_i$); $\eta_i \in \mathcal{E}$ significa que el reporte no corresponde a la proyección (error grosero). La **confiabilidad** del observador es

$$\omega_i = \Pr(\eta_i = \varnothing) \in (0, 1]$$

y el **costo de atribuirle un error** es su sorpresa:

$$c(\omega) = -\ln\big(1 - \min(\omega, \omega_{\max})\big), \qquad \omega_{\max} = 0.999$$

| $\omega$ | 0.5 | 0.6 | 0.8 | 0.9 | 0.95 | 0.99 | 1 (tope 0.999) |
|---|---|---|---|---|---|---|---|
| $c(\omega)$ | 0.69 | 0.92 | 1.61 | 2.30 | 3.00 | 4.61 | 6.91 |

El tope evita costos infinitos: ni siquiera un instrumento "perfecto" impide considerar que esta vez falló, solo lo hace muy caro.

### 9.1.3 De dónde sale $\omega$ (salvaguarda anti-consenso)

$\omega_i$ **nunca** se estima a partir del acuerdo de $O_i$ con los demás observadores del mismo caso. Hacerlo reintroduciría el sesgo de consenso que el proyecto rechaza ([01](01-problema-y-tesis.md)): el observador disidente es con frecuencia el único que ve la variable latente.

Fuentes admisibles, en orden:

1. Calibración independiente del instrumento o la fuente (especificación, auditoría externa).
2. Historial en casos cerrados cuya verdad quedó establecida por evidencia independiente.
3. Valor por defecto del dominio (`confiabilidad_por_defecto` en `rules/<dominio>.yaml`).

Una observación puntual puede declarar una confiabilidad propia (p. ej. un dato transcrito a mano de un PDF escaneado).

### 9.1.4 Función objetivo extendida

Sea $E(H)$ el conjunto de observaciones activas que $H$ explica y $R(H)$ el de las que no explica (su **residuo**, que $H$ atribuye a error de los observadores):

$$\text{Score}(H) = \alpha \sum_{i \in E(H)} \omega_i \;+\; \beta\, K(H) \;-\; \gamma\, P(H) \;-\; \lambda \sum_{j \in R(H)} c(\omega_j)$$

- Explicar una observación confiable vale más que explicar una dudosa.
- Dejar sin explicar una observación confiable cuesta mucho; dejar una dudosa, poco.
- $\lambda \ge 0$ pondera el costo del residuo. Con $\lambda = 0$ el residuo solo cuesta lo que se deja de ganar en consiliencia.

El residuo de $H^*$ se reporta explícitamente: "esta explicación supone que $y_3$ es un error de $O_3$".

### 9.1.5 Reducción a la versión base

Con $\lambda = 0$ y $\omega_i = 1$ para todo $i$: $\sum_{E} \omega_i = C(H)$ y el último término desaparece, así que $\text{Score}(H) = \alpha C(H) + \beta K(H) - \gamma P(H)$, la función original. Los dominios cuyas proyecciones son exactas (`sintetico`) usan $\omega = 1$.

### 9.1.6 Culpar al observador o ampliar la ontología

Sea $H_0$, que deja $y_j$ en el residuo, y $H_1$, que lo explica postulando $\Delta P$ entidades más (lo demás igual). $H_1$ gana si y solo si

$$\alpha\, \omega_j + \lambda\, c(\omega_j) > \gamma\, \Delta P$$

Con los pesos por defecto ($\alpha = 1.5$, $\gamma = 1$, $\lambda = 1$), el máximo de entidades nuevas que se justifica postular para no culpar a $O_j$:

| $\omega_j$ | 0.6 | 0.8 | 0.9 | 0.95 | 0.99 |
|---|---|---|---|---|---|
| $\alpha\omega_j + \lambda c(\omega_j)$ | 1.82 | 2.81 | 3.65 | 4.42 | 6.09 |
| $\Delta P$ máximo | 1 | 2 | 3 | 4 | 6 |

Ante un analista poco confiable, inventar más de una entidad para salvar su dato es peor que asumir que se equivocó. Ante un sensor calibrado, hace falta una explicación muy cargada para descartarlo.

### 9.1.7 Disparo de la expansión ontológica

La versión base amplía la ontología si ninguna hipótesis coherente explica las $m$ observaciones ([03 §3.5](03-formalizacion.md#35-ampliación-ontológica)). Con observadores falibles, la expansión **vale la pena** solo si el residuo de la mejor hipótesis cuesta más que la entidad nueva más barata:

$$\text{expandir} \iff \min_{H \text{ coherente}} L(H) > \gamma, \qquad L(H) = \sum_{j \in R(H)} \big(\alpha\,\omega_j + \lambda\, c(\omega_j)\big)$$

En el caso base ($\lambda = 0$, $\omega = 1$): $L(H) = \alpha (m - C(H)) > \gamma \iff C(H) < m$ con los pesos por defecto, que es la condición original.

### 9.1.8 Derrota graduada

Una observación nueva $y_k$ que $H$ no explica:

- **derrota** a $H$ si $\omega_k \ge \omega_d$ (umbral de derrota, por defecto 0.95): solo un observador muy confiable puede derribar una hipótesis por sí solo;
- si no, $H$ queda **en tensión**: sigue viva, $y_k$ entra en su residuo y el ranking decide.

Con $\omega = 1$ toda evidencia nueva no explicada derrota, como en la versión base. La derrota sigue siendo reversible ([08, D6](08-decisiones-y-limitaciones.md)).

### 9.1.9 Qué no resuelve

- $\omega$ por defecto es una suposición del dominio. Hasta tener historial de casos cerrados, el sistema solo es tan bueno como esa suposición.
- Un error sistemático (un observador que *siempre* reporta mal lo mismo) no es error aleatorio: es un marco. Debe modelarse en $\pi_{O_i}$, no en $\omega_i$.

## 9.2 Subdeterminación y abducción activa

### 9.2.1 El problema

Dos hipótesis incompatibles pueden proyectar las mismas sombras en todos los marcos disponibles: $\pi_{O_i}(H_a) \approx y_i \iff \pi_{O_i}(H_b) \approx y_i$ para todo $i$. La versión base desempata por el identificador ([08, D7](08-decisiones-y-limitaciones.md)): el resultado es determinista pero **finge una certeza** que la evidencia no da.

Caso real: en el experimento `finanzas-llm`, tras el comunicado, cuatro hipótesis (descuentos fuera de factura, canal outlet encubierto, cambio de mezcla, promociones financiadas) quedaron con el mismo score (C = 4/4, P = 1) y se eligió una por su id.

### 9.2.2 Definiciones

- $H_a$ y $H_b$ son **empíricamente equivalentes** sobre $Y$ si $E(H_a) = E(H_b)$.
- El conjunto **empatado** es $T = \{ H \text{ viva y coherente} : \text{Score}(H) \ge \text{Score}^* - \delta \}$, con $\delta \ge 0$ la tolerancia de empate.
- El caso está **subdeterminado** si $|T| \ge 2$.

Dos hipótesis pueden empatar sin ser equivalentes (explican conjuntos distintos con el mismo score); ambos casos son subdeterminación.

### 9.2.3 Comportamiento

Si el caso está subdeterminado, **no hay $H^*$**: el sistema informa el conjunto $T$ en lugar de elegir. El desempate por identificador queda solo como orden de presentación.

### 9.2.4 Abducción activa: pedir la observación que separa

Para romper la simetría, el sistema busca un marco $O_k$ (existente o nuevo) y una magnitud tales que las hipótesis empatadas predigan cosas distintas:

$$\exists\, H_a, H_b \in T : \pi_{O_k}(H_a) \not\approx \pi_{O_k}(H_b)$$

El poder discriminante de una consulta es el número de clases en que parte a $T$ (cuántas predicciones distintas produce). Se prefieren las consultas que dejan clases más chicas.

- Con proyecciones computables, las consultas se calculan: se recorren los marcos posibles del dominio y se comparan las proyecciones.
- Con verificador LLM, un modelo propone consultas con la predicción de cada hipótesis, y el motor descarta las que no separan (predicciones iguales).

La respuesta al usuario deja de ser "la mejor explicación es X" y pasa a ser "hay N explicaciones igual de buenas; para distinguirlas, observe Z desde el marco W".

## 9.3 Observadores correlacionados (propuesto)

Diez analistas que usan el mismo modelo comparten **marco**: son una proyección repetida, no diez. Contarlos por separado infla la consiliencia de la hipótesis que los satisface.

Propuesta: cada observador declara sus **fuentes** (datos, modelos, informes de los que depende). Los observadores con fuentes comunes forman grupos (componentes conexas). Cada observación pesa $1/|G(O_i)|$, donde $G(O_i)$ es el grupo de su observador, tanto en la consiliencia como en el residuo.

Pendiente: así formulado penaliza también hechos distintos aportados por observadores relacionados; el peso debería aplicarse solo a la **misma** afirmación repetida. Se refinará con el dataset de casos frontera.

## 9.4 Asincronía temporal (propuesto)

Si $y_1$ y $y_2$ se tomaron en momentos distintos, el estado pudo cambiar entre ellos: $S(t_1) \ne S(t_2)$. Suponer un $S$ estático lleva a inventar latentes para lo que es dinámica.

Propuesta mínima, sin un modelo dinámico aparte:

1. Las observaciones llevan fecha o período.
2. El generador recibe las fechas y considera explícitamente "cambio de régimen entre $t_1$ y $t_2$" como hipótesis candidata. Un cambio de régimen es una entidad latente más (cuesta parsimonia) y compite en igualdad con las demás.

## 9.5 Reglas falibles (propuesto)

Las reglas duras descartan sin apelación ($K = 0$). Si la regla es empírica y está incompleta, puede eliminar la hipótesis verdadera.

Convertir las reglas duras en blandas reabriría la puerta a las alucinaciones que las reglas existen para cerrar. Propuesta:

- Cada regla declara su naturaleza: `axiomatica` (contable, física, lógica) o `empirica` (regularidad del dominio).
- Las reglas siguen descartando igual. Pero si una hipótesis descartada por una regla **empírica** habría superado a $H^*$ con $K = 1$, el sistema emite una **alerta de revisión**: "H₇ sería la mejor explicación si no violara R". La regla la revisa un humano ([ADR-0004](../../arquitectura/adr/0004-reglas-solo-lectura.md)).

## 9.6 Parsimonia y realidad compleja (no se cambia)

Objeción: una penalización lineal $\gamma P(H)$ preferiría una explicación monocausal falsa a una multicausal verdadera.

Con la función actual, una hipótesis multicausal que **explica más** gana ([04 §4.5](04-funcion-objetivo-ibe.md#45-el-intercambio-entre-parsimonia-y-consiliencia)). La simple solo gana cuando las causas adicionales no aportan consiliencia; en ese caso preferirla es exactamente lo que pide la IBE, y si ambas explican lo mismo con distinto costo la situación está cubierta por la subdeterminación (§9.2) en cuanto la diferencia de score cae dentro de $\delta$.

Usar la parsimonia solo como desempate (consiliencia primero) haría ganar siempre a la hipótesis *ad hoc* que postula una entidad por cada anomalía. Por eso no se adopta. Una mejora posible, pendiente de evidencia: penalizar más las entidades que explican una sola observación (las típicamente *ad hoc*) que las que unifican varias.
