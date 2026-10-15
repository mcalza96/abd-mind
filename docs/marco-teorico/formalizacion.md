# Formalización: lo que el código implementa

Referencia compacta del filtro y la prueba. Cuando el código dice `NN §x`, apunta a [histórico](../historico/marco-teorico/), donde está la derivación completa.

## Objetos

| Objeto | Contenido | Código |
|---|---|---|
| **Observador** $O_i$ | Marco, parámetros, tolerancia $\varepsilon_i$, confiabilidad $\omega_i$ | `contracts/observation.py` |
| **Observación** $y_i$ | Valor o texto, rol (`explanandum`, lo que hay que explicar, o `evidencia`) y ω propia opcional | `contracts/observation.py` |
| **Hipótesis** $H$ | Mecanismo, entidades latentes, afirmaciones variable → valor, `parametros_libres` (familia), predicciones | `contracts/abduction.py` |
| **Reglas del dominio** | Variables, vocabulario verificado, reglas duras y blandas, verificador (`proyeccion` o `llm`), `seleccion`, `puntuacion` | `rules/*.yaml`, `contracts/rules.py` |

Hay más reglas generales:

- Una opinión de un observador no es una observación (D8).
- La confiabilidad nunca se infiere del acuerdo entre observadores (D11).

## Veredicto

Para cada par (H, y_i) el veredicto es `explica`, `neutral` o `contradice`. Lo emite una **proyección** exacta, $\pi_i(H) \approx y_i$ dentro de $\varepsilon_i$, o un **LLM**. El LLM puede juzgar par por par o, en el modo comparativo, calificar un hecho contra todas las hipótesis a la vez:

| Calificación | Peso | Efecto |
|---|---|---|
| Muy esperable | 1 | Explica |
| Esperable | 0,5 | Explica |
| Indiferente | — | Neutral |
| Inesperado | — | Contradice |

Lo neutral no suma, no cuesta y no derrota. Un *explanandum* neutral queda **sin explicar**.

## Puntuación por consiliencia (por defecto)

$$\text{Score}(H) = \alpha \sum_{\text{explica}} \omega_i\,g_i + \beta K - \gamma P - \lambda \sum_{\text{contradice}} c(\omega_i), \qquad c(\omega) = -\ln(1 - \min(\omega, 0{,}999))$$

- **Pesos por defecto:** α = 1,5, β = 10, γ = 1, λ = 1.
- **P:** entidades de H que no están en el vocabulario verificado. Incluye las que afirma en variables de tipo entidad y las que señala un juez de parsimonia.
- **K:** una regla dura violada descarta la hipótesis. Las reglas blandas gradúan K entre 0 y 1.

## Puntuación por predicción (opción, [EXP-015](../bitacora/EXP-015-puntuacion-predictiva-en-el-motor.md))

$$\text{Score}_\text{pred}(H) = \sum_i \log p(y_i \mid y_{-i}, H) - \gamma P$$

$$p(y_i \mid y_{-i}, H) = \sum_\theta w^{(-i)}_\theta\,\ell_i(\theta), \qquad \ell_j(\theta) = \omega_j\,[\pi_j(\theta) \approx y_j] + \frac{1 - \omega_j}{|Y_j|}$$

- **Los parámetros θ** recorren los `parametros_libres` de la familia, con un prior uniforme y como máximo 50.000 miembros.
- **$|Y_j|$** es el número de valores que podría reportar el observador.
- **Solo aplica con proyección.**
- **Límite conocido:** una instancia fija propuesta después de ver los datos se trata como una predicción. Falta dar crédito solo a lo que se dijo antes de mirar.

## Decisión

- **Empate:** si varias hipótesis coherentes quedan a menos de δ = 10⁻⁶ de la mejor, no hay ganadora y el caso queda **subdeterminado**.
- **Derrota:** una observación nueva con ω ≥ ω_d = 0,95 que contradice una hipótesis la derrota. Con ω menor, la hipótesis queda en tensión. Retractar la observación la reactiva.
- **Expansión sugerida:** cuando lo que la mejor hipótesis coherente no explica cuesta más que una entidad. Se cuentan las contradicciones (α·ω + λ·c(ω)) y los *explananda* sin explicar (α·ω).
- **Pregunta y respuesta:** con una pregunta (variable y valores), la respuesta se decide entre clases de hipótesis. Se informan el líder, el rival y el **margen**, que es cuántos veredictos de LLM habría que cambiar para invertir la respuesta. La respuesta es frágil si el margen es de 1 o menos.
- **Selección:** con proyección, gana el puntaje. Con un LLM, la selección es **holística**: un juez de otra familia ve todo junto, ordena o se abstiene, y queda registrado como juicio, no como cálculo (ADR-0016).
- **Sugerencia de observación:** ante un empate o una respuesta frágil, el motor busca el marco posible cuya predicción separa a las candidatas.

## Verdad y predicciones

- **Predicciones:** quedan registradas con su horizonte (`que_vigilar`) y no puntúan.
- **Verdad de cierre:** es una observación falible, con fuente, fecha e historia. Su estado es `sin_verdad`, `tentativa`, `establecida` o `disputada` (ADR-0013, ADR-0014).
