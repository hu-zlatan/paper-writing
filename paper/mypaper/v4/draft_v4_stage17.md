```text
FIGURE 1 PROMPT (v4; generated schematic for panels A-C, panel D plotted separately from the results JSON)

Target model: Nano Banana 2 (image generation). Output: one wide scientific schematic figure, aspect ratio 3:1 (full
text width of a two-column robotics paper, about one third of a page tall), pure white background (#FFFFFF), clean
flat-vector style, no photorealism, no 3D shading, no gradients, no drop shadows, no textures, no decorative icons
beyond those listed, no people, no robot arm, no logos, no watermark. Uniform line weights (thin 1.5 px outlines,
2.5 px arrows). Font: one clean sans-serif (Helvetica/Arial-like), dark grey #222222, all text horizontal, no text
other than the exact labels quoted below, spelled exactly as given (keep Greek letters and symbols exactly: φ, ψ, κ,
Δφ, π, *, ×, °). Exactly two accent colours: BLUE #1F6FB4 = information / probing, ORANGE #E07B1A = travel / cost.
Neutral greys for objects (#9A9A9A fill, #555555 outline). Four panels side by side, left to right, separated by
generous white space, no boxes around panels A, B and C. Each panel has a bold panel letter in its top-left corner:
"A", "B", "C", "D". Approximate widths: A 24 %, B 26 %, C 30 %, D 20 %.

PANEL A - "the task", top-down view:
 1. Centre: one flat irregular polygon (6 main sides, one small rectangular notch cut into its upper-right edge),
    solid grey fill #9A9A9A, outline #555555, seen from directly above.
 2. Around the polygon, a dashed thin grey square (#888888, dash 4-3) slightly larger than the polygon: the
    position-uncertainty box. No label on it.
 3. Three or four faint ghost outlines of the same polygon and of one slightly different polygon (same size, notch on
    a different edge), each shifted and rotated by small amounts, very light grey outlines (#CFCFCF, no fill, 30 %
    opacity), overlapping the solid polygon. Small label beneath the box: "belief over identity × pose".
 4. A thin solid grey circle (#777777) centred on the polygon, radius about 2.2× the polygon size: the stand-off
    circle. No label on the circle.
 5. A small filled dark dot (#222222) on the circle at about 8 o'clock: the fingertip. Label next to it, outside the
    circle: "φ_t".
 6. A curved ORANGE arrow running along the circle clockwise from the fingertip (8 o'clock) over the top to about
    1 o'clock, drawn just outside the circle line so both stay visible, arrowhead at the 1 o'clock end. Orange label
    outside the circle: "travel cost c(a) = 1 + κ|Δφ|/π". A small open orange circle at the arrow end, labelled "φ′".
 7. From φ′, a straight BLUE arrow pointing inward toward the polygon, tilted about 15° away from the radial
    direction; a thin dotted grey radial reference line from φ′ to the centre shows the tilt, and a small arc between
    the radial line and the blue arrow is labelled "ψ" in blue.
 8. The blue arrow ends exactly on the polygon edge at a small filled blue diamond (contact) with a short blue tick
    perpendicular to the edge (measured normal). Small blue label: "contact + normal".

PANEL B - "two travel regimes", two small schematic copies of the stand-off circle side by side (no polygon detail
needed: a small grey polygon silhouette in each centre is enough):
 1. Left copy, title above it: "S12, κ = 12". The fingertip dot sits at about 9 o'clock; from it, a fan of four short
    BLUE probe arrows all start at the same point on the circle and point inward at slightly different tilts (a fan).
    Almost no orange: only one very short orange arc (a few degrees) next to the dot. Label under the circle:
    "6.1° / episode".
 2. Right copy, title above it: "S2, κ = 2". Four BLUE probe arrows start from four different points spread around
    the circle (about 9, 11, 1 and 3 o'clock), each pointing inward; consecutive start points are joined by ORANGE
    arcs drawn just outside the circle. Label under the circle: "46.9° / episode".
 3. One small grey italic word centred under both copies: "schematic".

PANEL C - "three ways to pick the next touch", block diagram:
 1. At the far left, vertically centred, a small cloud of about 20 tiny grey dots inside a rounded outline: the
    belief icon. Label below: "belief b".
 2. From it, three thin grey arrows fan out into three horizontal lanes stacked top to bottom; each lane is a row of
    rounded rectangles (white fill, #555555 outline) joined by thin grey arrows.
 3. Lane (i), top. Bold lane title at its left: "(i) Greedy G*". Blocks: "EIG / c over 512 actions" (inside, a tiny
    row of 12 thin vertical BLUE bars of varying height, one taller and outlined darker) -> "argmax".
 4. Lane (ii), middle. Bold title: "(ii) One-step look-ahead". Blocks: "screened first actions" -> a small tree glyph
    (one root branching to four children, each continuing as a short dashed line to a leaf dot) with the label under
    it: "completed by reduced greedy" -> "best first action".
 5. Lane (iii), bottom. Bold title: "(iii) Learned policy". Blocks: a cluster of 4 small blue points with short tick
    marks, labelled "touch history (finger frame)" -> "DeepSets" -> "512 masked logits" (inside: a tiny row of 12
    thin bars, a few greyed out to suggest masking).
 6. Two training arrows enter the "DeepSets" block:
    - a SOLID BLUE arrow coming down from lane (i)'s "EIG / c over 512 actions" block, blue label:
      "DAgger: G* score labels";
    - a DASHED ORANGE arrow entering from below, orange label: "PPO: reward = ball-sPCE".
 7. No other arrows and no numbers other than "512" (twice).

PANEL D - headline data inset: leave as an EMPTY placeholder, a plain white rectangle with a thin light-grey border
(#DDDDDD), the panel letter "D" in its top-left corner and NOTHING else inside (no axes, bars, numbers or text). The
inset is plotted separately from the results JSON and pasted into this frame; the generator must not draw any chart,
value or label here.

Global: balanced composition, generous margins, all labels legible when printed 17 cm wide, no overlapping text, no
clutter, no title above the figure, no caption inside the image.

---
PANEL D INSET (plotted with matplotlib, not generated; values copied from the results JSONs):
 Main plot: grouped bars of test3 0-299 success (sub-8 evaluator), two groups "S12" and "S2"; bars G* / student / RL /
 B-fan (B-fan hatched, labelled "exploratory"). Whiskers are paired ci95 relative to G*, drawn on the learner bar.
  S12 (v3:14_m4_analysis): G* 0.4267 (rows.gstar.success); student 0.3822 (rows.student.success), whisker from
   diffs["student-gstar:success"].ci95 = [-0.0933, +0.0056]; RL 0.3567 (rows.rl.success), whisker from
   diffs["gstar-rl:success"].ci95 = [+0.0022, +0.1367] sign-flipped; B-fan 0.36 (exploratory_b_fan.success), whisker
   from exploratory_b_fan["b_fan-gstar:success"].ci95 = [-0.12, -0.01].
  S2 (v4:14_s2_analysis.test3_sub8): G* 0.5533 (rows.gstar.success); student 0.4511 (rows.student.success), whisker from
   diffs["student-gstar:success"].ci95 = [-0.1656, -0.0433]; RL 0.4233 (rows.rl.success), whisker from
   diffs["gstar-rl:success"].ci95 = [+0.0644, +0.1944] sign-flipped; B-fan 0.37 (rows.b_fan.success), whisker from
   diffs["b_fan-gstar:success"].ci95 = [-0.2467, -0.12].
  No random bar (S2 random row incomplete: [PENDING:v4:14_s2_analysis.test3_sub8.rows.random]).
 Side strip: H3 one-sided 95 % UB of G(kappa): 0.0221 at kappa = 12 (v3:12_g2_analysis.k12.ub95) and 0.0197 at
  kappa = 2 (v3:12_g2_analysis.k2.ub95), dashed line at the pre-registered Hold threshold 0.03.
 Caption note: "paired ci95, uncorrected; one cell per regime; no cross-cell test".

Draft caption:
Figure 1. Cost-aware touch selection in two travel regimes. (A) A finger on a stand-off circle chooses where to move,
paying travel cost proportional to |Δφ|, and which way to probe; the belief is a particle set over identity and planar
pose. (B) At κ = 12 the cost-aware greedy planner G* mostly stays and fans its probes (6.1° travel per episode); at
κ = 2 it travels (46.9°). Traces are schematic. (C) We compare G*, a one-step look-ahead over a reduced greedy
completion, and one belief-free DeepSets policy trained by DAgger on G*'s scores or by PPO on ball-sPCE. (D) One-step
look-ahead gains ≤ 2.2 % at κ = 12 (one-sided 95 % bound), and neither learned policy was shown to reach G* in either
regime (test success, paired ci95; one cell per regime, preliminary; B-fan exploratory).
```

# Cost-Aware Information-Gain Touch Selection under Travel Cost: Look-Ahead Headroom and Learnability in a Stay-and-Probe and a Travelling Regime

## Abstract

Active tactile localization chooses the next touch from a belief over object identity and pose, and when moving the
finger costs time, that choice trades information against travel. We ask how much headroom one-step look-ahead leaves
over greedy cost-aware information-gain touch selection (G\*), and whether G\* can be amortized by a policy distilled
from it or trained by reinforcement learning (RL) on the same objective. The task uses a joint identity × planar-pose
particle belief and a finger on a stand-off circle with travel cost $c(a) = 1 + \kappa|\Delta\phi|/\pi$. We study two
cells: S12 (κ = 12), a stay-and-probe regime in which G\* moves the finger 6.1° per episode on average, and S2 (κ = 2),
in which it travels 46.9°. Over 32 screened first actions, one-step rollout over a reduced greedy completion gains at
most 2.2 % of the remaining expected ball information at κ = 12 (one-sided 95 % bound). With one belief-free DeepSets
head, neither the DAgger-distilled student nor PPO was shown to reach G\* in either cell: the student failed its
pre-registered non-inferiority gate twice in S12 and once in S2. Distillation was not shown to be better than RL on
RL's own objective in either cell. In S2 the student exceeds a stay-and-fan heuristic on test success (+8.1 pp,
exploratory). Reduced-size G\* at 21–46 ms per decision does not exceed the distilled students (exploratory). The
study is pre-registered, with one cell per regime, and its results are preliminary.

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
reaches the planner, and whether dense supervision does better than RL on RL's own objective with the same head.

**Two regimes.** Our first design iteration studied one cell, S12 (shape set S, κ = 12, four probes). It turned out to
be a *stay-and-probe* regime: on test, 79.3 % of the planner's between-probe moves are zero and its mean travel is
6.1° per episode, so the motivating scenario of a finger stranded far from the informative region has little room to
occur. We therefore added a second cell, S2 (κ = 2, budget recalibrated so that the planner still executes four
probes), in which the planner travels 46.9° per episode on average. Both cells use the same planner, the same
learners and the same head.

**Findings.** In S12, one-step rollout over a reduced greedy completion gains at most 2.2 % of the remaining expected
ball information over the 32 screened first actions (one-sided 95 % bound); the κ = 2 row of the same estimator,
measured in the S2 cell, is also small. Neither learner was shown to reach G\* in either regime. In S12 the distilled
student failed its pre-registered non-inferiority gate on the first attempt and after its one remedy. In S2 the
student was not shown to reach G\* either: on validation the success deficit was −2.80 pp against a threshold of
−1.46 pp, and on test episodes 0–299 the gap is −10.2 pp (ci95 [−16.6, −4.3]). On RL's own objective, the
contrastive return $g_T$, no advantage of distillation was detected in either cell; in S2 the point estimate favours
RL (exploratory). In S2 the student exceeds a belief-free stay-and-fan heuristic on success and ball information,
which it did not do on success in S12 (exploratory, uncorrected, no cross-cell test). At logged median per-decision
latencies of 20.8 and 46.0 ms, neither of two reduced-size G\* configurations exceeds the distilled students: both are
lower on ball information and success is unresolved.

**Contributions.**
- **C1.** A pre-registered bound on one-step look-ahead headroom over cost-aware greedy touch selection at κ = 12 over
  the screened first actions with a reduced greedy completion (H3, Hold), with κ = 0 and κ = 2 rows, instrument
  checks and an on-belief bias check.
- **C2.** A learnability study of one belief-free relative head in a stay-and-probe cell (two gate attempts) and a
  travelling cell (one gate), with a behavioural diagnosis of finger travel and probe use.
- **C3.** A comparison of planner distillation against RL on RL's own objective in both cells, the observation that
  this objective and the grid posterior order the planner differently, and an exploratory separation of the student
  from a stay-and-fan heuristic in S2.
- **C4.** A methods note on evaluator resolution, the $g_T$ / ball-information disagreement about G\*, and a
  validation/test discrepancy in S2.
- **C5.** A per-decision cost analysis: a latency decomposition of G\* and an exploratory comparison of reduced-size
  G\* with the students at logged latency.

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
\cite{seminara2019active}. Per-step (myopic) selection is the norm in this line. How much it leaves on the table under
travel cost, and whether the answer depends on whether the selector actually travels, is rarely measured; C1 and C2
address both for one task and two regimes. Greedy cost-aware selection itself is established, and we propose no new
selector.

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
candidates, not the gap to the optimal policy.

**Amortized and learned active sensing.** Deep adaptive design trains a design network on contrastive information
bounds so that each decision is a forward pass \cite{foster2021deep}; implicit and RL formulations remove the need for
likelihoods or differentiable simulators \cite{ivanova2021implicit, blau2022optimizing}; semi-amortized variants
refine the policy online \cite{hedman2025step}; nested particle filters amortize design in dynamical systems
\cite{iqbal2024recursive}; and transformer policies amortize inference and acquisition jointly \cite{huang2026aline}.
A recent review covers the field \cite{rainforth2024modern}. In touch, RL agents explore for recognition with rewards
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
planner; amortization claims are informative only against that alternative, which C5 examines at logged latency.

## 3 Method

### 3.1 Task, belief, metrics and the two cells

**State and observations.** The object is a planar polygon with identity $k \in \{1,\dots,K\}$ from shape library S
(K = 8 near-symmetric base/variant pairs) and unknown pose, so the state is $s = (k, x, y, \theta)$ with a uniform
prior over identity, position in a ±15 mm box and orientation, and $G_k$ is the exact symmetry group of shape $k$. A
probe returns either a contact point and a surface normal, both with Gaussian noise ($\sigma_p$ = 1.0 mm,
$\sigma_n$ = 5°), or a miss $y = \varnothing$. Every method uses the same ε-softened likelihood
$p_\varepsilon(y \mid s, a)$.

**Actions and travel cost.** The finger rests on a stand-off circle at angle $\phi_t$, with a start angle shared by
all methods on an episode. An action $a = (\phi', \psi)$ selects one of 64 target angles $\phi'$ (grid step 5.625°)
and one of 8 approach offsets $\psi$, so $|\mathcal{A}| = 64 \times 8 = 512$. The finger travels the shorter way to
$\phi'$, probes inward along direction $\phi' + \pi + \psi$ with a guarded stroke, and then $\phi_{t+1} = \phi'$. In
units of one stroke,

$$c(a) = 1 + \kappa\,\frac{|\Delta\phi|}{\pi}, \qquad \Delta\phi = \mathrm{wrap}(\phi' - \phi_t) \in (-\pi, \pi],$$

so κ is the time to travel half the circle. With remaining time $\tau_{\mathrm{rem}}$, the feasible set is
$\mathcal{F}(\tau_{\mathrm{rem}}) = \{a : c(a) \le \tau_{\mathrm{rem}}\}$, every method chooses only within it, and the
episode ends when no action is feasible.

**Probe-matched budgets and the two cells.** The budget $\tau$ is calibrated (gate Cal′) so that G\* executes $n^\*$
probes on average; for set S, $n^\* = 4$. The two cells differ only in the price of moving:

- **S12** = (S, κ = 12, τ = 4.9, $n^\* = 4$). At this budget G\* executes 3.96 probes on average over 200 calibration
  episodes. Less than one stroke-unit remains beyond four unit-cost probes, so any substantial move costs a probe.
- **S2** = (S, κ = 2, τ = 4.7, $n^\* = 4$). The calibration episodes show a mean unbudgeted travel time of 0.7257
  stroke-units for G\*, and a move across the circle costs at most 2 stroke-units.

The H3 row at κ = 2 was measured with exactly this configuration (set S, κ = 2, τ = 4.7, $n^\* = 4$), so it is the S2
cell's headroom evidence.

**Metrics.** From the evaluator's posterior after the last probe, the identity estimate $\hat k$ is the maximum-mass
identity and the pose estimate is refined locally. Success requires the correct identity, a position error below
5 mm and an orientation error below 5° modulo $G_{k_0}$. With $B(s_0)$ the success ball around the true state, the
ball information is

$$\mathrm{BI}(h) = \log \hat P(B(s_0) \mid h) - \log P(B(s_0)) \quad \text{[nats]}.$$

BI is the shared information target of every information-based method below.

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
$C$, which is why pruning candidates alone bounds the achievable speed-up (Section 5.6).

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
not measured; no bias-corrected G is reported.

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
recorded but not used to stop. S12 uses seeds 511–513 and S2 seeds 611–613.

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
belief, so it is the natural reference for a stay-and-probe regime and a stress test for a travelling one.

## 4 Experiments

**Pre-registration and routing.** Hypotheses, thresholds, the outcome map and a list of analyses not allowed after the
run were frozen before any S12 run, and the main-run set was frozen before any test episode. Three hypotheses were
registered: H1, a distilled student non-inferior to G\* (with a fallback H1-fb in which the student prunes G\*'s
candidates); H2, distillation beating RL on RL's own objective; and H3, small one-step headroom. The S12 record
reached row 4 (characterisation): D3 failed on the first attempt and after its one remedy, so H1 was never tested on
test, and H1-fb was withdrawn at the latency gate. An amendment written before any S2 run added the S2 cell with three
fixed readings: the learnability gate D4 (same rule as D3), H2-S2 (same rule as H2), and an exploratory
reduced-planner comparison E5 on S12; it allowed no remedy round. The amendment changes no S12 verdict.

**Splits.** Disjoint episode streams: calibration (200 episodes per configuration), pilot3 (margins and H★), val3
episodes 0–499 (D3, D4), test3 episodes 0–499 ($g_T$ for H2 and H2-S2, S12 behaviour) and test3 episodes 0–299
(success and BI rows, S2 behaviour, E5). Within a split, all methods run on the same episodes with the same initial
state, start angle and observation stream (paired design). S2 success, BI and travel numbers are on test3 0–299; S12
travel numbers are on test3 0–499 (B-fan: 0–299). H3 uses 100 G\*-reached beliefs per κ.

**Evaluator (methods note).** Success and BI are read from an adaptive grid posterior that rebuilds each history
exactly. Its gate E′ compared grid subdivision 4 with 8 on 16 episodes and failed: one counted success flip occurred
(mean |ΔBI| 0.0126 nats, maximum 0.0523). Subdivision 8 is therefore used for every reported success and BI number.
Between subdivisions 4 and 8 the success outcome flips on 7.5 % of 200 set-S calibration episodes, and no finer grid was
checked, so success differences of a few points should be read with that in mind. $g_T$, H3, latency and label fit do
not use the grid.

**Statistics.** Paired differences use a crossed episode × seed bootstrap with B = 10,000. H2 bounds are the 5 % / 95 %
quantiles (one-sided 95 %); ci95 contrasts are the 2.5 % / 97.5 % quantiles (two-sided); the D3/D4 standard error is
the SD of an episode × student-seed bootstrap. There is no multiplicity correction. The S2 test rows and E5 are
descriptive and exploratory. With three seeds per learner, the seed dimension of the bootstrap is coarse.

**Gates D3 and D4.** On 500 paired val3 episodes with three student seeds, the gate passes iff (i)
$\hat\Delta_{\mathrm{succ}} \ge \max(-2\,\mathrm{pp},\ -\delta + 1.645\,\mathrm{SE}\sqrt{0.5})$; (ii) the same for BI
with ε and a −0.15-nat floor; (iii) every seed's $\hat\Delta_{\mathrm{succ}} > -\delta$. Here δ = 0.04 (the cap). S2 has
no pilot margin cell, so δ is borrowed from S12 and only the −0.15 BI floor applies. Because the margin in (i) adds
$1.645\,\mathrm{SE}\sqrt{0.5}$ to −δ, the threshold becomes stricter as the paired standard error grows.

**H2 and H3 rules.** H2 (and H2-S2) passes iff the one-sided 95 % lower bound of $g_T(\text{student}) - g_T(\text{RL})$
on test3 0–499 exceeds +0.10 nats. H3 is Hold iff the one-sided 95 % UB of G(12) is below 0.03, Kill iff the lower
bound exceeds 0.05, otherwise Inconclusive. A near-identical estimate from the previous design iteration was known
when the 0.03 threshold was registered, so H3 is a pre-registered replication on the 64 × 8 action set.

**Behaviour diagnostics (report-only).** Per episode we log total finger travel, the number of probes, the fraction of
between-probe moves that are zero or exceed one grid step, whether $g_T$ reached its cap, and in S2 the per-seed
Pearson correlation of the student's and G\*'s per-episode travel and the number of episodes with identical action
sequences.

**Implementation.** Everything is numpy with hand-written backpropagation and single-threaded BLAS, run on
GitHub-hosted standard runners (CPU model not logged); distillation training ran in a separate sandbox runtime.
Latency follows a fixed protocol (Lat′): configurations timed interleaved on the same S12 pilot decision states with
one thread, 1,000 decisions on 253 pilot episodes from two runner jobs. E5 latencies are medians of per-decision
latencies logged during the eval3 runs on free runners, not Lat′ measurements.

**Table 1. Settings (design constants; RL configuration from the S12 sweep).**

| Component | Setting |
|---|---|
| G\* | N = 2,000 particles, C = 512 candidates, M = 64 outcome samples |
| E5 reduced G\* | g125_512_16 (N = 125, C = 512, M = 16); g500_512_4 (N = 500, C = 512, M = 4) |
| Distillation loss | Adam, lr 1e-3, β_T = 4, λ = 0.5, batch 256; ρ = 0.05 in $\bar R$ |
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
| R1 | Cal′ budgets | S12 τ = 4.9 (G\* 3.96 probes); S2 τ = 4.7 | $n^\* = 4$ probes | pass |
| R2 | E′ evaluator | mean \|ΔBI\| 0.0126 nats; 1 counted flip | no counted flip | fail → sub 8 |
| R3 | G5′ S12 pilot | G\* 0.426 (n = 500), random 0.075 (n = 200); D_c 0.351; H★ B-fan | G\* ≥ random + 10 pp | pass |
| R4 | Lat′ / H1-fb | full G\* / pruned-16 = 3.22 | ≥ 10 | H1-fb withdrawn |
| R5a | D3 S12, first attempt | Δ̂_succ −5.87 pp (thr −1.43); Δ̂_BI −0.199 (thr −0.15); seeds −4.2 / −8.0 / −5.4 pp | (i)–(iii) | fail |
| R5b | D3 S12, remedy | −4.40 pp (thr −1.68) ✗; −0.096 ✓; seeds −4.6 / −4.6 / −4.0 pp ✗ | (i)–(iii) | fail → H1 dead |
| R5c | D3-B belief input (300 episodes) | −20.1 pp (thr −0.75); −1.02 nats; seeds −21.7 / −17.3 / −21.3 pp | as D3 (report-only) | fail |
| R5d | D4 S2 | −2.80 pp (thr −1.46) ✗; −0.105 ✓; seeds −3.6 / −2.8 / −2.0 pp ✓ | (i)–(iii) | fail |
| R6 | H2 S12 | Δg_T +0.0002 nats, LB −0.3103 | LB > +0.10 | rejected |
| R6b | H2-S2 | Δg_T −0.4452 nats, LB −0.7485, UB −0.1616 | LB > +0.10 | not detected |
| R7 | H3 | UB95 G(12) = 0.0221; bias ratio 0.957 | UB < 0.03; ratio ≤ 1.02 | Hold |

All D4, test3, H2 and E5 blocks are complete. The S2 test3 random anchor is not: 215 of 300 episodes have run, so it
enters no contrast.

## 5 Results

### 5.1 H3: one-step look-ahead headroom is small among the screened actions

H3 is **Hold**. At κ = 12, one-step rollout over the reduced greedy completion gains at most 2.2 % of the remaining
expected ball information over the 32 screened first actions (G(12) = 0.01624, one-sided 95 % UB 0.0221 < 0.03). In
absolute terms the gap is 0.0414 nats on a mean $V_{G^\*}$ of 2.506 nats (Table 3). The κ = 2 row was measured in the
S2 cell and is the headroom evidence nearest to the travelling regime: G(2) = 0.01418 (UB 0.01974); it is reported,
not a separate test. The point estimates follow the ordering G(0) ≤ G(2) ≤ G(12), which was not tested, and even the
largest is small. The look-ahead picks a different first action from G\* on 62 % of beliefs at κ = 12 yet gains little
on average, which is consistent with near-ties among the top actions; the record does not separate near-ties from
selection noise. The result replicates the previous design iteration's estimate on a coarser action set.

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

Table 4 establishes the regimes before any learning result. In S12, G\* moves the finger 6.1° per episode on average
(test3 0–499), 79.3 % of its between-probe moves are zero and it executes 3.962 probes. In S2 it travels 46.9° per
episode (test3 0–299) and executes 3.873 probes. B-fan logs the same mean travel, 1.454°, in both cells. RL ends at
exactly 3 probes in both cells and travels 136.8° per episode in S2 and 23.0–25.8° in S12. Random travels 172.2° in S2.

**Table 4. Behaviour (report-only). S12: test3 0–499 (B-fan 0–299); S2: test3 0–299. Travel is logged total finger
travel per episode.**

| Policy | S12 travel (°) | S12 probes | S12 zero moves | S2 travel (°) | S2 probes |
|---|---|---|---|---|---|
| G\* | 6.13 | 3.962 | 79.3 % | 46.91 | 3.873 |
| Student (3 seeds) | 1.52 / 2.05 / 1.88 | 4.0 | 97.7–99.7 % | 39.14 | 3.926 |
| RL (3 seeds) | 23.02 / 25.76 / 25.65 | 3.0 | 0.0–21.9 % | 136.8 | 3.0 |
| B-fan | 1.454 | 4.0 | 100 % | 1.454 | 4.0 |
| Random | 38.45 | 1.946 | 33.0 % | 172.2 | 2.367 |

In S2 the student travels a similar amount to G\* on average (39.1° vs 46.9° per episode, test3 0–299), unlike S12
(1.5–2.0° vs 6.1°, test3 0–499), but its per-episode travel is only weakly correlated with G\*'s (r 0.14–0.24 by
seed: 0.162, 0.238, 0.141), and none of its 300 episodes per seed reproduces G\*'s action sequence. S2 therefore shows
that the student is not confined to stay-and-probe, not that it reproduces G\*'s travel decisions.

### 5.3 Learnability against G\* in both regimes

**S12 (D3).** On 500 paired val3 episodes, the first-attempt students reached Δ̂_succ = −5.87 pp against a threshold of
−1.43 pp and Δ̂_BI = −0.199 nats against −0.15. After the remedy, success was −4.40 pp against −1.68 pp (fail), BI
−0.096 (pass) and per-seed −4.6 / −4.6 / −4.0 pp (fail), so H1 is dead. On test3 0–299 the remedied student trails G\*
by 4.4 pp (ci90 [−8.6, −0.3], ci95 [−9.3, +0.6]) and by 0.049 nats BI (ci95 [−0.114, +0.019]). An exploratory,
post-freeze student trained for 200 epochs on the remedied data was not shown to differ from G\* on test3 (−1.7 pp,
ci95 [−6.8, +3.4]; long − remedied +2.8 pp, ci95 [−1.0, +6.7]), so in S12 the optimisation budget is left open as an
explanation.

**S2 (D4).** The S2 student was not shown to reach G\* (val3 Δ̂_succ −2.80 pp vs threshold −1.46 pp; BI and per-seed
clauses pass). On test3 0–299 the gap is −10.2 pp (ci95 [−16.6, −4.3]); it is wider than on val3 for every seed (by
5.4, 11.2 and 5.7 pp), both the G\* (+3.9 pp) and student (−3.5 pp) rows move, the difference is ≈ 2.0 combined SE
under independence (conservative given shared students), and its cause is untested. On S2 test3 the student − G\* BI
ci95 [−0.269, −0.094] excludes 0; on val3 the deficit is −0.105 (SE 0.039), with no interval computed. The S2 recipe
already was the budget-matched 200-epoch recipe, so the optimisation-budget explanation left open in S12 does not
account for the S2 result in the same way.

**S2 training record.** Every S2 round ran to its 200-epoch cap. Held-out $\bar R$ did not improve over DAgger: it was
0.300–0.312 after round 0 and 0.298–0.322 after round 2 across the three seeds. Training $\bar R$ was not logged in S2,
so the S12 label-fit rule cannot be applied there.

**S12 label fit and belief input.** All six S12 history students fit their training labels by the registered rule
(train top-1 0.511–0.534, train $\bar R$ 0.169–0.206; under-fit requires $\bar R$ > 0.25 or top-1 < 0.50), which
assigns the deficit to generalisation rather than capacity; support for that reading is weak, because held-out top-1
(0.483–0.507) sits close to train top-1, which an under-optimised model would also show. The belief-input students are
under-fit (train top-1 0.327–0.362) and fail every D3 criterion (Δ̂_succ −20.1 pp), so that control isolates nothing
about the representation.

### 5.4 Distillation against RL on RL's own objective

**S12 (H2).** The student reaches $g_T$ = 5.368 nats and RL 5.368; Δ = +0.0002 nats with one-sided 95 % bounds
[−0.3103, +0.3034]. H2 is rejected; with three seeds per learner the test was powered only for large effects, and no
equivalence test was registered or run.

**S2 (H2-S2).** H2-S2 is not detected (LB −0.749 ≤ +0.10); in exploratory terms the crossed-bootstrap point estimate
favours RL by 0.445 nats on $g_T$ (one-sided 95 % UB of student − RL −0.162, bootstrap p 0.0064, not pre-registered).
The LB (−0.749) is 0.85 nats below the threshold, about 2.9 one-sided half-widths (0.293), so the non-detection is not
near the margin. Every S2 RL seed (5.832–6.179) is above every S2 student seed (5.450–5.612) on $g_T$.

**Success and BI (Table 5).** Student − RL success is +2.6 pp (ci95 [−3.7, +8.8]) in S12 and +2.8 pp (ci95
[−4.1, +9.6]) in S2; student − RL BI is +0.289 nats (ci95 [+0.117, +0.465]) in S12 and +0.180 nats (ci95
[+0.091, +0.273]) in S2. G\* − RL success is +13.0 pp (ci95 [+6.4, +19.4]) in S2 and +7.0 pp (ci95 [+0.2, +13.7]) in
S12; RL ends at 3 probes and travels several times G\*'s distance in both cells (2.9× in S2, about 4× in S12), so the
record does not identify why the gap differs, and no cross-cell test of it exists.

**Instrument ordering.** On seed-averaged point estimates $g_T$(G\*) is below both learned policies in S2 (5.40 vs
5.53 / 5.98) and marginally in S12 (5.30 vs 5.37, with 3 of 6 S12 learner seeds below G\*); every S2 learner seed is
above 5.397; no interval exists for these contrasts. The grid posterior orders G\* above both learners in both cells.
In S12, cap saturation of $g_T$ is rare (5.8 % of G\* episodes, 0.4–3.4 % for the learners) and ordered like BI, so the
cap alone is unlikely to explain the inversion. We record this as a methods observation, not a mechanism.

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

**Seed variability and RL training.** In S12 the RL per-seed SD of $g_T$ is 3.29× the student's, and its test success
range is 7.7 pp against 1.0 pp. All six RL seeds ran to the 200,064-episode cap; the plateau rule fired at 102,400
episodes for every S2 seed. The S2 trainer's last-batch $g_T$ (5.989–6.340) is on training episodes and is not
comparable to the test3 rows.

### 5.5 Learned policies against the stay-and-fan heuristic (exploratory)

On S2 test3 the student exceeds B-fan on success (+8.1 pp, ci95 [+1.7, +14.7]) and BI (+0.53, ci95 [+0.42, +0.64]);
in S12 it exceeded B-fan on BI (+0.23, ci95 [+0.14, +0.31]) but not on success (+2.2 pp, ci95 [−2.8, +7.3]), so S2
adds a success separation, exploratory, uncorrected and untested across cells. B-fan − G\* success is −18.3 pp in S2
and −6.7 pp in S12. In S12, RL − B-fan is −0.3 pp (ci95 [−6.9, +6.3]); in S2 no RL − B-fan interval was computed, so
it is not reported as a contrast.

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
distilled students: both are lower on BI (ci95 exclude 0) and success is unresolved. On a different split (pilot3,
n = 186 / 177, incomplete) the same configurations scored 0.382 / 0.390 success at 18.2 / 44.1 ms, against 0.360 /
0.377 at 20.8 / 46.0 ms here; unpaired.

## 6 Discussion

**Greedy is a defensible teacher, within the measured scope.** One-step headroom over the reduced greedy completion is
small at κ = 12, and the κ = 2 row measured in the S2 cell is also small. In the narrow sense that one deviating step
buys little among the screened first actions, the cost-aware greedy planner is a reasonable target for amortization in
both regimes. The measurement bounds one step followed by a reduced completion; it does not speak to deeper planning,
and in S12 the planner rarely moves, which leaves the travel coupling little room to create headroom.

**Making the planner travel did not make it learnable to non-inferiority.** S12 left open the explanation that the
student failed because the registered stopping rule under-trained it, since the exploratory 200-epoch student was not
shown to differ from G\* on test. S2 was trained with that budget-matched recipe from the start and still failed its
gate, and on test its deficit is larger than on validation for every seed. The behavioural record locates part of the
difficulty. In S2 the student moves a G\*-like amount on average, so it is not merely a stay-and-probe policy, but its
travel is only weakly correlated with G\*'s episode by episode: it travels, but its travel tracks G\*'s only weakly. The student's
held-out regret did not improve across DAgger rounds in S2, so additional on-policy labels at this data scale did not
translate into better agreement with the teacher's scores.

**What learning buys over no learning.** Where staying is cheap (S12), neither learner was shown to exceed the
travel-nearest stay-and-fan heuristic on success. In S2 the student does exceed it on both success and BI
(exploratory), while the heuristic falls further behind G\*. A cautious reading is that the learned head captures some
belief-dependent structure of the planner's choices that a belief-free rule cannot, and that this becomes visible on
success only when the planner's own strategy departs from staying; we did not test this across cells.

**$g_T$ as a yardstick.** The contrastive objective that RL optimises ranks G\* below both learners in both cells,
whereas the grid posterior ranks it above. In S2 the point estimate on $g_T$ favours RL while every success and BI
contrast between the learners is either undetected or favours the student. Consequently, "no advantage on RL's own
objective" carries little information about localization quality, and H2 and H2-S2 are best read as findings about
that proxy. Semi-amortized schemes that refine a learned proposal online \cite{hedman2025step} or keep a cheaper
nested filter in the loop \cite{iqbal2024recursive} are natural next designs, although our latency decomposition shows
that the particle filter itself bounds the speed-up of any scheme that keeps it.

**Cost.** Per decision, the learned head is orders of magnitude cheaper than full-size G\*, but at tens of
milliseconds two reduced-size planners trail the students on BI with success unresolved. The relevant comparison for
practitioners is therefore not against full-size G\* but along a latency–accuracy frontier that is only partly mapped.

**Open questions.** Does regret measured on student-visited states confirm covariate shift? Does the S2 validation/test
discrepancy persist with more episodes and seeds? Do the findings hold in more cells per regime? Would a full 512-action
screen change H3? Where do the learners sit on a reduced-planner frontier timed under Lat′?

## 7 Limitations

- **One cell per regime.** All learning results come from one stay-and-probe cell (S12) and one travelling cell (S2);
  S2 borrows δ from S12 and has no pilot margin, so its gate rests on the −0.15 BI floor and a borrowed success margin.
- **Evaluator not shown converged.** The evaluator gate failed and sub 8 is used without a finer check; S2 test3 rows
  were produced on more than one machine and pipeline.
- **Unexplained S2 validation/test gap.** The S2 test gap is wider than the validation gap for every seed, and its
  cause is untested.
- **Comparators not shown tuned.** No S2 hyperparameter grid was run; RL was not re-tuned for S2 (config 2 was chosen on
  the trainer's val_v2 stream and sits at the edge of the learning-rate grid); three seeds per learner give H2 power
  only for large effects.
- **H3 scope.** H3 covers 32 screened first actions with a reduced greedy completion, and the selection bias of
  $V_{LA}$ was not measured.
- **Latency.** The Lat′ protocol is incomplete (several configurations exceeded the CI-width criterion, two runner jobs
  pooled), and E5 latencies are logged during evaluation on free runners, not Lat′ measurements.
- **Incomplete random anchor.** The S2 test3 random row has 215 of 300 episodes and enters no contrast.
- **Test-split reuse.** test3 is reused by exploratory rows (the long student, B-fan, S2 rows and E5), so it is no
  longer untouched.
- **Registered items not executed.** The Holm-corrected family, the TOST equivalence test, the behaviour-cloning and
  absolute-frame student rows and the reduced-planner H1 comparison were descoped because each was conditional on H1
  reaching test, which D3 prevented.
- **Simulation only.** All results are in simulation with planar objects; no held-out shapes or hardware were tested.

## 8 Conclusion

We asked how much headroom one-step look-ahead leaves over greedy cost-aware information-gain touch selection under
travel cost, and whether that planner can be amortized by distillation or by RL on the same objective, in a
stay-and-probe regime where the planner barely moves and in a regime where it travels. Four answers follow from a
pre-registered characterisation with one cell per regime. First, one-step headroom is small: among the screened first
actions, rollout over a reduced greedy completion gains at most about 2.2 % at κ = 12, and the κ = 2 row is also
small. Second, neither learner was shown to reach the planner in either regime with one belief-free head; in the
travelling regime the distilled student moves the finger about as much as the planner on average, but its
travel is only weakly correlated with the planner's. Third, distillation was not shown to be better than RL on RL's own objective in either regime, and that
objective orders the planner differently from the grid posterior. Fourth, at tens of milliseconds per decision,
reduced-size planners trail the students on ball information with success unresolved; nothing was compared at matched
accuracy. Concrete next steps are more cells and seeds per regime, regret on student-visited states, a full-action
screen for the headroom estimator, a resolution of the S2 validation/test discrepancy, and reduced planners timed
under the latency protocol alongside the learners.

