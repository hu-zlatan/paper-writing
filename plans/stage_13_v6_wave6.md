# Stage 13 [v6] — wave 6 (run 49, 2026-11-12 ≈ 19:50 UTC)

Plan written before dispatch. Continues `plans/stage_13_v6_wave5.md`.

1. Wave 5 (Actions runs 218–223) finished except one job of run 221 (`v6_e12_p1`, `S_k4_student_s705_sub16_092`) that
   was still in its Run step after ≈ 2 h (the 25-min guard is checked between episodes only). Decision: cancel run 221
   so its partial output is committed (the commit step runs on `always()`), then resume it like every other stop.
   It committed 2 of 4 episodes. Counts only (`analysis_v6.py --check`), no outcome read.
2. E11: `v6_e11_p1_f2` left 0 → **E11 complete** (with E8, E9, E10: test5 0–499 and g_T complete in every cell).
3. E12 follow-ups (`code/tools_resume_regrid.py`, same commands, remaining episodes only, no setting changed):
   `v6_e12_p0_f2` (20), `v6_e12_p1_f1` (32), `v6_e12_p2_f1` (26) = 78 jobs.
4. Then repeat until 0 left; `analysis_v6.py --check` complete → read-out → stage 14 [v6].
5. Red lines: no outcome read before `--check` is complete; no manifest setting changed.
