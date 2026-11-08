# Stage 13 (v5) — run 37 plan: test5 follow-ups, E5 dispatch, E6 d1000 read-out, g_T; then paper 2 stage 2

Inputs (07:50 UTC): finished — test5 S2/S12 f1 (run 166), S4_p1 (169), S8_p1 (171), E6 d1000 (167). Still running —
S4_p0 (168), S8_p0 (170), A16-2 p0/p1 (173/174).

1. `tools_resume_manifest.py` on the three finished manifests → one combined follow-up `experiments/v5_test5_f2.json`
   (frozen weights unchanged; only the time-guarded/missing shards).
2. `tools_v5_e5.py` now passes (G\* and student 701 have test5 0–199 in S2/S12) → `experiments/v5_e5_sub16.json` (56).
3. `analysis_e6_v5.py` with the d1000 records (report-only; addendum v5.1g: no further extension whatever it shows).
4. `tools_v5_gt.py` for new test5 files.
5. Then paper 2 (AUTOPILOT §7): stage 2 PROBLEM_DECOMPOSE.
Red lines: no test5 outcome read (only counts); no rule changed.
