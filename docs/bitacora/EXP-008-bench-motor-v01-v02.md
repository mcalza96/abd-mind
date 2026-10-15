# EXP-008 — abd-bench: motor sobre V01 y V02

- **Fecha:** 2026-10-14 · **Estado:** corrido
- **Registro previo:** no (prueba de humo del ejecutor)
- **Commit / artefactos:** `76765b9`; `datasets/abd-bench/resultados/2026-10-14-motor-v01-v02/`

## Pregunta
¿El motor completo distingue el par Neptuno/Vulcano disfrazado (entidad nueva frente a ley incorrecta, en el mismo dominio)?

## Diseño
Dominio `abierto`, pregunta `tipo_de_causa`, generación contrastiva, verificador LLM de tres valores y expansión si hace falta. 31 llamadas y unos 5 minutos por caso.

## Resultado
- **El motor no determinó la respuesta en ninguno de los dos casos:** empates de 2 a 4 tipos de causa.
- **La línea base acertó ambos** con Muse; DeepSeek falló V02.

## Sorpresas y errores
- **El generador funcionó bien:** propuso una hipótesis por tipo de causa, incluida la correcta.
- **El verificador es indulgente:** casi todas las hipótesis "explican" casi todos los hechos. De 30 veredictos por caso, ninguno fue `contradice`.
- **Hipótesis inmunizada:** en V02, la conexión clandestina "explica" cinco inspecciones sin hallazgo porque el generador la volvió "sin huella visual". Es un ajuste ad hoc, y el verificador no lo castigó.
- **Parsimonia autodeclarada:** las hipótesis declaran sus propias entidades y casi todas declaran cero. Por ejemplo, "una maniobra no registrada" no se contó.

## Lecciones
- Confirma con datos las brechas B6 (hipótesis vagas) y la de parsimonia del documento 10, y las lecciones transversales 3 a 5.
- **Advertencia de sobreajuste:** la propuesta siguiente nace de solo 2 casos. Debe validarse en casos que no la motivaron.

## Decisiones derivadas
EXP-009: verificación comparativa y parsimonia juzgada por un tercero, con [ADR-0015](../historico/arquitectura/adr/0015-verificacion-comparativa.md).
