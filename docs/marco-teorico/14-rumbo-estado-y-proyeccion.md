# 14 — Rumbo: el motor como capa de estado y verificación exacta

Decisión tomada con el usuario después de [EXP-010](../bitacora/EXP-010-juez-comparativo.md) y [EXP-012](../bitacora/EXP-012-bench-v2-perturbaciones-y-sin-respuesta.md). Opciones A + C.

## 14.1 Qué mostraron los experimentos

- **Dominio con proyección exacta (sintético):** el motor hace lo que promete.
- **Dominios abiertos, con LLM en cada pieza:** el motor rinde por debajo de un LLM en una sola llamada en precisión, en seguimiento de la evidencia y en abstención.
- **Explicación probable:** el score suma juicios por observación y pierde los patrones entre hechos. Además, las diferencias de score son del orden del ruido de un veredicto.

No se mostró que la teoría (abducción, proyecciones, derrotabilidad) sea falsa. Lo que falla en dominios abiertos es una de sus piezas: **decidir sumando juicios independientes de un LLM.**

## 14.2 Qué hace el motor a partir de ahora

| | Dominio con proyección calculable (C) | Dominio abierto (A) |
|---|---|---|
| **Quién propone hipótesis** | Generadores LLM y Hermes | Igual |
| **Quién juzga la explicación** | El motor: score con proyección exacta (04, 09, 11) | Un **juicio holístico**: un modelo ve todas las observaciones y todas las hipótesis a la vez y las ordena, o declara que la evidencia no alcanza |
| **Qué aporta el motor** | La decisión, verificable | Estado del caso, reglas duras (K = 0 descarta), derrota y reactivación con evidencia nueva, sugerencias de observación, predicciones, verdad falible y auditoría |
| **Qué no promete** | — | Acertar más que un LLM |

**El motor no finge una precisión que no tiene.** En dominios abiertos, la elección la hace un juicio que ve todo junto y que queda registrado como tal: fuente `juicio:<modelo>`, con su justificación. El motor no la presenta como un cálculo. Sí conserva:

- las reglas duras, que siguen descartando sin apelación;
- la derrota, que se dispara cuando un hecho nuevo de fuente confiable contradice una hipótesis;
- la auditoría, que separa lo calculado de lo juzgado.

## 14.3 C: proyección calculable en dominios reales

Un hecho es verificable de forma exacta cuando se puede comparar con lo que una hipótesis afirma: variables numéricas o categóricas con una relación de consistencia definida (03 §3.3). La idea de los "observadores derivados" (10 B5) generaliza la proyección del dominio sintético:

- **Hechos estructurados:** el hecho declara variables (`retorno_anormal_3m = −0,23`, `revision_consenso = baja`).
- **Hipótesis estructuradas:** la hipótesis afirma los valores o rangos que predice.
- **Verificación híbrida:** si ambos comparten variables, el veredicto es determinista (proyección). Si no, cae al juicio. La auditoría dice cuál se usó.

El primer dominio será `mercado`: descomposición del retorno en sistemático e idiosincrático, revisiones de estimaciones, flujos, valoración y las identidades contables como reglas duras. Se valida con el conjunto F de la segunda investigación, cuyos resultados son posteriores a mayo de 2026.

## 14.4 Cómo se evalúa A

En casos estáticos, A no puede superar a la línea base, porque usa el mismo tipo de juicio. Solo se verifica que no la degrade. Su valor se mide donde la línea base no tiene memoria: **casos secuenciales** (conjunto S), con evidencia que llega por etapas.

- ¿Se ancla al primer dato?
- ¿Cambia de opinión sin razón?
- ¿Revisa cuando debe?
- ¿Deja trazado por qué cambió?

## 14.5 Qué se conserva y qué se archiva

- **Se conserva todo el código.** El score con veredictos por observación sigue siendo el método del dominio sintético y la referencia de los experimentos.
- **En dominios con `verificador: llm`, la selección por defecto pasa a ser el juicio holístico** (ADR-0016). La verificación comparativa (ADR-0015) se mantiene para la derrota y la auditoría por observación.
- **Lo que no se valida no se promociona.** El README y la skill de Hermes dejan de presentar el motor como "más preciso que un LLM".
