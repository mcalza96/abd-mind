# Prompt de investigación 3: literatura relacionada

Tercer encargo de investigación. Busca qué se sabe ya sobre las hipótesis del [documento 15](../marco-teorico/15-forma-y-material.md) y su [evaluación externa](../marco-teorico/15-forma-y-material.md#1510-evaluación-externa-2026-10-15), antes de construir nada nuevo. Aplica las lecciones de la bitácora:

- pedir salida en un formato verificable (EXP-006);
- pedir **también la evidencia en contra** (sesgo de confirmación).

Se pega tal cual, en inglés.

---

```text
ROLE
You are a research analyst doing a critical literature review for a small project. Find what is
ALREADY KNOWN (peer-reviewed papers, strong preprints, well-documented benchmarks, up to the present
date) about the questions below, including evidence that CONTRADICTS the project's hypotheses. Do
not try to please; a finding that kills a hypothesis is the most valuable output.

PROJECT CONTEXT (short)
We built an "abductive reasoning engine": an LLM proposes hypotheses that explain conflicting
observations, then a pipeline scores them (per-observation LLM verdicts summed with weights for
consilience, coherence, parsimony) and later a "holistic" LLM judge picks the best. Results on ~20
text cases per experiment: the engine never beat a single call to a strong LLM; against the SAME
model it roughly tied (10/18 vs 10/18); decomposing into per-observation judgments lost accuracy;
abstention on underdetermined cases stayed low (≤3/10). There was no equal-compute baseline. Our
current hypotheses:
 H1 "Form vs material": arranging/combining judgments of the same LLMs can add form (consistency,
    traceability, defeasibility) but not knowledge of the world; only external feedback (data,
    experiments, time-resolved outcomes, computation) adds content.
 H2 Decomposing an abductive judgment into independent per-observation judgments and summing them
    loses inter-observation patterns and underperforms holistic judgment.
 H3 "Pre-commitment": the value of an engine around an LLM agent is to force it to register
    falsifiable predictions BEFORE observing, choose the most discriminating observation, pay for
    failed predictions, and score judges/sources by resolved outcomes; this should improve
    calibration/accuracy versus the same agent with the same tools and no such discipline.
 H4 A closed text benchmark can measure hypothesis generation/selection but not the test cycle of
    abduction (deduction + empirical testing).

QUESTIONS (answer each; cite evidence for AND against)
Q1 Aggregation without external feedback. What does the literature show about self-consistency,
   majority voting, best-of-n, multi-agent debate, mixture-of-agents, LLM-as-judge ensembles and
   cross-family ensembles: do they raise accuracy (not only consistency) at EQUAL COMPUTE? Where do
   gains vanish (e.g. open-ended or abductive tasks, correlated errors between models)?
Q2 Self-correction limits. Evidence that LLMs cannot self-correct reasoning without external
   feedback (e.g. "Large Language Models Cannot Self-Correct Reasoning Yet") and evidence of
   when they can (verifiers, tools, execution feedback).
Q3 Decomposition. When does breaking a judgment into sub-judgments (least-to-most, factored
   verification, chain-of-verification, per-claim fact checking, compound AI systems, error
   accumulation) help or hurt? Any results specifically on combining per-evidence scores vs
   holistic evaluation (including the human judgment literature: clinical vs actuarial, Dawes'
   improper linear models, naive-Bayes independence assumptions)?
Q4 LLM abductive reasoning. Systems and benchmarks for abduction / inference to the best
   explanation with LLMs (e.g. abductive NLI/ART, hypothesis generation, diagnostic reasoning,
   detective puzzles, neuro-symbolic abduction, LLM + probabilistic programming). What added value
   over a single LLM call has been demonstrated, with what baselines?
Q5 Pre-commitment and forecasting. LLM forecasting with time-resolved questions (e.g. Halawi et al.
   2024, ForecastBench, Metaculus/AI benchmarks, prediction-market comparisons): do scaffolds,
   retrieval, ensembling, or structured hypothesis tracking improve Brier scores? Is there evidence
   that committing to predictions before seeing data, or tracking source/judge reliability by
   resolved outcomes, improves an AI agent's accuracy (not only its credibility)? Human evidence
   (Tetlock superforecasters, belief updating, preregistration effects on the predictor).
Q6 Active information gathering. LLM agents that choose the most informative next observation
   (Bayesian experimental design, expected information gain, active inference, 20-questions style,
   "AI scientist" agents with experiment logs). Measured gains vs agents that search freely?
Q7 Theory-ladenness / single-point-of-failure. Work treating an LLM as a biased "observer" or
   annotator whose judgments are model-dependent; evidence on correlated errors across model
   families; whether observer plurality (different families/prompts) restores independence.
Q8 Evaluation design. Recommended methodology for testing H3: equal-compute baselines, ablations,
   power analysis for Brier differences, equivalence tests, leakage control for forecasting with
   web search (retrieval of post-cutoff information), domains with fast external verification.

RULES
1. Every claim needs a citation: authors, year, title, venue or arXiv id, and a URL. No invented
   references; if unsure a paper exists, leave it out.
2. Distinguish: peer-reviewed / preprint / blog. Give sample sizes and baselines when reported.
3. For each question, state a verdict on the related hypothesis: SUPPORTED, CONTRADICTED, MIXED,
   or NO EVIDENCE, with a one-paragraph justification.
4. Report what is genuinely NOVEL in H3 versus prior work (or say plainly that nothing is).
5. Prefer recent work (2023 onward) but include classic results where they matter.
6. Be concise: no filler, no restating the questions.

OUTPUT FORMAT (Markdown)
- Section per question Q1–Q8: key findings (bullets with citations), verdict, open gaps.
- Table "Hypotheses verdict": H1–H4 | verdict | strongest supporting source | strongest
  contradicting source.
- Section "Closest prior work to this project" (5–10 items, one line each on how it differs).
- Section "Recommended next experiments" (max 5), each with baseline and success/failure criterion.
- Reference list with URLs.
```

---

## Uso previsto

| Pregunta | Hipótesis o decisión que afecta |
|---|---|
| Q1, Q2 | H1, versión estrecha (15.10 punto 3): ¿combinar juicios sin retroalimentación agrega contenido? |
| Q3 | H2 y el análisis de errores pendiente |
| Q4 | ¿Alguien demostró valor agregado de un motor abductivo sobre un LLM? |
| Q5, Q6 | H3: ¿es nuevo?, ¿hay evidencia de que mejore el acierto? |
| Q7 | Pluralidad de observadores (contradicción 15.2 / 15.3) |
| Q8 | Diseño de la prueba de 15.8 |

La salida se verifica antes de usarla (lección transversal 8): que las referencias existan y que el formato sea el pedido.
