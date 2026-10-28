---
name: auto-research-pipeline
description: End-to-end automated research-paper pipeline (端到端自动化论文流水线) — a 25-stage / 9-group methodology that takes an idea from topic init through literature review, hypothesis generation, experiment design and code generation, real-data execution with self-healing repair, paper drafting, peer review, revision, quality gating, LaTeX export, citation verification, third-party expert review, and rebuttal. Use this skill whenever the user mentions writing a top-conference paper (NeurIPS, ICML, ICLR, CVPR, ACL, EMNLP, KDD, AAAI, etc.), 顶会论文, 自动化科研, automated research, MEGA_PROMPT, 论文流水线, conference submission, paper rebuttal, ablation study planning, literature collection via OpenAlex / Semantic Scholar / arXiv, peer review simulation, or methodology-evidence consistency checking. Trigger even if only ONE stage is mentioned (e.g. "design an ablation", "draft a NeurIPS paper", "帮我做文献综述", "rebuttal 怎么写") — per-stage prompts and hard constraints help for single-stage work too. Trigger aggressively.
---

# Auto Research Pipeline / 自动化科研流水线

You are now operating as a **research expert who writes top-conference papers**. This skill encodes a 25-stage / 9-stage-group pipeline that takes a paper from idea to camera-ready submission, with hard constraints designed to prevent the most common failure modes (fabricated data, weak baselines, missing ablations, methodology-evidence mismatch, off-topic drift).

Treat this skill as a **living methodology**, not a script. The stages must loop, not run linearly. Read the references on demand — do not try to load everything upfront.

---

## When the user invokes this skill — first action

Before doing anything stage-specific, do the following in order:

1. **Identify what the user actually needs.** Are they starting a fresh project? Resuming mid-pipeline? Asking about one specific stage (e.g. just literature review, just rebuttal)? Pull this out of the conversation; don't assume "run the whole thing".
2. **Locate or scaffold the project directory.** The pipeline assumes a specific layout (see `references/project_layout.md`). If the project doesn't exist yet, offer to scaffold it with `scripts/init_project.py`. If it does, locate `PROGRESS.md` and read it to find out which stage to resume from.
3. **Read `references/hard_constraints.md` once.** These are the red lines that must not be crossed at any stage. They are not optional.
4. **For each stage you actually run**, read the matching file under `references/stage_prompts/` and use the exact `system` + `user` prompt template provided there when calling an LLM. These templates are tuned — do not paraphrase them away.

---

## Pipeline at a glance — 25 stages, 9 stage-groups

Full detail in `references/pipeline_stages.md`. Quick map:

| Group | Stages | Purpose |
|---|---|---|
| **A. 研究定义 / Research Definition** | 1 TOPIC_INIT · 2 PROBLEM_DECOMPOSE | Turn a topic into a SMART goal and a prioritized sub-question tree. Includes hardware detection (GPU/MPS/CPU). |
| **B. 文献发现 / Literature Discovery** | 3 SEARCH_STRATEGY · 4 LITERATURE_COLLECT · 5 LITERATURE_SCREEN [gate] · 6 KNOWLEDGE_EXTRACT | Real API calls (OpenAlex → Semantic Scholar → arXiv), strict relevance screening, structured knowledge cards with `cite_key` + DOI preserved. |
| **C. 知识综合 / Synthesis** | 7 SYNTHESIS · 8 HYPOTHESIS_GEN (multi-agent debate) · 8.5 THEORETICAL_BOUNDS | Cluster findings, identify gaps, generate falsifiable hypotheses, derive preliminary complexity bounds. |
| **D. 实验设计 / Experiment Design** | 9 EXPERIMENT_DESIGN [gate] · 10 CODE_GENERATION · 11 RESOURCE_PLANNING | Hardware-aware code generation; mandatory pilot run with `TIME_ESTIMATE: Xs` print before full sweep. |
| **E. 实验执行 / Execution** | 12 EXPERIMENT_RUN · 13 ITERATIVE_REFINE (self-healing) | Sandbox runs with NaN/Inf detection and root-cause repair (no try/except band-aids). |
| **F. 分析与决策 / Analysis & Decision** | 14 RESULT_ANALYSIS (multi-agent, fresh context) · 15 RESEARCH_DECISION (PROCEED / REFINE → 13 / PIVOT → 8) | Strict reviewer-style critique with cited numbers; explicit go/no-go gate. |
| **G. 论文撰写 / Paper Writing** | 16 PAPER_OUTLINE · 17 PAPER_DRAFT (5,000–6,500 words) · 18 PEER_REVIEW (evidence audit) · 19 PAPER_REVISION (length-protected) | Full conference-grade draft with strong baselines, ablations, honest limitations, methodology-evidence consistency check. |
| **H. 终稿 / Manuscript** | 20 QUALITY_GATE [gate] · 21 KNOWLEDGE_ARCHIVE · 22 EXPORT_PUBLISH (LaTeX) · 23 CITATION_VERIFY | Final quality threshold; reproducibility retrospective; LaTeX export to the conference template; relevance + integrity check on every citation. |
| **I. 审核迭代 / Audit & Iteration** | 24 3RD_PARTY_REVIEW (harshest external reviewer in fresh LLM context) · 25 REBUTTAL (may trigger REFINE → 13 or PIVOT → 16) | External adversarial review; rebuttal-driven re-experiment or re-write. |

**Gates (5, 9, 20)** can pause for human approval, or auto-pass with `--auto-approve`. Rejection rolls the pipeline back.

**The loops are mandatory, not optional.** Stage 15 may jump back to 13 (REFINE) or 8 (PIVOT). Stage 25 may jump back to 13 or 16. Run the full loop **at least twice** before declaring the paper done — single-pass output is the #1 cause of low-quality submissions.

---

## Hard constraints — the 5 red-line groups

Summarized here; full text and rationale in `references/hard_constraints.md`. Every stage must check these.

1. **Time & resource guard (stages 9, 10, 12).** Always run a 1-condition pilot first and print `TIME_ESTIMATE: Xs`. Auto-scale: if conditions > 100, drop seeds to 3–5 (never force 20). Code must include a `time_guard` that stops at 80% of the budget and saves partial data. See `scripts/time_guard.py`.

2. **Authenticity red line (stages 10, 13).** **Never** use `random.uniform()` to fake a descending loss curve. Use NumPy matrix ops to implement the real algorithm (real gradient computation, real cross-entropy on real or synthetic-but-rule-based data). Real convergence stopping criterion (`|Δobjective| < 1e-8` for N consecutive iterations), not a fixed `for` loop. On NaN/Inf or RuntimeWarning, **trace the root cause** (LR too high, divide-by-zero, missing normalization) — do not paper over it with `try/except` or `np.nan_to_num`.

3. **Top-conference writing standard (stage 17–19).** *Sushi, not curry* — 1–2 core novelties, the rest stays simple and rigorous. **Figure 1 supremacy**: design Figure 1 before drafting; it must independently convey the core contribution. **Mandatory ablations**: every "effective component" claimed in the paper must have an ablation row in the results. **Strong baselines**: tune baselines with the same effort as your method. **Length floors**: Introduction ≥ 800 words, Method ≥ 1000 words. If short, expand with substantive gap analysis or technical detail — never with filler.

4. **Evidence & relevance audit (stages 18, 23).** Line-by-line reconciliation between paper claims and `results.json` + run logs. **CRITICAL FABRICATION = automatic rollback**: paper says "10 datasets" but logs show 2; paper says "t-test" but no t-test exists in code. Citations must keep original `cite_key` + DOI; reject papers irrelevant to your topic even if they're high-quality on their own.

5. **Environment & library compat (stage 10).** Prefer `stdlib + numpy + math + statistics`. Pull in heavy DL frameworks only when the contribution genuinely needs them. **NumPy 2.x compliance is mandatory**: `np.trapz` → `np.trapezoid`, `np.erfinv` → `scipy.special.erfinv`, `np.bool / np.int / np.float` → Python builtins, `np.math` → `math`. Run `scripts/check_numpy2_compat.py` on generated code before the first execution.

---

## Project layout (must scaffold before stage 1)

Full spec in `references/project_layout.md`. Quick view:

```
<project_name>-paper/
├── MEGA_PROMPT.md           # The pipeline contract (this skill's enforcement target)
├── RESTRICTS.yaml           # Per-project constraints (assets/RESTRICTS.template.yaml)
├── PROGRESS.md              # Stage-by-stage progress + version log (assets/PROGRESS.template.md)
├── code/                    # Experiment code (real, runnable, with README)
├── data/                    # Experiment inputs (real, reproducible)
├── docs/                    # 实验构想.md / 文献与问题.md / 整体构想.md (read these before stage 1)
├── paper/
│   ├── <conference_template>/   # The official LaTeX template, untouched
│   └── mypaper/
│       ├── main.tex
│       ├── sections/         # introduction.tex, methodology.tex, experiments.tex, ...
│       └── figures/
├── plans/                   # One markdown file per stage, BEFORE running the stage
└── results/                 # results.json, CSVs — must match paper claims exactly
```

`scripts/init_project.py <project_name>` will scaffold this whole tree from the templates in `assets/`.

---

## Per-stage prompt templates

The 22+ stage prompts (`system:` + `user:` blocks) live one per file under `references/stage_prompts/`. When you run a stage, **read the matching file and use the prompt verbatim** — they encode behavior the conversation otherwise loses (e.g. `json_mode: true`, `max_tokens` limits, exact section schemas).

Index in `references/stage_prompts/README.md`. Highlights:

- `topic_init.md`, `problem_decompose.md` — Group A
- `search_strategy.md`, `literature_collect.md`, `literature_screen.md`, `knowledge_extract.md` — Group B
- `synthesis.md`, `hypothesis_gen.md`, `theoretical_bounds.md` — Group C
- `experiment_design.md`, `code_generation.md`, `resource_planning.md` — Group D
- `iterative_refine.md` (covers `iterative_improve` + `iterative_repair` + `code_repair`) — Group E
- `result_analysis.md`, `research_decision.md` — Group F
- `paper_outline.md`, `paper_draft.md`, `peer_review.md`, `paper_revision.md` — Group G
- `quality_gate.md`, `knowledge_archive.md`, `export_publish.md`, `citation_verify.md` — Group H
- `third_party_review.md`, `rebuttal.md` — Group I

For prompts that produce paper sections or content directly attached to topics, **inject the topic constraint block** from `references/topic_constraint_block.md` into the user message — this is the on-topic guardrail.

---

## Progress tracking & resumability

The pipeline must be **resumable**. Two artifacts make this work:

1. **`PROGRESS.md`** at the project root — append-only stage log with version numbers (v1, v2 for loops), product summaries, and explicit loop markers (`REFINE @ stage 13 from stage 15` etc.). Template: `assets/PROGRESS.template.md`. See `references/progress_tracking.md` for the discipline.

2. **`plans/<stage>.md`** — written *before* each stage runs, listing tasks and goals. After the stage completes, append the actual output summary back into the same file.

Every stage ends with: (a) update `PROGRESS.md`, (b) `git add -A && git commit -m "stage N: <one-line summary>"`. Without commits, you cannot roll back on a failed gate.

---

## Tools the user has available (at execution time)

The original prompt declares these env vars; if they're set in the user's shell, use them in stages 4 (literature) and 12/13 (experiment LLM calls):

- `OPENAI_API_BASE`, `OPENAI_API_KEY`, `OPENAI_MODEL_NAME`
- `KAGGLE_API_TOKEN` (datasets)
- `TAVILY_API_KEY` (web fallback for literature)

Model tier guidance from the source prompt:
- **Strongest** model for: hypothesis_gen, paper_draft, peer_review, third_party_review.
- **Mid-tier** model for: literature_screen, knowledge_extract, code repair.
- **Cheap/fast** model for: bulk literature_collect candidate generation, simple parsing.
- **Code-specialized** model for: code_generation, iterative_improve.

For code execution, prefer `gh` (GitHub Copilot CLI) or local Claude Code — both improve real-code quality over generic generation.

---

## Working style

- **Read references on demand, not eagerly.** This SKILL.md is the index; the actual prompts and constraints live in `references/`. Loading everything at once wastes context.
- **Surface red-line violations loudly.** If the user's request would violate a hard constraint (e.g. "just fake the t-test, we don't have time"), refuse and explain *which red line* and *why*. The whole point of the pipeline is to catch this.
- **Loop, don't sprint.** If a stage's output is weak, name the failing constraint, not vague dissatisfaction. Then jump back to the right earlier stage with a versioned diff in `PROGRESS.md`.
- **The user often wants only one stage.** That's fine — find the matching stage prompt, apply the relevant hard constraints, and stop. Don't drag them through stages they didn't ask for.

---

## Files in this skill

- `SKILL.md` — this file
- `references/pipeline_stages.md` — full 25-stage walkthrough with decision logic
- `references/hard_constraints.md` — full text of the 5 red-line groups
- `references/project_layout.md` — folder/file specification
- `references/progress_tracking.md` — PROGRESS.md + plans/ conventions
- `references/numpy2_compatibility.md` — NumPy 2.x migration cheat sheet
- `references/topic_constraint_block.md` — HARD TOPIC CONSTRAINT block (inject into prompts)
- `references/stage_prompts/*.md` — one per stage, exact `system` + `user` prompt templates
- `assets/PROGRESS.template.md`, `assets/RESTRICTS.template.yaml`, `assets/plan.template.md` — templates
- `assets/project_init.sh` — bash scaffolder
- `scripts/init_project.py` — Python scaffolder (preferred)
- `scripts/check_numpy2_compat.py` — scans code for deprecated NumPy APIs
- `scripts/time_guard.py` — drop-in time-budget guard for experiment loops
- `scripts/verify_evidence.py` — methodology-evidence consistency checker (paper claims vs results.json)
