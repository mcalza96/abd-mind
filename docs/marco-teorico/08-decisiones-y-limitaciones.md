# 08 — Decisiones y limitaciones

Registro de las decisiones que precisan o corrigen los documentos fuente, y de los límites que el proyecto asume conscientemente. Cada decisión tiene un identificador para referenciarla desde el código y los tests.

## Decisiones

### D1 — La consiliencia se verifica, no se declara

**Origen.** Las instrucciones de implementación calculan $C$ como `len(observaciones_explicadas)`, una lista que escribe el propio generador.

**Problema.** El generador se puntúa a sí mismo. IBE-Eval documenta que los LLM son racionalizadores fuertes: afirmarán explicar observaciones que no explican.

**Decisión.** $C(H) = \sum_i \mathbb{I}(\pi_i(H) \approx y_i)$ se calcula observación por observación con una fuente independiente: función de proyección (dominios sintéticos) o verificador separado (dominios reales). La lista del generador se conserva como predicción y la discrepancia se registra como indicador de racionalización.

**Compatibilidad.** El evaluador de la especificación se implementa tal cual como primer paso (sus tests deben pasar); la verificación independiente se agrega como insumo que reemplaza la lista declarada.

### D2 — La parsimonia se contrasta con el vocabulario verificado

**Problema.** Mismo que D1: `len(entidades_latentes)` es autodeclarado, y el generador puede subdeclarar.

**Decisión.** Una extracción independiente identifica las entidades del mecanismo; $P$ cuenta las que no están en $\mathcal{V}$. Una entidad sale de $P$ cuando se verifica y se promueve a $\mathcal{V}$.

### D3 — La coherencia usa predicados estructurados

**Origen.** El motor de reglas de ejemplo devuelve $K=0$ solo si un predicado contiene la cadena "tasa negativa".

**Problema.** Es un simulador, no una verificación: cualquier paráfrasis lo evade, y las otras dos reglas de ejemplo nunca se evalúan.

**Decisión.** Se conserva el motor de ejemplo para los tests iniciales. El motor real evalúa predicados estructurados (variable, operador, valor, y relaciones entre variables) contra reglas declaradas como datos. Si la lógica del dominio lo exige, se evalúa un solucionador SMT (p. ej. Z3) como backend.

### D4 — Dos clases de reglas: duras y blandas

**Origen.** Los documentos fuente definen $K$ de tres maneras: $\{0,1\}$, $[0,1]$ y `float`.

**Decisión.** Reglas **duras**: si alguna se viola, $K=0$ y score $-\infty$. Reglas **blandas** (opcionales): fracción satisfecha en $[0,1]$, ponderada por $\beta$. Con solo reglas duras, $\beta$ no afecta el ranking ([04, §4.4](04-funcion-objetivo-ibe.md#44-propiedad-del-peso-de-coherencia)).

### D5 — La relación $\approx$ se define por observador

**Origen.** Los documentos usan $\approx$ para consiliencia y $=$ / $\neq$ para derrotabilidad, sin definir ninguna.

**Decisión.** Una sola relación $\approx$ con discrepancia $d_i$ y tolerancia $\varepsilon_i$ por observador ([03, §3.3](03-formalizacion.md#33-relación-de-consistencia)), usada en ambos lugares. Las jerarquías de categorías (¿es un cuadrado un rectángulo?) se declaran, no se deciden caso a caso.

### D6 — La derrota reevalúa a todas y es reversible

**Origen.** La especificación derrota $H^*$ y pasa "a la siguiente mejor".

**Decisión.** Ante evidencia nueva se reevalúan todas las hipótesis vivas. Las derrotadas se conservan con la evidencia que las derrotó y pueden volver si esa evidencia se retracta ([03, §3.6](03-formalizacion.md#36-derrotabilidad-no-monotonía)).

### D7 — Umbral de aceptación y desempate explícitos

**Decisión.** Si ningún score alcanza $\tau$, el sistema no concluye. Ante empates: mayor $C$, menor $P$, luego identificador. Ningún resultado depende del orden de llegada.

### D8 — Las opiniones del observador no cuentan como observaciones

**Decisión.** El córtex perceptivo separa hechos de juicios ("vender", "comprar"). Solo los hechos entran en $Y$. Los juicios se guardan como metadatos del marco del observador: informan sobre $\pi_{O_i}$, pero no se cuentan en la consiliencia.

### D9 — Proveedor y modelos de LLM son configuración

**Decisión.** Ningún nombre de modelo en el código. Un cliente compatible con la API de OpenAI y una tabla de configuración asignan modelos a roles (córtex, generadores, verificador). La lista de modelos disponibles se consulta en tiempo de ejecución. El verificador usa, por defecto, un modelo distinto al del generador.

### D10 — Toda comparación lleva línea base

**Decisión.** Cada experimento se corre también contra un LLM en decodificación directa con las mismas observaciones y se evalúa con el mismo verificador. Sin esa comparación no hay evidencia a favor de la tesis.

## Limitaciones asumidas

### L1 — La generación sigue siendo autorregresiva

El marco ideal busca hipótesis optimizando las virtudes directamente, sin muestrear tokens. Con un LLM vía API, eso no es posible. El proyecto lo aproxima con diversidad forzada, varios modelos y selección externa ([06, §6.4](06-arquitectura.md#64-generación-aproximar-una-búsqueda-no-guiada-por-verosimilitud)). Una hipótesis que ningún modelo llega a proponer no puede ganar.

### L2 — En dominios reales, $\pi_i$ es un juicio, no una función

Fuera de los entornos sintéticos, "¿explica $H$ lo que vio $O_i$?" lo responde un verificador basado en LLM. Es independiente del generador, pero no es determinista en sentido estricto. Mitigaciones: temperatura cero, una observación por llamada, paneles de varios verificadores, registro de justificaciones.

### L3 — Sin álgebra de transición entre marcos

Los operadores $\pi_{O_i}$ se tratan por separado. No se modela cómo se transforma la observación de un marco en la de otro ($T_{ij}$). Es la condición 1 del vacío formal ([07](07-estado-del-arte.md#el-vacío-formal)) y queda fuera del alcance inicial.

### L4 — Las reglas invariantes se escriben a mano

$\mathcal{R}$ lo provee un experto. El sistema no descubre leyes invariantes nuevas; descubre hipótesis compatibles con las leyes dadas. Reglas incompletas o erróneas descartan hipótesis correctas o admiten incorrectas (ver *Safe ABL* en [07](07-estado-del-arte.md#pilar-3--aprendizaje-abductivo-más-allá-del-mundo-cerrado)).

### L5 — Los pesos son heurísticos

$\alpha$, $\beta$, $\gamma$, $\tau$ no se derivan de la teoría. Se calibran con los experimentos canónicos y se reporta la sensibilidad de los resultados a ellos ([04, §4.5](04-funcion-objetivo-ibe.md#45-el-intercambio-entre-parsimonia-y-consiliencia)).

### L6 — Explosión del espacio de hipótesis

La expansión ontológica sin límite hace crecer el espacio de búsqueda rápidamente (C-ABL lo demuestra para el caso cerrado). Se fijan presupuestos de profundidad, de número de hipótesis por ronda y de llamadas al LLM.

## Decisiones de robustez epistémica

Desarrolladas en [09 — Robustez epistémica](09-robustez-epistemica.md).

### D11 — El observador es falible, y su confiabilidad no sale del consenso

Cada observación pesa según la confiabilidad $\omega_i$ de su observador, y dejarla sin explicar cuesta $-\ln(1-\omega_i)$. $\omega_i$ viene de calibración independiente, historial en casos cerrados o el valor por defecto del dominio; nunca del acuerdo con los otros observadores del caso. ([ADR-0009](../arquitectura/adr/0009-observadores-falibles.md))

### D12 — La derrota es graduada

Solo una observación con $\omega \ge \omega_d$ derrota por sí sola a una hipótesis; las demás la dejan en tensión. La expansión ontológica se dispara cuando el residuo de la mejor hipótesis cuesta más que una entidad nueva. Con $\omega = 1$ ambas reglas coinciden con D6 y con [03 §3.5](03-formalizacion.md#35-ampliación-ontológica).

### D13 — Un empate no se resuelve por el identificador

Si varias hipótesis vivas y coherentes quedan a menos de $\delta$ del mejor score, no hay $H^*$. El sistema informa el empate y propone observaciones que separen a las candidatas (abducción activa). D7 sigue valiendo para ordenar, no para elegir. ([ADR-0010](../arquitectura/adr/0010-subdeterminacion.md))

### D14 — La parsimonia se mantiene lineal

Se evaluó usarla solo como desempate. Se rechaza: favorecería sistemáticamente a las hipótesis *ad hoc* que postulan una entidad por anomalía. Ver [09 §9.6](09-robustez-epistemica.md#96-parsimonia-y-realidad-compleja-no-se-cambia).

### Pendientes (propuestos en 09)

- Observadores correlacionados: peso por grupo de fuentes compartidas (§9.3).
- Observaciones con fecha y cambio de régimen como hipótesis candidata (§9.4).
- Naturaleza de las reglas (axiomática o empírica) y alerta de revisión (§9.5).

### L7 — La confiabilidad por defecto es una suposición

Mientras no haya historial de casos cerrados con verdad establecida, $\omega$ es una suposición del dominio, y los resultados dependen de ella. Un error sistemático de un observador no es error aleatorio: debe modelarse como parte de su marco, no de su confiabilidad.
