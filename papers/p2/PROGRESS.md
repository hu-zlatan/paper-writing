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
