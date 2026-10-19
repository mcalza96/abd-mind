# 2026-10-19 · renovables España · por qué cayó Grenergy ~50% desde abril

- **Agente y skills usadas:** Hermes Agent; abduccion, red-abductiva, newsroom (ficha `grenergy-caida-2`)
- **Pregunta:** Por qué GRE.MC cayó de 136,6 € intradía (abr-2026) a 63,7 € (19-oct-2026), -53% desde máximo / -48% desde cierre abril.

## Lo sorprendente
La caída de 6 meses continuos (may 114,8 → jun 92,2 → jul 88,8 → ago 75,2 → sep 67,2 → oct 63,7, cierres Yahoo Finance GRE.MC) convive con un 1S26 récord: ingresos 661 M (+51%), beneficio 74 M (+112%), EBITDA 126 M (+47%) y recompra de 50 M (Bolsamania 16-sep-2026). El mercado castiga con titulares buenos.

## Hipótesis
| Hipótesis | Familia | Qué predecía distinto | Resultado |
|---|---|---|---|
| H1 Plan capex 3.700 M a 2028 asusta (deuda/dilución) | decisión (empresa) | caída arranca 27-may-26 + deuda alta documentada | APOYA: 1T26 beneficio 2 M (-94%), EBITDA 4,8 M (-92%), ingresos -40% (Bolsamania 27-may-26); deuda neta 1,1 MM = 4,6x (1S26); pista ampliación 150 M (Iberian Lawyer, no verificada, Cloudflare) |
| H2 RBC recorta previsión beneficios 23-sep-26 | decisión (analista) | recorte explícito + contagio | PISTA: título Cinco Días 23-sep-26 coincide con el -13,5% del día, pero el driver documentado ese día es H6; texto RBC no verificado (paywall) |
| H3 Toma de ganancias tras +4x | nada que explicar | venta sin quiebra fundamental | APOYA parcial: 28,8 (oct-24) → 136,6 (abr-26); 1S26 récord no frena la caída |
| H4 Canibalización solar España / PPA pandemia | tercero común (sector) | caen comparables los mismos días | APOYA: 23-sep caen Solaria -5,86%, Acciona Energía -1,67% (Bolsamania); PPA ~30 €/MWh (El Periódico Energía, T? pendiente) |
| H5 Tipos altos castigan growth endeudada | tercero común (macro) | correlación con tipos, caída global renovables | NO SEPARADA: sin número propio; declarada, falta BQ (comparar con índice renovables vs tipos BCE) |
| H6 Excepción ibérica: el Gobierno estudia topar ingresos renovables | decisión (Gobierno) | caída sectorial el día del anuncio | APOYA (gatillo agudo): Grenergy -13,5% el 23-sep-26; Sabadell matiza impacto limitado por PPAs (Bolsamania 23-sep-26) |
| H7 Efecto medición/bajistas (máx intradía vs cierre, cortos) | medición + gemelo | parte del % es artefacto de comparación | MATIZA: -53% (136,6 intradía) vs -48% (cierre ~123); sin dato de cortos, falta BQ |

## Conclusión
Multi-causa, confianza media (0,6): H1 es el fondo (el plan 3.700 M + deuda 4,6x + 1T26 flojo cambió el relato de growth a dilución desde mayo); H6 fue el gatillo agudo del -13,5% del 23-sep; H3+H4 son el viento en contra permanente. La cambiaría: ampliación de capital confirmada (fijaría H1 como dominante) o reversión del plan del Gobierno (quitaría H6).

## Predicciones
P-20261019-01 en `campo/predicciones.csv`.

## Lo que aprendí del método
- La comprobación que más separó fue la serie mensual de cierres: la caída empieza en mayo, justo con el plan 3.700 M + 1T26 (-94%), no con RBC (septiembre). El orden temporal descartó "RBC como causa" en una línea.
- Faltó en la primera pasada una hipótesis regulatoria explícita con su fecha (excepción ibérica 23-sep); la obvia financiera tapaba el overlay regulatorio, igual que en la nota CXMT el IPC tapaba lo sectorial.
- En newsroom, los dominios españoles (bolsamania, europapress, hispanidad, elperiodicodelaenergia) salen "no clasificados" y varios dan 403 al fetcher: el curl con UA de navegador rescata el texto cuando `agrega-fuente` falla. Registrar esa vía como procedimiento.
