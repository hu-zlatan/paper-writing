# Stage 18 peer review, pass 2, run 1

Paper: *Probe, Then Certify: Minimal-Force Grasping with a Tactile Friction-Onset Probe and Conformal Slip-Risk Control*
System role: balanced conference reviewer, rigorous about methodology-evidence consistency.

## CRITICAL_FABRICATION: no

Reasons:
- **Trial and instance counts match the raw files.** The paper reports 2,000 calibration instances (n = 500 per stratum), 2,800 test instances, 800 selection instances, 800 monotonicity-gate instances plus 3 × 100 shift instances, 20 stream orderings, predictor seeds 0–4 and 2,000 bootstrap draws. Each of these matches `crc_grids.json`, `crc/*.jsonl`, `labels/`, `mono/`, `h3_analysis.json` and the analysis code. Nowhere does the paper claim more runs than exist.
- **The statistical procedures it describes are in the code.** These are the Clopper–Pearson limit (`analysis_h1m.py`), the object-cluster bootstrap with λ̂ refitted on every draw (1.25/98.75 percentiles, `analysis_crc.py`), TOST-style decision rules (`decide()`), DerSimonian–Laird pooling (`sec08g.json`, which I recomputed) and score-space OQT with anti-windup and a decaying-step variant (`h3_streams.py`).
- **The headline numbers reproduce from raw files.** I recomputed H2a (CRC and label route), H2b, H4e, the slip rates, the λ̂ indices, the detector statistics, the monotonicity count and the heterogeneity Q/τ independently (see the spot-check list below).
- **The problems I found are real errors and omissions, not invented results.** One wrong label in the Abstract (D = 0.4739 is described as "against the proprioceptive arm"), one undisclosed deviation from the pre-registered multiplicity rule, several overstated characterisations, and omitted secondary results.

---

## Spot-checks (31 items; ✓ = matches, ✗ = discrepancy, ~ = matches but the wording needs care)

Scripts I wrote and ran are in the session scratchpad: `rc1.py` to `rc5.py`. They read only raw files.

| # | Paper claim | Source / recomputation | Result |
|---|---|---|---|
| 1 | H2a D = 0.4168, RE 0.4567 vs 0.7832 (CRC 08c) | rc1.py: own CRC (monotonised loss, (nR+1)/(n+1) ≤ α, per stratum) from `crc/*.jsonl` + labels → D 0.41682, RE 0.45673 / 0.78318 | ✓ |
| 2 | Physical test slip 0.0829 (CertGrip-full), 0.1021 (CSF-1) | rc1.py: 0.082857 / 0.102143 | ✓ |
| 3 | CSF-μ̂ λ̂ at grid index 0 in D1/D2; CSF-1 at index 1 | rc1.py: CSF-μ̂@0.2 idx {0,0,14,12}; CSF-1 {1,1,15,14} | ✓ |
| 4 | H2b 08c D = 0.0569; H4e D = −0.0534; onset-only RE 0.4336 with slip 0.0857 | rc1.py: 0.05692, −0.05341, 0.43357 / 0.08571 | ✓ |
| 5 | Label route H2a D = 0.4292, H2b D = 0.0134 | rc5.py: own split-conformal (⌈(n+1)(1−α)⌉-th score per stratum) → 0.42916, 0.01335 | ✓ |
| 6 | CSF-1 and CSF-μ̂ formulas (Section 3.3) | rc5.py: stored `log_g` equals the `baselines.py` formula to within 5e−7 for all 4,800 instances | ✓ |
| 7 | Detector: found on all 8,000; r = 0.948; bias +0.319; SD 0.110 | rc4.py from label `rec.onset`: 1.0, 0.94798, 0.31864, 0.11029 | ✓ |
| 8 | "The bias is constant across instances" | rc4.py: corr(error, log μ) = −0.25; error SD by family F1 0.062, F2 0.045, **F3 0.196**, F4 0.063 | ✗ overstated |
| 9 | Probe displacement median 0.126 mm, p95 0.254, max 1.924, none ≥ 2 mm | rc4.py: 0.12634 / 0.25429 / 1.92376 / 0 | ✓ |
| 10 | H1-M: 8 of 800 non-monotone, 7 under D2; CP upper 0.02115 | rc3.py recount from `mono/*.jsonl`: 8 (D2 7, D1 1); scipy beta.ppf(0.9875, 9, 792) = 0.021147 | ✓ |
| 11 | Shift-pool violations S1 0, S3 1, S2 1 | rc3.py: 0 / 1 / 1 | ✓ |
| 12 | Splits train 0–149, selection 150–199, calibration 200–324, test 325–499 | rc1/rc5: labels' `split` field per object index | ✓ |
| 13 | No unavoidable instances in calibration or test | rc1.py: 0 (2 exist in the training pool) | ✓ |
| 14 | μ log-uniform [0.3, 1], independent of mass and family | rc1.py: range 0.300–1.000; corr(log μ, log m) = 0.007; family means of log μ within 0.024 | ✓ |
| 15 | Disturbance ranges D1–D4; one μ per object | rc2.py: D1 [1, 10], D2 [5, 20] mm at [2, 5] Hz, D3 [0.5, 2], D4 [0.2, 1.0]; 1 μ per object | ✓ |
| 16 | 11 bisection replays; bracket width ≈ 0.7 % | rc1.py: 7,998 rows with 11 replays (2 unavoidable rows with 1); median relative width 0.0067 | ✓ |
| 17 | F5 thickness 4–10 mm; 550 objects; stream objects 175–549 | rc5/labels: 4.02–9.96 mm; s2 stream objects 275–549 seen in one shard, 2,200 rows in the S2 pool | ✓ |
| 18 | MuJoCo 4.0.0, dt 0.002, elliptic cone, impratio 10, condim 6, solref and solimp as stated | `sim.py` lines 26 and 87–88; JSONL headers | ✓ |
| 19 | Detector constants (6/8/2/0.5, r_arm 0.1, 1 mN, 0.02 s return); taxel noise | JSONL header `rd_detector`, `taxel_noise` | ✓ (the `_rd_touch_probe` docstring still says "100 Hz"; the code runs at 500 Hz) |
| 20 | Slip reference is the pre-probe pose | `sim.py` l.312–334: `ref_p = p1` taken before `_rd_touch_probe` | ✓ |
| 21 | Learner search space (Table) | `models.py` `configs()` | ✓ |
| 22 | COMP selection 0.7686 / 0.8294 / 0.8335 | `comp_selection.json` | ✓ |
| 23 | Seed range, CRC 0.3932–0.4494; label route 0.4145–0.4442 | `crc_analysis.json`, `h2_label_rule.json` | ✓ (seed 4 CRC physical slip is 0.1018 > α, not reported) |
| 24 | H2-H pooled 0.4388, τ 0.0511, Q 31.04; every cell lower limit > 0.16 | Own DerSimonian–Laird from `sec08g.json` cell D/se: 0.43882, 0.05109, 31.044 (p = 0.0087); minimum lower limit 0.1602 | ✓ (the 0.16 margin is very thin) |
| 25 | D3 cells weakest: 0.2979 / 0.3868 / 0.3115 / 0.3348 | `sec08g.json` | ✓ |
| 26 | H4a S vs P −0.0084; full vs S −0.0263; CertGrip-full vs full 0.4739 | `h4a_label_rule.json`; 1 − 0.4264/0.8104 = 0.474 | ✓ in Section 5.2; **✗ in the Abstract**: there "0.4739 against the proprioceptive arm", but against P the value is 1 − 0.4264/0.7831 = 0.4555 |
| 27 | D-μ: P 0.7937, CSF-1 0.6034, CertGrip-full 0.0105 / 0.0452 / 0.2142 / 0.5655, CSF-μ̂@0.2 0.0054 | `sec08f_dmu.json` | ✓ (500 draws and 95 % CI, not the CI\*\* protocol) |
| 28 | H3 table (all 15 cells), R_E and CIs, physical audits 0.103 / 0.092 / 0.101, matched differences 0.032 / −0.035 / 0.009 | `h3_analysis.json` | ✓ (Frozen-CertGrip S1 raw value 0.30555, printed as 0.3056) |
| 29 | η = 0.03412; nothing capped in any window | `h3_analysis.json` eta 0.034125; `capped_window` = 0 for every arm and shift | ✓ |
| 30 | H3-S ΔC 58.15 / 42.40 / 2.90 / 2.75 | `sec08h_h3s.json` | ✓ |
| 31 | Compute 14.5 CPU-h = 5.72 + 8.03 + 0.60 + 0.15 | `19_report_rows.json` (sum 14.4998) | ✓ |

Further checks that matched: H1-V Δ values; H1c values and intervals; H2-T 0.5918; oracle gap 0.5172 with oracle RE 0.1271; H2-C 0.4381; H2-R −0.2614 [−0.5320, −0.0325] (n_cal 352, n_test 548); H4b 0.4638 / 0.4555; D-FID 0.7257; H2-M 0.4598 and 0.4603 with COMP RE 0.7991; UT3 160/160 (20 degenerate cells at α 0.01, n 50); 08e read-outs 0.4289 / 0.0240 [−0.0949, 0.1001] / −0.1522 / 0.3315; 08e grid of 41 points with half-width 0.8; 08c grid half-width exactly ±0.4 around q̂_sel.

One claim could not be verified. "CRC route written after the H1-M gate and before any predictor was fitted" rests only on the status note in 08c. The git clone is shallow (`git rev-parse --is-shallow-repository` returns true), and its earliest commit is already the 08e read-out, so the history cannot confirm the order.

---

## Topic adherence

The paper stays on topic: probe plus CRC, the comparison with the best non-tactile conformal baseline, the attribution ablations and online binary-feedback calibration. Environment issues are not presented as contributions. The physics choices (pseudo-force disturbances, rigid contact, the "≈ gross-slip" detector) are disclosed as simplifications.

## Length

Word counts are about 9,650 words in total, plus three tables and an algorithm box:

| Section | Words |
|---|---|
| Abstract | 345 |
| Introduction | 1,144 |
| Related Work | 598 |
| Method | 2,051 |
| Experimental setup | 1,399 |
| Results | 2,455 |
| Discussion | 871 |
| Limitations | 483 |
| Conclusion | 293 |

No section is under-length. The problem is the reverse: the draft very likely exceeds 9 pages, and the abstract is far beyond the usual ~250 words. Section 5 and the Discussion repeat each other, for example on the grid-floor caveat, which appears four times.

---

## Reviewer A (robotics and tactile manipulation): score 4/10 (borderline reject)

**Summary.** After a fixed, uninformative preload, the gripper lowers its force until a touch-only detector flags onset. The onset gives μ̂ = mg/(2F_onset). A per-stratum conformal-risk-control offset on the binary physical slip loss then sets the force. In MuJoCo, the probe arm needs 42 % less relative excess force than a friction-blind physics plug-in calibrated to the same α.

**Strengths**
1. The reporting is unusually honest. Of four pre-registered core decisions, only one is confirmed, and the paper says so. It also reports a regime where the method loses (H2-R), the case where frozen calibration does not break (S2), and the case where the tracker's force cost is above the oracle's.
2. The protocol is careful. A common preload carries no mass or friction information. The slip reference is the pre-probe pose, so probe-induced slip counts against the method. The static and squeeze features are noise-free, so the attribution is conservative.
3. The ablation chain is clean: P → S → full → +onset, onset-only and shuffled. It establishes, within this simulator, that the gain sits in the onset reading and not in learned touch.
4. The probe-safety data (median 0.126 mm displacement, none ≥ 2 mm) and the per-instance detector statistics are concrete and reproducible.

**Weaknesses**
1. **H2a is close to guaranteed by design.**
   - μ is drawn independently of every non-tactile input over a factor-3.3 range, so every non-tactile baseline is friction-blind by construction.
   - The comparator set {CSF-1, Mondrian-CSF, CertGrip-P} cannot use any proxy for friction.
   - A short Coulomb calculation predicts most of the margin, and the oracle decomposition (51.7 % of the gap closed) shows it.
   - The paper acknowledges this, but the headline and C2 still present the 42 % as the main finding.
   - The scientifically open question is H2b, whether learning on top of the onset helps beyond a calibrated physics formula. That question remains unresolved at the primary σ.
2. **The probe is not new.** Friction estimation by force reduction to slip is classic, and the cited friction-estimation and incipient-slip controllers already use it. The novelty is the pairing with a distribution-free certificate. That certificate is the standard CRC theorem, and its offline version cannot be deployed: it needs F\* labels and 20 replays per instance.
3. **Simulation only, and the operating point is assumed.**
   - σ = 0.2 is not grounded in any sensor measurement.
   - The effect shrinks to D = 0.14 at σ = 0.4.
   - MuJoCo's soft-constraint contact does not resolve partial slip, so the "incipient-slip" detector actually detects gross-slip saturation.
   - For a robotics venue, the absence of a hardware probe experiment (even onset noise measured on one real sensor) is the major gap.
4. **Missing baselines that practitioners would use.**
   - No reactive slip-tightening controller.
   - No uncalibrated "probe + hand-set margin" rule in the style of khamis2021real. RAW-Q/RAW-G in H1c are only a partial substitute: they use the full learned feature set and report label slip.
   - No non-tactile baseline with a noisy friction proxy (for example a vision-like μ̂ with a given error).
   - Without these, readers cannot tell what the certificate buys over existing practice.
5. **The detector characterisation is overstated.** The paper says the +0.319 bias "is constant across instances, so a calibrated rule absorbs it". In the raw data the detector error correlates with log μ (r = −0.25), and its SD is four times larger for capsules (F3, 0.196) than for cylinders (F2, 0.045). This friction- and family-dependent error is exactly what calibration does not absorb. It is a plausible mechanism for several results: the 0.21 residual D-μ of CertGrip-full at σ = 0.2, the D3 weakness and the H2-R reversal. It should be reported and discussed.
6. **The lateral-pull (D3) weakness is left unexplained** in every family, and the paper offers an untested reading. A per-cell analysis of μ̂ error versus needed force under D3 is cheap with the existing rows.

**Actionable revisions (A)**
- A1. Correct the Abstract: 0.4739 is CertGrip-full against the squeeze arm *full*. Against the proprioceptive arm P, D = 0.4555.
- A2. Replace "the bias is constant across instances" with the measured dependence (corr with log μ, SD per family) and discuss its consequences.
- A3. Add at least one practitioner baseline: probe + fixed margin (uncalibrated, report its physical slip), or a reactive tightening rule. Better, add a non-tactile μ-proxy arm at a few proxy noise levels, so the H2a margin becomes a curve rather than a property of one distribution.
- A4. Put the "friction-blind by construction" caveat and the analytic expectation next to the headline D in the Abstract and C2. Frame H2b as the open scientific question.
- A5. If at all possible, measure onset noise on one physical sensor and gripper (even 20 objects) to anchor σ.

---

## Reviewer B (statistics, conformal methods, pre-registration): score 5/10 (borderline)

**Summary.** The paper applies CRC to a monotonised physical slip loss on a 20-point λ-grid per disturbance stratum. It runs a pre-registered decision framework (Bonferroni over four core decisions, SESOI 0.10, TOST) with object-cluster bootstrap CIs, and adds an online score-space quantile-tracking study under three shifts.

**Strengths**
1. The CRC construction is correct and correctly scoped. Monotonising the loss gives L̃ ≥ L and keeps validity without assuming monotonicity. The paper is explicit that the guarantee is marginal and in expectation, not training-conditional, and per-stratum test slip above α for CSF-1 is presented honestly.
2. The bootstrap recomputes λ̂ on every draw without new simulation, which is the right way to propagate calibration variance. I reproduced the point estimates exactly from raw replays.
3. Decision rules are stated before the read-outs, and failed or inconclusive decisions are reported as such. The post hoc 08e grid is explicitly forbidden from upgrading a decision.
4. The grid-floor defect is found and disclosed, and its effect on H2b is quantified three ways.

**Weaknesses**
1. **Undisclosed deviation in the multiplicity plan.**
   - `07_hypotheses.md` (l.223, l.412) pre-registers Holm at 5 % within each secondary family.
   - It defines the H2-H safety guard on *Holm-adjusted* cell limits (l.445; also 08g §3).
   - 08f, 08g and 08h then state "Holm not applied".
   - The paper says secondaries were "pre-registered in 07 and operationalised in 08f–08h … unadjusted" and does not list the dropped Holm correction among the five deviations.
   - The conclusions probably survive (most secondary CIs are far from their margins), but this has to be listed as a deviation.
   - In the same vein, 07 pre-registered an efficiency frontier (RE against realised slip over the α grid) as a robustness figure. It is not shown.
2. **The method itself came from a pilot-driven amendment, and the paper underplays this.** In 07 the CertGrip arm was static plus squeeze touch, and the rationale said the pad readings "cannot reveal μ". After the pilot showed those features gave nothing, 08a (before any main-pool data) introduced the ramp-down probe, CSF-μ̂, the H2a/H2b split and the Bonferroni-over-four rule. This is legitimate, because it predates the main data. However, "pre-registered decision rules" in the abstract should be accompanied by one sentence saying that the probe arm and its comparators were defined in a pilot-driven amendment (08a). Otherwise "static touch adds nothing" reads as a discovery, when it was the pilot expectation stated in 08a item 5.
3. **Realised slip rates are not matched, and the label-route slips are not reported.**
   - CRC slip is 0.083 for CertGrip-full against 0.102 for CSF-1. CSF-1 slips more *and* uses more force, so D is conservative here. The paper should say so.
   - 07 pre-registers reporting the label-rule test slip rates of both methods. Those are 0.0846 / 0.1036 (CRC) and **0.1057 / 0.1146 on the label route**: both arms are above α on the label route.
   - In the H1-V direct-replay audit, label-route CSF-1 at α 0.10 slips physically at 0.1114, with CI\*\* [0.091, 0.134].
   - These numbers belong in Table 1 next to the label-route D, because the paper uses that D as corroboration.
   - Seed 4 of the CRC primary arm also slips at 0.1018. That is fine under an in-expectation bound, but it should be listed with the per-seed D values.
4. **Grid design.** The 08c grid is ±0.4 around a q̂_sel pooled over strata. Since D1/D2 and D3/D4 need very different offsets, the plug-ins land near the edges (CSF-1 at index 1, CSF-μ̂ at index 0). Pooling over strata was a foreseeable design weakness. The 08e per-stratum grid fixes it, and its H2a (0.4289) agrees. A short justification of why the pooled centring was pre-registered would help. So would stating that CSF-1's index-1 position (not at the floor) makes H2a itself unaffected, a point the paper only implies.
5. **H2b is unresolved, and the paper's wording should be tightened.** The label route gives "equivalence" (secondary), the 08e upper limit is 0.1001 and the 08c interval is [−0.040, 0.145]. Across label-route seeds, H2b is "equivalence" for seeds 0, 1 and 4 and "not confirmed" for seeds 2 and 3. The paper's "no demonstrated gain" is correct. The Discussion sentence "the probe is what makes it large" is fine. Statements that the learner "pays off only when the friction reading is noisy" rest on a secondary, unadjusted σ sweep, and the 08c and 08e routes disagree on its sign at σ = 0.1. Label them exploratory.
6. **The online study measures something narrower than its framing suggests.**
   - The H3 CertGrip arm is initialised from the *label-route* split-conformal q̂ (`h3_streams.py` `offline()`), not from the CRC primary.
   - Its feedback is the label rule in all 20 orderings, and the physical outcome is audited on ordering 0 only.
   - The oracle's realised slip is 0.075–0.135, because it recalibrates on 175 objects per stratum. That makes R_E a comparison between arms at different slip rates.
   - "Keeps the window slip rate near α" is therefore shown for label feedback, with one physical audit. The Abstract and Conclusion already hint at this. Section 3.5 and Table 3 should state explicitly that the offline starting point is the label route.
   - The paper also omits H3-B, which passed for all no-probe arms: the location model predicts frozen breakage within 0.004. That is a positive check of the shift model and is worth one sentence. The 08a note that about 42 % of S1 instances fall outside the probe arm's training μ support is also not mentioned.
7. **Overbroad statement about inference.** "All intervals CI\*\* are two-sided 97.5 % … 2,000 draws" is not true for D-μ and D-FID (500 draws, 95 %), the H2-H pooled CI (95 %) or UT3 (1,000 re-splits). The exceptions should be stated.
8. **Table 2 caption.** It says the H4a rows are "comparisons … against P". Only S vs P is. The other two compare full vs S and CertGrip-full vs full.

**Actionable revisions (B)**
- B1. Add deviation 6: Holm within secondary families (07 §4) and the Holm-adjusted H2-H guard were replaced by unadjusted CIs in 08f–08h. Optionally, report the Holm-adjusted H2-H guard; it passes easily, since the minimum cell lower limit is 0.16 at 97.5 %.
- B2. Add one sentence and a deviation entry: the onset probe, CSF-μ̂ and the H2a/H2b split come from the pilot-driven amendment 08a, made before any main-pool data.
- B3. Add realised label-rule and physical slip rates for both arms and both routes to Table 1, and include the per-seed slip rates. State that the unmatched rates make H2a conservative. Add the pre-registered efficiency frontier, or say why it is omitted.
- B4. State in Sections 3.5 and 5.5 that the online arms start from the label-route q̂, and report H3-B.
- B5. Fix the inference-protocol sentence and the Table 2 caption.
- B6. Shorten to fit 9 pages: cut the abstract to about 220 words and move the robustness bullets and secondary tables to an appendix.

---

## Recommendation

Both reviewers: borderline, leaning reject for NeurIPS/ICML in its current form.

The work is executed carefully and reported transparently. All headline numbers reproduce from the raw files, and no fabrication was found. However:
- the confirmed result is largely a consequence of the instance distribution;
- the open scientific question (learned versus plug-in) is unresolved;
- the online efficiency question is inconclusive;
- everything is simulation-only, with an assumed noise level.

With a hardware anchor for σ, a friction-proxy non-tactile baseline and the disclosure fixes below, it would become a solid robotics-venue paper (RSS/CoRL).

Scores: **Reviewer A 4/10, Reviewer B 5/10.**

## Top must-fix items

1. Abstract: "D = 0.4739 against the proprioceptive arm" is wrong. 0.4739 is CertGrip-full vs the squeeze arm *full*; against P, D = 0.4555.
2. Add the undisclosed deviation: 07 pre-registered Holm within secondary families and a Holm-adjusted H2-H guard, and 08f–08h dropped both.
3. Disclose that the probe arm, CSF-μ̂ and the H2a/H2b split were introduced in the pilot-driven amendment 08a, replacing the original static/squeeze-touch CertGrip of 07.
4. Report the realised slip rates for both arms and routes in Table 1: label route 0.1057 / 0.1146, H1-V CSF-1 physical 0.1114, CRC seed 4 0.1018. Note that the unmatched CRC rates make D conservative, and add or explain the missing pre-registered efficiency frontier.
5. Replace "the detector bias is constant across instances" with the measured μ-dependence (r = −0.25) and family-dependence (F3 SD 0.196 vs F2 0.045), and discuss what it implies for D-μ, D3 and H2-R.
6. State that the online study's CertGrip arm starts from the label-route q̂ and uses label feedback, with a physical audit on ordering 0 only. Report the passed H3-B check and the S1 out-of-support caveat.
7. Make clear that H2a is near-guaranteed by the friction-independent design. Add a non-tactile friction-proxy baseline (or a correlated-μ pool) and a practitioner baseline (probe + fixed margin, or reactive tightening).
8. Fix the inference-protocol overstatement (D-μ, D-FID and H2-H use 500 draws or 95 % CIs) and the Table 2 caption. Cut the paper to 9 pages, including an abstract of about 220 words (currently 345).
