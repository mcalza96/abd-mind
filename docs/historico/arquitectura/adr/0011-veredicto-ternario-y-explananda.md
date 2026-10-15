# ADR-0011 — Veredicto de tres valores y explananda

**Estado:** aceptada

## Contexto

El veredicto era booleano. "No explica" significaba a la vez "contradice" y "no dice nada". En dominios abiertos, un hecho neutral de fuente calibrada derrotaba a todas las hipótesis, y cada hecho no tratado cobraba el costo de suponerlo un error. Además, todo hecho se trataba como algo que hay que explicar. Ver [10](../../marco-teorico/10-validacion-caida-accion.md) (B1, B2) y [11 §11.1–11.2](../../marco-teorico/11-explicacion-en-dominios-abiertos.md).

## Decisión

1. `Veredicto.relacion ∈ {explica, neutral, contradice}`. El campo `explica` se mantiene como derivado (`relacion == explica`), y los veredictos booleanos ya guardados se leen como `explica` o `contradice`.
2. **Proyección:** devuelve `explica` o `contradice`, y `neutral` cuando la hipótesis no permite proyectar.
3. **Verificador LLM:** responde la relación con criterios explícitos. El cambio de prompt invalida la caché de veredictos LLM.
4. **Score:** C suma ω de lo explicado; el residuo cobra c(ω) solo de lo contradicho.
5. **Derrota y tensión:** solo por lo contradicho.
6. `Observacion.rol ∈ {explanandum, evidencia}`, por defecto `explanandum`. Un explanandum neutral queda *sin explicar*: suma α·ω a la pérdida que dispara la expansión, pero no cambia el score.
7. Las operaciones `agregar_observacion` y `nueva_evidencia` aceptan `rol`.

## Consecuencias

- **+** Invarianza ante evidencia irrelevante: un hecho al que todas son neutrales no cambia nada.
- **+** El dominio sintético no cambia, porque la proyección no produce `neutral` cuando puede calcularse.
- **−** El verificador LLM tiene una decisión más difícil (tres clases). La frontera entre neutral y contradice es un juicio del modelo.
- **−** Hermes debe decidir qué es explanandum. La skill debe guiarlo: lo que el usuario pregunta es explanandum, y lo que se reúne para decidir es evidencia.
