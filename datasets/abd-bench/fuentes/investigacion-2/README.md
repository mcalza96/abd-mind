# Investigación 2: salida original

Salida de la segunda investigación ([prompt](../../../../docs/investigacion/prompt-deep-research-2-casos-recientes-y-secuenciales.md)), sin modificar. Contiene 60 casos: R, S, U y F, 15 de cada conjunto. **No es un archivo de abd-bench**: hay que limpiarlo y convertirlo antes de usarlo.

## Revisión inicial (2026-10-15)

**Formato:** las 60 líneas son JSON válido, todas las observaciones tienen fecha y fuente, y los conjuntos están completos.

**Verificación puntual de fuentes posteriores a mayo de 2026** (búsqueda web):

| Caso | Fuente verificada | Estado |
|---|---|---|
| R03 | Informe final del CSB sobre la explosión de Givaudan, 2026-05-27 | Existe y coincide |
| S12 | Caída de GitHub del 17 de agosto de 2026 | Existe y coincide: falla de capacidad y tormenta de reintentos. Las fuentes del archivo son blogs secundarios; la primaria es el blog de GitHub |
| F11 | Resultados del cuarto trimestre fiscal 2026 de Supermicro, 2026-08-11 | El comunicado existe. El precio a 12 meses no está verificado |
| S13 | Juicio por Nord Stream, 2026-10-14 | No se encontró. Además es una acusación en curso, no una resolución |

**Problemas encontrados:**

1. **Observaciones escritas con conocimiento posterior.** 21 casos tienen observaciones fechadas el mismo día de la resolución o después, y en varios el texto se parece mucho al mecanismo:
   - solapamiento de 0,6 o más con el mecanismo: S01 y S15;
   - alrededor de 0,5: R06, R07, R15 y S05;
   - S13 cita, para hechos de 2022, artículos de 2026.
2. **El conjunto S está contaminado.** 11 de 15 casos son anteriores a mayo de 2026 y varios son muy conocidos (CrowdStrike, el puente de Baltimore, el Titan, el síndrome de La Habana). Solo S10, S12 y S15 sirven sin reservas; S13 está pendiente de juicio.
3. **El conjunto U es casi todo ciencia famosa** (señal Wow!, tensión de Hubble, g-2, materia oscura). Un modelo sabe que son problemas abiertos, así que abstenerse ahí mide memoria. Los menos conocidos son U08, U09, U11, U12 y U14.
4. **Mínimos sospechosos en el conjunto F.** F06, F13 y F14 tienen el mínimo justo en 2025-05-01, el primer día de la ventana pedida. Probablemente es el precio en esa fecha y no el mínimo real. Además, la mezcla no es la mitad de cada tipo: 9 rebotes, 4 caídas estructurales y 2 planas. Los precios a 12 meses no están verificados.
5. **El conjunto R es el mejor:** 15 casos resueltos entre mayo y octubre de 2026, poco famosos y con fuentes primarias (CSB, NTSB, CDC, FDA, revistas).
