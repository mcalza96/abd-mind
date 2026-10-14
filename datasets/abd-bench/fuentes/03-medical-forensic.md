# abd-bench — Serie C: medicina / forense / accidentes (C01–C08)

Fase 1 (recolección escueta, sin análisis). Tesis del bench: y_i = proyección de S vía marco del observador. Cada caso registra observadores/marcos, conflicto, H latente por observador, respuesta inductiva errónea, verdad de base + URLs reales, flags derrotables/ontológicos.

Formato por caso: OBS (observadores y marcos) · CONFLICTO · H-LATENTE (mapeo por observador) · RESPUESTA INDUCTIVA ERRÓNEA · VERDAD + FUENTES · FLAGS [derrotable? / ontológico?].

---

## C01 — Muertes por Tylenol adulterado, Chicago 1982

- OBS:
  - O1 clínicos/urgencias: marco = intoxicación endógena (infarto, ACV). y = "muertes cardíacas dispersas".
  - O2 enfermera salud pública (Helen Jensen) + médico forense (Donoghue) + toxicólogo (Schaffer): marco = exposición exógena común. y = "olor a almendra + cápsulas con cianuro".
  - O3 fabricante (J&J/McNeil): marco = control de fábrica. y = "lotes de PA y TX, todo normal en planta".
- CONFLICTO: O1 ve muertes inconexas; O3 ve proceso fabril limpio; O2 ve un vehículo común post-fábrica (botella compartida por los Janus, 6 píldoras faltantes).
- H-LATENTE (mapeo por observador): H = adulteración post-fábrica con cianuro potásico en cápsulas en góndolas. O1 no la ve (sin marco toxicológico); O3 no la ve (su marco termina en puerta de fábrica); O2 la revela (rastreo botella→tienda→cápsula).
- RESPUESTA INDUCTIVA ERRÓNEA: "falla de manufactura de J&J / sobredosis de acetaminofén" → retirar control de calidad en planta.
- VERDAD + FUENTES: 7 muertos; cápsulas Extra-Strength con ~3× dosis letal de cianuro; lotes de dos plantas distintas → manipulación en tiendas (Jewel Foods, Osco, Walgreens, Dominick's, Frank's); recall nacional de ~31M botellas 05-oct-1982; autor nunca condenado; Lewis condenado solo por extorsión.
  - https://en.wikipedia.org/wiki/Chicago_Tylenol_murders
  - https://pbs.org/newshour/updates/tylenol-murders-1982
  - https://publichealth.uic.edu/news-stories/people-politics-and-poison-the-tylenol-murders-revisited-forty-years-later/
- FLAGS: derrotable = sí (conclusión "fábrica culpable" cae ante dato dos-plantas + multi-tienda) / ontológico = no (H es acción humana, no entidad nueva de la naturaleza; sí crea clase regulatoria: envase inviolable).

## C02 — Accidentes Therac-25, 1985–1987 (EE.UU./Canadá)

- OBS:
  - O1 operadoras/técnicos: marco = "máquina indica dosis baja / error de tipeo; antes bastaba reingresar". y = "malfunción transitoria / paciente exagera (quemadura eléctrica?)".
  - O2 físicos hospitalarios: marco = calibración dosimétrica puntual. y = "calibración OK, sin falla eléctrica" (firma independiente no halló problema de tierra).
  - O3 fabricante (AECL): marco = "software no puede fallar de ese modo; hardware heredado basta". y = "mejora menor (microswitch)".
- CONFLICTO: 6 sobredosis masivas (hasta ~16.500–25.000 rad en <1 s en ~1 cm) con quemaduras y muertes; cada marco local explica su ventana y niega la de los otros; la máquina se repone en servicio (caso ETCC, abril 1986) tras chequeo local.
- H-LATENTE (mapeo): H = condiciones de carrera en software + ausencia de interlocks de hardware (heredados del Therac-20 sin replicar). O1 la enmascara (interfaz opaca, mensajes crípticos "Malfunction 54"); O2 la enmascara (dosímetro mide régimen normal, no el transitorio de alta tasa); O3 la niega (reutilización de software sin análisis de seguridad).
- RESPUESTA INDUCTIVA ERRÓNEA: "error de operador / falla de puesta a tierra / microswitch aislado" → reentrenar operadoras, ajustar microswitch.
- VERDAD + FUENTES: 11 unidades instaladas (5 EE.UU., 6 Canadá); 6 accidentes con sobredosis conocidos jun-1985–ene-1987; causa raíz en software + diseño sin salvaguardas; recall final con rediseño y salvaguardas de hardware. Investigación Leveson & Turner.
  - http://users.csc.calpoly.edu/~csturner/courses/508/Therac-25.pdf
  - https://escholarship.org/content/qt5dr206s3/qt5dr206s3.pdf
  - https://postmortem.io/incidents/therac-25--1993-07-01--an-investigation-of-the-therac-25-accidents
- FLAGS: derrotable = sí (cada hipótesis local cae ante reproducción del accidente y auditoría de código) / ontológico = parcial (nueva clase: accidente de software en sistema crítico; no nueva entidad física).

## C03 — Challenger STS-51-L, O-rings, 28-ene-1986

- OBS:
  - O1 ingenieros Morton Thiokol: marco = datos de erosión/blow-by vs temperatura. y = "no lanzar bajo 53 °F (mínimo previo STS-51-C)".
  - O2 gerencia Thiokol + NASA (nivel III FRR): marco = "probar que NO es seguro para detener un programa con presión de calendario". y = "datos no concluyentes → luz verde".
  - O3 comisión Rogers / Feynman: marco = física del elastómero + gestión. y = "pérdida de resiliencia en frío + falla de comunicación".
- CONFLICTO: noche previa, ingenieros recomiendan no lanzar a 28–29 °F; caucus gerencial de 30 min revierte la recomendación; la objeción no sube más allá del FRR nivel III.
- H-LATENTE (mapeo): H = junta tórica del segmento aft del SRB derecho pierde sellado en frío → blow-by → llama → falla del tanque externo a los 73 s. O1 la proyecta como riesgo térmico; O2 la proyecta como "riesgo aceptable / falta de prueba"; O3 la fija como causa física + causa raíz organizacional ("accidente enraizado en la historia", falla conocida desde 1977).
- RESPUESTA INDUCTIVA ERRÓNEA: "anomalía de erosión dentro de familia de vuelo / clima como factor menor" → seguir volando.
- VERDAD + FUENTES: causa inmediata = falla de O-rings del aft field joint del SRB derecho agravada por baja temperatura; causa contribuyente = no-respuesta a flaw conocido desde 1977 + proceso de decisión seriamente defectuoso; 9 recomendaciones; exigencia de reporte a Reagan en 30 días.
  - https://en.wikipedia.org/wiki/Rogers%20Commission%20Report
  - https://www.nasa.gov/history/rogersrep/genindex.htm
- FLAGS: derrotable = sí (tesis gerencial "seguro hasta prueba en contra" derrotada por física + historial) / ontológico = no (misma física, distinto umbral de evidencia por marco).

## C04 — Air France 447, A330, 1-jun-2009 (Río→París)

- OBS:
  - O1 sondas Pitot (×3): marco = presión total. y = velocidades inconsistentes entre sí (obstrucción por cristales de hielo).
  - O2 EFCS/piloto automático: marco = coherencia de datos. y = "datos no fiables → desconexión AP/AT, ley alterna ALT2, menos protecciones".
  - O3 tripulación (PF + relevo, capitán descansando): marco = "stall warning espurio / overspeed por buffet". y = "pull-up sostenido en vez de push-down".
- CONFLICTO: tres observadores de velocidad discrepan; la automatización degrada el marco de protección; la tripulación no ejecuta el procedimiento de "pérdida de velocidad indicada" y confunde buffet con overspeed.
- H-LATENTE (mapeo): H = obstrucción de Pitots por cristales de hielo (sin acreción visible externa: los cristales rebotan fuera pero se ingieren por la toma) + stall sostenido no reconocido hasta el mar. O1 la ve como ruido; O2 la ve como condición de degradación; O3 no la ve (display no indica "Pitot bloqueado", solo consecuencias).
- RESPUESTA INDUCTIVA ERRÓNEA: "falla de motores / turbulencia severa / overspeed" → tirar del stick y mantener actitud nose-up (16,2° al final, caída ~10.913 fpm, 107 kt groundspeed).
- VERDAD + FUENTES: 228 muertos; caída desde FL350 en ~4,5 min; secuencia BEA: inconsistencia transitoria → desconexión AP → inputs inapropiados → no aplicar procedimiento → no reconocer stall; restos a 3.900 m (hallados 2-abr-2011); informe final BEA jul-2012 (~300 pp.).
  - https://flightsafety.org/asw-article/sustained-stall
  - https://ainonline.com/aviation-news/2012-07-09/french-release-final-report-air-france-447
  - http://www.bea.aero/docspa/2009/f-cp090601.en/pdf/f-cp090601.en.pdf
- FLAGS: derrotable = sí (lectura "overspeed" derrotada por FDR + ACARS + CVR) / ontológico = parcial (nueva entidad operativa: icing por cristales de hielo, mal comprendido entonces).

## C05 — Cólera de Broad Street, Soho 1854

- OBS:
  - O1 marco miasma (Board of Health, Farr): marco = aire/olor/suelo del Támesis. y = "vapores que infectan por aire; limpiar y ventilar".
  - O2 John Snow (+ Rev. Whitehead, puerta a puerta): marco = agua/contagio fecal-oral. y = "muertes clusterizadas en usuarios de la bomba de Broad St".
  - O3 química/microscopía del agua de la bomba: marco = impureza visible. y = "agua aparentemente limpia" (falso negativo instrumental).
- CONFLICTO: 616 muertos (127 en 3 días desde 31-ago; >500 al 10-sep); Snow pide quitar la manivela el 7-sep; la Junta lo hace pero atribuye la epidemia al miasma ("rivalry of foulness" aire vs agua).
- H-LATENTE (mapeo): H = Vibrio cholerae en agua por filtración de pozo negro (lavado de ropa de la bebé Lewis) al pozo de la bomba. O1 la invisibiliza (marco aéreo); O2 la infiere por mapa + excepciones (mujer de Hampstead que pedía agua de Broad St; cervecería y workhouse con agua propia = cero muertes); O3 la falla (instrumento sin resolución para el agente).
- RESPUESTA INDUCTIVA ERRÓNEA: "miasma del aire londinense" → saneamiento de olores, no de agua.
- VERDAD + FUENTES: transmisión hídrica fecal-oral (ensayo 1849 + 2ª ed. 1855); remoción de la manivela como símbolo; Vibrio aislado en 1854 pero aceptado décadas después (Pasteur 1861).
  - https://en.wikipedia.org/wiki/Broad_Street_Pump
  - https://www.gavi.org/vaccineswork/john-snow-and-pump-handle-public-health
  - https://pmc.ncbi.nlm.nih.gov/articles/PMC7150208/
- FLAGS: derrotable = sí (miasma derrotado por cluster + contraejemplos) / ontológico = sí (nueva clase causal: patógeno hídrico; germen como entidad).

## C06 — Fiebre puerperal, Viena 1846–1848 (Semmelweis)

- OBS:
  - O1 clínica 1ª (estudiantes/médicos, autopsias→partos): marco = miasma/constitución/"fiebre de leche". y = mortalidad ~98,4/1.000 (12–18%).
  - O2 clínica 2ª (parteras, sin autopsias): marco = mismo aire, distinta práctica. y = mortalidad ~36,2/1.000.
  - O3 Semmelweis: marco = materia cadavérica en manos. y = "partículas" transferidas; lavado con cal clorada → caída a ~2,4% (1848 ~1,27%).
- CONFLICTO: mismo hospital, mismo aire, mortalidades divergentes; la muerte de Kolletschka (corte en autopsia → sepsis como fiebre puerperal) rompe el marco miasmático; la élite rechaza la hipótesis por implicar culpa médica.
- H-LATENTE (mapeo): H = infección cruzada por materia orgánica en manos/instrumentos (hoy: estreptococo puerperal y otros). O1 la niega (marco moral/atmosférico); O2 la evita sin teorizarla (práctica sin autopsias); O3 la operacionaliza (cloro hasta quitar olor cadavérico) sin conocer el agente.
- RESPUESTA INDUCTIVA ERRÓNEA: "miasma / hacinamiento / constitución de la paciente" → sangrías, ventilación, no higiene.
- VERDAD + FUENTES: lavado con cal clorada desploma la mortalidad en un mes (12,14%→2,38%); extensión a instrumentos 1848; publicación 1861 rechazada por estilo y resistencia corporativa; vindicación con Pasteur/Lister y bacteriología.
  - https://www.ebsco.com/research-starters/history/semmelweis-develops-antiseptic-procedures
  - https://pmc.ncbi.nlm.nih.gov/articles/PMC7240806
  - https://ncbi.nlm.nih.gov/pmc/articles/PMC11568873
- FLAGS: derrotable = sí (miasma derrotado por experimento natural 1ª vs 2ª + intervención) / ontológico = sí (clase nueva: contagio por contacto; agente aún innominado: "partículas cadavéricas").

## C07 — Talidomida y focomelia, 1957–1961

- OBS:
  - O1 fabricante (Grünenthal/CIBA/Distillers): marco = "DL50 no alcanzable en roedores = atóxico; náusea del embarazo alivia". y = "sedante seguro, sin receta en muchos países".
  - O2 pediatras/genetistas de campo (Lenz Hamburgo, McBride Australia): marco = conteo de malformaciones raras. y = "pico de focomelia/amelia + atresias ligado a ingesta días 34–49 post-FUM".
  - O3 FDA (Frances Kelsey): marco = "sin datos de seguridad no hay aprobación". y = "rechazo 1960 (neuropatía periférica como señal)".
- CONFLICTO: ~10.000–20.000 afectados en el mundo; el fabricante contesta los hallazgos; EE.UU. casi indemne por el dique regulatorio; ventana teratogénica estrecha (una sola dosis basta) invisible al marco "dosis-respuesta lineal del adulto".
- H-LATENTE (mapeo): H = teratogenicidad ventana-dependiente (días ~35–49). O1 no la ve (sin test en gestantes/animales preñados, modelo roedor); O2 la ve (cluster temporal-geográfico madre→hijo); O3 la previene sin verla (carga de la prueba invertida).
- RESPUESTA INDUCTIVA ERRÓNEA: "aumento genético/de novo de malformaciones" o "seguro porque no mata ratas" → seguir prescribiendo a embarazadas.
- VERDAD + FUENTES: Lenz (nov-1961, 50+ casos) + McBride (dic-1961) → retiro fin-1961; ~40% de afectados muere el primer año; Kelsey recibe premio presidencial 1962; enmienda Kefauver-Harris 1962 (eficacia + test en animales preñados).
  - https://ncbi.nlm.nih.gov/pmc/articles/PMC3573415
  - https://mayoclinicproceedings.org/article/S0025-6196(11)62157-5/fulltext
  - https://drugfyi.com/timeline/thalidomide-tragedy-1960
- FLAGS: derrotable = sí (tesis "atóxico" derrotada por epidemiología) / ontológico = sí (nueva clase regulatoria/científica: teratógeno ventana-dependiente; fármaco→malformación como entidad causal).

## C08 — Legionelosis, Filadelfia 1976 (convención Legión Americana)

- OBS:
  - O1 clínicos: marco = neumonía bacteriana típica. y = "fiebre + infiltrados; antibióticos habituales no responden".
  - O2 epidemiólogos/CDC: marco = ¿portador? ¿tóxico externo? y = "cluster post-convención (221 casos, 34 muertos) ligado al hotel, no a persona".
  - O3 laboratorio: marco = cultivo estándar. y = "solo contaminantes" durante meses (falso negativo instrumental).
- CONFLICTO: ~4.400 asistentes en el Bellevue-Stratford; casos también en no-huéspedes ("Broad Street pneumonia", exposición en la acera); pánico a gripe porcina/bioterror; el agente no crece en medios usuales.
- H-LATENTE (mapeo): H = Legionella pneumophila en torre de enfriamiento del aire acondicionado, aerosolizada. O1 la trata como neumonía común; O2 la localiza (hotel como fuente ambiental); O3 la aísla recién ene-1977 con técnicas rickettsiales desde tejido pulmonar (cepas Philadelphia-1 a -4), reclasificando los "contaminantes".
- RESPUESTA INDUCTIVA ERRÓNEA: "nuevo virus gripal / intoxicación / portador humano" → buscar persona cero, tratar con penicilina.
- VERDAD + FUENTES: anuncio CDC 18-ene-1977; Philadelphia-1 como cepa tipo sg1 (secuenciada entre las primeras); fuente = torre de enfriamiento; nuevas normas de climatización; reexamen genómico confirma linaje común con diversidad (episoma + loci transferidos).
  - https://en.wikipedia.org/wiki/1976_philadelphia_legionnaires'_disease_outbreak
  - https://pmc.ncbi.nlm.nih.gov/articles/PMC5042515
  - https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0164074
- FLAGS: derrotable = sí (hipótesis persona-portador derrotada por casos sin ingreso al hotel + aislamiento) / ontológico = sí (género/especie nuevos: Legionella; fuente ambiental antes "inocua").

---

## Nota de bench (Fase 2, fondo mínimo)

Patrón C: el desacuerdo no es ruido sino proyección diferencial de una H común sobre marcos con distinta resolución (instrumento, ventana temporal, carga de la prueba). El error inductivo típico: generalizar dentro del propio marco ("más calibración", "más limpieza del aire", "más control fabril") en vez de cambiar de marco. Flags: C01/C03 no-ontológicos (acción humana + gestión); C02 parcial; C04 parcial; C05–C08 ontológicos (nuevo agente/clase causal). Todos derrotables: cada verdad de base revierte la conclusión inductiva al agregar el observador faltante.
