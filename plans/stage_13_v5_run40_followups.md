# Stage 13 (v5) — run 40 plan: last test5 follow-up f5, g_T, then read-out → stage 14; then paper 2

Inputs (01:50 UTC 11-09): f4a (182), f4b (183), e5_f2 (181) all finished `success`; nothing running.
`analysis_test5_v5.py --check` (counts only): S2 5997/6000, S4 4496/4500, S8 4497/4500, S12 5999/6000, A16-2 4499/4500.
`tools_resume_e5.py` on e5_f2 → 0 jobs (E5 complete).

1. `tools_resume_manifest.py` on f4a / f4b → 11 single/two-episode random-baseline jobs → `experiments/v5_test5_f5.json`
   (same commands, frozen inputs, `--budget-minutes 60` time guard only) → dispatch.
2. E5 complete → `analysis_e5_v5.py` (report-only), commit.
3. `tools_v5_gt.py --workers 2` in the sandbox for the remaining test5 files; commit outputs.
4. When every cell is at 300 for every method and g_T is complete → `analysis_test5_v5.py` read-out → stage 14 plan.
5. Then paper 2 (AUTOPILOT §7): see `papers/p2/PROGRESS.md` (fits landed → COMP selection → CRC replay).
Red lines: no rule changed; frozen weights untouched; test5 read only once complete, by the pre-written script.

## Update (≈ 02:00 UTC) — g_T moved to runners (operational, addendum v5.1h)
The sandbox pace was ≈ 1 file / min with 2 workers (483 files left, mostly S4 / S8 → ≈ 4 h, longer than this run).
Same `main.py gt3` command (J 16, L 4095), one job per source file, output name unchanged
(`results/v5/test5_gt/<name>.jsonl`; the workflow's `set -o pipefail` keeps failed jobs from committing).
`experiments/v5_gt_r0.json` / `v5_gt_r1.json` (243 + 242 jobs). Two files already computed in the sandbox are
recomputed on runners into `results/v5/test5_gt_check/` to check sandbox/runner agreement (g_T is a deterministic
function of the recorded actions and fixed per-episode draws). No g_T value has been read; nothing else changes.
