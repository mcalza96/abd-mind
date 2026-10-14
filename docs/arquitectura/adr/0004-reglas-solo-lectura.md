# ADR-0004 — Las reglas del dominio son de solo lectura para el agente

**Estado:** aceptada

## Contexto

La coherencia $K$ depende del conjunto de reglas invariantes $\mathcal{R}$. Si el agente pudiera agregar, editar o desactivar reglas, podría hacer pasar una hipótesis que las viola, o descartar una correcta. Es el mismo problema de autoevaluación de ADR-0002, en otra virtud.

## Decisión

- Las reglas viven en `rules/<dominio>.yaml`, versionadas en el repositorio y revisadas por un humano.
- El servidor MCP expone `listar_reglas(dominio)` (lectura) y **ninguna** herramienta de escritura.
- Un caso declara su dominio al crearse; las reglas se cargan en ese momento y su versión (hash del archivo) queda registrada en el caso. Evaluar el mismo caso con otra versión de reglas es una operación explícita, no un efecto lateral.
- Si Hermes o el usuario detectan que falta una regla, el flujo es: Hermes lo **sugiere** en el chat → el humano edita el YAML → se recarga.

## Formato de una regla (borrador)

```yaml
dominio: finanzas
version: 1
reglas:
  - id: tasa_descuento_no_negativa
    tipo: dura
    descripcion: La tasa de descuento no puede ser negativa
    condicion: { variable: tasa_descuento, op: ">=", valor: 0 }

  - id: dividendos_bajo_caja
    tipo: dura
    descripcion: Los dividendos pagados no pueden exceder la caja disponible
    condicion: { variable: dividendos_pagados, op: "<=", variable_ref: caja_disponible }

  - id: reduccion_precio_comprime_margen
    tipo: dura
    descripcion: Una reducción de precios sostenida comprime el margen bruto
    condicion:
      si: { variable: tendencia_precio, op: "==", valor: baja_sostenida }
      entonces: { variable: tendencia_margen_bruto, op: "in", valor: [baja, estable_con_compensacion] }
```

El lenguaje exacto de condiciones se fija al implementar el motor de reglas; debe ser declarativo y evaluable sin LLM.

## Consecuencias

- **+** $K$ no puede manipularse desde la conversación.
- **+** Cada resultado es reproducible: caso + versión de reglas + versión de pesos.
- **−** Agregar conocimiento de dominio requiere intervención humana. Es intencional.
- **−** Convertir los predicados en lenguaje natural de una hipótesis a variables del YAML requiere un paso de extracción (córtex). Un predicado que no se puede mapear a ninguna variable conocida **no** viola reglas, pero se registra como "no verificable" en la auditoría.
