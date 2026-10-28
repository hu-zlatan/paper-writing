# Stage 8 v3 · Pass 2: Skeptic (fresh subagent, 2026-10-28)

> System: "You are a senior scientific skeptic. Your job is to find ways each proposed hypothesis could be
> UNFALSIFIABLE, vague, or trivially true. You are intentionally harsh — the goal is to make every hypothesis precise."
> Task (verbatim template): "For each hypothesis below, identify: precision of prediction; quantitative failure
> condition; competing mechanisms and the distinguishing measurement; trivial truth. Output markdown: per-hypothesis
> critique, then a verdict (KEEP / REVISE / REJECT). Hypotheses: {proposer_output}"
> `{proposer_output}` = `docs/07a_proposer_v3.md` (read in full).
> Premises checked against `results/v2/14_analysis.md`, `results/v2/15_decision.md`, `docs/07_hypotheses_v2.md` §1.7.
> Novelty checked by web search (§6). Nothing was run.

---

## 0. Premise check (numbers the hypotheses rely on)

| Proposer statement | Source check | Status |
|---|---|---|
| G1 notch relative gap 0.829 in [0.573, 0.860] | 14_analysis l.28 | Correct. One of 5 runs (0.8629) is outside the band. |
| G(12) = 0.0146 (UB 0.0208), G(0) = 0.0049 (UB 0.0071) | 14_analysis l.30, l.73–76 | Correct. **G is relative** (absolute 0.039 / remaining 2.68 nats). H3a's thresholds (0.05, 0.03) are therefore relative units. The proposer never says so in H3. |
| RL S12 0.204 vs G\* 0.410 (500 ep); 0.243 after 2× | 14_analysis l.33–34 | Correct. |
| Relative head 0.305 vs 0.440, Δ −13.5 pp [−21.0, −6.5], 3.0 vs 4.175 probes | 15_decision l.222–232 | Correct, but **one seed, 200 episodes, G\* 0.440 from a different episode set than 0.410**. 14_analysis l.328 forbids mixing these. The proposer correctly calls it exploratory. |
| "Look-ahead differs from G\* on 41–58 %, near-ties" | 14_analysis l.178, AC row 3 (l.442) | The audit row explicitly says the record **does not separate near-ties from argmax-selection noise** (21 % positive gaps at exact-zero beliefs). The proposer cites the caveat and then uses near-ties as the rationale for H1. It is a hypothesis, not a fact. |
| G\* median 0.840 s / decision on 32 × 8; policy ≈ 0.53 ms | 15_decision l.243–244 | Correct, but both informal. The 0.53 ms was on 256 actions; 1.7 s on 512 is an extrapolation. The split of 0.840 s between PF assimilation and candidate scoring is unmeasured (the proposer admits this for H1-fb only; it also matters for H1b, see below). |
| Estimator under-reads V_greedy (0.597), so G is conservative | 14_analysis l.225–226 | Measured on **one constructed notch**. Transfer of the bias sign to real beliefs is assumed, not shown. |
| D_c = success(G\*) − success(random), D(S12) = 0.300 → δ = 4 pp | 07_hyp_v2 §1.7, 15_decision l.191 | Correct. Note D_c is against **random**, the only reference policy. There is no heuristic baseline anywhere in the set. |

---

## 1. H1: distilled student non-inferior to G\* and ≥ 100× cheaper

### 1.1 Precision
- **H1a is precise** (one-sided LB vs frozen δ_c, ε_c, per informative cell, 4/5 seeds). Good.
- **H1b is not well defined.**
  - R_b is "the most expensive rung whose median latency ≤ 100 × the student's". Student ≈ 0.53 ms → R_b must run in
    ≤ 53 ms. The ladder only varies candidate count (R0 = 512 → R7 = 32). If PF assimilation with N = 2,000 alone
    exceeds 53 ms, **no rung qualifies** and H1b has no test. The proposer gives no rule for this case. Required: state
    that an empty R_b set counts as H1b pass ("no greedy configuration on the ladder reaches 100× cost") **or** extend
    the ladder (see 1.3), and say which, now.
  - The ladder varies only C. The cost of G\* is ∝ N × C × M. A ladder that never reduces N (particles) or M
    (outcome samples) is a strawman for "cheap greedy". Required: a 2-D ladder over (N, C) or (N, M), e.g.
    N ∈ {2000, 500, 125}, M ∈ {64, 16}, C ∈ {512, 128, 32}, with the Pareto front of greedy configurations as the
    comparator.
  - "Per decision" latency for the student hides the fact that **the final identity + pose estimate still needs a
    belief** (success is scored on an estimate). If the PF is run anyway (online or once at the end), the honest
    unit is **episode wall-clock including estimation**. Required: report both per-decision and per-episode latency,
    and state which one carries the "≥ 100×" claim.
  - "One pinned core" for both. If G\* is not vectorised the same way as the network (batched NumPy/BLAS vs
    per-candidate Python loops), the 1,000× ratio is partly an implementation artefact. Required: a profiled G\*
    statement (fraction of time in vectorised kernels) or a GPU/vectorised G\* row.
- **H1c is ill-posed.**
  - "Episodes where the student disagrees with G\*'s **first** action": if the prior belief is identical across
    episodes and the student is deterministic given the history, first-action agreement is constant across episodes
    (all agree or all disagree) and the comparison is empty. If episodes differ (initial finger pose), the split is
    a selection on belief type, so the success difference is confounded. Use per-decision regret vs. per-episode
    BI loss (regression), not a first-action split.
  - R̄'s denominator max − median s(a) → 0 exactly at near-ties, the regime the rationale cares about. R̄ is then
    unstable or infinite. Required: a floor (e.g. denominator ≥ 0.05 · max s, or drop beliefs below it and report
    the fraction dropped), fixed now.
  - "R̄ ≤ 0.25" has no justification relative to success. Descriptive is fine, but say so and drop the threshold, or
    calibrate it on G\*-ladder rungs (what R̄ does R3 have?).

### 1.2 Failure conditions
- (a)–(d) are quantitative. Good.
- **(d) conflicts with 07_hyp_v2 §1.7**, which already says a non-informative cell is decided on BI alone. H1 (d)
  says "fewer than 2 of 3 informative → inconclusive on success, decided on BI". Make the two rules one rule.
- **D3 gate is looser than the test.** D3 passes at seed-mean success ≥ G\* − 5 pp (point estimate, 500 episodes,
  3 seeds). The test requires one-sided LB > −4 pp. A student at −4.9 pp passes D3 and then fails H1a almost surely.
  The gate wastes the 125 CPU-h main budget on a predictable failure. Required: D3 at **≥ G\* − 2 pp point** (or the
  test's own LB rule at n = 500), and BI ≥ G\* − 0.15 nats.
- Pilot G\* at S12 varies by 16.5 pp between the first 200 and last 100 pilot episodes (14_analysis AC row 8).
  δ_c and the informative-cell rule rest on ≤ 300 pilot episodes. Freeze n_pilot ≥ 500 for the v3 pilot, or the
  margin itself is noise.

### 1.3 Competing mechanisms for a "pass"
A non-inferiority pass at δ = 4 pp can be produced by at least four different things:

| Mechanism | What it means | Distinguishing measurement |
|---|---|---|
| (i) The student has learned G\*'s decision rule | Intended | Per-decision regret R̄ on **held-out beliefs** low; DAgger > BC ablation |
| (ii) The task is flat: many action sequences are near-equivalent, so any reasonable policy is within 4 pp | Trivial pass | **A non-random heuristic baseline** (e.g. fixed scripted sweep of φ, or travel-nearest unprobed φ with fixed ψ) evaluated with the same NI rule. If the heuristic is also non-inferior, H1 says nothing about learning. D_c is only measured against random; that is not enough. |
| (iii) The student memorises the training object set / pose distribution | Overfitting interpolation | Held-out objects or a shifted pose prior. Without it "amortized" means "lookup table for the test distribution it was trained on". |
| (iv) Success saturates at n\* probes (both reach the same ceiling/floor) | Degenerate | §1.7 handles ceiling/floor; also report the full success-vs-probe-count curve, not only at n\*. |

Mechanism (ii) is the most serious. The rationale argues that near-ties make NI easy. That same argument predicts
that a cheap heuristic is also NI. **Add a heuristic-baseline row with a pre-registered prediction: the heuristic is
NOT non-inferior (LB ≤ −δ_c) in at least 2 informative cells.** If it is non-inferior, H1's contribution reduces to
latency only, and the "learning" claim must be dropped. That is the single most important revision.

### 1.4 Trivially true?
Partly. "A network that imitates an algorithm runs faster than the algorithm" is true by construction. H1b's
latency half is trivial **unless** it is stated at matched accuracy against the best cheap greedy Pareto front
(see 1.1) and per episode. H1a is not trivial given v2 (RL fell 13–21 pp short), but it is trivial if (ii) holds.

### 1.5 Verdict: **REVISE**
Required changes: (1) heuristic-baseline row with its own pre-registered prediction; (2) H1b with a (N, C, M) greedy
ladder, a rule for an empty R_b, and per-episode latency including the final estimate; (3) D3 tightened to the test
rule; (4) R̄ denominator floor; (5) H1c's first-action split replaced; (6) a held-out object/pose condition, at
least as a reported row; (7) one rule for informative cells shared with §1.7.

---

## 2. H1-fb: student-pruned greedy (k = 16)

### 2.1 Precision and failure
- Prediction and failure are quantitative (NI by H1a rules; latency ratio ≥ 10×). Good.
- The proposer's own honest limit makes H1-fb **likely to fail by construction**: if PF assimilation is ≥ 10 % of
  0.840 s, the 10× target is unreachable regardless of pruning. Measure the split (gate Lat′) **before** the
  hypothesis is registered, and drop H1-fb now if scoring is < 90 % of the cost. A hypothesis whose outcome is fixed
  by an unmeasured profiler number is not a scientific test.

### 2.2 Competing mechanisms
- Near-ties again: **random-16** or **travel-nearest-16** pruning may also be non-inferior. Without these controls a
  pass says nothing about the student. The ladder rung R5 (C = 128) / R7 (C = 32) is a random-subset control only if
  the rung's subset is random; say so. Required: random-k (k = 16) row and a pre-registered prediction that it is
  not non-inferior, or the claim is "pruning works", not "learned pruning works".
- Step-DAD (in the cards) and Choudhury et al. are close precedents for proposal + online refinement; novelty is
  thin (see §6).

### 2.3 Verdict: **REVISE** (add random-k control; register only after the PF/scoring split is known)

---

## 3. H2: RL failure is optimisation, not representation

### 3.1 Precision
- H2a (LB > +5 pp in both cells) is precise.
- **H2 is largely implied by H1.** v2 has RL 13.5–20.6 pp below G\*. If H1a passes (student ≥ G\* − 4 pp), H2a
  (student − RL > +5 pp) follows unless the retrained 512-action RL closes ~10 pp on its own. H2 adds information
  only in the branch where H1 fails. State it as a contrast whose **informative outcome is the RL retrain**, or merge
  it into H1 as a row.
- H2b's ratio [student − RL] / [G\* − RL] is unstable when the denominator is small (if the v3 RL row improves). Add a
  rule: H2b is reported only if LB(G\* − RL) > δ_c.

### 3.2 Asymmetric inference (the main defect)
- Pass branch: "the architecture can represent the policy, so RL failed for optimisation reasons." Valid only as an
  existence proof, and nearly definitional.
- Fail branch: "the encoder, not the optimiser, is the limiting factor." **Not supported.** A failing DAgger student
  can fail because of too little data (1,500 + 800 rollouts), a mismatched loss (soft-target temperature β), or
  covariate shift that two DAgger rounds do not fix. None of these is "representation".
- Required distinguishing measurements:
  1. **Capacity check:** training-set regret R̄_train and top-1 on labelled beliefs. If the student cannot fit its own
     training labels, it is representation; if it fits train but not validation, it is data/generalisation.
  2. **Privileged-input control:** same head, input = PF belief summary (e.g. particle-weighted features) instead of
     the DeepSets history. If the belief-input student succeeds and the history student fails, the encoder is named.
     Without this row the fail-branch sentence cannot be written.
- "Optimisation" lumps credit assignment, exploration and objective saturation. Also a fourth cause the proposer does
  not list: **objective mismatch** (RL optimises ball-sPCE return; G\* optimises EIG_B/c greedily; success is a
  third quantity). Distinguishing measurement: evaluate the **student under RL's own objective** (sPCE-total). If
  student sPCE > RL sPCE, RL is under-optimising its own objective (optimisation failure). If not, RL optimises
  sPCE fine and sPCE is the wrong target (objective failure). The notch already hints at optimisation failure
  (RL 0.172 vs exact 0.615 on its own objective) — say so and replicate on S12.
- Compute: the student uses G\* labels at 0.84–1.7 s per decision. H2's comparison is not compute-matched. Reporting
  CPU-h is fine, but then the claim must be "with dense labels", not "RL fails".

### 3.3 Failure conditions
- Quantitative (LB ≤ +5 pp). "Not testable if RL fails to plateau" is acceptable but must have a numeric plateau rule
  in the text (cite v2 §2.1 rule explicitly).

### 3.4 Verdict: **REVISE**
Keep the pass-branch statement; delete or condition the fail-branch statement on the capacity check and the
privileged-input row; add the student-under-sPCE measurement to separate optimisation from objective mismatch.

---

## 4. H3: small look-ahead headroom over G\* on 64 × 8

### 4.1 Precision
- H3a thresholds are numeric, but **units are unstated** (G is relative to remaining value; say so).
- **Overlapping outcome regions.** "Kill: G ≥ 0.10 **or** LB95 > 0.05" and "Inconclusive: UB95 ≥ 0.05 with
  LB95 ≤ 0.05" overlap when G ≥ 0.10 and LB ≤ 0.05. Give precedence (kill first) or partition on LB/UB only.
- κ = 2 is measured but has no prediction. Either predict (e.g. monotone ordering G(0) ≤ G(2) ≤ G(12), as v2 did) or
  label it descriptive.
- "H3 never blocks H1" is fine, but the outcome map (§4) makes H3 decide the *title* ("near-optimal"). So H3 is
  load-bearing for the headline and must be stated with the scope below.

### 4.2 What H3 actually measures (vague claim)
- The estimator is a **one-step rollout improvement over greedy** (look-ahead with greedy base policy, 100 beliefs).
  A small G bounds what *rollout* gains, not what an optimal or deeper planner gains. The proposer's §0 phrase
  "close to the rollout-improvable optimum" is correct; the outcome-map phrase "**near-optimal** touch selection" is
  not. Required wording: "one-step rollout over G\* gains ≤ X % of remaining ball information". "Near-optimal" may not
  appear in the title.
- The instrument's sensitivity was shown on **one constructed trap** (notch). The under-read bias (0.597) that
  "makes G conservative" is a notch number; its sign on real beliefs is assumed. Distinguishing measurement: a second
  constructed instance with a known gap of a different structure (e.g. travel-trap: informative far action vs.
  cheap near action), or exact DP on a down-scaled S instance (few objects, coarse pose grid) where V_opt is
  computable, to check G's sign and scale on non-notch beliefs.
- G is in **BI nats**, not success. 0.039 nats of BI may or may not be pp of success. Report the rollout policy's
  success on a small paired episode set, or state that H3 makes no success claim.

### 4.3 Trivially true?
Close to it. v2 measured UB 0.0208 on 32 × 8; the prediction is UB < 0.05 on 64 × 8. Halving φ spacing can add cheap
set-up moves, but a 2.4× jump in the UB is needed to fail. This is a **replication with a generous margin**, low risk,
low information. Acceptable as a supporting characterisation, not as a headline. Tighten to the v2 value plus a
stated tolerance (e.g. UB95(G(12)) < 0.03) if the authors want it to carry "greedy is enough".

### 4.4 Verdict: **REVISE** (units; partition of outcomes; κ = 2 prediction; ban "near-optimal"; second instrument check)

---

## 5. Outcome map and the package

### 5.1 Outcome map
- Rows 1–4 are pre-written, which is good. But row 1's title "Near-optimal touch selection in one forward pass"
  overstates H3 (rollout bound, not optimum) and H1b (per-decision, not per-episode). Rename to e.g. "Amortizing
  cost-aware information-gain touch selection".
- Missing row: **H1 passes and the heuristic baseline is also non-inferior** (§1.3 (ii)). Pre-write it: "the task is
  flat at this budget; the contribution is the measurement (H3) and the evaluator finding, not the policy".
- Row 4 relies on "SMC under-reads BI by 0.063–0.177 nats" as a finding; that is a methods note, not an RSS result.

### 5.2 Is the set a publishable RSS contribution, or trivially true as a package?
As written, the core of the package reads as **"a network trained to imitate greedy EIG matches greedy and is
faster"**. That is expected by construction and has direct precedents (§6): Choudhury et al. (RSS 2017) imitate an
information-gathering oracle with near-optimality guarantees under adaptive submodularity; Nguyen, Sarkar & Garnett
(arXiv:2405.15031) distil an expensive nonmyopic active-search policy with DAgger and report competitive performance
at a fraction of the cost. Swapping the domain to tactile localisation is not, on its own, an RSS contribution.
The set is simulation-only, with G\* success ≈ 0.41 at S12, no hardware and no held-out objects.

What would make it non-trivial (any two of these, pre-registered):
1. **A heuristic baseline that fails NI while the student passes.** This shows the task needs belief-aware
   selection, so amortization learns something non-trivial.
2. **Generalisation:** held-out object shapes or pose priors, with a quantitative degradation bound vs G\* re-run
   online on those objects. Amortization's value is reuse beyond the training distribution.
3. **End-to-end, Pareto-honest latency:** student vs the best (N, C, M) greedy front, per episode including the
   final estimate. Show a region of the Pareto plot where greedy cannot reach the student's accuracy at its cost.
4. **A mechanism result for H2** that survives the capacity and privileged-input controls (e.g. "RL under-optimises
   its own sPCE objective by X nats; the same encoder, supervised, reaches it"). This is the most RSS-relevant
   scientific claim in the set, because "why not just RL?" is a standing question for active perception.
5. **One physical demonstration** (even a small one) where 0.84–1.7 s per decision is a real bottleneck relative to
   probe execution time. Without it, a reviewer will ask why 1 s of compute matters when a probe takes seconds.
6. **H3 with a ground-truth check** (exact DP on a down-scaled instance) so "greedy is enough under travel cost"
   becomes a validated characterisation, which the touch literature lacks.

Without (1) and at least one of (2)–(5), the package is a solid workshop paper / RA-L candidate, not an RSS main
contribution.

---

## 6. Novelty threats (verified identifiers only)

| Work | Identifier | Overlap | Effect on claims |
|---|---|---|---|
| Choudhury, Kapoor, Ranade, Scherer, Dey, "Adaptive Information Gathering via Imitation Learning", RSS 2017 | DOI 10.15607/RSS.2017.XIII.041; arXiv:1705.07834 | Imitates a clairvoyant oracle for informative sensing; shows equivalence to posterior-sampling oracle and near-optimality under adaptive submodularity; learned policies are cheap to evaluate. | **Verified (proceedings page).** H1's "amortize information gathering by imitation" is not new. Novelty must rest on: touch with joint identity × SE(2) belief and travel cost; teacher quality *measured* (H3); latency at matched accuracy against a Pareto greedy front; H2 mechanism. Cite. |
| "Learning to Gather Information via Imitation" (Choudhury et al., ICRA 2017) | arXiv:1611.04180 | Earlier version of the above. | Title/ID seen in search results only; abstract not fetched here. Verify before citing. |
| Nguyen, Sarkar, Garnett, "Amortized nonmyopic active search via deep imitation learning" | arXiv:2405.15031 (venue not confirmed here) | DAgger distillation of an expensive nonmyopic expert (ENS); competitive with the expert at a fraction of the cost. | Closest methodological precedent for H1 (DAgger + amortization + speed-up). Strengthens the "trivial as a package" concern. Cite. |
| Ross, Gordon, Bagnell, DAgger, AISTATS 2011 | (not re-verified here) | Method used. | Proposer must verify the citation as planned. |
| Tremblay, Meger, Hogan, Dudek, "Learning active tactile perception through belief-space control" | arXiv:2312.00215 (no venue on arXiv page) | Learned world model + differentiable filter + information-gathering MPC for tactile property estimation. | Not distillation; not pose. Related work for "learned active tactile". |
| Gordon, Baraki, Bui, Posa, "Active Tactile Exploration for Rigid Body Pose and Shape Estimation" | arXiv:2510.13595 | EIG-driven touch selection for pose + shape, real robot; no per-decision compute or travel cost reported. | Supports the proposer's gap claim (no per-decision compute reported in tactile EIG work). Must be cited as current tactile EIG baseline. |

Not found in this search: a paper that distils greedy EIG specifically for tactile localisation. The search was
limited (standard web search, a handful of queries); stage 8 should run one more targeted search before the novelty
paragraph is written.

---

## 7. Verdicts

| Hypothesis | Verdict | Most serious problem |
|---|---|---|
| H1 (a, b, c) | **REVISE** | No heuristic baseline: near-ties that make NI plausible also make any sensible heuristic NI. H1b's ladder varies only C; R_b may be empty; per-decision latency ignores the PF still needed for the final estimate. D3 looser than test. |
| H1-fb | **REVISE** | Outcome decided by an unmeasured profiler split; no random-k control. |
| H2 | **REVISE** | Fail branch ("encoder is the bottleneck") does not follow; pass branch largely implied by H1. Needs capacity check, privileged-input row, and student-under-sPCE to separate optimisation from objective mismatch. |
| H3 | **REVISE** | Low-risk replication (needs a 2.4× rise to fail); measures rollout headroom in BI nats, not optimality or success; overlapping kill/inconclusive regions; "near-optimal" wording not licensed. |
| Package | Workshop/RA-L as is | "Imitating greedy is faster than greedy" has precedents (RSS 2017 DOI 10.15607/RSS.2017.XIII.041; arXiv:2405.15031). Needs heuristic-fails control + generalisation or Pareto-honest latency or a validated H2 mechanism. |

No hypothesis is rejected outright; none is ready to pre-register unchanged.
