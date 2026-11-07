# Stage 13 (v5) — run 35 plan: D5 val3 for S4/S8/A16-2, E6 latency, test5 read-out tooling

Inputs: round-2 students S4/S8/A16-2 (15/15 `max_epochs`), test5 S2/S12 running (runs 157/159), freeze S2/S12 done.

1. `tools_v5_manifests.py val S4|S8|A16-2` → dispatch (D5 read-out, val3 0–499, sub 8). Freeze of these cells waits
   for D5 (order of amendment v5.0).
2. E6: timing check in the sandbox → too slow for one session → addendum v5.1f (runners, same machine per cell job),
   `latency3 --configs/--no-pruned` opt-in flags + test, `experiments/v5_e6_lat.json` (10 jobs) → dispatch.
3. H2-v5 g_T: gt3 cost measured (≈ 0.08 s / episode) → sandbox after a cell's test5 completes.
4. `code/analysis_test5_v5.py` written and tested on synthetic data **before** any test5 number is read; it is run only
   when cells are complete (`--check` prints counts only).
Red lines: no test5 number read or printed this run before the script is committed; no rule changed (v5.1f fills
open details and moves E6's machine, stated with the reason).

## Outputs
- Dispatched: `v5_val_S4/S8/A162` (375 jobs), `v5_e6_lat` (10 jobs).
- Code: `latency3 --configs/--no-pruned`, `analysis_test5_v5.py` (+ synthetic test), `analysis_e5_v5.py`,
  `analysis_e6_v5.py`, `tools_v5_e5.py`, `tools_v5_gt.py`; addendum v5.1f.
- g_T for the 316 test5 files committed so far (`results/v5/test5_gt/`, not read).
- No test5 outcome was read in this run.
