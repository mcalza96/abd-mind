# 2026-10-19 · TPU de Google · por qué no es alternativa a Nvidia

- **Agente y skills usadas:** Hermes, abduccion, newsroom, red-abductiva
- **Pregunta:** ¿Por qué las TPU de Google, que entrenan a Gemini, no son una verdadera alternativa a las GPU de Nvidia? ¿Líneas de producción, cadena, calidad o confianza?

## Lo sorprendente

La alternativa técnica existe y escala (4,3M de TPUs 2026, Anthropic y Meta comprando capacidad, Ironwood y v8 en producción) pero el mercado no la trata como rival real de Nvidia. Técnica que sí funciona, precio que no se mueve.

## Hipótesis

| Hipótesis | Familia | Qué predice distinto de la obvia (antes de mirar) | Resultado de la comprobación |
|---|---|---|---|
| Obvia: cuello de oferta (fábrica/cadena) o brecha de calidad | tercero-comun | shipments estancados, sin clientes externos, benchmarks adversos | `refutada` como explicación única: 4,3M en 2026 con meta 35M a 2028 (Vertex/pista) y ventaja de inferencia de hasta +50% tokens/$ (BigGo, T?) |
| H1 Medición: el efecto está en costo por token y margen de Cloud, no en el ticker | medicion | costos de inferencia y márgenes moviéndose sin repricing de la acción | `sobrevive`: emisor T1 (call Q1-2026 abc.xyz): costo de respuestas IA -30%, Cloud +63% a $20B, TPU 8i +80% perf/$; Gemini congela precios con margen 35,6% bajo presión (ts2, T?) |
| H2 Decisión de Google: ventaja cautiva, no producto | decision | no existe venta merchant de tarjetas, solo arriendo de capacidad | `sobrevive`: T2 (Tom's): "selling TPU access aggressively beyond its own services", acuerdo Anthropic de hasta 1M de TPUs en la historia de Google Cloud; Reuters vía Livemint (T?): mayoría reservada para uso interno; CNBC (T2): Nvidia/AMD sí venden a clouds que rentan por hora |
| H3 Cuello físico TSMC/CoWoS y Broadcom | tercero-comun | backlog y constraint declarado hacia 2026 | `sobrevive`: T2 (Tom's): packaging más restrictivo que los wafers, backlog de IA de $73B |
| H4 Moat de software CUDA/JAX | decision | hardware parejo pero adopción frenada por software | `sobrevive` pero débil (solo T?): JAX interno vs PyTorch externo, proyecto TorchTPU en curso, "the core bottleneck in externalization has been the software stack" |
| Calidad/confianza (pregunta sin hipótesis; objeción del diablo falta-hipotesis) | gemelo | brecha de calidad medible o desconfianza declarada | `no separada`: calidad sin brecha (contraparte: Ironwood +50,4% tokens/$ vs B200); confianza equivale a H4 |

## Evidencia

- **decisiva:** Tom's Hardware T2 (2026-05-21): "Google is now selling TPU access aggressively beyond its own services" + "Anthropic committed to up to one million TPUs in the largest deal in Google Cloud history" — https://www.tomshardware.com/tech-industry/semiconductors/custom-ai-asics-examined-from-broadcom-to-mtia
- Emisor T1, call Q1-2026 (abc.xyz): "we have reduced the cost of core AI responses by more than 30%" · "Cloud revenues accelerated ... up 63% to $20 billion" · "TPU 8i ... 80% better performance per dollar" — https://abc.xyz/investor/events/event-details/2026/2026-Q1-Earnings-Call-2026-nW8kCrBAKS/default.aspx
- CNBC T2 (2025-11-21): "AMD and Nvidia sell their GPUs to cloud providers ... Those companies then rent the GPUs to AI companies by the hour or minute" — https://www.cnbc.com/2025/11/21/nvidia-gpus-google-tpus-aws-trainium-comparing-the-top-ai-chips.html
- Reuters vía Livemint T? (2025-12-17): "had long reserved the majority share of its own chips, or TPUs, for in-house use only" · "has traditionally relied on a different framework, Jax, used extensively by its internal teams" — https://www.livemint.com/companies/news/google-works-to-erode-nvidias-software-advantage-with-metas-help-11765988302860.html (Reuters original bloquea descarga server-side: https://www.reuters.com/business/google-works-erode-nvidias-software-advantage-with-metas-help-2025-12-17/ — primaria no encontrada en texto)
- Ficha newsroom completa (15 fuentes verificadas, gates en verde, 9 objeciones del diablo abiertas): Notes/Research/newsroom/epica-EST-mediciones/HIP-12a/news/investigaciones/2026-10-19/tpu-alternativa-nvidia/resumen-check.md

## Conclusión

No es una sola causa. H2 ~1/2: decide si existe alternativa comprable — no la hay, Google vende acceso, no tarjetas. H4 ~1/4: decide si terceros pueden usarla — el software (JAX vs PyTorch) frena, TorchTPU en curso. H3 ~1/4: decide el ritmo — el packaging manda y el backlog es gigante. H1 es el marco de lectura: el efecto sí existe pero en costos y márgenes de Cloud, no en el ticker. Confianza: alta en H1–H3 (T1/T2), media-baja en H4 (solo T?). Lo que la cambiaría: un SKU merchant de TPU o un entrenamiento frontera externo confirmado sobre TPU refutaría H2.

## Predicciones

P-20261019-13, P-20261019-14

## Lo que aprendí del método

- El gate S-ESQ exige `dato`+`periodo` en cada fuente: los fragmentos cualitativos obligan a re-registrar todo (23 fuentes, quita+re-alta). Diseñar fragmentos con cifra desde el inicio ahorra una pasada completa.
- Reuters bloquea la descarga server-side: los cables se verifican vía espejos que los sindican (Livemint); diez espejos del mismo cable cuentan como uno (P1).
- El diablo tenía razón en "dato-no-distingue" sobre F4 (+1,7% del ticker): matiza H1 sin refutarla — un movimiento chico y puntual no es un repricing. Registrar el matiz en vez de pelearlo dejó la ficha más honesta.
- La pregunta mezclaba "por qué" con "qué va a pasar": separarlas (abduccion paso 1) mandó el futuro a predicciones.csv en vez de inflar la conclusión.
