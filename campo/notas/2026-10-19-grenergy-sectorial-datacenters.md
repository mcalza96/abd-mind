# 2026-10-19 · renovables España · puntual o sectorial + datacenters

- **Agente y skills usadas:** Hermes Agent; abduccion, red-abductiva, newsroom (ficha `grenergy-sectorial`, 2 frentes delegados en medium)
- **Pregunta:** ¿Lo de Grenergy es puntual o generalizado? ¿Sostiene el boom de datacenters la tesis?

## Hechos (fecha y fuente)
- Drawdown abr→oct 2026 (Yahoo, cierres): GRE.MC -48% (123→63,7), SLR.MC -35% (23,5→15,16), ANE.MC -6% (23,12→21,66). Subagente con diaria: GRE -42,7%, SLR -35,3%, ANE +3%. Dirección idéntica.
- Solaria 1S26 (Bolsamania 24-sep-2026, texto verificado): beneficio 124,9 M (+50%), "despegue de su negocio de centros de datos" — y cae igual que Grenergy con récord.
- Colocación acelerada 5,5% del presidente y directivos con descuento 8,8% (96,24 M€, CNMV vía Estrategias de Inversión/Yahoo 18-jun-2025, texto verificado): precedente de dilución para dar liquidez/free float.
- Excepción ibérica (Bolsamania 23-sep-2026, texto verificado): GRE -13,5%, SLR -5,86%, ANE -1,67% el mismo día; Sabadell: impacto limitado por PPAs.
- Datacenters España (pistas Google News RSS, URLs pendientes de apertura): 22 GW en solicitudes; norma en borrador 80% renovable nueva; 12 GW baterías en desarrollo, objetivo 22,5 GW a 2030; Grenergy primera financiación BESS stand-alone 100 M; Cinco Días 23-ago-2026 "entre el bum y el riesgo de burbuja"; Texas pausa 474 GW en auditoría; CNMC pide flexibilizar exigencias del decreto; Aragón con red saturada.

## Lo sorprendente
Solaria gana +50% y presume datacenters y se hunde igual; Acciona Energía, del mismo sector y país, apenas cae. Hay ola, pero no moja a todos por igual.

## Hipótesis
| Hipótesis | Familia | Qué predecía distinto | Resultado |
|---|---|---|---|
| H1 Ola sectorial (canibalización, PPA ~30 €, precios volátiles) | tercero común | caen todas las renovables con el mismo timing | APOYA parcial: SLR -35% con +50% beneficio; "precios volátiles" tumba a Solaria tras ganar +52% (El Periódico Energía) |
| H2 Puntual Grenergy (capex 3.700 M, deuda 4,6x, colocaciones) | decisión | Grenergy peor que comparables todo el periodo | APOYA: -48% vs -35% vs -6%; colocación 5,5% con -8,8% (2025) + pista ampliación 150 M (2026, sin verificar) |
| H3 Regulatorio español (excepción ibérica) | decisión (Gobierno) | corte sectorial el 23-sep | APOYA como gatillo agudo; matiz Sabadell (PPAs cubren) |
| H4 Boom datacenter sostiene la tesis (22 GW, 80% renovable, BESS) | tercero común | PPAs tech y financiación BESS creciendo | PISTA a favor: 22 GW solicitudes, financiación 100 M BESS Grenergy; pendiente abrir URLs |
| H5 El boom no paga precio (PPA tech a la baja) | gemelo/volumen-vs-margen | precios PPA cayendo pese a más capacidad | PISTA: titular "PPA para centros de datos en Europa caen"; sin cifra, falta BQ |
| H6 La red no da (cuello de botella) | umbral/infraestructura | proyectos frenados por conexión, no por demanda | PISTA: Aragón satura red, EL PAÍS red/vivienda mar-2026; falta cifra de GW rechazados |
| H7 Sobreventa y rebote técnico | medición | rebotes desacoplados tras pánico | PISTA: "mayor sobreventa de su historia" (GRE), Solaria +3,75% rebote; sin RSI verificado, falta BQ |

## Conclusión
Mixto, confianza media (0,55): H1 pone el suelo (todas caen con buenos resultados), H2 pone la diferencia (Grenergy cae ~13 pp más que Solaria y ~42 pp más que ANE: capex+deuda+dilución pesan). H4 dice que la tesis datacenter sigue viva en volumen; H5+H6 advierten que volumen no es precio ni conexión. La cambiaría: si ANE y SLR recuperan y GRE no (H2 dominante) o si los PPA tech confirman caída de precios (H5 muerde la tesis).

## Predicciones
P-20261019-02 en `campo/predicciones.csv`.

## Lo que aprendí del método
- El par comparado (ANE casi plana) separó más que cualquier titular: sin ANE, H1 parecía explicar todo.
- La colocación de 2025 apareció buscando 2026: el historial de dilución es parte del relato aunque el evento sea viejo. Fechar cada pieza evitó colgarle a 2026 lo de 2025.
- Los links CBM de Google News no resuelven con curl (requieren JS): la vía es `busca` GNSS del pipeline, que sí entrega URL final. Registrar ese orden (RSS para detectar, GNSS para fijar).
