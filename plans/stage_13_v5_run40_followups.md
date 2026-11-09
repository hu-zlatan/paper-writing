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
