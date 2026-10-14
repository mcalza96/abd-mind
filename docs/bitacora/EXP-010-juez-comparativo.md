# EXP-010 — Juez de parsimonia comparativo

- **Fecha:** 2026-10-14 · **Estado:** registrado (expectativas escritas antes de implementar y correr)
- **Registro previo:** sí
- **Origen:** [EXP-009](EXP-009-verificacion-comparativa.md), abortado por el juez

## Pregunta
Las mismas de EXP-009, con un juez que no sobrecuente: ¿la verificación comparativa y la parsimonia juzgada hacen que el motor decida cuando la evidencia lo permite?

## Cambio respecto de EXP-009
1. **Juez comparativo.** Una sola llamada califica el lote de hipótesis nuevas, con las ya registradas como contexto (con sus postulados ya juzgados), para usar **la misma granularidad** en todas.
2. **Definición más estrecha de postulado:** una entidad, agente o evento independiente cuya existencia la hipótesis afirma y que ninguna observación registra. **No cuentan:**
   - reformulaciones de observaciones;
   - negaciones o ausencias;
   - afirmaciones sobre qué observación es correcta;
   - pasos o consecuencias de otro postulado (si solo existen juntos, cuentan como uno);
   - conocimiento establecido.
3. **Salida mínima:** solo nombres, sin descripción, para no agotar tokens.
4. **Prueba de humo obligatoria** antes de la corrida grande: un caso real (V02) con inspección manual de los postulados y los niveles del verificador. Lo que se observe en la prueba de humo se registra aquí antes de la corrida grande.

No se cambia ningún peso ni `peso_esperable`.

## Expectativa (antes de correr)
Se mantienen E1 a E7 de EXP-009 sin cambios, más:

| Id | Expectativa | Fracaso si… |
|---|---|---|
| E8 | El juez cuenta en promedio entre 0,5 y 4 postulados por hipótesis | Promedio mayor que 4 o igual a 0 |
| E9 | Ninguna operación falla por respuesta truncada | Una o más fallas por truncamiento |

## Diseño
Prueba de humo con `--casos V02`; después `--casos pares --paralelo 5`.

## Resultado
*(pendiente)*
