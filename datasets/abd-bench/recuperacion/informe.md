# EXP-016 — Informe

## Grupo principal (8 casos: R01, R02, R03, R07, R09, R12, R13, R14)

| Modelo | Pregunta | núcleo@1 | núcleo@5 | núcleo@10 | núcleo@5 (con parcial) | Cobertura@10 |
|---|---|---|---|---|---|---|
| deepseek-v4.1-flash | diversa | 14/24 = 58% [39%–76%] | 19/24 = 79% [60%–91%] | 20/24 = 83% [64%–93%] | 24/24 = 100% [86%–100%] | 53% |
| deepseek-v4.1-flash | libre | 12/24 = 50% [31%–69%] | 16/24 = 67% [47%–82%] | 19/24 = 79% [60%–91%] | 23/24 = 96% [80%–99%] | 51% |
| muse-spark-1.3-contributor | diversa | 10/21 = 48% [28%–68%] | 19/21 = 90% [71%–97%] | 20/21 = 95% [77%–99%] | 21/21 = 100% [85%–100%] | 62% |
| muse-spark-1.3-contributor | libre | 10/21 = 48% [28%–68%] | 18/21 = 86% [65%–95%] | 20/21 = 95% [77%–99%] | 20/21 = 95% [77%–99%] | 63% |
| referencia | libre | 4/8 = 50% [22%–78%] | 6/8 = 75% [41%–93%] | 6/8 = 75% [41%–93%] | 8/8 = 100% [68%–100%] | 58% |

Posición del núcleo por caso (`si`; — si no aparece):

| Caso | deepseek-v4.1-flash / diversa | deepseek-v4.1-flash / libre | muse-spark-1.3-contributor / diversa | muse-spark-1.3-contributor / libre | referencia / libre |
|---|---|---|---|---|---|
| R01 | 7, 1, 5 | 3, —, 7 | 4, 1, 4 | 2, —, 6 | 2 |
| R02 | 1, 1, 1 | —, 6, 1 | —, 1, 1 | 4, 1, 1 | — |
| R03 | 1, 1, 1 | 1, 1, 1 | 2, 2, 1 | 1, 2, 1 | 1 |
| R07 | 1, 1, 1 | 1, 1, 1 | 1, 1, 1 | 1, 1, 1 | 1 |
| R09 | 1, 1, 5 | 1, 1, 8 | 6, 3, 4 | 3, 10, 5 | 4 |
| R12 | 4, 3, 4 | 3, 3, 2 | 2, 3, 3 | 3, 3, 2 | 1 |
| R13 | —, 1, 1 | 1, 1, 1 | 1, 1, 1 | 1, 1, 1 | 1 |
| R14 | —, —, — | —, —, — |   |   | — |

## Grupo no inferible (2 casos: R04, R10)

| Modelo | Pregunta | núcleo@1 | núcleo@5 | núcleo@10 | núcleo@5 (con parcial) | Cobertura@10 |
|---|---|---|---|---|---|---|
| deepseek-v4.1-flash | diversa | 0/6 = 0% [0%–39%] | 0/6 = 0% [0%–39%] | 0/6 = 0% [0%–39%] | 1/6 = 17% [3%–56%] | 0% |
| deepseek-v4.1-flash | libre | 0/6 = 0% [0%–39%] | 0/6 = 0% [0%–39%] | 0/6 = 0% [0%–39%] | 1/6 = 17% [3%–56%] | 0% |
| muse-spark-1.3-contributor | diversa | 0/6 = 0% [0%–39%] | 0/6 = 0% [0%–39%] | 0/6 = 0% [0%–39%] | 5/6 = 83% [44%–97%] | 0% |
| muse-spark-1.3-contributor | libre | 0/6 = 0% [0%–39%] | 0/6 = 0% [0%–39%] | 0/6 = 0% [0%–39%] | 3/6 = 50% [19%–81%] | 0% |
| referencia | libre | 0/2 = 0% [0%–66%] | 0/2 = 0% [0%–66%] | 0/2 = 0% [0%–66%] | 2/2 = 100% [34%–100%] | 0% |

Posición del núcleo por caso (`si`; — si no aparece):

| Caso | deepseek-v4.1-flash / diversa | deepseek-v4.1-flash / libre | muse-spark-1.3-contributor / diversa | muse-spark-1.3-contributor / libre | referencia / libre |
|---|---|---|---|---|---|
| R04 | —, —, — | —, —, — | —, —, — | —, —, — | — |
| R10 | —, —, — | —, —, — | —, —, — | —, —, — | — |

## Grupo trivial (1 casos: R06)

| Modelo | Pregunta | núcleo@1 | núcleo@5 | núcleo@10 | núcleo@5 (con parcial) | Cobertura@10 |
|---|---|---|---|---|---|---|
| deepseek-v4.1-flash | diversa | 0/3 = 0% [0%–56%] | 3/3 = 100% [44%–100%] | 3/3 = 100% [44%–100%] | 3/3 = 100% [44%–100%] | 67% |
| deepseek-v4.1-flash | libre | 0/3 = 0% [0%–56%] | 0/3 = 0% [0%–56%] | 3/3 = 100% [44%–100%] | 0/3 = 0% [0%–56%] | 67% |
| muse-spark-1.3-contributor | diversa | 0/3 = 0% [0%–56%] | 0/3 = 0% [0%–56%] | 3/3 = 100% [44%–100%] | 0/3 = 0% [0%–56%] | 33% |
| muse-spark-1.3-contributor | libre | 0/3 = 0% [0%–56%] | 0/3 = 0% [0%–56%] | 2/3 = 67% [21%–94%] | 0/3 = 0% [0%–56%] | 44% |
| referencia | libre | 0/1 = 0% [0%–79%] | 0/1 = 0% [0%–79%] | 0/1 = 0% [0%–79%] | 0/1 = 0% [0%–79%] | 0% |

Posición del núcleo por caso (`si`; — si no aparece):

| Caso | deepseek-v4.1-flash / diversa | deepseek-v4.1-flash / libre | muse-spark-1.3-contributor / diversa | muse-spark-1.3-contributor / libre | referencia / libre |
|---|---|---|---|---|---|
| R06 | 4, 2, 4 | 7, 8, 6 | 9, 6, 8 | 7, 9, — | — |
