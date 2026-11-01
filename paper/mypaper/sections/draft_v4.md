# Cost-Aware Information-Gain Touch Selection under Travel Cost: Look-Ahead Headroom and Learnability in a Stay-and-Probe and a Travelling Regime

## Abstract

Active tactile localization chooses the next touch from a belief over object identity and pose, and when moving the
finger costs time, that choice trades information against travel. We ask how much headroom one-step look-ahead leaves
over greedy cost-aware information-gain touch selection (G\*), and whether G\* can be amortized by a policy distilled
from it or trained by reinforcement learning (RL) on the same objective. The task uses a joint identity × planar-pose
particle belief and a finger on a stand-off circle with travel cost $c(a) = 1 + \kappa|\Delta\phi|/\pi$. We study two
cells: S12 (κ = 12), a stay-and-probe regime where G\* moves the finger 4.3° between probes per episode, and S2
(κ = 2), in which it moves 44.8°. Over 32 screened first actions, one-step rollout over a reduced greedy completion
gains at most 2.2 % of the remaining expected ball information at κ = 12 (one-sided 95 % bound). With one belief-free
DeepSets head, neither the DAgger-distilled student nor PPO was shown to reach G\* in either cell: the student failed its
pre-registered non-inferiority gate twice in S12 and once in S2. Distillation had no detected advantage over RL on
RL's own contrastive objective, which ranks G\* below both learners, unlike the grid posterior. In S2 the
student exceeds a stay-and-fan heuristic on ball information (+0.53 nats) and success (+8.1 pp). Reduced-size G\* at
21–46 ms per decision trails the students on ball information. The study is pre-registered, with one cell per regime;
results are preliminary.

## 1 Introduction

A robot that localizes an object by touch receives sparse, ambiguous measurements: one contact point and one surface
normal per probe, or a miss. A single contact rarely fixes the pose, and near-symmetric object families make even the
identity uncertain. The standard remedy is to maintain a belief over identity and pose, typically a particle filter,
and to choose the next touch by its expected information gain \cite{petrovskaya2011global, hebert2013next,
zheng2024bayesian, zheng2026bayesian}. Probing is not free. The finger has to travel to the next approach direction,
and travel time competes with probes inside a fixed time budget. Cost-aware selection therefore scores each candidate
by information per unit cost \cite{ottenhaus2018active}, and surveys of active haptic perception identify this
trade-off as central to practical exploration \cite{seminara2019active}.

Two questions follow for every information-driven touch selector that pays for travel. The first concerns planning
depth. Greedy information gathering is backed by (adaptive) submodularity: for touch-based localization, entropy
reduction is submodular under certain assumptions, and greedy selection is then comparable to the optimal offline
policy \cite{javdani2012efficient, vien2015touch}. These guarantees weaken when actions constrain the future
\cite{chen2015submodular, esfandiari2019adaptivity}, and travel cost is exactly such a coupling: where the finger ends
up after a probe determines what the next probe costs. Whether paying for look-ahead is worth it under travel cost is
an empirical question that, to our knowledge, has not been measured directly.

The second question concerns amortization. Online particle-filter information gain re-optimises at every decision,
with a cost that grows with particles × candidates × outcome samples. Amortized Bayesian experimental design replaces
this with a policy network trained once, by RL on contrastive information bounds or related objectives
\cite{foster2021deep, blau2022optimizing, ivanova2021implicit, hedman2025step, rainforth2024modern}, and tactile RL
methods learn exploration policies end to end \cite{riou2024reinforcement, niemann2024when}. A validated greedy
planner offers a second route: supervising the policy with the planner's dense per-action scores through DAgger
\cite{ross2011reduction}, in the spirit of imitating an information-gathering expert \cite{choudhury2017adaptive},
which removes long-horizon credit assignment and 512-way exploration from the learning problem. PPO
\cite{schulman2017proximal} on the same objective is the natural comparator. The questions are whether either learner
reaches the planner, and whether dense supervision does better than RL on RL's own objective with the same head. A
third, less obvious question is hidden inside the second: whether RL's own objective, a contrastive bound on
information, orders policies the same way as the posterior that is used to judge localization.

**Two regimes.** Our first design iteration studied one cell, S12 (shape set S, κ = 12, four probes). It turned out to
be a *stay-and-probe* regime: on test, 79.3 % of the planner's between-probe moves are zero, and the finger moves on
average 4.3° per episode between probes (test3 episodes 0–299). The logged total travel is slightly larger, 5.7° on
episodes 0–299 and 6.1° on episodes 0–499, because every episode starts from a continuous start angle and its first
move includes a snap onto the 5.625° action grid that no policy chooses (Section 3.1). Either way, the motivating
scenario of a finger stranded far from the informative region has little room to occur. We therefore added a second
cell, S2 (κ = 2), whose budget was set by the same calibration rule for four probes; that rule's probe-count
verification for S2 has not yet been completed ([PENDING:v4:cal_verify_S_k2]), and on test the planner executes
3.873 probes on average. In S2 the planner moves 44.8° between probes per episode (46.9° logged). Both cells use the
same planner, the same learners and the same head, so the price of moving is the only design variable that changes
between them.

*Figure 1 (placeholder; schematic panels A–C and data inset D are produced separately): cost-aware touch selection in
two travel regimes, the three selectors compared, and the headline headroom bound and test rows.*

**Findings.** We state each result once and plainly here; the qualifiers that apply to all of them (one cell per
regime, three seeds per learner, no multiplicity correction, an evaluator not shown converged, a reused test split)
are collected in Section 7. In S12, one-step rollout over a reduced greedy completion gains at most 2.2 % of the
remaining expected ball information over the 32 screened first actions (one-sided 95 % bound); the κ = 2 row of the
same estimator, measured in the S2 cell configuration, is also small (upper bound 2.0 %). Neither learner was shown
to reach G\* in either regime. In S12 the distilled student failed its pre-registered non-inferiority gate on the first attempt and
after its one remedy. In S2 it failed again: on validation the success deficit was −2.80 pp against a threshold of
−1.46 pp, and on test episodes 0–299 the student trails G\* by 0.183 nats of ball information (ci95 [−0.269, −0.094])
and by 10.2 pp in success (ci95 [−16.6, −4.3]). On RL's own objective, the contrastive return $g_T$, no advantage of
distillation was detected in either cell, and in S2 the point estimate favours RL by 0.445 nats. That objective,
however, ranks G\* below both learners, whereas the grid posterior ranks G\* above both, and on the grid posterior the
student leads RL on ball information in both cells (+0.289 and +0.180 nats). In S2 the student exceeds a belief-free
stay-and-fan heuristic on ball information (+0.528 nats) and on success (+8.1 pp), whereas in S12 it exceeded the
heuristic only on ball information. Two reduced-size G\* configurations, at logged median per-decision latencies of
20.8 and 46.0 ms, trail the distilled student on ball information by 0.16–0.23 nats, with success unresolved.

**Contributions.**
- **C1.** A pre-registered bound on one-step look-ahead headroom over cost-aware greedy touch selection at κ = 12 over
  the screened first actions with a reduced greedy completion (H3, Hold), with κ = 0 and κ = 2 rows, instrument
  checks and an on-belief bias check.
- **C2.** A learnability study of one belief-free relative head in a stay-and-probe cell (two gate attempts) and a
  travelling cell (one gate), with a behavioural diagnosis of finger travel, split into the unavoidable grid snap and
  discretionary between-probe travel, and of probe use.
- **C3.** A comparison of planner distillation against RL on RL's own objective in both cells, together with the
  observation that this contrastive objective and the grid posterior order the planner and the learners differently,
  and an exploratory separation of the student from a stay-and-fan heuristic in S2.
- **C4.** A per-decision cost analysis: a latency decomposition of G\* and an exploratory comparison of reduced-size
  G\* with the students at logged latency, cross-checked against the latency protocol where it covers the same
  configurations.

Instrument notes that earlier drafts listed as a contribution (the resolution of the evaluator and the S2
validation/test discrepancy) are reported as methods notes in Section 4 and as limitations in Section 7, because they
describe the measurement rather than the answer to the research question. The $g_T$/grid-posterior disagreement stays
inside C3 because it changes how the learner comparison must be read.

The outcome reported here (row 4 of the pre-registered outcome map: a characterisation paper with no method claim)
was written before the runs, and the S2 readings were fixed in an amendment written before any S2 run. Section 2
reviews related work, Section 3 defines the task, planner, headroom estimator and learners, Section 4 gives the
protocol, Section 5 the results, and Sections 6–8 discuss, bound and conclude.

## 2 Related Work

**Tactile localization and next-best touch.** Estimating object pose from touch is usually posed as Bayesian
filtering. Scaling-series Monte Carlo achieves global localization from sparse contacts on polygonal meshes
\cite{petrovskaya2011global}; manifold particle filters sample on the contact manifold to avoid degeneracy in planar
contact manipulation \cite{koval2015pose}; Tac2Pose returns a pose distribution from a single high-resolution touch
\cite{bauza2023tac2pose}. On top of such estimators, information-driven selection picks the next touch. The next best
touch maximises information gain on pose uncertainty \cite{hebert2013next}; Bayesian frameworks jointly track class
and pose with customised particle filters and choose exploratory actions by expected information
\cite{zheng2024bayesian, zheng2026bayesian}; recent work selects contacts by expected information gain for rigid-body
pose and shape \cite{gordon2026active}, or learns a single exploration policy on hardware that balances global search
against local refinement \cite{kamtikar2026tactful}. Cost-aware information gain combines expected gain with expected
cost in one score \cite{ottenhaus2018active}, and reviews of active haptic perception summarise the space
\cite{seminara2019active}, including the coverage-style heuristics that remain the usual reference points for any
information-driven selector. Per-step (myopic) selection is the norm in this line. How much it leaves on the table
under travel cost, and whether the answer depends on whether the selector actually travels, is rarely measured; C1 and
C2 address both for one task and two regimes. Greedy cost-aware selection itself is established, and we propose no new
selector. Several of the systems above run on hardware with 3D geometry and real contact; our study is planar and
simulated, and we use it to isolate the selection question rather than to compete with those systems.

**Greedy versus non-myopic information gathering.** Submodularity explains why greedy selection works well for touch:
Shannon entropy reduction is submodular under certain assumptions, and adaptive submodularity gives online guarantees
\cite{javdani2012efficient}. Hierarchical action structure can be folded into the same framework through sequential
submodular optimisation \cite{vien2015touch}. Outside touch, submodular surrogates approximate the value of
information when the objective itself is not submodular \cite{chen2015submodular}, and semi-adaptive policies show how
much adaptivity is needed to retain guarantees \cite{esfandiari2019adaptivity}. These results assume structure that
travel cost can break: a probe changes the price of every later probe, so the information an action buys is no longer
independent of where the finger ends up. Rather than bound the gap theoretically, we measure one-step rollout headroom
over the cost-aware greedy planner directly, with an estimator checked on a construction whose exact gap is known and
on a bank whose gap is zero. The measurement is empirical and local: it bounds one deviating step among screened
candidates, not the gap to the optimal policy. A small measured headroom is therefore expected from the theory above
and is informative mainly as a check that travel cost, at the tested budgets, does not break it.

**Amortized and learned active sensing.** Deep adaptive design trains a design network on contrastive information
bounds so that each decision is a forward pass \cite{foster2021deep}; implicit and RL formulations remove the need for
likelihoods or differentiable simulators \cite{ivanova2021implicit, blau2022optimizing}; semi-amortized variants
refine the policy online \cite{hedman2025step}; nested particle filters amortize design in dynamical systems
\cite{iqbal2024recursive}; and transformer policies amortize inference and acquisition jointly \cite{huang2026aline}.
A recent review covers the field \cite{rainforth2024modern}. In this line a contrastive bound of the sPCE type is
usually both the training objective and the reported quality measure of a learned policy \cite{foster2021deep,
blau2022optimizing}; whether such a bound orders policies in the same way as a posterior-based localization metric is
rarely checked, and C3 reports a case in which it does not. In touch, RL agents explore for recognition with rewards
for correct classification \cite{riou2021seeing, fleer2020efficient}, for classification, exploration and pose
\cite{riou2024reinforcement}, or learn when to stop \cite{niemann2024when}; TANDEM3D co-trains exploration and decision
making on 3D contacts \cite{xu2023tandem3d}, and Tactile MNIST provides a benchmark that includes localization
\cite{schneider2025tactile}. A second route imitates an information-gathering expert: imitation of a clairvoyant oracle
\cite{choudhury2017adaptive} and deep imitation of a nonmyopic active-search expert \cite{nguyen2024amortized}, both
building on DAgger's no-regret reduction \cite{ross2011reduction}. The comparison between the two routes therefore has
precedent in spirit. What is missing is a controlled comparison of RL against supervised distillation of a validated
planner, with the same head, the same action set and the same objective, evaluated on the objective RL itself
optimises, and repeated in a regime where the planner barely moves and one where it travels. C2 and C3 supply that
comparison for one cell per regime. A third route to a cheaper decision is not to learn at all but to shrink the
planner; amortization claims are informative only against that alternative, which C4 examines at logged latency.

## 3 Method

### 3.1 Task, belief, metrics and the two cells

**State and observations.** The object is a planar polygon with identity $k \in \{1,\dots,K\}$ from shape library S
(K = 8 identities: 4 near-symmetric base shapes and one symmetry-breaking variant of each, i.e. 4 base/variant pairs)
and unknown pose, so the state is $s = (k, x, y, \theta)$ with a uniform prior over identity, position in a ±15 mm box
and orientation, and $G_k$ is the exact symmetry group of shape $k$. A probe returns either a contact point and a
surface normal, both with Gaussian noise ($\sigma_p$ = 1.0 mm, $\sigma_n$ = 5°), or a miss $y = \varnothing$. Every
method uses the same ε-softened likelihood $p_\varepsilon(y \mid s, a)$, so differences between methods come from
which actions they choose and how they use the resulting observations, not from different sensor models.

**Actions and travel cost.** The finger rests on a stand-off circle at angle $\phi_t$, with a start angle shared by
all methods on an episode. An action $a = (\phi', \psi)$ selects one of 64 target angles $\phi'$ (grid step 5.625°)
and one of 8 approach offsets $\psi$, so $|\mathcal{A}| = 64 \times 8 = 512$. The finger travels the shorter way to
$\phi'$, probes inward along direction $\phi' + \pi + \psi$ with a guarded stroke, and then $\phi_{t+1} = \phi'$. In
units of one stroke,

$$c(a) = 1 + \kappa\,\frac{|\Delta\phi|}{\pi}, \qquad \Delta\phi = \mathrm{wrap}(\phi' - \phi_t) \in (-\pi, \pi],$$

so κ is the time to travel half the circle. With remaining time $\tau_{\mathrm{rem}}$, the feasible set is
$\mathcal{F}(\tau_{\mathrm{rem}}) = \{a : c(a) \le \tau_{\mathrm{rem}}\}$, every method chooses only within it, and the
episode ends when no action is feasible.

**Start angle, logged travel and between-probe travel.** The start angle $\phi_0$ is drawn from a continuous uniform
distribution on the circle, whereas every target angle lies on the 5.625° grid. The first leg of every episode
therefore includes a move onto the grid, even for a policy that "stays where it is"; the cost formula above applies to
that leg as to any other. We call the total angular distance the finger covers in an episode, including this first
leg, its *logged travel*, and the part covered after the first probe its *between-probe travel*; logged travel is the
sum of the first-leg and between-probe travel. On test3 episodes 0–299 the grid-snap floor of the first leg averages
1.454° for every policy, so a policy that never moves between probes logs exactly that amount. Between-probe travel is
the quantity that reflects a policy's own travel decisions, and it is the one we use to characterise the regimes.

**Probe-matched budgets and the two cells.** The budget $\tau$ is calibrated (rule Cal′) so that G\* executes $n^\*$
probes on average; for set S, $n^\* = 4$. Cal′ sets τ from the mean unbudgeted travel time of G\* over 200 calibration
episodes and then verifies that G\* executes $n^\* \pm 0.3$ probes on average under the enforced budget (calibration
episodes cal3 0–199). The two cells differ only in the price of moving:

- **S12** = (S, κ = 12, τ = 4.9, $n^\* = 4$). The mean unbudgeted travel time of G\* is 0.9388 stroke-units, and in
  the verification run G\* executes 3.96 probes on average over 200 calibration episodes. Less than one stroke-unit
  remains beyond four unit-cost probes, so any substantial move costs a probe.
- **S2** = (S, κ = 2, τ = 4.7, $n^\* = 4$). τ was set by the Cal′ rule from a mean unbudgeted travel time of 0.7257
  stroke-units for G\* over the calibration episodes, and a move across the circle costs at most 2 stroke-units. The
  Cal′ probe-count verification for S2 is pending: [PENDING:v4:cal_verify_S_k2]. As an observation, not a gate
  result, G\* executes 3.873 probes on average on S2 test3 episodes 0–299.

The H3 row at κ = 2 was measured with exactly this configuration (set S, κ = 2, τ = 4.7, $n^\* = 4$), so it is the S2
cell's headroom evidence.

**Metrics.** From the evaluator's posterior after the last probe, the identity estimate $\hat k$ is the maximum-mass
identity and the pose estimate is refined locally. Success requires the correct identity, a position error below
5 mm and an orientation error below 5° modulo $G_{k_0}$. With $B(s_0)$ the success ball around the true state, the
ball information is

$$\mathrm{BI}(h) = \log \hat P(B(s_0) \mid h) - \log P(B(s_0)) \quad \text{[nats]}.$$

BI is the shared information target of every information-based method below. It is also the more stable of the two
evaluation metrics: success is a thresholded event that depends on whether posterior mass near the ball boundary falls
inside or outside it, whereas BI changes smoothly with that mass. For this reason BI is the primary metric wherever a
success contrast is within the evaluator's resolution (Section 4).

### 3.2 Cost-aware greedy planner G\*

G\* maintains an online particle filter $b = \{s_n, w_n\}_{n=1}^{N}$ and selects

$$G^\*(b) = \arg\max_{a \in \mathcal{F}(\tau_{\mathrm{rem}})} \frac{\mathrm{EIG}_B(a; b)}{c(a)},$$

where the ball EIG, the expected one-step increment of $\log P(B(s_0)\mid h)$, is estimated by nested Monte Carlo with
$j_m \sim w$ and $y_m \sim p_\varepsilon(\cdot \mid s_{j_m}, a)$:

$$\mathrm{EIG}_B(a;b) = \frac{1}{M}\sum_{m=1}^{M}\Big[\log\!\!\sum_{n \in B(s_{j_m})}\!\! w_n\, p_\varepsilon(y_m \mid s_n,a)
- \log\!\!\sum_{n \in B(s_{j_m})}\!\! w_n - \log \sum_n w_n\, p_\varepsilon(y_m \mid s_n, a)\Big].$$

Full size is $(N, C, M) = (2{,}000, 512, 64)$ particles, candidates and outcome samples. At each decision G\* exports
the score vector $s(a) = \max(0, \mathrm{EIG}_B(a;b))/c(a)$ over feasible actions (zero elsewhere), whose argmax is
G\*'s action; this vector is the distillation target. Reduced-size configurations are named gN_C_M; two of them,
g125_512_16 and g500_512_4, keep all 512 candidates and are used in the exploratory cost comparison (E5).
**Complexity.** Per decision, G\* evaluates $O(MNC)$ likelihoods and builds ball-neighbour lists in $O(N^2)$, on top of
the particle-filter assimilation of the last observation. The assimilation and neighbour-list terms do not depend on
$C$, which is why pruning candidates alone bounds the achievable speed-up (Section 5.6). Because the ratio of
information to cost is evaluated per action, a move is chosen only when the information it buys outweighs its extra
travel cost; at κ = 12 this makes staying and varying the approach offset the typical choice, and at κ = 2 it does not.

### 3.3 One-step look-ahead headroom estimator

For a belief $b$ reached by G\*, let $V_{G^\*}(b)$ be the expected ball information gained over the remaining budget
by following a greedy completion, and $V_{LA}(b)$ the value of the best screened first action followed by the same
completion. The headroom is the ratio of means over a bank of beliefs,

$$G(\kappa) = \frac{\overline{V}_{LA} - \overline{V}_{G^\*}}{\overline{V}_{LA}}.$$

The estimator screens 32 first actions with common random numbers: G\*'s own action, three structured set-up moves,
and random feasible actions, out of up to 512 feasible ones; it then re-estimates the best few together with G\*'s
action with more samples. Rollouts are completed by a **reduced greedy** (fewer particles resampled from G\*'s filter,
a candidate subset and fewer outcome samples, cost-aware and feasibility-restricted). G(κ) is therefore
one-step-deviation headroom over a reduced greedy completion, restricted to the screened first actions; it is not the
gap to the optimal policy and makes no success claim. Because $V_{LA}$ is a maximum over noisy estimates that always
include G\*'s action, the per-belief gap cannot be negative and $V_{LA}$ can carry an upward selection bias that was
not measured; no bias-corrected G is reported. Because most screened candidates are random rather than structured,
a structured multi-step plan (for example, travel to a new angle and then fan the approach offset) is represented only
through the three set-up moves and the greedy completion that follows them.

Hold requires instrument checks: (a) an abstract notch problem with a known exact relative gap, (c) a travel-notch
that places the same problem on the circle (so (a) and (c) are one construction checked twice, both re-used from the
previous design iteration), and (b) a bank of 100 beliefs with exact gap 0, which tests false positives. A bias check
compares the estimator's $V_{G^\*}$ with an independent full-G\* rollout on 20 beliefs; a ratio above 1.02 would make
Hold unavailable. The guard is one-sided and the reference differs from the estimator in both policy and filter
implementation.

### 3.4 One shared head, two learners

**Head.** Both learners use the same belief-free DeepSets head. Each touch in the history is encoded in the finger
frame (contact indicator, contact point, normal and the action that produced it), summed, and concatenated with a
context of a relative angle (cosine, sine), the remaining-budget fraction $\tau_{\mathrm{rem}}/\tau$ and the absolute
finger angle $\phi_t$ (cosine, sine). The head outputs 512 relative logits, masked to $-\infty$ outside
$\mathcal{F}(\tau_{\mathrm{rem}})$. Architecture, input and action set are the controlled variables; the training
signal differs. **Complexity.** Re-encoding the history at each decision costs $O(T^2H^2 + THA)$ for $T$ touches,
hidden width $H$ and $A = 512$, with no particle filter in the loop.

**Distillation.** The student $\pi_\theta$ minimises a soft cross-entropy to tempered teacher scores plus a hard term
on the teacher's argmax,

$$\mathcal{L}(\theta) = -\sum_{a \in \mathcal{F}} q(a)\log \pi_\theta(a \mid h) - \lambda \log \pi_\theta(a^\* \mid h),
\qquad q = \mathrm{softmax}\big(\beta_T\, s(a)/\sigma_s\big)_{a \in \mathcal{F}},$$

with $\sigma_s$ the per-decision standard deviation of $s$ over feasible actions and $a^\* = \arg\max_a s(a)$.
Held-out quality is the floored normalised regret

$$r = \frac{s_{\max} - s(a_\pi)}{\max(s_{\max} - s_{\mathrm{med}},\ \rho\, s_{\max})}, \qquad \rho = 0.05,$$

whose mean $\bar R$ drives model selection and, in S12, the stopping rule. No success-based selection is used.
Mini-batches are specified in decisions: a batch of 256 corresponds to $\lfloor 256/T \rfloor$ episodes per gradient
step, i.e. 64 episodes at $T = 4$ (derived), with all decisions of an episode kept together.

> **Algorithm 1 (DAgger distillation of G\*).**
> 1. Round 0: roll out G\* on label episodes, storing $(h, \phi_t, \tau_{\mathrm{rem}}, \mathcal{F}, s, a^\*)$ at every
>    decision; hold out a fixed episode block for $\bar R$; train $\pi_\theta$ on $\mathcal{L}$.
> 2. For rounds $r = 1, 2$ with mixing $\beta_{\mathrm{DAgger}} \in \{0.5, 0\}$: roll out episodes executing G\*'s
>    action with probability $\beta_{\mathrm{DAgger}}$ and $\pi_\theta$'s otherwise; run G\*'s filter alongside, label
>    every visited belief with $s$, aggregate, and continue training.
> 3. **S12 recipe:** stop each round when held-out $\bar R$ stops improving (registered rule); keep the last checkpoint;
>    if gate D3 fails, apply the registered remedy once (double round 0 and both DAgger rounds) and retrain. An
>    exploratory post-freeze student retrains on the remedied data for a fixed 200 epochs.
> 4. **S2 recipe:** remedy-sized data, the S12 hyperparameter configuration reused without a new grid (a stated
>    deviation), a fixed 200 epochs per round, last checkpoint, seeds 601–603.

In S2 this gives 2,700 training episodes and 10,499 training decisions at round 0, and 4,300 episodes and
16,729–16,793 decisions after round 2, per seed.

**RL (PPO).** The RL policy uses the same head and action set and is trained with PPO-clip \cite{schulman2017proximal}
(clip 0.2, 4 epochs per update) with a critic baseline. Its reward is the increment of ball-sPCE, a contrastive
estimate of ball information in the style of \cite{foster2021deep}: with $L$ contrastive states $s_{1:L} \sim p$ and
$J$ states $s_0^{(j)}$ drawn uniformly in $B(s_0)$,

$$g_t = \log \hat p_B(h_t \mid s_0) - \log\Big[\tfrac{1}{L+1}\Big(\hat p_B(h_t \mid s_0) + \sum_{l=1}^{L} p(h_t \mid
s_l)\Big)\Big], \qquad \hat p_B(h \mid s_0) = \tfrac{1}{J}\sum_j p(h \mid s_0^{(j)}),$$

and $r_t = g_t - g_{t-1}$. The return telescopes to $g_T$, capped at $\log(L+1)$ = 8.318 nats, so $g_T$ is RL's own
objective. Each seed trains for 200,064 episodes with the configuration selected in S12 (config 2); a plateau rule is
recorded but not used to stop. S12 uses seeds 511–513 and S2 seeds 611–613. The reward contains no explicit term for
the number of probes or for travel; both enter only through the budget, which ends the episode when no action is
feasible.

**Design rationale.** Holding the head fixed makes the comparison one of training signal: DAgger receives a dense
512-way label at every visited belief and needs no exploration or credit assignment, while PPO sees only the
telescoped contrastive return. A belief-input control (S12 only) replaces the history encoder with a summary of G\*'s
particle filter.

### 3.5 Baselines

Random selects uniformly among feasible actions. Three heuristics reserve budget for the remaining probes:
**B-spread** (belief-free) maximises angular distance to previous probe angles; **B-fan** (belief-free,
travel-nearest) stays at $\phi_t$ when allowed and cycles the approach offset, otherwise moving to the nearest allowed
angle; **B-cov** (belief-using) maximises coverage under an online filter. The best heuristic on pilot data, H★, was
frozen before test; for S12 it is B-fan. B-fan encodes "stay where you are and vary the approach offset" without a
belief, so it is the natural reference for a stay-and-probe regime and a stress test for a travelling one. In S2 only
B-fan was run, as the S12 H★ carried over; no S2 pilot selected an S2 H★, and B-spread and B-cov were not run there.

## 4 Experiments

**Pre-registration and routing.** Hypotheses, thresholds, the outcome map and a list of analyses not allowed after the
run were frozen before any S12 run, and the main-run set was frozen before any test episode. Three hypotheses were
registered: H1, a distilled student non-inferior to G\* (with a fallback H1-fb in which the student prunes G\*'s
candidates); H2, distillation beating RL on RL's own objective; and H3, small one-step headroom. The S12 record
reached row 4 (characterisation): D3 failed on the first attempt and after its one remedy, so H1 was never tested on
test, and H1-fb was withdrawn at the latency gate. An amendment written before any S2 run added the S2 cell with three
fixed readings: the learnability gate D4 (same rule as D3), H2-S2 (same rule as H2), and an exploratory
reduced-planner comparison E5 on S12; it allowed no remedy round. The amendment changes no S12 verdict. Refine cycles
for this study are exhausted, so the requests for further experiments that this record raises are listed in Section 7
rather than answered with new claims.

**Splits.** Disjoint episode streams: calibration (200 episodes per configuration), pilot3 (margins and H★), val3
episodes 0–499 (D3, D4), test3 episodes 0–499 ($g_T$ for H2 and H2-S2, S12 behaviour) and test3 episodes 0–299
(success and BI rows, S2 behaviour, the travel split, E5). Within a split, all methods run on the same episodes with
the same initial state, start angle and observation stream (paired design). S2 success, BI and travel numbers are on
test3 0–299; S12 logged-travel numbers in the behaviour log are on test3 0–499 (B-fan: 0–299), and the split into
first-leg and between-probe travel is on test3 0–299 for both cells. H3 uses 100 G\*-reached beliefs per κ.

**Test-split reuse.** test3 episodes 0–299 were scored first for the pre-registered S12 rows. They were later reused for
the exploratory long student, the exploratory B-fan rows, all S2 test rows and E5. The split is therefore no longer
untouched, and every claim that rests only on these later rows (in particular the S2 student versus B-fan separation)
is exploratory.

**Evaluator.** Success and BI are read from an adaptive grid posterior that rebuilds each history exactly. Its gate E′
compared grid subdivision 4 with 8 on 16 episodes and failed: one counted success flip occurred (mean |ΔBI| 0.0126
nats, maximum 0.0523). Subdivision 8 is therefore used for every reported success and BI number. Between subdivisions 4
and 8 the success outcome flips on 7.5 % of 200 set-S calibration episodes (mean |ΔBI| 0.0060 nats on the same
episodes), and no finer grid was checked. $g_T$, H3, latency and label fit do not use the grid.

**Reading rule: BI first.** Because a per-episode success flip rate of 7.5 % between two grid resolutions is of the same
order as many success contrasts, we read any success contrast whose magnitude is below 7.5 pp as within the
evaluator's resolution. For such contrasts BI is the primary metric and success is reported second. The rule is
conservative (flips between resolutions need not all move in one direction), it was fixed in this revision rather than
pre-registered, and it changes no gate verdict; the D3/D4 gates keep their registered success and BI clauses.

**Scoring pipelines.** Two code paths produce success and BI. In S2, the val3 episodes for D4 were scored inline by the
evaluation runner (eval3) at subdivision 8, whereas every S2 test3 row is a re-read (regrid3) of runs that were first
executed without the grid, and the test3 rows were produced on more than one machine. This val/test asymmetry is a
candidate cause of the S2 validation/test discrepancy reported in Section 5.3. The same two paths were also used for
S12, where the remedied student's validation and test deficits agree (−4.40 pp and −4.4 pp), which makes the
asymmetry an unlikely but untested cause. A report-only check re-reads val3 episodes 0–49 through the test pipeline:
[PENDING:v4:pipe_check].

**Methods notes.** Three properties of the instruments matter for reading the results, and we record them here rather
than as contributions. (i) The evaluator has a finite resolution, as above. (ii) The contrastive return $g_T$ and the
grid posterior do not order the policies in the same way (Section 5.4); $g_T$ is RL's objective by construction and
is reported for H2 and H2-S2, but it is not used as a localization metric. (iii) In S2 the student's deficit to G\* on
test3 is larger than on val3 for every seed (Section 5.3); its cause is untested and the pipeline check above is
pending.

**Statistics.** Paired differences use a crossed episode × seed bootstrap with B = 10,000. H2 bounds are the 5 % / 95 %
quantiles (one-sided 95 %); ci95 contrasts are the 2.5 % / 97.5 % quantiles (two-sided); the D3/D4 standard error is
the SD of an episode × student-seed bootstrap. There is no multiplicity correction. The S2 test rows and E5 are
descriptive and exploratory. With three seeds per learner, the seed dimension of the bootstrap is coarse. Where we add
a post-hoc sensitivity figure for H2 or the D gates, it is computed from the reported bounds and standard errors under
a normal approximation, labelled post hoc and derived, and used only to describe what the tests could detect.

**Gates D3 and D4.** On 500 paired val3 episodes with three student seeds, the gate passes iff (i)
$\hat\Delta_{\mathrm{succ}} \ge \max(-2\,\mathrm{pp},\ -\delta + 1.645\,\mathrm{SE}\sqrt{0.5})$; (ii) the same for BI
with ε and a −0.15-nat floor; (iii) every seed's $\hat\Delta_{\mathrm{succ}} > -\delta$. Here δ = 0.04 (the cap). S2 has
no pilot margin cell, so δ is borrowed from S12 and only the −0.15 BI floor applies. Because the margin in (i) adds
$1.645\,\mathrm{SE}\sqrt{0.5}$ to −δ, the threshold becomes stricter as the paired standard error grows.

**H2 and H3 rules.** H2 (and H2-S2) passes iff the one-sided 95 % lower bound of $g_T(\text{student}) - g_T(\text{RL})$
on test3 0–499 exceeds +0.10 nats; otherwise the advantage is "not detected". H3 is Hold iff the one-sided 95 % UB of
G(12) is below 0.03, Kill iff the lower bound exceeds 0.05, otherwise Inconclusive. A near-identical estimate from the
previous design iteration was known when the 0.03 threshold was registered, so H3 is a pre-registered replication on
the 64 × 8 action set.

**Behaviour diagnostics (report-only).** Per episode we log total finger travel (logged travel, Section 3.1), its split
into the first leg and between-probe travel together with the grid-snap floor, the number of probes, the fraction of
between-probe moves that are zero or exceed one grid step, whether $g_T$ reached its cap, and in S2 the per-seed
Pearson correlation of the student's and G\*'s per-episode travel and the number of episodes with identical action
sequences.

**Implementation.** Everything is numpy with hand-written backpropagation and single-threaded BLAS, run on
GitHub-hosted standard runners (CPU model not logged); distillation training ran in a separate sandbox runtime.
Latency follows a fixed protocol (Lat′): configurations timed interleaved on the same S12 pilot decision states with
one thread, 1,000 decisions on 253 pilot episodes from two runner jobs. E5 latencies are medians of per-decision
latencies logged during the eval3 runs on free runners, not Lat′ measurements; where Lat′ also timed the same
configuration, we report both.

**Table 1. Settings (design constants; RL configuration from the S12 sweep).**

| Component | Setting |
|---|---|
| G\* | N = 2,000 particles, C = 512 candidates, M = 64 outcome samples |
| E5 reduced G\* | g125_512_16 (N = 125, C = 512, M = 16); g500_512_4 (N = 500, C = 512, M = 4) |
| Distillation loss | Adam, lr 1e-3, β_T = 4, λ = 0.5, batch 256 decisions-equivalent (⌊256/T⌋ episodes per step, 64 at T = 4); ρ = 0.05 in $\bar R$ |
| DAgger | 2 rounds, β_DAgger = 0.5 then 0; S12: registered stopping rule, one remedy; S2: remedy-sized data, 200 epochs per round |
| Student seeds | S12: 501–503 (belief-input control 521–523); S2: 601–603 |
| PPO | clip 0.2, 4 epochs per update, critic baseline; 200,064 episodes per seed; S12 seeds 511–513, S2 seeds 611–613 |
| PPO sweep (S12) | 4 configurations, 1 seed, 50,048 episodes each; selected config 2: lr 1.09e-3, entropy 1.33e-4, batch 128, critic lr 1.43e-3; selected on the trainer's validation stream (val_v2) |
| ball-sPCE | L = 4095 contrastive states, J = 16 ball states; cap log(L+1) = 8.318 nats |
| H3 estimator | 32 screened first actions, common random numbers, reduced greedy completion; 100 beliefs per κ |
| Evaluator | adaptive grid posterior, subdivision 8 |
| Statistics | crossed episode × seed bootstrap, B = 10,000; δ = 0.04; BI floor −0.15 nats; H2 margin +0.10 nats; H3 threshold 0.03 |

**Table 2. Pre-registered gates and decisions.**

| Row | Item | Measured | Rule | Outcome |
|---|---|---|---|---|
| R1 | Cal′ budgets | S12 τ = 4.9 (G\* 3.96 probes over 200 calibration episodes); S2 τ = 4.7, verification [PENDING:v4:cal_verify_S_k2] | G\* mean executed probes on cal3 0–199 within 4 ± 0.3 | S12 pass; S2: τ set by the Cal′ rule; verification pending |
| R2 | E′ evaluator | mean \|ΔBI\| 0.0126 nats; 1 counted flip | no counted flip | fail → sub 8 |
| R3 | G5′ S12 pilot | G\* 0.426 (n = 500), random 0.075 (n = 200); D_c 0.351; H★ B-fan | G\* ≥ random + 10 pp | pass |
| R4 | Lat′ / H1-fb | full G\* / pruned-16 = 3.22 | ≥ 10 | H1-fb withdrawn |
| R5a | D3 S12, first attempt | Δ̂_succ −5.87 pp (thr −1.43); Δ̂_BI −0.199 (thr −0.15); seeds −4.2 / −8.0 / −5.4 pp | (i)–(iii) | fail |
| R5b | D3 S12, remedy | −4.40 pp (thr −1.68) ✗; −0.096 ✓; seeds −4.6 / −4.6 / −4.0 pp ✗ | (i)–(iii) | fail → H1 dead |
| R5c | D3-B belief input (300 episodes) | −20.1 pp (thr −0.75); −1.02 nats; seeds −21.7 / −17.3 / −21.3 pp | as D3 (report-only) | fail |
| R5d | D4 S2 | −2.80 pp (thr −1.46) ✗; −0.105 ✓; seeds −3.6 / −2.8 / −2.0 pp ✓ | (i)–(iii) | fail |
| R6 | H2 S12 | Δg_T +0.0002 nats, LB −0.3103 | LB > +0.10 | not detected |
| R6b | H2-S2 | Δg_T −0.4452 nats, LB −0.7485, UB −0.1616 | LB > +0.10 | not detected |
| R7 | H3 | UB95 G(12) = 0.0221; bias ratio 0.957 | UB < 0.03; ratio ≤ 1.02 | Hold |
| R8 | S2 val3 0–49 re-read through the test pipeline (report-only) | [PENDING:v4:pipe_check] | report-only | pending |

All D4, test3, H2 and E5 blocks are complete. The S2 test3 random anchor is not yet complete
([PENDING:v4:14_s2_analysis.test3_sub8.rows.random]), so it enters no contrast. The S2 Cal′ verification (R1) and the
pipeline check (R8) are report-only diagnostics; neither can change a registered verdict.

## 5 Results

### 5.1 H3: one-step look-ahead headroom is small among the screened actions

H3 is **Hold**. At κ = 12, one-step rollout over the reduced greedy completion gains at most 2.2 % of the remaining
expected ball information over the 32 screened first actions (G(12) = 0.01624, one-sided 95 % UB 0.0221 < 0.03). In
absolute terms the gap is 0.0414 nats on a mean $V_{G^\*}$ of 2.506 nats (Table 3). The κ = 2 row was measured in the
S2 cell configuration and is the headroom evidence nearest to the travelling regime: G(2) = 0.01418 (UB 0.01974), a
gap of 0.0371 nats on a mean $V_{G^\*}$ of 2.580 nats; it is reported, not a separate test. The point estimates follow
the ordering G(0) ≤ G(2) ≤ G(12), which was not tested, and even the largest is small. The look-ahead picks a different
first action from G\* on 62 % of beliefs at κ = 12 (54 % at κ = 2) yet gains little on average, which is consistent
with near-ties among the top actions; the record does not separate near-ties from selection noise. The result
replicates the previous design iteration's estimate on a coarser action set.

**Table 3. Headroom over G\* (set S, 100 beliefs per κ).**

| κ | G | LB95 | UB95 | gap (nats) | mean $V_{LA}$ | mean $V_{G^\*}$ | frac LA ≠ G\* | no budget left |
|---|---|---|---|---|---|---|---|---|
| 0 | 0.006374 | 0.004028 | 0.009401 | 0.01795 | 2.816 | 2.798 | 0.58 | 0 |
| 2 (S2 cell) | 0.01418 | 0.009616 | 0.01974 | 0.03712 | 2.617 | 2.580 | 0.54 | 4 |
| 12 (S12) | 0.01624 | 0.01148 | 0.02210 | 0.04137 | 2.548 | 2.506 | 0.62 | 1 |

All instrument checks passed: the notch construction gives a mean relative gap of 0.8290 (band [0.573, 0.860]); its
travel-notch form gives 0.7438 against the exact 0.7166 shared by both forms; the zero-gap bank gives 0.00254 (UB
0.00374). The notch readings over-read the exact gap, in line with the upward selection bias of $V_{LA}$. On bias, the
estimator's $V_{G^\*}$ reads 1.940 nats against 2.026 for the independent full-G\* rollout on 20 beliefs (ratio 0.957,
inside the guard), so Hold is not downgraded; this direction alone would inflate G, and whether $V_{LA}$ is
under-read by more was not checked. These results are consistent with greedy-competitiveness arguments
\cite{javdani2012efficient, chen2015submodular} carrying over at the tested budgets, for one deviating step among the
screened candidates; they say nothing direct about deeper planning.

### 5.2 Two regimes: what the planner does

Table 4 establishes the regimes before any learning result, and it reports two travel measures (Section 3.1): logged
travel, which includes the unavoidable first-leg snap onto the action grid, and between-probe travel, which reflects
only the policy's own choices. On test3 0–299 the snap floor averages 1.454° per episode for every policy; this is the
whole of B-fan's logged travel (1.454° in both cells), because B-fan never moves between probes.

In S12, G\* moves the finger 4.3° per episode between probes on test3 0–299 (logged 5.7° on the same episodes, and
6.1° on test3 0–499 in the behaviour log); 79.3 % of its between-probe moves are zero and it executes 3.962 probes
(0–499). Removing the snap therefore makes the stay-and-probe character of S12 slightly stronger than the logged figure
suggests. In S2, G\* moves 44.8° between probes (logged 46.9°) and executes 3.873 probes. Its first leg is only the grid
snap in 74 % of S2 episodes, against 94 % in S12, so in S2 G\* also chooses to move away from the start angle on its
first decision in about a quarter of episodes (26 %, derived as 1 − 0.74). RL ends at exactly 3 probes in both cells;
it moves 108.8° between probes in S2 and 16.8° in S12 (seeds pooled, test3 0–299), and its first leg is never only the
snap in S2. Random moves 82.4° between probes in S2 and 8.0° in S12, with most of its travel in its first leg.

**Table 4. Behaviour (report-only). Logged travel includes the first-leg grid snap (floor 1.454° on test3 0–299);
between-probe travel excludes the first leg. S12 logged travel, probes and zero moves: test3 0–499 (B-fan 0–299), per
seed for learners; S12 between-probe travel: test3 0–299, learner seeds pooled; S2: test3 0–299, learner seeds pooled.**

| Policy | S12 logged travel (°) | S12 between-probe (°) | S12 probes | S12 zero moves | S2 logged travel (°) | S2 between-probe (°) | S2 probes |
|---|---|---|---|---|---|---|---|
| G\* | 6.13 (0–299: 5.75) | 4.26 | 3.962 | 79.3 % | 46.91 | 44.79 | 3.873 |
| Student (3 seeds) | 1.52 / 2.05 / 1.88 (0–299 pooled: 1.77) | 0.31 | 4.0 | 97.7–99.7 % | 39.14 | 37.66 | 3.926 |
| RL (3 seeds) | 23.02 / 25.76 / 25.65 (0–299 pooled: 24.80) | 16.82 | 3.0 | 0.0–21.9 % | 136.8 | 108.75 | 3.0 |
| B-fan | 1.454 | 0.0 | 4.0 | 100 % | 1.454 | 0.0 | 4.0 |
| Random | 38.45 (0–299: 38.99) | 7.99 | 1.946 | 33.0 % | 172.2 | 82.37 | 2.367 |

In S2 the student moves a similar amount to G\* on average (37.7° vs 44.8° between probes, test3 0–299; 39.1° vs
46.9° logged), unlike S12 (0.3° vs 4.3° between probes), but its per-episode travel is only weakly correlated with
G\*'s (r 0.14–0.24 by seed: 0.162, 0.238, 0.141), and none of its 300 episodes per seed reproduces G\*'s action
sequence. S2 therefore shows that the student is not confined to stay-and-probe, not that it reproduces G\*'s travel
decisions.

### 5.3 Learnability against G\* in both regimes

**S12 (D3).** On 500 paired val3 episodes, the first-attempt students reached Δ̂_BI = −0.199 nats against a threshold
of −0.15 and Δ̂_succ = −5.87 pp against a threshold of −1.43 pp. After the remedy, BI was −0.096 (pass), success was
−4.40 pp against −1.68 pp (fail) and per-seed success −4.6 / −4.6 / −4.0 pp (fail), so H1 is dead. On test3 0–299 the
remedied student trails G\* by 0.049 nats BI (ci95 [−0.114, +0.019]) and by 4.4 pp success (ci90 [−8.6, −0.3], ci95
[−9.3, +0.6]); the success contrast is within the evaluator's resolution, and neither ci95 excludes 0. An exploratory,
post-freeze student trained for 200 epochs on the remedied data was not shown to differ from G\* on test3 (BI −0.008,
ci95 [−0.083, +0.066]; success −1.7 pp, ci95 [−6.8, +3.4]; long − remedied BI +0.041, ci95 [−0.016, +0.098], success
+2.8 pp, ci95 [−1.0, +6.7]), so in S12 the optimisation budget is left open as an explanation.

**S2 (D4).** The S2 student failed D4: on val3 the success deficit was −2.80 pp against a threshold of −1.46 pp, while
the BI clause (−0.105 nats, SE 0.039, against the −0.15 floor) and the per-seed clause passed. The val3 means are 0.486
(student) and 0.514 (G\*) for success and 6.563 and 6.667 nats for BI. On test3 0–299 the student trails G\* by 0.183
nats BI (ci95 [−0.269, −0.094]) and by 10.2 pp success (ci95 [−16.6, −4.3]); both intervals exclude 0, and the success
gap exceeds the evaluator's resolution. The test gap is wider than the val3 gap for every seed (by 5.4, 11.2 and
5.7 pp); both the G\* row (+3.9 pp from val3 to test3) and the student row (−3.5 pp) move, and the difference is ≈ 2.0
combined SE under independence (conservative given shared students). Its cause is untested: the val3 rows were scored
inline and the test3 rows by a re-read on more than one machine (Section 4), and the pipeline check is pending
([PENDING:v4:pipe_check]). No interval was computed for the val3 BI deficit beyond its SE. The S2 recipe already was
the budget-matched 200-epoch recipe, so the optimisation-budget explanation left open in S12 does not account for the
S2 result in the same way.

**Post-hoc sensitivity of the D gates (derived, not pre-registered).** Taking the observed SE as fixed, clause (i)
passes with 80 % probability only if the true success difference is at least the threshold plus 0.842 SE: about
+0.4 pp for D4 (−1.46 pp + 0.842 × 2.18 pp) and about 0.0 pp for the remedied D3 (−1.68 pp + 0.842 × 1.99 pp). The
success clause therefore demanded near-parity with G\* rather than tolerating a deficit of a few points. The BI clause
of D4 is looser in the same sense (−0.150 + 0.842 × 0.039 ≈ −0.12 nats), which is consistent with its passing.

**S2 training record.** Every S2 round ran to its 200-epoch cap. Held-out $\bar R$ did not improve over DAgger: it was
0.300–0.312 after round 0 and 0.298–0.322 after round 2 across the three seeds. Training $\bar R$ was not logged in S2,
so the S12 label-fit rule cannot be applied there, and under-fitting in S2 cannot be ruled out from the record.

**S12 label fit and belief input.** All six S12 history students fit their training labels by the registered rule
(train top-1 0.511–0.534, train $\bar R$ 0.169–0.206; under-fit requires $\bar R$ > 0.25 or top-1 < 0.50), which
assigns the deficit to generalisation rather than capacity; support for that reading is weak, because held-out top-1
(0.483–0.507) sits close to train top-1, which an under-optimised model would also show. The belief-input students are
under-fit (train top-1 0.327–0.362) and fail every D3 criterion (Δ̂_BI −1.02 nats, Δ̂_succ −20.1 pp), so that control
isolates nothing about the representation; whether a belief input would close the gap remains open.

### 5.4 Distillation against RL on RL's own objective

**S12 (H2).** The student reaches $g_T$ = 5.368 nats and RL 5.368; Δ = +0.0002 nats with one-sided 95 % bounds
[−0.3103, +0.3034]. H2 is not detected (LB −0.3103 ≤ +0.10). No equivalence test was registered or run, so the result
is not evidence that the two are equal.

**S2 (H2-S2).** H2-S2 is not detected (LB −0.749 ≤ +0.10). The crossed-bootstrap point estimate favours RL by 0.445
nats on $g_T$ (one-sided 95 % UB of student − RL −0.162, bootstrap p 0.0064, not pre-registered). The LB (−0.749) is
0.85 nats below the threshold, about 2.8 lower one-sided half-widths (0.303), so the non-detection is not near the
margin. Every S2 RL seed (5.832–6.179) is above every S2 student seed (5.450–5.612) on $g_T$.

**Post-hoc sensitivity of H2 (derived, not pre-registered).** In S12 the lower one-sided half-width is 0.311 nats
(+0.0002 − (−0.3103)), so a point estimate above about 0.41 nats would have been needed for the LB to clear +0.10, and
under a normal approximation (SE ≈ 0.311/1.645 = 0.189) a true advantage of about 0.57 nats would have been needed for
an 80 % chance of passing. In S2 the corresponding figures are 0.40 nats (0.10 + 0.303) and about 0.56 nats. Both
tests could therefore detect only advantages of roughly half a nat.

**Success and BI (Table 5).** On BI, the student leads RL by +0.289 nats (ci95 [+0.117, +0.465]) in S12 and +0.180
nats (ci95 [+0.091, +0.273]) in S2; on success, student − RL is +2.6 pp (ci95 [−3.7, +8.8]) in S12 and +2.8 pp (ci95
[−4.1, +9.6]) in S2, both within the evaluator's resolution. G\* − RL is +0.338 nats BI (ci95 [+0.158, +0.520]) and
+7.0 pp success (ci95 [+0.2, +13.7]) in S12, and +0.363 nats BI (ci95 [+0.263, +0.467]) and +13.0 pp success (ci95
[+6.4, +19.4]) in S2. RL ends at 3 probes and travels several times G\*'s distance in both cells (logged travel 2.9×
in S2 and about 4× in S12), so the record does not identify why the success gap differs between cells, and no
cross-cell test of it exists.

**The RL policies.** All six PPO policies converge to exactly 3 probes per episode, and the three S12 policies end
training with near-zero entropy (0.002–0.013). Their between-probe travel is 108.8° in S2 and 16.8° in S12. The
contrastive reward contains no term that ties the number of probes to the budget, and these policies travel more and
probe less than G\* in both cells. We read this as a property of this RL setup (one configuration, selected
in S12 and not re-tuned for S2) rather than of RL in general; H2 and H2-S2 compare against this setup only.

**Instrument ordering.** On seed-averaged point estimates $g_T$(G\*) is below both learned policies in S2 (5.40 vs
5.53 / 5.98) and marginally in S12 (5.30 vs 5.37, with 3 of 6 S12 learner seeds below G\*); every S2 learner seed is
above 5.397; no interval exists for these contrasts. The grid posterior orders G\* above both learners in both cells,
and the student above RL on BI. In S12, cap saturation of $g_T$ is rare (5.8 % of G\* episodes, 0.4–3.4 % for the
learners) and ordered like BI, so the cap alone is unlikely to explain the inversion. We record this as a methods
observation, not a mechanism.

**Table 5. Test rows. Success and BI on test3 0–299 (sub-8 grid); $g_T$ on test3 0–499. S12 rows are from the S12
study, S2 rows from the v4 amendment; no cross-cell test.**

| Method | S12 success | S12 BI | S12 $g_T$ | S2 success | S2 BI | S2 $g_T$ |
|---|---|---|---|---|---|---|
| G\* | 0.4267 | 6.248 | 5.299 | 0.5533 | 6.673 | 5.397 |
| Student (per-seed success) | 0.3822 (0.3833 / 0.3767 / 0.3867) | 6.200 | 5.368 | 0.4511 (0.4633 / 0.4133 / 0.4767) | 6.490 | 5.534 |
| RL (per-seed success) | 0.3567 (0.3667 / 0.3900 / 0.3133) | 5.910 | 5.368 | 0.4233 (0.3967 / 0.4200 / 0.4533) | 6.310 | 5.979 |
| B-fan (exploratory) | 0.36 | 5.973 | — | 0.37 | 5.962 | 5.263 |
| Random | — | — | 2.618 | [PENDING:v4:14_s2_analysis.test3_sub8.rows.random] | [PENDING:v4:14_s2_analysis.test3_sub8.rows.random] | 3.510 |

| Paired contrast (ci95) | S12 success | S12 BI | S2 success | S2 BI |
|---|---|---|---|---|
| student − G\* | −0.0444 [−0.0933, +0.0056] | −0.0487 [−0.1138, +0.0190] | −0.1022 [−0.1656, −0.0433] | −0.1830 [−0.2694, −0.0944] |
| student − RL | +0.0256 [−0.0367, +0.0878] | +0.2893 [+0.1170, +0.4652] | +0.0278 [−0.0411, +0.0956] | +0.1797 [+0.0908, +0.2732] |
| G\* − RL | +0.0700 [+0.0022, +0.1367] | +0.3380 [+0.1585, +0.5196] | +0.1300 [+0.0644, +0.1944] | +0.3628 [+0.2634, +0.4672] |
| student − B-fan | +0.0222 [−0.0278, +0.0733] | +0.2263 [+0.1412, +0.3110] | +0.0811 [+0.0167, +0.1467] | +0.5281 [+0.4202, +0.6371] |
| B-fan − G\* | −0.0667 [−0.12, −0.01] | −0.2750 [−0.3665, −0.1843] | −0.1833 [−0.2467, −0.12] | −0.7112 [−0.8299, −0.5936] |
| RL − B-fan | −0.0033 [−0.0689, +0.0633] | −0.0630 [−0.2465, +0.1199] | not computed | not computed |

**Seed variability and RL training.** In S12 the RL per-seed SD of $g_T$ is 3.29× the student's, and its test success
range is 7.7 pp against 1.0 pp. All six RL seeds ran to the 200,064-episode cap; the plateau rule fired at 102,400
episodes for every S2 seed. The S2 trainer's last-batch $g_T$ (5.989–6.340) is on training episodes and is not
comparable to the test3 rows.

### 5.5 Learned policies against the stay-and-fan heuristic (exploratory)

On S2 test3 the student exceeds B-fan on BI (+0.53 nats, ci95 [+0.42, +0.64]) and on success (+8.1 pp, ci95
[+1.7, +14.7]); the success contrast is just above the evaluator's resolution. In S12 it exceeded B-fan on BI (+0.23,
ci95 [+0.14, +0.31]) but not on success (+2.2 pp, ci95 [−2.8, +7.3]), so S2 adds a success separation; the comparison
across cells is untested. B-fan − G\* is −0.711 nats BI and −18.3 pp success in S2, against −0.275 nats and −6.7 pp in
S12. In S12, RL is not distinguishable from B-fan on either metric (BI −0.063, ci95 [−0.246, +0.120]; success −0.3 pp,
ci95 [−6.9, +6.3]); in S2 no RL − B-fan interval was computed, so it is not reported as a contrast. B-fan is the only
heuristic run in S2, and it was chosen as H★ on S12 pilot data, so the S2 separation is from the stay-and-fan heuristic,
not from the best available heuristic in the travelling regime.

### 5.6 Cost: per-decision latency and reduced planners

Per decision, the student's median latency (0.408 ms) is about 2,200× below full-size G\* (0.9135 s) under Lat′, not
compared at matched accuracy. Pruning candidates cannot recover much of G\*'s cost: the assimilation (0.0402 s) and
neighbour-list (0.0967 s) medians do not depend on the number of scored candidates, while scoring takes 0.7169 s; the
component medians do not sum to the total median, so the ceiling on pruning depends on which total it is attributed
to, but under either attribution it is below the registered 10×. Measured full / pruned-16 is 3.22, which withdrew
H1-fb.

**Table 6. E5: reduced-size G\* on S12 test3 0–299 (sub 8), paired with the S12 rows; latency is the median of
eval3-logged per-decision latencies on free runners (not Lat′).**

| Configuration | Success | BI | Probes | Latency / decision | − student (succ; BI) | − long student (succ; BI) | − G\* (succ; BI) |
|---|---|---|---|---|---|---|---|
| g125_512_16 | 0.36 | 5.969 | 3.843 | 20.8 ms | −2.2 pp [−6.9, +2.4]; −0.231 [−0.318, −0.145] | −5.0 pp [−10.1, +0.1]; −0.271 [−0.371, −0.174] | −6.7 pp [−12.0, −1.0]; −0.279 [−0.381, −0.179] |
| g500_512_4 | 0.3767 | 6.037 | 3.777 | 46.0 ms | −0.6 pp [−5.8, +4.8]; −0.162 [−0.261, −0.065] | −3.3 pp [−8.9, +2.3]; −0.203 [−0.304, −0.099] | −5.0 pp [−11.0, +1.3]; −0.211 [−0.314, −0.108] |

At logged median per-decision latencies of 20.8 and 46.0 ms (eval3, free runners), neither reduced G\* exceeds the
distilled students: both are lower on BI by 0.16–0.27 nats (ci95 exclude 0), and every success contrast with the
students is within the evaluator's resolution and unresolved. Lat′ also timed these two configurations on the S12
pilot decision states: 20.2 ms for g125_512_16 and 40.0 ms for g500_512_4 (relative CI half-widths 1.6 % and 6.2 %),
close to the eval3-logged medians; against the student's Lat′ median of 0.408 ms these are about 49× and 98× slower
(derived). On a different split (pilot3, n = 186 / 177, incomplete) the same configurations scored 0.382 / 0.390
success at 18.2 / 44.1 ms, against 0.360 / 0.377 at 20.8 / 46.0 ms here; unpaired.

## 6 Discussion

**Greedy is a defensible teacher, within the measured scope.** One-step headroom over the reduced greedy completion is
small at κ = 12, and the κ = 2 row measured in the S2 cell configuration is also small. In the sense that one deviating
step buys little among the screened first actions, the cost-aware greedy planner is a reasonable target for
amortization in both regimes. The measurement bounds one step followed by a reduced completion; it does not speak to
deeper planning. In S12 the planner moves only 4.3° between probes per episode, which leaves the travel coupling little
room to create headroom; the κ = 2 row, where the planner travels about ten times as far (44.8° vs 4.3° between probes; ratio derived), is therefore the more
relevant evidence that travel cost does not open a large one-step gap, and it too is small.

**Making the planner travel did not make it learnable to non-inferiority.** S12 left open the explanation that the
student failed because the registered stopping rule under-trained it, since the exploratory 200-epoch student was not
shown to differ from G\* on test. S2 was trained with that budget-matched recipe from the start and still failed its
gate, and on test its success deficit is larger than on validation for every seed; the pooled BI deficit also grows
(−0.183 nats on test3 against −0.105 on val3). The behavioural
record locates part of the difficulty. In S2 the student moves a G\*-like amount between probes on average, so it is
not merely a stay-and-probe policy, but its travel is only weakly correlated with G\*'s episode by episode: it travels,
but its travel tracks G\*'s only weakly. The student's held-out regret did not improve across DAgger rounds in S2, so additional
on-policy labels at this data scale did not translate into better agreement with the teacher's scores. The post-hoc
sensitivity of the gates adds a second reading: the success clause, as registered with δ = 0.04 and the observed
standard errors, could be passed reliably only by a student at parity with G\*, so these gates test near-equivalence
rather than a tolerance of a few points.

**What learning buys over no learning.** Where staying is cheap (S12), neither learner was shown to exceed the
travel-nearest stay-and-fan heuristic on success, and RL was not distinguishable from it on BI either. In S2 the student
exceeds it on both BI and success, while the heuristic falls further behind G\*. One reading is that the learned head
captures some belief-dependent structure of the planner's choices that a belief-free rule cannot, and that this
becomes visible on success only when the planner's own strategy departs from staying. We did not test this across
cells, and S2 compares against B-fan only.

**$g_T$ as a yardstick.** This is the most transferable observation of the study. The contrastive objective that RL
optimises ranks G\* below both learners in both cells, whereas the grid posterior ranks it above, and on the grid
posterior the student leads RL on BI in both cells. In S2 the point estimate on $g_T$ favours RL by 0.445 nats while
every BI contrast between the learners favours the student and every success contrast is within the evaluator's
resolution. Consequently, "no advantage on RL's own objective" carries little information about localization quality,
and H2 and H2-S2 are best read as findings about that proxy. The RL policies also show what optimising this proxy
under a budget can produce: all of them stop at three probes and travel several times as far as G\*. For amortized
design work that reports sPCE-type bounds as the quality of a learned policy, our record suggests checking the
ordering against a posterior-based metric. Semi-amortized schemes that refine a learned proposal online
\cite{hedman2025step} or keep a cheaper nested filter in the loop \cite{iqbal2024recursive} are natural next designs,
although our latency decomposition shows that the particle filter itself bounds the speed-up of any scheme that keeps
it.

**Cost.** Per decision, the learned head is orders of magnitude cheaper than full-size G\*, but at tens of
milliseconds two reduced-size planners trail the students on BI with success unresolved, and Lat′ timings of the same
two configurations agree with the logged ones. The relevant comparison for practitioners is therefore not against
full-size G\* but along a latency–accuracy frontier that is only partly mapped.

**Open questions.** Does regret measured on student-visited states confirm covariate shift? Does the S2 validation/test
discrepancy survive the pipeline check and persist with more episodes and seeds? Do the findings hold in more cells per
regime? Would a full 512-action screen, or a structured travel-then-fan candidate family, change H3? Would a
probe-count-aware RL objective or an S2-tuned RL configuration change H2-S2? Would a belief-input head that fits its
labels close the learnability gap? Where do the learners sit on a reduced-planner frontier timed under Lat′?

## 7 Limitations

The qualifiers that the body states once are collected here; each applies to every result it names.

- **One cell per regime.** All learning results come from one stay-and-probe cell (S12) and one travelling cell (S2);
  S2 borrows δ from S12 and has no pilot margin, so its gate rests on the −0.15 BI floor and a borrowed success margin.
  Regime-dependent statements (for example, that the student separates from B-fan on success only in S2) compare two
  cells without a cross-cell test and are anecdotal.
- **Low power, three seeds.** Three seeds per learner give H2 and H2-S2 power only for large effects: post hoc, about
  half a nat of true advantage would have been needed for an 80 % chance of passing. No equivalence test was run, so
  non-detection is not evidence of equality.
- **No multiplicity correction; exploratory rows.** No contrast is corrected for multiplicity, and the S2 test rows,
  B-fan rows, the long student and E5 are exploratory.
- **Evaluator not shown converged.** The evaluator gate failed and sub 8 is used without a finer (for example sub-16)
  check; success flips on 7.5 % of calibration episodes between sub 4 and sub 8, which is the order of most success
  contrasts. S2 test3 rows were produced on more than one machine and pipeline.
- **Unexplained S2 validation/test gap.** The S2 test gap is wider than the validation gap for every seed, and its
  cause is untested. The val3 rows were scored inline and the test3 rows by a re-read; the check that would rule this
  out is pending ([PENDING:v4:pipe_check]).
- **S2 calibration not verified.** The S2 budget was set by the Cal′ rule, but its probe-count verification is pending
  ([PENDING:v4:cal_verify_S_k2]); the test3 figure of 3.873 probes is an observation, not a gate result.
- **Comparators not shown tuned.** No S2 hyperparameter grid was run, and training $\bar R$ was not logged in S2, so
  under-fitting there cannot be ruled out; RL was not re-tuned for S2 (config 2 was chosen on the trainer's val_v2 stream
  and sits at the edge of the learning-rate grid), and every RL policy collapses to exactly three probes, so H2 and
  H2-S2 compare against this RL setup, not against RL in general. No probe-count-aware RL variant was run.
- **Representation question open.** The belief-input control is under-fit and isolates nothing; no larger or
  attention-based head was tried.
- **Baselines in S2.** Only B-fan, the S12 H★, was run in S2; no S2 H★ was selected, and B-spread and B-cov were not run.
- **H3 scope.** H3 covers 32 screened first actions with a reduced greedy completion, mostly random, with no full
  512-action screen and no structured two-step candidate family, and the selection bias of $V_{LA}$ was not measured.
- **Covariate shift not measured.** Regret on student-visited states was not computed.
- **Latency.** The Lat′ protocol is incomplete (several configurations exceeded the CI-width criterion, two runner jobs
  pooled), and E5 latencies are logged during evaluation on free runners, not Lat′ measurements.
- **Incomplete random anchor.** The S2 test3 random row is not yet complete
  ([PENDING:v4:14_s2_analysis.test3_sub8.rows.random]) and enters no contrast.
- **Test-split reuse.** test3 is reused by exploratory rows (the long student, B-fan, S2 rows and E5), so it is no
  longer untouched.
- **Travel definition.** Logged travel includes a first-leg grid snap that no policy chooses; the between-probe split is
  available only on test3 0–299, with learner seeds pooled.
- **Registered items not executed.** The Holm-corrected family, the TOST equivalence test, the behaviour-cloning and
  absolute-frame student rows and the reduced-planner H1 comparison were descoped because each was conditional on H1
  reaching test, which D3 prevented.
- **Simulation only.** All results are in simulation with planar objects, one shape library, a single fingertip on a
  fixed circle, Gaussian point and normal noise and no contact dynamics; no held-out shapes, 3D objects or hardware were
  tested.

## 8 Conclusion

We asked how much headroom one-step look-ahead leaves over greedy cost-aware information-gain touch selection under
travel cost, and whether that planner can be amortized by distillation or by RL on the same objective, in a
stay-and-probe regime where the planner barely moves and in a regime where it travels. Four answers follow from a
pre-registered characterisation with one cell per regime. First, one-step headroom is small: among the screened first
actions, rollout over a reduced greedy completion gains at most about 2.2 % at κ = 12, and the κ = 2 row, where the
planner moves 44.8° between probes rather than 4.3°, is also small. Second, neither learner was shown to reach the
planner in either regime with one belief-free head; in the travelling regime the distilled student moves the finger
about as much as the planner on average, but its travel is only weakly correlated with the planner's, and it trails
the planner on ball information on test. Third, no advantage of distillation over RL was detected on RL's own
objective in either regime, and that contrastive objective orders the planner and the learners differently from the
grid posterior, on which the student leads RL in both cells; we regard this disagreement as the study's most
transferable lesson for amortized active sensing. Fourth, at tens of milliseconds per decision, reduced-size planners
trail the students on ball information with success unresolved; nothing was compared at matched accuracy. Concrete
next steps are more cells and seeds per regime, regret on student-visited states, a full-action screen for the
headroom estimator, completion of the S2 calibration and pipeline checks, a resolution of the S2 validation/test
discrepancy, a probe-count-aware RL comparator, and reduced planners timed under the latency protocol alongside the
learners.
