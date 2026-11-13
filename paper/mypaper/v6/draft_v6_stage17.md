<!-- Stage 17 PAPER_DRAFT [v6], 2026-11-13; fresh-context subagent; prompts paper/mypaper/prompts/stage17_v6_{system,user}.txt; outline paper/mypaper/sections/00_outline.md (stage 16 v6). Sources of numbers: A = results/v6/14_v6_analysis.json, D = results/v6/15_derived_v6.json (post hoc, no CI), v5 = results/v5/results_v5.json; "(derived)" = arithmetic printed in results/v6/14_analysis.md; method constants carried from paper/mypaper/v5/draft_v5_final.md §3 (code and amendments, not a results field). -->

```
FIGURE 1 PROMPT (v6; panel A generated as a schematic, panels B-F plotted from JSON with matplotlib following the dataviz skill)

Layout: one full-width figure for a two-column robotics paper, aspect ratio about 3.2:1, white background (#FFFFFF),
flat vector style, no shading, gradients, shadows, textures, people, robot arms, logos or watermark. One sans-serif font
(Helvetica/Arial-like), dark grey #222222, all text horizontal. Accent colours: BLUE #1F6FB4 = student / probing,
ORANGE #E07B1A = travel cost, GREY #777777 = reduced planners, BLACK #222222 = planner G*, PURPLE #7A4FA3 = second
shape library (A16-2 only). Panel letters bold, top-left: "A" (left, about 20 % of the width) and "B"-"F" (five equal
small multiples, right, about 80 %).

PANEL A - schematic (image generator; no numbers anywhere on this panel)
 1. Top half, top-down view: one flat irregular grey polygon (#9A9A9A fill, #555555 outline) with three or four very
    light ghost outlines (#CFCFCF, no fill) shifted and rotated slightly around it; small label "belief over identity × pose".
 2. A thin grey stand-off circle (#777777) around the polygon; a small dark dot on it at about 8 o'clock labelled "φ_t".
 3. An ORANGE arc just outside the circle from the dot clockwise to about 1 o'clock, arrowhead at the end, orange label
    "cost 1 + κ|Δφ|/π"; a small open orange circle at the arc end labelled "φ′".
 4. From φ′ a BLUE arrow pointing inward, tilted about 15° from the radial direction, small blue arc label "ψ", ending on
    the polygon edge at a small blue diamond with a short perpendicular tick, label "contact + normal".
 5. Bottom half, block diagram: a rounded box "G* (EIG / cost, argmax)". Three arrows leave it to the right:
    - GREY solid arrow, label "shrink" -> box "R-500, R-125";
    - BLUE solid arrow, label "distil (BC round 0 -> DAgger rounds 1-2)" -> box "student";
    - dashed BLACK arrow, label "PPO on g_T" -> box "RL".

PANELS B-F - data (plotted, NOT generated). One panel per cell, left to right: "S2, κ = 2", "S4, κ = 4", "S8, κ = 8",
"S12, κ = 12", "A16-2, κ = 2" (A16-2 title in PURPLE).
 x axis: median per-decision latency (s), log10 scale, shared range 1e-4 to 1e1; label only under the middle panel:
   "median latency per decision (s, log scale; previous-round timings)".
 y axis: success on test episodes 0-499, shared range 0.20-0.56; label only on panel B: "success (episodes 0-499)".
 Markers:
   G* run 1 = filled black circle; G* run 2 = hollow black circle at the same x; thin vertical black segment between
   them, labelled "teacher run-to-run" in panel B only;
   R-500 = grey square; R-125 = grey triangle;
   student 5-seed mean = blue diamond with a vertical bar for the min-max over the five seeds.
 Thin grey arrows from R-125 and from R-500 to the student diamond; a small star at the arrow head where Holm rejects on
   0-499 (S2: R-125; S4: R-125 and R-500; S8: R-125; S12: R-125; A16-2: R-125 and R-500).
 Two horizontal dashed lines across each panel, no latency position: "H* (latency not timed)" (dark grey) and
   "RL (latency not timed)" (black, dash-dot).
 No fresh-window points, no contrast CIs, no fitted frontier curve.

 Data (copied; keys below):
 | Cell  | x: G* / R-500 / R-125 / student (s)  | y: G* r1 / G* r2 / R-500 / R-125 / student [seed min-max] | H* / RL |
 | S2    | 4.880 / 0.194 / 0.116 / 0.000500     | 0.518 / 0.532 / 0.462 / 0.406 / 0.4988 [0.464-0.526]        | 0.432 / 0.4132 |
 | S4    | 3.375 / 0.141 / 0.080 / 0.000494     | 0.496 / 0.494 / 0.390 / 0.402 / 0.4576 [0.432-0.482]        | 0.368 / 0.3964 |
 | S8    | 1.234 / 0.061 / 0.030 / 0.000358     | 0.432 / 0.464 / 0.372 / 0.356 / 0.4188 [0.408-0.436]        | 0.344 / 0.3932 |
 | S12   | 0.910 / 0.048 / 0.022 / 0.000358     | 0.434 / 0.434 / 0.390 / 0.358 / 0.4144 [0.398-0.428]        | 0.358 / 0.3576 |
 | A16-2 | 2.702 / 0.098 / 0.058 / 0.000326     | 0.474 / 0.498 / 0.374 / 0.330 / 0.4832 [0.464-0.496]        | 0.312 / 0.2144 |

 Keys:
   x: A:cells.<cell>.frontier.latency_median_s.{gstar, g500_512_4, g125_512_16, student}
      (= v5:14_e6_analysis.json > <cell> > job1 > * > median)
   y: A:cells.<cell>.frontier.success_0_499.{gstar, g500_512_4, g125_512_16, student};
      G* run 2: A:cells.<cell>.0-499.means.gstar2.success
   seed range: A:cells.<cell>.0-499.means.student_s70{1..5}.success
   H*: A:cells.<cell>.0-499.means.<A:cells.<cell>.0-499.v5_row_updates.H_star>.success
   RL: D:cells.<cell>.0-499.rl_mean (post hoc, no CI)
   stars: A:cells.<cell>.0-499.holm.{H6b_g125_512_16, H6b_g500_512_4}

DRAFT CAPTION
Figure 1. Distil or shrink a cost-aware touch planner? (A) The task, and three ways to make the planner G* fast:
shrink it (reduced planners R-500, R-125), distil it into a belief-free policy (behaviour cloning, then DAgger), or
train the same policy with RL. (B-F) Success on 500 test episodes against median per-decision latency (log scale;
timings from the previous round, point medians without dispersion) for travel cost κ = 2, 4, 8, 12 on shape library S
and κ = 2 on library A16. Filled and hollow circles are two independent G* runs. Diamonds are the 5-seed student mean
with the seed range. Stars mark student-vs-reduced-planner contrasts confirmed by Holm (7 of 10; 2 of 10 on the 200
fresh episodes, where only the direction replicates). Dashed lines show the pilot-chosen heuristic H* and RL, whose
latency was not timed. The student's position relative to G* is undecided: neither a difference nor equivalence within
4 pp is shown (Table 1), and changing the evaluator grid alone moves that contrast by up to 5 pp. Simulation; preliminary.
```

# Amortizing a Cost-Aware Information-Gain Touch Planner: A Pre-Registered Accuracy–Latency Study in TouchBED

## Abstract

A cost-aware greedy information-gain touch planner (G\*) for active tactile localization under travel cost chooses
each probe by expected information per unit of travel, but it spends up to several seconds of computation per decision. A
practitioner who needs a fast policy can distil the planner into a learned policy or shrink the planner itself; we ask
which buys more accuracy per millisecond and whether the DAgger rounds of distillation matter. We report a
pre-registered five-cell study: travel cost κ = 2/4/8/12 on one planar shape library and a second library, A16, at
κ = 2, with 500 test episodes per method (200 of them fresh), two independent G\* runs, two reduced planners, behaviour
cloning (BC) and DAgger students with five seeds each, and an evaluator-grid check. By Holm, the student is more
accurate than the smaller reduced planner in all five cells and than the larger one in two, at 62–389× lower
per-decision latency (point medians); on the fresh episodes only 2 of these 10 contrasts survive Holm, so only the
direction replicates. The student is neither shown to differ from G\* nor shown equivalent within 4 pp: point estimates
are 0.3–3.7 pp below G\*, and deficits of about 7–8 pp are not excluded. DAgger adds no detectable accuracy over BC.
Changing only the evaluator's read-out grid moves the student − G\* contrast by up to 5 pp, and two G\* runs agree on
only 25–45 % of first decisions. Simulation; planar shapes; preliminary.

## 1 Introduction

A robot that localizes an object by touch receives sparse and ambiguous evidence: one contact point and one surface
normal per probe, or a miss. A single contact rarely fixes the pose, and families of near-symmetric shapes make even
the identity uncertain. The standard remedy is to keep a belief over identity and pose, usually a particle filter, and
to choose the next touch by its expected information gain \cite{petrovskaya2011global, hebert2013next,
zheng2024bayesian}. Greedy selection of this kind is supported by adaptive-submodularity arguments for touch-based
localization \cite{javdani2012efficient}. Probing is not free, however: the finger has to travel to the next approach
direction, and travel competes with probes inside a fixed time budget. Cost-aware selection therefore scores each
candidate touch by information per unit cost \cite{ottenhaus2018active}, a trade-off that reviews of active haptic
perception place at the centre of practical exploration \cite{seminara2019active}. The price is computation. A planner
that re-estimates the expected information of every feasible touch at every decision, by nested Monte Carlo over the
particle belief, spends up to several seconds of computation per decision on a commodity CPU.

There are two obvious ways to make such a planner fast. The first is to amortize it: train a policy once, either by
imitating the planner, as in DAgger and behaviour cloning \cite{ross2011reduction, choudhury2017adaptive}, or by
policy-based experimental design on an information bound \cite{foster2021deep, blau2022optimizing,
rainforth2024modern}, or by reinforcement learning on a task reward \cite{riou2024reinforcement}. The second is to
shrink the planner: use fewer particles and fewer sampled outcomes, and accept a noisier score. Both routes trade
accuracy for speed. For a practitioner the relevant question is which of the two buys more accuracy per millisecond of
decision time, and, if the planner is distilled, whether the interactive DAgger rounds are worth their cost over plain
behaviour cloning on planner-visited states.

The previous round of this study asked a different question, whether the distilled student matches G\*. Its
pre-registered validation gate failed in 5/5 cells, as had the single-cell gates of the rounds before, and its test
contrasts were too wide to decide anything. At the power available in this setting a parity test is the wrong headline:
the interesting comparison is not student against teacher alone, but student against the cheaper versions of the
teacher that a practitioner could deploy instead. The present round therefore pre-registered, before any episode was
run, three hypothesis families: the accuracy–latency frontier of the student against two reduced planners (H6b), parity
with G\* counting the teacher's own run-to-run variance and tested with two one-sided tests (TOST) at a 4 pp margin
(H6a), and DAgger against behaviour cloning (H6c). It added 200 fresh test episodes, an independent second G\* run, and
an evaluator-grid check in every cell and for every student seed.

We make one narrow positive claim and three qualified ones, in decision order.

- **C1. Frontier.** By Holm, the student is more accurate than the smaller reduced planner (R-125) in all 5 cells and
  than the larger one (R-500) in S4 and A16-2; against R-500 in S2, S8 and S12 no accuracy difference is shown. It is
  62–389× faster per decision than both reduced planners (point medians from the previous round), while the reduced
  planners themselves are 19–47× faster than G\*. On the fresh window only 2/10 contrasts survive Holm, so the fresh
  window replicates the direction, not the significance.
- **C2. Parity is not established.** With G\*'s two runs in the contrast, the student's success point estimate is
  0.3–3.7 pp below G\* in every cell, with no registered difference and no registered equivalence; deficits of up to
  about 7–8 pp cannot be excluded. On the primary window the student is not more than 4 pp better than G\* in any cell
  (unadjusted, per cell).
- **C3. DAgger.** Round-0 (BC-only) students already reach the round-2 success level (|r2 − r0| ≤ 1.3 pp); DAgger adds
  no detectable accuracy, and no equivalence test was registered.
- **C4. Methods note.** Changing only the read-out grid moves student − G\* by 4.6–5.0 pp in three cells, comparable to
  the 4 pp margin, and two G\* runs from the same state agree on only 0.25–0.45 of first decisions. Success contrasts of
  a few pp in this setting therefore depend on the evaluator and on the teacher's Monte Carlo variation, which is a
  reporting lesson for evaluations of amortized information-gathering policies.

The study is a measurement in a planar simulator, not a method paper, and none of it is evidence about hardware.
Section 2 reviews related work. Section 3 defines the task, the planner and its reduced versions, the student and its
training rounds, and the comparators. Section 4 gives the pre-registration, the data windows and the statistics.
Section 5 reports C1–C3, Section 6 discusses them together with the C4 methods note, and Sections 7 and 8 state the
limitations and conclude.

## 2 Related Work

**Tactile localization and next-best touch.** Estimating object pose from touch is usually posed as Bayesian
filtering. Scaling-series Monte Carlo achieves global localization from sparse contacts on polygonal meshes
\cite{petrovskaya2011global}, manifold particle filters sample on the contact manifold to avoid particle degeneracy in
planar contact manipulation \cite{koval2015pose}, and Tac2Pose returns a pose distribution from a single high-resolution
touch \cite{bauza2023tac2pose}. On top of such estimators, information-driven selection picks the next touch. The next
best touch maximises information gain on pose uncertainty \cite{hebert2013next}; Bayesian frameworks jointly track
class and pose with customised particle filters and choose exploratory actions by expected information
\cite{zheng2024bayesian, zheng2026bayesian}; recent work selects contacts by expected information gain for rigid-body
pose and shape \cite{gordon2026active}, or learns a single exploration policy on hardware that balances global search
and local refinement \cite{kamtikar2026tactful}. Cost-aware information gain combines expected gain and expected cost
in one score \cite{ottenhaus2018active}. Several of these systems run on hardware with 3D geometry and real contact; our
setting is planar and simulated, and we use it to isolate the selection question rather than to compete with them. In
this line cost-aware selection runs online at every decision, and how well it can be amortized, measured against
cheaper versions of the same planner rather than against heuristics alone, is rarely reported.

**Greedy information gathering.** Submodularity explains why greedy selection works well for touch: entropy reduction
is submodular under certain assumptions, and adaptive submodularity gives online guarantees for touch-based
localization \cite{javdani2012efficient}. Hierarchical action structure can be folded into the same framework by
sequential submodular optimisation \cite{vien2015touch}. Outside touch, submodular surrogates approximate the value of
information when the objective itself is not submodular \cite{chen2015submodular}, and semi-adaptive policies quantify
how much adaptivity is needed to keep guarantees \cite{esfandiari2019adaptivity}. Travel cost couples successive
decisions, because where the finger ends one probe sets the price of the next, which is exactly the structure that
weakens these guarantees. All of these results concern the planner, not a learned copy of it, and none says how
accuracy degrades when the planner's Monte Carlo budget is cut. We therefore treat G\* as the reference that faster
policies are measured against, not as an optimum, and make no claim about its distance to the optimal policy.

**Amortized active sensing.** Deep adaptive design trains a design network on contrastive information bounds so that
each decision is one forward pass \cite{foster2021deep}; implicit-likelihood and RL formulations remove the need for a
likelihood or a differentiable simulator \cite{ivanova2021implicit, blau2022optimizing}; semi-amortized variants refine
the policy online \cite{hedman2025step}; nested particle filters amortize design in dynamical systems
\cite{iqbal2024recursive}; and transformer policies amortize inference and acquisition jointly \cite{huang2026aline}. In
touch, RL agents learn exploration for recognition with rewards on correct classification \cite{riou2021seeing}, on
classification, exploration and pose \cite{riou2024reinforcement}, or learn when to stop \cite{niemann2024when}, and
TANDEM3D co-trains exploration and decision making on 3D contacts \cite{xu2023tandem3d}. A third route imitates an
information-gathering expert: a clairvoyant oracle \cite{choudhury2017adaptive} or a nonmyopic active-search expert
\cite{nguyen2024amortized}, typically through DAgger's no-regret reduction \cite{ross2011reduction}. These works compare
learned policies with heuristics, with each other or with the expert, and usually report one evaluator. We know of no
pre-registered comparison of a distilled policy against reduced versions of its own teacher on an accuracy–latency
frontier that also reports the teacher's run-to-run variance, a BC-versus-DAgger ablation and the sensitivity of the
contrasts to the evaluator. This paper supplies that comparison, as a measurement rather than as a new method.

## 3 Method

### 3.1 Task, belief, cost and metrics

**State, actions, observations.** The object is a planar polygon with identity $k \in \{1,\dots,K\}$ and unknown pose,
so the state is $s = (k, x, y, \theta)$, with a uniform prior over identity, position in a bounded box and orientation.
The finger rests on a stand-off circle of radius 100 mm at angle $\phi_t$; the start angle is shared by all methods on
an episode. An action $a = (\phi', \psi)$ selects a target angle $\phi'$ and an approach offset $\psi$ from a grid of 64
target angles (5.625° apart) × 8 offsets (−35° to +35° in 10° steps), $|\mathcal{A}| = 512$. The finger travels the
shorter way to $\phi'$, probes inward along $\phi' + \pi + \psi$, and then $\phi_{t+1} = \phi'$. A probe returns a
contact point and surface normal, both with Gaussian noise, or a miss $y = \varnothing$. All methods share the same
softened likelihood $p_\varepsilon(y \mid s, a)$, so differences between methods come from the actions they choose, not
from their sensor models. The belief is a particle filter $b = \{s_n, w_n\}_{n=1}^{N}$ over identity and pose
\cite{petrovskaya2011global, koval2015pose}.

**Travel cost and budget.** In units of one probe stroke,

$$c(a) = 1 + \kappa\,\frac{|\Delta\phi|}{\pi}, \qquad \Delta\phi = \mathrm{wrap}(\phi' - \phi_t) \in (-\pi, \pi],$$

so κ is the time needed to travel half the circle. With remaining time $\tau_{\mathrm{rem}}$ the feasible set is
$\mathcal{F}(\tau_{\mathrm{rem}}) = \{a : c(a) \le \tau_{\mathrm{rem}}\}$; every method chooses only within it, and an
episode ends when no action is feasible. The budget τ of each cell is calibrated so that G\* executes about $n^\*$
probes, from G\*'s mean unbudgeted travel time over 200 calibration episodes.

**Metrics.** From the evaluator's posterior after the last probe, the identity estimate is the maximum-mass identity
and the pose is refined locally. *Success* requires the correct identity and position and orientation errors inside
fixed tolerances, orientation taken modulo the shape's symmetry group; it is read from an adaptive grid posterior at
subdivision 8 (sub 8), the registered evaluator. With $B(s_0)$ the success ball around the true state, the *ball
information* is $\mathrm{BI}(h) = \log \hat P(B(s_0) \mid h) - \log P(B(s_0))$ in nats. The RL objective $g_T$
(ball-sPCE, Section 3.4) is computed without the grid. *Travel* is the total angular distance (rad) the finger covers in
an episode, including the first leg from the continuous start angle onto the action grid; we also log the number of
probes.

**Libraries and cells.** Library S has $K = 8$ identities, four near-symmetric base shapes and one symmetry-breaking
variant of each. Library A16 has $K = 16$ star-shaped irregular polygons with 8 to 14 vertices and trivial symmetry
groups, rejection-sampled for a minimum edge length and a cap on self-confusability. A16 differs from S in shape family,
$K$ and $n^\*$ at once, and its first 8 identities are the asymmetric library A of earlier rounds, so it is only partly
new. Table 0 lists the five pre-registered cells; the S2 and S12 budgets are carried from earlier calibration rounds.

**Table 0. The five cells.**

| Cell | Library | κ | $n^\*$ | τ |
|---|---|---|---|---|
| S2 | S | 2 | 4 | 4.7 |
| S4 | S | 4 | 4 | 4.8 |
| S8 | S | 8 | 4 | 4.8 |
| S12 | S | 12 | 4 | 4.9 |
| A16-2 | A16 | 2 | 3 | 3.4 |

### 3.2 Planner G\* and the reduced planners

G\* selects

$$G^\*(b) = \arg\max_{a \in \mathcal{F}(\tau_{\mathrm{rem}})} \frac{\mathrm{EIG}_B(a; b)}{c(a)},$$

where the ball EIG, the expected one-step increment of $\log P(B(s_0)\mid h)$, is estimated by nested Monte Carlo with
$j_m \sim w$ and $y_m \sim p_\varepsilon(\cdot \mid s_{j_m}, a)$:

$$\mathrm{EIG}_B(a;b) = \frac{1}{M}\sum_{m=1}^{M}\Big[\log\!\!\sum_{n \in B(s_{j_m})}\!\! w_n\, p_\varepsilon(y_m \mid s_n,a)
- \log\!\!\sum_{n \in B(s_{j_m})}\!\! w_n - \log \sum_n w_n\, p_\varepsilon(y_m \mid s_n, a)\Big].$$

A configuration is named `g`N`_`C`_`M for $N$ particles, $C$ candidates scored and $M$ sampled outcomes per
candidate. The deployed G\* is `g2000_512_64`. At each decision it exports the score vector
$s(a) = \max(0, \mathrm{EIG}_B(a;b))/c(a)$ over feasible actions (zero elsewhere), whose argmax is its action and which
is the distillation label.

**Run-to-run stochasticity.** G\* samples particles and outcomes, so it is a Monte Carlo procedure, and two runs from
the same state need not choose the same action. We therefore run it twice per cell with independent streams: run 1 is
the previous round's record extended to the new episodes, and run 2 salts the policy and decision-filter streams while
keeping state, start-angle and observation streams fixed. Both runs enter the parity contrast.

**Reduced planners.** R-125 (`g125_512_16`) and R-500 (`g500_512_4`) keep all 512 candidates and cut particles and
outcome samples; each is run once per cell.

**Complexity and design rationale.** Per decision, a planner evaluates $O(MNC)$ likelihoods and builds ball-neighbour
lists in $O(N^2)$, on top of assimilating the last observation; the latter terms do not depend on $C$. The product
$N \cdot M$ is 128,000 for G\* and 2,000 for both reduced planners, so the reduced planners differ in how they split the
same Monte Carlo budget: R-125 keeps more outcome samples per candidate, R-500 more particles, and its $O(N^2)$ term is
larger. Keeping $C = 512$ fixes the action set, so a reduced planner and the student choose among the same actions as
G\*. G\* is a greedy reference: we measure faster policies against it and make no claim that it is optimal
\cite{javdani2012efficient, ottenhaus2018active}.

### 3.3 Student: shared head, behaviour-cloning round and DAgger rounds

**Head.** The student is a belief-free DeepSets head [CITE-MISSING: DeepSets (Zaheer et al. 2017)]. Each touch in the
history is encoded in the finger frame (contact indicator, contact point, normal and the action that produced it),
summed, and concatenated with a context of the relative angle, the remaining-budget fraction $\tau_{\mathrm{rem}}/\tau$
and the absolute finger angle $\phi_t$. The head outputs one logit per action, masked to $-\infty$ outside
$\mathcal{F}(\tau_{\mathrm{rem}})$. Re-encoding the history costs $O(T^2H^2 + THA)$ for $T$ touches, hidden width $H$
and $A$ actions, with no particle filter in the loop, which is why its per-decision cost is sub-millisecond. The RL
comparator uses the same head and action set.

**Loss.** The student $\pi_\theta$ minimises a soft cross-entropy to tempered teacher scores plus a hard term on the
teacher's argmax,

$$\mathcal{L}(\theta) = -\sum_{a \in \mathcal{F}} q(a)\log \pi_\theta(a \mid h) - \lambda \log \pi_\theta(a^\* \mid h),
\qquad q = \mathrm{softmax}\big(\beta_T\, s(a)/\sigma_s\big)_{a \in \mathcal{F}},$$

with $\sigma_s$ the per-decision standard deviation of $s$ over feasible actions and $a^\* = \arg\max_a s(a)$. Held-out
quality is the floored normalised label regret

$$r = \frac{s_{\max} - s(a_\pi)}{\max(s_{\max} - s_{\mathrm{med}},\ \rho\, s_{\max})},$$

averaged over held-out decisions to $\bar R$. No success-based model selection is used. One hyper-parameter setting is
used in all 75 training runs (5 cells × 5 seeds × 3 rounds; Table S).

> **Algorithm 1 (behaviour cloning, then DAgger, on G\* scores).**
> 1. **Round 0 (BC).** Roll out G\* on 3,000 label episodes, storing $(h, \phi_t, \tau_{\mathrm{rem}}, \mathcal{F}, s, a^\*)$
>    at every decision; hold out 300 episodes for $\bar R$, train on 2,700.
> 2. Train $\pi_\theta$ on $\mathcal{L}$ for 200 epochs; after each epoch evaluate held-out $\bar R$ and **keep the
>    checkpoint with the lowest held-out $\bar R$**.
> 3. **Rounds 1 and 2 (DAgger).** Roll out 800 episodes per round, executing G\*'s action with probability
>    $\beta_{\mathrm{DAgger}}$ (0.5 in round 1, 0 in round 2) and $\pi_\theta$'s otherwise; run G\*'s filter alongside,
>    label every visited belief with $s$, aggregate (3,500 and 4,300 training episodes), and repeat step 2.
> 4. Freeze the kept checkpoint of every round and record its weight hash before any test episode.

The deployed student is the round-2 checkpoint of seeds 701–705. The **BC student** is the round-0 checkpoint of the
same seeds; comparing the two is the one component ablation of this paper (H6c). In S2 and S12 the round-0 labels are
re-used from earlier rounds, where library, κ, τ and code path match; the DAgger rounds are new in every cell. One
qualifier applies to the selection metric: $\bar R$ is measured on G\*-visited decisions, so it cannot register what the
DAgger rounds are meant to add, namely labels on student-visited beliefs \cite{ross2011reduction,
choudhury2017adaptive}.

### 3.4 Comparators

**RL.** The RL policy uses the same head and is trained with PPO \cite{schulman2017proximal} and a critic baseline. Its
reward is the increment of ball-sPCE, a contrastive estimate of ball information in the style of
\cite{foster2021deep, blau2022optimizing}: with $L$ contrastive states $s_{1:L} \sim p$ and $J$ states $s_0^{(j)}$
drawn uniformly in $B(s_0)$,

$$g_t = \log \hat p_B(h_t \mid s_0) - \log\Big[\tfrac{1}{L+1}\Big(\hat p_B(h_t \mid s_0) + \sum_{l=1}^{L} p(h_t \mid
s_l)\Big)\Big], \qquad \hat p_B(h \mid s_0) = \tfrac{1}{J}\sum_j p(h \mid s_0^{(j)}),$$

and $r_t = g_t - g_{t-1}$, so the return telescopes to $g_T$. The test read-out of $g_T$ uses $J = 16$ and $L = 4{,}095$
on histories rebuilt from the recorded actions. One configuration (cfg 6) was selected on S2 from 8 candidates by a
pre-registered rule, highest final ball-sPCE on the trainer's own validation stream with ties within 0.02 nats going to
the lower index, each candidate trained with a single sweep seed (719). It is reused in every cell with seeds 711–715,
each trained to the 200,000-episode cap (PPO clip 0.2, 4 epochs per update, hidden width 128).

**Success-reward RL control.** In S2 and S12 only, the same configuration is trained with a terminal-success reward.
Nine of its ten runs were stopped by the trainer's wall-clock guard at 80 % of the job budget before the episode cap,
and the saved weights are the models of record; we state this as a disclosure of shorter training, not as a finding.

**Heuristics.** Random selects uniformly among feasible actions. Three heuristics reserve budget for the remaining
probes. B-spread (belief-free) maximises angular distance to the previous probe angles; B-fan (belief-free,
travel-nearest) stays at $\phi_t$ when allowed and cycles the approach offset; B-cov (belief-using) maximises coverage
under an online filter. In each cell the reference heuristic H\* is the best of the three on 200 pilot episodes, ties
broken B-spread < B-fan < B-cov; the pilot chose B-cov in S2 and S8 and B-fan in S4, S12 and A16-2. The choice was frozen
before any test episode and is not revisited here.

## 4 Experiments

**Pre-registration.** Amendment v6.0 and its addendum v6.1 were written before any v6 episode. They fix the test
windows, the three hypothesis families H6a, H6b and H6c, the equivalence margin δ, the Holm families, and the
evaluator check E12. The read-out script was committed before the first new record was read, and no outcome was
inspected before every block reached 100 % completeness. No policy was trained in this round: the students, RL
policies and success-reward controls are the frozen weights of the previous round, identified by their recorded
hashes. Values that no frozen rule produced are labelled report-only, exploratory or post hoc throughout.

**Test windows.** All test episodes are drawn from one disjoint stream, and within a window every method runs on the
same episodes with the same initial state, start angle and observation stream (a paired design). The primary window is
episodes 0–499; its episodes 0–299 were already evaluated, for a subset of the methods, in the previous round. Episodes
300–499 are fresh: no method had been evaluated on them. Every contrast is computed on both windows and reported side
by side. Every method has 500 episodes on the primary and 200 on the fresh window in every cell, and every $g_T$ block
is complete.

**Methods evaluated per cell.** G\* runs 1 and 2; R-125 and R-500; five round-2 students and five round-0 (BC)
students; five RL seeds; B-fan, B-spread and B-cov; and, in S2 and S12, five success-reward RL seeds. Random was not
extended to the new episodes and enters no contrast. In total there are 27 evaluated policy instances (counting seeds) in S2 and S12 and 22 in
the other cells.

**Statistics.** Contrasts are paired over episodes and use a crossed episode × seed bootstrap with B = 10,000 resamples
for the two-sided ci95 and p-value [CITE-MISSING: bootstrap CI (Efron)]. Seeds enter as one bootstrap factor: five for
the students, RL and BC students, two for G\* in the parity contrast (runs 1 and 2 as two "seeds"), and one for the
reduced planners and heuristics, which were run once. A p-value of 0 at this resolution is printed p < 1e-4.

- **H6a (parity).** Δ = student (5 seeds) − G\* (runs 1 + 2), success. (i) A difference test, two-sided. (ii) TOST at
  δ = 0.04: $p_{\mathrm{TOST}} = \max(p_{\mathrm{lower}}, p_{\mathrm{upper}})$ of the one-sided bootstrap p-values
  against −δ and +δ, with its ci90. "Equivalent within 4 pp" is licensed only where Holm rejects the TOST; otherwise the
  verdict is "neither a difference nor equivalence shown". No pooled estimate across cells is computed.
- **H6b (frontier).** Student − R-125 and student − R-500, success. "The student is more accurate than a reduced
  planner" is licensed only where Holm rejects with a positive sign.
- **H6c (DAgger vs BC).** Round-2 student − round-0 student, success, five seeds each. "DAgger improves success" is
  licensed only where Holm rejects with a positive sign; otherwise "not detected".
- **Holm** \[CITE-MISSING: Holm (1979)\] is applied over the 5 cells for the H6a difference test, the H6a TOST and H6c,
  and over the 10 contrasts for H6b, separately per window. BI, $g_T$, E12, the fresh-window replications and the
  report-only updates of earlier rows are not multiplicity-controlled.

**Power.** The design note expected 90 % half-widths of about 3.5–4 pp at 500 episodes; the observed half-widths were
2.84–3.85 pp (derived). With δ = 4 pp, equivalence could be shown only if a cell's point gap were well under 1 pp, so a
failure to show equivalence is largely a power outcome, not evidence of a difference.

**Why TOST replaces the previous gate.** The previous round's validation gate failed in 5/5 cells. Its success clause
added a multiple of the paired standard error to −δ, so at the observed standard errors its effective thresholds were
−1.23 to −1.72 pp against a nominal δ = 4 pp; a TOST at the stated margin is the direct test of the question that gate
was meant to answer.

**Evaluator check (E12, report-only).** E12 re-reads test episodes 0–99 at subdivision 16 instead of 8, for G\* run 1
and all five round-2 students in every cell. It reports per-method flip rates (the fraction of episodes whose success
outcome changes) and the student − G\* run 1 contrast at both resolutions. It is not used to re-decide any hypothesis.

**Latency.** Latency is not re-timed in this round. The frontier uses the previous round's latency job, which timed
student seed 701, full G\* and both reduced planners interleaved on the same G\*-reached decision states, 1,000 decisions
per S cell and 500 in A16-2, on 2-core runners that differ across cells. We report point medians per decision; the
pre-registered half-width rule for the G\*/student ratio is met only in A16-2. Latency is computation per decision; no
physical model of probe duration is used.

**Implementation and hardware.** Everything is numpy with hand-written backpropagation and single-threaded BLAS, run on
GitHub-hosted 2-core runners (CPU model not logged). The pre-run timing pilot projected about 733 CPU-h for the five new
rows, below the registered reduction threshold, so every row ran at its registered size. Table S lists all settings.

**Table S. Settings.** Constants without a results key are taken from the code and the amendments, not from a results
field.

| Component | Setting |
|---|---|
| Cells | Table 0 (κ, $n^\*$, τ); action grid 64 × 8, $|\mathcal{A}| = 512$ |
| G\* | `g2000_512_64`; two runs per cell (run 2 with salted policy and filter streams) |
| Reduced planners | R-125 `g125_512_16`, R-500 `g500_512_4`; one run per cell |
| Student | DeepSets head; round 0 BC + DAgger rounds 1–2; 3,000 label episodes (300 held out); 800 episodes per DAgger round, $\beta_{\mathrm{DAgger}}$ 0.5 then 0; 200 epochs per round; best held-out $\bar R$ checkpoint; Adam, lr 0.001, batch 256, hidden 128, $\beta_T$ 4.0, λ 0.5, ρ 0.05; seeds 701–705 |
| RL | PPO + critic, reward Δ ball-sPCE; cfg 6 selected on S2 (8 candidates, sweep seed 719); seeds 711–715; 200,000-episode cap; clip 0.2, 4 epochs, hidden 128; $g_T$ read-out $J = 16$, $L = 4{,}095$ |
| Success-reward RL | cfg 6, terminal-success reward, S2 and S12, seeds 711–715; 9 of 10 runs time-guard stopped |
| Heuristics | Random, B-spread, B-fan, B-cov; H\* chosen on 200 pilot episodes |
| Windows | test 0–499 (primary, 500 per method), 300–499 (fresh, 200); E12 on 0–99 |
| Evaluator | adaptive grid posterior, sub 8; E12 re-read at sub 16 |
| Statistics | crossed episode × seed bootstrap, B = 10,000; δ = 0.04; Holm over 5 (H6a, TOST, H6c) and over 10 (H6b) |
| Latency | previous-round job 1: 1,000 decisions per S cell, 500 in A16-2; point medians |

## 5 Results

### 5.1 C1. Distilled student versus shrunken planner: the frontier

**The latency axis.** Per decision and per cell, full G\* takes 0.910–4.880 s, R-500 0.048–0.194 s, R-125 0.022–0.116 s
and the student 0.326–0.500 ms (point medians from the previous round, no dispersion; Figure 1). The reduced planners
are therefore 19–47× faster than G\* (derived), and the student is 62–389× faster again than both reduced planners
(post hoc, no CI; last column of Table 2). Full G\* is about 2,544–9,767× slower per decision than the student (post
hoc, no CI). These ratios rest on one student seed and on runners that differ between cells, the pre-registered
half-width rule for the G\*/student ratio is met only in A16-2, and no task-time model is applied, so they are statements
about computation per decision, not about the duration of a probing episode.

**The cost of shrinking.** On the primary window the reduced planners lose 4.4–14.4 pp of success against G\* run 1
(point values, derived), from S12 R-500 (0.390 against 0.434) to A16-2 R-125 (0.330 against 0.474). Spending the Monte Carlo
budget on particles rather than outcome samples does not help uniformly: in S4, R-500 (0.390) is below R-125 (0.402).

**H6b.** By Holm, the student is more accurate than R-125 in all 5 cells and than R-500 in S4 and A16-2; against R-500
in S2, S8 and S12 no accuracy difference is shown (Table 2). Seven of the ten contrasts are rejected on 0–499, all with
a positive sign. The largest rejected p-value is 0.0098 (S12, R-125); the next, S8 against R-500 (p = 0.0314), is not
rejected, and neither are S2 (p = 0.1378) and S12 (p = 0.2688) against R-500. On the fresh 300–499 window only 2/10
contrasts survive Holm (S4 and A16-2 against R-125), so the fresh window replicates the direction, not the
significance; nine of the ten fresh point estimates are positive, and the exception, S12 against R-500, is
−0.011 [−0.072, 0.051]. Each reduced planner was run once, so its run-to-run variance is missing from these intervals;
the marginal rejections, S12 and S4 against R-125 with lower bounds of about +1.3 and +1.4 pp, could be sensitive to it.

**Table 2. H6b: student (5 seeds) − reduced planner, success.** Δ [ci95], two-sided p, Holm over 10 contrasts per
window. Latency ratios are post hoc point ratios of medians, no CI.

| Cell | − R-125, 0–499 | − R-500, 0–499 | − R-125, 300–499 | − R-500, 300–499 | R-125 / R-500 latency ÷ student |
|---|---|---|---|---|---|
| S2 | +0.0928 [0.044, 0.140], p < 1e-4, **yes** | +0.0368 [−0.012, 0.087], 0.1378, no | +0.094, 0.0198, no | +0.004, 0.9268, no | 231× / 389× |
| S4 | +0.0556 [0.014, 0.098], 0.0072, **yes** | +0.0676 [0.024, 0.112], 0.0016, **yes** | +0.112, 0.0002, **yes** | +0.077, 0.0198, no | 163× / 285× |
| S8 | +0.0628 [0.022, 0.104], 0.0022, **yes** | +0.0468 [0.004, 0.090], 0.0314, no | +0.066, 0.055, no | +0.026, 0.4638, no | 84× / 171× |
| S12 | +0.0564 [0.013, 0.099], 0.0098, **yes** | +0.0244 [−0.018, 0.067], 0.2688, no | +0.019, 0.5484, no | −0.011, 0.7368, no | 62× / 134× |
| A16-2 | +0.1532 [0.102, 0.204], p < 1e-4, **yes** | +0.1092 [0.058, 0.159], p < 1e-4, **yes** | +0.136, 0.0012, **yes** | +0.086, 0.032, no | 176× / 299× |

**Strongest comparator per cell (post hoc, no CI).** Taking, in each cell, the most accurate non-oracle method other
than the student on 0–499, the student clears it at the registered level in 1/5 cells, A16-2, where it is R-500. In the
other cells the strongest comparator is R-500 in S2, B-cov in S4 and S12, and RL in S8, and the student's untested point
margins over it are +3.68, +4.16, +2.56 and +2.44 pp in S2, S4, S8 and S12.

### 5.2 C2. Parity with G\* is not established

**H6a.** With both G\* runs in the contrast, the student's success point estimate is 0.3–3.7 pp below G\* in every cell
on 0–499, with no registered difference and no registered equivalence in any cell on either window (Table 1); deficits
of up to about 7–8 pp (ci95) cannot be excluded. All five primary point estimates are negative, from −0.28 pp (A16-2)
to −3.74 pp (S4); on the fresh window four are negative and A16-2 is +0.1 pp. In the other direction, on 0–499 the
student is not more than 4 pp better than G\* in any cell (unadjusted, per cell, p_upper ≤ 0.0348); on 300–499 this
fails in A16-2 (p = 0.1557). Equivalence required |gap| ≤ 0.15–1.16 pp depending on the cell; no cell met its own
threshold, A16-2 having the smallest p_TOST (0.0548; gap 0.28 against a requirement of 0.15 pp, ci90 lower bound
−4.12 pp). S4 is the weakest cell: its ci90 lies below 0 on both windows, [−0.0716, −0.0036] and [−0.106, −0.0005], an
unregistered one-sided indication of a deficit. Every one of these success numbers should be read beside the
evaluator-grid sensitivity of Section 6.1, which is of the same size.

**Table 1. H6a: student (5 seeds) − G\* (runs 1 + 2), success.** Δ [ci95]; ci90 and p_TOST of the TOST at δ = 4 pp;
Holm (difference and TOST) over 5 cells; G\* run 2 − run 1 on 0–499; E12 shift = change of the 100-episode student − G\*
contrast from sub 8 to sub 16 (derived, report-only).

| Cell | Δ 0–499 [ci95] | ci90 | p_TOST | Holm | Δ 300–499 [ci95] | ci90 fresh | p_TOST fresh | G\* r2 − r1 | E12 shift |
|---|---|---|---|---|---|---|---|---|---|
| S2 | −0.0262 [−0.0688, 0.0168] | [−0.0616, 0.0092] | 0.2621 | no / no | −0.036 [−0.114, 0.042] | [−0.102, 0.029] | 0.4524 | +0.014 | −1.6 pp |
| S4 | −0.0374 [−0.0784, 0.0024] | [−0.0716, −0.0036] | 0.4559 | no / no | −0.053 [−0.1165, 0.0095] | [−0.106, −0.0005] | 0.6561 | −0.002 | +4.6 pp |
| S8 | −0.0292 [−0.0704, 0.0136] | [−0.0640, 0.0060] | 0.2908 | no / no | −0.034 [−0.095, 0.028] | [−0.085, 0.017] | 0.4211 | +0.032 | +5.0 pp |
| S12 | −0.0196 [−0.0532, 0.0148] | [−0.0480, 0.0088] | 0.1157 | no / no | −0.016 [−0.067, 0.035] | [−0.0585, 0.026] | 0.1659 | 0.000 | −4.6 pp |
| A16-2 | −0.0028 [−0.0496, 0.0436] | [−0.0412, 0.0358] | 0.0548 | no / no | +0.001 [−0.077, 0.080] | [−0.064, 0.0665] | 0.1557 | +0.024 | −0.6 pp |

Footnotes. Upper-margin p (0–499, per cell, unadjusted): 0.0014 / 0.0003 / 0.0004 / 0.0009 / 0.0348. BI difference
(0–499, uncorrected): −0.093 / −0.138 / −0.103 / −0.055 / +0.024 nats.

**Ball information (exploratory).** On BI the student is lower in S4, −0.138 [−0.202, −0.075] nats, p < 1e-4, and in
S8, −0.103 [−0.172, −0.033], p = 0.0048. Both survive an unregistered Holm over the five BI p-values, and both are below
0.05 on the fresh window as well (S4 p = 0.0206, S8 p = 0.0354). S2 is nominally lower on 0–499 only (p = 0.0206) and
is not a finding; S12 (p = 0.0664) and A16-2 (p = 0.638) show no difference.

**Teacher variance.** G\*'s run 2 − run 1 success difference is +0.014, −0.002, +0.032, 0.000 and +0.024 on 0–499 (S2,
S4, S8, S12, A16-2), none significant, with half-widths of about 4–5 pp; on the fresh window it reaches +0.05 in S2 and
A16-2, again not significant. From the same initial state, the two runs choose the same first action on only 0.274,
0.402, 0.452, 0.426 and 0.314 of the primary episodes (0.245, 0.415, 0.445, 0.420 and 0.305 fresh). The student's own
seed spread is 2.8–6.2 pp (derived). The student − G\* point gaps are therefore of the same magnitude as the teacher's
own run-to-run variation, and a single G\* run would have understated the uncertainty of the parity contrast.

**v6 update of the previous single-run row (report-only).** Against G\* run 1 alone the gaps are −1.92, −3.84, −1.32,
−1.96 and +0.92 pp (none significant); S4 now exceeds the previous round's 0.2–2.5 pp range and A16-2 has changed sign.
This instability under 200 added episodes is a further reason not to read the single-run gaps as estimates of a fixed
deficit.

### 5.3 C3. DAgger versus behaviour cloning, and the baseline rows

**H6c (the ablation).** Round-0 (BC-only) students already reach the round-2 success level (|r2 − r0| ≤ 1.3 pp); DAgger
adds no detectable accuracy (95 % upper bounds ≤ 4.8 pp on 0–499, ≤ 7.1 pp fresh; no equivalence test). Holm rejects in
0/5 cells on both windows (Table 3); the primary p-values lie in 0.453–0.997 and the fresh ones in 0.5372–0.9208. Round 2
− round 0 on BI is not significant either (p = 0.0564–0.8056, uncorrected). The training record points the same way:
the held-out regret of the kept checkpoints of round 0 and round 2 overlaps in every cell (for example 0.2803–0.2848
against 0.2776–0.2857 in S2; report-only). Regret on student-visited states, the quantity DAgger targets, was not
measured, so this ablation shows that the rounds add no detectable success in this setting, not why.

**Table 3. H6c: DAgger round 2 − BC round 0, success (5 seeds each).** Δ [ci95]; Holm over 5 cells, rejected in none.
5-seed means are post hoc, no CI.

| Cell | Δ 0–499 [ci95], p | Δ 300–499 [ci95], p | round 0 / round 2 mean, 0–499 |
|---|---|---|---|
| S2 | +0.0132 [−0.0224, 0.0480], 0.453 | +0.011 [−0.049, 0.071], 0.715 | 0.4856 / 0.4988 |
| S4 | +0.0084 [−0.0228, 0.0400], 0.5968 | +0.002 [−0.040, 0.046], 0.9206 | 0.4492 / 0.4576 |
| S8 | +0.0072 [−0.0196, 0.0336], 0.5984 | +0.002 [−0.043, 0.046], 0.9208 | 0.4116 / 0.4188 |
| S12 | +0.0004 [−0.0280, 0.0304], 0.997 | −0.012 [−0.050, 0.027], 0.5372 | 0.414 / 0.4144 |
| A16-2 | −0.0052 [−0.0316, 0.0208], 0.6834 | −0.005 [−0.042, 0.034], 0.7826 | 0.4884 / 0.4832 |

**Heuristics (report-only, v6 update of an earlier row).** The student is above the pilot-chosen H\* in all cells on
0–499, by +6.68, +8.96, +7.48, +5.64 and +17.12 pp, each ci95 excluding 0; on the fresh window S2 (p = 0.0694) and S12
(p = 0.0672) are not below 0.05. H\* is, however, not the best test heuristic in S4, S8 and S12, and against the best
heuristic the untested point margins are about +4.2 / +5.1 / +2.4 pp (post hoc, no CI). In A16-2 the best test
heuristic is B-cov rather than the pilot's B-fan, by 0.2 pp, and the margin over it is +16.92 pp (post hoc). B-spread
scores 0.006–0.074 in every cell and is a weak reference, not a competitor.

**RL (report-only).** The student is significantly above the S2-tuned RL configuration in 4/5 cells on 0–499 (S8 not)
and in 3/5 on the fresh window. The 0–499 differences are +0.0856 (S2), +0.0612 (S4), +0.0256 [−0.010, 0.062] (S8),
+0.0568 (S12) and +0.2688 (A16-2). Against the success-reward control the student is higher by +0.1096 [0.066, 0.153] in
S2 and +0.0708 [0.024, 0.116] in S12, with the control's training cut short by the time guard. On RL's own objective,
"student higher on $g_T$" holds only in A16-2 (+0.709 nats, one-sided lower bound 0.479), where RL uses 2.0 of 3 probes
in 4/5 seeds; the comparator fails there rather than the student excelling. In S2, S4 and S8, RL − student $g_T$ is
significantly positive, and in S2 and S4 the registered inversion flag is true: RL is ahead on $g_T$ while the student
is ahead on success. The configuration was tuned once on S2, and whether it is under-tuned elsewhere was not tested.

**Behaviour (descriptive).** The student travels less than G\* in every cell, for example 0.487–0.674 against 0.820 rad
per episode in S2 and 0.044–0.056 against 0.110 rad in S12 (seed ranges against G\* run 1).
RL travels the most, 2.061–2.546 rad in S2 with about 3 probes per episode. We claim no mechanism for the student's
lower travel.

## 6 Discussion

### 6.1 C4. Methods note: evaluator-grid sensitivity and teacher stochasticity

**Evaluator grid.** On episodes 0–99, with G\* run 1 and all five student seeds, changing only the read-out grid from
sub 8 to sub 16 moves student − G\* by 4.6–5.0 pp in S4, S8 and S12, comparable to the 4 pp margin; in S2 (1.6 pp) and
A16-2 (0.6 pp) the shift is small. Per cell the contrast moves from −0.026 to −0.042 (S2), −0.036 to +0.010 (S4),
−0.020 to +0.030 (S8), +0.008 to −0.038 (S12) and +0.050 to +0.044 (A16-2). Neither grid shows a significant difference
on these 100 episodes, whose ci95 half-widths are 7–10 pp. The sign changes in 3/5 cells, and the shifts do not favour
either policy systematically. The success outcome flips on 4–13 % of episodes in the S cells and 0–1 % in A16-2; for G\*
the flip rates are 0.10, 0.08, 0.07, 0.07 and 0.01. This is a *sensitivity* of the read-out: a thresholded success
computed from a finite-resolution posterior grid, applied to near-tied posteriors, decides a non-trivial fraction of
outcomes, and the decision falls differently for different policies. Re-deciding H6a on sub 16 would be post hoc and was
not done; E12 covers only 100 episodes and G\* run 1, and it cannot correct the primary contrasts.

**Teacher stochasticity.** First-decision agreement between two G\* runs from the same state is 0.25–0.45 across cells
and windows; no run-2 − run-1 success difference is significant (Section 5.2). The teacher is thus a distribution over
action sequences, not a fixed target, and two of its runs differ in success by up to 3.2 pp on the primary window.

**Lesson.** In this setting, success contrasts of a few pp depend on the read-out grid and on the teacher's own Monte
Carlo variation at the size of the equivalence margin. Parity claims for amortized planners therefore need teacher
reruns and an evaluator check registered in advance, and a single-run, single-grid contrast is not an estimate of a
fixed gap. This complements the practice in amortized experimental design of reporting a contrastive bound as the
quality of a learned policy \cite{foster2021deep, rainforth2024modern}: whichever quantity is reported, its sensitivity
to the evaluator should be reported beside it. Our RL rows illustrate the point from the other side, since in two cells
the bound and the posterior read-out order the student and RL differently.

### 6.2 Interpretation

**What the frontier says.** For a practitioner who must replace G\* by something three to four orders of magnitude
faster per decision, the registered evidence favours distillation over the two reduced planners we tested in 7 of 10
contrasts, and in none does a reduced planner come out significantly ahead. The advantage is clearest against R-125 and
in A16-2, and it is unresolved against R-500 in three S cells. Shrinking the planner already costs 4.4–14.4 pp against
G\* run 1 for a 19–47× speed-up, whereas the student pays a further 62–389× less per decision. The frontier is,
however, drawn from one run of each reduced planner, from latency medians of the previous round, and from only two
reduced configurations, both with the same $N \cdot M$ budget; a reduced planner with a better split of its budget, or a
cheap information-based heuristic, could move it. The fresh window confirms the direction in nine of ten point
estimates but not the significance, which is what 200 episodes can deliver at this effect size.

**What parity says.** The study was designed with enough episodes for a 4 pp equivalence test, and it shows neither a
difference nor equivalence. The point estimates are all on the student's deficit side on the primary window, S4 shows
a one-sided indication of a deficit, and the student's ball information is lower in S4 and S8, so a real shortfall in
some cells is plausible. Its size, however, is of the same order as G\*'s own run-to-run difference and as the shift
induced by the evaluator grid alone. The honest summary is that parity is not established and a deficit of up to about
7–8 pp is not excluded.

**What the ablation says.** The DAgger rounds were meant to correct the covariate shift between planner-visited and
student-visited beliefs \cite{ross2011reduction}. In this setting, with three to four probes per episode and a dense
per-action label at every decision, behaviour cloning on G\*-visited states already reaches the round-2 success level
within the resolution of 500 episodes. Short horizons limit how far a student can drift from states the teacher visits,
which may be why DAgger's benefit is not visible here; we did not test this explanation, and the absence of an
equivalence test means we cannot say the rounds are useless either.

**Comparison with the previous round.** The previous round reported only student − G\* contrasts against a single G\*
run on 300 episodes. With 500 episodes and the second G\* run, the S4 gap widened and the A16-2 gap changed sign, and the
new evaluator check shows that the read-out alone moves contrasts of this size. The previous verdicts stand as recorded,
but the present design is the better basis for any statement about a few-pp gap.

## 7 Limitations

1. **Teacher variance.** It is estimated from only two G\* runs, so the G\* component of the bootstrap is poorly
   estimated.
2. **Single runs.** The reduced planners and H\* were run once per cell, so their run-to-run variance is missing from
   the H6b and heuristic intervals.
3. **Evaluator.** E12 covers 100 episodes and G\* run 1 only, and it cannot correct the 0–499 contrasts.
4. **Latency.** The latencies are point medians from the previous round's job 1, without dispersion, for one student
   seed; the CI rule for the G\*/student ratio is met in 1/5 cells, the runners differ across cells, and there is no
   task-time model, so no saving in episode time is shown.
5. **Windows.** Episodes 0–299 of the primary window were seen in the previous round. The fresh window has 200
   episodes, and its intervals are about 1.6× wider (derived).
6. **Multiplicity.** BI, $g_T$, the fresh replications and the baseline rows are not Holm-controlled; for example, the
   S8 fresh G\* − student $g_T$ difference (p = 0.0068) should not be read as a finding.
7. **DAgger.** Regret on student-visited states was not measured, and no equivalence test was registered for H6c.
8. **Comparators.** The RL configuration was tuned once, on S2, with one sweep seed; the success-reward control was
   truncated by the time guard; H\* comes from a 200-episode pilot of the previous round; no cheap information-based
   heuristic was included.
9. **A16-2.** The second library changes shape family, $K$ and $n^\*$ at once, is run at one κ, and shares 8 identities
   with an earlier library. A cross-cell trend of the student − G\* run 1 gap on G\* travel is uninformative: slope
   −0.0070 per 100° (ci95 [−0.137, 0.124]); the CI spans about 26 pp, so the test is uninformative, and no statement
   about independence from travel cost is made.
10. **G\* is a greedy reference.** A report-only one-step look-ahead screen of the previous round shows headroom over
    greedy selection in nats at 512 candidates (S2 +0.0658 [0.0297, 0.1084], S12 +0.0422 [0.0250, 0.0614]); headroom in
    success terms was not measured.
11. **Scope.** Planar simulation (TouchBED), one fingertip on a fixed circle, a likelihood shared by planner, filter and
    evaluator, five cells, frozen policies of the previous round, no hardware. Jobs were time-guarded and resumed with
    identical commands on the remaining episodes; resumption is assumed to be outcome-neutral.
12. **Not run, by decision.** Additional G\* or reduced-planner runs, a sub-16 re-read of H6a, latency re-timing, RL
    re-tuning, retraining, and new BI or $g_T$ tests.

## 8 Conclusion

We asked how a policy distilled from a cost-aware greedy information-gain touch planner compares, as a fast
replacement, with simply shrinking the planner, whether it matches the full planner once the planner's own variance is
counted, and whether the DAgger rounds of distillation add anything over behaviour cloning. A pre-registered study in
five cells, four travel costs on one shape library and a second library at one travel cost, gives four answers. First,
as a fast policy, distilling G\* gave more accuracy than shrinking it in 7 of 10 registered contrasts, at 62–389× lower
per-decision latency; on fresh episodes only the direction held. Second, parity with G\* is neither shown nor refuted,
and deficits of about 7–8 pp are not excluded. Third, the DAgger rounds added no detectable accuracy over behaviour
cloning. Fourth, evaluator choice and teacher stochasticity move the contrasts by as much as the margin, so few-pp
claims about amortized planners need registered teacher reruns and evaluator checks. The next steps follow from the
limitations: repeated runs of the planner and of the reduced planners to put their variance into the intervals, more
reduced configurations and a cheap information-based heuristic on the same frontier, regret measured on
student-visited states, per-cell RL tuning, and a task-time model of a probe. Pre-registered; simulation; preliminary.
