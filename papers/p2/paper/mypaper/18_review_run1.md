# Stage 18 — Simulated Peer Review (run 1)

**CRITICAL_FABRICATION: no.**
Reasons: (1) The evidence block in the prompt is byte-identical (after JSON parsing) to `results/v1/results_v1.json`. All ~120 numbers I compared in the draft match that file to the reported precision; one Table 3 cell has a last-digit rounding difference. (2) Every trial and sample count the paper states matches code and raw files: 2,000 cal / 2,800 test / 800 selection instances; 20-point grid; 2,000 bootstrap draws; predictor seeds 0–4; 20 orderings; 2,096 / 1,500 stream instances. The draft never claims "N independent runs" that did not happen. Each instance is one deterministic simulation; replication comes from instances, refit seeds and orderings, and the draft says so. (3) Three numbers recomputed from raw replays/labels reproduce exactly: H2a D, H2b D, and the H1-M count. (4) Every `\cite` key (52) exists in `docs/05_knowledge_cards.json`. There *are* method-description discrepancies (geometry families described but not implemented, an understated compute figure, a misattributed maximum). They are listed below as MAJOR/MINOR, not as fabrication of results.

Word count (paper body, excluding the figure prompt): Abstract 276, Introduction 879, Related Work 547, Method 1,607, Experimental Setup 1,202, Results 1,784, Discussion 580, Limitations 268, Conclusion 221. **Total ≈ 7,380.** Every section is above the minimum. The paper is not under-length. At ~7.4k words plus three tables, an algorithm box and a full-width figure, it is probably **over** a 9-page NeurIPS/ICML limit (see must-fix 8).

Topic adherence: the paper stays on topic (probe + CRC on physical slip vs. the strongest non-tactile conformal baseline, ablations attributing the saving, online binary-feedback study under shift). Nothing drifts to unrelated topics. Environment details appear only in the Compute paragraph ("free GitHub Actions runners") and are not presented as contributions. That sentence can be dropped.

---

## Spot-checks (35)

| # | Draft claim | Source checked | Result |
|---|---|---|---|
| 1 | H2a D = 0.4168 [0.3484, 0.4778] | `crc_analysis.json` H2a; **recomputed from `results/v1/crc/*.jsonl` + labels via `analysis_crc.build/evaluate`** → 0.416821 | ✓ |
| 2 | CertGrip-full RE 0.4567, phys slip 0.0829; CSF-1 RE 0.7832, slip 0.1021 | recomputed from raw replays: 0.45673 / 0.08286; 0.78318 / 0.10214 | ✓ |
| 3 | H2b D = 0.0569 [−0.0399, 0.1454], CSF-μ̂ RE 0.4843 slip 0.0657 | recomputed from raw: 0.056918; 0.48430 / 0.06571 | ✓ |
| 4 | onset-only RE 0.4336, slip 0.0857 | recomputed from raw: 0.43357 / 0.08571 | ✓ |
| 5 | H1-M: 8 of 800 non-monotone, 7 under D2 | **recomputed from `results/v1/mono/id_F*.jsonl`**: 800, 8, D1 1 / D2 7 | ✓ |
| 6 | CP upper 0.02115 | `scipy.stats.beta.ppf(0.9875, 9, 792)` = 0.0211471 | ✓ |
| 7 | "largest slip force above F*_hi exceeds it by 0.00904", given in the context of the 8/800 | `h1m_analysis.json` violations: 0.00904 comes from the **S3 and S2 shift-pool** violations; the max over the 8 id instances is 0.00225 | ✗ misattributed (minor) |
| 8 | COMP = CSF-1 (0.7686 vs 0.8294 / 0.8335) | `comp_selection.json` | ✓ |
| 9 | F*_lo / F*_hi D 0.4150 / 0.4186 | `crc_analysis.json` | ✓ |
| 10 | Seed range 08c 0.3932–0.4494; label 0.4145–0.4442 | crc / h2_label_rule seeds 1–4 | ✓ |
| 11 | 08e H2a 0.4289; H2b 0.0240 [−0.0949, 0.1001]; σ0 −0.1522; σ0.4 0.3315 | `crc_analysis_v2.json` | ✓ |
| 12 | σ curve D 0.6789 / 0.5825 / 0.4168 / 0.1401; σ* = 0.4, lower 0.0832 | `crc_analysis.json` | ✓ |
| 13 | 08c H2b σ0 0.2461, σ0.1 0.1072 "superiority" | `crc_analysis.json` | ✓ |
| 14 | λ̂ floor: CSF-μ̂ index 0 in D1/D2 at σ ≤ 0.2; CSF-1 index 1 | `lam_idx` in crc_analysis.json; recomputed | ✓ (but see must-fix 5: σ = 0.2 is affected too) |
| 15 | H2-C vs Mondrian 0.4381; oracle gap 0.5172 [0.4489, 0.5762]; oracle RE 0.1271 | `sec08g.json` | ✓ |
| 16 | H2-H pooled 0.4388, τ 0.0511; min cell F1D3 0.2979; every lower > 0.16 | `sec08g.json` H2H (min lower F3D3 0.1602) | ✓ (Q = 31.0 on 15 df not reported) |
| 17 | H2-T T = 0.5918 [0.5540, 0.6564] | `sec08f_tail.json` crc_08c | ✓ |
| 18 | H2-R D −0.2614 [−0.5320, −0.0325], n_cal 352, n_test 548; μ∈[0.5,0.8], mid-50 % amplitude | `sec08g.json`; `secondaries_08g.py` l.63–64 | ✓ |
| 19 | H2-n 0.4146 (α 0.10), 0.4654 (α 0.20) | `sec08g.json` H2n | ✓ |
| 20 | H4a: −0.0084, −0.0263, 0.4739 with CIs | `h4a_label_rule.json` | ✓ |
| 21 | H4e −0.0534 [−0.1233, 0.0508]; label −0.0417 equivalence | crc / h2_label_rule | ✓ |
| 22 | H4c −0.0253 [−0.0526, 0.0085] | `sec08f_label.json` | ✓ |
| 23 | D-μ: P 0.7937, CSF-1 0.6034, CertGrip 0.0105/0.0452/0.2142/0.5655, CSF-μ̂ 0.0054 | `sec08f_dmu.json` | ✓ |
| 24 | D-FID accuracy 0.7257; D_FID 0.4638 vs D 0.4555 | `sec08h_dfid.json`, `sec08h_h4b.json` | ✓ (the comparator is P, not CSF-1: unstated) |
| 25 | H2-M no-mass D 0.4598, change 0.0042 [−0.0446, 0.0399]; mass-noise D 0.4603, COMP RE 0.7991 | `sec08f_label.json`, `sec08h_massnoise.json` | ✓ (no-mass comparator is P_nomass: unstated) |
| 26 | H1-V Δ −0.00429 … −0.00143, all pass | `h1v_analysis.json` | ✓ |
| 27 | UT3 160/160; 20 degenerate cells (α 0.01, n 50) | `sec08f_ut3.json` (20 cells at (0.01, 50); mean_miss 0) | ✓ |
| 28 | H1c slip − α in [0.0096, 0.0507]; α 0.05 CIs [0.020, 0.045], [0.016, 0.042] | `sec08h_h1c.json` | ✓ |
| 29 | Table 3 all cells (OQT / Frozen / Oracle slips & RE, R_E CIs) | `h3_analysis.json` | ✓, except Frozen-CertGrip S2 0.10165 printed as 0.1017 (file gives 0.10164999…) |
| 30 | Audits 0.103 / 0.092 / 0.101; matched diff 0.032 / −0.035 / 0.009 | `h3_analysis.json` audit | ✓ |
| 31 | S1m R_E 0.8871 [0.7723, 1.0265], label diff 0.0248; H3-L 0.0857 [−0.0444, 0.1859] | `h3_analysis.json` | ✓ |
| 32 | H3-S ΔC 58.15 [48.20, 70.20] (S1), 42.40 [32.40, 49.35] (S3) | `sec08h_h3s.json` | ✓ (S2 and S1m inconclusive not mentioned) |
| 33 | η = 0.03412; friction drop shifts score by ≈ +0.51 | `h3_analysis.json` eta; `sec08g` D_loc dlogF_mean 0.509; ln(1/0.6) = 0.511 | ✓ |
| 34 | Learner search space / 30 configs / 4-fold GroupKFold / HistGBR quantile | `code/certgrip/models.py` | ✓ |
| 35 | MuJoCo 4.0.0, dt 0.002, elliptic, impratio 10, condim 6, solref/solimp; UT7 asserts identical physics | `code/requirements.txt`, `sim.py` l.87–88, `tests/test_conformal.py::test_ut7…` | ✓ |
| 36 | Detector: 500 Hz, w 6, k 8, consec 2, slope ½, r_arm 0.1, n_min 1 mN; taxel noise 0.05 / 0.002 / 0.10; probe 0.25 s to 0.005 F₀, return 0.02 s, hold 0.1 s | `sim.py` RD2, TAXEL_NOISE, `_rd_touch_probe` | ✓. Wording nit: falling below 1 mN *declares onset* (contact lost); it does not "arm" the detector. The docstring says "100 Hz", which is stale. |
| 37 | F₀ = 32.7 N; μ̂ clip [0.1, 3]; CSF-1 formula with μ̄ = √0.3 | `sim.preload_force`, `baselines.py` | ✓ |
| 38 | Splits 0–149/150–199/200–324/325–499; stream 369–499; S2 0–174 / 175–549 | `certgrip/data.py` | ✓ |
| 39 | Bisection 11 replays, bracket ≈ 0.7 % | `sim.bisect_fstar`; ln(1000)/1024 → 0.68 % | ✓ |
| 40 | "F3 ellipsoids and capsules"; "F5 thin plates (box ≤ 5 mm thick) and disks"; "F4 two-body composites" | `sim.build_xml`, `data.sample_object` | ✗ **F3 is capsules only. F5 is boxes only ("disks are a later option" in the code comment), and half-size 2–5 mm means 4–10 mm thick. F4 is one body: a box plus a non-colliding sphere used only as mass.** |
| 41 | "main simulation needs about 2–3 CPU-hours" | `results/v1/logs/p2_crc_*.log` sum 5.72 h (08c grid replays alone); `p2_crcv2_*` 8.03 h | ✗ understated (labels alone may be ~0.5–1 h; the total including CRC replays is ≥ 14 CPU-h) |
| 42 | Static touch "carries per-taxel noise" (Sec 3.2) | `sim.run`: `touch_preload` / `touch_probe` features are raw `sensordata`; noise is applied only inside the onset detector | ✗ undisclosed (and it favours S/full, so the attribution result is conservative) |
| 43 | D1 lift / D2 shake as hand motions | `sim._dist_apply`: the hand is held still and the motion enters as an inertial pseudo-force on the object | undisclosed modelling simplification |

Additional raw-data facts from the recomputation: there are no unavoidable instances in cal/test. The raw physical loss on the CRC grids is non-monotone for only 0–3 of 4,800 instances per arm, so monotonisation is practically inert. Per-stratum test slip of CertGrip-full is 0.071–0.097. CSF-1 is 0.089–0.116, with D1 at 0.1157 (above α).

---

## Reviewer A (robotics / tactile manipulation) — Score: **4 / 10** (borderline reject)

**Summary.** After a fixed preload the gripper ramps its force down until a modelled touch-only detector flags slip onset. The onset force (plus pre-registered log-noise σ) feeds a learned quantile model or a Coulomb plug-in, and CRC on direct-replay slip sets a per-stratum force multiplier. In MuJoCo at α = 0.10 the probe arm needs 42 % less relative excess force than the best non-tactile conformal baseline (CSF-1). Ablations put the saving in the onset feature. An online tracker keeps slip near α under three shifts.

**Strengths.**
1. Pre-registration and reporting are unusually honest. Three of four core decisions are reported as not confirmed or inconclusive. A losing regime (H2-R) is in the abstract, and deviations are enumerated. All reported numbers trace to result files.
2. The attribution chain (P → S → full → +onset, onset-only, shuffled, family-ID control, D-μ) is thorough and answers a question practitioners care about. The headline learned model adds nothing over a one-line Coulomb plug-in at the primary noise level (H2b), and onset-only is in fact the lowest-RE arm (0.4336 vs 0.4567). This finding is genuinely useful.
3. The common protocol for every arm (same preload, same probe history, slip reference before the probe) is a fair design choice. Probe-caused slip counts against the method.

**Weaknesses.**
1. **The main result is close to true by construction.** In the generator (`data.sample_object`), μ is drawn log-uniform on [0.3, 1] independently of family, geometry and mass. No non-tactile observable can therefore carry friction information, and a friction-blind certified rule must cover a 3.3× μ range. "The probe beats every friction-blind conformal rule" is then largely implied by the simulator design. The Mondrian/family-ID control cannot help because family is independent of μ by design. A real object set has strong material-friction correlation with appearance and category. A vision/category-informed conformal baseline, or a simulated μ–family correlation, is needed before the 42 % figure means anything outside this generator.
2. **The tactile model is idealised.** MuJoCo contacts are rigid point/patch contacts with soft constraints. They do not produce the peripheral partial slip that the Related Work invokes ("incipient slip, the partial slip at the contact periphery"). The detector effectively finds saturation of T/N, which equals μ at gross sliding, so it reads μ almost exactly (corr 0.988). σ = 0.2 is an assumed number, and the effect collapses quickly (σ = 0.4: lower limit 0.083 < SESOI). The headline therefore depends on a free parameter with no hardware anchor.
3. **The method description does not match the implementation** (spot-checks 40, 42, 43). F3 has no ellipsoids. F5 has no disks, and its plates are 4–10 mm thick, not ≤ 5 mm. F4 is not a two-body composite. Static-touch and squeeze features are noise-free, while the paper implies taxel noise everywhere. D1/D2 are pseudo-forces on a stationary hand, not hand motions. None of these changes the numbers, but each misdescribes what was simulated.
4. **Deployability.** The offline certificate needs F\* labels and 20 replays per instance, so it is simulation-only. The online route is evaluated with label-rule feedback 1{F < F\*_hi}, not physical slip, with physical audits on a single ordering. The abstract's "from binary slip feedback" should say so.
5. Probe cost and safety are under-analysed. Ramping to 0.005 F₀ deliberately induces slip on every grasp. The distribution of probe-induced displacement (pilot: median 0.13 mm, p99 0.4–0.7 mm, per 08a) and its share of the 2 mm slip budget should be reported in the main text, as should the number of slips the probe itself caused.
6. Heterogeneity is under-reported: Q = 31.0 on 15 df, and all four D3 (lateral pull) cells are the lowest (0.30–0.39). A short mechanism note is warranted.

**Actionable revisions.**
- Add a non-tactile baseline that has access to a friction proxy (e.g., a noisy category/material label correlated with μ), or re-simulate with a μ–family correlation, and report D against it.
- Correct the geometry and touch-noise descriptions to the code (or implement ellipsoids/disks), and state the pseudo-force implementation of D1/D2.
- Report probe-induced displacement and probe-caused slip counts. Add per-stratum test slip (D1 for CSF-1 is 0.1157).
- Reframe C2 as "under a friction-independent object distribution" and move the σ sweep into the headline claim, e.g. "42 % at σ = 0.2, 14 % at σ = 0.4".

**Recommendation.** Not ready for NeurIPS/ICML in its current form. The work is careful and honest, but its confirmed claim follows largely from the simulator design, and no hardware or realistic-sensor anchor for σ is given. A robotics venue (RSS/CoRL) with a hardware σ measurement and a friction-informed non-tactile baseline would be a better fit.

---

## Reviewer B (statistics / conformal methodology, methodology–evidence consistency) — Score: **5 / 10** (borderline)

**Summary.** CRC is applied with a monotonised binary physical loss on a fixed 20-point λ-grid per arm, per disturbance stratum (n = 500), with paired object-cluster bootstrap CIs for the excess-force ratio. Four core decisions are Bonferroni-split. Online score-space quantile tracking is studied under shift.

**Strengths.**
1. The statistical pipeline is correctly implemented. The `lam_index` code computes the monotonised loss with a reverse cumulative max and the (n R̃ + 1)/(n + 1) ≤ α rule. The bootstrap resamples cal and test objects within family with λ̂ recomputed per draw, CI\*\* uses 1.25/98.75 percentiles, and the H2a decision checks lo/mid/hi. The headline numbers reproduce from raw replays.
2. Choosing CRC on the physical loss after the monotonicity gate failed is principled, and the paper is transparent that it followed a pre-registered failure branch. The H1-V audit shows the label rule errs on the safe side.
3. Good separation of primary, co-primary and unadjusted secondary results. H2b is reported as not confirmed rather than spun as equivalence.

**Weaknesses.**
1. **The H2b grid-floor defect also affects the primary σ = 0.2.** Deviation 2 states correctly that CSF-μ̂'s λ̂ sits at index 0 in D1/D2 "at σ ≤ 0.2". The plug-in is therefore over-protected at the primary σ as well: its test slip is 0.0657 against 0.0829 for CertGrip, and 08e moves D from 0.0569 to 0.0240. Sec 5.2 and Limitations single out only σ = 0 and 0.1 as unreliable. The 08e reporting rule ("unreliable only if the decision changes") explains why. The text should still say explicitly that the 08c σ = 0.2 point estimate is biased towards CertGrip, and Figure 1(c)'s CSF-μ̂ bar inherits that bias.
2. **The SESOI is applied to the point estimate, not the bound.** Superiority requires D ≥ 0.10 and lower > 0. That was pre-registered and is fine, but "exceeds the SESOI" should not be read as "demonstrated ≥ 10 %". At σ = 0.4 the file marks "superiority" while the lower limit is 0.083. The paper's σ\* handling is correct, but the table/decision vocabulary should make this distinction explicit.
3. **The guarantee is marginal per stratum and holds in expectation over calibration draws.** The paper says this. CSF-1 test slip is 0.1021 overall and 0.1157 in D1. A per-stratum test-slip table plus a calibration-conditional (PAC/training-conditional, cf. Bian & Barber, cited) variant would strengthen the "certified" language. Labelling physical slip ≤ α "certified" for a single fixed calibration set overstates what CRC gives.
4. **Monotonisation is practically inert** (0–3 of 4,800 raw flickers per arm), while the H1-M failure was 8/800 with bracket-level (≤ 0.9 %) violations. The pivotal story ("CRC was needed because monotonicity failed") is technically right but practically immaterial. The label route gives nearly identical D (0.4292), so CRC is mainly a cleaner validity argument. Say so.
5. **H3 design.** Feedback is the label rule. R_E is confounded by unequal realised slip (the paper notes this), and the matched-rate check uses a single audited ordering. The 20 orderings share the same instances, so they are not independent replicates; the object-cluster bootstrap is the right unit and should be stated as such. H3-S omits that S2 and S1m are inconclusive.
6. **Methodology–evidence discrepancies** (non-fabrication):
   - (a) Compute: "2–3 CPU-hours" against 5.7 h (08c) + 8.0 h (08e) of CRC replays in the logs.
   - (b) The H1-M maximum 0.00904 comes from shift-pool instances, and those two extra violations (1/100 S3, 1/100 S2) are not reported.
   - (c) D_FID, D-no-mass and the H4 chain are D-values against P, not against COMP. The text juxtaposes them with H2a (0.4168) without saying so.
   - (d) The "detector armed … or normal < 1 mN" wording does not match the code.
   - (e) Table 3: Frozen-CertGrip S2 0.1017 should be 0.1016.
   - (f) Figure 1(c) mixes CRC-route bars with a label-route H2-R footnote.
   - (g) RE excludes unavoidable instances. There were none in cal/test, but the definition in Sec 3.1 should say so.
7. Novelty on the statistics side is limited: off-the-shelf CRC, Mondrian stratification and quantile tracking. The contribution is the empirical attribution, not a new method.

**Actionable revisions.**
- State that the H2b 08c σ = 0.2 estimate is floor-biased. Present 08e and the label route alongside it in Table 2, with the same visual weight.
- Add per-stratum test slip rates and a training-conditional or high-probability variant (or at least the spread of test slip over the 2,000 bootstrap λ̂ draws).
- Fix the compute statement, the H1-M maximum and the comparator labels, and add Q/heterogeneity.
- Note in the abstract that online feedback is the simulator label rule, with physical audits on one ordering.

**Recommendation.** Borderline. The statistical work is clean, honest and reproducible. The confirmed claim is narrow and partly design-induced, and the most interesting result (learned ≈ plug-in) is not confirmed either way. A workshop or robotics venue is a better fit unless realism is improved.

---

## Must-fix list (ranked)

1. **Make the method description match the code.** F3 is capsules only. F5 is boxes only, 4–10 mm thick, no disks. F4 is a box plus a non-colliding mass sphere. Static/squeeze touch features are noise-free. D1/D2 are pseudo-forces on a fixed hand. Either fix the text or implement the stated geometry.
2. **Acknowledge that friction is independent of all non-tactile observables by design**, so H2a is largely structural. Add or discuss a friction-informed non-tactile conformal baseline, or a μ–family correlation run, and narrow C2 accordingly.
3. **State that the 08c H2b at σ = 0.2 is also floor-biased** (CSF-μ̂ λ̂ index 0 in D1/D2). Make Sec 5.2 and Limitations consistent with Deviation 2, and caveat the Fig 1(c) CSF-μ̂ bar.
4. **Fix the compute claim.** The "2–3 CPU-hours" claim contradicts the logs (≥ 13.7 CPU-h of CRC replays alone).
5. **Qualify the online claim.** The 20-ordering streams use label-rule feedback, not physical slip, and the physical audit is a single ordering. Say this in the abstract and C4.
6. **Fix the H1-M reporting.** Attribute 0.00904 to the shift-pool instances (id max 0.00225) and report the 2 shift-pool violations (1/100 S3, 1/100 S2).
7. **Label comparators and report heterogeneity.** Say that D_FID, D-no-mass and H4a are D against P, not COMP. Report Q = 31.0 (15 df) and the systematically weaker D3 cells. Add per-stratum test slip (CSF-1 D1 = 0.1157).
8. **Trim to the 9-page limit** (~7.4k words now). Condense Related Work's robotics-conformal list, the deviations list and Sec 5.2's σ paragraph. Correct the minor items: Table 3 S2 0.1016, the detector "arming" wording, the RE definition (unavoidable excluded), and the H3-S S2/S1m inconclusive results.
