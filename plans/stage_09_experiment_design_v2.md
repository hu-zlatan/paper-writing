# Stage 9 · EXPERIMENT_DESIGN [GATE] · v2

## Goal
Experiment plan YAML for the v2 hypotheses → docs/08_experiment_plan_v2.yaml.

## Output Summary
- Required keys present; 4 effective components each with an ablation (A1 myopic-rate, A2 full-state objective, A3 No-NC-input, A4 greedy ladder for amortization); every baseline has a tuning protocol (script-checked). Pre-run gates G0–G5 carried over with numeric rules. Compute: gates ≈ 47 CPU-h, main ≈ 121 (fallback 99).
- **GATE auto-approved** (AUTOPILOT §1): evidence — design derives from a three-agent debate that resolved the skeptic's confounds (horizon, objective mismatch, action resolution, latency matching); comparators optimise the same target with the same action set; H1 is protected from downscaling; gates prevent main runs before PF convergence, learnability and comparator strength are shown.
- **Decision:** PROCEED → stage 10 (v2): travel environment, categorical masked head, ball-sPCE, ball-EIG / G*, ladder, rollout planner, exact notch, G1 estimator, TOST; write docs/07c_amendment_v2_0.md first.
