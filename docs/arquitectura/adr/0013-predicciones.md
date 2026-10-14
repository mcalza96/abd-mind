# ADR-0013 — Predicciones y cierre del ciclo

**Estado:** aceptada

## Contexto

IBE explica el pasado, pero preguntas como "¿vendrá un rebote?" son sobre el futuro. Además, sin casos cerrados con verdad conocida no hay forma de calibrar ω, δ ni k_f (L7). Ver [11 §11.5](../../marco-teorico/11-explicacion-en-dominios-abiertos.md).

## Decisión

1. `HipotesisCandidata.predicciones: [{que, horizonte, esperado}]`. Los generadores las piden y `proponer_hipotesis` las acepta. **No entran en el score.**
2. `mejor_explicacion` devuelve `que_vigilar`: predicciones del líder y del principal rival, de modo que Hermes vea en qué difieren.
3. `cerrar_caso` acepta `verdad` (texto y, si hay pregunta, el valor verdadero) y la guarda como evento.
4. Hermes programa una revisión al vencer el horizonte (cron) y registra el resultado con `nueva_evidencia`.

## Consecuencias

- **+** El ciclo predicción → observación → calibración queda cerrado en el contrato.
- **−** El horizonte es texto libre hasta implementar las fechas de 9.4.
