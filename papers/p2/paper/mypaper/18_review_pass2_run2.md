# p2 · Stage 18 PEER_REVIEW pass 2, run 2: "Probe, Then Certify" (revised draft)

Fresh-context review. System prompt: `prompts/stage18_pass2_system.txt`. User message: `prompts/stage18_pass2_user.txt`
(read in full: the draft at lines 64–297, the evidence block (a)–(d)). Reviewer A is an RSS reviewer who works on tactile
manipulation and grip control. Reviewer B is an RSS reviewer who works on conformal prediction and statistical safety.
The venue is RSS 2027 (Stage 1 extended abstract, condensed from this master draft). The length check below follows
the NeurIPS/ICML thresholds as the prompt states them; significance is judged for RSS.

---

## CRITICAL_FABRICATION: **no**

Reasons:
- **Trial and instance counts match the raw files.** I counted 8,000 unshifted in-distribution label rows, split
  train 2,400 / select 800 / cal 2,000 / test 2,800. Calibration has 500 per stratum and test has 700 per stratum. There
  are 4,800 CRC replay lines, each with 20 grid points, for 14 arms. The bootstrap uses 2,000 draws, the H3 study 20
  orderings, and seeds 0–4 have 5 prediction files each. Streams have 2,096 (id) and 1,500 (S2) instances. The paper
  states no trial count that differs from any of these.
- **Headline numbers recomputed independently.** I wrote my own CRC loop over `results/v1/crc/*.jsonl` and the
  labels, without importing `analysis_crc.py`. It gives H2a D = 0.4168, H2b D = 0.0569 and H4e D = −0.0534. It also
  reproduces the σ curve (0.6789 / 0.5825 / 0.4168 / 0.1401), the seed range 0.3932–0.4494, every per-stratum λ̂ index
  and every per-stratum test slip rate. On `crc_v2` it gives the 08e values 0.4289 and 0.0240.
- **Every statistical procedure the paper names exists in code.** These are the Clopper–Pearson limit
  (`analysis_h1m.py`), the object-cluster bootstrap with λ̂ recomputed per draw (`analysis_crc.py`, `h3_streams.py`),
  TOST via the CI-inside-margin rule, and the random-effects pooling (sec08g).
- **The method equations match `code/certgrip/*.py` and `analysis_crc.py`.** This covers the monotonisation, the
  (nR+1)/(n+1) rule, the score, OQT with anti-windup, decaying η/√(n_u+1), the μ̂ clip and the CSF formulas.
- **All 52 `\cite` keys appear in `docs/05_knowledge_cards.json`.**
- **The errors I found are wording and method-description errors, not invented results.** They are listed below:
  the abstract names the wrong comparator, the F4 CoM description is likely wrong, and the Table 2 caption is
  inaccurate.

---

## Spot-checks (36; ✓ = matches, ✗ = discrepancy)

Recomputation scripts are in my scratch space (`crc_check.py` plus inline snippets). No repository file was modified.

| # | Claim in draft | Source checked | Result |
|---|---|---|---|
| 1 | H2a D = 0.4168, CertGrip-full RE 0.4567, CSF-1 RE 0.7832 | own CRC loop on crc/*.jsonl + labels | ✓ 0.4168 / 0.4567 / 0.7832 |
| 2 | Physical test slip 0.0829 (CertGrip) / 0.1021 (CSF-1) | own loop | ✓ |
| 3 | Per-stratum slip CertGrip 0.0871/0.0714/0.0757/0.0971; CSF-1 0.1157/0.0886/0.1057/0.0986 | own loop | ✓ |
| 4 | λ̂ index 0 in D1/D2 for CSF-μ̂@0.2; index 1 for CSF-1 | own loop | ✓ (CSF-μ̂@0.0/0.1 also 0; @0.4 index 2) |
| 5 | CSF-μ̂@0.2 RE 0.4843, slip 0.0657 (D1 0.0586, D2 0.0386) | own loop | ✓ |
| 6 | H2b (08c) D = 0.0569 [−0.0399, 0.1454] | own loop (point); crc_analysis.json (CI) | ✓ |
| 7 | Onset-only RE 0.4336, slip 0.0857, H4e D = −0.0534 | own loop | ✓ |
| 8 | σ curve D(H2a) 0.6789 / 0.5825 / 0.4168 / 0.1401; σ\* = 0.4; lower 0.0832 at σ 0.4 | own loop + crc_analysis.json | ✓ |
| 9 | Seeds 1–4, 08c D 0.3932–0.4494 | own loop (0.4343, 0.4197, 0.3932, 0.4494) | ✓ |
| 10 | 08e: H2a 0.4289, H2b 0.0240 | own loop on crc_v2 | ✓ |
| 11 | F\*_lo / F\*_hi robustness 0.4150 / 0.4186 | crc_analysis.json | ✓ |
| 12 | Label route H2a 0.4292 [0.3654, 0.4822]; seeds 0.4145–0.4442; H2b 0.0134; H4e −0.0417 | h2_label_rule.json | ✓ |
| 13 | Label route H2b by σ: −0.2022, −0.0753, 0.3275 | h2_label_rule.json | ✓ |
| 14 | COMP selection: 0.7686 / 0.8294 / 0.8335 | comp_selection.json | ✓ |
| 15 | Splits 0–149 / 150–199 / 200–324 / 325–499; n = 500 per stratum; 2,800 test | `certgrip/data.py` split_of; label rows | ✓ |
| 16 | No unavoidable instances in cal/test | label rows | ✓ (2 unavoidable id rows, both train: F3 #31 D3, F4 #43 D3; see A-m3) |
| 17 | Bracket width ≈ 0.7 %, 11 replays | label rows (median 0.68 %; 7,998 rows with 11 replays) | ✓ |
| 18 | Detector at σ 0: r = 0.948, bias +0.319, SD 0.110, found 100 % | recomputed from label rows | ✓ |
| 19 | Displacement at onset: median 0.126, p95 0.254, max 1.924 mm | recomputed | ✓ |
| 20 | μ independent of non-tactile inputs | `sim.py` sample_instance; corr(log μ, log m) = 0.007; family geometric-mean μ 0.534–0.547 | ✓ |
| 21 | F₀ = 32.7 N; squeeze 0.3 s; probe 0.25 s to 0.005 F₀; 500 Hz; w 6, k 8, consec 2, ½ rate, r_arm 0.1, n_min 1 mN; return 0.02 s + hold 0.1 s | `sim.py` RD2, `_rd_touch_probe`, `run` | ✓ (the "stick-phase rise" is the *commanded* log-rate s, not a measured rise; wording only) |
| 22 | Taxel noise 0.05 / 0.002 N / gain 0.10, applied only in the detector; static/squeeze features noise-free | `sim.py` `_noisy_ratio`, `run(record)` | ✓ |
| 23 | D1/D2 as inertial pseudo-force on a still hand; D3/D4 ramped over 0.1 s | `sim.py` `_dist_apply` | ✓ |
| 24 | F5 box half-size 2–5 mm, F3 capsules, no ellipsoids | `sim.py` | ✓ |
| 25 | F4: "non-colliding sphere carries half the mass and shifts the CoM" | `sim.py` build_xml | ✗ likely: every body has an explicit `<inertial pos="0 0 com">`, which in MuJoCo overrides the geom-derived mass and CoM, so the sphere probably does not shift the CoM. The CoM is the sampled `com` (±60 % for F4) |
| 26 | Learner search space (lr, max_iter, leaves, min_samples_leaf, l2), 30 configs, 4-fold GroupKFold | `certgrip/models.py` | ✓ |
| 27 | CSF-1 / CSF-μ̂ formulas, μ̄ = √0.3, μ̂ clip [0.1, 3] | `certgrip/baselines.py` | ✓ (a_cmd = 0 for D3/D4, so CSF-μ̂ uses m g/(2μ̂) there; the paper's single formula is implicitly right) |
| 28 | η = 0.03412 = 0.1 × IQR of cal scores | recomputed from a010_full_rd_s0.2_seed0 preds + labels | ✓ 0.034125 |
| 29 | OQT decaying step η/√(n_u+1), anti-windup | `certgrip/conformal.py` + h3_streams.py | ✓ (the conformal.py docstring says η/√t, but the code and the paper agree) |
| 30 | H1-M 8/800, CP upper 0.02115, 7 of 8 in D2, id max 0.00225, shift max 0.00904 | h1m_analysis.json; scipy beta.ppf(0.9875, 9, 792) = 0.021147 | ✓ |
| 31 | H1-V Δ from −0.00429 to −0.00143 | h1v_analysis.json | ✓ |
| 32 | H2-H τ 0.0511, Q 31.04; D3 cells 0.2979/0.3868/0.3115/0.3348; all lower limits > 0.16 | sec08g.json (min lower 0.1602) | ✓ (passes by 0.0002) |
| 33 | H2-R −0.2614 [−0.5320, −0.0325], n 352/548; H2-T 0.5918; oracle share 0.5172; H2-n 0.4146 / 0.4654 | sec08g.json, sec08f_tail.json | ✓ |
| 34 | Table 3 (all 21 cells), S1m R_E 0.8871 and diff 0.0248, physical audit 0.103/0.092/0.101, matched diffs 0.032/−0.035/0.009 | h3_analysis.json | ✓ |
| 35 | H3-S ΔC 58.15 / 42.40 / 2.90 / 2.75; H1c ranges; D-μ values; D-FID 0.7257; H4b 0.4638 vs 0.4555; no-mass 0.4598 (change 0.0042); mass-noise 0.4603, COMP RE 0.7991 | sec08h_*.json, sec08f_*.json | ✓ |
| 36 | **Abstract: "adding the onset gives D = 0.4739 against the proprioceptive arm"** | h4a_label_rule.json | ✗ 0.4739 is CertGrip-full **vs `full`** (P + static touch + squeeze). Against P the value is 0.4555 (sec08f_label / sec08h_h4b) |

Further observations from the raw files:
- The stored static-touch statistics show a normal sum of exactly F₀ = 32.7 N and a shear sum of m g/2 on each pad (for
  example, F1 object 0: 0.257 N = 0.0524 · 9.81/2). Static touch is therefore a pure function of mass in this simulator.
- The preload-slip flag is 0 on every instance in every pool (sec08g D_loc). The feature is constant.
- The OQT trackers are warm-started from the *label-route* q̂ (`h3_streams.offline`), not from the CRC λ̂.

---

## 1. Topic adherence

The paper stays on the stated topic. The sections, in order, cover the probe, CRC on the physical slip loss, the
comparison with the strongest non-tactile conformal baseline, the attribution ablations and the online binary-feedback
study. Environment issues are not presented as contributions. The compute paragraph and the "Deviations" list report
infrastructure facts honestly and do not claim them as contributions. Two places lean towards self-description of the
pipeline rather than science: the 08c/08e/08f–08h addendum identifiers in the main text, and the long deviation list.
These are fine for a master draft but should be compressed for RSS.

## 2. Methodology–evidence consistency

Nearly everything is consistent, as the spot-checks show. Four discrepancies need fixing, plus two clarifications:
1. **Abstract, comparator mislabelled** (✗36). "D = 0.4739 against the proprioceptive arm" should say "against the
   static-touch-plus-squeeze arm (`full`)". If the authors want the comparison with P, the value is 0.4555.
2. **Table 2 caption.** It says "The H4a, H4c and H4b rows are comparisons along the learned feature chain against P".
   Only S-vs-P, H4c and H4b are against P. The full-vs-S row and the CertGrip-full-vs-full row are not.
3. **F4 composite** (✗25). Each body has an explicit `<inertial>` element, so in MuJoCo the sphere's `mass` attribute
   and position most likely do not affect the dynamics. F4 is then effectively a box whose CoM offset range is larger
   (±60 %). Either verify on the compiled model (`m.body_ipos`) or reword. This matters for how H4d is interpreted
   (the CoM test is inconclusive).
4. **"Stick-phase rise"** (21). The detector compares the 8-frame rise of log r with half of the *commanded* log-force
   rate s. It does not compare with a measured stick-phase rise. A one-word fix.
5. **Clarification: OQT warm start.** "initialised at the stratum's offline q̂" should say that this is the label-route
   q̂, because the primary offline route is CRC.
6. **Clarification: static touch.** State that the simulated static touch reads exactly F₀ (normal) and m g/2 (shear),
   so S ≡ P + mass, which P already has. H4a's "equivalence" is then a consistency check of the simulator, not an
   empirical finding (see A-W3).

No claimed statistical test is missing from the code. No number in the paper is absent from the results.

## 3. Trial count

The paper makes no "N independent trials" claim that contradicts the evidence. All counts it does state (n = 500 per
stratum, 2,800 test, 800 H1-M instances, 2,000 bootstrap draws, 20 orderings, seeds 0–4, 1,000 UT3 re-splits) match
the raw files. **No critical trial-count fabrication.**

## 4. Length

| Section | Words | Threshold | Status |
|---|---|---|---|
| Abstract | ≈ 345 | ≥ 150 | OK (too long for RSS; aim for ≤ 200) |
| Introduction | ≈ 1,150 | ≥ 700 | OK |
| Related Work | ≈ 600 | ≥ 500 | OK |
| Method (§3) | ≈ 2,060 | ≥ 800 | OK |
| Experiments (§4) | ≈ 1,400 | ≥ 600 | OK |
| Results (§5) | ≈ 2,460 | ≥ 500 | OK |
| Discussion + Limitations + Conclusion | ≈ 1,660 | — | OK |
| **Total** | **≈ 9,700** | ≥ 4,000 | Not under-length. **Over-length** for 9 pages and far over an RSS Stage 1 extended abstract |

No section is too short. The real risk is the opposite: the condensation for RSS must cut roughly 60 %. It should keep
H2a, the attribution in one table, H2-R and the online rescue, and move the 08c/08e bookkeeping to an appendix.

---

## Reviewer A: RSS, tactile manipulation and grip-force control

**Summary.** After a fixed preload and squeeze, the gripper ramps its force down until a touch-only detector flags
incipient slip. The onset force feeds a quantile regressor or a Coulomb plug-in, and CRC on the physical binary slip
loss sets a per-disturbance force multiplier. In MuJoCo the probe arm needs 42 % less relative excess force than a
friction-blind calibrated physics formula. The learned model is no better than the plug-in using the same onset, and
online quantile tracking repairs frozen calibration under friction and amplitude shifts.

### Strengths
- **A1. A clean, fair comparison protocol.** Every arm runs the same physical history, the probe included. The
  comparator was selected on a disjoint split before test. Calibration is to the same α. This is the right way to ask
  "what does touch buy you once everyone is calibrated?" Tactile grip papers rarely do it.
- **A2. Honest negative results.** H2b is not confirmed, so learning on top of the onset buys nothing at σ = 0.2. The
  method loses in the narrow-friction sub-pool (D = −0.26). Frozen calibration does not fail under the new family, and
  H3 is inconclusive with an unfavourable direction in S2. The paper reports all of these prominently.
- **A3. Disclosure of simulator assumptions.** The draft states that μ is independent of every non-tactile input, that
  the static and squeeze features are noise-free, that the detector reads saturation of the shear/normal ratio rather
  than a partial-slip annulus, and that disturbances act on a still hand. The intrinsic detector error (r = 0.948, SD
  0.110) is reported, which I verified.
- **A4. A gentle probe in simulation.** Onset was found on 100 % of instances, with median displacement 0.126 mm and
  no instance at 2 mm.

### Weaknesses
- **A-W1. The main result is close to true by construction.** In rigid MuJoCo contact the shear/normal ratio saturates
  exactly at μ, so the detector is an idealised Coulomb-cone reader. The ramp-down onset force is essentially a direct
  measurement of the static holding force m g/(2μ). It is not merely "a friction reading". The no-mass result shows
  this: the probe arm without mass has D = 0.4598, unchanged, because F_onset already encodes m/μ. μ is drawn
  log-uniformly over a factor of 3.3, independently of everything the baseline sees. A rule that measures the holding
  force therefore beats a rule that cannot see it. The size of the margin is set mainly by the μ range and by σ. It
  falls to 0.14 at σ = 0.4, and σ = 0.2 is an assumed value. For RSS the open question is how large σ is on a real
  sensor (GelSight-type, barometric, or piezoresistive) at this ramp rate. The paper cannot answer it.
- **A-W2. The probe-based baseline that actually competes is CSF-μ̂, and it ties.** CSF-μ̂ is essentially the
  "estimate friction, add a margin" family of grip controllers \cite{khamis2021real}, with the margin calibrated by CRC.
  Under H2b the learned GBM adds nothing over it. The honest headline is therefore "a ramp-down friction probe plus a
  one-line Coulomb formula plus CRC". The learned tactile model is unnecessary. The paper says this in the Discussion,
  but the title, C1–C3 and Algorithm 1 still centre the learned predictor g. Re-centre the method on the plug-in, or
  justify keeping the GBM (it helps only at σ = 0.4).
- **A-W3. The attribution chain is decided by the contact model.** The stored static touch equals F₀ (normal) and m g/2
  (shear) on every instance, and the preload-slip flag is always 0. S is therefore P plus redundant mass information,
  and the squeeze above the friction limit cannot reveal μ under rigid Coulomb contact. "Static touch and squeeze add
  nothing" is a property of the simulator, which C3 partly concedes. It should not be counted as evidence about real
  tactile sensing. Present H4a as a sanity check and drop it from the contribution list, or test it with a compliant
  or elastomer contact model (MuJoCo soft contacts with larger solref, or a hydroelastic model) in which shear fields
  under partial slip do depend on μ.
- **A-W4. Missing standard tactile baselines.** There is no reactive incipient-slip tightening controller
  \cite{dong2019maintaining, veiga2020grip}. There is no uncalibrated friction-estimate-plus-safety-factor controller of
  the kind roboticists actually deploy (for example the safety factor of \cite{khamis2021real}), which would show how
  much the conformal step itself costs or saves relative to practice. The latter needs only existing replays and the
  existing CSF-μ̂ predictions at a few hand-set margins: report its RE and its realised slip.
- **A-W5. Probe practicality is under-examined.** The descent rate is log(200)/0.25 s ≈ 21 log-units per second (the
  force halves every 33 ms). The +0.319 log bias is plausibly detector latency at that rate. On hardware it would
  depend on actuator bandwidth, sensor frame rate and object inertia, and need not be constant across objects. The
  maximum probe displacement is 1.92 mm, just under the 2 mm slip threshold. Because the slip reference is the
  pre-probe pose, such an instance has almost no slip budget left in the window. The probe is also run with the hand
  still. On a robot it would be run in the air after lift-off, where a mis-detected onset drops the object. Please
  report the distribution of probe displacement against mass and μ, and how often the probe's own displacement is the
  bulk of a later slip.
- **A-W6. An alternative explanation for the D3 pattern was not considered.** The D3 cells, and to a lesser extent the
  D4 cells, are the weakest. The paper suggests tangential in-plane loading. A simpler reading is that D3 and D4
  amplitudes are hidden from every method. For those strata the needed force is dominated by an unknown amplitude
  multiplier (U[0.5, 2] m g for D3), so knowing μ removes a smaller *relative* share of the required margin. D1 and D2
  amplitudes are commanded and known. The pattern D1/D2 > D4 > D3 fits this. A quick check: compute D-μ, or the
  residual variance share of amplitude, per stratum.
- **A-W7. The disturbance and contact model is simplified.** D1/D2 enter as pseudo-forces on a still hand with rigid
  primitives and isotropic inertia I = m(hw² + 0.03²)/5 for all shapes. Rotational slip (3° threshold) depends on
  inertia and CoM, so it is only approximately modelled. This is acceptable for a simulation study but should be
  stated.

### Minor
- A-m1. Algorithm 1 should show the probe step (line 0: "run protocol, record onset").
- A-m2. "Lifted preload" is misleading. The hand never lifts, and gravity acts during the preload hold.
- A-m3. Two id training instances are labelled unavoidable (F3 #31, F4 #43, both D3, mass ≈ 0.05–0.06 kg). In S1, 50 g
  objects with μ ≈ 0.2–0.27 also slip at 100 N, which they should not physically (the static need is about 1 N). This
  points to high-force contact artefacts. Mention it, because it bears on H1-M and on the bisection premise.
- A-m4. The abstract's 0.4739 comparator is wrong (see §2.1).
- A-m5. Reword the F4 CoM mechanism (see §2.3).

### Actionable revisions (A)
1. Fix the abstract comparator (0.4739 is against `full`; against P it is 0.4555) and the Table 2 caption.
2. Re-centre the method on "probe + Coulomb plug-in + CRC", with the GBM as a variant. Put H2b in the abstract's
   second sentence rather than after the ablations.
3. Move H4a out of the contributions. State that S ≡ P + mass in this simulator (static touch reads F₀ and m g/2).
4. Add an uncalibrated friction-estimate-plus-margin baseline at 2–3 hand-set margins, using existing replays.
5. Give the alternative hidden-amplitude explanation for D3/D4 and a one-number check.
6. Report the probe displacement distribution and the probe's share of window slips. Discuss detection latency as the
   source of the bias and how it scales with ramp rate.
7. Verify or reword F4.

### Questions for authors (A)
- What onset noise σ (log units) would a GelSight-class or barometric sensor give at a 33 ms halving time? Can you cite
  any measurement?
- Does the probe arm still win if a non-tactile baseline gets a friction proxy with correlation ρ to μ (for example
  ρ = 0.7)? This could be simulated from existing labels by synthesising a proxy feature.

### Score (A): **4 / 10** (borderline reject for RSS)
The work is careful, honest and reproducible, and the verified numbers are solid. For an RSS tactile audience, however,
the central finding is that measuring the holding force via a slip onset beats not measuring it. That finding is shown
only in a rigid-contact simulator, with an idealised Coulomb sensor and an assumed noise level. The learned component
turned out to be unnecessary. Without at least a soft-contact simulation or a small hardware onset-noise measurement,
the robotics contribution is thin. I would raise my score to 6 with either a hardware σ measurement or a
compliant-contact replication of H2a and H4a.

---

## Reviewer B: RSS, conformal prediction and statistical safety

**Summary.** The paper applies split CRC with a monotonised binary physical loss, per disturbance stratum, on a
λ-grid fixed from a disjoint selection split. Decisions are pre-registered with Bonferroni-adjusted one-sided levels
and an object-cluster bootstrap that recomputes λ̂ per draw. Online score-space quantile tracking from binary feedback
handles shift.

### Strengths
- **B1. Correct CRC mechanics.** The monotonisation L̃ = max_{λ' ≥ λ} L preserves the bound on physical slip. The
  grid comes from a split disjoint from calibration, so validity is untouched. The (nR̃ + 1)/(n + 1) rule matches
  Angelopoulos et al. with B = 1. I verified that the code implements exactly this.
- **B2. The guarantee is described precisely.** It is marginal, in expectation over the calibration draw, per stratum,
  at the object level, under fixed family proportions. The paper explicitly does not claim a per-deployment bound, and
  it shows CSF-1 exceeding α in two strata to make that point. This is a model of honest conformal reporting in
  robotics.
- **B3. The inference is sound.** The object-cluster bootstrap resamples calibration and test within family and
  recomputes λ̂, so the CI reflects calibration-draw variability, which matches the in-expectation target. The
  Bonferroni split matches the CI\*\* level (two-sided 97.5 % = one-sided 0.0125). Pre-registration with dated
  addenda, a failure branch that was actually used, and a post hoc grid that "cannot upgrade a decision" are all good
  practice.
- **B4. The label-versus-physical gap is audited.** The H1-V Δ is small and on the safe side. The H1-M violations are
  confined within 1 % of F\*_hi.

### Weaknesses
- **B-W1. The CRC precondition is not stated.** The finite-sample CRC bound requires the loss at the largest grid
  point to be ≤ α (Angelopoulos et al. assume L(λ_max) ≤ α). With "λ̂ = max Λ if none qualifies", unavoidable
  instances counted as slips at every λ, and the F_max cap, the bound is not guaranteed in that fallback. Empirically
  no stratum hit the ceiling, which the paper reports. The theorem statement in §3.4 should still carry this
  condition. Without it, "certified" is over-stated whenever the fallback fires.
- **B-W2. No high-probability (training-conditional) version, although it needs no new simulation.** Every
  calibration instance is replayed on the full grid. A Learn-then-Test or Clopper–Pearson/Hoeffding–Bentkus upper
  confidence bound on R̃_n(λ) per stratum (δ = 0.1, for example) can therefore be computed from the existing files in
  minutes. The comparator already exceeds α at 0.1157 in D1, so this is what a safety-minded RSS reader will ask for
  first. It would also show whether the 42 % margin survives when both arms inflate. Recommend adding it as a
  pre-specified secondary, or at least a report-only row.
- **B-W3. Efficiency is compared at unequal realised risk, and grid granularity drives part of it.** The test slip is
  0.083 for CertGrip-full and 0.102 for CSF-1, and the grid step is 0.8/19 ≈ 0.042 in log-force. The probe arm sits
  well below α while CSF-1 sits at α. This favours the comparator, which is reassuring for H2a. It also means the
  reported D mixes the effect of information with grid quantisation. A risk–efficiency frontier would be cleaner: RE
  against realised calibration risk across the whole grid, per arm, using existing replays. So would RE at matched
  realised slip. The same issue hits H2b more strongly, where the floor-bound CSF-μ̂ slips at 0.066. The paper
  already notes this.
- **B-W4. The H2a decision rule is weak in form, though fine here.** "Superiority" requires the point D ≥ SESOI but
  only CI lower > 0, so at σ = 0.4 the rule declares superiority (D 0.140, lower 0.083) while the CI does not exclude
  effects below the SESOI. The paper handles this through σ\*, but readers will see "superiority" in
  crc_analysis.json for σ = 0.4. Say explicitly that H2a at σ 0.2 also clears the stricter lower > SESOI (0.348).
- **B-W5. The online claim is largely a known theorem.** Score-space OQT with constant step satisfies |rate − α| ≤
  (max q − min q)/(ηT) deterministically. That the window slip lands at 0.0999–0.1016 is therefore expected, not an
  empirical discovery. What is empirical is (i) the transient, (ii) efficiency relative to the oracle, and (iii) whether
  label-rule feedback matches physical feedback. (ii) is inconclusive and confounded by unequal oracle slip, and (iii)
  is audited on one ordering. The trackers are also warm-started from the label-route q̂ while the offline primary is
  CRC, which should be stated. The 20 orderings permute the same instances, so the ordering is not an independent
  replicate. The paper notes this in the Table 3 caption. Recommendation: frame C4 as "transient and catch-up
  behaviour" (H3-S is the solid finding: constant η beats decaying η, ΔC 58 / 42) and state the deterministic rate
  bound explicitly.
- **B-W6. Garden of forking paths in the robustness narrative.** C2 says the result "holds under label-quantisation,
  seed, label-route, per-cell, small-calibration and post hoc grid checks". The supporting checks are reassuring, but
  they come from 08e–08h, written after related read-outs, and they are unadjusted. Keep them, but drop "holds under
  … post hoc grid checks" from the contribution bullet, or mark it as post hoc there.
- **B-W7. The comparator set is narrow given the data-generating process.** Because μ is independent of family, the
  privileged Mondrian-CSF cannot help, so "strongest non-tactile baseline" is strongest among baselines that are all
  equally friction-blind. A friction-proxy baseline could be synthesised from existing labels as log μ + noise with
  correlation ρ. Running it would turn the paper's main caveat into a measured curve (D against ρ), which is far more
  informative for practitioners.
- **B-W8. Terminology.** "Certified" in robotics usually connotes a worst-case or high-probability guarantee. Consider
  "risk-controlled" or "conformally calibrated" in the title and C1, or define the term in the abstract's first use
  (the abstract does give the expectation qualifier).

### Minor
- B-m1. Table 1's H2-H row reports τ and Q in the CI column. Give the pooled 95 % CI [0.4036, 0.4741] instead and move
  τ and Q to the text.
- B-m2. The H2-H "lower limit above 0.16" is met by a margin of 0.0002 (F3D3 0.1602). Say "≥ 0.16".
- B-m3. For the H2-n (n = 50) row, state which interval it is (it is not CI\*\*-labelled in sec08g).
- B-m4. Docstring drift in `conformal.py` (η/√t against the code's η/√(n_u+1)) does not affect the paper but should be
  fixed for the release.
- B-m5. The H3 projected half-width "≈ 0.12" should cite its source (08d).

### Actionable revisions (B)
1. State the CRC precondition (L̃(max Λ) ≤ α, or report that the fallback never fired) next to the theorem in §3.4.
2. Add a report-only high-probability (LTT / UCB) λ̂ and the resulting RE and D from existing replays.
3. Add a risk–efficiency frontier plot (RE against calibration risk on the grid) for CSF-1, CSF-μ̂ and CertGrip-full.
   It could replace Figure 1(b)'s schematic with real curves.
4. Reframe C4 around transient behaviour and H3-S, and state the deterministic long-run rate bound. Say that the warm
   start is the label-route q̂.
5. Remove "post hoc grid checks" from C2, or flag it as post hoc.
6. Simulate a friction-proxy comparator at 2–3 correlation levels from existing labels (report-only).
7. Make the terminology consistent ("certified" in the expectation sense, defined once).

### Score (B): **5 / 10** (borderline)
Statistically this is one of the more careful conformal-robotics applications I have reviewed. The guarantee is stated
correctly, the inference matches the target, and pre-registration is used honestly. The conformal machinery is
standard, though. The new statistical content is limited to applying CRC on a monotonised physical loss, which is a
direct use of known results. The cheap, high-value additions (a high-probability variant and a risk–efficiency
frontier) are missing. With B-W1 to B-W3 fixed I would move to 6.

---

## Overall verdict

**Borderline (A 4, B 5; mean 4.5). Not yet ready for RSS as a full paper; acceptable as a Stage 1 extended abstract
only after condensation and the must-fix items.** No fabrication was found, the numbers reproduce from raw files, and
the limitations are disclosed with unusual care. Significance for RSS is limited by three things: the evidence is
simulation-only, the rigid-contact detector is idealised, and the learned model turned out to be unnecessary. The
contribution reduces to "ramp-down probe + Coulomb plug-in + CRC on physical slip".

## Top must-fix items (ranked)
1. **Abstract comparator error.** "D = 0.4739 against the proprioceptive arm" is wrong. That value is against `full`;
   against P it is 0.4555. Fix the Table 2 caption too (not every row is against P).
2. **State the CRC precondition** (bound valid only if L̃ at max Λ ≤ α; the fallback λ̂ = max Λ voids it) and report
   that no stratum hit it.
3. **Re-centre the method on probe + Coulomb plug-in (CSF-μ̂) + CRC,** since H2b shows the learned GBM adds nothing at
   σ 0.2. Adjust the title/C1–C3 emphasis and Algorithm 1 (add the probe step).
4. **Recast H4a as a simulator consistency check.** Static touch reads exactly F₀ and m g/2 (S ≡ P + mass) and the
   preload-slip flag is constant 0, so "static touch / squeeze add nothing" holds by construction.
5. **Add a report-only high-probability (LTT/UCB) certificate** and a risk–efficiency frontier from the existing
   replays, to address unequal realised slip (0.083 vs 0.102) and grid quantisation.
6. **Verify or correct the F4 description.** The explicit `<inertial>` likely overrides the sphere's mass and CoM,
   so the CoM shift comes from the sampled `com` (±60 %).
7. **Probe practicality.** Discuss the +0.319 bias as detection latency at a halving time of about 33 ms, report the
   probe-displacement distribution (max 1.92 mm against the 2 mm threshold) and its share of window slips, and state
   that on hardware the probe runs in the air.
8. **Condense to RSS length.** The draft is about 9,700 words and the abstract about 345. Remove the 08c/08e/08f–08h
   identifiers from the main text, drop "post hoc grid checks" from C2, and consider the hidden-amplitude explanation
   for the weak D3/D4 cells.

## Items possibly worth remembering (for the main session)
- From the raw files (not from memory): static touch in this simulator equals F₀ (normal) and m g/2 (shear) per pad,
  and the preload-slip rate is 0 in every pool.
- From the raw files: H3 trackers are warm-started from the label-route q̂.
- From the raw files: 2 unavoidable id rows exist (train only), and several low-mass S1 instances slip even at 100 N.
