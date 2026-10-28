# Stage 8 · HYPOTHESIS_GEN — final hypotheses (Pass 3 Methodologist, fresh opus subagent, 2026-10-28)

> System: "You are a methodology lead synthesizing a proposer and a skeptic into final, defensible hypotheses."
> Task: "Produce the final hypothesis set, addressing every critique. For each surviving hypothesis include: rationale, measurable prediction (with concrete metric and threshold), failure condition (with concrete metric and threshold), and the experiment design sketch (datasets / baselines / ablations needed)."
> `{proposer_output}` = full content of `docs/07a_proposer.md`; `{skeptic_output}` = full content of `docs/07b_skeptic.md`.
> Feasibility constraints (from `docs/00_topic_init.md`): CPU only (2 vCPU / 7 GB sandbox, plus free GitHub Actions CPU runners); simulation only (numpy geometric probe model, MuJoCo physical-contact check); known object library; static object; SE(2) pose + identity. Total compute is held to about 70 CPU-hours (see §7).

## 0. Outcome of the debate

| Proposer | Skeptic verdict | Final form |
|---|---|---|
| H1 | REVISE | Split into **H1a** (accuracy non-inferiority to greedy EIG, superiority to random/coverage), **H1b** (latency at matched accuracy; the fixed-configuration ratio is demoted to a measurement), **H1c** (information objective vs sparse task reward). The PF-entropy-reward RL baseline becomes a secondary estimator comparison. |
| H2 | REVISE | **H2a** (outcome: non-myopic advantage on ambiguous sets at small budget), **H2b** (mechanism: set-up moves, via an oracle two-step EIG analysis and an analytic positive control), **H2c** (shrinkage with budget, secondary). The myopic control's loss is written out (§3) and differs from the treatment **only** in credit assignment. |
| H3 | REVISE | **H3** (planning for no-contact outcomes), with a normalized conditional-likelihood ablation whose bias is derived (§3.4). Both ablations are required, the effect size appears in the failure rule, and mechanism measurements are added (P(NC) at selection, NC-branch EIG share, contact-only probe check). |
| H4 | REVISE | **H4** (geometric → MuJoCo transfer). The fidelity shift is pre-registered and measured, and fingertip radius is swept at 3 levels. Kendall τ is replaced by sign preservation on pre-separated pairs. The 10 pp absolute criterion is restored. 1,000 scenes per cell. |
| H5 | REJECT | Dropped as a hypothesis. The latency sweep is kept as a measurement under H1b. Replaced by **H5′** (accuracy cost of amortization as K grows). |

A table mapping each critique to its resolution is in §8.

---

## 1. Global definitions

### 1.1 World, actions, observations

- **Objects.** Planar simple polygons. Every shape is scaled so that its **circumradius about its centroid is R = 40 mm**, and its smallest feature (edge, notch or bump) is ≥ 6 mm. The object frame sits at the centroid.
- **State.** s = (k, x, y, θ). **Prior:** k ~ Uniform{1..K}; x, y ~ U[−15, 15] mm; θ ~ U[0, 2π).
- **Exact symmetry group G_k.** The set of rotations that map shape k onto itself (computed by IoU ≥ 0.999). Rotation error is always measured modulo G_k, so success is attainable for exactly symmetric shapes.
- **Action (probe).** a = (φ, ψ). The probe starts at 100·(cos φ, sin φ) mm and points in direction φ + π + ψ, with ψ ∈ [−40°, 40°] and a 200 mm stroke (guarded move). Baseline candidate sets are scrambled-Sobol draws from the same (φ, ψ) box.
- **Observation.** If the ray hits the shape: y = (contact point + N(0, σ_p² I), normal angle + N(0, σ_n²)), with **σ_p = 1.0 mm** and **σ_n = 5°**. Otherwise y = ∅ (no contact, NC).
- **Likelihood used everywhere** (training, greedy, evaluation PF): ε-softened, p_ε(y | s, a) = (1 − ε)·p_geom(y | s, a) + ε·u(y), with **ε = 10⁻³**. Here u is uniform over {∅} ∪ (workspace disc × normal circle), with mass ½ on each branch. This prevents zero likelihoods. One code path computes this likelihood for every method.

### 1.2 Object sets and the quantitative ambiguity definition

- **A (K = 8), asymmetric/dissimilar.** Eight irregular polygons with 8–14 vertices, generated from a fixed seed. A shape is accepted only if G_k is trivial and the confusability scores below are ≤ 0.80.
- **S (K = 8), ambiguous.** Four near-symmetric *base* shapes: a 2:1 rectangle, a rounded equilateral triangle, a regular hexagon and an isosceles trapezoid. Each base is paired with a *variant* that differs by one local feature (a notch, chamfer or bump, 6 mm wide and 3–4 mm deep) placed so that it breaks the base's symmetry. Bases may have non-trivial G_k. Variants have trivial G_k, so their orientation is identifiable only through the feature.
- **A4 ⊂ A8 ⊂ A16** (for H5′): A8 is set A. A16 adds eight more shapes generated under the same rule. A4 is the first four shapes of A.
- **Geometric confusability.** Pairwise c(k, k′) = max over (x, y, θ) of IoU(shape k, T_{x,y,θ}·shape k′). It is found by grid search (0.5 mm, 1°) followed by Nelder–Mead refinement. Self near-symmetry c_self(k) = max over θ more than 10° from G_k of IoU(k, R_θ·k). Set level: C(O) = mean_k max(c_self(k), max_{k′≠k} c(k, k′)). **Requirement: C(S) ≥ 0.90 and C(A) ≤ 0.80.**
- **Decision-relevant ambiguity (the independent variable of H2): the myopia gap.**
  - **Belief bank B_O** (100 beliefs per set): the prior, plus 99 posteriors obtained by drawing a random true state and applying 1–2 random probes (about half each).
  - For each belief b, let EIG₁(a; b) be the one-step EIG. Define the optimal two-step value EIG₂*(b) = max_{a₁} [EIG₁(a₁; b) + E_{y₁} max_{a₂} EIG₁(a₂; b ⊕ (a₁, y₁))].
  - EIG₂^greedy(b) is the same quantity with a₁ fixed to argmax EIG₁(·; b).
  - **Myopia gap: G(O) = mean_{b ∈ B_O} [(EIG₂*(b) − EIG₂^greedy(b)) / EIG₂*(b)].**
  - Computation uses nested MC with N = 1,000 particles, C = 32 candidates at each level and M = 32 outcome samples. About 0.5 s per first action, so about 1 CPU-h for both sets.
  - **Requirement (manipulation check, verified before any main run): G(S) ≥ 0.10 and G(A) ≤ 0.03.** If it fails, S is redesigned (deeper or more off-center features) and the check is re-run. Main runs do not start until it passes.
  - Also reported for each set: the mean of max_a EIG₁ (so that "S is just harder" is visible), and **NC-relevance R_NC(O)**. R_NC(O) is the fraction of bank beliefs whose EIG₁-maximizing action has predicted P(NC) ∈ [0.2, 0.8] (used by H3).

### 1.3 Success metric and the non-saturating co-primary metric

- **Point estimate.** k̂ is the identity with the largest posterior mass. The pose is the highest-posterior particle of identity k̂, refined by 30 Nelder–Mead iterations on the log-posterior with k̂ fixed.
- **Success** = [k̂ = k₀] ∧ [‖(x̂, ŷ) − (x₀, y₀)‖ < **5 mm (= 0.125 R)**] ∧ [min_{g ∈ G_{k₀}} |wrap(θ̂ − θ₀ − g)| < **5°**]. At the circumradius, 5° of rotation corresponds to 3.5 mm of arc, so the two thresholds are of similar strictness.
- **Co-primary, non-saturating metric: realized information gain**
  IG_T = log p̂(s₀ | h_T) − log p(s₀).
  Here p̂(s₀ | h_T) is the PF posterior mass of k₀ times a KDE over k₀'s particles. The KDE uses bandwidth 1 mm in translation and 1° in rotation, with rotation wrapped modulo G_{k₀}. p̂ is floored at 10⁻³·p(s₀), so IG_T ≥ −6.9 nats.
  Because E[log p(s | h) − log p(s)] = I(s; h_T), the mean of IG_T estimates the policy's **true total EIG**. It is the "high-N estimate of true EIG" that the skeptic asked for. It is reported for every method in every cell.
- **Saturation rule.** A cell (set, T, fidelity) is *success-testable* for a comparison only if the pilot (§1.5) puts both compared methods' success in [10 %, 90 %]. Every directional claim must hold on IG_T in all cells, and also on success in success-testable cells. The success-testable cell list is frozen after the pilot and before the main runs.

### 1.4 Evaluation particle filter (identical for every method; methods differ only in which probes they choose)

- **N_eval = 10,000 particles.** Initialized stratified: N_eval/K per identity, with pose from a scrambled Sobol sequence over the prior box.
- Observations are assimilated one at a time with the ε-softened likelihood.
- When ESS < N_eval/2: systematic resampling, followed by **resample-move**. This is 3 Metropolis–Hastings steps per particle against the full-history likelihood. Proposals: a random walk with σ_xy = 0.5 mm and σ_θ = 0.5° (identity fixed) with probability 0.9, or an independent prior draw with a new identity with probability 0.1. Resample-move prevents depletion for a static state.
- Every PF and nested-MC computation runs single-threaded (OMP/MKL threads = 1), with fixed per-episode RNG streams.
- **Convergence check (pilot, before main runs).** Use 300 pilot episodes × {A, S} × T ∈ {3, 10} × {random, pilot sPCE-total, full greedy}, and compare N_eval with 4·N_eval. The check passes if, for every method and cell: |Δ success| ≤ 1 pp (point estimate) with a 95 % CI inside ±2 pp, and |Δ mean IG_T| ≤ 0.05 nats. Otherwise N_eval is doubled and the check repeated, up to 40,000. A sensitivity check is also reported: method ordering on IG_T must not change when the KDE bandwidth is halved or doubled.

### 1.5 Episode sets, seeds and the statistical unit

- **Disjoint episode sets**, each drawn with its own fixed seed: pilot (200 per cell), validation (500 per cell, used for hyperparameter and checkpoint selection) and **test (2,000 per (set, T) cell)**.
- The test set is **shared by all methods** (a paired design). The first 1,000 test episodes are also the MuJoCo scenes.
- **Training seeds.** 10 for sPCE-total and sPCE-myopic (the core H2 contrast). 5 for every other learned method. The deterministic baselines (greedy, coverage) and random use one fixed RNG stream per episode.
- **Statistical unit.** The primary test is a **paired comparison over test episodes**. Each method's per-episode outcome is its mean over its training seeds (success fraction, or mean IG_T).
- **Seed variance in the CIs.** Uncertainty is estimated by a **crossed (two-way) bootstrap**, B = 10,000. Each resample draws episodes with replacement, using the **same indices for all methods** (this preserves pairing). It independently draws each learned method's seeds with replacement. The statistic is recomputed on each resample. One-sided bounds are percentile bounds. Bootstrap p-values are the fraction of resampled Δ* on the wrong side of the null.
- **Secondary replication factor (seeds).** For every *superiority* claim, each seed of the treatment is compared with the seed-averaged comparator on the same test episodes. The direction must hold in **≥ 8 of 10 seeds (or ≥ 4 of 5)**. Otherwise the claim is recorded as "rejected: not seed-robust".
- **Expected precision** (to be re-estimated in the pilot). A paired per-episode SD of about 0.35 on seed-averaged success gives an episode component of 0.35/√2000 ≈ 0.8 pp. A between-seed SD of about 2 pp contributes 0.6–0.9 pp per learned method. This gives **SE(Δ success) ≈ 1.0–1.5 pp**.
- **Power rule (pre-registered).** If the pilot projects SE(Δ) > 1.6 pp for any primary contrast, that cell's test set grows to 4,000 episodes. If that is still above 1.6 pp, the non-inferiority margin is widened from 4 to 5 pp. Both changes are declared before the main runs.

---

## 2. Methods compared

All learned methods share one architecture and are deterministic (policy mean) at evaluation.

- **Architecture.** The policy is budget-conditioned: π_φ(a_t | h_{t−1}, T − t + 1).
  - DeepSets history encoder: e(h) = ρ(Σ_τ ψ(a_τ, y_τ)). The sum is permutation-invariant, which suits a static object.
  - Each observation is encoded as (1[contact], p, cos n, sin n), with zeros on NC.
  - ρ and ψ are 2×128 MLPs. The head outputs a Gaussian over unconstrained (φ̃, ψ̃), mapped by φ = wrap(φ̃) and ψ = 40°·tanh(ψ̃).
  - About 50k parameters, PyTorch on CPU, one thread.
- **sPCE-total (ours)** and **sPCE-myopic (control).** The exact objectives are in §3.
- **RL-success** (task-reward baseline for H1c): γ = 1 with sparse terminal reward r_T = 1[success], computed by a training PF (same algorithm as §1.4, N = 1,000). All other rewards are 0.
- **RL-PFIG** (secondary estimator comparison): dense reward r_t = log p̂_t(s₀) − log p̂_{t−1}(s₀), from the same training PF and KDE. It telescopes to IG_T, so it is a *different Monte Carlo estimator of the same total-EIG objective*. Comparing it with sPCE-total therefore tests estimator quality, not the objective (as the skeptic noted). It is run on S only with 5 seeds, and no confirmatory claim is made.
- **Greedy PF-EIG.**
  - Online PF as in §1.4 with N particles. C candidates are re-drawn by scrambled Sobol at every step.
  - EIG(a) = (1/M) Σ_m [log p_ε(y_m | s_{j_m}, a) − log Σ_n w_n p_ε(y_m | s_n, a)], with j_m ~ w and y_m ~ p_ε(· | s_{j_m}, a).
  - It ray-casts all N particles per candidate once (N·C casts), then evaluates the M·N·C Gaussian terms in fully vectorized numpy.
  - **Full size: N = 2,000, C = 64, M = 64.** The Pareto sweep for H1b is in §4.
- **Coverage.** Picks the candidate (C = 64) that maximizes the minimum distance from its predicted contact point on the current MAP shape and pose to all previous contacts. This follows zheng2026bayesian.
- **Random.** A uniform draw over (φ, ψ).
- **Equal tuning and budget.**
  - Every learned method gets the same hyperparameter search: 12 configurations drawn from identical ranges (learning rate, entropy coefficient, batch size, critic learning rate), each trained for 10⁵ episodes on S with one pilot seed. **All methods are selected on the same criterion: validation success at T = 5.** This criterion is neutral to the information objectives.
  - The H3 ablations inherit sPCE-total's configuration.
  - **The training budget unit is environment episodes: E_train = 4·10⁵ episodes per run (10⁵ for each T ∈ {3, 5, 8, 10}, with T sampled uniformly per episode).** Likelihood evaluations, which include the L contrastive samples, and CPU-hours are reported separately for every method.
- **Convergence.** Validation is evaluated every 2·10⁴ episodes. A run counts as plateaued when the 5-evaluation moving average improves by < 0.5 pp. If any method in a comparison has not plateaued at the cap, the cap is doubled for **all** methods in that comparison. This addresses the skeptic's under-training mechanism.

---

## 3. Training objectives: non-myopic policy vs myopic control

### 3.1 Shared quantities (identical for both)

For each training episode:

- Draw T ~ U{3, 5, 8, 10}, the true state s₀ ~ p(s) and **L = 255** contrastive states s₁..s_L iid ~ p(s). These are fixed for the episode.
- Roll out a_t ~ π_φ(· | h_{t−1}, T − t + 1) and y_t ~ p_ε(· | s₀, a_t).
- With p(h_t | s) = Π_{τ ≤ t} p_ε(y_τ | s, a_τ) (the static object makes this factorize, and the policy terms cancel in the ratio), define

  g_t = log p(h_t | s₀) − log[ (1/(L+1)) Σ_{l=0}^{L} p(h_t | s_l) ],  g₀ = 0,

  **r_t = g_t − g_{t−1}**  (per-step sPCE increment, as in Blau et al. 2022).
- Then Σ_{t=1}^{T} r_t = g_T, and E[g_T] = sPCE_T(π; L) ≤ EIG_T(π) (Foster et al. 2021).
- As L → ∞, r_t → log p(y_t | s₀, a_t) − log p(y_t | h_{t−1}, a_t). Its expectation given h_{t−1} is the **one-step conditional EIG at the current posterior**.

### 3.2 sPCE-total (non-myopic)

  **J_tot(φ) = E_{T, s₀, s_{1:L}, h_T ∼ π_φ} [ Σ_{t=1}^{T} r_t ] = sPCE_T(π_φ; L).**

The gradient is the score-function form with full returns-to-go (γ = 1, no GAE), because outcomes are discrete (hit/miss, identity) and not reparameterizable:

  ∇_φ J_tot = E[ Σ_t ∇_φ log π_φ(a_t | h_{t−1}, T−t+1) · (G_t − V_ω(h_{t−1}, T−t+1)) ],  **G_t = Σ_{τ=t}^{T} r_τ.**

The critic V_ω minimizes E[(G_t − V_ω)²]. The update is PPO-clip (clip 0.2, 4 epochs per batch of 256 episodes, advantages normalized per batch, entropy bonus β_H). Action a_t is credited with **every later information increment it enables**. This is the credit assignment across steps that makes the objective non-myopic.

### 3.3 sPCE-myopic (control): only credit assignment differs

Everything is identical to §3.2: network, budget input, contrastive set, L, the rewards r_t, PPO settings, hyperparameter search and episode budget. The only change is the advantage:

  **A_t^my = r_t − V_ω^my(h_{t−1}, T−t+1)**, with the critic regressing r_t (γ = 0).

Equivalently, at the current parameters φ̄, the myopic update ascends

  **J_my(φ; φ̄) = Σ_{t=1}^{T} E_{h_{t−1} ∼ d_t^{π_φ̄}} [ stop-grad ] · E_{a_t ∼ π_φ(·|h_{t−1})} [ r_t ]**,

that is, each decision is trained to maximize its own immediate increment, with no gradient through how it changes later histories. As L → ∞, its fixed point is a learned greedy-EIG policy.

**Why this answers the skeptic.**
- (i) The control is not "the sum of increments with credit flowing back" (which would equal J_tot by the MI chain rule). It is γ = 0, so the chain-rule identity cannot make Δ ≈ 0 by construction.
- (ii) Both methods use the **same estimator r_t with the same L**, so neither has a different bound to be loose about. Each policy's reported sPCE_T is the same function g_T. The true EIG of both trained policies is still measured independently by IG_T (§1.3).
- (iii) The remaining-budget input is present in both networks, and only the total objective gives it any incentive.

### 3.4 H3 ablation objective (normalized), and its bias

- **No-NC-objective.** Each step's training likelihood is replaced by a *conditional* likelihood q:
  - On an NC outcome, q(∅ | c = NC, s, a) = 1 for every s. Misses carry no likelihood ratio.
  - On a contact, q(y | c = contact, s, a) = p_ε(y | contact, s, a) if the ray hits s, and u(y | contact) if it misses s. Here u is the ε-uniform branch.
  - q is a normalized density over y given the hit/miss pattern c, for every s. The rewards r_t^{NC−} are built from q exactly as in §3.1, and training is otherwise identical to sPCE-total.
- **What the ablated objective converges to** (L → ∞):
  - It equals I(s; Y | C) + E_C KL(p(y | C) ‖ m_q(y | C)), where m_q(y | c) = ∫ q(y | c, s) p(s) ds.
  - By data processing, the KL term is ≤ E_C KL(p(s | C) ‖ p(s)) = I(s; C).
  - So **I(s; Y | C) ≤ J_NC−(∞) ≤ I(s; Y, C)**. The ablation *under-weights* the information in the hit/miss pattern without removing it entirely.
  - The ablation therefore makes the Full-vs-ablation gap **conservative** with respect to "valuing misses". The opposite risk, that the ablated gradient hurts *contact* probes too and so inflates the gap, is checked directly by H3 prediction P3.
- **No-NC-input.** NC entries are removed from the DeepSets sum, so the policy cannot see misses. The objective is the full one.

---

## 4. Final hypotheses

Every hypothesis states **one decision rule: confirmed iff all listed conditions hold; otherwise rejected.** The failure condition is the exact complement. For interpretation, the report also says which condition failed and, where relevant, whether a TOST shows equivalence ("evidence of no effect") or the result is merely inconclusive. That label does not change the decision.

Common thresholds:
- **SESOI** (smallest effect size of interest) for superiority on success = **3 pp**.
- **Non-inferiority (NI) margin** on success = **4 pp**. On IG_T it is **5 % of the comparator's mean IG_T**.
- **Equivalence (TOST) margin** = **±3 pp** on success and **±0.05 nats** on IG_T.

### H1a: The sPCE-total policy is non-inferior to full-size greedy PF-EIG and better than random/coverage

**Rationale.** Information-driven touch selection (hebert2013next, javdani2012efficient, gordon2026active) optimizes EIG online. Policy-based BED (foster2021deep, blau2022optimizing) amortizes the same optimization, but it has not been applied to touch. If the sPCE bound is a good training signal, the policy should reach greedy-EIG touch quality. Non-myopia (H2) may even let it exceed greedy on S.

**Precondition** (checked in the pilot and again in the main run): full greedy beats random by ≥ 10 pp in success at T ∈ {3, 5} on both sets. If the pilot fails this, σ_p and σ_n are scaled down by a factor of 2 before main runs (pre-registered). If the main run fails it, H1a is rejected as uninformative.

**Measurable prediction (confirmed iff all hold):**
1. **Non-inferiority** in all 8 geometric cells (set ∈ {A, S} × T ∈ {3, 5, 8, 10}). The one-sided 95 % upper bound of [greedy − sPCE-total] must be < 4 pp on success (success-testable cells) and < 5 % of greedy's IG_T on IG_T (all cells). Because every cell must pass, this is an intersection–union test and needs no multiplicity correction.
2. **Superiority over random and coverage** at T ∈ {3, 5} on both sets (8 contrasts). The Holm-adjusted one-sided lower bound must be > 0 and the point estimate ≥ 3 pp on success, the lower bound on IG_T must be > 0, and seed replication must be ≥ 8/10.

**Failure condition.** The upper bound of [greedy − sPCE-total] is ≥ 4 pp (or ≥ 5 % of IG_T) in **any** cell, or any of the 8 superiority contrasts misses its threshold. An underpowered study therefore fails, not passes.

**Design sketch.** Datasets: sets A and S, test set of 2,000 episodes per cell. Baselines: greedy (N = 2,000, C = 64, M = 64), coverage and random. Metrics: success, IG_T, translation and rotation error, identity accuracy. Secondary (reported, not part of the decision): RL-PFIG vs sPCE-total on S under TOST ±3 pp, with learning curves.

### H1b: The latency advantage holds at matched accuracy, not only at a fixed greedy configuration

**Rationale.** The skeptic noted that a ≥ 100× ratio against N = 2,000 × C = 64 × M = 64 is guaranteed by construction. The non-trivial claim compares the policy with the **cheapest greedy configuration that keeps full-size accuracy**.

**Measurable prediction (confirmed iff all hold).**
- **Setup.**
  - Greedy is swept over N ∈ {500, 2,000, 8,000} × C ∈ {16, 64, 256} × M ∈ {16, 64} (18 configurations), on A and S at T = 5, using the first 1,000 test episodes.
  - Selecting the configuration on test data favours greedy, which is conservative for us.
  - The **matched configuration** is the one with the lowest median latency among those whose success is ≥ full-size success − 3 pp and whose IG_T is ≥ 95 % of full-size IG_T.
  - Latency is the median of 200 timed decisions after 20 warm-up decisions, on one core with batch size 1 and threads = 1.
  - Greedy latency includes its PF update plus candidate scoring. Policy latency includes history encoding and the head. Both are the full per-decision selection cost.
- **Prediction:** on **both** sets, the matched greedy configuration's median latency is ≥ **100×** sPCE-total's median latency.

**Failure condition.** The ratio is < 100× on either set.

**Reported measurements** (not part of the decision):
- Full-size ratio (expected > 10³).
- **Break-even episode count:** training CPU-seconds, with and without the hyperparameter-search share, divided by the per-episode decision time saved at T = 5 against the matched configuration. Expected ≤ 10⁶ episodes.
- The former H5 sweep: greedy latency vs N·C·M with a log–log fit, and policy latency vs K ∈ {4, 8, 16} and T ≤ 10.

### H1c: The information objective beats a sparse task reward at equal training budget

**Rationale.** Learned tactile exploration (riou2024reinforcement, xu2023tandem3d) relies on task or hand-designed rewards. Total-EIG training gives a dense, posterior-grounded signal at every step. The comparison is against **sparse success reward only**. The dense PF-entropy variant is the same objective under a different estimator (see RL-PFIG).

**Measurable prediction (confirmed iff all hold).** sPCE-total beats RL-success (same architecture, PPO, γ = 1, E_train = 4·10⁵ episodes, equal 12-configuration search, both plateau-checked):
- On **success**: Holm-adjusted one-sided lower bound > 0 and point estimate ≥ 3 pp in **≥ 3 of the 4 primary cells** {A, S} × T ∈ {3, 5}, with no primary cell having a negative point estimate.
- On **IG_T**: the lower bound is > 0 in the same cells.
- Seed replication is ≥ 4/5 in those cells.

**Failure condition.** Fewer than 3 of 4 primary cells pass on success, or any primary cell has a negative point estimate, or the IG_T condition fails, or seed replication fails.

**Design sketch, with mechanism diagnostics** (reported, addressing the skeptic's three explanations: objective, gradient variance, tuning):
- Learning curves (validation success and IG_T against episodes and against CPU-hours) for both methods.
- The trace of the gradient-estimate covariance at the 50 % checkpoint, from 20 independent batches.
- The full hyperparameter-search tables for both methods.
- T ∈ {8, 10} cells are reported as secondary.

### H2a: The non-myopic advantage appears on ambiguous sets at small budgets (outcome)

**Rationale.** Under adaptive submodularity, greedy pruning is near-optimal (javdani2012efficient). When hypotheses cannot be separated in one step, myopic value of information can be arbitrarily poor (chen2015submodular). Set S is built so that G(S) ≥ 0.10 and G(A) ≤ 0.03 (§1.2). That makes "one-step separability fails" an explicit, measured property of S rather than general difficulty.

**Measurable prediction (confirmed iff all hold).** Let Δ(set, T) = sPCE-total − sPCE-myopic (10 seeds each, paired test episodes).
1. **Advantage on S.** On S at T = 3 **and** at T = 5: the one-sided lower bound of Δ_success is > 0 with point estimate ≥ 3 pp (where success-testable), and the lower bound of Δ_IG is > 0. Intersection–union, so no correction.
2. **Interaction with ambiguity.** At T = 3 **and** at T = 5, the difference-in-differences Δ(S) − Δ(A), crossed-bootstrapped, has lower bound > 0 with point estimate ≥ 3 pp on success. On IG_T, the lower bound must be > 0 after normalizing each Δ_IG by sPCE-total's IG_T in that set and T, so that the two sets are on a common scale.
3. **Seed replication.** On S, at T ∈ {3, 5}, ≥ 8 of 10 sPCE-total seeds beat the seed-averaged myopic policy.

**Failure condition.** Any condition fails. In particular, Δ = 2 pp with p < 0.05 is a rejection, because it is below the SESOI. If Δ(A) is untestable on success because of saturation, the interaction is decided on normalized IG_T alone.

**Secondary (reported, threshold stated, not part of the decision).** On S at T ∈ {3, 5}, sPCE-total − greedy has one-sided lower bound > 0 on IG_T. This is the proposer's "greedy shows the same deficit" claim, now with a test.

**Design sketch.** Sets A and S, all 4 budgets, 10 seeds per objective. The validity checks are the G manipulation check (§1.2), the plateau check and the saturation rule.

### H2b: The advantage comes from set-up moves (mechanism)

**Rationale.** Without a mechanism check, a positive Δ could also come from a worse first move that happens to work out, or from under-training of the control. The skeptic's distinguishing measurement is oracle two-step EIG on *identical* belief states, together with a constructed problem where the optimal plan is known.

**Measurable prediction (confirmed iff both hold).**

**P1. Oracle analysis on S.**
- Take 300 belief states: 100 each at t = 0, 1 and 2, reached by running the myopic policy on test episodes.
- Query both policies' next action on the *same* belief and history.
- Estimate EIG₁ and EIG₂ (the chosen action followed by the oracle-greedy second action) with nested MC: N = 2,000, C₂ = 64, M = 64 outer and 32 inner outcome samples. Paired bootstrap over beliefs.
- Prediction: mean[EIG₂(a_tot) − EIG₂(a_my)] ≥ **0.05 nats** with lower bound > 0, **and** mean[EIG₁(a_my) − EIG₁(a_tot)] has lower bound > 0. In words, the total policy trades immediate information for two-step information.
- For reference, 0.05 nats is about 2.4 % of the identity entropy log 8 = 2.08 nats. It is also reported relative to the mean per-touch IG.

**P2. Analytic positive control** (identity is the target, x is a nuisance parameter).
- Shapes: P₁ is an 80 × 30 mm rectangle. P₂ is the same rectangle with a 6 mm wide, 4 mm deep notch in the top edge, centred 20 mm from the left end.
- Known parameters: θ = 0, y = 0. Unknown: x ~ U[−20, 20] mm. Target: k ∈ {P₁, P₂}.
- Likelihoods are marginalized exactly over x on a 401-point grid, so the sPCE uses p(h | k).
- T = 2. Actions are vertical probes at u ∈ [−70, 70] or horizontal probes from the left at v ∈ [−15, 15].
- Analytically:
  - Any horizontal first probe has identity EIG exactly 0, but it localizes x (σ_p = 1 mm).
  - The best vertical probe has immediate EIG ≈ 0.15·ln 2 ≈ 0.10 nats.
  - The optimal plan (horizontal probe, then a vertical probe at x̂ − 20) reaches ≈ ln 2 ≈ 0.69 nats.
  - Greedy reaches ≈ 0.2 nats.
- The exact optimum and the exact greedy value are computed on the grid.
- Prediction (10 seeds each):
  - sPCE-total reaches exact two-step identity EIG ≥ **80 % of the optimum**, with a horizontal first probe in ≥ 80 % of episodes.
  - sPCE-myopic reaches ≤ exact greedy value + 0.05 nats.
  - Both are decided on the seed mean, with ≥ 8/10 seeds individually satisfying the condition.

**Failure condition.** P1 or P2 fails. If H2a holds and H2b fails, the paper reports "a non-myopic training advantage, mechanism unexplained" and does **not** claim set-up moves.

**Design sketch.** The positive control is training at T = 2 (about 1 CPU-h in total). The oracle analysis is about 0.7 CPU-h.

### H2c (secondary): The advantage shrinks as the budget grows

**Rationale.** With enough touches, both policies eventually resolve identity and symmetry modes, so the myopic penalty, which concerns discrete disambiguation, should fade. The skeptic's ceiling confound is handled by the saturation rule and by IG_T normalization.

**Measurable prediction (confirmed iff all hold).** On S:
- (i) The OLS slope of the cell estimates Δ_success(S, T) against T ∈ {3, 5, 8, 10} has crossed-bootstrap one-sided upper bound < 0. Only success-testable cells are used. If fewer than 3 cells remain, (i) is dropped and (ii) decides alone.
- (ii) The slope of the relative IG deficit, Δ_IG(S, T) / IG_T(sPCE-total; S, T), has upper bound < 0. All 4 budgets are used, so the trend is tested as monotone and not only at its endpoints.

**Failure condition.** Either slope has upper bound ≥ 0. Also reported is a TOST on Δ_success(S, 10) with ±3 pp. Equivalence is **not** claimed from a non-significant difference.

### H3: Planning for no-contact outcomes, not only filtering them, improves touch selection on multimodal beliefs

**Rationale.** NC evidence is already used inside beliefs (koval2015pose, zheng2026bayesian), so the open question is at the policy level. On multimodal identity × pose beliefs, a probe through space that some hypotheses occupy and others leave free is informative whatever the outcome. The pilot must show R_NC(S) ≥ 0.20 and R_NC(S) > R_NC(A) (§1.2). Without that, there is no a-priori reason for miss-planning to dominate, and H3 is reported as untestable.

**Measurable prediction (confirmed iff all hold).** Full is the main sPCE-total model (10 seeds). The ablations No-NC-objective (§3.4) and No-NC-input have 5 seeds each. All are scored by the full evaluation PF (§1.4).
1. **Both ablations hurt.** On S at T = 3 and T = 5, for **each** ablation: lower bound of [Full − ablation] > 0 with point estimate ≥ 3 pp on success, lower bound > 0 on IG_T, and seed replication ≥ 4/5. Intersection–union over 2 ablations × 2 cells.
2. **Misses are planned, not incidental.**
   - Fix one sample of test probes on S at T ≤ 5, and evaluate each probe under the evaluation PF's pre-touch belief.
   - (a) The mean **NC-branch share of pre-touch EIG** is P_NC·E[log-ratio | NC] / EIG. It must exceed No-NC-objective's by ≥ **0.10** (absolute), with lower bound > 0.
   - (b) The fraction of Full's probes with predicted P(NC) ∈ [0.2, 0.8] must exceed No-NC-objective's by ≥ **10 pp**, with lower bound > 0. It must also exceed random's fraction on S. This normalization removes the "S shapes just cause more misses" confound.
   - (c) The realized IG of Full's NC probes, averaged per probe, must exceed the realized IG of *random*'s NC probes by a lower bound > 0. Both are also reported next to Full's contact-probe IG for scale.
3. **Not just a biased objective.** Among probes that ended in **contact**, the per-touch pre-touch EIG under the full model is equivalent between Full and No-NC-objective (TOST ±0.03 nats). Equivalently, the ablation did not degrade contact-probe selection.

**Failure condition.** Any condition fails. The outcome is labelled for the report:
- Only No-NC-input matters: "history conditioning, not miss planning".
- P1 holds but P3 fails: "objective-calibration effect, not miss planning".
- On A, effects are reported for scale and expected to be smaller (not part of the decision).

**Design sketch.** Sets S (primary) and A (reference). The ablations are the two trainings in §3.4, 5 seeds × 2 sets each. The probe-level analyses re-use the evaluation PF and nested MC with N = 2,000, M = 64.

### H4: Geometric-model policies keep their advantage under a measured, non-trivial MuJoCo contact shift

**Rationale.** Policy-based BED has not been tested under simulator mismatch. The skeptic pointed out that with a tiny rigid fingertip the test is trivial. The shift is therefore pre-registered, measured, and swept.

**Pre-registered MuJoCo setup.**
- Static object: extruded polygon, 20 mm tall, fixed to the world. The fingertip is a sphere of radius **r ∈ {1, 4, 8} mm** (primary level **r = 4 mm**), moved kinematically along the probe line at 50 mm/s.
- Timestep 1 ms, default solref/solimp, and the guard fires at the first contact with penetration > 0.1 mm.
- Reported observation: MuJoCo's contact position and contact normal, projected to the plane. A miss is no contact within the stroke.
- **Shift measurement** (first 200 scenes, random probes): the distribution of contact-point error and normal error against the ray-cast prediction, and the rate of hit/miss disagreement.
- **Non-triviality requirement at the primary level:** median point error ≥ 2σ_p (2 mm) **or** hit/miss disagreement ≥ 5 %. If neither holds at r = 4 mm, the primary level moves to r = 8 mm. This choice is made before any policy is evaluated in MuJoCo.
- No fine-tuning. The evaluation PF keeps the geometric likelihood, so all methods face the same mismatch.

**Measurable prediction (confirmed iff all hold, at the primary radius, sets A and S, T ∈ {3, 5, 10}, the first 1,000 test scenes):**
1. **Sign preservation.**
   - A method pair is **pre-separated** if its geometric-fidelity success difference has a Holm-adjusted lower bound > 0 and point estimate ≥ 3 pp. Pairs are taken over sPCE-total, greedy, RL-success, coverage and random.
   - Every pre-separated pair has a MuJoCo point estimate of the same sign.
   - The key pairs **sPCE-total > random** and **sPCE-total > coverage** at T ∈ {3, 5} must also have MuJoCo lower bound > 0 with point estimate ≥ **10 pp**. This guards against all methods collapsing toward the PF floor together.
2. **Absolute transfer gap.** For sPCE-total, success(geometric) − success(MuJoCo), paired over the same scenes, has one-sided upper bound ≤ **10 pp** in each cell.
3. **Relative brittleness.** [gap(sPCE-total) − gap(greedy)] has one-sided upper bound ≤ **5 pp** in each cell.

**Failure condition.** Any pre-separated pair reverses sign, a key pair falls below its threshold, any sPCE-total gap upper bound exceeds 10 pp, or any relative-gap upper bound exceeds 5 pp. The paper then reports the measured shift distributions as a diagnosis.

**Exploratory (no decision).** The gaps at r = 1 and r = 8 mm. The predicted outcome is that the gap grows with r and that sign preservation first breaks at r = 8 mm for the closest pre-separated pair.

**Power.** With 1,000 scenes paired across fidelities and methods, the pilot projects SE(gap difference). If it exceeds 2 pp, the primary radius uses 2,000 scenes. This is pre-registered.

### H5′ (secondary, replaces H5): The accuracy cost of amortization grows slowly with library size

**Rationale.** H5 as proposed (latency scaling) is true by construction. The open question is whether a fixed-capacity policy, under a fixed training budget, loses accuracy relative to greedy as K grows.

**Measurable prediction.**
- Design: nested asymmetric pools A4 ⊂ A8 ⊂ A16, T = 5, 1,000 test episodes per pool.
- Fixed network size and E_train. Greedy uses N = 250·K particles (constant per identity), C = 64 and M = 64.
- Let D(K) = success(greedy) − success(sPCE-total) and β = [D(16) − D(4)] / 2, the change per doubling of K.
- **Confirmed iff the crossed-bootstrap one-sided upper bound of β is ≤ 3 pp per doubling**, and the analogous relative IG_T deficit grows by ≤ 5 % per doubling (upper bound).

**Failure condition.** Either upper bound exceeds its threshold. The paper then states that amortization degrades with library size at this capacity.

**Design sketch.** A4 and A16 trainings with 5 seeds each (A8 re-uses the main runs), plus greedy evaluation at K = 4 and K = 16.

---

## 5. Design ablations required by SC3 (reported rows, not hypotheses)

| Component | Variants | Where | Seeds | Expected (stated, not tested for a decision) |
|---|---|---|---|---|
| Non-myopic objective | sPCE-myopic | all cells | 10 | H2a |
| No-contact use | No-NC-objective, No-NC-input | A, S | 5 | H3 |
| History encoder | DeepSets (main) vs padded-concatenation MLP vs GRU | S | 3 | DeepSets ≥ others at T = 10 (order invariance) |
| Contrastive samples L | 15, 63, **255** (main), 1023 | S | 3 | IG_T increases with L and saturates by 255 (Δ(255 → 1023) < 0.05 nats) |

---

## 6. Pre-registered analysis plan

1. **Freeze before main runs:**
   - object sets and their G, C and R_NC values;
   - σ_p, σ_n and ε;
   - N_eval (after the convergence check);
   - success-testable cells per contrast (pilot saturation rule);
   - test-set sizes (power rule);
   - the MuJoCo primary radius (shift check);
   - hyperparameters (search on validation).

   All of these go into `docs/` with a commit hash before the main runs start.
2. **Primary metrics.** Success (co-primary on success-testable cells) and IG_T (co-primary in all cells). Every directional claim requires both, where applicable. Secondary metrics: translation error, rotation error, identity accuracy, per-decision latency and training CPU-hours.
3. **Unit and test.** A paired comparison over the shared test episodes, with seed-averaged per-episode outcomes. CIs come from a crossed bootstrap (episodes shared across methods × seeds per learned method, B = 10,000), with one-sided 95 % bounds. Seed-level replication (≥ 8/10 or ≥ 4/5 seeds in the predicted direction) is required for superiority claims.
4. **Primary cells per hypothesis.**

   | Hypothesis | Primary cells / contrasts | Combination rule | Correction |
   |---|---|---|---|
   | H1a-NI | 8 cells, sPCE-total vs greedy | all must pass | none (intersection–union) |
   | H1a-sup | 8 contrasts (2 baselines × 2 sets × T ∈ {3, 5}) | all must pass | Holm across the 8 |
   | H1b | 2 sets, T = 5 | both must pass | none (latency is a deterministic measurement, reported with bootstrap CI over decisions) |
   | H1c | 4 cells ({A, S} × T ∈ {3, 5}) | ≥ 3 of 4 | Holm across the 4 |
   | H2a | (S,3), (S,5); interaction at T = 3 and T = 5 | all must pass | none (intersection–union) |
   | H2b | oracle P1 (S), positive control P2 | both must pass | none |
   | H2c | slope over T on S | single test | none |
   | H3 | 2 ablations × (S,3), (S,5); P2(a–c); P3 | all must pass | none (intersection–union) |
   | H4 | pre-separated pairs, key pairs, gaps at primary r | all must pass | Holm for *defining* pre-separated pairs (geometric stage) |
   | H5′ | β and relative IG slope | both must pass | none |

   General rule: no correction when every test in a family must pass (an intersection–union test is level-α). Holm when the decision accepts "any" or "at least k". Hypotheses are separate claims, so there is no correction across them, and each is reported with its own decision.
5. **Margins.** NI 4 pp on success and 5 % of the comparator's mean IG_T. SESOI 3 pp (superiority). TOST ±3 pp on success and ±0.05 nats on IG_T (±0.03 nats per touch for H3-P3). Mechanism thresholds: 0.05 nats (H2b-P1), 0.10 share and 10 pp (H3-P2), 80 % of the optimum (H2b-P2). Transfer: 10 pp absolute, 5 pp relative, 10 pp key-pair floor (H4). Scaling: 3 pp per doubling (H5′). Latency: 100× at matched accuracy (H1b).
6. **Null and partial results.** All are reported under the labels defined in each hypothesis (SC2). No post-hoc cell selection. Exploratory analyses are labelled as such.

---

## 7. Compute estimate (CPU-hours; every figure is re-checked by a TIME_ESTIMATE pilot before its sweep)

Assumptions: a vectorized ray cast costs about 1 µs per (state × step) including the likelihood. One training run (E_train = 4·10⁵ episodes, mean T = 6.5, L = 255, batch 256) is about **0.35 CPU-h**. The evaluation PF averages about 5 ms per step with resample-move. Greedy at full size is about 0.1 s per decision.

| Item | Runs / volume | CPU-h |
|---|---|---|
| Pilot (TIME_ESTIMATE, saturation, power, N_eval convergence, G / C / R_NC checks) | — | ≈ 4 |
| Hyperparameter search (4 learned methods × 12 configs × 10⁵ episodes) | 48 short runs | ≈ 4.5 |
| sPCE-total + sPCE-myopic (2 sets × 10 seeds × 2) | 40 | ≈ 14 |
| RL-success (2 × 5); RL-PFIG (S × 5) | 15 | ≈ 6 |
| H3 ablations (2 variants × 2 sets × 5) | 20 | ≈ 7 |
| Design ablations (encoder 2 × 3; L ∈ {15, 63} × 3; L = 1023 × 3 at about 4× cost) | 15 | ≈ 7 |
| H5′ (A4, A16 × 5 seeds) + positive control (2 × 10 seeds, T = 2) | 30 | ≈ 5.5 |
| Geometric evaluation (≈ 45 policy evaluations per set × 2,000 episodes × ΣT = 26, at 5 ms per step) | — | ≈ 6 |
| Greedy full-size evaluation (2 sets × 2,000 × 26 decisions × 0.1 s) + H1b Pareto sweep (18 configs × 2 sets × 1,000 × 5) | — | ≈ 6 |
| MuJoCo (3 radii × 2 sets × 3 budgets × 1,000 scenes; greedy dominates) | — | ≈ 9 |
| Oracle two-step analysis (H2b-P1) + probe-level NC analysis (H3-P2/P3) + latency benchmarks | — | ≈ 2 |
| **Total** | | **≈ 71 CPU-h** |

How this fits the hardware:
- Every training run fits in 7 GB of RAM (10k particles; contrastive batches of 256 × 256).
- Jobs are split into ≤ 5 h shards with `time_guard`, below the GitHub Actions 6 h job limit. With about 10 concurrent 2-vCPU runners, wall-clock time is about 4–6 h.
- If the pilot shows costs above 1.5× these estimates, the pre-registered reductions are, in this order: (1) design ablations drop to S × 2 seeds; (2) MuJoCo r = 1 mm is dropped; (3) RL-PFIG is dropped. Primary hypotheses keep their seeds and episode counts.

---

## 8. Critique → resolution map

| Skeptic point | Resolution (section) |
|---|---|
| X1: Wilcoxon over 5 seeds cannot reach p < 0.05; pseudoreplication | The unit is the paired test episode, with seed-averaged outcomes and a crossed episode × seed bootstrap. Seeds are a secondary replication factor (≥ 8/10 or ≥ 4/5) (§1.5). |
| X1: 3 pp NI margin underpowered | Margin 4 pp. 2,000 episodes per cell. Precision projected from the pilot (SE ≈ 1.0–1.5 pp). Pre-registered escalation to 4,000 episodes or a 5 pp margin (§1.5). |
| X1: multiplicity | Per-hypothesis families: intersection–union (no correction) or Holm for "≥ k" rules (§6). |
| X2: scale, prior and noise unstated; floor/ceiling | R = 40 mm, prior box, σ_p, σ_n and ε stated (§1.1). Cells checked for [10 %, 90 %]. IG_T is co-primary (§1.3). |
| X3: evaluation PF unspecified | N_eval = 10,000 with resample-move, plus a convergence check against 4·N_eval and a bandwidth sensitivity check (§1.4). |
| X4: prediction and failure not complements | One rule per hypothesis, "confirmed iff all hold" (§4 preamble). |
| H1: bundled claims | Split into H1a, H1b, H1c. |
| H1: greedy M, candidates, vectorization | M = 64, Sobol candidates re-drawn each step, ray-cast once per particle and candidate, single thread (§2). |
| H1: ambiguous RL baseline | RL-success is the H1c comparator. RL-PFIG is labelled an estimator comparison (§2). |
| H1: training-budget unit | Environment episodes. Likelihood evaluations and CPU-h reported separately (§2). |
| H1: failure rule in the wrong direction; ≥ 2/8 tolerance | The upper bound must be < margin in all 8 cells. An underpowered study fails (H1a). |
| H1: greedy-vs-random precondition | Greedy must beat random by ≥ 10 pp at T ≤ 5, with a pre-registered noise adjustment (H1a). |
| H1: aggregate test for (c) undefined | Holm, 4 cells, ≥ 3 of 4, SESOI 3 pp (H1c). |
| H1: latency trivially true; amortization cost | Matched-accuracy Pareto comparison is primary. The break-even episode count is reported (H1b). |
| H1: why sPCE might beat RL | Learning curves, gradient variance, equal search, plateau rule (H1c, §2). |
| H2: the 1-step control may equal the total objective | γ = 0 control with identical rewards and estimator; loss written out (§3.3). |
| H2: bound-tightness confound | Same r_t and L for both. True EIG measured by IG_T (§3.3, §1.3). |
| H2: S qualitative | Myopia gap G(S) ≥ 0.10 vs G(A) ≤ 0.03, plus confusability C (§1.2). |
| H2: monotone shrinkage tested only at endpoints | Slope over all 4 budgets (H2c). |
| H2: "greedy same sign" untested | Secondary test, lower bound > 0 on IG_T (H2a). |
| H2: entropy-after-touch-1 confounded | Oracle EIG₁ / EIG₂ comparison on identical beliefs (H2b-P1). |
| H2: "not significant" taken as zero; ceiling | Slope test on testable cells and IG_T. TOST reported, never inferred from a non-significant result (H2c). |
| H2: interaction test unstated | Difference-in-differences with crossed bootstrap, ≥ 3 pp, plus normalized IG_T (H2a). |
| H2: the 2 pp significant Δ gap in the rule | SESOI is part of the confirm rule, so such a result is a rejection (H2a). |
| H2: competing mechanisms; positive control | Oracle analysis, plateau and equal search, saturation rule, analytic notch positive control (H2b). |
| H3: unnormalized ablation likelihood | Normalized conditional likelihood, with its limit sandwiched between I(s; Y \| C) and I(s; Y, C) (§3.4). |
| H3: a-priori direction | Precondition R_NC(S) ≥ 0.20 and R_NC(S) > R_NC(A) (H3). |
| H3: NC fraction confounded by geometry | Normalized against random on the same set (H3-P2b). |
| H3: 0.1 nats without a reference | Compared with random's NC probes and Full's contact probes (H3-P2c). |
| H3: one ablation enough; effect size dropped | Both ablations required, with SESOI, in the confirm rule (H3-P1). |
| H3: indistinguishable-IG margin | TOST ±0.03 nats on contact probes (H3-P3). |
| H3: objective-bias mechanism | Contact-only probe equivalence check (H3-P3). |
| H4: uncontrolled shift | Pre-registered MuJoCo parameters, measured shift, non-triviality requirement, radius sweep (H4). |
| H4: τ ≥ 0.8 dominated by ties | Sign preservation over pre-separated pairs only (H4-P1). |
| H4: unclear separability rule | Holm-adjusted lower bound > 0 and ≥ 3 pp, replacing non-overlapping CIs (H4-P1). |
| H4: 10 pp dropped; 200 scenes underpowered | 10 pp restored as an upper-bound rule. 1,000 scenes, escalating to 2,000 by the power rule (H4). |
| H4: collapse toward the PF floor | Key pairs need ≥ 10 pp over random and coverage in MuJoCo (H4-P1). |
| H5: true by construction | Rejected. Latency kept as a measurement (H1b). Replaced by the K-scaling accuracy hypothesis H5′. |
