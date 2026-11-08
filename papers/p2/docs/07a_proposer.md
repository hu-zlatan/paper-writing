# Stage 8 · Pass 1 — Proposer (fresh opus subagent, 2026-11-08)

> **System:** "You formulate testable scientific hypotheses."
> **Task (verbatim template):** "Generate at least 2 falsifiable hypotheses from synthesis. Output markdown and for each
> hypothesis provide rationale, measurable prediction, failure condition. Synthesis: {synthesis}"
> **{synthesis}** = the full content of `docs/06_synthesis.md`. Constraints taken from `docs/00_topic_init.md` and
> `docs/01_problem_tree.md`.

Nothing below is a result. No paper-2 experiment has run. All numbers are pre-registration targets or cost
assumptions that the stage-10/12 pilot must confirm. Citation keys are only those that appear in the synthesis.

---

## 0. Shared experimental setting

### 0.1 Environment (CPU only, MuJoCo only)
- **Simulator:** pip `mujoco` 4.x, fixed timestep and solver settings frozen after the pilot (SQ1 sensitivity check
  done once, then locked). A parallel-jaw gripper with position-controlled approach and a **force-controlled closing
  axis**. The grasp pose is fixed per instance (given, not chosen).
- **Tactile:** one `touch_grid` sensor-plugin array per finger pad. Features are taken (i) at contact under a small
  preload F₀ ("static") and (ii) during a short **probe squeeze** F₀ → 2F₀ → F₀ ("probe": pressure-centroid shift,
  contact-area growth, per-taxel force slope). The probe is normal-only, so it shows contact geometry and compliance,
  **not friction**. This matters for H3 and H4.
- **Proprioception (all methods):** jaw aperture at contact, commanded and measured closing force, and object mass
  (metadata). The mass is privileged information. Giving it to every method, including the baseline, favours the
  baseline, so the comparison is conservative.
- **Objects:** rigid primitives and composites in 4 families: F1 boxes, F2 cylinders, F3 ellipsoids/capsules, F4
  two-body composites with an off-centre CoM. Randomised mass, size, friction μ (log-uniform within a nominal range),
  and grasp offset from the CoM.
- **Disturbances:** 4 types: D1 lift with acceleration, D2 shake (sinusoidal), D3 lateral pull, D4 added payload
  mid-hold. Each instance's disturbance has a fixed seed, so a replay is bit-identical at every force.
- **Slip outcome:** slip(F) = 1 if the relative object–pad displacement exceeds δ_slip (e.g. 2 mm, or rotation >
  3°) at any time in the episode. δ_slip is frozen in the pilot.
- **Label F\*:** bisection over [0, F_max] with the identical disturbance; 10 iterations, so ε = F_max/1024. We store
  the bracket [F\*_lo, F\*_hi]. Evaluation uses **slip ⇔ F < F\*_hi**, which is conservative under monotonicity. A
  direct-replay audit (§0.6) checks this rule against the real outcome at the method's chosen force.

### 0.2 Splits (disjoint object identities; unit-tested, risk R8)
- **In-distribution pool:** 4 families × 600 objects × 5 instances (pose/disturbance variants) = 12,000 labelled
  instances. Split **by object**: 50 % train, 25 % calibration pool, 25 % test (3,000 test instances).
- **Shift pools** (pre-registered, 2,000 instances each, never used for training or calibration):
  - **S1 lower friction:** μ × 0.6 for every object (mirrors the friction decrease in `willemet2024grip`).
  - **S2 new object family:** F5 (thin plates / mesh objects), held out entirely.
  - **S3 stronger disturbance:** disturbance amplitude × 1.5 (acceleration, shake amplitude, pull force, payload).

### 0.3 Calibration constants
- **α ∈ {0.01, 0.05, 0.10, 0.20}.**
- **Calibration size n ∈ {100, 500, 2000}**, drawn from the calibration pool.
- **Seeds:** 5 predictor-training seeds × 200 random calibration/test re-draws per (α, n) cell. The shift and online
  streams use 5 seeds × 20 stream orderings.
- **Finite-sample band:** with continuous scores, the conditional miscoverage given the calibration set is
  Beta(l, n+1−l) with l = ⌊(n+1)α⌋ (`angelopoulos2023conformal`). The test slip count on m test points is therefore
  Beta-binomial. The **band** is the central 95 % interval of that Beta-binomial. Validity requires both (i) a mean
  slip rate within [α − 1/(n+1), α] ± Monte-Carlo SE, and (ii) a fraction of re-draws outside the band ≤ 8 %
  (5 % nominal plus a binomial tolerance for 200 draws).

### 0.4 Methods

All conformal variants use **multiplicative scores** s = log(F\*_hi / g(x)), with F = g(x)·exp(q̂) and q̂ the
⌈(n+1)(1−α)⌉-th smallest calibration score. Additive scores are a secondary analysis.

| ID | Method | Inputs | Calibrated to α? | Role |
|---|---|---|---|---|
| FSF-k | Fixed safety factor: F = k·F_nom, k ∈ {1.2 (the 20 % margin of `khamis2021real`), 1.5, 2.0}; F_nom = m(g + a_nom)/(2 μ_nom), μ_nom = training-mean μ | mass, nominal disturbance | no | heuristic reference |
| **CSF** | **Calibrated safety factor:** score log(F\*/F_nom) on the **same calibration set**; F = F_nom·exp(q̂) | same as FSF | yes (one-parameter conformal, no touch) | **primary comparator** |
| RAW-Q | Quantile regressor at level 1−α, not conformalized | proprio + static + probe | no (targets α) | Gap-1 test |
| RAW-G | Gaussian μ̂ + z₁₋α σ̂ (heteroscedastic MLP), not conformalized | proprio + static + probe | no (targets α) | Gap-1 test |
| CP-pt | Conformalized point regressor (multiplicative score) | proprio + static + probe | yes | variant |
| CP-σ | Normalized score (log F\* − μ̂)/σ̂ | proprio + static + probe | yes | variant |
| **CertGrip** | One-sided CQR (`romano2019conformalized`) on the 1−α quantile regressor, multiplicative | proprio + static + probe | yes | **pre-registered primary** |
| CertGrip-P / -S | Same as CertGrip with proprio only / proprio + static | ablation inputs | yes | H4 |

- **Predictors:** gradient-boosted trees (the default) or a small MLP, trained on CPU in minutes. The choice is
  made once, on a validation split carved from **train**, before any test access. CertGrip is designated primary in
  advance. CP-pt and CP-σ are reported but not selected post hoc.
- **Online methods (H3):**
  - **OQT:** online quantile tracking in score space, q_{t+1} = q_t + η(slip_t − α) (`angelopoulos2023conformala`).
    Primary. It never saturates to "infinite force".
  - **ACI:** level update α_{t+1} = α_t + γ(α − slip_t) over the offline calibration scores (`gibbs2021adaptive`),
    with a pre-registered grid γ ∈ {0.005, 0.01, 0.05}.
  - **Decaying-step OQT** (`angelopoulos2024online`).
  - **OQT-CSF:** the same tracker applied to the safety-factor score. This is the strongest simple online baseline.
  - **Frozen** offline CertGrip and frozen CSF.
  - **Oracle re-calibration:** split conformal on 500 labelled shifted instances. It needs F\*, so it is not
    deployable; it serves only as a reference.
  - Every online method sees **only slip_t** after choosing F_t. Under monotonicity, slip_t = 1{F_t < F\*_t}
    (Synthesis Cluster 5).
- **Force cap:** F ≤ F_max (gripper limit). We report the fraction of instances with F\*_hi > F_max in every pool,
  because those are unavoidable slips that no method can fix.

### 0.5 Metrics
- **Slip rate** (validity), against the §0.3 band.
- **Force excess:** mean E[F − F\*_hi] (N), relative excess E[(F − F\*_hi)/F\*_hi], and the 95th-percentile excess
  (crush-risk proxy).
- **Online metrics:** running slip rate (1/T)Σslip_t; windowed slip rate (W = 200); transient slips, i.e. extra
  slips above α·t in the 500 steps after a shift onset; and the mean excess after the transient.
- **Statistics:** paired comparisons on identical test instances. The bootstrap resamples **objects** (cluster
  bootstrap, 2,000 draws), because instances of one object are correlated. Holm correction across the 16
  family × disturbance conditions.

### 0.6 Budget (≈ 100 CPU-hours total; free Actions runners plus the 2-vCPU sandbox)

The pilot must time the replay cost c. The plan below assumes **c ≤ 1 CPU-s per replay** (≈ 2 s of simulated time
with touch grids).

| Item | Count | CPU-h at c = 1 s |
|---|---|---|
| F\* labels (in-dist. + 3 shifts), 11 replays each | 18,000 × 11 | 55 |
| Monotonicity grid (H1a), 40 forces | 1,000 × 40 | 11 |
| Direct-replay audit at chosen forces | 2,000 × 4 methods | 2.2 |
| Training, conformal, online streams (label replay) | — | < 3 |
| Slack (25 %) | — | ~18 |
| **Total** | | **≈ 89** |

If c > 1 s, apply the pre-registered downscale order (risk R2) in this sequence:
1. Reduce bisection iterations to 8 (ε = F_max/256, still conservative via F\*_hi).
2. Reduce to 400 objects per family.
3. Shorten the disturbance window.

The online streams **replay already-labelled instances**, so H3 costs almost nothing beyond the labels.

---

## H1 — Offline slip-rate validity, including the monotonicity premise (Gaps 4 → 1; SQ1, SQ2)

**Rationale.** A guarantee on P(F < F\*) is a guarantee on P(slip) only if slip is monotone in F. Synthesis Gap 4
notes that no prior work measured this. MuJoCo's soft contacts, high-force ejection and rolling could break it.
Given monotonicity and exchangeability, the slip-rate bound is a theorem (`lei2017distribution`,
`angelopoulos2022conformal`), so its empirical content lies in the premises and in whether simple targeting methods
already work (Gap 1).

**H1a (empirical, genuinely uncertain): monotonicity.**
- *Prediction:* on a 40-point log-spaced force grid over [0.5·F\*_lo, F_max], for 1,000 in-distribution instances
  (250 per family), **≤ 1 % of instances** show a non-monotone slip pattern, defined as at least one force above
  F\*_hi that slips. The same holds within each family (≤ 3 %) and within each shift pool.
- *Failure condition:* a non-monotone rate > 1 % overall, or > 3 % in any family. In that case the quantile route is
  declared invalid for the affected pool and the primary analysis switches to conformal risk control on the binary
  loss 1{slip(F)}, using the non-monotone variant (`angelopoulos2026conformal`). The paper states this change.
- *Why uncertain:* F4 composites and D2 shake are plausible sources of rolling or ejection at high force, and we have
  no prior estimate.

**H1b (mostly a theorem; a pipeline check): conformal validity.**
- *Prediction:* for CSF, CertGrip, CP-pt and CP-σ, in **every** (α, n) cell and for each of the 5 seeds, the mean test
  slip rate lies in [α − 1/(n+1), α] ± 2 MC-SE, and ≤ 8 % of re-draws fall outside the 95 % Beta-binomial band. The
  same holds when slip is the direct-replay outcome (audit subset).
- *Failure condition:* any cell outside the band. Because the bound is a theorem, a violation means a **premise or
  pipeline defect** (leakage, label error beyond ε, non-monotonicity, ties), not a refutation of conformal
  prediction. It must be diagnosed before H2–H4 are reported.
- *Honesty note:* we will **not** present H1b as a discovery. It is the necessary check that the simulator labels
  satisfy the premises.

**H1c (empirical, uncertain): uncalibrated targeting fails (Gap 1 is non-empty).**
- *Prediction:* the non-conformal methods that *aim* at α, RAW-Q and RAW-G, fall **above** the upper band edge
  (under-coverage, i.e. too many slips) for at least one α ∈ {0.01, 0.05} in ≥ 4 of 5 seeds. The expected cause is
  quantile-regression and Gaussian-tail miscalibration in the extreme tail.
- *Failure condition:* RAW-Q **and** RAW-G both land inside the band at all four α in ≥ 4 of 5 seeds. That outcome
  would show Gap 1 to be practically empty for learned quantile predictors, and calibration would be insurance rather
  than a fix. We would report this and down-weight the validity claim.
- *Note:* FSF-k trivially misses most α, because one factor yields one slip rate. It is reported for context (what
  slip rate does a 20 % margin actually give here?), not as evidence for H1c.

---

## H2 — Force efficiency vs the calibrated safety factor at matched α (Gap 2; SQ3) — *primary comparative claim*

**Rationale.** CSF and CertGrip are both conformal, so both meet α by construction, and the only open question is
cost. CSF must cover the full spread of log(F\*/F_nom) across instances. That spread includes unmodelled friction,
contact geometry, CoM offset and disturbance severity. CertGrip covers only the **residual** spread after per-grasp
prediction. If tactile and probe features explain contact geometry and CoM offset (via the pressure centroid), the
residual quantile is smaller and so is the excess. If the dominant variance is friction, which the normal-only probe
cannot see, the gain shrinks. That makes the outcome genuinely uncertain. The 9–30 % excess of a hand-set 20 % margin
(`khamis2021real`) is the kind of number at stake.

**Measurable prediction (pre-registered).**
1. **Pooled:** at α ∈ {0.05, 0.10} with n = 2000, CertGrip's mean force excess is **≥ 15 % lower** (relative) than
   CSF's. The lower limit of the object-cluster-bootstrap 95 % CI on the reduction is > 0 in both α.
2. **Per condition:** a significant reduction (paired, Holm-corrected, p < 0.05) in **≥ 8 of 16** family × disturbance
   conditions at α = 0.10.
3. **Tail:** CertGrip's 95th-percentile excess is **not higher** than CSF's (CI on the difference includes or lies
   below 0). This guards against per-grasp predictors buying a lower mean with rare very high forces, which would
   mean crush risk.
4. **Small n:** at n = 100 the reduction persists at α ∈ {0.10, 0.20}, with a lower CI limit > 0. At α = 0.01 with
   n = 100 both methods use the maximum score, and no claim is made.

**Failure condition.**
- A pooled reduction **< 5 %**, or a CI including 0 at both α: **refuted**. The calibrated safety factor matches
  CertGrip, and per-grasp tactile adaptation adds no force efficiency at a guaranteed slip rate. We report this as the
  headline negative (risk R3), and the paper leans on H1 + H3.
- A reduction between 5 % and 15 %: "weak". We report the effect size without claiming the primary threshold.
- Prediction 3 violated: the mean gain is reported only together with the tail cost, and the efficiency claim is
  qualified.

**Explicit non-claim.** We do not compare against FSF-k on excess. FSF-k does not meet a matched α, so an excess
comparison with it is meaningless. (This is the point of Gap 2.)

---

## H3 — Online slip-rate control from binary slip feedback under shift (Gap 3; SQ5) — *second core claim*

**Rationale.** In grasping, the miscoverage indicator is the slip event itself (Synthesis Cluster 5). Online
trackers (`gibbs2021adaptive`, `angelopoulos2023conformala`) therefore need no F\* at deployment. Their long-run
bound is **deterministic**: for OQT with scores bounded by B, |(1/T)Σslip_t − α| ≤ (B + η)/(ηT). That bound is a
theorem whenever the force cap never binds, so it is not the uncertain part. Three things are genuinely uncertain:
(i) whether the pre-registered shifts actually break offline calibration (if not, Gap 3 is empty); (ii) how many
extra slips the transient costs; (iii) whether per-grasp prediction still lowers the force after adaptation, or the
tracker simply turns CertGrip into a safety factor.

**Streams.** T = 2,000 steps per stream:
- Abrupt: 500 in-distribution steps, then 1,500 shifted steps.
- Gradual: S1 friction scale moving linearly 1.0 → 0.6 over steps 500–1,500.

Each of S1, S2 and S3 gets 5 seeds × 20 orderings. Main condition: α = 0.10 (α = 0.05 secondary).

**Measurable predictions.**
1. **Offline breaks in the predicted direction (empirical):**
   - Frozen CertGrip and frozen CSF have post-shift slip rates **above the band's upper edge**, and ≥ 1.5α, under S1
     (lower friction raises F\*, and the probe cannot see μ) and under S3 (larger disturbance raises F\*).
   - S2 is pre-registered as **two-sided**: we predict leaving the band but do not commit to a direction.
2. **Long-run validity (theorem check):** OQT's running slip rate at T is within the deterministic bound, for every
   stream with zero cap-binding steps. Streams where the cap binds are reported separately.
3. **Transient (empirical):**
   - After an abrupt shift, OQT (η pre-set from the in-distribution score scale) brings the windowed (W = 200) slip
     rate back to within ±0.05 of α within **≤ 400 steps** in ≥ 80 % of streams.
   - Transient slips stay **≤ 60** per stream at α = 0.10, against roughly 0.1 × 500 = 50 slips expected over the
     500 steps at the target rate. This means the excess slips cost at most about 1.2× the budgeted ones.
   - Fixed-γ ACI at γ = 0.05 is predicted to oscillate more: the windowed slip-rate SD over the last 1,000 steps is
     ≥ 1.5× that of decaying-step OQT.
4. **Efficiency after adaptation (empirical, the main uncertainty):** over the last 1,000 steps, OQT-on-CertGrip
   has a mean excess **≥ 10 % lower** than OQT-on-CSF under S3 and S2.
   - **Under S1 we predict no significant difference** (|Δ| CI includes 0). Both methods must rescale for an
     unseen friction change, and touch does not observe it.
   - This asymmetry is the falsifiable mechanistic content.
5. **Price of deployability:** the post-transient excess of OQT-on-CertGrip is within 20 % of oracle
   re-calibration (which uses 500 labelled shifted instances).

**Failure conditions.**
- (1) fails for all three shifts, i.e. offline stays in the band: **Gap 3 is empty for these shifts.** The online
  claim reduces to "costs nothing when not needed" (we would then check that its excess is within 5 % of the frozen
  version) and is demoted.
- (2) fails on a stream with no cap binding: an **implementation bug** (the bound is deterministic) that blocks
  reporting.
- (3) fails: the transient is too costly for the stated η. We report the measured transient and do not claim fast
  recovery.
- (4) shows **no** advantage under S2 and S3, or shows an advantage under S1 (contradicting the predicted
  asymmetry): the mechanism story ("touch helps through geometry, not friction") is refuted, whatever the validity
  result.

---

## H4 — Value of touch in one currency (Gap 5; SQ4) — *secondary; shares H2's runs*

**Rationale.** Validity holds for every input set (H1b), so force excess at a fixed α is the only quantity that
changes in the ablation. This gives a single currency, newtons above F\*, for the question "does touch help?"
(`luu2025manifeel`, `birtalan2026impact` measure task success instead).

**Measurable prediction.** At α = 0.10 and n = 2000, pooled:
- CertGrip-S (proprio + static touch) has ≥ 10 % lower mean excess than CertGrip-P (proprio only).
- CertGrip (+ probe) has a further ≥ 5 % lower excess than CertGrip-S.
- The largest touch gain falls in F4 (off-centre CoM), where the pressure centroid is informative, and the smallest in
  F1/F2 with centred grasps.

**Failure condition.** CertGrip-P is within 5 % of CertGrip (CI including 0). In that case touch adds nothing to this
decision in MuJoCo, and any H2 gain comes from learned proprioceptive/mass features, not touch. The paper's framing
would change from "tactile" to "learned + calibrated". The probe-specific claim is dropped if the CertGrip vs
CertGrip-S CI includes 0.

*Secondary analysis (no hypothesis; Gap 6):* we report per-group slip rates for the friction tertile, the CoM-offset
tertile and each family under marginal calibration. Mondrian calibration (`ding2023class`) is run only if a group's
slip rate exceeds 2α.

---

## Theorem vs empirical, at a glance

| Claim | Status if premises hold | What is genuinely uncertain |
|---|---|---|
| H1a monotonicity ≤ 1 % | — | fully empirical (simulator behaviour) |
| H1b conformal slip-rate band | **theorem** (exchangeability + monotonicity + labels within ε) | only the pipeline; a violation means a bug or a broken premise |
| H1c raw quantile/Gaussian miss α | — | empirical; failure would shrink Gap 1 |
| H2 ≥ 15 % less excess than CSF, no worse tail | — | fully empirical; the paper's main comparative risk (R3) |
| H3-1 offline breaks under S1/S3 | — | empirical, with a physical argument for the direction |
| H3-2 OQT long-run bound | **theorem** (deterministic, cap not binding) | only cap-binding and implementation |
| H3-3/4/5 transient, post-shift excess, S1 asymmetry | — | fully empirical |
| H4 touch/probe gains | — | fully empirical; shares runs with H2 |

**Scope for the 5-page abstract:**
- **Contribution 1** = H1 + H2: guaranteed offline slip rate, and its force cost against the calibrated safety
  factor.
- **Contribution 2** = H3: online calibration from binary slip feedback under shift.
- H4 and the Gap-6 analysis go in only as one figure or table if space allows.
