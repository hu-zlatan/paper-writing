# Stage 13 [v6] — wave 7 (run 50, 2026-11-13)

Plan written before dispatch. Continues `plans/stage_13_v6_wave6.md`.

1. Wave 6 (Actions runs 224–226) finished, all success. `analysis_v6.py --check` (counts only, no outcome read):
   test5 0–499 and g_T complete in every cell; E12 complete except 9 student episodes (S2 s702 ×1, S4 s702 ×2,
   S4 s705 ×2, S8 s703 ×2, S8 s705 ×1, A16-2 s702 ×1).
2. Follow-ups via `code/tools_resume_regrid.py` (same commands, remaining episodes only): `v6_e12_p0_f3` (1),
   `v6_e12_p1_f2`, `v6_e12_p2_f2`. These are long single episodes (the 25-min guard is only checked between
   episodes), so each remaining episode gets its own job (`--episodes <e>`, `--out <base>_r<e>`): 1 + 5 + 3 = 9 jobs.
   This changes only the job split, not any setting (sub, sources, episodes, budget).
3. When they land: `--check` E12 100 everywhere → `python code/analysis_v6.py` read-out → stage 14 [v6] with a fresh
   subagent. If an episode still does not finish within the 350-min job timeout, record it and decide in a plan
   before reading any outcome.
4. Red lines: no outcome read before `--check` is complete; no manifest setting changed.
