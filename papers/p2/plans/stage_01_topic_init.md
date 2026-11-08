# Paper 2 · Stage 1 TOPIC_INIT — plan (2026-11-08, owner's chat session)

Trigger: owner directive 2026-11-08 (AUTOPILOT §1): open a second paper in a new direction in `papers/p2/`, direction
chosen by Claude, distinct from paper 1 (TouchBED, active tactile localization), within dexterous manipulation /
tactile sensing / embodied learning, CPU-feasible, 1–2 core ideas.

1. Venue: check which AI / robot-learning venues have a posted deadline (ICML, NeurIPS, CoRL 2027; RSS 2027 already
   verified for paper 1).
2. Gap scan with WebSearch / arXiv abstract pages: tactile slip / grip-force regulation, tactile benefit studies,
   conformal prediction in contact-rich robotics. Pick a topic with a clear, checkable claim and an evaluation that
   runs on CPU (MuJoCo).
3. Write `docs/00_topic_init.md` (template `pipeline/references/stage_prompts/topic_init.md`, 6 sections),
   `MEGA_PROMPT.md`, `RESTRICTS.yaml` project block, the three design docs, `PROGRESS.md`, `OWNER_TODO.md`,
   `AI_USAGE.md`; hardware record.
Red lines: no numbers about results (none exist); literature mentioned here is only what was actually opened; full
collection with verifiable IDs happens in stage 4.

## Outputs
- Venue: RSS 2027 Stage 1 (only AI / robot-learning venue with a posted deadline on 2026-11-08); ICML / CoRL /
  NeurIPS 2027 pages not yet posted (ICML 2027 CFP page: "will be posted here soon"; corl.org shows 2026 only).
- Topic: CertGrip — conformal (risk-control) calibration of a tactile minimal-no-slip-force predictor, plus an online
  adaptive variant for shift. Closest works opened and why they differ: see `docs/文献与问题.md`.
- Files listed above written.
