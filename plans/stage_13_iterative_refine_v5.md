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
