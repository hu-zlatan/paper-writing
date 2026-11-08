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

- **Started / Finished:** 2026-11-08T07:55Z / 08:02Z (scheduled run 37, after paper 1's time-critical work)
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

- **Finished:** 2026-11-08T08:05Z (run 37). Plan: `plans/stage_03_search_strategy.md`.
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

- **Finished:** 2026-11-08T08:17Z (run 37). Plan: `plans/stage_05_literature_screen.md`.
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

- **Finished:** 2026-11-08T08:19Z (run 37). Plan: `plans/stage_06_knowledge_extract.md`.
- **Outputs produced:** `docs/05_knowledge_cards.json` (52 cards, abstracts only), `code/literature/build_cards_v1.py`.
  Extraction by a fresh Sonnet subagent with the stage template; the session checked keys (52/52, none extra) and that
  every number in findings / data / metrics occurs in the source abstract (0 violations).
- **Notes for stage 7:** closest grasping-side evidence is reactive / margin-based (e.g. a fixed 20 % safety margin
  giving 9–30 % excess force in `khamis2021real`; a tactile safety-margin CNN in `boonstra2024estimate`), none with a
  slip-rate guarantee; online calibration from partial / binary feedback exists in other robotics settings
  (`lekeufack2024conformal`, `zhang2024bayesian`, `ge2024stochastic`, `zhao2024conformalized`).
- **Decision:** PROCEED → stage 7 SYNTHESIS.

## Stage 7. SYNTHESIS     [v1]

- **Finished:** 2026-11-08T08:21Z (run 37). Plan: `plans/stage_07_synthesis.md`.
- **Outputs produced:** `docs/06_synthesis.md` — 7 clusters (reactive slip control; force selection by estimation;
  guarantees / risk in grasping; offline conformal / risk control; online conformal under shift and partial feedback;
  conformal in robotics; tactile simulation & human grip), 6 falsifiable gaps, ranked opportunities. Key observation:
  with a monotone slip threshold the ACI miscoverage indicator equals the observed slip event, so online calibration
  needs no F\* label at deployment. Targeted WebSearch (2 queries) found no conformal grip-force / slip-rate work.
- **Decision:** PROCEED → stage 8 HYPOTHESIS_GEN (fresh-context proposer / skeptic / methodologist subagents).

- **Timestamp correction (run 37):** the stage 2, 3, 5, 6 and 7 entries above first carried estimated finish times
  (08:25–09:45Z) that were wrong; they now show the commit times from `git log`.

## Stage 8. HYPOTHESIS_GEN     [v1]

- **Finished:** 2026-11-08T08:40Z (run 37). Plan: `plans/stage_08_hypothesis_gen.md`.
- **Method:** three-pass debate, each pass a fresh Opus subagent with only the input files (AUTOPILOT §3).
- **Outputs produced:** `docs/07a_proposer.md`, `docs/07b_skeptic.md`, `docs/07_hypotheses.md` (canonical).
- **Core hypotheses (pre-registration targets, nothing run yet):**
  - **H1 validity** — gate: slip non-monotone in force in ≤ 7 of 800 pilot instances (upper limit ≤ 2 %), else the
    non-monotone risk-control fallback; then a physical replay audit at the chosen forces: (real − label-predicted)
    slip-rate gap upper limit ≤ 0.02 at α = 0.10.
  - **H2 efficiency (primary endpoint)** — D = 1 − RE(CertGrip) / RE(COMP) at α = 0.10, COMP = the better (on a
    held-out selection split, frozen before test) of a Mondrian safety factor (per family × disturbance, true family
    given) and a no-touch learned conformal predictor; confirmed if D ≥ 0.10 with lower limit > 0, robust to the label
    bracket end; negative result if the CI lies within ±0.10.
  - **H3 online** — quantile tracking q ← q + η(slip − α) from binary slip feedback; excess ratio vs an oracle
    recalibrated on 500 labelled shifted grasps upper limit < 1.10 and slip-rate gap ≤ 0.02 under S1 friction ×0.6,
    S2 new family, S3 disturbance ×1.5. Each core test at one-sided 0.0167.
- **Limitation recorded:** offline calibration needs F\* labels, available only in simulation; the online tracker is the
  deployable route on hardware.
- **Decision:** PROCEED → stage 8.5 THEORETICAL_BOUNDS, then stage 9 (pilot items in `07_hypotheses.md` §8 settle
  before the pre-registration freeze).

## Stage 8.5. THEORETICAL_BOUNDS     [v1]

- **Finished:** 2026-11-08T08:40Z (run 37). Plan: `plans/stage_08_5_theoretical_bounds.md`.
- **Outputs produced:** `docs/07b_theoretical_bounds.md` — standard results restated with premises (no new theory):
  G1 offline coverage ≤ α of the label rule, physical slip ≤ α only under monotonicity; caveat that several instances
  per object break plain instance-level exchangeability (stage 9 must pick a clustered calibration rule); G2 online
  identity Σ(slip − α) = Δq/η and long-run bound on uncapped steps, any sequence, informal boundedness argument relying
  on the cap-rarity design condition. Complexity: ≈ 10 replays per label dominate; decision one tree-ensemble call.
- **Decision:** PROCEED → stage 9 EXPERIMENT_DESIGN [gate] — next run; the pilot items of `07_hypotheses.md` §8 are
  needed for the freeze.

## Stage 9. EXPERIMENT_DESIGN [GATE]     [v1]

- **Finished:** 2026-11-08T08:42Z (run 37). Plan: `plans/stage_09_experiment_design.md`.
- **Outputs produced:** `docs/08_experiment_plan.yaml` (objectives C1/C2 + secondary/exploratory; datasets: MuJoCo
  parallel-jaw, 4 families × 500 objects × 4 disturbances = 8,000 labelled instances, 4 shift pools; baselines CSF-1,
  Mondrian-CSF (privileged family ID), CertGrip-P, COMP = better of the two frozen on a selection split, RAW-Q/Qv/G,
  oracle ceiling, oracle recalibration; 10 proposed components each with an ablation; metric formulas; risks; budget).
- **GATE — auto-approved (AUTOPILOT §1).** Evidence: all 8 required keys; every proposed component (PM1–PM10) has a
  matching ablation (checked by script; 4 added at this stage, none needs extra simulation); every baseline has a tuning
  protocol (equal 30-config search for every learned input set); primary comparator is the stronger of two non-tactile
  conformal methods, one with privileged family ID; failure conditions are pre-stated as negative results. Reason: the
  design answers every skeptic point (07_hypotheses §9) and stays within ≈ 90 CPU-h on free runners.
  **Condition:** the approval covers the design only. Pilot-dependent constants (replay cost c, determinism, δ_t,
  F_max, η, power re-projection) are frozen in `docs/08b_preregistration.md` after the stage-10/12 pilot and before any
  non-pilot data.
- **Compute note:** ≈ 90 CPU-h (assumption c = 1 CPU-s per replay) exceeds `RESTRICTS.yaml` `budget_total_hours: 12`
  under a CPU-hour reading; as for paper 1, it is read as wall-clock on parallel free runners (≈ 5–6 h at 20 runners),
  recorded here and in OWNER_TODO; the downscale order applies if the pilot measures a higher c.
- **Decision:** PROCEED → stage 10 CODE_GENERATION (`papers/p2/code/`, with the pilot), next run.

## Stage 10. CODE_GENERATION     [v1] — increment 1 of 4 (in progress)

- **Time:** 2026-11-08T08:45Z (run 37). Plan: `plans/stage_10_code_generation.md`.
- **Outputs produced:** `code/certgrip/sim.py`, `code/pilot_smoke.py`, `code/requirements.txt` (mujoco 4.0.0),
  `results/pilot/pilot_smoke.json` (pilot smoke, not a paper result).
- **Pilot smoke (sandbox, 16 instances × 25-point force grid, seed 1):** median replay 0.008 s (p95 0.013 s) —
  ≈ 100× cheaper than the 1 CPU-s assumption, so the downscale order is not needed (runner-image timing still to do);
  0 / 16 instances non-monotone; replays bit-identical (same sandbox); `touch_grid` gives normal + 2 tangential
  channels (07_hypotheses §8 item 4: tangential available; preload normal sum = F0 per pad as expected).
- **Fixed before the look:** slip metric 2 mm tangential / 3° / contact loss (07_hypotheses assumption, unchanged).
- **Design deviation (logged in the plan):** D1/D2 hand motion applied as the exact inertial pseudo-force in the hand
  frame; no table phase.
- **Next:** increment 2 (features + `main.py label` with time_guard + runner timing / determinism via Actions).
