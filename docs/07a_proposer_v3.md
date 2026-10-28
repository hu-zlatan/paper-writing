# Stage 8 v3 · Pass 1: Proposer (fresh opus subagent, 2026-10-28)

> System: "You formulate testable scientific hypotheses."
> Task (verbatim template): "Generate at least 2 falsifiable hypotheses from synthesis. Output markdown and for each
> hypothesis provide rationale, measurable prediction, failure condition. Synthesis: {synthesis}"
> `{synthesis}` = full content of `docs/06_synthesis.md`.
> PIVOT context read in full: `results/v2/14_analysis.md`, `results/v2/15_decision.md`, `docs/07_hypotheses_v2.md`
> (definitions §1–§2), `results/v2/12_diag_analysis.json`, `results/v1/15_decision.md` (head).
> Also inspected: `code/touchbed/relframe.py` (docstring) and the module list of `code/touchbed/`.
> No prior involvement in this project. Nothing was run. Every number below is quoted from those files, with the
> source given. Thresholds are pre-registration proposals, not results.

**Status of this loop.** v3 is the last loop before escalation to the owner. The hypotheses below are chosen so that
**every outcome of the pre-registered tests maps to a pre-written paper statement** (§4). No outcome may trigger a
fourth design.

---

## 0. What the evidence allows, in one paragraph

Two facts are now measured, and one is not.
- **Fact 1. Cost-aware ball greedy G\* is close to the rollout-improvable optimum in this task.** The validated
  estimator (G1 pass: notch relative gap 0.829 in [0.573, 0.860]; zero-gap bank UB 0.00374) finds G(12) = 0.0146
  (UB 0.0208) and G(0) = 0.0049 (UB 0.0071) on S, 𝒜 = 32 × 8. Absolute gaps are 0.015–0.049 nats on 2.6–3.0 nats of
  remaining value (14_analysis §1.2). The caveat: 32 × 8 failed flatness at S12 (ΔBI +0.170 > 0.10), so this must be
  re-measured once on 64 × 8.
- **Fact 2. RL on ball-sPCE does not learn G\*'s policy in our CPU budget.** At S12 the absolute head reaches 0.204
  success against G\* 0.410 (500 validation episodes), 0.243 after 2× training. Exploratory κ = 0 policies trail by
  23.5–25.0 pp at equal probe counts (4.0 vs 4.0). On the exact notch every RL seed lands on the greedy move
  (f ≈ −0.005). The finger-relative head (one seed, exploratory) reaches 0.305 vs 0.440 (Δ −13.5 pp, CI
  [−21.0, −6.5]) and executes 3.0 probes vs 4.175.
- **Not measured: whether the policy architecture can represent G\*'s choices at all.** Every learned number so far
  mixes two causes: (i) the belief-free DeepSets history encoder cannot express G\*'s decision rule, or (ii) RL cannot
  find it (credit assignment over the budget, 256-way exploration, objective saturation). v2 cannot separate them.
  Supervised distillation of G\*'s full score vectors removes cause (ii). So it is both the most likely route to the
  headline and the experiment that **diagnoses** the RL failure.

G\* costs a recorded median of 0.840 s per decision on 32 × 8 (8,359 decisions, informal, 15_decision §3.4), about
1.7 s expected on 512 actions (estimate, not measured), against ≈ 0.53 ms for a policy forward pass (informal). That
1,000×-plus gap is the room in which an amortized policy can be useful even if it is slightly less accurate.

**The two ideas ("sushi, not curry").**
1. **Idea A: distil the validated-near-optimal teacher.** A finger-relative, belief-free student trained by DAgger on
   G\*'s EIG_B/c score vectors matches G\* at ≥ 100× lower per-decision latency (H1), and it does so where RL with the
   same architecture fails (H2, the diagnostic that turns v2's negative result into a finding).
2. **Idea B: the reason to distil greedy and not to plan.** Under travel cost the rollout-improvable headroom over G\*
   stays small on the corrected action set (H3, a characterisation with a kill condition).

H2 is the mechanism claim of Idea A, not a third idea. H3 is the justification of the teacher choice, which is also the
novelty boundary against imitation-of-oracle information gathering (§5).

Definitions are those of `docs/07_hypotheses_v2.md` §1 unless changed here: G\* (argmax over feasible a of
EIG_B(a; b)/c(a), N = 2,000, M = 64), ball information BI, success (identity + 5 mm + 5° mod symmetry), travel model
c(a) = 1 + κ·|Δφ|/π with probe-matched τ_κ, non-degeneracy rule §1.7, adaptive grid evaluator (sub = 4), crossed
episode × seed bootstrap with B = 10,000. Global v3 changes taken from 15_decision §4.1: 𝒜 = 64 φ′ × 8 ψ = 512 for every
method; primary cells {S0, S12, A12}; κ_hi = 12; n\*, τ_κ re-calibrated on 64 × 8; δ_c = min(4 pp, 0.15·D_c) and
ε_c = min(0.05·BI_c(G\*), 0.15·D_c^BI), both from the v3 pilot and frozen before test.

---

## H1: A distilled finger-relative policy is non-inferior to cost-aware greedy G\* and ≥ 100× cheaper per decision (Idea A, primary)

### Rationale
- **Gap.** 06_synthesis Gaps 1 and 3: information-driven touch selection re-optimises online at every decision
  (cost ∝ particles × candidates × outcomes), no tactile paper reports per-decision compute, and amortized BED has only
  been shown on scientific toy models. v2 measured the size of the online cost: 0.840 s median per G\* decision on
  256 actions.
- **Why distillation should work where RL did not.**
  - The label at every visited belief is the **whole 512-vector** of EIG_B(a)/c(a) over feasible actions. RL gets one
    scalar per step and must discover which of 256–512 actions produced it. Supervision removes credit assignment
    and exploration, the two RL failure modes v2 cannot rule out.
  - The teacher already includes travel cost, so the student need not learn the cost trade-off from returns. The RL
    relative head lost about one probe to travel (3.0 vs 4.175 executed probes, 15_decision §3.4).
  - The finger-relative frame is the one architectural change with positive evidence. On the same 200 episodes it beat
    the absolute head by +0.135 [+0.060, +0.210], +0.070 [−0.005, +0.140] and +0.115 [+0.040, +0.190] (15_decision
    §3.4, derived there). It used 32 distinct first φ vs 4 for every absolute seed.
  - DAgger is used because a student that deviates from G\* visits beliefs G\* never produces. Behaviour cloning alone
    is an ablation row.
- **Why near-ties make non-inferiority plausible even with imperfect imitation.** The look-ahead's chosen action
  differed from G\*'s on 41–58 % of beliefs, while the mean value gain was only 0.015–0.049 nats (14_analysis §1.2;
  AC row 3: near-ties are not separated from argmax noise). If many G\* decisions are near-ties, a student can disagree
  with G\*'s argmax often and still lose little value. So **top-1 agreement is the wrong selection metric**. I propose
  **normalised score regret** instead (below).

### Method (fixed before any v3 run)
- **Student.** `relframe.py` head on 𝒜 = 512 with the feasibility mask, same DeepSets encoder as v2.
- **Teacher.** Full-size G\* (N = 2,000, C = 512, M = 64). A `score_vector()` export writes EIG_B(a)/c(a) for every
  feasible a at every decision.
- **Loss.** Cross-entropy to softmax(β·s(a)/σ_s) over feasible a, where s(a) = EIG_B(a)/c(a) and σ_s is the per-belief
  standard deviation of s over feasible a, plus λ × CE to G\*'s argmax.
- **Data.** Round 0: 1,500 G\* rollouts per cell, shared across seeds. Then 2 DAgger rounds × 400 student rollouts per
  seed, labelled by G\* at every visited belief, with mixing β_DAgger = 1, 0.5, 0 (15_decision §4.1).
- **Hyperparameter selection.** At most 4 configurations of (lr, β, λ, batch), 1 seed each at S12. Selected on
  validation **normalised score regret**
  R̄ = mean over decisions of [max_a s(a) − s(a_student)] / [max_a s(a) − median_a s(a)],
  never on success. Ties within 0.01 go to the lower index. Top-1 agreement is reported, not used.
  This replaces the decision's top-1 rule and must be recorded as a deviation in amendment v3.0.
- **Seeds.** 5 per cell. Test 1,000 paired episodes per primary cell, grid evaluator.

### Measurable predictions
- **H1a (non-inferiority, success).** In every informative primary cell c ∈ {S0, S12, A12}, the one-sided 95 % lower
  bound of success(student) − success(G\*) is **> −δ_c**.
- **H1a (non-inferiority, BI).** In every informative primary cell, the one-sided 95 % lower bound of
  BI(student) − BI(G\*) is **> −ε_c**.
- **H1a (seed robustness).** At least **4 of 5** seeds have point Δsuccess > −δ_c in every informative cell.
- **H1b (latency at the student's accuracy).** With the §2.3 latency protocol (one pinned core, 20 warm-up + 500 timed
  decisions, interleaved), the boundary rung R_b (the most expensive rung of the ladder rescaled to 512, R0 = 512
  candidates → R7 = 32, whose median latency is ≤ 100 × the student's) satisfies: upper 95 % bound of
  success(R_b) − success(student) **< 0** in every informative cell.
- **H1c (mechanism, reported with its interval).** On S12 validation, the student's normalised score regret R̄ is
  **≤ 0.25**, and episodes where the student disagrees with G\*'s first action lose no more than δ_c in success versus
  episodes where it agrees. (Descriptive; it explains a pass, it does not decide one.)

### Failure conditions
H1 is **rejected** if any of the following holds on test:
- (a) any informative primary cell has success LB ≤ −δ_c **or** BI LB ≤ −ε_c;
- (b) fewer than 4 of 5 seeds pass in some informative cell;
- (c) any informative cell has R_b upper bound ≥ 0 (the cheap greedy is not worse than the student);
- (d) fewer than 2 of the 3 primary cells are informative under §1.7: then H1 is **inconclusive on success** and is
  decided on BI alone, labelled so.

Partial outcomes are pre-labelled:
- Failure only at S12 or A12 (κ = 12), pass at S0: "amortized ball greedy is supported without travel; **cost-aware**
  amortization is rejected". The title drops "cost-aware".
- H1a passes but H1b fails: "non-inferior but not ≥ 100× cheaper at its accuracy". The latency claim is dropped.

### Learnability gate before any main run (D3, from 15_decision §4.3, made stricter on the diagnosis)
- S12, 3 seeds, chosen HP, full DAgger recipe, 500 validation episodes, grid evaluator.
- **Pass:** seed-mean success ≥ success(G\*) − 5 pp **and** seed-mean BI ≥ BI(G\*) − 0.30 nats.
- **One remedy:** double round 0 and both DAgger rounds once. If it still fails, H1 is dead and the paper goes to
  outcome row 3 or 4 of §4.

### Pre-registered fallback inside Idea A (not a new idea): student-pruned greedy
If D3 fails after the remedy, or H1a fails on test, the **same trained student** is evaluated as a candidate
generator: G\* scores only the student's top-k actions (k = 16 of 512) and picks argmax EIG_B/c among them.
- **Prediction (H1-fb).** Non-inferior to full G\* by the H1a rules, at a measured per-decision latency ≥ 10× lower
  than full G\*.
- **Failure.** Non-inferiority fails, or the measured latency ratio is < 10×.
- **Honest limit, stated now.** This variant still runs the online PF (N = 2,000) and its assimilation step. The share
  of G\*'s 0.840 s spent on candidate scoring vs PF assimilation has **not been measured**. If scoring is not the
  dominant share, the 10× target cannot be met, and H1-fb fails by its own rule. The split is measured in gate Lat′
  before any H1-fb claim is drafted.
- k = 16 is fixed now. No sweep over k is run on test.

---

## H2: The v2 RL failure is an optimisation failure, not a representation failure (Idea A, mechanism)

### Rationale
- v2 shows a large deficit for RL on ball-sPCE, at κ = 12 and at κ = 0 (exploratory), with both heads. The deficit
  persists after 2× training (+3.9 pp only) and on the notch the policy value is identical to the last digit after
  doubling training (14_analysis §2.3).
- The **same architecture and inputs** trained with dense teacher labels isolate the cause:
  - if the student closes the gap that RL leaves, the architecture can represent the G\*-level policy and RL's
    failure is one of optimisation (credit assignment, exploration, saturation);
  - if the student fails too, the belief-free history encoder is the bottleneck, which is itself a finding for the
    amortized-BED literature (Cluster 5 methods all use history encoders of this kind).
- This turns the v2 negative result into a controlled contrast, which is what an RSS reviewer will ask for: "why not
  just RL?".

### Method
- **Comparator row.** RL sPCE-total with the finger-relative head on 𝒜 = 512 (hp1, E_train 10⁵, plateau rule,
  doubling rule of v2 §2.1), 3 seeds, cells S12 and S0. Retrained under v3 settings. The v2 seeds 400–402 are not used.
- **Student.** The H1 student, seeds 1–3 of the 5, same cells.
- **Test.** 500 paired test episodes per cell (row size), grid evaluator. Training CPU-h of both methods is reported,
  including G\* labelling cost, so the comparison is not presented as compute-matched when it is not.

### Measurable predictions
- **H2a.** In S12 **and** S0, success(student) − success(RL-relative) has a paired crossed-bootstrap two-sided 95 % CI
  with **lower bound > +5 pp**.
- **H2b.** In S12 and S0, the student closes ≥ 75 % of the RL gap to G\*:
  [success(student) − success(RL)] / [success(G\*) − success(RL)] ≥ 0.75 (point estimate, with its bootstrap CI
  reported).
- **H2c (travel mechanism, S12 only).** The student's mean executed probe count is within 0.3 of G\*'s, while the RL
  row's is lower by ≥ 0.5. (v2: RL relative 3.0 vs G\* 4.175 probes.)

### Failure conditions
- H2 is **rejected** if, in either cell, the CI of success(student) − success(RL) includes +5 pp or less (LB ≤ +5 pp).
  The paper then states that dense supervision does not rescue the belief-free encoder, and the encoder, not the
  optimiser, is named as the limiting factor.
- H2 is **not testable** (and is reported as such) if the RL row fails to plateau after the doubling rule in either
  cell.
- H2c is descriptive and cannot fail H2.

---

## H3: Under travel cost, validated look-ahead headroom over G\* stays small on the corrected action set (Idea B, characterisation with a kill condition)

### Rationale
- 06_synthesis Gap 2 asked whether a myopic-vs-non-myopic gap exists for touch localization; Cluster 6 predicts that
  greedy is competitive under (near-)adaptive submodularity and weak when actions constrain the future. v1 measured no
  gap with free repositioning. v2 added travel cost, which is exactly the setting where budgeted / orienteering
  results say greedy can be weak, and still measured G(12) = 0.0146 (UB 0.0208).
- The estimator is not blind: on the constructed notch it recovers an exact gap (V_opt 0.615 vs V_greedy 0.174; LA
  estimate 0.981 of exact). Its known bias (V_greedy under-read at 0.597 of exact) **inflates** G, so a small G is a
  conservative reading.
- The 32 × 8 set failed flatness (ΔBI +0.170 at S12). The measurement must be repeated once on 64 × 8, where the φ′
  spacing halves (11.25° → 5.625°, 256 → 512 actions), i.e. **finer travel choices for both G\* and the
  look-ahead**. That could in principle create headroom (a finer grid lets a planner pick a cheaper set-up
  move), so the result is not foregone.
- Role in the paper: it justifies choosing G\* as the teacher (distilling a planner would buy ≤ the measured
  headroom), and it is the novelty boundary against imitation of clairvoyant oracles (§5).

### Method (frozen; no re-run on 32 × 8, no added κ levels)
- B6-frozen G1 estimator, unchanged. 100 G\*-reached beliefs per κ ∈ {0, 2, 12}, set S, 𝒜 = 64 × 8, n\* re-calibrated.
- Notch control re-run once with the frozen estimator (5 runs) to confirm the instrument on the new code path.
- Report alongside: the 32 × 8 values, and the fraction of beliefs where look-ahead and G\* disagree.

### Measurable predictions
- **H3a.** UB95(G(12)) **< 0.05** and UB95(G(0)) **< 0.03** (one-sided bootstrap bounds over beliefs, B = 10,000).
- **H3b (instrument still sensitive).** Notch mean relative gap across 5 runs in [0.573, 0.860] (the G1 (a) band).

### Failure conditions
- **Kill:** G(12) ≥ 0.10 **or** LB95(G(12)) > 0.05. The paper may not say "greedy is near-enough"; it reports the
  headroom, and H1's teacher choice is stated as a limitation (look-ahead reopened for the full paper only).
- **Inconclusive:** UB95(G(12)) ≥ 0.05 with LB95 ≤ 0.05. Stated with its interval; no "near-optimal" wording.
- **Instrument failure:** H3b fails. Then H3 is **untested** on 64 × 8, and only the 32 × 8 numbers are quoted with
  the flatness caveat.
- H3 never blocks H1: H1 is a non-inferiority claim against G\* and stands without H3.

---

## 4. Outcome map (all four rows are pre-written; the owner is told which row occurred)

| Row | Outcome | Paper | Venue fit |
|---|---|---|---|
| 1 | H1 pass, H3 holds (± H2) | "Near-optimal touch selection in one forward pass": validated small headroom over cost-aware greedy, so distil it; ≥ 100× cheaper at matched accuracy; RL on the information bound fails for optimisation reasons (H2). | RSS main claim |
| 2 | H1 pass, H3 killed or inconclusive | Amortization result as row 1; H3 reported as measured headroom; "teacher could be improved" as limitation. | RSS, weaker framing |
| 3 | H1 fails, H1-fb passes | "Learned candidate pruning for online information-gain touch selection": same quality as G\* at the measured speed-up (≥ 10×), with H2 and H3 as supporting findings. | RSS short / workshop-to-full |
| 4 | H1 and H1-fb fail | Characterisation paper: H3 + learnability failure of both RL and distillation with the same encoder + evaluator finding (SMC under-reads BI by 0.063–0.177 nats against the 128k reference, 14_analysis §1.2). Escalate to owner: submit as RSS extended abstract or retarget (e.g. RA-L / workshop). | Owner decision |

Not allowed after the run: switching the selection metric, changing k in H1-fb, adding cells, re-running H3 on another
grid, or choosing between RL and distillation on test data.

---

## 5. Literature checks this hypothesis set depends on (stage 8 must verify before citing)

- **Imitation of information-gathering oracles.** Choudhury et al., "Adaptive information gathering via imitation
  learning" (RSS 2017) is believed to imitate a clairvoyant oracle for exploration. **Unverified here; do not cite
  until checked.** If verified, H1's novelty narrows to: (i) touch localization with a joint identity × SE(2) belief and
  travel cost; (ii) a teacher whose near-optimality is *measured* with a validated estimator (H3) rather than assumed;
  (iii) latency at the student's own accuracy (H1b). If a verified paper already distils greedy EIG for touch, the
  skeptic decides whether H1 survives as a claim.
- **DAgger** (Ross, Gordon, Bagnell, AISTATS 2011): verify the citation.
- **Budgeted / adaptive submodularity** for the H3 framing (javdani2012efficient, chen2015submodular are in the cards;
  any orienteering-type greedy bound must be verified before it is cited).
- **Step-DAD** (hedman2025step, in the cards) is the closest precedent for H1-fb (amortized proposal + test-time
  refinement) and must be credited there.

---

## 6. Feasibility (from 15_decision §4.5, not re-estimated here)
- Gates ≈ 45 CPU-h, main ≤ 125 CPU-h on GitHub Actions, with the decision's downscale order. H2's RL rows
  (2 cells × 3 seeds) fit inside the "ablation / comparator rows ≈ 15 CPU-h" line only if one RL run costs ≤ ≈ 2 CPU-h
  (v2: 0.8–1.7 CPU-h per 10⁵ episodes on 256 actions; 512 actions not yet measured). If it does not fit, H2 drops S0
  first and is reported for S12 only, labelled so.
- H1-fb adds G\* scoring of 16 candidates per decision on 1,000 test episodes per cell. It is run only if row 3 is
  reached, from the 11-20 → 11-22 buffer.
- Timeline: gates and D3 decided by 11-12 (11-14 with the remedy); main runs 11-13 → 11-19; analysis 11-23 → 11-25;
  extended abstract 2026-12-04. Every outcome row of §4 can be written by then.
