# Stage 13 (v5) — run 38 plan: test5 follow-ups f3, E5 follow-up f1, g_T; then paper 2 stage 10 increment 2

Inputs (13:50 UTC): every run-37 dispatch finished (test5 S4_p0 168, S8_p0 170, A16-2 p0/p1 173/174, f2 175,
E5 176), all `success`; no workflow running.

1. `tools_resume_manifest.py` on S4_p0, S8_p0, A162_p0, A162_p1, v5_test5_f2 → `experiments/v5_test5_f3a.json`
   (126: S4 52, S8 45, f2 29) and `v5_test5_f3b.json` (187: A16-2) — split to stay under the 256-job matrix cap.
   Frozen weights and commands unchanged except start/count/out of time-guarded shards.
2. E5 (regrid3) shards early-stopped at ≈ 7 of 15 episodes (sub 16 ≈ 3 min/episode); `tools_resume_manifest.py`
   does not parse `--episodes` → new `code/tools_resume_e5.py` re-runs each shard's `remaining` episodes in chunks of
   5 (`experiments/v5_e5_sub16_f1.json`, 111 jobs / 444 episodes). Same inputs, same sub 16; only the episode split
   changes. `analysis_e5_v5.py` already merges all `_sub16_*` files per episode.
3. `tools_v5_gt.py` in the background for new test5 files; commit outputs (never dot-prefixed temps).
4. Then paper 2 (AUTOPILOT §7): stage 10 increment 2 (`papers/p2/plans/stage_10_code_generation.md`).
Red lines: no test5 outcome read (only counts); no rule changed; no pre-registered number touched.
