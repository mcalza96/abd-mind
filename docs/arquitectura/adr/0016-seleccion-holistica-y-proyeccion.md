# ADR-0016 — Selección holística en dominios abiertos y proyección calculable en dominios estructurados

**Estado:** aceptada (decisión de rumbo del usuario, opciones A + C)

## Contexto

En dominios abiertos, el score por suma de veredictos LLM rindió por debajo de un LLM en una sola llamada ([EXP-010](../../bitacora/EXP-010-juez-comparativo.md), [EXP-012](../../bitacora/EXP-012-bench-v2-perturbaciones-y-sin-respuesta.md)). Ver [14](../../historico/marco-teorico/14-rumbo-estado-y-proyeccion.md).

## Decisión

1. **Selección por dominio.** `ConjuntoReglas.seleccion ∈ {score, holistica}`. Por defecto es `score` con verificador por proyección y `holistica` con verificador LLM.
2. **Juicio holístico.** Un rol (`juez`, por defecto el modelo del verificador) recibe todas las observaciones y todas las hipótesis vivas y coherentes. Devuelve un orden, si la evidencia alcanza para decidir y una justificación. El motor lo guarda como evento y lo usa para H* y para la respuesta a la pregunta. Las reglas duras y la derrota siguen operando antes del juicio.
3. **Verificación híbrida** (C): un hecho con variables estructuradas se verifica por proyección contra las afirmaciones de la hipótesis cuando comparten variables. Si no, por juicio.
4. **Transparencia:** la evaluación informa `metodo: score | holistica`, y la auditoría separa lo calculado de lo juzgado.

## Consecuencias

- **+** En dominios abiertos el motor no queda por debajo del juicio de un LLM. Su valor está en el estado, la derrota y la auditoría.
- **+** Donde hay estructura, la verificación vuelve a ser exacta.
- **−** En dominios abiertos, la decisión deja de ser un cálculo. El margen en veredictos no aplica y se informa la confianza declarada por el juez.
- **−** Hay que construir dominios estructurados (`mercado` primero) para que C exista en la práctica.
