# p2 Stage 13 — ITERATIVE_REFINE (v1), run 42

**Plan.** Template `pipeline/references/stage_prompts/iterative_refine.md`. Pick the sub-mode by what failed:
- 13a code_repair: static check `pipeline/scripts/check_numpy2_compat.py papers/p2/code` and `pytest code/tests`.
- 13b iterative_repair: scan all 194 run logs in `results/v1/logs/` for NaN / Inf / RuntimeWarning / overflow.
- 13c iterative_improve: **not used.** The study is pre-registered (08b frozen; 08c–08h written before their
  quantities). "Improving" a predictor or protocol after seeing test results would be post hoc tuning against the
  test split; weak or negative registered outcomes (H1-M, H2b, H3, H2-R) are reported as results, not repaired.
- Then freeze: sha256 of every result file the paper may cite → `results/v1/13_freeze.json`, so later stages can
  check that no number moved.

**Outcome.** numpy-2 check 0 errors / 0 warnings; tests 28 / 28 pass; 0 / 194 logs contain NaN / Inf /
RuntimeWarning / overflow → no repair sub-mode applies. Frozen: `results/v1/13_freeze.json`. Next: stage 14.
