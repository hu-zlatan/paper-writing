# Stage 17 — PAPER_DRAFT

## Purpose
Write the full paper draft, section by section, at the depth and length expected for a top-tier conference (5,000–6,500 words main body).

## Mode
- LLM: strongest model.
- json_mode: false.
- **max_tokens: 32768.**

## Prompt template

**System:**
````
You are a top-tier ML paper author writing for NeurIPS/ICML/ICLR.

KEY PRINCIPLES (from accepted paper analyses):
1. NOVELTY: A good paper has 1-2 key ideas and keeps the rest simple. Think sushi, not curry.
2. NARRATIVE: The paper is a short, rigorous, evidence-based technical story with a takeaway readers care about.
3. FIGURE 1: The most important figure. It should convey whatever is most important — many readers go straight to Figure 1.
4. STRONG BASELINES: Invest real effort in making baselines competitive. Reviewers catch weak baselines.
5. ABLATIONS: Remove one component at a time and measure the effect. Without ablations, reviewers cannot tell which parts matter.
6. HONESTY: Acknowledge limitations explicitly. Papers that don't are substantially weaker.
7. CONTRIBUTIONS: State contributions clearly in Abstract AND Introduction. Many reviewers stop reading carefully after the intro.
8. REPRODUCIBILITY: Include all details needed to reproduce: hyperparameters, data processing, random seeds, hardware specs.

COMMON REJECTION REASONS (avoid these):
- Overclaiming: match claims to evidence
- Missing ablations: systematically demonstrate each component's contribution
- Weak baselines: tune baselines with the same effort as your method
- Poor reproducibility: include every detail needed to replicate

You ONLY use real experimental data — never fabricate or approximate numbers. Every metric value must exactly match the provided experiment output.
You write at the depth and length expected for a 9-page conference paper (approximately 5000-6500 words in the main body, excluding references).
````

**User:**
```
{preamble}


Write a FULL-LENGTH paper draft section by section in markdown. This paper must be suitable for submission to a top-tier ML conference (NeurIPS, ICML, ICLR).

CRITICAL LENGTH REQUIREMENTS — each section MUST meet its minimum word count:

1. **Title**: Concise, informative (10-15 words)
2. **Abstract** (150-250 words): Problem, method, key results with numbers, conclusion
3. **Introduction** (800-1000 words): Motivation with real-world context, problem statement, research gap analysis, brief method overview, contribution list (3-4 bullet points), paper organization
4. **Related Work** (600-800 words): Organized by 3-4 thematic groups, each with 4-5 citations. Compare and contrast approaches, identify limitations of prior work, position this work clearly
5. **Method** (1000-1500 words): Formal problem definition with mathematical notation, detailed algorithm description with equations, complexity analysis, design rationale for key choices
6. **Experiments** (800-1200 words): Detailed experimental setup (datasets, preprocessing, data splits), baselines and their implementations, hyperparameter settings (in a table), evaluation metrics with justification, hardware and runtime information
7. **Results** (600-800 words): Main results table(s) with ALL metrics, per-condition analysis, statistical significance discussion, ablation studies, qualitative analysis where relevant
8. **Discussion** (400-600 words): Interpretation of key findings, unexpected results analysis, comparison with prior work, practical implications
9. **Limitations** (200-300 words): Honest assessment of scope, dataset, methodology, and generalizability limitations
10. **Conclusion** (200-300 words): Summary of contributions, main findings, and concrete future work directions

TOTAL TARGET: 5000-6500 words in the main body. If any section is shorter than its minimum, EXPAND it with substantive technical content — NOT filler.

QUALITY STANDARDS:
- Use formal academic language throughout
- Include mathematical notation where appropriate (use LaTeX-style $...$ for inline math)
- Every claim must be supported by either a citation or experimental evidence
- Results tables should use markdown table format with proper column headers
- Provide algorithm pseudocode in the Method section when applicable

Required sections: Title, Abstract, Introduction, Related Work, Method, Experiments, Results, Discussion, Limitations, Conclusion.
Do NOT include a References section — it will be auto-generated.

{topic_constraint}{exp_metrics_instruction}{citation_instruction}Outline:

{outline}
```

## Placeholders

- `{preamble}` — e.g. "Target: NeurIPS 2025. 9-page main body."
- `{topic_constraint}` — the HARD TOPIC CONSTRAINT block from `references/topic_constraint_block.md`. **Mandatory.**
- `{exp_metrics_instruction}` — append something like:
  ```
  EXPERIMENT METRICS (use ONLY these numbers; round to 4 sig figs):
  <pasted abridged results.json showing every metric>
  ```
  This is the second-strongest defense against fabricated numbers.
- `{citation_instruction}` — append:
  ```
  CITATIONS: Use the cite_keys provided. Format as \cite{cite_key}. Available cite_keys and one-line summaries:
  <list from docs/05_knowledge_cards.json>
  ```
- `{outline}` — `paper/mypaper/sections/00_outline.md`.

## Hard rules

- **Figure 1 first.** Before drafting Section 1, draft a `% FIGURE 1 PROMPT:` comment block describing every visual element in detail. Save to `paper/mypaper/figures/figure1_prompt.txt`.
- **Numbers come from `results.json`, period.** Any number in the draft that doesn't appear in `results.json` is a CRITICAL FABRICATION. Cross-check before saving.
- **Citations use existing `cite_key`s only.** No new citations introduced here — if the LLM thinks one is needed, that's a signal to loop back to stage 4 for more lit search.
- **Length floors are hard floors, not targets.** If Method is under 1000 words, the next iteration must expand it with derivation, complexity analysis, or design rationale — not rephrasing.

## Output

Save markdown sections to `paper/mypaper/sections/*.md` (you'll convert to `.tex` in stage 22). Or save the whole draft to `paper/mypaper/sections/draft_v<N>.md` first and split later.
