# Glosario y notación

## Notación

| Símbolo | Significado | Definido en |
|---|---|---|
| $\mathcal{S}$ | Espacio de mecanismos y estados latentes (abierto) | [03 §3.1](03-formalizacion.md#31-espacios-y-observadores) |
| $\mathcal{V}$ | Vocabulario verificado actual | [03 §3.1](03-formalizacion.md#31-espacios-y-observadores) |
| $O_i$ | Observador $i$ | [03 §3.1](03-formalizacion.md#31-espacios-y-observadores) |
| $\pi_{O_i}$, $\pi_i$ | Operador de proyección del observador $i$ | [03 §3.1](03-formalizacion.md#31-espacios-y-observadores) |
| $y_i$, $Y$ | Observación $i$; conjunto de observaciones ($m$ en total) | [03 §3.1](03-formalizacion.md#31-espacios-y-observadores) |
| $\eta_i$ | Ruido intra-marco | [03 §3.1](03-formalizacion.md#31-espacios-y-observadores) |
| $\mathcal{R}$ | Reglas invariantes del dominio | [03 §3.1](03-formalizacion.md#31-espacios-y-observadores) |
| $H$, $\mathcal{H}$ | Hipótesis; conjunto de hipótesis generadas | [03 §3.2](03-formalizacion.md#32-hipótesis) |
| $L(H)$ | Entidades latentes nuevas que postula $H$ | [03 §3.2](03-formalizacion.md#32-hipótesis) |
| $\Phi(H)$ | Predicados de consistencia de $H$ | [03 §3.2](03-formalizacion.md#32-hipótesis) |
| $\approx$, $d_i$, $\varepsilon_i$ | Relación de consistencia, discrepancia y tolerancia del observador $i$ | [03 §3.3](03-formalizacion.md#33-relación-de-consistencia) |
| $P$, $C$, $K$ | Parsimonia, consiliencia, coherencia | [04 §4.2](04-funcion-objetivo-ibe.md#42-las-tres-virtudes) |
| $\alpha$, $\beta$, $\gamma$ | Pesos de $C$, $K$, $P$ | [04 §4.3](04-funcion-objetivo-ibe.md#43-el-score-abductivo) |
| $\tau$ | Umbral de aceptación | [04 §4.3](04-funcion-objetivo-ibe.md#43-el-score-abductivo) |
| $H^*$ | Hipótesis ganadora actual | [04 §4.3](04-funcion-objetivo-ibe.md#43-el-score-abductivo) |

## Términos

**Abducción.** Inferencia que va de una observación sorprendente a una hipótesis que, de ser cierta, la haría esperable. *Peirceana* o *ampliativa* cuando puede introducir conceptos nuevos; *deducción inversa* cuando solo busca dentro de una ontología fija.

**Ampliación (expansión) ontológica.** Agregar a $\mathcal{S}$ una variable latente no observada porque ninguna hipótesis con el vocabulario actual reconcilia las observaciones.

**Coherencia externa ($K$).** Compatibilidad de una hipótesis con las reglas invariantes del dominio, decidida por un motor de reglas.

**Consiliencia ($C$).** Número de observaciones que una hipótesis hace esperables. Poder unificador.

**Córtex perceptivo.** Módulo LLM que convierte observaciones en lenguaje natural en hechos y predicados estructurados.

**Derrotabilidad.** Propiedad de una conclusión de poder ser retirada ante evidencia nueva sin reentrenar. El razonamiento es *no monótono*.

**Entidad latente.** Entidad, variable o mecanismo que una hipótesis postula y que no ha sido observada ni verificada.

**IBE (Inferencia a la Mejor Explicación).** Elegir, entre hipótesis rivales, la que mejor satisface un conjunto de virtudes explicativas.

**Invariante causal.** Ley o restricción del mecanismo generativo que no depende del marco del observador.

**Línea base.** LLM en decodificación directa (una llamada, sin pipeline) evaluado con el mismo verificador. Referencia obligatoria de todo experimento.

**Marco de referencia (del observador).** Perspectiva, instrumental y convenciones que determinan qué puede registrar un observador de $S$.

**Motor de reglas.** Componente determinista que evalúa predicados contra $\mathcal{R}$ y produce $K$.

**Parsimonia ($P$).** Número de entidades latentes no verificadas que postula una hipótesis. Menor es mejor.

**Quimera estadística.** Respuesta que promedia proyecciones incompatibles y no corresponde a ningún estado posible del mundo (p. ej., "óvalo" para un cilindro).

**Racionalización.** Producción de justificaciones lógicamente válidas para conclusiones incorrectas. Se mide como discrepancia entre lo que el generador declara explicar y lo que el verificador confirma.

**Tronco determinista.** Código sin IA que calcula el score, aplica umbral y desempate, y selecciona $H^*$.

**Verificador.** Proceso independiente del generador que decide $\pi_i(H) \approx y_i$ cuando $\pi_i$ no es computable.
