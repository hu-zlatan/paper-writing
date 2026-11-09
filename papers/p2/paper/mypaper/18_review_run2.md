# Stage 18 Peer Review, run 2

**Paper:** "Probe, Then Certify: Minimal-Force Grasping with a Tactile Friction-Onset Probe and Conformal Slip-Risk Control" (draft_v1, as embedded in `prompts/stage18_user.txt`)
**Target used for significance judgement:** RSS 2027 (Stage 1 extended abstract; this master draft will be condensed). The length check is applied as the prompt states it (NeurIPS/ICML 9-page thresholds).

---

## CRITICAL_FABRICATION: no

**Reasons.**
- I recomputed every headline number I could from the raw files (`results/v1/crc/*.jsonl` with 4,800 instances, 0 missing, 0 duplicates; `results/v1/labels/*.jsonl`; `results/v1/mono/*.jsonl`) using the project's own `build`/`evaluate` code plus an independent CRC loop of my own. The results match the paper to four decimals: RE 0.4567 / 0.7832 / 0.4843 / 0.4336, physical slip 0.0829 / 0.1021 / 0.0657 / 0.0857, D(H2a) = 0.4168, D(H2b) = 0.0569, and the λ̂ indices per stratum.
- Trial and instance counts in the paper match the evidence: 2,000 calibration and 2,800 test instances, 800 selection instances, 8 of 800 non-monotone, 20 orderings, 2,000 bootstrap draws, seeds 0 to 4, T = 2,000 stream steps, a 2,096 / 1,500 instance stream.
- Every statistical procedure the paper names exists in code. These are the Clopper–Pearson limit (`analysis_h1m.py`), the object-cluster bootstrap with λ̂ recomputed per draw (`analysis_crc.py`, `h3_streams.py`), CRC on the monotonised loss, split-conformal q̂, OQT with anti-windup, and the decaying-step variant.
- The discrepancies I found are **descriptive misstatements, not invented results**. Two object-shape claims (F3 "ellipsoids", F5 "disks") describe shapes that were pre-registered but never implemented. The F5 thickness is misstated by a factor of 2. The compute claim is understated by about 5x. A tuning-set correlation is presented as the general detector quality. Two over-generalisations appear in the abstract and conclusion. All must be fixed (see the must-fix list), but none changes a reported number or decision.

---

## Length and topic check (as instructed)

| Section | Words | Threshold | Status |
|---|---|---|---|
| Abstract | 274 | ≥150 | OK (long for RSS; condense to about 200) |
| Introduction | 876 | ≥700 | OK |
| Related Work | 543 | ≥500 | OK |
| Method (Sec. 3) | 1,601 | ≥800 | OK |
| Experiments (Sec. 4) | 1,198 | ≥600 | OK |
| Results (Sec. 5) | 1,781 | ≥500 | OK |
| Total (body) | ≈7,350 | ≥4,000 | OK, not under-length |

**Topic.** The paper stays on topic throughout. It covers the ramp-down probe, CRC on the physical slip loss, the comparison with the strongest non-tactile conformal baseline, the attribution ablations, and the online binary-feedback study under shift. Environment details (GitHub Actions runners, MuJoCo version, bit-identity) appear only as reproducibility notes and are not presented as contributions. No drift.

**Note for condensation.** For an RSS Stage-1 extended abstract the paper will have to shed about 60 % of its text. The deviation list, the H4b/H4c/H4d/H2-M secondary rows and most of Table 3's columns are the natural cuts. The H2-R failure regime and the H2b "not confirmed" must survive the cut.

---

## Spot-checks against code and raw results (31 items)

| # | Claim in draft | Source checked | Result |
|---|---|---|---|
| 1 | D(H2a) = 0.4168, CI\*\* [0.3484, 0.4778]; lo/hi 0.4150 / 0.4186 | `crc_analysis.json`; **recomputed** from `crc/*.jsonl` + labels | ✔ exact |
| 2 | RE CertGrip-full 0.4567 [0.4079, 0.5033], CSF-1 0.7832 [0.6968, 0.8583] | `crc_analysis.json`; recomputed point values | ✔ |
| 3 | Physical test slip 0.0829 / 0.1021 / 0.0657 / 0.0857 | recomputed | ✔ |
| 4 | CRC rule: monotonise by max over λ' ≥ λ, choose first λ with (nR̃+1)/(n+1) ≤ α, else max Λ | `analysis_crc.lam_index`; my independent loop gives the same λ̂ (D1 10, D2 10, D3 11, D4 10) | ✔ matches Eq. in §3.4 / Alg. 1 |
| 5 | Grid Λ = q̂_sel + linspace(−0.4, 0.4, 20), pooled over strata, selection split only | `crc_grids.py main()` | ✔ (step 0.042 log units) |
| 6 | 08e grid q̂_sel,d + linspace(−0.8, 0.8, 41), per stratum | `crc_grids.py main_v2()` | ✔ |
| 7 | Split-conformal q̂ = ⌈(n+1)(1−α)⌉-th smallest score, s = log F\*_hi − log ĝ | `certgrip/conformal.py qhat/scores` | ✔ |
| 8 | OQT q_{t+1} = q_t + η(slip_t − α), anti-windup on capped steps; decaying variant | `conformal.OQT` (decay η/√(n_uncapped+1)) | ✔ (the decay schedule is in code but not stated in the paper) |
| 9 | CSF-1: F_nom = m(g + a_cmd)/(2μ̄), μ̄ = geometric mean; m g/(2μ̄) for D3/D4 | `baselines.py` (a_cmd = 0 for D3/D4; D2 a_cmd = A(2πf)²) | ✔ |
| 10 | CSF-μ̂ uses the same noisy onset; μ̂ clipped to [0.1, 3] | `baselines.mu_hat`, `crc_grids.base_logs` | ✔ |
| 11 | λ̂ at grid floor (index 0) in D1/D2 for CSF-μ̂ at σ ≤ 0.2, index 1 for CSF-1 | `crc_analysis.json` lam_idx (CSF-μ̂@0.4 sits at 2) | ✔ |
| 12 | COMP = CSF-1, selection RE 0.7686 vs 0.8294 / 0.8335 | `comp_selection.json` | ✔ |
| 13 | F₀ = 32.7 N = m_max g / μ_min | `sim.preload_force`, crc log header | ✔ |
| 14 | Probe: F₀ → 0.005 F₀ over 0.25 s at 500 Hz, w = 6, k = 8, consec = 2, slope_frac 0.5, r_arm 0.1, n_min 1 mN, t_up 0.02 s, hold 0.1 s | `sim.RD2`, `_rd_touch_probe` (DT 0.002, frame_steps 1) | ✔ (the docstring says "100 Hz", which is stale; the code runs at 500 Hz) |
| 15 | Taxel noise mult 0.05, add 0.002 N, gain 0.10 | `sim.TAXEL_NOISE` | ✔ |
| 16 | MuJoCo timestep 0.002, elliptic, impratio 10, condim 6, solref/solimp as stated; unit test asserts identity | `sim.build_xml`; `tests/test_conformal.py::test_ut7_…` | ✔ |
| 17 | Slip = pad-plane displacement > 2 mm, rotation > 3°, or contact loss; reference pose before the probe | `sim.run` (ref_p = p1, taken after the squeeze and before the rd probe) | ✔ |
| 18 | Learner: HistGB quantile, 30-config search, 4-fold GroupKFold, stated search space | `certgrip/models.py` | ✔ |
| 19 | Feature sets P / S / full / full_rd / P_onset as described; amplitudes hidden | `certgrip/featsets.py` | ✔ |
| 20 | Splits 0–149 / 150–199 / 200–324 / 325–499; stream 369–499 (2,096), S2 175–549 (1,500) | `certgrip/data.py split_of, h3_role`; label counts (cal 2,000, test 2,800, select 800, s2 stream 1,500) | ✔ |
| 21 | **F3 = "ellipsoids and capsules"** | `data.sample_object` and `sim.build_xml`: **capsule only** | ✘ misstatement |
| 22 | **F5 = thin plates "of at most 5 mm thickness" and disks** | `data.py` comment: "disks are a later option"; box half-size 2–5 mm, so the **thickness is 4–10 mm**, and **no disks** | ✘ misstatement (2 errors) |
| 23 | H1-M 8/800, CP upper 0.02115, 7 of 8 under D2, max rel. 0.00904 | `h1m_analysis.json`; recount from `mono/*.jsonl` gives 10/1,100 including the shift pools (8 id + 1 S3 + 1 S2) | ✔ |
| 24 | Bracket width about 0.7 % | labels: median F_hi/F_lo − 1 = 0.68 % | ✔ |
| 25 | "log(mg/2F_onset) correlated with log μ at 0.988" | pilot value (08a). **On the 8,000 main id instances it is 0.948**, with an intrinsic log-error SD of 0.110 and a bias of +0.319 at σ = 0 | ⚠ true for tuning only; overstates detector quality |
| 26 | H1-V Δ −0.00429 to −0.00143, all pass | `h1v_analysis.json` | ✔ |
| 27 | UT3 160/160 with 20 degenerate (α 0.01, n 50) | `sec08f_ut3.json` (5 arms × 4 strata at α 0.01, n 50 = 20 cells) | ✔ |
| 28 | H4a / H4c / H4e / H2b label and 08e values, seeds 0.3932–0.4494 and 0.4145–0.4442 | `h4a_label_rule.json`, `sec08f_label.json`, `h2_label_rule.json`, `crc_analysis(_v2).json` | ✔ |
| 29 | H2-H pooled 0.4388, τ 0.0511, min cell F1D3 0.2979, all lower limits > 0.16 (min 0.1602) | `sec08g.json` | ✔ (the 0.16 bound is met only to the third decimal) |
| 30 | Table 3 (all 24 entries), R_E CIs, audit 0.103 / 0.092 / 0.101, matched diffs 0.032 / −0.035 / 0.009, S1m 0.8871 and 0.0248, H3-S ΔC | `h3_analysis.json`, `sec08h_h3s.json` | ✔ |
| 31 | **"The main simulation needs about 2–3 CPU-hours"** | `logs/p2_crc_*` sum to 5.7 h, `p2_crcv2_*` to 8.0 h, labels 0.6 h, mono 0.15 h; the CRC rows hold 14 arms × 20 = 280 replays per instance | ✘ understated about 5x (≈14–15 CPU-h) |

Further checks that passed: oracle decomposition 0.5172 and oracle RE 0.1271; D-μ values; D_FID 0.4638 vs D 0.4555; touch-only family accuracy 0.7257; H2-M 0.4598 / 0.0042 / 0.4603 / 0.7991; H2-R −0.2614 with n 352 / 548; H2-n 0.4146 / 0.4654; H1c ranges and α 0.05 intervals; T = 0.5918; η = 0.03412; "no step capped"; onset found on 100 % of id instances (not reported in the paper); probe displacement at onset median 0.13 mm, p99 0.48 mm, max 1.92 mm (below the 2 mm slip threshold; not reported in the paper).

---

## Reviewer A: RSS reviewer, tactile manipulation / grip-force control

**Summary.** The paper proposes a grasp protocol: a fixed preload, then a log-linear force ramp-down until a touch-grid detector flags incipient slip. The onset force is used as a friction reading, and the commanded grip force is calibrated by conformal risk control on physical slip. In MuJoCo, against a friction-blind physics formula calibrated to the same α, the probe arm needs 42 % less relative excess force at a test slip rate of 8.3 %. The probe, not the touch/squeeze features or the learner, carries the saving. A narrow-friction sub-pool reverses the effect.

### Strengths
1. **The right comparator.** Comparing against a *calibrated* non-tactile rule, chosen beforehand on a disjoint split, is much more honest than the usual comparison against a fixed-margin or uncalibrated controller. I would like this framing to become standard in the grip-control literature.
2. **A careful protocol design.** The preload is identical for all instances, so no mass or friction leaks through it. Probe-induced slip counts as grasp failure. The slip criterion (2 mm / 3° / contact loss) is explicit. Detector constants are frozen on disjoint pilot objects.
3. **Honest reporting of negative results.** H2b is not confirmed. The H2-R reversal is reported, the σ-dependence is shown, and the full deviation list is given. The statement "Of four core decisions, one was confirmed" is unusual and welcome.
4. **The engineering message is clear.** It is CSF-μ̂: a one-line Coulomb plug-in on the onset, followed by calibration, does about as well as a learned model. Practitioners can use that directly.

### Weaknesses
1. **No hardware, and the "tactile" signal is idealised (major for RSS).** The onset reading comes from MuJoCo's pad touch grids under a soft-constraint point-contact model. That model has no real stick/slip annulus, no elastomer shear field, and no sensor dynamics. The paper itself concedes that the detector is "close to a perfect friction sensor" and injects synthetic noise σ. The headline effect is therefore a function of an assumed parameter: D = 0.68, 0.58, 0.42 and 0.14 at σ = 0, 0.1, 0.2 and 0.4. Nothing ties σ = 0.2 to any real sensor (GelSight-type, BioTac, uSkin, barometric). For RSS this is the decisive weakness. At minimum, the authors should cite measured onset-force repeatability from the literature or from a bench test and place it on the σ axis.
2. **The ablation conclusions are partly built into the simulator.** "Static touch and the squeeze carry no friction information" (C3) is close to tautological here. Under rigid Coulomb contact, μ does not affect static normal or shear readings below the friction limit, and the squeeze does not move the contact towards slip. The recorded static touch is essentially the deterministic m g/2 shear split (the logged `touch_preload` rows show identical symmetric values). On real elastomer sensors, partial-slip fields under tangential load *do* carry friction information; this is the principle behind several of the cited estimators. C3 should be scoped to "in a rigid-contact simulator" rather than stated as a property of touch.
3. **Detector quality is overstated.** The 0.988 correlation is a pilot (tuning) number. On the 8,000 main id instances I get corr = 0.948. log(m g/2F_onset) − log μ has an SD of 0.11 log units and a **+0.32 bias** already at σ = 0, so the "σ = 0" arm is not noise-free and the effective noise at σ = 0.2 is about 0.23. Report the intrinsic detector error on the main data and state that σ is *added* noise. The bias also matters for any uncalibrated use of μ̂.
4. **The object set is described inaccurately and is narrow.** F3 is capsules only (no ellipsoids are implemented). F5 has no disks (`data.py`: "disks are a later option"). F5 plates are 4–10 mm thick, not "at most 5 mm" (MuJoCo box sizes are half-extents). All objects are rigid primitives, and pad friction equals object friction. The new-family shift S2 is therefore a mild shift, which is consistent with frozen calibration not breaking there.
5. **Missing tactile baselines and prior work.** There is no comparison with a *reactive* slip controller (detect slip, tighten) or with a friction-estimate-plus-hand-tuned-margin controller in the style of the cited estimators. The relevant question for this community is whether the calibrated probe beats reactive tightening at equal drop rate. Classic work on friction from incipient slip and on human-inspired slip-reactive grip control should be cited and discussed: Tremblay & Cutkosky 1993 on estimating friction with incipient slip sensing, Romano et al. 2011 (T-RO) on human-inspired grasp control with tactile sensing, and Johansson & Westling's work on human grip-force regulation. The probe is a known idea (lower force until slip). The novelty lies in coupling it to a certificate, and the paper should say so more plainly.
6. **The cost and risk of probing are not reported.** The probe deliberately drives the grasp to slip. The logs contain the displacement at onset (median 0.13 mm, max 1.92 mm, close to the 2 mm slip threshold) and the found-rate (100 %), but the paper reports neither. It should report the probe-induced slip contribution to the 0.0829, and discuss objects for which a probe slip is unacceptable (liquids, assemblies). Total protocol time before the task (≈1.4 s) should also be stated against a no-probe grasp.
7. **The H2-R reversal deserves an answer, not a "plausible reading".** It is the most practically relevant result for a tactile audience. Practitioners will ask whether the probe can be skipped when the friction spread is small. A simple diagnostic would answer this, for example D as a function of the μ-range width or onset-noise-to-friction-spread ratio, using existing replays.

### Actionable revisions (A)
- A1. Ground σ in a measured or literature value, or add a small hardware probe study, even a bench test of onset repeatability on one sensor. Otherwise retitle and frame the paper as a simulation study of how far the sensor noise must fall.
- A2. Scope C3 to the simulator. Add one sentence explaining why static touch is uninformative under rigid Coulomb contact.
- A3. Replace the 0.988 statement with main-data numbers (corr 0.948, residual SD 0.11, bias +0.32) and say that σ is added on top.
- A4. Fix the object-family description (no ellipsoids, no disks, F5 thickness 4–10 mm).
- A5. Add a reactive slip-tightening baseline, or explain why it is out of scope. Add the missing classic citations.
- A6. Report the found-rate, the onset-displacement distribution and the probe-induced slip share.
- A7. Turn H2-R into a dose-response plot over friction spread.

**Score (A): 4 / 10 (Borderline, leaning reject for RSS).** The work is careful and honest, but it is simulation-only with an idealised tactile channel whose noise is assumed, and the ablation conclusions are largely set by the contact model. With a hardware or sensor-grounded σ it would be a 6.

---

## Reviewer B: RSS reviewer, conformal prediction / statistical safety

**Summary.** The paper applies per-stratum conformal risk control, with the binary loss of a fresh physical replay monotonised over a fixed λ-grid, to choose a log-force multiplier. It compares arms by a paired ratio-of-means effect D with an object-cluster bootstrap that recomputes λ̂. It also studies score-space online quantile tracking from binary feedback under three shifts.

### Strengths
1. **A correct and clean CRC instantiation.** The monotonisation L̃(λ) = max_{λ'≥λ} L(λ') makes the loss non-increasing and dominates the raw loss, so the CRC bound transfers to physical slip. I verified the implementation (`analysis_crc.lam_index`) against Eq. (§3.4) and Alg. 1 and re-derived λ̂ independently. The grid is fixed from a disjoint split. Unavoidable instances count as losses. Test slip is the *raw* replay outcome at λ̂, as it should be.
2. **Pre-registration with a working failure branch.** The H1-M gate failed narrowly (8/800, CP upper 0.0212). Switching to CRC on the physical loss rather than shipping the label-route certificate is the right call, and it is disclosed.
3. **Inference is done properly.** The bootstrap resamples objects within family (all four instances move together) and recomputes λ̂ in every draw. CI\*\* matches the Bonferroni split, and the H2a robustness requirement uses F\*_lo/F\*_hi. The equivalence claims use TOST with pre-stated margins.
4. **The online study is honest.** H3 is declared inconclusive. The paper explains that unequal realised slip rates confound R_E and does not spin S1m.

### Weaknesses
1. **The guarantee is the weakest kind for a safety claim.** CRC bounds E[slip] marginally over the calibration draw *and* the test point. With n = 500 per stratum and binary loss, the realised slip of a deployed λ̂ fluctuates by roughly ±0.013 (1 SD) around its expectation. CSF-1 already shows 0.1021 > α on test. For a "certified" grasp, readers will expect a training-conditional (PAC) statement: P(risk(λ̂) ≤ α) ≥ 1 − δ via an RCPS-style upper confidence bound or Learn-then-Test, which fits a fixed finite Λ naturally. The paper cites training-conditional work but does not use it. At minimum, report the (α, δ) achievable from the existing replays (no new simulation is needed) and the resulting force cost. The word "certified" in C1 and in the title framing should be qualified as "in expectation".
2. **The exchangeability statement is imprecise.** Calibration and test are stratified by family (125 / 175 objects per family). The claim that "exchangeability holds at the object level, and the guarantee holds per stratum and hence marginally" needs a sentence. Under fixed family counts the joint law is exchangeable only within family. The marginal statement holds for a test point drawn with the same family proportions, but not under arbitrary family mix. This should be stated precisely, together with the absence of any per-family guarantee (already in Limitations).
3. **The grid design limits efficiency and complicates H2b.** The 20-point grid has a 0.042 log step, so λ̂ is coarse: CertGrip's D1 stratum sits at risk 0.078 at λ̂, and the index below exceeds α. More importantly, the comparator CSF-μ̂ hits the grid floor in D1/D2, which biases H2b towards the learned arm. The authors acknowledge the floor defect and run the post hoc 08e grids, but the primary H2b read-out is computed on a grid known to be defective for the comparator. The paper should say plainly that the primary H2b test is uninformative on the plug-in side and that the 08e and label-route results, both closer to 0, are the better estimates.
4. **The D-μ diagnostic is misinterpreted.** D-μ is the R² of log μ on an arm's log-force residual. It measures *systematic* friction dependence (bias, shrinkage) and is blind to friction-independent noise. CSF-μ̂ has D-μ of 0.005 at σ = 0.2 *and* 0.003 at σ = 0.4, yet at σ = 0.4 it is the worst arm in the study (RE 0.988). An unbiased but noisy plug-in will always score about 0. The Discussion's contrast "R² 0.7937 (P) … against 0.0054 for the plug-in fed by the onset" therefore does not show that the plug-in "captures" friction. It shows that its errors are uncorrelated with μ. Either drop this diagnostic from the argument or pair it with the residual variance.
5. **The online study does not test what the abstract claims.** (a) The feedback in the 20 orderings is the label rule 1{F < F\*_hi}, not physical slip; physical audits cover ordering 0 only. The abstract says "online quantile tracking from binary slip feedback" without that caveat. (b) The abstract and conclusion say frozen calibration "fails" or "breaks" under the three shifts, but under S2 neither frozen arm breaks (0.1017 / 0.1051), so OQT's rescue is shown for S1 and S3 only. (c) In S2 the R_E CI lies entirely above 1 ([1.023, 1.428]). OQT is then *less* efficient than the oracle, though at a lower slip rate. "Inconclusive" is formally correct, but the text should state the direction. (d) The design rationale for score-space OQT over ACI (saturation at F_max) is argued, not shown. One ACI arm on the existing streams would settle it.
6. **The confirmatory framing is stretched.** The primary analysis route (08c CRC) was operationalised after the H1-M counts were seen (Deviation 1). Several secondaries were specified after related read-outs (08e, H3-L). The abstract's "under pre-registered decisions" should become "under pre-registered decision rules, with the CRC route specified after the monotonicity gate failed". The H2a rule (point estimate ≥ SESOI, lower limit > 0) is also a weak superiority criterion. It does not change the outcome here (the lower limit is 0.348), but this should be noted when σ\* is discussed: at σ = 0.4, H2a is still "superiority" while the lower limit is below the SESOI.
7. **The statistical novelty is modest.** CRC, Mondrian stratification and quantile tracking are used off the shelf, and the authors say so. The contribution for a statistics-minded RSS reader is the demonstration that the physical-loss route is needed (8/800 non-monotone) and costs little. That is a solid workshop-to-short-paper contribution, not a methods advance. Missing references: Bates et al. 2021 (risk-controlling prediction sets) and Angelopoulos et al. (Learn then Test), both directly relevant to a finite-grid binary-risk certificate.

### Actionable revisions (B)
- B1. Add an (α, δ)-PAC variant (RCPS/LTT on the existing grid replays) with its force cost, or qualify "certified" as an expectation guarantee everywhere.
- B2. State the exchangeability assumption precisely, given family-stratified splits.
- B3. Present H2b's primary 08c read-out as compromised by the floor defect, and lead with 08e and the label route.
- B4. Remove or correct the D-μ interpretation. Report residual SD next to it.
- B5. Fix the abstract and conclusion: the feedback is label-rule in the 20 orderings, frozen calibration fails in S1 and S3 (not S2), and the S2 R_E direction should be stated. Optionally add an ACI arm.
- B6. Reword the pre-registration claims to reflect Deviation 1. Note the H2a decision at σ = 0.4.
- B7. State the decaying-step schedule (η/√t over uncapped steps) used for H3-S.
- B8. Cite RCPS and LTT. Report per-seed H2b (point estimates range from 0.019 to 0.110 across seeds 0–4) to show that H2b instability is not seed noise alone.

**Score (B): 5 / 10 (Borderline).** The statistics are executed correctly and reported with unusual candour. The guarantee is the expectation-only kind, two diagnostics and the online claims are over-read, and the methodological novelty is small.

---

## Methodology–evidence consistency summary

| Item | Paper | Evidence | Severity |
|---|---|---|---|
| F3 family | "ellipsoids and capsules" | capsule only (`data.py`, `sim.py`) | must fix |
| F5 family | "thin plates (≤ 5 mm thick) and disks" | boxes only, half-size 2–5 mm, so 4–10 mm thick; disks not implemented | must fix |
| Compute | "about 2–3 CPU-hours" | CRC 08c 5.7 h + 08e 8.0 h + labels 0.6 h + mono 0.15 h (logs) | must fix |
| Detector quality | corr 0.988 ("in tuning") | main id data corr 0.948, intrinsic SD 0.11, bias +0.32 | should fix |
| Frozen calibration | "fails/breaks under three shifts" (abstract, conclusion) | no break in S2 | must fix |
| OQT feedback | "binary slip feedback" | label-rule feedback in the 20 orderings; physical audit only on ordering 0 | must qualify in abstract |
| D-μ reading | plug-in "captures" friction (R² 0.0054) | at σ 0.4 the plug-in has R² 0.003 but the worst RE | must fix interpretation |
| Not reported | | found-rate 100 %, onset displacement (max 1.92 mm), decaying-step formula, RAW-Qv in H1c (its CIs include 0), D(onset-only vs CSF-μ̂) ≈ 0.105 | should add |
| Everything else checked | | see spot-check table | consistent |

Trial counts: consistent with the evidence. No CRITICAL trial-count fabrication.

---

## Top must-fix items (ranked)

1. **Sensor-grounding of σ.** For RSS, either ground σ = 0.2 in measured or literature onset repeatability of a real tactile sensor (ideally a small hardware bench test), or reframe the headline as "D as a function of onset noise" with σ = 0.2 as an assumption.
2. **Correct the object-family description.** F3 has no ellipsoids, F5 has no disks, and F5 thickness is 4–10 mm.
3. **Fix the over-generalised online claims** in the abstract and conclusion. Frozen calibration breaks in S1 and S3 only. The stream feedback is label-rule, with a physical audit on one ordering. State that the S2 R_E CI lies entirely above 1.
4. **Qualify "certified".** Either add an RCPS/LTT (α, δ) training-conditional variant from the existing replays, or label the guarantee "in expectation" everywhere. Cite Bates et al. and Learn-then-Test.
5. **Drop or correct the D-μ "friction captured" argument.** Pair it with residual variance; the plug-in has near-zero R² even when it is the worst arm.
6. **Scope C3 and the attribution claims to the rigid-contact simulator.** Static touch and squeeze are uninformative about μ by construction. Report the main-data detector error (corr 0.948, SD 0.11, bias +0.32) instead of the pilot 0.988.
7. **Present H2b's primary 08c read-out as compromised** by the comparator's grid-floor defect. Lead with 08e and the label route, and reword "pre-registered decisions" to reflect that the CRC route was written after the gate failed.
8. **Correct the compute claim** (≈14–15 CPU-h from the logs, not 2–3). Report the probe's own cost: found-rate, onset displacement, probe-induced slip share and protocol time. Add or justify the absence of a reactive slip-tightening baseline.
