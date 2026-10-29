# Amendment v3.0 (2026-10-29, run 5 — before any v3 code change or v3 run)

Freezes everything listed in `docs/07_hypotheses_v3.md` §6.1 before the first v3 run (pre-registration). Where an item
is "frozen as written", the cited section of `07_hypotheses_v3.md` (commit 14415bb) is the binding text; this file adds
only what that text leaves open, the integrity corrections required by `results/v2/15_decision.md` §3.5, and the two
discrepancies found in stage 8.5 v3. Values that can only be known after a gate (n\*, τ_κ, δ_c, ε_c, H★, R_b, H1-fb
activation, test sizes) are added later as dated **status notes** at the end of this file, each with the commit hash
of the data it rests on; the rules that produce them are frozen here and cannot change.

The commit that adds this file is the **pre-registration commit for v3**; its hash is recorded in PROGRESS.md.

---

## C1 — Action set (§1.2, item 1)
- 𝒜 = 64 φ′ (5.625° spacing, φ′ = i·2π/64) × 8 ψ ∈ {−35°, −25°, …, +35°} = 512 actions, index a = i_φ·8 + i_ψ, for
  every method, cell and row.
- Implementation: `touchbed/travel.py` reads the environment variable `TOUCHBED_NPHI` once at import (allowed: 32, 64;
  default 32). Every v3 job sets `TOUCHBED_NPHI=64` and records it in its output JSON; an output without it is not a v3
  result. Default 32 must reproduce the v2 32 × 8 results bit-for-bit (G0′ unit test on the v2 κ = 0/τ = 3 reproduction
  episode set and on `rung_subset`).
- Nested candidate subsets on 64 × 8: C = 512 (all), 128 = `rung_subset(32, 4)` (every 2nd φ′, ψ indices 0, 2, 5, 7),
  32 = `rung_subset(16, 2)` (every 4th φ′, ψ indices 2, 5). `rung_subset` becomes relative to the current N_PHI.
- 64 × 16 vs 64 × 8 at S12 on 300 pilot episodes (G\* only, same episodes): **reported only**. No further change of 𝒜.

## C2 — Evaluator (§1.2, item 2)
- `gridpost.AdaptiveGridPosterior`, sub = 4, as frozen by amendment v2.0 B8 (MAP identity, Nelder–Mead pose, ball mass
  with PF floor 1/(2·32,000)); histories rebuilt exactly from recorded actions and observation streams.
- Tie band, **pre-registered here** (it was post hoc in v2, 15_decision §3.5 item 6): a success flip between two
  evaluator settings counts only if the episode's true-identity mass is outside [0.45, 0.55] under both settings.
- Gate E′ (07_hypotheses_v3 §4): sub 4 vs sub 8 on 8 S12 + 8 A12 pilot episodes (4 G\*, 4 B-fan each, from the first
  G5′ shard). Pass: mean |ΔBI| ≤ 0.02 nats and no success flip outside the tie band. Fail → sub = 8 for every v3 number,
  and its measured cost enters the downscale order (C5).

## C3 — Cells and informative-cell rule (§1.2, §1.4, item 3)
- Primary cells {S0, S12, A12} (set S/A at κ = 0 or 12); κ_hi = 12; no κ = 6 cells. A0 is re-checked once on the v3
  calibration under v2 §1.7 and enters as a fourth primary cell only if informative there (decided at G5′, before any
  test episode).
- Rules I1, I2, I3 frozen as written in §1.4. No other informative-cell rule exists.

## C4 — Calibration (§1.2, item 4)
- n\* per set: the κ = 0, τ = 4 rule of v2 §1.2, recomputed on 64 × 8. τ_κ per cell: v2 §1.2 probe-matched rule. 200
  calibration episodes per cell (split `cal3`). Pass: verified mean probes within n\* ± 0.3. ≤ 3 bisection steps on τ_κ;
  still failing → the cell is removed (I1).

## C5 — Episode streams, sizes, power rule, downscale order (§1.3, §7, item 5)
- New split names with new salts, added to `evaluate.SPLIT_SALT` (existing entries unchanged):
  `cal3` 61, `pilot3` 67, `val3` 71, `test3` 79, `label3` 83 (round-0 teacher rollouts), `dagger3` 89 (DAgger student
  rollouts), `g2v3` 97 (H3 beliefs), `bank3` 101 (G1′ (b)). Episode i of split s on set X uses
  `stream("state", X, s, salt, i)` (unchanged function), so v3 streams are disjoint from all v2 streams by key.
- Sizes as the table in §1.3. Paired designs use the same episode indices for every method in a cell.
- Power rule (§4): if the projected SE_test of a cell's D3-based success contrast exceeds δ_c/2.5, that cell's test grows
  1,000 → 2,000 episodes (indices 1,000–1,999 of `test3`), at most 2 cells, decided at the freeze commit.
- Downscale order exactly as §7 (abs-frame row → random sanity 100→50 → success-vs-probe curve → Gen-κ → BC/RL success
  reads 300→200). Never reduced: student seeds, cells, 1,000-episode tests, G\* test, H★ test, R_b test, H2 g_T test.

## C6 — Margins (§1.5, item 6)
- δ_c = min(4 pp, 0.15·D_c); ε_c = min(0.05·BI_c(G\*), 0.15·D_c^BI) nats; G\* on 500 and random on 200 `pilot3`
  episodes per cell. Values added by a status note after G5′.

## C7 — Distillation recipe (§2.1, §1.6, item 7)
- Student: `relframe.RelDeepSets` finger-relative head, context dim 5, hidden sizes as v2 (`train_v2` defaults), 512
  relative actions with feasibility mask; belief-free input (touch history, finger angle, τ_rem/τ).
- Label format (per decision, stored as `.npz`): history (actions, observations), finger angle, τ_rem, feasibility mask
  (bool[512]), score vector s (float32[512], s(a) = max(0, EIG_B(a; b))/c(a) on feasible a, 0 elsewhere) from G\* at
  N = 2,000, M = 64, G\*'s chosen action, episode key. `GStar.score_vector()` must satisfy argmax = `GStar.act` on the
  same RNG state (G0′ test).
- Loss: CE(student logits, softmax(β_T·s/σ_s) over feasible a) + λ·CE(student logits, argmax of s); σ_s = per-decision
  SD of s over feasible a; if σ_s < 10⁻⁶ the soft target is uniform over the argmax set.
- Data: round 0 = 1,500 G\* rollouts per cell (`label3`, indices 0–1,499), every decision labelled, shared by all seeds
  of the cell; episodes 1,200–1,499 are the held-out validation-regret set (20 %). DAgger round 1: 400 student rollouts
  per seed (`dagger3`, indices seed-specific: 1,000·r + 400·(seed−501) + j), each decision executes G\*'s action with
  probability 0.5 (β_DAgger = 0.5); round 2: 400 rollouts, β_DAgger = 0. G\* labels at every visited belief (decision PF
  N = 2,000 run alongside). Data aggregated; each round restarts from the previous round's weights.
- Regret metric (§1.6): floored normalised regret r = (s_max − s(a_π)) / max(s_max − s_med, ρ·s_max), ρ = 0.05;
  decisions with s_max = 0 excluded and counted; tie decisions (s_max − s_med < ρ·s_max) reported as a fraction.
  Teacher noise floor on 200 validation beliefs as §1.6.
- Stop: per round, validation R̄ after every epoch; stop when it improves by < 0.005 over 3 consecutive evaluations; hard
  cap 50 epochs; last checkpoint; no success-based selection.
- HP grid (1 seed = 501, S12, round 0 only, selected on held-out R̄; ties within 0.01 → lower index):
  config 0 (lr 1e-3, β_T 4, λ 0.5, batch 256); 1 (3e-4, 4, 0.5, 256); 2 (1e-3, 16, 0.5, 256); 3 (1e-3, 4, 0, 512).
  Adam, no weight decay, gradient-norm clip 1.0 (as `train_v2`). The chosen config is used in every cell and row.

## C8 — Seeds (§1.3, item 8)
- Student: 501–505 per primary cell (S12 seeds 501–503 are the D3 students, reused without retraining).
- RL-relative (H2): 511–513 (S12). Belief-input student: 521–523 (S12). Absolute-frame student: 531–533 (S12).
  BC-only: the round-0 checkpoints of student seeds 501–503 at S12 (no separate training; BC = round 0, no DAgger).
- v2 seeds 100–102, 200–202, 300–301, 400–402 are never reused. Deterministic methods use one RNG stream per episode
  (`stream("policy", …)` as in v2).

## C9 — Comparator settings and rows (§2.2, item 9)
- RL-relative, belief-input student (48 PF-summary features: per identity k = 1…8, (w_k, weighted mean x, y, weighted
  SD x, y, resultant length of |G_k|·θ), plus the relative context), BC-only, absolute-frame student
  (`train_v2.CategoricalDeepSets`, same recipe), Gen-κ row, success-vs-probe curve: frozen as written in §2.2.

## C10 — Heuristics (§1.7, item 10)
- B-spread, B-fan, B-cov with the budget reservation rule c(a) ≤ τ_rem − max(0, n\* − t − 1); H★(c) = highest success
  on the 200 `pilot3` episodes of cell c (ties B-spread < B-fan < B-cov). Frozen as written in §1.7.

## C11 — Greedy grid, latency, R_b, H1-fb (§1.8, §3.2, item 11)
- 27 configurations N ∈ {2,000, 500, 125} × C ∈ {512, 128, 32} (subsets C1) × M ∈ {64, 16, 4}; per-decision latency
  L_dec split into t_assim, t_nb, t_score, t_select (greedy) and t_feat, t_fwd, t_mask (student); L_ep and L_final as
  §1.8; protocol v2 §2.3 extended (one pinned core, BLAS threads = 1, interleaved, 20 warm-up + 500 timed decisions,
  +500 if any CI half-width > 10 % of its median). R_b rule incl. "grid floor" (125, 32, 4) as §1.8.
- The "≥ 100×" claim is per decision and is a **constants statement at these sizes**, not an asymptotic separation
  (07b_theoretical_bounds_v3 §2.3); the paper says so.
- H1-fb (pruned-16: student top-16 + G\* re-scoring), its activation rule, the ≥ 10× measured latency-ratio rule and the
  random-16 control: frozen as written in §3.2. Stage 8.5 op counts put pruned-16 at ≈ 11× (N² neighbour lists
  dominate); activation is decided by Lat′ measurements only.
- The student's implementation re-encodes the full relative history each decision (O(T²·H² + T·H·A)); this is what is
  timed. No incremental encoder is added after seeing latencies.

## C12 — H3 (§3.4, item 12)
- Estimator code unchanged from the v2 G1/G2 runs (`lookahead.lookahead_gap` via `g2.py`, CRN, C1 = 32 screened incl.
  structured set-up moves, M_outer = 64, top 4 + G\*'s action re-estimated with 4 × 64 samples).
- **Correction (stage 8.5 v3 finding; documentation only, no code change):** `07_hypotheses_v3` §3.4 and amendment v2.0
  B6 say the rollouts are completed by "G\*, M = 64". The code that produced the validated v2 G1/G2 numbers calls
  `lookahead_gap(..., greedy_M=0)`, so rollouts are completed by the `TouchbedProblem` default greedy: belief =
  N_LA = 500 particles resampled from G\*'s decision PF (no MH inside rollouts), 128 candidates (`rung_subset(16, 8)`,
  i.e. 16 φ′ × 8 ψ; on 64 × 8 this is every 4th φ′), M = 16, cost-aware, feasible-restricted — as the
  `lookahead_tb.py` docstring states. The v2 G(κ) numbers rest on these settings and the v3 measurement keeps them, so
  H3 measures one-step-deviation headroom over **this reduced greedy completion**; the paper states the settings. The
  bias check of §3.4 (estimator V_G\* vs an independent 4×-sample full G\* rollout on 20 S12 beliefs) is the guard; its
  rule is unchanged.
- κ ∈ {0, 2, 12}, set S, 100 beliefs each (`g2v3`), uniform step in {0, …, n\*−1}; notch (5 runs), zero-gap bank
  (100 beliefs, `bank3`), travel-notch control (G1′ (c)), outcome regions Kill/Hold/Inconclusive: frozen as §3.4 and §4.

## C13 — Tests and labels (§1.9, §3, §5, item 13)
- Frozen as written: crossed episode × seed bootstrap, B = 10,000, one-sided α = 0.05, intersection–union across cells,
  Holm only within the reported-rows family, TOST reported only; label vocabulary of §6.2; outcome rows of §5.

## C14 — Integrity corrections (15_decision §3.5, item 14)
1. Amendment v2.0 B5 quotes the S diagnostic as +0.007; the JSON (`results/v2/12_g4_b5_analysis.json`,
   `S_k0_random_30mh_vs_128k3mh`) gives **−0.0066**. The JSON value is the correct one; B5's text is superseded.
2. The G4 note used a 2 pp point tolerance; the pre-registered rule is |Δsuccess| ≤ 1 pp with the 95 % CI inside ±2 pp,
   and all four success CIs leave ±2 pp. G4 is reported as failed under the pre-registered rule.
3. The B8 note quoted 0.006–0.014 as 0.006–0.019 (partial data) and "S random 250" where the JSON has 300; the final
   JSON values are binding.
4. `12_g3_notch_analysis.json` and `12_g3_hp_selection.txt` had no producing script. G0′ adds
   `code/analysis_g3_notch.py` and `code/analysis_g3_hp.py`; each must reproduce its file from the committed raw
   outputs or write a diff that is reported. Until then, neither file is quoted.
5. Run-4 numbers absent from any JSON (validation ball-sPCE 4.85 / 5.03 / 4.96; travel 0.54–0.63 rad; remedy plateau
   episodes) are not quoted unless a script extracts them from the raw logs into a committed JSON.
6. Two post-observation rule changes of v2 — the B2 per-shape rule and the B8 tie band — are stated in the paper as post
   hoc. (The tie band is pre-registered for v3 in C2.)
7. The 14_analysis area-chair rewrites (rows 1–17) are binding wording for any v3 text citing v2 numbers.
8. (New, stage 8.5 v3) H3 completion settings: see C12.
9. (New, stage 8.5 v3) The two informal G\* latency figures in the record (0.840 s per decision on 256 actions,
   15_decision §3.4; "≈ 2.3 s per decision at M = 32", PROGRESS stage 10 v2) were not taken under the latency protocol
   and are not quoted; Lat′ supersedes both.
- Every v2 learned-policy number is validation/pilot; κ = 0/6 diagnostics and relative-head seeds 400–402 are
  exploratory and are never promoted to confirmatory.

## C15 — Deviations from 15_decision §4 (item 15)
As listed in `07_hypotheses_v3` §0.2: HP selection by floored normalised regret (not top-1 agreement); tightened D3
rule; three heuristic baselines; G\* pilot 500 per cell; 27-configuration greedy grid instead of the 8-rung ladder; RL
comparator E_train = 2 × 10⁵ from the start; H3 hold threshold 0.03 with partitioned outcome regions. Added here: the
`TOUCHBED_NPHI` flag mechanism (C1), split salts (C5), seed IDs (C8), and the C12 correction.

---

## Status notes
(added after gates, dated, each citing the commit hash of the data used)

### 2026-10-29 (run 6) — Cal′ and G1′
- **Cal′ n\*** (data commit 949d247, `results/v3/12_cal_analysis.json`): S: G\* success 0.605 at κ = 0, τ = 4 on 200
  cal3 → **n\* = 4**; A: 0.985 > 0.88 → **n\* = 3**. τ_0 = n\*: **S0 τ = 4**, A0 τ = 3.
- **τ_12** (same file, regenerated at 635d045 after including the n\* = 3 shards): **S12 τ = 4.9** (n\* 4, mean travel
  0.939, 200 cal3); **A12 τ = 3.3** (n\* 3, mean travel 0.260, 200 cal3). The speculative A12 n\* = 4 value (τ 5.0) is
  kept in the JSON and not used.
- **Verification:** S12 at τ 4.9: mean executed probes **3.96** (200 cal3) — within 4 ± 0.3, **pass**. S0 at τ = n\* = 4
  with κ = 0: every episode executes exactly 4 probes (mean 4.0 on the 200 n\* episodes) — pass by construction. A12 at
  τ 3.3: dispatched (`experiments/v3_cal_verify_A.json`).
- **G1′** (`results/v3/12_g1_analysis.json`, all files complete): (a) notch mean 0.829 ∈ [0.573, 0.860] — pass;
  (b) zero-gap bank, 100 beliefs, mean 0.0025, UB 0.0037 — pass; (c) travel-notch exact 0.717, mean estimate 0.744
  ∈ ±20 % — pass. As recorded at stage 10, (c) checks the estimator's travel/feasibility handling; it does not show
  travel-created headroom.
- **Cal′ A12 verification** (Actions run 40839618917): mean executed probes **2.98** on the 200 cal3 episodes at
  τ 3.3 — within 3 ± 0.3, **pass**. Cal′ is complete for S0, S12, A12 (A0 not run; it enters only via the reserve, v3.1 D3).
- **E′** (Actions run 40844118214, `results/v3/12_e_analysis.json`): 16 episodes (S12/A12 × G\*/B-fan × 4). Mean |ΔBI|
  0.0126 nats (≤ 0.02, max 0.052), but **one counted success flip** (A12 B-fan episode 1: sub 4 fail → sub 8 success,
  true-identity mass 0.228 under both settings, i.e. outside the tie band); a second flip (S12 B-fan episode 3) is inside
  the tie band (mass 0.4999) and does not count. **E′ FAILS → sub = 8 for every v3 number** (C2). Measured sub-8
  read-out cost: 40.6 s per episode on these 16 (3.6 × the recorded sub-4 eval3 wall time); a random-policy episode at
  sub 8 did not finish within the 5-minute sandbox pilot (sub 4 on the runner: 120 s). All v3 evaluator numbers already
  taken at sub 4 (Cal′ n\* success, G5′ pilot) are re-read at sub 8 with `regrid3` (histories rebuilt exactly; the
  sandbox re-read reproduces the runner's E′ values bit-for-bit) and the gates are decided on the sub-8 values.
- **τ_2 = 4.7** (descriptive H3 level; 200 cal3, n\* 4, mean travel 0.726; same rule as τ_12).
- **HP config** (Actions run 40846478310, `results/v3/hp/`): held-out R̄ (label3 1,200–1,499, 1,196 decisions, 3
  excluded): cfg 0 **0.3827**, cfg 1 0.4194, cfg 2 0.3832, cfg 3 0.3872; cfg 0, 2, 3 within 0.01 of the best → lowest
  index → **config 0** (lr 1e-3, β_T 4, λ 0.5, batch 256). Every round-0 run stopped by the frozen stop rule after 4–5
  epochs. Seeds 502/503 round 0 trained in the sandbox with config 0 (R̄ 0.3867 / 0.3846; env recorded in the JSON).
- **RL sweep validation set (recorded before the sweep, run 6):** v3.1 D9 names "500 `val3` episodes"; the trainer
  (`train_v2.Trainer.validate`) validates on its own fixed 500-episode stream (`stream("val_v2", set, κ, τ)`, states from
  the same prior). The sweep uses the trainer's set unchanged (no code change to the trainer); stated as a deviation.
