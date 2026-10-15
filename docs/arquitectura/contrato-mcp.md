# Contrato MCP de abd-mind

Herramientas que el servidor MCP expone a Hermes (o a cualquier cliente MCP). Los esquemas definitivos se generan desde los modelos Pydantic de `src/factory/contracts/`; este documento fija la semántica.

## Convenciones

- Los nombres están en español, en `snake_case`, igual que los contratos de la especificación.
- Toda respuesta incluye `caso_id` cuando aplica y un campo `avisos: list[str]` (presupuesto agotado, predicados no verificables, configuración dudosa, etc.).
- Los errores se devuelven como resultado de herramienta con `isError: true` y un texto que termina en `{"codigo": "...", "mensaje": "..."}`: un `codigo` estable (tabla al final) y un mensaje legible para que Hermes lo explique al usuario.
- **Ninguna herramienta acepta como entrada valores de $C$, $P$, $K$ o score** ([ADR-0002](adr/0002-verificacion-interna.md)).
- **Ninguna herramienta modifica reglas** ([ADR-0004](adr/0004-reglas-solo-lectura.md)).

## Gestión de casos

### `crear_caso`

Abre un caso abductivo.

| Entrada | Tipo | Notas |
|---|---|---|
| `descripcion` | str | Qué se quiere explicar |
| `dominio` | str | Nombre de un archivo en `rules/` (p. ej. `finanzas`, `sintetico`) |
| `pesos` | {alpha, beta, gamma, tau}? | Opcional; por defecto los de configuración |
| `pregunta` | {variable, valores, descripcion?}? | Pregunta contrastiva, p. ej. `persistencia ∈ {estructural, transitoria, mixta}`. Cada hipótesis debe fijar la variable ([ADR-0012](adr/0012-pregunta-y-margen.md)) |

**Salida:** `caso_id`, `dominio`, `version_reglas`, `pregunta`, `pesos`.

### `listar_casos`

**Entrada:** `estado?` (`abierto` / `cerrado`), `limite?`.
**Salida:** lista de `{caso_id, descripcion, dominio, n_observaciones, n_hipotesis_vivas, h_estrella?, actualizado}`.

### `estado_caso`

Resumen del caso sin recalcular nada: observadores, observaciones activas, hipótesis por estado, $H^*$ actual si existe.

### `cerrar_caso`

Marca el caso como cerrado (sigue consultable; no admite más cambios). Entrada opcional `verdad`, igual que en `registrar_verdad`.

### `registrar_verdad`

Agrega lo que una fuente reporta que realmente ocurrió. Funciona también con el caso cerrado. La verdad es una observación, no un dato incuestionable ([ADR-0014](adr/0014-verdad-como-observacion.md)).

| Entrada | Tipo | Notas |
|---|---|---|
| `caso_id` | str | |
| `verdad` | {descripcion, valor?, fuente, marco?, confiabilidad?} | `valor`: uno de la pregunta. `fuente` debe ser independiente de los observadores del caso. Sin `confiabilidad`, la del dominio |

**Salida:** el caso, con `verdades` (historial; nada se sobrescribe) y `estado_verdad`:
- `sin_verdad`;
- `tentativa`: ninguna fuente alcanza $\omega_d$;
- `establecida`: las fuentes que alcanzan $\omega_d$ coinciden;
- `disputada`: las fuentes que alcanzan $\omega_d$ discrepan.

Solo los casos `establecida` sirven para calibrar.

## Observaciones

### `agregar_observacion`

Registra una observación de un observador. Pasa por el **córtex perceptivo**, que separa hechos de opiniones (D8).

| Entrada | Tipo | Notas |
|---|---|---|
| `caso_id` | str | |
| `observador` | {nombre, marco?, confiabilidad?} | Si no existe en el caso, se crea. `marco`: perspectiva, metodología, instrumento. `confiabilidad` ω ∈ (0, 1]: solo si hay calibración independiente; si no, se usa la del dominio ([ADR-0009](adr/0009-observadores-falibles.md)) |
| `contenido` | str | Texto crudo (fragmento de informe, mensaje, medición) |
| `fuente` | str? | Referencia al documento o mensaje de origen |
| `rol` | `"explanandum"` \| `"evidencia"` | Por defecto `explanandum`. Explanandum: lo que el caso quiere entender. Evidencia: sirve para elegir entre explicaciones y no exige ser explicada ([ADR-0011](adr/0011-veredicto-ternario-y-explananda.md)) |

**Salida:**

```json
{
  "observacion_id": "obs_3",
  "observador_id": "analista_fundamental",
  "hechos": [
    {"id": "obs_3.h1", "enunciado": "El margen bruto cayó 4 pp en tres trimestres", "variables": {"tendencia_margen_bruto": "baja"}}
  ],
  "opiniones": [
    {"enunciado": "Recomienda vender"}
  ],
  "avisos": []
}
```

Cada **hecho** es una observación atómica $y_i$ para efectos de consiliencia. Las opiniones se guardan como metadatos del marco del observador y **no** cuentan en $C$.

> Si el córtex no está seguro de si algo es hecho u opinión, lo marca en `avisos`. Hermes debe mostrárselo al usuario para que confirme (ver [interacción por Telegram](interaccion-telegram.md)).

### `corregir_observacion`

Permite al usuario (vía Hermes) reclasificar un enunciado como hecho u opinión, o corregir su texto. Queda registrado como evento.

## Hipótesis

### `generar_hipotesis`

Ejecuta los generadores propios del motor.

| Entrada | Tipo | Notas |
|---|---|---|
| `caso_id` | str | |
| `n` | int? | Hipótesis por ronda (por defecto según presupuesto) |
| `modo` | `"contrastivo"` \| `"expansion"` \| `"auto"` | `auto`: contrastivo, y expansión si ninguna viva alcanza $C = m$ |
| `ejecucion` | `"sincrono"` \| `"asincrono"` | [ADR-0008](adr/0008-presupuestos-y-trabajos-largos.md) |

**Salida:** hipótesis creadas `{id, mecanismo, entidades_latentes_declaradas, origen}`; o `trabajo_id` en modo asíncrono.

### `proponer_hipotesis`

Hermes o el usuario aportan candidatas ([ADR-0003](adr/0003-generacion-hibrida.md)).

| Entrada | Tipo | Notas |
|---|---|---|
| `caso_id` | str | |
| `hipotesis` | list[{mecanismo, entidades_latentes?, afirmaciones?, predicados?, predicciones?}] | Lo declarado se guarda como declaración, no como insumo. `predicciones: [{que, horizonte, esperado}]` no puntúan ([ADR-0013](adr/0013-predicciones.md)) |
| `origen` | `"hermes"` \| `"usuario"` | |

**Salida:** ids asignados.

## Evaluación

### `evaluar`

Verifica todas las hipótesis vivas contra todas las observaciones activas (reutilizando veredictos en caché) y calcula el ranking.

**Salida:**

```json
{
  "caso_id": "caso_7",
  "m": 3,
  "ranking": [
    {
      "id_hipotesis": "h_4",
      "mecanismo": "Estrategia deliberada de reducción de precios para ganar cuota",
      "consiliencia_c": 3,
      "parsimonia_p": 1,
      "coherencia_k": 1.0,
      "score_final": 13.5,
      "veredictos": [
        {"observacion_id": "obs_1.h1", "relacion": "explica", "fuente": "verificador:<modelo>", "justificacion": "..."}
      ],
      "declarado_vs_verificado": {"coinciden": true, "diferencias": []}
    }
  ],
  "descartadas_por_reglas": [
    {"id_hipotesis": "h_9", "regla": "dividendos_bajo_caja"}
  ],
  "expansion_sugerida": false,
  "presupuesto_agotado": false,
  "avisos": []
}
```

`expansion_sugerida` es `true` cuando el residuo de la mejor hipótesis coherente cuesta más que una entidad nueva ([09 §9.1.7](../historico/marco-teorico/09-robustez-epistemica.md#917-disparo-de-la-expansión-ontológica)); con observadores infalibles equivale a que ninguna alcance $C = m$.

Campos adicionales ([ADR-0009](adr/0009-observadores-falibles.md), [ADR-0010](adr/0010-subdeterminacion.md)):

- en cada entrada del ranking, `atribuidas_a_error`: observaciones que la hipótesis **contradice** y por lo tanto supone erróneas, con su costo; `sin_explicar`: explananda ante los que es neutral;
- `subdeterminada` y `empatadas`: si varias hipótesis empatan, no hay `h_estrella` y se listan las candidatas;
- `respuesta` ([ADR-0012](adr/0012-pregunta-y-margen.md)): `{valor, determinada, scores_por_valor, candidatas, lider, rival, margen_veredictos, fragil, sin_responder}`. Con pregunta, se decide entre sus valores: un empate de mecanismos dentro de la clase ganadora no impide responder. Sin pregunta describe a $H^*$. `margen_veredictos` es cuántos veredictos de LLM habría que cambiar para invertirla (nulo: no se puede, p. ej. con proyección); `fragil` si basta con `pesos.veredictos_fragil`.

Cada veredicto tiene `relacion`: `explica`, `neutral` o `contradice`. Solo `contradice` cuesta residuo o derrota ([ADR-0011](adr/0011-veredicto-ternario-y-explananda.md)).

### `mejor_explicacion`

Devuelve $H^*$ si existe una hipótesis con score $\ge \tau$; si no, `{"h_estrella": null, "motivo": "..."}`. "No hay explicación suficiente" es una respuesta válida, no un error.

Incluye además `respuesta` (como en `evaluar`) y `que_vigilar`: las predicciones de las candidatas en disputa (líder y rival, o las empatadas), con su `clase`. Son las señales que cambiarían la respuesta; Hermes puede programar una revisión al vencer su horizonte.

### `sugerir_observacion`

Abducción activa ([ADR-0010](adr/0010-subdeterminacion.md), [ADR-0012](adr/0012-pregunta-y-margen.md)). Actúa si hay empate, si la respuesta no está determinada o si es frágil. Con pregunta, compara la mejor hipótesis de cada clase en disputa.

**Salida:** lista de `{observador_sugerido, marco, que_observar, predicciones: {id_hipotesis: prediccion}, clases}` ordenada por poder discriminante. Vacía si el resultado no está en disputa.

## Evidencia y derrotabilidad

### `nueva_evidencia`

Igual que `agregar_observacion`, y además reevalúa **todas** las hipótesis vivas contra los hechos nuevos (D6).

**Salida adicional:** `derrotadas: [{id_hipotesis, derrotada_por}]` (solo las que **contradicen** el hecho nuevo), `en_tension` (lo contradicen pero no quedan derrotadas porque el observador no alcanza $\omega_d$), `h_estrella_anterior`, `h_estrella_nueva`. Un hecho ante el que una hipótesis es neutral no la afecta.

### `retractar_evidencia`

Marca una observación como retractada. Las hipótesis derrotadas únicamente por ella vuelven a estado `viva` y se reevalúa.

**Salida:** `reactivadas`, `h_estrella_nueva`.

## Consulta

### `auditoria`

Historia completa del caso: eventos, todas las hipótesis con estado y veredictos, versión de reglas y pesos, llamadas LLM (modelo, rol, costo estimado). Formato `json` o `markdown` (para que Hermes lo envíe como archivo por Telegram).

### `listar_reglas`

Reglas del dominio del caso (solo lectura).

### `estado_trabajo`

*Pendiente (ADR-0008): por ahora todas las operaciones son síncronas.* Para operaciones asíncronas: `{trabajo_id, estado: "en_curso"|"terminado"|"fallido", progreso, resultado?}`.

## Códigos de error

| Código | Significado |
|---|---|
| `caso_no_encontrado` | |
| `caso_cerrado` | El caso no admite cambios |
| `dominio_desconocido` | No existe `rules/<dominio>.yaml` |
| `sin_observaciones` | Se pidió generar o evaluar sin observaciones activas |
| `sin_hipotesis` | Se pidió evaluar sin hipótesis vivas |
| `presupuesto_caso_agotado` | Se agotó el presupuesto total del caso |
| `proveedor_llm_no_disponible` | Error de red, autenticación o cuota con OpenCode Go |
| `respuesta_llm_invalida` | El LLM no devolvió JSON válido tras los reintentos |
| `valor_invalido` | El valor no pertenece a la pregunta del caso (p. ej. en `cerrar_caso`) |
