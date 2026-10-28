# Stage 8 · HYPOTHESIS_GEN v3 — final hypotheses (Pass 3 Methodologist, fresh subagent, 2026-10-28)

> System: "You are a methodology lead synthesizing a proposer and a skeptic into final, defensible hypotheses."
> Task (verbatim template): "Produce the final hypothesis set, addressing every critique. For each surviving hypothesis
> include: rationale, measurable prediction (with concrete metric and threshold), failure condition (with concrete metric
> and threshold), and the experiment design sketch (datasets / baselines / ablations needed)."
> `{proposer_output}` = `docs/07a_proposer_v3.md`; `{skeptic_output}` = `docs/07b_skeptic_v3.md` (both read in full).
> Context read: `results/v2/15_decision.md`, `results/v2/14_analysis.md` (incl. the AC table), `docs/07_hypotheses_v2.md`,
> `docs/07c_amendment_v2_0.md` (B8), `results/v2/12_diag_analysis.json`, and `code/touchbed/` (`travel.py`,
> `policies_v2.py`, `relframe.py`, `latency.py`, `stats.py`, `lookahead.py`, `notch.py`, `gridpost.py`).
> Nothing was run. Every number is quoted with its source; numbers marked **[derived]** are arithmetic on quoted numbers.
> Thresholds are pre-registration values, not results.

`docs/07_hypotheses_v2.md` stays untouched as the v2 record. This file is the canonical v3 hypothesis set. It binds only
after `docs/07c_amendment_v3_0.md` (§6.1 list) is committed with a hash recorded in `PROGRESS.md`, before any v3 run.

**Status of this loop.** v3 is the last loop before escalation to the owner (15_decision §4.6). Every outcome of every
pre-registered test maps to a pre-written paper statement (§5). No outcome triggers a fourth design.

---

## 0. Outcome of the debate

### 0.1 Verdicts and final form

| Proposer item | Skeptic verdict | Final form (this file) |
|---|---|---|
| H1 (a) NI to G\*, (b) latency, (c) regret mechanism | REVISE | **H1a** NI kept (one rule for informative cells, §1.4). **H1b** latency at the student's accuracy against the best *Pareto* greedy configuration over (N, C, M), with a rule for an empty set, measured component split, per-episode latency reported (§1.8). **H1c (new)**: the best of three pre-registered non-random heuristics must be *demonstrably* outside the margin where the student passes (§1.7). The proposer's H1c (first-action split, R̄ ≤ 0.25) is withdrawn; regret becomes a selection metric with a floor (§1.6) and a descriptive read-out. |
| D3 learnability gate | (in H1) REVISE | D3 applies the test's own lower-bound rule with the projected test SE, floored at the skeptic's −2 pp / −0.15 nats (§4). G\* pilot ≥ 500 episodes. |
| H1-fb student-pruned greedy | REVISE | Kept as a **conditionally registered** fallback: active only if the measured latency ratio (gate Lat′, before any accuracy number) is ≥ 10. Random-16 pruning control added (§3.2). |
| H2 RL failure = optimisation | REVISE | **Re-centred on RL's own objective:** student vs RL on ball-sPCE g_T, the quantity PPO maximises (§3.3). Success contrast becomes a reported row. Fail-branch wording requires a label-fit check **and** a belief-input control. |
| H3 small headroom on 64 × 8 | REVISE | Units stated (relative, dimensionless). Outcome regions partitioned on LB/UB with precedence. Hold threshold tightened to UB95 < 0.03. κ = 2 descriptive. "Near-optimal" banned. Second instrument check (travel-notch) and an on-belief bias check added (§3.4). |
| Outcome map | REVISE | Title renamed. Row for "heuristic also non-inferior" added. Row 4's evaluator finding labelled a methods note (§5). |

Two core ideas remain ("sushi, not curry"):
- **Idea A: amortize the validated cost-aware greedy teacher G\* by supervised DAgger** (H1 = claim, H2 = its mechanism
  contrast against RL, H1-fb = pre-registered fallback inside Idea A).
- **Idea B: one-step rollout headroom over G\* under travel cost is small** (H3, a characterisation with a kill
  condition; it is the reason the teacher is greedy and not a planner).

### 0.2 v2 → v3 change log (cites `results/v2/15_decision.md`)

- **PIVOT** (15_decision §1): Idea 2 (learned look-ahead) is refuted in the tested range (G1 pass, G2 fail,
  G(12) = 0.0146, UB 0.0208). RL on ball-sPCE fails learnability G3 after its remedy (S12 success 0.204 → 0.243 vs
  G\* 0.410, 500 validation episodes). Both v2 hypotheses are retired as claims; their numbers are reported as findings.
- **Global changes** from 15_decision §4.1, all methods: 𝒜 = 64 φ′ × 8 ψ = 512 (the pre-registered flatness consequence
  of G5, ΔBI +0.170 > 0.10 at S12, applied once); adaptive grid evaluator, sub = 4, with the tie-band rule written in;
  primary cells {S0, S12, A12}; κ_hi = 12; n\*, τ_κ re-calibrated on 64 × 8.
- **Deviations from the 15_decision text** (recorded in amendment v3.0): HP selection by floored normalised regret, not
  top-1 agreement (§1.6); D3 rule tightened (§4); three heuristic baselines added (§1.7); G\* pilot 500 episodes per
  primary cell (was 300); greedy comparator is a 27-configuration (N, C, M) grid, not the 8-rung ladder (§1.8); RL
  comparator gets E_train = 2 × 10⁵ from the start; C1 hold threshold 0.05 → 0.03 and partitioned outcome regions (§3.4).

### 0.3 Evidence base (all validation/pilot, never test; AC wording of 14_analysis is binding)

- **Teacher headroom (32 × 8, voided action set):** G(12) = 0.0146 (UB95 0.0208), G(0) = 0.0049 (UB 0.0071); absolute
  0.015–0.049 nats on 2.6–3.0 nats of remaining value (14_analysis §1.2). The look-ahead's choice differs from G\*'s on
  41–58 % of beliefs; the record does **not** separate near-ties from argmax-selection noise (AC row 3). Near-ties are
  therefore a *hypothesis* of this file, measured in §1.6, not a premise.
- **RL deficit, absolute head:** S12 0.190 / 0.230 / 0.192 vs G\* 0.410 (500 episodes); κ = 0 exploratory −23.5 / −25.0 pp
  at 4.0 vs 4.0 probes (separately trained seeds 300/301; AC row 2).
- **RL deficit, finger-relative head (exploratory, not pre-registered; `12_diag_analysis.json` k12.rel_sd400–402):**
  hp from v2, E_train 10⁵, S12, the same 200 validation episodes: success 0.305 / 0.365 / 0.290 vs G\* 0.440, i.e.
  Δ −13.5 [−21.0, −6.5], −7.5 [−15.5, +0.5], −15.0 [−22.0, −8.0] pp; mean 0.320, Δ −12.0 pp **[derived]**; BI 5.789 /
  6.069 / 5.739 vs 6.380; probes 3.0 / 3.57 / 3.0 vs 4.175; 32 distinct first φ per seed. Absolute 1× seeds on episodes
  0–199: 0.170 / 0.235 / 0.190 (15_decision §3.4, derived there). These seeds enter v3 only as context; the v3 RL row is
  retrained.
- **Three G\* S12 success numbers are never mixed:** 0.410 (500 validation), 0.440 (300 pilot / first 200 validation),
  0.385 (first 200 pilot).
- **Latency (informal, 15_decision §3.4):** G\* median 0.840 s per decision over 8,359 decisions on 32 × 8; learned policy
  ≈ 0.53 ms. The split of 0.840 s into PF assimilation and candidate scoring is **unmeasured**; v3 measures it (gate Lat′).

---

## 1. Global definitions

### 1.1 Reused by reference from `docs/07_hypotheses_v2.md`

§1.1 (objects, libraries A/S, observation model, ε-likelihood), §1.2 (travel model c(a) = 1 + κ·|Δφ|/π, feasibility,
episode end at τ_rem < 1, probe-matched τ_κ rule, n\* rule), §1.3 (success = identity ∧ 5 mm ∧ 5° mod symmetry; ball
information BI in nats with cap −log P(B)), §1.4 (G\* = argmax over feasible a of EIG_B(a; b)/c(a), online PF N = 2,000,
M = 64; ball-sPCE definition, L = 4095, J = 16), §1.7 (non-degeneracy: success(G\*) ∈ [0.15, 0.90], D_c ≥ 20 pp, BI
saturation < 50 %), §1.8 (crossed episode × seed bootstrap, B = 10,000, one-sided 95 % percentile bounds),
§2.3 latency protocol (one pinned core, OMP/MKL/OPENBLAS = 1, interleaved timing, 20 warm-up + 500 timed decisions).

### 1.2 v3 changes (frozen in amendment v3.0)

- **Action set.** 𝒜 = 64 φ′ (5.625° spacing) × 8 ψ ∈ {−35°, −25°, …, +35°} = 512 actions for every method
  (`travel.py` N_PHI 32 → 64 behind a flag; 32 × 8 stays reproducible by unit test). The 64 × 8 vs 64 × 16 comparison
  at S12 on 300 pilot episodes is **reported only**; there is no further 𝒜 change.
- **Evaluator.** `gridpost.AdaptiveGridPosterior`, sub = 4 (07c v2 B8): histories rebuilt exactly from recorded actions
  and observation streams; MAP identity, Nelder–Mead pose, ball mass with PF floor convention 1/(2·32,000). Tie-band
  rule, now pre-registered: success flips between evaluator settings count only for episodes whose true-identity mass
  is outside [0.45, 0.55] under both settings. Checked at κ_hi by gate E′.
- **Cells.** Primary {S0, S12, A12}. A0 is re-checked once under §1.7 on the v3 calibration and enters only if
  informative. κ_hi = 12; no κ = 6 cells.
- **Calibration.** n\* per set and τ_κ per cell re-calibrated on 64 × 8 with the v2 §1.2 rule (gate Cal′).

### 1.3 Episodes, seeds, unit

- **Episode streams** carry a "v3" salt and are disjoint from every v2 stream and from each other.

  | Set | Size per cell | Used by |
  |---|---|---|
  | Calibration | 200 | Cal′ (n\*, τ_κ) |
  | Pilot | G\* 500; random 200; each heuristic 200; greedy-grid candidates 200 (S12 only) | G5′, margins, H★ and R_b selection |
  | Validation | 500 | D3 (and D3-B on its first 300) |
  | Test | 1,000 paired (power rule: up to 2,000 in ≤ 2 cells) | H1a, H1b, G\* |
  | Test subsets | first 500: H★ (H1c), H2 g_T, BC/abs/RL success rows use the first 300; random sanity first 100 | rows |

- **Seeds** (IDs frozen in amendment; v2 seeds 100–102, 200–202, 300–301, 400–402 are never reused): student 5 per
  primary cell (S12 seeds 1–3 are the D3 students, reused without retraining); RL-relative 3 (S12); belief-input
  student 3 (S12); absolute-frame student 3 (S12); BC-only 3 (S12). Deterministic methods use one RNG stream per episode.
- **Unit.** The paired test episode with seed-averaged per-episode outcomes; crossed bootstrap with the same episode
  indices for all methods (v2 §1.8). One-sided 95 % bounds unless stated.

### 1.4 One rule for informative cells (replaces proposer H1 (d); consistent with v2 §1.7 and 15_decision §4.1)

- **I1 (pre-test).** A primary cell that violates §1.7 on the v3 pilot, after the one n\* adjustment where the n\* rule
  allows it, is removed from **both** success and BI parts of every hypothesis, before any test episode. Reported.
- **I2 (on test).** A pilot-informative cell that violates §1.7 (1) or (2) on test has its success contrasts labelled
  "non-informative (ceiling/floor)" and is decided on BI alone, labelled so.
- **I3 (hypothesis level).** H1 is "decided on success" iff ≥ 2 of the cells surviving I1 are success-informative on
  test. Otherwise H1's label is "inconclusive on success; decided on BI only". There is no other informative-cell rule
  in this file.

### 1.5 Margins (rule frozen now, values frozen after G5′ with a commit hash)

- δ_c = min(4 pp, 0.15·D_c), D_c = success(G\*) − success(random) on the pilot (G\* on 500, random on 200 episodes).
  Since δ_c reaches its 4 pp cap whenever D_c ≥ 26.7 pp (v2 pilot D: 0.300–0.460), random's smaller pilot changes δ_c only
  near that boundary.
- ε_c = min(0.05·BI_c(G\*), 0.15·D_c^BI) nats, D_c^BI = BI(G\*) − BI(random), same pilot episodes.
- The 16.5 pp first-200 / last-100 split of v2's S12 pilot (AC row 8) is the reason for G\* 500.

### 1.6 Teacher scores and regret (well-defined at ties)

- **Score vector.** At every labelled decision G\* exports s(a) = max(0, EIG_B(a; b))/c(a) for all feasible a (512 with
  mask), full size N = 2,000, M = 64, float32 (`score_vector()`; unit test: argmax equals `GStar.act`).
- **Unnormalised regret** of an action a_π: r_u = s_max − s(a_π), in nats per stroke. r_u = 0 for any a_π in the argmax
  set.
- **Floored normalised regret:** r = r_u / max(s_max − s_med, ρ·s_max), ρ = 0.05, s_med = median of s over feasible a.
  Decisions with s_max = 0 are excluded and counted. r ≤ 1/ρ = 20 by construction. A decision is a **tie decision** when
  s_max − s_med < ρ·s_max; their fraction is reported. R̄ = mean r over decisions.
- **Teacher noise floor.** On 200 validation beliefs, G\* is re-scored with an independent RNG stream; R̄ of G\*'s own
  first choice under the second score draw is the noise floor (answers AC row 3: argmax noise vs genuine near-ties).
  The fraction of decisions with (s_max − s_(2))/s_max < 0.05 is reported.
- **Use.** R̄ (validation, held-out beliefs) is the HP selection metric (ties within 0.01 → lower config index). It is
  descriptive otherwise; **no R̄ threshold is a prediction**. R̄ of R_b and of the noise floor are reported on the same
  beliefs for scale.

### 1.7 Non-random heuristic baselines (answers skeptic §1.3 (ii))

All use the shared feasibility mask and a **budget reservation rule** so they cannot strand themselves: an action is
allowed iff c(a) ≤ τ_rem − max(0, n\* − t − 1), t = probes executed so far; if none is allowed, the cheapest feasible
action is taken.
- **B-spread** (belief-free): φ′ maximises the minimum wrap distance to {φ₀} ∪ previous probe angles among allowed
  actions; ψ = +5°; ties → lower c(a), then lower index.
- **B-fan** (belief-free, travel-nearest): φ′ = φ_t whenever allowed (no travel), ψ cycles +5°, −5°, +15°, −15°, +25°,
  −25°, +35°, −35°; if staying is not allowed, nearest allowed φ′.
- **B-cov** (belief-using): v2 coverage (`CoverageV2`, online PF N = 2,000) restricted to allowed actions.
- **H★(c)** = the heuristic with the highest success on the 200 pilot episodes of cell c (ties → B-spread < B-fan <
  B-cov). Selected before test, frozen with the margins.

### 1.8 Greedy comparator grid and latency accounting (answers skeptic §1.1 and the "fair latency" requirement)

- **Grid of 27 greedy configurations:** N ∈ {2,000, 500, 125} particles × C ∈ {512, 128, 32} candidates × M ∈ {64, 16, 4}
  outcome samples. Candidate subsets are nested (`rung_subset` on 64 × 8: 128 = 32 φ′ × 4 ψ, 32 = 16 φ′ × 2 ψ). (The
  proposer's ladder description varied only C; the v2 ladder varied N, C and M jointly. The full grid replaces both.)
- **What is counted, per decision (L_dec, primary):** time from receiving y_t to emitting a_{t+1}.
  - Greedy configuration: t_assim (PF update of y_t incl. resample-move at its N) + t_nb (ball neighbour lists,
    O(N²)) + t_score (EIG_B over C × M) + t_select. Each component is timed separately.
  - Student: t_feat (re-encoding of the relative history) + t_fwd (forward pass, 512 logits) + t_mask.
  - Selection-only time is reported for both.
- **Per episode (L_ep, reported, no threshold):** Σ L_dec + L_final, where L_final is the cost of the deployable final
  estimate: for the student, one PF (N = 2,000) pass over the whole history + MAP identity + 30 Nelder–Mead iterations;
  for greedy, the read-out only (its PF is current). The grid evaluator is the scoring instrument for all methods and is
  excluded from both.
- **Which carries the claim.** The "≥ 100×" claim is **per decision** (the compute stall between probes). Any
  per-episode statement uses the measured L_ep ratio with its CI. The abstract says "per decision".
- **Protocol.** v2 §2.3, extended: all 27 configurations, the student, pruned-16 (§3.2) and L_final are timed
  interleaved on the same decision states (S12 pilot episodes in Lat′; repeated on 500 test decisions after the main
  runs, reported). Median with bootstrap 95 % CI; ≥ 500 more decisions if any CI half-width exceeds 10 % of its median.
- **Implementation parity.** A cProfile statement of G\* (fraction of L_dec inside vectorised numpy kernels) and
  implementation-independent counts (likelihood evaluations M·N·C + N·C per greedy call, `latency.lik_evals_rung`;
  student MACs, `latency.macs_policy` with n_act = 512) are reported.
- **R_b (boundary configuration).** Q = configurations whose median L_dec ≤ 100 × median L_dec(student) (Lat′). Keep the
  maximal elements of Q under the componentwise order on (N, C, M) (≤ 7 configurations). Run each on the 200 S12 pilot
  episodes. R_b = highest pilot success (ties → higher median L_dec). **Empty Q:** R_b = (125, 32, 4), labelled "grid
  floor"; it must still be shown worse than the student (H1b).

### 1.9 Statistical tests (one per claim; all numpy, `code/touchbed/stats.py` or `analysis_g2.py`)

| Claim | Test | Decision rule | Code |
|---|---|---|---|
| H1a | crossed bootstrap of paired Δ (student − G\*), B = 10,000, one-sided 95 % LB, success and BI, per cell; intersection–union (IU) across cells | LB > −δ_c (success), LB > −ε_c (BI) | `crossed_bootstrap_diff` |
| H1b | crossed bootstrap of success(R_b) − success(student), one-sided 95 % UB per cell; IU | UB < 0 | `crossed_bootstrap_diff` |
| H1c | paired episode bootstrap of success(H★) − success(G\*), one-sided 95 % UB, per cell where H1a passes; IU | UB < −δ_c | `crossed_bootstrap_diff` (1 column each) |
| H1-fb | as H1a for pruned-16; latency ratio: bootstrap over decisions of median ratio, one-sided 95 % LB | NI as H1a; ratio LB ≥ 10 | as above + new 10-line ratio bootstrap |
| H1-fb control | as H1c for random-16 | UB < −δ_c | as H1c |
| H2 | crossed bootstrap of g_T(student) − g_T(RL), S12, one-sided 95 % LB | LB > +0.10 nats | `crossed_bootstrap_diff` |
| H3 | bootstrap over beliefs of the ratio of means G(12), one-sided 95 % bounds | partition in §3.4 | `analysis_g2.py` |
| Reported rows | two-sided bootstrap p-values, Holm within the family {student vs BC, vs abs-frame, vs random per cell} | reported only | `holm` |
| Secondary | TOST of student vs G\* at ±δ_c (success) per cell | reported only | `tost` |

IU across cells needs no correction (every component must pass). There is no correction across H1, H2, H3: separate
claims with separate decisions. The H1a seed rule (§3.1) is a robustness rule, not a test.

---

## 2. Methods

### 2.1 Student and distillation recipe (Idea A)

- **Architecture.** The finger-relative DeepSets head of `relframe.py` (`RelDeepSets`, context dim 5) on 512 relative
  actions with the feasibility mask; hidden sizes as v2. Belief-free: input = touch history + finger angle + τ_rem/τ.
- **Loss.** CE to softmax(β_T · s(a)/σ_s) over feasible a, σ_s = per-decision SD of s over feasible a (if σ_s < 10⁻⁶,
  the target is uniform over the argmax set), plus λ · CE to G\*'s argmax.
- **Data.** Round 0: 1,500 G\* rollouts per cell, labelled at every decision, shared across seeds; 20 % of round-0
  episodes held out for validation regret. DAgger rounds 1–2: 400 student rollouts per seed per round, G\* labels at every
  visited belief, mixing β_DAgger = 0.5 (round 1: each decision executes G\*'s action with probability 0.5) and 0
  (round 2). Aggregated data; training restarts from the previous round's weights.
- **Training stop.** Per round, evaluate validation R̄ every epoch; stop when it improves by < 0.005 over 3 evaluations,
  hard cap 50 epochs. Last checkpoint, no success-based selection.
- **HP grid (≤ 4 configs, 1 seed, S12, selected on held-out round-0 R̄ before DAgger):** proposed default
  (lr, β_T, λ, batch) ∈ {(1e-3, 4, 0.5, 256), (3e-4, 4, 0.5, 256), (1e-3, 16, 0.5, 256), (1e-3, 4, 0, 512)}; exact values
  frozen in amendment v3.0. The chosen config is used in every cell and row.

### 2.2 Comparators, controls and rows

- **G\*** full size (2,000, 512, 64): teacher and comparator in every H1 contrast. **R_b** (§1.8). **H★** (§1.7).
  **Random** (sanity, Holm-reported).
- **RL-relative** (H2): PPO sPCE-total, relframe head, 512 actions, v2 hp1 (selected at S κ = 6 on 32 × 8; stated as a
  limitation), E_train = 2 × 10⁵ (the v2 remedy budget, given up front), v2 plateau rule (validation ball-sPCE on 500
  episodes every 10⁴ episodes; plateau = 5-evaluation moving average improves < 0.02 nats) recorded but not used to stop
  early. 3 seeds, S12.
- **Belief-input student** (H2 control, gate-period item D3-B): same head and recipe, input = PF (N = 2,000) summary in
  place of the DeepSets history: per identity k, (w_k, weighted mean x, y, weighted SD x, y, resultant length of
  |G_k|·θ) = 48 features, plus the relative context. 3 seeds, S12.
- **Ablation rows** (S12, 3 seeds, first 300 test episodes, reported): BC-only (round 0, no DAgger); absolute-frame
  student (same recipe, absolute head of `train_v2.CategoricalDeepSets`).
- **Gen-κ row** (reported): S12-trained students (seeds 1–3) run unchanged in S0 on the first 300 test episodes vs
  G\* at S0. Wording rule: "the student transfers to κ = 0 without retraining" only if the H1a success LB > −δ_S0 there;
  otherwise amortization is stated as per cell.
- **Success-vs-probe curve** (reported, answers skeptic §1.3 (iv)): grid evaluation after each probe, S12, G\* and student
  seed 1, first 200 test episodes.

---

## 3. Final hypotheses

Working title (the outcome map can only shorten it): **"Amortizing cost-aware information-gain touch selection."**
"Near-optimal" may not appear in the title or abstract under any outcome.

### 3.1 H1 — A DAgger-distilled, belief-free student is non-inferior to cost-aware greedy G\*, needs learning to get there, and is ≥ 100× cheaper per decision at its own accuracy (Idea A, primary)

**Rationale.**
- **Gap.** Information-driven touch selection re-optimises online at every decision (cost ∝ N × C × M); tactile EIG work
  does not report per-decision compute (06_synthesis Gaps 1, 3; skeptic §6 on arXiv:2510.13595). v2 measured 0.840 s per
  G\* decision on 256 actions (informal).
- **Why distillation where RL failed.** The label at each visited belief is the whole 512-vector of EIG_B/c, so credit
  assignment and 512-way exploration disappear; the teacher already prices travel. RL with the same relative head
  stayed 7.5–15 pp short (§0.3, exploratory). DAgger addresses covariate shift; BC is an ablation row.
- **Why the claim is not trivial.** The skeptic's mechanism (ii) (flat task: near-ties make *any* sensible policy
  non-inferior) is tested directly by H1c. The latency half is stated at the student's accuracy against the best
  configuration on a 27-point greedy grid, not against full-size G\*.
- **Novelty boundary (to be verified, §8).** Imitation of information-gathering oracles (Choudhury et al., RSS 2017) and
  DAgger distillation of a nonmyopic active-search expert (arXiv:2405.15031) exist. The claim rests on: touch with a joint
  identity × SE(2) belief and travel cost; a teacher whose rollout headroom is *measured* (H3); learning shown necessary
  against heuristics (H1c); latency against a Pareto greedy grid with measured component split (H1b); the RL contrast (H2).

**Measurable predictions.**
1. **H1a (NI, success).** In every success-informative cell (§1.4), one-sided 95 % LB of success(student) −
   success(G\*) **> −δ_c** (δ_c ≤ 4 pp).
2. **H1a (NI, BI).** In every cell surviving I1, LB of BI(student) − BI(G\*) **> −ε_c** nats.
3. **H1a (seeds).** ≥ **4 of 5** seeds have point Δsuccess > −δ_c in every success-informative cell.
4. **H1b (latency at accuracy).** In every success-informative cell, UB of success(R_b) − success(student) **< 0**,
   with R_b fixed by §1.8 before test (or "grid floor").
5. **H1c (learning is needed).** In every cell where H1a passes on success, UB of success(H★) − success(G\*) **< −δ_c**
   (the best heuristic is demonstrably outside the NI margin), on the first 500 test episodes. Power rule: if the pilot
   gap success(G\*) − success(H★) < 12 pp in a cell, that cell uses all 1,000 test episodes.
6. **Reported, no threshold:** full-size L_dec and L_ep ratios with CIs; component split; likelihood-evaluation/MAC
   ratio; Pareto plot (latency of all 27 configurations, pilot success of the evaluated ones); R̄ (student, R_b, noise
   floor), tie fraction; break-even episodes = training CPU time (incl. labelling) / (per-episode G\* time − per-episode
   student time); Gen-κ, success-vs-probe curve; TOST.

**Failure conditions.**
- **H1a rejected** if any success-informative cell has success LB ≤ −δ_c, any I1-surviving cell has BI LB ≤ −ε_c, or
  < 4 of 5 seeds pass in some success-informative cell. If I3 fails, H1a is "inconclusive on success" and decided on BI.
- **H1b rejected** if any success-informative cell has UB(success(R_b) − success(student)) ≥ 0, including the grid-floor
  case. Then the paper reports the full-size ratio only and drops "≥ 100× cheaper at its accuracy".
- **H1c outcomes** (per cell where H1a passes): UB < −δ_c → **pass**; LB(success(H★) − success(G\*)) > −δ_c (H★ is itself
  non-inferior) → **flat task**; otherwise **unresolved**. One flat cell → the learning claim is restricted to the other
  cells and the flat cell is named; flat in ≥ 2 cells → outcome row 1′ (§5); unresolved in any cell → "necessity of
  learned selection not established in cell c".
- **Label rules.** A failure confined to κ = 12 cells (S12, A12) with S0 passing → "amortized ball greedy supported
  without travel; cost-aware amortization rejected"; "cost-aware" leaves the title.

**Experiment design sketch.**
- *Datasets:* libraries S and A; cells S0, S12, A12; 𝒜 = 512; probe-matched τ_κ; streams per §1.3.
- *Baselines:* G\* (teacher/comparator), R_b and the 27-config grid, H★ (from B-spread / B-fan / B-cov), random.
- *Ablations (rows):* BC-only, absolute-frame student; Gen-κ; success-vs-probe curve.
- *Measurements:* success, BI, identity/translation/rotation errors, executed probes, travel, L_dec components, L_ep,
  counts, training and labelling CPU-h.

### 3.2 H1-fb — student-pruned greedy (conditionally registered fallback inside Idea A)

**Rationale.** If the student is not non-inferior on its own, its ranking may still contain G\*'s choice: G\* scores
only the student's top-k = 16 feasible actions. Closest precedent: semi-amortized BED (Step-DAD, card hedman2025step)
and imitation-based information gathering (§8); credited there.

**Activation (decided in gate Lat′, before any accuracy number; answers skeptic §2.1).** H1-fb is active iff the
measured median L_dec(G\* full) / L_dec(pruned-16) ≥ **10** on the Lat′ decisions (an untrained network suffices:
latency does not depend on weights). If < 10, H1-fb is withdrawn on 11-10 with the statement "PF assimilation and
neighbour lists account for x % of G\*'s per-decision time; pruning candidates cannot give 10×". k = 16 is fixed; no k
sweep.

**Measurable prediction (if active and reached, §5 rows 3/4).** NI to full G\* by the H1a rules in every informative
cell, and one-sided 95 % LB of the latency ratio (500 test decisions) ≥ **10**. **Control:** random-16 pruned G\*
(16 feasible actions drawn uniformly per decision): UB of success(random-16) − success(G\*) **< −δ_c** in every cell
where H1-fb passes.

**Failure conditions.** NI fails in any informative cell, or ratio LB < 10 → H1-fb rejected. If H1-fb passes but the
random-16 control is not demonstrably worse, the claim is "pruning to 16 candidates preserves accuracy"; the word
"learned" is dropped.

**Design sketch.** Students from the main runs (5 seeds; or, in the D3-fail branch, 3 remedied-recipe seeds per cell
trained in the main window); 1,000 test episodes per informative cell for pruned-16 and random-16; latency per §1.8.

### 3.3 H2 — RL with the same architecture under-optimises its own objective (Idea A, mechanism; S12)

**Rationale.**
- v2: RL on ball-sPCE fell 20.6 pp short (absolute head) and 7.5–15 pp short (relative head, exploratory); doubling
  training added +3.9 pp; on the exact notch RL's value was 0.172 vs optimum 0.615, unchanged after 2× training
  (14_analysis §2.3), i.e. RL did not reach the optimum of its own objective there.
- The skeptic is right that "student beats RL on success" is nearly implied by H1a, and that a failing student does not
  show a representation limit. The informative contrast is on **RL's own objective**: ball-sPCE g_T, whose return PPO
  maximises (v2 §1.4; telescoping return = g_T). If a policy in the same architecture class, trained by supervision,
  scores higher on that objective, PPO under-optimised its own objective at this budget (optimisation failure,
  existence proof). If not, RL optimises sPCE as well as the student does and the success gap is an objective mismatch.

**Measurable prediction (one test).** On the first 500 S12 test episodes, with the same per-episode contrastive draws
(L = 4095, J = 16) for every method: one-sided 95 % crossed-bootstrap LB of g_T(student, seeds 1–3) − g_T(RL-relative,
3 seeds) **> +0.10 nats**. (0.10 nats = the v2 flatness BI tolerance, about one third of ε_S12 ≤ 0.32.)

**Reported with the test (no thresholds):** g_T of G\*; success and BI of RL on the first 300 test episodes and its
paired difference to the student; gap closure [success(student) − success(RL)] / [success(G\*) − success(RL)], reported
**only if** LB(success(G\*) − success(RL)) > δ_S12; executed probes (student vs G\* vs RL); RL plateau status; CPU-h of
both methods including G\* labelling ("with dense teacher labels", not compute-matched).

**Failure condition and pre-written readings.**
- **Pass** (LB > 0.10): "On its own training objective, PPO with this architecture reaches ≥ 0.10 nats less than the
  same architecture trained on G\* labels: at 2 × 10⁵ episodes, RL's deficit is at least partly an optimisation failure."
- **Fail** (LB ≤ 0.10): H2 rejected. If the student's success exceeds RL's (paired two-sided CI excluding 0, reported):
  "RL reaches the student's sPCE but not its success: objective mismatch (sPCE vs success), not optimisation". Otherwise:
  "dense supervision does not improve on RL with this head".
- **Encoder sentence (fail branch of H1/D3), allowed only under the label-fit and belief-input conditions:**
  - *under-fit* := training-set R̄ > 0.25 **or** training top-1 agreement < 0.50 at the end of round 2;
  - *belief-input passes* := D3-B students meet the D3 rule (§4) on their 300 validation episodes.
  - under-fit ∧ belief-input passes → "the belief-free history encoder is the limiting factor";
  - not under-fit (fits training labels) but fails validation → "generalisation / covariate shift, not capacity";
  - under-fit ∧ belief-input fails → "neither input fits G\*'s decisions with this head and recipe; representation not
    isolated".

**Design sketch.** S12; RL-relative 3 seeds (2 × 10⁵ episodes); student seeds 1–3; G\* reference; D3-B (belief-input,
3 seeds); training-set and validation R̄/top-1 logged for every student. S0 RL row from 15_decision is dropped for
budget; the v2 κ = 0 numbers stay exploratory.

### 3.4 H3 — One-step rollout headroom over G\* under travel cost is small on 64 × 8 (Idea B, characterisation)

**Rationale.** Greedy is competitive under (near-)adaptive submodularity and can be weak when actions constrain the
future (cards javdani2012efficient, chen2015submodular; §8). v2 measured G(12) = 0.0146 (UB 0.0208) on the voided
32 × 8 set. Halving the φ′ spacing adds cheaper set-up moves for both G\* and the look-ahead, so a rise is possible. H3
justifies the teacher choice; it is supporting, not the headline.

**Metric and units.** G(κ) = [mean V_LA − mean V_G\*] / mean V_LA over 100 G\*-reached beliefs, a **dimensionless relative
gap** in expected remaining-budget ball information (V in nats). Absolute gaps in nats are reported. The B6-frozen G1
estimator (CRN; screen C1 = 32 incl. structured set-up moves; top 4 re-estimated 4×; G\* completion, M = 64) is
unchanged; it measures **one-step-deviation (rollout) headroom over G\***, not the gap to the optimum, and makes no
success claim.

**Measurable prediction (one test, κ = 12).** One-sided 95 % UB of G(12) **< 0.03** (S, 𝒜 = 512, n\* re-calibrated).

**Outcome regions (disjoint, exhaustive; kill takes precedence).**
- **Kill:** LB95(G(12)) > 0.05 → the paper may not say "greedy is enough"; it reports the headroom and states the teacher
  choice as a limitation.
- **Hold:** UB95(G(12)) < 0.03 → "one-step rollout over G\* gains ≤ 100·UB % of the remaining expected ball information
  at κ = 12 (S, n\* probes)".
- **Inconclusive:** otherwise; stated with its interval, no "small" wording.
- **Instrument conditions** (gate G1′): if G1′ (a) or (b) fails, H3 is **untested** on 64 × 8 and only the 32 × 8 values
  are quoted with the flatness caveat. If G1′ (c) fails or the bias check shows over-reading (below), "Hold" is
  downgraded to "Inconclusive".
- **Bias check (answers skeptic §4.2):** on 20 S12 beliefs, the estimator's V_G\* vs an independent 4×-sample G\* rollout
  estimate. If the ratio estimate/reference > 1.02 (estimator over-reads greedy, which deflates G), "Hold" is not
  available.
- **Descriptive:** G(0), G(2), the ordering G(0) ≤ G(2) ≤ G(12), fraction LA ≠ G\*, beliefs with no budget left, the
  32 × 8 values.

**Design sketch.** Set S; κ ∈ {0, 2, 12}; 100 beliefs each (uniform step in {0, …, n\*−1}); notch control (5 runs) and
zero-gap bank (100 beliefs) re-run on the v3 code path; travel-notch control (G1′ (c)); bias check. No re-run on 32 × 8,
no added κ, no added beliefs.

---

## 4. Pre-run gates (numeric pass rules, dates, routing). No main run before G0′, Cal′, E′, G5′, Lat′ and D3 pass.

| Gate | Date | Check | Pass rule | If it fails |
|---|---|---|---|---|
| **G0′** hygiene | 11-05 | Unit tests in CI: 64 × 8 masks and costs; 32 × 8 bit-reproduction; relative ↔ absolute round trip on 512; soft-label CE gradient check; `score_vector()` argmax = `GStar.act`; regret floor and tie handling (§1.6); heuristic determinism and reservation rule; latency component timers sum to L_dec (±5 %); provenance scripts `analysis_g3_notch.py`, `analysis_g3_hp.py` reproduce or diff the v2 files (15_decision §3.5). TIME_ESTIMATE pilots (≤ 5 min each). | All green, commit hash | Nothing downstream starts; if not green by 11-07, the buffer is consumed; by 11-09 escalate to owner |
| **Cal′** | 11-06 | n\* (κ = 0, τ = 4 rule) and τ_κ for S0, S12, A12 (+ A0 recheck), 200 calibration episodes each | Verified mean probes within n\* ± 0.3 | ≤ 3 bisection steps; then the cell is removed (I1) |
| **E′** grid at κ_hi | 11-07 | sub 4 vs sub 8 on 8 S12 + 8 A12 pilot episodes (4 G\*, 4 B-fan, from the first G5′ shard) | Mean \|ΔBI\| ≤ 0.02 nats; no success flips outside the tie band | sub = 8 becomes the evaluator; its cost enters the downscale order |
| **G5′** | 11-09 | G\* 500, random 200, B-spread/B-fan/B-cov 200 pilot episodes per primary cell; §1.7; margins; H★; 64 × 16 report at S12 (300) | G\* ≥ random + 10 pp and §1.7 per cell | Cell removed (I1). If < 2 cells survive: H1 proceeds, labelled per I3. **Flat′ screen:** if H★ point success ≥ G\* − δ_c in ≥ 2 cells, the owner is told on 11-12 that row 1′ is likely; runs proceed unchanged |
| **G1′** instrument | 11-07 | (a) notch, 5 runs; (b) zero-gap bank, 100 beliefs; (c) travel-notch: notch geometry with actions on the stand-off circle and κ such that the identity feature is far from the cheap action; exact values by enumeration, T = 2 | (a) mean relative gap in [0.573, 0.860]; (b) mean in [−0.01, +0.02] and UB < 0.03; (c) exact relative gap ≥ 0.10 and estimate within ±20 % of it | (a)/(b): H3 untested on 64 × 8. (c) fails or not built by 11-05: H3 "Hold" unavailable (§3.4) |
| **G2′** (H3) | 11-10 | §3.4 measurement + bias check | Finding either way (§3.4 regions) | Does not block H1 |
| **Lat′** | 11-10 | §1.8 timing of 27 configs, student, pruned-16, L_final on S12 pilot decisions; R_b selection on 200 S12 pilot episodes | Protocol complete, CI half-widths ≤ 10 % of medians | 500 more decisions; R_b and H1-fb activation frozen |
| **D3** learnability | 11-12 | S12, 3 student seeds, chosen HP, full recipe; 500 validation episodes paired with G\* | (i) Δ̂_succ ≥ max(−2 pp, −δ_S12 + 1.645·SE_s·√(500/1,000)); (ii) Δ̂_BI ≥ max(−0.15, −ε_S12 + 1.645·SE_BI·√(500/1,000)); (iii) every seed's point Δ̂_succ > −δ_S12. SE from the crossed bootstrap on the D3 data. | **One remedy:** double round 0 and both DAgger rounds once; re-check 11-14. Still failing → **H1 dead**: H1-fb branch if active, else fallback row 4 (§5) |
| **D3-B** (report-only) | 11-12 | Belief-input student, 3 seeds, 300 validation episodes | Same rule as D3 (used only by the H2 encoder sentence) | No routing |

- **Why D3 is consistent with the test.** The test passes iff LB = Δ̂ − 1.645·SE_test > −δ_c. D3 (i) asks that the
  validation point estimate would pass that rule at the projected test SE (√(500/1,000) scaling; ignoring the 3 → 5 seed
  reduction keeps it conservative). At v2 variance levels (paired SD ≈ 0.5) this is ≈ −1.5 pp, never looser than the
  skeptic's −2 pp; the old "G\* − 5 pp" rule is withdrawn. The v2 power rule then sizes the test: if the projected
  SE_test > δ_c/2.5, the cell's test grows to 2,000 (≤ 2 cells; reserve in §7).
- **Freeze commit** after the gate decision (11-12, or 11-14 with the remedy): n\*, τ_κ, informative cells, δ_c, ε_c,
  H★ per cell, R_b, H1-fb activation, power-rule test sizes, HP config.

---

## 5. Outcome map (all rows pre-written; the owner is told which row occurred)

| Row | Outcome | Paper statement | Venue fit |
|---|---|---|---|
| 1 | H1a, H1b, H1c pass; H3 Hold (± H2) | "Amortizing cost-aware information-gain touch selection": a belief-free student matches G\* within δ_c, heuristics do not, and no greedy configuration within 100× of its per-decision cost is as accurate; one-step rollout gains ≤ x % over G\*; (H2) RL under-optimises its own objective. | RSS Stage 1 main claim |
| 1′ | H1a passes, H1c "flat" in ≥ 2 cells | "At this probe budget the task is flat: a simple heuristic is also non-inferior to G\*." The contribution is the measurement (H3, H2) and the latency characterisation; the learning claim is dropped. | Workshop / RA-L; owner decides |
| 2 | Row 1 but H3 Inconclusive or Kill | As row 1; measured headroom reported; "the teacher could be improved" as limitation. | RSS, weaker framing |
| 2b | H1a passes, H1b fails | "Non-inferior, but not ≥ 100× cheaper than the best greedy configuration at its accuracy"; full-size ratio only. | RA-L / workshop |
| 3 | H1 fails (D3 or test), H1-fb active and passes | "Learned candidate pruning for online information-gain touch selection" (≥ 10× per decision); "learned" only if the random-16 control is demonstrably worse; H2, H3 supporting. | RSS short / workshop |
| 4 | H1 and H1-fb fail, or H1-fb withdrawn | **Fallback paper:** characterisation: H3; learnability of RL and of distillation with the same encoder, with the label-fit / belief-input diagnosis (§3.3); H2 result; the evaluator observation (32k × 3 MH SMC under-reads BI by 0.073–0.166 nats vs the grid, 14_analysis §2.5) as a **methods note**, not a result. Owner decides: RSS Stage 1 extended abstract or retarget (RA-L / workshop). | Owner decision |

Not allowed after the run: switching the selection metric, changing k, H★ or R_b, adding cells or κ levels, re-running
H3 on another grid, choosing between RL and distillation on test data, promoting v2 exploratory seeds to confirmatory.

**Honest prior.** The closest learned evidence (RL, relative head) is 12 pp short of G\*; D3 asks for ≈ −1.5 pp. Rows 3–4
are realistic outcomes, which is why both are written now and both are publishable at some venue without a fourth design.

---

## 6. Pre-registered analysis plan

### 6.1 Must be frozen in `docs/07c_amendment_v3_0.md` before any v3 run (commit hash in PROGRESS.md)

1. 𝒜 = 64 × 8 (flag, unit test); 32 × 8 reproducibility; the 64 × 16 report-only comparison.
2. Evaluator: AdaptiveGridPosterior sub = 4, tie band [0.45, 0.55] (pre-registered this time), E′ rule and sub = 8 switch.
3. Cells {S0, S12, A12}, A0 re-check, κ_hi = 12, the I-rule (§1.4).
4. Calibration rules (n\*, τ_κ; bisection); values added by a dated status note after Cal′.
5. Episode streams and sizes (§1.3), power rule, downscale order (§7).
6. Margin rules (§1.5); values added after G5′.
7. Distillation recipe (§2.1): round sizes, β_DAgger schedule, loss, σ_s rule, HP grid, selection metric with ρ = 0.05
   and tie rule, stop rule, held-out split, label format.
8. Seeds and their IDs (§1.3); D3 seeds = main seeds 1–3.
9. RL comparator settings (§2.2); belief-input feature list; BC and absolute-frame rows; Gen-κ; success curve.
10. Heuristics, reservation rule and H★ selection (§1.7).
11. Greedy grid, subsets, latency scopes, protocol, R_b rule incl. grid floor (§1.8); H1-fb k = 16, activation rule,
    random-16 control.
12. H3: B6 estimator settings unchanged; beliefs and κ levels; outcome regions; travel-notch specification; bias check.
13. The test table §1.9 (B = 10,000, α = 0.05 one-sided, Holm family) and the label rules of §3 and §5.
14. Integrity corrections of 15_decision §3.5 (items 1–7) and the two provenance scripts; the statement that every v2
    learned-policy number is validation/pilot and that κ = 0/6 diagnostics and relative seeds 400–402 are exploratory.
15. Deviations from 15_decision §4 listed in §0.2.

### 6.2 Reporting

Labels only from §3 and §5 (pass / rejected / rejected as titled / flat / unresolved / inconclusive / untested /
withdrawn / non-informative cell). Gate results reported in full. Exploratory analyses labelled. AC wording of
14_analysis is binding for every v2 number quoted.

---

## 7. Compute estimate and timeline

**Planning unit costs** (every sweep is preceded by a ≤ 5 min TIME_ESTIMATE that re-measures them):
- G\* decision at 512: ≈ 1.7 s (2 × the 0.840 s informal median on 256; the Lat′ split may lower it). Decisions per
  episode: S ≈ 4.2, A ≈ 3.0 (v2 verified probes 3.9–4.1 / 2.75–2.97).
- Grid evaluation per episode: G\*-like 7.4 s (S12, measured); passing student ≈ 10 s; weak policies (RL, BC, abs) ≈ 20 s
  (measured range 10.6–26.4 s); heuristics ≈ 40 s (assumed, between G\* and random); random 66–76 s (measured).
- Labelled student rollout ≈ 7 s (S), 5 s (A). RL run at 2 × 10⁵ on 512 ≈ 4 CPU-h (v2: 0.8–1.7 CPU-h per 10⁵ on 256).

**Gates (11-05 → 11-12): ≈ 96 CPU-h (+ 13 for the D3 remedy).**

| Item | CPU-h |
|---|---|
| TIME_ESTIMATE + G0′ | 1.5 |
| Cal′ (4 cells) | 5 |
| G5′: G\* 3 × 500 (6.0), random 3 × 200 (11.7), heuristics 9 × 200 (20.0), 64 × 16 report (1.8) | 39.5 |
| E′ | 1 |
| G1′ (notch, bank, travel-notch) | 3 |
| G2′ (3 κ × 100 beliefs, 15_decision estimate) + bias check | 17 |
| D3: round-0 labels 2.9, HP 1, DAgger 4.7, training 0.9, validation students 4.2 + G\* 2.0, noise floor 0.1 | 15.8 |
| D3-B | 8.1 |
| Lat′ (timing 1.5, R_b pilot selection ≤ 7 × 200 episodes 4.0) | 5.5 |

**Main (11-13 → 11-19): nominal ≈ 149 CPU-h; protected core ≈ 120.**

| Item | CPU-h |
|---|---|
| Labels: round 0 S0 + A12 (5.0); DAgger 12 seed-cells × 800 rollouts (16.5) | 21.5 |
| Student training (12 runs) | 3.6 |
| Student test grid: 5 seeds × 3 cells × 1,000 | 41.7 |
| G\* test (3 × 1,000) | 11.4 |
| H★ test (3 × 500) | 16.7 |
| R_b test (3 × 1,000) | 8.5 |
| H2: RL 3 × 2 × 10⁵ (12.0), g_T (0.2), RL success read 3 × 300 (5.0) | 17.2 |
| Random sanity (3 × 100) | 5.8 |
| BC row (3 × 300) | 5.0 |
| Absolute-frame row (labels, training, 3 × 300) | 10.6 |
| Gen-κ (3 × 300) | 2.5 |
| Success-vs-probe curve | 3.3 |
| Final latency benchmark | 1.5 |

- **Downscale order** (if TIME_ESTIMATE projects > 150, or to reach ≈ 125): (1) drop the absolute-frame row; (2) random
  sanity 100 → 50; (3) drop the success-vs-probe curve; (4) drop Gen-κ; (5) BC and RL success reads 300 → 200. **Never
  reduced:** student seeds, cells and 1,000-episode tests, G\* test, H★ test, R_b test, the H2 g_T test.
- **Reserve (buffer 11-20 → 11-22):** ≤ 2 power-rule enlargements (≈ 21 CPU-h each) or H1-fb (pruned-16 + random-16,
  3 × 1,000 each, ≈ 20 CPU-h) — not both in full; the power enlargements take precedence only if row 1 is still reachable.
- **Fit.** ~20 concurrent 2-vCPU ubuntu jobs ≈ 40 single-thread processes, ≤ 6 h per job, `time_guard` at 80 %. Gates
  ≈ 2.5 h of saturated runners, main ≈ 4 h, spread over the dated windows for dependencies and queueing. Total
  programme ≈ 260–300 CPU-h; the main session must confirm the Actions minutes quota before 11-05 (if capped, apply the
  downscale order first).

**Timeline (today 2026-10-28; RSS 2027 Stage 1 extended abstract due 2026-12-04 AoE).**

| Dates | Stage | Work |
|---|---|---|
| 10-28 → 10-31 | 8 / 8.5 | This file; `07c_amendment_v3_0.md` (§6.1); literature verification (§8). |
| **11-01** | 9 | `08_experiment_plan_v3.yaml`, compute envelope above. |
| 11-01 → **11-05** | 10 | Code: N_PHI flag, `score_vector()`, `distill.py` (loss, DAgger driver, regret), heuristics, 27-config grid + component timers, belief-summary features, travel-notch, `main.py label/distill/eval2 --method student`, analysis scripts; G0′ green. |
| 11-05 → **11-12** | 11–12 | Cal′ 11-06 → E′, G1′ 11-07 → G5′ 11-09 → Lat′, G2′ 11-10 → D3, D3-B 11-12. **Gate decision 11-12**; D3 remedy re-check **11-14**. Freeze commit. |
| 11-13 (11-15) → **11-19** | 13 | Main runs. |
| 11-20 → 11-22 | — | Buffer: power enlargement or H1-fb. |
| 11-23 → **11-25** | 14–15 | Analysis and decision; if not PROCEED, escalate to owner (no third loop). |
| 11-26 → 12-03 | 16+ | Extended abstract draft (the row of §5 that occurred). 12-03 owner decision; 12-04 AoE submission. |

---

## 8. References (only those given with a verifiable identifier by the proposer or skeptic; all **to be verified in stage 8.5/23** before citing)

| Reference | Identifier | Use |
|---|---|---|
| Choudhury, Kapoor, Ranade, Scherer, Dey, "Adaptive Information Gathering via Imitation Learning", RSS 2017 | DOI 10.15607/RSS.2017.XIII.041; arXiv:1705.07834 | Novelty boundary of H1 (skeptic: proceedings page seen) |
| Choudhury et al., "Learning to Gather Information via Imitation", ICRA 2017 | arXiv:1611.04180 | Earlier version (skeptic: search result only) |
| Nguyen, Sarkar, Garnett, "Amortized nonmyopic active search via deep imitation learning" | arXiv:2405.15031 (venue unconfirmed) | Closest DAgger-amortization precedent for H1 |
| Tremblay, Meger, Hogan, Dudek, "Learning active tactile perception through belief-space control" | arXiv:2312.00215 | Related learned active tactile work |
| Gordon, Baraki, Bui, Posa, "Active Tactile Exploration for Rigid Body Pose and Shape Estimation" | arXiv:2510.13595 | Current tactile EIG baseline; gap claim on per-decision compute |
| javdani2012efficient (card C04), "Efficient Touch Based Localization through Submodularity" | doi:10.1184/r1/6554705 (from `05_knowledge_cards.json`) | H3 framing |
| chen2015submodular (card C49), "Submodular Surrogates for Value of Information", AAAI 2015 | doi:10.1609/aaai.v29i1.9694 (card) | H3 framing |
| hedman2025step (card C41), "Step-DAD: Semi-Amortized Policy-Based Bayesian Experimental Design", ICML 2025 | doi:10.48550/arXiv.2507.14057 (card) | H1-fb precedent |

DAgger (Ross, Gordon, Bagnell, AISTATS 2011) was named without an identifier: the method is described in text and is
**not cited** until stage 8.5 supplies a verified identifier. Any orienteering / budgeted-greedy bound is likewise not
cited until verified. One more targeted search for "distilled greedy EIG for tactile localisation" is required before
the novelty paragraph (skeptic §6).

---

## 9. Critique → resolution map (every point of `07b_skeptic_v3.md`)

| # | Skeptic point | Resolution |
|---|---|---|
| P1 | One of 5 G1 notch runs (0.8629) outside the band | G1′ (a) keeps the pre-registered mean-of-5 rule (v2 B6) and reports every run (§4). |
| P2 | G is relative; H3 thresholds' units unstated | G(κ) defined as a dimensionless relative gap; absolute nats reported (§3.4). |
| P3 | Relative head: one seed, 200 episodes, G\* 0.440 ≠ 0.410 | All 3 exploratory seeds quoted with their episode set; the three G\* numbers never mixed (§0.3). |
| P4 | Near-ties are a hypothesis, not a fact (AC row 3) | Stated as hypothesis; teacher noise floor and tie fraction measured (§1.6). |
| P5 | Latency informal; 1.7 s extrapolated; split unmeasured | Lat′ measures t_assim, t_nb, t_score, t_select and student components (§1.8, §4). |
| P6 | Estimator bias measured on one notch only | Travel-notch G1′ (c) and on-belief bias check; "Hold" unavailable if either fails (§3.4). |
| P7 | D_c only against random; no heuristic | Three heuristics, H★ per cell, H1c (§1.7, §3). |
| 1.1a | R_b may be empty | Grid floor (125, 32, 4) must still be worse (§1.8, H1b). |
| 1.1b | Ladder varies only C; strawman | 27-configuration (N, C, M) grid; R_b from the maximal qualifying set by pilot success (§1.8). |
| 1.1c | Per-decision hides the final estimate | L_ep with L_final measured and reported; claim scoped "per decision" with the reason (§1.8). |
| 1.1d | Vectorisation artefact | cProfile share of vectorised kernels; likelihood-evaluation and MAC counts (§1.8). |
| 1.1e | H1c first-action split ill-posed | Withdrawn; per-decision regret descriptive only (§1.6). |
| 1.1f | R̄ denominator → 0 at ties | Floor ρ = 0.05·s_max; tie decisions flagged; s_max = 0 excluded and counted (§1.6). |
| 1.1g | R̄ ≤ 0.25 unjustified | Dropped as a prediction; R̄ scaled by R_b and the noise floor. 0.25 survives only in the H2 under-fit labelling rule, stated as a rule, not a finding (§3.3). |
| 1.2a | H1 (d) conflicts with §1.7 | One I-rule (§1.4). |
| 1.2b | D3 looser than the test | D3 = test LB rule at projected SE, floored at −2 pp / −0.15 nats (§4). |
| 1.2c | Margins rest on ≤ 300 pilot episodes | G\* pilot 500 per primary cell (§1.5). |
| 1.3 (i) | Distinguish learned rule | Held-out-belief R̄; DAgger vs BC row (§2.2). |
| 1.3 (ii) | Flat-task pass | H1c with pre-registered prediction and row 1′ (§3, §5). |
| 1.3 (iii) | Memorisation / no held-out condition | Gen-κ transfer row with wording rule; held-out objects **not tested** and stated as a limitation (§2.2). |
| 1.3 (iv) | Success saturation | §1.7 via I-rule plus the success-vs-probe curve (§2.2). |
| 1.4 | Latency half trivially true | Stated at matched accuracy against the Pareto grid; full-size ratio report-only (§3). |
| 2.1 | H1-fb fixed by an unmeasured split | Activation decided by measured ratio in Lat′ before any accuracy data; withdrawn if < 10 (§3.2). |
| 2.2 | No random-k control | Random-16 control with its own prediction; "learned" dropped if it is not worse (§3.2). |
| 3.1a | H2 implied by H1 | H2 re-centred on RL's own objective g_T, informative in every H1 branch (§3.3). |
| 3.1b | H2b ratio unstable | Reported only if LB(G\* − RL) > δ_c (§3.3). |
| 3.2a | Fail branch does not show representation | Encoder sentence only under under-fit ∧ belief-input-passes (§3.3). |
| 3.2b | Capacity check | Training-set R̄ and top-1 at end of round 2 (§3.3). |
| 3.2c | Privileged-input control | D3-B belief-input student, 3 seeds (§2.2, §4). |
| 3.2d | Objective mismatch | The H2 test itself, with the pre-written mismatch reading (§3.3). |
| 3.2e | Compute not matched | CPU-h incl. labelling reported; wording "with dense teacher labels" (§3.3). |
| 3.3 | Numeric plateau rule | v2 §2.1 rule quoted; E_train = 2 × 10⁵ given up front, so "not testable" cannot arise (§2.2). |
| 4.1a | Overlapping kill / inconclusive | Partition on LB/UB with kill precedence (§3.4). |
| 4.1b | κ = 2 has no prediction | Descriptive, labelled (§3.4). |
| 4.1c | H3 decides the title | "Near-optimal" banned; H3 wording fixed (§3, §3.4). |
| 4.2a | Rollout ≠ optimum | Scope sentence "one-step rollout over G\* gains ≤ x %" (§3.4). |
| 4.2b | One constructed instance | Travel-notch + bias check (§3.4, G1′). Exact DP on a down-scaled S instance is not feasible by 11-05 and is left to the full paper, stated. |
| 4.2c | BI not success | H3 makes no success claim (§3.4). |
| 4.3 | Low-risk replication | Hold threshold tightened to UB < 0.03; H3 is supporting, not headline (§3.4). |
| 5.1a | Row 1 title overstates | Title renamed (§3, §5). |
| 5.1b | Missing heuristic-NI row | Row 1′ (§5). |
| 5.1c | Evaluator finding is a methods note | Labelled so in row 4 (§5). |
| 5.2 | Package trivial without (1) + one of (2)–(5) | Pre-registered: (1) H1c; (3) Pareto latency with components; (4) H2 on RL's objective with controls; partial (2) Gen-κ; partial (6) travel-notch. (5) physical demonstration: **not done**; the paper states that the relevance of 0.84–1.7 s per decision relative to probe execution time is not measured. Without H1c passing, the package is pre-labelled workshop / RA-L (row 1′, §5). |
| 6 | Novelty threats | Cited with identifiers, to be verified; novelty statement narrowed (§3 H1 rationale, §8). |
