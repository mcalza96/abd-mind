# 07 — Estado del arte

Resumen de la síntesis bibliográfica *Epistemic Invariants, Observer-Dependent Labeling, and Abductive Learning in AI*, entregada con los documentos de diseño. Las referencias provienen de esa síntesis y deben verificarse contra la fuente primaria antes de citarse en una publicación.

## Conclusión en una línea

Ningún marco existente une las tres piezas de la tesis: (1) etiquetas como **proyecciones** dependientes del observador, (2) descubrimiento de **invariantes causales** como problema inverso entre observadores, y (3) **abducción abierta** (peirceana) que no dependa de una base de conocimiento cerrada ni de la verosimilitud de tokens. Hay cuatro paradigmas adyacentes, cada uno con una pieza.

## Pilar 1 — Proyecciones del observador vs. *ground truth*

**Lo que hay.** El *Data Perspectivism* (Cabitza, Campagner & Basile 2023; Davani, Díaz & Prabhakaran 2022) muestra que el desacuerdo entre anotadores en tareas subjetivas es sistemático, no aleatorio, y que el voto mayoritario descarta señal. Lo modela con cabezas de predicción por anotador, embeddings de anotador o distribuciones de etiquetas.

**Lo que falta.** Trata el desacuerdo como varianza estadística o sesgo personal, no como **proyección de un estado invariante** a través de un marco. No hay un operador $\pi_O$ explícito ni, por tanto, un problema inverso. Formalismos de otras áreas apuntan en esa dirección (haces/*sheaves* sobre marcos de observación; marcos de referencia cuánticos, Giacomini, Castro-Ruiz & Brukner 2019), pero no se han llevado al aprendizaje supervisado.

**Qué toma el proyecto.** La validación empírica de que el desacuerdo es informativo. Aporta el operador de proyección.

## Pilar 2 — Aprendizaje de representaciones causales e invariancia

**Lo que hay.** El principio de Mecanismos Causales Independientes (Schölkopf et al. 2021) y la Minimización de Riesgo Invariante, IRM (Arjovsky et al. 2019): buscar representaciones cuyo predictor óptimo sea el mismo en todos los entornos, para aislar relaciones causales estables.

**Lo que falta.** El "entorno" es un cambio exógeno de distribución (otro hospital, otra iluminación), no un **observador epistémico** con un marco. El descubrimiento causal se limita a aprender la estructura de un DAG sobre variables dadas; cuando los datos violan el modelo, se trata como falla de fidelidad o suficiencia causal, no como disparador para **inventar** un mecanismo nuevo.

**Qué toma el proyecto.** La idea de invariante como objetivo (Postulado 2). Aporta el disparo abductivo ante la anomalía.

## Pilar 3 — Aprendizaje abductivo más allá del mundo cerrado

**Lo que hay.** *Abductive Learning*, ABL (Zhou 2019; Dai et al. 2019): un bucle entre percepción neuronal y razonamiento simbólico sobre una base de conocimiento de primer orden. Cuando la percepción contradice la base, se busca la modificación mínima de símbolos que restaura la consistencia. Variantes recientes: ABL-Refl (Hu et al. 2025, eficiencia), C-ABL (Hu et al. 2025, demuestra que la complejidad crece cuadráticamente con el tamaño del espacio de abducción y lo controla por currículo), *Safe ABL* (Yang et al. 2025, reglas imprecisas).

**Lo que falta.** ABL vive bajo el **supuesto de mundo cerrado**: la abducción es deducción inversa dentro de una ontología fija. No puede inventar predicados fuera de su firma. Si la causa de la anomalía no está en la base, el espacio de abducción colapsa.

**Qué toma el proyecto.** El bucle percepción ↔ razonamiento y la advertencia sobre explosión combinatoria. Aporta la expansión ontológica (Postulado 3), con parsimonia como freno.

## Pilar 4 — IBE y decodificación en modelos generativos

**Lo que hay.** La IBE filosófica (Harman; Thagard 1989) con sus virtudes: parsimonia, consiliencia, coherencia, robustez epistémica. Operacionalizaciones recientes:

- **IBE-Eval** (Dalal, Valentino, Freitas & Buitelaar 2024): mide parsimonia por profundidad de prueba y deriva conceptual, coherencia por entailment NLI, incertidumbre por *hedging*. Hallazgo clave: la consistencia lógica **sola** es mala señal de corrección, porque los LLM son "racionalizadores fuertes" que producen deducciones válidas desde premisas falsas.
- **PEIRCE** (Quan et al. 2025): refina conjeturas de LLM con críticas formales (demostrador Isabelle) y modelos de virtudes.
- **Taxonomía de dos etapas** (Salimi et al. 2026): separa **generación** de hipótesis (ampliativa) de **selección** (discriminativa).

**Lo que falta.** Las virtudes se aplican *a posteriori* sobre candidatos producidos por decodificación autorregresiva, que:

1. favorece lugares comunes y racionalizaciones (patología de racionalización);
2. poda temprano conjeturas de baja probabilidad local que serían globalmente óptimas;
3. no ofrece una búsqueda guiada directamente por virtudes en un espacio latente.

**Qué toma el proyecto.** La separación generación/selección, las virtudes como función objetivo y la advertencia de IBE-Eval: por eso $C$ y $P$ no pueden ser autodeclarados ([04, §4.6](04-funcion-objetivo-ibe.md#46-riesgo-virtudes-autodeclaradas)). Aporta la selección **fuera** del LLM y generación con diversidad forzada; no resuelve el punto 3 (ver [08](08-decisiones-y-limitaciones.md)).

## Cuadro comparativo

| Paradigma | Observador | Invariante | Hipótesis abiertas |
|---|---|---|---|
| Perspectivismo | Varianza / embedding de anotador | No | No: etiquetas fijas |
| CRL / IRM | Entorno pasivo, no epistémico | Sí | No: DAG sobre variables dadas |
| ABL y variantes | Observador único | Vía base de conocimiento | No: mundo cerrado |
| IBE computacional | Persona en prompt | Verificación posterior | Limitada por decodificación autorregresiva |
| **Este proyecto** | **Operador $\pi_{O_i}$ explícito** | **Reglas $\mathcal{R}$ + consiliencia entre marcos** | **Sí, con expansión ontológica y costo de parsimonia** |

## El vacío formal

La síntesis plantea tres condiciones que la literatura no cumple a la vez:

1. **Álgebra de marcos.** Los $\pi_{O_i}$ no deberían ser embeddings estáticos sino operadores dentro de una estructura geométrica coherente, con mapas de transición entre marcos que satisfagan compatibilidad: $\pi_{O_j} = T_{ij} \circ \pi_{O_i}$ donde corresponda.
2. **Espacio de hipótesis abierto.** Debe permitir síntesis de variables, relaciones y mecanismos nuevos.
3. **Generación no autorregresiva.** La búsqueda de $H$ debería optimizar directamente un objetivo de virtudes $\mathcal{E}(H)$, sin muestrear de $p(\text{token} \mid \text{contexto})$.

**Posición del proyecto.** Aborda la condición 2 de forma operativa, la condición 1 de forma parcial (operadores explícitos por observador, sin álgebra de transiciones) y la condición 3 solo por aproximación (diversidad + selección externa). Ver [08](08-decisiones-y-limitaciones.md).

## Referencias base

| Autores | Año | Trabajo | Identificador |
|---|---|---|---|
| Cabitza, Campagner, Basile | 2023 | Toward a Perspectivist Turn in Ground Truthing for AI | DOI 10.1609/aaai.v37i13.26871 |
| Davani, Díaz, Prabhakaran | 2022 | Dealing with Disagreements | DOI 10.1162/tacl_a_00449 |
| Schölkopf et al. | 2021 | Toward Causal Representation Learning | DOI 10.1109/JPROC.2021.3058954 |
| Arjovsky, Bottou, Gulrajani, Lopez-Paz | 2019 | Invariant Risk Minimization | arXiv:1907.02893 |
| Zhou | 2019 | Abductive Learning: Towards Bridging Machine Learning and Logical Reasoning | DOI 10.1007/s11432-018-9801-4 |
| Dai, Xu, Yu, Zhou | 2019 | Bridging Machine Learning and Logical Reasoning by Abductive Learning | NeurIPS 2019 |
| Hu, Dai, Jiang, Zhou | 2025 | Efficient Rectification of Neuro-Symbolic Reasoning Inconsistencies by Abductive Reflection | DOI 10.1609/aaai.v39i16.33905 |
| Hu, Li, Jia, et al. | 2025 | Curriculum Abductive Learning | arXiv:2505.12275 |
| Yang et al. | 2025 | Safe Abductive Learning in the Presence of Inaccurate Rules | AAAI 2025 |
| Dalal, Valentino, Freitas, Buitelaar | 2024 | Inference to the Best Explanation in Large Language Models | DOI 10.18653/v1/2024.acl-long.14 |
| Quan, Valentino, Carvalho, Dalal, Freitas | 2025 | PEIRCE: Unifying Material and Formal Reasoning via LLM-Driven Neuro-Symbolic Refinement | DOI 10.18653/v1/2025.acl-demo.2 |
| Salimi et al. | 2026 | Wiring the 'Why': A Unified Taxonomy and Survey of Abductive Reasoning in LLMs | arXiv:2604.08016 |
| Thagard | 1989 | Explanatory Coherence | DOI 10.1017/S0140525X00057046 |
| Giacomini, Castro-Ruiz, Brukner | 2019 | Quantum Mechanics and the Covariance of Physical Laws in Quantum Reference Frames | DOI 10.1038/s41467-018-08155-0 |
