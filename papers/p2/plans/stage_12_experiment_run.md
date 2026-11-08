# p2 Stage 12 — EXPERIMENT_RUN (v1), after the 08b freeze

Increment 1 (run 39): main-pool labels under protocol `"rd"` in the sandbox (`code/run_labels_v1.sh`, two processes,
--budget-minutes 100 per command, outputs `results/v1/labels/<pool>_<family>[_<shift>].jsonl`):
- id: F1–F4 × objects 0–499 × D1–D4 (8,000); S1 / S1m / S3: F1–F4 × id objects 325–499 (2,800 each); s2: F5 ×
  objects 0–549 (2,200). Counts are checked (instances, unavoidable, preload slips) — no predictor is fitted and no
  test-split statistic is looked at in this increment.
Increment 2: H1-M grids (800 id instances, 25 log + 10 dense local points + bisection; 100 per shift pool) — needs the
dense-grid option in `main.py mono`. Increment 3: analysis code (COMP selection on the selection split, offline
conformal, bootstrap, OQT streams) written and tested on synthetic / pilot data **before** reading any cal/test result.
Red lines: frozen protocol and splits (08b); every number from these files; no change to 08b after data exist.
