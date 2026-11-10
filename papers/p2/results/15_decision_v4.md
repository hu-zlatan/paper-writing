# p2 · Stage 15 RESEARCH_DECISION [v4] (run 47, 2026-11-10)

Prompt: template `research_decision.md` with the REFINE augmentation; `{analysis}` = `results/14_analysis_v4.md`.

## Decision
**PROCEED** → stage 16 [v4]: rewrite the outline around the confirmatory v4 result and its boundary conditions. v1–v3
verdicts and statements of record stand; v4 C1–C5 are the paper's confirmatory evidence.

## Justification
v4 turned the exploratory v3 attribution into pre-registered tests on objects never simulated before. The three
registered predictions all held: the probe-based plug-in beats the friction-blind conformal baseline (C1), the learned
model is equivalent to the plug-in at σ 0.2 on the registered route (C2), and the v1 H2a result replicates (C3). The
gate's other question — does the saving survive a friction-informative, deployable prior? — got a clear negative
answer (C4 / C5: the family prior wins by D ≈ −0.55 to −0.58). That is not a contradiction of the scoped hypothesis
(the saving is claimed against a friction-blind prior) but it fixes the scope: the probe pays off when friction is
not predictable from what the robot can see, with low probe noise, a wide friction range and holds longer than
≈ 18–27 s. PIVOT is not warranted (the predicted phenomenon appears, confirmatorily); REFINE is not available (3 / 3
cycles used) and the remaining gaps (hardware σ, adaptive preload, replay-free calibration) are out of CPU-simulation
scope. A paper that states these conditions honestly is a stronger and more useful contribution than the v3 framing.

## Hard rules
- Primary metric difference meaningful: C1 D 0.4314, CI\*\* [0.3824, 0.4835]; C3 D 0.4135, CI\*\* [0.3578, 0.4903];
  both Holm-adjusted p < 0.005 (object-cluster bootstrap, 2,000 draws, fresh pool f4). ✔
- Claimed effective components have non-degenerate ablations: probe (C1: CSF-muhat vs CSF-1; S6 no-probe grasp);
  calibration (v3 A1 / A5, v4 S7 re-splits); the learned model is explicitly **not** claimed (C2 equivalence at σ 0.2,
  matched route only). ✔
- No CRITICAL FABRICATION in stage 14 (pass 2: 16 findings, 1 numeric wording error on the p bound, no fabricated
  number). ✔

## Evidence (from `results/14_analysis_v4.md`)
- C2 0.01117 [−0.05552, 0.05686] (matched); CRC route −0.06291 [−0.1226, 0.08396] → not equivalent there.
- C4 −0.5814 [−0.7208, −0.4563]; C5 −0.5461 [−0.6590, −0.4290]; CSF-fam RE_match 0.2674, slip 0.05929.
- σ band: D(plug-in vs CSF-1) 0.6486 / 0.4314 / −0.2065 at σ 0.1 / 0.2 / 0.4.
- Width sweep: 0.4314 → 0.2414 → −0.1094 → −0.6967 (w 1.0 → 0.25), σ 0.2 only, descriptive.
- Break-even vs no-probe grasp: 17.74 s (learner) / 27.07 s (plug-in), point values.
- Certificate marginal: 31.5–70 % of 200 re-splits have a stratum above α.

## Next actions
- Stage 16 [v4]: new outline. Contribution = a confirmatory, condition-mapped answer to "when does a tactile friction
  probe plus conformal calibration reduce grip force at a slip-rate guarantee?" Results: C1–C5 table first; σ band,
  width sweep, family prior and break-even as the boundary map; v1–v3 rows as supporting / secondary. Title and abstract
  must state the conditions and the simulation-only scope; the learner is demoted to a C2 footnote-level result.
- Stages 17–20 (RSS 2027 Stage 1 format, ≤ 5 pages + references) by ≈ 11-24. If the stage-20 gate fails again with
  evidence-level weaknesses → owner decision (no further loop), per 11_amendment_v4 timeline.
