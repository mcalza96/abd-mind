# Oráculo de la prueba A/B (EXP-017)

`mundo.b64` contiene los 11 casos R de EXP-016: sus hechos de la época y los hallazgos que entrega el oráculo cuando se pide mirar algo concreto. Está comprimido y en base64 para que no aparezca en búsquedas de texto. No contiene la resolución.

**Cómo se hicieron los hallazgos.** Los escribió un agente sin contexto a partir de la resolución:

- de 4 a 5 relevantes por caso;
- 2 irrelevantes por caso.

**Advertencia.** Algunos detalles de los hallazgos no vienen de los informes oficiales: el agente los inventó como observaciones plausibles. Algunos ejemplos:

- la pérdida de velocidad en el ADS-B (R01);
- los valores de resistencia (R09);
- la cavidad de fundición en el acople (R13);
- los 22 hallazgos irrelevantes.

**La verdad del mundo es por construcción:** coincide con la resolución en el mecanismo, no necesariamente en cada detalle.

**Uso:** `uv run abd-mind oraculo`. Variables de entorno:

- `ABD_ORACULO_AGENTE`: nombre del agente en el registro;
- `ABD_ORACULO_REGISTRO`: ruta del registro (por defecto, `~/.abd-mind/oraculo.jsonl`).
