# Stage 13 (v5) — run 36 plan: follow-ups, E6 completeness, g_T, D5 S4/S8/A16-2 → freeze

Inputs: all run-35 dispatches finished (val S4/S8/A16-2 runs 161–163, E6 run 164, test5 S2/S12 runs 157–160).

1. Follow-up manifests via `tools_resume_manifest.py`: D5 val3 S4/S8/A16-2 (one manifest) and test5 S2/S12 (one
   manifest, frozen weights unchanged) → dispatch.
2. E6: `analysis_e6_v5.py`; if a job-1 CI fails the v3 Lat′ 10 % rule, apply that rule's "500 more decisions" as one
   1,000-decision job per cell (same machine) — addendum v5.1g, report-only.
3. g_T (`tools_v5_gt.py`) for new test5 files; E5 manifest once G\* and student 701 have test5 0–199 in S2/S12.
4. If the D5 val3 follow-ups land within the run: `analysis_d5_v5.py` → freeze each complete cell
   (`tools_v5_test5.py freeze`), commit + log **before** its test5 manifest → dispatch test5.
Red lines: no test5 outcome read; no rule changed (v5.1g applies an existing v3 rule); D5 has no remedy step.

## Outputs
- Dispatched: val3 follow-ups (79 + 2, the last 2 run in the sandbox), test5 S2/S12 follow-up (141), E6 d1000 (4),
  test5 S4 (267), S8 (300), A16-2 (485).
- D5 complete in all 5 cells: fails everywhere (H5a validation 0/5); all 5 cells frozen before their test5 jobs.
- E6 500-decision read-out + addendum v5.1g; g_T for 148 new test5 files. No test5 outcome read.
