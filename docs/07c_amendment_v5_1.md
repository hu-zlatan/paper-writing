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

## Addendum v5.1d — E7 decided (run 32, before any E7 job)
- **Timing (sandbox, one process, design info only):** `g2v3` on S κ 2, τ 4.7, belief 0: C1 = 32 → 15 s; C1 = 512
  (all feasible first actions; 168 feasible at this belief) → 20 s; C1 = 512 + independent re-estimate → 33 s for
  beliefs 0–1. E7 therefore costs ≈ 1 CPU-h, far below the 60 CPU-h cap → **full screen (C1 = 512)**.
- **Rows:** g2v3 beliefs 0–31 (split `g2v3`, n\* 4, decision PF and estimator unchanged) in S2 (κ 2, τ 4.7) and S12
  (κ 12, τ 4.9); on the same beliefs both C1 = 32 (the v3/v4 estimator, for a paired comparison) and C1 = 512.
- **Independent re-estimate** (new opt-in flag `--indep-M`, default 0 so every earlier command is unchanged; test in
  `tests/test_v5.py`): after selection, the selected look-ahead action and the greedy action are re-valued on a fresh
  stream (`g2_indep` key) with M = 256 (= reest × M_outer, the size of the selection re-estimate). The sandbox check
  showed the absolute values shift by seed (common to both actions under CRN), so the read-out is on **gaps**:
  selection bias = mean(gap_abs) − mean(indep.gap_abs); headroom reported as mean indep.gap_abs and as the
  ratio-of-means relative gap, each with a belief bootstrap ci95; C1 32 vs 512 paired on the same beliefs.
- Report-only (H3 was a characterisation in v3/v4 and stays one); no decision rule depends on it.
- Manifest: `experiments/v5_e7_h3.json` (16 jobs × 8 beliefs).

## Addendum v5.1e — test5 size by the frozen reduction order (run 33, before any test5 job; no round-2 student exists yet)
- **Re-projection.** Recorded v5 CPU time so far ≈ 266 CPU-h (sum of `wall_s` in `results/v5/`; excludes E7 and the
  re-used v3/v4 S2/S12 labels). test5 sized for real for the first time (`code/tools_v5_test5.py`: every method of E4,
  mean per-episode wall time per (cell, method) from pilot3/val3, sub 8): ≈ 690 CPU-h at 500 episodes per cell
  (2,918 jobs; B-spread / B-cov at sub 8 and the A16 cell dominate; the amendment v5.0 guess was 75 CPU-h per cell).
  Remaining non-test5 work (distill r1/r2, DAgger r2 for S4/S8/A16-2, D5 val3 read-out, E5) ≈ 300 CPU-h →
  **projected total ≈ 1,250 CPU-h > 1,000.**
- **Decision (mechanical, by the order frozen in amendment v5.0 "Reduction order"):** step (1) "E7 skipped" is no longer
  available (E7 has run, ≈ 1 CPU-h), so step (2) applies: **test5 500 → 300 episodes per cell (indices 0–299)**,
  every method, all 5 cells. Projected total ≈ 975 CPU-h ≤ 1,000, so steps (3) drop S8 and (4) val3 500 → 300 are not
  applied. E5 (sub 16 on test5 0–199) is unchanged and lies inside 0–299.
- **Blindness.** Decided before any test5 episode of any method and before any round-2 student or D5 read-out exists
  (round-2 distillation is still running); it depends only on wall-time records. Every number on test5 is reported
  with n = 300 per cell and the reason for the size.
- Compute is free (public-repo GitHub-hosted runners); the reduction also shortens wall time (≈ 1,750 → ≈ 1,050 test5
  jobs, ≈ 13 h at 20 concurrent) toward the stage-20 date of 2026-12-01.

## Addendum v5.1f — E6 latency on runners, g_T for H2-v5, test5 read-out script (run 35, before any test5 number is read)
- **E6 machine.** Amendment v5.0 put E6 in the sandbox ("same machine, one session"). Measured in run 35: on the
  sandbox one full-G\* decision (2,000 / 512 / 64) takes ≈ 3.7 s, and the Lat′ driver is itself a full G\*, so 25
  students × 520 decisions do not fit one session (≈ 27 h). E6 therefore runs on GitHub-hosted runners
  (`experiments/v5_e6_lat.json`), keeping "same machine" where a comparison is made: per cell, **one job times student
  701, full G\* and the two reduced G\* configs of v4 E5 (g125_512_16, g500_512_4) interleaved on the same pilot3
  decision states** (the latency–accuracy frontier is read within that job); a second job per cell times students
  702–705 (student timers only; seed spread of student latency). Cross-cell latency is reported per runner, not
  compared as if on one machine. Protocol otherwise the v3 Lat′ one (500 decisions after 20 warm-up, pilot3, single
  thread). New opt-in CLI flags `latency3 --configs … --no-pruned` (defaults leave the v3 protocol unchanged; test in
  `tests/test_v5.py`). The accuracy side of the frontier is test5 success / BI (G\*, students) and, for the reduced
  configs, the v4 E5 rows only where they exist (S12); no new reduced-G\* accuracy runs are added in v5.
- **g_T (H2-v5).** `gt3` (J 16, L 4095, no grid, histories rebuilt from the recorded actions) costs ≈ 0.08 s per
  episode in the sandbox, so it is run in the sandbox on every test5 record of G\*, students, RL and rl_success after
  a cell's test5 is complete, outputs `results/v5/test5_gt/`.
- **Read-out script** `code/analysis_test5_v5.py` (synthetic test `tests/test_v5_test5_analysis.py`) implements the
  frozen H5a / H5b / H2-v5 / baseline / Holm rules; it fixes the two details the amendment left open: H5b weights =
  1 / bootstrap variance of each cell's Δ_succ (held fixed across replicates), and travel in radians (also reported per
  100°). A cell is analysed only when every method has all 300 test5 episodes.

## Addendum v5.1g — E6 job-1 extension (run 36, 2026-11-08; E6 is report-only, no hypothesis reads it)
- **Observed:** E6 job 1 (500 decisions) met the v3 Lat′ completeness rule (every bootstrap CI half-width ≤ 10 % of its
  median) only in A16-2. In S2 / S4 / S8 / S12 the full-G\* timings are multimodal across decision steps (e.g. S2
  quartiles 3.1 / 4.9 / 5.2 s), so the median CI is wide. Students' latency CIs pass everywhere.
- **Rule applied (pre-existing, v3 hypotheses table, Lat′ row):** "not complete → 500 more decisions". Because pooling
  two runners would break the "same machine" property of job 1, the four cells are re-timed in **one job each with
  1,000 decisions** (same pilot3 states order, same configs; `experiments/v5_e6_lat_d1000.json`). That record becomes
  the job-1 record (`analysis_e6_v5.py` prefers `<tag>_s701_gstar_d1000.jsonl`); the 500-decision records stay
  committed and are mentioned in the appendix. If a 1,000-decision CI still fails the 10 % rule, it is reported as is
  with its CI and the multimodality noted; no further extension.
