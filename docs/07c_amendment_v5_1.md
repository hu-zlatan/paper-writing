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
| A16-2 | A16 | 2 | 3 | 3.4 | n\* rule: G\* sub-8 success at κ 0, τ 4 = 0.975 > 0.88 → n\* = 3; τ = 3 + 0.351 (200 cal3) |

**A16 keep check (reading fixed here, before the run):** "G\* sub-8 success at that n\*" is read with the same
conditions as the n\* rule (κ 0, τ = n\* = 3, the same 200 cal3 episodes, sub 8). Keep iff in [0.30, 0.90]; if not,
A16-2 is dropped and reported, no substitute. The τ calibration for A16 κ 2 (n\* 3) runs in parallel and is discarded
if the cell is dropped. Manifest `experiments/v5_p0_a16.json`.
**Result (run 30):** G\* sub-8 success at κ 0, τ 3 = 0.800 (200/200 episodes) ∈ [0.30, 0.90] → **A16-2 kept**,
τ = 3.4. Labels + RL: `experiments/v5_a16_label_rl.json`.

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

## Addendum v5.1a — `rl_success` in the 64 × 8 relative-frame trainer (run 30, before any `rl_success` job)
- `touchbed/train_v2.py`, method `rl_success`: reward 0 at every step except the last executed probe, where it is
  1[success] of a training PF (N = 1,000 particles, 3 MH steps, `estimate(refine_iters=10)`, success tolerance 5 mm /
  5°) run on that episode's executed probes — the v1 definition (`touchbed/train.py`). γ = 1, PPO and network as
  `spce_total`; config = selected cfg 6. The trainer-validation value (ball-sPCE, PF-free) uses the same stream as
  `spce_total`, so it is comparable; it is logged, not used for selection. Test: `tests/test_train_v2.py`.
- Cost measured in the sandbox: ≈ 0.05 s per PF episode → ≈ 2.8 CPU-h of PF per 2 × 10⁵-episode run on top of the
  RL run itself; inside the 330-min job budget (the time guard stops and saves if not).
- Runs: S2 and S12, seeds 711–715 (`experiments/v5_e3_rlsucc.json`).
- Pilot TIME_ESTIMATE (sandbox, sub-4 grid, design info only; `results/v5/pilot/`): S4 label 9.8 s / episode, S8 5.6 s.

## Addendum v5.1b — D5 read-out details (run 30, before any v5 val3 job)
- G\* val3 records are re-used where they already exist with the same split, episodes 0–499, (set, κ, τ), sub 8 and
  G\* code path: S2 from `results/v4/d4_val/` (v4 D4), S12 from `results/v3/d3_val/` (v3 D3). The v5 code changes
  (test5 salt, DAgger index range, `--keep best`, sub > 8 batching) do not touch G\* at sub 8. New cells (S4, S8,
  A16-2) run G\* on val3 0–499 in `results/v5/d5_val/`.
- Script: `code/analysis_d5_v5.py` → `results/v5/12_d5_analysis.json`.

## Addendum v5.1c — run 31 execution notes (before any v5 evaluation of `rl_success`, A16-2 students or test5)
- **`rl_success` budget truncation.** 9 of the 10 runs hit the trainer's time guard (80 % of 330 min) before
  2 × 10⁵ episodes: S2 seeds 711/712/713/715 stopped at 123k / 125k / 182k / 125k episodes (714 reached 200k); S12
  seeds 711–715 at 185k / 113k / 111k / 162k / 166k. The PF reward cost more on the runners than the sandbox estimate.
  The trainer has no resume, so the time-guard-saved weights are the models of record; the episode count of each is
  reported next to every `rl_success` number, and the arm stays a control (it is not a hypothesis test). The
  trainer's plateau detector (logged only, `--no-plateau-stop`) had fired at 102k–113k episodes in 7 of the 10 runs.
- **A16-2 labels.** All 60 label jobs of the run-30 dispatch failed in the packing step (belief buffer fixed at 48
  wide; K = 16 needs 96). Fixed (width follows the labels; S outputs unchanged) and re-run with identical commands.
- **Shard follow-ups.** Baseline (pilot3) and G\* val3 shards that the 25-min time guard stopped are completed by
  follow-up manifests that start at the recorded `next_index`, with smaller shards; commands otherwise identical.
