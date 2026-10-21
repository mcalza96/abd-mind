# 2026-10-21 · titulares investing · qué fuente usar en los cron de búsqueda

- **Agente y skills usadas:** Claude Code (PM épica TIT), abduccion + red-abductiva
- **Pregunta:** ¿cuál es el método más eficaz para los cron de búsqueda de noticias, con el volumen que usaremos?

## Lo sorprendente
La ronda de las 13:24 resolvió 2074/2074 enlaces de Google (≈4150 pedidos en 173 s). La de las 14:02 trajo el RSS completo (paso A, 14:02–14:06) y después falló el 100 % de la resolución desde el primer enlace (14:10). El RSS recién aparece bloqueado a las 15:15. Lo que hay que explicar no es que hubo un bloqueo, sino su orden: primero el resolvedor y después el RSS.

## Hipótesis
| Hipótesis | Familia | Qué predice distinto de la obvia (antes de mirar) | Resultado de la comprobación |
|---|---|---|---|
| H0: la ráfaga de resolución (≈24 pedidos/s) gatilló el bloqueo | obvia | el resolvedor cae antes que el RSS; las rondas con poca resolución no se bloquean | sobrevive: RSS ok 14:02–14:06, resolución 0/2080 a las 14:10; corridas del 20-10 con ≤400 resoluciones sin bloqueo |
| H1: lo gatilló el volumen acumulado de RSS del día (rondas + medir-lote de TIT-02h a las 13:50) | umbral | el RSS cae primero o junto con el resolvedor | refutada: el RSS de la ronda de las 14:02 salió completo (6008 crudos) con el resolvedor ya caído |
| H2: otro job en la misma IP (newsroom, calendario) | tercero común | pedidos a Google de otro proceso entre 13:35 y 14:10 | sin comprobar: los crons de noticias corren a las 07:00 y 08:00 (hora de Chile); no se revisaron sus registros |
| H3: una IP de datacenter con un umbral más bajo | selección | bloqueo con volúmenes bajos | no separada de H0 con estos datos; no cambia la decisión |

## Evidencia
- **decisiva:** `rondas/2026-10-21_1324/06-traza.jsonl` tiene 2074 de 2074 con URL real, y `06-tiempo.txt` dice `s=173.3`. En `rondas/pedido-2026-10-21_140223/06-traza.jsonl` hay 0 de 2080 con URL real, y `01-tiempo.txt` dice `crudos=6008 s=258.4` (RSS ok).
- `curl news.google.com/rss/search?q=Cencosud…` a las 18:15 UTC → 503, página «Sorry...». `www.google.com/search` → 200.
- Comparación en vivo con 16 símbolos (6 CL, 10 US) contra los asignados de Google de las 13:24 (coincidencia de título por Jaccard ≥ 0,5):
  - **Bing News RSS:** 200 en 16/16, unos 12 ítems por consulta (tope), URL real dentro del enlace (`url=`). Recupera CL 9/21 (43 %) y US 4/56 (7 %).
  - **GDELT DOC:** 429 en 12/16 consultas aun con una pausa de 7 s. Recupera 2/56 en US.
- Concentración de medios en los 419 asignados: CL son 31 ítems de 27 dominios (los 10 primeros suman el 45 %). US son 388 ítems de 149 dominios. Un RSS directo por medio no cubre.
- Términos de Vertex grounding (cloud.google.com/terms/service-terms §20(k)(i)(2)): prohíben recolectar Links con medios automatizados. Fuente primaria.
- Términos de Bing News RSS para uso comercial: primaria no encontrada.

## Conclusión
El bloqueo lo causó la ráfaga de resolución, no el volumen de RSS (confianza alta, ≈85 %). El método más eficaz es Google News RSS al ritmo de siempre (≈250–300 consultas por ronda, ≈1/s, ≈900 al día) **sin resolver en la ronda** (TIT-09 + TIT-10). Bing sirve de respaldo cuando Google bloquea, sobre todo para Chile, pero no lo reemplaza. GDELT y Vertex se descartan. Confianza en el método: media-alta (≈70 %), porque no se sabe si después de este bloqueo la IP queda con menos tolerancia.
Qué la cambiaría: que una ronda solo de RSS, sin resolución, vuelva a ser bloqueada en la primera semana. Entonces el volumen de RSS sí importa, y harían falta consultas agrupadas con OR más Bing.

## Predicciones
P-20261021-01

## Lo que aprendí del método
El hecho que decidió fue el **orden** de las fallas (resolvedor antes que RSS), visible solo cruzando los tiempos de los pasos con el conteo de URL reales. Comparar fuentes por «recuperación de lo que eligió Google» está sesgado a favor de Google: lo elegido salió de su conjunto. Además, el tope de 12 ítems de Bing castiga a US, donde hay más volumen. Faltó medir lo que Bing trae y Google no.
