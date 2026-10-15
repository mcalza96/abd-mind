# abd-bench · 05 — Percepción/cognición (E01–E08) + rechazados + índice maestro

## E01 — El vestido (azul-negro vs blanco-dorado)
- Observadores: O1 ve azul-negro; O2 ve blanco-dorado. Misma foto, informes incompatibles.
- Latente: reflectancia real del vestido + iluminante asumido (priors de iluminación distintos, ratios de conos).
- Wrong: "uno de los dos miente / monitores distintos".
- Ground truth: vestido azul-negro; la discrepancia la explica el descuento del iluminante.
- Fuentes: https://en.wikipedia.org/wiki/The_dress

## E02 — Efecto McGurk (audio vs visión)
- Observadores: O-audio oye /ba/; O-visual (labios /ga/) percibe /da/. Mismo estímulo, sílaba distinta.
- Latente: fonema emitido + integración audiovisual (el percepto fusiona ambas vías).
- Wrong: "el audio cambió".
- Ground truth: señal acústica /ba/ con visual /ga/; el percepto /da/ es fusión, no alucinación.
- Fuentes: https://en.wikipedia.org/wiki/McGurk_effect

## E03 — Ilusión de la mano de goma
- Observadores: O-propioceptivo siente su mano en su lugar; O-visual-táctil siente la goma como propia. Ubicación del "yo" incompatible.
- Latente: propiedad corporal inferida por integración visuo-táctil sincrónica (modelo corporal bayesiano).
- Wrong: "la mano real se movió".
- Ground truth: la mano real no se mueve; la sincronía induce propiedad sobre el objeto externo.
- Fuentes: https://en.wikipedia.org/wiki/Rubber_hand_illusion

## E04 — Gorila invisible (ceguera por inatención)
- Observadores: O-tarea (cuenta pases) no ve el gorila; O-libre sí lo ve. Reportes incompatibles del mismo video.
- Latente: foco atencional impuesto por la tarea (marco de tarea filtra el resto).
- Wrong: "el video era distinto / O-tarea no miraba".
- Ground truth: mismo video; la carga atencional suprime el estímulo inesperado.
- Fuentes: https://en.wikipedia.org/wiki/Inattentional_blindness

## E05 — Relleno del punto ciego
- Observadores: O-fóvea reporta campo continuo; O-medida (mapeo monocular) detecta escotoma donde no hay fotorreceptores. Continuidad vs hueco.
- Latente: disco óptico sin fotorreceptores + relleno cortical predictivo.
- Wrong: "toda la retina ve".
- Ground truth: hay zona ciega real; la experiencia continua es construcción del sistema visual.
- Fuentes: https://en.wikipedia.org/wiki/Blind_spot_(vision)

## E06 — Miembro fantasma
- Observadores: O-paciente siente mano amputada (dolor/posición); O-externo constata ausencia. Presencia vs ausencia.
- Latente: representación cortical persistente del miembro + reorganización somatosensorial.
- Wrong: "el paciente finge / es solo memoria".
- Ground truth: no hay miembro; el mapa cortical sigue generando sensaciones localizadas.
- Fuentes: https://en.wikipedia.org/wiki/Phantom_limb

## E07 — Murciélago (ecolocación) vs visión humana en caverna oscura
- Observadores: humano ve "espacio vacío intransitable"; murciélago navega y caza con precisión. Mapas del mismo espacio incompatibles.
- Latente: geometría de la caverna + presas, accesible por sonar y no por visión sin luz.
- Wrong: "el murciélago ve en la oscuridad con los ojos".
- Ground truth: ecolocación ultrasónica con delays de eco; el humano carece del sensor, no del mundo.
- Fuentes: https://en.wikipedia.org/wiki/Animal_echolocation

## E08 — Víbora de foseta (IR) vs visión humana de noche
- Observadores: humano ve "nada" en oscuridad total; la víbora localiza una presa de sangre caliente. Detección vs nada.
- Latente: presa caliente presente + canal infrarrojo del órgano de foseta (imagen térmica).
- Wrong: "la serpiente huele/oye a la presa".
- Ground truth: órgano de foseta mapea radiación IR; observadores difieren por sensor, no por escena.
- Fuentes: https://en.wikipedia.org/wiki/Infrared_sensing_in_snakes

## Rechazados (≥12, con criterio que falla)
Criterios (1–5): (1) dos+ observadores genuinamente incompatibles · (2) latente único resolvente · (3) respuesta ingenua/wrong definible · (4) ground truth verificable · (5) no-trivial / no deducible sin abducción.
1. Ilusión Müller-Lyer — falla (5): truco geométrico conocido, sin latente oculto.
2. Vestido ya usado como E01, duplicado "tierra plana vs fotos" — falla (2): sin latente común, es negación.
3. Déjà vu — falla (4): sin ground truth verificable.
4. Sueños premonitorios — falla (4): sin verificación controlada.
5. Horóscopo capaz de todo — falla (3): sin wrong_answer falsable.
6. Placebo sin grupo control — falla (4): ground truth no aislable.
7. "Fantasma en foto" (pareidolia) — falla (2): ruido, no latente único.
8. Testigos ovni contradictorios sin radar — falla (4): sin ground truth.
9. Sabor de vino caro vs barato (expectativa) — falla (1): observadores no incompatibles sobre el mismo estímulo ciego.
10. Daltónicos discuten color sin anomaloscopio — falla (4): se resuelve por medición directa, no abducción.
11. Eco confundido con voz — falla (2): latente trivialmente observable.
12. Reflejo en espejo "doble" — falla (5): óptica directa, deducción simple.
13. Sonambulismo (reporte vs acto) — falla (2): estados temporales distintos, no mismo evento.
14. IA "alucina" cita — falla (1): un solo observador, sin marcos en conflicto.

## Índice maestro A–E (IDs/títulos)
- 01 (A, física): A01–A08 — archivo del slice A (no este).
- 02 (B): B01–B08 — archivo del slice B.
- 03 (C): C01–C08 — archivo del slice C.
- 04 (D): D01–D08 — archivo del slice D.
- 05 (E, percepción/cognición, este archivo):
  - E01 El vestido · E02 Efecto McGurk · E03 Mano de goma · E04 Gorila invisible
  - E05 Punto ciego · E06 Miembro fantasma · E07 Ecolocación murciélago · E08 Víbora IR
- Total: 40 casos (32 A–D + 8 E).

## Stats por categoría
- E humana-visual: E01, E05 (2) · E multisensorial: E02, E03 (2) · E atencional/corporal: E04, E06 (2) · E animal-sensor: E07, E08 (2).

## Riesgo de contaminación (famoso vs oscuro)
- Alto (muy famosos, probable memorización): E01, E02, E04.
- Medio (conocidos en neurociencia): E03, E05, E06.
- Bajo (más oscuros / comparativos): E07, E08.
- Nota: E01/E02/E04 medirán más memoria que abducción; E07/E08 son los más limpios.
