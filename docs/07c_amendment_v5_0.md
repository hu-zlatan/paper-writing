# Amendment v5.0 — REFINE from stage 20 → stage 13 (2026-11-06; written before any v5 run)

## Why
Stage 20 QUALITY_GATE (v4) scored 5.0 < 7.5 (`paper/mypaper/v4/20_quality_gate.json`). Its required actions are
evidence-level: one cell per regime, three learner seeds, an untuned RL comparator in S2, a re-used test split, an
evaluator not checked below sub 8, and S2 baselines limited to B-fan. On 2026-11-06 the owner told the pipeline to fix
these ("那你提升这里啊", in chat, reply to the run-29 summary) and the cap was raised to `max_refine_cycles: 4`. This is
refine cycle 4. All v3/v4 rows and verdicts stay as they are (`results/v3/`, `results/v4/`); v5 writes to `results/v5/`.

Scope is deliberately narrow (one question, more evidence): **is a cost-aware online planner (G\*) learnable by an
amortized student, and does the answer change with how much the planner travels?** Not in v5: belief-input / attention
heads, 3D objects, hardware, new planners.

## Rows (design frozen here; sizes may only go down, via the reduction order, after pilot P0)

**P0 · pilot and calibration (sandbox + Actions, report-only).**
- τ for each new cell by the v3 Cal′ rule (`calib3`, n\* = 4 unless stated, 200 cal3 episodes).
- Second library: A16 (set A, K = 16) at κ = 2, n\* by the unchanged v3 Cal′ rule (G\* at κ 0, τ 4 on the 200 cal3
  episodes, sub 8: success > 0.88 → 3, < 0.20 → 5, else 4; A with K = 8 is at ceiling, 0.985). The cell is kept only if
  G\* sub-8 success at that n\* is in [0.30, 0.90]; otherwise it is dropped and reported (no substitute library is chosen
  after seeing results). *(Edited 2026-11-06 before any v5 job: first draft used an ad-hoc n-scan; replaced by the
  existing rule.)*
- `pilot3` TIME_ESTIMATE per cell; G\* travel per episode on 20 pilot3 episodes (design info, not a paper number).

**Cells.** S2 (κ 2, τ 4.7), S4 (κ 4), S8 (κ 8), S12 (κ 12, τ 4.9), A16-2 (κ 2). Five cells spanning the travel range;
S2 and S12 re-run under the v5 recipe so every cell is comparable.

**E1 labels.** `label3`, 3,000 episodes per cell (indices 0–2,999; held-out 1,200–1,499). Existing v4 S2 and v3 S12
labels are re-used where generated with the same (set, κ, τ) and code path (training data only; checked by hash of the
labeller config).

**E2 students — one recipe in every cell.** Same DeepSets head and hp 0 as v3/v4. DAgger 2 rounds × 800 episodes
(β 0.5 then 0). Every round trains a fixed 200 epochs and **keeps the checkpoint with the lowest held-out label regret
R̄** (pre-declared response to the S2 over-fitting finding; the last-checkpoint variant is logged for every seed as a
sensitivity row). **5 seeds per cell** (701–705).

**E3 RL — tuned, then fixed.** (i) Sweep on S2 only: 8 configurations (log-uniform lr ∈ [3e-4, 3e-3], ent ∈ [1e-5,
1e-3], batch ∈ {64, 128, 256}; sampler seed 7) × 1 seed × 10⁵ episodes, selected by g_T on pilot3 0–199 (the v3 rule).
(ii) Selected config, `spce_total`, 5 seeds per cell (711–715), 2 × 10⁵ episodes. (iii) Probe-count control:
`rl_success` (terminal-success reward, same config) 5 seeds in S2 and S12 only, so the g_T/posterior inversion can be
separated from the three-probe collapse.

**E4 fresh test split `test5`.** New split salt (not used by any earlier split); 500 episodes per cell, indices
0–499. It is not evaluated for any method until every student and RL policy of that cell is frozen; the freeze commit
is recorded in PROGRESS before the first test5 job. Each (method, cell) is evaluated on test5 once. Methods per cell:
G\*, 5 students, 5 RL, random, B-fan, B-spread, B-cov (+ 5 rl_success in S2/S12). Sub 8 grid read-out; g_T without grid.

**E5 evaluator check.** G\* and student seed 701 on test5 S2 and S12, episodes 0–199, re-read at sub 16 (`regrid3
--sub 16`); success flip rate and mean |ΔBI| sub 8 → sub 16 reported, and every success contrast is reported next to
the measured flip rate.

**E6 latency.** `latency3` (Lat′ protocol) for students and the two reduced G\* configs on the sandbox, same machine,
one session; latency–accuracy frontier figure.

**E7 (optional, cost-capped) H3 full screen.** All 512 first actions in S2 and S12 on 32 g2v3 beliefs, plus an
independent re-estimate of the selected action to measure V_LA selection bias. Runs only if the P0 estimate is ≤ 60
CPU-h; otherwise 128 actions; otherwise skipped and stated.

## Decision rules (fixed now)
- **D5 per cell (val3 0–499, sub 8, best-checkpoint students):** the D4 rule, δ = 4 pp: pass iff (i) Δ̂_succ(student −
  G\*) ≥ max(−2 pp, −δ + 1.645·SE·√0.5), (ii) Δ̂_BI ≥ −0.15 nats, (iii) ≥ 4 of 5 seeds have Δ_succ > −δ.
- **H5a (learnability across regimes):** reported as "student within δ of G\* on validation in m of 5 cells", with the
  test5 Δ_succ and Δ_BI (crossed episode × seed bootstrap ci95) for every cell.
- **H5b (regime trend, the one cross-cell claim):** slope of test5 Δ_succ(student − G\*) on the cell's mean G\* travel
  (test5), weighted least squares over the 5 cells, ci95 from the crossed bootstrap. Claim "the gap grows with travel"
  only if the 95 % interval excludes 0 (and its sign is reported as measured); otherwise "no trend detected over 5 cells".
- **H2-v5:** per cell, g_T(student) − g_T(RL) one-sided 95 % LB > +0.10 nats → "distillation scores higher on RL's own
  objective". Also report g_T(G\*) − g_T(learner) with ci95 and the posterior-success ordering on test5; the inversion is
  claimed only in cells where both orderings have intervals excluding 0, and is checked against `rl_success`.
- **Baselines:** each cell's H\* is the best of B-fan / B-spread / B-cov on pilot3 0–199 (not test5); student vs H\* on
  test5 with ci95.
- Multiplicity: Holm across the 5 cells for the per-cell test5 student − G\* and student − H\* contrasts.

## Compute (estimate before P0; free GitHub-hosted runners, public repo)
Per newly labelled cell ≈ 16 (labels) + 33 (DAgger, 5 seeds) + 6 (RL) + 30 (val3) + 75 (test5) ≈ 160 CPU-h; S2/S12
re-use labels. Total ≈ 3 × 160 + 2 × 145 + 5 (RL sweep) + 10 (rl_success) + 15 (E5) + E7 ≤ 60 → **≈ 800–860 CPU-h**,
≈ 40–45 h wall at 20 concurrent single-thread jobs. Over the 12-h wall reading of `RESTRICTS.yaml`; the owner chose
this loop knowing it (2026-11-06), and the overrun is recorded, not hidden.

**Reduction order** if P0 projects > 1,000 CPU-h (applied in this order, recorded in amendment v5.1 before main runs):
(1) E7 skipped; (2) test5 500 → 300 episodes; (3) drop S8; (4) val3 500 → 300. Not reducible: 5 seeds per learner,
fresh test5, all four heuristic baselines, E5.

## Order
P0 → amendment v5.1 (τ, n\* for A16, sizes) → E1 → E2 r0 → r1 → r2 and E3 in parallel → D5 on val3 → freeze → E4 test5
→ E5, E6, E7 → stages 14 → 15 → 16–20. Target: RSS 2027 Stage 1 (2026-12-04 AoE) if v5 finishes stage 20 by
2026-12-01; otherwise v5 goes into the Stage-2 full paper / CoRL 2027 and the Stage-1 decision returns to the owner.
