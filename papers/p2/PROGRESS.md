# PROGRESS — paper 2 (CertGrip, `papers/p2/`)

Format and resume rules: `pipeline/references/progress_tracking.md`. Paper 1's progress is the root `PROGRESS.md`.
Run order when both papers are active: AUTOPILOT §7.

## Stage 1. TOPIC_INIT     [v1]

- **Started:** 2026-11-08T03:20Z (owner's chat session, right after paper-1 run 36)
- **Finished:** 2026-11-08T04:00Z
- **Trigger:** owner directive 2026-11-08 (AUTOPILOT §1): second paper in a new direction, in `papers/p2/`, topic by
  Claude, distinct from paper 1.
- **Inputs used:** AUTOPILOT.md; `pipeline/references/stage_prompts/topic_init.md`; paper 1's cloud-adapted
  `MEGA_PROMPT.md` (methodology part reused); WebSearch; arXiv abstract pages 2607.25049, 2411.07833, 2605.23568,
  2608.09166; icml.cc 2027 CFP / Dates pages; corl.org.
- **Outputs produced:** `papers/p2/MEGA_PROMPT.md`, `RESTRICTS.yaml` (project block; `max_refine_cycles` 3),
  `docs/00_topic_init.md`, `docs/整体构想.md`, `docs/实验构想.md`, `docs/文献与问题.md`, `AI_USAGE.md`, `OWNER_TODO.md`,
  `data/README.md`, `plans/stage_01_topic_init.md`. Root: AUTOPILOT §1 directive + §7 (two papers); `experiments.yml`
  gains an optional `workdir` input (default `code`, paper 1 unchanged).
- **Decision — topic:** CertGrip: a learned tactile predictor of the per-grasp minimal no-slip force F\*, calibrated by
  split conformal prediction into a one-sided upper bound so that P(slip) ≤ α with a finite-sample, model-free
  guarantee; plus an online adaptive-conformal variant driven by binary slip feedback for distribution shift. Chosen
  because (i) the closest works opened (CVaR friction margin under an assumed prior; CBF safety under bounded
  disturbances; threshold reflexes; conformal prediction for contact-aware planning) give no distribution-free slip-rate
  guarantee for online force choice; (ii) simulation can measure F\* exactly by replaying a grasp at different forces,
  so validity and force excess are checkable; (iii) MuJoCo runs it on CPU. Alternatives considered and dropped: a
  controlled "does touch help" study (crowded: ManiFeel 2505.18472, 2601.10268 and others); in-hand rotation RL (needs
  GPU-scale RL); another active-touch topic (too close to paper 1).
- **Decision — venue:** RSS 2027 (Stage 1 extended abstract 2026-12-04 23:59 AoE), the only AI / robot-learning venue
  with a posted deadline on 2026-11-08 (ICML 2027 CFP page "will be posted here soon"; corl.org shows 2026 only; the
  NeurIPS 2027 CFP page could not be fetched). Re-verify the RSS CFP before stage 3. If stage 20 is not passed by
  2026-12-01, retarget instead of rushing (recorded in `docs/00_topic_init.md`).
- **Hardware (stage 1+):** sandbox 2 vCPU, 7 GB RAM, no GPU; GitHub-hosted runners (shared 20-job cap with paper 1).
  CPU is enough for the planned scale (estimate < 100 CPU-h, to be replaced by a pilot TIME_ESTIMATE).
- **Summary:** paper 2 initialised; no experiment run, no result exists.
- **Next stage:** 2 PROBLEM_DECOMPOSE (then 3 → 4 literature with verifiable IDs).

## Stage 2. PROBLEM_DECOMPOSE     [v1]

- **Started / Finished:** 2026-11-08T08:10Z / 08:25Z (scheduled run 37, after paper 1's time-critical work)
- **Inputs used:** `docs/00_topic_init.md`, `RESTRICTS.yaml` topic; template `stage_prompts/problem_decompose.md` verbatim.
- **Plan:** `plans/stage_02_problem_decompose.md`.
- **Outputs produced:** `docs/01_problem_tree.md` — 6 sub-questions: SQ1 is F\* (minimal no-slip force) a monotone,
  measurable label in MuJoCo; SQ2 split-conformal slip-rate validity (exchangeable); SQ3 force efficiency vs a safety
  factor calibrated on the same calibration set (primary comparator) and conformalized point / quantile / σ predictors;
  SQ4 tactile / probe-squeeze ablation; SQ5 online adaptive conformal with binary slip feedback under 3 shifts; SQ6
  group-conditional coverage. Priority SQ1 > SQ2 > SQ3 > SQ5 > SQ4 > SQ6. 8 risks, each with a mitigation (non-monotone
  slip → conformal risk control; label cost → pilot TIME_ESTIMATE; calibrated safety factor may match → reported either
  way; sim-only; novelty; time; split leakage).
- **Hard constraints:** no results exist or are claimed; no new citations introduced beyond stage-1 docs.
- **Decision:** PROCEED → stage 3 SEARCH_STRATEGY (re-verify the RSS 2027 CFP first).

## Stage 3. SEARCH_STRATEGY     [v1]

- **Finished:** 2026-11-08T08:45Z (run 37). Plan: `plans/stage_03_search_strategy.md`.
- **Outputs produced:** `docs/02_search_plan.yaml` (5 strategies: grip force & slip; guarantees in grasping; conformal
  methods; conformal in robotics; tactile simulation & benchmarks — 22 queries + 4 seminal), `docs/02_sources.json`
  (OpenAlex, Semantic Scholar, arXiv API, stage-1 seed IDs). Root `.github/workflows/literature.yml`: optional
  `docs_dir` input (default `docs`; paper 1 behaviour unchanged).
- **RSS CFP re-check:** not possible this run (page fetch timed out on permission; no content). Last verified
  2026-11-06. Retry before stage 5.
- **Decision:** PROCEED → stage 4 LITERATURE_COLLECT (dispatch `literature.yml` with `docs_dir: papers/p2/docs`).

## Stage 4. LITERATURE_COLLECT     [v1]

- **Finished:** 2026-11-08T08:09Z (Actions run 42461442407, `literature.yml` with `docs_dir: papers/p2/docs`).
  Plan: `plans/stage_04_literature_collect.md`.
- **Outputs produced:** `docs/03_candidates.jsonl` — 872 unique candidates (1,115 raw) from OpenAlex (26/26 queries
  ok) and arXiv (26/26 ok); Semantic Scholar failed on 25/26 queries (rate limit, logged in `docs/03_collect_log.json`).
  Every record has a DOI / arXiv ID / OpenAlex ID; 60 lack an abstract. All 9 stage-1 seed arXiv IDs are present.
- **Environment note (for stage 10):** pip `mujoco` 4.0.0 installs in the sandbox and loads the
  `mujoco.sensor.touch_grid` plugin (smoke test only; no experiment).
- **Decision:** PROCEED → stage 5 LITERATURE_SCREEN [gate, auto-approve with logged reasons].

## Stage 5. LITERATURE_SCREEN [GATE]     [v1]

- **Finished:** 2026-11-08T09:00Z (run 37). Plan: `plans/stage_05_literature_screen.md`.
- **Outputs produced:** `docs/04_prefiltered.tsv` (824 after year / ID / abstract filter), `docs/04_screen_decisions.json`,
  `docs/04_shortlist.jsonl` — **52 papers**: grip force & slip 17, guarantees / risk in grasping 5, conformal methods 13,
  conformal in robotics / control 11, tactile simulation & benchmarks 5 (+ the 9 stage-1 seeds, all kept). Code:
  `code/literature/screen_p2.py` (adapted from paper 1's `code/literature/screen.py`, noted in its docstring),
  `code/literature/screen_decisions_v1.py`.
- **GATE — auto-approved (AUTOPILOT §1).** Evidence: 52 ≥ 30 (template) and ≥ 20 (`RESTRICTS.yaml`
  `min_papers_after_screen`); every entry keeps its original `cite_key` / DOI / arXiv ID and has a verifiable ID; all
  entries ≥ 2018 except 2 recorded seminal exceptions; off-topic rejections recorded in the script docstring. Reason:
  coverage spans every stage-2 sub-question (SQ1–SQ6) and the closest guarantee-type competitors (FIRMGrasp, tactile
  CBF grasping, conformal decision theory). Known gap for stage 6–7: no paper found that conformally calibrates grip
  force; to be re-checked with a targeted search in stage 7.
- **RSS CFP:** still not re-verified (WebFetch unavailable this run). Last verified 2026-11-06.
- **Decision:** PROCEED → stage 6 KNOWLEDGE_EXTRACT.

## Stage 6. KNOWLEDGE_EXTRACT     [v1]

- **Finished:** 2026-11-08T09:20Z (run 37). Plan: `plans/stage_06_knowledge_extract.md`.
- **Outputs produced:** `docs/05_knowledge_cards.json` (52 cards, abstracts only), `code/literature/build_cards_v1.py`.
  Extraction by a fresh Sonnet subagent with the stage template; the session checked keys (52/52, none extra) and that
  every number in findings / data / metrics occurs in the source abstract (0 violations).
- **Notes for stage 7:** closest grasping-side evidence is reactive / margin-based (e.g. a fixed 20 % safety margin
  giving 9–30 % excess force in `khamis2021real`; a tactile safety-margin CNN in `boonstra2024estimate`), none with a
  slip-rate guarantee; online calibration from partial / binary feedback exists in other robotics settings
  (`lekeufack2024conformal`, `zhang2024bayesian`, `ge2024stochastic`, `zhao2024conformalized`).
- **Decision:** PROCEED → stage 7 SYNTHESIS.

## Stage 7. SYNTHESIS     [v1]

- **Finished:** 2026-11-08T09:45Z (run 37). Plan: `plans/stage_07_synthesis.md`.
- **Outputs produced:** `docs/06_synthesis.md` — 7 clusters (reactive slip control; force selection by estimation;
  guarantees / risk in grasping; offline conformal / risk control; online conformal under shift and partial feedback;
  conformal in robotics; tactile simulation & human grip), 6 falsifiable gaps, ranked opportunities. Key observation:
  with a monotone slip threshold the ACI miscoverage indicator equals the observed slip event, so online calibration
  needs no F\* label at deployment. Targeted WebSearch (2 queries) found no conformal grip-force / slip-rate work.
- **Decision:** PROCEED → stage 8 HYPOTHESIS_GEN (fresh-context proposer / skeptic / methodologist subagents).
