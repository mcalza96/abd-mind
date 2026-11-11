# 2026-10-16 · JKSE/IHSG · desplome −11,57% por amenaza MSCI Standalone

- **Agente y skills usadas:** Hermes Agent; abduccion, red-abductiva
- **Pregunta:** Qué pasó con Jakarta Stock Exchange Composite (JKSE/IHSG) y por qué cayó el 16-oct-2026.

## Lo sorprendente

No es que Indonesia caiga: es que el índice pierda 11,57% en un día hasta un nuevo mínimo de 2026 —el peor desplome en casi 30 años— justo después de que MSCI abriera una consulta (15-oct) para reclasificar al país directo de Emerging a Standalone, saltándose el paso por Frontier. Si fuera macro o earnings, la caída habría sido gradual y correlacionada con otros EM. Si fuera solo pánico local, no citaría a MSCI. Lo valioso si fuera de otra manera: si el índice hubiera aguantado pese a la advertencia, habría señalado que el flujo pasivo ya no pesa o que la estructura de free float había mejorado.

## Hipótesis

| Hipótesis | Familia | Qué predice distinto de la obvia (antes de mirar) | Resultado de la comprobación |
|---|---|---|---|
| H1 Amenaza MSCI: la consulta Emerging→Standalone por opacidad, free float y trading coordinado desata miedo a la exclusión y salida de flujos | decision | — (es la obvia) | sobrevive: anuncio MSCI el 15-oct; el 16-oct −8,01% a 5.393 y −11,57% a mínimo de 2026 (Jakarta Globe, 16-oct); Business Times lo llama el peor desplome en casi 30 años |
| H2 Deterioro real: macro indonesia, rupia, tasas del BI, earnings débiles, commodities | tercero-comun | deriva gradual previa, un dato macro nuevo el 15–16 y correlación con otros EM | refutada: lo predicho no se vio —ningún dato macro gatillo publicado el 15–16 en las fuentes consultadas; la inflación de septiembre fue 3,28% vs 3,19% en agosto (+0,09 pp por alimentos, movimiento menor que no distingue) |
| H3 Estructura frágil: free float bajo, concentración, opacidad y negociación coordinada vuelven al índice ilíquido y amplifican la caída | medicion | caída desproporcionada frente al fundamental más respuesta regulatoria sobre el free float (no solo miedo a la exclusión) | sobrevive: MSCI cita explícitamente opacidad, free float y trading coordinado (Jakarta Globe, 16-oct); IDX/OJK responden subiendo el free float mínimo a 15% desde 7,5%; con salvedad: el fragmento de MSCI no separa H1 de H3 (mismo motivo para ambas) —lo que distingue a H3 es la magnitud, no el motivo |

## Evidencia

- **decisiva:** el 16-oct las acciones indonesias se desplomaron 8,01% a 5.393 tras el anuncio de consulta de MSCI y perdieron 11,57% hasta un nuevo mínimo de 2026; Business Times: peor desplome en casi 30 años. Fuentes: Jakarta Globe y Business Times, 16-oct-2026 (prensa, no regulador). **Primaria no encontrada:** el comunicado de MSCI y la serie oficial de IDX no se consultaron directo. Confianza media.
- MSCI abrió consulta para reclasificar a Indonesia directo de Emerging a Standalone, con decisión final el 30-jun-2027; motivos: opacidad en la propiedad, medición del free float y trading coordinado. Fuentes: Jakarta Globe y BriefAsia, 16-oct-2026 (prensa; el comunicado primario de MSCI no se consultó).
- Respuesta regulatoria: IDX junto a OJK anuncian duplicar el free float mínimo a 15% desde 7,5% (The Jakarta Post vía asianews.network: ~US$11bn en acciones nuevas; Jakarta Globe). El ministro de Finanzas Purbaya dijo que la presión era probablemente temporal y que los reguladores estaban comprometidos a resolver lo planteado (Jakarta Globe, contrapeso).
- Macro de contexto (no gatillo): inflación anual 3,28% en septiembre vs 3,19% en agosto, por alimentos (Jakarta Globe, 01-oct).
- **No verificado (se elimina de la primera versión de esta nota):** halt de 30 min, cierre en 5.185, consulta "hasta el 30-abr-27", outflows de US$3bn pasivos + US$15bn activos, free float "15–25% desde el 9-oct", YTD −40% y cierres puntuales del 5/7-oct —ninguno aparece en los fragmentos citados de la investigación; el cierre −11,57% y la decisión 30-jun-27 sí están verificados arriba.
- Investigación: `Notes/Research/newsroom/epica-EST-mediciones/HIP-12a/news/investigaciones/2026-10-16/jkse-caida-msci-oct26/` (ficha.json, resumen-check.md, snapshots).

## Conclusión

Multi-causa H1+H3, confianza media: H1 es la causa necesaria y suficiente del timing (amenaza MSCI → expectativa de exclusión); H3 explica la magnitud (−11,57% y peor caída en casi 30 años) por estructura frágil e ilíquida. H2 queda refutada como causa del 16-oct. **Aporte sin estimar:** haría falta el flujo extranjero neto (datos KSEI/Bloomberg de la semana del 16-oct) más la comparativa con otros EM ese mismo día para repartir H1/H3. La cambiaría: si MSCI aclara antes del 30-jun-27 que mantiene a Indonesia en Emerging sin condiciones, o si el flujo extranjero neto no registra salida en la semana del 16-oct.

## Predicciones

P-20261016-10 en `campo/predicciones.csv`.

## Lo que aprendí del método

- La comprobación que más separó fue el timing anuncio→caída (15→16-oct) frente a la ausencia de gatillo macro: descartó H2 en una línea.
- H3 (medición) no compite con H1 sino que la multiplica; sin esa familia se subestima la magnitud y se atribuye todo a pánico.
- Para mercados frontera, pedir siempre la cifra de free float y la fecha de consulta/decisión de MSCI: sin ellas el relato "caída por miedo" queda sin ancla.
- La plantilla actual obliga a primaria o «primaria no encontrada»: varias cifras de la primera versión (halt, 5.185, outflows US$bn) no estaban en los fragmentos y se eliminaron en vez de sostenerlas.
