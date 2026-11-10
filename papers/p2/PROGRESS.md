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
- **Run 38 (2026-11-08, ≈ 14:00–15:20 UTC): increments 2, 3, 4a, 4b** (details in `plans/stage_10_code_generation.md`).
  - Code: `certgrip/data.py` (pools / object splits / paired shifts), `features.py`, `conformal.py` (q̂, Mondrian, OQT
    with anti-windup + UT4 books), `baselines.py` (CSF), `featsets.py` (fairness-table sets), `models.py` (HGB quantile,
    equal 30-config grouped-CV search, RAW-G), `main.py label / mono / timing`; tests UT1, UT2, UT4, UT7, UT9 + shapes:
    12 passed. Runner UT6 / timing job `experiments/p2_timing.json` dispatched (queued behind paper-1 follow-ups).
  - Replay cost in the sandbox ≈ 0.008 s (not 1 s): the whole simulation budget is ≈ 0.5 CPU-h; no downscale needed.
  - **Pilot (pilot pool only):** 0 / 140 non-monotone; 0 unavoidable in ID / S1 / S3 / F5 (max F\*_hi 33 N ≪ 100 N);
    0 preload slips. Cross-fitted conformal RE at α 0.10 (pilot scale): P 1.02, S 0.97, full 0.94, CSF-1 0.76,
    oracle 0.39; every non-oracle residual correlates ≈ −0.79 with log μ → **the squeeze probe gives touch almost no
    friction information.** Candidate fix tested behind a flag (default protocol unchanged): an incipient-slip
    ramp-down probe; its onset force recovers μ with corr 0.999 in simulation (a perfect detector, so too optimistic).
  - **Design decision (same run, after a fresh-context skeptic subagent review): option C** —
    `docs/08a_pilot_amendment.md`: ramp-down probe for every method, onset detected from pad readings with a noise
    model (primary σ 0.2 in log units; σ 0 only an upper bound), new comparator CSF-μ̂ and CSF-1 in COMP, H2 split into
    H2a (vs COMP) and H2b (vs CSF-μ̂, TOST), H4/D-μ/H3 premises re-stated, no slip-reference reset after the probe.
  - **Next (run 39+):** implement 08a (detector + noise, CSF-μ̂, tests), re-pilot on pilot objects 25–124 under the
    new protocol, then write and commit `docs/08b_preregistration.md` (freeze) before any main-pool data → stage 12.
- **Run 39 (2026-11-08, ≈ 20:00–21:40 UTC): increment 5 + re-pilot + freeze — stage 10 DONE.**
  - 5a/5b: amendment 08a implemented (protocol `"rd"`: ramp-down probe with a touch-only incipient-slip detector,
    taxel noise, onset feature with σ, CSF-μ̂; tests 18 / 18). Detector constants tuned on pilot objects 0–24 only;
    a first re-pilot attempt (objects 25–124, older constants) failed UT8 on probe slips and was set aside unused
    (`results/pilot/rd_attempt1/`); full log in `docs/08a_pilot_amendment.md`.
  - 5c: re-pilot on fresh pilot objects 125–224 (`results/pilot/rd/`): 0 / 140 non-monotone, unavoidable ≤ 1 / 1,600
    per pool, S1 shift Δlog F\* 0.509 (Coulomb 0.511). 12 predictor arms (equal 30-config search) on Actions run
    42519521710, reproduced in the sandbox to 1e-15. Read-out `results/pilot/rd/pilot_analysis_rd.json`: RE at α 0.10
    CSF-1 0.80, P 0.89, S+squeeze 0.90, CertGrip-full (σ 0.2) 0.46, onset-only 0.45, CSF-μ̂ 0.43, oracle 0.16.
    So the friction probe carries the gain; static / squeeze touch add nothing; the learned model does not beat the
    physics plug-in with the same onset estimate (pilot).
  - **Freeze:** `docs/08b_preregistration.md` FROZEN (four core decisions at 0.0125: H1, H2a vs COMP, H2b vs CSF-μ̂,
    H3). Pilot power rules applied: 50 train objects per family moved to test (H2b SE 0.037 > 0.035); H3 oracle share
    175 objects (S2 pool 550 objects) and H3 pre-registered with reduced power (projected half-width ≈ 0.12).
  - Next: stage 11 RESOURCE_PLANNING (`docs/09_schedule.json`), then stage 12 main-pool labels on Actions.

## Stage 11. RESOURCE_PLANNING     [v1]
- **Finished:** 2026-11-08 (run 39). Plan `plans/stage_11_resource_planning.md`; output `docs/09_schedule.json`.
- 1-condition pilot: TIME_ESTIMATE 0.124 s per label instance (sandbox); whole plan ≈ 350 CPU-min, CPU only; the
  label set runs in the sandbox because paper 1 holds the Actions queue for ≈ 10 h. **Decision:** PROCEED → 12.

## Stage 12. EXPERIMENT_RUN     [v1] — in progress
- **Run 39, increment 1 (labels):** 18,600 main-pool labels under protocol `"rd"` (`code/run_labels_v1.sh`,
  `results/v1/labels/`): id 8,000 (train 2,400 / select 800 / cal 2,000 / test 2,800), S1 / S1m / S3 2,800 each on the
  id test objects, s2 2,200 (oracle 700 / stream 1,500). UT8: unavoidable 2 / 8,000 (id), 6 / 2,800 (S1, 0.21 %),
  1 (S1m), 1 (S3), 2 / 2,200 (S2) — all ≤ 1 %. Preload slips 0. No predictor fitted, no cal / test statistic read.
- **Run 39, increment 2 — H1-M design gate (`code/run_h1m_v1.sh`, `analysis_h1m.py` → `results/v1/h1m_analysis.json`):
  FAILS.** 8 / 800 id instances non-monotone (pre-registered pass: ≤ 7; Clopper–Pearson 98.75 % upper limit 2.11 % >
  2 %). By family F1 3, F2 2, F3 2, F4 1; by disturbance D2 (shake) 7, D1 1. Every violation is a single slip outcome
  at most 0.9 % above F\*_hi (just above the first no-slip force); shift pools (descriptive): S1 0 / 100, S3 1 / 100,
  S2 1 / 100. The pilot had 0 / 140, which only bounded the rate at ≈ 2 %.
  **Pre-registered consequence (07_hypotheses H1-M failure condition, unchanged by 08a/08b):** reported as a negative
  finding ("slip is not monotone in force in this simulator at rate ≈ 1 %, as narrow flickers just above F\*, mostly
  under shaking"), and the primary validity route switches to conformal risk control on the binary loss
  1{slip(F)} (non-monotone form, 20-point λ-grid per calibration instance). No family exceeds the 5 % flag.
- **Next (run 40):** implement the CRC route (λ-grid replays on the cal and test instances, ≈ 2,000 × 20 + audits) and
  write the analysis code (`docs/08c_analysis_plan.md`: COMP selection, seeds, bootstrap) before fitting / reading
  any cal or test result; then `main.py fit` per arm × seed.
- **Run 39, later:** addendum `docs/08c_analysis_plan.md` committed before any predictor / cal / test statistic
  (H1 not confirmed; CRC route with a 20-point λ-grid built on the selection split, monotonised binary loss, per-stratum
  CRC; seed 0 primary; COMP selection by even/odd halves of the selection split; 2,000-draw object bootstrap, 97.5 %).
  Offline fits dispatched: `experiments/p2_fit_a010.json` (12 arms × 5 seeds, Actions run 185).
  **Where to resume (run 40):** fits landed → COMP selection script + commit → λ-grids + CRC replay command
  (`main.py crc`, cal + test × 20 λ for the §4 arms) → manifest → analysis script with a synthetic test → read-out.
- **Run 40 (2026-11-09, from ≈ 02:00 UTC): 08c §5 steps 2–3.**
  - Fits (Actions run 185, 12 arms × 5 seeds) all landed: `results/v1/preds/` (60 files, keys_sha256 matches the labels).
  - **COMP selection** (`code/comp_selection.py`, test `tests/test_comp_selection.py`; selection split only, even/odd
    object halves, label rule, α 0.10) → `results/v1/comp_selection.json`: CSF-1 RE 0.769, Mondrian-CSF 0.829,
    CertGrip-P 0.834 → **COMP = CSF-1** (committed in 04c6343 before any cal / test statistic). The learned no-touch
    model does not beat the one-parameter formula on the selection split. (08b §3 still says "objects 200–249" for the
    selection split — stale text from before the pilot power rule moved the split; `split_of` and 08c use 150–199.)
  - **λ-grids** (`code/crc_grids.py` → `results/v1/crc_grids.json`; selection split only): 14 arms — CertGrip-full seed 0
    at σ 0 / 0.1 / 0.2 / 0.4, seeds 1–4 at σ 0.2 (decision made now: per-seed D under the CRC route too, so the 08c §3
    secondary uses the same route as the primary), CSF-1 (COMP), CSF-μ̂ at the four σ, onset-only σ 0.2. q_sel ≈ 0.01–0.04
    for the learned onset arms, 0.82 for CSF-1, 0.96–1.19 for CSF-μ̂.
  - **`main.py crc`** (new command; sim / features / conformal code unchanged): protocol rd, 20 grid forces per arm,
    identical forces replayed once; ≈ 3.6 s per instance in the sandbox; two identical smoke runs bit-identical (one
    smoke shard printed the slip pattern of 4 calibration instances of F2 obj 200 — a code check, no statistic).
    Manifest `experiments/p2_crc_v1.json` (60 jobs, 4,800 cal + test instances, ≈ 4.8 CPU-h) dispatched.
  - **Next:** CRC analysis script (`analysis_crc.py`: per-stratum λ̂, RE, physical slip, D(H2a)/D(H2b), object-cluster
    bootstrap 2,000 draws with λ̂ recomputed) + synthetic test, committed **before** reading the replay files; then the
    read-out; then H1-V, H3 stream (OQT), H4 diagnostics.
  - **(later, run 40) H3 streams.** Addendum `docs/08d_h3_stream_plan.md` committed before any stream quantity
    (per-stratum trackers initialised at the offline q̂, η = 0.1 × IQR of CertGrip's pooled ID cal scores = 0.0341,
    label-rule feedback for the 20 orderings and the regenerated-ordering bootstrap, two ordering-0 direct-replay
    audits: the pre-registered steps 501–1,000 and, added for 08c §3, the whole window for OQT vs Oracle). One wording
    error in 08d (unavoidable steps) corrected before any result. Code `code/h3_streams.py` + tests (3 passed),
    `main.py replay`; 10,000 audit replays in the sandbox (≈ 0.015 s each). A 40-draw timing smoke of the committed
    read-out printed the point R_E values before the full run (same script; the 2,000-draw run below is the result).
  - **H3 read-out** (`results/v1/h3_analysis.json`, 2,000 draws, CI\*\* 97.5 %): R_E = OQT / Oracle window RE —
    S1 0.878 [0.740, 1.120], S2 1.174 [1.023, 1.428], S3 0.963 [0.836, 1.145] → **all three inconclusive** (none has
    upper < 1.10, none lower > 1.10); H3 not confirmed — the reduced-power outcome 08b §5 stated in advance.
    The matched-rate co-requirement (physical window slip, ordering 0) **fails for S1 (+0.032) and S2 (−0.035)**,
    holds for S3 (+0.009): the 175-object oracle q̂ is itself off α in the window (label slip S1 7.5 %, S2 13.5 %),
    while OQT sits at 10.0–10.2 % on every shift. So the excess ratios on S1 / S2 are unmatched and reported only
    next to the slip rates. Frozen CertGrip breaks under S1 (30.6 %) and S3 (24.6 %), not under S2 / S1m; decaying-step
    OQT does not recover under S1 / S3 (20.2 % / 18.1 %). Physical vs label disagreement Δ in all 14 audits between
    −0.8 % and 0 (physical slip never above the label rule; CI\*\* upper ≤ 0). H3-L: ρ_s − ρ_ID S1 +0.086
    [−0.044, 0.186] (TOST ±0.05 not met → not confirmed), S2 +0.064, S3 +0.082, S1m −0.019.
  - **CRC replays** (Actions, 60 jobs) still landing; `analysis_crc.py --check` gates the H2 read-out.
  - **H1-V (secondary after the H1-M failure; `code/h1v.py` committed before running; 11,200 direct replays in the
    sandbox → `results/v1/h1v/`, read-out `results/v1/h1v_analysis.json`):** label-rule split conformal per stratum
    (cal n = 500) on the 2,800 id test instances. Δ = mean(slip_direct − slip_label): CertGrip α 0.10 −0.0043
    [−0.0075, −0.0014], α 0.05 −0.0014 [−0.0039, 0.0007]; CSF-1 α 0.10 −0.0032, α 0.05 −0.0029 → all **pass**
    (CI\*\* upper ≤ 0.02). Physical slip is at or below the label rule; the H1-M flickers do not raise the physical
    rate at the conformal force. H1 stays "not confirmed" (H1-M failed); H1-V is reported as the transfer check.
  - **H2 read-out, CRC route (primary, `code/analysis_crc.py` committed before the replays were read;
    `results/v1/crc_analysis.json`, 4,800 instances × 14 arms × 20 λ, 2,000 draws, CI\*\* 97.5 %):**
    RE at λ̂: CertGrip-full σ 0.2 0.457 (phys. slip 8.3 %), CSF-1 (COMP) 0.783 (10.2 %), CSF-μ̂ σ 0.2 0.484 (6.6 %),
    onset-only 0.434 (8.6 %). **H2a: D = 0.417 [0.348, 0.478], F\*_lo / F\*_hi 0.415 / 0.419 → superiority (confirmed).**
    **H2b: D = 0.057 [−0.040, 0.145] → not confirmed** (neither superiority nor TOST equivalence). H4e (vs onset-only)
    −0.053 [−0.123, 0.051]. Per seed: H2a 0.39–0.45, all superiority; H2b 0.02–0.11, all not confirmed. σ\* = 0.4
    (H2a lower limit 0.083 < 0.10 at σ 0.4; D 0.68 / 0.58 / 0.42 / 0.14 at σ 0 / 0.1 / 0.2 / 0.4).
  - **Defect found in the 08c λ-grid (reported, not hidden):** the grid is centred on the *pooled* selection q̂ ± 0.4,
    and for the physics plug-ins the D1 / D2 strata need λ below the grid: λ̂ sits on the lowest grid point for CSF-μ̂ at
    σ 0 / 0.1 / 0.2 in D1 and D2 (index 0) and one step above it for CSF-1. A floor-bound λ̂ over-protects (CSF-μ̂ σ 0
    physical slip 2.7 % vs α 10 %) and inflates the comparator's RE, so the CRC-route D(H2b) is biased **in CertGrip's
    favour** (CSF-1 in H2a is affected much less: index 1, not the floor). The H2b-σ "superiority" at σ 0 / 0.1 on the
    CRC route is this artifact.
  - **Label-rule route (08c §3 secondary, no grid; `code/h2_label_rule.py` → `results/v1/h2_label_rule.json`):**
    H2a D = 0.429 [0.365, 0.482] → superiority (agrees); **H2b D = 0.013 [−0.085, 0.081] → equivalence**;
    H4e −0.042 [−0.099, 0.013] → equivalence; H2b at σ 0 −0.202 and σ 0.1 −0.075 → **inferiority** (the physics
    plug-in with a good onset estimate beats the learned model). Since H1-V passes (physical ≤ label rule), the
    label-rule route is a valid, conservative read here. Honest summary so far: touch-with-probe beats the best
    no-touch conformal method by ≈ 42 % force (H2a, robust to route), but the learned model adds nothing over a physics
    plug-in that uses the same friction-onset estimate (H2b equivalent on the label route; CRC route biased by the grid).
  - **Next:** addendum 08e (post hoc, decided before its outcome): per-stratum-centred, wider λ-grid CRC replays for the
    plug-in and onset arms as a sensitivity check of H2b; then stage 13/14 (H4 diagnostics, D-μ, H2-T, H3-B).
  - **Where to resume (run 41):** `p2_crc_v2` (60 jobs, dispatched ≈ 02:30 UTC) → `python analysis_crc.py --v2 --check`,
    then `--v2` read-out → report per 08e's reporting rule. Then the remaining secondaries (H4a steps, H4c shuffle fits,
    D-μ, H2-T tail, H2-M no-mass, H3-B location prediction, UT3) and stage 13/14 for paper 2.

- **Run 41 (2026-11-09, from ≈ 07:50 UTC, scheduled).** No open issues; AUTOPILOT §1 unchanged. `add_repo` not available
  as a tool; the existing checkout was reset onto origin/main. `p2_crc_v2` (Actions run 190, 60 jobs) `success`.
  - **08e sensitivity read-out** (`python code/analysis_crc.py --v2 --check` → 4,800 / 4,800 instances, 0 duplicates;
    then `--v2` → `results/v1/crc_analysis_v2.json`, 2,000 draws, CI\*\* 97.5 %). **No floor- or ceiling-bound λ̂**:
    every arm × stratum selects grid index 20–22 of 0–40, so the 08c defect is removed.
    RE at λ̂: CertGrip σ 0.2 0.444 (phys. slip 9.0 %), CSF-1 0.778 (10.0 %), CSF-μ̂ σ 0.2 0.455 (7.5 %), onset-only 0.435.
    **H2a D = 0.429 [0.358, 0.477] → superiority** (same decision as 08c and the label route).
    **H2b D = 0.024 [−0.095, 0.100] → not confirmed** (same decision as 08c; the label route said equivalence).
    H4e −0.022 [−0.121, 0.037] not confirmed. σ curve, H2b: σ 0 −0.152 [−0.303, −0.060] **inferiority**;
    σ 0.1 −0.102 [−0.191, 0.022] not confirmed; σ 0.4 +0.332 [0.234, 0.406] superiority. H2a: σ 0 / 0.1 / 0.2 / 0.4
    = 0.692 / 0.587 / 0.429 / 0.161, all superiority.
  - **Per the 08e reporting rule:** the sensitivity changes the 08c CRC decisions for H2b at σ 0 and σ 0.1 (08c:
    "superiority", now inferiority / not confirmed) → those two pre-registered CRC results are reported as unreliable
    because of the grid defect. No decision is upgraded. Honest reading: the learned model is worse than the physics
    plug-in when the onset estimate is clean (σ ≤ 0.1), indistinguishable at the pre-registered σ 0.2, and better only
    at the heaviest noise σ 0.4 (σ\* = 0.4 is where H2a itself is weakest, 0.16).
  - **Next:** the remaining secondaries (H4a steps, H4c shuffle fits, D-μ, H2-T tail, H2-M no-mass, H3-B location
    prediction, UT3) → stage 13 freeze note → stage 14 RESULT_ANALYSIS.
  - **H4a steps (secondary; `code/h4a_label_rule.py` committed before it was run; label-rule route, 2,000 draws,
    CI\*\* 97.5 %, seed-0 predictors; `results/v1/h4a_label_rule.json`):** RE P 0.783, S 0.790, S+squeeze (full) 0.810,
    +onset (full_rd σ 0.2) 0.426. S vs P D = −0.008 [−0.036, 0.013] → **equivalence** (±0.05): static touch adds nothing;
    full vs S D = −0.026 [−0.056, 0.015] → **not confirmed** (±0.03): the squeeze probe adds nothing (the pilot
    expectation stated in 08b §6), so the registered "probe-specific claim" is dropped for the squeeze; +onset D = 0.474
    [0.415, 0.523] (no registered margin, reported only). Consistent with H2b: the gain comes from the ramp-down onset
    estimate, not from static / squeeze touch features.
  - **Still to do (paper 2 secondaries):** H4c shuffled-touch fits, D-μ, H2-T tail, H2-M no-mass fits, H3-B location
    prediction, UT3 (new fits → Actions manifest), then stage 13 freeze note → stage 14.

- **Run 42 (2026-11-09, from ≈ 13:52 UTC, scheduled).** No open issues; AUTOPILOT §1 unchanged (paper 1 still waits for
  the owner's stage-20 choice). `add_repo` not available as a tool; the existing checkout was reset onto origin/main.
  - **Addendum `docs/08f_secondaries_batch.md`** (committed before any of these quantities were computed) fixes the
    operational details 07 §4 / 08b §6 left open for H2-T, H4c, H2-M (no-mass only; mass-noise not run), H3-B, D-μ, UT3.
    Code `code/secondaries_08f.py`, feature set `full_rd_shuf` (+ `tests/test_shuffle.py`; tests 27 / 27 pass), committed
    before running. All results below are secondary; CI\*\* 97.5 %, 2,000 object-cluster draws unless stated.
  - **H2-T** (`results/v1/sec08f_tail.json`): T = P95 RE(CertGrip-full σ 0.2) / P95 RE(CSF-1) — CRC 08c (primary route)
    0.592 [0.554, 0.656], CRC 08e 0.602 [0.549, 0.649], label 0.601 [0.552, 0.646] → **pass** on every route (upper
    < 1.10). P95 RE 1.17 vs 1.98: the mean gain does not come with a worse tail.
  - **H3-B** (`results/v1/sec08f_h3b.json`): for the no-onset arms (P, S, full, CSF-1) the location model predicts the
    frozen offline slip rate within 0.004 on S1 (p_obs 0.50–0.52) and S1m (0.18–0.19); all CI\*\* inside ±0.02 →
    **pass** (S1 is a pure location shift for these arms). The onset arm full_rd σ 0.2 is far below the location
    prediction (S1 p_obs 0.304 vs 0.782; S1m 0.125 vs 0.213) — the onset probe partially tracks the friction change
    (not tested: 08b never specified its prediction). S3 p_obs 0.19–0.25 (up, as predicted). S2: no arm breaks
    (p_obs 0.094–0.096, CI\*\* within ±0.05 of α).
  - **D-μ** (`results/v1/sec08f_dmu.json`, 500-draw 95 % intervals): CV R² of log μ → each arm's residual — P 0.794,
    S 0.788, full 0.779, CSF-1 0.603 (the friction variation stays in the residual of every no-onset arm: static and
    squeeze touch do not see friction, which is the premise 07 / 08b state for no-probe arms; 08b measures it on the
    residual, so the 07 "R² ≤ 0.05 of touch features" threshold is not on this scale and is not applied);
    full_rd σ 0 / 0.1 / 0.2 / 0.4 = 0.011 / 0.045 / 0.214 / 0.566; onset-only σ 0.2 0.197; CSF-μ̂ 0.003–0.006 at every σ;
    oracle 0.016. At σ ≥ 0.2 the learned onset arm leaves more friction in its residual than the physics plug-in
    (it shrinks the noisy estimate), consistent with H2b.
  - **UT3** (`results/v1/sec08f_ut3.json`, 1,000 re-splits, K = 160 cells, z 3.60): **160 / 160 pass**; worst cell
    CSF-1 D3 α 0.01 n 500 (mean miss 0.0103, band [0.0073, 0.0107]). Re-split SD of miss ≤ 0.025 (n 500), ≤ 0.059
    (n 50). The label-rule pipeline is correct.
  - **Fits** (sandbox, `OMP_NUM_THREADS=1`; two parallel processes with the default threads were ≈ 10× slower from
    over-subscription and were restarted): `a010_full_rd_shuf_s0.2_seed0`, `a010_P_nomass_seed0`,
    `a010_full_rd_nomass_s0.2_seed0`. Reproducibility check: refitting `a010_P_seed0` with one thread reproduced the
    committed Actions predictions exactly (max |Δ| 0, same config, same CV pinball).
  - **H4c** (`results/v1/sec08f_label.json`, label route): RE shuffled 0.803 vs P 0.783, D = −0.025 [−0.053, +0.009] →
    **inconclusive** (lower limit 0.003 outside the ±0.05 equivalence band); the failure condition (shuffled beats P by
    > 5 %) is clearly not met — no capacity / tuning artefact; permuted touch + onset features are at best useless.
  - **H2-M, no mass** (COMP re-selected = CertGrip-P no mass, the only non-tactile candidate without mass): RE P 0.792,
    CertGrip-full 0.428; D_nm = 0.460 [0.397, 0.506] vs with mass (label route, same draws) 0.456 [0.402, 0.507];
    change +0.004 [−0.045, +0.040]. Removing the mass feature changes nothing for the learned arms. Mass-noise not run.
  - **Gap found (honest record):** 07 §4 also pre-registered H1c, H2-C, H2-n, H2-H, H2-R, H3-S, H4b, H4d and the
    diagnostics D-FID, D-loc and the oracle decomposition; none had been run, and earlier "still to do" lists omitted
    them. Part 1 below (addendum `docs/08g_secondaries_batch2.md` + `code/secondaries_08g.py`, both committed before
    running; label route, 2,000 draws; `results/v1/sec08g.json`):
  - **H2-C** vs Mondrian-CSF (family-ID-privileged cells): D = 0.438 [0.373, 0.487] → superiority.
  - **H2-n** (n = 50 cal per stratum): α 0.10 D 0.415 [0.259, 0.548], α 0.20 0.465 [0.279, 0.598] → confirmed (lower > 0).
  - **H2-H** (16 family × disturbance cells, DerSimonian–Laird): pooled D 0.439 [0.404, 0.474], τ 0.051; cell D
    0.30 (F1 D3) – 0.53 (F2 D2), every cell CI\*\* lower ≥ 0.16 → guard **pass** (no cell worse). D3 (external
    disturbance) cells are the weakest in every family.
  - **H2-R (design-range dependence) — important negative:** in the nested sub-pool μ ∈ [0.5, 0.8] × middle-50 %
    amplitude (352 cal / 548 test instances, q̂ recalibrated inside) **D = −0.261 [−0.532, −0.032]: CertGrip uses more
    force than CSF-1.** When friction varies little and sits near the formula's μ̄ (0.548), the noisy onset estimate
    costs more than it gains; the 42 % H2a gain is a property of the wide μ range [0.3, 1.0]. The paper must state this.
  - **H4d** (CoM mechanism, D_F4 − D_F1 of touch vs P): CertGrip-full 0.034 [−0.042, 0.114], squeeze-only `full`
    0.002 [−0.017, 0.021] → both inconclusive (pressure-centroid / CoM story not supported; squeeze touch is ≈ P in
    every family, D_F −0.02 to −0.06).
  - **Oracle decomposition:** RE CSF-1 0.747, CertGrip 0.426, oracle 0.127 → CertGrip closes 51.7 % [44.9, 57.6] of the
    CSF-1 → oracle gap.
  - **D-loc:** S1 is a pure location shift in F\* (mean Δlog F\* 0.509, SD 0.009, 2,794 pairs; Coulomb 0.511, 0). Under
    S1 the predictions of P / S / full move by < 0.2 % (touch does not see the friction change), CertGrip's by 44.7 %
    (the onset probe follows ≈ 2/3 of the e^0.51 − 1 = 67 % change). Preload-slip rate 0 in every pool.
  - **Last batch: addendum `docs/08h_secondaries_batch3.md`** (before any fit), code (`_fid` / `_mn` feature sets,
    `touch_only`, `main.py fitg`, `secondaries_08h.py`; tests 28 / 28) committed before running. 8 new seed-0 fits on
    the id train objects in the sandbox (`OMP_NUM_THREADS=1`): `a001/a005/a020_full_rd_s0.2`, `g_full_rd_s0.2` (RAW-G,
    config of the α 0.10 search), `a010_P_fid`, `a010_full_rd_fid_s0.2`, `a010_P_mn`, `a010_full_rd_mn_s0.2`.
  - **H1c** (`results/v1/sec08h_h1c.json`, label slip of uncalibrated targeters on id test, CI\*\* of slip − α):
    RAW-Q 3.4 / 8.3 / 13.3 / 23.5 % at α 1 / 5 / 10 / 20 %; RAW-G 2.0 / 7.9 / 14.9 / 25.1 %; RAW-Qv (log-shift variant,
    deviation stated in 08h) 1.3 / 6.6 / 11.3 / 24.0 %. RAW-Q and RAW-G under-cover at every α (CI\*\* lower > 0), but at
    α 0.05 their CI\*\* (RAW-Q [+0.020, +0.045], RAW-G [+0.016, +0.042]) does not exclude ±0.025 → the registered
    "miss by ≥ 0.5α" prediction is **not confirmed**; the failure condition (all inside ±0.25α) is not met either. RAW-Qv
    is indistinguishable from α everywhere (CI\*\* includes 0). Honest read: in distribution, a validation-tuned
    quantile is roughly enough; the uncalibrated learners miss by 1.3–3.4× at α 0.01 and by about +3 points elsewhere.
  - **H3-S** (`results/v1/sec08h_h3s.json`, 20 orderings, 2,000 draws): extra slips Σ(slip − α) over shifted steps
    1–500, constant vs decaying η — S1 19.3 vs 77.5, ΔC 58.2 [48.2, 70.2]; S3 18.6 vs 61.0, ΔC 42.4 [32.4, 49.4] →
    **confirmed**; S2 ΔC 2.9 [−6.7, 7.0], S1m 2.8 [−2.1, 11.9] → inconclusive (small shifts).
  - **H4b** (`results/v1/sec08h_h4b.json`): with family ID given to both arms D_FID = 0.464 [0.394, 0.514] vs D = 0.456
    [0.393, 0.513]; D_FID − 0.5 D = 0.236 [0.196, 0.261] → **confirmed**: the touch gain is not a family identifier.
  - **D-FID** (`results/v1/sec08h_dfid.json`): touch-only features identify the family with accuracy 0.726 [0.701,
    0.751] (chance 0.25; + onset 0.730) — touch does carry family information, but H4b shows the gain does not come
    from it.
  - **H2-M mass-noise** (`results/v1/sec08h_massnoise.json`): COMP re-selected on the selection split = CSF-1 (noisy
    mass; RE 0.761 vs Mondrian 0.897, P 0.892). RE CertGrip-mn 0.431 vs CSF-1-mn 0.799: D_mn 0.460 [0.411, 0.505] vs
    noise-free D(H2a, label) 0.429 [0.373, 0.482]; change +0.031 [−0.008, +0.071]. 10 % mass noise hurts the formula
    more than the learner.
  - **All 07 §4 secondaries and diagnostics have now been run** (H2-M fully, both conditions).
  - **Where to resume (run 43):** stage 13 freeze note for p2 v1 (all result files, sha256) → stage 14 RESULT_ANALYSIS
    (fresh subagent, template verbatim) → stage 15 decision. Writing (stage 16) must start by ≈ 11-16 for the 12-04 RSS
    Stage 1 deadline.

## Stage 13. ITERATIVE_REFINE     [v1]

- **Finished:** 2026-11-09 (run 42). Plan `plans/stage_13_iterative_refine.md`, template `iterative_refine.md`.
  13a: numpy-2 check 0 errors, tests 28 / 28; 13b: 0 / 194 run logs with NaN / Inf / RuntimeWarning / overflow → no
  repair needed; 13c (improve) deliberately not used — the study is pre-registered, so weak or negative registered
  outcomes are results, not things to tune away. Freeze: `results/v1/13_freeze.json` (sha256 of every result file).
- **Next:** stage 14 RESULT_ANALYSIS (fresh subagent, `result_analysis.md` verbatim) → `results/14_analysis.md`.

## Stage 14. RESULT_ANALYSIS     [v1]

- **Finished:** 2026-11-09 (run 42). Plan `plans/stage_14_result_analysis.md`; template `result_analysis.md` verbatim
  (`docs/prompts/build_stage14.py` → `stage14_{system,user}.txt`, every analysis JSON unaltered + 08a–08h).
  Pass 1: fresh opus subagent → `results/14_analysis_pass1.md`. Pass 2 (template's area-chair prompt verbatim): fresh
  opus subagent re-checked every number against the JSON → `results/14_analysis_pass2.md`, 23 findings, no
  fabrication. Merged `results/14_analysis.md` (audit binding). Main-session adjudication: 22 accepted; "H3-L not run"
  rejected in part (it is in `h3_analysis.json`: S1 ρ−ρ_ID +0.0857 [−0.0444, 0.1859] → not confirmed).
- Corrections to this file's run-42 notes, adopted from the audit: UT3's 160 / 160 includes 20 degenerate cells
  (α 0.01, n 50: q̂ = ∞, miss 0) → 140 informative cells, all pass; H2-M (no mass / mass noise) is descriptive only
  and must not be used for the friction story (08a / 08b); H1c is "not confirmed"; H2-T is a secondary.

## Stage 15. RESEARCH_DECISION     [v1]

- **Finished:** 2026-11-09 (run 42). Plan `plans/stage_15_research_decision.md`, template `research_decision.md` +
  REFINE option → `results/15_decision.md`. **Decision: PROCEED**, re-scoped: the contribution is the friction-onset
  probe + conformal calibration (H2a D 0.4168 [0.3484, 0.4778], robust on every route / seed / cell), with the
  learned tactile model adding no demonstrated gain (H2b), H1-M failed, H3 inconclusive, and the H2-R scope limit
  (D −0.261 when μ varies little). All three PROCEED hard rules met; REFINE rejected (the weak results are
  pre-registered outcomes, not thin evidence); loops still owed via stages 18–20 / 25. Refine cycles used 0 / 3.
- **Next (run 43):** stage 16 PAPER_OUTLINE for the RSS 2027 Stage 1 extended abstract (≤ 5 pages + references).


## Stage 16. PAPER_OUTLINE     [v1]

- **Finished:** 2026-11-09 (run 43). Plan `plans/stage_16_paper_outline.md`; template `paper_outline.md` verbatim
  (`paper/mypaper/prompts/build_stage16.py` → `stage16_{system,user}.txt`), fresh opus subagent →
  `paper/mypaper/sections/00_outline.md` (≈ 4,200 words; 5-page extended-abstract targets ≈ 3,300 words body, a
  stated deviation from the 9-page floors).
- Pre-step: `code/tools_results_v1.py` → `results/v1/results_v1.json` (every v1 analysis JSON unchanged; grid dumps
  and freeze referenced only). New `code/tools_number_audit.py` (p2 copy of paper 1's audit, reads results_v1.json):
  outline 0 unmatched decimals.
- Working title "Probe, Then Certify: Minimal-Force Grasping with a Tactile Friction-Onset Probe and Conformal
  Slip-Risk Control"; H2a + mandatory H2-R scope limit in the abstract; H1 / H2b not confirmed, H3 inconclusive;
  Figure 1 plan (force timeline with probe, CRC curve, RE bars); 45 result rows mapped to JSON keys.
- **Next:** stage 17 PAPER_DRAFT (template `paper_draft.md`, fresh subagent) → `paper/mypaper/draft_v1.md`.

## Stage 17. PAPER_DRAFT     [v1]

- **Finished:** 2026-11-09 (run 43). Plan `plans/stage_17_paper_draft.md`; template `paper_draft.md` verbatim
  (`paper/mypaper/prompts/build_stage17.py` → `stage17_{system,user}.txt`, results_v1.json pasted in full, 52 cards),
  fresh opus subagent → `paper/mypaper/draft_v1.md` + `paper/mypaper/figures/figure1_prompt.txt`.
- ≈ 7,300 words (all sections above the RESTRICTS floors; condensed to 5 pages at stage 22). Number audit 0 unmatched;
  52 / 52 cite keys in cards. The one [NEED] (GBDT search space) filled by the main session from
  `code/certgrip/models.py` (the code that ran). H2a, H2-R scope limit in abstract, H1 / H2b not confirmed, H3
  inconclusive, H2-M descriptive, post hoc analyses labelled, five deviations listed.
- **Next:** stage 18 PEER_REVIEW (two fresh subagents, evidence audit).

## Stage 18. PEER_REVIEW     [v1]

- **Finished:** 2026-11-09 (run 43). Plan `plans/stage_18_peer_review.md`; template verbatim
  (`paper/mypaper/prompts/build_stage18.py`); two fresh opus subagents. Scores run 1 A 4 / B 5, run 2 A 4 / B 5.
  **CRITICAL_FABRICATION: no** (43 + 31 spot-checks; H2a / H2b D recomputed from raw replays, exact).
- Merged record `paper/mypaper/18_peer_review.md`: 10 paper-level must-fix items (family description ≠ code, μ
  independence by construction, grid floor binds H2b at σ 0.2 too, compute 14.5 CPU-h not 2–3, online-study feedback
  is the label rule, H1-M max attribution, comparators, main-data detector quality, "certified" in expectation, C3
  scope) and 5 evidence-level items (PAC / LTT variant, friction-proxy baseline, σ grounding, reactive baseline,
  classic citations) for stage 20.
- Report-only rows: `code/tools_stage19_rows.py` → `results/v1/19_report_rows.json` (now in results_v1.json).
- **Next:** stage 19 PAPER_REVISION (template `paper_revision.md`, fresh subagent, length-protected).

## Stage 19. PAPER_REVISION     [v1] — pass 1

- **Finished:** 2026-11-09 (run 43). Plan `plans/stage_19_paper_revision.md`; snapshot before
  `paper/mypaper/v1/draft_v1_stage17.md`, after `v1/draft_v1_stage19pass1.md`. Template verbatim
  (`build_stage19.py`), fresh opus subagent, targeted edits for merged items 1–10; E1–E5 only as limitations.
- Words 7,333 → 9,639 (+31 %), no section shorter; number audit 0 unmatched; cite keys unchanged (52, all in cards).
- +31 % > 30 % → **second stage-18 pass** (template rule) before stage 20.

## Stage 18. PEER_REVIEW     [v1] — pass 2

- **Finished:** 2026-11-09 (run 43) on `v1/draft_v1_stage19pass1.md`; same template / evidence (prompt
  `stage18_pass2_user.txt`); two fresh opus subagents. Scores run 1 A 4 / B 5, run 2 A 4 / B 5 (mean 4.5).
  **CRITICAL_FABRICATION: no** (headline values recomputed from raw replays by an independent CRC loop, exact).
- Merged record `paper/mypaper/18_peer_review_pass2.md` (P1–P9): abstract names the wrong comparator for 0.4739 (vs
  *full*); undisclosed Holm deviation (07 → 08f–08h); 08a provenance of the probe arm; CRC precondition; realised
  slip; detector error structure; H4a is a simulator consistency check; online-study warm start; CI levels.
- New report-only rows (`19_report_rows.json`): detector error vs log μ r −0.253, F3 SD 0.196; static touch = F0 and
  m g / 2 (99th pct rel. dev. 3.1e-4), preload slip 0 / 8,000.
- **Next:** stage 19 pass 2 (`stage19_pass2_user.txt`), then stage 20.

## Stage 19. PAPER_REVISION     [v1] — pass 2

- **Finished:** 2026-11-09 (run 43). Prompt `stage19_pass2_user.txt` (`build_stage19.py --pass2`), fresh opus
  subagent, targeted edits for P1–P9 (+ F4 inertial description). Snapshot after `v1/draft_v1_stage19pass2.md`.
- Abstract 345 → 250 (reviewer request); all other sections no shorter; total ≈ 11,600 words (master draft; the
  5-page condensation is stage 22). Number audit 0 unmatched; no new citations. Deviations list now 8 items (Holm
  dropped; 08a provenance; frontier not produced).
- **Next:** stage 20 QUALITY_GATE.

## Stage 20. QUALITY_GATE     [v1]

- **Finished:** 2026-11-09 (run 43). Plan `plans/stage_20_quality_gate.md`; template verbatim (threshold 7.5), fresh
  opus subagent, paper only → `paper/mypaper/20_quality_gate.json`.
- **Score 6.5 / 10 → FAIL; not auto-approved** (below threshold). 11 required actions: 8 paper-level (risk–efficiency
  frontier and a high-probability certificate from existing replays, CSF-μ̂ / onset-only vs CSF-1 contrasts,
  descriptive names instead of document codes, a label-route H2b row wording error, classic related work, Figure 1
  from data, exploratory stratifications) and 3 evidence-level (friction-proxy / probe + margin / reactive baselines;
  online study with physical feedback; σ grounding).
- **Decision (template table):** below threshold with evidence-level weaknesses → **stage 13** (refine cycles 0 / 3
  used, so the loop is available). This is the paper's first mandatory loop.

## LOOP MARKER — REFINE from stage 20 → stage 13     [version v1 → v2]

- **Reason:** gate 6.5 < 7.5 with evidence-level weaknesses (`paper/mypaper/20_quality_gate.json`; also stage-18
  E1–E4).
- **Amendment of record (written before any v2 code / run):** `docs/09_amendment_v2.md` — A (frontier, Learn-then-Test
  certificate, extra contrasts on existing replays), B1 CSF-proxy baseline σ_p ∈ {0.2, 0.4, 0.8} with registered
  read-out H5, B2 probe + fixed margin, B3 online study with physical feedback (pilot-gated, downscale order), C not
  done with reasons. All v2 rows secondary; v1 verdicts unchanged.
- **Snapshot taken:** `paper/mypaper/v1/` (draft after stage 17, 19 pass 1, 19 pass 2; reviews and gate stay in
  `paper/mypaper/`); `results/v1/` is the frozen v1 evidence (sha256 in `results/v1/13_freeze.json`).
- **Refine cycles used:** 1 / 3. **Next stage:** 13 ITERATIVE_REFINE [v2]: implement A (sandbox), B1 / B2 replay code
  + tests, 5-minute pilot, then replays (Actions or sandbox) → `results/v2/`.
- **Resuming under version:** v2. Writing time: deadline 12-04 AoE; stages 16–20 again by ≈ 11-22.

## Stage 13. ITERATIVE_REFINE     [v2] — amendment 09 runs (in progress)

- **Started:** 2026-11-09 (run 43). Plan = `docs/09_amendment_v2.md` (frozen before any v2 code). Code committed before
  each run: `code/analysis_v2_a.py` (+ `tests/test_v2_a.py`, 32 / 32 tests), `code/crc_grids_09.py`,
  `code/analysis_v2_b.py`. Replays on GitHub Actions (`experiments/p2_crc09_v2.json`, 12 jobs, ≈ 525 s each; logs
  land in `results/v1/logs/p2_crc09_*` because of the workflow's tee path — new files only, frozen v1 files unchanged).
- **A (existing replays, 2,000 draws; `results/v2/a_analysis.json`, `_08e.json`)**, all vs CSF-1, secondary:
  matched slip 0.10 — D_match CertGrip-full 0.4563 [0.4096, 0.4896] (08c) / 0.4475 [0.4111, 0.4880] (08e), onset-only 0.4736 /
  0.4629, CSF-μ̂ 0.469 / 0.4793 → all superiority; Learn-then-Test (δ 0.10) — D_ltt CertGrip-full 0.4043 / 0.4015,
  onset-only 0.4148 / 0.4303, CSF-μ̂ 0.3704 / 0.404, all superiority, no fallback; LTT test slip CertGrip-full 0.0696
  (08c). A3: D(CSF-μ̂ vs CSF-1) 0.3816 [0.2965, 0.4505], D(onset-only vs CSF-1) 0.4464 [0.3776, 0.4906] → superiority. Caveat: CSF-μ̂
  still sits at grid index 0 in D1 / D2 on 08c (also under LTT), so its 08c rows are biased against it; 08e rows are
  the fair ones. Reading: the probe's saving survives matched slip and a high-probability certificate; the plug-in and
  the learner are indistinguishable.
- **B1 / H5 (`results/v2/b_analysis.json`)**: D(CertGrip-full vs CSF-proxy σ_p) = 0.0514 [−0.0673, 0.166] at σ_p 0.2
  (not shown), 0.5042 [0.4362, 0.5635] at 0.4, 0.8361 at 0.8 (superiority). Prediction "margin shrinks as σ_p falls"
  held; the CI\*\* first includes 0 at σ_p 0.2. CSF-proxy@0.4 is worse than CSF-1 (RE 0.9213 vs 0.783): a log-noise of
  0.4 exceeds the log-μ prior spread. CSF-proxy@0.2 hit grid index 0 in D1 / D2 → edge rule: 08e-recipe grids
  (`crc_grids_09e.json`, `experiments/p2_crc09e_v2.json`, dispatched) → `analysis_v2_b.py --edge`.
- **B2 (probe + fixed margin, no calibration)**: test physical slip 0.9582 / 0.8257 / 0.6182 / 0.335 at m 0 / 0.25 /
  0.5 / 1.0 (D3 / D4 ≥ 0.619 even at m 1.0) — the bare Coulomb force is far below F\*; calibration is what sets the
  margin. Descriptive.
- **B1 edge rule read (`results/v2/b_analysis_edge.json`, 08e-recipe grids, both arms off the grid edges):**
  D(CertGrip-full vs CSF-proxy@0.2) = −0.0299 [−0.1903, 0.0816] → not shown (RE 0.4442 vs 0.4312; test slip 0.09 vs
  0.0825). So a non-tactile friction prior with log-error 0.2 does as well as the probe at onset noise σ 0.2: the
  paper must say the probe's value is "a friction estimate of about that quality", not touch per se.
- **B3 (online, physical feedback; run 44, plan `plans/stage_13_v2_b3_online_physical.md`, code `code/b3_online.py`
  + `tests/test_b3.py` committed before any replay):** pilot 200 replays in 2.5 s → 40,000 replays ≈ 0.14 CPU-h ≤ 6 h,
  so the full design ran (S1 / S3 × orderings 0–4 × 2 arms, sandbox, ≈ 25 s per stream; `results/v2/b3/`,
  `results/v2/b3_analysis.json`). Physical slip, mean over 5 orderings (range), steps 1,501–2,000: CertGrip 0.1032
  (0.100–0.106) S1 / 0.0992 (0.090–0.112) S3; CSF-1 0.0988 (0.082–0.110) / 0.0936 (0.088–0.100). RE_mid same window:
  CertGrip 0.4626 / 0.5135, CSF-1 0.7998 / 0.8726 → D_RE 0.4216 (S1) / 0.4115 (S3); steps 1–500 D_RE 0.4387 / 0.4438.
  Label-rule OQT on the same orderings (08d start): CertGrip RE 0.4723 / 0.515, slip_label 0.1012 / 0.1008.
  Reading (descriptive, 5 orderings, no CI registered): with real slip feedback the tracker holds physical slip at
  ≈ α under both shifts and the probe's force saving (≈ 41–44 %) is unchanged from the offline / label-feedback rows.
- **Next (run 45):** stage 14
  [v2] (fresh subagent), 15, and stages 16–20 again on draft_v1 (v2 rows enter as secondary, v1 verdicts unchanged).

## Stage 13. ITERATIVE_REFINE     [v2] — closed (run 44)

- All amendment-09 rows done (A, B1 + edge rule, B2, B3); C items stay limitations (09 §C). numpy-2 check 0 / 0;
  tests 33 / 33; 0 flagged logs. Frozen: `results/v2/13_freeze.json` (73 files, sha256).

## Stage 14. RESULT_ANALYSIS     [v2]

- **Finished:** 2026-11-10 (run 44). Plan `plans/stage_14_result_analysis_v2.md`; template verbatim via
  `docs/prompts/build_stage14_v2.py` (v2 analysis JSONs + v1 crc / h3 read-outs, unaltered; 09 amendment + B3 plan).
  Pass 1 fresh opus subagent → `results/14_analysis_v2_pass1.md`; pass 2 area-chair prompt verbatim, fresh opus
  subagent → `results/14_analysis_v2_pass2.md`: 17 findings, 1 numeric (truncation by 0.0001), no fabrication; all
  accepted. Merged `results/14_analysis_v2.md` with six statements of record (main session re-checked B2 per-stratum
  slip and the v1 H2b σ rows against the JSON).
- Key reading: the probe + calibration saving vs CSF-1 survives every route / grid and online physical feedback;
  no demonstrated gain of the learned model over the probe-in-physics formula; a non-tactile friction prior of
  log-error 0.2 is not distinguishable from the probe; uncalibrated margins miss α per stratum.
- **Next:** stage 15 RESEARCH_DECISION [v2].

## Stage 15. RESEARCH_DECISION     [v2]

- **Finished:** 2026-11-10 (run 44). Plan `plans/stage_15_research_decision_v2.md`; `results/15_decision_v2.md`.
  **Decision: PROCEED** (all three hard rules met; the claim is re-scoped to "friction-onset probe + conformal
  calibration", with H5 at σ_p 0.2 and H2b stated as limits). REFINE rejected: remaining gaps are hardware-only or
  out of scope (09 §C). Refine cycles used 1 / 3.
- **Next:** stage 16 PAPER_OUTLINE [v2].

## Stage 16. PAPER_OUTLINE     [v2]

- **Finished:** 2026-11-10 (run 44). Plan `plans/stage_16_paper_outline_v2.md`; template verbatim
  (`paper/mypaper/prompts/build_stage16_v2.py`), fresh opus subagent → `paper/mypaper/sections/00_outline_v2.md`
  (≈ 7,100 words of outline; body target ≈ 3,300 words for ≤ 5 pages + refs, stated deviation).
- Title "Probe, Then Certify: A Tactile Friction-Onset Probe with Conformal Risk Control for Certified-Slip
  Minimal-Force Grasping"; method framed as probe + force rule + CRC (learned model optional); v2 rows secondary;
  descriptive names + hypothesis glossary; Figure 1(b) from the real frontier data. Number audit: 0 unmatched apart
  from rounding notes in the header (0.0001 / 0.4042 / 0.0228 quoted from the stage-14 file) — main session checked
  D_crc(CSF-μ̂) 0.4149 against `a_analysis_08e.json` point.
- Corrected `results/15_decision_v2.md` wording ("would do as well" → "no advantage is shown"; no equivalence test).
- Open: missing verified cite keys (Learn-then-Test; classic grip-load; early incipient slip) → add via verified
  entries before stage 17.
- **Next:** citations, then stage 17 PAPER_DRAFT [v2].

## Stage 17. PAPER_DRAFT     [v2]

- **Finished:** 2026-11-10 (run 44). Plan `plans/stage_17_paper_draft_v2.md`; template verbatim
  (`paper/mypaper/prompts/build_stage17_v2.py`), fresh opus subagent → `paper/mypaper/draft_v2.md` (≈ 7,440 words
  main body; every RESTRICTS floor met; condensed to 5 pages at stage 22) + `figures/figure1_prompt_v2.txt`
  (panel b from the 36 real frontier points).
- The one [NEED] (v2 compute) filled by the main session from logs: `code/tools_compute_v2.py` →
  `results/v2/compute_v2.json` (2.357 CPU-h: 1.347 B1/B2, 0.868 edge rule, 0.142 B3; CPU model not logged).
- Number audit 0 unmatched; 55 / 55 cite keys in cards. Draft deviations from the outline noted by the drafter
  (onset-only label-route row not claimed within ±0.05; Discussion / Limitations split).
- **Next:** stage 18 PEER_REVIEW [v2] (two fresh subagents, evidence audit).

## Stage 18. PEER_REVIEW     [v2]

- **Finished:** 2026-11-10 (run 44). Plan `plans/stage_18_peer_review_v2.md`; template verbatim
  (`prompts/build_stage18_v2.py`); two fresh opus subagents. Run 1 A 5 / B 4, run 2 (RSS pair) A 4 / B 6
  (mean 4.75; v1 pass 2 4.5). **CRITICAL_FABRICATION: no** (≈ 100 numbers checked, > 46 recomputed from raw
  replays — H2a, all B3 windows, CSF-proxy@0.2 on crc09e — all exact).
- Merged record `paper/mypaper/18_peer_review_v2.md`: 10 paper-level must-fix items (LTT plug-in sentence wrong;
  RAW-Qv omitted from H1c; mixed-grid comparisons; one hedge for learned vs plug-in; headline conditional on σ;
  "certified" scope; force accounting incl. preload; route labels; small fixes incl. D-FID; B2 framing; density) and
  4 evidence-level items (reactive / tuned-margin baselines; σ grounding; direct learned-vs-plug-in at matched slip
  + conditional tables; hardware / online with intervals) for stage 20.
- **Next:** stage 19 PAPER_REVISION [v2] (`prompts/build_stage19_v2.py`; snapshot `paper/mypaper/v2/draft_v2_stage17.md`).

## Stage 19. PAPER_REVISION     [v2] — pass 1

- **Finished:** 2026-11-10 (run 44). Plan `plans/stage_19_paper_revision_v2.md`; template verbatim
  (`prompts/build_stage19_v2.py`), fresh opus subagent; snapshot after `paper/mypaper/v2/draft_v2_stage19pass1.md`.
- All 10 must-fix items addressed (LTT sentence corrected: plug-in 0.3704 vs 0.4043 primary, 0.4040 vs 0.4015
  refined; RAW-Qv reported, every CI contains 0; same-grid pairs; one hedge; headline conditional on σ 0.2 /
  μ range with σ* = 0.4; title "… in Simulation", certificates scoped; hold-force vs preload / squeeze; route labels;
  D-FID 0.7257; Holm drop stated as deviation; B2 reframed; Appendix A–F). E1–E4 as limitations only.
- Words 9,117 → 12,155 (+33 %; main body +12.6 %, appendix 1,892); no section shorter except Experiments (moved to
  the appendix). Number audit 0 unmatched; main session re-checked probe displacement / static-touch values against
  `19_report_rows.json`. +33 % > 30 % → **second stage-18 pass** before stage 20 (template rule).
- **Next:** stage 18 [v2] pass 2 on `draft_v2.md`.

## Stage 18. PEER_REVIEW     [v2] — pass 2

- **Finished:** 2026-11-10 (run 45) on `v2/draft_v2_stage19pass1.md`. Plan `plans/stage_18_peer_review_v2_pass2.md`;
  template verbatim (`prompts/stage18_v2_pass2_user.txt`); two fresh opus subagents. Run 1 A 4 / B 5, run 2 (RSS pair)
  A 4 / B 5 (mean 4.5). **CRITICAL_FABRICATION: no** (≈ 190 + ≈ 240 numbers checked, ≈ 35 recomputed from raw
  replays / labels by an independent script — all match).
- Merged record `paper/mypaper/18_peer_review_v2_pass2.md` (P1–P9, E1–E8). Main one, verified by the main session:
  the draft says "no equivalence test was registered" for H2b, but `docs/08b_preregistration.md` §4 item 3 registers
  a TOST at ±0.10 (implemented in `code/analysis_crc.py`) → "registered TOST not met". Others: RAW-Qv wording, slip
  above α per seed / refined-grid stratum, σ vs σ_p scale claim wrong, weak unshrunk comparators, force accounting
  vs preload, §6 redundancy.
- **Next:** stage 19 pass 2 (`prompts/stage19_v2_pass2_user.txt`, builder `build_stage19_v2.py --pass2`), then stage 20.

## Stage 19. PAPER_REVISION     [v2] — pass 2

- **Finished:** 2026-11-10 (run 45). Plan `plans/stage_19_paper_revision_v2_pass2.md`; template verbatim
  (`prompts/stage19_v2_pass2_user.txt`, builder `build_stage19_v2.py --pass2`), fresh opus subagent, targeted edits.
  Snapshot after `paper/mypaper/v2/draft_v2_stage19pass2.md`.
- P1 H2b: registered TOST (±0.10, 0.0125 / side) not met on primary (0.1454) / refined (0.1001), met only on the label
  route (secondary); the H5 "no equivalence test" sentence kept (09 registers none). P2 RAW-Qv point slip above α;
  P3 heterogeneity (Q 31.04 / 15 df, guard only); P4 per-seed slips (seed 4 0.1018 > α), refined-grid strata above α
  described without numbers; P5 σ / σ_p on one scale; P6 unshrunk comparators (plug-in σ 0.4 RE 0.9877 vs CSF-1 0.7832);
  P7 force accounting vs preload, Frozen-CertGrip 0.2461 vs Frozen-COMP 0.1910 under S3; P8 ≈ 88 cal / stratum (352 / 4);
  P9 §6 1,016 → 901 words (P9 asked to tighten; above floor).
- Words 12,155 → 13,155 (+8 %); floors met; number audit 0 unmatched with design docs; main session spot-checked
  0.1018, 0.2461, 0.1910, 0.9877, n_cal 352 in the results JSONs.
- **Next:** stage 20 QUALITY_GATE [v2].

## Stage 20. QUALITY_GATE     [v2]

- **Finished:** 2026-11-10 (run 45). Plan `plans/stage_20_quality_gate_v2.md`; template verbatim (threshold 7.5),
  builder `build_stage20.py paper/mypaper/draft_v2.md _v2`, fresh opus subagent, paper only →
  `paper/mypaper/20_quality_gate_v2.json`.
- **Score 5.5 / 10 (v1 6.5) → FAIL; not auto-approved** (below threshold — no evidence for approval). The gate found
  the numbers internally consistent (recomputed headline / refined-grid / matched-slip / H2b / H4e / LTT contrasts).
  12 weaknesses (9 evidence-level), 11 required actions: σ grounding; reactive and estimate + per-stratum-margin
  tactile baselines at matched slip; force in newtons (absolute / peak / integrated, minimal-force distribution vs
  preload, adaptive preload); shrunk plug-in + direct learned-vs-plug-in at matched slip / LTT; repeated object
  re-splits + per-stratum / cell / friction-quintile slip tables (existing replays); losing sub-pool on the CRC route
  (existing replays); Holm for secondaries as registered; stronger online physical-feedback study; title / density /
  table-order fixes (paper-level).
- **Decision (template table):** below threshold with evidence-level weaknesses → **stage 13** (refine cycles 1 / 3
  used → loop available). Second full loop of paper 2.

## LOOP MARKER — REFINE from stage 20 → stage 13     [version v2 → v3]

- **Reason:** gate 5.5 < 7.5 with evidence-level required actions (`paper/mypaper/20_quality_gate_v2.json`; also
  stage-18 pass-2 E1–E8 in `paper/mypaper/18_peer_review_v2_pass2.md`).
- **Snapshot taken:** `paper/mypaper/v2/` (draft after stage 17, 19 pass 1, 19 pass 2; reviews and gates stay in
  `paper/mypaper/`); `results/v1/`, `results/v2/` frozen; v3 writes to `results/v3/`.
- **Refine cycles used:** 2 / 3. **Next stage:** 13 ITERATIVE_REFINE [v3]: amendment `docs/10_amendment_v3.md`
  written and committed before any v3 code / run (rows from existing replays first: re-splits, per-stratum tables,
  Holm, sub-pool on CRC, shrunk plug-in, per-stratum tuned margin, force in N; then new replays: reactive baseline,
  adaptive preload, online study at 20 orderings × 3 shifts).
- **Resuming under version:** v3. Deadline 12-04 AoE; stages 16–20 again by ≈ 11-24, else retarget (AUTOPILOT §1).

## Stage 13. ITERATIVE_REFINE     [v3] — amendment 10 (in progress)

- **Started:** 2026-11-10 (run 45). Plan `plans/stage_13_v3_amendment.md`; amendment `docs/10_amendment_v3.md`
  committed before any v3 code; `code/analysis_v3_a.py` + `code/tests/test_analysis_v3_a.py` (3 passed) committed
  before its first run.
- **Part A done (existing replays, sandbox, ≈ 1 min):** `results/v3/a_analysis.json` (08c grids),
  `results/v3/a_analysis_08e.json` (08e grids). Sanity: reproduces v1 H2a D 0.4168 and H2b 0.0569 [−0.0399, 0.1454].
  - A1 re-splits (R 200): CRC overall test slip > α in 5 % (CertGrip-full) / 12 % (CSF-1) of splits on 08c grids
    (9 % / 7.5 % on 08e), mean 0.085; some stratum > α in 41–69 % of splits. LTT: overall > α in ≤ 1.5 %.
  - A5 empirical margin: same λ̂ as CRC on 08c (n 500 / stratum), D unchanged; on 08e CSF-μ̂ slip 0.0796 vs 0.075.
  - A6 learned vs plug-in: matched slip −0.0238 [−0.0845, 0.0194] (08c), −0.061 [−0.1104, 0.0123] (08e); LTT 0.0538
    [−0.0568, 0.1222] / −0.0042 [−0.086, 0.1069] — not shown either way.
  - A4 losing sub-pool on CRC: **grid-dependent** — 08c grids superiority (D 0.3754), 08e refined grids inferiority
    (D −0.3152 [−0.5231, −0.0172]); the μ-only restriction carries it (08e −0.1717), amplitude-only does not (+0.49).
  - A7 force: F\*_mid on avoidable test rows median 3.18 N (10 % 0.95, 90 % 11.35, max 31.87), none above the 32.7 N
    preload; hold force CertGrip-full mean 6.52 N vs CSF-1 7.61 N (excess 1.62 vs 2.71 N); shared protocol phases
    ≈ 13.1 + 12.9 + 1.4 N·s for every arm.
  - A3 (Holm as registered) not yet run.
- **Next:** A3 Holm; B1 shrunk plug-in grids + replay manifest; B3 pilot; B2 controller code + pilot.
- **B1 shrunk plug-in done (sandbox, run 45):** grids `results/v3/crc_grids_10.json` (OLS on 800 selection rows:
  σ 0.2 a −0.386 b 0.740; σ 0.4 a −0.474 b 0.404), replays `results/v3/crc10/` (4,800 instances, protocol rd),
  read-out `results/v3/b1_analysis.json` (`code/analysis_v3_b.py`, committed before the replays finished):
  D(CertGrip-full vs shrunk plug-in) σ 0.2 −0.0322 [−0.0982, 0.0743] not shown; **σ 0.4 −0.1395 [−0.1832, −0.0126]
  inferiority** (the registered prediction "advantage shrinks, CI includes 0" was wrong in direction: a shrunk
  one-line plug-in beats the learned model at σ 0.4). Shrunk plug-in vs CSF-1: 0.435 (σ 0.2), 0.2454 (σ 0.4), both
  superiority. **Edge rule triggered** for CSF-shrunk@0.2 (λ̂ at index 0 in D1 / D2) → 08e-recipe grids
  `results/v3/crc_grids_10e.json`; replays `results/v3/crc10e/` queued in the sandbox after B3
  (`analysis_v3_b.py --edge`). σ 0.4 not on an edge (index 1).
- **B3 running (sandbox):** 100 new streams → `results/v3/b3/`; v2 streams reused (60-step determinism check exact).
- **B2 reactive controllers done (sandbox, run 45; addendum 10a fixed before code):** `code/react_run.py`, controller
  hook in `Sim.run` (default path identical to the v1 replays, `tests/test_react.py`; 38 tests pass); runs
  `results/v3/react/` (4,800 id cal + test instances; F5 has no id cal / test objects, empty file), read-out
  `results/v3/b2_analysis.json` (test split, descriptive): REACT-blind@0.5 slip 0.765 (RE −0.173), @0.75 slip 0.463
  (RE 0.419, 54 % at the 4-step cap); REACT-probe@0.5 0.992, @0.75 0.951 (detector rarely fires: 0.5 steps). With the
  registered detector / thresholds no reactive variant comes near α = 0.10. Note: the 3-object timing pilot before the
  full run printed 12 cal-instance outcomes; no parameter was changed afterwards (all fixed in 10a).
- **B3 done (sandbox, run 45):** 100 new streams `results/v3/b3/` + 20 reused v2 streams; read-out
  `results/v3/b3_analysis.json` (`b3v3_online.py analyse`). Physical slip over the 20 orderings: steady windows
  0.098–0.102 for both arms in S1 / S2 / S3; **post-shift transient (steps 501–1,000)** CertGrip 0.139 / 0.098 /
  0.137 vs CSF-1 0.209 / 0.094 / 0.126 (S1 / S2 / S3). D_RE 0.31–0.44 in every window and shift (CertGrip lower force).
  Caveat for the paper: the 95 % intervals are over orderings only (fixed object pools), so they are narrow and do not
  cover object-sampling uncertainty.
- **B1 edge rule done:** replays `results/v3/crc10e/`, read-out `results/v3/b1_analysis_edge.json`: CSF-shrunk@0.2 λ̂
  indices 20–22 of 41 (no edge), slip 0.0771, RE 0.429; D(CertGrip-full vs shrunk plug-in) σ 0.2 −0.0646 [−0.1851,
  0.0087] not shown (this row supersedes the 08c-grid σ 0.2 row; caveat: CertGrip-full is on its 08c grid here — a
  same-grid row against CertGrip-full's 08e replays (`results/v1/crc_v2/`) is to be added at stage 14).
- **Pending (next run):** A3 Holm (re-draw the v1 secondaries' bootstraps per 07 §4 families); the same-grid σ 0.2
  shrunk row; `tools_results_v3.py` → `results/v3/results_v3.json`; then stage 14 [v3] → 15 → 16–20.
- **A3 Holm done (sandbox, run 46):** `code/analysis_v3_c.py` (plan + code committed before running) re-ran the v1
  secondary parts in memory with their recorded seeds / 2,000 draws; **52 / 52 CI\*\* rows reproduced exactly** (none
  "not adjusted"). `results/v3/a3_holm.json`: Holm 5 % within 07 §4 families — H1c 8 / 12 rejected, H2-x 27 / 29,
  H3-x 2 / 4, H4-x 3 / 6; over all 52 rows 40 rejected. Every row not rejected after Holm already had a v1 decision
  of "inconclusive" / CI covering 0 (H4c, H4d, RAW-Qv ×4, H3-S S2 / S1m, H2-M change, mass-noise change), so **Holm
  changes no v1 verdict**. Caveats kept in the file: p is vs 0 as registered, which is not the own threshold for H2-T
  (ratio vs 1.10), H4c (margin) and the oracle share (flagged `null_not_registered_threshold`); p resolution 1 / 2,000;
  v2 rows not re-drawn (sensitivity over v1 rows only).
- **Same-grid σ 0.2 shrunk row done:** `analysis_v3_b.py --edge --samegrid` (flag committed before running) →
  `results/v3/b1_analysis_edge_samegrid.json`: CertGrip-full and CSF-1 from their 08e-recipe replays vs CSF-shrunk@0.2 on
  its 08e-recipe grid: D(CertGrip-full vs shrunk) −0.0353 [−0.1688, 0.0103] **not shown** (same reading as the
  mixed-grid edge row −0.0646); shrunk vs CSF-1 0.4484 [0.4015, 0.5146] superiority; slips 0.090 / 0.077 / 0.0996.
- `code/tools_results_v3.py` → `results/v3/results_v3.json` (8 analysis files, unchanged content).
- **Stage 13 [v3] complete. Next: stage 14 RESULT_ANALYSIS [v3]** (fresh subagent, template `result_analysis.md`).

## Stage 14. RESULT_ANALYSIS     [v3]

- **Finished:** 2026-11-10 (run 46). Plan `plans/stage_14_result_analysis_v3.md`; template verbatim via
  `docs/prompts/build_stage14_v3.py` (v3 analysis JSONs + v1 crc / h3 read-outs unaltered; amendment 10 + context).
  Pass 1 fresh opus → `results/14_analysis_v3_pass1.md`; pass 2 area-chair prompt verbatim, fresh opus →
  `results/14_analysis_v3_pass2.md`: 15 findings, 3 numeric, **no fabrication**; all accepted. Merged
  `results/14_analysis_v3.md` (7 statements of record).
- Key reading: probe + calibration saving vs CSF-1 holds at pool level everywhere but reverses inside the 08e
  μ ∈ [0.5, 0.8] sub-pools; a shrunk plug-in beats the learned model at σ 0.4; reactive controllers fail; Holm changes
  no v1 verdict. Gap found: A7 integrated force / break-even (registered) not produced by code.
- **Next:** stage 15 RESEARCH_DECISION [v3] (refine cycles 2 / 3 used).

## Stage 15. RESEARCH_DECISION     [v3]

- **Finished:** 2026-11-10 (run 46). Plan `plans/stage_15_research_decision_v3.md`; `results/15_decision_v3.md`.
- **Decision: PROCEED** → stage 16 [v3]. Hard rules met (H2a superiority kept at pool level on all v3 routes; Holm
  changes no v1 verdict; ablations for probe and calibration; no fabrication). Refine cycles stay 2 / 3.
- **Next:** A7 integrated-force / break-even by script (or state not produced); stage 16 PAPER_OUTLINE [v3] (revise
  `paper/mypaper/` outline with v3 rows), then 17–20 by ≈ 11-24.
- **A7 integrated force done (run 46, script `code/analysis_v3_d.py`, arithmetic on `a_analysis.json`):**
  `results/v3/a7_integrated.json`. Shared phases 27.4258 N·s (probe-specific squeeze + ramp-down 14.3458). CertGrip-full
  σ 0.2 holds 1.085 N less than CSF-1 → break-even hold **13.22 s** (probe phases) / 25.28 s (all phases); for shorter
  holds the probe costs more force-time than the lower hold force saves. Point values, no interval. To be stated in the
  paper's Limitations. `results_v3.json` regenerated.

## Stage 16. PAPER_OUTLINE     [v3]

- **Finished:** 2026-11-10 (run 46). Plan `plans/stage_16_paper_outline_v3.md`; template verbatim via
  `paper/mypaper/prompts/build_stage16_v3.py` (v2 gate + v2 stage-18 pass-2 record + v2 outline; v3 merged analysis
  binding + pass 1 / 2; 15_decision_v3; note that A7 integrated rows now exist). Fresh opus subagent →
  `paper/mypaper/sections/00_outline_v3.md`.
- Title "Probe, Then Calibrate: Conformal Slip-Risk Control of Grip Force from a Tactile Friction-Onset Probe (a
  Simulation Study)"; learner demoted; v3 rows (A1–A7, B1–B3, Holm) secondary; abstract states σ assumption and the
  μ ∈ [0.5, 0.8] reversal; break-even 13.22 / 25.28 s in §6.
- Self-check: number audit (now also reads `results_v3.json`) 3 unmatched — 2 × 0.0142 (= 0.4551 − 0.4409, a stated
  difference) and 1 × 27.429 quoted only as the forbidden pass-1 value; cite keys for LTT / Johansson / Marconi exist in
  `docs/05_knowledge_cards.json`.
- **Next:** stage 17 PAPER_DRAFT [v3] (template `paper_draft.md`, builder from `build_stage17_v2.py`), then 18 (two
  passes), 19, 20.

## Stage 17. PAPER_DRAFT     [v3]

- **Finished:** 2026-11-10 (run 46). Plan `plans/stage_17_paper_draft_v3.md`; template verbatim via
  `build_stage17_v3.py`; fresh opus subagent → `paper/mypaper/draft_v3.md` (snapshot `v3/draft_v3_stage17.md`).
- ≈ 7,440 body words (abstract 236) — above the RSS Stage 1 target; stage 22 must cut to 5 pages. §6 split into
  Discussion / Limitations. Number audit: 1 unmatched (0.0142, stated difference 0.4551 − 0.4409). One `[NEED]`
  marker (third-round CPU-hours) replaced by the truth: those sandbox runs were not logged as CPU-hours.
- **Next:** stage 18 PEER_REVIEW [v3] (two fresh subagents, builder from `build_stage18_v2.py`), 19, second
  18/19 pass, 20.

## Stage 18. PEER_REVIEW     [v3]

- **Finished:** 2026-11-10 (run 46). Plan `plans/stage_18_peer_review_v3.md`; template verbatim via
  `build_stage18_v3.py`; two fresh opus subagents. Scores: run 1 A 5 / B 4; run 2 A 4 / B 5 (mean 4.5; v2 4.75).
  **CRITICAL_FABRICATION: no** (≈ 40 + many numbers recomputed from raw replays, all match).
- **Code-level finding (both runs), fixed by code:** A7 omitted the probe's 0.02 s return and 0.1 s re-hold at F₀
  (`certgrip/sim.py`). `analysis_v3_a.py::a7_force` fixed, A re-run on both grids (all other values identical),
  `a7_integrated.json`: shared 31.0448 / probe 17.9648 N·s, break-even **16.56 s / 28.61 s** (were 13.22 / 25.28).
- Merged record `paper/mypaper/18_peer_review_v3.md` (must-fix 1–10, E1–E6 evidence-level).

## Stage 19. PAPER_REVISION     [v3] — pass 1

- **Finished:** 2026-11-10 (run 46). Template verbatim via `build_stage19_v3.py`, fresh opus subagent, targeted edits;
  snapshot `paper/mypaper/v3/draft_v3_stage19pass1.md`. All 10 items addressed (item 10 length only partly:
  10,186 → 10,743 words; stage 22 will make the 5-page version). Floors kept. Number audit: 1 flag (0.0142, stated
  difference). Main session checked the new A7 numbers against `a7_integrated.json` and the half-sine squeeze in
  `sim.py`.
- **Next:** stage 18 pass 2 [v3] (two fresh subagents), stage 19 pass 2, stage 20.

## Stage 18. PEER_REVIEW     [v3] — pass 2

- **Finished:** 2026-11-10 (run 46) on `v3/draft_v3_stage19pass1.md`; two fresh opus subagents: run 1 A 4 / B 5; run 2
  A 4 / B 5 (mean 4.5). **CRITICAL_FABRICATION: no** (≈ 30 + 30 numbers recomputed with independent CRC
  re-implementations). Merged record `paper/mypaper/18_peer_review_v3_pass2.md` (P1–P8 paper-level; E1–E7
  evidence-level: correlated-friction pool / width sweep, low / adaptive preload, replay-free calibration, no-probe
  CSF-1 run, pre-specified wide grid + fresh-object matched-slip replication, corrected REACT-probe, hardware σ).

## Stage 19. PAPER_REVISION     [v3] — pass 2

- **Finished:** 2026-11-10 (run 46). Fresh opus subagent, targeted edits P1–P8; snapshot
  `paper/mypaper/v3/draft_v3_stage19pass2.md`. 11,381 words (floors kept; stage 22 compresses). Number audit: 1 flag
  (0.0142, stated difference). E1–E7 only as Limitation 10.
- **Next:** stage 20 QUALITY_GATE [v3].

## Stage 20. QUALITY_GATE     [v3]

- **Finished:** 2026-11-10 (run 46). Plan `plans/stage_20_quality_gate_v3.md`; template verbatim (threshold 7.5) via
  `build_stage20.py paper/mypaper/draft_v3.md _v3`; fresh opus subagent, paper only → `paper/mypaper/20_quality_gate_v3.json`.
- **Score 6.8 / 10 (v1 6.5, v2 5.5) → FAIL; not auto-approved** (below threshold). Numbers found internally
  consistent. Required actions: 4 evidence-level (confirmatory fresh-object replication of the attribution on a
  pre-specified wide grid at matched slip; friction-correlated pool + deployable prior + width sweep; simulate the
  no-probe CSF-1 grasp; ground σ or report a σ band) and 4 paper-level (abstract / contributions readability; one
  evidence-status legend instead of repeated hedges; reframe motivation / title; remove the Figure 1 prompt from the
  body and supply a real Figure 2).
- **Decision (template table):** below threshold with evidence-level weaknesses → **stage 13** (refine cycle 3 / 3,
  the last).

## LOOP MARKER — REFINE from stage 20 → stage 13     [version v3 → v4]

- **Reason:** gate 6.8 < 7.5 with evidence-level required actions (`paper/mypaper/20_quality_gate_v3.json`; stage-18
  v3 pass-2 E1–E7).
- **Snapshot taken:** `paper/mypaper/v3/` (draft after stage 17, 19 pass 1, 19 pass 2); `results/v1–v3/` frozen;
  v4 writes to `results/v4/`.
- **Refine cycles used:** 3 / 3 (last). **Next stage:** 13 ITERATIVE_REFINE [v4]: amendment `docs/11_amendment_v4.md`
  (committed now, before any v4 code / run): fresh pool `f4` + correlated pool `c4`, wide pre-specified 81-point grid,
  confirmatory C1–C5 (Holm), σ band, friction-width sweep, no-probe CSF-1 grasp.
- **Next steps (stage 13 [v4]):** code — pools `f4` / `c4` in `certgrip/data.py` (default paths unchanged + test),
  protocol `noprobe` in `sim.py` (default unchanged + test), grid builder `crc_grids_11.py`, `CSF-fam` arm, manifests;
  2-object-per-family timing pilot; then labels → grids → replays; read-out `analysis_v4.py` committed before the
  first replay result.
- **Resuming under version:** v4. If the v4 gate fails again → owner decision (no further loop).

## Stage 13. ITERATIVE_REFINE     [v4] (in progress)

- **Started:** 2026-11-10 (run 46). Amendment `docs/11_amendment_v4.md` committed before any v4 code.
- Code (each committed before use, defaults reproduce v1 — 46 tests pass): pools `f4` / `c4` + protocol `noprobe`
  (`certgrip/data.py`, `sim.py`, `tests/test_v4.py`); `main.py crc --pool / --rep-protocol`; `predict_v4.py` (frozen
  v1 seed-0 fits re-fitted with the stored best config; reproduce all 18,600 stored v1 predictions to 5e-7);
  `crc_grids_11.py` (W grids, selection rows only); read-out `analysis_v4.py` + synthetic test, committed **before any
  v4 replay**.
- Timing pilot `results/v4/pilot/` → ≈ 15 CPU-h, no reduction. Labels `results/v4/labels/` (f4 4,800, c4 5,600
  instances, sandbox). Preds `results/v4/preds/`; grids `results/v4/crc_grids_11_{f4,c4,np}.json` (CSF-fam μ̄ from c4
  selection objects: F1 0.379, F2 0.496, F3 0.677, F4 0.852).
- **Dispatched:** `experiments/p2_crc_v4_{f4,c4,np}.json` (48 + 24 + 8 jobs, workdir `papers/p2/code`); they queue
  behind paper 1's wave 3.
- **Where to resume:** when the runs finish: `python analysis_v4.py --check` (counts only); time-guard stops → follow-up
  manifests (crc lines carry EARLY_STOP next_index); when complete → `python analysis_v4.py` → stage 14 [v4].
- (run 47, ≈ 19:55 UTC) Actions runs 209–211 (f4 / c4 / np replays) all success; `analysis_v4.py --check`: 4,800
  instances with replays per pool, 0 duplicates → complete. Read-out run once → `results/v4/v4_analysis.json`.

## Stage 14. RESULT_ANALYSIS     [v4]

- **Finished:** 2026-11-10 (run 47). Plan `plans/stage_14_result_analysis_v4.md`; template verbatim via
  `docs/prompts/build_stage14_v4.py` (v4_analysis.json + v3 a7_integrated.json unaltered; amendment 11 + context).
  Pass 1 fresh opus → `results/14_analysis_v4_pass1.md`; pass 2 area-chair prompt verbatim, fresh opus →
  `results/14_analysis_v4_pass2.md`: 16 findings, 1 numeric (p bound), **no fabrication**; all accepted. Merged
  `results/14_analysis_v4.md` (9 statements of record).
- Key reading: **C1 superiority** (plug-in vs CSF-1, D 0.4314), **C2 equivalence** (learner vs plug-in, 0.01117 on the
  matched route only), **C3 superiority** (0.4135) on fresh objects — predictions met; **C4 / C5 not superior, CI below
  0** (−0.5814 / −0.5461): on a friction-correlated pool a family prior beats both tactile arms. Saving shrinks / flips
  with σ 0.4 and narrow friction windows (sweep 0.4314 → −0.6967); measured break-even 17.74 s / 27.07 s; certificate
  marginal (31.5–70 % of re-splits have a stratum above α).
- **Next:** stage 15 RESEARCH_DECISION [v4] (refine cycles 3 / 3 used; no further loop without the owner).

## Stage 15. RESEARCH_DECISION     [v4]

- **Finished:** 2026-11-10 (run 47). Plan `plans/stage_15_research_decision_v4.md`; `results/15_decision_v4.md`.
- **Decision: PROCEED** → stage 16 [v4]. Hard rules met (C1 / C3 superiority, Holm p < 0.005, fresh objects; ablations
  for probe and calibration; no fabrication). Scope fixed by C4 / C5, the σ band, the width sweep and the break-even:
  the saving holds against a friction-blind prior, with low probe noise, a wide friction range and long holds.
  Refine cycles 3 / 3 (no further loop without the owner).
- **Next:** stage 16 PAPER_OUTLINE [v4] (fresh subagent, template verbatim), then 17–20 by ≈ 11-24.
