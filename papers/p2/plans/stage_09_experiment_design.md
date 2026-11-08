# p2 Stage 9 · EXPERIMENT_DESIGN [GATE] — plan (run 37, 2026-11-08)

- Template `stage_prompts/experiment_design.md` verbatim; {hypotheses} = `docs/07_hypotheses.md`; preamble empty.
- Output `docs/08_experiment_plan.yaml` with the 8 required keys; hard rules: every proposed component has an ablation;
  each baseline has a tuning protocol; metrics have formulas; honest compute budget.
- Gate: auto-approve (AUTOPILOT §1) with evidence logged; the gate approves the *design*. The pre-registration freeze
  (numeric constants that depend on the pilot: δ_t, F_max, η, c, power re-projection) is a separate document
  `docs/08b_preregistration.md`, written after the stage-10/12 pilot and committed before any non-pilot data.

## Outputs
- `docs/08_experiment_plan.yaml`: 10 proposed components (PM1–PM10), all with ablations (4 ablations added at this
  stage: pooled calibration, additive score, η sensitivity / no anti-windup, cold start — none needs extra simulation); budget ≈ 90 CPU-h at an assumed 1 CPU-s per replay.
