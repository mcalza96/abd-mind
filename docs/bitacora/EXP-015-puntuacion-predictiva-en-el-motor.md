# EXP-015 — Puntuación predictiva en el motor, comparada con la consiliencia

- **Fecha:** 2026-10-15 · **Estado:** registrado
- **Registro previo:** sí (este commit va antes del código)
- **Origen:** [EXP-014](EXP-014-salas-en-codigo.md), [16, P3](../marco-teorico/16-fundamentos-desde-las-historias.md)

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

*(pendiente)*
