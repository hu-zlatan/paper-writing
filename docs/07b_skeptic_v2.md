# Stage 8 v2 · Pass 2 — Skeptic (fresh opus subagent, 2026-10-28)

> System: "You are a senior scientific skeptic. Your job is to find ways each proposed hypothesis could be
> UNFALSIFIABLE, vague, or trivially true. You are intentionally harsh — the goal is to make every hypothesis precise."
> Task: "For each hypothesis below, identify: precision of the prediction; quantitative failure condition; whether
> several mechanisms could 'confirm' it (and what measurement separates them); whether it is trivially true. Output
> markdown: per-hypothesis critique, then a verdict (KEEP / REVISE / REJECT)."
> `{proposer_output}` = full content of `docs/07a_proposer_v2.md`. I read only that file. Where I say something is
> "not defined", I mean it is not defined *in 07a*. If it is defined elsewhere (15_decision, 07c amendment), 07a should
> cite the exact section, because the hypothesis has to stand on its own when it is pre-registered.

---

## Cross-cutting problems (affect both H1 and H2)

**X1. "κ = 0 is the v1 model, bit-identical" contradicts the v2 action model.** v1 evaluated at T = 3 probes. v2 at
κ = 0 has a time budget τ that fits **8–10 probes**, plus a stroke_time cost and a remaining-time input. So κ = 0 has a
different horizon, a different policy input and a different stopping rule. A bit-identical unit test can only hold if
τ at κ = 0 is set to exactly 3 probes. That conflicts with the "≈ 8–10 probes" pilot target. The consequences:
- The H2 negative control and the H1 κ = 0 cells are **not** the v1 setting. v1's "no look-ahead gap" evidence does
  not carry over automatically.
- With 8–10 probes on set A, where greedy already beats random by +64 pp at T = 3, success is likely to **saturate
  near 100 %**. Non-inferiority (H1a) and equivalence (H2 TOST) then pass trivially through a ceiling effect.
- **Fix:** state τ at each κ in the pre-registration. Either keep the probe budget fixed across κ (adjust τ so that
  the *same* number of probes would fit if there were no travel), or add a κ × τ factorial (see H2, problem 1).
  Rename the unit test to "κ = 0 **and** τ = 3 probes reproduces v1".

**X2. "Success" and "ball information" are not defined in 07a.** Is success MAP-in-ball, posterior mass in the ball
≥ some threshold, or a 0/1 outcome after a terminal grasp? What is the ball radius in (x, y, θ), and does identity have
to match? Every threshold below (−4 pp, 3 pp, ±3 pp) is meaningless until this is fixed. **Fix:** define both
metrics inline, with numeric radii and the exact posterior estimator (evaluation PF at the G4 size).

**X3. Ceiling and floor checks are missing.** No cell has a pre-registered requirement that it be non-degenerate.
At κ_hi with 2–3 probes, every method might sit near the floor. At κ = 0 with 8–10 probes, every method might sit
near the ceiling. **Fix:** a cell counts toward H1/H2 only if G*'s success is in [15 %, 90 %] and the random-to-G*
gap is ≥ 15 pp. Otherwise, re-tune τ before test (pre-registered), or report the cell as non-informative instead
of as a pass.

**X4. Action-space resolution is not matched.** Greedy picks from C = 64 candidates. The policy's output head is not
specified (continuous (Δφ, ψ)? discretised?). At κ = 0 a 1-D ψ grid of 64 is fine. At κ > 0 the action space is 2-D
(Δφ × ψ), and 64 candidates is an 8 × 8 grid. A continuous policy then gets an advantage from finer resolution,
not from amortization (H1) or look-ahead (H2). **Fix:** the policy chooses from the same candidate set as greedy, or
greedy's C is raised until its success is flat in C (pre-registered check, e.g. C = 256 changes success by < 1 pp).

**X5. Greedy's objective must match the policy's.** 07a says the training reward is ball-sPCE. It does not say whether
greedy PF-EIG / cost-aware greedy maximise **ball** EIG or **full-state** EIG. If greedy maximises full-state EIG
(as in v1, where fine pose dominates: 3.07 vs 0.92 nats), then any sPCE-total advantage on ball metrics can be
explained by the objective mismatch alone. **Fix:** both greedy variants maximise ball EIG (or EIG/c) for the primary
contrasts. Full-state greedy is an extra row.

---

## H1 — Amortized goal-oriented sPCE is non-inferior to G* and ≥ 100× cheaper at matched accuracy

### Is the prediction precise enough for one experiment?
Mostly. Cells, comparator, margin, CI type and seed rule are all stated. What is still vague:
- **Success / ball information** are not defined (X2).
- **Ball-information ratio lower bound > 0.95.** The ratio's CI method is not given (ratio of means? mean of ratios?
  Fieller / bootstrap?). It is also unstable if the denominator can be near 0 at the κ_hi floor. **Fix:** use a
  difference with a margin in nats, or pre-specify a bootstrap of the ratio of means and require G*'s mean ball
  information ≥ some value (in nats) for the ratio to be computed.
- **H1b latency measurement scope.** Does greedy's per-decision latency include the PF update (resample-move) after each
  observation? Greedy cannot act without a belief. The policy is belief-free and needs no PF. Including the PF update
  inflates the ratio, excluding it understates the real cost. Either choice has to be stated. Also needed: hardware,
  framework (PyTorch eager vs TorchScript vs NumPy), warm-up, number of timed calls, and whether thread count is pinned
  to 1.
- **"Searched on a pre-registered grid"**: the grid itself (values of N, C, outcome samples) is not given. Risk 5 in 07a
  admits this.

### Is the failure condition quantitative?
Yes for (a), (c), (d). (b) is quantitative but depends on G*_match, which is badly defined (next point).

### The matched-accuracy definition favours the policy (serious)
G*_match is matched to **full-size greedy** (within 1 pp). But H1a allows the policy to be up to **4 pp worse** than
full-size greedy. The fair latency comparison at *matched accuracy* uses the cheapest greedy that **matches the policy's
accuracy**, not greedy's own. If the policy is 3 pp below G*, then a greedy shrunk to "G* − 3 pp" is a legitimate
comparator, and it may be far cheaper than G*_match. As written, H1b can be confirmed by under-performing.
Second, "within 1 pp" on validation episodes is below the Monte Carlo resolution. With 1,000 episodes the SE of a
success rate near 70 % is ≈ 1.4 pp, so "within 1 pp" picks a configuration largely at random.
**Fix:** G*_match = the smallest grid configuration whose success has a one-sided 95 % lower bound ≥ success(sPCE-total)
− 1 pp (state the number of validation episodes, ≥ 2,000, paired). Report both "matched to policy" and "matched to
full greedy". The ≥ 100× threshold applies to the former.

### Could several mechanisms "confirm" it?
- **Ceiling (X1, X3):** non-inferiority is automatic if both methods are near 100 % (or near 0 %). *Distinguish:* the
  non-degeneracy rule in X3, and a margin stated as a **fraction of the random-to-G* gap** (e.g. sPCE-total closes
  ≥ 85 % of the gap, lower bound) instead of a flat −4 pp. A flat 4 pp is 6 % of a 64 pp gap on A but 14 % of a 29 pp
  gap on S. That is not the same claim on both sets.
- **Resolution advantage (X4)** at κ_hi.
- **Objective mismatch (X5)**: a policy trained on ball-sPCE vs a greedy on full-state EIG.
- **Latency from implementation rather than amortization:** a Python-loop greedy against a fused forward pass. This is
  not wrong, but "≥ 100×" then measures code quality. *Distinguish:* also report a FLOP / multiply-add count per decision
  for both, as an implementation-independent ratio. Use a vectorised greedy (batched over particles × candidates ×
  outcomes) as the timed comparator.

### Trivially true?
- **H1a "beats random and coverage by ≥ 10 pp":** effectively trivial. Greedy beats random by 64 / 29 pp, and any
  policy that is non-inferior to greedy must beat random by about that much. This is a sanity check, not a hypothesis.
  Keep it as a reported check and remove it from the failure conditions. Otherwise it only adds 8 tests to the Holm
  family.
- **H1b at full size:** 0.65 s vs ≈ 3·10⁴ multiply-adds is a 10³–10⁴× gap almost by construction. 07a already reports
  it without a threshold, which is correct. Only the matched-accuracy version is non-trivial, and only once it is fixed
  as above.
- **Seed robustness "point estimate > −4 pp in ≥ 5 of 6 seeds":** loose. With ≈ 1,000 episodes per seed the per-seed SE
  is ≈ 2 pp. A policy that is 2 pp worse on average passes most seeds. Acceptable as a secondary rule, but report the
  per-seed lower bounds as well.

### Escape clause
"If H1 fails only at κ_hi … partial result." This is pre-registered, so it is acceptable. But the title and abstract
must then drop "cost-aware". State now that a κ_hi-only failure **is** a failure of H1 as titled.

### Verdict H1: **REVISE**
Required: (1) G*_match matched to the policy's accuracy with a CI-based rule and a stated validation N; (2) margin as a
fraction of the random-to-G* gap plus a non-degeneracy rule per cell; (3) define success / ball information and the
latency measurement scope (PF update in or out, hardware, threads); (4) greedy maximises ball EIG; (5) resolution-matched
action sets; (6) move "beats random/coverage" to sanity checks.

---

## H2 — Under travel/time budget, non-myopic sPCE beats the strongest myopic selector; Δ grows with κ, vanishes at κ = 0

### Is the prediction precise enough for one experiment?
The contrast structure (H2a point + LB, slope, TOST) is precise. What is vague:
- **G in gate G2 has no unit.** "G(κ_hi) ≥ 0.10" — nats of ball information? Success probability? Under which policy
  pair (exact/rollout optimum vs cost-aware greedy)? 0.10 nats and 0.10 success are very different bars.
- **κ_mid / κ_hi are defined through probe counts ("≈ 8–10 / 4–6 / 2–3"), not values.** "≈" is not a rule. The one
  "pre-registered κ_hi escalation" has no trigger and no target value. **Fix:** give the pilot's exact rule (e.g. κ such
  that cost-aware greedy's median executed probes = 9 / 5 / 2.5, measured on 200 pilot episodes) and the escalation
  value (e.g. "κ_hi ← 2·κ_hi, once, only if G2 fails on the size of G(κ_hi) and not on monotonicity").
- **H2b P1 "remaining-budget value under the G1-validated estimator"** is not defined in 07a (value of what? estimated
  how? ball nats from the remaining budget under which continuation policy?).
- **sPCE-myopic's reward under travel.** With γ = 0 and a per-step information reward, the myopic policy has **no
  incentive to economise time at all**, because cost only shows up through the future budget, which γ = 0 discards. So
  "only credit assignment differs" is false: γ = 0 also removes cost-awareness. 07a sees this (hence M*), but the
  ablation is still mislabelled. **Fix:** the myopic ablation uses a rate reward (information gain / c(a), γ = 0), which
  is the learned analogue of cost-aware greedy. Then total vs myopic really differs only in credit assignment.

### Is the failure condition quantitative?
(a), (b), (e) yes. Problems:
- **(c) is nearly impossible to trigger.** It needs TOST to fail **and** Δ(0) > +3 pp. An underpowered TOST with
  Δ(0) = +2.9 pp passes. A strongly **negative** Δ(0) (e.g. −5 pp, which H1 tolerates up to −4 pp) also passes, and it
  even *inflates* the slope in (b). **Fix:** fail if |Δ(0)| > 3 pp **or** TOST fails. State the TOST power: with 6 seeds
  under a crossed bootstrap, the seed variance may make ±3 pp unreachable. Run a pre-registered power calculation from
  v1 variance components.
- **P2 has thresholds but is not in any failure condition.** (d) lists only P1 and P3, so P2 cannot fail H2.
  Either add it or call it exploratory.
- **The gate makes H2 conditionally unfalsifiable (serious).** If G1/G2 fail, "H2 is neither confirmed nor rejected."
  But a failed G2 (validated headroom over cost-aware greedy < 0.10 at κ_hi) **is** direct evidence against Idea 2,
  which is that look-ahead pays when touches cost travel. Calling it "not tested" lets the paper avoid stating a negative
  result about its own second idea. **Fix:** split the outcomes. A G1 failure (estimator broken) means untested. A G2
  failure with a valid estimator means "Idea 2 refuted at this κ range: headroom ≤ X (UB)". State the upper bound as the
  result, using the word "refuted", in the pre-registration.

### Could several mechanisms "confirm" it? (most serious section)
1. **Horizon length, not travel, drives Δ(κ).** κ is tuned so that probe count drops from 8–10 to 2–3. So κ is perfectly
   confounded with **horizon**, and with ceiling/floor position (X1, X3). A Δ that grows with κ could come from "short
   horizons punish greedy's final-step choices" or from "at 8–10 probes everyone saturates (Δ(0) ≈ 0 by ceiling)". The
   dose–response slope then measures saturation, not travel. **Distinguishing measurement:** a κ × τ factorial (at least
   κ = 0 with τ set so that only 2–3 probes fit, i.e. short horizon, no travel). If Δ is ≈ 0 at (κ = 0, short τ) and
   > 0 at (κ_hi, short τ), travel is the cause. If Δ > 0 at both, horizon is the cause. This one extra cell (sPCE-total +
   M* at κ = 0, τ_short; 6 + 6 runs, or 6 runs if greedy is M*) is the most valuable addition to v2.
2. **Budget-feasibility bookkeeping, not look-ahead.** "An action whose cost exceeds the remaining time is not
   executed." If cost-aware greedy can pick an infeasible final action and lose the probe, while the policy (which sees
   remaining time) learns to avoid that, Δ > 0 follows from a trivial terminal effect. **Fix:** greedy restricted to
   feasible actions. Report Δ separately for the last executed step vs earlier steps, and the number of executed probes
   per method (already listed as transparency — make "executed probes differ by < 0.2 on average" a pre-registered
   check).
3. **Objective mismatch (X5)** and **resolution (X4)**: both grow with κ (because the travel dimension only matters
   when κ > 0), so they also produce a positive slope.
4. **Remaining-time input vs γ.** Even with the rate-reward fix, γ = 1 PPO and γ = 0 PPO differ in variance and
   convergence. The κ = 0 TOST does not rule this out, because at κ = 0 the time input carries little information.
   *Distinguish:* report training curves and the plateau epoch per variant. Check that sPCE-myopic(rate) matches
   cost-aware greedy within the H1 margin (it should, if training works). If it does not, the "learned myopic" arm is
   under-trained and the ablation is uninformative.

### Trivially true / tautological parts
- **H2b P1, first half, is true by definition.** Cost-aware greedy is the argmax of EIG/c. Any first action that differs
  from greedy's has lower EIG/c, up to MC noise. Only the second half (higher remaining-budget value) carries content.
  Also, averaging over all 100 beliefs dilutes the effect with beliefs where the two choose the same action. **Fix:**
  report the disagreement rate. Test the value difference on disagreeing beliefs only, and require a minimum
  disagreement rate (e.g. ≥ 20 %) for P1 to count as evidence.
- **H2b P2 thresholds are trivially passable.** "≥ 80 % of the exact optimum" can be *below greedy* if greedy already
  reaches 90 % of the optimum on the notch. "sPCE-myopic ≤ greedy + 10 %" is a ceiling that any weak policy meets.
  **Fix:** express P2 as the fraction of the **gap** closed: (V_total − V_greedy) / (V_opt − V_greedy) ≥ 0.5, and
  require sPCE-myopic to close ≤ 0.2 of the gap. Also state whether the notch control has travel cost. If the notch has
  a gap at κ = 0, it contradicts the H2 premise that no gap exists without travel. Explain why it does not.
- **H2b P3 "fewer direction reversals" is satisfied by any sweeping policy**, including coverage. **Fix:** compare
  against coverage too, and require sPCE-total to have *both* fewer reversals than M* *and* more ball information per
  unit travel than coverage. "Travel per nat" is a ratio with a possibly small denominator. Use a difference at matched
  travel, or ball information per unit time with a bootstrap of the ratio of means.
- **Dose–response slope is mostly implied by H2a + the negative control.** With three κ points, Δ(0) ≈ 0 forced by
  design (and possibly by ceiling) and Δ(κ_hi) > 0 from H2a, an OLS slope > 0 is almost automatic. The κ spacing is set by
  probe counts, not linearly, so the slope's magnitude is not interpretable. **Fix:** replace the slope with an
  ordered-alternative test (Jonckheere or isotonic LR), and make the middle point carry weight: require
  Δ(κ_mid) lower bound > Δ(0) upper bound − 1 pp, or drop the dose–response claim and keep "present at κ_hi, absent at
  κ = 0 under matched horizon" (problem 1).

### Novelty / literature
The rationale's "greedy is weak in orienteering / budgeted IPP" and 07a's risk 1 ("cost-benefit greedy has
constant-factor guarantees under budgeted adaptive submodularity") pull in opposite directions. The second point is a
theoretical reason to *expect* G2 to fail, and it also means a constant-factor guarantee leaves room for a gap of a
few pp. **Fix:** before stage 9, verify ≥ 3 IPP / cost-aware BED / budgeted adaptive-submodularity references.
Pre-register what size of gap those results allow, so that a "3 pp at κ_hi" result can be placed against theory.

### Verdict H2: **REVISE**
Required: (1) de-confound κ from horizon (κ × τ cell at κ = 0, short τ), with the non-degeneracy rule; (2) units and
exact rules for G2, the κ pilot and the escalation; (3) reclassify a G2 failure with a valid estimator as a
**refutation** of Idea 2, not "untested"; (4) rate-reward myopic ablation, feasibility-restricted ball-EIG greedy,
matched action resolution; (5) tighten (c) to |Δ(0)| > 3 pp or TOST fails, with a power calculation; (6) P1 on
disagreeing beliefs only, P2 as fraction of gap and inside the failure conditions, P3 against coverage; (7) replace the
3-point OLS slope with an ordered-alternative test or drop dose–response.

---

## Summary

| hypothesis | verdict | blocking issue |
|---|---|---|
| H1a non-inferiority | REVISE | flat −4 pp margin plus no ceiling/floor rule → can pass by saturation; metrics undefined |
| H1a beats random/coverage | demote to sanity check | trivially implied by non-inferiority to greedy |
| H1b latency at matched accuracy | REVISE | matched to full greedy, not to the policy's (lower) accuracy; "within 1 pp" below MC resolution; PF-update scope unstated |
| H2a effect + dose–response | REVISE | κ confounded with horizon / saturation; slope nearly implied; negative control (c) almost cannot fail |
| H2b mechanism P1–P3 | REVISE | P1 half-tautological, P2 thresholds trivially met and absent from failure set, P3 met by any sweep |
| H2 gate / fallback | REVISE | G2 failure labelled "untested" instead of "refuted"; G has no unit |

No hypothesis is rejected outright. Both carry a real, falsifiable core, but both currently have at least one path to
"confirmation" that does not depend on the claimed mechanism.
