# Stage 13 ITERATIVE_REFINE [v6] — P6 timing pilot and dispatch (2026-11-10, owner session)

1. P6 (`experiments/v6_p6.json`, Actions, 10 jobs): pilot3 episodes 0–2 for g125_512_16, g500_512_4, G\* --run-salt r1,
   round-0 student 701, in S2 and A16-2; sub-16 re-read timing on 3 v5 test5 G\* episodes (already seen; timing only).
2. TIME_ESTIMATE per row from the P6 wall times (+ v5 test5 wall times for E8) → addendum v6.1 in
   `docs/07c_amendment_v6_0.md` (sizes; apply the frozen reduction order if > 800 CPU-h) — before any main job.
3. Manifests `experiments/v6_e8_*.json` … `v6_e12_*.json` (≤ 25-min time-guarded jobs, same split into small
   episode ranges as v5), dispatch in batches sized to the shared 20-runner cap.
4. Write `code/analysis_v6.py` + a synthetic test and commit before the first E8–E12 record is read.
