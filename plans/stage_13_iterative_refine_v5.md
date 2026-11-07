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

## Plan (run 32)
1. All run-31 dispatches finished (no failures). Check inputs complete, then dispatch from `tools_v5_manifests.py`:
   `dag2 S2 S12`, `dag1 S4 S8`, `r0 A16-2`; when A16 r0 lands, `dag1 A16-2`.
2. Baselines: `analysis_base_v5.py` shows 21 pilot3 episodes still missing (S2 1, S8 6, S12 2, A16-2 12) →
   follow-up 2 via `tools_resume_manifest.py` (budget 90 min so single long episodes finish).
3. G\* val3 new cells: verify 500/500 in S4, S8, A16-2.
4. E7: was "decided after the pilot timing" (v5.1). Time `g2v3` at C1 32 / 512 in the sandbox; if ≤ 60 CPU-h, add
   an opt-in independent re-estimate (default off, so v3/v4 commands are unchanged), write addendum v5.1d before any
   E7 job, dispatch, pre-write `analysis_e7_v5.py`.
5. Pre-write the D5 val3 student manifest step. test5 untouched.

### Run 33 plan (2026-11-07, scheduled)
1. Verify run-32 dispatches (DAgger r2 S2/S12, r1 S4/S8, r1 A16-2, baseline f2, E7) are complete; dispatch distill2
   S2/S12 and distill1 S4/S8/A16-2.
2. Read out H\* per cell (`analysis_base_v5.py`) and E7 (`analysis_e7_v5.py`); follow-up for E7 shards stopped by the
   time guard (one belief per job).
3. Pre-write the E4 freeze + test5 manifest tool (`tools_v5_test5.py`), size test5 from recorded wall times, and if the
   projection crosses the 1,000 CPU-h trigger apply the frozen reduction order in an addendum before any test5 job.
   test5 untouched.
