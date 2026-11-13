<!-- Stage 17 PAPER_DRAFT [v6], 2026-11-13; revised in stage 19 [v6] pass 1; revised in stage 19 [v6] pass 2; fresh-context subagent; prompts paper/mypaper/prompts/stage17_v6_{system,user}.txt and stage19_v6_{system,user}.txt; outline paper/mypaper/sections/00_outline.md (stage 16 v6). Sources of numbers: A = results/v6/14_v6_analysis.json, D = results/v6/15_derived_v6.json (post hoc, no CI), P = results/v6/18_posthoc_v6.json (post hoc, report-only, not pre-registered), v5 = results/v5/results_v5.json; E6 = results/v5/14_e6_analysis.json (registered latency statistic, G*/student median per-decision ratio with ci95, copied and rounded to integers); "(derived)" = arithmetic printed in results/v6/14_analysis.md; method constants carried from paper/mypaper/v5/draft_v5_final.md §3 (code and amendments, not a results field); DAgger warm start from code/tools_v5_manifests.py (--init). -->

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
   "median latency per decision (s, log scale; phase-1 timings)".
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
timings from an earlier phase of the study, medians plotted without their intervals; computation per decision only, no
task-time or hardware model) for travel cost κ = 2, 4, 8, 12 on shape
library S and κ = 2 on library A16. Filled and hollow circles are two independent G* runs. Diamonds are the 5-seed
student mean with the seed range. Stars mark student-vs-reduced-planner contrasts confirmed by Holm (7 of 10 at the
registered bootstrap seed and at 100,000 resamples, 5 of 10 under one of 11 bootstrap seeds, both post hoc; 2 of 10 on the 200 fresh episodes, where
only the direction replicates). Each reduced planner is a single run, and both have the same Monte Carlo budget. Dashed
lines show the pilot-chosen heuristic H* and RL, whose latency was not timed. The student's position relative to G* is
undecided: neither a difference nor equivalence within 4 pp is shown (Table 1), and changing the evaluator grid alone
shifts that contrast by point values of up to 5 pp, with a post hoc ci95 that excludes 0 in one cell only.
Simulation; preliminary.
```

# Amortizing a Cost-Aware Information-Gain Touch Planner: A Pre-Registered Accuracy–Latency Study in TouchBED

## Abstract

A cost-aware greedy information-gain touch planner (G\*) for active tactile localization under travel cost chooses
each probe by expected information per unit of travel, at up to several seconds of computation per decision. We ask
whether distilling or shrinking the planner buys more accuracy per millisecond, and whether DAgger adds anything over
behaviour cloning (BC). In a pre-registered five-cell planar simulation study (travel cost κ = 2/4/8/12 on one shape
library, κ = 2 on a second, A16), every compared method (all but a random baseline) runs the same 500 test episodes,
200 fresh, with two G\* runs.
By Holm, the student is more accurate than the smaller of two single-run, same-budget reduced planners in all five
cells and than the larger in two (7/10 contrasts; 5/10 under one of 11 bootstrap seeds, post hoc), at 62–389× lower
per-decision latency (point ratios of medians; a computational gain only, with no task-time or hardware model). On the fresh episodes only 2/10 survive Holm, so only the direction replicates.
Parity with G\* is neither shown nor refuted at a 4 pp margin, a test with little power by design: point estimates are
0.3–3.7 pp below G\*, and deficits of about 5–8 pp are not excluded. Under our recipe (warm-started rounds,
lowest-held-out-regret checkpoints) no DAgger benefit over BC is detected. Changing only the evaluator grid shifts the
student − G\* contrast by point values of up to 5 pp (post hoc ci95 excludes 0 in one cell), and two G\* runs agree on
only 25–45 % of first decisions. Simulation; preliminary.

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

Two features of this setting make the comparison harder than it looks. First, the teacher is itself a Monte Carlo
procedure: two runs of G\* from the same state need not choose the same touch, so "the teacher's accuracy" is a
distribution, and a contrast against a single teacher run understates its uncertainty. Second, success is a thresholded
read-out of a posterior computed on a finite grid, so a few near-tied episodes can change their outcome when only the
evaluator changes. At the sample sizes that a planner costing seconds per decision allows, a parity test between
student and teacher is therefore a weak headline on its own; the more informative comparison is between the student and
the cheaper versions of the teacher that a practitioner could deploy instead, reported together with the teacher's
run-to-run variation and with the evaluator's sensitivity. An earlier pre-registered phase of this study tested parity
alone and could not decide it; Appendix A summarises that history and what this paper reuses from it.

We therefore pre-registered, before any of the present episodes was run, three hypothesis families. The
pre-registration is internal: a timestamped commit of the amendment to the project repository, not an entry in a public
registry (Section 4). The families are the
accuracy–latency frontier of the student against two reduced planners (H6b), parity with G\* counting the teacher's own
run-to-run variance and tested with two one-sided tests (TOST) at a 4 pp margin (H6a), and DAgger against behaviour
cloning (H6c). The design adds 200 fresh test episodes, an independent second G\* run, and an evaluator-grid check in
every cell and for every student seed. The experiments run in TouchBED, our planar simulator of active tactile
localization, in which the task, the particle filter, the planners, the learned policies and the evaluator are
implemented on one shared likelihood. The five cells vary travel cost κ = 2, 4, 8 and 12 on one shape library and add a
second library, A16, at κ = 2.

We make one narrow positive claim and three qualified ones, in decision order.

- **C1. Frontier against two reduced planners.** By Holm, the student is more accurate than the smaller reduced planner
  (R-125) in all 5 cells and than the larger one (R-500) in S4 and A16-2; against R-500 in S2, S8 and S12 no accuracy
  difference is shown. This is 7/10 registered contrasts on episodes 0–499 at the registered bootstrap seed; under one
  of 11 bootstrap seeds (post hoc) it is 5/10, because two contrasts sit near the Holm threshold; at 100,000 resamples
  (post hoc) it is again 7/10, with S12 − R-125 just inside its Holm cut (Appendix B). On the fresh window only 2/10
  contrasts survive Holm under every one of the 11 seeds and at 100,000 resamples, so the fresh window replicates the
  direction, not the significance. Both reduced planners have the same Monte Carlo budget and were run once each, and
  the evaluator-grid check did not re-read them, so this one positive claim, unlike the null ones, has no evaluator
  check. The student is 62–389× faster per decision than both (point ratios of medians), while the reduced planners
  themselves are 19–47× faster than G\*; these are gains in computation per decision only, since no task-time or
  hardware model is applied. Taking post hoc, in each cell, the strongest non-oracle comparator, the registered H6b
  contrast against it is Holm-rejected in 1/5 cells (A16-2, where it is R-500); in the other cells it is either not
  rejected or not covered by any registered test.
- **C2. Parity is not established.** With G\*'s two runs in the contrast, the student's success point estimate is
  0.3–3.7 pp below G\* in every cell, with no registered difference and no registered equivalence; deficits of about
  5–8 pp, depending on the cell, cannot be excluded. The TOST had little power by design. On the primary window the
  student is not more than 4 pp better than G\* in any cell (unadjusted, per cell).
- **C3. No DAgger benefit detected under this recipe.** Round-0 (BC-only) students already reach the round-2 success
  level (|r2 − r0| ≤ 1.3 pp). The recipe warm-starts every DAgger round from the previous round's weights and keeps the
  checkpoint with the lowest regret on teacher-visited held-out decisions, which is often an early epoch. No
  equivalence test was registered, so this is not evidence that DAgger is useless in general.
- **C4. Methods note.** Changing only the read-out grid shifts student − G\* by point values of 4.6–5.0 pp in three
  cells, comparable to the 4 pp margin, but on 100 episodes the post hoc ci95 of the shift excludes 0 only in S12; and
  two G\* runs from the same state agree on only 0.25–0.45 of first decisions. Success contrasts of a few pp in this
  setting therefore depend on the evaluator and on the teacher's Monte Carlo variation, which is a reporting lesson for
  evaluations of amortized information-gathering policies.

The study is a measurement in a planar simulator, not a method paper, and none of it is evidence about hardware.
Section 2 reviews related work. Section 3 defines the task, the planner and its reduced versions, the student and its
training rounds, and the comparators. Section 4 gives the pre-registration, the data windows and the statistics.
Section 5 reports C1–C3, Section 6 discusses them together with the C4 methods note, and Sections 7 and 8 state the
limitations and conclude. Appendix A gives the study history and Appendix B the bootstrap-seed check of H6b.

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
likelihood or a differentiable simulator \cite{ivanova2021implicit, blau2022optimizing}, and RL has been applied to
sequential and robust experimental design more broadly \cite{asano2022sequential, shen2023reinforcement};
semi-amortized variants refine the policy online \cite{hedman2025step}; nested particle filters amortize design in
dynamical systems \cite{iqbal2024recursive}; and transformer policies amortize inference and acquisition jointly
\cite{huang2026aline}. In touch, RL agents learn exploration for recognition with rewards on correct classification
\cite{riou2021seeing, fleer2020efficient}, on classification, exploration and pose \cite{riou2024reinforcement}, or
learn when to stop \cite{niemann2024when}; TANDEM3D co-trains exploration and decision making on 3D contacts
\cite{xu2023tandem3d}, and Tactile MNIST offers a benchmark that includes localization \cite{schneider2025tactile}. A
third route imitates an information-gathering expert: a clairvoyant oracle \cite{choudhury2017adaptive} or a nonmyopic
active-search expert \cite{nguyen2024amortized}, typically through DAgger's no-regret reduction
\cite{ross2011reduction}. These works compare learned policies with heuristics, with each other or with the expert, and
usually report one evaluator.

**How amortized policies are evaluated.** In amortized experimental design a contrastive bound of the sPCE type is
usually both the training objective and the reported quality of a learned policy \cite{foster2021deep,
blau2022optimizing}, and reviews of the field treat such bounds as the standard yardstick \cite{rainforth2024modern}.
In tactile localization the reported quality is more often a thresholded success computed from the estimator's
posterior. Whether the two kinds of read-out rank policies in the same way, how sensitive a thresholded read-out is to
the resolution of the posterior it is computed from, and how much of a student − teacher gap is the teacher's own
Monte Carlo variation, are rarely checked; imitation work usually treats the expert as a fixed target
\cite{ross2011reduction, choudhury2017adaptive}. We know of no pre-registered comparison of a distilled policy against
reduced versions of its own teacher on an accuracy–latency frontier that also reports the teacher's run-to-run
variance, a BC-versus-DAgger ablation and the sensitivity of the contrasts to the evaluator. This paper supplies that
comparison, as a measurement rather than as a new method.

## 3 Method

### 3.1 Task, belief, cost and metrics

**Simulator.** All experiments run in TouchBED, our planar simulator of active tactile localization. It implements the
object and finger geometry, the sensor model, the particle filter, the planners, the learned policies and the
evaluator described below, all on the same likelihood.

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
$K$ and $n^\*$ at once, and its first 8 identities are an asymmetric library used in an earlier phase, so it is only
partly new. Table 0 lists the five pre-registered cells; the S2 and S12 budgets are carried from earlier calibration
runs.

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
the record of the earlier phase extended to the new episodes, and run 2 salts the policy and decision-filter streams
while keeping state, start-angle and observation streams fixed. Both runs enter the parity contrast.

**Reduced planners.** R-125 (`g125_512_16`) and R-500 (`g500_512_4`) keep all 512 candidates and cut particles and
outcome samples; each is run once per cell. They are two points of one shrink family, with the same Monte Carlo budget;
candidate subsampling ($C < 512$), other budget splits and accelerated implementations of G\* were not tested.

**Complexity and design rationale.** Per decision, a planner evaluates $O(MNC)$ likelihoods and builds ball-neighbour
lists in $O(N^2)$, on top of assimilating the last observation; the latter terms do not depend on $C$. The product
$N \cdot M$ is 128,000 for G\* and 2,000 for both reduced planners, so the reduced planners differ in how they split the
same Monte Carlo budget: R-125 keeps more outcome samples per candidate, R-500 more particles, and its $O(N^2)$ term is
larger. Keeping $C = 512$ fixes the action set, so a reduced planner and the student choose among the same actions as
G\*. G\* is a greedy reference: we measure faster policies against it and make no claim that it is optimal
\cite{javdani2012efficient, ottenhaus2018active}.

### 3.3 Student: shared head, behaviour-cloning round and DAgger rounds

**Head.** The student is a belief-free DeepSets head \cite{zaheer2017deep}. Each touch in the
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
>    at every decision; hold out 300 episodes for $\bar R$, train on 2,700. Round 0 starts from a fresh initialisation.
> 2. Train $\pi_\theta$ on $\mathcal{L}$ for a fixed 200 epochs; after each epoch evaluate held-out $\bar R$ and **keep
>    the checkpoint with the lowest held-out $\bar R$** (every run trained all 200 epochs; the kept checkpoint is the
>    best one, not the last).
> 3. **Rounds 1 and 2 (DAgger).** Roll out 800 episodes per round, executing G\*'s action with probability
>    $\beta_{\mathrm{DAgger}}$ (0.5 in round 1, 0 in round 2) and $\pi_\theta$'s otherwise; run G\*'s filter alongside,
>    label every visited belief with $s$, aggregate (3,500 and 4,300 training episodes), and repeat step 2, **warm-started
>    from the kept checkpoint of the previous round** (round 1 from round 0, round 2 from round 1).
> 4. Freeze the kept checkpoint of every round and record its weight hash before any test episode.

The deployed student is the round-2 checkpoint of seeds 701–705. The **BC student** is the round-0 checkpoint of the
same seeds; comparing the two is the one component ablation of this paper (H6c). In S2 and S12 the round-0 labels are
re-used from earlier calibration runs, where library, κ, τ and code path match; the DAgger rounds are new in every
cell. Two qualifiers apply to the selection rule. First, $\bar R$ is measured on G\*-visited decisions, so it cannot
register what the DAgger rounds are meant to add, namely labels on student-visited beliefs \cite{ross2011reduction,
choudhury2017adaptive}. Second, because each DAgger round is warm-started and keeps its lowest-$\bar R$ epoch, the kept
round-1 and round-2 checkpoints are often early (Table 4): the kept epoch index is 39–187 in round 0, 2–92 in round 1
and 0–126 in round 2, and in several cell-seeds the kept round-2 network is the round-1 network after a few epochs on
the aggregated data (for example epochs 8, 7 and 5 for seeds 702, 704 and 705 in S2, and epoch 0 for seed 701 in A16-2).
H6c therefore tests this particular recipe, DAgger with warm starts and early stopping on teacher-visited regret, rather
than DAgger in general.

**Table 4. Kept-checkpoint epoch per cell and seed, round 0 / round 1 / round 2** (epoch index as logged, of 200; copied
from the training record, report-only).

| Cell | 701 | 702 | 703 | 704 | 705 |
|---|---|---|---|---|---|
| S2 | 89 / 73 / 124 | 46 / 10 / 8 | 39 / 43 / 50 | 68 / 4 / 7 | 106 / 9 / 5 |
| S4 | 44 / 40 / 17 | 74 / 11 / 126 | 65 / 27 / 36 | 97 / 6 / 10 | 92 / 23 / 14 |
| S8 | 115 / 92 / 30 | 101 / 2 / 25 | 109 / 44 / 54 | 83 / 58 / 63 | 98 / 27 / 41 |
| S12 | 72 / 50 / 70 | 68 / 32 / 43 | 93 / 45 / 4 | 187 / 80 / 41 | 187 / 3 / 50 |
| A16-2 | 54 / 37 / 0 | 96 / 2 / 14 | 121 / 11 / 47 | 95 / 55 / 29 | 84 / 24 / 28 |

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
before any test episode and is not revisited here. No cheap information-based heuristic was included, and apart from
the heuristics and RL no comparator sits near the student's latency.

## 4 Experiments

**Pre-registration.** Amendment v6.0 and its addendum v6.1 were written before any of the present episodes was run. They
fix the test windows, the three hypothesis families H6a, H6b and H6c, the equivalence margin δ, the Holm families, and
the evaluator check E12. This pre-registration is internal to the project: the amendment, its addendum and the
read-out script are timestamped commits in the project's version-controlled repository, not entries in a public
registry, so their precedence over the data rests on the commit order (Appendix A), which an external reader can audit
only with access to the repository. The read-out script was committed before the first new record existed (Appendix A
gives the commit), and no outcome was inspected before every block reached 100 % completeness. No policy was trained for this
study's test phase: the students, RL policies and success-reward controls are the frozen weights of the earlier phase
(Appendix A), identified by their recorded hashes. Values that no frozen rule produced are labelled report-only,
exploratory or post hoc throughout.

**Test windows.** All test episodes are drawn from one disjoint stream, and within a window every compared method runs on the
same episodes with the same initial state, start angle and observation stream (a paired design). The primary window is
episodes 0–499; its episodes 0–299 had already been evaluated, for a subset of the methods (the students, G\* run 1 and
the heuristics, but not the reduced planners), in the earlier phase, so H6a on 0–499 is not fully prospective, whereas
H6b is. Episodes 300–499 are fresh: no method had been evaluated on them. Every contrast is computed on both windows and
reported side by side. Every method listed in the next paragraph, that is every method except Random, has 500 episodes
on the primary and 200 on the fresh window in every cell (per-method episode counts of the read-out), and every $g_T$
block is complete. Random has only the episodes of the earlier phase and enters no contrast.

**Methods evaluated per cell.** G\* runs 1 and 2; R-125 and R-500; five round-2 students and five round-0 (BC)
students; five RL seeds; B-fan, B-spread and B-cov; and, in S2 and S12, five success-reward RL seeds. Random was not
extended to the new episodes and enters no contrast. In total there are 27 evaluated policy instances (counting seeds)
in S2 and S12 and 22 in the other cells.

**Statistics.** Contrasts are paired over episodes and use a crossed episode × seed bootstrap with B = 10,000 resamples
for the two-sided ci95 and p-value \cite{efron1979bootstrap}. Seeds enter as one bootstrap factor: five for
the students, RL and BC students, two for G\* in the parity contrast (runs 1 and 2 as two "seeds"), and one for the
reduced planners and heuristics, which were run once. With two G\* runs resampled with replacement, about half of the
resamples draw the same run twice, so the teacher component of the interval rests on two values and is poorly
estimated (Limitation 1). A p-value of 0 at this resolution is printed p < 1e-4.

- **H6a (parity).** Δ = student (5 seeds) − G\* (runs 1 + 2), success. (i) A difference test, two-sided. (ii) TOST at
  δ = 0.04: $p_{\mathrm{TOST}} = \max(p_{\mathrm{lower}}, p_{\mathrm{upper}})$ of the one-sided bootstrap p-values
  against −δ and +δ, with its ci90. "Equivalent within 4 pp" is licensed only where Holm rejects the TOST; otherwise the
  verdict is "neither a difference nor equivalence shown". No pooled estimate across cells is computed.
- **H6b (frontier).** Student − R-125 and student − R-500, success. "The student is more accurate than a reduced
  planner" is licensed only where Holm rejects with a positive sign.
- **H6c (DAgger vs BC).** Round-2 student − round-0 student, success, five seeds each. "DAgger improves success" is
  licensed only where Holm rejects with a positive sign; otherwise "not detected".
- **Holm** \cite{holm1979simple} is applied over the 5 cells for the H6a difference test, the H6a TOST and H6c,
  and over the 10 contrasts for H6b, separately per window. BI, $g_T$, E12, the fresh-window replications and the
  report-only baseline rows are not multiplicity-controlled.

**Power.** The TOST at δ = 4 pp had little power by design. The pre-registered design note expected 90 % half-widths of
about 3.5–4 pp at 500 episodes and stated that "equivalence can be shown only if the point gap is near 0". The observed
half-widths were 2.84–3.85 pp (derived). Unadjusted, equivalence would have required a cell's point gap to be within
δ minus its half-width, that is |gap| ≤ 0.15–1.16 pp depending on the cell; under the registered Holm over five cells
the smallest p_TOST must in addition fall below 0.05/5, which is stricter still and, in A16-2, close to unattainable
even at a zero gap. A failure to show equivalence is therefore largely a power outcome, not evidence of a difference,
and C2 is close to a designed-in null. The informative content of H6a is the interval itself: on the deficit side the
ci90 bounds of Table 1 reach between −4.12 pp (A16-2) and −7.16 pp (S4), which is the margin each cell could have
certified at the unadjusted level.

**Evaluator check (E12, report-only).** E12 re-reads test episodes 0–99 at subdivision 16 instead of 8, for G\* run 1
and all five round-2 students in every cell. It reports per-method flip rates (the fraction of episodes whose success
outcome changes) and the student − G\* run 1 contrast at both resolutions. It is not used to re-decide any hypothesis.
The reduced planners were not re-read.

**Post hoc checks (report-only, not pre-registered).** In response to review, four checks were run with the frozen
loaders and statistics unchanged, and none re-decides a hypothesis: (P1) a bootstrap ci95 of the E12 shift of
student − G\* (sub 16 − sub 8, episodes 0–99); (P2) the H6b Holm count under bootstrap seeds 0 (the registered one) to
10; (P3) the kept-checkpoint epochs of every training run (Table 4); and (P4) the H6b family re-run with 100,000
instead of 10,000 bootstrap resamples at the registered bootstrap seed (Appendix B).

**Latency.** Latency was not re-timed for this study. The frontier uses the latency job of the earlier phase, which
timed student seed 701, full G\* and both reduced planners interleaved on the same G\*-reached decision states, 1,000
decisions per S cell and 500 in A16-2, on 2-core runners that differ across cells. The registered latency statistic is
the median over decisions of the per-decision G\*/student ratio, with a bootstrap ci95: 9,933 [8,179, 10,224] in S2,
6,990 [4,747, 7,270] in S4, 3,463 [2,680, 3,645] in S8, 2,523 [2,068, 2,675] in S12 and 8,301 [8,080, 8,472] in A16-2
(copied from the earlier phase's latency read-out, rounded to integers). Its pre-registered half-width rule is met only
in A16-2; the rule concerns the width of the interval relative to the median, so in the S cells the ratio has an
interval but not one as narrow as registered. The same rule also fails for the G\* median in every S cell and for some
reduced-planner medians (R-125 in S2, S4 and S8; R-500 in S4). The other latency figures in this paper, including the
student-versus-reduced-planner ratios and the 2,544–9,767× G\*/student range, are ratios of the per-method medians:
point values without intervals and not the registered statistic. Latency is computation per decision only; no physical
model of probe duration or travel time, no overlap of planning with motion and no hardware is modelled, so no saving in
episode time follows from these figures.

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
| Student | DeepSets head; round 0 BC + DAgger rounds 1–2, each DAgger round warm-started from the previous round's kept checkpoint; 3,000 label episodes (300 held out); 800 episodes per DAgger round, $\beta_{\mathrm{DAgger}}$ 0.5 then 0; 200 epochs per round; best held-out $\bar R$ checkpoint (Table 4); Adam, lr 0.001, batch 256, hidden 128, $\beta_T$ 4.0, λ 0.5, ρ 0.05; seeds 701–705 |
| RL | PPO + critic, reward Δ ball-sPCE; cfg 6 selected on S2 (8 candidates, sweep seed 719); seeds 711–715; 200,000-episode cap; clip 0.2, 4 epochs, hidden 128; $g_T$ read-out $J = 16$, $L = 4{,}095$ |
| Success-reward RL | cfg 6, terminal-success reward, S2 and S12, seeds 711–715; 9 of 10 runs time-guard stopped |
| Heuristics | Random, B-spread, B-fan, B-cov; H\* chosen on 200 pilot episodes |
| Windows | test 0–499 (primary, 500 per method), 300–499 (fresh, 200); E12 on 0–99 |
| Evaluator | adaptive grid posterior, sub 8; E12 re-read at sub 16 |
| Statistics | crossed episode × seed bootstrap, B = 10,000, registered bootstrap seed 0; δ = 0.04; Holm over 5 (H6a, TOST, H6c) and over 10 (H6b) |
| Latency | earlier-phase job 1: 1,000 decisions per S cell, 500 in A16-2; registered statistic = median per-decision G\*/student ratio with bootstrap ci95; all other ratios are point ratios of medians; computation only, no task-time model |

## 5 Results

### 5.1 C1. Distilled student versus shrunken planner: the frontier

**The latency axis.** Per decision and per cell, full G\* takes 0.910–4.880 s, R-500 0.048–0.194 s, R-125 0.022–0.116 s
and the student 0.326–0.500 ms (medians from the earlier phase, plotted in Figure 1 without their intervals). The
reduced planners are therefore 19–47× faster than G\* (derived), and the student is 62–389× faster again than both
reduced planners (post hoc, no CI; point ratios of medians; last column of Table 2). Full G\* is about 2,544–9,767×
slower per decision than the student as a ratio of medians (post hoc, no CI). The registered statistic for this
comparison is instead the median per-decision G\*/student ratio, with its ci95: 9,933 [8,179, 10,224] (S2), 6,990
[4,747, 7,270] (S4), 3,463 [2,680, 3,645] (S8), 2,523 [2,068, 2,675] (S12) and 8,301 [8,080, 8,472] (A16-2), copied
from the earlier phase's latency read-out (Section 4). Its pre-registered half-width rule is met only in A16-2, and the
same rule also fails for the G\* medians of the S cells and for some reduced-planner medians. All of these ratios rest on
one student seed and on runners that differ between cells, and no task-time or hardware model is applied, so they are
statements about computation per decision, not about the duration of a probing episode: whether a 48–194 ms or even a
multi-second decision would lengthen an episode depends on probe and travel durations and on whether planning can
overlap with motion, none of which is modelled here. No reduced planner
sits near the student's latency: the gap between the student and the faster reduced planner is still more than an
order of magnitude in every cell.

**The cost of shrinking.** On the primary window the reduced planners lose 4.4–14.4 pp of success against G\* run 1
(point values, derived), from S12 R-500 (0.390 against 0.434) to A16-2 R-125 (0.330 against 0.474). Spending the Monte
Carlo budget on particles rather than outcome samples does not help uniformly: in S4, R-500 (0.390) is below R-125
(0.402).

**H6b.** By Holm, the student is more accurate than R-125 in all 5 cells and than R-500 in S4 and A16-2; against R-500
in S2, S8 and S12 no accuracy difference is shown (Table 2). Seven of the ten contrasts are rejected on 0–499, all with
a positive sign. The largest rejected p-value is 0.0098 (S12, R-125); the next, S8 against R-500 (p = 0.0314), is not
rejected, and neither are S2 (p = 0.1378) and S12 (p = 0.2688) against R-500. On the fresh 300–499 window only 2/10
contrasts survive Holm (S4 and A16-2 against R-125), so the fresh window replicates the direction, not the
significance; nine of the ten fresh point estimates are positive, and the exception, S12 against R-500, is
−0.011 [−0.072, 0.051].

**How fragile the count is.** Two sources of fragility qualify the 7/10. First, each reduced planner was run once, so
its run-to-run variance is missing from these intervals; G\*'s own two runs differ by up to 3.2 pp on the primary
window, and a noisier reduced planner is unlikely to vary less. The marginal rejections, S12 and S4 against R-125 with
lower bounds of about +1.3 and +1.4 pp, could be sensitive to it. Second, the count depends on the bootstrap's own
Monte Carlo error (post hoc check P2, report-only): re-running the ten contrasts under bootstrap seeds 0 (registered) to
10, Holm rejects 7/10 on 0–499 under seeds 0–9 and 5/10 under seed 10, where S4 and S12 against R-125 drop out; across
the 11 seeds their p-values range over 0.0072–0.0124 and 0.0076–0.0104, close to the Holm cut-off at their ranks. On
the fresh window the count is 2/10 under all 11 seeds (Appendix B). A better-resolved bootstrap (post hoc check P4,
report-only; 100,000 resamples at the registered seed) gives the same seven rejections on 0–499 and the same two on
300–499, but it does not remove the fragility: S12 − R-125 has p = 0.00968 against its rank-6 Holm cut of α/5 with
α = 0.05, and S4 − R-125 has p = 0.0105 against its rank-7 cut of α/4, while the next contrast, S8 − R-500, has
p = 0.03238 and is not rejected. The registered seed gives the result of record, but the 7/10 rests on two contrasts
that sit within bootstrap error of the threshold. E12 did not re-read the reduced
planners, so H6b's sensitivity to the evaluator grid is unknown.

**Table 2. H6b: student (5 seeds) − reduced planner, success.** Δ [ci95], two-sided p, Holm over 10 contrasts per
window (registered bootstrap seed). Latency ratios are post hoc point ratios of medians, no CI. Each reduced planner is
a single run.

| Cell | − R-125, 0–499 | − R-500, 0–499 | − R-125, 300–499 | − R-500, 300–499 | R-125 / R-500 latency ÷ student |
|---|---|---|---|---|---|
| S2 | +0.0928 [0.044, 0.140], p < 1e-4, **yes** | +0.0368 [−0.012, 0.087], 0.1378, no | +0.094, 0.0198, no | +0.004, 0.9268, no | 231× / 389× |
| S4 | +0.0556 [0.014, 0.098], 0.0072, **yes** | +0.0676 [0.024, 0.112], 0.0016, **yes** | +0.112, 0.0002, **yes** | +0.077, 0.0198, no | 163× / 285× |
| S8 | +0.0628 [0.022, 0.104], 0.0022, **yes** | +0.0468 [0.004, 0.090], 0.0314, no | +0.066, 0.055, no | +0.026, 0.4638, no | 84× / 171× |
| S12 | +0.0564 [0.013, 0.099], 0.0098, **yes** | +0.0244 [−0.018, 0.067], 0.2688, no | +0.019, 0.5484, no | −0.011, 0.7368, no | 62× / 134× |
| A16-2 | +0.1532 [0.102, 0.204], p < 1e-4, **yes** | +0.1092 [0.058, 0.159], p < 1e-4, **yes** | +0.136, 0.0012, **yes** | +0.086, 0.032, no | 176× / 299× |

**Strongest comparator per cell (post hoc, no CI).** Taking, in each cell, the most accurate non-oracle method other
than the student on 0–499 (a post hoc choice of comparator), the registered H6b contrast against that comparator is
Holm-rejected in 1/5 cells, A16-2, where it is R-500. In the other cells the strongest comparator is R-500 in S2 (its
registered contrast not rejected), B-cov in S4 (no registered test), RL in S8 (no registered test; report-only ci95
[−0.010, 0.062]), and in S12 a tie between R-500 and B-cov at
0.390 (B-cov is the one listed by the derived record; the registered contrast against R-500 is not rejected); the
student's untested point margins over it are +3.68, +4.16,
+2.56 and +2.44 pp in S2, S4, S8 and S12, the last being the same against either tied comparator. The student is
therefore not shown to be the best non-oracle policy in S2, S4, S8 or S12.

### 5.2 C2. Parity with G\* is not established

**H6a.** With both G\* runs in the contrast, the student's success point estimate is 0.3–3.7 pp below G\* in every cell
on 0–499, with no registered difference and no registered equivalence in any cell on either window (Table 1); deficits
of about 5–8 pp, depending on the cell, cannot be excluded (ci95 lower bounds −6.9, −7.8, −7.0, −5.3 and −5.0 pp in S2,
S4, S8, S12 and A16-2). All five primary point estimates are negative, from −0.28 pp (A16-2) to −3.74 pp (S4); on the
fresh window four are negative and A16-2 is +0.1 pp. In the other direction, on 0–499 the student is not more than 4 pp
better than G\* in any cell (unadjusted, per cell, p_upper ≤ 0.0348); on 300–499 this fails in A16-2 (p = 0.1557).
Unadjusted, equivalence required |gap| ≤ 0.15–1.16 pp depending on the cell, and Holm makes the requirement stricter
(Section 4); no cell met even its unadjusted threshold, A16-2 having the smallest p_TOST (0.0548; gap 0.28 against an
unadjusted requirement of 0.15 pp, ci90 lower bound −4.12 pp). S4 is the weakest cell: its ci90 lies below 0 on both
windows, [−0.0716, −0.0036] and [−0.106, −0.0005], an unregistered one-sided indication of a deficit. Every one of
these success numbers should be read beside the evaluator-grid sensitivity of Section 6.1, whose point values are of the
same size.

**Table 1. H6a: student (5 seeds) − G\* (runs 1 + 2), success.** Δ [ci95]; ci90 and p_TOST of the TOST at δ = 4 pp;
Holm (difference and TOST) over 5 cells; G\* run 2 − run 1 on 0–499; E12 shift = change of the 100-episode student − G\*
contrast from sub 8 to sub 16 (derived, report-only; its post hoc ci95 is in Section 6.1).

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
is not a finding; S12 (p = 0.0664) and A16-2 (p = 0.638) show no difference. Because BI is a continuous read-out that
does not pass through the success threshold, these exploratory deficits are the strongest indication in the data that
the student falls short of G\* in S4 and S8.

**Teacher variance.** G\*'s run 2 − run 1 success difference is +0.014, −0.002, +0.032, 0.000 and +0.024 on 0–499 (S2,
S4, S8, S12, A16-2), none significant, with half-widths of about 4–5 pp; on the fresh window it reaches +0.05 in S2 and
A16-2, again not significant. From the same initial state, the two runs choose the same first action on only 0.274,
0.402, 0.452, 0.426 and 0.314 of the primary episodes (0.245, 0.415, 0.445, 0.420 and 0.305 fresh). The student's own
seed spread is 2.8–6.2 pp (derived). The student − G\* point gaps are therefore of the same magnitude as the teacher's
own run-to-run variation, and a single G\* run would have understated the uncertainty of the parity contrast. Against
G\* run 1 alone, the gaps also moved noticeably between the earlier 300-episode read-out and the present 500 episodes
(Appendix A), a further reason not to read single-run gaps as estimates of a fixed deficit. For readers who want parity
per teacher run, the read-out also carries student − G\* run 1 alone as a report-only row (Table A1, Appendix A): on
0–499 it is −1.92, −3.84, −1.32, −1.96 and +0.92 pp, none with p below 0.05. No row against G\* run 2 alone was
registered or computed, and no new statistic is introduced here; the two-run H6a contrast of Table 1 remains the
contrast of record.

### 5.3 C3. DAgger versus behaviour cloning, and the baseline rows

**H6c (the ablation).** Round-0 (BC-only) students already reach the round-2 success level (|r2 − r0| ≤ 1.3 pp); no
DAgger benefit is detected under this recipe (95 % upper bounds ≤ 4.8 pp on 0–499, ≤ 7.1 pp fresh; no equivalence
test). Holm rejects in 0/5 cells on both windows (Table 3); the primary p-values lie in 0.453–0.997 and the fresh ones
in 0.5372–0.9208. Round 2 − round 0 on BI is not significant either (p = 0.0564–0.8056, uncorrected). The training
record points the same way: the held-out regret of the kept checkpoints of round 0 and round 2 overlaps in every cell
(for example 0.2803–0.2848 against 0.2776–0.2857 in S2; report-only). Two properties of the recipe limit what this
null can mean. Each DAgger round is warm-started from the previous round's kept weights, and the kept round-2
checkpoint is often an early epoch (0–126 across the 25 cell-seeds, Table 4), selected by regret on G\*-visited
decisions, which by construction cannot see the student-visited states DAgger targets. Regret on student-visited states
was not measured, and no last-epoch checkpoint was evaluated. The ablation therefore shows that this recipe's DAgger
rounds add no detectable success in this setting, not that DAgger cannot help, and not why.

**Table 3. H6c: DAgger round 2 − BC round 0, success (5 seeds each).** Δ [ci95]; Holm over 5 cells, rejected in none.
5-seed means are post hoc, no CI.

| Cell | Δ 0–499 [ci95], p | Δ 300–499 [ci95], p | round 0 / round 2 mean, 0–499 |
|---|---|---|---|
| S2 | +0.0132 [−0.0224, 0.0480], 0.453 | +0.011 [−0.049, 0.071], 0.715 | 0.4856 / 0.4988 |
| S4 | +0.0084 [−0.0228, 0.0400], 0.5968 | +0.002 [−0.040, 0.046], 0.9206 | 0.4492 / 0.4576 |
| S8 | +0.0072 [−0.0196, 0.0336], 0.5984 | +0.002 [−0.043, 0.046], 0.9208 | 0.4116 / 0.4188 |
| S12 | +0.0004 [−0.0280, 0.0304], 0.997 | −0.012 [−0.050, 0.027], 0.5372 | 0.414 / 0.4144 |
| A16-2 | −0.0052 [−0.0316, 0.0208], 0.6834 | −0.005 [−0.042, 0.034], 0.7826 | 0.4884 / 0.4832 |

**Heuristics (report-only).** The student is above the pilot-chosen H\* in all cells on 0–499, by +6.68, +8.96, +7.48,
+5.64 and +17.12 pp, each ci95 excluding 0; on the fresh window S2 (p = 0.0694) and S12 (p = 0.0672) are not below
0.05. H\* is, however, not the best test heuristic in S4, S8 and S12, and against the best heuristic the untested point
margins are about +4.2 / +5.1 / +2.4 pp (post hoc, no CI). In A16-2 the best test heuristic is B-cov rather than the
pilot's B-fan, by 0.2 pp, and the margin over it is +16.92 pp (post hoc). B-spread scores 0.006–0.074 in every cell and
is a weak reference, not a competitor.

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
sub 8 to sub 16 shifts student − G\* by point values of 4.6–5.0 pp in S4, S8 and S12, comparable to the 4 pp margin; in
S2 (1.6 pp) and A16-2 (0.6 pp) the shift is small. Per cell the contrast moves from −0.026 to −0.042 (S2), −0.036 to
+0.010 (S4), −0.020 to +0.030 (S8), +0.008 to −0.038 (S12) and +0.050 to +0.044 (A16-2). These shifts are themselves
uncertain on 100 episodes. A post hoc bootstrap ci95 of the shift (check P1, report-only) is −1.6 [−8.6, +5.2] pp in
S2, +4.6 [−2.2, +11.6] in S4, +5.0 [−0.6, +11.0] in S8, −4.6 [−9.4, −0.2] in S12 and −0.6 [−3.0, +1.2] in A16-2: only
the S12 interval excludes 0. "Comparable to the margin" is therefore a statement about point values; what the data
establish is that shifts of that size are plausible, not that they occurred in every cell. Neither grid shows a
significant student − G\* difference on these 100 episodes, whose ci95 half-widths are about 7–10 pp. The sign of the
contrast changes in 3/5 cells, and the shifts do not favour either policy systematically. The success outcome flips on
4–13 % of episodes in the S cells and 0–1 % in A16-2; for G\* the flip rates are 0.10, 0.08, 0.07, 0.07 and 0.01, so
much of each shift comes from the teacher's own flips. This is a *sensitivity* of the read-out: a thresholded success
computed from a finite-resolution posterior grid, applied to near-tied posteriors, decides a non-trivial fraction of
outcomes, and the decision falls differently for different policies. Re-deciding H6a on sub 16 would be post hoc and was
not done; E12 covers only 100 episodes and G\* run 1, and it cannot correct the primary contrasts.

**Teacher stochasticity.** First-decision agreement between two G\* runs from the same state is 0.25–0.45 across cells
and windows; no run-2 − run-1 success difference is significant (Section 5.2). The teacher is thus a distribution over
action sequences, not a fixed target, and two of its runs differ in success by up to 3.2 pp on the primary window.

**Lesson.** In this setting, success contrasts of a few pp depend on the read-out grid and on the teacher's own Monte
Carlo variation, at point values the size of the equivalence margin. Parity claims for amortized planners therefore
need teacher reruns and an evaluator check registered in advance, with enough episodes in the check to put an interval
on the shift, and a single-run, single-grid contrast is not an estimate of a fixed gap. This complements the practice in
amortized experimental design of reporting a contrastive bound as the quality of a learned policy \cite{foster2021deep,
rainforth2024modern}: whichever quantity is reported, its sensitivity to the evaluator should be reported beside it.
Our RL rows illustrate the point from the other side, since in two cells the bound and the posterior read-out order the
student and RL differently.

### 6.2 Interpretation

**What the frontier says.** For a practitioner who must replace G\* by something three to four orders of magnitude
faster per decision, the registered evidence favours distillation over the two reduced planners we tested in 7 of 10
contrasts, and in none does a reduced planner come out significantly ahead. The advantage is clearest against R-125 and
in A16-2, and it is unresolved against R-500 in three S cells. Shrinking the planner already costs 4.4–14.4 pp against
G\* run 1 for a 19–47× speed-up, whereas the student pays a further 62–389× less per decision. These speed-ups are
computational: R-500 already decides in 48–194 ms, and without a task-time model of probing and travel we cannot say
whether any of them would shorten a physical episode. The frontier is,
however, drawn from one run of each reduced planner, from latency medians of the earlier phase, and from only two
reduced configurations, both with the same $N \cdot M$ budget and all 512 candidates; no shrunken or accelerated planner
sits near the student's latency. Two of the seven rejections are within bootstrap Monte Carlo error of the Holm
threshold. A reduced planner with a better split of its budget, candidate subsampling, an accelerated implementation of
G\*, or a cheap information-based heuristic could move the frontier. The fresh window confirms the direction in nine of
ten point estimates but not the significance, which is what 200 episodes can deliver at this effect size. The claim is
therefore "distillation was more accurate than these two reduced planners", not "distillation beats shrinking".

**What parity says.** The TOST at a 4 pp margin had little power by design (Section 4): with observed 90 % half-widths
of 2.84–3.85 pp, equivalence was reachable only for point gaps well under about 1 pp unadjusted, and under Holm not even
then in every cell. That the study shows neither a difference nor equivalence is therefore the expected outcome, and
the informative content is the interval: per cell, the data could certify equivalence only at margins between about
4.1 and 7.2 pp (the deficit-side ci90 bounds of Table 1, unadjusted). The point estimates are all on the student's
deficit side on the primary window, S4 shows a one-sided indication of a deficit, and the student's ball information is
lower in S4 and S8, so a real shortfall in some cells is plausible. Its size, however, is of the same order as G\*'s own
run-to-run difference and as the point shifts induced by the evaluator grid alone. The honest summary is that parity is
not established and a deficit of about 5–8 pp, depending on the cell, is not excluded.

**What the ablation says.** The DAgger rounds were meant to correct the covariate shift between planner-visited and
student-visited beliefs \cite{ross2011reduction}. In this setting, with three to four probes per episode and a dense
per-action label at every decision, behaviour cloning on G\*-visited states already reaches the round-2 success level
within the resolution of 500 episodes. Short horizons limit how far a student can drift from states the teacher visits,
which may be why DAgger's benefit is not visible here; we did not test this explanation. The recipe also matters: each
DAgger round starts from the previous round's weights and keeps its lowest-regret epoch on teacher-visited decisions,
which in several cell-seeds is within the first ten epochs of the round, so the round-2 student is often close to the
network it was initialised from. A recipe that selected checkpoints on student-visited regret, kept the last epoch, or
trained each round from scratch might behave differently. The absence of an equivalence test means we cannot say the
rounds are useless either.

**What the reader can take away.** For an engineer facing the same choice, the measured evidence says three things.
A sub-millisecond distilled policy was in no cell significantly less accurate than either of two planners shrunk by a
factor of 64 in Monte Carlo budget, and was more accurate than the smaller of them in every cell at the registered
bootstrap seed; whether it matches the full planner is
not decided by 500 episodes; and the interactive DAgger rounds, as run here, did not pay for themselves. Each of these
statements comes with the evaluator and teacher-variance qualifications of Section 6.1.

## 7 Limitations

1. **Teacher variance.** It is estimated from only two G\* runs, so the G\* component of the bootstrap is poorly
   estimated: about half of the resamples draw the same run twice. No sensitivity analysis holding the two runs fixed
   was run, and G\* runs 3–4 were not run.
2. **Single runs of the reduced planners.** The reduced planners and H\* were run once per cell, so their run-to-run
   variance is missing from the H6b and heuristic intervals; given G\*'s own run-to-run differences, the H6b intervals
   are probably too narrow.
3. **Bootstrap-seed sensitivity of H6b.** The 7/10 count holds under 10 of 11 bootstrap seeds and falls to 5/10 under
   one (post hoc, report-only); S4 and S12 against R-125 sit within bootstrap Monte Carlo error of the Holm threshold.
   At 100,000 resamples (post hoc check P4, report-only) the count is again 7/10 on 0–499 and 2/10 on 300–499, but
   S12 − R-125 (p = 0.00968) lies just below its Holm cut, so the count still turns on Monte Carlo resolution. No
   sensitivity that inflates the reduced-planner term by a G\*-sized run-to-run variance was run.
4. **Narrow shrink family; no comparator near the student's latency.** Both reduced planners keep all 512 candidates
   and the same $N \cdot M$ budget, and both are still 62–389× slower than the student. Apart from the heuristics and
   RL, no comparator sits near the student's latency: candidate subsampling, a pruned or accelerated G\*, and a cheap
   information-based heuristic were not tested.
5. **Evaluator.** E12 covers 100 episodes and G\* run 1 only, it did not re-read the reduced planners, and it cannot
   correct the 0–499 contrasts. Its shifts are point values whose post hoc ci95 excludes 0 in one cell only.
6. **Latency, task time and hardware.** The latencies are medians from the earlier phase's job 1, for one student
   seed, and were not re-timed. Only the registered G\*/student statistic (median per-decision ratio) is reported with
   a ci95; its pre-registered half-width rule is met in 1/5 cells, the same rule fails for the G\* medians of the S
   cells and for some reduced-planner medians, and every other ratio in the paper is a point ratio of medians without
   an interval. The runners differ across cells, and there is no task-time model of probe duration and travel, no
   model of planning overlapping with motion, and no hardware check, so the gain is computational only and no saving
   in episode time, throughput or real-robot success is shown.
7. **Windows.** Episodes 0–299 of the primary window had been evaluated, for the students, G\* run 1 and the heuristics,
   in the earlier phase, so H6a on 0–499 is not fully prospective. The fresh window has 200 episodes, and its intervals
   are about 1.6× wider (derived).
8. **Multiplicity.** BI, $g_T$, the fresh replications and the baseline rows are not Holm-controlled; for example, the
   S8 fresh G\* − student $g_T$ difference (p = 0.0068) should not be read as a finding.
9. **DAgger.** Each DAgger round is warm-started from the previous round's weights, and checkpoints were selected on
   regret over G\*-visited decisions, often at early epochs. Regret on student-visited states was not measured, no
   last-epoch checkpoint was evaluated, no horizon sweep was run, and no equivalence test was registered for H6c.
10. **Comparators.** The RL configuration was tuned once, on S2, with one sweep seed; the success-reward control was
    truncated by the time guard; H\* comes from a 200-episode pilot of the earlier phase.
11. **TOST power.** The parity test had little power by design at δ = 4 pp, so C2 is close to a designed-in null.
12. **A16-2.** The second library changes shape family, $K$ and $n^\*$ at once, is run at one κ, and shares 8 identities
    with an earlier library. A cross-cell trend of the student − G\* run 1 gap on G\* travel is uninformative: slope
    −0.0070 per 100° (ci95 [−0.137, 0.124]); the CI spans about 26 pp, so the test is uninformative, and no statement
    about independence from travel cost is made.
13. **G\* is a greedy reference.** A report-only one-step look-ahead screen of the earlier phase shows headroom over
    greedy selection in nats at 512 candidates (S2 +0.0658 [0.0297, 0.1084], S12 +0.0422 [0.0250, 0.0614]); headroom in
    success terms was not measured.
14. **Scope.** Planar simulation (TouchBED), one fingertip on a fixed circle, a likelihood shared by planner, filter and
    evaluator, five cells, frozen policies of the earlier phase, no hardware. Jobs were time-guarded and resumed with
    identical commands on the remaining episodes; resumption is assumed to be outcome-neutral.
15. **Not run, by decision or because the refinement budget was used.** Additional G\* or reduced-planner runs,
    comparators near the student's latency, E12 on the reduced planners, a sub-16 re-read of H6a, latency re-timing, a
    task-time model or hardware check, RL re-tuning, retraining (including last-epoch or student-visited-regret DAgger
    checkpoints), new BI or $g_T$ tests, and a sensitivity of H6b that inflates the reduced-planner term by G\*'s
    observed run-to-run variance.
16. **Internal pre-registration.** The amendment, addendum and read-out script were registered as timestamped commits
    in the project's own repository, not in a public registry; their precedence over the data can be checked only from
    the commit history (Appendix A).

## 8 Conclusion

We asked how a policy distilled from a cost-aware greedy information-gain touch planner compares, as a fast
replacement, with simply shrinking the planner, whether it matches the full planner once the planner's own variance is
counted, and whether the DAgger rounds of distillation add anything over behaviour cloning. An internally
pre-registered study (timestamped repository commits) in five cells, four travel costs on one shape library and a second library at one travel cost, gives four answers. First,
as a fast policy, distilling G\* gave more accuracy than shrinking it in 7 of 10 registered contrasts against two
single-run, same-budget reduced planners, at 62–389× lower per-decision latency (point ratios of medians, a
computational gain with no task-time model); two of the seven are within bootstrap error of the threshold (5/10 under
one of 11 bootstrap seeds, 7/10 at 100,000 resamples, both post hoc), and on fresh episodes only the direction held
(2/10). Second, parity with G\* is neither shown nor refuted by a test that had little power by design, and deficits of
about 5–8 pp are not excluded. Third, under our recipe of warm-started rounds and lowest-regret checkpoints, the DAgger
rounds added no detectable accuracy over behaviour cloning. Fourth, evaluator choice and teacher stochasticity move the
contrasts by point values as large as the margin, with intervals that exclude zero in one cell, so few-pp claims about
amortized planners need registered teacher reruns and evaluator checks. The next steps follow from the limitations:
repeated runs of the planner and of the reduced planners to put their variance into the intervals, more reduced
configurations including candidate subsampling, an accelerated G\* and a cheap information-based heuristic near the
student's latency, an evaluator check that covers the reduced planners, DAgger checkpoints selected on student-visited
regret or taken at the last epoch, per-cell RL tuning, and a task-time model of a probe or a small hardware check.
Pre-registered; simulation; preliminary.

## Appendix A. Study history

This study is the second pre-registered phase of a project on amortizing G\*. The first phase asked only whether the
distilled student matches G\*. Its pre-registered validation gate failed in 5/5 cells, as had the single-cell gates of
the rounds before it, and its test contrasts against a single G\* run on 300 episodes were too wide to decide anything.
The present phase therefore re-framed the question around the frontier against reduced planners, added the TOST, the
second G\* run, the fresh episodes and the evaluator check, and reused from the first phase the frozen student, BC, RL
and success-reward weights, the round-0 labels in S2 and S12, the pilot choice of H\*, the latency job, and the
evaluations of episodes 0–299 for the students, G\* run 1 and the heuristics. The read-out script `code/analysis_v6.py`
was added in commit `ae3c3899` (2026-11-10, 01:47 UTC), before any record of the present phase existed, and has not been
modified since; the first result commits of this phase followed later the same day. Amendment v6.0 and addendum v6.1
are likewise commits of the same repository made before the first result commit. "Pre-registered" in this paper
therefore means internally pre-registered by timestamped repository commits; no external registry was used.

**Why TOST replaces the earlier gate.** The first phase's success clause added a multiple of the paired standard error
to −δ, so at the observed standard errors its effective thresholds were −1.23 to −1.72 pp against a nominal
δ = 4 pp; a TOST at the stated margin is the direct test of the question that gate was meant to answer.

**Update of the earlier single-run row (report-only).** Against G\* run 1 alone the 500-episode gaps are −1.92, −3.84,
−1.32, −1.96 and +0.92 pp (none significant); S4 now exceeds the first phase's 0.2–2.5 pp range and A16-2 has changed
sign. This instability under 200 added episodes is a further reason not to read the single-run gaps as estimates of a
fixed deficit. Table A1 copies the full row, which uses the same crossed bootstrap with five student seeds and the one
G\* run; it is not Holm-controlled and decides nothing.

**Table A1. Student (5 seeds) − G\* run 1 alone, success (report-only; read-out row
`v5_row_updates > student_minus_gstar_run1_success`).** Δ [ci95], two-sided p.

| Cell | 0–499 | 300–499 |
|---|---|---|
| S2 | −0.0192 [−0.0636, 0.0244], 0.3936 | −0.011 [−0.088, 0.064], 0.7696 |
| S4 | −0.0384 [−0.0824, 0.0068], 0.0988 | −0.058 [−0.129, 0.012], 0.1056 |
| S8 | −0.0132 [−0.0512, 0.0256], 0.5064 | −0.014 [−0.075, 0.046], 0.6486 |
| S12 | −0.0196 [−0.056, 0.0172], 0.2904 | −0.026 [−0.080, 0.027], 0.3394 |
| A16-2 | +0.0092 [−0.036, 0.0564], 0.6964 | +0.026 [−0.051, 0.102], 0.506 |

**Comparison with the first phase.** The first phase reported only student − G\* contrasts against a single G\* run on
300 episodes. With 500 episodes and the second G\* run, the S4 gap widened and the A16-2 gap changed sign, and the new
evaluator check shows that the read-out alone can shift contrasts of this size. The first phase's verdicts stand as
recorded, but the present design is the better basis for any statement about a few-pp gap.

## Appendix B. Bootstrap-seed check of H6b (post hoc, report-only)

Number of the ten H6b contrasts rejected by Holm under bootstrap seeds 0 (registered) to 10, with the frozen bootstrap
(B = 10,000) and Holm procedure unchanged.

| Window | Seeds 0–9 (each) | Seed 10 | Contrasts that drop out under seed 10 |
|---|---|---|---|
| 0–499 | 7 | 5 | S4 − R-125, S12 − R-125 |
| 300–499 | 2 | 2 | none (S4 − R-125 and A16-2 − R-125 rejected under every seed) |

**100,000 resamples (post hoc check P4, report-only).** The same ten contrasts re-run with 100,000 instead of 10,000
resamples at the registered bootstrap seed 0, Holm unchanged (α = 0.05 over 10 contrasts per window).

| Window | Rejected | Same set as the registered read-out | p-values nearest the Holm cut |
|---|---|---|---|
| 0–499 | 7 / 10 | yes | S12 − R-125 0.00968 (rank 6, cut α/5, rejected); S4 − R-125 0.0105 (rank 7, cut α/4, rejected); S8 − R-500 0.03238 (rank 8, cut α/3, not rejected) |
| 300–499 | 2 / 10 | yes | A16-2 − R-125 0.0013 and S4 − R-125 0.0006 rejected; S2 − R-125 0.0208 and S4 − R-500 0.02034 not rejected |

The better-resolved bootstrap therefore reproduces the registered counts, 7/10 and 2/10, but on 0–499 the decision
still turns on the rank-6 p-value lying just below α/5; had it exceeded α/5, Holm's step-down would have stopped there
and both S12 − R-125 and S4 − R-125 would have fallen, which is the pattern behind the 5/10 under bootstrap seed 10.
