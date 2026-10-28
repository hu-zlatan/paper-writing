# Stage 13 ITERATIVE_REFINE [v2] — plan and record (run 4, 2026-10-28)

**Plan.** Sub-mode selection per pipeline/references/stage_prompts/iterative_refine.md:
- code_repair: run check_numpy2_compat.py and the unit tests.
- iterative_repair: scan all Actions logs (results/v1/logs/*.log, the version-agnostic log folder) for NaN / Inf /
  RuntimeWarning / Traceback and trace each to its root cause.
- iterative_improve: NOT applied before stage 15. The gate failures (G3 ii/iii, flatness) are pre-registered decision
  inputs; changing the learner after seeing them would be a post-hoc design change that only stage 15 may authorise.

**Record.**
- numpy2 compat: 0 errors / 0 warnings. Unit tests: 26 passed.
- One RuntimeWarning in a *test helper* (0 · (−inf) in the masked-entropy reference of tests/test_train_v2.py); the
  production code (train_v2.py) already masks before multiplying. Fixed in the test at the root (mask before the
  product), not suppressed.
- Log scan: `log1p` divide-by-zero warnings appear only in v1 logs written before the v1 stage-13 fix; the 5 `g2_*`
  tracebacks are the exhausted-budget crash fixed and re-run in run 3; `grid_*_random_sh6–11` FileNotFound errors are
  grid jobs whose 32k source shards were never produced (the G4 runs for shards 6–11 were cancelled) — no affected
  number is used. No open runtime bug.
- Decision: → stage 14 (v2) once the G3 remedy read-out (experiments/v2_g3_remedy_val.json) has landed.
