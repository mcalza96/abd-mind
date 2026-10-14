# ADR-0014 — La verdad de cierre es una observación

**Estado:** aceptada. Reemplaza el punto 3 de [ADR-0013](0013-predicciones.md).

## Contexto

ADR-0013 permitía cerrar un caso con una `verdad` única que se trataba como cierta para calibrar. Eso repite el error que la tesis critica: tomar el reporte de un observador por el estado real. Ver [12 §12.1](../../marco-teorico/12-verdad-y-entrenamiento.md#121-la-verdad-de-cierre-es-una-observación).

## Decisión

1. Una verdad registrada tiene `{descripcion, valor?, fuente, marco?, confiabilidad, momento}`. Si no se declara la confiabilidad, se usa la del dominio.
2. El caso guarda un **historial** (`verdades`). `cerrar_caso(verdad?)` agrega una, y la nueva operación `registrar_verdad` agrega más incluso con el caso cerrado. Nada se sobrescribe.
3. `estado_verdad` se deriva con ω_d: `sin_verdad`, `tentativa`, `establecida` o `disputada`. Solo una verdad `establecida` sirve para calibrar.
4. Si el caso tiene pregunta, `valor` debe ser uno de sus valores.

## Consecuencias

- **+** Una verdad corregida años después (reexpresión contable, autopsia) se registra sin borrar la anterior, y el caso queda disputado hasta resolverse.
- **−** Calibrar exige verdad `establecida`, así que habrá menos casos útiles.
- **−** La independencia entre quien establece la verdad y los observadores del caso no se verifica automáticamente.
