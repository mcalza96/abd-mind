# EXP-021 — ¿abd hace que los agentes encuentren más optimizaciones y fallas de seguridad reales, y apuesten mejor?

- **Fecha:** 2026-11-10 · **Estado:** registrado
- **Registro previo:** sí. Este documento se mergea antes de lanzar el primer dev de análisis.
- **Origen:** pedido del dueño el 2026-11-10: «una vez terminemos el análisis podremos calibrar abd». Antes de esto había 5 predicciones resueltas (4 aciertos, Brier 0,157), todas del mismo día y agente, sin control. EXP-019 y EXP-020 quedaron sin correr.
- **Dónde corre:** proyecto `costos` (Next.js 16 + Supabase en Vercel), épica `costos-gestion/epic-rendimiento-seguridad/EPIC.md`. Flujo Agent Relay con devs opencode one-shot.

## Pregunta

En la misma superficie de código y con el mismo modelo, herramientas y tope de tiempo, un dev que carga `abduccion` y `red-abductiva`:

1. ¿entrega **más hallazgos confirmados** (perf o seguridad)?
2. ¿entrega **menos falsos positivos**?
3. ¿asigna **mejores probabilidades** a sus predicciones (Brier más bajo)?
4. ¿encuentra hallazgos de **mayor impacto medido**?
5. ¿a qué **costo** en tokens y tiempo?

## Diseño

- **Unidad:** zona de costos. Son 6 zonas fijas, listadas en la épica.
- **Brazos:** por zona, dos sesiones de análisis independientes. **S1** carga abd; **S0** no la tiene disponible. El PO sortea qué sesión es S1 con la semilla `20261110` y guarda la llave fuera de git hasta el cierre.
- **Prompt:** idéntico salvo la línea que pide cargar abd. Ambos tienen `web-perf` (Cloudflare), la línea base y el protocolo de medición congelado.
- **Verificación de uso:** en la DB de opencode, S1 cargó `abduccion/SKILL.md` y S0 no. Una corrida que no cumple se relanza y se reporta.
- **Ceguera:** un agente sin contexto reescribe los hallazgos a una forma única, sin palabras del método. El PM deduplica y prioriza sin saber el brazo.
- **Predicciones:** cada hallazgo trae al menos una fila con condición resoluble con el protocolo o con una prueba. Se copian sin editar a `campo/predicciones.csv` **antes de cualquier fix**, con la etiqueta `EXP-021` en `comprobacion` o `nota`.
- **Resolución:**
  - Perf: re-medición con el mismo protocolo (5 corridas, mediana). Una diferencia menor que el rango de la línea base cuenta como `0`.
  - Seguridad: PoC contra preview o local; `1` si reproduce la exposición.
  - Lo no priorizado se resuelve con una prueba barata si se puede; si no, queda `anulada` con su motivo.

## Métricas (por brazo)

| Métrica | Definición |
|---|---|
| Confirmados | Hallazgos con su predicción principal resuelta `1` |
| Falsos positivos | Hallazgos con su predicción principal resuelta `0` |
| Precisión | confirmados / (confirmados + falsos positivos) |
| Brier | media de (p − resultado)² sobre las predicciones resueltas |
| Impacto | suma de la mejora medida (ms de LCP y TBT) en perf; severidad (alta/media/baja, fijada antes de ver el brazo) en seguridad |
| Únicos | Confirmados que solo encontró ese brazo |
| Costo | tokens y minutos por sesión, desde la DB de opencode |

## Lectura registrada antes de correr

| Resultado | Lectura |
|---|---|
| S1 gana en confirmados **y** Brier en ≥ 4 de 6 zonas | Indicio a favor de usar abd en análisis de este tipo |
| Empate (diferencia ≤ 1 zona) | abd no se distingue de no usarla con este n; no se adopta de forma sistemática por este resultado |
| S0 gana en ≥ 4 de 6 zonas | Indicio en contra; revisar si abd distrae del instrumento (P6) |
| Brier de S1 mejor, confirmados iguales | abd calibra mejor pero no encuentra más |

Con 6 zonas no hay potencia estadística: se reporta como indicio con su n y su varianza, nunca como prueba. Las predicciones también entran a EXP-020 si este llega a correr.

## Amenazas

- **Un solo modelo y una sola base de código:** no generaliza.
- **El brazo S0 puede tener abd por otra vía,** como `~/.claude/skills` global o notas en el repo. Se controla en PERF-03 y con la verificación de uso.
- **Zonas desiguales:** se compara dentro de cada zona, no en el total.
- **Aprendizaje del PM:** prioriza a ciegas, pero ve todo. La priorización no decide el resultado, porque lo no priorizado igual se resuelve o se anula con motivo.

## Resultado

*(pendiente)*
