# Stage 13 [v6] — wave 5 (run 48, 2026-11-12)

Plan written before dispatch. Continues `plans/stage_13_v6_p6_and_dispatch.md`.

1. Wave 4 (Actions runs 212–217) finished 2026-11-11 01:48 UTC, all success. Counts only (`analysis_v6.py --check`),
   no outcome read.
2. Follow-ups: `tools_resume_manifest.py` for `v6_e11_p1`, `v6_e11_p2` (eval3 jobs); second follow-ups for the three
   `_f1` manifests (`v6_e8_p3_f1`, `v6_e8_p4_f1`, `v6_e11_p0_f1`) left 0 jobs → complete.
3. `v6_e12_p0` (regrid3) uses `--episodes`, which `tools_resume_manifest.py` does not parse → new helper
   `code/tools_resume_regrid.py`: same command, `--episodes` = the time guard's `remaining` list, `--out <out>_r<first>`.
   This is the addendum v6.1 rule ("time-guard stops are resumed with the same commands on the remaining episodes");
   no setting changes (sub 16, 25-min budget). 118 / 250 E12 p0 jobs stopped early (≈ 2.9 episodes per job of 4).
4. Wave 5 = `v6_e11_p1_f1` (35) + `v6_e11_p2_f1` (10) + `v6_e12_p0_f1` (118) + `v6_e12_p1` (250) + `v6_e12_p2` (150)
   = 563 jobs (≤ 650). E12 p1/p2 will also need regrid follow-ups (expect ≈ 190 jobs).
5. g_T: `tools_v6_gt.py` in the sandbox on newly committed test5 files.
6. Red lines: no outcome is read before `--check` is complete; no manifest setting changed.
