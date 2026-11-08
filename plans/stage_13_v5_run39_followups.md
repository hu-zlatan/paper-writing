# Stage 13 (v5) — run 39 plan: test5 follow-ups f4, E5 follow-up f2, g_T; then paper 2

Inputs (19:50 UTC): run-38 dispatches f3a (177), f3b (179), e5_f1 (178) all finished `success`; nothing running.

1. `tools_resume_manifest.py` on f3a / f3b → 93 time-guarded shards remain (random baseline ≈ 900 episodes in all
   cells — ≈ 700 s / episode under sub 8, so each 25-min job only finished ≈ 2 episodes; RL A16-2 13 episodes).
   New `code/tools_split_manifest.py`: random shards split into 3-episode jobs with `--budget-minutes 60` (time guard
   only, same precedent as run 36's 25 → 50); everything else unchanged → `experiments/v5_test5_f4a.json` /
   `f4b.json` (166 + 166 jobs, under the 256 matrix cap). The analysis merges `<tag>_<method>_*.jsonl` per episode.
2. `tools_resume_e5.py` on `v5_e5_sub16_f1.json` → `v5_e5_sub16_f2.json` (25 jobs / 45 episodes).
3. `tools_v5_gt.py` for new test5 files; commit outputs (never dot-prefixed temps).
4. Then paper 2 (AUTOPILOT §7): see `papers/p2/PROGRESS.md`.
Red lines: no test5 outcome read (counts only); no rule changed; frozen weights untouched.
