# Amendment v5.1 — P0 read-out, calibrated cells, RL selection (2026-11-06, run 30; before any E1/E2-r1/E3(ii) job)

Applies the rules frozen in `docs/07c_amendment_v5_0.md`. Nothing here changes a rule; it fills in values the rules
produce. Source files: `results/v5/12_cal_analysis.json` (`code/analysis_cal_v5.py`),
`results/v5/12_rl_sweep_selection.json` (`code/analysis_rl_sweep_v5.py`).

## Cells
| cell | set | κ | n\* | τ | source |
|---|---|---|---|---|---|
| S2 | S | 2 | 4 | 4.7 | v3 Cal′ (unchanged) |
| S4 | S | 4 | 4 | 4.8 | Cal′ rule: 4 + mean G\* travel time 0.797 (200 cal3) |
| S8 | S | 8 | 4 | 4.8 | Cal′ rule: 4 + 0.834 (200 cal3) |
| S12 | S | 12 | 4 | 4.9 | v3 Cal′ (unchanged) |
| A16-2 | A16 | 2 | 3 | pending | n\* rule: G\* sub-8 success at κ 0, τ 4 = 0.975 > 0.88 → n\* = 3 |

**A16 keep check (reading fixed here, before the run):** "G\* sub-8 success at that n\*" is read with the same
conditions as the n\* rule (κ 0, τ = n\* = 3, the same 200 cal3 episodes, sub 8). Keep iff in [0.30, 0.90]; if not,
A16-2 is dropped and reported, no substitute. The τ calibration for A16 κ 2 (n\* 3) runs in parallel and is discarded
if the cell is dropped. Manifest `experiments/v5_p0_a16.json`.

## RL configuration (E3 i)
v3 D9 rule on the 8 sweep runs (seed 719, 10⁵ episodes, S2): highest final trainer-validation ball-sPCE is cfg 6
(6.300) vs cfg 0 = the v3/v4 config (6.241); gap 0.059 > 0.02 tie band → **cfg 6** (lr 1.257e-3, ent 9.50e-4,
batch 256, critic lr 4.93e-4) for every cell, seeds 711–715, 2 × 10⁵ episodes.

## Sizes
No reduction step is triggered: the P0 numbers do not move the ≈ 800–860 CPU-h estimate of v5.0 above 1,000 CPU-h
(the RL sweep took ≈ 0.5 h per 10⁵-episode run, as budgeted; cal3 shards finished inside their 25-min budget).
test5 500 episodes per cell, val3 500, S8 kept, E7 decided after the pilot timing.

## Recorded incidents (no rule changed)
- The first E2 round-0 dispatch and the RL sweep committed their JSON logs but not the `.npz` weights (`*.npz` was
  ignored for `results/v5/`, the same slip as v4 run 8). `.gitignore` now keeps `results/v5/**/*.npz`; round 0 is
  re-run with identical commands (`experiments/v5_d5_r0_S2_S12_rerun.json`). The first JSONs are kept in
  `results/v5/prev_r0_json/` as a determinism check. Sweep weights are not needed (only the selection is).
- `rl_success` (E3 iii) exists only in the v1 trainer (`touchbed/train.py`, terminal 1[success] from a 1,000-particle
  PF). The 64 × 8 relative-frame trainer (`train_v2.py`) needs the same reward added before E3 (iii) runs; until then
  E3 (iii) is pending. Its definition will follow the v1 one (terminal 1[success] of the PF estimate), stated in a
  short addendum before any `rl_success` job.
