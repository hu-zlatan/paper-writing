# Stage 15 · RESEARCH_DECISION (v1) — fresh opus subagent, 2026-10-28

> System: "You are a research program lead making go/no-go decisions."
> Task (verbatim instruction): "Make a PROCEED, REFINE, or PIVOT decision from analysis. PROCEED: results are strong
> enough to write the paper. Proceed to stage 16. REFINE: hypothesis is correct but the experimental evidence has
> fixable weaknesses (more seeds, more conditions, an additional ablation, a baseline tuning pass). Stay on the same
> hypothesis; loop back to stage 13 with specific code changes. PIVOT: results contradict the hypothesis or reveal a
> more interesting question. Loop back to stage 8 with a new hypothesis informed by what was learned. Output markdown
> with: Decision, Justification, Evidence (with cited numbers from the analysis), Next Actions (specific stage and
> tasks)."
> `{analysis}` = `results/v1/14_analysis.md` (full) + the addendum of `results/v1/12_manipulation_checks.md` (myopia
> bank on positive-control set PC). Context read: `docs/07_hypotheses.md`, `docs/06_synthesis.md`,
> `docs/00_topic_init.md`, `docs/07c_amendment_v1_1.md`, `docs/10_dev_findings_v1.md`, `docs/07b_theoretical_bounds.md`.
> No prior involvement in this project.

---

## 1. Decision

**PIVOT — loop back to stage 8.** The paper keeps the non-myopic claim only by moving to an action model where
look-ahead has a structural reason to matter: the finger has to **travel between probes under a time budget**. The
manipulated variable is the travel-cost ratio κ, which replaces "ambiguous vs asymmetric shape set". Amortization
(non-inferiority to greedy at ≥ 100× lower latency) is the guaranteed core. The non-myopic claim is a second idea that
enters the paper only if a pre-registered gate passes, and the gate depends on an estimator that has first been
validated against a known gap. H3 (planning for no-contact outcomes) leaves the claim set.

The two core ideas ("sushi, not curry"):
1. **Amortized, goal-oriented touch selection.** One forward pass matches online greedy PF-EIG (non-inferior, 4 pp) at
   ≥ 100× lower latency at matched accuracy. This idea does not depend on non-myopia.
2. **Look-ahead pays when touches cost travel** (conditional on gate G2 in §4.2). The non-myopic advantage over
   myopic training and over cost-aware greedy appears and grows with κ. At κ = 0 it is ≈ 0, which is the v1 finding
   recovered as one end of a dose–response curve.

Everything else (NC-input ablation, history encoder, L or objective ablation, RL-success baseline, MuJoCo transfer) is
a component ablation or a supporting experiment, not a claim.

## 2. Justification

**Why not PROCEED.** None of the three hard requirements can be met:
- No policy has been trained, so there is no primary-metric difference between the proposed method and any baseline.
  14_analysis states this directly: "No trained policy appears in any of the files".
- No component has been ablated.
- There are integrity flags. They are not fabrication, but they must be closed:
  - an unrecorded estimator deviation (C1/Y1/C2/M = 16/8/16/16 instead of 32/32/32);
  - three S self-symmetry entries that are exactly 0.0 (likely a sentinel or skipped computation);
  - five overstated claims in 12_md that the area-chair pass rewrote (rows 1, 3, 4, 5 and 6 of §6).

**Why not REFINE.** REFINE requires a hypothesis that looks correct with thin evidence. That is not the situation:
- **H2a has no measured premise.** Its pre-registered manipulation check fails in the wrong direction, and S is no
  more myopia-prone than A.
- **H3 is untestable by its own rule.** Its precondition fails on both parts.
- **The measuring instrument itself failed.** On PC, a set built to contain a look-ahead gap, the estimator again
  reports a significantly *negative* full-state gap. So "fix S until G passes" would mean iterating an unvalidated
  estimator on a redesigned set until a threshold is met. 14_analysis §5 calls this a forking path.
- A redesign of S is a change of hypothesis premise. It is not a seeds, conditions or baseline-tuning change, so it
  belongs at stage 8, not stage 13.

**Why PIVOT, and why this pivot.** Both PIVOT triggers apply:
- **The predicted phenomenon does not appear.** No positive two-step advantage is found on S, A, S-identity or PC.
- **A more interesting question emerged.** The pattern points to a structural explanation. In the v1 action model,
  every probe can be launched from anywhere at zero cost, and contacts are precise (σ_p = 1 mm, σ_n = 5°). So any
  "set-up" information a planner could buy with probe 1 is also available to greedy at probe 2 at no extra cost.
  Greedy is close to adaptive-submodular in this regime (javdani2012efficient), and look-ahead has little headroom.
  This is an informal argument and is labelled as such. Look-ahead matters when actions *constrain the future*: travel
  time, reachability, or a shared time budget (budgeted and orienteering-type informative path planning, where greedy
  is known to be weak). This gives a clean, single independent variable, κ, with a built-in negative control (κ = 0
  reproduces v1), and the claim is more relevant to robots.

**Options considered** (as required by the task):

| option | verdict | reason |
|---|---|---|
| (a) Keep the non-myopic claim, move to a travel / time-budget action model | **adopted as idea 2, gated** | It is the only option that keeps the paper's headline (Gap 2 of 06_synthesis) on a principled premise. It turns v1's null into the κ = 0 control instead of a failed check. Risk: greedy-per-cost may still be near-optimal, so the gate decides. |
| (b) Centre on amortization (non-inferiority to greedy PF-EIG at much lower latency) | **adopted as idea 1, guaranteed core** | H1a/H1b need no myopia gap. Greedy is a strong, non-trivial comparator (+28.7 pp and +64.3 pp over random at T = 3), and full-size greedy costs ≈ 0.65 s per decision (A4). This is what the 2026-12-04 extended abstract can stand on. Alone it is the weaker paper (novelty "medium", 06_synthesis Gap 3), so (a) is pursued as well. |
| (c1) Goal-oriented (identity × symmetry-mode / success-region) information objective as a headline | **folded into idea 1 as the method's objective, not a separate claim** | F2 shows total-state information is dominated by fine pose (mean max EIG₁ 3.07 nats full state vs 0.92 identity on the same S beliefs). The objective has to be decision-focused for both ideas. It is defended by one ablation row (total-state sPCE vs goal-oriented). |
| (c2) Redesign S (deeper or off-center features) and re-run the v1 check | rejected | Forking path, and the instrument has not been validated. Without a structural reason, a redesign is unlikely to move G from −0.033 to ≥ 0.10. |
| (c3) Keep H3 (planning for no-contact outcomes) | dropped as a claim; NC-input ablation kept as a component row | R_NC(S) = 0.03 < R_NC(A) = 0.07. Misses are almost never decision-relevant for greedy choices. |

## 3. Evidence (numbers cited from the analysis)

**The H2 premise fails: no myopia gap, and the wrong ordering.**
- Myopia gap on S (full state): G(S) = **−0.0329** (SE 0.0102), bootstrap 95 % CI [−0.0538, −0.0143], one-sided 95 %
  upper bound **−0.0171** against the required ≥ 0.10. Sign test: 13/49 positive, p = 0.9998.
- G(A) = −0.0198 [−0.0387, −0.0007]. The required ordering G(S) ≥ 0.10 > 0.03 ≥ G(A) is reversed (−0.033 < −0.020).
- Absolute gaps are almost identical: −0.110 vs −0.112 nats, even though C(S) = 0.971 vs C(A) = 0.772. Geometric
  confusability does not translate into decision ambiguity.
- Identity-only target on S (the best case, exploratory): G = **+0.0029**, CI [−0.0201, +0.0251], upper bound
  **+0.0213**. That is about one-fifth of the 0.10 threshold. Sign test 23/43, p = 0.38. 12 % of beliefs have a
  relative gap ≥ 0.10.
- 2-step-selected vs greedy mean EIG₂: S 4.072 vs 4.182; A 4.635 vs 4.746. The two-step choice is worse.

**The estimator is not validated: positive control PC (addendum).**
- Full state: G = **−0.052**, absolute gap −0.183 nats [−0.261, −0.110].
- Identity: G = −0.006, absolute gap +0.006 [−0.005, +0.017] (mean max EIG₁ 0.118, EIG₂* 0.261).
- So the bank estimator (16/8/16/16 with fresh re-estimation) cannot detect a gap even where one was designed in. It
  is a lower bound with a negative selection bias.
- The analytic H2b-P2 notch scenario was never computed. Its expected values are: greedy ≈ 0.2 nats, optimum
  ≈ 0.69 nats, relative gap ≈ 0.7.
- Implication: v1 cannot say "no gap exists". It can say "no gap was detectable, and the instrument is not shown to be
  able to detect one". Both readings call for a new premise and a validated instrument, not more seeds.

**H3 premise fails.**
- R_NC(S) = **0.03** and R_NC(A) = **0.07**. The precondition requires R_NC(S) ≥ 0.20 and R_NC(S) > R_NC(A), so it
  fails on both parts.
- The greedy action has P(NC) = 0 for 45 % of S beliefs.

**Evaluation PF not converged.**
- N = 8,000 vs 32,000 fails the A3 rule in **6/6** cells.
- Ball information is higher at 32k by **0.089–0.396 nats**, and every 90 % CI is above 0.
- S-T10-random: Δ success = **+6.0 pp** [+1.3, +11.0], Δ identity +7.7 pp.
- The ±2 pp CI criterion fails in 6/6 cells. With 300 paired episodes it is near the limit of what can be shown.
- The greedy-T10 and pilot-policy cells are unanalysed.

**Idea 1 is viable: greedy is a strong comparator with headroom in latency, and on S in accuracy.**
- At T = 3, N_eval = 32k: greedy beats random by **+64.3 pp** on A (0.767 vs 0.123, 95 % CI [58.3, 70.4]) and by
  **+28.7 pp** on S (0.420 vs 0.133, [21.9, 35.5]).
- T = 5 is not yet reported.
- Full greedy costs ≈ **0.65 s per decision** (A4), against an O(d²) ≈ 3·10⁴ multiply-add policy forward pass
  (07b §2). The H1b matched-accuracy 100× ratio is plausible but untested.

**Confusability: set level passes, per-shape rule violated.**
- C(S) = 0.9709 ≥ 0.90 and C(A) = 0.7724 ≤ 0.80. Both are lower bounds.
- A2 = 0.806, A4 = 0.818 and A6 = 0.818 violate the per-shape ≤ 0.80 acceptance rule.
- The S self-symmetry entries of S_rect, S_rtri and S_hex are exactly 0.0 (unexplained).

**Integrity flags to close before any main run** (not fabrication):
- The estimator deviation 16/8/16/16 vs 32/32/32 is not in 07c.
- The claim "mixing, not particle count, is the bottleneck" rests on 40 episodes (SE ≈ 8 pp) and its data are not in
  the cited JSON.
- 12_md overstated "Confusability PASS" and "greedy vs random met" (T = 5 missing). See 14_analysis §6, rows 1–14.

## 4. Next actions

### 4.1 Stage 8 (HYPOTHESIS_GEN, v2): start from these hypotheses

Write v2 hypotheses as a new file, `docs/07_hypotheses_v2.md`. Keep 07_hypotheses.md intact as the v1 record, and add a
short "v1 → v2 change log" that cites this decision.

**Action model (v2).**
- The finger rests on a stand-off circle of radius 100 mm around the workspace.
- An action is a = (Δφ, ψ). The finger first moves along the circle by Δφ, then probes with offset ψ.
- Each action costs time: c(a) = κ·|Δφ|·R_s / v_travel + stroke_time(hit or miss).
- An episode ends when a **time budget** τ is exhausted. T is no longer a touch count.
- κ ∈ {0, κ_mid, κ_hi}, fixed in stage 9 by a pilot so that roughly 2–3 / 4–6 / 8–10 probes fit in τ at κ_hi / κ_mid /
  κ = 0.
- **κ = 0 is exactly the v1 free-repositioning model.** It is the built-in negative control.

**Target.**
- The information objective and the co-primary metric are both goal-oriented: **ball information** (A2) or
  identity × symmetry-mode information. Total-state sPCE becomes an ablation.
- Sets A and S are both kept, for generality of idea 1. Replace A2, A4 and A6, or amend the per-shape rule, before the
  freeze.

| v2 hypothesis | status | core content (thresholds keep the v1 conventions: SESOI 3 pp, NI 4 pp, TOST ±3 pp) |
|---|---|---|
| **H1a′** amortized non-inferiority | core (idea 1) | The goal-oriented sPCE-total policy is non-inferior (upper bound < 4 pp on success, < 5 % on ball information) to the online greedy comparator in every primary cell: plain PF-EIG at κ = 0, **cost-aware greedy (EIG per unit time)** at κ > 0. It beats random and coverage at the small budgets. |
| **H1b′** latency at matched accuracy | core (idea 1) | The matched-accuracy greedy configuration is ≥ 100× slower per decision than the policy, on both sets. Also reported: the full-size ratio, break-even episodes, and the online **rollout planner's** latency. |
| **H2a′** non-myopic advantage grows with travel cost | core (idea 2), **only if gate G2 passes** | Δ(κ) = sPCE-total − sPCE-myopic, both with identical cost input and only credit assignment differing (§3.3 of v1). At κ_hi: lower bound > 0 and point estimate ≥ 3 pp on success, and lower bound > 0 on ball information. Slope over κ ∈ {0, κ_mid, κ_hi}: lower bound > 0. At κ = 0: reported with TOST ±3 pp (expected equivalence). Secondary: sPCE-total vs cost-aware greedy at κ_hi, lower bound > 0 on ball information. |
| **H2b′** mechanism | core (idea 2), gated | (P1) On identical beliefs at κ_hi, the total policy's first action has lower EIG₁ but higher multi-step value (validated estimator, threshold 0.05 nats). (P2) The analytic notch positive control, computed **exactly on the grid**: the policy reaches ≥ 80 % of the exact optimum. (P3, travel-specific) Policy routes show fewer backtracks and less travel per nat than cost-aware greedy. |
| H1c (objective vs sparse task reward) | demoted to a reported ablation row | RL-success is kept as a baseline row, with no confirmatory claim. |
| H3 | **dropped as a claim** | NC-input ablation is kept as a component row (SC3). R_NC is reported per κ for transparency. |
| H4 (MuJoCo transfer) | supporting experiment, full paper only | Not in the extended abstract. |
| H5′ | deferred to the full paper or dropped | — |

**Fallback, pre-registered in stage 8.** If gate G2 fails by **2026-11-12**:
- The paper is idea 1 (H1a′/H1b′) plus a **measured finding**: "with a validated estimator, look-ahead headroom over
  greedy is ≤ X for free-repositioning touch, and ≤ Y even under travel cost".
- That finding is reported as a characterisation result, with its CI, and not as a failed hypothesis.
- H2a′/H2b′ are not run. Main runs stay at κ = 0 and κ_hi, with cost-aware greedy as the comparator.

### 4.2 Pre-run checks that must pass before any main run (stage 10–12, all on CPU)

Every change goes into a dated amendment, `docs/07c_amendment_v2_0.md`, written *before* the check is re-run.

| gate | check | pass rule |
|---|---|---|
| **G0** hygiene | Record the 16/8/16/16 deviation. Fix and explain the S self-symmetry 0.0 entries. Replace or amend A2, A4 and A6. Add the missing greedy-T10 and pilot-policy PF cells. Report greedy vs random at T = 5. | Done, with a commit hash, before G1. |
| **G1** estimator validation (positive control) | Compute the analytic H2b-P2 notch scenario **exactly on the 401-point grid**: the exact optimum and the exact greedy value. Fix the estimator against selection bias: common random numbers across candidates; screen C1 ≥ 32 candidates that include structured set-up moves; re-estimate the top-4 with ≥ 4× fresh samples; horizon = remaining budget, completed by greedy rollout. Run it on the notch scenario. | The estimated relative gap recovers the exact gap within ±20 % of its value (exact ≈ 0.7). The mean gap is ≥ 0 on a bank of 100 beliefs where the exact gap is 0 (no negative bias beyond −0.01). **If G1 fails, G2 is uninterpretable, and the fallback applies.** |
| **G2** manipulation check, travel model | Run the G1-validated estimator on a bank of 100 beliefs reached by **cost-aware greedy** (not random probes) at each κ, target = goal-oriented information. | G(κ_hi) ≥ 0.10 with one-sided 95 % lower bound > 0.05; G(κ = 0) ≤ 0.03; G increases monotonically over κ. One attempt at the pre-registered κ grid, plus at most one pre-registered κ_hi escalation. No set redesign loop. |
| **G3** learnability | Train sPCE-total (goal-oriented objective) on the notch control and on one κ_hi cell, 3 pilot seeds. | Notch: ≥ 80 % of the exact optimum. κ_hi cell: reaches cost-aware greedy minus 5 pp on validation within the E_train cap with a plateau. Objective saturation < 10 % of episodes (F2 rule). |
| **G4** evaluation PF | N vs 4N on ball information and success, with ≥ 600 paired episodes per cell (re-specify the CI rule in the amendment, since 300 cannot reach ±2 pp), in all cells including greedy-T10 and the pilot policy. Use 32k, or a better-mixing kernel validated by an arm with 32k × 30 MH steps. | The A3 rule as amended: \|Δ ball info\| ≤ 0.05 nats, \|Δ success\| ≤ 1 pp with 95 % CI inside ±2 pp. |
| **G5** comparator strength | Cost-aware greedy vs random under the same time budget at each κ; online 2-step rollout planner run on 200 episodes at κ_hi for an upper reference. | Greedy ≥ random + 10 pp in every primary cell. The rollout planner's latency is measured (it is part of the H1b′ story). |

### 4.3 Stage-by-stage plan and dates (RSS 2027: extended abstract 2026-12-04, full paper 2027-04-16)

| dates | stage | tasks |
|---|---|---|
| 10-29 → 10-31 | **8** | Write `docs/07_hypotheses_v2.md` per §4.1, including the fallback rule and gate thresholds. Run the skeptic pass on the travel model. The specific risks to check: greedy-per-cost near-optimality (budgeted adaptive submodularity), novelty vs informative path planning, and the need for a cost-aware greedy baseline and an online rollout baseline. Verify ≥ 3 new references on budgeted / non-myopic informative path planning and cost-aware BED before citing them. |
| 10-31 → 11-02 | 8.5 / 9 | Theoretical note: an informal argument for why look-ahead headroom → 0 at κ = 0 with precise contacts, and when it is > 0 under travel. Update `docs/08_experiment_plan.yaml`: κ grid, τ, cost-aware greedy, rollout planner, goal-oriented objective, reduced claim set, compute re-estimate (target ≤ 70 CPU-h; drop H4/H5′ from the extended abstract). |
| 11-02 → 11-08 | 10 | Code: travel / time-budget environment (vectorized numpy, κ = 0 path unit-tested to reproduce v1 outputs bit-for-bit). Goal-oriented sPCE rewards. Cost-aware greedy. Rollout planner. Fixed estimator (G1). Exact grid notch. PF kernel or N_eval (G4). |
| 11-08 → 11-12 | 11–12 | Run G0–G5 in order and write the v2 manipulation-check report. **Gate decision on 2026-11-12:** idea 2 in, or fallback. |
| 11-12 → 11-22 | 13 | Main runs: H1a′/H1b′ (both sets, κ ∈ {0, κ_hi}); if G2 passed, H2a′/H2b′ (κ grid, 6 seeds per objective per A1/D2); component ablations (myopic, NC-input, objective, L). |
| 11-22 → 11-26 | 14–15 | Analysis, then the next decision. |
| 11-26 → 12-03 | 16+ | Extended-abstract draft. The full paper adds H4 MuJoCo transfer, a second loop, and more κ levels by 2027-04-01. |

**Not to be done:**
- Redesigning S and re-running the v1 bank check.
- Claiming "greedy is near-optimal" from the v1 estimator.
- Starting any main run before G0–G4 pass.
