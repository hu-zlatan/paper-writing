# Stage 13 · ITERATIVE_REFINE · v5

## Goal
Make the code ready for the v5 rows of `docs/07c_amendment_v5_0.md` without changing any v3/v4 code path, then run P0.

## Steps
1. `touchbed/v3.py`: add split `test5` (new salt 107, unique-salt assert kept). Test: episode streams of test3 unchanged.
2. `touchbed/distill.py` / `distill3`: `--keep best` option (keep weights with lowest held-out R̄; also save the last
   checkpoint as `<out>_last.npz`). Default stays `last` so v3/v4 commands reproduce. Unit test on a tiny dataset.
3. Check `regrid3 --sub 16` runs on one episode (sandbox) and time it.
4. P0 manifests: `calib3` for S κ 4, S κ 8 (n\* 4); A16 κ 2 n\* scan (n = 2…6, 200 cal3 episodes each); `pilot3`
   for S4, S8, A16-2. Dispatch on Actions; analyse; write amendment v5.1 (τ, n\*, sizes after reduction order).
5. PROGRESS + push after each step.

## Red lines
No v3/v4 output changed; test5 not touched before the freeze; all numbers from committed results.

## Status (run 30)
Steps 1–3 done (chat session). Step 4: P0 analysed (`results/v5/12_cal_analysis.json`), amendment v5.1 written
(+ addenda a: rl_success; b: G* val3 re-use). Main runs E1/E2/E3 dispatched; stage 13 continues as the execution
stage of the v5 rows until test5 is frozen and evaluated, then stage 14.

## Plan (run 31)
1. Audit run-30 dispatches: every label / DAgger shard `complete`; Actions run 42233537062 failed in all 60 A16 label
   jobs (`episode_arrays` belief buffer fixed at 48; A16 has K = 16 → 96). A16 RL jobs in that run succeeded.
2. Fix: belief buffer width follows the labels (48 for S → S outputs unchanged); regression test; sandbox check
   (A16 label3 2 episodes + 3-epoch distill3). Re-dispatch the 60 A16 label jobs with identical commands.
3. Dispatch `distill1 S2 S12` (r1 students) and `r0 S4 S8` (round-0 students) from `tools_v5_manifests.py`.
4. Baselines on pilot3 landed → write `code/analysis_base_v5.py` (H\* per cell by the amendment rule) if the rule is
   fully specified in the amendment; otherwise log and defer.
