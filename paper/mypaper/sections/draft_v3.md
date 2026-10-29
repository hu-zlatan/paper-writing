<!--
% FIGURE 1 PROMPT:
% Target model: Nano Banana 2 (image generation). Output: one wide scientific schematic figure, aspect ratio 3:1
% (full text width of a two-column robotics paper, about one third of a page tall), pure white background (#FFFFFF),
% clean flat-vector style, no photorealism, no 3D shading, no gradients, no drop shadows, no textures, no decorative
% icons beyond those listed, no people, no robot arm, no logos, no watermark. Line weights uniform (thin 1.5 px
% outlines, 2.5 px arrows). Font: a single clean sans-serif (Helvetica/Arial-like), dark grey #222222, all text
% horizontal, no text other than the exact labels quoted below, spelled exactly as given (keep Greek letters and
% symbols exactly: φ, ψ, κ, Δφ, π, *, ×). Exactly two accent colours: BLUE #1F6FB4 = information / probing, ORANGE
% #E07B1A = travel / cost. Neutral greys for objects (#9A9A9A fill, #555555 outline). The figure is divided into three
% panels side by side, left to right, separated by generous white space (no boxes around panels A and B). Each panel
% has a bold panel letter in its top-left corner: "A", "B", "C".
%
% PANEL A (left, about 30 % of the width) - "the task", top-down view:
%  1. Centre: one flat, irregular polygon (6 main sides, one small rectangular notch cut into its upper-right edge),
%     solid grey fill #9A9A9A, outline #555555, seen from directly above.
%  2. Around the polygon, a dashed thin grey square (#888888, dash pattern 4-3) slightly larger than the polygon:
%     the position-uncertainty box. No label.
%  3. Three to four faint "ghost" outlines of the same polygon and of one slightly different polygon (same size, notch
%     on a different edge), each shifted and rotated by small amounts, drawn as very light grey outlines (#CFCFCF,
%     no fill, 30 % opacity), overlapping the solid polygon: the particle belief over identity and pose. Small label
%     beneath the box: "belief over identity × pose".
%  4. A thin solid grey circle (#777777) centred on the polygon, radius about 2.2× the polygon's size: the stand-off
%     circle. No label on the circle itself.
%  5. A small filled dark dot (#222222) on the circle at about the 8 o'clock position: the current fingertip. Label
%     next to it, outside the circle: "φ_t".
%  6. A curved ORANGE arrow running along the circle clockwise from the fingertip dot (8 o'clock)
%     up over the top to about the 1 o'clock position, arrowhead at the 1 o'clock end, drawn just outside the circle
%     line so both remain visible. Label next to the arrow, outside the circle, orange text: "travel cost
%     c(a) = 1 + κ|Δφ|/π". Small open orange circle at the arrow's end marking the new angle, labelled "φ′".
%  7. From φ′, a straight BLUE arrow pointing inward toward the polygon, tilted slightly (about 15°) away from the
%     radial direction; a thin dotted grey radial reference line from φ′ to the circle centre shows the tilt, and a
%     small arc between the radial line and the blue arrow is labelled "ψ" in blue.
%  8. The blue arrow ends exactly on the polygon's edge at a small blue filled diamond (contact marker) with a short
%     blue tick perpendicular to the edge (the measured surface normal). Small blue label: "contact + normal".
%
% PANEL B (centre, about 45 % of the width) - "three ways to pick the next touch", block diagram:
%  1. At the far left of panel B, vertically centred, a small cloud of about 20 tiny grey dots inside a rounded
%     outline: the belief icon. Label below: "belief b".
%  2. From the belief icon, three thin grey arrows fan out to the right into three horizontal lanes stacked top to
%     bottom, each lane a row of rounded rectangles (white fill, #555555 outline) connected by thin grey arrows.
%  3. Lane (i), top. Lane title at its left, bold: "(i) Greedy G*". Blocks left to right: "particle filter" ->
%     "EIG / c over all 512 actions" (inside this block a tiny row of 12 thin vertical bars of varying height in BLUE,
%     one bar taller and outlined darker) -> "argmax". To the right of the lane, a small simple clock icon (grey
%     outline) with the label "0.91 s / decision".
%  4. Lane (ii), middle. Lane title, bold: "(ii) One-step look-ahead". Blocks: "EIG / c scores" -> a small tree glyph
%     (one root node branching to four child nodes, each child continuing in a short dashed line to a leaf dot) with the
%     label under the tree: "rollouts completed by reduced greedy" -> "best first action".
%  5. Lane (iii), bottom. Lane title, bold: "(iii) Learned policy". Blocks: a small cluster of 4 blue points with short
%     tick marks, labelled "touch history (finger frame)" -> a block labelled "DeepSets" -> "512 masked logits"
%     (inside: a tiny row of 12 thin bars, a few greyed out to suggest masking).
%  6. Two training arrows enter the "DeepSets" block from above/below:
%     - a SOLID BLUE arrow coming down from lane (i)'s "EIG / c over all 512 actions" block, labelled in blue:
%       "DAgger: dense score labels from G*";
%     - a DASHED ORANGE arrow entering from below, labelled in orange: "PPO: reward = ball-sPCE (g_T)".
%  7. No other arrows, no numbers other than "512" (twice) and "0.91 s / decision".
%
% PANEL C (right, about 25 % of the width) - headline answers:
%  Leave this panel as an EMPTY placeholder: a plain white rectangle with a thin light-grey border (#DDDDDD), the
%  panel letter "C" in its top-left corner, and NOTHING else inside (no axes, no bars, no numbers, no text). The data
%  inset is plotted separately from the results JSON and pasted into this frame; the generator must not draw any
%  chart, value or label here.
%
% Global: balanced composition, generous margins, all labels legible when the figure is printed 17 cm wide, no
% overlapping text, no clutter, no title above the figure, no caption inside the image.
%
% (Panel C inset, plotted with matplotlib, not generated; values from results/v3/results_v3.json:)
%  left mini-plot: G(12) = 0.01624 (12_g2_analysis.k12.G), one-sided 95 % UB 0.02210 (.k12.ub95), dashed line at the
%    pre-registered Hold threshold 0.03; y-axis "one-step headroom G(12)".
%  right mini-plot: test3 0-299 success: G* 0.4267 (14_m4_analysis.rows.gstar.success); student 0.3822
%    (.rows.student.success) with whisker from diffs["student-gstar:success"].ci95 = [-0.0933, +0.0056] relative to
%    G*; RL 0.3567 (.rows.rl.success) with whisker from diffs["gstar-rl:success"].ci95 = [+0.0022, +0.1367],
%    sign-flipped relative to G*; hatched fourth bar "B-fan (exploratory)" 0.36
%    (.exploratory_b_fan.success) with whisker from exploratory_b_fan["b_fan-gstar:success"].ci95 = [-0.12, -0.01].
-->

<!-- Title: owner chooses between the proposed title (below) and Fallback B: "Cost-Aware Information-Gain Touch
Selection: Look-Ahead Headroom and the Learnability of Amortized Policies" (07_hypotheses_v3 §3: the outcome map can
only shorten the working title). Outcome row 4 (characterisation; no method claim). Stage-18 triage S1 asks for a
regime qualifier ("stay-and-probe" regime, four-probe budget); it is carried in the abstract and introduction, and
whether the title also carries it is an owner decision (OWNER_TODO). -->

# Can Cost-Aware Information-Gain Touch Selection Be Amortized? Look-Ahead Headroom and Learnability under Travel Cost

## Abstract

Active tactile localization chooses the next touch from a belief over object identity and pose; when finger travel
costs time, that choice trades information against travel. We ask how much headroom one-step look-ahead leaves over
greedy cost-aware information-gain touch selection, and whether that planner can be amortized by a policy distilled
from it or trained by reinforcement learning (RL) on the same objective. The
task uses a joint identity × planar-pose particle belief, a finger on a stand-off circle with travel cost
$c(a) = 1 + \kappa|\Delta\phi|/\pi$, and the greedy planner G\*, which maximises expected ball-information gain per unit
cost. In a pre-registered characterisation of one cell (shape set S, κ = 12, four probes), travel is so costly that G\*
mostly stays and probes (mean finger travel 6.1° per episode). Over 32 screened first actions, one-step rollout
over a reduced greedy completion gains ≤ 2.2 % of the remaining expected ball information (one-sided 95 % bound),
replicating an earlier estimate. With an identical belief-free DeepSets head, neither DAgger distillation nor PPO was
shown to reach G\*: the student failed its non-inferiority gate (−4.40 pp against −1.68 pp), and RL trails G\* by
7.0 pp in test success. On RL's own objective no learner difference was detected (Δ = +0.0002 nats, bounds
[−0.31, +0.30]); equivalence was not tested. Neither learner was shown to exceed a travel-nearest stay-and-fan heuristic
(exploratory). Per decision, the learned head's median latency is about 2,200× below full-size G\*, not at matched
accuracy. Results are preliminary.

## 1 Introduction

A robot that localizes an object by touch receives sparse, ambiguous measurements: one contact point and one surface
normal per probe, or a miss. A single contact rarely fixes the pose, and near-symmetric object families make even the
identity uncertain. The standard remedy is to maintain a belief over identity and pose, typically a particle filter, and
to choose the next touch by its expected information gain \cite{petrovskaya2011global, hebert2013next,
zheng2024bayesian, zheng2026bayesian}. Probing is not free. The finger has to travel to the next approach direction,
and travel time competes with probes within a fixed time budget. Cost-aware selection therefore scores each candidate
by information per unit cost \cite{ottenhaus2018active}, and surveys of active haptic perception identify this trade-off
as central to practical exploration \cite{seminara2019active}.

Two questions follow for every information-driven touch selector that pays for travel. The first concerns planning
depth. Greedy information gathering is backed by (adaptive) submodularity: for touch-based localization, entropy
reduction is submodular under certain assumptions, and greedy selection is then comparable to the optimal offline policy
\cite{javdani2012efficient, vien2015touch}. These guarantees weaken when actions constrain the future
\cite{chen2015submodular, esfandiari2019adaptivity}, and travel cost is exactly such a coupling: where the finger ends up
after a probe determines what the next probe costs. A greedy selector may strand the finger far from the region that
separates the remaining hypotheses. Whether paying for look-ahead is worth it under travel cost is an empirical question
that, to our knowledge, has not been measured directly.

The second question concerns amortization. Online particle-filter EIG re-optimises at every decision, with a cost that
grows with particles × candidates × outcome samples. Amortized Bayesian experimental design replaces this with a policy
network trained once, through RL on contrastive information bounds or related approaches \cite{foster2021deep,
blau2022optimizing, ivanova2021implicit, hedman2025step, rainforth2024modern}, and tactile RL methods learn exploration
policies end to end \cite{riou2024reinforcement, niemann2024when}. A validated greedy planner offers a second route:
supervising the policy with the planner's dense per-action scores through DAgger \cite{ross2011reduction}, which removes
long-horizon credit assignment and 512-way exploration from the learning problem. The question is whether such dense
supervision beats RL on the same objective with the same head, and whether either learner reaches the planner.

**What we did and found.** We ran a pre-registered study in which hypotheses, thresholds and the full outcome map were
frozen before any test episode. Three hypotheses were registered: H1, a distilled student non-inferior to G\* (with a
fallback, H1-fb, in which the student prunes G\*'s candidates); H2, distillation beating RL on RL's own objective; and
H3, small one-step look-ahead headroom over G\*. The record reached the pre-written characterisation outcome.

The tested cell (shape set S, κ = 12, four probes) turned out to be a *stay-and-probe* regime. The budget leaves less
than one stroke-unit of time beyond four unit-cost probes, and G\* uses little of it: its mean logged finger travel is
6.1° per episode, 79.3 % of its between-probe moves are zero, and 6.3 % exceed one grid step. The planner mostly varies
the approach offset at the current angle. The scenario of a finger stranded far from the informative region therefore
has little room to occur here, and all findings below are findings for this regime.

Within it, one-step rollout over the reduced greedy completion gains ≤ 2.2 % of the remaining expected ball information
at κ = 12 (S, n\* = 4; one-sided 95 % UB of G(12) = 0.0221). The bound covers 32 screened first actions (G\*'s own
action, three structured set-up moves and random actions), not every feasible action, and it replicates the previous
design iteration's estimate on a coarser action set (G(12) = 0.0146, UB 0.0208), which was known when the threshold was
registered. With the same relative DeepSets head, neither learner was shown to reach G\*: the student failed the
pre-registered non-inferiority rule on validation (−4.40 pp against a threshold of −1.68 pp) and trails by 4.4 pp on
test, while RL trails by 7.0 pp (ci95 [+0.2, +13.7] for G\* − RL). On RL's own objective, ball-sPCE, no advantage of
distillation was detected (H2 rejected); passing would have required an observed difference above 0.41 nats, so the
test was powered only for large effects. Neither learner was shown to exceed a belief-free, travel-nearest heuristic
that stays and fans its approach offset (exploratory). The learned head is about 2,200× cheaper per decision than
full-size G\*, not at matched accuracy, and H1-fb was withdrawn before any accuracy number because candidate pruning
cannot reach the registered 10× latency ratio.

**Contributions.**
- **C1.** A measured, pre-registered bound on one-step look-ahead headroom over cost-aware greedy touch selection in a
  stay-and-probe cell (H3, Hold), stated for the 32 screened first actions, with a replication of the previous
  iteration's estimate, instrument checks on one exact construction plus a zero-gap bank, and an on-belief bias check.
- **C2.** A controlled learnability comparison of planner distillation (DAgger) against RL (PPO) with an identical
  belief-free head, together with a behavioural diagnosis (finger travel, probe use, policy entropy) and a belief-input
  control.
- **C3.** A test of distillation against RL on RL's own objective (H2: rejected; a non-detection with stated power and a
  saturation analysis of the objective).
- **C4.** A per-decision latency decomposition of G\* that explains why candidate pruning cannot amortize it, because
  particle-filter work outside candidate scoring bounds the speed-up.

The evaluator's sensitivity to grid resolution is reported as a methods note (Section 4), not as a contribution. The
outcome reported here (row 4 of the pre-registered outcome map, a characterisation paper with no method claim) was
written before the runs. Section 2 reviews related work, Section 3 defines the task, the planner, the headroom estimator
and the two learners, Section 4 gives the protocol, Section 5 the results, and Sections 6–8 discuss, bound and conclude.
Appendix A holds the pre-registered gate record.

## 2 Related Work

**Tactile localization and next-best touch.** Estimating object pose from touch is usually posed as Bayesian filtering.
Scaling-series Monte Carlo achieves global localization from sparse contacts on polygonal meshes
\cite{petrovskaya2011global}; manifold particle filters sample on the contact manifold to avoid degeneracy in planar
contact manipulation \cite{koval2015pose}; Tac2Pose returns a pose distribution from a single high-resolution touch
\cite{bauza2023tac2pose}. On top of such estimators, information-driven selection picks the next touch. The next best
touch maximises information gain on pose uncertainty \cite{hebert2013next}; Bayesian frameworks jointly track class and
pose with customised particle filters and choose exploratory actions by expected information \cite{zheng2024bayesian,
zheng2026bayesian}; recent work chooses contacts by expected information gain for rigid-body pose and shape
\cite{gordon2026active} or learns exploration policies that balance global search and local refinement
\cite{kamtikar2026tactful}. Cost-aware information gain combines expected gain with expected cost in one score
\cite{ottenhaus2018active}, and reviews of active haptic perception summarise the space \cite{seminara2019active}.
Per-step (myopic) selection is the norm in this line. Its headroom under travel cost, and the per-decision compute it
costs, are rarely measured; C1 and C4 address both for one task. Greedy cost-aware selection itself is established; what
we add is a measurement of how much it leaves on the table in one regime, not a new selector.

**Greedy versus non-myopic information gathering.** Submodularity explains why greedy selection works well for touch:
Shannon entropy reduction is submodular under certain assumptions, and adaptive submodularity gives online guarantees
\cite{javdani2012efficient}. Hierarchical action structure can be folded into the same framework through sequential
submodular optimisation \cite{vien2015touch}. Outside touch, submodular surrogates approximate the value of information
when the objective itself is not submodular \cite{chen2015submodular}, and semi-adaptive policies show how much
adaptivity is needed to retain guarantees \cite{esfandiari2019adaptivity}. These results assume structure that travel
cost can break: a probe changes the price of every later probe, so the information an action buys is no longer
independent of where the finger ends up. Rather than bound the gap theoretically, we measure the one-step rollout
headroom over the cost-aware greedy planner directly, with an estimator checked on a construction whose exact gap is
known and on a bank whose gap is zero (H3). The measurement is empirical and local: it bounds one deviating step among
the screened candidates, not the gap to the optimal policy.

**Amortized and learned active sensing.** Deep adaptive design trains a design network on contrastive information
bounds so that each decision is a forward pass \cite{foster2021deep}; implicit and RL formulations remove the need for
likelihoods or differentiable simulators \cite{ivanova2021implicit, blau2022optimizing}, semi-amortized variants refine
the policy online \cite{hedman2025step}, nested particle filters amortize design in dynamical systems
\cite{iqbal2024recursive}, and transformer policies amortize inference and acquisition jointly \cite{huang2026aline}; a
recent review covers the field \cite{rainforth2024modern}. In touch, RL agents explore for recognition with rewards for
correct classification \cite{riou2021seeing, fleer2020efficient}, for classification, exploration and pose
\cite{riou2024reinforcement}, or learn when to stop \cite{niemann2024when}; TANDEM3D co-trains exploration and decision
making on 3D contacts \cite{xu2023tandem3d}, and Tactile MNIST provides a benchmark including localization
\cite{schneider2025tactile}. A second route imitates an information-gathering expert: imitation of a clairvoyant oracle
\cite{choudhury2017adaptive} and deep imitation of a nonmyopic active-search expert \cite{nguyen2024amortized}, both
building on DAgger's no-regret reduction \cite{ross2011reduction}. The comparison between the two routes therefore has
precedent in spirit; what is missing is a controlled comparison of RL against supervised distillation of a validated
planner, with the same head, the same action set and the same objective, evaluated on the objective RL itself
optimises. C2 and C3 supply that comparison for one cell, and the behavioural diagnosis shows what each learner actually
does with the finger.

## 3 Problem and Methods

### 3.1 Task, belief and metrics

**State and observations.** The object is a planar polygon with circumradius R = 40 mm, identity
$k \in \{1,\dots,K\}$ from library S (K = 8, near-symmetric base/variant pairs), and unknown pose. The state is
$s = (k, x, y, \theta)$ with prior $k \sim U\{1..K\}$, $x, y \sim U[-15, 15]$ mm, $\theta \sim U[0, 2\pi)$, and $G_k$
is the exact symmetry group of shape $k$. A probe returns either a contact point with noise $\mathcal{N}(0,\sigma_p^2 I)$,
$\sigma_p = 1.0$ mm, and a normal with noise $\mathcal{N}(0,\sigma_n^2)$, $\sigma_n = 5°$, or a miss
$y = \varnothing$. Every method uses the same ε-softened likelihood $p_\varepsilon(y \mid s, a)$ with ε = 10⁻³.

**Actions and travel cost.** The finger rests on a stand-off circle of radius $R_s$ = 100 mm at angle $\phi_t$, with
start angle $\phi_0 \sim U[0, 2\pi)$ shared by all methods on an episode. An action $a = (\phi', \psi)$ selects one of 64
target angles $\phi'$ (5.625° spacing) and one of 8 offsets $\psi \in \{-35°, -25°, \dots, +35°\}$, giving
$|\mathcal{A}| = 512$. The finger travels the shorter way to $\phi'$ and probes from $100(\cos\phi', \sin\phi')$ mm in
direction $\phi' + \pi + \psi$ with a 200 mm guarded stroke; afterwards $\phi_{t+1} = \phi'$. In units of one stroke,

$$c(a) = 1 + \kappa\,\frac{|\Delta\phi|}{\pi}, \qquad \Delta\phi = \mathrm{wrap}(\phi' - \phi_t) \in (-\pi, \pi],$$

so κ is the time to travel half the circle. Each episode has a time budget $\tau_\kappa$; with remaining time
$\tau_{\mathrm{rem}}$ the feasible set is $\mathcal{F}(\tau_{\mathrm{rem}}) = \{a \in \mathcal{A} : c(a) \le
\tau_{\mathrm{rem}}\}$, every method chooses only within it, and the episode ends when $\tau_{\mathrm{rem}} < 1$.
Budgets are **probe-matched**: $\tau_\kappa$ is calibrated so that G\* executes $n^\*$ probes on average at every κ. For
set S, $n^\* = 4$, $\tau_0 = 4.0$, $\tau_2 = 4.7$ and $\tau_{12} = 4.9$; at $\tau_{12}$, G\* executes 3.96 probes on
average over 200 calibration episodes. Only the price of moving differs between κ levels, not the horizon. A
consequence matters for every result below: at κ = 12, $\tau_{12}$ leaves less than one stroke-unit beyond four probes,
so any substantial move costs a probe. This is the stay-and-probe regime measured in Section 5.3.

**Metrics.** From the evaluator's posterior after the last probe, the identity estimate $\hat k$ is the maximum-mass
identity and the pose is refined by 30 Nelder–Mead iterations. Success is
$[\hat k = k_0] \wedge [\|(\hat x, \hat y) - (x_0, y_0)\| < 5\,\mathrm{mm}] \wedge [\min_{g \in G_{k_0}}
|\mathrm{wrap}(\hat\theta - \theta_0 - g)| < 5°]$. With $B(s_0)$ the success ball around the true state, the ball
information is

$$\mathrm{BI}(h) = \log \hat P(B(s_0) \mid h) - \log P(B(s_0)) \quad \text{[nats]},$$

with the posterior mass floored at $1/(2 \cdot 32{,}000)$ and the prior mass computed exactly. BI is the shared
information target of every information-based method below.

### 3.2 Cost-aware greedy planner G\*

G\* maintains an online particle filter $b = \{s_n, w_n\}_{n=1}^{N}$ and selects

$$G^\*(b) = \arg\max_{a \in \mathcal{F}(\tau_{\mathrm{rem}})} \frac{\mathrm{EIG}_B(a; b)}{c(a)},$$

where the ball EIG is estimated by nested Monte Carlo with $j_m \sim w$, $y_m \sim p_\varepsilon(\cdot \mid s_{j_m}, a)$:

$$\mathrm{EIG}_B(a;b) = \frac{1}{M}\sum_{m=1}^{M}\Big[\log\!\!\sum_{n \in B(s_{j_m})}\!\! w_n p_\varepsilon(y_m \mid s_n,a)
- \log\!\!\sum_{n \in B(s_{j_m})}\!\! w_n - \log \sum_n w_n p_\varepsilon(y_m \mid s_n, a)\Big].$$

This is the expected one-step increment of $\log P(B(s_0) \mid h)$. Full size is $(N, C, M) = (2{,}000, 512, 64)$. At
κ = 0 G\* reduces to plain ball greedy. At each decision G\* also exports the full score vector
$s(a) = \max(0, \mathrm{EIG}_B(a;b))/c(a)$ over feasible $a$ (zero elsewhere), whose argmax coincides with G\*'s action;
this vector is the distillation target. **Complexity.** Per decision, G\* evaluates $M \cdot N \cdot C + N \cdot C$
likelihoods and builds ball-neighbour lists in $O(N^2)$, on top of the particle-filter assimilation of the last
observation.

### 3.3 One-step look-ahead headroom estimator

To ask whether depth is worth paying for, we compare G\* with a policy that may deviate from it for one step. For a
belief $b$ reached by G\*, let $V_{G^\*}(b)$ be the expected ball information gained over the remaining budget by
following the greedy completion, and $V_{LA}(b)$ the value of the best screened first action followed by the same
completion. The headroom is the dimensionless ratio of means over a bank of beliefs:

$$G(\kappa) = \frac{\overline{V}_{LA} - \overline{V}_{G^\*}}{\overline{V}_{LA}}.$$

The estimator screens $C_1 = 32$ first actions with common random numbers and $M_{\text{outer}} = 64$: G\*'s own
action, three structured set-up moves, and random feasible actions up to 32, out of as many as 512 feasible ones. It
then re-estimates the top 4 together with G\*'s action using 4 × 64 samples. Rollouts are completed by a **reduced
greedy**: $N_{LA} = 500$ particles resampled from G\*'s decision filter, a 128-action candidate subset, M = 16,
cost-aware and feasibility-restricted. G(κ) is therefore one-step-deviation headroom over a reduced greedy completion,
restricted to the screened first actions; it is not the gap to the optimal policy, not the best possible one-step
deviation, and it makes no success claim. Because $V_{LA}$ is the maximum over a few noisy re-estimates, it can carry an
upward selection bias; the re-estimation step is meant to limit it, but its size was not measured separately.

Hold requires instrument checks on two objects. The first is a notch construction with a known exact relative gap,
used in two forms: (a) the abstract notch problem (pass band [0.573, 0.860], 5 runs) and (c) a travel-notch that places
the same problem's actions on the circle (estimate within ±20 % of the exact gap computed by enumeration). Both forms
share one exact gap, so they are one construction checked twice, not two independent checks, and both were re-used from
the previous design iteration. The second object is (b) a bank of 100 beliefs with exact gap 0 (mean in [−0.01, 0.02],
UB < 0.03), which tests false positives. In the notch construction the gainful first move is among the structured
set-up moves, so the checks show that the estimator detects a gap that the screened set contains; they do not show
that random screening would find one. A bias check compares the estimator's $V_{G^\*}$ with an independent 4×-sample
full-G\* rollout on 20 beliefs; a ratio above 1.02 (over-reading greedy, which deflates G) would make Hold unavailable.
The guard is one-sided by registration: it does not cover under-reading of $V_{G^\*}$ or any bias of $V_{LA}$.

### 3.4 Amortized policies with one shared head

**Shared architecture.** Both learners use the same belief-free DeepSets head. Each touch in the history is encoded in
the finger frame (contact indicator, contact point, normal, and the action that produced it), summed by a DeepSets
encoder, and concatenated with a 5-dimensional context: the cosine and sine of a relative angle, the remaining-budget
fraction $\tau_{\mathrm{rem}}/\tau$, and the cosine and sine of the absolute finger angle $\phi_t$. The context is
therefore not purely finger-relative; we keep the name "relative head" for the history encoding and the action
parameterisation. The encoder and head are 2 × 128 MLPs and output 512 relative logits, masked to $-\infty$ outside
$\mathcal{F}(\tau_{\mathrm{rem}})$. The architecture, input and action set are the controlled variables of C2 and C3;
the training signal differs, and so, as Section 5.2 reports, does the optimisation budget. **Complexity.** The
implementation re-encodes the full history at each decision, $O(T^2 H^2 + T H A)$ for $T$ touches, hidden width $H$ and
$A = 512$ actions.

**Distillation.** The student $\pi_\theta$ minimises

$$\mathcal{L}(\theta) = -\sum_{a \in \mathcal{F}} q(a)\log \pi_\theta(a \mid h) - \lambda \log \pi_\theta(a^\* \mid h),
\qquad q = \mathrm{softmax}\big(\beta_T\, s(a)/\sigma_s\big)_{a \in \mathcal{F}},$$

with $\sigma_s$ the per-decision standard deviation of $s$ over feasible actions (uniform over the argmax set if
$\sigma_s < 10^{-6}$) and $a^\* = \arg\max_a s(a)$. Hyperparameters were selected on held-out floored normalised regret,

$$r = \frac{s_{\max} - s(a_\pi)}{\max(s_{\max} - s_{\mathrm{med}},\ \rho\, s_{\max})}, \qquad \rho = 0.05,$$

whose mean $\bar R$ also drives the stopping rule; decisions with $s_{\max} = 0$ are excluded. The selection used a
4-configuration grid on one seed and round 0 only; the selected configuration (lr 1e-3, Table 0) is the largest
learning rate in that grid and won narrowly, so the student's tuning is not shown to be converged. No success-based
selection is used anywhere.

> **Algorithm 1 (DAgger distillation of G\*).**
> 1. Round 0: roll out G\* on 1,500 label episodes, store $(h, \phi_t, \tau_{\mathrm{rem}}, \mathcal{F}, s, a^\*)$ at
>    every decision; hold out episodes 1,200–1,499 for $\bar R$. Train $\pi_\theta$ on $\mathcal{L}$.
> 2. For round $r = 1, 2$ with mixing $\beta_{\mathrm{DAgger}} \in \{0.5, 0\}$: roll out 400 episodes per seed, executing
>    G\*'s action with probability $\beta_{\mathrm{DAgger}}$ and $\pi_\theta$'s otherwise; run G\*'s filter alongside and
>    label every visited belief with $s$; aggregate all data; continue training from the previous weights (the Adam
>    optimiser state is re-initialised at each round).
> 3. In every round, evaluate held-out $\bar R$ after each epoch; stop when it improves by < 0.005 over 3 evaluations
>    (cap 50 epochs); keep the last checkpoint.
> 4. Remedy (pre-registered, applied once if gate D3 fails): double round 0 and both DAgger rounds and retrain.

The applied remedy raised the end-of-round-2 training set from 7,957 to 17,083 decisions per seed.

**RL (PPO).** The RL policy uses the same head and action set and is trained with PPO-clip \cite{schulman2017proximal}
(clip 0.2, 4 epochs per update), γ = 1 and a critic baseline. Its reward is the increment of ball-sPCE, a contrastive
estimate of ball information in the style of \cite{foster2021deep}: per episode, $L = 4095$ contrastive states
$s_{1:L} \sim p$ and $J = 16$ states $s_0^{(j)}$ uniform in $B(s_0)$ are fixed, and

$$g_t = \log \hat p_B(h_t \mid s_0) - \log\Big[\tfrac{1}{L+1}\Big(\hat p_B(h_t \mid s_0) + \sum_{l=1}^{L} p(h_t \mid
s_l)\Big)\Big], \quad \hat p_B(h \mid s_0) = \tfrac{1}{J}\sum_j p(h \mid s_0^{(j)}),$$

with $r_t = g_t - g_{t-1}$. The return telescopes to $g_T$ (capped at $\log(L+1) = 8.32$ nats), so **$g_T$ is RL's own
objective**. Because of the cap, episodes whose history already separates the true ball from all $L$ contrastive states
add no further reward; Section 5.4 reports how often this happens. Each RL seed trains for 200,064 episodes; the
learning rate was chosen by a 4-configuration sweep (Section 4).

**Belief-input control.** The same distillation recipe with the history encoder replaced by a 48-feature summary of
G\*'s particle filter (per identity: weight, weighted mean and SD of $x$ and $y$, and the resultant length of
$|G_k|\theta$) plus the relative context, trained on first-attempt-size data. It is used only by the encoder sentence of
H2's fail branch.

### 3.5 Baselines

Random selects uniformly among feasible actions. Three heuristics use a budget-reservation rule, allowing $a$ only if
$c(a) \le \tau_{\mathrm{rem}} - \max(0, n^\* - t - 1)$ after $t$ probes (else the cheapest feasible action):
**B-spread** (belief-free) maximises the minimum angular distance to previous probe angles with ψ = +5°; **B-fan**
(belief-free, travel-nearest) stays at $\phi_t$ when allowed and cycles ψ through +5°, −5°, +15°, …, −35°, otherwise
moving to the nearest allowed $\phi'$; **B-cov** (belief-using) maximises coverage under an online filter. The best
heuristic on pilot data, H★, was frozen before test; for S12 it is B-fan. B-fan is the natural reference for the
stay-and-probe regime: it encodes "stay where you are and vary the approach offset" without any belief.

## 4 Experimental Protocol

**Pre-registration and routing.** Hypotheses, thresholds, the outcome map (rows 1–4) and a list of analyses not allowed
after the run were frozen in design documents before any v3 run, and the main-run set was frozen before any test
episode. The record reached row 4: the learnability gate D3 failed on the first attempt and again after its one remedy
(H1 dead, never tested on the test split), and H1-fb was withdrawn at the latency gate. Under row 4 the remaining
pre-registered decisions are H2, H3 and the encoder sentence; all other numbers are gate data or reported rows without
a test. The full gate record (Table A1) is in Appendix A.

**Pre-registered items not executed.** Several registered items were descoped by the row-4 routing, because each was
conditional on H1 reaching the test split, which D3 prevented: the Holm-corrected family of reported rows (student
against behaviour cloning, against an absolute-frame student, and against random), the secondary equivalence test
(TOST) of student against G\* at ±δ_c, the behaviour-cloning and absolute-frame student rows themselves, and the
reduced-G\* candidates R_b registered for the H1 cost comparison. None was run; their absence follows from the
routing, not from a post-hoc choice.

**Cell.** All learning results are for set S at κ = 12 with $n^\* = 4$ (S12). H3 also uses κ ∈ {0, 2}.

**Splits.** Disjoint episode streams: calibration (200), pilot3 (G\* 500 episodes; random and heuristics 200 each, for
margins and H★), val3 (500 paired episodes, for D3 and its remedy), test3 episodes 0–499 (H2, $g_T$, behaviour
diagnostics) and 0–299 (success and BI rows). Within a split, all methods run on the same episodes with the same
initial state, start angle and observation stream (paired design). H3 uses 100 G\*-reached beliefs per κ, at a
uniformly drawn step in $\{0, \dots, n^\*-1\}$.

**Evaluator (methods note).** Success and BI are read from an adaptive grid posterior that rebuilds each history exactly.
Its gate compared grid subdivision 4 with 8 on 16 episodes drawn from S12 and A12 and failed: one counted success flip
occurred outside the [0.45, 0.55] true-identity-mass tie band, in an A12 B-fan episode. Subdivision 8 is therefore used
for every reported number. The evaluator is not shown to be converged (Section 7), and success differences of a few
points should be read with that in mind; BI moves little between subdivisions (mean |ΔBI| 0.0126 nats on the 16
episodes). $g_T$, H3, latency and label fit do not use the grid.

**Statistics.** Paired differences use a crossed episode × seed bootstrap with B = 10,000; bounds are one-sided 95 %
unless labelled ci90/ci95 (two-sided). Each claim has one test and there is no correction across claims, because H2 and
H3 are separate claims with separate decisions. The test-split success and BI intervals are descriptive, not tests.
With three seeds per learner, the seed dimension dominates the learner intervals.

**Gate D3.** On 500 paired val3 episodes with 3 student seeds, D3 passes iff (i)
$\hat\Delta_{\mathrm{succ}} \ge \max(-2\,\mathrm{pp},\ -\delta + 1.645\,\mathrm{SE}_s\sqrt{0.5})$; (ii) the same for BI
with ε and a −0.15-nat floor; (iii) every seed's $\hat\Delta_{\mathrm{succ}} > -\delta$. Here δ = min(4 pp, 0.15·D_c)
and ε = min(0.05·BI(G\*), 0.15·D_c^BI), with D_c the pilot random-to-G\* gap; for S12, δ = 0.04 (the cap) and
ε_S12 = 0.3145 (provisional; Appendix A).

**H2 and H3 rules.** H2 passes iff the one-sided 95 % lower bound of $g_T(\text{student}) - g_T(\text{RL})$ on test3
0–499 exceeds +0.10 nats. H3 is Hold iff UB95(G(12)) < 0.03, Kill iff LB95(G(12)) > 0.05 (precedence), otherwise
Inconclusive. The previous design iteration had measured G(12) = 0.0146 (UB95 0.0208) on a coarser action set before
this threshold was registered, so H3 is a pre-registered replication on the 64 × 8 action set rather than a first
measurement.

**Behaviour diagnostics (report-only).** On test3 0–499 (B-fan: 0–299) we log, per episode, the total finger travel,
the number of probes, the fraction of between-probe moves that are zero or exceed one grid step (5.625°), and whether
$g_T$ reached its cap $\log(L+1)$; for RL we also read the final training entropy. These rows carry no test.

**Hyperparameters and implementation.** Table 0 lists the training and estimator settings. Everything is numpy with
hand-written backpropagation (Python 3.12.15, numpy 2.5.4), run single-threaded (OMP/OPENBLAS/MKL_NUM_THREADS = 1) on
GitHub-hosted standard runners whose CPU model is not logged. Latency follows a fixed protocol: all configurations are
timed interleaved on the same S12 pilot decision states with threads = 1 and no core pinning, 20 warm-up and 500 timed
decisions, plus 500 more if any 95 % CI half-width exceeds 10 % of its median; the pooled 1,000 decisions on 253 pilot
episodes came from two runner jobs. The timed student is the round-0 checkpoint of seed 501, which has the same
architecture and therefore the same per-decision cost as the remedied students. The latency protocol also timed
reduced-size G\* configurations (fewer particles, candidates and samples); their accuracy was not measured.

**Table 0. Settings (design constants from the frozen design documents; RL learning rate from the sweep).**

| Component | Setting |
|---|---|
| G\* | N = 2,000 particles, C = 512 candidates, M = 64 outcome samples |
| Distillation | Adam, lr 1e-3, β_T = 4, λ = 0.5, batch 256, gradient-norm clip 1.0, no weight decay; selected from a 4-configuration grid (1 seed, round 0) |
| Distillation data | round 0: 1,500 G\* rollouts; DAgger: 2 rounds × 400 rollouts per seed (β = 0.5, then 0); remedy doubles all three |
| Stopping | held-out $\bar R$; < 0.005 improvement over 3 evaluations; ≤ 50 epochs; ρ = 0.05 |
| Student seeds | 501, 502, 503 (belief-input control: 521–523) |
| PPO | γ = 1, critic baseline, clip 0.2, 4 epochs per update; 200,064 episodes per seed; seeds 511–513 |
| PPO sweep | 4 configs, 1 seed, 50,048 episodes each; selected cfg 2: lr 1.09e-3, entropy 1.33e-4, batch 128, critic lr 1.43e-3 |
| ball-sPCE | L = 4095 contrastive states, J = 16 ball states |
| H3 estimator | C₁ = 32 screened, M_outer = 64, top 4 re-estimated with 4 × 64; completion N_LA = 500, 128 candidates, M = 16 |
| Evaluator | adaptive grid posterior, subdivision 8; 30 Nelder–Mead iterations; tie band [0.45, 0.55] |
| Runtime | Python 3.12.15, numpy 2.5.4, BLAS threads = 1; GitHub-hosted standard runners (CPU model not logged) |

## 5 Results

### 5.1 H3: one-step look-ahead headroom is small among the screened actions

H3 is **Hold**. One-step rollout over the reduced greedy completion gains ≤ 2.2 % of the remaining expected ball
information at κ = 12 (S, n\* = 4; one-sided 95 % UB of G(12) = 0.0221). The bound is over the 32 screened first
actions. The point estimate is G(12) = 0.01624, and the upper bound clears the 0.03 threshold by 0.0079. In absolute
terms the gap is 0.041 nats on a mean $V_{G^\*}$ of 2.506 nats (Table 2a). The point estimates follow the descriptive
ordering G(0) ≤ G(2) ≤ G(12) (differences not tested), and even the largest is small. The result replicates the
previous design iteration on its coarser action set, where G(12) was 0.0146 (UB95 0.0208) and G(0) 0.0049; that
estimate was known when the 0.03 threshold was set, so Hold was the expected outcome and is reported as a replication.

**Table 2a. Headroom over G\* (set S, 100 beliefs per κ).**

| κ | G | LB95 | UB95 | gap (nats) | mean V_LA | mean V_G\* | frac LA ≠ G\* | no budget left |
|---|---|---|---|---|---|---|---|---|
| 0 | 0.006374 | 0.004028 | 0.009401 | 0.01795 | 2.816 | 2.798 | 0.58 | 0 |
| 2 | 0.01418 | 0.009616 | 0.01974 | 0.03712 | 2.617 | 2.580 | 0.54 | 4 |
| 12 | 0.01624 | 0.01148 | 0.02210 | 0.04137 | 2.548 | 2.506 | 0.62 | 1 |

The look-ahead chooses a different first action from G\* on 62 % of beliefs at κ = 12, yet gains little on average.
This pattern is consistent with near-ties among the top actions; the record does not separate near-ties from
argmax-selection noise. All instrument checks passed: the notch construction gives a mean relative gap of 0.8290
(band [0.573, 0.860]); its travel-notch form gives 0.7438 against the exact 0.7166 shared by both forms; the zero-gap
bank gives 0.00254 (UB 0.00374). The notch readings over-read the exact gap, in line with the upward selection bias of
$V_{LA}$ noted in Section 3.3. These checks reproduce the previous design iteration's values, so they are not
independent new evidence, and none of them is an in-domain positive control on the touch task. On bias: on 20 separate
beliefs the estimator reads V_G\* 0.087 nats (4.3 %, no CI) below an independent full-G\* rollout, comparable in size to
the 0.041-nat κ = 12 gap; this direction alone would inflate G, and Hold could be affected only if V_LA were under-read
by more, which was not checked. The ratio (0.957) is within the pre-registered guard, so Hold is not downgraded.

In this stay-and-probe cell, then, the reduced greedy completion leaves little headroom for one deviating step among
the screened candidates, consistent with greedy-competitiveness arguments \cite{javdani2012efficient,
chen2015submodular} carrying over at the tested budget. Because G\* rarely moves (Section 5.3), the cell gives the
travel coupling little room to create headroom, and the result says little about regimes in which travel binds.

### 5.2 Learnability: distillation and RL against the greedy teacher

**D3 (binding evidence).** On 500 paired val3 episodes, the first-attempt students reached Δ̂_succ = −5.87 pp against a
threshold of −1.43 pp and Δ̂_BI = −0.199 nats against −0.15, with per-seed success deficits of −4.2 / −8.0 / −5.4 pp.
After the remedy, success was −4.40 pp against −1.68 pp (fail), BI −0.096 against −0.15 (pass), and seeds −4.6 / −4.6 /
−4.0 pp (fail). Seed 503 sits exactly at −δ, but the verdict does not hinge on it, because rule (i) fails by 2.7 pp.
After the one remedy (round 0 and both DAgger rounds doubled; 7,957 → 17,083 training decisions), the point estimates
moved from −0.199 to −0.096 nats BI and from −5.87 to −4.40 pp success; this change was not tested.

**Test3 (descriptive).** Table 2b reports test3 0–299. Neither learned policy was shown to reach G\*: the student failed
the D3 non-inferiority rule on val3 (Δ̂_succ −4.40 pp vs threshold −1.68 pp), and on test3 it trails by −4.4 pp
(significant one-sided only) while RL trails by −7.0 pp (ci95 [+0.2, +13.7] for G\* − RL). The student's BI deficit
(−0.0487 nats) has a ci90 that includes 0, whereas G\* exceeds RL in BI by 0.338 nats (ci95 [+0.1585, +0.5196]). The
remedied students agree closely with each other (per-seed success 0.3833 / 0.3767 / 0.3867), so the deficit is
consistent across seeds. No fraction of the random-to-G\* gap is reported as recovered, because the pre-registered
condition for reporting it (the lower bound of G\* − RL success exceeding δ_S12) is not met.

**Table 2b. Test-set rows (S12; success and BI on test3 0–299, sub-8 grid; $g_T$ on test3 0–499).**

| Row | Method / contrast | Success | BI (nats) | Probes | $g_T$ (nats) |
|---|---|---|---|---|---|
| R8a | G\* | 0.4267 | 6.248 | 3.963 | 5.299 (no interval) |
| R8b | Student (remedied, 3 seeds) | 0.3822 (0.3833 / 0.3767 / 0.3867) | 6.200 | 4.0 | 5.368 |
| R8c | RL-relative (3 seeds) | 0.3567 (0.3667 / 0.3900 / 0.3133) | 5.910 | 3.0 | 5.368 |
| — | Random | — | — | — | 2.618 (no interval) |
| R8d–e | student − G\* | −0.0444, ci90 [−0.0856, −0.0033], ci95 [−0.0933, +0.0056] | −0.0487, ci90 [−0.1035, +0.0078], ci95 [−0.1138, +0.0190] | | |
| R8f–g | student − RL | +0.0256, ci95 [−0.0367, +0.0878] | +0.2893, ci95 [+0.1170, +0.4652] | | +0.00023, bounds [−0.3103, +0.3034] |
| R8h–i | G\* − RL | +0.0700, ci95 [+0.0022, +0.1367] | +0.3380, ci95 [+0.1585, +0.5196] | | |
| R9 | B-fan (exploratory, paired) | 0.36 | 5.973 | 4.0 | — |
| R9 | student − B-fan | +0.0222, ci95 [−0.0278, +0.0733] | +0.2263, ci95 [+0.1412, +0.3110] | | |
| R9 | B-fan − G\* | −0.0667, ci95 [−0.12, −0.01] | −0.2750, ci95 [−0.3665, −0.1843] | | |
| R9 | RL − B-fan | −0.0033, ci95 [−0.0689, +0.0633] | −0.0630, ci95 [−0.2465, +0.1199] | | |

**Label fit, training budget and the encoder sentence.** All six history students fit the training labels by the
pre-registered rule: train top-1 agreement 0.511–0.534 and train $\bar R$ 0.169–0.206 at the end of round 2 (under-fit
requires $\bar R$ > 0.25 or top-1 < 0.50). Held-out top-1 is below 0.50 for 4 of the 6 (0.4833–0.4916; the remedied
seeds 501 and 502 reach 0.5067 and 0.5059). By the pre-registered label-fit rule the deficit is assigned to
generalisation rather than capacity, and because the held-out regret is measured on teacher-visited states, covariate
shift is inferred, not observed. The rule's support is weak for a second reason. The stopping rule ended every student
round after 4–16 epochs, with 3.2–27.6 s of wall time per round across all 27 logged rounds, whereas each RL seed
trained for 200,064 episodes. The two learners therefore differ in optimisation budget as well as in training signal,
and a train top-1 of about 0.52 on the student's own training labels, close to its held-out top-1, is also what an
under-optimised model would show. Under-optimisation is not excluded. The teacher tie fraction, as logged, is 0.0 in all
210 logged evaluations, so exact ties in G\*'s scores do not depress top-1; near-ties are not measured by that
statistic.

**Long-training student (exploratory, pre-registered readings).** To test the stopping-rule explanation, a student is
trained for each of seeds 501–503 from scratch on exactly the remedied round-2 data, for a fixed 200 epochs without the
stopping rule, and read on test3 0–299 paired with G\* and the remedied students. The row is still running:
[PENDING:long_student]. Its readings were written before it runs: (a) if the long − remedied student success ci95
excludes 0 in favour of the long student, "the D3 deficit was partly an optimisation artefact of the stopping rule
(exploratory; D3 and row 4 unchanged)"; (b) otherwise, "training 200 epochs without a stopping rule did not detectably
change test success; the stopping rule is not shown to explain the deficit". In both cases long − G\* is reported with
its ci95, and held-out $\bar R$ worse than the remedied student's for all three seeds is reported as over-fit.

**Belief-input control.** The belief-input students are under-fit (train top-1 0.327–0.362, train $\bar R$
0.338–0.379). Their validation read is incomplete and provisional: on 298 val3 episodes, Δ̂_succ = −19.9 pp against a
threshold of −0.78 pp and Δ̂_BI = −1.01 nats against −0.15, with per-seed success deficits of −21.5 / −17.1 / −21.1 pp;
every criterion fails. Because these students are under-fit, the control isolates nothing about the representation; it
shows only that this 48-feature summary, trained on first-attempt-size data, is a worse input than the touch history.

### 5.3 Behaviour in the tested cell: a stay-and-probe regime

Table 2d reports how each policy uses the finger on test3 (report-only, no tests). The cell's travel cost is high
enough relative to the budget that G\* mostly stays: its mean logged travel is 6.1° per episode (median 6.3°, maximum
24.9°), 79.3 % of its between-probe moves are zero and only 6.3 % exceed one 5.625° grid step, while it executes four
probes in 481 of 500 episodes. The remedied students stay even more: 1.5–2.0° of mean travel, 97.7–99.7 % zero moves,
and four probes in every episode. B-fan stays by construction; all its between-probe moves are zero, so its 1.5° of
logged travel occurs before the first probe. RL behaves differently from all three. Every RL seed executes exactly three
probes in all 500 episodes and moves the finger 23.0–25.8° per episode on average, with 47.3–54.9 % of its moves longer
than one grid step: it trades a probe for travel. Its final training entropy is 0.0020–0.0125, so the policies are
close to deterministic. Random travels most (38.4°) and executes 1.946 probes on average.

**Table 2d. Behaviour on test3 0–499 (B-fan 0–299); travel is the logged total finger travel per episode.**

| Policy | Travel mean / median / max (°) | Probes (mean; histogram) | Zero moves | Moves > 1 step | $g_T$ at cap |
|---|---|---|---|---|---|
| G\* | 6.1 / 6.3 / 24.9 | 3.962 (3: 19, 4: 481) | 79.3 % | 6.3 % | 5.8 % |
| Student s501 | 1.5 / 1.5 / 12.3 | 4.0 (4: 500) | 99.7 % | 0.1 % | 3.0 % |
| Student s502 | 2.0 / 1.6 / 13.3 | 4.0 (4: 500) | 97.7 % | 1.3 % | 3.4 % |
| Student s503 | 1.9 / 1.6 / 13.3 | 4.0 (4: 500) | 98.5 % | 1.1 % | 2.4 % |
| RL s511 | 23.0 / 23.7 / 28.4 | 3.0 (3: 500) | 0.0 % | 54.9 % | 1.2 % |
| RL s512 | 25.8 / 25.7 / 28.5 | 3.0 (3: 500) | 21.9 % | 50.0 % | 0.4 % |
| RL s513 | 25.7 / 25.7 / 28.5 | 3.0 (3: 500) | 18.4 % | 47.3 % | 1.2 % |
| B-fan | 1.5 / 1.5 / 2.8 | 4.0 (4: 300) | 100 % | 0.0 % | — |
| Random | 38.4 / 39.0 / 58.5 | 1.946 (1: 136, 2: 259, 3: 101, 4: 4) | 33.0 % | 37.4 % | 0.0 % |

Two readings follow, both descriptive. First, the student's behaviour is close to B-fan's in the quantities logged
here, which is consistent with the paired B-fan contrast in Section 5.5; the record does not show which of G\*'s
belief-dependent offset choices the student reproduces. Second, RL and the student differ in strategy (three probes with
travel against four probes without), even though their $g_T$ does not detectably differ (Section 5.4).

### 5.4 H2: distillation against RL on RL's own objective

On test3 0–499, the student reaches $g_T$ = 5.3678 nats and RL 5.3676; Δ = +0.00023 nats with one-sided 95 % bounds
[−0.3103, +0.3034] (p_greater 0.4883). H2 is **rejected**. The pre-registered fail-branch reading applies: "dense
supervision does not improve on RL with this head", because the paired success ci95 [−3.67, +8.78] pp contains 0; the
alternative pre-written reading required that interval to exclude 0. Passing required an observed Δ > 0.41 nats; with
SE ≈ 0.19, the test had about 80 % power only for a true Δ near 0.57 nats. No equivalence test (TOST) was pre-registered
or run for H2. Overall, no difference between the two learned policies was detected on g_T (Δ = +0.0002 nats, one-sided
95 % bounds [−0.31, +0.30]) or on test success (ci95 [−3.7, +8.8] pp); equivalence was not tested. With three seeds per
learner, H2 as run is best read as a feasibility probe: it could detect only a large advantage.

**Why g_T and BI disagree.** The grid evaluator gives a further observation, not a mechanism. Student − RL BI is +0.289
nats (ci95 [+0.117, +0.465]) on test3 0–299, while the g_T difference on 0–499 is undetected with bounds wide enough
(±0.31 nats) to include a gap of that size; RL executes 3.0 probes against the student's 4.0. The g_T rows also order
G\* differently from BI: $g_T$(G\*) = 5.299 lies below both learners' 5.368, whereas grid BI orders G\* above both. We
checked saturation at the cap $\log(L+1) = 8.32$ nats on test3 0–499 (Table 2d): 5.8 % of G\* episodes, 2.4–3.4 % of
student episodes and 0.4–1.2 % of RL episodes reach it exactly. Saturation at the cap is therefore rare and ordered like
BI (G\* most often), so on this definition the cap is unlikely on its own to explain why G\*'s mean $g_T$ is lower. We
read the inversion as the contrastive estimate with $L = 4095$ and $J = 16$ ranking histories differently from the grid
posterior; the record contains no analysis of why, and we do not rank G\* against the learned policies on $g_T$. A different quantity, the RL trainer's own saturation fraction on its
last training batch, is 22.7–31.3 %; it is computed on training episodes with the trainer's definition and is not
comparable to the test3 rows. The companion rows $g_T$(G\*) and $g_T$(random) = 2.618 on the same episodes carry no
interval and no test.

**Seed variability.** RL varies more across its 3 seeds than the student (test success range 7.7 vs 1.0 pp; g_T range
0.48 vs 0.14 nats), and the RL per-seed SD of g_T is about 3.3× the student's (0.253 vs 0.077 nats; range ratio 3.5).
This spread is the likely source of the interval width, inferred from the per-seed SDs; no variance decomposition was
done. All three RL seeds ran to the 200,064-episode cap; the plateau rule fired at 102,400, 102,400 and 112,640
episodes, so training continued well past the point at which the registered plateau rule fired. The RL comparator's
learning rate is the largest in its 4-configuration sweep (Section 7), so the RL arm, like the student arm, is not shown
to be tuned to convergence.

### 5.5 Learned policies against a travel-nearest heuristic (exploratory)

The paired B-fan row on test3 0–299 completed (Table 2b, R9). Student − B-fan success is +2.2 pp with ci95
[−2.8, +7.3] pp, which contains 0, so the pre-written reading (b) applies: on test3 the learned policies were not shown
to exceed a travel-nearest heuristic (RL − B-fan −0.3 pp, ci95 [−6.9, +6.3]). The second clause of reading (b), that the
S12 task may be flat at $n^\* = 4$, is not supported on test3: B-fan trails G\* by 6.7 pp (ci95 [−12.0, −1.0]) and by
0.275 nats BI (ci95 [−0.3665, −0.1843]), so the clause is omitted. As a report-only row, student − B-fan BI is +0.226
nats (ci95 [+0.141, +0.311]). The pilot flat-screen flag for S12 rests on an incomplete sub-8 B-fan row (0.403 ± 0.040,
n = 154 of 200, provisional); on the complete sub-4 screen, H★ for S12 was also B-fan (0.395, n = 200). This row is
exploratory, it is not the dropped heuristic test of H1, and it does not change the outcome row.

### 5.6 Per-decision cost

**Table 2c. Per-decision latency (1,000 decisions, 253 S12 pilot episodes, two runner jobs pooled; student = round-0
checkpoint of seed 501, same architecture as the remedied students).**

| Quantity | Median | 95 % CI |
|---|---|---|
| Student, L_dec | 0.408 ms | [0.4036, 0.4137] ms |
| G\* full (2,000, 512, 64), L_dec | 0.9135 s | [0.7910, 0.9413] s |
| G\* components (assim / neighbour lists / scoring) | 0.0402 / 0.0967 / 0.7169 s | — |
| Pruned-16 (student top-16 + G\* re-scoring) | 0.2833 s | [0.2811, 0.2853] s |
| Student final read-out, L_final (per episode) | 0.2043 s | [0.1929, 0.2135] s |

Per decision, the student's median latency is about 2,200× below full-size G\* (pooled-machine latency, protocol
incomplete; G\* median CI alone ≈ 1,900–2,300×), not compared at matched accuracy. The ratio is against full-size G\*
only: reduced-size G\* configurations were timed but their accuracy was not measured, so the record does not show
whether learning beats simply shrinking the filter, and the ratio should not be read as the value of amortization. PF
assimilation and neighbour lists account for 15.0 % of G\*'s per-decision time (component medians), so pruning
candidates cannot exceed about 6.7× and cannot give 10×; measured full / pruned-16 = 3.22. This is why H1-fb was
withdrawn before any accuracy was measured.

## 6 Discussion

**What the results say together.** C1 shows that, in this stay-and-probe cell, one deviating step over the reduced
greedy completion gains ≤ 2.2 % of the remaining expected ball information among the 32 screened first actions
(one-sided 95 % UB), replicating the previous iteration. Within that scope, a greedy teacher is a defensible
amortization target: there is little evidence that a deeper planner would have been a better one at this budget. C2
shows that a defensible target is not enough. With the same belief-free head, neither the distilled student nor PPO was
shown to recover G\*'s success, and C3 shows that the dense per-action labels did not buy a detectable advantage on the
objective RL optimises. The supervision signal that removed credit assignment and exploration from the learning problem
did not, at this data scale and optimisation budget, bring the student to the teacher.

**What the regime means for the claims.** The motivating coupling, a finger stranded far from the informative region,
barely arises at κ = 12 with this budget: G\* moves the finger little, the students and B-fan hardly at all. Small
one-step headroom is then less surprising than it would be where travel binds, and the learnability comparison is a
comparison of how well each learner chooses approach offsets near the current angle. Neither learner was shown
to exceed B-fan, which encodes exactly that rule without a belief, while B-fan trails G\*. A cautious reading is that
the student recovered the stay-and-fan pattern of the teacher's behaviour but not the belief-dependent part of its
offset choice, and that RL settled on a different strategy (three probes with travel) that also was not shown to exceed
B-fan; the record supports the behavioural half of that reading (Table 2d) and is consistent with, but does not test,
the rest. A cell in which travel binds is the necessary next design; it was not run here.

**Why the student falls short.** The pre-registered label-fit rule points to generalisation rather than capacity, but
two other explanations remain open. The first is optimisation: student rounds stopped after 4–16 epochs and seconds of
wall time, and train top-1 of about 0.52 sits close to held-out top-1, which an under-optimised model would also show;
the long-training row is designed to separate this. The second is covariate shift onto the student's own states, which
is inferred rather than observed because the held-out set is teacher-visited. The H3 pattern suggests a complementary
reading: if many beliefs have several near-tied actions, top-1 agreement is a coarse measure of policy quality, and small
score differences that the student cannot reproduce may still matter for the final pose estimate.

**Unexpected results.** Three observations do not fit a simple story. First, BI separates the student from RL (+0.289
nats) while $g_T$ does not, and RL executes one probe fewer and travels more; the two instruments and episode sets
differ, so we report this as an observation only. Second, $g_T$ places G\* below both learners while BI places it above,
and saturation at the cap is too rare on test3 to account for this; the contrastive estimate and the grid posterior
rank histories differently, which limits what H2 can say about task success. Third, on test3 the learned policies were
not shown to exceed a travel-nearest heuristic, while that heuristic trails G\* in both success and BI; the pre-written
reading is reported without its flat-task clause.

**Relation to prior work.** Amortized design methods \cite{foster2021deep, blau2022optimizing} and imitation of
information-gathering experts \cite{choudhury2017adaptive, nguyen2024amortized} propose learned policies as replacements
for online design or planning; our controlled single-cell result is a caution that, for contact sensing with a joint
identity × pose belief and travel cost, neither route reached the online planner with a belief-free head. Semi-amortized
designs that refine a learned proposal online \cite{hedman2025step}, or nested-filter amortization
\cite{iqbal2024recursive}, are natural directions, although our latency split shows that the particle filter itself
bounds the speed-up of any scheme that keeps it in the loop. For practitioners, the missing comparison is against a
smaller filter: until reduced-size G\* is scored for accuracy, the per-decision ratio against full-size G\* overstates
what amortization buys.

**Open questions.** Would held-out evaluation on student-visited states confirm covariate shift? Does the
long-training student close part of the D3 deficit? Would an equivalence test or a variance decomposition sharpen H2,
and would more seeds give it useful power? Do the findings hold in a cell where travel binds, in other cells such as
the asymmetric set or κ = 0, and with a full-action screen for H3?

## 7 Limitations

- **Single cell, stay-and-probe regime.** All learning results are S12 only, with $n^\* = 4$, a cell in which G\*
  travels 6.1° per episode on average; findings may not transfer to regimes where travel binds. S0 and A12 appear only
  as pilot rows (provisional PASS on incomplete random rows, n = 162 / 199 / 197 of 200 for S0 / S12 / A12).
- **H3 scope.** H3 measures headroom over a reduced greedy completion and over 32 screened first actions, not over all
  feasible actions and not to the optimum. The instrument checks rest on one notch construction (checked in two forms,
  both re-used from the previous iteration) plus a zero-gap bank; there is no in-domain positive control, $V_{LA}$'s
  selection bias was not measured, and the bias guard is one-sided. The Hold threshold was registered after a
  near-identical previous estimate was known.
- **Evaluator not shown converged.** The evaluator gate failed: the one counted flip (an A12 B-fan episode) occurred
  with the true-identity mass unchanged (0.228) and outside the [0.45, 0.55] tie band; the JSON does not record which
  part of the success criterion changed. Sub 4 → 8 flips the success outcome of 7.5 % of the 200 S0 calibration
  episodes, and no finer grid was checked. Sub-8 read-out costs 40.6 s per episode, which limited the grid-scored rows
  (G5′ re-reads, D3/D3-B, test rows on 300 episodes).
- **Comparators not shown tuned.** The RL sweep used 4 configurations on 1 seed and was selected on the trainer's own
  validation stream rather than val3, with 50,048-episode sweep runs; the selected configuration has the largest
  learning rate in the sweep and won by 0.919 nats of final validation ball-sPCE, so the optimum may lie beyond the grid.
  The distillation grid also had 4 configurations on 1 seed and round 0, and its winner, also the largest learning rate,
  won narrowly.
- **Unmatched optimisation budgets.** Student rounds stopped after 4–16 epochs (3.2–27.6 s), while each RL seed trained
  for 200,064 episodes; the long-training row is pending.
- **RL behaviour differs.** RL executes exactly 3 probes and travels 23.0–25.8° per episode against the student's 4
  probes and 1.5–2.0°, with near-deterministic final policies.
- **Low power.** Three seeds per learner; H2 had about 80 % power only for a true Δ near 0.57 nats, and success
  intervals at n = 300 are several points wide.
- **Label-fit thresholds are coarse** (top-1 ≈ 0.52 counts as "fits"), and the held-out set is teacher-visited.
- **Latency.** The latency protocol is incomplete (six configurations with CI half-widths above 10 %, two machines
  pooled, no core pinning), the timed student is the round-0 checkpoint, the per-episode latency was not measured, and
  the accuracy of reduced-size G\* was not measured.
- **Cross-split comparisons are unpaired.** G\* success is 0.426 on pilot3, 0.446 on val3 and 0.4267 on test3.
- **Missing pre-registered report items.** Training compute including teacher labelling, and the teacher noise-floor
  $\bar R$, are not reported; without the latter, the scale of $\bar R$ ≈ 0.18 is unknown. The teacher tie fraction is
  reported (0.0 in 210 logged evaluations).
- **Incomplete rows.** The belief-input validation (298 episodes) and the sub-8 pilot re-reads are provisional, and the
  long-training student row is running.
- **No physical demonstration.** All results are in simulation with planar objects; held-out object shapes were not
  tested.

## 8 Conclusion

We asked two questions about active tactile localization under travel cost: how much one-step look-ahead adds over
greedy cost-aware information-gain touch selection, and whether that greedy planner can be amortized by a learned
policy, through distillation from the planner or RL on the same objective. In a pre-registered characterisation on a
single cell, which turned out to be a stay-and-probe regime in which the planner moves the finger little, the answers
are as follows. Greedy leaves little one-step headroom among the screened first actions: rollout over the reduced
greedy completion gains at most about 2.2 % of the remaining expected ball information (one-sided 95 % bound),
replicating an earlier estimate. Neither amortization route was shown to reach the planner with an identical
belief-free head; the distilled student failed its non-inferiority gate, RL trails the planner on test, and neither was
shown to exceed a belief-free stay-and-fan heuristic. Dense planner supervision did not improve on RL on RL's own
objective, a non-detection with power only for large effects, not a demonstration that the two are the same. The
learned head is far cheaper per decision than full-size G\*, not at matched accuracy and not compared with a smaller
filter, and candidate pruning cannot recover the planner's cost because the particle filter bounds it. Concrete next
steps are a cell in which travel binds, a full-action screen and an in-domain positive control for the headroom
estimator, a longer-trained student (running), evaluation on student-visited states, more seeds with an equivalence
test for the distillation–RL comparison, accuracy for reduced-size planners, and semi-amortized schemes that keep a
cheaper filter in the loop. All hypotheses, thresholds and readings were fixed before the runs, and the scope is one
shape set, one travel cost and four probes.

## Appendix A: Pre-registered gate record

This appendix holds the gate bookkeeping that routed the study to outcome row 4. Rows use the design documents' gate
names: Cal′ (budget calibration), E′ (evaluator resolution), G5′ (pilot margins and H★), Lat′ (latency), D3 and D3-B
(learnability on val3), and the H2 and H3 decisions.

**Table A1. Pre-registered gates and decisions (S12 unless stated).**

| Row | Item | Measured | Rule | Outcome |
|---|---|---|---|---|
| R1 | Cal′ n\*, verification | S: G\* success 0.605 at κ = 0, τ = 4 → n\* = 4 (0.62 at sub 8); mean probes 3.96 | probes within n\* ± 0.3 | pass |
| R2 | E′ evaluator (16 episodes, S12 and A12) | mean \|ΔBI\| 0.0126 nats; 1 counted flip, A12 B-fan (true-identity mass 0.2282 / 0.2281) | \|ΔBI\| ≤ 0.02, no counted flip | fail → sub 8 |
| R3 | G5′ pilot | G\* 0.426 ± 0.0221 (n = 500); random 0.0754 (n = 199 of 200, provisional); D_c 0.3506 (provisional); δ 0.04 | G\* ≥ random + 10 pp; non-degenerate | provisional pass (note 2) |
| R4 | Lat′ / H1-fb | G\* full / pruned-16 = 3.22 | ≥ 10 | H1-fb withdrawn |
| R5a | D3, first attempt | Δ̂_succ −5.87 pp (thr −1.43); Δ̂_BI −0.199 (thr −0.15); seeds −4.2 / −8.0 / −5.4 pp | (i)–(iii) | fail |
| R5b | D3, remedy | −4.40 pp (thr −1.68) ✗; −0.096 (thr −0.15) ✓; seeds −4.6 / −4.6 / −4.0 pp ✗ | (i)–(iii) | fail → H1 dead |
| R5c | D3-B belief input (298 episodes, incomplete) | Δ̂_succ −19.9 pp (thr −0.78); Δ̂_BI −1.01 (thr −0.15); seeds −21.5 / −17.1 / −21.1 pp | as D3 (report-only) | fail (provisional) |
| R6 | H2 | Δg_T +0.00023 nats, LB −0.3103 | LB > +0.10 | rejected |
| R7 | H3 | UB95 G(12) = 0.0221; bias ratio 0.957 | UB < 0.03; ratio ≤ 1.02 | Hold |

**Notes.** (1) The D3 files carry ε_S12 = 0.314266 from an earlier pilot read, against 0.314507 in the current one; the BI threshold is
the −0.15 floor under either value. (2) Provisional PASS in all 3 cells on incomplete random rows (n = 162 / 199 / 197 of
200 for S0 / S12 / A12); D_c ≥ 0.35 everywhere, so δ_c = 0.04 (cap) is unlikely to move. Current sub-8 values, all
provisional while the re-reads run: S0, G\* 0.66 (n = 500), random 0.2284 (n = 162), D_c 0.4316, H★ B-spread; S12, G\*
0.426, random 0.0754 (n = 199), D_c 0.3506, H★ B-fan (0.403, n = 154), flat-screen flag set; A12, G\* 0.47, random
0.0305 (n = 197), D_c 0.4395, H★ B-fan.

**Routing.** R5a and R5b failed, so H1 was never tested on test3; R4 withdrew H1-fb; the record therefore reached row 4,
under which R6, R7 and the encoder sentence are the remaining decisions. R1–R3 and R5c are gate or report-only data.

<!-- WORD COUNTS (python, whitespace tokens, HTML comments and "## " heading lines excluded; tables and equations
included; subsections counted in their section)
  Abstract: 249
  1 Introduction: 964
  2 Related Work: 587
  3 Problem and Methods: 1880
  4 Experimental Protocol: 1064
  5 Results: 2914
  6 Discussion: 756
  7 Limitations: 552
  8 Conclusion: 290
  Appendix A (gate record): 500
  Main body total (excluding Abstract and Appendix): 9007
  Total including Abstract and Appendix: 9756
  Remaining placeholder: [PENDING:long_student] (Section 5.2, by instruction; readings pre-written).

CHANGE LOG (stage 19, review item -> change)
- Mismatch 1 (stale 62/199/161) -> 162 / 199 / 197 of 200 (S0 / S12 / A12) in Appendix A note 2 and Section 7.
- Mismatch 2 (pinned core) -> Section 4 and Section 7: threads = 1, no core pinning; BLAS thread variables named.
- Mismatch 3 (E' cells) -> Section 4 methods note and Table A1 R2: 16 episodes from S12 and A12; counted flip is A12 B-fan.
- Mismatch 4 (latency checkpoint) -> Section 4 and Table 2c caption: timed student is the round-0 checkpoint of seed 501.
- Mismatch 5 ([CONST?]) -> PPO clip 0.2, 4 epochs (Section 3.4, Table 0); Python 3.12.15, numpy 2.5.4; GitHub-hosted
  standard runners, CPU model not logged.
- Mismatch 6 ([PENDING] G5'/D3-B) -> filled with provisional sub-8 values (R3, note 2, Section 5.5 B-fan 0.403 n = 154)
  and the incomplete D3-B read (298 episodes, -19.9 pp, -1.01 nats, all fail), marked provisional.
- Mismatch 7 (context) -> Section 3.4 documents the 5-d context incl. absolute cos/sin phi_t; Adam re-initialised per round.
- S1 (travel barely happens) -> new Section 5.3 + Table 2d (travel, probes, zero/>1-step moves, g_T at cap); stay-and-probe
  regime stated in Abstract, Introduction, Section 3.1, 5.1, Discussion, Limitations, Conclusion; title left to owner
  (comment). Reviewer's "13.5 deg" not used.
- S2 (student under-training) -> epochs 4-16 / 3.2-27.6 s reported; encoder sentence qualified (under-optimisation not
  excluded); long-training row placed as [PENDING:long_student] with both pre-written readings.
- S3 (32 of 512 screened; checks share one construction) -> Abstract, C1, Sections 3.3, 5.1, 6, 7 narrowed to the screened
  set; (a)/(c) described as one construction in two forms re-used from v2 plus a zero-gap bank; V_LA selection bias and
  one-sided guard discussed.
- S4 (v2 G(12) known before threshold) -> disclosed (0.0146, UB 0.0208) in Introduction, Section 4, 5.1; H3 called a replication.
- S5 (g_T vs BI; saturation) -> Section 5.4: test3 saturation G* 5.8 %, students 2.4-3.4 %, RL 0.4-1.2 %; trainer sat_frac
  22.7-31.3 % flagged as a different quantity; RL 3 probes, entropy 0.0020-0.0125. Reviewer's 15-26 % not used.
- S6 (thin RL sweep, low power) -> Limitations: edge-of-grid lr for RL and distillation grids; power statement; H2 read as
  a feasibility probe.
- S7 (reduced-G* baseline) -> Sections 4, 5.6, 6, 7: reduced G* timed, accuracy not measured; ratio stays "per decision,
  vs full-size G*". Reviewer's 10-50x not used.
- S8 (B-fan) -> Abstract and Discussion carry pre-written reading (b); never "zero-travel".
- S9 (gate bookkeeping) -> Table 1 and routing moved to Appendix A (Table A1); evaluator demoted from C4 to a methods note.
- S10 (unexecuted pre-registered items) -> Section 4 paragraph (Holm family, TOST vs G*, BC/abs-frame rows, R_b) with
  routing reason.
- S11 (tie fraction) -> reported: 0.0 in 210 logged evaluations (Section 5.2, Section 7).
- Presentation (repetition, "equal" wording) -> "not at equal accuracy" -> "not at matched accuracy"; repeated verbatim
  phrases reduced; "near-equal" -> "near-tied".
- Not addressed (need new runs, owner/next loop): travel-binding cell, more cells/seeds, full-512 H3 screen, in-domain
  positive control, V_LA bias check, reduced-G* accuracy, extended RL sweep, sub-16 evaluator re-read.
-->
