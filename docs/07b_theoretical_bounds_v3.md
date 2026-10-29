# Stage 8.5 · THEORETICAL_BOUNDS v3 (fresh subagent, template verbatim)

> System: "You are a theoretical computer scientist with a strong applied math background. You produce concise, honest
> preliminary analysis — never fabricate proofs or guarantees. When the analysis is informal, mark it clearly as such."
> `{hypotheses}` = `docs/07_hypotheses_v3.md` (read in full). `{method_sketch}` = its §1.6–§1.8 and §2 plus the code as
> read on 2026-10-29: `relframe.py`, `policies_v2.py`, `ball.py`, `pf.py`, `gridpost.py`, `latency.py`, `lookahead.py`,
> `travel.py` (and, to resolve calls, `train_v2.py` `act`, `lookahead_tb.py`, `g2.py`, `geometry.cast`, `nn.py`).
> Builds on `docs/07b_theoretical_bounds_v2.md`; everything there is re-derived for 𝒜 = 64 × 8 = 512 and the 27-point grid.
> **No experiment was run.** One short Python snippet (< 1 s, scratchpad, not committed) counted elementary operations
> for the 27 configurations and the student (§2.4); its output is arithmetic, not a measurement. Measured numbers are
> quoted only from `docs/07_hypotheses_v3.md` (§0.3, §7), `results/v2/15_decision.md` (via §0.3) and `PROGRESS.md`,
> each labelled **[measured, source]**. Arithmetic on quoted numbers is labelled **[derived]**.

---

## 1. Setup & notation

| Symbol | Meaning (code reference) |
|---|---|
| s = (k, x, y, θ) | object identity k ∈ {1..K} (K = 8 for S and A) and planar pose; prior uniform, x, y ∈ [−15, 15] mm |
| G_k | rotation symmetry group of shape k (`lib.sym[k]`); \|G\| = its size |
| V | padded number of polygon edges per shape (`lib.V`); cast cost is O(V) per (state, ray). v1 doc: V ≤ 14 (A), up to ≈ 40 (S) |
| a = (φ′, ψ) ∈ 𝒜 | 64 φ′ × 8 ψ = **A = 512** actions; c(a \| φ_t) = 1 + κ·\|wrap(φ′ − φ_t)\|/π strokes; budget τ, feasible iff c ≤ τ_rem |
| y = (c, p_x, p_y, n) | contact flag, contact point, normal angle; ε-softened likelihood p_ε(y \| s, a) (`likelihood.py`) |
| h_t | history of t executed probes and outcomes; **T** = history length at a decision (≈ 3–6; S ≈ 4.2 decisions/episode, §7) |
| b_t | particle belief {(s_n, w_n)}_{n=1..N} of a PF with resample-move (`pf.py`), N ∈ {2000, 500, 125} |
| B(s₀) | success ball: same k, ‖Δ(x, y)‖ < 5 mm, folded rotation error < 5°. P(B) ≈ 3.03·10⁻⁴, −log P(B) ≈ 8.10 nats [derived, \|G\| = 1] |
| EIG_B(a; b) | one-step expected increment of log P(B(s) \| h): `ball.ball_eig`, M outcome samples per candidate |
| G\*(N, C, M) | argmax over C feasible candidates of EIG_B/c (`policies_v2.GStar`); full size (2000, 512, 64) |
| m_s | mh_steps of resample-move (= 3); triggered when ESS < N/2 |
| H, F | student hidden width (128) and per-touch feature dim (FEAT_DIM = 9); context dim 5 (`relframe.REL_CTX_DIM`) |
| s(a), r, R̄ | teacher score vector, floored normalised regret, its mean (`07_hypotheses_v3` §1.6) |
| G(κ) | relative one-step rollout headroom (§3.4 of the hypotheses) |

The student is `RelDeepSets`: ψ-MLP [F, H, H] on each (relative) touch, masked sum, ρ-MLP [H + 5, H, H, A], then a
per-row permutation from relative to absolute action order, feasibility mask, argmax (`train_v2.act`).

---

## 2. Time complexity (per decision / per call)

### 2.1 Greedy configuration G\*(N, C, M) — components of L_dec (§1.8 of the hypotheses)

Read off the code; constants dropped; "ops" means elementwise numpy work, not flops.

| Component | What the code does | Cost |
|---|---|---|
| t_assim (no resample) | `pf.update`: one `loglik` over N particles (cast against V edges) + normalisation + ESS | O(N·V) |
| t_assim (resample-move) | systematic resample O(N); m_s MH sweeps, each re-evaluating the **whole history** (`_hist_loglik`, T casts) and the contact-proposal density `_q_logpdf` (≤ T contacts × N × V) | O(m_s·T·N·V) |
| t_nb | `ball.neighbours`: N×N identity and distance tests, then per identity an n_k × n_k × \|G_k\| rotation test (n_k ≈ N/K) | O(N² + N²·\|G\|/K) |
| t_score | `ball_eig` in chunks of 16 candidates: casts N·C·V; M·C outcome samples; likelihood tensor (M, N, C); gather of nb rows (M, C, N); three masked log-sum-exps over N | O(N·C·V + M·N·C) |
| t_select | divide by c(a), argmax | O(C) |

**Total:** L_dec(G\*) = O(N·C·(V + M) + N²·(1 + \|G\|/K) + N·V·(1 + 𝟙_resample·m_s·T)).
This matches the implementation-independent count of `latency.lik_evals_rung` (M·N·C + N·C) for t_score but adds two
terms that count does not include: the O(N·C·V) casts and the O(N²) neighbour lists.

### 2.2 Student

- **As implemented** (`train_v2.act` builds a (T+1) × (T+1) relative-feature grid and runs ρ on all T+1 positions,
  then uses the last row): O((T+1)²·(F·H + H²) + (T+1)·((H+5)·H + H² + H·A)) MACs, plus O(T² ) trig for re-expressing
  the history relative to φ_t, plus O(A) for the permutation and mask.
- **Minimal** (only the current decision): O(T·(F·H + H²) + (H+5)·H + H² + H·A) MACs. This is what
  `latency.macs_policy(hidden, n_touch, ctx_dim=5, n_act=512)` counts.
- Both are **independent of N, C, M and V**. In A the cost is linear (last layer H·A); in T it is linear (minimal) or
  quadratic (as implemented). With H = 128, A = 512 the last layer (65,536 MACs) is the largest single term.
- Parameters: 117,504 [derived: ψ 17,792 + ρ 99,712].

### 2.3 Where a ≥ 100× per-decision ratio can come from, asymptotically

Ratio ρ_dec(N, C, M) = L_dec(G\*(N, C, M)) / L_dec(student) =
Θ( [N·C·(V + M) + N² + N·V·m_s·T] / [T·H² + H·A] ) (minimal student; replace by T²·H² + T·H·A as implemented).

- In the problem dimensions the ratio grows **linearly in each of N, C, M** (quadratically in N through the neighbour
  lists) because the student's cost does not depend on them. For fixed (N, C, M) it is a constant; "≥ 100×" is a
  statement about constants at the chosen sizes, not an asymptotic separation. Asymptotically one can only say that
  ρ_dec → ∞ as N·C·M → ∞ with (T, H, A) fixed, and that the student's cost scales with A while greedy scales with C ≤ A.
- A is shared: both sides are linear in A at C = A (greedy through N·(V+M)·A, the student through H·A). So the
  A-dependence cancels in the full-size ratio; the ratio is ≈ N·(V+M)/H at large A, i.e. it is the per-action
  cost "N particles × (V edges + M outcomes)" against "H hidden units".

### 2.4 Operation counts for the 27 configurations (snippet, arithmetic only)

Assumptions of the count: T = 4, m_s = 3, resample-move on every decision (upper bound), K = 8, \|G\| = 1, V = 14.
Units are mixed (ray–edge tests, likelihood evaluations, boolean pair tests vs MACs), so ratios are **order-of-magnitude
only**; a likelihood evaluation (Gaussian/von-Mises-type log terms, ε-mixture) costs several times a MAC.

| (N, C, M) | t_score ops | t_nb ops | t_assim ops | total | ÷ student (minimal, 1.69·10⁵) | ÷ student (as impl., 9.33·10⁵) |
|---|---|---|---|---|---|---|
| (2000, 512, 64) | 8.1·10⁷ | 4.5·10⁶ | 7.0·10⁵ | 8.6·10⁷ | ≈ 510 | ≈ 92 |
| (2000, 512, 4) | 2.0·10⁷ | 4.5·10⁶ | 7.0·10⁵ | 2.5·10⁷ | ≈ 146 | ≈ 26 |
| (2000, 32, 4) | 1.2·10⁶ | 4.5·10⁶ | 7.0·10⁵ | 6.4·10⁶ | ≈ 38 | ≈ 7 |
| (500, 512, 64) | 2.0·10⁷ | 2.8·10⁵ | 1.8·10⁵ | 2.1·10⁷ | ≈ 122 | ≈ 22 |
| (500, 128, 16) | 2.0·10⁶ | 2.8·10⁵ | 1.8·10⁵ | 2.4·10⁶ | ≈ 14 | ≈ 3 |
| (125, 512, 64) | 5.1·10⁶ | 1.8·10⁴ | 4.4·10⁴ | 5.1·10⁶ | ≈ 30 | ≈ 5 |
| (125, 32, 4) (grid floor) | 7.6·10⁴ | 1.8·10⁴ | 4.4·10⁴ | 1.4·10⁵ | ≈ 1 | ≈ 0.15 |

(All 27 rows were computed; with V = 40 the full-size ratio rises to ≈ 670 / 120.) Readings:

1. **Full-size G\*:** t_score ≈ 94 % of ops, t_nb ≈ 5 %, t_assim ≈ 1 % (V = 14). On op counts alone the full-size
   ratio is ≈ 10²–5·10². The only measured full-size figure, 0.840 s **[measured, 15_decision §3.4, 32 × 8, informal]**
   vs ≈ 0.53 ms **[measured, same source]**, gives ≈ 1,585× **[derived]**; with t_score doubling at 512 actions the
   planning value 1.7 s (§7) would give ≈ 3,200× **[derived, not measured]**. The gap between op ratio and wall ratio
   (≈ 3–15×) must therefore come from per-op constants (transcendentals in the likelihood and log-sum-exp, (M, N, 16)
   temporaries of ≈ 16 MB per array at full size, a Python loop over K in `neighbours`, 32 chunk iterations in
   `ball_eig`) versus the student's small dense matmuls. This is exactly what the cProfile share and the count ratio
   of §1.8 are meant to expose; until Lat′ the ≥ 100× full-size claim rests on one informal measurement.
2. **Small configurations:** for N·C·M ≲ 10⁶ the op ratio is O(1–10). Their wall time will be dominated by fixed
   numpy/Python dispatch overhead (identity loop, chunk loop, PF bookkeeping), which is also what dominates the
   student's ≈ 0.5 ms. Prediction (informal): the set Q of configurations within 100× of the student (§1.8) is
   **non-empty** and contains mid-sized configurations; H1b then rests entirely on their *accuracy* being worse, which is
   the intended design. The "grid floor" branch is unlikely on op counts but cannot be excluded without Lat′.
3. **H1-fb activation (pruned-16).** Pruned-16 keeps t_assim and t_nb at N = 2,000 and scores 16 candidates:
   ops ≈ 4.5·10⁶ + 7·10⁵ + 2.5·10⁶ + student ≈ 7.9·10⁶, ratio to full G\* ≈ **11** (V = 14) or ≈ 11.4 (V = 40)
   **[derived from the count]**. This is close to the pre-registered threshold 10; the O(N²) neighbour list is the
   binding term. Reviewers should expect H1-fb activation to be decided by constants, i.e. by Lat′, and the paper should
   not pre-announce it. (A spatial-hash neighbour list, O(N·n̄_B), would remove the N² term; that would be a code change
   affecting the comparator and is **not** proposed for v3.)
4. **Student implementation.** The as-implemented student does ≈ 5.5× the MACs of the minimal one at T = 4. Either is
   legitimate; the paper must state which one was timed. It does not change the asymptotics.

### 2.5 Other per-call costs (for compute accounting, not for claims)

- **L_final** (student only, §1.8): one N = 2,000 PF pass over T probes with resample-moves, O(T·N·V·(1 + m_s·T)),
  plus Nelder–Mead 30 iterations × O(T·V) per evaluation. Per episode, not per decision.
- **Evaluator** (`AdaptiveGridPosterior`, excluded from latency): coarse grid K·(30/h_xy)²·(360/h_θ) states × T casts
  (h_xy = 1 mm, h_θ = 2°: 8·900·180 ≈ 1.3·10⁶ states per probe [derived]) plus sub³ = 64 fine cells per refined
  coarse cell.
- **Labelling** for distillation: one full-size G\* call per labelled decision (the score vector is a by-product of the
  argmax, no extra asymptotic cost). Per cell: 1,500 round-0 episodes + 2 rounds × 400 × 5 seeds ≈ 5,500 episodes ×
  ≈ 4 decisions ≈ 2.2·10⁴ G\* calls [derived from §2.1 of the hypotheses].
- **H3 estimator** (`lookahead.py` + `lookahead_tb.py`): per belief (C1·M_out + (top+1)·reest·M_out) = 32·64 + 5·256
  = 3,328 rollouts [derived], each up to (n\* − t − 1) greedy completions on a fixed 500-particle set
  (no MH inside rollouts, neighbour list precomputed once): O(3,328·n\*·(500·128·(V + 16))) with the completion
  settings read from the code (see §6 item 9).

---

## 3. Space complexity

| Object | Space |
|---|---|
| PF (any configuration) | O(N·(4 + 1)) state + O(N) cached history log-likelihood + O(T) history |
| Neighbour lists | O(N²) booleans (4 MB at N = 2,000; 0.25 MB at 500) + O((N/K)²·\|G\|) float temporaries per identity |
| `ball_eig` working set | per 16-candidate chunk: casts O(N·16·V), likelihood/joint tensors O(M·N·16) floats (≈ 16 MB each at full size), nb gather O(M·16·N) booleans |
| Greedy total | **O(N² + M·N·16 + N·16·V)**, independent of C thanks to chunking |
| Student weights | O(F·H + H² + H·A) = 117,504 parameters (≈ 0.9 MB float64) |
| Student activations | O(T²·H + T·A) as implemented; O(T·H + A) minimal |
| Distillation data | O(#labelled decisions × A) floats: ≈ 2.2·10⁴ × 512 × 4 B ≈ 45 MB per cell [derived] |
| Evaluator | O(K·n_xy²·n_θ) floats for the coarse grid (≈ 10 MB) + batched fine cells |

---

## 4. Convergence statements

None of the hypotheses is a convergence claim; all are statistical claims about finite-sample experiments. The
statements below say what can and cannot be guaranteed about the components. **Every item in this section is an
informal argument; full proof deferred to appendix / future work** unless it is explicitly an existing published result
described in words (to be verified, §8).

### 4.1 Consistency of the EIG_B estimate (informal)

*Statement.* Fix a history h and an action a. If the PF is consistent for p(s | h) as N → ∞ (resample-move with
posterior-invariant MH kernels, as in `pf.py`), then the `ball_eig` estimate converges in probability to EIG_B(a; b)
as N → ∞ and M → ∞, with bias of order 1/N (nested estimator) and variance of order 1/M + 1/N.

*Sketch.* The per-outcome term is log P̂(B(s_j) | y) − log P̂(B(s_j)) where both are ratios of weighted particle sums;
each sum is a consistent estimator, so the log-ratio is consistent by the continuous-mapping argument, and its bias
from the concave log is O(1/N) by a delta-method expansion (the generic nested-MC behaviour of Rainforth et al.,
to verify). The ε-softened likelihood is bounded above and below by positive multiples of a reference density, so
likelihood ratios are bounded and each per-outcome term is bounded by a constant R(ε) that does not depend on N.

*Why rigor is hard here.* (i) Uniform-in-time PF consistency with resample-move on a multimodal, partly unidentifiable
SE(2) × identity posterior needs mixing assumptions on the MH kernels that we cannot verify. (ii) The "true state" in
each outcome is a particle j_m, and the ball around it includes particle j_m itself. With the prior ball mass
P(B) ≈ 3.0·10⁻⁴, the expected number of *other* particles in a ball before any contact is ≈ 0.61 (N = 2,000), 0.15
(500) and 0.04 (125) [derived]. So at early decisions EIG_B as estimated is dominated by the self term and behaves like
a particle-level full-state information gain; the ball target only "switches on" after resample-move concentrates
particles. This self-inclusion bias is upward, **action-dependent** and larger at small N, so it can change the
argmax, not only the value. It is one plausible mechanism by which small-N grid configurations lose accuracy; the
claim is informal and is tested only indirectly (pilot success of grid configurations).

### 4.2 Argmax selection error of G\* (informal)

*Statement.* Conditional on the particle set, let Δ = gap between the best and second-best true (particle-level)
EIG_B/c among the C candidates. Because each per-outcome term is bounded by R(ε), a Hoeffding-type bound plus a union
bound over C candidates gives P(G\* selects an action with score below the best by > Δ) ≤ 2C·exp(−M·Δ²·c_min²/(2R²))
in form. *Informal argument; full proof deferred*: candidates share the particle set and the sampling across
candidates is not independent (the bound holds per candidate regardless, the union bound does not need independence),
but R(ε) as implemented is large (ε small), so the bound is vacuous at M = 64 for realistic Δ. Its only use is
qualitative: at near-ties (small Δ) the teacher's argmax is noise-driven for any feasible M. This is why the regret is
floored and why the teacher noise floor of §1.6 is measured rather than bounded.

### 4.3 What the DAgger reduction does and does not guarantee here

*Published result, described.* The DAgger reduction of Ross, Gordon & Bagnell (2011) shows, roughly: if the learner
used across rounds is a no-regret online learner on a surrogate loss ℓ evaluated on the aggregated states visited by
the learned policies, then after enough rounds there is a policy among the iterates whose expected surrogate loss under
**its own** state distribution is close to the best achievable in the class (ε_class) plus a regret term that vanishes
with the number of rounds, and, when ℓ upper-bounds the probability of disagreeing with the expert, its task cost
exceeds the expert's by at most a term linear in the horizon times that loss (times a constant bounding how much one
deviation increases the expert's cost-to-go). A cost-to-go variant (AggreVaTe, Ross & Bagnell 2014, to verify) replaces
disagreement by the expert's Q-value regret. The precise constants must be taken from the papers.

*Reading for this design (informal).* The performance-difference identity (Kakade & Langford, to verify) gives exactly
J(G\*) − J(π) = Σ_t E_{b_t ∼ d_π}[ Q^{G\*}_t(b_t, G\*(b_t)) − Q^{G\*}_t(b_t, π(b_t)) ] for any terminal or additive
objective J (success probability or BI). What the design does **not** satisfy:

1. **Teacher, not optimum.** Every bound is relative to G\*. Non-inferiority to G\* says nothing about optimality; H3
   is the only (partial) handle on G\*'s own sub-optimality.
2. **Surrogate ≠ task loss, and ≠ Q-regret.** The student minimises soft-label CE to softmax(β_T·s/σ_s) (+ λ·CE to the
   argmax). s(a) = EIG_B/c is a one-step score, not Q^{G\*}(b, a). Two actions with equal s can have different
   Q^{G\*} (their future travel positions differ), and vice versa. Hence neither small CE nor small R̄ implies small
   per-step Q-regret, and the linear-in-horizon task bound does not follow. Only the λ·CE-to-argmax term relates to
   the disagreement loss that the reduction uses; the soft term is a regulariser with no guarantee. This is consistent
   with the hypotheses' rule that **no R̄ threshold is a prediction**.
3. **Noisy, approximate teacher.** G\*'s action is a random function of the history (PF and MC randomness, §4.2).
   The disagreement loss then has an irreducible floor ≈ the teacher's own self-disagreement rate (measured as the
   noise floor, §1.6), so "ε_class small" is not available even for a perfect learner. A deterministic student can at
   best match the modal teacher action; near ties this is harmless for J, away from ties it is not.
4. **No-regret learner.** The reduction needs a no-regret online learner (e.g. follow-the-leader on a strongly convex
   loss). Here the learner is a non-convex network warm-started from the previous round, trained for a finite number
   of epochs with early stopping on R̄. No regret guarantee holds.
5. **Three rounds.** The vanishing regret and β-mixing terms of the reduction are asymptotic in the number of rounds.
   With round 0 (pure teacher), round 1 (β = 0.5) and round 2 (β = 0) nothing quantitative survives; the reduction
   only motivates why student-visited beliefs are labelled. The hypotheses use the last iterate, whereas the reduction
   guarantees the best (or a uniformly mixed) iterate.
6. **Short horizon.** With ≈ 4 decisions per episode, behavioural cloning's compounding (quadratic in the horizon) and
   DAgger's (linear) differ by a factor ≈ 4 in the worst-case bounds [derived], so a small BC-vs-DAgger difference in
   the ablation row would not contradict the theory.
7. **Partial observability / policy class.** G\* acts on a belief; the student acts on the raw relative history. Since
   the belief is a (randomised) function of the history, the teacher is realisable in principle by a history policy,
   but the DeepSets encoder (permutation-invariant sum over touches, order only through the features) may not represent
   it; realisability is an assumption, probed by the training-set fit and the belief-input control of H2.

What the reduction *does* license: it explains why labelling on student-visited beliefs (rounds 1–2) addresses the
covariate shift that BC suffers; and, if the student's per-belief disagreement with G\* is small on its own
distribution *and* disagreements happen mostly at near-ties of Q^{G\*}, then J(student) ≈ J(G\*). Neither condition is
guaranteed; H1a tests the conclusion directly.

### 4.4 Why adaptive-submodularity guarantees for greedy do not transfer (informal)

*Published results, described.* Golovin & Krause (adaptive submodularity) show that for an adaptive monotone
submodular objective with **modular, state-independent** item costs, adaptive greedy (gain, or gain per cost) is within
a constant factor (1 − 1/e for cardinality-type budgets) or a logarithmic factor (for minimum-cost coverage) of the
optimal adaptive policy. For Bayesian identification with noise, plain information gain is in general **not**
adaptive submodular, which is why surrogate objectives (EC², Golovin, Krause & Ray; submodular surrogates of value of
information, chen2015submodular) were introduced; touch-based localisation via submodularity (javdani2012efficient)
uses such a surrogate.

*Why nothing transfers here.*
1. **Objective.** G\* maximises EIG_B, a one-step expected increment of a log ball mass. We know no argument that
   log P(B(s) | h) is adaptive monotone submodular in the probe set; log-mass objectives can show complementarity (two
   probes jointly resolve a symmetry that neither resolves alone: the S set's near-symmetric pairs are built for that).
   So even at κ = 0 no guarantee is available for G\*.
2. **Order-dependent costs.** With travel, c(a | φ_t) depends on the previous action. The budget constraint is on a
   path length, i.e. an (adaptive, stochastic) orienteering-type problem. Ratio-greedy then has no constant-factor
   guarantee even for modular rewards (informative path planning: singh2009efficient, hollinger2014sampling). A
   standard informal failure mode: a slightly better ratio far away moves the finger to where nothing else is
   informative, and travelling back exhausts the budget.
3. **A trivial bound and why it is useless.** In a non-adaptive idealisation with submodular gains and n\* affordable
   probes: the greedy first pick has ratio ≥ g_max/(1 + κ) and cost ≥ 1, so gain ≥ g_max/(1 + κ), while OPT ≤
   n\*·g_max. Hence a factor ≤ n\*·(1 + κ) ≈ 4·13 = 52 at κ = 12 [derived]. This is vacuous and itself rests on
   submodularity, which we do not have.

Conclusion: the teacher's quality is an empirical question; H3 measures one aspect of it.

### 4.5 What the one-step look-ahead headroom (H3) can and cannot say

*An exact fact (finite horizon, exact evaluation; standard dynamic programming, "rollout"/policy-improvement
argument of Bertsekas, to verify).* For a deterministic base policy π on the belief MDP, the one-step rollout policy
is no worse than π. If at **every reachable belief** and **every feasible action** the one-step deviation followed by
π has value ≤ π's value, π satisfies the Bellman optimality equation and is optimal.

*What G(12) measures instead (as implemented).*
- 100 beliefs reached by G\* (not all reachable beliefs, not the student's beliefs).
- ≤ 32 screened first actions of 512 (G\*'s own, structured set-up moves, the rest uniform), top 4 re-estimated: V_LA
  is a **lower bound** on the best one-step deviation (up to MC noise and the max-of-noisy-means upward bias the
  re-estimation is designed to remove).
- Completion by a greedy that, as read in `lookahead_tb.py`/`g2.py`, uses N = 500 fixed particles (no MH), the
  (16, 8) candidate rung and M = 16, while the first G\* action is the full-size one. The hypotheses text says
  "G\* completion, M = 64" (§6 item 9).
- Values are ratio-of-means in expected remaining ball information (nats), not success.

*Hence H3 can say:* "replacing G\*'s first action by the best of ≤ 32 screened alternatives, with this greedy
completion, gains ≤ 100·UB % of the remaining expected ball information on average over G\*-reached beliefs at κ = 12".
*It cannot say:* that G\* is near-optimal (multi-step deviations; the completion policy is itself greedy; unscreened
actions; G is a mean, so a minority of beliefs with large headroom is compatible with a small G); anything about
success; anything at beliefs the student visits. A small G is necessary but far from sufficient for optimality, and
the Bellman fact above shows what a sufficient check would require (all beliefs, all actions, exact evaluation).

### 4.6 Training convergence

No convergence guarantee is claimed for the student (non-convex network, finite epochs, stop on R̄ plateau) or for PPO
(H2). The operational criteria are the pre-registered stop rules.

---

## 5. Comparison with the closest baselines' known bounds

| Method | Per-decision cost | Space | Guarantee known to us |
|---|---|---|---|
| G\* full size (teacher; closest baseline) | O(N·A·(V+M) + N² + N·V·m_s·T) | O(N² + M·N·16) | none (§4.4); consistency of EIG_B estimate only, informal (§4.1) |
| Greedy grid G\*(N, C, M) | O(N·C·(V+M) + N² + N·V·m_s·T) | same | as G\*; selection noise grows as M falls (§4.2), self-inclusion bias grows as N falls (§4.1) |
| H1-fb pruned-16 | O(student) + O(N·16·(V+M) + N² + N·V·m_s·T) | as G\* | inherits G\*'s; ≈ 11× op ratio to G\* (§2.4) |
| Heuristics B-spread / B-fan | O(A·T) / O(A) | O(A) | none; belief-free |
| B-cov (`CoverageV2`) | O(N + A·V + A·T) per decision + PF update O(N·V·(1 + m_s·T)) | O(N) | none |
| Student (ours) | O(T·H² + H·A) minimal; O(T²·H² + T·H·A) as implemented | O(H² + H·A) | none for task loss; DAgger motivation only (§4.3) |
| RL-relative (H2) | as student | as student | none (PPO, non-convex) |
| Rollout planner / H3 estimator | O(W^D·N·C·(V+M)) per decision for depth D; H3: ≈ 3.3·10³ rollouts per belief | — | policy improvement over the base greedy for exact evaluation only |
| Published tactile EIG selection (Gordon et al., arXiv:2510.13595) | online one-step EIG; per-decision compute not reported (06_synthesis gap, per the hypotheses) | — | qualitative only; not verified by us |
| Imitation of information-gathering experts (Choudhury et al. 2017; Nguyen et al. arXiv:2405.15031) | forward pass of a learned policy | — | imitation-reduction type, relative to the expert; exact statements to verify |

Qualitative position: the student's cost is of the same kind as amortised/policy-based BED and imitation-learned
information gathering (a forward pass, independent of the belief resolution); greedy information gathering re-optimises
online at cost linear in particles × candidates × outcome samples. No published bound compares the two at matched
accuracy; H1b is an empirical, not a theoretical, comparison.

---

## 6. Honesty section

**Assumptions that could fail in practice.**
1. **Op counts ≠ time.** The 100× claim is about wall time under the §2.3 protocol of v2. Op ratios (§2.4) are
   ≈ 10²–5·10² at full size; the measured 1,585× [derived from informal measurements] relies on constants. A
   vectorisation or compilation change (numba/JAX for `ball_eig`, a C++ PF) could reduce greedy time by an order of
   magnitude without changing asymptotics. The claim must be stated "for these numpy implementations", with the count
   ratios reported (as §1.8 requires).
2. **The two latency figures in the repository disagree.** 0.840 s/decision **[measured, 15_decision §3.4, 32 × 8,
   G5 runs]** vs "G\* ≈ 2.3 s/decision at M = 32" **[measured, PROGRESS.md stage-10 v2 note, sandbox]**. Machine,
   build and decision mix differ; neither is a protocol measurement. The 1.7 s planning figure at 512 is an assumption.
3. **The split of L_dec is unmeasured.** §2.4 predicts t_score ≈ 94 % of ops; if t_nb or resample-move dominate wall
   time (Python loop over identities, history re-evaluation at large T), the H1-fb activation and the shape of the
   Pareto front change.
4. **Q is likely non-empty and contains mid-sized configurations** (§2.4 item 2). H1b then hinges on their pilot
   accuracy; if success is flat in N, C, M (a flat task), H1b fails, and it should.
5. **Student not realisable / teacher noisy.** §4.3 items 3 and 7. A training-set R̄ well above the noise floor at
   the end of round 2 indicates non-realisability (capacity or encoder), not a DAgger failure.
6. **Ball target degenerate at early decisions** (§4.1): if most first-decision scores are self-term dominated, the
   student is in effect distilling a particle-level full-state EIG early and a ball EIG later. Not wrong, but the
   paper should not describe the early decisions as "ball-targeted".
7. **Travel model.** Finger on a stand-off circle with cost linear in angular travel; conclusions about κ hold for
   this model only (unchanged from v2).
8. **History length.** All student costs assume T ≤ 6; the as-implemented quadratic re-encoding would matter only for
   much longer episodes.
9. **Code/text mismatch to reconcile before the amendment.** `g2.py` calls `lookahead_gap(..., greedy_M=0)`, so
   rollouts use `TouchbedProblem.M` = 16 with `rung_subset(16, 8)`; the hypotheses say "G\* completion, M = 64". The amendment should state which
   completion is frozen. (`travel.rung_subset` uses `N_PHI // n_phi`, so the nested subsets of §1.8 follow the N_PHI
   flag as long as it is the module constant.) This is an observation from reading the code, not verified by running it.

**Observed behaviour that would invalidate the statements above.**
- Lat′ finds full-size L_dec ratio < 100× → the "≥ 100× per decision" statement fails at full size, regardless of H1b.
- The measured L_dec of any configuration does not grow with N·C·M (e.g. flat across C) → overhead dominates and the
  asymptotic reading of §2.3 does not apply at these sizes; only measured ratios may be quoted.
- Pruned-16 ratio far from ≈ 11 (e.g. < 5 or > 30) → the component model of §2.1 is wrong about t_nb or t_assim.
- G\* re-scored with an independent RNG disagrees with itself on a large fraction of decisions away from ties →
  §4.2's "noise only at near-ties" is wrong; the teacher is noisier than assumed, and the student's NI margin must
  absorb teacher noise.
- Small-N configurations are as accurate as N = 2,000 → the self-inclusion mechanism of §4.1 is negligible.
- H3: the bias check ratio > 1.02 or the travel-notch control fails → the estimator cannot certify small headroom
  (already pre-registered). Additionally, a G(12) that is small on average while a visible minority of beliefs show
  relative gaps ≫ 0.03 would mean "small on average", not "small", and the wording must say so.
- BC-only matches the DAgger student → consistent with §4.3 item 6 (short horizon), not a refutation of DAgger; the
  paper must then not attribute NI to DAgger specifically.

---

## 7. Summary of formal status

| Statement | Status |
|---|---|
| Per-decision costs and space (§2, §3) | derived from the code; constants unmeasured |
| ≥ 100× per decision | empirical; op counts give 10²–5·10² at full size; one informal wall-clock measurement gives ≈ 1.6·10³ |
| EIG_B consistency, selection error | informal argument; full proof deferred (§4.1, §4.2) |
| DAgger guarantee for this student | does not apply as stated; motivation only (§4.3) |
| Greedy approximation guarantee | none; classical results do not transfer (§4.4) |
| H3 meaning | one-step rollout headroom over G\* with reduced completion, on G\*-reached beliefs; no optimality claim (§4.5) |

---

## 8. References to verify

Only described in this file; none is cited as verified. Identifiers marked "believed" come from memory and must be
checked by the main session.

| Reference (as described) | Identifier |
|---|---|
| Ross, Gordon, Bagnell, "A Reduction of Imitation Learning and Structured Prediction to No-Regret Online Learning", AISTATS 2011 (DAgger) | arXiv:1011.0686 (believed) |
| Ross, Bagnell, "Reinforcement and Imitation Learning via Interactive No-Regret Learning" (AggreVaTe), 2014 | arXiv:1406.5979 (believed) |
| Kakade, Langford, "Approximately Optimal Approximate Reinforcement Learning", ICML 2002 (performance difference identity) | identifier unknown |
| Golovin, Krause, "Adaptive Submodularity: Theory and Applications in Active Learning and Stochastic Optimization", JAIR 2011 | arXiv:1003.3967 (believed) |
| Golovin, Krause, Ray, "Near-Optimal Bayesian Active Learning with Noisy Observations" (EC²), NeurIPS 2010 | arXiv:1010.3091 (believed) |
| chen2015submodular, "Submodular Surrogates for Value of Information", AAAI 2015 | doi:10.1609/aaai.v29i1.9694 (from knowledge card) |
| javdani2012efficient, "Efficient Touch Based Localization through Submodularity" | doi:10.1184/r1/6554705 (from knowledge card) |
| singh2009efficient, efficient informative path planning, JAIR | doi:10.1613/jair.2674 (v2 file says verified via OpenAlex) |
| hollinger2014sampling, sampling-based informative path planning, IJRR | doi:10.1177/0278364914533443 (v2 file says verified via OpenAlex) |
| Bertsekas, rollout / policy-improvement property (textbook or rollout-algorithm papers) | identifier unknown |
| Rainforth et al., "On Nesting Monte Carlo Estimators", ICML 2018 (nested-MC bias) | arXiv:1709.06181 (believed) |
| Hoeffding, "Probability Inequalities for Sums of Bounded Random Variables", JASA 1963 | doi:10.1080/01621459.1963.10500830 (believed) |
| SMC / particle-filter consistency with MCMC moves (e.g. Del Moral; Chopin) | identifier unknown |
| Gordon, Baraki, Bui, Posa, "Active Tactile Exploration for Rigid Body Pose and Shape Estimation" | arXiv:2510.13595 (from 07_hypotheses_v3 §8) |
| Choudhury et al., "Adaptive Information Gathering via Imitation Learning", RSS 2017 | arXiv:1705.07834; DOI 10.15607/RSS.2017.XIII.041 (from 07_hypotheses_v3 §8) |
| Nguyen, Sarkar, Garnett, "Amortized nonmyopic active search via deep imitation learning" | arXiv:2405.15031 (from 07_hypotheses_v3 §8) |
