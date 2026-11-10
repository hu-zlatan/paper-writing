# Stage 18 v2 — Simulated peer review, run 1

Paper: *Probe, Then Certify: A Tactile Friction-Onset Probe with Conformal Risk Control for Certified-Slip Minimal-Force Grasping*
Reviewer stance: balanced conference reviewer who checks that the methodology matches the evidence.
Evidence used: the draft and the evidence block in `prompts/stage18_v2_user.txt`, plus my own reading of `code/`, `docs/`, `plans/` and the raw replay files in `results/v1/{crc,crc_v2,labels}` and `results/v2/{crc09,b3}`. I re-ran the point estimates with the repository's own analysis functions. As instructed, I opened no other review files (18_*, 20_*) and no results/14_* or 15_* files.

---

## 0. Verdict at a glance

| Item | Result |
|---|---|
| **CRITICAL FABRICATION** | **No.** All 40 numbers I spot-checked match the JSON. The 26 point estimates I recomputed from raw replays match to every printed digit. The trial, seed, ordering, draw and instance counts claimed in the paper match the code and the files. |
| Trial count | Consistent. 4,800 grid instances (2,000 cal = 500 per stratum, 2,800 test = 700 per stratum). Predictor seeds 0–4. 20 orderings (`N_ORD = 20`, h3_streams.py). 5 orderings × 2 arms × 2 shifts = 20 B3 stream files of 2,000 steps each. 2,000 bootstrap draws everywhere stated. No inflated "N independent trials" claim. |
| Statistical tests claimed vs present | Present in code. Object-cluster bootstrap with λ̂ refitted per draw, CI** at the 1.25 / 98.75 percentiles (analysis_crc.py, analysis_v2_a.py). Clopper–Pearson (analysis_h1m.py, analysis_v2_a.py). DerSimonian–Laird pooling (secondaries_08g.py). Grouped CV R² (secondaries_08f.py). There are no ANOVA or t-test claims. |
| Topic drift | None material. Environment details (grid-floor defect, CPU model not logged) are reported as deviations or limitations, not as contributions. |
| Length | **Over-length, not under-length.** About 8,800 words plus 6 tables and an algorithm block; every section is above the minimum (Abstract 244, Intro 1,052, Related 564, Method 1,851, Setup 1,281, Results 2,566). This will not fit in 9 NeurIPS/ICML pages. |
| Scores | Reviewer A (ML / statistics) **5 / 10**. Reviewer B (robotics / tactile) **4 / 10**. Consolidated **4.5: borderline, leaning reject** for NeurIPS/ICML in the current form. |

---

## 1. Spot-check of numbers (40 checked; R = recomputed from raw replays with the repo's own functions, J = matched against the analysis JSON)

| # | Claim in draft | Source | Check | Status |
|---|---|---|---|---|
| 1 | H2a D = 0.4168 | crc/*.jsonl + labels → `analysis_crc.evaluate` | R: 0.416821 | ✓ |
| 2 | CertGrip-full RE 0.4567, slip 0.0829 | same | R: 0.4567 / 0.0829 | ✓ |
| 3 | CSF-1 RE 0.7832, slip 0.1021 | same | R | ✓ |
| 4 | λ̂ idx CertGrip 10/10/11/10; CSF-1 1/1/15/14; CSF-μ̂ 0/0/14/12 | same | R | ✓ |
| 5 | Per-stratum slip CertGrip 0.0871/0.0714/0.0757/0.0971; CSF-1 0.1157/0.0886/0.1057/0.0986 | same | R | ✓ |
| 6 | σ curve D 0.6789 / 0.5825 / 0.4168 / 0.1401 | same | R | ✓ |
| 7 | H2b primary 0.0569 | same | R: 0.056918 | ✓ |
| 8 | Refined grid H2a 0.4289, H2b 0.0240, CSF-μ̂ RE 0.4551 slip 0.0750 | crc_v2/*.jsonl | R | ✓ |
| 9 | CertGrip refined RE 0.4442 slip 0.0900 | crc_v2 | R | ✓ |
| 10 | D_match 0.4563, RE_match 0.4290 / 0.7891 | analysis_v2_a.stats on crc | R | ✓ |
| 11 | D_ltt 0.4043; LTT idx 10/10/12/11; slip 0.0696, RE 0.4895; CSF-1 0.0907 / 0.8216 | same | R | ✓ |
| 12 | Refined D_match 0.4475, D_ltt 0.4015 | same on crc_v2 | R | ✓ |
| 13 | Onset-only D_crc 0.4464 / D_match 0.4736; CSF-μ̂ D_match 0.4690 / 0.4793, D_ltt 0.3704 / 0.4040, D_crc 0.3816 / 0.4149 | same | R | ✓ |
| 14 | "onset-only larger on all six route × grid rows" | same | R: 6/6 | ✓ |
| 15 | Fig. 1b frontier points (36 points, 4 arms) | a_analysis(.json / _08e) | J; CertGrip, onset-only and CSF-1 primary also R | ✓ |
| 16 | B2 test slip 0.9582 / 0.8257 / 0.6182 / 0.3350; RE −0.3829 / −0.2287 / −0.0744 / 0.2341 | crc09/*.jsonl + labels | R | ✓ |
| 17 | B2 κ=1 strata 0.0414 / 0.0229 / 0.6571 / 0.6186 | crc09 | R | ✓ |
| 18 | B3 Table 3 lower block (6 rows × 4 values) | b3/*.jsonl + labels | R: all 24 | ✓ |
| 19 | B3 per-ordering range 0.082–0.112 | b3 | R | ✓ |
| 20 | Monotonicity CP upper 0.02115 (8/800) | scipy `beta.ppf(0.9875, 9, 792)` | R: 0.021147 | ✓ |
| 21 | Splits: cal objects 200–324, test 325–499; n_cal 500 per stratum; 2,800 test | labels + crc_grids | R | ✓ |
| 22 | COMP selection 0.7686 / 0.8294 / 0.8335 | comp_selection.json | J | ✓ |
| 23 | H5: 0.8361, 0.5042, −0.0299 (edge), 0.0514 (primary) with CIs | b_analysis(_edge).json | J | ✓ |
| 24 | Proxy RE 2.786, 0.9213, 0.4312 (slip 0.0825) | same | J | ✓ |
| 25 | H3 R_E 0.8778 / 1.174 / 0.9629 with CIs; S1m 0.8871 [0.7723, 1.026] | h3_analysis.json | J | ✓ |
| 26 | Frozen 0.3056 / 0.5101 (S1), 0.2461 (S3) | same | J | ✓ |
| 27 | Physical audit 0.103 / 0.092 / 0.101; matched diff 0.032 / −0.035 | same | J | ✓ |
| 28 | ρ − ρ_ID 0.0857 [−0.0444, 0.1859]; ΔC 58.15 / 42.40 | h3_analysis, sec08h_h3s | J | ✓ |
| 29 | η = 0.03412, η = 0.1 × IQR | h3_streams.py l.72–76 + JSON | code + J | ✓ |
| 30 | H4a −0.0084, −0.0263, 0.4739; H4c −0.0253 | h4a_label_rule, sec08f_label | J | ✓ |
| 31 | H2-H pooled 0.4388, τ 0.0511, Q 31.04; D3 cells 0.2979 / 0.3868 / 0.3115 / 0.3348; min cell lower 0.1602 | sec08g.json | J | ✓ |
| 32 | H2-R −0.2614 [−0.5320, −0.0325], n 352 / 548 | sec08g.json | J | ✓ |
| 33 | T = 0.5918 [0.5540, 0.6564]; oracle share 0.5172 | sec08f_tail, sec08g | J | ✓ |
| 34 | D-μ R² 0.7937 / 0.6034 / 0.0105 / 0.0452 / 0.2142 / 0.5655 / 0.0054 | sec08f_dmu | J | ✓ |
| 35 | Detector r 0.9480, bias +0.3186, SD 0.1103; err r −0.2529; capsule SD 0.1965; median disp 0.126 mm, 0 ≥ 2 mm | 19_report_rows | J | ✓ |
| 36 | Seeds 1–4: 0.4343 / 0.4197 / 0.3932 / 0.4494; label route 0.4145–0.4442 | crc_analysis, h2_label_rule | J | ✓ |
| 37 | Compute 14.50 = 5.72 + 8.03 + labels 0.60 + mono 0.15; v2 2.357 = 1.347 + 0.868 + 0.142 | 19_report_rows, compute_v2 | J | ✓ (scope caveat, see M8) |
| 38 | Protocol constants (F₀ 32.7 N, T 0.25 s, floor 0.005, w 6, k 8, consec 2, r_arm 0.1, n_min 1 mN, t_up 0.02, taxel noise, dt 0.002, elliptic, impratio 10, condim 6) | certgrip/sim.py + replay headers | code | ✓ |
| 39 | Learner search (30 configs, GroupKFold 4, ranges) | certgrip/models.py | code | ✓ |
| 40 | H1c "0.0096–0.0507 above α, every CI** above 0" | sec08h_h1c.json | J | **⚠ selective.** True only for RAW-Q / RAW-G. The registered RAW-Qv has CI** containing 0 at every α and is not reported (see M3). |

Small imprecisions, not fabrication:
(i) §5.2 says "static touch reads F₀ and m g/2". The normal reading is within 0.16 N of F₀, but the shear deviates from m g/2 by up to 6.40 N, with 24 instances off by more than 1 % (19_report_rows `static_touch_check`).
(ii) "OQT-CertGrip window slip between 0.0999 and 0.1016": S1 is 0.10155, which is a rounding-edge case.
(iii) The sim.py docstring says the detector runs at 100 Hz, but `frame_steps = 1` means 500 Hz. The paper's 500 Hz is correct; the docstring is stale.

---

## 2. Methodology–evidence consistency (check 2)

Confirmed consistent:
- **CRC.** `lam_index`: smallest λ with (n R̃ + 1)/(n + 1) ≤ α, R̃ monotonised by a reverse cumulative maximum. This is exactly Eq. in §3.4.
- **Fresh replays.** Every (instance, λ) loss is a fresh replay at F(x; λ), so the paper's "not the bisection label" is correct.
- **Bootstrap.** Cal and test objects are resampled within family, all 4 instances of an object move together, and λ̂ is recomputed in every draw. The 1.25 / 98.75 percentiles match the Bonferroni 0.0125 one-sided split.
- **LTT.** Fixed-sequence scan from the top of the grid with a CP(1 − δ) upper bound ≤ α.
- **Matched slip.** Linear interpolation between adjacent k with clipped indices; 2,000 of 2,000 valid draws.
- **Plug-ins and features.** CSF-1 and CSF-μ̂ formulas, the μ̂ clip [0.1, 3] and the onset noise model (`log F_onset + σ ε`, ε fixed per instance) are as described. Feature sets P ⊂ S ⊂ full ⊂ full_rd and P_onset are as in the text.
- **Slip reference.** The reference is the pre-probe pose, so probe displacement counts against the 2 mm budget. That holds for all arms.
- **Disturbances.** They are inertial pseudo-forces on the object with a still mocap hand, as disclosed.
- **Deviations.** The selection split deviation (200–249 vs 150–199 in 08b) is real and disclosed. H2-R was pre-registered in 07 §4 "with no prediction", as the paper says. The H5 prediction in 09 §B1 ("superiority at σ_p 0.8, margin shrinking; report where CI first includes 0") was registered and held as the paper says. The B3 pilot rule of ≤ 6 CPU-h is in plans/stage_13_v2_b3 and docs/09.

Discrepancies and omissions (none rise to fabrication):
1. **H1c, selective report.** 07 §4 and 08h §1 register three uncalibrated targeters: RAW-Q, RAW-G and RAW-Qv (validation-tuned shift, "the practitioner baseline 07 meant"). The paper's "uncalibrated targeters over-slip at every level … every CI** above 0" silently drops RAW-Qv. RAW-Qv's slip − α is 0.0029 / 0.0161 / 0.0125 / 0.0396 at α = 0.01 / 0.05 / 0.10 / 0.20, and every CI** contains 0. This matters because it shows a non-conformal validation-tuned quantile already lands near α in distribution at n = 500. That bears directly on what CRC adds.
2. **D-FID omitted.** This is a registered secondary (08h §4). Touch-only features classify object family at 72.6 % [70.1, 75.1] (chance 25 %). It is not a friction channel, but it qualifies "static touch is uninformative" and should be reported.
3. **Route not named in text.** Several headline secondaries run on the **label route**, whose validity premise failed: the 16-cell pooled D 0.4388 and cell CIs, the oracle gap share 0.5172, H2-C vs Mondrian, the H4 chain, H2-M and H2-R. Table 1 marks some of them, but §5.1 states the pooled D, the cell results and the oracle share without naming the route.
4. **Compute scope.** "Logged compute for the first-round study is 14.50 CPU-hours" counts CRC grid replays, labels and monotonicity replays only. Predictor fits, H3 streams, pilots and h1v are not in that sum (19_report_rows `compute_logged_cpu_hours`). It should say "logged simulation replays".
5. **Excluded instances not stated.** RE is computed over "avoidable" test instances; unavoidable ones count as slips at every λ. In the id pool there are 0 unavoidable instances (checked), so nothing changes numerically, but §3.1 should say so.
6. **Fig. 1b mixes grids.** CSF-μ̂ is drawn on the refined grid and the other three arms on the primary grid. The legend notes this, but one frontier figure with two calibration grids is not like-for-like. Plot all four on the refined grid, or both grids in two sub-panels.

---

## 3. Reviewer A: machine learning / statistics (conformal methods)

**Summary.** The paper calibrates a family of grip-force rules with conformal risk control on a monotonised binary physical-slip loss, per disturbance stratum. It compares a tactile ramp-down "onset" feature against the best non-tactile conformal baseline, selected on a disjoint split. It also adds Learn-then-Test, matched-slip frontiers and online quantile tracking under shift. Everything is in MuJoCo.

**Strengths**
1. **Exceptional confirmatory hygiene.** The pre-registration was written before the data, Bonferroni over four core decisions, an SESOI, and every deviation listed once. The draft reports that only 1 of 4 core decisions is confirmed. I rarely see this level of candour, and the numbers reproduce exactly from raw replays.
2. **The comparator is chosen properly.** COMP was selected on a disjoint selection split before calibration or test data were read. That is the right way to avoid the strawman "uncalibrated controller" baseline.
3. **The certificate is on the physical outcome, not on simulator labels.** When the monotonicity gate failed, the registered branch to CRC on the monotonised physical loss is statistically sound: L̃ ≥ L, L̃ is monotone in λ, and CRC holds for bounded monotone losses.
4. **Robustness is shown on several axes.** The result holds under CRC, matched slip and LTT on two grids, under seed refits and with small n. The paper correctly separates route robustness (re-analysis of the same replays) from replication (refits).
5. **Interval estimation is careful.** The object-cluster bootstrap recomputes λ̂ inside every draw, so calibration-draw variability is in the CI. That is the right uncertainty for an in-expectation bound.

**Weaknesses**
1. **The statistical contribution is a direct application.** CRC with a binary loss (Angelopoulos et al. 2022), LTT (2025) and score-space quantile tracking (2023) are used as-is. The monotonisation is a one-line max. Nothing here is new statistically; the novelty claim must rest on the robotics protocol.
2. **The effect size is largely set by design choices.** μ is drawn log-uniform on [0.3, 1.0], independent of every non-tactile input "by construction". So any friction-aware rule must beat any friction-blind one, and the size of D is a function of (i) the μ range and (ii) the assumed onset noise σ. D falls from 0.68 at σ = 0 to 0.14 at σ = 0.4. The narrow-range sub-pool (μ ∈ [0.5, 0.8]) reverses the sign. H5 shows a σ_p = 0.2 non-tactile prior matches the probe. The "≈ 42 %" headline is therefore a statement about σ = 0.2 and a 3.3× friction range, not a measured property of tactile sensing. The limitations say so, but the abstract and conclusion lead with 0.4168 as if it were a general effect.
3. **What does conformal add over a tuned validation shift?** RAW-Qv, the registered practitioner baseline, achieves slip near α at every level in distribution. It is omitted (M3). Without it, the reader cannot judge whether the certificate buys anything beyond the finite-sample +1 correction at n = 500. The honest framing is that the value of CRC here is the finite-sample statement plus a per-stratum offset, and that under shift neither frozen CRC nor frozen RAW-Qv survives. The paper should show this.
4. **The co-primary H2b contrast is uninterpretable on its registered grid.** The plug-in arm sat on the primary grid floor in D1/D2. The draft discloses this, but the main attribution claim ("the plug-in already captures it") then rests on post hoc refined-grid and secondary results. The contrast is "not confirmed", not "equivalent". The wording "captures the saving" in the abstract, contributions and conclusion is stronger than "no demonstrated gain". Use one consistent hedge.
5. **The certificate's scope is narrow.** It is marginal per stratum and in expectation over the calibration draw. LTT is per stratum at δ = 0.1, not family-wise across 4 strata (family-wise δ ≈ 0.34 by a union bound). CertGrip seed 4 realises test slip 0.1018 > α on the primary grid; CSF-1 realises 0.1157 in D1. Both are compatible with an in-expectation bound, but readers will take "certified" more strongly. Report the union-bound δ or apply Bonferroni across strata for LTT.
6. **Multiplicity in secondaries.** There are more than 60 unadjusted secondary intervals; Holm was registered and then dropped by addendum. The H2-R reversal (lower limit −0.0325) and several "superiority" secondaries would be fragile under Holm. At minimum, report Holm-adjusted versions for the secondary families named in 07 §4.
7. **The online study is underpowered and partly descriptive.** H3 is inconclusive in all three shifts (realised half-widths 0.15–0.20). The deployable physical-feedback variant has 5 orderings and no intervals. Online quantile tracking keeping long-run slip near α is guaranteed by the update identity (UT4) itself, so "keeps slip near α" is confirmation of a theorem, not a finding.

**Actionable revisions (A)**
- A1. Report RAW-Qv in §5.5 and add a per-stratum validation-tuned margin on the CSF-μ̂ plug-in as an uncalibrated-but-tuned baseline. Then state plainly what CRC adds.
- A2. Rewrite the abstract and conclusion lead as a conditional claim: "at an assumed onset noise of σ = 0.2 and μ spread 3.3×, D = 0.42; D = 0.14 at σ = 0.4; reverses for μ ∈ [0.5, 0.8]". Plot D against σ and against μ range as the central figure.
- A3. Harmonise the H2b wording to "no demonstrated gain (not confirmed; not equivalent)" everywhere, and drop "captures".
- A4. Give the family-wise LTT level across strata, or rerun LTT at δ/4.
- A5. Name the route (CRC vs label) for every number in §5.1–5.2 prose.
- A6. Report Holm-adjusted secondaries as registered in 07 §4, or justify the addendum change beyond "operational".

**Score A: 5 / 10 (borderline).** The work is rigorous and honest and every number is real. But the statistical machinery is off-the-shelf, the main effect is close to guaranteed by the simulation design and an assumed noise level, and the most informative practitioner baseline is left out.

---

## 4. Reviewer B: robotics / tactile manipulation

**Summary.** A parallel-jaw gripper in MuJoCo preloads at a fixed 32.7 N, squeezes, then ramps force down until a modelled touch-grid detector reports incipient slip. μ̂ = m g/(2 F_onset) feeds a force rule whose log offset is calibrated per disturbance type.

**Strengths**
1. **The protocol design is clean.** A friction-free preload isolates the ramp-down onset as the only friction channel. The nested ablation (P → S → full → +onset) cleanly shows that static touch and the squeeze carry nothing and the onset carries everything (D 0.4739 for adding the onset).
2. **A strong, practical takeaway.** A one-line Coulomb plug-in on the onset, calibrated, is about as good as a learned quantile model at σ = 0.2. That is useful advice for the tactile-learning community, and it is stated with the right caveats about σ dependence.
3. **The failure regime is honest.** The narrow-friction sub-pool where the method loses is reported, as are the weak lateral-pull cells and a non-tactile prior that ties.
4. **Reproducibility is good.** Constants are in the replay headers, replays are deterministic, and the code is clean enough that I could recompute every headline number in minutes.

**Weaknesses**
1. **Simulation only, with a modelled sensor and an assumed noise level.** There is no hardware and no measured σ. The detector, the taxel noise and σ = 0.2 are all assumptions, and the effect is highly sensitive to σ. For a tactile paper this is the single largest gap. One real gripper with a GelSight or BioTac-class sensor, even on 10 objects, would change the evaluation.
2. **The contact physics is narrow.** The contact is rigid and soft-constraint, there are no elastomer pads, there are four primitive families, and the pads share μ with the object. The "touch-only detector" reads MuJoCo touch_grid shear/normal ratios, which under Coulomb saturate exactly at μ. Real incipient-slip signals (partial slip at the contact periphery, viscoelastic creep) are far messier. The +0.32 log-unit detector bias and the capsule-specific error (SD 0.20) hint at this, even in simulation.
3. **The disturbances are not robot motions.** D1/D2 are applied as pseudo-forces with the hand fixed, so there is no actual lift, no arm dynamics and no pad compliance coupling. "Lift acceleration" and "shake" are body forces on the object.
4. **The offline certificate is not deployable.** It needs 20 replays of the *same* grasp instance at different forces, for every calibration grasp. On hardware that means 20 physically identical re-grasps, which is not achievable. The only deployable route is OQT, whose guarantee is long-run and was run on 5 orderings without intervals. Title, abstract and C1 should not lead with "certified" without immediately saying "in simulation; online tracking is the hardware route".
5. **The probe drives every object to incipient slip on every grasp.** For the motivating fragile or valuable objects that is itself a risk. The median displacement is 0.126 mm and the maximum 1.92 mm, which is close to the 2 mm slip threshold. The probe costs about 0.37 s per grasp. The paper notes the scope limit, but the motivation ("fragile, valuable") and the method conflict.
6. **The baselines are missing the obvious robotics competitor.** No reactive slip-detection-and-tighten controller was evaluated (e.g. dong2019, veiga2020-style). The probe + fixed-margin study (B2) is close to a strawman: the D3/D4 plug-in force ignores the hidden external load, so no uniform κ can work. A per-stratum tuned margin (a practitioner's first idea) is missing.
7. **Too long and too dense.** About 8,800 words, 6 tables and hundreds of four-decimal numbers. The main story (probe → plug-in → CRC; σ dependence; failure regime) is buried. Table 0's 9-row hypothesis ledger and the deviation paragraph belong in an appendix for a 9-page venue.

**Actionable revisions (B)**
- B1. Add even a small hardware experiment, or at minimum a measured onset-noise level from a real sensor (literature-derived if necessary), and place σ_real on the D(σ) curve.
- B2. Add a reactive slip-tightening baseline and a per-stratum tuned-margin baseline.
- B3. Re-title or re-frame: "certified in simulation". In the abstract, state that the offline certificate needs simulator replays and only OQT is deployable.
- B4. Discuss the probe's own risk for fragile objects and its time cost. Report the distribution of probe displacement relative to the 2 mm budget, per family.
- B5. Cut to 9 pages. Main text: protocol, CRC, H2a + σ curve + H2-R + H5, attribution chain, a short online section. Move LTT, matched-slip tables, D-μ diagnostics, compute, deviations and B2/B3 to the appendix.
- B6. Fix the small text issues: "static touch reads m g/2" (shear deviates by up to 6.4 N in 24 instances), report D-FID (touch identifies family at 72.6 %), and name the route for pooled-cell and oracle-share numbers.

**Score B: 4 / 10 (borderline reject).** A careful simulation study with a sensible protocol and honest attribution. But there is no hardware, the sensor and noise are modelled, the "certificate" is not deployable, and the strongest robotics baseline is absent. Better suited to CoRL or RSS once hardware or measured σ is available.

---

## 5. Check-list answers

1. **On topic?** Yes. Every section serves the stated topic (probe + CRC; non-tactile comparator; attribution; online shift). The grid-floor defect and the monotonicity failure appear as deviations or validity results, not as contributions. Compute and CPU-model remarks are environment details best moved to the appendix.
2. **Methodology–evidence consistency.** High. The issues are listed in §2: selective H1c, D-FID omitted, route unnamed, compute scope, mixed-grid figure.
3. **Trial count.** No mismatch, so no CRITICAL flag. A single simulation pool with seed-0 replays is re-analysed by several routes, and the paper says so explicitly ("route robustness, not replication").
4. **Length.** All sections exceed the minima; the paper is over the 9-page budget. It needs cutting, not padding.
5. **Top-conference judgement.**
   - Novelty: incremental. Ramp-down friction probing and CRC are both known; the protocol and the attribution are the contribution.
   - Baselines: COMP is selected properly; a reactive controller and a tuned practitioner margin are missing.
   - Ablations: meaningful and well designed.
   - Claims: supported, except where "captures" and "certified" overreach.
   - Limitations: unusually honest.
   - Recommendation: not yet. **4.5 / 10, borderline.**

---

## 6. Consolidated must-fix list (priority order)

1. **M1: State the headline as conditional on σ and the μ range.** In the abstract, intro and conclusion, make D = 0.42 explicitly a σ = 0.2 / μ-range-3.3× result. Promote the D(σ) curve and H2-R to the headline figure.
2. **M2: Re-scope "certified".** The offline CRC/LTT certificate needs simulator replays and is not deployable; only OQT is (5 orderings, no CI). Say so in the title or abstract, and give LTT's family-wise δ across strata.
3. **M3: Report RAW-Qv in §5.5** (registered H1c arm; CI** contains 0 at every α) and say what CRC adds over a validation-tuned shift. Add a per-stratum tuned-margin plug-in baseline.
4. **M4: One hedge for H2b everywhere.** Use "not confirmed / no demonstrated gain" and remove "already captures it"; the registered contrast was biased by the grid floor and is not equivalence.
5. **M5: Add a reactive slip-tightening controller baseline, or justify its absence prominently.** Reframe B2 as a demonstration that per-stratum offsets are needed, not as evidence against hand-set margins.
6. **M6: Name the route (CRC vs label) for every secondary number in prose** (pooled cells 0.4388, oracle share 0.5172, H2-C, H4 chain, H2-M), and either plot Fig. 1b on one grid or show both grids.
7. **M7: Cut to the 9-page limit.** Move Table 0 detail, the deviation list, compute, LTT and matched-slip tables, D-μ diagnostics and B2/B3 to the appendix; reduce four-decimal clutter.
8. **M8: Small factual fixes.** "Static touch reads m g/2" (shear up to 6.4 N off, 24 instances >1 %). Report D-FID (72.6 % family accuracy from touch). Compute "14.50 CPU-h" means logged replay jobs only. State that RE excludes unavoidable instances (0 in the id pool). Holm-adjusted secondaries as registered, or justify dropping them.

**CRITICAL_FABRICATION: NO.**
