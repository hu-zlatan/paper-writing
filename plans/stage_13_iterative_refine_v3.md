# Stage 13 ITERATIVE_REFINE [v3] — plan and record (run 7, 2026-10-29)

**Plan.** Sub-modes per `pipeline/references/stage_prompts/iterative_refine.md`:
- code_repair: `pipeline/scripts/check_numpy2_compat.py code` and the unit tests.
- iterative_repair: scan every v3 Actions log (`results/v1/logs/v3_*.log`) for NaN / Inf / RuntimeWarning /
  OverflowError / Traceback / "killed"; trace each to its root cause.
- iterative_improve: **not applied.** D3 and H2 are pre-registered decisions; changing the student, the RL trainer or
  the evaluator after seeing them would be a post-hoc design change. v3 is the last loop before escalation
  (07_hypotheses_v3 header) and row 4 forbids a fourth design.

**Record.**
- numpy2 compat: 0 errors / 0 warnings. Unit tests: 60 passed (run 7, after the changes below).
- Log scan: 1,398 v3 logs, 0 matches for traceback / nan / runtimewarning / overflow / killed / error.
- Root-caused fixes during the v3 runs (each with a test or a reproduction check, none silences a warning):
  1. `dagger3` passed no particle filter to a belief-input student (D3-B crash, run 6) → PF passed in `_label_loop`;
     history-student path re-run reproduces s501 r1 episode 0 actions.
  2. `label3` / `save_shard` / `save_student` crashed on a fresh output directory (run 6) → directory creation; I/O only.
  3. `analysis_cal_v3.py` did not glob n\* = 3 shards (run 6) → glob fixed.
  4. PPO trainer stopped at the plateau, while the 08 plan says the H2 runs record the plateau but do not stop
     (run 7) → `--no-plateau-stop` flag; default unchanged; new test `test_plateau_recorded_without_stopping`.
  5. `regrid3` required `success` / `ball_info` in its source records (run 7) → optional (`.get`), so no-grid eval3
     outputs can be re-read; no-grid G\* + regrid sub 8 reproduces the grid eval bit-for-bit on val3 episode 3.
- Sandbox resource note: one sub-8 grid read-out peaks at ≈ 3.7 GB; two in parallel were OOM-killed by the sandbox
  memory cgroup (no result affected: the killed shard was deleted and its episodes come from the runner job).
- Decision: → stage 14 (v3) when the M4 re-reads (`v3_t3_m4*.json`) and the D3-B validation have landed.
