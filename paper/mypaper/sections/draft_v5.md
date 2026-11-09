<!-- Stage 17 PAPER_DRAFT [v5], run 41, 2026-11-09; fresh-context subagent; template paper_draft.md verbatim; prompts paper/mypaper/prompts/stage17_v5_*.txt -->

```
FIGURE 1 PROMPT (v5; generated schematic for panels A-C, panel D plotted separately from results/v5/results_v5.json)

Target model: Nano Banana 2 (image generation). Output: one wide scientific schematic figure, aspect ratio 3:1 (full
text width of a two-column robotics paper, about one third of a page tall), pure white background (#FFFFFF), clean
flat-vector style, no photorealism, no 3D shading, no gradients, no drop shadows, no textures, no decorative icons
beyond those listed, no people, no robot arm, no logos, no watermark. Uniform line weights (thin 1.5 px outlines,
2.5 px arrows). Font: one clean sans-serif (Helvetica/Arial-like), dark grey #222222, all text horizontal, no text
other than the exact labels quoted below, spelled exactly as given (keep Greek letters and symbols exactly: φ, ψ, κ,
Δφ, π, *, ×, °, ′). Accent colours: BLUE #1F6FB4 = information / probing, ORANGE #E07B1A = travel / cost, and one
second-library colour PURPLE #7A4FA3 used ONLY for the A16-2 outline in panel B. Neutral greys for objects (#9A9A9A
fill, #555555 outline). Four panels side by side, left to right, separated by generous white space, no boxes around
panels A, B and C. Each panel has a bold panel letter in its top-left corner: "A", "B", "C", "D". Approximate widths:
A 22 %, B 30 %, C 28 %, D 20 %.

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
    outside the circle: "c(a) = 1 + κ|Δφ|/π". A small open orange circle at the arrow end, labelled "φ′".
 7. From φ′, a straight BLUE arrow pointing inward toward the polygon, tilted about 15° away from the radial
    direction; a thin dotted grey radial reference line from φ′ to the centre shows the tilt, and a small arc between
    the radial line and the blue arrow is labelled "ψ" in blue.
 8. The blue arrow ends exactly on the polygon edge at a small filled blue diamond (contact) with a short blue tick
    perpendicular to the edge (measured normal). Small blue label: "contact + normal".

PANEL B - "five cells, ordered by planner travel": a single horizontal row of FIVE small copies of the stand-off
circle, equal size, evenly spaced, each with a small grey polygon silhouette in its centre (no detail needed).
 1. Order from LEFT to RIGHT, with a title above each circle exactly as given:
    "S12, κ = 12" | "S8, κ = 8" | "A16-2, κ = 2" | "S4, κ = 4" | "S2, κ = 2".
 2. Probe marks change smoothly from left to right:
    - S12 (far left): fingertip dot at about 9 o'clock; a fan of four short BLUE probe arrows all starting at the same
      point and pointing inward at slightly different tilts; one very short ORANGE arc (a few degrees) next to the dot.
    - S8: the same fan, with a slightly longer short ORANGE arc.
    - A16-2 (middle): THREE BLUE probe arrows (not four) from two nearby start points joined by one medium ORANGE arc;
      this circle's outline is drawn in PURPLE #7A4FA3 instead of grey (second shape library).
    - S4: four BLUE probe arrows from three start points joined by medium ORANGE arcs.
    - S2 (far right): four BLUE probe arrows from four start points spread around the circle (about 9, 11, 1 and
      3 o'clock), consecutive start points joined by long ORANGE arcs drawn just outside the circle.
 3. Label under each circle, exactly: "6.373°" (S12), "9.404°" (S8), "21.22°" (A16-2), "23.18°" (S4), "47.06°" (S2).
 4. One small grey line of text centred under the whole row: "planner travel per test episode · schematic traces".

PANEL C - "one planner, one learned head, three comparators", block diagram:
 1. At the far left, vertically centred, a small cloud of about 20 tiny grey dots inside a rounded outline: the
    belief icon. Label below: "belief b".
 2. From it, three thin grey arrows fan out into three horizontal lanes stacked top to bottom; each lane is a row of
    rounded rectangles (white fill, #555555 outline) joined by thin grey arrows.
 3. Lane (i), top. Bold lane title at its left: "(i) Planner G*". Blocks: "EIG / c over feasible actions" (inside, a
    tiny row of 12 thin vertical BLUE bars of varying height, one taller and outlined darker) -> "argmax".
 4. Lane (ii), middle. Bold title: "(ii) Learned head". Blocks: a cluster of 4 small blue points with short tick
    marks, labelled "touch history (finger frame)" -> "DeepSets" -> "masked logits" (inside: a tiny row of 12 thin
    bars, a few greyed out to suggest masking).
 5. Two training arrows enter the "DeepSets" block:
    - a SOLID BLUE arrow coming down from lane (i)'s "EIG / c over feasible actions" block, blue label:
      "DAgger on G* scores (best held-out checkpoint)";
    - a DASHED ORANGE arrow entering from below, orange label: "PPO, reward = ball-sPCE (g_T)".
 6. Lane (iii), bottom. Bold title: "(iii) Heuristics". Three small rounded blocks side by side: "B-fan", "B-spread",
    "B-cov", and under them one small grey label: "H* chosen on pilot".
 7. No numbers, timings or ratios anywhere in panel C.

PANEL D - headline data inset: leave as an EMPTY placeholder, a plain white rectangle with a thin light-grey border
(#DDDDDD), the panel letter "D" in its top-left corner and NOTHING else inside (no axes, points, numbers or text). The
inset is plotted separately from the results JSON and pasted into this frame; the generator must not draw any chart,
value or label here.

Global: balanced composition, generous margins, all labels legible when printed 17 cm wide, no overlapping text, no
clutter, no title above the figure, no caption inside the image.

---
PANEL D INSET (plotted with matplotlib following the dataviz skill, NOT generated; values copied from
results/v5/results_v5.json; multiply proportions by 100 to plot in pp):
 x axis: G* mean test5 travel (rad), 14_test5_analysis.json > H5b > gstar_mean_travel_rad:
   S2 0.8213, S4 0.4046, S8 0.1641, S12 0.1112, A16-2 0.3704.
 y axis: student - G* success (pp).
 Filled points with 95 % CI whiskers (test5; 14_test5_analysis.json > <cell> > student_minus_gstar > success > {diff, ci95}):
   S2 -0.02467 [-0.07600, +0.02667]; S4 -0.02533 [-0.08333, +0.03267]; S8 -0.01267 [-0.06133, +0.03733];
   S12 -0.01533 [-0.06333, +0.03267]; A16-2 -0.002000 [-0.06267, +0.06067].
 Hollow points at the same x, NO whiskers (validation; 12_d5_analysis.json > <cell> > succ > delta_hat):
   S2 -0.0328; S4 -0.0548; S8 -0.0364; S12 -0.0324; A16-2 -0.0596.
 Horizontal dashed lines at 0 and at -delta = -0.04 (12_d5_analysis.json > <cell> > delta).
 Point labels S2 / S4 / S8 / S12 / A16-2; A16-2 in the second-library colour #7A4FA3, S cells in #222222.
 Corner text: "D5: 0/5 pass · H5b slope −0.0157/rad, ci95 [−0.104, 0.073], no trend detected".
 No fitted line (the WLS intercept is not in the JSON). [NEED: WLS intercept, only if a fitted line is wanted.]

DRAFT CAPTION
Figure 1. Amortizing a cost-aware touch planner across travel costs. (A) A finger on a stand-off circle chooses where
to move, paying a travel cost proportional to |Δφ|, and which way to probe; the belief is a particle set over identity
and planar pose. (B) The five pre-registered cells, ordered by the planner G*'s mean travel per test episode (6.373° at
κ = 12 to 47.06° at κ = 2 on shape set S; A16-2 is a second shape set at κ = 2); traces are schematic. (C) One
belief-free DeepSets head is trained by DAgger on G*'s scores or by PPO on G*'s information objective, and is compared
with hand-designed probing heuristics. (D) Student − G* success: test5 mean with paired 95 % CI (filled; 300 episodes,
5 student seeds) and validation point estimate (hollow; 500 episodes). The student is below G* in every cell on both
splits, and the pre-registered gate fails in all five cells, so a match within δ = 4 pp (dashed) is not supported; no
trend with travel is detected. Simulation; preliminary.
```

# Amortizing a Cost-Aware Information-Gain Touch Planner under Travel Cost: A Pre-Registered Five-Cell Characterisation

## Abstract

Active tactile localization chooses each touch from a particle belief over object identity and pose. A cost-aware
greedy information-gain planner (G\*), which scores every feasible touch by expected information per unit of travel
cost, is a strong but slow way to make that choice. We ask whether a policy distilled from G\* matches it, how it
compares with reinforcement learning (RL) on the same objective and with hand-designed probing heuristics, and how the
gap behaves as travel cost changes. A pre-registered five-cell study covers travel cost κ = 2/4/8/12 on one shape
library and a second library, A16, at κ = 2, with five seeds per learner, a fresh test split (test5), and the earlier
single-cell rounds as prior evidence. The pre-registered gate failed in all five cells (m = 0). The student is below
G\* in every cell on both splits (validation 3.2–6.0 pp, with two cells beyond the 4 pp margin; test5 0.2–2.5 pp, CIs
down to −8.3 pp), so matching G\* is not supported. The student beats the pilot-chosen heuristic in 4/5 cells after
Holm correction (+6.1 to +16.8 pp), but against the best heuristic on test5 the post-hoc margin falls to +3.5 to
+14.5 pp, with no CI. Distillation scores higher on RL's own contrastive objective only in A16-2, where RL collapses,
and no inversion between that objective and the posterior read-out is detected. No trend of the gap with planner
travel is detected, but a change of about 7 pp is not excluded. Per decision the student is 2,523–9,933× faster
(seed-701 timings). Simulation, planar shapes, preliminary.

## 1 Introduction

A robot that localizes an object by touch receives sparse and ambiguous measurements: one contact point and one
surface normal per probe, or a miss. A single contact rarely fixes the pose, and near-symmetric object families make
even the identity uncertain. The standard remedy is to maintain a belief over identity and pose, usually a particle
filter, and to choose the next touch by its expected information gain \cite{petrovskaya2011global, hebert2013next,
zheng2024bayesian, zheng2026bayesian}. Greedy information gathering of this kind is backed by (adaptive)
submodularity arguments for touch-based localization \cite{javdani2012efficient}. Probing is not free, however. The
finger must travel to the next approach direction, and travel time competes with probes inside a fixed time budget.
Cost-aware selection therefore scores each candidate by information per unit cost \cite{ottenhaus2018active}, and
reviews of active haptic perception identify this trade-off as central to practical exploration
\cite{seminara2019active}. The price is computation. A cost-aware planner that re-estimates expected information for
every feasible touch at every decision, by nested Monte Carlo over the particle belief, spends up to seconds of
computation per decision on a commodity CPU.

Amortization replaces that online optimisation with a policy network trained once. Policy-based Bayesian experimental
design learns such a policy from a contrastive information bound \cite{foster2021deep, ivanova2021implicit,
blau2022optimizing, hedman2025step, rainforth2024modern}; tactile RL learns exploration policies end to end for
recognition and localization \cite{riou2024reinforcement, niemann2024when}; and a third route imitates an
information-gathering expert \cite{choudhury2017adaptive, nguyen2024amortized}, typically through DAgger's no-regret
reduction \cite{ross2011reduction}. Distilling a validated cost-aware planner is attractive because the planner
supplies a dense per-action score at every visited belief, which removes long-horizon credit assignment and large-action
exploration from the learning problem. The open question is whether a policy distilled in this way keeps the
planner's quality, how it compares with RL trained on the same objective with the same network, and whether the
answer changes when the price of moving changes.

Earlier rounds of this study could not answer the regime question. Each tested one cell per regime: a stay-and-probe
cell at high travel cost, whose learnability gate failed on the first attempt and after its one remedy, and a
travelling cell at low travel cost, whose gate also failed. A review of those rounds asked for more cells per regime
(several κ values and at least one more shape library) and more learner seeds, and for a fresh test split, an RL
configuration tuned in the travelling regime, every heuristic in every cell, and a check of the evaluator's resolution.
The present round pre-registered all of these before any run, in a written amendment and its addenda, including a
learnability gate (D5) with no remedy step, a test-split hypothesis with Holm correction over cells, a cross-cell
trend hypothesis, and a rule for choosing the reference heuristic on pilot data. The paper therefore reports a
pre-registered measurement. It makes no method claim, and its headline is a negative result for the primary question.

**Findings.** The pre-registered gate failed in all five cells (m = 0). The student is below G\* in every cell on both
splits (validation 3.2–6.0 pp, with S4 and A16-2 beyond the 4 pp margin; test5 0.2–2.5 pp, CIs down to −8.3 pp), so
matching G\* is not supported. The student beats the pilot-chosen heuristic H\* in 4/5 cells after Holm (+6.1 to
+16.8 pp). In 4/5 cells, though, H\* is not the best heuristic on test5, and against the best test5 heuristic the
post-hoc margin falls to +3.5 to +14.5 pp, with no CI. On RL's own objective, the student is ahead only in A16-2,
where the reused RL configuration collapses, and no inversion between that objective and the posterior read-out is
detected in any cell. The cross-cell trend test detects no trend of the student − G\* success gap on G\* travel over
5 cells, but a change of up to about 7 pp across the observed travel range cannot be excluded. With seed-701 timings,
full G\* is 2,523–9,933× slower per decision than the student.

**Contributions.**
- **C1. Learnability across five cells.** The gate D5 fails in 5/5 cells; the student is below G\* in every cell on
  both splits and is not shown to lie within the pre-registered margin δ. Together with the two earlier rounds, the
  amortization hypothesis has failed its pre-registered gate in every cell tested.
- **C2. A cheap policy that beats pilot-chosen heuristics.** The student exceeds H\* in 4/5 cells under Holm, reported
  beside the post-hoc margins over the best test5 heuristic and the per-decision latency range.
- **C3. Distillation versus RL on the same objective.** The pre-registered advantage on RL's objective holds only in
  A16-2, where RL collapses; the inversion check is false everywhere; the student − RL success contrasts are
  uncorrected.
- **C4. Travel cost and behaviour.** No trend of the gap is detected and about 7 pp is not excluded; the student
  travels less than G\* in every cell.
- **C5. Methods notes.** The evaluator's finite resolution, an upward selection bias in G\*'s value estimates, the
  differing orderings of the contrastive bound and the posterior read-out, and the practice of reporting the
  validation and test splits separately. These describe the measurement, not the answer, and are placed in Sections 4
  and 8 rather than in Section 5.

Section 2 reviews related work. Section 3 defines the task, the planner, the shared head, the two learners, the
heuristics and the five cells. Section 4 gives the pre-registered protocol and the decision record, Section 5 the
results, and Sections 6–8 discuss, bound and conclude.

## 2 Related Work

**Tactile localization and next-best touch.** Estimating object pose from touch is usually posed as Bayesian
filtering. Scaling-series Monte Carlo achieves global localization from sparse contacts on polygonal meshes
\cite{petrovskaya2011global}; manifold particle filters sample on the contact manifold to avoid degeneracy in planar
contact manipulation \cite{koval2015pose}; and Tac2Pose returns a pose distribution from a single high-resolution touch
\cite{bauza2023tac2pose}. On top of such estimators, information-driven selection picks the next touch. The next best
touch maximises information gain on pose uncertainty \cite{hebert2013next}; Bayesian frameworks jointly track class
and pose with customised particle filters and choose exploratory actions by expected information
\cite{zheng2024bayesian, zheng2026bayesian}; recent work selects contacts by expected information gain for rigid-body
pose and shape \cite{gordon2026active}, or learns one exploration policy on hardware that balances global search
against local refinement \cite{kamtikar2026tactful}. Cost-aware information gain combines expected gain and expected
cost in one score \cite{ottenhaus2018active}, and a review of active haptic perception summarises the space, including
the coverage-style heuristics that remain the usual reference points \cite{seminara2019active}. Several of these
systems run on hardware with 3D geometry and real contact; our study is planar and simulated, and we use it to isolate
the selection question rather than to compete with them. In this line cost-aware greedy selection is common, but it
runs online at every decision. How well it can be amortized, and how that changes with travel cost, is rarely
measured.

**Greedy information gathering and its guarantees.** Submodularity explains why greedy selection works well for touch:
Shannon entropy reduction is submodular under certain assumptions, and adaptive submodularity gives online guarantees
for touch-based localization \cite{javdani2012efficient}. Hierarchical action structure can be folded into the same
framework through sequential submodular optimisation \cite{vien2015touch}. Outside touch, submodular surrogates
approximate the value of information when the objective itself is not submodular \cite{chen2015submodular}, and
semi-adaptive policies show how much adaptivity is needed to retain guarantees \cite{esfandiari2019adaptivity}. Travel
cost couples decisions, because where the finger ends up after one probe sets the price of the next, which is exactly
the kind of structure that weakens these guarantees. All of these results concern the greedy planner itself, not a
learned copy of it. We therefore treat G\* as the reference that a learned policy is measured against, not as an
optimum, and we make no claim about how far G\* is from the optimal policy.

**Amortized Bayesian experimental design.** Deep adaptive design trains a design network on contrastive information
bounds so that each decision is one forward pass \cite{foster2021deep}. Implicit-likelihood and RL formulations remove
the need for likelihoods or a differentiable simulator \cite{ivanova2021implicit, blau2022optimizing}, and RL has been
applied to sequential and robust experimental design more broadly \cite{asano2022sequential, shen2023reinforcement}.
Semi-amortized variants refine the policy online \cite{hedman2025step}, nested particle filters amortize design in
dynamical systems \cite{iqbal2024recursive}, and transformer policies amortize inference and acquisition jointly
\cite{huang2026aline}. A recent review covers the field \cite{rainforth2024modern}. In this literature a contrastive
bound of the sPCE type is usually both the training objective and the reported quality of a learned policy
\cite{foster2021deep, blau2022optimizing}. Whether that bound ranks policies the same way as a posterior-based
localization read-out is rarely checked, and the bound is seldom compared with a planner-supervised alternative
trained on the same network.

**Learned tactile exploration and imitation of information gathering.** In touch, RL agents explore for recognition
with rewards on correct classification \cite{riou2021seeing, fleer2020efficient}, on classification, exploration and
pose \cite{riou2024reinforcement}, or learn when to stop \cite{niemann2024when}. TANDEM3D co-trains exploration and
decision making on 3D contacts \cite{xu2023tandem3d}, and Tactile MNIST offers a benchmark that includes localization
\cite{schneider2025tactile}. A second route imitates an information-gathering expert: imitation of a clairvoyant oracle
\cite{choudhury2017adaptive} and deep imitation of a nonmyopic active-search expert \cite{nguyen2024amortized}, both
building on DAgger \cite{ross2011reduction}. The two routes have been compared in spirit, but we know of no
pre-registered, multi-cell comparison of planner distillation and RL that uses the same head and action set, evaluates
both on the objective RL itself optimises, and reports the posterior-success read-out beside the contrastive bound.
This paper supplies that comparison across five cells, and it supplies it as a measurement rather than as a new
method.

## 3 Method

### 3.1 Task, belief, cost and metrics

**State, actions and observations.** The object is a planar polygon with identity $k \in \{1,\dots,K\}$ and unknown
pose, so the state is $s = (k, x, y, \theta)$, with a uniform prior over identity, position in a bounded box and
orientation. The finger rests on a stand-off circle at angle $\phi_t$, with a start angle shared by all methods on an
episode. An action $a = (\phi', \psi)$ selects a target angle $\phi'$ and an approach offset $\psi$ from a discrete
grid [NEED: action-grid size and stand-off geometry, copied from the frozen design doc into a citable source]. The
finger travels the shorter way to $\phi'$, probes inward along direction $\phi' + \pi + \psi$, and then
$\phi_{t+1} = \phi'$. A probe returns a contact point and a surface normal, both with Gaussian noise, or a miss
$y = \varnothing$. Every method uses the same softened likelihood $p_\varepsilon(y \mid s, a)$, so differences between
methods come from which actions they choose, not from different sensor models. The belief is a particle filter
$b = \{s_n, w_n\}_{n=1}^{N}$ over identity and pose \cite{petrovskaya2011global, koval2015pose}.

**Travel cost and budget.** In units of one probe stroke,

$$c(a) = 1 + \kappa\,\frac{|\Delta\phi|}{\pi}, \qquad \Delta\phi = \mathrm{wrap}(\phi' - \phi_t) \in (-\pi, \pi],$$

[NEED: cite the frozen design-doc line for the cost formula], so κ is the time to travel half the circle. With
remaining time $\tau_{\mathrm{rem}}$, the feasible set is $\mathcal{F}(\tau_{\mathrm{rem}}) = \{a : c(a) \le
\tau_{\mathrm{rem}}\}$; every method chooses only within it, and the episode ends when no action is feasible. The
budget τ of each cell is set by a calibration rule so that G\* executes about $n^\*$ probes: τ is derived from G\*'s
mean unbudgeted travel time over 200 calibration episodes (Table 0).

**Metrics.** From the evaluator's posterior after the last probe, the identity estimate is the maximum-mass identity
and the pose estimate is refined locally. *Success* requires the correct identity and position and orientation errors
inside fixed tolerances, orientation taken modulo the shape's symmetry group; it is read from an adaptive grid
posterior at subdivision 8 (sub 8). With $B(s_0)$ the success ball around the true state, the *ball information* is
$\mathrm{BI}(h) = \log \hat P(B(s_0) \mid h) - \log P(B(s_0))$ in nats. The RL objective $g_T$ (ball-sPCE, Section 3.3)
is computed without the grid. *Travel* is the total angular distance the finger covers in an episode, including the
first leg from the continuous start angle onto the action grid, which no policy chooses; it is logged in radians and
degrees. We also log the number of probes.

**Cells.** Shape library S has $K = 8$ identities, four near-symmetric base shapes and one symmetry-breaking variant of
each. Library A16 is the second library [NEED: A16 identity count in a citable results/doc field; it is stated in
`docs/07c_amendment_v5_0.md` P0, not in JSON]. The five pre-registered cells are listed in Table 0. For A16 the
probe count $n^\* = 3$ came from the pre-registered rule, and a keep check at κ = 0 and τ = $n^\*$ on 200 calibration
episodes gave G\* success 0.8, inside the pre-registered keep range [NEED: the keep range, stated in amendment v5.0
P0, in a citable field].

**Table 0. The five cells.** τ is set by the calibration rule from G\*'s mean unbudgeted travel time (stroke units) over
200 calibration episodes; the S2 and S12 values come from the earlier rounds.

| Cell | Library | κ | $n^\*$ | G\* mean travel time | τ |
|---|---|---|---|---|---|
| S2 | S | 2 | 4 | 0.7257 | 4.7 |
| S4 | S | 4 | 4 | 0.7967 | 4.8 |
| S8 | S | 8 | 4 | 0.8335 | 4.8 |
| S12 | S | 12 | 4 | 0.9388 | 4.9 |
| A16-2 | A16 | 2 | 3 | 0.3514 | 3.4 |

### 3.2 Planner G\*

G\* selects

$$G^\*(b) = \arg\max_{a \in \mathcal{F}(\tau_{\mathrm{rem}})} \frac{\mathrm{EIG}_B(a; b)}{c(a)},$$

where the ball EIG, the expected one-step increment of $\log P(B(s_0)\mid h)$, is estimated by nested Monte Carlo with
$j_m \sim w$ and $y_m \sim p_\varepsilon(\cdot \mid s_{j_m}, a)$:

$$\mathrm{EIG}_B(a;b) = \frac{1}{M}\sum_{m=1}^{M}\Big[\log\!\!\sum_{n \in B(s_{j_m})}\!\! w_n\, p_\varepsilon(y_m \mid s_n,a)
- \log\!\!\sum_{n \in B(s_{j_m})}\!\! w_n - \log \sum_n w_n\, p_\varepsilon(y_m \mid s_n, a)\Big].$$

The deployed configuration is `g2000_512_64` [NEED: meaning of the three numbers in `g2000_512_64` (particles /
candidates / inner samples), from the frozen design doc]. At each decision G\* exports the score vector
$s(a) = \max(0, \mathrm{EIG}_B(a;b))/c(a)$ over feasible actions (zero elsewhere), whose argmax is G\*'s action; this
vector is the distillation label. Two reduced configurations, `g125_512_16` and `g500_512_4`, are timed in the latency
study (Section 4) and nowhere else. **Complexity.** Per decision, G\* evaluates $O(MNC)$ likelihoods for $C$ scored
candidates and builds ball-neighbour lists in $O(N^2)$, on top of assimilating the last observation; the latter two
terms do not depend on $C$. G\* is a greedy reference: we measure a learned policy against it and make no claim that
it is optimal \cite{javdani2012efficient, ottenhaus2018active}.

### 3.3 One shared head, two learners

**Head.** Both learners use the same belief-free DeepSets head [CITE-MISSING: DeepSets (Zaheer et al. 2017)]. Each
touch in the history is encoded in the finger frame (contact indicator, contact point, normal and the action that
produced it), summed, and concatenated with a context of the relative angle, the remaining-budget fraction
$\tau_{\mathrm{rem}}/\tau$ and the absolute finger angle $\phi_t$. The head outputs one logit per action, masked to
$-\infty$ outside $\mathcal{F}(\tau_{\mathrm{rem}})$. Architecture, input and action set are held fixed, so the
training signal is the isolated variable. Re-encoding the history costs $O(T^2H^2 + THA)$ for $T$ touches, hidden width
$H$ and $A$ actions, with no particle filter in the loop.

**Distillation.** The student $\pi_\theta$ minimises a soft cross-entropy to tempered teacher scores plus a hard term on
the teacher's argmax,

$$\mathcal{L}(\theta) = -\sum_{a \in \mathcal{F}} q(a)\log \pi_\theta(a \mid h) - \lambda \log \pi_\theta(a^\* \mid h),
\qquad q = \mathrm{softmax}\big(\beta_T\, s(a)/\sigma_s\big)_{a \in \mathcal{F}},$$

with $\sigma_s$ the per-decision standard deviation of $s$ over feasible actions and $a^\* = \arg\max_a s(a)$. Held-out
quality is the floored normalised label regret

$$r = \frac{s_{\max} - s(a_\pi)}{\max(s_{\max} - s_{\mathrm{med}},\ \rho\, s_{\max})},$$

averaged over held-out decisions to $\bar R$. No success-based selection is used. Training follows Algorithm 1 with
seeds 701–705 and the same hyper-parameters (hp 0) in every cell \cite{ross2011reduction, choudhury2017adaptive}.

> **Algorithm 1 (DAgger distillation of G\*, v5 recipe).**
> 1. Round r0: roll out G\* on label episodes, storing $(h, \phi_t, \tau_{\mathrm{rem}}, \mathcal{F}, s, a^\*)$ at every
>    decision; hold out a fixed block of decisions for $\bar R$.
> 2. Train $\pi_\theta$ on $\mathcal{L}$ for a fixed number of epochs; after each epoch evaluate held-out $\bar R$;
>    **keep the checkpoint with the lowest held-out $\bar R$**.
> 3. For rounds r1 and r2 with a decaying mixing coefficient $\beta_{\mathrm{DAgger}}$: roll out episodes executing
>    G\*'s action with probability $\beta_{\mathrm{DAgger}}$ and $\pi_\theta$'s otherwise; run G\*'s filter alongside,
>    label every visited belief with $s$, aggregate, and repeat step 2.
> 4. Freeze the round-r2 kept checkpoint; record its weight hash before any test episode.
>
> [NEED: label episodes per cell, number of DAgger rounds and β schedule, episodes per round and epochs per round,
> and the hp-0 values of $\beta_T$, λ, ρ, optimiser and batch, from `docs/07c_amendment_v5_0.md` E2, in a citable
> field.]

Keeping the best held-out checkpoint is the pre-declared answer to an over-fitting finding of the previous round,
where held-out regret rose after an early minimum under a last-checkpoint recipe.

**RL.** The RL policy uses the same head and action set and is trained with PPO \cite{schulman2017proximal} and a
critic baseline. Its reward is the increment of ball-sPCE, a contrastive estimate of ball information in the style of
\cite{foster2021deep, blau2022optimizing}: with $L$ contrastive states $s_{1:L} \sim p$ and $J$ states $s_0^{(j)}$ drawn
uniformly in $B(s_0)$,

$$g_t = \log \hat p_B(h_t \mid s_0) - \log\Big[\tfrac{1}{L+1}\Big(\hat p_B(h_t \mid s_0) + \sum_{l=1}^{L} p(h_t \mid
s_l)\Big)\Big], \qquad \hat p_B(h \mid s_0) = \tfrac{1}{J}\sum_j p(h \mid s_0^{(j)}),$$

and $r_t = g_t - g_{t-1}$, so the return telescopes to $g_T$, RL's own objective. The configuration was swept on S2
only: 8 configurations, each trained for 100,096 episodes (100,032 at batch 64) and selected by the earlier rounds'
rule, highest final ball-sPCE on the trainer's validation stream (92,160 episodes), ties within 0.02 nats to the lower
index. The rule selected cfg 6 (learning rate 1.257e-3, entropy coefficient 9.504e-4, batch 256, critic learning rate
4.925e-4), with final validation ball-sPCE 6.300 against 6.241 for cfg 0, the configuration of the earlier rounds. On
the sampled-policy version of the same metric, cfg 1 scores higher (6.316 against 6.205 for cfg 6). cfg 6 is reused in
every cell with seeds 711–715 [NEED: RL training episodes per seed for the cfg-6 test arm; not in `results_v5.json`]. A
control arm, `rl_success`, replaces the reward by a terminal-success reward and is run in S2 and S12 only; its
per-seed training lengths are printed beside its results (Section 5.3). The reward contains no explicit term for probe
count or travel; both enter only through the budget.

### 3.4 Heuristics

Random selects uniformly among feasible actions. Three heuristics reserve budget for the remaining probes.
**B-spread** (belief-free) maximises angular distance to the previous probe angles. **B-fan** (belief-free,
travel-nearest) stays at $\phi_t$ when allowed and cycles the approach offset, otherwise moving to the nearest allowed
angle. **B-cov** (belief-using) maximises coverage under an online filter. In each cell the reference heuristic H\* is
the best of the three on pilot episodes 0–199 (sub 8), with ties broken B-spread < B-fan < B-cov. The pilot chose
B-cov in S2 and S8 and B-fan in S4, S12 and A16-2 (Table 1). All three heuristics and Random are run on test5 in every
cell.

### 3.5 Decision rules

Five pre-registered decisions are read: the validation gate D5, the test5 hypothesis H5a (student − G\* success, Holm
over the five cells), the student − H\* contrast (Holm over the five cells), H2-v5 (student − RL on $g_T$) with its
inversion check, and the cross-cell trend H5b. Section 4 states each rule and Table 1 records each outcome.

## 4 Experiments

**Pre-registration.** Amendment v5.0, written before any run of this round, fixes the five cells, the seeds, the fresh
test split test5, the gate D5, the hypotheses H5a, H5b and H2-v5, the H\* selection rule and the Holm families. Amendment
v5.1 fills in values that the frozen rules produce: the budgets τ, the A16 probe count $n^\*$ and the RL configuration
cfg 6. Its addenda fix the E7 design and require the `rl_success` training lengths to be printed beside every
`rl_success` result. Addendum v5.1e cuts test5 from 500 to 300 episodes per method and cell, under the frozen reduction
order and before any test5 episode was run. Every decision in this paper is read off a rule fixed in these documents;
values that no rule produced are labelled report-only, exploratory or post hoc.

**Splits.** All splits are disjoint episode streams, and within a split every method runs on the same episodes with the
same initial state, start angle and observation stream (a paired design). D5 uses validation episodes val3 0–499 (500
per cell). H5a, the heuristic and RL contrasts, H2-v5 and H5b use test5 0–299, with 300 episodes per method per cell;
every test5 block, including the $g_T$ blocks, is complete. H\* is chosen on pilot3 0–199 (200 episodes per heuristic)
and τ on calibration episodes cal3 0–199. The G\* validation rows of D5 do not all come from this round: S2 uses the
previous round's files, S12 those of the round before, and S4, S8 and A16-2 new runs. Before any test5 job, the weight
hashes of every learner were recorded, 15 per cell in S2 and S12 (students, RL and `rl_success`) and 10 per cell in S4,
S8 and A16-2; that the recording preceded test5 is taken from the run context.

**Gate D5.** On the 500 paired val3 episodes with five student seeds, D5 passes iff three clauses hold. (i) The success
deficit clears an SE-dependent threshold, $\hat\Delta_{\mathrm{succ}} \ge -\delta + 1.163\,\mathrm{SE}$ with δ = 0.04
(for example −0.01454 in S2) [NEED: the lower floor of clause 1 in a citable field; it is stated in amendment v5.0, not
in JSON]. (ii) The BI deficit satisfies $\hat\Delta_{\mathrm{BI}} \ge -0.15$ nats. (iii) Enough seeds pass the
per-seed clause on $\hat\Delta_{\mathrm{succ}}$ against −δ [NEED: the per-seed clause count in a citable field]. The
SE is the standard deviation of an episode × student-seed bootstrap; because the threshold adds a multiple of SE to −δ,
it becomes stricter as the paired SE grows. No remedy round follows a failure. The number m of cells that pass D5 is
the registered H5a validation count.

**Statistics.** Test5 contrasts use a crossed episode × seed bootstrap for the two-sided ci95 and p-value, with
`n_seeds` = [5, 1] against G\* and H\* (G\* and the heuristics are run once per cell) and [5, 5] against RL [NEED:
bootstrap resample count; not in JSON]. Bootstrap p-values resolve to 0.0002, so a reported p of zero is printed as
p < 0.0002. Holm's step-down procedure over the five cells is applied to two families only, student − G\* success (H5a)
and student − H\* success [CITE-MISSING: Holm (1979) step-down procedure]. H2-v5 is met iff the one-sided 95 % lower
bound of $g_T(\text{student}) - g_T(\text{RL})$ exceeds +0.10 nats. The registered inversion check asks, per cell,
whether $g_T$ and the posterior read-out order the student and RL in opposite directions with a resolved $g_T$
contrast; it is run for cfg-6 RL in every cell and for `rl_success` in S2 and S12. H5b is a weighted least-squares
slope of the five test5 success deficits on G\*'s mean test5 travel, with weights fixed in advance, read through the
ci95 of the slope. All BI, RL, `rl_success` and $g_T$ contrasts are uncorrected and
exploratory [CITE-MISSING: bootstrap confidence intervals (Efron)].

**Methods note: evaluator resolution (E5).** Success is a thresholded read-out of a finite-resolution grid posterior.
E5 re-reads 200 single-seed episodes of G\* and student seed 701 in S2 and S12 at sub 16 instead of sub 8. The success
outcome flips on 8 % (G\*) and 7 % (student) of S2 episodes and on 7.5 % and 6.5 % of S12 episodes. G\* success moves
from 0.54 to 0.54 in S2 (8 gains, 8 losses) and from 0.48 to 0.505 in S12 (10 gains, 5 losses); the student moves from
0.465 to 0.485 (9, 5) and from 0.455 to 0.45 (6, 7). The mean |ΔBI| is at most 0.004034 nats. Re-reading at sub 16
therefore flips 6.5–8 % of single-seed outcomes and shifts the seed-701 student − G\* contrast by +0.02 (S2) and −0.03
(S12) on 200 episodes, about 0.8× the test5 gap in S2 and about 2× in S12; its effect on the 5-seed test5 contrast was
not measured. Every test5 success contrast in Section 5 should be read next to this caveat.

**Methods note: planner value estimates (E7).** E7 (design: G\*-reached beliefs 0–31, independent re-estimate with 256
outcome samples) repeats a one-step screen of first actions on 32 beliefs per cell with a 32-candidate and a
512-candidate setting (mean candidates 29.0 and 302.0 in S2, 30.5 and 85.75 in S12) and re-scores the selected action
with independent samples. In S2 and S12, the 512-candidate setting gives a larger independent-estimate gap than the
32-candidate setting (+0.04838 nats per belief, ci95 [0.01681, 0.08697], in S2; +0.01830, ci95 [0.004013, 0.03652], in
S12; n = 32). The selection bias of the screen, selected minus independent estimate, is positive with a CI excluding 0
in S2 (0.01926, ci95 [0.001030, 0.04193], at 32 candidates; 0.02179, ci95 [0.004270, 0.04013], at 512) and is not
detected in S12 (0.004470, ci95 [−0.007718, 0.01884]; −0.002040, ci95 [−0.01574, 0.01258]). The estimates are in nats
on G\*-reached beliefs; whether the deployed G\* has headroom in success terms was not measured.

**Latency protocol (E6).** Job 1 times student seed 701, full G\* and the two reduced configurations interleaved on the
same G\*-reached decision states, n = 1000 decisions in each S cell and 500 in A16-2 (its job-1 completeness flag is
true in A16-2 and false in the four S cells). Job 2 times students 702–705 separately, n = 500 decisions each. A
per-cell ratio is reported with its bootstrap ci95 and the pre-registered half-width check.

**Implementation.** Everything is numpy with hand-written backpropagation and single-threaded BLAS, run on
GitHub-hosted 2-core runners (CPU model not logged); runners differ across cells. Table S lists the settings that the
results record holds; the remaining design constants are marked.

**Table S. Settings.**

| Component | Setting |
|---|---|
| Cells | Table 0 (κ, $n^\*$, τ) |
| G\* | `g2000_512_64`; reduced `g125_512_16`, `g500_512_4` (timed only) [NEED: meaning of the three numbers] |
| Student | DeepSets head; DAgger rounds r0–r2; best held-out $\bar R$ checkpoint per round; hp 0 in every cell; seeds 701–705 [NEED: label, DAgger and epoch budgets, hp-0 values] |
| RL | PPO, critic baseline; cfg 6 selected on S2 (Section 3.3) and reused in every cell; seeds 711–715 [NEED: episodes per seed] |
| `rl_success` | terminal-success reward, cfg 6, S2 and S12 only, seeds 711–715; training lengths in Section 5.3 |
| Heuristics | Random, B-spread, B-fan, B-cov; H\* on pilot3 0–199, 200 episodes each |
| Splits | cal3 0–199; pilot3 0–199; val3 0–499 (D5); test5 0–299, 300 episodes per method per cell |
| Evaluator | adaptive grid posterior, sub 8; E5 re-read at sub 16 |
| Statistics | crossed episode × seed bootstrap [NEED: resample count]; δ = 0.04; BI floor −0.15 nats; H2-v5 margin +0.10 nats; Holm over 5 cells (two families) |
| Latency | job 1 n = 1000 (S cells) / 500 (A16-2); job 2 n = 500 per seed |

**Table 1. Decision record.** D5 on val3 0–499 (proportions; Δ̂ = student − G\*); H\* from pilot3; H5a, student − H\*
and H2-v5 on test5 0–299. All rows DEC except the H\* column (GATE). G\* validation source: S2 previous round, S12 the
round before, others this round.

| Cell | D5 student / G\* | D5 Δ̂_succ (threshold) | D5 Δ̂_BI | D5 seeds ok | D5 | H\* (pilot success) | H5a Holm | Student − H\* Holm | H2-v5 LB (> +0.10?) | Inversion |
|---|---|---|---|---|---|---|---|---|---|---|
| S2 | 0.4812 / 0.514 | −0.0328 (−0.01454) | −0.0682 | 3/5 | fail | B-cov (0.445) | no | no | −0.4971 (no) | no |
| S4 | 0.4492 / 0.504 | −0.0548 (−0.01503) | −0.1334 | 1/5 | fail | B-fan (0.43) | no | yes | −0.6555 (no) | no |
| S8 | 0.4116 / 0.448 | −0.0364 (−0.01639) | −0.0465 | 4/5 | fail | B-cov (0.405) | no | yes | −0.4861 (no) | no |
| S12 | 0.4136 / 0.446 | −0.0324 (−0.01722) | −0.06348 | 3/5 | fail | B-fan (0.41) | no | yes | −0.3044 (no) | no |
| A16-2 | 0.4124 / 0.472 | −0.0596 (−0.01229) | −0.06293 | 0/5 | fail | B-fan (0.33) | no | yes | +0.5964 (yes) | no |

Summary rows: H5a validation m = 0 of 5 (DEC). H5a test5: 0/5 Holm rejections (DEC). Student − H\*: 4/5 Holm
rejections (DEC). Inversion: false in 5/5 cells and in both `rl_success` checks, S2 and S12 (DEC). H5b: "no trend detected over 5 cells" (DEC; slope in Section
5.4). Prior S12 gate (two rounds back):
Δ̂_succ −0.05867 (threshold −0.01435) on the first attempt and −0.044 (threshold −0.01681) after the remedy, both fail
(PRIOR DEC). Prior S2 gate (previous round): −0.028 (threshold −0.01464), fail (PRIOR DEC). A16 $n^\*$ = 3 (rule
reading 0.975; keep check 0.8, kept) (GATE). Weight hashes recorded, 15 or 10 per cell (GATE). Test5 complete, 300
episodes per method, $g_T$ complete (GATE).

## 5 Results

### 5.1 C1. Does the student match G\*?

**D5 on validation.** The pre-registered gate failed in all five cells (m = 0; Table 1). In every cell the success
deficit is below its threshold, while the BI clause passes in 5/5. All 25 per-seed success differences are negative,
from −0.068 to −0.01, and no A16-2 seed passes the per-seed clause. Validation point gaps are 3.2–6.0 pp, with S4 and
A16-2 beyond the 4 pp margin. The G\* validation rows come from three rounds (S2 from the previous round, S12 from the
round before, the other cells from this one), so the five validation gaps are not drawn from one G\* run.

**H5a on test5.** On the fresh split the student is again below G\* in every cell (Table 2b): test5 point gaps are
0.2–2.5 pp, with 95 % CIs from −8.3 to +6.1 pp, and no pooled estimate was computed. Holm rejects in 0/5 cells, and
equivalence is not shown: the CIs are 9.6–12.3 pp wide. A shortfall of up to 6.1 pp (the tightest lower bound, S8) is
consistent with the data in every cell, and up to 8.3 pp in S4. Test5 point gaps are smaller than the validation gaps
in every cell, but applying the D5 rule to test5 would still fail in about 4 of 5 cells, so test5 does not contradict
the D5 verdict. Each of these success contrasts sits within the evaluator-resolution caveat of E5 (Section 4).

**BI on test5 (uncorrected).** The student − G\* BI ci95 excludes 0 in S4 and S12 only (Table 2b). In A16-2 the BI
point estimate is positive, with a CI that includes 0.

**Prior cells, the previous test gap, and the teacher's variance.** The two earlier rounds failed their gates in S12
(twice) and S2 (Table 1). The previous round's test3 gap (−10.2 pp, ci95 [−16.6, −4.3]; different test split and
training recipe) lies outside the v5 S2 test5 ci95 [−7.6, +2.7] pp; the two were not formally compared. With this
round, the amortization hypothesis has now failed its pre-registered gate in every cell tested across three rounds.
G\* was run once per cell (`n_seeds` = [5, 1]), so any run-to-run variability of G\* (E7 shows noisy, upward-biased
value estimates in S2) is missing from the student − G\* CIs, and those CIs may be too narrow.

**Checkpoint sensitivity (report-only).** By construction the kept checkpoint is never worse than the last epoch on
held-out $\bar R$; the training record shows the size of that difference. In every seed × round run of every cell, the
last epoch's held-out $\bar R$ exceeds the kept one, by 0.0002753 to 0.03172. Kept $\bar R$ lies in 0.2773–0.2857 in
S2 (1161 held-out decisions), 0.2230–0.2378 in S4 (1180), 0.1764–0.1859 in S8 (1179), 0.1647–0.1778 in S12 (1196) and
0.1123–0.1178 in A16-2 (880), and the kept epochs range from 0 to 187. Whether the last checkpoint would change success
was not tested.

**Table 2a. Test5 success, 300 episodes per method and cell (sub 8).** † marks the pilot-chosen H\*. Student and RL
5-seed means are recovered from the registered contrasts (post hoc, no CI).

| Method | S2 | S4 | S8 | S12 | A16-2 |
|---|---|---|---|---|---|
| G\* | 0.5333 | 0.4967 | 0.4567 | 0.4567 | 0.49 |
| Student, 5-seed mean (PH) | 0.5087 | 0.4713 | 0.444 | 0.4413 | 0.488 |
| Student, seed range | 0.4967–0.53 | 0.4333–0.5033 | 0.42–0.4567 | 0.42–0.46 | 0.4567–0.5133 |
| RL cfg 6, 5-seed mean (PH) | 0.424 | 0.4167 | 0.412 | 0.3687 | 0.222 |
| RL cfg 6, seed range | 0.39–0.48 | 0.3833–0.4567 | 0.3833–0.43 | 0.3367–0.3867 | 0.1833–0.29 |
| B-fan | 0.35 | 0.3733† | 0.3833 | 0.38† | 0.32† |
| B-cov | 0.45† | 0.42 | 0.3733† | 0.4067 | 0.3433 |
| B-spread | 0.04667 | 0.09 | 0.05 | 0.07 | 0.01 |
| Random | 0.1033 | 0.08333 | 0.09667 | 0.07667 | 0.03333 |

**Table 2b. Test5 paired contrasts: difference, [ci95], two-sided p.** Holm over 5 cells applies to the two success
rows marked DEC; every other row is uncorrected (EXPL) or post hoc (PH).

| Contrast | S2 | S4 | S8 | S12 | A16-2 |
|---|---|---|---|---|---|
| Student − G\* success (DEC) | −0.02467 [−0.07600, +0.02667], p 0.3526 | −0.02533 [−0.08333, +0.03267], p 0.3888 | −0.01267 [−0.06133, +0.03733], p 0.63 | −0.01533 [−0.06333, +0.03267], p 0.5378 | −0.002000 [−0.06267, +0.06067], p 0.9572 |
| Holm reject | no | no | no | no | no |
| Student − G\* BI (EXPL) | −0.07862 [−0.1615, +0.004763], p 0.061 | −0.1314 [−0.2112, −0.05320], p 0.002 | −0.06764 [−0.1392, +0.003764], p 0.0624 | −0.09100 [−0.1681, −0.01867], p 0.0124 | +0.08477 [−0.05888, +0.2320], p 0.2642 |
| Student − H\* success (DEC) | +0.05867 [−0.001333, +0.1180], p 0.0558 | +0.09800 [+0.04667, +0.1487], p < 0.0002 | +0.07067 [+0.01667, +0.1247], p 0.0098 | +0.06133 [+0.01067, +0.1120], p 0.0178 | +0.1680 [+0.1060, +0.2300], p < 0.0002 |
| Holm reject | no | yes | yes | yes | yes |
| Student − H\* BI (EXPL) | +0.1441 [+0.03379, +0.2520], p 0.011 | +0.4180 [+0.3301, +0.5094], p < 0.0002 | +0.1948 [+0.09552, +0.2963], p < 0.0002 | +0.2361 [+0.1568, +0.3168], p < 0.0002 | +0.7842 [+0.6135, +0.9579], p < 0.0002 |
| Best test5 heuristic, student − it (PH, no CI) | B-cov (= H\*), +0.05867 | B-cov, +0.05133 | B-fan, +0.06067 | B-cov, +0.03467 | B-cov, +0.1447 |
| Student − RL success (EXPL) | +0.08467 [+0.03067, +0.1373], p 0.0032 | +0.05467 [−0.002000, +0.1100], p 0.0584 | +0.03200 [−0.01467, +0.07933], p 0.19 | +0.07267 [+0.02467, +0.1207], p 0.0032 | +0.2660 [+0.1993, +0.3300], p < 0.0002 |
| Student − RL BI (EXPL) | +0.2297 [+0.1469, +0.3139], p < 0.0002 | +0.1577 [+0.04248, +0.2783], p 0.0046 | +0.08290 [−0.007993, +0.1794], p 0.079 | +0.2475 [+0.1124, +0.3878], p 0.0002 | +1.025 [+0.8492, +1.190], p < 0.0002 |

### 5.2 C2. Against heuristics, and at what cost

**Student − H\* (Holm).** The student beats the pilot-chosen H\* in 4/5 cells after Holm (+6.1 to +16.8 pp; Table 2b).
S2 is the exception: its CI includes 0 at the lower end. In 4/5 cells, though, H\* is not the
best heuristic on test5, and against the best test5 heuristic the post-hoc margin falls to +3.5 to +14.5 pp, with no
CI. The pilot used 200 episodes per heuristic and its choice was frozen before test5, so the gap between the
registered and the post-hoc margin measures how much the pilot choice mattered, not a property of the student. On BI
the student − H\* ci95 excludes 0 in all five cells (uncorrected). B-spread and Random are far below the other methods
in every cell (Table 2a).

**Latency (E6, report-only).** With seed-701 timings, full G\* is 2,523–9,933× slower per decision (median paired
ratio, CI rule met only in A16-2; Table 4). Other seeds' student medians (0.36–0.51 ms) differ by up to about 24 %
within a cell, so each per-cell ratio is uncertain at about that level; the job-2 ratios are a post-hoc sensitivity
column (ratio of medians, not paired). Only S2 (9,933×) and A16-2 (8,301×) lie in the 7,000–10,000× band, so no single
band describes all cells. The seed-701 student median varies between 0.326 and 0.500 ms, whereas full G\* varies
between 0.910 and 4.880 s, so most of the cross-cell spread of the ratio comes from G\*'s time. The two reduced G\* configurations are listed as timings only; their
accuracy was not measured on test5, so the table supports no latency–accuracy frontier and no matched-accuracy claim.
All timings were taken on 2-core runners that differ across cells.

**Table 4. Per-decision latency (E6).** Medians; ratio = full G\* / student seed 701, median paired ratio with
bootstrap ci95; "CI rule" is the pre-registered half-width check. Job-2 range: full G\* median over the medians of
students 702–705 (post hoc, no CI).

| Cell | Student 701 (ms) | Full G\* (s) | Ratio [ci95] | CI rule | Job-2 ratio range (PH) | `g125_512_16` (ms) | `g500_512_4` (ms) |
|---|---|---|---|---|---|---|---|
| S2 | 0.4996 | 4.880 | 9,933 [8,179, 10,224] | not met | 9,521–9,569 | 115.6 | 194.3 |
| S4 | 0.4942 | 3.375 | 6,990 [4,747, 7,270] | not met | 8,060–8,123 | 80.38 | 140.9 |
| S8 | 0.3577 | 1.234 | 3,463 [2,680, 3,645] | not met | 3,356–3,397 | 30.16 | 61.17 |
| S12 | 0.3579 | 0.9103 | 2,523 [2,068, 2,675] | not met | 2,083–2,150 | 22.05 | 48.04 |
| A16-2 | 0.3261 | 2.702 | 8,301 [8,080, 8,472] | met | 6,640–6,688 | 57.53 | 97.65 |

### 5.3 C3. Distillation versus RL on the same objective

H2-v5 is met only in A16-2 (LB 0.596 > 0.10; Table 1), where cfg-6 RL collapses to 2 of 3 probes in 4/5 seeds and G\*
also beats RL by 0.85 nats, so the result reflects RL failing to transfer rather than a student advantage. In S2, S4
and S8, RL has the higher $g_T$ as a point estimate while the student has the higher success, but no RL-higher $g_T$
CI excludes 0 (Table 3), so the inversion is false in every cell; the `rl_success` check is also false in S2 and S12.
Without multiplicity correction, the student beats cfg-6 RL on success with CIs excluding 0 in S2, S12 and A16-2
(A16-2 confounded by RL collapse; Table 2b).

The `rl_success` arm scores below the student on success in both cells where it was run: +0.1087 [+0.05933, +0.158]
in S2 and +0.07933 [+0.022, +0.134] in S12 (student − `rl_success`, uncorrected), and on BI by +0.2992 [+0.2031,
+0.3992] and +0.2920 [+0.1773, +0.4139]. Its seeds 711–715 trained for 123,392 / 124,672 / 181,760 / 200,192 / 125,440
episodes in S2 and 184,576 / 113,408 / 111,104 / 162,304 / 165,888 episodes in S12; all but one run ended before the
episode cap, so these rows describe training shorter than the episode cap. With those training lengths, its per-seed test5
success lies in 0.3767–0.4333 (S2) and 0.3167–0.4233 (S12).

In A16-2, RL seeds 712–715 use 2.0 probes per episode against $n^\* = 3$, with success 0.1833–0.2267, while seed 711
uses 2.773 probes. One RL configuration chosen on S2 was reused everywhere; it visibly fails in A16-2, and whether it
is under-tuned in S4, S8 or S12 was not tested \cite{blau2022optimizing, foster2021deep}.

**Table 3. RL objective $g_T$ on test5 (nats; uncorrected contrasts with ci95).** The H2-v5 lower bounds are in Table 1.
`rl_success` rows: training lengths as in Section 5.3.

| Item | S2 | S4 | S8 | S12 | A16-2 |
|---|---|---|---|---|---|
| Mean $g_T$ student / RL / G\* | 5.666 / 5.870 / 5.480 | 5.506 / 5.822 / 5.385 | 5.541 / 5.712 / 5.380 | 5.275 / 5.245 / 5.068 | 6.899 / 6.066 / 6.920 |
| RL − student | +0.2044 [−0.1216, +0.5435] | +0.3164 [−0.07608, +0.7258] | +0.1712 [−0.1856, +0.5379] | −0.03084 [−0.4196, +0.3711] | −0.8332 [−1.117, −0.5464] |
| G\* − RL | −0.3900 [−0.8566, +0.06472] | −0.4371 [−0.9095, +0.01035] | −0.3321 [−0.7602, +0.07182] | −0.1762 [−0.6604, +0.2803] | +0.8541 [+0.5670, +1.144] |
| G\* − student | −0.1856 [−0.6788, +0.2997] | −0.1207 [−0.5957, +0.3161] | −0.1609 [−0.5300, +0.2019] | −0.2071 [−0.6172, +0.1834] | +0.02089 [−0.2299, +0.2863] |
| `rl_success` mean; − student | 5.820; +0.1540 [−0.2520, +0.5456] | — | — | 5.196; −0.07973 [−0.4255, +0.2791] | — |

### 5.4 C4. Travel cost and behaviour

H5b detects no trend of Δsucc on G\* travel over 5 cells (slope −0.0157/rad, ci95 [−0.104, 0.073]; per 100°,
−0.02741, ci95 [−0.1817, +0.1270]), but a change of up to about 7 pp across the observed travel range cannot be
excluded. Over the observed span of G\* travel, 0.1112 to 0.8213 rad, the slope's ci95 translates to −0.07393 to
+0.05167 in success (post hoc, no CI of its own). The regressor is G\*'s mean test5 travel, not κ, and A16-2, a
different library, is one of the five points; the weights were fixed before test5.

**Behaviour (descriptive).** In every cell the student travels less than G\*, and RL travels more than both (Table 5).
On set S, G\* travel is largest in S2 and smallest in S12. B-fan, which never moves between probes,
logs only the first-leg grid snap. RL uses about 3 probes in the S cells, below the student and G\*. We claim no
mechanism; why the student travels less than its teacher while staying below it on success is an open question.

**Table 5. Test5 behaviour: travel per episode (degrees, including the first-leg grid snap) and probes per episode.**
Learner entries are ranges over seeds.

| Cell | G\* travel / probes | Student travel / probes | RL cfg 6 travel / probes | B-fan travel |
|---|---|---|---|---|
| S2 | 47.06 / 3.863 | 28.65–38.25 / 3.940–3.963 | 118.1–145.8 / 3.0 | 1.422 |
| S4 | 23.18 / 3.913 | 11.27–16.67 / 3.947–3.983 | 69.31–80.43 / 2.813–3.010 | 1.422 |
| S8 | 9.404 / 3.933 | 5.022–5.643 / 3.987–3.997 | 28.82–37.60 / 3.000–3.083 | 1.422 |
| S12 | 6.373 / 3.970 | 2.457–3.315 / 3.990–4.0 | 22.53–25.02 / 3.000–3.097 | 1.422 |
| A16-2 | 21.22 / 2.933 | 17.18–20.36 / 2.900–2.973 | 40.43–118.6 / 2.0–2.773 | 1.445 |

## 6 Discussion

**What the five cells say about amortization.** Across four travel costs on one library and a second library, a cheap
distilled policy sits below its teacher in every cell and is not shown to lie within the 4 pp margin. The two splits
tell the same story at different magnitudes: the test5 point gaps lie below the validation gaps but come with wide
intervals, and neither split, read under its own rule, supports a match. We report the splits separately and computed
no pooled estimate, because the validation rows of G\* come from three rounds and test5 is the only split on which
every method ran in this round. Compared with the earlier single-cell rounds, the added cells do not reveal a regime in
which the gate passes; they replace two anecdotes with five measurements that agree in sign.

**What the student does buy.** Against hand-designed heuristics chosen on a pilot, the student wins in 4/5 cells under
Holm, and it remains ahead of the best test5 heuristic in every cell on point estimates, although by a smaller,
post-hoc margin with no interval. It does so at a per-decision cost far below that of full G\*, by a factor that differs between cells (Section 5.2).
For a practitioner, the result is therefore a cheap policy that sits between the heuristics and the planner on
success, not a substitute for the planner; whether the remaining shortfall is acceptable depends on the application
and on the evaluator caveat of E5.

**What the RL comparison says.** RL on the same objective, with one configuration tuned on S2, does not transfer to
A16-2, where it collapses to fewer probes than the budget allows. The one cell in which distillation scores higher on
RL's own objective is therefore the cell in which the comparator failed, and in the other cells no advantage either way
is resolved on $g_T$. The contrast between the routes is thus a statement about this RL setup, not about RL in general
\cite{blau2022optimizing}.

**The contrastive bound and the posterior read-out (C5).** On test5 point estimates, G\* has the lowest mean $g_T$ of
the three policies in all four S cells, while it has the highest success (Tables 2a and 3). Every G\* − learner $g_T$
CI includes 0 in the S cells, and the registered inversion check is false everywhere. The observation is only that the
contrastive bound and the posterior read-out can rank policies differently; it is not a finding. Amortized design work
that reports sPCE-type bounds as the quality of a learned policy \cite{foster2021deep} may still wish to check the
ordering against a posterior-based metric, and semi-amortized schemes that refine a policy online
\cite{hedman2025step} or keep a cheaper nested filter in the loop \cite{iqbal2024recursive} are natural designs in
which that check could be built in.

**Open questions.** Does label regret measured on student-visited states, rather than G\*-visited ones, explain the
shortfall? Would per-cell RL tuning change the RL rows outside S2? How much would a second G\* run per cell widen the
student − G\* intervals? Why does the student travel less than G\* in every cell while staying below it on success?

## 7 Limitations

1. **Power and equivalence.** Test5 has 300 episodes per method and cell (cut from 500 by addendum v5.1e), its
   student − G\* CIs are 9.6–12.3 pp wide, and no equivalence test was run.
2. **G\* run once.** G\* was run once per cell, so its run-to-run variance is missing from the student − G\* CIs; E7 is
   in nats and is not linked to the deployed G\* or to success.
3. **Evaluator.** Success is read at sub 8, and the sub-16 check (E5) covers 2 cells, 200 episodes and one student seed,
   so its effect on the five-seed test5 contrasts is unknown.
4. **Heuristic selection.** H\* came from a 200-episode pilot and is not the best test5 heuristic in 4/5 cells; the
   margins over the best test5 heuristic are post hoc and untested.
5. **RL.** One configuration, selected on S2, is used everywhere and collapses in A16-2; the `rl_success` arm exists
   only in S2 and S12, and nine of its ten runs ended before the episode cap (training lengths in Section 5.3).
6. **Multiplicity.** More than 30 BI, RL, `rl_success` and $g_T$ contrasts are reported without correction.
7. **Latency.** The CI rule is met in 1/5 cells, the ratios rest on one student seed, and the runners differ across
   cells.
8. **Validation sources.** The G\* validation rows of D5 come from three rounds (S2 previous round, S12 the round before).
9. **Scope.** Simulation only, planar shapes, a single fingertip on a fixed circle, two shape libraries, one κ for A16,
   the sub-8 read-out, and H5b fitted on five points; no hardware, 3D objects or held-out shapes were tested.
10. **Not run, by decision.** Retraining or remedy rounds, per-cell RL re-tuning, more test5 episodes, a G\* rerun,
    latency re-timing, a test of the post-hoc margins, and any new BI or $g_T$ test were not run.
11. **Design constants.** Several design constants (action grid, planner sizes, label and DAgger budgets, RL episodes per
    seed, bootstrap resamples) are not yet in a citable results field and are marked in the text.

## 8 Conclusion

We asked whether a policy distilled from a cost-aware greedy information-gain touch planner can stand in for it under
travel cost, how it compares with RL on the same objective and with hand-designed heuristics, and whether the gap
changes with travel cost. A pre-registered study across five cells gives four answers. First, the pre-registered gate
fails in all five cells, so matching G\* is not supported; the student is below G\* in every cell on both splits.
Second, the student beats the pilot-chosen heuristics in 4/5 cells and decides 2,523–9,933× faster per decision
(seed-701 timings), with smaller, post-hoc margins over the best test5 heuristic. Third, distillation scores higher on
RL's own objective only where RL collapses, and no inversion between that objective and the posterior read-out is
detected. Fourth, no travel-cost trend in the gap is detected, and a change of about 7 pp is not excluded. Concrete
next steps follow from the record rather than from new claims: regret measured on student-visited states, per-cell RL
tuning, repeated G\* runs to put the teacher's variance into the intervals, a finer evaluator check on all seeds, and
more test episodes for an equivalence test. Pre-registered; simulation; preliminary.
