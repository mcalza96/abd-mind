# Interacción por Telegram

Cómo se ve un caso de punta a punta para el usuario, que habla con Hermes por Telegram. Hermes traduce la conversación en llamadas MCP; la [skill](../hermes/skills/razonamiento-abductivo/SKILL.md) le indica cómo hacerlo.

## Ejemplo: informes financieros contradictorios

> **Usuario:** Tengo dos informes sobre la empresa X que se contradicen. Te los mando. *(adjunta dos PDF)*

Hermes lee los PDF (capacidad propia de Hermes), reconoce un caso de discrepancia entre observadores y abre un caso.

```
crear_caso(descripcion="Discrepancia entre informes sobre empresa X", dominio="finanzas")
agregar_observacion(caso, observador={nombre:"Analista A", marco:"análisis fundamental"}, contenido=<extracto PDF 1>)
agregar_observacion(caso, observador={nombre:"Analista B", marco:"análisis de ventas"}, contenido=<extracto PDF 2>)
```

> **Hermes:** Abrí el caso #7. Separé hechos de opiniones:
> **Analista A** — hecho: el margen bruto cayó 4 pp en 3 trimestres. Opinión: vender.
> **Analista B** — hecho: el volumen de unidades creció 18 %. Opinión: comprar.
> Las opiniones no las uso como evidencia, solo los hechos. ¿Está bien la separación?

> **Usuario:** Sí. Agrega también que leí que el competidor principal perdió cuota.

```
agregar_observacion(caso, observador={nombre:"Prensa sectorial"}, contenido="El principal competidor perdió cuota de mercado")
```

Hermes propone sus propias hipótesis **antes** de pedir el ranking (ADR-0003), luego pide al motor que genere y evalúe.

```
proponer_hipotesis(caso, [{mecanismo:"Suben los costos de insumos"}], origen="hermes")
generar_hipotesis(caso, modo="auto")
evaluar(caso)
```

> **Hermes:** Evalué 7 explicaciones. La mejor:
> **Estrategia deliberada de reducción de precios para ganar cuota** — explica los 3 hechos (C=3), postula 1 elemento no confirmado (la estrategia no está anunciada), respeta las reglas del dominio. Score 13,5.
> Segunda: *la demanda del sector crece* — solo explica el aumento de volumen (C=1).
> Descartada por reglas: *dividendos extraordinarios*, viola "dividendos ≤ caja disponible".
> Ninguna explicación es el promedio de "comprar" y "vender": eso no explica ningún hecho.
> ¿Quieres el detalle completo?

> **Usuario:** Sí, mándamelo.

```
auditoria(caso, formato="markdown")
```

Hermes envía el informe como **archivo** (los mensajes de Telegram tienen límite de largo).

**Días después:**

> **Usuario:** La empresa X acaba de publicar que no ha cambiado sus precios de lista en 12 meses.

```
nueva_evidencia(caso, observador={nombre:"Empresa X", marco:"comunicado oficial"}, contenido=...)
```

> **Hermes:** Ese dato **derrota** la hipótesis de reducción de precios (no es compatible con precios de lista estables). Ninguna de las restantes explica los 4 hechos. Voy a buscar explicaciones nuevas… La mejor ahora: **cambio en la mezcla de ventas hacia productos de menor margen**, que explica los 4 hechos. Si el comunicado resultara incorrecto, la hipótesis anterior volvería a estar disponible.

## Reglas para Hermes en Telegram

Recogidas en la skill:

1. **Confirmar la separación hecho/opinión** cuando el córtex lo marque en `avisos` o cuando el material sea ambiguo.
2. **Proponer hipótesis propias antes de mirar el ranking.**
3. **Nunca inventar ni redondear números**: C, P, K y score se reportan tal como vienen del motor.
4. **No presentar opiniones como evidencia** ni "promediar" recomendaciones de observadores.
5. **Decir explícitamente** cuando no hay explicación suficiente (`mejor_explicacion` → `null`) en lugar de elegir la menos mala.
6. **Mensajes cortos** con lo esencial (ganadora, por qué, siguiente alternativa); el detalle va como archivo.
7. **Trabajos largos:** si una operación se lanza en modo asíncrono, avisar ("estoy evaluando, te aviso") y consultar `estado_trabajo`.
8. **Reglas faltantes:** si el usuario o Hermes detectan una ley del dominio que debería existir, sugerirla como texto para que el humano la agregue al repo; nunca tratarla como regla activa.

## Seguridad del canal

- El bot de Telegram de Hermes debe restringirse a los IDs de usuario autorizados (lista de permitidos en la configuración del gateway de Hermes).
- Los documentos que se envían por Telegram pasan por el LLM de Hermes y por OpenCode Go. No enviar información que no deba salir del PC.
