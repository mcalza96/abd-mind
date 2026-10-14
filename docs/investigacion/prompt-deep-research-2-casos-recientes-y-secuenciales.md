# Prompt de investigación 2 — casos recientes, secuenciales y abiertos

Segundo encargo de investigación. Aplica las lecciones de la bitácora:

- **Contaminación:** casos famosos que los modelos ya conocen (EXP-007).
- **Etiquetas ambiguas** (EXP-010).
- **Observaciones escritas sabiendo la respuesta** (abd-bench, saneamiento).
- **Salida fuera de formato** (EXP-006).

Se pega tal cual, en inglés.

---

```text
ROLE
You are a research assistant building a benchmark for an abductive-reasoning engine. The engine
receives reports from several observers whose reports seem to contradict each other and must
infer the hidden cause. Your job is to COLLECT DOCUMENTED REAL CASES, not to analyze them.

WHAT TO COLLECT — four sets, 15 cases each (60 total)

Set R — Recent resolved cases (most important).
Real incidents whose RESOLUTION was published on or after 2026-05-01. They must not appear in
model training data. If you cannot find 15, complete the set with cases resolved between
2025-07-01 and 2026-04-30 and mark them with "antes_de_mayo_2026": true. Domains: infrastructure/IT outages with public post-mortems, aviation and
rail incident reports (NTSB, BEA, AAIB, TSB), product recalls, outbreak investigations, data or
measurement errors in published science (corrections, retractions), industrial accidents.
Requirement: before resolution, at least two sources reported things that seemed incompatible.

Set S — Sequential cases.
Real cases with a dated TIMELINE of evidence, where early evidence pointed to a wrong explanation
and later evidence reversed it. Examples: an outage status page that blamed X and a post-mortem
that found Y; a preliminary accident report vs the final report. Any date is fine, but prefer
obscure cases.

Set U — Open cases.
Real cases that are STILL UNRESOLVED as of today, where at least two explanations remain
seriously proposed by credible sources and the public evidence does not decide between them.
These test whether the engine abstains. For each, name the evidence that would decide it.

Set F — Equity drawdowns with known outcome.
Listed companies whose share price fell 30% or more within 3 months between 2016 and 2023.
For each: what was publicly known within 30 days of the low (earnings, guidance, sector moves,
insider trades, short interest, news), AND what happened in the following 12–24 months (recovered
or not, and the documented reason). Mix of structural declines and rebounds, about half each.
Avoid household-name crises (e.g. famous bankruptcies) — prefer mid-caps.

STRICT RULES
1. No hindsight in observations. Each observation must be something an observer reported AT THE
   TIME, in their own words or close paraphrase, with its date. Never write the resolution, or
   words that point to it, inside an observation. Keep the resolution in a separate field.
2. One fact per observation. 4–8 observations per case, from at least 2 different observers.
3. Every observation and every resolution needs a source URL and a date. Prefer primary sources
   (official reports, post-mortems, filings, papers). If you cannot find a source, drop the fact.
4. Describe the resolution as a MECHANISM in plain words ("a firmware update changed the unit of
   the sensor feed"), not as a category label. Do not classify cases into types.
5. The resolution is itself a report: say who established it, when, and whether anyone disputes
   it. If it was later revised, include every version with its date.
6. For set S, give observations in chronological order with dates, and mark which ones were
   available at each stage.
7. Exclude any case you judge to be widely known (would appear in textbooks, Wikipedia
   "notable" lists, or major news worldwide). If in doubt, include it but flag "maybe_famous".
8. Do not invent. If a field is unknown, write null.

OUTPUT FORMAT — exactly one file, JSON Lines (one JSON object per line), nothing else.
Keys (Spanish, as below):
{
  "id": "R01",                       // R01–R15, S01–S15, U01–U15, F01–F15
  "conjunto": "R|S|U|F",
  "titulo": "short neutral title that does not reveal the cause",
  "dominio": "...",
  "observadores": [{"id": "O1", "nombre": "...", "marco": "method/instrument/position, no hint of the cause"}],
  "observaciones": [{"observador": "O1", "contenido": "...", "fecha": "YYYY-MM-DD", "fuente": "URL"}],
  "resolucion": {
    "mecanismo": "plain-language mechanism, or null for set U",
    "establecida_por": "who", "fecha": "YYYY-MM-DD", "fuente": "URL",
    "disputada": true|false, "versiones_previas": [{"mecanismo": "...", "fecha": "...", "fuente": "..."}]
  },
  "explicaciones_rivales": ["for set U: each seriously proposed explanation; otherwise optional"],
  "evidencia_que_decidiria": "set U only",
  "resultado_12_24_meses": "set F only: what happened, with source",
  "quizas_famoso": true|false,
  "antes_de_mayo_2026": true|false,   // set R only
  "notas": "anything the builder should know"
}

Before finishing, check: 60 lines; every observation has fecha and fuente; no observation
contains the resolution; set R resolutions are dated 2026-05-01 or later (or marked
"antes_de_mayo_2026").
```

---

## Uso previsto

| Conjunto | Experimento | Qué mide |
|---|---|---|
| R | Precisión sin contaminación (resueltos desde mayo de 2026; los marcados como anteriores se analizan aparte) | ¿Motor y línea base razonan igual de bien cuando el caso no está en el entrenamiento? |
| S | Revisión secuencial (`nueva_evidencia`, derrota) | ¿Se ancla al primer dato o revisa? |
| U | Abstención con casos reales | Complementa la serie U sintética de EXP-012 |
| F | Dominio `mercado` y predicciones (10 §B4, B11) | La pregunta "¿estructural o rebote?" con resultado conocido |

La conversión al formato de abd-bench la hacemos nosotros. La resolución entra como verdad con fuente, fecha y estado (12 §12.1). La evaluación se hará **por mecanismo**, con un juez independiente, y no por etiqueta de tipo (EXP-010).
