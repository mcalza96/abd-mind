# Contrato MCP de abd-mind

Herramientas que el servidor MCP expone a Hermes (o a cualquier cliente MCP). Los esquemas definitivos se generan desde los modelos Pydantic de `src/factory/contracts/`; este documento fija la semántica.

## Convenciones

- Los nombres están en español, en `snake_case`, igual que los contratos de la especificación.
- Toda respuesta incluye `caso_id` cuando aplica y un campo `avisos: list[str]` (presupuesto agotado, predicados no verificables, configuración dudosa, etc.).
- Los errores se devuelven como error MCP con un `codigo` estable (tabla al final) y un mensaje legible para que Hermes lo explique al usuario.
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

**Salida:** `caso_id`, `dominio`, `version_reglas`, `pesos`.

### `listar_casos`

**Entrada:** `estado?` (`abierto` / `cerrado`), `limite?`.
**Salida:** lista de `{caso_id, descripcion, dominio, n_observaciones, n_hipotesis_vivas, h_estrella?, actualizado}`.

### `estado_caso`

Resumen del caso sin recalcular nada: observadores, observaciones activas, hipótesis por estado, $H^*$ actual si existe.

### `cerrar_caso`

Marca el caso como cerrado (sigue consultable; no admite más cambios).

## Observaciones

### `agregar_observacion`

Registra una observación de un observador. Pasa por el **córtex perceptivo**, que separa hechos de opiniones (D8).

| Entrada | Tipo | Notas |
|---|---|---|
| `caso_id` | str | |
| `observador` | {nombre, marco?} | Si no existe en el caso, se crea. `marco`: perspectiva, metodología, instrumento |
| `contenido` | str | Texto crudo (fragmento de informe, mensaje, medición) |
| `fuente` | str? | Referencia al documento o mensaje de origen |

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
| `hipotesis` | list[{mecanismo, entidades_latentes?, predicados?}] | Lo declarado se guarda como declaración, no como insumo |
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
        {"observacion_id": "obs_1.h1", "explica": true, "fuente": "verificador:<modelo>", "justificacion": "..."}
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

`expansion_sugerida` es `true` cuando ninguna hipótesis coherente alcanza $C = m$ (condición de [03 §3.5](../marco-teorico/03-formalizacion.md#35-ampliación-ontológica)).

### `mejor_explicacion`

Devuelve $H^*$ si existe una hipótesis con score $\ge \tau$; si no, `{"h_estrella": null, "motivo": "..."}`. "No hay explicación suficiente" es una respuesta válida, no un error.

## Evidencia y derrotabilidad

### `nueva_evidencia`

Igual que `agregar_observacion`, y además reevalúa **todas** las hipótesis vivas contra los hechos nuevos (D6).

**Salida adicional:** `derrotadas: [{id_hipotesis, derrotada_por}]`, `h_estrella_anterior`, `h_estrella_nueva`.

### `retractar_evidencia`

Marca una observación como retractada. Las hipótesis derrotadas únicamente por ella vuelven a estado `viva` y se reevalúa.

**Salida:** `reactivadas`, `h_estrella_nueva`.

## Consulta

### `auditoria`

Historia completa del caso: eventos, todas las hipótesis con estado y veredictos, versión de reglas y pesos, llamadas LLM (modelo, rol, costo estimado). Formato `json` o `markdown` (para que Hermes lo envíe como archivo por Telegram).

### `listar_reglas`

Reglas del dominio del caso (solo lectura).

### `estado_trabajo`

Para operaciones asíncronas: `{trabajo_id, estado: "en_curso"|"terminado"|"fallido", progreso, resultado?}`.

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
