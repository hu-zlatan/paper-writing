# Pipeline Stages — Detailed Walkthrough

This file expands every stage in the 25-stage pipeline. Read the section for the stage you are about to run; do not read the whole file unless you are planning the entire project from scratch.

Each stage block below has the same shape:

- **Inputs** — what must exist before the stage runs
- **Action** — what to do (call which prompt template, run which script, etc.)
- **Outputs** — files/artifacts produced
- **Gates / loops** — when to roll back

The exact LLM prompt templates live in `stage_prompts/`. This file is the operational guide; the prompt files are the literal text to send.

---

## Group A — Research Definition

### Stage 1. TOPIC_INIT
- **Inputs:** topic string, list of domains, project name, target quality threshold.
- **Action:** Use `stage_prompts/topic_init.md`. Output a SMART research goal in markdown.
- **Outputs:** `docs/00_topic_init.md` with sections: Topic, Scope, SMART Goal, Constraints, Success Criteria, Generated.
- **Loop:** none — first stage.

### Stage 1+. Hardware detection
- **Action:** detect GPU (NVIDIA CUDA / Apple MPS / pure CPU). If pure CPU, warn the user and bias stage 10 toward lightweight numpy code. Log the decision into `PROGRESS.md`.

### Stage 2. PROBLEM_DECOMPOSE
- **Inputs:** stage 1 goal markdown.
- **Action:** Use `stage_prompts/problem_decompose.md`. Generate ≥4 prioritized sub-questions.
- **Outputs:** `docs/01_problem_tree.md` with sections: Source, Sub-questions, Priority Ranking, Risks.

---

## Group B — Literature Discovery

### Stage 3. SEARCH_STRATEGY
- **Inputs:** topic, problem tree.
- **Action:** Use `stage_prompts/search_strategy.md` (json_mode). At least 3 strategies, 8+ short queries (3–6 words each). Cover: core topic, related methods, benchmarks/datasets, theoretical foundations, applications.
- **Outputs:** `docs/02_search_plan.yaml` and a sources manifest with `id, name, type, url, status, query, verified_at`.

### Stage 4. LITERATURE_COLLECT (real APIs)
- **Inputs:** search plan.
- **Action:** Hit OpenAlex first (best metadata + free), then Semantic Scholar, then arXiv as fallback. Use `stage_prompts/literature_collect.md` only if API access is unavailable; the LLM is the worst source for real bibliographic data — always prefer the API. Aim for **≥30 candidate papers** with full `id, title, source, url, year, abstract, collected_at` fields.
- **Outputs:** `docs/03_candidates.jsonl`.
- **API endpoints reminder:**
  - OpenAlex: `https://api.openalex.org/works?search=<q>&per_page=25`
  - Semantic Scholar: `https://api.semanticscholar.org/graph/v1/paper/search?query=<q>&limit=25&fields=title,abstract,year,authors,externalIds`
  - arXiv: `http://export.arxiv.org/api/query?search_query=all:<q>&max_results=25`

### Stage 5. LITERATURE_SCREEN  [GATE]
- **Inputs:** candidates JSONL.
- **Action:** Use `stage_prompts/literature_screen.md` (json_mode, strict). **Reject off-topic papers aggressively** — even high-quality papers in adjacent domains must go. Preserve every original field, including `cite_key`, `doi`, `arxiv_id`. Output `relevance_score`, `quality_score`, `keep_reason` per paper.
- **Year filter:** by default keep papers ≥ specified year (the source prompt asks for ≥ a configurable cutoff; ICML/NeurIPS-style papers usually want ≥2018).
- **Output:** `docs/04_shortlist.jsonl` with ≥30 entries (if fewer, loop back to stage 3 with a broader strategy).
- **Gate:** human review or `--auto-approve`. Reject → loop back to stage 3.

### Stage 6. KNOWLEDGE_EXTRACT
- **Inputs:** shortlist.
- **Action:** Use `stage_prompts/knowledge_extract.md` (json_mode). Each card: `card_id, title, cite_key, problem, method, data, metrics, findings, limitations, citation`. **Preserve `cite_key` exactly.**
- **Output:** `docs/05_knowledge_cards.json`.

---

## Group C — Synthesis

### Stage 7. SYNTHESIS
- **Inputs:** knowledge cards.
- **Action:** Use `stage_prompts/synthesis.md`. Output: Cluster Overview, Cluster 1..N, Gap 1..N, Prioritized Opportunities.
- **Output:** `docs/06_synthesis.md`.

### Stage 8. HYPOTHESIS_GEN  (multi-agent debate)
- **Inputs:** synthesis markdown.
- **Action:** Use `stage_prompts/hypothesis_gen.md`. Generate **≥2 falsifiable hypotheses** with rationale, measurable prediction, failure condition. To get the multi-agent debate, run the prompt 2–3 times with adversarial roles ("the proposer", "the skeptic", "the methodologist") and merge.
- **Output:** `docs/07_hypotheses.md`.
- **Loop target:** stage 15's PIVOT decision routes back here.

### Stage 8.5. THEORETICAL_BOUNDS
- **Inputs:** hypotheses.
- **Action:** Use `stage_prompts/theoretical_bounds.md`. Preliminary mathematical proof + algorithmic complexity (time/space) analysis. Even a rough big-O is better than none — reviewers ask for it.
- **Output:** `docs/07b_theoretical_bounds.md`.

---

## Group D — Experiment Design

### Stage 9. EXPERIMENT_DESIGN  [GATE]
- **Inputs:** hypotheses.
- **Action:** Use `stage_prompts/experiment_design.md`. Output YAML with keys: `objectives, datasets, baselines, proposed_methods, ablations, metrics, risks, compute_budget`.
- **Hard constraint:** **every "effective component" listed in `proposed_methods` must have a matching ablation in `ablations`.** This is the only way to satisfy the stage-18 evidence audit later.
- **Output:** `docs/08_experiment_plan.yaml`.
- **Gate:** human review. Reject → loop back to stage 8.

### Stage 10. CODE_GENERATION
- **Inputs:** experiment plan.
- **Action:** Use `stage_prompts/code_generation.md`. Generate the full project under `code/`. **Mandatory checks before considering this stage done:**
  1. Run `scripts/check_numpy2_compat.py code/` — must pass.
  2. `main.py` must contain a `time_guard` (use `scripts/time_guard.py` as the template).
  3. Code must implement a **real convergence stop**: track `|Δobjective|` for N consecutive iterations against `1e-8`, not just a fixed loop.
  4. Code must write a structured `results.json` (per-algorithm × per-function × per-dimension).
  5. **Forbidden:** `subprocess`, `os.system`, `eval`, `exec`, network calls, fake `random.uniform()` "loss" curves.
- **Output:** `code/main.py`, `code/<modules>.py`, `code/README.md`.

### Stage 11. RESOURCE_PLANNING
- **Inputs:** experiment plan.
- **Action:** Use `stage_prompts/resource_planning.md` (json_mode). Schedule with `tasks[{id,name,depends_on,gpu_count,estimated_minutes,priority}], total_gpu_budget`.
- **Mandatory pilot:** before queuing the full sweep, run **1 condition** end-to-end and print `TIME_ESTIMATE: Xs`. Multiply by N conditions × M seeds; if the total exceeds the budget, apply scaling rules:
  - >100 conditions → drop seeds to 3–5
  - over-budget → cap optimization steps at ≤5,000

---

## Group E — Execution

### Stage 12. EXPERIMENT_RUN
- **Inputs:** validated code, schedule.
- **Action:** Run the experiments in the sandbox. Stream logs to `results/run_<timestamp>.log`. Watch for `nan`, `inf`, `RuntimeWarning`, `OverflowError`. On any of these → stage 13.
- **Output:** `results/results.json` + per-condition CSVs/logs.

### Stage 13. ITERATIVE_REFINE  ← self-healing
- **Inputs:** failed/warning-emitting run, all project files.
- **Action:** Use `stage_prompts/iterative_refine.md`. This single template covers three sub-modes from the original prompt:
  - **`code_repair`** — static validation errors (syntax, undefined names, import errors).
  - **`iterative_repair`** — runtime bugs (NaN, Inf, divide-by-zero, overflow).
  - **`iterative_improve`** — improving a working but underperforming experiment.
- **Hard rule:** trace the root cause. Do not wrap things in `try/except` to silence warnings. Do not call `np.nan_to_num()` to "smooth over" a NaN that came from a real bug (e.g. a divide by zero or unnormalized log).
- **Loop target:** stages 15 and 25 may re-enter here.

---

## Group F — Analysis & Decision

### Stage 14. RESULT_ANALYSIS  ← multi-agent, fresh context
- **Inputs:** `results/results.json`, run logs.
- **Action:** Use `stage_prompts/result_analysis.md`. **Spawn this in a fresh LLM context** with no prior conversation contamination. The prompt instructs the LLM to be the harshest reviewer and to cite *exact* numbers from the data — this is how we catch fabrication early.
- **Required sections:** Metrics Summary (with real values), Comparative Findings, Statistical Checks, Limitations, Conclusion.
- **Output:** `results/14_analysis.md`.

### Stage 15. RESEARCH_DECISION  ← PROCEED / REFINE / PIVOT
- **Inputs:** analysis markdown.
- **Action:** Use `stage_prompts/research_decision.md`. Output: Decision (PROCEED | REFINE | PIVOT), Justification, Evidence, Next Actions.
- **Loop:**
  - **PROCEED** → continue to stage 16.
  - **REFINE** → snapshot current results into `results/v<N>/`, then jump back to **stage 13**. Increment version in `PROGRESS.md`.
  - **PIVOT** → snapshot, then jump back to **stage 8** (hypothesis_gen).
- **Output:** `results/15_decision.md`.

---

## Group G — Paper Writing

### Stage 16. PAPER_OUTLINE
- **Inputs:** analysis + decision + topic constraint block.
- **Action:** Use `stage_prompts/paper_outline.md`. Per-section goals + evidence links. **Inject `references/topic_constraint_block.md` into the user message** to keep the outline on-topic.
- **Output:** `paper/mypaper/sections/00_outline.md`.

### Stage 17. PAPER_DRAFT
- **Inputs:** outline, results, knowledge cards.
- **Action:** Use `stage_prompts/paper_draft.md` (max_tokens: 32768).
- **Length floors (NeurIPS/ICML/ICLR-style 9-page paper, 5,000–6,500 words main body):**
  - Title: 10–15 words
  - Abstract: 150–250 words
  - Introduction: 800–1000 words
  - Related Work: 600–800 words
  - Method: 1000–1500 words
  - Experiments: 800–1200 words
  - Results: 600–800 words
  - Discussion: 400–600 words
  - Limitations: 200–300 words
  - Conclusion: 200–300 words
- **Hard rules:**
  - Every metric value in the draft must exactly match `results.json`. No rounding tricks, no rephrasing of numbers.
  - **Figure 1 must be sketched first.** Leave a detailed `% FIGURE 1 PROMPT:` comment in the LaTeX file describing every visual element — this becomes the Nano Banana 2 prompt.
  - **Sushi, not curry** — 1–2 core novelties. Resist adding unrelated modules.
- **Output:** `paper/mypaper/sections/{introduction,related_work,method,experiments,results,discussion,limitations,conclusion}.tex` (or `.md` first, then LaTeX in stage 22).

### Stage 18. PEER_REVIEW  ← evidence audit
- **Inputs:** draft + `results.json` + run logs.
- **Action:** Use `stage_prompts/peer_review.md`. Two reviewer perspectives (Reviewer A, Reviewer B), each with strengths, weaknesses, actionable revisions.
- **The audit is the point.** The prompt forces line-by-line comparison of paper claims vs evidence. Specific red-line checks:
  - Number of trials in paper == number in code/logs?
  - Statistical tests claimed (ANOVA, t-test, Mann-Whitney) actually implemented in code?
  - Metrics reported in paper present in `results.json`?
  - Methods described in paper match code?
  - Section length thresholds met?
  - Score 1–10 with rubric: 1–3 Reject, 4–5 Borderline, 6–7 Weak Accept, 8–9 Accept, 10 Strong Accept.
- **CRITICAL FABRICATION trigger:** any mismatch above forces a rollback to stage 13 (re-experiment) or stage 17 (rewrite). No exceptions.
- **Output:** `paper/mypaper/18_peer_review.md`.

### Stage 19. PAPER_REVISION  ← length-protected
- **Inputs:** draft + reviews.
- **Action:** Use `stage_prompts/paper_revision.md` (max_tokens: 32768). **Never shorten** during revision — only expand, improve, add. The final paper must be ≥ the draft's length.
- **Output:** revised draft in place; previous version saved to `paper/mypaper/v<N>/`.

---

## Group H — Manuscript

### Stage 20. QUALITY_GATE  [GATE]
- **Inputs:** revised paper.
- **Action:** Use `stage_prompts/quality_gate.md` (json_mode). Returns `{score_1_to_10, verdict, strengths, weaknesses, required_actions}`.
- **Threshold:** project's `quality_threshold` (typically 7.5+ for NeurIPS/ICML).
- **Gate:** fails → loop back to stage 19 with `required_actions`. Three failed cycles → loop back to stage 13 (the experiments themselves are weak).
- **Output:** `paper/mypaper/20_quality_gate.json`.

### Stage 21. KNOWLEDGE_ARCHIVE
- **Inputs:** decision, analysis, revised paper.
- **Action:** Use `stage_prompts/knowledge_archive.md`. Reproducibility-focused retrospective with lessons, repro notes, future work.
- **Output:** `docs/21_retrospective.md`.

### Stage 22. EXPORT_PUBLISH  ← LaTeX
- **Inputs:** revised markdown sections + the official conference template under `paper/<conference_template>/`.
- **Action:** Convert each section markdown into LaTeX inside `paper/mypaper/sections/*.tex`. Do **not** modify the template — only the `mypaper/` files. Build with `pdflatex` + `bibtex` + `pdflatex` × 2.
- **Page limit:** body must end (Conclusion's last line) within the conference's page limit (e.g., NeurIPS = 9). References can spill onto extra pages. Appendix is unlimited but reviewers don't have to read it; put non-essential detail there.
- **Output:** `paper/mypaper/main.pdf`.

### Stage 23. CITATION_VERIFY  ← relevance audit
- **Inputs:** `*.bib`, draft text.
- **Action:** For every `\cite{...}` in the draft, verify:
  1. The `cite_key` exists in `*.bib`.
  2. The DOI/URL resolves to a real paper.
  3. The paper is *actually relevant to the topic*. Reject high-quality but unrelated papers — these are tells of LLM hallucination.
- **Output:** `paper/mypaper/23_citation_audit.md` with a green/yellow/red flag per citation.

---

## Group I — Audit & Iteration

### Stage 24. 3RD_PARTY_REVIEW  ← harshest external reviewer
- **Inputs:** final PDF + experiment evidence.
- **Action:** Spawn a **fresh LLM context** with no project history. Use `stage_prompts/third_party_review.md`. The role: a senior area-chair who has rejected 80% of the papers they've reviewed this cycle. They look for: incremental contributions, weak baselines, missing ablations, unsupported claims, dishonest limitations, off-topic drift.
- **Output:** `paper/mypaper/24_external_review.md`.

### Stage 25. REBUTTAL
- **Inputs:** stage 24 review.
- **Action:** Use `stage_prompts/rebuttal.md`. Generate a point-by-point response. Some responses can be done in text alone; others demand new experiments or a method-section rewrite.
- **Loop:**
  - **Experiment-related issue** → REFINE → stage 13.
  - **Paper-structure or framing issue** → PIVOT → stage 16.
  - **Both** → do experiments first, then re-outline.
- **Run the full loop ≥ 2 times** before declaring done. Single-pass papers fail acceptance thresholds.

---

## Decision-loop summary (cheat sheet)

```
        ┌────────── PIVOT ───────────────────┐
        ↓                                    │
  [8 hypothesis_gen] → [9 design] → [10 code] → [12 run] → [13 refine] ←──┐
                                                       ↓                  │
                                                 [14 analysis]            │
                                                       ↓                  │
                                            [15 decision] ─── REFINE ─────┘
                                                       ↓ PROCEED
        ┌────────── PIVOT (rebuttal) ────────────────┐
        ↓                                            │
  [16 outline] → [17 draft] → [18 peer review] → [19 revise] → [20 gate]
                                                                  ↓
                                                       [22 LaTeX] → [23 cite verify]
                                                                  ↓
                                                       [24 ext review] → [25 rebuttal] ──> REFINE/PIVOT
```

Always commit after each stage. Always update `PROGRESS.md`. Always run the loop at least twice.
