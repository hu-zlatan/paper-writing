# Stage 8.5 · THEORETICAL_BOUNDS (v2) — preliminary analysis for docs/07_hypotheses_v2.md

> Prompt: `pipeline/references/stage_prompts/theoretical_bounds.md` (same system prompt as v1), `{hypotheses}` =
> docs/07_hypotheses_v2.md. Session model, 2026-10-28. Builds on docs/07b_theoretical_bounds.md (v1), which stays valid
> for everything not listed here. Citations marked (to verify) are pending the supplementary lookup
> (docs/03_supplement_queries.yaml); they must not enter the paper before verification.

## 1. Setup & notation (additions to v1)
- Discrete action set 𝒜 with |𝒜| = A = 256 (shared by all methods), feasibility mask per state of the finger.
- Finger angle φ_f on the stand-off circle; action a = (φ, ψ); cost c(a | φ_f) = 1 + κ·|wrap(φ − φ_f)|/π (stroke units); time
  budget τ; κ ∈ {0, 2, 6} (escalation 12).
- Target: ball information U(h) = log P(B(s₀) | h) − log P(B(s₀)) (success region B); all information-based methods
  optimise E[U].

## 2. Time complexity
- Cost-aware greedy G* per decision: score_a = EIG_B(a; b) / c(a | φ_f) for all feasible a ∈ 𝒜:
  O(N·A·(V + M)) — with N = 2,000, A = 256, M = 64, V ≈ 14: ≈ 4× the v1 cost (≈ 2.6 s per decision, scaled from the
  measured 0.65 s at A = 64). EIG_B needs, per sampled outcome, the posterior mass of the ball around the sampled state,
  computed from the same reweighted particles: O(N) extra per (outcome, action) → same order.
- Policy: O(d² + d·A) per decision (categorical head over 256 actions), independent of N, M, V.
- Rollout planner reference (depth D, width W): O(W^D · N·(V+M)) per decision — exponential in depth; only used as an
  offline reference on small cells.

## 3. Space complexity
Unchanged from v1 except the policy head (O(d·A) parameters) and greedy temporaries O(N·A) (chunked over A).

## 4. Statements

**4.1 Why travel cost can create look-ahead value (informal argument; formal treatment deferred).**
Greedy guarantees for adaptive information gathering rely on (i) adaptive submodularity of the objective and (ii)
costs that do not depend on the order of actions (modular costs); under both, the cost-benefit greedy rule is within a
logarithmic or constant factor of the optimal adaptive policy for coverage-type objectives (Golovin & Krause 2011 — to
verify). With travel, the cost of an action depends on the previous action (c(a | φ_f)), i.e. the problem becomes an
adaptive orienteering-type problem, for which ratio-greedy has no constant-factor guarantee even for modular rewards
(informative path planning literature, e.g. Hollinger & Sukhatme 2014 — to verify). Hence look-ahead *can* help
when κ is large; v1's null result at κ = 0 is consistent with near-greedy-optimality when costs are modular.
Nothing here guarantees that it *does* help in our environment — that is what gate G2 measures.

**4.2 Ball-information objective and the sPCE cap.** U(h) ≤ −log P(B) ≈ 8.1 nats (asymmetric shapes); with L = 4095,
log(L+1) = 8.32 nats ≥ −log P(B), so the training bound's cap sits just above the maximal decision-relevant information
(informal calibration argument from amendment A1; not a theorem — the sPCE target is still full-state information,
truncated). Hypotheses that compare policy and greedy use U, measured by the evaluation PF, so the comparison is on the
same target even though the training bound is a surrogate.

**4.3 Convergence.** As in v1: no guarantee for PPO (informal only); categorical head removes the tanh-squashing
issue; the plateau rule is the operational stopping criterion.

**4.4 Exact notch control (G1).** On a discretized two-shape problem (rectangle ± notch, pose on a grid), the optimal
two-step value V₂* = max_{a₁} E_{y₁}[U-gain(a₁) + max_{a₂} E U-gain(a₂ | y₁)] is computable exactly by enumeration over
the grid posterior and a finite outcome discretization; this gives the reference against which the MC estimator's bias
is measured (G1 rule: recovered gap within ±20 %).

## 5. Comparison with closest baselines
| Method | Per-decision cost | Handles travel cost | Look-ahead |
|---|---|---|---|
| Greedy PF-EIG (v1) | O(N·A·(V+M)) | no | 1 step |
| Cost-aware greedy G* (EIG/cost) | O(N·A·(V+M)) | myopically (ratio) | 1 step |
| Rollout planner | O(W^D·N·(V+M)) | yes | D steps |
| Max–min coverage (zheng2026bayesian) | O(A·contacts) | no | none |
| Ours (sPCE-total policy) | O(d² + d·A) | learned (cost in the budget/time features) | learned over the whole budget |

## 6. Honesty section
1. The travel model (finger on a stand-off circle, cost linear in angular travel) is a simplification of arm kinematics;
   conclusions about κ are about this model.
2. If G2 fails (no headroom even at κ_hi), the informal argument of 4.1 is simply not realised in this environment and
   H2 is recorded as refuted in the tested range.
3. EIG_B for greedy is estimated by nested MC on a particle belief; its estimator bias is bounded only empirically (G1).
4. The A = 256 discretization may cap achievable accuracy; the 1,024-action flatness check (G5) bounds that effect.
