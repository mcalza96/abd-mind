# EXP-015 — Puntuación predictiva en el motor, comparada con la consiliencia

- **Fecha:** 2026-10-15 · **Estado:** corrido
- **Registro previo:** sí (este commit va antes del código)
- **Origen:** [EXP-014](EXP-014-salas-en-codigo.md), [16, P3](../historico/marco-teorico/16-fundamentos-desde-las-historias.md)

## Pregunta

Si la puntuación predictiva entra al motor como opción, incluyendo el error del observador según su confiabilidad, ¿en qué experimentos existentes cambia la decisión, y los cambios son mejoras?

## Diseño

**La opción.** `puntuacion: predictiva` en las reglas del dominio, o en el árbol. Por defecto sigue la consiliencia: no hay regresión.

**La puntuación.** Para cada hipótesis H, que puede ser una familia con `parametros_libres`:

$$\text{score}_\text{pred}(H) = \sum_i \log p(y_i \mid y_{-i}, H) \;-\; \gamma \cdot P(H)$$

- **Predicción de la observación oculta:** $p(y_i \mid y_{-i}, H) = \sum_\theta w_\theta^{(-i)}\,\ell_i(\theta)$, con $w^{(-i)} \propto \prod_{j \ne i} \ell_j(\theta)$ y un prior uniforme sobre los parámetros θ de la familia.
- **Verosimilitud con error del observador:** $\ell_j(\theta) = \omega_j\,[\pi_j(\theta) \approx y_j] + (1-\omega_j)/|Y_j|$. Si H no proyecta lo que vería ese observador, $\ell_j = 1/|Y_j|$.
- **Tamaño del universo:** $|Y_j|$ es el número de valores posibles de la variable observada. En el dominio `sintetico`, la silueta tiene 5.
- **Prior de las entidades nuevas:** $-\gamma P$, con γ = 1 nat por entidad no verificada. Es el prior de A5: la frecuencia como apuesta.
- **Lo que no cambia:** las reglas duras siguen descartando y la derrota sigue igual. La sugerencia de expandir conserva la regla actual.
- **Alcance:** solo dominios con proyección exacta. Con un verificador LLM no hay proyección que ajustar, y la opción no aplica.

**La comparación.** Se corren ambas puntuaciones sobre los escenarios deterministas existentes: cilindro (5.1), expansión (5.2), tercer observador (5.3), errata (ω = 0,3, 0,6, 0,9 y 1), empate y las salas de EXP-014, ahora como familias. El caso reservado usa veredictos de tabla, no proyección, así que no aplica.

## Expectativa (antes de correr)

| Id | Escenario | Expectativa | Fracaso si… |
|---|---|---|---|
| E1 | Cilindro 5.1 | Ambas eligen el cilindro | Difieren |
| E2 | Expansión 5.2 | Ambas eligen la latente. Con γ/α = 2, la consiliencia deja de elegirla, pero la predictiva la **sigue eligiendo**: la ganancia por explicar el rectángulo (≈ log 5) supera γ = 2 nats | La predictiva deja de elegirla con γ = 2 |
| E3 | Tercer observador 5.3 (ω = 1) | Ambas eligen el tapón | Difieren |
| E4 | Errata | Con ω = 0,3 **difieren**: la consiliencia conserva el cilindro, la predictiva elige el tapón por poco (−1,84 contra −1,98). Con ω ≥ 0,6, ambas eligen el tapón | La predictiva conserva el cilindro con ω = 0,3 |
| E5 | Empate | Ambas declaran el empate (esfera, cilindro, cono y elipsoide predicen lo mismo) | Alguna elige |
| E6 | Salas (historia 5), familias con medidas {4, 7, 10} | La predictiva ordena: lámpara torcida primera, Merlín último; el cilindro supera al cilindro elíptico. La consiliencia empata a la verdad con Merlín, como en EXP-014 | Merlín no queda último, o la lámpara no queda primera |
| E7 | Historia 8 | Con las dos puntuaciones, cubo y cubo hueco empatan | Alguna los separa |
| E8 | Toda la suite | Las pruebas existentes pasan sin cambios | Alguna falla |

**Interpretación registrada antes de correr.** E4 con ω = 0,3 no es claramente una mejora. El tapón se propuso **después** de ver el triángulo, como instancia fija, y la predictiva lo trata como si lo hubiera predicho. La diferencia muestra el límite del diseño: sin familias declaradas ni orden temporal (qué se registró antes de qué), una hipótesis hecha a la medida solo paga el prior γ. E2 muestra lo mismo.

## Resultado

**Implementación:**

- `parametros_libres` en `HipotesisCandidata`: una hipótesis puede ser una familia.
- El módulo `transition/deterministic/prediccion.py`.
- El campo `score_predictivo`, que se calcula siempre que el dominio proyecta, en cualquiera de los dos modos.
- La opción `puntuacion` en las reglas del dominio y en `ArbolHipotesis`.
- Experimento: `abd-mind experimento puntuacion`. Pruebas: `tests/units/test_prediccion.py`.

Se cumplió E8: las 125 pruebas previas pasan sin cambios, 128 con las nuevas.

### H* con cada puntuación

| Escenario | Consiliencia | Predictiva |
|---|---|---|
| E1 cilindro 5.1 | cilindro | cilindro |
| E2 expansión, α = 1,5, γ = 1 | latente | latente |
| E2 expansión, α = 1, γ = 2 | empate esfera–cono | **latente** |
| E3 tercer observador | tapón | tapón |
| E4 errata, ω = 0,3 | cilindro | **tapón** (−1,84 contra −1,98) |
| E4 errata, ω = 0,6 / 0,9 / 1 | tapón | tapón |
| E5 empate | empate de cuatro | empate de cuatro |
| E7 cubo y cubo hueco | — | empate: volumen sin determinar |

E1 a E5 y E7 se cumplen tal como se registraron, incluidas las dos divergencias anunciadas (E2 con γ = 2 y E4 con ω = 0,3).

### E6: historia 5 con familias (ω = 0,95)

| Familia | Medidas {4, 7, 10} | Medidas {2, 4, 7, 10, 12} |
|---|---|---|
| Lámpara torcida (verdad) | **−1,25** | **−1,55** |
| Objeto que se deforma | −2,38 | −3,42 |
| Pantalla de Sara distorsionada | −2,40 | −3,45 |
| Cilindro (Tomás se equivocó) | −5,37 | −6,41 |
| Merlín | −6,59 | −9,66 |
| Cilindro elíptico | −10,17 | −12,72 |

**E6 se cumple en parte.** La lámpara queda primera y el cilindro supera al cilindro elíptico. Merlín queda bajo el cilindro, pero no último: el último es el cilindro elíptico. La segunda columna es una sensibilidad agregada **después** de ver la primera; no estaba registrada.

## Sorpresas y errores

1. **Una predicción segura y equivocada cuesta más que no predecir.** El cilindro elíptico predice con precisión (el costado de 7) y se equivoca dos veces. Merlín no predice nada y paga 1/|Y| en cada ventana. Con una regla de puntuación propia, eso es lo correcto: quien arriesga y falla pierde más que quien no arriesga. Por eso **el castigo a Merlín depende de cuántas cosas podían pasar**: con 9 siluetas posibles por ventana está 1,2 nats bajo el cilindro, y con 25, 3,3 nats. A24 queda cuantificado: lo que prohíbe una hipótesis vale log |Y| por ventana.
2. **Los resultados dependen de la discretización.** El tamaño del universo y de los parámetros funciona como un prior. Con pocas medidas posibles, las familias con parámetros libres salen baratas. Es una elección de modelo que hay que declarar, no un detalle técnico.
3. **Con error del observador, culpar a Tomás sale caro.** El cilindro simple (−5,37) queda bajo las auxiliares de error, porque solo le asigna (1 − ω)/|Y| a la elipse. Las auxiliares, en cambio, dicen **cómo** falla el instrumento. Esto confirma A15 y A16: dar un mecanismo de error concreto es mejor que culpar al observador en abstracto.
4. **E2 y E4 confirman el límite anunciado.** La predictiva acepta la latente con γ = 2 y el tapón con ω = 0,3 porque ambas son **instancias fijas propuestas después** de ver los datos. Para la puntuación predictiva son predicciones perfectas. La consiliencia las frenaba con un término de parsimonia arbitrario; la predictiva solo con el prior γ. Ninguna de las dos sabe **cuándo** se propuso cada hipótesis.

## Lecciones

- La puntuación predictiva se comporta como se esperaba en los escenarios simples, y donde difiere lo hace por las razones registradas antes de correr.
- **Lo que resuelve:** Merlín, la coincidencia como evidencia, el mecanismo de error concreto frente al genérico y los empates legítimos.
- **Lo que no resuelve:** las hipótesis hechas a la medida y presentadas como fijas. Para eso falta la dimensión temporal: dar crédito solo por lo que una hipótesis registró **antes** de ver la observación (historia 4, el sobre cerrado).

## Decisiones derivadas

- **Valor por defecto:** la opción queda disponible y el dominio `sintetico` sigue con la consiliencia. No se cambia hasta resolver lo que la predictiva no resuelve.
- **Siguiente paso: el orden temporal.** Cada veredicto guarda si la hipótesis existía antes que la observación. Lo explicado después de ver no da crédito, o da menos. Es la versión de P3 que no depende de que el generador declare familias.
- **Se declara el universo |Y| y las medidas posibles de cada dominio:** son parte del modelo.
