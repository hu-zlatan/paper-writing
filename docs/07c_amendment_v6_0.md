# Amendment v6.0 — REFINE from stage 20 → stage 13 (2026-11-10; written before any v6 run)

## Why
Stage 20 QUALITY_GATE (v5) scored 5.5 < 7.5 (`paper/mypaper/v5/20_quality_gate.json`), with 8 evidence-level required
actions. On 2026-11-10 the owner chose to open v6 for new experiments ("开 v6", in chat, reply to the run-41 summary)
and raised `max_refine_cycles` 4 → 5 (AUTOPILOT §1). This is refine cycle 5. Every v3 / v4 / v5 row and verdict stays as
it is (`results/v3/`–`results/v5/`); v6 writes to `results/v6/`. Nothing below re-tests a v5 decision rule on the data
that produced it: v5's D5 / H5a / H5b verdicts stand as recorded.

Scope (one question, the gate's sharpest points): **is a learned student a better fast policy than simply shrinking
the planner, does it match G\* once the teacher's own variance and enough test episodes are counted, and do the DAgger
rounds add anything over behaviour cloning?** Not in v6: new cells, new shape libraries, per-cell RL re-tuning, a new
heuristic, hardware. These stay limitations.

## Data
- **test5 episodes 300–499** are fresh: no method has been evaluated on them (checked 2026-11-10: max evaluated test5
  index = 299). Episodes 0–299 were seen in v5. Every v6 contrast is computed on **0–499** (the size v5.0 E4 originally
  registered, before the v5.1e compute reduction) **and, separately, on the fresh 300–499 alone**; both are reported.
- Frozen policies only: v5 students (`results/v5/d5/<cell>_s70x_r2.npz` and the round-0 checkpoints `_r0.npz`), v5 RL
  cfg 6 seeds 711–715, rl_success (S2 / S12), weight hashes as in `results/v5/13_freeze.json`. No training in v6.
- Same evaluator (sub 8 grid read-out), same `eval3` command and episode keys as v5 test5.

## Rows (design frozen here; sizes may only go down, via the reduction order, after the P6 timing check)
- **E8 · test5 extension.** Episodes 300–499 for G\* (run 1, default streams), 5 students (r2), 5 RL, the three
  heuristics, and rl_success (S2 / S12). Random is **not** extended (it enters no contrast; ≈ 620–820 s per episode).
  g_T (`gt3`, J 16, L 4095) on every new record of G\*, students, RL and rl_success.
- **E9 · reduced planners on test5.** `g125_512_16` and `g500_512_4` (the two configurations timed in v5 E6), episodes
  0–499, all five cells. This is the accuracy side of the v5.0 E6 latency–accuracy frontier.
- **E10 · second G\* run.** G\* with `eval3 --run-salt r1` (new opt-in flag: the policy and decision-PF streams are
  salted; state, start angle and observation streams unchanged; the default reproduces v5 exactly — `tests/test_v6.py`),
  episodes 0–499, all five cells.
- **E11 · DAgger vs behaviour cloning.** The round-0 (behaviour-cloning) student checkpoints `_r0.npz`, seeds 701–705,
  episodes 0–499, all five cells.
- **E12 · evaluator check, all cells.** `regrid3 --sub 16` on test5 episodes 0–99 for G\* run 1 and the five r2 students
  in all five cells (v5 E5 records re-used where they exist).

## Decision rules (fixed now)
All contrasts: crossed episode × seed bootstrap (`touchbed.stats.crossed_bootstrap_diff`, B = 10,000), success (sub 8)
first, BI beside it; on 0–499 (primary) and on 300–499 (fresh check).
- **H6a — student vs G\* with teacher variance.** Δ = student(5 seeds) − G\*(runs 1 and 2 as two "seeds"), per cell.
  (i) Difference: two-sided ci95, Holm over 5 cells. (ii) Equivalence (TOST) at δ = 4 pp: per cell p_TOST = max of the
  two one-sided bootstrap p-values against −δ and +δ; Holm over 5 cells; "equivalent within 4 pp" only where Holm
  rejects. Otherwise "neither a difference nor equivalence shown". No pooled estimate. (Design note, not a threshold:
  at v5's test5 spread, 500 episodes give a 90 % half-width of roughly 3.5–4 pp, so equivalence can be shown only if
  the point gap is near 0.)
- **H6b — student vs reduced planner.** Per cell, student − g125_512_16 and student − g500_512_4 success, two-sided ci95,
  Holm over the 10 contrasts. "The student is more accurate than a reduced planner of that latency" only where Holm
  rejects with a positive sign; a negative significant sign is reported as such. The frontier figure: per cell, E6
  job-1 median decision latency (v5, unchanged) against test5 0–499 success for G\*, both reduced configurations and
  the student; no new timing.
- **H6c — DAgger rounds vs behaviour cloning.** Per cell, student r2 − student r0 success (5 seeds each), two-sided
  ci95, Holm over 5 cells. "DAgger improves success over BC" only where Holm rejects with a positive sign; otherwise
  "not detected".
- **E12 (report-only).** Per cell: sub-8 → sub-16 success flip rate for G\* and for the students, and the student − G\*
  (run 1) success contrast on episodes 0–99 at sub 8 and at sub 16, with ci95.
- **Report-only updates on 0–499:** H5b slope (same WLS rule), student − H\* and student − RL success, H2-v5 g_T
  contrasts and the inversion check (same code). They are labelled "v6 update of a v5 row" and do not replace v5 verdicts.
- Agreement ceiling: per cell, the fraction of decisions where G\* run 2's action equals run 1's on the same episode
  prefix is **not** computable from eval3 records (the trajectories diverge after the first differing action), so only
  the first-decision agreement (identical state at step 0) is reported, report-only.

## Compute (estimate before P6, from v5 test5 wall times; free GitHub-hosted runners, public repo)
E8 ≈ 230 CPU-h · E9 ≈ 65 · E10 ≈ 30 · E11 ≈ 140 · E12 ≈ 180 → **≈ 645 CPU-h**, ≈ 32 h wall at 20 runners (shared with
paper 2). **P6:** before the main dispatch, a timing pilot of E9 / E10 / E11 / E12 on 2 episodes each (pilot3, S2 and
A16-2) gives a TIME_ESTIMATE; no test5 episode is used by it.
**Reduction order** if P6 projects > 800 CPU-h (in this order, recorded in an addendum before the main dispatch):
(1) E12 → G\* + student 701 only; (2) E11 → seeds 701–703; (3) E8 heuristics → H\* only; (4) E9 → g125_512_16 only.
Not reducible: E8 for G\* / students / RL, E10.

## Order
P6 → addendum v6.1 (sizes) → E8–E12 in parallel → freeze note (no training, so the freeze is the set of files) →
`code/analysis_v6.py` (written and committed before the first E8–E12 record is read) → stage 14 v6.

## Addendum v6.1 — sizes after P6 (2026-11-10, before any E8–E12 job)
- **P6** (`experiments/v6_p6.json`, Actions run 193; `results/v6/p6/`): pilot3 episodes 0–2 on single runners. Wall
  per episode (s): S2 g125_512_16 21 / 25 / 27, g500_512_4 33 / 12 / 76, G\* --run-salt 24 / 21 / 91, round-0 student
  9 / 13 / 51; A16-2 g500_512_4 91 / 78 / 47, G\* --run-salt 46 / 133 / 34; sub-16 re-read (S2, 3 v5 G\* episodes)
  226 / 59 / 25. Consistent with the v5 test5 means (grid read-out dominates), so the estimate uses the v5 per-method
  means and 245 s per sub-16 episode (v5 E5).
- **TIME_ESTIMATE:** E8 302 · E9 67 · E10 33 · E11 154 · E12 177 → **≈ 733 CPU-h ≤ 800 → no reduction step applies**;
  all rows at the v6.0 sizes. Over the 12-h wall reading of `RESTRICTS.yaml`, as in v5; the owner chose this loop.
- **Manifests** (`code/tools_v6_manifests.py`; v5 test5 commands with new ranges / methods / outputs, ≈ 17-min jobs):
  E8 1,169 jobs (`v6_e8_p0–p4`), E9 250 (`v6_e9_p0`), E10 125 (`v6_e10_p0`), E11 590 (`v6_e11_p0–p2`), E12 650
  (`v6_e12_p0–p2`). Dispatched in waves (the shared 20-runner cap; GitHub drops jobs queued > 24 h), in this order:
  E9, E10, E8, E11, E12. Time-guard stops are resumed with the same commands on the remaining episodes.
- g_T (`gt3`) on every new E8 record of G\*, students, RL, rl_success, one job per file after they land.
