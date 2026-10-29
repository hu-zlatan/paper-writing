# Stage 9 · EXPERIMENT_DESIGN [GATE] · v3  (run 5, 2026-10-29)

## Goal
Experiment plan YAML for the v3 hypotheses → docs/08_experiment_plan_v3.yaml, consistent with the frozen amendment
v3.0 (pre-registration commit a1de0fc).

## Tasks
- [ ] Fresh strongest-model subagent with `stage_prompts/experiment_design.md` verbatim; {preamble} = "this is
      iteration v3; previous results showed …" (results/v2/14_analysis.md, results/v2/15_decision.md);
      {hypotheses} = docs/07_hypotheses_v3.md; told that docs/07c_amendment_v3_0.md is frozen and binding.
- [ ] Hard-rule checks (script): required keys; every effective component in proposed_methods has an ablation; every
      baseline has a tuning_protocol; metrics have formulas; compute budget = conditions × seeds × unit cost, with the
      downscale order; consistency with amendment v3.0 (seeds, salts, sizes, HP grid).
- [ ] GATE (AUTOPILOT §1: auto-approve with evidence recorded in PROGRESS.md).
- [ ] PROGRESS.md, commit, push.

## Output Summary
(filled at the end)
