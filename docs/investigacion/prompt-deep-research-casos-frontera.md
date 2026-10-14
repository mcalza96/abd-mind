# Deep research brief: boundary cases for an abductive reasoning benchmark

## Context

We are building **abd-mind**, an abductive reasoning engine. Its core thesis:

- An observation or label is not "ground truth plus noise". It is a **projection** of a hidden real state through the **frame** of a specific observer (their vantage point, instrument, method, conventions or incentives): `y_i = π_{O_i}(S)`.
- When observers disagree, the right move is **not** to average them, take a majority vote, or pick the most popular explanation. It is to find the hidden state or mechanism `H` that would produce **every** observation, each one from its own observer's frame.
- If no known explanation reconciles all observations, the system must **postulate a new latent entity or mechanism**. That postulate has a cost (parsimony), and it must be **defeasible**: new evidence can overturn it.
- Hypotheses are ranked by explanatory virtues: consilience (how many observations they explain), parsimony (how few unverified entities they postulate), and coherence with known domain laws.

Our canonical toy example is a cylinder: a front observer sees a "rectangle" and a top observer sees a "circle". An inductive system averages these into a chimera ("oval"); an abductive system infers the cylinder. **In a pilot, every LLM we tested solved this case in a single call**, so it cannot discriminate between systems. We need harder, better-documented cases.

## Your task

Research and compile a dataset of **boundary cases**: real, documented situations where observers with different frames reported conflicting observations, and where a **latent cause**, established later by independent evidence, explains all of them, while the consensus or "obvious" answer was wrong or incomplete.

Target: **40 fully specified cases**, plus a list of rejected candidates.

## What qualifies as a boundary case

A case must meet **all** of these:

1. **At least two observers with distinct, describable frames.** For example: different instruments, vantage points, specialties, units, methodologies, data sources, or incentives.
2. **Conflicting observations on the surface.** Taken at face value, the reports seem incompatible or point to different conclusions.
3. **A documented latent explanation** that makes every observation expected *given each observer's frame*. You must be able to state, observation by observation, why that observer reported what they did.
4. **A concrete wrong "inductive" answer.** This is what averaging, majority vote, siding with the most authoritative observer, or the most common explanation would have produced. State it explicitly and say why it fails.
5. **Ground truth established independently.** For example: a later investigation, an experiment, a court finding, an autopsy, or a recovered data recorder. Cite it.

Strongly preferred:

- **Defeasibility.** An explanation was once accepted, and later evidence overturned it.
- **Ontological expansion.** The resolution required postulating an entity or mechanism that was not in the investigators' vocabulary at the time.

## Categories to cover

Spread the 40 cases across these categories. The seeds below are starting points to verify, not answers to copy. Prefer less famous cases (see the contamination section).

| Category | What to look for | Seeds to verify (some are deliberately famous; use them for structure, then find lesser-known analogues) |
|---|---|---|
| Scientific discovery from anomalies | An anomaly resolved by a new entity or law | Neptune from Uranus's orbit; the neutrino from the beta-decay energy deficit |
| Failed latent postulates (defeasibility) | A latent entity postulated, accepted, then refuted | Vulcan (Mercury's perihelion explained by general relativity); N-rays; polywater; OPERA faster-than-light neutrinos (loose fibre-optic cable) |
| Frame or unit mismatches | Teams or instruments using incompatible conventions | Mars Climate Orbiter (imperial vs metric); Gimli Glider (fuel units); lesser-known engineering or medical dosing incidents |
| Engineering and accident investigations | Crew reports, sensors and maintenance logs in conflict, resolved by a hidden fault | NTSB, BEA, ATSB or AAIB reports: pitot icing, angle-of-attack sensor faults, intermittent wiring. Prefer reports that are not headline cases |
| Medicine and diagnosis | Specialists seeing different "diseases" that are one systemic condition | Published case reports where cardiology, dermatology, neurology, etc. disagreed, and a unifying diagnosis was found later (sarcoidosis, Wilson's disease, amyloidosis, lupus, rare toxicology) |
| Epidemiology and confounding | Group-level data contradicting subgroup data; a hidden confounder | John Snow's Broad Street pump; Semmelweis; Simpson's-paradox cases (kidney stones, Berkeley admissions). Prefer local outbreak investigations from MMWR or Eurosurveillance |
| Finance and accounting | Analysts or auditors disagreeing, resolved by a hidden mechanism (fraud, accounting change, strategy) | Short-seller report vs auditor vs sell-side cases: Wirecard, Luckin Coffee, smaller regional cases. Also non-fraud mechanisms such as price wars, channel stuffing, or mix shifts that explain margin falling while volume rises |
| Measurement and instruments | Instruments disagreeing because of calibration, sampling or physics | Sensor-fusion conflicts, satellite vs ground measurements, contamination artifacts in labs |
| Testimony and vantage point | Witnesses from different positions reporting different events | Documented legal or investigative cases where reconstruction showed every witness was accurate from their position |
| Annotation disagreement | Labelers disagreeing systematically because of their frame | Dialect and toxicity labeling (e.g. Sap et al., 2019); medical image annotation by different specialties |
| **Negative controls** | Disagreement that **is** noise, or where averaging **is** correct, or where no latent cause exists | Wisdom-of-crowds estimates (Galton's ox); measurement repeatability studies; cases where an apparent conflict was a transcription error |

**Negative controls are mandatory.** Include at least 6. A system that always postulates hidden causes is as broken as one that always averages.

## Contamination risk (important)

Current LLMs have memorized famous cases. A benchmark built only from Neptune, John Snow and Enron would measure recall, not reasoning. For every case:

- Rate `riesgo_contaminacion` as `low`, `medium` or `high`, with a one-line justification.
- Propose a `variante_ofuscada`: a sketch of how to preserve the logical structure (observers, frames, conflicts, latent cause) while renaming entities, shifting the domain or changing numbers, so the answer cannot be recalled. Example: Neptune becomes a fictional exoplanet system with invented orbital residuals.
- Prefer primary sources that are well documented but not widely retold: individual case reports, local outbreak investigations, non-headline accident reports, regional financial cases.

Target: at least 15 cases rated `low` contamination.

## Output format

Deliver a JSONL file with one record per line. **Keep the keys exactly as written below.** They are in Spanish to match our codebase. Write the values in English.

```json
{
  "id": "snake_case_unique_id",
  "titulo": "Short title",
  "categoria": "scientific_discovery | failed_latent | frame_mismatch | engineering_incident | medicine | epidemiology | finance | measurement | testimony | annotation | negative_control",
  "tipo_frontera": ["latent_entity", "frame_mismatch", "confounder", "defeated_hypothesis", "noise_control", "unit_mismatch", "incentive_bias"],
  "descripcion": "Neutral setup as it looked BEFORE the resolution. Must not reveal or hint at the answer.",
  "observadores": [
    {"id": "O1", "nombre": "Who", "marco": "Their frame: vantage point, instrument, method, conventions, incentives"}
  ],
  "observaciones": [
    {"id": "y1", "observador_id": "O1", "contenido": "One atomic fact as the observer reported it, without interpretation", "fecha": "optional"}
  ],
  "opiniones": [
    {"observador_id": "O1", "contenido": "Judgments, recommendations or interpretations made by the observer (kept separate from facts)"}
  ],
  "respuesta_inductiva": {
    "contenido": "The averaged, majority, consensus or most-common answer",
    "por_que_falla": "Which observations it fails to explain, or why it is wrong"
  },
  "hipotesis_correcta": {
    "mecanismo": "The latent cause or mechanism",
    "entidades_latentes": ["Entities or mechanisms that had to be postulated"],
    "como_explica_cada_observacion": {"y1": "Why O1, given its frame, reported y1", "y2": "..."}
  },
  "hipotesis_distractoras": [
    {"mecanismo": "A plausible rival explanation", "observaciones_que_explica": ["y1"], "por_que_falla": "..."}
  ],
  "reglas_invariantes": ["Domain laws or constraints that any valid hypothesis must respect"],
  "evidencia_derrotante": {
    "contenido": "Later evidence that overturned a previously accepted explanation",
    "hipotesis_derrotada": "Which explanation it overturned",
    "nueva_mejor_explicacion": "What replaced it"
  },
  "verdad_establecida_por": "How and when the ground truth was established",
  "fuentes": [
    {"cita": "Full citation", "url": "https://...", "tipo": "primary | secondary"}
  ],
  "dificultad": 3,
  "riesgo_contaminacion": "low | medium | high — justification",
  "variante_ofuscada": "Sketch of a structure-preserving obfuscated version",
  "notas": "Caveats, uncertainty, contested points"
}
```

Use `null` for `evidencia_derrotante` when there is none. For negative controls, `hipotesis_correcta` describes why no latent cause is needed (for example "independent measurement noise; the mean is the best estimate"), and `respuesta_inductiva` may be correct; say so in `por_que_falla`.

`dificultad` runs from 1 (a frontier LLM solves it from the observations alone) to 5 (it requires postulating something outside the obvious vocabulary, or resisting a strong consensus).

## Quality rules

- **Do not leak the answer.** `descripcion` and `observaciones` must read as they would have before the resolution.
- **Facts, not interpretations.** Each observation is one atomic fact as the observer reported it. Opinions and recommendations go in `opiniones`.
- **2 to 6 observations per case**, from at least 2 distinct observers.
- **Every case needs at least one source**, preferably primary: an investigation report, a peer-reviewed paper, or a court or regulatory filing. Include URLs.
- **Do not fabricate.** If a detail cannot be verified, leave it out or flag it in `notas`. If the ground truth is still contested, move the case to the rejected list.
- **One mechanism per case.** If the resolution needed several independent causes, either split the case or explain it in `notas`.

## Coverage targets

| Requirement | Minimum |
|---|---|
| Total cases | 40 |
| Negative controls | 6 |
| Cases with `evidencia_derrotante` | 8 |
| Cases with `latent_entity` (ontological expansion) | 8 |
| Frame or unit mismatch cases | 5 |
| Finance or accounting cases | 5 |
| `low` contamination risk | 15 |
| Categories represented | at least 8 of the 11 |

## Deliverables

1. `boundary_cases.jsonl`: the 40 records.
2. A summary table: id, title, category, boundary types, difficulty, contamination risk.
3. A coverage matrix: categories × boundary types, with counts.
4. A rejected-candidates list: candidates you considered and dropped, with the reason (contested ground truth, too few observers, answer only available from one source, and so on).
5. A top-10 shortlist for a first benchmark run, balancing difficulty, contamination risk and category, with a one-line rationale per case.
6. Any patterns you noticed. For example: which frame types most often produce conflicts, and which kinds of latent causes are hardest to postulate.
