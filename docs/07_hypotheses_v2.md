# Stage 8 · HYPOTHESIS_GEN v2 — final hypotheses (Pass 3 Methodologist, fresh opus subagent, 2026-10-28)

> System: "You are a methodology lead synthesizing a proposer and a skeptic into final, defensible hypotheses."
> Task: "Produce the final hypothesis set, addressing every critique. For each surviving hypothesis include: rationale,
> measurable prediction (with concrete metric and threshold), failure condition (with concrete metric and threshold),
> and the experiment design sketch (datasets / baselines / ablations needed)."
> `{proposer_output}` = `docs/07a_proposer_v2.md`; `{skeptic_output}` = `docs/07b_skeptic_v2.md`.
> Context kept consistent with: `results/v1/15_decision.md` (PIVOT, gates G0–G5, fallback, timeline),
> `docs/07c_amendment_v1_1.md` (L = 4095, ball information, measured costs), `docs/07_hypotheses.md` §1 (v1 global
> definitions, reused where stated), `code/README.md` (existing `touchbed/` code).
> Constraints: CPU only, GitHub Actions runners (~20 concurrent 2-vCPU jobs, ≤ 6 h each); main-run compute ≤ ≈ 120
> CPU-h; main runs finished by 2026-11-22; extended abstract 2026-12-04.

`docs/07_hypotheses.md` stays untouched as the v1 record. This file replaces it for every v2 run.

---

## 0. Outcome of the debate

### 0.1 Verdicts and final form

| Proposer item | Skeptic verdict | Final form (this file) |
|---|---|---|
| H1a non-inferiority to G* | REVISE | **H1a.** Margin is a fraction of the random→G* gap, capped at 4 pp (§1.7, §5). A cell counts only if it passes the non-degeneracy rule (§1.7). G* and the policy optimise the **same** ball-information target (§1.4) over the **same** discrete action set (§1.5). The ball-information ratio is replaced by a difference with a nats margin. |
| H1a beats random / coverage | demote | **Sanity check**, reported with Holm-corrected p-values. It is not a failure condition. |
| H1b latency at matched accuracy | REVISE | **H1b.** No matched-accuracy search. A pre-registered greedy **ladder** (§2.3) fixes, by measured latency alone, the "boundary rung" R_b: the most expensive greedy configuration that is still < 100× slower than the policy. H1b holds iff R_b is **significantly less accurate than the policy** on the test set. This is matched to the policy's accuracy (not greedy's), and nothing is selected on noisy validation numbers. Latency scope, hardware and threads are fixed (§2.3). |
| H2a effect + dose–response | REVISE | **H2a.** The horizon confound is removed by **probe-matched budgets**: at every κ the budget τ_κ is set so that G* executes the same number n* ∈ {3, 4, 5} of probes (§1.2). The κ = 0 cell is therefore the v1-style short-budget, free-repositioning cell. The 3-point OLS slope is dropped. The confirmatory test is the κ_hi effect plus the κ × method interaction, against **both** G* and the rate-reward myopic policy. The negative control fails if \|Δ(0)\| > 3 pp **or** TOST fails. |
| H2b mechanism P1–P3 | REVISE | **H2b.** P1 is tested only on beliefs where the policy and G* disagree (disagreement ≥ 20 % required). P2 is stated as the fraction of the exact gap closed and is a failure condition. P3 is tested against G* **and** coverage. |
| Gate / fallback | REVISE | G1 failure → Idea 2 **untested** (instrument broken). G1 pass + G2 failure → Idea 2 **refuted** in the tested range, with the measured headroom and its upper bound as the reported result (§3, H2 "Gate outcomes"). G now has units (§4). |

No hypothesis is rejected. Two core ideas remain ("sushi, not curry"): **Idea 1 = H1 (amortization)** and **Idea 2 = H2
(gated look-ahead under travel cost)**. Everything else is a component row or a supporting measurement.

### 0.2 v1 → v2 change log (cites `results/v1/15_decision.md`)

- **Manipulated variable.** "Ambiguous (S) vs asymmetric (A) set" is replaced by travel cost κ under a time budget
  (decision §1, option (a)). v1 H2a/H2b/H2c are withdrawn: their premise check failed (G(S) = −0.033, UB −0.017),
  and the estimator was not validated (PC: G = −0.052). See decision §3.
- **H3** (planning for no-contact outcomes) is dropped as a claim: R_NC(S) = 0.03 < R_NC(A) = 0.07. The NC-input
  ablation stays as a component row.
- **H1c** (information objective vs sparse task reward) and the RL-success / RL-PFIG baselines, the encoder ablation,
  the L ablation, **H4** (MuJoCo transfer) and **H5′** are moved to the full paper (2027-04-16).
- **Objective.** The training reward, the greedy score and the co-primary metric are now all ball information
  (07c A2). The v1 full-state sPCE (L = 4095, 07c A1) becomes the objective-ablation row.
- **Action model.** v2 uses the travel / time-budget model of §1.2. At κ = 0 with τ = T and the v1 candidate generator
  switched on, it reproduces v1 (unit test, §1.2).

---

## 1. Global definitions

### 1.1 Reused unchanged from v1 (`docs/07_hypotheses.md` §1.1, §1.4, §1.5)

- **Objects and state.** Planar polygons, circumradius R = 40 mm. s = (k, x, y, θ). Prior: k ~ U{1..K},
  x, y ~ U[−15, 15] mm, θ ~ U[0, 2π). Exact symmetry group G_k.
- **Libraries.** A (K = 8, asymmetric) and S (K = 8, near-symmetric base/variant pairs), as frozen in v1 (`shapes.py`).
  **Amendment (G0):** the per-shape confusability rule for A (≤ 0.80) becomes a set-level rule only
  (C(A) = 0.772 ≤ 0.80 passes). A2, A4 and A6 (0.806, 0.818, 0.818) are kept. Reason: confusability is no longer the
  independent variable in v2, and keeping A unchanged keeps the v1 greedy and random reference numbers valid for the
  κ = 0 reproduction test. The three S self-symmetry entries that are exactly 0.0 are recomputed with the
  symmetry-element exclusion fixed (07c A6). Both changes go into `docs/07c_amendment_v2_0.md`.
- **Observation model.** Contact: point + N(0, σ_p² I) and normal + N(0, σ_n²), σ_p = 1.0 mm, σ_n = 5°. Miss: y = ∅.
  ε-softened likelihood with ε = 10⁻³, one code path (`likelihood.py`) for every method.
- **Single-threaded execution, fixed per-episode RNG streams, disjoint pilot / validation / test episode sets, paired
  test design.** Sizes are in §1.8.

### 1.2 v2 action model: travel cost κ and time budget τ

- **Finger state.** The finger rests on the stand-off circle R_s = 100 mm at angle φ_t. The start angle is
  φ₀ ~ U[0, 2π), drawn from the episode seed. It is identical for all methods on a given episode.
- **Action.** a = (φ′, ψ). The finger travels along the circle to target angle φ′, the shorter way
  (Δφ = wrap(φ′ − φ_t) ∈ (−π, π]). It then probes from 100·(cos φ′, sin φ′) mm in direction φ′ + π + ψ, with a 200 mm
  guarded stroke, exactly as in v1. After the probe, φ_{t+1} = φ′.
- **Cost, in units of one stroke.**
  **c(a) = 1 + κ·|Δφ|/π.**
  - κ is the time to travel half the circle (π·R_s ≈ 314 mm), in strokes. This is the decision's
    κ·|Δφ|·R_s/v_travel + stroke_time with v_travel absorbed into κ.
  - Stroke time is 1 for hits and misses alike. An outcome-dependent stroke time would make budget consumption depend
    on the outcome, a channel unrelated to travel. This is recorded as a deviation from the decision's
    "stroke_time(hit/miss)" in `07c_amendment_v2_0.md`.
- **Budget and feasibility.**
  - Each episode has a time budget τ_κ. With remaining time τ_rem, an action is feasible iff c(a) ≤ τ_rem.
  - **Every method chooses only among feasible actions.** Random, coverage, G*, the planner and every policy use the
    same feasibility mask.
  - The episode ends when τ_rem < 1, i.e. when not even Δφ = 0 is feasible. So unused budget at the end is < 1 stroke
    for every method by construction, and no method can lose a probe by choosing an infeasible action.
- **κ grid (fixed values, not probe-count targets):** κ ∈ {0, κ_mid = 2, κ_hi = 6}.
  - κ_mid appears only in gate G2 (estimator headroom). It is not a policy cell (§3, H2).
  - **One pre-registered escalation:** κ_hi ← 12. It is used once, only if all of the following hold:
    - G1 passed;
    - G2 failed on magnitude only (G(κ_hi) < 0.10 or its LB ≤ 0.05);
    - the ordering G(0) ≤ G(κ_mid) ≤ G(κ_hi) held.

    If it is used, κ_hi = 12 replaces 6 in every κ_hi cell (H1 and H2) and in G3. There is no further escalation.
- **Probe-matched budgets (removes the horizon confound).**
  - **Reference probe count n\* per set.** Default n* = 4. On 200 pilot episodes at κ = 0 with τ = 4, if G*'s success
    is > 0.88, then n* = 3 for that set. If it is < 0.20, then n* = 5. Frozen before test.
  - **τ at κ = 0:** τ₀ = n* exactly. Every action costs 1, so exactly T = n* probes are executed. **This is the κ = 0
    short-budget cell (T ∈ {3, 4, 5}).** It reproduces the v1 free-repositioning setting at a v1-style touch count.
  - **τ at κ > 0 (pilot rule).** Run G* without a budget for n* probes on 200 pilot episodes. Set τ_κ = n* + the mean
    travel time of those n* actions, rounded to 0.1. Then check, with the budget enforced, that G*'s mean executed probe
    count is within n* ± 0.3. If not, bisect τ_κ (at most 3 steps). Frozen before test.
  - **Result.** G* executes the same number of probes on average at every κ. Only the price of moving differs between
    cells. A method can still execute more probes than G* if it travels less, and that is part of the effect H2
    measures (§3, H2b-P3).
- **Unit test (renamed per skeptic X1).** "κ = 0 **and** τ = 3 with the v1 Sobol candidate generator reproduces v1."
  Environment, likelihood, greedy PF-EIG (full-state, v1 objective) and the evaluation PF must give bit-identical
  outputs to v1 on the v1 dev episodes, given the same action sequences and RNG streams.

### 1.3 Success and ball information (co-primary metrics; define every threshold below)

Both are computed from the **evaluation PF** (§1.6) after the last executed probe.

- **Success** (unchanged from v1 §1.3).
  - k̂ = the identity with the largest posterior mass. The pose is the highest-weight particle of k̂, refined by 30
    Nelder–Mead iterations on the log-posterior.
  - Success = [k̂ = k₀] ∧ [‖(x̂, ŷ) − (x₀, y₀)‖ < 5 mm] ∧ [min_{g ∈ G_{k₀}} |wrap(θ̂ − θ₀ − g)| < 5°].
- **Success region (ball)** B(s₀) = {s : k = k₀, ‖(x, y) − (x₀, y₀)‖ < 5 mm, rotation error mod G_{k₀} < 5°}.
- **Ball information** (07c A2): **BI(h) = log P̂(B(s₀) | h) − log P(B(s₀))**, in nats.
  - **Posterior mass.** P̂(B(s₀) | h) = Σ_n w_n·1[s_n ∈ B(s₀)], floored at 1/(2·N_eval).
  - **Prior mass, exact.** P(B(s₀)) = (1/K) · area(disc₅ₘₘ(x₀, y₀) ∩ box) / 900 mm² · |G_{k₀}|·10°/360°. For an
    asymmetric shape away from the box edge, −log P(B) = 8.10 nats.
  - **Cap.** BI is reported with its cap −log P(B(s₀)). A cell's "BI saturation" is the fraction of episodes with BI
    within 0.5 nats of the cap.
- **Identity.** Since the prior is uniform within B(s₀) (up to the box clip), log P(B(s₀) | h) − log P(B(s₀)) =
  log p_B(h | s₀) − log p(h), where p_B(h | s₀) = E[p(h | s) | s ∈ B(s₀)]. This identity is what lets every method
  below optimise the same quantity.

### 1.4 One information target for every information-based method (answers skeptic X5)

**Target:** expected terminal ball information, **J_B(π) = E_{s₀, h ∼ π}[BI(h_T)]**. Every information-based method
optimises J_B or its per-step increment. The methods differ only in the **estimator** and in **planning depth**, which
are exactly what H1 (estimator: amortized vs online) and H2 (depth: total vs myopic) manipulate.

| Method | What it optimises | Estimator |
|---|---|---|
| sPCE-total (ours) | J_B over the whole budget | **ball-sPCE** (below), L = 4095, γ = 1 |
| sPCE-myopic(rate) | per-step increment of J_B per unit time | ball-sPCE increments ÷ c(a), γ = 0 |
| G* (cost-aware ball greedy) | argmax over feasible a of EIG_B(a; b) / c(a) | PF nested MC (below) |
| Rollout planner | J_B over the remaining budget | EIG_B with G* rollouts (§2.2) |
| *Ablation rows:* full-state sPCE; full-state greedy | full-state information (v1 / 07c A1) | as v1 |

- **Ball-sPCE (training reward).**
  - Per episode, draw s₀ ~ p, L = 4095 contrastive states s_{1:L} ~ p, and J = 16 states s₀^{(1..J)} uniform in
    B(s₀) ∩ prior support. All are fixed for the episode.
  - g_t = log p̂_B(h_t | s₀) − log[(1/(L+1)) (p̂_B(h_t | s₀) + Σ_{l=1}^{L} p(h_t | s_l))], with
    p̂_B(h | s₀) = (1/J) Σ_j p(h | s₀^{(j)}).
  - r_t = g_t − g_{t−1}. The return over the budget telescopes to g_T, which estimates BI(h_T) and is capped at
    log(L+1) = 8.32 nats ≈ −log P(B) = 8.10 nats (07c A1 calibration argument).
  - Extra cost over 07c A1: J = 16 extra likelihoods per step against 4,096, i.e. < 0.5 %.
  - We do **not** claim that ball-sPCE is a lower bound. Its bias against evaluation-PF BI is measured in G3: on 500
    validation episodes, report mean(g_T − BI) and its CI.
- **Ball EIG (greedy score).** On a PF belief {s_n, w_n}, with j_m ~ w and y_m ~ p_ε(· | s_{j_m}, a), m = 1..M:
  EIG_B(a; b) = (1/M) Σ_m [log Σ_{n ∈ B(s_{j_m})} w_n p_ε(y_m | s_n, a) − log Σ_{n ∈ B(s_{j_m})} w_n − log Σ_n w_n p_ε(y_m | s_n, a)].
  - This is the expected one-step increment of log P(B(s₀) | h) under b.
  - Ball neighbour lists are built once per belief (O(N²) distances). The likelihood terms are the same as in v1's
    vectorised greedy, so the cost is v1's plus sparse sums.
  - At κ = 0, c ≡ 1, so G* is plain ball greedy.

### 1.5 Action-resolution parity (answers skeptic X4)

- **One shared discrete action set 𝒜 = 32 target angles φ′ (11.25° spacing) × 8 offsets ψ ∈ {−35°, −25°, …, 35°} =
  256 actions**, the same at every κ.
- The policy head is **categorical over 𝒜** with the feasibility mask (logit −∞ for c(a) > τ_rem). Full-size G*
  scores all of 𝒜. Random draws uniformly from the feasible part of 𝒜. Coverage scores the feasible part of 𝒜. Ladder
  rungs (§2.3) use pre-registered nested subsets of 𝒜.
- **Flatness check** (part of G5). Compare full-size G* on 𝒜 with G* on the 4× finer grid 𝒜⁺ (64 × 16 = 1,024) on 300
  pilot episodes at (S, κ_hi). Pass: |Δ success| ≤ 2 pp and |Δ BI| ≤ 0.10 nats (paired point estimates). If it fails,
  𝒜 becomes 64 × 8 for **all** methods (once), and greedy costs in §6 double.

### 1.6 Evaluation particle filter

- The v1 / 07c A3 PF (`pf.py`), identical for every method: resample-move with random-walk plus contact-conditioned
  independence MH, ε-softened likelihood.
- **N_eval is fixed by G4** (§4). The working assumption for costing is 32,000.
- Methods differ only in the actions they choose. Greedy's own online PF (N = 2,000) is used only for choosing
  actions, never for scoring.

### 1.7 Non-degeneracy (saturation) rule for cells (answers skeptic X3)

A cell c = (set, κ) is **informative** for a contrast iff, on the 200 pilot episodes (frozen before test) **and** again
on the test set:
1. success(G*) ∈ [0.15, 0.90];
2. **D_c = success(G*) − success(random) ≥ 20 pp**;
3. BI saturation of G* < 50 % of episodes.

- **Before test.** A pilot violation triggers the pre-registered n* rule (§1.2) once. If the cell still violates,
  it is removed from the primary set before any test episode is run, and this is reported.
- **On test.** If an informative-on-pilot cell violates (1) or (2), its success contrast is labelled
  "non-informative (ceiling/floor)". The cell is then decided on BI alone and labelled so. It never counts as a
  success-based pass.
- **Margins** depend on D_c through §5. Because D_c ≥ 20 pp, the NI margin is always ≥ 3 pp, and power stays above the
  §5 minimum.

### 1.8 Episodes, seeds, unit

- **Episode sets per (set, κ) cell:** pilot 200 (G5 adds 100, so 300 for G4/G5), validation 500, and **test 1,000**
  (power rule in §5 can raise one cell to 2,000).
- **Test episodes** fix (s₀, φ₀, observation RNG stream) and are shared by all methods (paired).
- **Seeds.** 6 core seeds for sPCE-total and sPCE-myopic(rate) (07c A1/D2). 3 seeds for ablation rows.
  Deterministic methods use one RNG stream per episode.
- **Unit and CIs (v1 §1.5).** The unit is the paired test episode, with seed-averaged per-episode outcomes. CIs come
  from a crossed episode × seed bootstrap (B = 10,000) with the same episode indices for all methods; seeds are
  resampled independently per learned method. Bounds are one-sided 95 % percentile bounds.

---

## 2. Methods

### 2.1 Learned methods (new code in `train.py`; one architecture for all)

- **Architecture.**
  - DeepSets history encoder over (1[contact], contact point, cos n, sin n, cos φ′, sin φ′, ψ). NC entries are zeros
    except the action part.
  - Context: (cos φ_t, sin φ_t, τ_rem/τ_κ).
  - ρ, ψ are 2 × 128 MLPs. A **categorical head over 𝒜 with the feasibility mask**, and a critic with the same input.
  - Numpy with hand-written backprop, as in v1 (`nn.py`), extended by a softmax head. The gradient check is extended
    to it.
- **Policy input is identical for total and myopic**: history + current finger angle + remaining time. At κ = 0, the
  remaining time is the v1 remaining-budget input.
- **sPCE-total (ours).** Reward r_t from ball-sPCE (§1.4). PPO-clip, γ = 1, returns-to-go G_t = Σ_{τ ≥ t} r_τ, critic
  baseline. The rest is v1 §3.2. One policy is trained per (set, κ) cell.
- **sPCE-myopic(rate) (ablation of credit assignment; answers the skeptic's H2 point "γ = 0 also removes
  cost-awareness").**
  - Reward r_t^rate = r_t / c(a_t), γ = 0 (critic regresses r_t^rate). Everything else is identical.
  - Its fixed point as L → ∞ is the learned analogue of G*.
  - Stated honestly: total and myopic differ in credit assignment **and** in the 1/c normaliser. The normaliser is the
    minimum any myopic selector needs in order to see travel at all. At κ = 0, c ≡ 1 and the two differ only in γ, as
    in v1 §3.3.
- **Training budget and plateau.**
  - E_train = 10⁵ episodes per run (07c A1).
  - Validation ball-sPCE (no PF) on 500 validation episodes every 10⁴ episodes. A run counts as plateaued when the
    5-evaluation moving average improves by < 0.02 nats.
  - If any method in a comparison has not plateaued at the cap, the cap doubles for all methods in that comparison.
  - The final checkpoint is the last one (no checkpoint selection on success).
- **Hyperparameters.** 4 PPO configurations (learning rate, entropy coefficient, batch size, critic learning rate),
  from v1's ranges, 1 seed each at (S, κ_hi), selected on validation ball-sPCE (G3). The chosen configuration is used
  by every learned method and cell.
- **Ablation rows** (S, κ_hi, 3 seeds, 500 test episodes; reported, not hypotheses):
  1. full-state sPCE objective (07c A1, unsmoothed numerator);
  2. No-NC-input (NC entries removed from the DeepSets sum).

### 2.2 Non-learned methods

- **Random.** Uniform over the feasible part of 𝒜.
- **Coverage.** Maximises the minimum distance from the predicted contact on the current MAP shape and pose to all
  previous contacts, over the feasible part of 𝒜. Ties go to the lower c(a).
- **G\* — cost-aware ball greedy.** Online PF with N = 2,000 (v1 §1.4 kernel). It picks argmax_{a ∈ 𝒜 feasible}
  EIG_B(a; b)/c(a) with M = 64, fully vectorised over particles × candidates × outcomes. **Full size: N = 2,000,
  C = |𝒜| = 256, M = 64.** At κ = 0 it is plain ball greedy. **G\* is the comparator in every H1 and H2 contrast.**
- **Full-state greedy** (v1 objective, row only). Same as G* with full-state EIG/c. Run at (S, κ_hi) on 500 test
  episodes. It shows the size of the objective-mismatch effect separately.
- **Rollout planner (upper reference, not a claim).**
  - For each decision, screen the 16 feasible actions with the highest EIG_B/c.
  - For each, estimate EIG_B(a) + E_{y}[value of finishing the remaining budget with G* at ladder rung R3], with
    M = 8 outcomes and common random numbers.
  - Pick the action with the largest total (a budget sum, not a rate).
  - Run on 200 test episodes at (S, κ_hi). Success, BI and per-decision latency are reported.

### 2.3 Greedy ladder for H1b and the latency protocol

| rung | N particles | candidates (nested subset of 𝒜) | M | nominal cost vs full |
|---|---|---|---|---|
| R0 (full) | 2,000 | 256 (32 φ′ × 8 ψ) | 64 | 1 |
| R1 | 1,000 | 256 | 32 | 1/4 |
| R2 | 1,000 | 128 (16 φ′ × 8 ψ) | 32 | 1/8 |
| R3 | 500 | 128 | 16 | 1/32 |
| R4 | 500 | 64 (16 φ′ × 4 ψ) | 16 | 1/64 |
| R5 | 250 | 64 | 8 | 1/256 |
| R6 | 250 | 32 (8 φ′ × 4 ψ) | 8 | 1/512 |
| R7 | 125 | 32 | 4 | 1/2048 |

- Each rung uses a subset of the particles, candidates and outcome samples of the rung above, so accuracy is not
  expected to rise down the ladder. Nominal costs are only for ordering. **Latencies are measured.**
- **Latency scope (primary).** The time from receiving y_t to emitting a_{t+1}.
  - For a greedy rung this includes the PF assimilation of y_t, with resample-move at that rung's N, plus candidate
    scoring.
  - For the policy it includes the incremental DeepSets update, the forward pass and the mask.
  - Selection-only latency is reported as well.
- **Protocol.**
  - One GitHub Actions ubuntu runner type (CPU model recorded). Python and numpy versions pinned.
    OMP/MKL/OPENBLAS threads = 1, process pinned to one core.
  - Policy and rungs are timed interleaved in the same job: 20 warm-up decisions, then 500 timed decisions sampled
    from test episodes, stratified by step.
  - Median and bootstrap 95 % CI.
  - **Multiply-add counts per decision** are reported for both, as an implementation-independent ratio.
- **Boundary rung R_b(c).** The most expensive rung whose measured median latency is ≤ 100 × latency(policy) in cell c.
  If no rung qualifies, R_b = R7 and the label "ladder floor" is attached.
- **Break-even episodes** = training CPU-time / (per-episode G* time − per-episode policy time). Reported.

---

## 3. Final hypotheses

### H1 — Amortized, cost-aware ball-information gathering: one forward pass is non-inferior to online cost-aware greedy and ≥ 100× cheaper at the policy's accuracy (Idea 1, guaranteed core)

**Rationale.**
- **Gap.** Information-driven touch selection re-optimises EIG online at every decision, with cost ∝ particles ×
  candidates × outcomes, and no tactile work reports per-decision compute (06_synthesis Gaps 1 and 3). Policy-based BED
  amortises design selection into a forward pass but has not been shown on contact sensing.
- **v1 evidence.** It makes greedy the right opponent and non-inferiority the right claim. Greedy beats random by
  +64.3 pp (A) and +28.7 pp (S) at T = 3. No positive look-ahead gap was detected at κ = 0. There is a large latency
  gap: 0.65 s per decision for v1 greedy against ≈ 3·10⁴ multiply-adds for a forward pass.
- **Same target, so a mismatch cannot help.** H1 compares two estimators of the **same** target J_B (§1.4) over the
  **same** action set (§1.5). A pass therefore means that amortization reproduces the online optimiser. It is not
  produced by a better-aligned objective or finer action resolution.
- **κ_hi matters for the title.** Testing at κ_hi makes the claim about cost-aware gathering. If H1 fails at κ_hi, H1
  as titled is rejected (see failure condition).

**Primary cells.** {A, S} × {κ = 0, κ_hi}, i.e. 4 cells, each informative per §1.7. Policy = sPCE-total (6 seeds).
Comparator = full-size G*.

**Measurable prediction.**
1. **H1a (non-inferiority, success).** In every informative cell c, the one-sided 95 % lower bound of
   success(sPCE-total) − success(G*) is **> −δ_c, with δ_c = min(4 pp, 0.15·D_c)**. D_c is the pilot random→G* gap,
   frozen before test (δ_c ∈ [3, 4] pp because D_c ≥ 20 pp).
2. **H1a (non-inferiority, BI).** In all 4 cells, the lower bound of BI(sPCE-total) − BI(G*) is
   **> −ε_c, with ε_c = min(0.05·BI_c(G*), 0.15·D_c^BI) nats** (pilot values, frozen). This replaces the proposer's
   ratio > 0.95.
3. **H1a (seeds).** In each cell, ≥ 5 of 6 seeds have point estimate Δ_success > −δ_c. Per-seed lower bounds are
   reported.
4. **H1b (latency at the policy's accuracy).** In every primary cell, the boundary rung R_b(c) (§2.3), run on the same
   1,000 test episodes, is less accurate than the policy: the one-sided 95 % **upper** bound of
   success(R_b) − success(sPCE-total) is **< 0**, and BI(R_b) < BI(sPCE-total) as a point estimate.
   - No configuration is selected on validation data, so the "within 1 pp is below MC resolution" problem does not
     arise.
   - The burden of proof is on the policy: if a < 100×-cheaper greedy is not demonstrably worse, H1b fails.
5. **Reported without thresholds.**
   - Full-size latency ratio and multiply-add ratio.
   - Matched-to-policy and matched-to-full-greedy ratios: walk up the ladder from R_b on 500 test episodes at (S, κ_hi)
     until a rung's point success is ≥ policy − 1 pp, respectively ≥ G* − 1 pp. If none is reached by R1, report
     "> ratio(R1)".
   - Rollout planner latency and accuracy. Break-even episodes.
6. **Sanity checks (not failure conditions).** sPCE-total vs random and vs coverage in each cell. 8 contrasts,
   Holm-corrected bootstrap p-values, point differences reported.

**Failure condition.** H1 is **rejected** if any of these holds:
- (a) In any informative cell, the success lower bound of Δ is ≤ −δ_c. Or, in any of the 4 cells, the BI lower bound
  of Δ is ≤ −ε_c.
- (b) In any cell, fewer than 5 of 6 seeds have Δ_success > −δ_c.
- (c) In any cell, the upper bound of success(R_b) − success(sPCE-total) is ≥ 0. This includes the "ladder floor" case:
  if even R7 is not demonstrably worse than the policy, H1b fails.
- (d) Fewer than 3 of the 4 cells are informative on success after the pre-test n* rule. Then H1 is "inconclusive on
  success" and only the BI part can be reported.

**Label rule (closes the escape clause).**
- A failure confined to κ_hi cells is still "**H1 rejected as titled**".
- The paper may then report "amortization supported for free repositioning only" as a partial result. The title and
  abstract must drop "cost-aware".

**Experiment design sketch.**
- **Datasets.** Libraries A and S. Per cell: 200 pilot, 500 validation and 1,000 paired test episodes. Probe-matched
  τ_κ (§1.2).
- **Baselines.** Random, coverage, G* (full), the G* ladder R_b (and the report-only walk), full-state greedy (row,
  S κ_hi), and the rollout planner (reference, S κ_hi).
- **Ablations (rows).** Full-state sPCE objective and No-NC-input at (S, κ_hi), 3 seeds.
- **Measurements.** Success, BI, translation / rotation / identity errors, executed probes, travel, latency (§2.3),
  multiply-adds, training CPU-h.

---

### H2 — Under travel cost, a non-myopically trained policy beats the strongest myopic selectors at the same probe-matched horizon, and the advantage is absent without travel (Idea 2, gated)

**Gate outcomes (pre-registered; decided on 2026-11-12, §4).**

| G1 (instrument) | G2 (headroom) | Status of Idea 2 | What the paper states |
|---|---|---|---|
| fail | — | **untested** | "The look-ahead estimator could not be validated on the exact notch control (recovered gap X vs exact Y), so headroom under travel was not measured." H2 is not run. |
| pass | fail (after the single permitted escalation, if eligible) | **refuted in the tested range** | "Idea 2 is refuted for κ ≤ κ_hi(final), probe-matched n*, set S: the validated rollout-improvable headroom over cost-aware greedy is G(κ_hi) = x (one-sided 95 % UB u), G(0) = y (UB v)." It appears in the abstract as a negative result. The scope is stated: the estimator measures one-step-deviation (rollout) headroom, which lower-bounds the true optimum's headroom. H2 policies are not trained. |
| pass | pass | **tested** | H2a/H2b are run as below and confirmed or rejected by their failure conditions. |

**Rationale.**
- **Gap.** The myopic vs non-myopic gap for touch has not been measured (Gap 2). Greedy is near-optimal under adaptive
  submodularity (javdani2012efficient). Non-myopia matters when actions constrain the future (chen2015submodular;
  esfandiari2019adaptivity).
- **Why v1 found nothing.** With free repositioning and precise contacts, information that a planner could set up with
  probe t can be bought by greedy at probe t + 1 at the same price. This is an informal argument for the stage 8.5 note.
- **Why travel changes this.** A probe's value now depends on where the finger ends up. A cost-aware greedy selector
  maximises immediate EIG_B per unit time. It can then strand the finger far from the region that separates the
  remaining hypotheses: on S, the single notch / chamfer / bump that breaks a base shape's symmetry. A total-objective
  policy that sees φ_t and τ_rem can accept a lower-rate probe now in exchange for a cheaper route to that region.
- **Why set S.** S is the primary set for H2 for two reasons:
  - its decision-relevant information is spatially localised in one feature, which is the proposed mechanism;
  - A is closer to the ceiling at κ = 0 (0.767 at T = 3 in v1), which threatens §1.7.

  The proposer's "set A only" is changed accordingly.
- **Literature (risk 1/2 of 07a, skeptic "novelty").**
  - Budgeted / orienteering informative path planning (where greedy can be weak) and budgeted adaptive submodularity
    (where cost-benefit greedy has constant-factor guarantees) pull in opposite directions.
  - **Before stage 9, ≥ 3 such references are verified** (no citation before verification). The stage 8.5 note states
    what gap size those guarantees permit, so that the measured G(κ) and Δ can be placed against theory.
  - No confirmatory threshold depends on this.

**Horizon de-confounding (skeptic's most serious point).**
- With probe-matched budgets (§1.2), G* executes n* probes on average at both κ = 0 and κ_hi. The κ = 0 cell is the
  "short horizon, no travel" cell the skeptic asked for, and the κ_hi cell is "same horizon, travel".
- A Δ that appears only at κ_hi is attributable to travel. A Δ at both is attributable to horizon or training and fails
  H2 (failure (c)).
- The 3-point dose–response slope is **dropped** as a confirmatory claim (it was nearly implied by design). κ_mid
  survives only as a G2 level.

**Arms (S only).**
- sPCE-total at κ = 0 and κ_hi: the same 12 runs as H1's S cells.
- sPCE-myopic(rate) at κ = 0 and κ_hi: 6 seeds each.
- G* (full), on 1,000 paired test episodes per cell.
- The "strongest myopic selector" is **both** G* and sPCE-myopic(rate), combined by an intersection–union rule.
  There is no validation-based choice of M*.

Write Δ_X(κ) = metric(sPCE-total) − metric(X) for X ∈ {G*, myopic}.

**Measurable prediction (all must hold; intersection–union).**
1. **H2a-1 (effect vs cost-aware greedy at κ_hi).** Δ_G*,success(κ_hi) ≥ **3 pp** (point) with one-sided 95 %
   **LB > 0**, and Δ_G*,BI(κ_hi) LB > 0.
2. **H2a-2 (effect vs learned myopic at κ_hi).** Δ_myopic,success(κ_hi) ≥ 3 pp with LB > 0, and Δ_myopic,BI(κ_hi)
   LB > 0.
3. **H2a-3 (interaction: travel-specific).** The LB of [Δ_G*,success(κ_hi) − Δ_G*,success(0)] is > 0. The two cells
   are bootstrapped jointly; their episode sets are independent.
4. **H2a-4 (negative control at κ = 0).** |Δ_G*,success(0)| ≤ 3 pp (point) **and** TOST with ±3 pp margins passes
   (both one-sided p < 0.05). BI TOST ±0.10 nats is reported as a secondary result.
5. **H2a-5 (seeds).** ≥ 5 of 6 sPCE-total seeds have Δ_G*,success(κ_hi) > 0 (point).
6. **H2b-P1 (set-up value on disagreeing beliefs).**
   - Take 100 beliefs at (S, κ_hi), reached by running G* for a uniform number of steps in {0, …, n*−1} on fresh
     episodes.
   - The disagreement rate is the fraction of beliefs where the seed-majority sPCE-total action ≠ G*'s action. It must
     be **≥ 20 %**.
   - On the disagreeing beliefs: Q_g(b, a) = expected BI gained by executing a and then G* until the budget ends,
     estimated with the **G1-validated estimator** (same CRN and re-estimation settings).
   - Required: mean[Q_g(b, a_π) − Q_g(b, a_G*)] ≥ **0.05 nats**, with bootstrap LB > 0.
   - The immediate EIG_B/c deficit of a_π is reported, not tested; it is true by definition.
7. **H2b-P2 (exact notch control: learnability of set-up moves).**
   - Use the v1 H2b-P2 notch scenario: identity target, T = 2, exact likelihood on the 401-point grid, 6 seeds per
     objective.
   - Fraction of the exact gap closed: f = (V_π − V_greedy)/(V_opt − V_greedy), where the exact values are
     ≈ 0.2 / 0.69 nats.
   - sPCE-total: seed-mean **f ≥ 0.6**, with ≥ 5/6 seeds at f ≥ 0.5 and a horizontal first probe in ≥ 80 % of
     episodes. sPCE-myopic: seed-mean **f ≤ 0.2**.
   - *Why a gap exists here at κ = 0 without contradicting the premise.* The notch is a constructed instrument control
     in which the nuisance x must be localised before the identity feature can be targeted (a pure set-up move). It
     shows that set-up value *can* exist without travel. The v2 premise is not "no gap without travel". It is that on
     the natural libraries the measured headroom at κ = 0 is ≤ 0.03 (G2 requires this to be measured), and that
     travel creates headroom there.
8. **H2b-P3 (route structure, not "any sweep").** At (S, κ_hi):
   - (i) direction reversals of Δφ per episode: sPCE-total < G*, paired bootstrap LB of the difference > 0;
   - (ii) BI per unit travel (ratio of means, bootstrap): sPCE-total > coverage, LB > 0. Computed only if both
     methods' mean travel is ≥ 0.25 half-circles; otherwise P3(ii) is "not estimable" and counts as failed.

**Diagnostics with labelling rules (pre-registered).**
- **Training dynamics.** Learning curves and plateau epochs are shown for total vs myopic.
  - If sPCE-myopic(rate) is not within δ_c of G* at a κ (the H1a criterion), the learned-myopic arm is labelled
    "under-trained". H2a-2 is then reported but **cannot by itself carry the claim**: H2a-1 must hold.
- **Terminal bookkeeping.** Δ_G*,BI(κ_hi) is decomposed into the last executed step and earlier steps. Executed probes
  per method are reported.
  - If > 50 % of Δ_BI comes from the last step **and** executed probes differ by < 0.2, the effect is labelled
    "terminal-step effect" and H2b fails.
  - Infeasible actions cannot occur (§1.2).
- **Transparency.** R_NC, executed probes, travel and the rollout planner's success and latency at (S, κ_hi).

**Failure condition.** With G1 and G2 passed:
- **H2a is rejected** if any of these holds:
  - (a) Δ_G*,success(κ_hi) LB ≤ 0 or point < 3 pp, or Δ_G*,BI(κ_hi) LB ≤ 0;
  - (b) the same for Δ_myopic (unless myopic is labelled under-trained, see diagnostics);
  - (c) the interaction LB ≤ 0, **or** |Δ_G*,success(0)| > 3 pp, **or** TOST at κ = 0 fails ("not travel-specific");
  - (d) fewer than 5 of 6 seeds satisfy H2a-5.

  Partial label: if (b) passes but (a) fails, the paper may state only "non-myopic credit assignment helps a learned
  policy". It may not state "learned look-ahead beats cost-aware greedy", and H2a is rejected as titled.
- **H2b is rejected** if P1 (disagreement < 20 %, or mean < 0.05 nats, or LB ≤ 0), P2 (f_total < 0.6 or < 5/6 seeds
  ≥ 0.5, or f_myopic > 0.2), or P3 (i or ii) fails, or the terminal-step label applies. If H2a passes and H2b fails, the
  paper reports "a travel-specific non-myopic advantage, mechanism not supported".

**Power for the negative control (skeptic: "TOST may be unreachable").**
- From G3 pilot seeds and the G5 pilot, estimate the episode and seed variance components and project SE(Δ_G*(0)).
- If the projected TOST power at true Δ = 0 is < 0.80 with 1,000 episodes, the (S, κ = 0) test set grows to 2,000
  before the main run (compute reserve, §6).
- The margin is never widened. If power is still < 0.80, this is stated next to the result.

**Experiment design sketch.**
- **Dataset.** S. Cells κ ∈ {0, κ_hi} at probe-matched τ; 1,000 paired test episodes per cell.
- **Baselines.** G* (primary), sPCE-myopic(rate) (primary ablation, same network and input), coverage (for P3), and
  the rollout planner (upper reference).
- **Ablations.** Full-state sPCE objective, No-NC-input (rows; shared with H1), full-state greedy (row).
- **Mechanism.** P1 belief bank (100), notch control (P2), route statistics (P3).

---

## 4. Pre-run gates G0–G5 (numeric pass rules; all on CPU, before any main run; changes go into `docs/07c_amendment_v2_0.md` before a check is re-run)

| gate | date | check | pass rule | if it fails |
|---|---|---|---|---|
| **G0** hygiene | by 11-08 | (i) Record the 16/8/16/16 deviation (done in 07c A6). (ii) Recompute the S self-symmetry entries. (iii) Amend A's per-shape rule (§1.1). (iv) Add v1's missing greedy-T10 and pilot-policy PF cells (300 episodes). (v) Report greedy vs random at T = 5. (vi) κ = 0, τ = 3 bit-identity unit test (§1.2). (vii) Gradient check of the categorical head. (viii) Ball-EIG and ball-sPCE unit tests: on a 2-hypothesis toy, both agree with the exact ball-information increment within MC error. | All 8 items done, with a commit hash. Unit tests (vi)–(viii) green in CI. | Nothing downstream starts. |
| **G1** estimator validation | by 11-09 | Exact notch values on the 401-point grid. Fixed look-ahead estimator: CRN across candidates; screen C1 = 32 candidates including structured set-up moves (antipodal travel, travel to the region of maximal mode disagreement); re-estimate the top 4 with 4× fresh samples; horizon = remaining budget, completed by G* rollouts at rung R3. | (a) The estimated relative gap is within ±20 % of the exact relative gap (exact ≈ 0.7, so [0.56, 0.84] if exact = 0.70). (b) On a bank of 100 beliefs with exact gap 0, the mean estimated gap is in [−0.01, +0.02] with one-sided 95 % UB < 0.03. The added positive-bias guard stops a biased estimator from passing G2. | Idea 2 **untested** (§3, H2 gate table). H2 is not run. Fallback compute plan (§6). |
| **G2** headroom under travel | by 11-11 (escalation by 11-12) | Validated estimator on 100 beliefs per κ ∈ {0, 2, 6} on S, reached by G* (uniform step in {0, …, n*−1}). Target J_B. **Unit:** G(κ) = [mean V_LA − mean V_G*] / mean V_LA, a dimensionless relative gap in expected remaining-budget ball information (ratio of means over beliefs). V_LA = the best re-estimated look-ahead candidate completed by G*; V_G* = G* from b. The absolute gap in nats is reported. | G(6) ≥ **0.10** with one-sided 95 % bootstrap LB > **0.05**; G(0) ≤ **0.03** (point; UB reported); G(0) ≤ G(2) ≤ G(6) (point; ties pass). | If eligible (§1.2), one escalation to κ_hi = 12 with the same rules (G(12) replaces G(6) in the ordering). Otherwise Idea 2 is **refuted in the tested range** (§3), and the fallback plan applies. |
| **G3** learnability | by 11-12 | (i) 4 hyperparameter configurations × 1 seed at (S, κ_hi). (ii) 3 pilot seeds of the chosen configuration at (S, κ_hi). (iii) sPCE-total on the notch control, 3 seeds. (iv) ball-sPCE vs evaluation-PF BI bias on 500 validation episodes. | Notch: seed-mean ≥ **80 % of the exact optimum**. (S, κ_hi): seed-mean validation success ≥ success(G*) − **5 pp**, with plateau within the E_train cap. Objective saturation (g_T within 0.5 nats of log(L+1)) in < 10 % of training episodes. (iv) is reported. | One remedy: the E_train cap doubles for **all** learned methods; re-check by 11-14 (main runs shift by 2 days into the buffer). If it still fails: halt and go to stage 15 with learnability failure as the finding. If κ_hi was escalated in G2, (ii) is re-run at κ_hi = 12 (+4 CPU-h). |
| **G4** evaluation PF | by 11-10 | N_eval = 32,000 (3 MH steps) vs reference 128,000 (4N, 07c A3). 600 paired episodes per cell (S/A × κ = 0/κ_hi), 200 each from random, G* and a pilot policy (G3 seed). | \|Δ BI\| ≤ 0.05 nats; \|Δ success\| ≤ 1 pp (point) with 95 % CI inside ±2 pp. If only the CI width fails, the cell is extended once to 1,200 episodes. | Replace the kernel with 10 MH steps per move, validated against 32k × 30 MH steps on the same episodes, under the same rule. Its cost enters §6 through the downscale order. N_eval > 32k is not affordable. |
| **G5** comparator strength and resolution | by 11-10 | G* vs random on 300 pilot episodes per primary cell (A0, A_hi, S0, S_hi). Rollout planner latency on 20 decisions at (S, κ_hi). Flatness check of 𝒜 (§1.5). n* and τ_κ calibration (§1.2). Non-degeneracy (§1.7). | G* ≥ random + **10 pp** in every primary cell (the §1.7 cell rule then additionally requires D ≥ 20 pp). Flatness: \|Δ success\| ≤ 2 pp and \|Δ BI\| ≤ 0.10 nats. Planner latency recorded. | A cell that fails after the one n* adjustment is removed from the primary set (reported). A flatness failure moves 𝒜 to 64 × 8 for all methods. |

**Gate decision on 2026-11-12.** Idea 2 is in (G1 ∧ G2 pass, with G3/G4/G5 also passed), or the fallback applies.
**No main run starts before G0, G3, G4 and G5 pass.** G1/G2 failures do not block H1.

---

## 5. Pre-registered analysis plan

1. **Freeze before main runs** (commit hash recorded in `docs/`):
   - n* per set and τ_κ per cell; κ_hi (6 or 12); the action set 𝒜;
   - N_eval / kernel; informative cells; D_c, δ_c and ε_c;
   - test-set sizes (power rules); the ladder and R_b per cell (from latency measurements);
   - hyperparameters; the G1 estimator settings.
2. **Unit and inference.**
   - The unit is the paired test episode, with seed-averaged outcomes per learned method.
   - Crossed episode × seed bootstrap, B = 10,000, one-sided 95 % percentile bounds. Bootstrap p-values = the fraction
     of resampled statistics on the null side.
   - The H2a-3 interaction bootstraps the two cells' independent episode sets jointly.
   - Ratio statistics (P3(ii), G(κ)) use the ratio of means, with denominator guards stated where they are defined.
3. **Margins.**

   | Margin | Value |
   |---|---|
   | NI, success | δ_c = min(4 pp, **0.15 × D_c**), where D_c is the pilot random→G* gap (≥ 20 pp), so 3–4 pp |
   | NI, BI | ε_c = min(0.05·BI_c(G*), **0.15 × D_c^BI**) nats |
   | H2 SESOI | 3 pp on success; LB > 0 on BI |
   | TOST | ±3 pp on success; ±0.10 nats on BI (secondary) |
   | H2b-P1 | 0.05 nats; disagreement ≥ 20 % |
   | H2b-P2 | f ≥ 0.6 (total) / ≤ 0.2 (myopic) |
   | H1b | 100× latency |
   | Gates | as in §4 |

   The fraction-of-gap form makes "non-inferior" mean the same thing (≤ 15 % of the gap lost, capped at 4 pp) on A and S.
4. **Families and multiplicity.**

   | family | tests | combination | correction |
   |---|---|---|---|
   | H1a | 4 cells × (success, BI) + seed rule | all must pass | none (intersection–union) |
   | H1b | 4 cells | all must pass | none (IU) |
   | H1 sanity | 8 (2 baselines × 4 cells) | reported only | Holm |
   | H2a | H2a-1 … H2a-5 | all must pass | none (IU) |
   | H2b | P1, P2, P3(i), P3(ii) | all must pass | none (IU) |
   | gates | G1–G5 rules | as stated | none |

   There is no correction across H1 and H2: they are separate claims, each with its own decision.
5. **Power rules.**
   - H1a: the pilot (G3 + G5) projects SE(Δ_success) per cell. If SE > δ_c / 2.5 in a cell, that cell's test set grows
     to 2,000.
   - H2a-4: the TOST power rule in §3.
   - At most two cells may grow. If more need to, the downscale order (§6) is applied first.
6. **Seed rule.** ≥ 5 of 6 seeds in the stated direction (H1a: Δ > −δ_c; H2a: Δ > 0). Per-seed bounds are reported.
7. **Reporting.**
   - Every outcome uses the labels defined in §3 (confirmed / rejected / rejected as titled / partial / untested /
     refuted in tested range / non-informative cell).
   - No post-hoc cell selection. Exploratory analyses are labelled as such.
   - Gate results are reported in full whatever the outcome.

---

## 6. Compute estimate (CPU-h; re-checked by a TIME_ESTIMATE pilot before every sweep)

**Unit costs.**
- **Training run** (E_train = 10⁵, L = 4095, ≈ n* = 4 steps): **≈ 1.2 CPU-h**. Basis: 07c A4 gives 65–80 ms per episode
  at v1's mean T ≈ 6.5, scaled to ≈ 4 steps; CI runners give 30–60 ms.
- **Evaluation PF** at 32k: **≈ 3 s per episode**. Basis: 07c A4 ≈ 1 s at 8k, × 4, × 0.75 for ≈ 4 probes.
- **Full-size G\*** (C = 256): **≈ 2.6 s per decision**. Basis: 0.65 s at C = 64, × 4. With ≈ 4 decisions, that is
  ≈ 10.4 s per episode, plus 3 s of evaluation PF.

**Main runs (gate G2 passed).**

| item | volume | CPU-h |
|---|---|---|
| sPCE-total training, {A, S} × {0, κ_hi} × 6 seeds (H1; S cells shared with H2) | 24 runs | 28.8 |
| sPCE-myopic(rate) training, S × {0, κ_hi} × 6 seeds (H2) | 12 runs | 14.4 |
| Ablation rows (full-state sPCE, No-NC-input) at S κ_hi × 3 seeds | 6 runs | 7.2 |
| Test evaluation, learned: 36 policy-seeds × 1,000 eps × 3 s; ablations 6 × 500 × 3 s | — | 32.5 |
| G* test: 4 cells × 1,000 eps × 13.4 s | — | 14.9 |
| Random + coverage test: 8 cell-methods × 1,000 × 3 s | — | 6.7 |
| Full-state greedy row (S κ_hi, 500 eps) | — | 1.9 |
| H1b: R_b and next-cheaper rung on 4 × 1,000 test eps (evaluation PF dominates); report-only ladder walk at S κ_hi (500 eps); latency benchmarks | — | 9.0 |
| Rollout planner reference (S κ_hi, 200 eps) | — | 3.5 |
| H2b: P1 bank (100 beliefs, Q_g for 2 actions), P2 notch (6 + 6 seeds, exact), P3 from logs | — | 2.0 |
| **Total main (H1 + H2)** | | **≈ 121** |

- **Fallback (G1 or G2 fails):** the H2 myopic runs become an ablation row (S κ_hi × 3 seeds, 500 episodes), and the
  H2b items are dropped. Main total ≈ **99 CPU-h**.
- **Pre-run gates (separate budget, 11-08 → 11-12):** ≈ 47 CPU-h in total.
  - TIME_ESTIMATE: 1. G0: 4. G1: 3.
  - n* / τ calibration: 3.7. G5 and flatness check: 5.5.
  - G2: 3 κ × 100 beliefs ≈ 7.5, plus escalation 2.5.
  - G3: hyperparameters 4.8 + 3 seeds 3.6 + notch 0.5 + validation evaluation PF 1.3.
  - G4: 4 cells × 600 eps × (3 + 12) s ≈ 10.
- **Reserve.** Up to two power-rule cell enlargements (≈ 8–15 CPU-h each) and one plateau-rule cap doubling are covered
  by the downscale order. Main-run total stays ≤ ≈ 120 CPU-h.

**Downscale order (if the TIME_ESTIMATE or the reserve pushes the main total above 125 CPU-h):**
1. ablation rows → 2 seeds;
2. the report-only H1b ladder walk is dropped;
3. the full-state greedy row is dropped;
4. the rollout planner → 100 episodes;
5. H2 myopic seeds 6 → 5 (seed rule becomes ≥ 4 of 5).

H1 primary seeds, cells and test sizes are never reduced.

**Fit to hardware and dates.**
- Each training run (≈ 1.2 CPU-h, ≤ 2.4 h if the cap doubles) and each evaluation shard fits in one ≤ 6 h job.
  `time_guard` stops at 80 %.
- With ≈ 20 concurrent 2-vCPU jobs (≈ 40 single-thread processes), the 42 main training runs take one wave of
  ≈ 2.5 h. The ≈ 70 CPU-h of evaluation sharded across 40 processes takes ≈ 2 h.

| dates | stage | work |
|---|---|---|
| 10-29 → 10-31 | 8 | This file. Verify ≥ 3 IPP / budgeted adaptive-submodularity / cost-aware BED references. |
| 10-31 → 11-02 | 8.5 / 9 | Theory note; `08_experiment_plan.yaml` v2. |
| 11-02 → 11-08 | 10 | Code: travel environment, categorical head, ball-sPCE, ball-EIG / G*, ladder, rollout planner, fixed estimator, exact notch. |
| 11-08 → 11-12 | 11–12 | Gates G0–G5. **Gate decision 11-12.** |
| 11-12 → 11-18 | 13 | Main runs (≈ 5 h of runner wall-clock for training + evaluation, scheduled over several days to absorb queueing and re-runs). |
| 11-18 → 11-22 | — | Buffer: one plateau-doubling re-run or one power enlargement. |
| 11-22 → 11-26 | 14–15 | Analysis, then decision. |
| 11-26 → 12-03 | 16+ | Extended abstract (due 12-04). |

---

## 7. Critique → resolution map

| Skeptic point (07b_skeptic_v2.md) | Resolution |
|---|---|
| X1 κ = 0 is not v1 (τ fits 8–10 probes; different horizon) | Probe-matched budgets. κ = 0 has τ = n* ∈ {3, 4, 5} = v1-style T. The unit test is renamed to "κ = 0 and τ = 3 reproduces v1" (§1.2). |
| X1 saturation at 8–10 probes | There are no long-budget cells. n* is chosen by the pilot ceiling/floor rule (§1.2, §1.7). |
| X2 success / ball information undefined | Defined inline with radii, prior mass and PF estimator (§1.3). |
| X3 no ceiling/floor rule | Informative-cell rule: G* ∈ [0.15, 0.90], D ≥ 20 pp, BI saturation < 50 %, checked on pilot and test (§1.7). |
| X4 action resolution not matched | One shared 256-action set; categorical policy head; flatness check vs a 1,024 grid (§1.5, G5). |
| X5 greedy objective ≠ policy objective | Everyone optimises J_B (ball information): ball-sPCE, ball-EIG/c, evaluation BI (§1.4). Full-state greedy is a separate row. |
| H1 ratio CI unstable | Replaced by a difference with an ε_c margin in nats (§3, H1a-2). |
| H1 latency scope / hardware / threads / framework | §2.3: y_t → a_{t+1} including PF update; selection-only also reported; one core; numpy; warm-up 20, 500 timed decisions; multiply-add counts. |
| H1 ladder grid not given | §2.3 table R0–R7 (nested). |
| H1 G*_match matched to greedy, not to the policy; "within 1 pp" below MC resolution | No selection. The boundary rung (< 100× latency) must be **significantly worse than the policy** on the test set (UB < 0). Matched-to-policy and matched-to-greedy ratios are reported (§3, H1b). |
| H1 ceiling / flat 4 pp means different things on A vs S | δ_c = min(4 pp, 0.15·D_c) plus the informative-cell rule (§1.7, §5). |
| H1 latency from implementation quality | Vectorised greedy as comparator; multiply-add ratio reported (§2.2, §2.3). |
| H1 "beats random/coverage" trivial | Sanity check, Holm-reported, not a failure condition (§3, H1-6). |
| H1 full-size ratio trivial | Reported without a threshold (§3, H1-5). |
| H1 seed rule loose | Kept as a secondary rule; per-seed LBs reported (§3, H1a-3). |
| H1 escape clause | A κ_hi-only failure = "H1 rejected as titled"; "cost-aware" leaves the title (§3, H1 label rule). |
| H2 G has no unit | G(κ) = relative gap in expected remaining-budget ball information (ratio of means); absolute nats also reported (§4, G2). |
| H2 κ grid by "≈ probes", escalation undefined | κ ∈ {0, 2, 6} fixed. One escalation to 12 with an explicit trigger (§1.2). |
| H2b-P1 "remaining-budget value" undefined | Q_g(b, a) = expected BI from a, then G* to budget end, estimated with the G1-validated estimator (§3, H2b-P1). |
| H2 myopic γ = 0 ignores cost | sPCE-myopic(rate): r/c, γ = 0, the learned analogue of G*. The residual difference is stated honestly (§2.1). |
| H2 (c) almost impossible to trigger | Fails if \|Δ(0)\| > 3 pp **or** TOST fails; plus a pre-registered power rule (§3). |
| H2b-P2 not in failure set | It is in the failure set, stated as fraction of gap closed (§3, H2b-P2). |
| H2 gate makes H2 unfalsifiable | G1 fail = untested; G1 pass + G2 fail = **refuted in tested range**, stated in the abstract with the UB (§3, H2 gate table). |
| H2 mechanism 1: horizon / saturation confounded with κ | Probe-matched τ_κ; the κ = 0 cell is the short-horizon no-travel cell; interaction test H2a-3; dose–response slope dropped (§1.2, §3). |
| H2 mechanism 2: budget-feasibility bookkeeping | Feasibility mask for all methods; terminal waste < 1 stroke by construction; last-step decomposition with a labelling rule (§1.2, §3 diagnostics). The skeptic's "executed probes differ < 0.2" is not imposed as a requirement, because travel economy (more probes in the same time) is part of the claimed effect. It enters the terminal-step rule instead. |
| H2 mechanism 3: objective mismatch / resolution grow with κ | §1.4, §1.5. |
| H2 mechanism 4: γ = 1 vs γ = 0 training dynamics | Curves and plateau epochs reported. A myopic arm not within δ_c of G* is labelled under-trained and cannot carry the claim alone (§3 diagnostics). |
| H2b-P1 half-tautological; dilution | Only the deviation value is tested, on disagreeing beliefs only, with ≥ 20 % disagreement required. The EIG/c deficit is reported only (§3). |
| H2b-P2 thresholds trivially met; notch at κ = 0 | f ≥ 0.6 / ≤ 0.2 of the exact gap. The notch is explained as a constructed instrument control (§3). |
| H2b-P3 met by any sweep; ratio denominator | Reversals vs G* **and** BI per unit travel vs coverage; denominator guard (§3). |
| H2 slope nearly implied by design | Dropped. Present at κ_hi and absent at κ = 0 under a matched horizon, plus the interaction (§3). |
| Novelty / theory tension (IPP vs budgeted adaptive submodularity) | ≥ 3 references verified before stage 9. The stage 8.5 note places the measured G and Δ against the permitted gap size. No threshold depends on it (§3, H2 rationale). |
| Proposer risk 4: evaluation PF convergence | G4 must pass before any H1/H2 number is reported (§4). |
| Proposer risk 5: matched-accuracy grid | Ladder pre-registered; no search (§2.3). |
