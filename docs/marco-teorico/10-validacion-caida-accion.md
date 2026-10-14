# 10 — Validación por ejercicio mental: ¿caída estructural o rebote?

Este documento somete el marco a una pregunta real y frecuente: *"La acción de la Empresa Z cayó 35 % en tres meses. ¿Es una caída estructural o viene un rebote?"*. Se simula, paso a paso, lo que haría Hermes con el contrato MCP actual ([contrato-mcp](../arquitectura/contrato-mcp.md)) y el motor de la fase 4b. Después se listan las brechas que aparecen.

> **Estado:** B1–B4 y B10 se abordaron en [11](11-explicacion-en-dominios-abiertos.md) (fase 4c). La conclusión sobre B2 se corrigió en 11 §11.0.

La empresa y los datos son ficticios. Los scores se calcularon con la función de [09 §9.1.4](09-robustez-epistemica.md#914-función-objetivo-extendida) y los pesos por defecto (α = 1.5, β = 10, γ = 1, λ = 1, ω_d = 0.95).

## 10.1 La simulación

### Paso 1 — Hermes abre el caso

```text
crear_caso(descripcion="¿La caída de 35 % de Z es estructural o transitoria?", dominio="finanzas")
```

El dominio `finanzas` describe la operación de la empresa (precio de venta, margen, volumen). No tiene variables de mercado: retorno relativo al sector, revisiones de estimaciones, flujos o valoración. Ver la brecha B11.

### Paso 2 — Hermes reúne evidencia y la registra

Hermes busca en la web y llama a `agregar_observacion` por cada fuente. El córtex separa los hechos de las opiniones:

| Hecho | Observador | ω |
|---|---|---|
| y1: el precio cayó 35 % en tres meses | Datos de mercado | 0.99 |
| y2: el índice del sector cayó 12 % en el mismo período | Datos de mercado | 0.99 |
| y3: ingresos −8 % interanual y margen bruto −4 pp | Informe trimestral | 0.98 |
| y4: la guía anual se recortó 15 % | Informe trimestral | 0.98 |
| y5: el volumen fue 6× el promedio el día del informe y después se normalizó | Datos de mercado | 0.99 |
| y6: un competidor lanzó hace cinco meses un sustituto más barato | Prensa | 0.9 |
| y7: los directivos compraron acciones después de la caída | Registro regulatorio | 0.98 |
| y8: un fondo grande liquidó su posición | Prensa | 0.9 |

Las opiniones quedan fuera de C. Por ejemplo: "Analista A: comprar, precio objetivo 50" y "Analista B: la tesis de inversión está rota". **Esto funciona bien:** el sistema no cuenta votos de analistas ni se contagia del rebaño.

### Paso 3 — Hipótesis

`generar_hipotesis(modo="contrastivo")` produce rivales de una sola causa. Hermes agrega dos combinaciones con `proponer_hipotesis`. El verificador LLM juzga cada par (H, y). El resultado plausible es este:

| Hipótesis | P | Explica | No explica | Score |
|---|---|---|---|---|
| H1 Erosión competitiva (pérdida de poder de precios) | 1 | y1 y3 y4 y5 y6 y8 | y2 y7 | 9.09 |
| H2 Shock transitorio (los clientes reducen inventario) | 1 | y1 y3 y4 y5 y7 | y2 y6 y8 | 7.17 |
| H3 Reajuste sectorial por tasas | 1 | y1 y2 y8 | y3 y4 y5 y6 y7 | −5.32 |
| **H4** = H1 + H3 | 2 | todo menos y7 | y7 | **14.18** |
| H5 = H2 + H3 | 2 | todo menos y6 y y8 | y6 y8 | 12.26 |
| H6 "Pánico / sentimiento negativo" | 1 | y1 y2 y5 y7 y8 | y3 y4 y6 | 6.15 |

`mejor_explicacion` devuelve H4: **estructural, con un componente sectorial**. La diferencia con H5 es 1.92 > δ, así que no hay subdeterminación y `sugerir_observacion` devuelve una lista vacía.

### Paso 4 — Llega evidencia nueva

Una semana después, Hermes registra con `nueva_evidencia` dos hechos de fuentes calibradas:

- y9 (informe del competidor, ω = 0.98): sus ventas crecieron 40 %. Lo explican H1 y H4; las demás quedan derrotadas. **Es correcto.**
- y10 (comunicado oficial, ω = 0.98): renunció el director financiero. Ninguna hipótesis lo explica, y como ω ≥ ω_d, **todas quedan derrotadas**. **Es incorrecto:** la renuncia no contradice a ninguna.

### Paso 5 — Hermes responde por Telegram

> "La mejor explicación es una erosión competitiva estructural, con un componente sectorial."

El usuario preguntó por el **futuro** ("¿vendrá un rebote?"), y el sistema respondió sobre el **pasado** ("qué produjo la caída"). Hermes tiene que hacer ese salto solo, sin apoyo del motor.

## 10.2 Lo que el ejercicio valida

- **La separación entre hechos y opiniones (D8)** evita el sesgo de rebaño de analistas.
- **ω distingue fuentes:** el informe trimestral pesa más que la prensa, y un rumor de prensa no derrota a nadie (D12).
- **La derrota es reversible:** si y9 resulta mal reportado, `retractar_evidencia` reactiva H2 y H5.
- **La auditoría** deja ver qué hecho decidió el resultado.
- **La forma del problema es abductiva:** dos lecturas incompatibles (estructural o transitoria) de los mismos datos. Es el caso para el que se diseñó el marco.

## 10.3 Brechas

Están ordenadas por gravedad. Las críticas (🔴) producen respuestas incorrectas hoy; las importantes (🟠) degradan la calidad; las menores (🟡) son extensiones.

### 🔴 B1 — "No explica" se trata igual que "contradice"

El verificador responde `explica = false` tanto si H contradice el hecho como si simplemente no habla de él. En el dominio sintético da igual: una proyección distinta es una contradicción. En dominios abiertos no. Hay dos consecuencias:

- **Derrota injusta** (paso 4, y10): un hecho neutral de fuente calibrada derrota a todas las hipótesis.
- **Residuo injusto:** H1 paga c(0.98) = 3.91 por no explicar la compra de los directivos (y7), aunque es compatible con ella. Los directivos pueden equivocarse o comprar por señalización.

**Propuesta:** un veredicto de tres valores: `explica` / `neutral` / `contradice`.

- `explica` suma a C.
- `contradice` es lo único que derrota (si ω ≥ ω_d) o cuesta c(ω) como residuo.
- `neutral` no suma ni resta, pero cuenta para medir la cobertura de la hipótesis (B2).

En el dominio sintético, la proyección solo produce `explica` o `contradice`, así que los experimentos actuales no cambian.

### 🔴 B2 — Todo hecho se trata como algo que hay que explicar

El marco asume que hay que explicar todas las observaciones (lo ideal es C = m). Pero en el caso solo y1 es el *explanandum*: lo que el usuario quiere entender. El resto es **evidencia** para elegir entre explicaciones. Mezclar ambos roles produce el efecto "cajón de sastre" (*kitchen sink*): H7 = H1 + H2 + H3 explica los ocho hechos, con P = 3 y score 18.57, y gana. Su respuesta es "es estructural, transitoria y sectorial a la vez", que no le sirve al usuario.

El problema de fondo: con ω alto, explicar un hecho más vale hasta 5 entidades (1.5 · 0.98 + 3.91 = 5.38 > γ). Sumar componentes casi siempre paga. D14 lo acepta para el tapón universal, donde la entidad es una sola. En dominios abiertos, el LLM inventa componentes sin costo.

**Propuesta:**

1. Al crear el caso se marcan los explananda. Las demás observaciones son evidencia, y solo pesan si la hipótesis las explica o las contradice (B1).
2. En una hipótesis compuesta, cada componente debe justificarse por sí mismo: tiene que explicar al menos un hecho que el resto no explique. Si no, se poda.
3. Las reglas pueden declarar componentes incompatibles (`excluye`).

### 🔴 B3 — El caso no tiene una pregunta

El usuario no pregunta "¿cuál mecanismo?", sino "¿estructural o transitorio?". Esa es una **variable de interés** que cada hipótesis fija: H1 y H4 dicen estructural; H2, H5 y H6 dicen transitorio; H3 depende de las tasas. Hay dos consecuencias:

- Un empate entre H2 y H5 no debería bloquear la respuesta, porque las dos dicen "transitorio". La subdeterminación que importa es **respecto de la pregunta**, no del mecanismo.
- `sugerir_observacion` debería priorizar las observaciones que separan las clases de la pregunta. Hoy prioriza las que separan hipótesis.

**Propuesta:** `crear_caso(pregunta={variable, valores})`. Cada hipótesis debe afirmar esa variable. `mejor_explicacion` responde en dos niveles: el valor de la pregunta (y si está determinado) y el mecanismo.

### 🔴 B4 — Explicar no es predecir

IBE elige la mejor explicación del pasado. "¿Vendrá un rebote?" necesita, además:

- **predicciones con horizonte** de cada hipótesis (por ejemplo, H2: "la guía se restablece en dos trimestres y la rotación de inventario de los clientes se normaliza");
- **señales de invalidación**: qué hecho futuro derrotaría a H*.

El motor no guarda predicciones ni fechas (lo que 9.4 dejó como propuesta). **Propuesta:** la hipótesis declara `predicciones: [{que, horizonte, valor_esperado}]`. La respuesta del caso incluye "qué vigilar". Hermes puede programar una revisión con su cron, y al vencer el horizonte registrar el resultado con `nueva_evidencia`. Así el caso se cierra con su verdad conocida y esos casos alimentan la calibración de ω (L7).

### 🟠 B5 — La consiliencia es binaria y no reparte magnitudes

y1 es un número: −35 %. El sector explica unos 12 puntos y lo idiosincrático unos 23, pero ≈ es sí o no. H3 "explica" y1 igual que H1, aunque solo dé cuenta de un tercio.

**Propuesta:** observadores derivados deterministas. El retorno anormal (−35 % − β·(−12 %)) se calcula fuera del LLM y se registra como hecho propio. Es el equivalente financiero de `proyectar_solido` y deja el reparto en la parte determinista.

### 🟠 B6 — Las hipótesis vagas explican todo

H6 ("pánico") explica cinco de ocho hechos con una sola entidad. El verificador LLM premia la elasticidad: una hipótesis que explicaría tanto el hecho como su contrario no aporta información (Popper). Aquí H6 no gana, pero con otra mezcla de hechos podría hacerlo.

**Propuesta:** en dominios con verificador LLM, una prueba contrafactual. Para cada hecho explicado se pregunta si H también explicaría el hecho opuesto. Si la respuesta es sí, ese hecho no suma a C. Duplica las llamadas por par (H, y), así que se puede limitar a las hipótesis del frente del ranking.

### 🟠 B7 — C depende de cómo el córtex divide los textos

Si el córtex divide el informe trimestral en seis hechos en vez de dos, H1 gana cuatro puntos de consiliencia sin evidencia nueva. **Propuesta:** contar líneas de evidencia, no frases: agrupar por documento de origen, que es la extensión natural de 9.3. Hoy y3 y y4 vienen del mismo informe y cuentan doble.

### 🟠 B8 — En los mercados, las creencias son causas

D8 descarta las opiniones, y en general está bien. Pero "el consenso recortó 10 % la estimación de utilidad por acción", "el interés corto subió al 18 %" o "el posicionamiento de los fondos está en mínimos" son **hechos sobre creencias**, y en los mercados esas creencias mueven el precio (reflexividad). **Propuesta:** un tercer tipo en el córtex, `hecho_sobre_creencias`: el sujeto es quien cree, se verifica como hecho y cuenta en C. La opinión del analista A sigue fuera; el hecho de que el consenso cambió, entra.

### 🟠 B9 — No hay tasas base

Ante caídas tras un recorte de guía, la literatura documenta deriva posterior al anuncio (*post-earnings announcement drift*), no reversión. IBE no tiene término de probabilidad previa: H2 podría ganar con una narrativa limpia aunque, en esa clase de referencia, la reversión sea poco frecuente. **Propuesta:** no meter priors en el score, para mantener la separación de la función objetivo. Las tasas base entran como reglas blandas empíricas (9.5) o como una "vista externa" que Hermes presenta junto a H*, nunca mezclada con ella.

### 🟠 B10 — Un margen pequeño se presenta como certeza

H4 gana por 1.92 puntos, menos que un hecho de prensa. Basta que el verificador cambie un solo veredicto (por ejemplo, que y8 también sea compatible con H5) para que gane la respuesta contraria. δ = 1e-6 solo detecta empates exactos. **Propuesta:**

- **Margen de victoria:** el mínimo de veredictos que habría que invertir para cambiar H*, y que valor de la pregunta queda con esos cambios.
- **Sugerencias también con margen frágil:** `sugerir_observacion` debe funcionar con margen frágil, no solo con empate.
- **Prueba severa del líder:** buscar el hecho que derrotaría a H*.

### 🟡 B11 — El dominio no corresponde a la pregunta

`finanzas.yaml` modela la operación de la empresa. Para esta pregunta hace falta un dominio `mercado` con:

- variables de retorno relativo, revisiones, flujos, valoración e interés corto;
- pocas reglas duras: identidades contables y retorno total = sistemático + idiosincrático.

Con pocas reglas, K es casi constante y β no discrimina. Es aceptable, pero conviene decirlo en la respuesta.

### 🟡 B12 — Sesgo en la selección de evidencia

El motor solo ve lo que Hermes le trae. Si Hermes busca "por qué cayó Z", encontrará sobre todo explicaciones bajistas. **Propuesta:** la skill de Hermes debe reunir evidencia para cada clase de la pregunta (B3) antes de evaluar, y usar `sugerir_observacion` como lista de búsqueda.

### Brechas ya identificadas que el caso confirma

- **9.3 Observadores correlacionados:** ocho notas de prensa que replican el mismo cable de agencia no son ocho fuentes.
- **9.4 Tiempo:** que el competidor lanzara su producto antes de la caída importa para la causalidad. Sin fechas, el verificador puede aceptar que un hecho posterior explique uno anterior.
- **Decisión:** "¿compro?" es teoría de decisión, con costos asimétricos. Queda fuera de alcance; Hermes debe decirlo y no presentar H* como recomendación de inversión.

## 10.4 Conclusión

El núcleo del marco funciona: proyecciones, consiliencia verificada, ω y derrota reversible. Pero el marco se diseñó con el dominio sintético, donde "no explica" es lo mismo que "contradice", todo lo observado es explanandum y la pregunta es el mecanismo. En una pregunta financiera real, esos tres supuestos fallan a la vez (B1–B3), y por eso la respuesta simulada es frágil. B4 muestra que la pregunta típica del usuario es predictiva. Por eso las predicciones con horizonte no son un extra: son lo que cierra el ciclo de calibración que L7 dejó abierto.

Orden de trabajo propuesto:

1. B1 + B2 (veredicto de tres valores y explananda), porque cambian la función objetivo.
2. B3 + B10 (pregunta del caso y margen de victoria).
3. B4 (predicciones y revisión programada vía Hermes).
4. El resto, junto con el dominio `mercado` (B11).
