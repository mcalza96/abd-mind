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
| $\omega_i$ | Confiabilidad del observador $i$: probabilidad de que su reporte no sea un error grosero | [09 §9.1.2](09-robustez-epistemica.md#912-observación-con-canal-de-error) |
| $E(H)$, $R(H)$ | Observaciones que $H$ explica; su residuo (las que atribuye a error) | [09 §9.1.4](09-robustez-epistemica.md#914-función-objetivo-extendida) |
| $\lambda$ | Peso del costo del residuo | [09 §9.1.4](09-robustez-epistemica.md#914-función-objetivo-extendida) |
| $\omega_d$ | Umbral de confiabilidad para que una observación derrote por sí sola | [09 §9.1.8](09-robustez-epistemica.md#918-derrota-graduada) |
| $\delta$, $T$ | Tolerancia de empate; conjunto de hipótesis empatadas | [09 §9.2.2](09-robustez-epistemica.md#922-definiciones) |
| $\tau$ | Umbral de aceptación | [04 §4.3](04-funcion-objetivo-ibe.md#43-el-score-abductivo) |
| $H^*$ | Hipótesis ganadora actual | [04 §4.3](04-funcion-objetivo-ibe.md#43-el-score-abductivo) |

## Términos

**Abducción.** Inferencia que va de una observación sorprendente a una hipótesis que, de ser cierta, la haría esperable. *Peirceana* o *ampliativa* cuando puede introducir conceptos nuevos; *deducción inversa* cuando solo busca dentro de una ontología fija.

**Ampliación (expansión) ontológica.** Agregar a $\mathcal{S}$ una variable latente no observada porque ninguna hipótesis con el vocabulario actual reconcilia las observaciones.

**Coherencia externa ($K$).** Compatibilidad de una hipótesis con las reglas invariantes del dominio, decidida por un motor de reglas.

**Consiliencia ($C$).** Número de observaciones que una hipótesis hace esperables. Poder unificador.

**Córtex perceptivo.** Módulo LLM que convierte observaciones en lenguaje natural en hechos y predicados estructurados.

**Abducción activa.** Pedir la observación que separa hipótesis empatadas, en lugar de elegir una al azar.

**Confiabilidad ($\omega$).** Probabilidad de que un observador reporte su proyección sin error grosero. Nunca se infiere del acuerdo con otros observadores del caso.

**Derrotabilidad.** Propiedad de una conclusión de poder ser retirada ante evidencia nueva sin reentrenar. El razonamiento es *no monótono*. Con observadores falibles es graduada: solo un observador muy confiable derrota por sí solo; los demás dejan la hipótesis *en tensión*.

**Entidad latente.** Entidad, variable o mecanismo que una hipótesis postula y que no ha sido observada ni verificada.

**IBE (Inferencia a la Mejor Explicación).** Elegir, entre hipótesis rivales, la que mejor satisface un conjunto de virtudes explicativas.

**Invariante causal.** Ley o restricción del mecanismo generativo que no depende del marco del observador.

**Línea base.** LLM en decodificación directa (una llamada, sin pipeline) evaluado con el mismo verificador. Referencia obligatoria de todo experimento.

**Marco de referencia (del observador).** Perspectiva, instrumental y convenciones que determinan qué puede registrar un observador de $S$.

**Motor de reglas.** Componente determinista que evalúa predicados contra $\mathcal{R}$ y produce $K$.

**Parsimonia ($P$).** Número de entidades latentes no verificadas que postula una hipótesis. Menor es mejor.

**Quimera estadística.** Respuesta que promedia proyecciones incompatibles y no corresponde a ningún estado posible del mundo (p. ej., "óvalo" para un cilindro).

**Residuo.** Observaciones que una hipótesis contradice y que, por lo tanto, atribuye a error de sus observadores; cuesta $-\ln(1-\omega)$ cada una. Lo neutral no entra en el residuo (11 §11.1).

**Subdeterminación.** Situación en que varias hipótesis incompatibles explican la evidencia igual de bien; el sistema no elige entre ellas.

**Racionalización.** Producción de justificaciones lógicamente válidas para conclusiones incorrectas. Se mide como discrepancia entre lo que el generador declara explicar y lo que el verificador confirma.

**Tronco determinista.** Código sin IA que calcula el score, aplica umbral y desempate, y selecciona $H^*$.

**Verificador.** Proceso independiente del generador que decide $\pi_i(H) \approx y_i$ cuando $\pi_i$ no es computable.

**Evidencia (rol).** Observación que sirve para elegir entre explicaciones y no exige ser explicada (11 §11.2).

**Explanandum.** Lo que el caso quiere entender. Una hipótesis neutral ante un explanandum lo deja sin explicar (11 §11.2).

**Margen en veredictos ($k$).** Cuántos veredictos de LLM habría que cambiar para invertir la respuesta. Frágil si $k \le k_f$ (11 §11.4).

**Pregunta del caso.** Variable contrastiva cuyos valores son las respuestas posibles; la respuesta se decide entre clases de hipótesis, no entre mecanismos (11 §11.3).

**Veredicto de tres valores.** `explica`, `neutral` o `contradice`; solo lo contradicho cuesta o derrota (11 §11.1).

### Generación abductiva ([17](17-generacion-abductiva.md))

- **Disparador:** lo que indica que hay algo que explicar. Puede ser una contradicción, una coincidencia, un residuo, una ausencia, un ajuste demasiado bueno, una regularidad sin mecanismo o una pregunta sin resolver.
- **Operador abductivo:** una pregunta que cambia el marco del generador para que una explicación no obvia se vuelva probable. Por ejemplo: "¿qué otra cosa produciría exactamente lo mismo?"
- **No obvia:** improbable para el generador con la pregunta habitual, pero con alta capacidad predictiva una vez propuesta.
- **Rebuscada:** improbable para el generador y además con poca capacidad predictiva.
- **Novedad:** que una hipótesis no esté entre lo que propone la generación libre.
- **Recuperación:** que la explicación verdadera aparezca entre las candidatas.

