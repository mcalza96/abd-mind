# ADR-0006 — Los experimentos corren sin Hermes

**Estado:** aceptada

## Contexto

La tesis se valida comparando el pipeline contra una línea base (D10 del marco teórico). Si los experimentos pasaran por Hermes, los resultados dependerían del modelo agente, de la skill, de la memoria de Hermes y de su versión: variables que no son el objeto de estudio.

## Decisión

- Los experimentos (`experiments/`) usan el **motor directamente**, vía `engine/case_service.py` o la CLI (`abd-mind experimento <nombre>`), nunca vía Hermes.
- Cada corrida guarda: configuración (modelos por rol, pesos, presupuestos), versión de reglas, semilla, todas las respuestas de LLM (caché) y métricas.
- La línea base es un LLM en una sola llamada con las mismas observaciones; su respuesta se evalúa con el **mismo** verificador.
- Hermes se prueba aparte, con pruebas de punta a punta que verifican la **integración** (que use bien las herramientas), no la tesis.

## Consecuencias

- **+** Resultados reproducibles y atribuibles al motor.
- **+** Se pueden correr en CI o en lote sin Telegram ni Hermes.
- **−** La CLI es una segunda interfaz que mantener (pequeña).
