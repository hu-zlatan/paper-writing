<!-- Condensed from draft_v4.md (the master, which stays the source of truth). Preparation only: not a stage 22 output,
not compiled, page count unknown. The stage 20 gate FAILED (5.0 / 10) and the owner has not chosen a direction, so this
text is not cleared for submission. It adds no number, claim or citation that is not in draft_v4.md. -->

# Cost-Aware Information-Gain Touch Selection under Travel Cost: Look-Ahead Headroom and Learnability in a Stay-and-Probe and a Travelling Regime

## Abstract

Active tactile localization chooses the next touch from a belief over object identity and pose, and when moving the
finger costs time, that choice trades information against travel. We ask how much headroom one-step look-ahead leaves
over greedy cost-aware information-gain touch selection (G\*), and whether G\* can be amortized by a policy distilled
from it or trained by reinforcement learning (RL) on the same objective. We study two cells of a planar simulated task:
S12 (κ = 12), a stay-and-probe regime where G\* moves the finger 4.3° between probes per episode, and S2 (κ = 2), in
which it moves 44.8°. Over 32 screened first actions, one-step rollout over a reduced greedy completion gains at most
2.2 % of the remaining expected ball information at κ = 12 (one-sided 95 % bound). With one belief-free DeepSets head,
neither the DAgger-distilled student nor PPO was shown to reach G\* in either cell: the student failed its pre-registered
non-inferiority gate twice in S12 and once in S2. Distillation had no detected advantage over RL on RL's own contrastive
objective; in S2 that objective ranks G\* below both learners, unlike the grid posterior, while in S12 the ordering is
marginal. The study is pre-registered, with one cell per regime; results are preliminary.

## 1 Introduction

A robot that localizes an object by touch receives sparse, ambiguous measurements. The standard remedy is to maintain a
belief over identity and pose and to choose the next touch by its expected information gain \cite{petrovskaya2011global,
hebert2013next, zheng2024bayesian, zheng2026bayesian}. Probing is not free: the finger has to travel, so cost-aware
selection scores each candidate by information per unit cost \cite{ottenhaus2018active, seminara2019active}.

Two questions follow. First, planning depth: greedy information gathering is backed by (adaptive) submodularity
\cite{javdani2012efficient, vien2015touch}, but these guarantees weaken when actions constrain the future
\cite{chen2015submodular, esfandiari2019adaptivity}, and travel cost is such a coupling, because where the finger ends
up determines what the next probe costs. Second, amortization: online information gain re-optimises at every decision.
Amortized experimental design replaces this with a policy trained once, by RL on contrastive information bounds
\cite{foster2021deep, blau2022optimizing, ivanova2021implicit, rainforth2024modern}. A validated planner offers a second
route, DAgger on the planner's dense per-action scores \cite{ross2011reduction, choudhury2017adaptive}, with PPO
\cite{schulman2017proximal} on the same objective as the natural comparator. Inside the second question sits a third:
whether RL's objective, a contrastive bound on information, orders policies the same way as the posterior used to judge
localization.

**Contributions.** (C1) A pre-registered bound on one-step look-ahead headroom over cost-aware greedy touch selection,
with instrument checks. (C2) A learnability study of one belief-free head in a stay-and-probe cell and a travelling
cell, with a behavioural diagnosis of finger travel. (C3) A comparison of planner distillation against RL on RL's own
objective in both cells, with the observation that this objective and the grid posterior order the planner and the
learners differently (clearly in S2, marginally in S12). (C4) A per-decision cost analysis, including an exploratory
comparison of reduced-size G\* with the students. The outcome reported here (a characterisation paper with no method
claim) is a row of the pre-registered outcome map; we propose no new selector.

## 2 Method

**Task.** The object is a planar polygon with identity from a library of K = 8 identities (4 near-symmetric base shapes
and one symmetry-breaking variant of each) and unknown pose. A probe returns a contact point and surface normal with
Gaussian noise ($\sigma_p$ = 1.0 mm, $\sigma_n$ = 5°) or a miss. All methods use the same likelihood. The finger rests
on a stand-off circle at angle $\phi_t$; an action selects one of 64 target angles and one of 8 approach offsets, so
$|\mathcal{A}| = 512$, with cost

$$c(a) = 1 + \kappa\,\frac{|\Delta\phi|}{\pi}, \qquad \Delta\phi = \mathrm{wrap}(\phi' - \phi_t),$$

and every method chooses only among actions that fit the remaining time. Between-probe travel excludes the first leg,
which includes a grid snap that no policy chooses.

**Cells.** The budget τ is calibrated so that G\* executes four probes on average. S12 = (κ = 12, τ = 4.9); S2 = (κ = 2,
τ = 4.7), whose probe-count verification (3.875 probes, within 4 ± 0.3) was run after the S2 experiments.

**Metrics.** Success requires the correct identity, position error below 5 mm and orientation error below 5° modulo
symmetry. Ball information BI is the log-ratio of posterior to prior mass in the success ball. BI is the primary metric
and every success contrast is reported second.

**Planner.** G\* maintains a particle filter and selects
$\arg\max_a \mathrm{EIG}_B(a;b)/c(a)$ among feasible actions, with ball EIG estimated by nested Monte Carlo at
$(N, C, M) = (2{,}000, 512, 64)$. Reduced configurations gN_C_M (g125_512_16, g500_512_4) keep all 512 candidates.

**Headroom.** $G(\kappa) = (\overline{V}_{LA} - \overline{V}_{G^\*})/\overline{V}_{LA}$ over a bank of 100
G\*-reached beliefs, where $V_{LA}$ is the value of the best of 32 screened first actions (G\*'s own, three structured
set-up moves, and random feasible actions), each followed by a reduced greedy completion. It is therefore
one-step-deviation headroom among the screened actions, not the gap to the optimal policy, and the selection bias of
$V_{LA}$ was not measured. Hold requires passing instrument checks on a construction with a known exact gap and on a
bank with exact gap 0, plus a bias guard.

**Learners.** Both use the same belief-free DeepSets head over the touch history with 512 masked logits, so the
training signal is the controlled difference. The student is trained by DAgger on tempered teacher scores (S12:
registered stopping rule and one remedy; S2: remedy-sized data and a fixed 200 epochs per round, last checkpoint). PPO
receives the increment of ball-sPCE, a contrastive estimate of ball information in the style of \cite{foster2021deep},
so its return telescopes to $g_T$, capped at 8.318 nats; each seed trains for 200,064 episodes with the configuration
selected in S12, not re-tuned for S2. Three seeds per learner per cell.

**Baselines.** Random, and B-fan, a belief-free heuristic that stays and cycles the approach offset. B-fan was chosen on
S12 pilot data and is the only heuristic run in S2.

**Protocol.** Hypotheses, thresholds and an outcome map were frozen before any S12 run; an amendment written before any
S2 run fixed the S2 readings and allowed no remedy round. H1: a student non-inferior to G\*, tested through gates D3
(S12) and D4 (S2) on 500 paired val3 episodes. H2 and H2-S2: lower one-sided 95 % bound of $g_T$(student) − $g_T$(RL)
above +0.10 nats. H3: Hold iff the one-sided 95 % upper bound of G(12) is below 0.03. Within a split all methods run
on the same episodes. Success and BI are read from an adaptive grid posterior at subdivision 8, after its gate E′ failed
at subdivision 4; no finer grid was checked. Contrasts use a crossed episode × seed bootstrap with B = 10,000 and no
multiplicity correction. test3 episodes 0–299 were reused for the S2 rows and later exploratory rows, so those rows are
exploratory.

## 3 Results

**Headroom (H3 Hold).** G(12) = 0.01624 (one-sided 95 % UB 0.0221 < 0.03), a gap of 0.0414 nats on a mean $V_{G^\*}$
of 2.506 nats. The κ = 2 row, measured in the S2 cell configuration and reported rather than tested, is also small:
G(2) = 0.01418 (UB 0.01974). All instrument checks passed. The result says nothing direct about deeper planning.

**Regimes.** In S12, 80.9 % of G\*'s between-probe moves are zero on test3 0–299 and it moves 4.3° per episode. In S2 it
moves 44.8°. RL ends at exactly 3 probes in both cells and moves 108.8° in S2 and 16.8° in S12. In S2 the student moves
a similar amount to G\* on average (37.7° vs 44.8°), unlike S12 (0.3° vs 4.3°), but its per-episode travel is only
weakly correlated with G\*'s (r 0.14–0.24 by seed), so the student is not confined to stay-and-probe, but it does not
reproduce G\*'s travel decisions.

**Learnability.** The student failed D3 in S12 on the first attempt (−5.87 pp against a threshold of −1.43 pp) and after
its one remedy (−4.40 pp against −1.68 pp), so H1 was never tested on test. It failed D4 in S2 (−2.80 pp against
−1.46 pp), although the BI clause (−0.105 nats) and the per-seed clause passed. On test, the S2 student trails G\* by
0.183 nats BI (ci95 [−0.269, −0.094]) and 10.2 pp success (ci95 [−16.6, −4.3]); the S12 remedied student trails by
0.049 nats (ci95 [−0.114, +0.019]) and 4.4 pp (ci95 [−9.3, +0.6]), neither interval excluding 0. The S2 test gap is wider
than the validation gap for every seed and its cause is not identified; a re-run of val3 0–49 through the test pipeline
rules out the scoring path on those episodes. Under-training does not explain S2: in all nine seed × round runs,
held-out regret was lowest at an epoch between 22 and 130 and rose by 0.007–0.026 to the kept checkpoint. Early stopping
was not tested.

**Table 1. Test rows. Success and BI on test3 0–299 (sub-8 grid); $g_T$ on test3 0–499. No cross-cell test.**

| Method | S12 success | S12 BI | S12 $g_T$ | S2 success | S2 BI | S2 $g_T$ |
|---|---|---|---|---|---|---|
| G\* | 0.4267 | 6.248 | 5.299 | 0.5533 | 6.673 | 5.397 |
| Student | 0.3822 | 6.200 | 5.368 | 0.4511 | 6.490 | 5.534 |
| RL | 0.3567 | 5.910 | 5.368 | 0.4233 | 6.310 | 5.979 |
| B-fan (exploratory) | 0.36 | 5.973 | — | 0.37 | 5.962 | 5.263 |
| Random | — | — | 2.618 | 0.1167 | 3.622 | 3.510 |

**Distillation against RL.** H2 is not detected in S12 (Δ$g_T$ +0.0002 nats, LB −0.3103), and H2-S2 is not detected
(Δ$g_T$ −0.4452 nats, LB −0.7485; the point estimate favours RL). No equivalence test was run, and post hoc both tests
could detect only advantages of roughly half a nat. On the grid posterior the student leads RL on BI in both cells
(+0.289 nats, ci95 [+0.117, +0.465]; +0.180 nats, ci95 [+0.091, +0.273]), and the success ci95 between them includes 0
in both. All six PPO policies converge to exactly 3 probes. We read this as a property of this RL setup, not of RL in
general.

**Instrument ordering.** On seed-averaged point estimates $g_T$(G\*) is below both learners in S2 (5.40 vs 5.53 / 5.98)
and marginally in S12 (5.30 vs 5.37, with 3 of 6 S12 learner seeds below G\*), whereas the grid posterior orders G\*
above both learners on point estimates (in S2 both ci95 exclude 0; in S12 the student − G\* BI ci95 includes 0). The
inversion is supported in S2 and marginal in S12. No interval exists for these $g_T$ contrasts, near-cap compression was
not measured on test, and the record cannot separate a property of the bound from RL's way of scoring well on it. We
record a methods observation, not a mechanism.

**Heuristic (exploratory).** In S2 the student exceeds B-fan on BI (+0.53 nats, ci95 [+0.42, +0.64]) and success
(+8.1 pp, ci95 [+1.7, +14.7]). The lower end of that success interval is small next to the evaluator's 7.5 % calibration
flip rate, the split is reused, and B-fan is not the best available heuristic for a travelling regime. In S12 the student
exceeded it on BI only (+0.23, ci95 [+0.14, +0.31]; success +2.2 pp, ci95 [−2.8, +7.3]).

**Cost.** The student's median latency (0.408 ms) is about 2,200× below full-size G\* (0.9135 s), not compared at
matched accuracy. Pruning candidates cannot reach the registered 10×, since assimilation and neighbour lists do not
depend on the number of scored candidates (measured full / pruned-16 is 3.22). In S12 only, at logged median latencies
of 20.8 and 46.0 ms, two reduced-size G\* trail the remedied student on BI by 0.16–0.23 nats, with every success ci95
against it including 0. These comparisons are exploratory and map a latency–accuracy frontier only partly.

## 4 Discussion and Limitations

Within the measured scope, greedy is a defensible teacher: one deviating step buys little among the screened first
actions in both cells. Making the planner travel did not make it learnable to non-inferiority, although the gates, as
registered with the observed standard errors, demanded near-parity with G\*, not a tolerance of a few points. For
amortized design work that reports sPCE-type bounds as the quality of a learned policy, our record suggests checking the
ordering against a posterior-based metric; in our data "no advantage on RL's own objective" carries little information
about localization quality.

The main limitations apply to every result above. There is one cell per regime and three seeds per learner, so
regime-dependent statements are anecdotal. There is no multiplicity correction, and test3 is reused. The evaluator is
not shown converged: success flips on 7.5 % of calibration episodes between subdivisions 4 and 8, the order of most
success contrasts. The S2 validation/test gap is unexplained. RL was not re-tuned for S2 and no S2 hyperparameter grid
was run for either learner. The belief-input control is under-fit and isolates nothing, so the representation question
is open. H3 covers 32 mostly random first actions with a reduced completion. S2 calibration was verified only after the
fact, and only B-fan was run there. Everything is simulated: planar objects, one shape library, one fingertip on a fixed
circle, Gaussian noise and no contact dynamics, with no held-out shapes, 3D objects or hardware.

## 5 Conclusion

In a pre-registered characterisation with one cell per regime, one-step headroom over cost-aware greedy touch selection
is small among the screened first actions. Neither learner was shown to reach the planner with one belief-free head. No
advantage of distillation over RL was detected on RL's own objective, and in the travelling regime that objective orders
the planner and learners differently from the grid posterior, which amortized active sensing work should check rather
than treat as an established lesson. Next steps are more cells and seeds per regime, regret on student-visited states, a
full-action screen, a resolution of the S2 validation/test discrepancy, a probe-count-aware RL comparator, and reduced
planners timed under the latency protocol alongside the learners.
