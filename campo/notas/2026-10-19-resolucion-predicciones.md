# 2026-10-19 · bolsas Asia · resolución de predicciones vencidas (P-20261015-01)

- **Agente y skills usadas:** opencode, red-abductiva (resolución; sin abducción causal)
- **Pregunta:** Resolver las filas de `campo/predicciones.csv` con `resolver_el` ≤ 2026-10-19 y `resultado` vacío (ticket ABD-05, pasos 2-4).

## Lo sorprendente

No hay sorpresa causal: es nota de resolución. Lo que había que resolver era una sola fila vencida, P-20261015-01, que junta dos condiciones en una afirmación («cierra sobre 5.554 **y** rebote ≥ +2 % desde el mínimo»). Una condición pasa y la otra no, así que la lectura literal decide el resultado.

## Hipótesis

No aplica: no es un análisis causal y no se generan rivales. Las dos condiciones de P-01 y su veredicto van en Evidencia y Conclusión.

## Evidencia

- Fila P-20261015-01 (`resolver_el` 2026-10-16, p = 0,6): «KOSPI cierra el 16-oct-2026 sobre 5.554 con rebote intradiario de al menos +2% desde el minimo».
- Fuente primaria intentada: KRX `data.krx.co.kr` devuelve HTTP 403 el 19-oct-2026 (`curl -I`: `HTTP/2 403`, `content-language: ko-KR`); no se pudo extraer el cierre ahí. Se recurre a dos fuentes independientes con la cifra literal, como permite el ticket.
- Investing.com, `KOSPI Historical Data` (https://www.investing.com/indices/kospi-historical-data), fila literal del 16-oct-2026: `Oct 16, 2026 | 5,668.05 | 5,653.99 | 5,809.94 | 5,590.33 | 298.85M | +2.05%` (Price | Open | High | Low | Vol. | Change %).
- Seoul Economic Daily (https://en.sedaily.com/finance/2026/10/16/kospi-closes-up-205-percent-at-566805): «Closes at 5,668.05, Up 113.83 Points, or 2.05 %». Confirma el cierre en segunda fuente independiente. Chosun (https://www.chosun.com/english/market-money-en/2026/10/16/VEL5V2EF2JCXJOWFBKM3UTBELA) repite la misma cifra: cierre 5.668,05, +113,83 (+2,05 %).
- Cálculo con las cifras literales: condición 1, cierre 5.668,05 > 5.554 → se cumple (también sobre el cierre previo 5.554,22). Condición 2, lectura literal cierre-vs-mínimo: (5.668,05 − 5.590,33) / 5.590,33 = 1,390 % < 2 % → no se cumple.
- Ambigüedad anotada sin cambiar la fila: si «rebote intradiario» se leyera como máximo-vs-mínimo, (5.809,94 − 5.590,33) / 5.590,33 = 3,928 % ≥ 2 % y la afirmación pasaría. Se resuelve con la lectura literal (el que «cierra» es el que trae el rebote: cierre vs mínimo), que da `0`.
- No vencidas al 19-oct-2026 y por tanto no resueltas: P-20261015-02 (`resolver_el` 2026-10-29). P-03 (22-oct), P-06 (23-oct), P-05 (30-oct) y P-04 (30-nov) ni siquiera están en `main`: viven en la rama `agente/hermes/ncpl-alza-2026-10-15`, cuyo PR #13 se abrió en el paso 1 y sigue sin fusionar, así que se dejan como están.

## Conclusión

P-20261015-01 → `resultado` 0, `resuelta_el` 2026-10-19, con la fuente y las cifras de la fila del CSV. Confianza alta en las cifras (dos fuentes independientes coinciden al tick: C 5.668,05, L 5.590,33, H 5.809,94) y media en el veredicto, porque depende de la lectura literal cierre-vs-mínimo; si Marcelo fija que «rebote intradiario» quería decir máximo-vs-mínimo, el resultado pasaría a 1. La cambiaría: una serie KRX o de la Korea Exchange con un mínimo distinto de 5.590,33 que mueva el cociente al otro lado del 2 %.

## Predicciones

Ninguna nueva. Resuelta: P-20261015-01 (`0`).

## Lo que aprendí del método

- Con 1 predicción resuelta no se calcula Brier como resultado: es solo indicación (el README pide ≥ 30 resueltas por dominio para tomarlo en serio).
- Afirmación difícil de resolver: P-01 junta cierre y rebote en una sola apuesta sin decir si el rebote se mide a cierre o a máximo. Las conjunciones «con» entre dos números necesitan operador explícito (p. ej. «cierre ≥ X y (cierre − mínimo)/mínimo ≥ Y») o acaban en lectura litigable al resolver.
- Segunda dificultad: la fuente primaria (KRX) bloquea scraping anónimo (403); el plan B de dos fuentes independientes funcionó porque Investing da OHLC completo y Sedaily/Chosun confirman el cierre, pero el mínimo solo queda con doble respaldo si se cuenta el snapshot histórico de CNBC (O 5.653,99 / H 5.809,94 / L 5.590,33).
- Nada nuevo sobre rivales: en resoluciones no hay familias que generar; el trabajo es aritmética contra fuente primaria.

## Propuesta

Un cron semanal de Hermes lista cada lunes las filas con `resolver_el` vencido y `resultado` vacío, busca la fuente primaria y abre un PR `agente/hermes/resoluciones-AAAA-MM-DD` que solo toca las 3 columnas de resolución más una nota de resolución.
Lo decide Marcelo; no se implementa nada en este PR.
