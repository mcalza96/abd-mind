# 12 — Verdad y entrenamiento

La tesis del proyecto ([01](01-problema-y-tesis.md)) es que una etiqueta no es la verdad, sino la proyección de un observador. Este documento aplica esa tesis al propio sistema: a los datos con que se lo valida o entrena y a las "verdades" que todavía trata como incuestionables.

## 12.0 Resumen

1. Los datos sintéticos solo dan verdad cuando el estado real se genera primero y los observadores se simulan con su marco y su error. Las respuestas escritas por un LLM no son verdad: son otra proyección (§12.2).
2. Cuestionar lo establecido sí, pero **con contabilidad**: dudar de una fuente confiable cuesta, y una revisión se activa por anomalías acumuladas, no por preferencia (§12.4).
3. La verdad con que se cierra un caso es una observación más, con su observador y su confiabilidad (§12.1, implementado).
4. El marco se validó hasta ahora con casos diseñados por quienes lo diseñaron. Eso es circular, y se reconoce así (§12.5).

## 12.1 La verdad de cierre es una observación

Al cerrar un caso se registra lo que realmente ocurrió. Sirve para calibrar ω, δ y k_f (L7). Tratarla como verdad absoluta repetiría el error que la tesis critica: el "ocurrió" también lo reporta alguien, desde un marco y con cierta confiabilidad. Una empresa puede reexpresar sus estados financieros años después; un diagnóstico puede corregirse en una autopsia.

**Definición.** Una verdad registrada es `{descripcion, valor?, fuente, marco?, confiabilidad ω, momento}`:

- Un caso acumula un **historial** de verdades. Se pueden agregar incluso después de cerrarlo; nada se sobrescribe.
- El **estado de la verdad** se deriva del historial con el mismo umbral ω_d de la derrota:

| Estado | Condición | ¿Sirve para calibrar? |
|---|---|---|
| `sin_verdad` | No hay registros | No |
| `tentativa` | Ningún registro alcanza ω_d | Solo ponderada por ω |
| `establecida` | Al menos uno alcanza ω_d y todos los que lo alcanzan coinciden en el valor | Sí |
| `disputada` | Dos registros que alcanzan ω_d discrepan en el valor | No, hasta resolverse |

Para que un registro sea fiable, el observador que establece la verdad debe ser independiente de los observadores del caso. Si no lo es, la calibración aprendería a confiar en quien se confirma a sí mismo. Por ahora esto es una advertencia en la skill de Hermes, no una verificación automática.

([ADR-0014](../../arquitectura/adr/0014-verdad-como-observacion.md))

## 12.2 Datos sintéticos

### Cuándo dan verdad

| Origen | ¿Hay verdad? | Por qué |
|---|---|---|
| **Mundo sintético:** se genera el estado S y cada observador lo proyecta con un marco y un modelo de error explícitos | Sí, por construcción | S se conoce antes de observarlo |
| Un LLM escribe el caso y su respuesta | No | La respuesta es la proyección del marco del modelo: el consenso que la tesis critica |
| Un humano o un agente de investigación anota la respuesta | No | Es una etiqueta; sirve como observador con su ω, no como verdad |

Entrenar con respuestas generadas por modelos recicla su marco y, repetido, degrada a los modelos (Shumailov et al., 2024, *AI models collapse when trained on recursively generated data*). Por eso el dataset de casos frontera (`boundary_cases.jsonl`) se tratará como observaciones de un observador falible, no como verdad. Sus "respuestas esperadas" sirven para encontrar casos difíciles, no para medir aciertos.

### Mundos sintéticos

Es la generalización del dominio de sólidos:

1. **Estado:** un generador produce S con variables latentes conocidas.
2. **Observadores:** cada uno tiene un marco (qué parte de S ve), una confiabilidad ω (errores groseros aleatorios) y, opcionalmente, un **sesgo sistemático**: por ejemplo, un analista que siempre reporta "baja". Un sesgo sistemático no es baja confiabilidad: es parte del marco (L7) y el motor debería atribuirlo al observador, no al estado.
3. **Correlación:** observadores que comparten fuentes (9.3) y observaciones tomadas en momentos distintos (9.4).

Usos, de menor a mayor riesgo:

- **Calibración:** estimar ω, δ y k_f sin esperar años de casos reales.
- **Regresión:** detectar cambios de comportamiento del motor.
- **Entrenamiento de roles:** por ejemplo, un verificador ajustado a veredictos de tres valores cuya respuesta correcta se conoce. Queda para la fase 7 o después, y solo con mundos sintéticos.

**Límite.** El simulador codifica la teoría del dominio de quien lo escribe. Un buen resultado en mundos sintéticos prueba que el motor es coherente con esa teoría, no que la teoría describa bien el dominio. Eso solo lo prueban casos reales cerrados con verdad `establecida`.

## 12.3 Formalizar un dominio

Hoy el conocimiento de un dominio vive en reglas YAML escritas a mano, sin proceso (L4). El camino que siguió este marco sirve como protocolo para cada dominio nuevo:

1. **Teoría del dominio:** variables, observadores típicos y sus marcos, reglas con su naturaleza (axiomática o empírica, 9.5) y qué preguntas suelen hacerse.
2. **Ejercicio mental:** simular un caso real de punta a punta, como en [10](10-validacion-caida-accion.md), y listar las brechas.
3. **Casos adversariales:** mundos sintéticos que ataquen cada supuesto: observadores sesgados, reglas en el límite, evidencia irrelevante.
4. **Casos reservados:** fijados antes de implementar cambios, con propiedades y no ganadores (11 §11.0).
5. **Validación externa:** casos reales cerrados con verdad `establecida`.

Los pasos 1 a 4 los puede hacer un LLM con supervisión. El paso 5 no.

## 12.4 Cuestionar lo establecido, con contabilidad

El progreso científico no viene de dudar de todo. Viene de dudar **con un costo** y de revisar una teoría cuando las anomalías se acumulan (Kuhn; Lakatos: programas progresivos frente a degenerativos). Una disposición general a dudar, sin costo, no es pensamiento científico sino contrarianismo; y un LLM puede racionalizar cualquier duda con la misma facilidad que cualquier conformidad.

El marco ya tiene esa estructura en el nivel de las observaciones: c(ω) es el precio de dudar de una fuente. Lo que faltaba era aplicarla a lo que el sistema trata como fijo:

| Qué se da por cierto | Estado | Cómo se cuestiona |
|---|---|---|
| Observaciones | Ya falibles (ω) | c(ω) por suponerlas erróneas; derrota reversible |
| Veredictos del verificador | Parcial | El margen en veredictos dice cuánto depende el resultado de ellos (11 §11.4) |
| Verdad de cierre | **Implementado aquí** | Historial con ω y estado; puede quedar disputada (§12.1) |
| Vocabulario "verificado" | Pendiente | Una entidad promovida debe guardar qué evidencia la verificó; si esa evidencia se retracta, vuelve a contar en P |
| Reglas del dominio | Propuesto | Registro de anomalías (abajo) |

### Registro de anomalías de las reglas (propuesto)

Extiende 9.5. En cada evaluación, si una hipótesis descartada por una regla **empírica** habría superado a H* con K = 1, se registra una anomalía contra esa regla. Cuando un caso se cierra con verdad `establecida` que coincide con la hipótesis descartada, la anomalía se marca como **confirmada**.

Una regla con anomalías confirmadas en varios casos independientes genera una propuesta de revisión para una persona. El sistema nunca la modifica solo (ADR-0004). Las reglas axiomáticas (identidades contables, física) no acumulan anomalías: si "fallan", el error está en la observación o en la formalización del caso.

El umbral de "varios casos" no se fija ahora. Se calibrará con mundos sintéticos que incluyan reglas deliberadamente falsas.

## 12.5 Circularidad y sesgos del asistente

Este marco lo redactó un LLM a partir de documentos del autor del proyecto. Los experimentos que lo validan los diseñó el mismo LLM, con verdades que él mismo fijó; incluso el caso reservado de 11 §11.6 lo escribió sabiendo qué iba a implementar. Además, los LLM se entrenan con etiquetas de consenso y tienden a coincidir con lo establecido y con su interlocutor. El acuerdo del asistente con la tesis vale poco como evidencia.

Consecuencias prácticas:

- Ningún resultado interno (experimentos, caso reservado) se presenta como validación del marco. Solo como coherencia.
- La validación externa exige casos que no haya diseñado ni el autor ni el asistente, con verdad `establecida` por observadores independientes.
- Cuando el asistente esté de acuerdo con una propuesta del autor, debe decir qué evidencia lo haría cambiar de opinión.

## 12.6 Qué no se adopta

- **Entrenar con respuestas escritas por modelos**, incluido el dataset de casos frontera como verdad.
- **Una disposición general a dudar** de lo establecido, sin costo ni contabilidad.
- **Que el agente modifique reglas**, aunque acumulen anomalías.
