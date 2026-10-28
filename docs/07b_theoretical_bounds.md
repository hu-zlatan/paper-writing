# Stage 8.5 · THEORETICAL_BOUNDS (v1) — preliminary analysis

> Prompt: `pipeline/references/stage_prompts/theoretical_bounds.md` (system: "You are a theoretical computer scientist with a strong applied math background. You produce concise, honest preliminary analysis — never fabricate proofs or guarantees. When the analysis is informal, mark it clearly as such."), `{hypotheses}` = `docs/07_hypotheses.md`, `{method_sketch}` = §2–3 of that file. Session model, 2026-10-28.
> Citations marked (to verify) are not yet in the verified shortlist and must be verified before use in the paper.

## 1. Setup & notation

| Symbol | Meaning |
|---|---|
| s = (k, x, y, θ) | object identity k ∈ {1..K} and planar pose |
| V | max number of polygon vertices (edges) per shape (≤ 14 for set A; ≤ ~40 for rounded/notched shapes in S) |
| a = (φ, ψ), y | probe action; observation (contact point + normal, or ∅) |
| T | touch budget (3–10) |
| N | particles of an online particle filter (greedy PF-EIG: 2,000 full size; evaluation PF: 10,000) |
| C, M | candidate actions per greedy decision; outcome samples per candidate |
| L | contrastive prior samples in the sPCE bound (L = 255 in the current plan) |
| d, P | hidden width (128) and parameter count (≈ 5·10⁴) of the policy network |
| E | training episodes per run (4·10⁵) |
| h_t | history {(a_τ, y_τ)}_{τ ≤ t} |

The probe likelihood p_ε(y | s, a) requires one ray–polygon intersection, O(V) time (test each edge, keep the nearest hit).

## 2. Time complexity

**Greedy PF-EIG, per decision.**
- Belief update with the latest observation: O(N·V).
- Candidate scoring: one ray cast per (particle, candidate) gives the predicted outcome geometry, O(N·C·V); then for each of the C·M sampled outcomes the likelihood under all N particles is a closed-form Gaussian/indicator lookup on the cached geometry, O(N·C·M).
- Total: **O(N·C·(V + M))** per decision, plus resample-move when ESS drops: O(R·N·t·V) for R MH steps against the full history at step t.
- Full size (N=2000, C=64, M=64, V≈14): ≈ 1.6·10⁶ ray-edge tests + 8.2·10⁶ Gaussian terms per decision.

**Amortized policy (sPCE-total), per decision.**
- DeepSets encoder maintained incrementally: add ψ(a_t, y_t) to a running sum, O(d²); head ρ + output, O(d²). Total **O(d²) = O(P)** per decision, independent of N, C, M, V and K. (Without incremental caching, O(t·d²) ≤ O(T·d²).)
- Ratio to greedy: O(N·C·(V+M)) / O(d²). With the numbers above, ≈ 10⁷ vs ≈ 3·10⁴ multiply-adds → a ≥ 100× gap is plausible *before* constant factors (numpy vs PyTorch overheads at batch size 1 can dominate the policy's real latency; H1b measures it).
- Note: a deployed system still needs a belief/estimator for the *final estimate*; that cost (O(N·V) per touch for a PF) is shared by all methods and excluded from selection latency in H1b, but must be reported separately so the end-to-end comparison is honest.

**Training (offline).**
- Per episode: likelihood of every action under s₀ and L contrastive states, O(T·(L+1)·V), plus T forward/backward passes O(T·d²).
- Per run: **O(E·T·(L+1)·V + E·T·d²)**. With E = 4·10⁵, T̄ = 6.5, L = 255, V ≈ 14: ≈ 9·10⁹ ray-edge tests — feasible on CPU only with vectorized numpy (batched over episodes × contrastive states × edges); the stage-11 pilot must confirm.
- Amortization break-even: training cost / (greedy cost − policy cost) per decision gives the number of deployed decisions after which training pays off (reported by H1b, not a hypothesis).

## 3. Space complexity

- Greedy PF-EIG: O(N·C) cached geometry + O(N·C·M) temporaries (can be chunked to O(N·C) by looping over M) + O(N) particles.
- Policy at deployment: O(P) parameters + O(d) running sum. Independent of history length.
- Training: O(B·T·(L+1)) likelihood tables per batch of B episodes (B = 256, L = 255 → ≈ 6.7·10⁵ floats per T-step slice) + O(P) network/optimizer state.
- Evaluation PF: O(N_eval) particles + O(N_eval·T) cached per-history likelihoods if resample-move reuses them.

## 4. Convergence / bound statements

**4.1 sPCE is a valid but saturating lower bound (known result).** For any policy π and L ≥ 1, sPCE_T(π; L) ≤ EIG_T(π), sPCE is non-decreasing in L, and sPCE_T(π; L) → EIG_T(π) as L → ∞ (Foster et al. 2021, foster2021deep). Moreover sPCE_T(π; L) ≤ log(L+1) for every policy, because the true state is one of the L+1 terms in the denominator.

**Consequence for this project (important, found at this stage).** With L = 255 the bound saturates at log 256 ≈ 5.55 nats. The information needed for the success criterion is roughly
  log K + log( prior translation area / success disc area ) + log( 2π / (2·5°) )
  ≈ log 8 + log( 30·30 / (π·5²) ) + log 36 ≈ 2.08 + 2.44 + 3.58 ≈ **8.1 nats** (informal; ignores symmetry groups, which reduce it for symmetric shapes).
So once a policy's histories carry more than ≈ 5.5 nats about s₀, the reward increments vanish (g_t is capped), and the training signal stops distinguishing policies that differ only in late-stage refinement. This would (a) bias the comparison toward early, coarse information, (b) weaken H1a at large T, and (c) confound H2 (both objectives flatten). **Recommendation for stage 9:** choose L with log(L+1) comfortably above the target information (e.g. L = 4095 → 8.3 nats, L = 16383 → 9.7 nats) and verify in the pilot that the fraction of training episodes with g_T > log(L+1) − 0.5 is small; keep the L-ablation (A4) to show the effect. Training cost scales linearly in L (§2), so L = 4095 is 16× the current estimate unless batched more cleverly — the stage-11 pilot decides. An alternative that avoids the cap is a proposal-based contrastive set (importance-weighted PCE, cf. rainforth2024modern); it is unbiased only with correct importance weights and is a fallback, not the default.

**4.2 Policy-gradient convergence.** Informal argument; full proof deferred to future work. The score-function gradient with full returns-to-go (γ = 1, finite horizon T ≤ 10) is an unbiased estimator of ∇J_tot for the *bound* with fixed L; PPO-clip with a learned critic converges only to a local stationary point under standard smoothness assumptions, with no global optimality guarantee. Rigor is hard because the objective is non-concave in φ, the outcome distribution is discontinuous in a (hit/miss boundaries), and PPO's clipping makes the update not exactly a gradient step. We therefore claim no convergence guarantee; we use empirical plateau detection (§2 of the hypotheses file) and report seed variance.

**4.3 Myopic control's fixed point.** Informal: with γ = 0 and L → ∞, the myopic update's expected per-step objective is the one-step conditional EIG at h_{t−1}; a policy maximizing it pointwise is the greedy-EIG policy (modulo function-approximation error). Hence sPCE-myopic is a learned approximation of greedy PF-EIG, which is why H2 compares two learned policies (credit assignment is the only difference) and H1a compares the learned non-myopic policy with the exact online greedy.

**4.4 When can non-myopia help? (qualitative, with known theory).** If the objective were adaptive submodular, greedy would be within a constant factor (1 − 1/e) of the optimal adaptive policy (golovin2010adaptive, arXiv:1003.3967 — verified 2026-10-28, docs/03_supplement.jsonl). Expected reduction in Shannon entropy is in general *not* adaptive submodular for hypothesis identification with noisy tests — this is why Javdani et al. (javdani2012efficient) optimize the EC²-style surrogate for touch localization, and Chen et al. (chen2015submodular) report that myopic value-of-information is poor in some regimes. Concretely, a single touch can have low one-step EIG yet create a belief where the next touch disambiguates two modes (the "notched rectangle" positive control of H2b): the optimal two-step value exceeds greedy's. This is the regime the myopia-gap manipulation check G(O) quantifies. No bound on the size of the gap is claimed; H2b measures it.

**4.5 Evaluation PF consistency.** With the ε-softened likelihood (ε = 10⁻³) every weight is strictly positive, so importance weights are well-defined; with resample-move (MH invariant to the posterior) the PF is a consistent estimator of posterior expectations as N → ∞ (standard SMC result, chopin2002sequential, Biometrika doi:10.1093/biomet/89.3.539 — verified 2026-10-28). The finite-N error is controlled empirically by the N vs 4N convergence check (§1.4 of the hypotheses file).

## 5. Comparison with the closest baselines

| Method | Selection cost per decision | Look-ahead | Objective | Notes |
|---|---|---|---|---|
| Greedy PF-EIG (hebert2013next-style; our full-size baseline) | O(N·C·(V+M)) | 1 step | exact (MC) one-step EIG | cost grows with belief resolution and candidate count |
| Fisher-information EIG (gordon2026active) | O(C_iter · forward-sim · dim²) per CEM iteration (qualitative; not published as big-O) | 1 step | local Gaussian approximation around MLE | fails on multimodal beliefs (authors' own limitation) |
| Max–min distance heuristic (zheng2026bayesian) | O(|candidates| · contacts) on the MAP shape | 1 step | geometric coverage, no expectation over outcomes | cheap, but ignores belief multimodality |
| EC² / DiRECt (javdani2012efficient, chen2015submodular) | O(C · H²) over H discrete hypotheses (qualitative) | 1 step on a non-myopic surrogate | submodular surrogate of decision-relevant information | requires a discretized hypothesis set |
| Task-reward RL (riou2024reinforcement, niemann2024when) | O(P) | learned | hand-designed rewards | fast; no information-theoretic objective |
| **sPCE-total (ours)** | **O(P), independent of N, C, M, K** | learned, full budget | sPCE bound of total EIG (capped at log(L+1)) | training cost O(E·T·L·V) offline |

Asymptotically, the policy's decision cost is constant in the belief resolution; greedy PF-EIG's is linear in N·C·(V+M). This is the formal content behind H1b; the empirical question is the constant factor and whether accuracy is retained (H1a).

## 6. Honesty section — what could fail

1. **Bound saturation (§4.1).** If L is not increased, the training signal flattens after ≈ 5.5 nats; observed symptom: sPCE-total and sPCE-myopic converge to similar policies with similar large-T accuracy and g_T clustered near log(L+1). Mitigation planned in stage 9.
2. **Static-object and known-library assumptions.** Real touches can move objects; unknown shapes break the likelihood. All complexity statements assume a fixed library of K polygons.
3. **Constant factors dominate at small N.** If greedy is run with small N·C·M (e.g. on S where few candidates matter), its latency may be within 10–50× of the policy; H1b would then fail at matched accuracy. That outcome would invalidate the "≥ 100×" claim, not the asymptotic statement.
4. **Function-approximation error.** A 50k-parameter network may not represent the optimal non-myopic policy for multimodal beliefs over K identities; symptom: H5′ deficit growing with K.
5. **Non-convergence of PPO.** No guarantee (§4.2); symptom: high seed variance or seeds disagreeing in sign (handled by the ≥ 8/10 seed-robustness rule).
6. **Geometric vs physical contact.** The O(V) ray model ignores fingertip radius and compliance; MuJoCo contacts differ (H4 measures it). The complexity of MuJoCo evaluation is not part of any claim.
7. **Information target estimate (§4.1) is informal.** The 8.1-nat figure ignores the observation noise floor and symmetry groups; it is only used to motivate choosing L, and the pilot measurement of g_T supersedes it.
