# 2026-10-21 · IA · draft S-1 Anthropic: la pérdida es contable, el riesgo es contractual

- **Agente y skills usadas:** Hermes (hermes-zen), abduccion v1, red-abductiva
- **Pregunta:** ¿qué pensar del post con las cifras del supuesto S-1 de Anthropic (H1 2026: revenue 16,3B USD, pérdida 80,7B USD, compromisos de cómputo de cientos de miles de millones)? Y después: ¿seguro que la madre es el WSJ?

## Lo sorprendente

No es la pérdida de 80,7B USD: con ~72B USD de cargos contables no caja (revalorización de notas convertibles e instrumentos de financiamiento), el cash operativo del semestre ronda los 9B USD de gasto en cómputo, un orden de magnitud menor. Lo que hay que explicar es el descalce a futuro: compromisos de cómputo firmados que superan los 600B USD, mayormente no cancelables, frente a un semestre de 16,3B USD, con los proveedores (Google, AWS, Microsoft) compitiendo a la vez contra Anthropic y racionándole capacidad. Lo valioso si fuera de otra manera: si esos compromisos fueran cancelables o mucho menores, la IPO a ~2T USD sería crecimiento financiado; como están firmados, es apalancamiento operativo.

## Hipótesis

| Hipótesis | Familia | Qué predice distinto de la obvia (antes de mirar) | Resultado de la comprobación |
|---|---|---|---|
| H0 obvia: la pérdida de 80,7B USD refleja quema de caja operativa | — | el gasto en efectivo del semestre se acerca a 80B USD | refutada (gasto en cómputo H1 ~9B USD; ~72B USD son cargos contables) |
| H1 la pérdida headline es artefacto contable (convertibles) | medicion | el cash burn es un orden menor que la pérdida y el revenue crece ~15x interanual | sobrevive (cómputo H1 ~9B USD vs 80,7B USD; revenue H1 16,3B USD vs 1,1B USD H1 2025) |
| H2 el riesgo real es contractual: compromisos no cancelables | decision | el S-1 público mantiene compromisos firmados >= 500B USD con hyperscalers | sin comprobar (falta el S-1 en EDGAR; apuesta P-20261021-01) |
| H3 la valuación ~2T USD supone crecimiento perpetuo; si se frena, los costos fijos mandan | umbral | el crecimiento trimestral cae bajo ~20% QoQ y los compromisos pesan igual | sin comprobar (falta Q4; Q3 habría sido +45% QoQ según dichos a inversionistas, no auditado) |

## Evidencia

- Revenue H1 2026 16,3B USD vs 1,1B USD H1 2025 (~15x); pérdida neta H1 80,7B USD con ~72B USD contables no caja; gasto en cómputo H1 ~9B USD (2025: 7,3B USD). Vía prensa que cita el draft visto por WSJ: https://cryptobriefing.com/anthropic-ipo-draft-revenue-net-loss/ y espejo del artículo WSJ (firma Anissa Gardizy, atribución intacta): https://www.msn.com/en-us/news/other/anthropic-s-1-shows-red-hot-growth-risks-and-massive-computing-costs/ar-AA2fG3Cc?ocid=BingNewsVerp
- Compromisos cloud ~450B USD a 7-10 años, mayormente no cancelables; totales de cómputo sobre 600B USD con más acuerdos en negociación; futuro posible hasta 750B USD. Fuente: https://investinglive.com/stocks/anthropic-ipo-draft-shows-nearly-15-fold-revenue-jump-and-600-billion-in-compute-deals
- Dos clientes = ~20% del revenue H1; proveedores que ven a Anthropic cada vez más como competidor y le restringen capacidad. Fuente: https://techcrunch.com/2026/10/20/anthropics-cloud-partnerships-are-getting-messy
- Tres hitos separados (decisiva para no mezclar documentos): Reuters 28-sept-2026, prospecto confidencial 2025 (pérdida 42B USD, obligaciones 518B USD): https://www.reuters.com/business/finance/anthropics-ipo-prospectus-shows-sweeping-ai-vision-surging-costs-2026-09-28/ — Q3 16,8B USD (+45% QoQ) dicho a inversionistas, madre FT vía BI: https://www.businessinsider.com/anthropic-reveals-16-8b-revenue-amid-ipo-preparations-2026-10 — draft WSJ 20-oct-2026 (el del post): espejo MSN arriba. La cadena de citación confirma al WSJ como madre: Reuters titula esa noche "WSJ reports".
- Bear vs bull: New Constructs valoriza 144B USD (-93% vs 2T): https://finance.yahoo.com/markets/stocks/articles/unprecedented-test-investor-gullibility-analyst-113001796.html — backer espera pop a 2,4T USD: https://fortune.com/2026/10/15/anthropic-investor-ipo-financials
- Primaria no encontrada: WSJ original con paywall, draft no público, EDGAR sin S-1 a la fecha. Confianza capped por esto.

## Conclusión

La pérdida headline es contable (H1 sobrevive, H0 refutada); el riesgo que decide la tesis es contractual (H2, sin comprobar hasta el filing). Confianza media, ~0,65, apoyada en prensa abierta convergente sin primaria. Lo que la cambiaría: S-1 público con compromisos firmados bajo 400B USD → H2 refutada; crecimiento trimestral bajo ~20% QoQ con costos fijos intactos → H3 al frente.

## Predicciones

P-20261021-01, P-20261021-02

## Lo que aprendí del método

La comprobación barata que más separó fue partir la madeja en tres hitos (Reuters-sept vs FT-Q3 vs WSJ-oct): sin eso, las cifras de 518B y 750B parecían contradecirse y eran documentos distintos. Error propio a corregir: dar por bueno el desglose del post (450B, 111B Google, 31B Microsoft, 86B Nvidia) sin verificarlo línea por línea; quedó marcado por confirmar. Hueco detectado: abd-mind y newsroom no tenían nada sobre Anthropic; esta nota lo estrena.
