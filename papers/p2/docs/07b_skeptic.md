# Stage 8 · Pass 2 — Skeptic (fresh opus subagent, 2026-11-08)

> **System (verbatim):** "You are a senior scientific skeptic. Your job is to find ways each proposed hypothesis could be
> UNFALSIFIABLE, vague, or trivially true. You are intentionally harsh — the goal is to make every hypothesis precise."
> **Task (verbatim):** "For each hypothesis below, identify:
> - Is the prediction precise enough that a single experiment could confirm or refute it? If not, what specifically is vague?
> - Is the failure condition stated quantitatively? If not, what threshold is missing?
> - Could the hypothesis be "confirmed" by any of several different mechanisms? If so, what additional measurement would distinguish them?
> - Is the hypothesis trivially true (e.g., "more compute helps")? If so, flag for rejection.
> Output markdown: per-hypothesis critique, then a verdict (KEEP / REVISE / REJECT).
> Hypotheses: {proposer_output}"
> **{proposer_output}** = the full content of `docs/07a_proposer.md`. Context read: `docs/06_synthesis.md`,
> `docs/00_topic_init.md`.

Nothing here is a result. Every number I quote is either from 07a or simple arithmetic on its stated design.

---

## 0. Cross-cutting problems (these apply to several hypotheses)

### X1. The validity evidence is largely circular
- F\* is produced by bisection on the replay. Evaluation then uses the rule **slip ⇔ F < F\*_hi**, applied to those
  same labels. Calibration and test scores are therefore deterministic functions of the same labels. Under an i.i.d.
  split, "slip rate ≤ α" is then **the conformal theorem applied to a column of numbers**. The robot, the simulator and
  the slip physics play no part in it.
- The only non-circular evidence is the **direct-replay audit**: simulate at the chosen F and observe slip. In 07a the
  audit is a side check (2,000 × 4 methods, α and n unspecified) and is not the primary validity endpoint. At α = 0.10
  and 500 audited instances per method, the binomial SE is ≈ 1.3 pp. At α = 0.01 the audit is almost powerless:
  about 5 expected slips.
- Bisection itself assumes monotonicity. On a non-monotone instance it returns a meaningless bracket.
- H1a defines non-monotonicity relative to that bracket ("a force above F\*_hi that slips") and starts its grid at
  0.5·F\*_lo. It therefore cannot see:
  - no-slip islands below F\*_lo (e.g. wedging or tilting at low force);
  - an instance whose bisection path happened to skip a slip region.
- **Fix:** make the direct-replay slip rate, at one pre-registered (α, n) cell per method, the primary validity
  endpoint. Size it by power analysis, e.g. enough instances to detect a slip rate of 1.5α at 80 % power.
  Re-describe the label-based band check as a pipeline unit test.

### X2. The Beta-binomial band assumes i.i.d. instances, but the data are clustered
- Calibration draws n instances from a pool of 600 objects × 5 instances. Instances of one object share geometry,
  μ and mass, so calibration points are exchangeable at the object level, not the instance level.
- The conditional-coverage distribution is then wider than Beta(l, n+1−l), because the effective n is somewhere
  between n/5 and n. The criterion "≤ 8 % of re-draws outside the band" can fail with no defect anywhere.
- Worse, the 200 re-draws come from one fixed pool. At n = 2000 from a 3,000-instance pool, any two draws overlap by
  about 2/3. The re-draws are not independent, so "5 % + binomial tolerance for 200 draws" is mis-derived.
- **Fix:** either calibrate on one instance per object (n ≤ 600 objects) or derive the band for cluster sampling. Use
  disjoint calibration/test object sets per re-draw, or report the effective number of independent re-draws.

### X3. Thresholds without power analysis; no multiplicity plan across hypotheses
- None of the following thresholds is derived from a variance estimate or a minimum detectable effect: 1 %, 3 %,
  8 %, 15 %, 5 %, 10 %, 8/16, 400 steps, 60 slips, 1.5×, 1.5α, 20 %.
- Holm is applied only within H2's 16 conditions. Elsewhere the plan makes many tests with no correction:
  - H1b: 4 α × 3 n × 5 seeds × 4 methods = 240 cells, each judged with "any cell outside the band" as the failure
    rule. At 95 % bands, about 12 cells fail by chance.
  - H2: 4 sub-predictions × 2 α levels.
  - H3: 5 predictions × 3 shifts × 2 α levels.
  - H4: 3 predictions.
- **Fix:**
  - Name **one primary endpoint**: H2.1, pooled relative excess vs the comparator at α = 0.10, n = 2000.
  - Order the rest as a pre-registered fixed sequence: H1a gate → H2.1 → H3.4 → H4 → secondaries.
  - Derive every threshold from the pilot's paired-difference SD (cluster bootstrap, 600 test objects).
  - Use a FWER rule for H1b, e.g. a Bonferroni-widened band, or "≤ k of 240 cells" with k from the binomial.

### X4. Non-inferiority and null predictions are stated as "CI includes 0"
Three predictions are confirmed by a CI containing 0: H2.3 (tail no worse), H3.4 (no difference under S1) and H3's
demotion clause ("within 5 % of frozen"). Low power then confirms them. Each needs an equivalence or non-inferiority
margin with TOST, e.g. "upper 95 % limit of the relative difference < +5 %".

### X5. Simulator artefacts that can produce both "results"
- **Penetration counted as slip.** With MuJoCo soft contacts, normal penetration grows with force. If the
  "object–pad displacement > 2 mm" metric is not restricted to the **tangential** plane, high forces register as
  slip. That creates non-monotonicity (H1a) for artefactual reasons.
- **Collision primitives.** Box–box, capsule and mesh collisions produce different numbers and layouts of contact
  points, and `condim` 3/4/6 decides whether torsional friction exists at all.
  - Rotational slip in F4 (off-centre CoM) is governed almost entirely by `condim` and contact-patch spread, both
    solver settings.
  - A touch_grid on a box-vs-pad contact essentially renders 4–8 contact points. Its "pressure centroid" is then a
    function of the collision routine, so it **identifies the geometry type and family**.
  - Any predictor that recognises the family can beat a one-parameter CSF, whether or not it reads touch in a
    physically meaningful way.
- **Probe "compliance".** For rigid objects, the compliance seen in the probe squeeze is set by `solref`/`solimp`,
  not by the object. If those parameters are global, the probe channel carries only geometry. If they differ by
  geom type, the probe channel is a family identifier.
- **Required diagnostics, pre-registered:**
  - (i) tangential-only displacement in the slip metric;
  - (ii) `condim`, `cone` and `solref`/`solimp` identical across families, stated in the paper;
  - (iii) a probe for "touch identifies family": family classification accuracy from tactile features alone;
  - (iv) a probe for "touch sees friction": R² of log μ regressed on tactile + probe features. H3.4 and H4 rest on
    the premise that this R² is ≈ 0.

### X6. "Just applying conformal prediction": the RSS reviewer's case, which 07a does not yet answer
- **Off-the-shelf methods.** CQR, OQT and ACI are used unchanged. H1b and H3.2 are existing theorems. The one new
  idea, "slip is the miscoverage indicator", is a single sentence in the synthesis. A reviewer will write: *"a
  simulation benchmark of known conformal methods on a label the authors generated themselves, with guarantees that
  are textbook and empirical results in a simulator whose slip physics is unvalidated."*
- **The offline method cannot be deployed as specified.** Calibration needs an F\* per calibration grasp, and on
  hardware F\* cannot be measured: the disturbance is not replayable, and bisection would take ~10 drops per grasp.
  07a never says how offline CertGrip would be calibrated on a robot.
  - Option: calibrate from **one binary outcome per grasp** at a chosen force. That is interval-censored F\* and
    turns the calibration into risk control on 1{slip(F)} from binary data.
  - Otherwise, state plainly that the offline method is a sim-to-real-transfer object and only the online method is
    deployable.
- **Learning from slips means dropping objects.** The online method learns only through slips, so it must drop
  α·T objects plus the transient. Neither the paper nor H3 says what that costs.
- **What the robotics contribution must be.** It has to rest on measurements nobody has made: the monotonicity rate,
  the variance decomposition of log F\* (X7), and what touch buys in newtons at a fixed α. It cannot rest on the
  guarantees.

### X7. The efficiency gain is set by the experimenter's randomisation ranges
- F\* ∝ m(g+a)/μ for translational slip. Var(log F\*) therefore splits into a friction term, a disturbance term,
  and the geometry and CoM terms that touch might explain.
- The friction and disturbance terms are invisible to every method. The friction range ("log-uniform within a
  nominal range") and the disturbance amplitude ranges are **free design choices** that are not yet numbers.
  - A wide μ range makes CSF ≈ CertGrip by construction.
  - A narrow μ range plus a wide CoM offset makes CertGrip win by construction.
- So H2 and H4 measure the design unless the ranges are fixed in advance from external sources and the
  decomposition is reported.
- **Fix:**
  - Pre-register the numeric ranges, citing a source for each.
  - Report an **oracle decomposition**: the residual spread of log F\* after regressing on privileged features
    (μ, disturbance amplitude, CoM offset, geometry), one group at a time.
  - Use it as the ceiling on any achievable gain. CertGrip's gain should be reported as a fraction of that ceiling.

---

## H1a — Monotonicity of slip in force

**Precision.** Good. This is the most genuinely empirical claim in the document. Remaining vagueness:
- **Grid.** 40 log-spaced points over [0.5 F\*_lo, F_max] are dense far from F\* and sparse near it. That catches
  gross ejection but not near-threshold flicker. Add a dense local grid (e.g. 10 points in [F\*_hi, 1.5 F\*_hi]).
- **Missed pattern.** No-slip below F\*_lo is not tested (see X1).
- **Shift pools.** "Within each shift pool" appears in the prediction, but the budget covers only 1,000
  in-distribution instances. Either add about 3 × 250 × 40 replays (≈ 8 CPU-h) or drop the shift-pool clause.
- **Slip metric.** It must be tangential-only (X5), and the pilot must freeze it **before** H1a runs. Otherwise δ_slip
  can be tuned until monotonicity passes.

**Failure threshold.**
- **Overall.** Quantitative, but its power is unstated. At n = 1000 and a true rate of 1 %, the 95 % CI is about
  [0.5 %, 1.8 %]. The test needs a rule for which side of the CI decides, e.g. "upper 95 % limit ≤ 2 %".
- **Per family.** With 250 instances, a 3 % threshold has a CI half-width of about ±2 pp, so the test is weak.

**Alternative mechanisms.** A low non-monotone rate could mean that physics is monotone, or that the slip metric and
episode are too short or too lenient to reveal ejection. Report the distribution of maximum tangential displacement
at F_max.

**Triviality.** Not trivial.

**Verdict: KEEP (minor revisions):** dense local grid, tangential slip metric, CI-based decision rule, and a fix for
the shift-pool budget inconsistency.

---

## H1b — Conformal validity on labels

This is a theorem, not a hypothesis, and 07a admits as much. It is also circular (X1) and uses the wrong band under
clustering (X2). Its failure rule ("any of 240 cells") will trigger by chance (X3).

**Verdict: REJECT as a hypothesis.** Keep it as a pipeline unit test with a FWER-correct rule and a cluster-aware
band. Move the direct-replay audit into H1 proper as the empirical validity claim, with power analysis (X1).

---

## H1c — Uncalibrated targeting misses α

**Triviality.** It is close to trivially true. Gradient-boosted quantile regression at the 1st and 5th percentile
tails, trained on about 6,000 clustered instances, is known to be miscalibrated. A Gaussian tail on a heavy-tailed
log-ratio is too. The prediction is the reason conformal prediction exists, and it confirms nothing about grasping.

**Asymmetric falsification.** The prediction needs only one α in 4 of 5 seeds to miss. The failure condition requires
**both** methods inside the band at **all four** α. The hypothesis is built to pass.

**Direction.**
- The prediction commits to "above the band" (too many slips), but quantile GBTs often **over**-cover in the tail
  because of leaf averaging.
- Either predict a direction and treat the opposite miss as a failure, or predict "outside the band" two-sided and
  test it as such.

**Missing comparator.** The fair "no-conformal" method is RAW-Q with its quantile level tuned on a held-out
validation split. That is what a practitioner would do, and it is almost conformal already. If it lands in the band,
Gap 1 is empty in practice.

**Missing effect size.** "Outside the band" at m = 3000 can be a 1 pp miss. Pre-register a practically relevant
miscalibration, e.g. |slip − α| ≥ 0.5α at α = 0.05.

**Verdict: REVISE (demote to secondary):** two-sided test, a validation-tuned RAW-Q, an effect-size threshold, and a
symmetric failure rule.

---

## H2 — Force efficiency vs the calibrated safety factor (primary)

### Precision
- **Ambiguous primary metric.** "Mean force excess ≥ 15 % lower (relative)" can mean (a) the ratio of mean absolute
  excess E[F−F\*], dominated by heavy objects, or (b) the difference in mean relative excess E[(F−F\*)/F\*],
  dominated by light objects. These can disagree in sign. Pick one.
- **Label quantisation is the same order as the effect.**
  - ε = F_max/1024, or F_max/256 under downscale step 1.
  - With F_max = 40 N, say, ε ≈ 0.04–0.16 N. For a 1 N light-object F\* that is 4–16 % relative error.
  - Using F\*_hi biases the measured excess downward by up to ε for every method. For relative excess the bias
    weighs light objects heavily.
  - Pre-register a minimum F\* (or an ε/F\* bound), and check how the result changes when F\*_lo is used instead
    of F\*_hi.

### Fairness of the comparator (the most serious issue)
1. **"Giving mass to everyone favours the baseline, so the comparison is conservative" is unsupported.**
   - CSF uses mass only through one fixed physics formula with a single global factor.
   - CertGrip uses mass, aperture and touch in a flexible nonlinear regressor that can learn interactions:
     mass × CoM offset, aperture × family, and the systematic error of the F_nom formula (which ignores torque from
     off-centre grasps and uses a_nom for pull and payload disturbances, where it is the wrong model).
   - Privileged mass may help the learner **more** than the formula, so it biases toward CertGrip, not against it.
   - On hardware mass is unknown, so the realistic comparison drops mass from both.
   - **Add a no-mass condition for both methods**, or drop the "conservative" claim.
2. **CSF is a one-parameter strawman relative to available non-tactile information.** A competent engineer would use
   at least:
   - **Mondrian-CSF**, a separate calibrated factor per family × disturbance type: 16 parameters, still no touch,
     still conformal, so still guaranteed;
   - **CertGrip-P**, the learned proprio-plus-mass predictor, conformalised.

   Beating one-parameter CSF shows "conditioning on something helps", which is trivially true once variance differs
   across conditions. The claim the paper wants, "per-grasp **tactile** adaptation buys force", needs
   CertGrip > Mondrian-CSF **and** CertGrip > CertGrip-P. Make the primary comparator **the stronger of
   Mondrian-CSF and CertGrip-P**, chosen on validation data from the train split.
3. **Disturbance information.** The robot knows its own planned lift acceleration and shake, so it is not
   unfair to give that to every method. Whether disturbance type and amplitude are inputs is unspecified. That choice
   changes the irreducible variance (X7). State it.

### Alternative mechanisms for a "confirmed" H2
A pooled gain ≥ 15 % could come from any of four sources:
- (a) touch features that encode contact geometry or CoM offset (the claimed mechanism);
- (b) touch features that act as a family or geom-type identifier through MuJoCo contact-point artefacts (X5);
- (c) the learner correcting the misspecified F_nom formula from mass and aperture alone, with no touch at all;
- (d) label-quantisation bias favouring the method whose forces sit closer to the ε-grid.

To tell them apart:
- **(c):** CertGrip-P vs CSF.
- **(b):** Mondrian-CSF and a family-ID probe.
- **(a):** within-family gains, and the F4-vs-F1 interaction test.
- **(d):** the F\*_lo/F\*_hi sensitivity check.
- **The ceiling (X7):** the oracle variance decomposition.

### Thresholds
- **15 % / 5 %.** Not derived. Pilot the paired SD and state the minimum detectable effect at 600 test objects.
- **"≥ 8 of 16 conditions significant after Holm."** Each condition has about 190 instances (~38 objects). Holm at
  16 needs p < 0.003 for the smallest p-value. Even with a true 15 % effect everywhere, 8/16 may be unreachable, which
  makes this a power artefact rather than a test. Replace it with a random-effects or meta-analytic estimate of the
  per-condition heterogeneity, or drop it.
- **Tail (H2.3).** This needs a non-inferiority margin (X4).
- **Small n (H2.4).** At n = 100 and α = 0.20, the conditional coverage is noisy for both methods. The paired gain
  CI must use the same calibration draw for both, which should be stated.

### Triviality
Against one-parameter CSF with privileged mass, a gain is close to trivial (point 2). Against Mondrian-CSF and
CertGrip-P it is not.

**Verdict: REVISE (major):**
- Make the stronger of Mondrian-CSF and CertGrip-P the primary comparator.
- Add a no-mass condition.
- Fix one primary metric.
- Run the ε sensitivity check.
- Report the oracle variance decomposition with pre-registered μ and disturbance ranges.
- Add a non-inferiority margin for the tail.
- Replace the 8/16 rule.
- Derive thresholds from a pilot power analysis.

---

## H3 — Online slip-rate control under shift

### H3.1: offline breaks under S1/S3 (trivially true by design)
- μ × 0.6 multiplies every translational F\* by 1/0.6 ≈ 1.67, a log shift of 0.51. That is several times the
  calibration quantile margin at α = 0.10, so frozen methods will fail massively. The ≥ 1.5α claim follows from
  Coulomb's law.
- S3 (×1.5 amplitude) is similar.
- The only uncertainty is S2, and that prediction is two-sided with no magnitude: "leaves the band".
- **Fix:**
  - Add a **mild shift** (e.g. μ × 0.9 and amplitude × 1.1) where breakage is genuinely uncertain.
  - Pre-register the predicted magnitude as the slip rate implied by the in-distribution score CDF shifted by the
    known log factor. That is a sharp, falsifiable number.
  - Give S2 a magnitude threshold.

### H3.2: OQT long-run bound (a theorem)
- With **conditioning on outcome**: streams where the cap binds are excluded. Under S1 and S3, F\* rises by
  1.5–1.67×, so cap binding is likely for heavy objects. The tracker then pushes q upward without bound while slips
  continue. Excluding those streams removes exactly the cases where the method fails.
- **The bound may be vacuous.** (B+η)/(ηT) with B ≈ 3 (log-score range), η = 0.05 and T = 2000 gives
  ≈ 0.03 = 0.3α. 07a never states the numeric bound. If it exceeds α, "within the bound" is meaningless.
- **Fix:**
  - Choose F_max and the object ranges so that the fraction of instances with F\*_hi > F_max is ≤ α/10 in every
    pool. Check this in the pilot.
  - Report every stream, with unavoidable slips counted separately.
  - Reclassify H3.2 as a unit test.

### H3.3: transient (mostly arithmetic and internally inconsistent)
- **Arithmetic.** With constant η, OQT on a location shift Δq in score space needs about Δq / (η(1−α)) slips to
  catch up. For S1 that is 0.51 / (0.05 × 0.9) ≈ 11 extra slips. The "transient" is therefore determined by η and
  the shift size, both chosen by the experimenter.
- **Inconsistent arithmetic.** "Transient slips" are defined as slips **in excess of** α·t, yet "≤ 60" is compared
  with the 50 budgeted slips and called "≤ 1.2× budget". If 60 is the excess, the total is 110, i.e. 2.2× budget.
  If 60 is the total, the definition is wrong.
- **Vague.**
  - "Within ±0.05 of α within ≤ 400 steps" does not say whether this means first entry or staying inside for some
    duration.
  - "η pre-set from the in-distribution score scale" has no formula.
  - With W = 200 and α = 0.1, the window SD is ≈ 0.021. The ±0.05 band is about 2.4 SD, so a "first entry" rule is
    met almost immediately by noise.
- **Confounded comparison.** The ACI-vs-OQT oscillation prediction compares **fixed-γ ACI (level update)** with
  **decaying-step OQT (score update)**. That changes two factors at once. Compare fixed vs decaying within OQT, and
  level vs score updates at matched effective step size.
- **Correlated streams.** 20 orderings of the same 1,500–2,000 shifted instances, sampled without replacement,
  overlap heavily. "≥ 80 % of streams" counts correlated units. Count seeds × disjoint sub-pools instead.
- **Fix:** predict the transient with the Δq/η formula and test that formula. Give η a pre-registered formula, e.g.
  η = 0.1 × IQR of calibration scores. Use a sustained-entry criterion: stays within ±0.05 for 200 consecutive steps.

### H3.4: the S1 "asymmetry" is mis-derived (its mechanistic content is wrong)
- Under S1, μ × 0.6 is a **pure location shift** in log F\* for every instance, at least for Coulomb translational
  slip, and for torsional slip too if `condim` 6 scales torsional friction with μ.
- In log-score space, both OQT-on-CertGrip and OQT-on-CSF absorb that shift with the same additive constant. Each
  method's residual spread is unchanged, and so is its **relative** excess.
- So the proposer's own model predicts that CertGrip's in-distribution advantage **persists unchanged** under S1, not
  that it vanishes. "Touch cannot see friction" is irrelevant once a tracker supplies the global rescale.
- If H2 holds, H3.4 will "fail" under S1 for arithmetic reasons, and the paper will report that the mechanism is
  refuted when the hypothesis was wrongly derived.
- **Conversely, S2 (new family) is where CertGrip may lose.** A learned predictor extrapolating to unseen plates or
  meshes can have **larger** residual spread than the formula-based CSF. Predicting a ≥ 10 % advantage there has the
  sign at risk.
- **The real mechanistic test** is whether a shift changes the **spread** of scores (heteroscedastic) or only their
  **location**. Measure the post-shift score variance for each method. Predict "advantage preserved" for
  location-only shifts (S1, and S3 if amplitude scaling is near-multiplicative), and "advantage uncertain or
  reversed" for spread-changing shifts (S2).
- **Null claims need margins.** Any "no difference" claim needs TOST with a margin (X4).

### H3.5: price of deployability vs the oracle
- Well posed. The 20 % threshold is arbitrary.
- The oracle's 500 labelled shifted instances must be disjoint from the stream instances. This is not stated, and
  with S2 having only 2,000 instances it is easy to violate.

### Gaps in the online design
- Online methods see only slip_t, and in replay slip_t comes from the F\*_hi rule, not from simulation. The online
  validity claim is therefore also circular (X1). Audit a subset of stream steps by direct replay.
- Streams are i.i.d. within each regime. That is the easiest possible online setting. Repeated grasps of the same
  object, which are correlated, are realistic and untested. At minimum, state this.

**Verdict: REVISE (major):**
- Reclassify H3.2 as a unit test with no cap-binding exclusion.
- Add a mild shift and pre-register predicted magnitudes for H3.1.
- Replace H3.3 with a Δq/η prediction, a sustained-entry criterion and fixed arithmetic.
- Re-derive H3.4 as location shifts vs spread shifts.
- Keep H3.5, with disjointness from the stream instances.

---

## H4 — Value of touch

### Precision
- **Unstated timing of the touch features.** It is not said **when** the static and probe features are taken.
  - If the preload contact happens with the object resting on the table, there is no gravitational torque. The
    pressure centroid then carries **no information about the CoM offset**, and the F4 prediction is impossible
    by construction.
  - If the object is lifted at preload, it may already slip at F₀.
  - State the protocol: lift height, F₀ relative to F\*, and whether the object is supported.
- **"Largest gain in F4, smallest in F1/F2 centred"** needs an interaction test with a threshold, e.g. F4 gain minus
  F1 gain > 0 with a CI. "Centred grasps" also contradicts the randomised grasp offset from the CoM in all families.

### Fairness
- Each feature set needs equal tuning effort. The same GBT hyperparameter search with the same budget should run per
  input set. Otherwise the higher-dimensional inputs are either over-fitted or under-tuned.
- Dimensionality is a confound. Add a "shuffled touch" control (tactile features permuted across instances) to show
  the gain is information, not capacity.

### Alternative mechanisms
Touch might help through contact geometry (the claim) or through family identification (X5). To separate them, use
within-family ablations and the family-ID-from-touch probe. A model that is given family ID explicitly should not
gain from touch if touch is only an identifier.

### Thresholds
10 % and 5 % are unpowered (X3). The failure rule "CertGrip-P within 5 % of CertGrip (CI including 0)" mixes an
equivalence margin with a significance test. Use TOST.

**Triviality.** Not trivial, provided the preload protocol makes the CoM observable at all.

**Verdict: REVISE:** specify the preload and probe protocol, equal tuning, a shuffled-touch control, a within-family
interaction test, and TOST.

---

## Secondary (Gap 6)
"Mondrian calibration only if a group exceeds 2α" is a data-dependent decision that is not pre-registered as a test.
Its α inflation is fine for an exploratory analysis. Label it exploratory.

---

## Verdict summary

| ID | Verdict | One-line reason |
|---|---|---|
| H1a | **KEEP** (minor) | Genuinely empirical. Add a dense local grid, a tangential-only slip metric, a CI decision rule and budget for the shift pools. |
| H1b | **REJECT** as a hypothesis | A theorem evaluated on its own labels (circular). Keep as a FWER-corrected, cluster-aware unit test. Promote the direct-replay audit to the empirical claim. |
| H1c | **REVISE** (demote) | Nearly trivially true with asymmetric falsification. Needs two-sided testing, a validation-tuned RAW-Q and an effect-size threshold. |
| H2 | **REVISE** (major) | The comparator is too weak and the "conservative" mass claim is unsupported. The gain is set by the μ and disturbance ranges. The metric is ambiguous. ε is comparable to the effect. 8/16 is unpowered. |
| H3 | **REVISE** (major) | H3.1 is trivial by Coulomb. H3.2 is a theorem with outcome-conditioned exclusion. H3.3 is arithmetic with an internal inconsistency. H3.4's S1 asymmetry is mis-derived because S1 is a location shift. |
| H4 | **REVISE** | The preload protocol may make CoM unobservable. Family-ID confound. Equal tuning, shuffled-touch control and TOST are needed. |

## The three most serious problems

1. **H2 measures the design, not the method.** One-parameter CSF with privileged mass is a weak comparator, and the
   size of the gain depends on unspecified μ and disturbance ranges. The fix has three parts: compare against the
   stronger of Mondrian-CSF and CertGrip-P; drop mass from both or test without it; pre-register the ranges and
   report the oracle variance decomposition as the ceiling.
2. **The validity evidence is circular and its band is wrong.** Bisection labels are scored with the same F\*_hi rule,
   so they reproduce the conformal theorem, and the clustered instances and overlapping re-draws invalidate the
   Beta-binomial band and the 8 % rule. Make a powered direct-replay audit the validity claim. Separately, a
   non-tangential slip metric and MuJoCo contact artefacts (penetration, `condim`, contact points that act as family
   identifiers) could produce both non-monotonicity and the "tactile" gain.
3. **H3's mechanistic test is mis-derived and the rest is theorem or arithmetic.** S1 is a uniform log shift, so
   CertGrip's advantage should persist, not vanish. Under S2 the sign of the gain is at risk. H3.1, H3.2 and H3.3
   follow from Coulomb's law, the OQT bound and Δq/η. Excluding cap-binding streams conditions the result on its
   outcome. The paper also never says how offline CertGrip would be calibrated on hardware, where F\* cannot be
   measured, which is the core of the "just conformal prediction" objection at RSS.
