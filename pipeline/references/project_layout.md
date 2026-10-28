# Project Layout — File and Folder Specification

This is the directory the pipeline operates on. **Scaffold this before running stage 1.** Use `scripts/init_project.py <project_name> <conference_template>` to create it from the templates in `assets/`.

```
<project_name>-paper/
│
├── MEGA_PROMPT.md             # The pipeline contract — copy of the master prompt
│                              # this skill enforces. Never edit during execution.
│
├── RESTRICTS.yaml             # Per-project constraints. Length limits, year cutoffs,
│                              # quality threshold, model tier choices, etc.
│                              # See assets/RESTRICTS.template.yaml
│
├── PROGRESS.md                # Stage-by-stage progress log with version markers
│                              # for every loop. THE single source of truth for
│                              # "where are we in the pipeline".
│                              # See assets/PROGRESS.template.md
│
├── code/                      # All experiment code.
│   ├── README.md              # How to run the experiments (commands, env vars, expected runtime).
│   ├── main.py                # Entry point — runs all conditions, writes results.json.
│   ├── algorithms/            # One file per algorithm (proposed + baselines).
│   ├── benchmarks/            # Objective functions, datasets, evaluation metrics.
│   ├── utils/                 # Logging, time_guard, seed helpers.
│   └── requirements.txt       # Pinned deps. Updated whenever a new package is added.
│
├── data/                      # Experiment inputs.
│   ├── README.md              # Provenance — where each dataset came from + license.
│   └── <datasets>/            # Raw or preprocessed data, one folder per dataset.
│                              # If data is large, a download script + manifest is fine.
│
├── docs/                      # Research artifacts produced by the pipeline.
│   ├── 00_topic_init.md           # Stage 1 output
│   ├── 01_problem_tree.md         # Stage 2
│   ├── 02_search_plan.yaml        # Stage 3
│   ├── 03_candidates.jsonl        # Stage 4
│   ├── 04_shortlist.jsonl         # Stage 5
│   ├── 05_knowledge_cards.json    # Stage 6
│   ├── 06_synthesis.md            # Stage 7
│   ├── 07_hypotheses.md           # Stage 8
│   ├── 07b_theoretical_bounds.md  # Stage 8.5
│   ├── 08_experiment_plan.yaml    # Stage 9
│   ├── 21_retrospective.md        # Stage 21
│   │
│   ├── 实验构想.md / experiment_concept.md       # MUST exist before stage 1.
│   │                              # Detailed experimental design — read at start.
│   ├── 文献与问题.md / lit_and_questions.md      # MUST exist before stage 1.
│   │                              # Related work analysis + anticipated reviewer questions.
│   └── 整体构想.md / overall_concept.md          # MUST exist before stage 1.
│                                  # Paper-level vision and outline.
│
├── paper/
│   ├── <conference_template>/   # The official LaTeX template, copied untouched
│   │                            # (e.g. neurips_2024/, icml2024/, iclr2024_conference/).
│   │                            # README.md, .bib, .bst, .pdf (sample), .sty, .tex, etc.
│   │
│   └── mypaper/                 # Where you actually write the paper.
│       ├── main.tex             # Top-level — \input{sections/*.tex}
│       ├── references.bib       # Bibliography. cite_keys preserved from stage 6.
│       ├── sections/
│       │   ├── 00_outline.md          # Stage 16 (markdown first, optional)
│       │   ├── abstract.tex
│       │   ├── introduction.tex
│       │   ├── related_work.tex
│       │   ├── method.tex
│       │   ├── experiments.tex
│       │   ├── results.tex
│       │   ├── discussion.tex
│       │   ├── limitations.tex
│       │   ├── conclusion.tex
│       │   └── appendix.tex            # Spillover content; reviewers don't have to read.
│       │
│       ├── figures/
│       │   ├── figure1.pdf            # The "Figure 1 supremacy" figure.
│       │   ├── figure1_prompt.txt     # Detailed prompt used to generate it.
│       │   └── ...
│       │
│       ├── 18_peer_review.md          # Stage 18 output
│       ├── 20_quality_gate.json       # Stage 20 output
│       ├── 23_citation_audit.md       # Stage 23 output
│       ├── 24_external_review.md      # Stage 24 output
│       └── v<N>/                       # Snapshots before each major revision.
│
├── plans/                     # Per-stage plan markdown — written BEFORE running each stage.
│   ├── stage_01_topic_init.md
│   ├── stage_02_problem_decompose.md
│   ├── ...
│   └── stage_25_rebuttal.md
│   # After the stage runs, append the actual output summary at the bottom of the same file.
│   # See assets/plan.template.md
│
└── results/                   # All experiment outputs.
    ├── results.json           # The canonical structured-results file. Paper claims
    │                          # are verified against this.
    ├── *.csv                  # Per-condition CSV exports (optional).
    ├── run_<timestamp>.log    # Stdout/stderr captures.
    ├── 14_analysis.md         # Stage 14 output
    ├── 15_decision.md         # Stage 15 output
    └── v<N>/                  # Snapshots taken on each REFINE/PIVOT loop.
```

## Rules about adding files

You can create extra files/folders as needed (e.g. `notebooks/` for exploratory analysis, `scripts/` for one-off project-specific tools), but:

- Their purpose must be clear from the name or a top-level README.
- They must not collide with the structure above.
- They must be tracked in git unless they are large generated artifacts (then `.gitignore` them).

## Rules about not editing files

- **The conference template directory** (`paper/<conference_template>/`) is sacred — never modify the original `.sty`, `.bst`, `.tex` files. If you need a custom command, define it in your own preamble inside `paper/mypaper/main.tex`.
- **`MEGA_PROMPT.md`** is the contract — copy of the source prompt this skill enforces. Don't edit it during a run; if requirements change, version it (`MEGA_PROMPT_v2.md`).

## Git discipline

Initialize git at the project root immediately after scaffolding. Commit:

- Once after scaffolding — `chore: scaffold project skeleton`.
- After every stage completes — `stage <N> <name>: <one-line summary>`.
- After every loop (REFINE/PIVOT) — `loop v<N>: REFINE from stage 15 to stage 13`.

This is what makes rollbacks safe.
