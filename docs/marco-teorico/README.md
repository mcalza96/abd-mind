# Marco Teórico — abd-mind

Motor de razonamiento abductivo: un pipeline orquestado que separa **percepción**, **generación de hipótesis**, **selección por virtudes explicativas** y **verificación determinista**, en lugar de usar un LLM como oráculo estadístico.

Este directorio es la referencia conceptual del proyecto. Todo módulo de código debe poder rastrearse a una definición de aquí; si el código y este marco discrepan, se corrige uno de los dos de forma explícita (ver [08 — Decisiones](08-decisiones-y-limitaciones.md)).

## Índice

| # | Documento | Contenido |
|---|---|---|
| 01 | [Problema y tesis](01-problema-y-tesis.md) | Por qué el aprendizaje supervisado tiene un techo y qué propone el proyecto |
| 02 | [Postulados epistemológicos](02-postulados.md) | Mediación, invariante causal, ampliación abductiva |
| 03 | [Formalización](03-formalizacion.md) | Espacios, operadores de proyección, problema inverso, expansión ontológica, derrotabilidad |
| 04 | [Función objetivo IBE](04-funcion-objetivo-ibe.md) | Parsimonia, consiliencia, coherencia y el score abductivo, con sus propiedades |
| 05 | [Experimentos canónicos](05-experimentos-canonicos.md) | Cilindro latente, expansión ontológica, caso financiero |
| 06 | [Arquitectura](06-arquitectura.md) | Pipeline, frontera estocástico/determinista, contratos de datos |
| 07 | [Estado del arte](07-estado-del-arte.md) | Cuatro pilares de la literatura y el vacío que ocupa el proyecto |
| 08 | [Decisiones y limitaciones](08-decisiones-y-limitaciones.md) | Correcciones a la especificación original y límites asumidos |
| — | [Glosario](glosario.md) | Términos y notación |

## Lectura rápida

1. Una etiqueta no es la verdad: es una **proyección** $y_i = \pi_{O_i}(S)$ del estado real $S$ a través del marco de un observador.
2. Cuando dos observadores discrepan, no se promedia: se busca la hipótesis $H$ que **produce ambas sombras**.
3. Si ninguna hipótesis conocida lo logra, se **amplía la ontología** con una variable latente.
4. El LLM **propone**; un backend determinista **decide** con $\text{Score}(H) = \alpha C(H) + \beta K(H) - \gamma P(H)$.
5. Toda hipótesis aceptada es **derrotable**: evidencia nueva incompatible la descarta sin reentrenar.

## Documentos fuente

Este marco consolida y precisa cinco documentos de diseño entregados al inicio del proyecto:

- *Plan Maestro: Arquitectura de Producto para Razonamiento Abductivo* (V3)
- *Arquitectura de Razonamiento Abductivo en IA: Especificación Formal de Producto* (v1.0)
- *Explicación de la Función Objetivo Abductiva (IBE)*
- *Instrucciones de Implementación para Agente Codificador: Pipeline Abductivo*
- *Epistemic Invariants, Observer-Dependent Labeling, and Abductive Learning in AI: A Critical Literature Synthesis*

Donde este marco se aparta de esos documentos, la diferencia está justificada en [08](08-decisiones-y-limitaciones.md).
