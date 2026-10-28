# Stage 9 · EXPERIMENT_DESIGN [GATE] · v1

## Goal
Experiment plan YAML with objectives, datasets, baselines (with tuning protocols), proposed methods, ablations covering every effective component, metrics with formulas, risks, compute budget → docs/08_experiment_plan.yaml.

## Tasks
- [x] Run `stage_prompts/experiment_design.md` with {hypotheses} = docs/07_hypotheses.md.
- [x] Fold in the stage-8.5 saturation finding (deviation D1: L chosen by a pre-registered pilot rule).
- [x] Script check: required keys present; every effective component has an ablation; every baseline has a tuning_protocol.
- [x] Update docs/实验构想.md (v1.1 note).
- [x] GATE: auto-approve with recorded evidence (AUTOPILOT §1).

## Expected outputs
- docs/08_experiment_plan.yaml

---

## Output Summary  (filled in AFTER the stage runs)
- Plan: 5 objectives (O1–O5 ↔ H1a–H5′), procedurally generated object sets A/S/A4/A16 + notch-rectangle positive control + MuJoCo scenes, 6 baselines (random, coverage, greedy PF-EIG with 18-config Pareto sweep, RL-success, RL-PFIG, sPCE-myopic), proposed sPCE-total with 5 effective components each mapped to an ablation (A1 myopic, A2a/A2b no-NC objective/input, A3 encoder, A4 L, A5 budget input), 10 metrics with formulas, 7 risks, compute ≈ 71 CPU-h at L=255 re-estimated by pilot.
- Deviations from the hypotheses doc: D1 (L by pilot rule from {255,1023,4095}), D2 (seed downscale order if L=4095).
- **GATE auto-approved** — evidence: required keys present (script), 5/5 components ablated (script), every baseline has an equal-effort tuning protocol, metrics operationalized with formulas, compute fits GitHub Actions sharding with pilot-first rule; the main statistical risks raised by the skeptic are pre-registered.
- **Decision:** PROCEED → stage 10.
