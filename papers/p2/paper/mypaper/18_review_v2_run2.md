# Stage 18 peer review (v2 draft, run 2)

**Paper:** *Probe, Then Certify: A Tactile Friction-Onset Probe with Conformal Risk Control for Certified-Slip Minimal-Force Grasping*

**Review setting.** This is a simulated RSS (Robotics: Science and Systems) program-committee pair. Reviewer A is an expert in robotics and tactile manipulation. Reviewer B is an expert in conformal prediction and statistics. The stage-18 checklist (topic, methodology–evidence consistency, trial count, length, top-conference criteria) is applied in full. Wherever the checklist mentions NeurIPS/ICML, the venue standard here is RSS.

**Evidence actually inspected.**
- The full prompt: paper, Fig. 1 prompt, `results_v1.json`, `results_v2.json`, run-log excerpt and grep of the statistical procedures.
- `docs/07_hypotheses.md`, `docs/08b_preregistration.md`, `docs/08h_secondaries_batch3.md`, `docs/09_amendment_v2.md` and `plans/stage_13_v2_b3_online_physical.md`.
- `code/b3_online.py`, `code/analysis_v2_a.py`, `code/analysis_v2_b.py`, `code/analysis_crc.py` and `code/h3_streams.py`.
- The raw replays in `results/v1/crc/*.jsonl`, `results/v2/crc09e/*.jsonl`, `results/v2/b3/*.jsonl` and `results/v1/labels/id_F*.jsonl`.

Following the instructions, no other review files (18_*, 20_*) and no results/14_* or 15_* files were opened.

---

## 0. Verdicts on the required checks

| Check | Verdict |
|---|---|
| 1. On topic | **Yes.** All sections serve the stated topic: probe, CRC on the physical slip loss, the strongest non-tactile comparator, attribution and online binary-feedback calibration. No environment or tooling issue is presented as a contribution. The compute paragraph and the long deviations list are bookkeeping, not drift. |
| 2. Methodology–evidence consistency | **Largely consistent.** Every headline number checked matches the JSON, and the key rows reproduce from raw replays (Section 3). There are four textual misstatements or omissions (M1–M4 below). None changes a decision. |
| 3. Trial count | **No mismatch.** The claimed counts all match the evidence: 2,000 calibration and 2,800 test instances (500 / 700 per stratum), 800 selection and 800 monotonicity instances, 2,000 bootstrap draws, 5 predictor seeds, 20 pre-registered orderings, 5 B3 orderings, 20 B3 streams of 2,000 steps (40,020 jsonl lines including headers), and 500 draws for the friction-residual diagnostic. |
| 4. Length | Per-section word counts: Abstract 244, Introduction 1,099, Related Work 564, Method 1,900, Setup 1,331, Results 2,766, Discussion 630, Limitations 340, Conclusion 274. Total ≈ 9,160 words, so no section is under length. The real problem is the reverse: the draft is **over-dense for an 8-page RSS paper**, with Tables 0–5 and many route × grid variants. |
| CRITICAL FABRICATION | **No.** |

---

## Reviewer A (robotics / tactile manipulation)

### Summary
The paper proposes a grasp protocol with three steps.
1. A fixed 32.7 N preload carries no friction information.
2. A 0.25 s log-linear ramp-down probe is read by a touch-grid shear/normal detector, giving a Coulomb estimate μ̂ = mg/(2F_onset).
3. A force rule F_base·e^λ is calibrated by conformal risk control (CRC) on a binary physical-slip loss, per disturbance type.

All experiments are in MuJoCo. At α = 0.10 and an assumed onset-noise level σ = 0.2, the probe arm needs 42 % less relative excess force than CSF-1, the best friction-blind conformal baseline. The paper argues that the saving comes from the probe and not from the learned model.

### Strengths
1. **Clean experimental design for attribution.** Making the preload identical for every object turns the onset into the only friction channel. This is a good piece of experimental design, and the nested feature chain plus the shuffled-touch control are sound.
2. **Honest reporting of negative results.**
   - The learned-versus-plug-in contrast (H2b) is "not confirmed".
   - There is a reversal sub-pool: D = −0.2614.
   - A non-tactile prior of log-noise 0.2 erases the advantage.
   - σ\* = 0.4.

   All of these appear in the abstract. This is rare and commendable.
3. **The B2 fixed-margin study is practically informative.** It shows why a single hand-set margin fails: at κ = 1.0, D1/D2 are over-protected (slip 0.04 / 0.02) while D3/D4 slip at 0.66 / 0.62. This is the comparison a practitioner would actually make.
4. **The online physical-feedback study (B3) points in the right direction for hardware.** Its numbers reproduce exactly from the raw streams (Section 3).

### Weaknesses
1. **The minimal-force story is contradicted by the protocol itself (major).**
   - Every object, including 50 g objects, receives a 32.7 N preload and a squeeze to 1.5 F₀ ≈ 49 N before the probe. The probe force F₀ = mg/μ is sized for the heaviest, most slippery object.
   - The paper is motivated by fragile, compliant or valuable objects and by prosthetics. For such objects, peak force during the protocol, not hold force after it, decides damage.
   - RE is measured only at the final commanded force, so a method that always crushes at 49 N first scores as "minimal force".
   - The paper must either (a) report the peak force and the force–time integral of the whole protocol per arm, or (b) restrict the claim to the steady hold force and remove the fragile-object and prosthetic framing.

   A protocol with an adaptive (low) preload would be the natural fix. The paper argues that such a preload would leak friction information, but that is a constraint of the attribution design, not of a deployable method.
2. **Simulation only, with an assumed noise level that controls the effect (major for RSS).**
   - D falls from 0.68 (σ 0) to 0.42 (σ 0.2) to 0.14 (σ 0.4), and at σ = 0.4 the lower limit falls below the smallest effect size of interest (SESOI). So the headline depends on a noise level that was not measured.
   - Rigid contact means static touch reads F₀ and mg/2 by construction. The H4a "equivalence" is therefore a simulator identity, as the authors concede.
   - Rigid contact also has no elastomer stick–slip transition zone. For a paper whose central mechanism is an incipient-slip onset, at least one real-sensor measurement of onset-force dispersion is the minimum RSS would expect. Examples: GelSight/DIGIT or BioTac on a few materials, compared with a force-gauge pull test.
3. **Missing robotics baselines.**
   - The comparator set is friction-blind by construction: friction is drawn independently of every non-tactile input.
   - The standard tactile alternative is absent, namely reactive slip detection plus grip tightening (Dong 2019, Veiga 2020, and many others).
   - The analytic friction-estimate-plus-margin controller of Khamis 2021 is also absent. B2 is a stand-in for it, but it is uncalibrated and run only on the paper's own probe.

   Without these baselines the paper shows "probe beats no-touch", which is expected. It does not show "probe + CRC beats existing tactile grip control at equal slip".
4. **Physical realism of the protocol.**
   - Disturbances are applied with the hand held still, as pseudo-forces.
   - Mass is "given on the assumption that the robot weighs the object during the lift", yet the probe and force choice happen before any lift motion. How is mass obtained before the probe?
   - The probe deliberately produces micro-slip: median 0.126 mm, p95 0.25 mm, max 1.92 mm. The maximum is close to the 2 mm slip threshold. Repeated probing on soft or coated surfaces changes friction (wear, contamination), and the paper should discuss this.
5. **The deployable route is under-evaluated.**
   - The offline certificate needs labels and 20 replays per calibration instance, which only a simulator can provide. The authors acknowledge this.
   - The hardware route is therefore B3, which covers 5 orderings, two shifts and no intervals. It also warm-starts from the simulator CRC offset, which presumes the simulator is calibrated to hardware.
   - The paper should state plainly that nothing in the paper is "certified" on a robot.
6. **Unexplained lateral-pull weakness.** D3 cells are weakest in every family (0.30–0.39). D3/D4 amplitudes are hidden, so a stratum-specific offset absorbs the load multiplier. That would also explain why "per-stratum" calibration matters. It deserves one more diagnostic rather than "a pattern we have not explained".

### Actionable revisions (A)
- A1. Report peak and integrated force over the entire protocol (preload, squeeze, probe, hold) for every arm. Either change the motivation or add an adaptive-preload variant.
- A2. Add a reactive slip-tightening baseline and a friction-estimate-plus-fixed-safety-factor baseline (Khamis-style), both evaluated at matched slip.
- A3. Ground σ, or at minimum bracket it with literature-reported incipient-slip onset dispersions. Make σ\* = 0.4 visible in the abstract next to the 42 %.
- A4. Explain when mass is known relative to the probe. Report probe displacement as a distribution, and flag that its maximum (1.92 mm) is close to the threshold.
- A5. Remove or qualify "certified" in the title and contributions; "simulation-calibrated" would be accurate.

**Score (A): 4 / 10 (borderline, leaning reject for RSS).** The work is careful and honest, but the robotics contribution is not shown outside a rigid-contact simulator. The force-minimisation claim ignores a 32.7–49 N preload on every object, and the tactile-control baselines are missing.

---

## Reviewer B (conformal prediction / statistics)

### Summary
The method applies split CRC with a binary, monotonised physical loss over a 20-point log-force grid, per stratum (n = 500). A Clopper–Pearson Learn-then-Test (LTT) variant and score-space online quantile tracking (OQT) are reported alongside. Analysis is pre-registered with four Bonferroni-split core decisions and 97.5 % object-cluster bootstrap intervals in which λ̂ is refitted in every draw.

### Strengths
1. **Correct CRC instantiation.**
   - The rule (n R̃_n(λ) + 1)/(n + 1) ≤ α is the B = 1 CRC bound.
   - Monotonising by a running maximum gives L̃ ≥ L, so the bound transfers to raw slip.
   - The grid is fixed from a disjoint selection split before calibration.
   - I re-derived λ̂ and the test rows independently from the raw replays (Section 3), and they match to all printed digits.
2. **The bootstrap re-runs the calibration step.** Calibration and test objects are resampled within family and λ̂ is recomputed in each draw, so the intervals include calibration variability. This is the right uncertainty for a "certified" efficiency claim and is often omitted in conformal-robotics papers.
3. **Clean LTT implementation.** It is a fixed-sequence scan from the top of the grid downwards with a one-sided Clopper–Pearson bound on the monotonised risk. Because a fixed sequence controls the family-wise error without further correction, the per-stratum (1 − δ) statement is valid. The paper correctly says it is not family-wise across strata.
4. **Exemplary pre-registration bookkeeping.** The failed monotonicity gate is used as the reason for the CRC route, and seven deviations are listed in one place.

### Weaknesses
1. **The certificate is weak as an object-level safety statement, and the paper should quantify that gap.**
   - The guarantee is marginal per disturbance stratum, in expectation over the calibration draw.
   - The paper has 16 family × disturbance cells and reports D per cell, but not **slip per cell**, nor the distribution of per-object slip.
   - A conditional-coverage audit is needed: physical slip per family × stratum cell and per friction quintile, and what fraction of test objects slip at the CRC force. A friction-blind CSF-1 will have strongly μ-dependent conditional slip (low-μ objects almost always slip). The probe arm should be much flatter. That comparison would be a stronger argument for touch than D and is currently missing.
   - Mondrian/class-conditional CRC by friction bin, available for evaluation only, would be a natural extra row.
2. **Matched-slip D is test-selected.** The A1 frontier interpolates the offset k at which **test** slip equals 0.10 (`analysis_v2_a.matched_re`). D_match is therefore an oracle-on-test descriptive contrast, not an operating point a user could choose. Say so explicitly. The bootstrap repeats the interpolation, which is fine for its sampling variability, but the point is not a certificate.
3. **Post hoc grid repair and mixed-grid comparisons.**
   - The primary grid has a floor defect: λ̂ is at index 0 for CSF-μ̂ in D1/D2, and at index 1 for CSF-1. The refined grid was added after seeing results.
   - The paper handles this conservatively in the decision rules, but its prose sometimes compares across grids. See M2: the Discussion sets the plug-in's refined-grid D 0.4149 against the learned arm's primary-grid D 0.4168. The like-for-like refined value for the learned arm is 0.4289.
   - Figure 1b draws CSF-μ̂ on the refined grid and the three other arms on the primary grid. All four arms should be shown on the same grid, with the other grid in the supplement.
4. **H2b remains unresolved, and C3's wording outruns the evidence.**
   - The decision-bearing contrast is 0.0569 [−0.0399, 0.1454]. On the refined grid it is 0.0240 [−0.0949, 0.1001], with the upper limit 0.0001 outside the equivalence margin.
   - The claim that "the saving comes from the probe" therefore rests on two secondary pieces of evidence: (a) separate D-versus-CSF-1 values whose ordering flips by route, and (b) the label-route equivalence (secondary).
   - No direct CertGrip-full vs CSF-μ̂ contrast was computed at matched slip or under LTT. Computing it would cost nothing, since the bootstrap already has both arms, and it would settle the attribution claim.
   - The friction-residual diagnostic points the other way from the narrative. CertGrip-full's residual still has R² = 0.21 against log μ at σ 0.2, against 0.005 for CSF-μ̂: the learned model *shrinks* the onset towards the mean. This explains why it adds nothing and should be discussed.
5. **Online study (H3 / B3).**
   - H3 is inconclusive: realised half-widths are 0.15–0.20 against a planned ≈ 0.12, so the study is underpowered.
   - The S2 "oracle" itself runs at label slip 0.1346 > α, so R_E in S2 is not a meaningful efficiency ratio.
   - B3 has 5 orderings and no interval. The per-ordering spread (0.082–0.112 window slip) is shown, which is good, but a simple across-ordering standard error would be cheap.
   - OQT guarantees only long-run average slip. The text should not imply per-window validity.
6. **Multiplicity.** The pre-registered Holm correction within secondary families was replaced by unadjusted intervals. This is disclosed, but with roughly 40 secondary rows, the "superiority" labels in Tables 1–2 need a family-wise caveat in the captions, not only in the text.
7. **Undefined handling of unavoidable instances.** RE excludes instances whose F\* exceeds F_max, while they count as slips (`analysis_crc.py`, `h3_streams.py`). There are none in the in-distribution test set, but the B3 streams contain 3 (S1) and 1 (S3). State the rule.

### Specific misstatements found (M1–M4)
- **M1 (factual error, Section 5.2).** The text says "Against CSF-1, CSF-μ̂'s D is … smaller under Learn-then-Test (0.3704 / 0.4040 against 0.4043 / 0.4015)". On the refined grid, 0.4040 > 0.4015 (`a_analysis_08e.json`: D_ltt:CSF-muhat 0.40398 vs D_ltt:full_rd 0.40146). So CSF-μ̂ is *larger* under refined-grid LTT. The sentence should say "smaller on the primary grid, marginally larger on the refined grid".
- **M2 (cross-grid comparison, Section 6 and the abstract).** "The plug-in … D 0.4149 on the refined grid, against the pre-registered 0.4168 for the learned arm" compares the refined grid with the primary grid. Like-for-like values: refined 0.4149 vs 0.4289; primary 0.3816 vs 0.4168.
- **M3 (selective reporting, Section 5.5, H1c).** "Uncalibrated targeters over-slip at every level (0.0096–0.0507 above α, every CI\*\* above 0)" holds only for RAW-Q and RAW-G. The third registered targeter, RAW-Qv (the selection-tuned variant "a practitioner would use", `07_hypotheses.md`), has CIs that include 0 at every α (for example α 0.10: +0.0125 [−0.0222, 0.0586]). It must be reported. Its absence overstates the case for conformal calibration over a simple tuned offset.
- **M4 (route not stated).** Several numbers in the "route robustness" paragraph come from the label route but sit in a CRC-route paragraph without saying so: the oracle-gap share 0.5172, the random-effects pooled D 0.4388 with its cell values, and the small-calibration D 0.4146 / 0.4654. The small-calibration "interval" [0.2585, 0.5477] is also of unstated type. Label the route and the interval type.

Minor points:
- The static-touch check reports only the normal channel (max |N − F₀| = 0.16 N). The shear channel deviates from mg/2 by up to 6.4 N, in 24 instances by more than 1 %.
- The label-route JSON labels H2b and H4e as "equivalence", while the paper reports them more cautiously. That caution is fine but should be stated consistently.
- Labels and v1 replays were produced on a different host and Python version (3.13.18, processor x86_64) than the v2 replays (3.12.16, processor empty). Bit-identity is claimed only "on the same machine", yet H5 mixes CSF-proxy replays from v2 with CertGrip-full replays from v1. A short cross-host replay check would close this.

### Actionable revisions (B)
- B1. Add a conditional-validity table: slip per family × stratum and per μ-quintile for CertGrip-full, CSF-μ̂ and CSF-1, plus the per-object slip distribution.
- B2. Compute the direct CertGrip-full vs CSF-μ̂ contrast at matched slip and under LTT on both grids. These numbers come from existing replays.
- B3. Fix M1–M4. Put all Figure 1b arms on one grid. Label D_match as test-selected.
- B4. Add an across-ordering standard error to B3. In S2, report R_E only together with the oracle's miscalibration.
- B5. Add a multiplicity caveat to the captions of Tables 1–2. Define the unavoidable-instance rule.

**Score (B): 6 / 10 (weak accept on statistical grounds).** The conformal machinery is standard but correctly applied. Inference is unusually rigorous and the reporting honest. The remaining issues are presentation and coverage-type gaps, not validity failures. The novelty on the conformal side is modest: an application of CRC and LTT to a binary physical loss.

---

## Meta-assessment (AC view)

- **Novelty.** "Lower the force until slip to read friction" is old (Section 2 concedes this). CRC and LTT on a binary loss are standard. The contribution is the integration and the attribution protocol. That is solid, but incremental for RSS without hardware.
- **Baselines.** The strongest *non-tactile* conformal comparator was chosen fairly and before calibration or test data were read. Tactile control baselines are missing.
- **Ablations.** Present and meaningful: nested chain, shuffled touch, onset-only, plug-in, the σ sweep, the friction-prior sweep and fixed margins.
- **Claims vs evidence.** The headline numbers are verified. The C3 attribution wording is somewhat stronger than the evidence (H2b not confirmed, no direct contrast at matched slip or LTT). The minimal-force framing conflicts with the protocol's preload.
- **Limitations.** Acknowledged well, except for the preload/peak-force issue and the RAW-Qv omission.
- **Recommendation.** Borderline. Weak reject for RSS in its current form; it would be acceptable with hardware onset-noise grounding, peak-force reporting and a reactive tactile baseline.

**Overall score: 5 / 10.**

---

## 3. Number spot-check (≥ 20; JSON and independent recomputation from raw data)

"Recomputed" means I computed the value with my own scripts from the raw jsonl files and labels, not by reading the analysis JSON. Scripts are in the session scratchpad: `b3_recompute.py`, `crc_recompute.py`, `crc_v1.py`.

| # | Paper value | Source | Result |
|---|---|---|---|
| 1 | H2a D = 0.4168 [0.3484, 0.4778] | crc_analysis.json; **recomputed** from v1/crc replays (D 0.4168) | match |
| 2 | CertGrip-full RE 0.4567, slip 0.0829, λ̂ 10/10/11/10 | **recomputed** | match |
| 3 | CSF-1 RE 0.7832, slip 0.1021, λ̂ 1/1/15/14 | **recomputed** | match |
| 4 | Per-stratum slip CertGrip 0.0871/0.0714/0.0757/0.0971; CSF-1 0.1157/0.0886/0.1057/0.0986 | **recomputed** | match |
| 5 | CSF-μ̂ σ0.2 primary RE 0.4843, slip 0.0657, λ̂ 0/0/14/12 | **recomputed** | match |
| 6 | onset-only RE 0.4336, slip 0.0857 | **recomputed** | match |
| 7 | H2b D 0.0569 | **recomputed** | match |
| 8 | D at σ 0.4 = 0.1401 | **recomputed** | match |
| 9 | Seed-3 D 0.3932 | **recomputed** | match |
| 10 | CSF-1 frontier k = +4: (0.0100, 1.110) | **recomputed** | match |
| 11 | CSF-proxy σ_p 0.2 edge-rule grid: RE 0.4312, slip 0.0825 (λ̂ 20/21/20/20) | **recomputed** from v2/crc09e + labels | match |
| 12 | B3 S1 CertGrip 1,001–2,000: slip 0.1002, RE 0.4633 | **recomputed** from v2/b3/*.jsonl | match |
| 13 | B3 S1 CSF-1 1,001–2,000: 0.1016 / 0.7915; D_RE 0.4146 | **recomputed** | match |
| 14 | B3 S1 1–500: 0.0984/0.4274 vs 0.1052/0.7615; D_RE 0.4387 | **recomputed** | match |
| 15 | B3 S1 1,501–2,000: 0.1032/0.4626 vs 0.0988/0.7998; D_RE 0.4216 | **recomputed** | match |
| 16 | B3 S3 all three windows (6 slip/RE pairs, D_RE 0.4438/0.4120/0.4115) | **recomputed** | match |
| 17 | B3 range 0.0936–0.1032, per-ordering 0.082–0.112; no capped steps | **recomputed** | match |
| 18 | D_match 0.4563 [0.4096, 0.4896]; RE_match 0.4290 / 0.7891 | a_analysis.json; interpolation checked by hand | match |
| 19 | D_ltt 0.4043 [0.3362, 0.4561]; LTT λ̂ 10/10/12/11; slip 0.0696, RE 0.4895 | a_analysis.json | match |
| 20 | Refined H2a 0.4289; refined H2b 0.0240 [−0.0949, 0.1001] | crc_analysis_v2.json | match |
| 21 | H5 σ_p 0.2 edge −0.0299 [−0.1903, 0.0816]; 0.4 → 0.5042; 0.8 → 0.8361 | b_analysis*.json | match |
| 22 | B2 test slip 0.9582/0.8257/0.6182/0.3350; κ = 1 D3/D4 slip 0.6571/0.6186 | b_analysis.json | match |
| 23 | H3 R_E 0.8778 [0.7404, 1.120], 1.174, 0.9629; Frozen 0.3056 / 0.5101 | h3_analysis.json | match |
| 24 | Monotonicity 8/800, CP upper 0.02115, 7 under D2 | h1m_analysis.json | match |
| 25 | COMP selection 0.7686 / 0.8294 / 0.8335 | comp_selection.json | match |
| 26 | H2-R −0.2614 [−0.5320, −0.0325], n 352/548 | sec08g.json | match |
| 27 | Random-effects 0.4388 [0.4036, 0.4741], τ 0.0511, Q 31.04; D3 cells 0.2979/0.3868/0.3115/0.3348 | sec08g.json | match |
| 28 | Friction-residual R²: 0.7937 (P), 0.6034, 0.2142, 0.0054 | sec08f_dmu.json | match |
| 29 | Compute 14.50 h (5.72 + 8.03 + …); v2 2.357 h | 19_report_rows, compute_v2 | match |
| 30 | "CSF-μ̂ smaller under LTT (… 0.4040 vs 0.4015)" | a_analysis_08e.json | **wording wrong (M1)** |
| 31 | H1c "every CI\*\* above 0" | sec08h_h1c.json | **true only for 2 of 3 targeters (M3)** |

About 60 individual values were checked, more than 20 of them recomputed independently from raw replays. Every numeric value matches. The two problems found (#30, #31) are an interpretive misstatement and a selective omission, not invented numbers.

**CRITICAL_FABRICATION: no.**

---

## 4. Top must-fix items (ranked)

1. Report peak and integrated grip force over the full protocol (the 32.7 N preload and 49 N squeeze apply to every object). Otherwise drop the fragile-object and prosthetic "minimal-force" framing.
2. Add a reactive slip-tightening baseline and a Khamis-style friction-estimate-plus-margin baseline, at matched slip.
3. Ground or bracket the onset noise σ with real-sensor data. Put σ\* = 0.4 (D 0.14) next to the 42 % headline.
4. Fix M1: the refined-grid LTT D of CSF-μ̂ (0.4040) exceeds CertGrip-full's (0.4015); the "smaller under LTT" claim is wrong.
5. Fix M2: compare the plug-in and learned arms on the same grid (refined 0.4149 vs 0.4289; primary 0.3816 vs 0.4168), and put all of Figure 1b on one grid.
6. Fix M3: report RAW-Qv in H1c; its CIs include 0 at every α.
7. Compute the direct CertGrip-full vs CSF-μ̂ contrast at matched slip and under LTT, and add a conditional-slip table (family × stratum, μ-quintile, per-object). Without these, "the saving comes from the probe" is stated too strongly.
8. Qualify "certified" (simulation-only, needs replays and labels). Label D_match as test-selected, B3 as 5-ordering descriptive and S2 R_E as confounded by oracle miscalibration. Cut density to fit 8 RSS pages.
