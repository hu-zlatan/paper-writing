# Stage 8 · Final hypotheses (pass 3 — Methodologist, fresh opus subagent, 2026-11-08)

> **System (verbatim):** "You are a methodology lead synthesizing a proposer and a skeptic into final, defensible
> hypotheses."
> **Task (verbatim):** "Produce the final hypothesis set, addressing every critique. For each surviving hypothesis
> include: rationale, measurable prediction (with concrete metric and threshold), failure condition (with concrete
> metric and threshold), and the experiment design sketch (datasets / baselines / ablations needed).
> Proposer output: {proposer_output}
> Skeptic critique: {skeptic_output}"
> **Inputs:** {proposer_output} = full content of `docs/07a_proposer.md`; {skeptic_output} = full content of
> `docs/07b_skeptic.md`. Context read: `docs/00_topic_init.md`, `docs/01_problem_tree.md`, `docs/06_synthesis.md`.
> Hard constraints: CPU-only MuJoCo (pip `mujoco` 4.x), ≈ 100 CPU-h on free GitHub Actions runners, parallel-jaw
> gripper, no hardware, RSS 2027 Stage 1 extended abstract (5 pages, ≤ 2 core contributions), pre-registered and
> runnable before 2026-12-01.

**Status of every number.** No paper-2 experiment has run. Every number below is either a **pre-registration target**
(tagged *[target]*), a **design choice** (*[design]*), or an **assumption the pilot will replace** (*[assumption]*).
Citation keys are only those in `06_synthesis.md`. The stage-10/12 pilot fills every *[assumption]* slot with measured
values **on pilot objects that are never reused in the main run**; the pre-registration is frozen before any main-run
label is generated.

---

## 0. What the paper claims (two contributions, "sushi")

| Contribution | Core hypotheses | One-sentence claim |
|---|---|---|
| **C1 — A guaranteed slip rate whose premise is measured, and what touch buys at that rate** | H1, H2 | In MuJoCo, slip is (measurably) monotone in grip force, the label-based conformal guarantee transfers to the simulated physical slip outcome, and at a matched guaranteed slip rate tactile per-grasp prediction lowers grip force relative to the strongest *non-tactile* conformal method — or it does not, which we report. |
| **C2 — Calibration from drops alone** | H3 | Because the slip event *is* the miscoverage indicator, score-space quantile tracking restores the target slip rate under shift from binary slip feedback only, at a force price measured against a label-requiring oracle recalibration. |

The guarantees themselves are textbook (`lei2017distribution`, `romano2019conformalized`, `gibbs2021adaptive`,
`angelopoulos2023conformala`). The paper does **not** present them as findings. They appear as unit tests (§2). The
robotics content is (a) the measured premise, (b) the matched-α force cost with a fair comparator and an oracle
ceiling, and (c) the deployable binary-feedback path with its measured price in force and in drops. That is the answer
to the "just conformal prediction" objection (X6).

Everything else (decomposition of the touch gain, raw-quantile miscalibration, per-group coverage, hardware
calibration routes) is secondary or exploratory and gets at most one table in the abstract.

---

## 1. Fixed design decisions

### 1.1 Simulator, gripper, protocol
- pip `mujoco` 4.x, version pinned. Timestep, solver, `cone`, `condim`, `solref`/`solimp`, and friction-related
  parameters are **identical for every family and every shift** and printed in the paper (UT7) *[design]*.
- Parallel-jaw gripper with position-controlled approach and a force-controlled closing axis. The grasp pose is given
  per instance (random offset from the CoM, all families).
- **Grasp protocol per episode** *[design; pilot may adjust constants before freeze]*:
  1. Close to a **constant preload** F₀ = 2 · m_max · g / (2 μ_min). This is the same for every instance, so F₀
     encodes neither mass nor friction.
  2. Lift quasi-statically by 5 mm and hold 0.2 s. The object is now supported by the grasp alone, so
     gravity-induced load (including torque from an off-centre CoM) shows up in the pad readings. This answers the
     H4 timing critique: a table-supported preload would hide the CoM.
  3. Probe squeeze F₀ → 1.5 F₀ → F₀ over 0.3 s.
  4. Ramp the force to the method's chosen F and settle for 0.1 s.
  5. Run the disturbance window. A slip during step 4 counts as a slip. A slip during step 2 is recorded as a binary
     "preload slip" feature.
- **Tactile:** one `touch_grid` array per pad. The pilot checks which channels the installed plugin provides (normal
  only, or normal + tangential). Tangential channels are used if available. If only normal pressure exists, the CoM
  prediction in H4d is weakened and the pre-registration says so.
- **Slip metric** (X5-i) *[design; δ frozen in pilot before any monotonicity data]*:
  - slip = 1 if, at any time from step 4 to the end of the window, the object's displacement relative to the pad frame
    **projected onto the pad plane** exceeds δ_t = 2 mm *[assumption]*;
  - or its rotation about the grasp axis exceeds 3° *[assumption]*;
  - or contact with both pads is lost.
  - The normal (penetration) component is excluded by construction, verified by UT9.
- **Label F\*:** bisection **in log-force** on [F_min, F_max] = [0.1 N, 100 N] *[assumption: F_max chosen by UT8]*.
  One replay at F_max plus 10 halvings gives 11 replays per instance and a relative bracket width
  ln(1000)/1024 ≈ 0.7 %. This replaces the proposer's linear bisection, whose quantisation is up to 16 % of a
  light-object F\* (skeptic H2). Stored values are [F\*_lo, F\*_hi] and F\*_mid = √(F\*_lo·F\*_hi).
  - **Calibration scores use F\*_hi** (conservative).
  - **Excess uses F\*_mid**, and the primary result is re-checked with F\*_lo and F\*_hi.
  - Instances with F\*_hi > F_max are "unavoidable" and reported per pool. UT8 requires them to be ≤ 1 % (= α/10 at
    α = 0.10) in every pool, including the shifts. If the pilot violates this, m_max is lowered (pre-registered rule)
    rather than excluding instances.

### 1.2 Objects, ranges and splits
- **Families:**
  - F1 boxes, F2 cylinders, F3 ellipsoids/capsules, F4 two-body composites with an off-centre CoM;
  - shift family **F5 = thin plates (box geoms ≤ 5 mm thick) and disks (flat cylinders)**.
  - F5 deliberately uses the same collision primitives as F1/F2. The proposer's mesh objects are dropped, because a
    new collision routine would confound "new family" with "new contact solver" (X5).
- **Ranges** (X7) *[design; no source in the synthesis gives numeric values, so they are stated as design choices and
  their influence is measured, §4 H2-R]*:
  - μ log-uniform on [0.3, 1.0];
  - mass log-uniform on [0.05, 1.0] kg;
  - CoM offset uniform up to 40 % of the half-extent along the jaw-parallel axis, and up to 60 % for F4;
  - D1 lift acceleration U[1, 10] m/s²;
  - D2 shake amplitude U[5, 20] mm at frequency U[2, 5] Hz;
  - D3 lateral pull U[0.5, 2]·m g;
  - D4 payload added mid-hold U[0.2, 1.0]·m.
- **In-distribution pool:**
  - 4 families × 500 objects; each object gets **exactly one instance per disturbance type** (D1–D4) with its own
    random pose offset, giving 8,000 instances.
  - Split **by object**, per family: 250 train / 125 calibration / 125 test. The 2,000 test instances therefore come
    from 500 objects.
  - **Selection split:** 20 % of the train objects are held out for tuning and comparator selection. Half of them act
    as a pseudo-calibration set and half as an evaluation set. The calibration and test pools are not touched before
    the freeze.
- **Calibration is stratified by disturbance type** (a known task variable, §1.3). Within a stratum each object
  contributes exactly one instance, so calibration and test points are exchangeable **at the object level**. This
  resolves X2 without throwing data away, and the guarantee holds per stratum and therefore marginally.
  - n_cal per stratum ∈ {50, 150, 500} objects *[design]* (this replaces the proposer's {100, 500, 2000}).
- **Shift pools** (never used for training; each is split by object into 125 objects for oracle calibration and
  375 objects for the stream segments):

| ID | Definition | Construction | Predicted direction for frozen offline methods |
|---|---|---|---|
| **S1** lower friction | μ ← 0.6 μ | **paired:** the 2,000 test instances re-simulated with only μ changed | slip rate **up** (F\* rises by 1/0.6; Δlog F\* = +0.51 if Coulomb scaling holds) |
| **S1m** mild friction | μ ← 0.9 μ | paired, as S1 | slip rate **up**, by a magnitude predicted in advance from the location model (Δlog F\* = +0.105); *whether it leaves the band is genuinely uncertain* |
| **S3** stronger disturbance | every amplitude × 1.5 | paired | slip rate **up**; F\* rises **non-uniformly** ((g + 1.5a)/(g + a) depends on a), so this is location **plus spread**. Learned predictors also extrapolate outside the training amplitudes for D1/D2. |
| **S2** new family | F5, 500 new objects × 4 disturbances | new objects | **two-sided**; "breaks" iff \|slip − α\| ≥ 0.5α |

The direction of S1 mirrors the friction decrease studied in humans (`willemet2024grip`). S1 and S3 do not pair with
the training data, only with the test objects, so no leakage arises.

### 1.3 Information each method receives (the fairness table)

| Input | Available on hardware? | CSF-1 | Mondrian-CSF | CertGrip-P | CertGrip-S | **CertGrip** |
|---|---|---|---|---|---|---|
| Disturbance **type** (D1–D4) | yes (task) | ✓ (strata) | ✓ | ✓ | ✓ | ✓ |
| D1/D2 commanded amplitude (self-generated motion) | yes | ✓ (in F_nom) | ✓ | ✓ | ✓ | ✓ |
| D3/D4 amplitude (external) | no | ✗ | ✗ | ✗ | ✗ | ✗ |
| Object mass m | **only by weighing** (wrist F/T or joint torques during the 5 mm lift) *[assumption]* | ✓ | ✓ | ✓ | ✓ | ✓ |
| Proprio: aperture at contact, measured preload force | yes | ✗ | ✗ | ✓ | ✓ | ✓ |
| Static touch at the lifted preload (+ preload-slip flag) | yes | ✗ | ✗ | ✗ | ✓ | ✓ |
| Probe-squeeze features | yes | ✗ | ✗ | ✗ | ✗ | ✓ |
| **Family ID** | no (privileged) | ✗ | **✓** | ✗ | ✗ | ✗ |

- CSF-1: F = F_nom · exp(q̂), with F_nom = m (g + a_cmd) / (2 μ̄) for D1/D2 and m g / (2 μ̄) for D3/D4, where μ̄ is
  the geometric mean of the μ range. Mondrian-CSF: the same, with one q̂ per family × disturbance cell (16 cells,
  125 calibration objects per cell at full n) (`ding2023class`).
- **Mass is given to every method in the main analysis.** The proposer's claim that this is "conservative" is
  **withdrawn**, because a learner may exploit mass better than the formula does (skeptic H2-1). A **no-mass** condition
  (all methods, H2-M) and a **10 % multiplicative mass-noise** condition are pre-registered secondary analyses.
- **Family ID is given only to Mondrian-CSF.** This strengthens the comparator, and the identifier confound is then
  tested directly in H4b.

### 1.4 Methods
- All conformal methods use **one-sided multiplicative scores**:
  - CQR (`romano2019conformalized`) score s = log F\*_hi − log ĝ_{1−α}(x), with F = ĝ_{1−α}(x)·exp(q̂);
  - q̂ = the ⌈(n+1)(1−α)⌉-th smallest score in the stratum (`lei2017distribution`, `angelopoulos2023conformal`);
  - F is capped at F_max.
- **Predictors:** gradient-boosted quantile trees, one model per τ = 1 − α. **Equal tuning effort** for every input
  set: the same 30-config random search with 4-fold grouped CV by object on the train objects (H4 fairness).
- **Primary comparator COMP (decided):** whichever of **Mondrian-CSF** and **CertGrip-P** has the lower mean relative
  excess at α = 0.10 on the selection split. The choice is made once, logged, and frozen before any calibration or test
  access.
  - This makes the primary claim "touch beats the best non-tactile conformal method" instead of "conditioning beats one
    global factor", which is the skeptic's strawman objection.
  - CSF-1 (the Gap-2 classic) is reported as a secondary comparator.
- **Raw (non-conformal) targeters, for H1c only:**
  - RAW-Q: quantile model at τ = 1 − α;
  - RAW-Qv: τ tuned on the selection split until the selection slip rate equals α (what a practitioner would do);
  - RAW-G: Gaussian heteroscedastic, μ̂ + z σ̂.
- **Online rule (decided): score-space online quantile tracking (OQT)** (`angelopoulos2023conformala`):

  q_{t+1} = q_t + η (slip_t − α), with F_t = min(F_max, ĝ(x_t)·exp(q_t)) and q₁ = offline q̂.

  - **Why score space rather than ACI's level update** (`gibbs2021adaptive`). ACI re-indexes a fixed set of offline
    calibration scores. A friction drop shifts every score by about +0.51, which can exceed the largest offline score,
    and ACI then saturates at "infinite force" (F_max for every grasp). OQT moves q itself, so it can track shifts
    beyond the calibration support.
  - **Why a constant step.** Decaying steps (`angelopoulos2024online`) stop adapting, so they cannot follow a shift
    that arrives late. Cluster 5 of the synthesis names this trade-off. Decaying-step OQT is a secondary arm, and ACI
    is exploratory.
  - **Step size (pre-registered formula):** η = 0.1 × IQR of the in-distribution calibration scores at α = 0.10
    *[design; value computed at freeze]*. The same η is used for every predictor's tracker.
  - **Anti-windup:** if F_t was capped at F_max, q is **not** updated. The robot knows it commanded F_max, and a slip
    at the cap carries no actionable information. Capped steps stay in every slip count; they are reported separately
    and never excluded (H3.2 critique).
  - The tracker sees **only slip_t** after acting, never F\*.
- **Oracle re-calibration (reference, not deployable):** split conformal at α on the 125 oracle objects of the shift
  pool (500 labelled instances, one per stratum per object). These objects are **disjoint** from the stream objects.

### 1.5 Metrics
- **Primary efficiency metric (decided, X/H2 ambiguity):** mean **relative** excess
  RE = mean over test instances of (F − F\*_mid)/F\*_mid, signed, including slipped instances.
  - Effect size: **D = 1 − RE(CertGrip)/RE(COMP)**, a paired ratio of means on identical instances.
  - Relative excess is chosen because every method is multiplicative, and because log-bisection makes relative label
    error uniform (≈ 0.7 %).
  - Absolute excess in newtons and mean log-excess are secondary.
- **Validity (physical):** the direct-replay slip outcome at the method's chosen F.
- **Inference:** object-cluster bootstrap with 2,000 draws. When calibration variability enters an estimate, the
  calibration objects are resampled too. Paired comparisons always use the **same calibration draw** for both methods
  (skeptic H2.4).

---

## 2. Theorem-backed properties → unit tests and sanity checks (not hypotheses)

A failure in this section is a **pipeline defect**. It blocks reporting until fixed. It is never reported as a
scientific result.

| ID | Property | Why it is not a hypothesis | Check |
|---|---|---|---|
| UT1 | Train, calibration, test, selection, oracle-calibration and stream object sets are disjoint (R8) | Bookkeeping | Assert on object IDs and seeds |
| UT2 | Quantile indexing (off-by-one) | Exact combinatorics | For random sets of n+1 distinct scores, the fraction of leave-one-out choices exceeding the ⌈(n+1)(1−α)⌉-th order statistic of the rest lies in [α − 1/(n+1), α] **exactly** |
| UT3 | Label-rule validity of split conformal (`lei2017distribution`) and its training-conditional form (`bian2023training`) | Theorem given object-level exchangeability. On labels it is circular (X1), so it only checks the pipeline. | 1,000 random object-level re-splits of the 1,000 calibration + test objects, for every (α, n, method, stratum). Given a uniformly random partition of a **fixed** pool, coverage is again within [α − 1/(n+1), α] **pool-conditionally**, and the re-splits are independent draws, so Monte-Carlo error is binomial. Pass iff the mean lies in [α − 1/(n+1) − z·SE, α + z·SE] with z Bonferroni-corrected over all K cells (FWER 5 %). This replaces "≤ 8 % of 200 draws outside a Beta band" (X2, X3). The re-split spread of conditional coverage is reported descriptively, with no band claim. |
| UT4 | OQT accounting identity and long-run bound (`angelopoulos2023conformala`) | Deterministic algebra | (a) Σ_{uncapped t}(slip_t − α) = (q_{T+1} − q₁)/η to float precision on every stream. (b) \|running rate over uncapped steps − α\| ≤ (max q − min q)/(η T_uncapped); the **numeric value** of this bound is printed per stream (it must be < α to be meaningful, which addresses the "vacuous bound" critique). **No stream is excluded.** Unavoidable slips are counted separately. |
| UT5 | Bracket consistency | Follows from bisection | The replay at F\*_hi does not slip and the replay at F\*_lo does slip (both are observed during bisection). F_max no-slip is checked. Violations are flagged and counted in H1-M. |
| UT6 | Determinism | Simulator property | Replaying the same instance at the same F twice gives a bit-identical trajectory hash on the runner image (50 instances per shard) |
| UT7 | Physics configuration is identical across families and shifts (X5-ii) | Configuration | Assert `condim`, `cone`, `solref`, `solimp`, timestep and integrator from the compiled models |
| UT8 | Cap rarity | Design condition | P(F\*_hi > F_max) ≤ 1 % in every pool (pilot estimate; full count reported) |
| UT9 | Slip metric is tangential-only (X5-i) | Metric definition | Synthetic tests: 3 mm of pure normal penetration gives slip = 0; 3 mm of tangential displacement gives slip = 1 |

**Consequence for drop accounting (H3.3 critique).** By UT4(a), the extra slips that OQT spends to adapt to a shift
equal Δq/η exactly, where Δq is the quantile change it had to make. The "transient slip count" is therefore an
**identity**, not a hypothesis. The paper reports it as **drops per shift = Δq/η** together with the measured Δq. The
empirical content is Δq, the size of the shift in score space, which H3-B predicts.

---

## 3. Core hypotheses (confirmatory)

**Multiplicity plan.**
- There are three core hypotheses, each with **one** primary decision. The family-wise error rate (FWER) is 5 %,
  split by Bonferroni: each core decision uses a one-sided level of 0.05/3 = 0.0167, equivalently **two-sided 96.7 %
  confidence intervals (CI\*)**.
- Within a core hypothesis, sub-conditions that must **all** hold are combined as an intersection-union test, which
  needs no further adjustment.
- Secondary hypotheses (§4) use Holm at 5 % within each family (H1c / H2-x / H3-x / H4-x).
- Exploratory items (§5) carry no correction and are labelled as such.
- The ordering is **not** a fixed-sequence gate. The online claim (H3) does not depend on the efficiency claim (H2),
  so it is not tested conditionally on H2. The one exception is H1-M, a **design gate**: if it fails, the validity
  route changes (see below) before H2/H3 run.

---

### H1 — The monotonicity premise holds, and the label guarantee transfers to the physical slip outcome (Gaps 4 → 1; SQ1, SQ2)

**Rationale.**
- A guarantee on P(F < F\*) is a guarantee on P(slip) only if slip is monotone in F. No prior work has measured this
  (Gap 4).
- Everything computed on bisection labels is circular (X1). The only evidence that the guarantee concerns the
  simulated robot, and not a column of numbers, is (a) a bracket-independent monotonicity measurement and (b) a
  direct replay at the forces the methods actually choose.
- Both are genuinely uncertain. Possible failure sources: MuJoCo soft-contact penetration, rolling or ejection at high
  force in F4 and D2, and wedging at low force.

**H1-M (design gate) — monotonicity.**
- *Data:* 800 in-distribution instances (50 per family × disturbance cell, from train and calibration objects).
- *Force grid:* 25 log-spaced forces on [F_min, F_max], plus a **dense local grid** of 10 log-spaced forces on
  [F\*_hi, 1.5 F\*_hi], plus the 11 bisection replays.
- *Non-monotone instance:* any pair F_a < F_b with slip(F_a) = 0 and slip(F_b) = 1 among all simulated forces. This
  definition is bracket-independent and also catches no-slip islands below F\*_lo (X1, H1a).
- *Prediction [target]:* the one-sided 98.3 % Clopper–Pearson upper limit of the non-monotone rate is **≤ 2 %**,
  i.e. **≤ 7 non-monotone instances out of 800**.
  - The 2 % tolerance is 0.2α at the primary α = 0.10: the largest label-to-physics gap that would still be smaller
    than the H1-V tolerance.
  - *Power [assumption, binomial]:* P(pass) ≈ 0.95 if the true rate is 0.5 %, ≈ 0.45 at 1 %, and ≈ 0.01 at 2 %.
- *Failure condition:* more than 7 non-monotone instances out of 800.
  - Reported as a negative finding: "slip is not monotone in force in this simulator at rate X".
  - The primary validity route switches to **conformal risk control on the binary loss** 1{slip(F)}, in its
    non-monotone form (`angelopoulos2026conformal`, cluster 4). The loss curve is evaluated on a 20-point λ-grid per
    calibration instance, funded by the slack and downscale step 1.
  - Per-family rates and CIs are reported **descriptively**, with no gate, because 200 per family is underpowered
    (skeptic). A family with a point rate > 5 % is flagged, and in that family validity is reported from direct replay
    only.
  - The shift pools S1, S3 and S2 each get 100 instances on the same grid, reported descriptively with no gate.
- *Leniency check (alternative mechanism):* the distribution of maximum tangential displacement at F_max, and the
  fraction of no-slip episodes with peak displacement in [0.5 δ_t, δ_t] ("near misses"). If near misses exceed 10 %
  *[target]*, monotonicity is reported as metric-dependent, with the δ_t ∈ {1, 2, 4} mm sensitivity (exploratory).

**H1-V (primary decision of H1) — physical validity by direct replay.**
- *Data:* all 2,000 test instances at α = 0.10 and n_cal = 500 per stratum, for CertGrip. Each instance is simulated
  at the chosen F.
- *Metric:* the **paired net disagreement** Δ = mean_i[slip_direct,i − 1{F_i < F\*_hi,i}] on identical instances.
  - This measures exactly how far the physical slip rate departs from the label-rule rate that the theorem controls.
  - A paired difference is far more powerful than the skeptic's absolute-rate test. At α = 0.01 an absolute audit has
    about 20 expected slips; a paired disagreement test does not depend on that count.
- *Prediction [target]:* the CI\* upper limit of Δ is **≤ τ = 0.2α = 0.02**.
- *Power [assumption]:* with a true Δ of 0.5 % (design effect 1.5 for 4 instances per object), the CI\* upper limit is
  ≈ 0.9 %, so the test passes with probability > 0.99. At a true Δ of 1 % it passes with probability ≈ 0.94.
- *Also reported (not decisive):*
  - the absolute direct-replay slip rate with its CI, against α and against 1.5α;
  - the same audit for COMP and CSF-1, and at α = 0.05 (secondary family H1-x, Holm).
- *Failure condition:* the CI\* **lower** limit of Δ is **> 0.02**. The physical slip rate then exceeds the
  guaranteed one by a practically relevant margin. This is reported as a headline negative ("the label guarantee does
  not transfer to the simulated outcome"), and no slip-rate guarantee is claimed for physical slip.
- If the CI straddles 0.02, the result is "not confirmed" and reported as inconclusive.

**H1 is confirmed iff H1-M passes and H1-V passes.**

**Design sketch:** labels for 8,000 in-distribution instances; the monotonicity grid; 2,000 direct replays for the
primary audit (+ 10,000 secondary audit replays). Baselines: none (validity claim). Ablation: none.

---

### H2 — At a matched guaranteed slip rate, touch lowers grip force relative to the best non-tactile conformal method (Gaps 2, 5; SQ3) — *primary comparative endpoint of the paper*

**Rationale.**
- Every conformal method meets α by construction, so the only open question is force.
- COMP already uses everything a robot knows without touch: mass, commanded disturbance, aperture, preload force and,
  for Mondrian-CSF, even privileged family ID. CertGrip adds pad readings at the lifted preload and during the probe.
- After lifting, the pad readings can reveal contact geometry and the gravity load of an off-centre CoM. They cannot
  reveal μ, because the probe is normal-only. They also cannot reveal the external disturbance amplitude.
- Whether that residual information is worth newtons depends on how much of Var(log F\*) it explains relative to the
  invisible terms (X7). We therefore also measure the **ceiling**.
- The outcome is genuinely uncertain. A tie is the headline negative that Gap 2 anticipates.

**Primary decision.**
- *Metric:* D = 1 − RE(CertGrip)/RE(COMP), pooled over the 2,000 test instances, at α = 0.10, with n_cal = 500 per
  stratum, in the main information condition (with mass).
- *Prediction [target]:* **D ≥ 0.10** (point estimate) **and** CI\* lower limit > 0.
  - **Robustness requirement:** both conditions also hold when F\*_lo and when F\*_hi replace F\*_mid as the
    reference (ε check, alternative mechanism (d)).
  - 0.10 is the smallest effect size of interest (SESOI). It is about the low end of the 9–30 % excess that a
    hand-set 20 % margin produces in `khamis2021real`. A smaller gain would not change a practitioner's choice of
    method.
- *Failure conditions (each reported as a negative result):*
  - **Equivalence (headline negative):** the CI\* for D lies entirely inside (−0.10, +0.10), a TOST at 0.0167 per side
    (X4). The report reads: "touch adds no practically relevant force efficiency at a guaranteed slip rate over the best
    non-tactile conformal method".
  - **Inferiority:** CI\* upper limit < 0. COMP is better.
  - **Otherwise** (e.g. 0 < D < 0.10 with lower limit > 0, or a CI straddling a margin): "not confirmed". The effect
    size is reported with its CI and no claim is made.
- *Power argument [assumption; pilot replaces]:*
  - Assume RE(COMP) ≈ 0.40 and an object-level SD of the paired difference σ_d ≈ 0.25, with 500 test objects. Then
    SE(D) ≈ 0.25/√500/0.40 ≈ 0.028.
  - At a true D = 0.15: P(D̂ ≥ 0.10) ≈ 0.96, and the lower limit is > 0 almost surely.
  - At a true D = 0: P(TOST equivalence) ≈ 0.85.
  - The minimum detectable D (80 %, one-sided 0.0167) ≈ 0.083.
  - **Pilot rule:** if the projected SE(D) is > 0.035, move objects from train to test (up to 175 test objects per
    family). If it is still > 0.035, the pre-registration states the reduced power.
- *Matched-rate condition:* both methods' realised label-rule test slip rates are reported. The paired RE comparison
  is valid as stated, since both use the same α, n and calibration draw. An **efficiency frontier** (RE against the
  realised slip rate over the α grid) is shown as a robustness figure (exploratory).

**What distinguishes the four mechanisms** (skeptic H2), all pre-registered:
- **(c) learner corrects the F_nom formula without touch:** CertGrip-P vs CSF-1. This is reported, and it is
  absorbed into COMP whenever CertGrip-P is selected.
- **(b) touch acts as a family/geometry-type identifier:** H4b (both arms given family ID) and the diagnostic D-FID.
- **(a) touch carries contact geometry / CoM information:** H4d (the F4 − F1 interaction) and the within-family
  estimates.
- **(d) label quantisation:** the F\*_lo/F\*_hi robustness requirement above. Log-bisection keeps this below 1 %.
- **Ceiling (X7):** an oracle CQR on privileged features (μ, amplitude, CoM offset, geometry parameters, mass).
  - Reported: the **gap closed** G = (RE_COMP − RE_CertGrip)/(RE_COMP − RE_oracle), and the leave-one-group-out R² of
    log F\* for each privileged group.
  - This shows how much of the result is set by the μ and disturbance ranges.

**Design sketch.**
- Data: the 8,000 in-distribution labels.
- Methods: CSF-1, Mondrian-CSF, CertGrip-P, CertGrip-S, CertGrip, the oracle ceiling, and for H4 CertGrip-shuffled
  and the +FID variants.
- Everything is trained and calibrated per α; tuning is equal for every input set.
- No extra simulation is needed beyond the labels; the H1-V audits cover the physical check.

---

### H3 — Calibration from binary slip feedback restores α under shift at a small force price relative to label-requiring recalibration (Gap 3; SQ5)

**Rationale.**
- Under monotonicity, slip_t = 1{F_t < F\*_t} (H1). The tracker therefore needs no F\* at deployment, and this is the
  only variant that can be deployed on a robot (§6).
- Its long-run slip rate is a theorem (UT4), and its drop cost is an identity (Δq/η). What is **not** known is how
  much force the deployable method gives up relative to an oracle that recalibrates with 500 F\* labels from the
  shifted distribution.
- Two forces pull in opposite directions:
  - the constant-step tracker's q oscillates around the shifted quantile, and because excess is convex in q, this
    costs force;
  - the oracle's quantile carries finite-sample noise at 125 objects per stratum.
- The net is unknown and depends on the score density near the quantile. It is the number a practitioner needs:
  "how much do I lose by learning from drops instead of measuring F\*?"

**Streams** *[design]*:
- T = 2,000 steps: 500 in-distribution steps, then 1,500 shifted steps, for S1, S2 and S3 (primary) and S1m
  (secondary). α = 0.10.
- The shifted segment is a random permutation of the 1,500 stream instances of that pool (375 objects). The
  pre-shift segment draws 500 in-distribution test instances from objects that are not in the shifted segment.
- **Orderings are Monte-Carlo replicates, not independent units** (skeptic H3.3, correlated streams):
  - each endpoint is averaged over 20 orderings;
  - the CI comes from an object-cluster bootstrap that resamples stream objects **and** oracle-calibration objects
    and regenerates the orderings. This is cheap because it replays labels.
- The post-transient window is stream steps 1,001–2,000, i.e. shifted steps 501–1,500. By the identity in §2, the
  expected catch-up for S1 is Δq/η ≈ 0.51/η slips spread over the first few dozen shifted steps *[assumption,
  location model]*.

**Primary decision.**
- *Metric:* for each primary shift s ∈ {S1, S2, S3}, the ratio
  R_E(s) = RE_window(OQT-CertGrip) / RE_window(Oracle-CertGrip) on identical stream instances.
- *Prediction [target]:* the CI\* upper limit of R_E(s) is **< 1.10 for all three shifts** (an intersection-union
  non-inferiority test).
  - The 10 % margin is set equal to H2's SESOI: the deployable method may lose no more force than the smallest gain we
    would count as worthwhile.
- **Co-requirement (matched rate):** in the same window, the label-rule slip rates of OQT and the oracle differ by
  ≤ 0.02. Otherwise the excess comparison is declared unmatched, and we report it only alongside its slip rates.
- **Physical co-check:** a direct-replay audit of 500 stream steps (steps 501–1,000) per shift for OQT-CertGrip, with
  Δ ≤ 0.02 by the H1-V rule (secondary H3-x).
- *Failure condition (negative result, per shift):* the CI\* **lower** limit of R_E(s) is **> 1.10**. Learning from
  drops then costs more than 10 % force relative to label-based recalibration under shift s. This is reported as
  "binary feedback suffices for validity but not for efficiency under s".
- If the CI straddles 1.10, the result is reported as inconclusive for s. H3 is confirmed only if all three shifts pass.
- *Power argument [assumption]:*
  - The oracle's quantile SE at 125 objects is ≈ √(0.09/125)/f. With a score density f ≈ 1.5 per log unit at the
    quantile, that is ≈ 0.018 in log-force, i.e. ≈ 2 % in RE.
  - The OQT oscillation adds ≈ √(η α(1−α)/(2f)) in q.
  - Expected CI\* half-width on R_E ≈ 0.04. A true ratio ≤ 1.04 then passes with high probability, and a true 1.06
    is borderline.
  - The pilot measures f and η and re-projects. If the projected half-width is > 0.06, the oracle-calibration share of
    each shift pool rises from 125 to 175 objects.

**Design sketch.**
- Data: 4 shift pools × 2,000 labelled instances.
- Online arms: OQT-CertGrip, OQT-COMP, decaying-step OQT-CertGrip, Frozen-CertGrip, Frozen-COMP,
  Oracle-CertGrip and Oracle-COMP.
- Direct-replay stream audit: 4 shifts × 2 methods × 500 steps.

---

## 4. Secondary hypotheses (Holm within each family; all share core runs)

Each item has a failure condition that is reported as a negative result if it is met.

### H1-x (validity details)
- **H1c — Do uncalibrated targeters miss α in practice? (Gap 1; demoted, made two-sided).**
  - *Metric:* \|slip_label − α\| at α ∈ {0.01, 0.05, 0.10, 0.20}, n_cal = 500, for RAW-Q, RAW-G and RAW-Qv.
  - *Prediction:* RAW-Q and RAW-G miss by a practically relevant amount: **\|slip − α\| ≥ 0.5α at α = 0.05**, with
    the CI excluding the ±0.5α region, in either direction (the skeptic's point about direction). For RAW-Qv **no
    direction is predicted**.
  - *Failure:* all three methods have CI\* inside ±0.25α at every α (TOST). Then Gap 1 is practically empty
    in-distribution. We report "a validation-tuned quantile suffices in-distribution", and the conformal guarantee
    is argued only for small n and for the shift setting (H3).
  - The small-n arm (n_cal = 50) is reported for all four α.
- **H1-V for COMP and CSF-1 and at α = 0.05:** the same rule as the H1-V primary decision.

### H2-x (efficiency details)
- **H2-T, tail non-inferiority (X4).**
  - *Metric:* 95th percentile of the relative excess.
  - *Prediction:* the CI upper limit of P95(CertGrip)/P95(COMP) is < 1.10.
  - *Failure:* the lower limit is > 1.10. The mean gain is then reported only together with its tail cost ("buys mean
    force with rare high forces").
- **H2-C, the Gap-2 classic:** D against CSF-1, and against Mondrian-CSF if it was not selected. Same SESOI and TOST
  rules as the primary decision.
- **H2-n, small calibration sets:**
  - D at n_cal = 50 for α ∈ {0.10, 0.20}, with the same calibration objects for both methods.
  - *Prediction:* lower limit > 0.
  - *Failure:* TOST equivalence at ±0.10.
  - At α = 0.01 with n = 50, both methods sit at the maximum score; this is reported, not tested.
- **H2-H, heterogeneity (replaces the "8 of 16 Holm-significant" rule):**
  - A random-effects estimate of D across the 16 family × disturbance cells: pooled D, τ, and 16 cell estimates with
    CIs.
  - *Prediction (safety guard):* **no cell where CertGrip is worse than COMP by more than 10 %**, i.e. no cell with a
    Holm-adjusted lower limit of −D > 0.10.
  - *Failure:* any such cell. It is named, and the efficiency claim is restricted accordingly.
- **H2-M, information sensitivity:** D repeated in the no-mass and mass-noise conditions, with COMP re-selected.
  There is **no directional prediction**. D and the sign of its change are reported.
- **H2-R, design-range dependence (X7):**
  - D recomputed on the nested sub-pools μ ∈ [0.5, 0.8] and amplitude in the middle 50 % of each range, with
    recalibration inside the sub-pool.
  - *Prediction:* none. This is a pre-registered **report** that, together with the oracle decomposition, tells
    readers how much of D the ranges set.

### H3-x (online details)
- **H3-B, offline breakage magnitude (replaces the near-trivial "breaks under S1/S3").**
  - *Metric:* frozen CertGrip's label-rule slip rate on each shift pool, compared with the slip rate the **location
    model** predicts: p_pred = 1 − F̂_ID(q̂ − Δ). Here F̂_ID is the in-distribution test-score CDF, Δ = 0.105 (S1m)
    and Δ = 0.511 (S1).
  - *Prediction:* \|p_obs − p_pred\| ≤ 0.02 (TOST) for S1m and S1. For S1m we additionally report whether p_obs
    exceeds the upper finite-sample edge; that is a genuinely uncertain outcome.
  - *Failure:* \|p_obs − p_pred\| > 0.02 with the CI excluding the margin. The friction shift is then **not** a pure
    location shift in this simulator. The likely causes are torsional or rotational slip modes and preload slips that
    change touch features, and diagnostic D-loc shows which.
  - For S3 and S2 we report p_obs with its CI. The predicted direction is "up" for S3. For S2 the test is two-sided:
    a break means \|p_obs − α\| ≥ 0.05 with the CI excluding the margin.
- **H3-L, location vs spread (H3.4 re-derived as the skeptic demands).**
  - *Metric:* ρ_s = log[RE_window(OQT-CertGrip) / RE_window(OQT-COMP)], compared with ρ_ID, the same log-ratio
    in-distribution.
  - *Prediction:*
    - **S1 (location): the advantage is preserved:** \|ρ_S1 − ρ_ID\| ≤ 0.05 (TOST). A tracker supplies the global
      rescale, and per-grasp prediction keeps its residual-spread advantage, so "touch cannot see μ" is irrelevant
      after adaptation.
    - **S2 and S3 (spread-changing): no direction.** Two-sided, reported with CIs, alongside the post-shift score SD
      for each method, which is the mechanism measurement.
  - *Failure:* the S1 CI excludes ±0.05. The advantage is then not preserved under a friction shift. The cause is
    reported via D-loc and D-μ.
  - If H2 found D ≈ 0, preservation is trivial. The test is still run, but it is labelled uninformative.
- **H3-S, step-size schedule within OQT (deconfounded):**
  - *Comparison:* constant η vs decaying η on the same score space.
  - *Prediction:* decaying η spends **more** catch-up drops under the abrupt shift at t = 500, i.e. a larger
    cumulative (slip − α) over shifted steps 1–500.
  - *Failure:* the CI upper limit of the difference is ≤ 0.

### H4-x (value of touch; Gap 5)
- **H4a, static vs probe.**
  - *Prediction:* D(CertGrip-S vs CertGrip-P) ≥ 0.05, and D(CertGrip vs CertGrip-S) ≥ 0.03, each with lower limit > 0
    *[targets]*.
  - *Failure:* TOST equivalence within ±0.05 / ±0.03. The probe-specific claim is then dropped.
- **H4b, identifier control (X5-iii).**
  - *Metric:* D_FID = 1 − RE(CertGrip+FID)/RE(CertGrip-P+FID), i.e. both arms are given family ID.
  - *Prediction:* D_FID ≥ 0.5·D.
  - *Failure:* D_FID is equivalent to 0 within ±0.05. Touch is then acting as a family identifier in MuJoCo, and the
    "tactile" framing is replaced by "learned + calibrated".
- **H4c, shuffled-touch control.**
  - *Setup:* touch features are permuted across objects within the stratum.
  - *Prediction:* RE is equivalent to CertGrip-P within ±0.05 (TOST).
  - *Failure:* the shuffled arm beats CertGrip-P by > 5 %. That indicates a capacity or tuning artefact, and every
    touch gain is then discounted by it.
- **H4d, CoM mechanism.**
  - *Prediction:* the interaction D_F4 − D_F1 > 0 with lower limit > 0, as F4 has the large CoM-offset range.
  - *Failure:* the CI upper limit is ≤ 0, so the pressure-centroid/CoM story is refuted.
  - The proposer's "centred grasps" wording is dropped: every family has random offsets.

### Pre-registered diagnostics (no thresholds to pass; they condition interpretation)
- **D-μ, does touch see friction?** Cross-validated R² of log μ regressed on touch + probe features (train objects).
  The interpretations of H3-L and H2 assume R² ≤ 0.05 *[assumption]*. If R² is higher, we say touch partially sees
  friction (e.g. via preload shear), and the S1 prediction is reinterpreted.
- **D-FID, does touch identify the family?** Family classification accuracy from touch-only features, against a
  chance level of 25 %.
- **D-loc, is S1 a location shift?** Over the paired S1 instances: the SD of log F\*_S1 − log F\*_ID (Coulomb
  predicts 0, with mean 0.511), and the mean \|Δĝ\|/ĝ caused by changed touch features. Preload-slip rates are
  reported per pool.
- **Oracle variance decomposition** (H2 ceiling).

---

## 5. Exploratory (labelled; no correction; one figure at most)
- **E1, Gap 6:** per-group label-rule slip rate (μ tertile, CoM-offset tertile, mass tertile, family) under marginal
  calibration. Mondrian calibration (`ding2023class`) is run if a group exceeds 2α; this is data-dependent and
  labelled as such.
- **E2:** ACI (`gibbs2021adaptive`) vs OQT at a matched effective step (γ mapped through the score density at the
  quantile), including how often ACI saturates.
- **E3, correlated streams:** each object grasped 4 times consecutively (its 4 instances in a row). We report the
  window slip rate and oscillation. The theory covers arbitrary sequences only for the long-run average, and
  non-exchangeable data are a known limitation (`farinhas2023non`).
- **E4, gradual drift:** an ID → S1 mixture whose weight ramps linearly over steps 500–1,500. This is a mixture drift,
  not a continuous friction change, and it is stated as such.
- **E5, hardware calibration routes (§6):**
  - (a) **warm-up-then-freeze:** OQT run over N ∈ {50, 150, 500} calibration grasps with binary feedback only, then q
    frozen. Its test slip rate and RE are compared with split conformal.
  - (b) **ramp-down F\* estimate:** for D4 and slow-D1 instances, hold the object and ramp the force down until slip
    onset in a single replay. Its agreement with bisection F\* is reported (2,000 replays).
- **E6, slip-threshold sensitivity:** δ_t ∈ {1, 2, 4} mm on the H1-M subsample.
- **E7, efficiency frontier figure** (§3 H2).

---

## 6. How calibration would be obtained on hardware (decided, with limitations)
1. **Deployable path = H3.** OQT needs only the binary slip outcome. On a robot it is warm-started from the
   sim-calibrated q̂ (or from q₁ = 0 when no sim prior is trusted) and converges at the cost of Δq/η extra drops
   (identity UT4). This is the contribution that transfers. Its cost in drops per shift is reported in C2.
2. **Offline split-conformal CertGrip is a simulation-calibrated object.** On hardware F\* is not measurable for
   dynamic disturbances (non-replayable, about 10 drops per grasp). We state this as a limitation and **do not claim**
   a hardware offline guarantee.
   - Two routes are evaluated in simulation only, as exploratory: warm-up-then-freeze (E5a), whose validity is the
     long-run average during warm-up rather than a split-conformal guarantee, and ramp-down estimation of F\* for
     quasi-static disturbances (E5b).
   - **Rejected as primary:** calibration from one binary outcome per grasp (the skeptic's interval-censored option).
     Conformal risk control (`angelopoulos2022conformal`) needs each calibration point's loss at every λ, and one
     outcome at one force does not provide it. A censored-likelihood estimator would not be distribution-free, which
     is the property the paper is about.
3. **Cost of learning from drops.** The long-run rate commits the robot to α·T drops plus Δq/η catch-up drops. The
   paper states this explicitly and limits deployment to objects that can be dropped safely (limitation).

---

## 7. Budget (≈ 100 CPU-h) and downscale order

Assumption: **c = 1 CPU-s per replay** *[assumption; the pilot times it on the runner image]*.

| Item | Replays | CPU-h at c = 1 s |
|---|---|---|
| In-distribution labels: 8,000 × 11 | 88,000 | 24.4 |
| Shift labels: 4 pools × 2,000 × 11 | 88,000 | 24.4 |
| H1-M grid: 800 × 35, plus 3 × 100 × 35 descriptive shift grids | 38,500 | 10.7 |
| H1-V and secondary offline audits: 2 α × 3 methods × 2,000 | 12,000 | 3.3 |
| Stream audits: 4 shifts × 2 methods × 500 | 4,000 | 1.1 |
| E5b ramp-down | 2,000 | 0.6 |
| Training, conformal, bootstraps, stream replays (no simulation) | — | ≈ 3 |
| Pilot (stage 10/12) | — | ≈ 5 |
| **Subtotal** | | **≈ 72.5** |
| Slack (25 %) | | ≈ 18 |
| **Total** | | **≈ 90** |

If H1-M fails, the risk-control fallback (20-point λ-grid × 2,000 calibration instances ≈ 11 CPU-h) is funded from the
slack plus downscale step 1.

**Downscale order.** These steps are applied in sequence until the projected total is ≤ 95 CPU-h. The savings are
estimates at c = 1 s and scale with c.

| Step | Action | Saves | What it costs scientifically |
|---|---|---|---|
| 1 | Drop E5b and E6, and the descriptive shift monotonicity grids | ≈ 3.5 h | Exploratory items only |
| 2 | Bisection 10 → 8 halvings (relative bracket ≈ 2.7 %, still conservative via F\*_hi). The robustness check with F\*_lo/F\*_hi keeps (d) honest. | ≈ 31 h × 2/11 ≈ 8.8 h | Coarser labels |
| 3 | Shift pools 500 → 300 objects (oracle 100 / stream 200). Streams shorten to 1,000 shifted steps. | ≈ 16 h | Wider H3 CIs; re-project power |
| 4 | Drop the S1m pool (H3-B then tests S1 only) | ≈ 3 h (after step 3) | Loses the genuinely uncertain breakage test |
| 5 | In-distribution 500 → 400 objects per family (test stays ≥ 100 objects per family) | ≈ 6 h | SE(D) rises to ≈ 0.031 [assumption] |
| 6 | H1-M grid 35 → 25 points (keep the dense local 10) | ≈ 2 h | Coarser global grid |
| 7 | Shorten the disturbance window | variable | **Changes the task.** Last resort, and stated in the paper. |

- **Never cut:** the H1-M in-distribution sample of 800, the H1-V primary audit, test objects below 100 per family, or
  any of S1/S2/S3.
- If step 7 is insufficient, the study is retargeted per the stage-1 constraint rather than run underpowered.

---

## 8. What the pilot (stages 10/12) must settle before the pre-registration freeze, in this order
1. **Replay cost c and determinism (UT6)** on the Actions runner image. These decide the downscale step.
2. **Slip metric**: δ_t, the rotation threshold and UT9, frozen **before** any monotonicity data. Also a pilot-scale
   monotonicity look on about 100 pilot instances. If the design will clearly fail H1-M, switch to the risk-control
   design before freezing.
3. **F_max / m_max** so that UT8 (≤ 1 % unavoidable) holds in S1 and S3; the rate of preload slips under constant F₀.
4. **touch_grid channels** available in the pinned version (normal only vs + tangential). This determines whether
   H4d is plausible.
5. **Variance inputs for power:** RE(COMP), σ_d, and the score density f at the 0.9 quantile, which also fixes η
   through the calibration-score IQR. The power projections in H2 and H3 are recomputed, and the object counts are
   adjusted by the stated rules.
6. Preliminary **D-μ** and **D-loc** values on pilot objects. These tell us whether the H3-L "location" premise is
   credible. They do not change the thresholds.

---

## 9. Critique → resolution

| # | Skeptic point | Resolution | Status |
|---|---|---|---|
| X1a | Label-based validity is circular | Label-based validity is now unit test UT3. The empirical validity claim is H1-V, a paired direct-replay disagreement test. | **Adopted** |
| X1b | Audit underpowered, especially at α = 0.01 | The paired disagreement Δ (tolerance 0.2α) is powered independently of the slip count. Power is stated (§3 H1-V). | **Partly adopted.** We use a more powerful paired design instead of an absolute 1.5α test; the absolute rate is still reported. |
| X1c | Bisection assumes monotonicity; H1a cannot see islands below F\*_lo | H1-M uses a bracket-independent definition on a global grid plus the bisection points; UT5 checks the bracket ends | **Adopted** |
| X2a | Clustered instances break the Beta band | Calibration is stratified by disturbance type. One instance per object per stratum gives object-level exchangeability. | **Adopted** |
| X2b | Overlapping re-draws invalidate the 8 %-of-200 rule | The Beta-band population claim is dropped. Re-splits are i.i.d. draws **conditional on the pool**, and pool-conditional coverage is exactly bounded by the permutation argument, so Monte-Carlo SE is valid for that estimand (UT3). | **Partly adopted.** The overlap does not invalidate pool-conditional Monte-Carlo error. |
| X3a | Thresholds not derived from variance | Each core threshold is tied to a SESOI or tolerance, with an explicit power calculation under labelled assumptions and pilot re-projection rules | **Adopted** |
| X3b | No multiplicity plan | Bonferroni across 3 cores (96.7 % CI\*), intersection-union within cores, Holm within secondary families, exploratory uncorrected; UT3 uses FWER over cells | **Adopted** |
| X3c | Fixed sequence H1a → H2 → H3 → H4 | H1-M is kept as a design gate. H3 is **not** gated on H2, because they are logically independent and a fixed sequence would let an H2 negative silence C2. | **Partly adopted** |
| X4 | Null and non-inferiority claims rest on "CI includes 0" | Every "no difference" claim now has a TOST margin: H2 ±0.10, H2-T 1.10, H3 1.10, H3-B ±0.02, H3-L ±0.05, H4 ±0.05/±0.03, H1c ±0.25α | **Adopted** |
| X5-i | Penetration counted as slip | Tangential-only metric plus UT9 | **Adopted** |
| X5-ii | condim, cone, solref differ by family | UT7 asserts they are identical; F5 uses the same primitives, and meshes are dropped | **Adopted** |
| X5-iii | Touch acts as a family identifier | D-FID diagnostic plus the H4b control with family ID in both arms; Mondrian-CSF gets family ID | **Adopted** |
| X5-iv | Does touch see friction? | Diagnostic D-μ with an interpretive threshold of R² ≤ 0.05 | **Adopted** |
| X6a | "Just conformal prediction" | Guarantees are demoted to unit tests. The contributions are the measured premise, the matched-α force cost against a fair comparator with a ceiling, and the deployable binary-feedback path with its measured price (§0). | **Adopted** |
| X6b | Offline method not deployable on hardware | §6: the offline method is stated as sim-calibrated; the online path is the deployable one; two hardware routes are explored (E5) | **Adopted** (as a limitation plus exploratory checks) |
| X6c | Calibrate from one binary outcome per grasp | Risk control needs the full loss curve per point, and a censored likelihood is not distribution-free | **Rejected** as the primary route (reason in §6) |
| X6d | Learning from slips means drops | Drops = αT + Δq/η, an identity (UT4); reported per shift; safe-to-drop limitation | **Adopted** |
| X7a | Gain set by the μ and disturbance ranges | Oracle ceiling, gap-closed G, leave-one-group-out R², nested-range re-analysis H2-R | **Adopted** |
| X7b | Cite a source for each range | The synthesis contains no numeric range sources, and inventing citations is prohibited. The ranges are stated as design choices, and their influence is measured instead. | **Rejected** (citation constraint) |
| H1a-1 | Grid sparse near F\* | Dense local grid of 10 points on [F\*_hi, 1.5 F\*_hi] | **Adopted** |
| H1a-2 | Shift-pool clause not budgeted | 3 × 100 descriptive grids, budgeted (10.7 h line), no gate | **Adopted** |
| H1a-3 | Slip metric must be frozen first | Pilot item 2, before any monotonicity data | **Adopted** |
| H1a-4 | Decision rule needs a CI side | One-sided 98.3 % CP upper limit ≤ 2 %, i.e. ≤ 7/800; power stated | **Adopted** |
| H1a-5 | Per-family 3 % rule underpowered | Per-family rates are descriptive; a flag at > 5 % switches that family to direct-replay-only validity | **Adopted** |
| H1a-6 | Metric may be too lenient | Max-displacement distribution at F_max, near-miss rate, δ sensitivity (E6) | **Adopted** |
| H1b | A theorem, not a hypothesis | Moved to UT3 with a cluster-aware design and FWER | **Adopted** |
| H1c-1 | Near-trivially true | Demoted to secondary | **Adopted** |
| H1c-2 | Asymmetric falsification | Symmetric rules: a miss ≥ 0.5α vs equivalence within ±0.25α | **Adopted** |
| H1c-3 | Wrong direction risk | Two-sided | **Adopted** |
| H1c-4 | Missing validation-tuned RAW-Q | RAW-Qv added, with no directional prediction | **Adopted** |
| H1c-5 | No effect size | \|slip − α\| ≥ 0.5α | **Adopted** |
| H2-1 | Relative vs absolute metric ambiguous | Primary = mean relative excess, ratio-of-means D; absolute is secondary | **Adopted** |
| H2-2 | Quantisation as large as the effect | Log-bisection (≈ 0.7 % relative); robustness check with F\*_lo/F\*_hi is a confirmation requirement | **Adopted** (with log-bisection instead of a minimum F\*) |
| H2-3 | "Mass is conservative" unsupported | Claim withdrawn; no-mass and noisy-mass conditions added (H2-M) | **Adopted** |
| H2-4 | Mass unavailable on hardware → drop it | Main analysis keeps mass, justified by weighing during the 5 mm lift (stated assumption), because the formula baselines are meaningless without it. No-mass is a pre-registered secondary. | **Partly adopted** |
| H2-5 | One-parameter CSF is a strawman | COMP = the better of Mondrian-CSF (with privileged family ID) and CertGrip-P, chosen on the selection split | **Adopted** |
| H2-6 | Disturbance information unspecified | Information table §1.3: type and self-generated amplitudes given; external amplitudes hidden | **Adopted** |
| H2-7 | Alternative mechanisms (a)–(d) | Each has a pre-registered discriminating measurement (§3 H2) | **Adopted** |
| H2-8 | 15 % / 5 % not derived | SESOI 0.10 justified, with power and pilot rule | **Adopted** |
| H2-9 | The 8/16 Holm rule is a power artefact | Replaced by a random-effects estimate and a no-harmful-cell guard (H2-H) | **Adopted** |
| H2-10 | Tail needs a non-inferiority margin | H2-T: P95 ratio < 1.10 | **Adopted** |
| H2-11 | Small n needs the same calibration draw | Stated (§1.5, H2-n) | **Adopted** |
| H3.1-1 | S1/S3 breakage trivial by Coulomb | "Breaks" demoted to H3-B, which tests the location-model magnitude rather than the direction | **Adopted** |
| H3.1-2 | Add a mild shift | S1m (μ × 0.9) | **Adopted** |
| H3.1-3 | Pre-register magnitudes | p_pred from the in-distribution score CDF, ±0.02 | **Adopted** |
| H3.1-4 | S2 needs a magnitude | \|slip − α\| ≥ 0.5α | **Adopted** |
| H3.2-1 | Excluding cap-binding streams conditions on the outcome | No exclusion; anti-windup rule; unavoidable slips counted; UT8 keeps the cap rare | **Adopted** (with an anti-windup design decision added) |
| H3.2-2 | Bound may be vacuous | Numeric bound printed per stream (UT4b) | **Adopted** |
| H3.2-3 | Reclassify as a unit test | UT4 | **Adopted** |
| H3.3-1 | Transient is arithmetic (Δq/η) | Stronger than the skeptic: catch-up drops are an exact identity, so this is a unit test plus reported drops, and **not** a hypothesis. The empirical content (Δq) sits in H3-B. | **Adopted** |
| H3.3-2 | Inconsistent "60 vs 50" arithmetic | The criterion is removed. Drops are reported as αT + Δq/η, unambiguously. | **Adopted** |
| H3.3-3 | "Within ±0.05 in ≤ 400 steps" is vague and noise-met | Replaced by a sustained re-entry time (200 consecutive steps), reported descriptively | **Adopted** |
| H3.3-4 | η has no formula | η = 0.1 × IQR of calibration scores | **Adopted** |
| H3.3-5 | ACI vs decaying OQT confounded | H3-S compares within OQT; ACI vs OQT at matched step is exploratory (E2) | **Adopted** |
| H3.3-6 | Correlated orderings counted as units | Orderings are averaged; inference by object-cluster bootstrap that regenerates streams | **Adopted** |
| H3.4-1 | S1 asymmetry mis-derived | Re-derived: preservation is predicted under S1 (H3-L, TOST ±0.05) | **Adopted** |
| H3.4-2 | S2 sign at risk | S2 is two-sided with no direction | **Adopted** |
| H3.4-3 | Test location vs spread | Post-shift score SD per method, plus D-loc | **Adopted** |
| H3.5-1 | 20 % threshold arbitrary | Now the H3 primary decision with a 1.10 margin tied to H2's SESOI | **Adopted** |
| H3.5-2 | Oracle instances must be disjoint | 125 oracle objects disjoint from 375 stream objects; UT1 | **Adopted** |
| H3-g1 | Online validity circular on labels | Direct-replay stream audit (500 steps × shift × method) | **Adopted** |
| H3-g2 | i.i.d. streams are the easiest case | Stated as a limitation; correlated-stream exploratory E3 | **Partly adopted** (exploratory, not confirmatory, because of budget and page limit) |
| H4-1 | Preload timing may hide the CoM | Constant F₀ with a quasi-static 5 mm lift before reading; table-supported preload excluded | **Adopted** |
| H4-2 | F4 claim needs an interaction test | H4d: D_F4 − D_F1 with CI | **Adopted** |
| H4-3 | "Centred grasps" contradicts the randomised offsets | Wording dropped | **Adopted** |
| H4-4 | Equal tuning effort | Identical 30-config grouped-CV search per input set | **Adopted** |
| H4-5 | Shuffled-touch control | H4c | **Adopted** |
| H4-6 | Family-ID confound | H4b and D-FID | **Adopted** |
| H4-7 | Mixed margin and significance test | TOST throughout | **Adopted** |
| G6 | Mondrian-if-2α is data-dependent | Labelled exploratory (E1) | **Adopted** |
