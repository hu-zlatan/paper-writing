# p2 · Stage 16 PAPER_OUTLINE: RSS 2027 Stage 1 extended abstract

**Format:** at most 5 content pages plus 1 page of references, no supplementary material. Main body target is 3,000–3,500 words. **Stated deviation:** the 9-page word floors of hard_constraints §3 do not apply. A longer master draft is allowed, and stage 22 condenses it.
**Binding inputs:** `results/15_decision.md` (re-scoped story) and the Part B audit rewrites in `results/14_analysis.md`.
**Evidence notation:** `block → key path` refers to `results/v1/results_v1.json`. For example, `crc_analysis.json → contrasts.H2a.D.mid` means block `crc_analysis.json`, key `contrasts`, then `H2a`, `D`, `mid`. Numbers are copied as they appear in that file or in 14_analysis.md.
**Naming used throughout:** *CertGrip-full* (code `full_rd`) = static touch + squeeze + onset feature, σ 0.2, seed 0. *Onset-only* = `P_onset`. *CSF-μ̂* is the physics plug-in that uses the same noisy onset. *COMP = CSF-1*. *RE* = mean relative excess (F − F\*_mid)/F\*_mid. *D* = 1 − RE(target)/RE(comparator). *CI\*\** = the 97.5 % two-sided object-cluster bootstrap interval (2,000 draws).

---

## Title (working)
**Probe, Then Certify: Minimal-Force Grasping with a Tactile Friction-Onset Probe and Conformal Slip-Risk Control**

Alternative: *Certified-Slip Grip Regulation: Where the Force Saving Comes From*.

---

## Abstract (≈ 200 words)
- **Goal:** State the problem. We want to choose the smallest grip force whose *physical* slip rate is ≤ α, using only information a robot can measure. Then state the four claims and the scope limit in one paragraph.
- **Content, in order:**
  1. The problem: there is a gap between minimal force and certified slip probability. Non-tactile conformal baselines are calibrated, but they are blind to friction.
  2. The method: a ramp-down friction-onset probe after a fixed preload. A quantile predictor feeds the probe's onset estimate into conformal risk control (CRC) on the binary physical-slip loss.
  3. The main result, against the strongest non-tactile conformal baseline (selected beforehand) at α 0.10 on the pre-registered CRC route: D = 0.4168, CI\*\* [0.3484, 0.4778]. Test physical slip is 0.0829.
  4. The attribution: the saving comes from the probe. Adding the onset feature gives D 0.4739. Static touch is equivalent to proprioception. At σ 0.2 a learned model shows no demonstrated gain over a physics plug-in that uses the same onset estimate (H2b not confirmed).
  5. The scope limit (mandatory, from H2-R): in a sub-pool with narrow friction (μ ∈ [0.5, 0.8]) and mid-amplitude disturbances, the method is *worse* than the baseline: D −0.2614, CI\*\* [−0.5320, −0.0325].
  6. The online study: binary-feedback quantile tracking under shift holds window slip near α while frozen calibration breaks. Its efficiency relative to an oracle recalibration is inconclusive.
  7. The setting: simulation only (MuJoCo), with a modelled tactile detector.
- **Evidence:** `crc_analysis.json → contrasts.H2a.{D.mid, CI**.mid, decision}`; `crc_analysis.json → arms.full_rd@0.2#0.slip_phys`; `h4a_label_rule.json → contrasts.H4a_onset_full_rd_vs_full.D.mid`; `crc_analysis.json → contrasts.H2b.decision`; `sec08g.json → H2R.{D, CI**}`; `h3_analysis.json → H3_primary`. cite: `angelopoulos2022conformal`, `angelopoulos2023conformala`.
- **Must not say:** "learned tactile model improves grasping", "guaranteed in the real world", or "holds on every check".

---

## 1 Introduction (≈ 550 words)
- **Goal:** Motivate certified minimal-force grasping. Name the missing ingredient, which is friction information obtained online. State the research question and the contributions, each of which maps to a confirmed or explicitly scoped result.
- **Paragraphs:**
  1. **Why minimal force with a slip certificate.** Fragile and compliant objects, prosthetics, and gentle grasp all need it. Current tactile grip controllers react to slip or estimate friction, but they give no distribution-free slip-rate bound. Cite `dong2019maintaining`, `khamis2021real`, `boonstra2024estimate`, `niu2026synchronized`, `veiga2020grip`, `berman2025autonomous`, `willemet2024grip`.
  2. **Why conformal methods alone are not enough.** Split conformal or CRC can certify any force rule (`angelopoulos2022conformal`, `lei2017distribution`). Without friction information, though, the calibrated quantile must cover the whole μ range, and the force becomes conservative. This sets up the comparison against the *strongest* non-tactile conformal baseline, chosen beforehand on a disjoint split. COMP selection: CSF-1 RE_mean 0.7686 vs Mondrian-CSF 0.8294 and CertGrip-P 0.8335.
  3. **Research question.** Can a short tactile ramp-down probe supply enough friction information to cut excess grip force at a certified physical slip rate ≤ α? Which component carries the saving? Does calibration survive distribution shift when only binary slip feedback is available?
  4. **Contributions (4 bullets):**
     - (C1) A grasp protocol. A fixed preload carries no mass or friction information, so a ramp-down onset probe is the only friction channel. CRC is applied on the *monotonised physical* binary slip loss. This is needed because the label rule is not exactly monotone in force (8 of 800 instances).
     - (C2) A pre-registered evaluation against the best non-tactile conformal comparator: D = 0.4168, CI\*\* [0.3484, 0.4778].
     - (C3) An ablation chain that localises the saving in the probe rather than in static touch, the squeeze, or the learned model. It also reports a sub-pool where the method loses.
     - (C4) An online binary-feedback study under three shifts: frozen calibration breaks, and score-space quantile tracking restores slip near α. Its efficiency vs oracle recalibration is inconclusive, and we report it as such.
  5. **Honesty sentence.** Say that 1 of the 4 pre-registered core decisions was confirmed (H2a). H1 was not confirmed, H2b was not confirmed, and H3 was inconclusive. These outcomes are reported, not tuned away.
- **Evidence:** `comp_selection.json → candidates.*.RE_mean, COMP`; `h1m_analysis.json → non_monotone, n`; `crc_analysis.json → contrasts.H2a`; `h3_analysis.json → H3_primary`.

## 2 Related Work (≈ 350 words, three compact paragraphs)
- **Goal:** Position the paper at the intersection of tactile grip-force control and conformal safety in robotics. Show that no prior work certifies a *physical slip rate* of a *minimal* grip force.
  1. **Tactile slip and friction for grip control.** Cite `chen2018tactile`, `romeo2020methods`, `james2020slip`, `grover2022detect`, `dong2019maintaining`, `khamis2021real`, `boonstra2024estimate`, `niu2026synchronized`, `kuo2025tracing`, `feng2026tactilereflex`, `lach2024zero`, `ayral2026reactive`, `almohammed2022switched`, `shang2026exp`. Gap: these works offer reactive or estimated margins and no coverage guarantee.
  2. **Robust and safe grasping under uncertainty.** Cite `cloutier2018examining`, `cortez2019control`, `kim2024robust`, `enwerem2026firmgrasp`, `enwerem2026variational`. These are model-based margins that depend on assumed uncertainty sets.
  3. **Conformal prediction and risk control in robotics.** Foundations: `vovk2005algorithmic`, `romano2019conformalized`, `angelopoulos2023conformal`, `angelopoulos2022conformal`, `angelopoulos2026conformal`, `bian2023training`, `ding2023class`. Shift and online: `gibbs2021adaptive`, `gibbs2022conformal`, `angelopoulos2023conformala`, `angelopoulos2024online`, `farinhas2023non`, `ge2024stochastic`. Robotics: `lekeufack2024conformal`, `lindemann2025formal`, `dixit2022adaptive`, `marques2026particle`, `lindemann2023conformal`, `ren2023robots`, `huang2023conformal`, `strawn2023conformal`, `zhang2024bayesian`, `zhao2024conformalized`, `kumar2026learnable`. Gap: none certifies a contact outcome as a binary loss in force space.
  - Simulators (one sentence in §4): `wang2022tacto`, `akinola2025tacsl`, `leins2025hydroelastictouch`, `luu2025manifeel`, `birtalan2026impact`.

## 3 Problem Formulation and Method (≈ 800 words)
- **Goal:** Give a self-contained technical description. Every symbol used in Results should be defined here. The section describes the approach, not a workflow.
- **3.1 Problem (≈ 150 w).**
  - Instance x: object, pose, and disturbance type D1–D4.
  - F\*(x) is the minimal no-slip force, defined by a slip criterion: 2 mm tangential displacement, 3° rotation, or contact loss.
  - Goal: choose F(x) to minimise E[(F − F\*)/F\*] subject to P(slip at F(x)) ≤ α.
  - Labels: F\*_lo / F\*_hi / F\*_mid come from 11-replay log-space bisection on [0.1, 100] N. They exist only in simulation, which is why §3.4 matters.
- **3.2 Grasp protocol and friction-onset probe (≈ 200 w).**
  - Fixed preload F₀ = 32.7 N, the same for every instance, so it encodes neither m nor μ. Lift and hold. Squeeze F₀ → 1.5 F₀ → F₀.
  - **Ramp-down probe:** decrease force at a fixed rate. A touch-only detector watches the shear/normal ratio of the pad touch grids and stops at incipient slip, giving F_onset. A Coulomb reading gives μ̂ = m g / (2 F_onset).
  - Onset noise model: log F_onset + σ ε, with σ ∈ {0, 0.1, 0.2, 0.4}. The primary level is σ 0.2, and σ 0 is only an upper bound. Then ramp to the chosen F and run the disturbance window. A slip during the probe counts as a slip.
  - Hardware-availability table (one compact table, or inline): which inputs each arm receives.
- **3.3 Predictors and baselines (≈ 150 w).**
  - Gradient-boosted quantile predictor ĝ(x) with feature sets P (proprioception) ⊂ S (+ static touch) ⊂ full (+ squeeze) ⊂ CertGrip-full (+ onset). Onset-only = P + onset.
  - Physics plug-ins:
    - CSF-1: F = F_nom · e^q̂, with F_nom = m(g + a_cmd)/(2 μ̄).
    - Mondrian-CSF: one q̂ per family × disturbance cell. It is given privileged family ID.
    - CSF-μ̂: F = m(g + a_cmd)/(2 μ̂) · e^q̂, using the same noisy onset as CertGrip-full.
  - COMP is selected on the selection split before any calibration or test access.
- **3.4 Conformal risk control on the physical binary loss (≈ 200 w).**
  - Force family: F_i(λ) = min(F_max, ĝ(x_i) e^λ). Loss: L_i(λ) = 1{physical slip in direct replay}. Monotonised loss: L̃_i(λ) = max_{λ' ≥ λ} L_i(λ').
  - Per disturbance stratum, choose λ̂ = min{λ ∈ Λ : (n R̃_n(λ) + 1)/(n + 1) ≤ α} (`angelopoulos2022conformal`). This gives E[slip] ≤ α for an exchangeable test instance.
  - Λ is a 20-point grid centred on the selection-split quantile.
  - Motivation: H1-M (the label-rule monotonicity gate) failed. There were 8 non-monotone instances of 800, CP upper limit 0.02115 > 0.02, and 7 of the 8 were in D2. So the plain split-conformal certificate on labels is not guaranteed, and CRC on the physical loss is the valid route.
  - The label-rule split-conformal version (CQR scores, `romano2019conformalized`) is reported as a secondary route.
- **3.5 Online calibration from binary feedback (≈ 100 w).**
  - Score-space online quantile tracking (OQT, `angelopoulos2023conformala`): q_{t+1} = q_t + η (slip_t − α). There is one tracker per stratum, initialised at the offline q̂. η = 0.03412 (frozen). Anti-windup applies at F_max.
  - Why score space rather than ACI (`gibbs2021adaptive`): a friction drop can shift scores beyond the calibration support.
  - Comparison arms: a decaying-step variant (`angelopoulos2024online`) and frozen and oracle-recalibrated references.
- **Evidence:** `h1m_analysis.json → {non_monotone, cp_upper_98.75, threshold_count, by_dist}`; `h3_analysis.json → eta`; `crc_analysis.json → n_cal_instances, n_test_instances, draws`.

## 4 Experimental Setup (≈ 450 words)
- **Goal:** Give enough detail to reproduce the setup and to interpret the decisions: simulator, objects, shifts, splits, statistics, and the pre-registration and deviations.
- **Content:**
  - Simulator: MuJoCo 4.0.0, with physics parameters identical across families and shifts. Parallel-jaw gripper with pad touch grids. Families: F1 boxes, F2 cylinders, F3 ellipsoids/capsules, F4 off-CoM composites; F5 thin plates/disks for shift.
  - Ranges: μ log-uniform [0.3, 1.0], m [0.05, 1.0] kg. Disturbances D1 lift acceleration, D2 shake, D3 lateral pull, D4 payload.
  - Splits by object. n_cal 2,000 and n_test 2,800 instances. A selection split is used for COMP and λ-grids.
  - Shifts: S1 μ × 0.6, S1m μ × 0.9 (not primary), S3 disturbance amplitude × 1.5, S2 new family F5. Streams have T = 2,000 steps with the shift at step 501. The window is steps 1,001–2,000, and there are 20 orderings.
  - Statistics:
    - Bonferroni over 4 core decisions, one-sided 0.0125 each, CI\*\* 97.5 %. Object-cluster bootstrap with λ̂ recomputed per draw. SESOI 0.10 for D. Robustness check with F\*_lo / F\*_hi.
    - Secondaries are unadjusted and labelled as such.
    - The 08e per-stratum 41-point grids are *post hoc*: they can mark an 08c result as unreliable but cannot upgrade it.
  - **Deviation list (compact, one paragraph):**
    1. The CRC route (08c) was written after the H1-M counts were seen and before any predictor existed.
    2. The 08c λ-grid floor defect (CSF-μ̂ λ̂ index 0 in D1/D2; CSF-1 index 1) was fixed post hoc in 08e.
    3. 08b §3 says selection objects 200–249, while 08b §5, 08c and `comp_selection.json` say 150–199.
    4. The H3-B probe arm was untested. D-μ was computed on cal + test. H2-M mass noise was drawn only in 08h.
    5. The H3-L TOST was computed after the read-out from `rho_minus_rhoID`.
- **Evidence:** `crc_analysis.json → n_cal_instances (2000), n_test_instances (2800), draws (2000)`; `comp_selection.json → objects`; `crc_analysis.json → arms.CSF-muhat@0.2.lam_idx`, `arms.CSF-1.lam_idx`; `h3_analysis.json → draws, eta`.

## 5 Results (≈ 900 words, 2 tables + Fig. 1 right panel + 1 small σ-curve figure)
- **Goal:** Report the quantitative outcomes in this order: main comparison, then where the saving comes from, then where it fails, then validity of the certificate, then online shift. Use the audit wording throughout.
- **5.1 Main comparison (H2a, primary, ≈ 220 w).**
  - Table 1 and Fig. 1c give the result: D = 0.4168, CI\*\* [0.3484, 0.4778], superiority. With F\*_lo / F\*_hi: 0.4150 / 0.4186.
  - Physical test slip: CertGrip-full 0.0829 vs CSF-1 0.1021. CSF-1 is marginally above α, which is consistent with an expectation guarantee on a finite test set.
  - Robustness (one sentence, audit rewrite #20): superiority holds for the label route (0.4292), the post hoc grids (0.4289), seeds 1–4 (08c 0.3932–0.4494; label 0.4145–0.4442), all 16 cells (pooled 0.4388, every cell CI\*\* lower > 0.16), H2-n at n_cal 50 (0.4146), and vs Mondrian-CSF (0.4381). It **reverses in H2-R** and its lower limit falls below 0.10 at σ 0.4.
  - Tail (secondary): P95 ratio T = 0.5918, CI\*\* [0.5540, 0.6564].
  - Oracle gap closed: 0.5172.
- **5.2 Where the saving comes from (≈ 280 w, Table 2).**
  - Feature chain:
    - Static touch is equivalent to P within ±0.05 (D −0.0084).
    - There is no evidence the squeeze helps (D −0.0263; equivalence within ±0.03 not shown).
    - Adding the onset feature gives D 0.4739.
  - Adding touch to onset-only does not help (H4e CRC D −0.0534, not confirmed; label-route equivalence).
  - Shuffled touch is inconclusive (D −0.0253).
  - **H2b, co-primary, not confirmed:** D 0.0569, CI\*\* [−0.0399, 0.1454]. The post hoc grid gives D 0.0240 with CI\*\* upper 0.1001, missing equivalence by 0.0001. The label-route CI\*\* [−0.0850, 0.0814] lies inside ±0.10. Equivalence is **not** claimed.
  - σ dependence (small figure):
    - H2a D 0.6789 / 0.5825 / 0.4168 / 0.1401 at σ 0 / 0.1 / 0.2 / 0.4 (σ\* = 0.4).
    - H2b secondary, label route: the plug-in is better at σ 0 (D −0.2022) and σ 0.1 (D −0.0753), equivalent at σ 0.2, and the learned arm is better at σ 0.4 (D 0.3275). 08e agrees in direction.
    - The 08c σ 0 / 0.1 H2b superiority results are unreliable (grid defect).
  - Friction-information diagnostic (D-μ, CV R² of log μ on the residual):
    - No-probe arms: P 0.7937, CSF-1 0.6034.
    - CertGrip-full: 0.0105 / 0.0452 / 0.2142 / 0.5655 by σ. CSF-μ̂ σ0.2: 0.0054.
  - Identifier control (H4b): D_FID 0.4638 vs D 0.4555. Report H4b as an unadjusted secondary.
  - H2-M is reported descriptively only. As pre-registered, the onset feature confounds m and μ, so H2-M is not used for the friction story.
- **5.3 Where it fails (≈ 100 w).**
  - H2-R sub-pool (μ ∈ [0.5, 0.8] and mid-amplitude disturbances; n_cal 352, n_test 548): D −0.2614, CI\*\* [−0.5320, −0.0325]. This is a secondary result with no registered prediction.
  - Whether the narrow friction range causes it is **not tested** (audit #19).
  - H4d (CoM mechanism): inconclusive.
- **5.4 Validity of the certificate (≈ 130 w).**
  - H1 is not confirmed (H1-M 8 / 800). The violations are small: max (slip force − F_hi)/F_hi = 0.00904.
  - H1-V passes for all four arm × α combinations. The label rule over-counts slips slightly: Δ −0.00429 (CertGrip α 0.10) to −0.00143.
  - UT3: 160/160 cells pass. 20 of them (α 0.01, n 50) are degenerate, so the informative count is 140 / 140.
  - H1c is not confirmed (inconclusive under 08h). RAW-Q and RAW-G over-slip at every α (slip − α 0.0096–0.0507, every CI\*\* > 0), but at α 0.05 their CIs ([0.020, 0.045], [0.016, 0.042]) do not exclude +0.025.
- **5.5 Online calibration under shift (≈ 170 w, Table 3).**
  - Window label-rule slip of OQT-CertGrip is 0.0999–0.1016 across shifts (physical, ordering 0: 0.092–0.103).
  - Frozen-CertGrip reaches 0.3056 (S1) and 0.2461 (S3), and Frozen-COMP reaches 0.5101 (S1). Neither frozen arm breaks in S2.
  - **H3 is inconclusive** in S1 / S2 / S3: R_E 0.8778 / 1.1739 / 0.9629. Realised CI\*\* half-widths (0.15–0.20) are wider than the projected ≈ 0.12.
  - The matched-rate co-requirement fails in S1 (0.032) and S2 (−0.035), physical. The R_E direction is consistent with the slip mismatch, so R_E is not a like-for-like efficiency comparison in S1 and S2.
  - S1m: R_E upper < 1.10, but the window label-rule slip rates differ by 0.025 (> 0.02), so the full criterion is not met.
  - OQT-CertGrip has lower window RE than OQT-COMP in every shift (S1 0.4763 vs 0.8087).
  - H3-L is not confirmed: S1 ρ − ρ_ID +0.0857 [−0.0444, 0.1859], with the TOST ±0.05 not met.
  - H3-S (unadjusted): constant η beats decaying η, ΔC 58.15 (S1) and 42.40 (S3).
  - capped_window = 0.0 everywhere.

## 6 Discussion and Limitations (≈ 250 words)
- **Goal:** State what the evidence licenses, and list the limits from 15_decision.
- **What it licenses:** The friction information comes from the probe, and conformal calibration makes the saving certifiable. Learning on top shows no demonstrated gain at σ 0.2 (`crc_analysis.json → contrasts.H2b`). In secondary, unadjusted analyses the learned model is better at σ 0.4 and worse at σ 0 (audit #18).
- **Limits:**
  - Simulation only, with a single simulator and 5 families. The detector is modelled, and σ 0.2 is an assumed noise level.
  - F\* labels exist only in simulation, so offline CRC is not deployable as is. OQT is the hardware route.
  - H1 failed, so validity rests on the post-failure CRC route, and the grid fix is post hoc.
  - H2b is unresolved. H3 is underpowered, and its feedback in the 20 orderings is the label rule.
  - H2-R is a regime where the method loses. The D2 concentration of the non-monotone instances is unexplained.
  - Secondaries are unadjusted.
- **Future work (one line):** a hardware probe-noise study and an online-only calibration study on a real gripper.

## 7 Conclusion (≈ 100 words)
- **Goal:** Restate the one confirmed claim with its number and its scope limit, and the online finding with its inconclusive efficiency verdict. Evidence: as in the Abstract.

---

## Figure 1 plan (top of page 1 or 2, full width, three panels)
- **Story:** "Probe, then certify." The ramp-down probe turns a friction-blind grasp into one with friction information. CRC turns any force rule into one whose physical slip rate is ≤ α. Most of the force saving survives with a plain physics plug-in, which shows that the probe is the ingredient.
- **(a) Protocol timeline.** Grip force vs time:
  - fixed preload F₀ = 32.7 N, then lift-and-hold, then squeeze to 1.5 F₀;
  - **ramp-down probe** with the detected onset marked (F_onset; inset: shear/normal ratio crossing the detector rule);
  - ramp to F = ĝ(x)·e^λ̂, then the disturbance window (D1–D4 icons).
  - Shade the probe segment, labelled "only friction channel".
- **(b) Certification.** For one stratum, plot the monotonised empirical risk (n R̃_n(λ)+1)/(n+1) vs λ on the 20-point grid. Draw a horizontal line at α = 0.10 and mark λ̂ (first crossing). Show two curves, CertGrip-full and CSF-1: the probe arm crosses α at a lower force multiplier. This panel is schematic but drawn from the real per-stratum λ̂ indices.
- **(c) Result bars** (08c CRC route, test set, α 0.10):
  - RE_mid with CI\*\* for CSF-1 0.7832, CSF-μ̂ σ0.2 0.4843, CertGrip-full σ0.2 0.4567, onset-only σ0.2 0.4336;
  - a dot for each arm's physical slip on a secondary axis (0.1021 / 0.0657 / 0.0829 / 0.0857) against a dashed α line;
  - annotation: "D = 0.4168 [0.3484, 0.4778]".
  - A small grey bar or footnote marker: "narrow-μ sub-pool: D −0.2614".
- **Evidence:** `crc_analysis.json → arms.{CSF-1, CSF-muhat@0.2, full_rd@0.2#0, P_onset@0.2#0}.{RE_mid, RE_mid_CI, slip_phys, lam_idx}`; `crc_analysis.json → contrasts.H2a`; `sec08g.json → H2R.D`.
- **Draft caption:** *Probe, then certify. (a) Every grasp starts from the same 32.7 N preload, so only the ramp-down probe's incipient-slip onset carries friction information. (b) Conformal risk control picks, per disturbance stratum, the smallest force multiplier whose monotonised physical slip risk is ≤ α. (c) At α = 0.10 the probe arm needs less relative excess force than the strongest non-tactile conformal baseline (CSF-1): D = 0.4168, CI\*\* [0.3484, 0.4778], with test physical slip 0.0829. A physics plug-in using the same onset (CSF-μ̂) is not distinguishable from the learned model (H2b not confirmed). In a narrow-friction, mid-amplitude sub-pool the probe arm is worse (D −0.2614). Simulation (MuJoCo), modelled detector, onset noise σ = 0.2.*

## Secondary figure (small, half column): σ curve
- Plot H2a D (08c) at σ 0 / 0.1 / 0.2 / 0.4: 0.6789 / 0.5825 / 0.4168 / 0.1401, with CI\*\*, the SESOI 0.10 line, and σ\* = 0.4 marked.
- Overlay H2b D on the label route: −0.2022 / −0.0753 / 0.0134 / 0.3275.
- **Evidence:** `crc_analysis.json → contrasts.H2a_sigma@{0.0,0.1,0.2,0.4}`, `sigma_star`; `h2_label_rule.json → contrasts.H2b_sigma@{0.0,0.1,0.2,0.4}`.

---

## Every comparison / ablation row in Results → evidence path

### Table 1: Main comparison and robustness (08c CRC route unless stated)
| # | Row | Value(s) | Evidence (`block → key`) |
|---|---|---|---|
| 1 | COMP selection | CSF-1 0.7686, Mondrian-CSF 0.8294, CertGrip-P 0.8335 → CSF-1 | `comp_selection.json → candidates.{CSF-1,Mondrian-CSF,CertGrip-P}.RE_mean, COMP` |
| 2 | CertGrip-full σ0.2 arm | RE 0.4567 [0.4079, 0.5033]; slip_phys 0.0829 | `crc_analysis.json → arms.full_rd@0.2#0.{RE_mid,RE_mid_CI,slip_phys}` |
| 3 | CSF-1 arm | RE 0.7832 [0.6968, 0.8583]; slip_phys 0.1021 | `crc_analysis.json → arms.CSF-1.*` |
| 4 | **H2a (primary)** | D 0.4168 [0.3484, 0.4778], superiority | `crc_analysis.json → contrasts.H2a.{D.mid,CI**.mid,decision}` |
| 5 | H2a F\*_lo / F\*_hi | 0.4150 / 0.4186 | `crc_analysis.json → contrasts.H2a.D.{lo,hi}` |
| 6 | H2a label route | 0.4292 [0.3654, 0.4822] | `h2_label_rule.json → contrasts.H2a` |
| 7 | H2a post hoc grids | 0.4289 [0.3577, 0.4770] | `crc_analysis_v2.json → contrasts.H2a` |
| 8 | H2a seeds 1–4 | 08c 0.3932–0.4494; label 0.4145–0.4442 | `crc_analysis.json → contrasts.H2a_seed{1..4}`; `h2_label_rule.json → contrasts.H2a_seed{1..4}` |
| 9 | H2-C vs Mondrian-CSF | 0.4381 [0.3733, 0.4872] | `sec08g.json → H2C_vs_Mondrian` |
| 10 | H2-H 16 cells | pooled 0.4388, τ 0.0511; smallest F1D3 0.2979 | `sec08g.json → H2H.{pooled_D_RE,tau,cells}` |
| 11 | H2-n (n_cal 50) | α 0.10 0.4146; α 0.20 0.4654 | 14_analysis.md §1.3 (H2-n row) |
| 12 | H2-T tail | T 0.5918 [0.5540, 0.6564] | `sec08f_tail.json → routes.crc_08c` |
| 13 | Oracle gap closed | 0.5172 [0.4489, 0.5762] | `sec08g.json → oracle_decomposition` |
| 14 | **H2-R (scope limit)** | D −0.2614 [−0.5320, −0.0325]; n_cal 352, n_test 548 | `sec08g.json → H2R` |

### Table 2: Attribution ablations (where the saving comes from)
| # | Row | Value(s) | Evidence |
|---|---|---|---|
| 15 | H4a S vs P (±0.05) | D −0.0084, equivalence | `h4a_label_rule.json → contrasts.H4a_S_vs_P` |
| 16 | H4a squeeze: full vs S (±0.03) | D −0.0263 [−0.0558, 0.0149], not confirmed | `h4a_label_rule.json → contrasts.H4a_squeeze_full_vs_S` |
| 17 | H4a + onset: full_rd vs full | D 0.4739 [0.4148, 0.5229] | `h4a_label_rule.json → contrasts.H4a_onset_full_rd_vs_full` |
| 18 | H4e full vs onset-only (CRC) | D −0.0534 [−0.1233, 0.0508], not confirmed; label −0.0417 equivalence | `crc_analysis.json → contrasts.H4e_vs_onset_only`; `h2_label_rule.json → contrasts.H4e_vs_onset_only` |
| 19 | Onset-only arm | RE 0.4336; slip_phys 0.0857 | `crc_analysis.json → arms.P_onset@0.2#0` |
| 20 | **H2b (co-primary)** vs CSF-μ̂ σ0.2 | D 0.0569 [−0.0399, 0.1454], not confirmed | `crc_analysis.json → contrasts.H2b` |
| 21 | H2b post hoc / label | 0.0240 (upper 0.1001) / 0.0134 [−0.0850, 0.0814] | `crc_analysis_v2.json → contrasts.H2b`; `h2_label_rule.json → contrasts.H2b` |
| 22 | CSF-μ̂ σ0.2 arm | RE 0.4843; slip_phys 0.0657; λ̂ idx 0/0/14/12 | `crc_analysis.json → arms.CSF-muhat@0.2` |
| 23 | H2a σ curve | 0.6789 / 0.5825 / 0.4168 / 0.1401; σ\* 0.4 | `crc_analysis.json → contrasts.H2a_sigma@*`, `sigma_star` |
| 24 | H2b σ curve (label; 08e) | −0.2022 / −0.0753 / 0.0134 / 0.3275; 08e σ0 −0.1522, σ0.4 0.3315 | `h2_label_rule.json → contrasts.H2b_sigma@*`; `crc_analysis_v2.json → contrasts.H2b_sigma@*` |
| 25 | H4c shuffled touch vs P | D −0.0253 [−0.0526, 0.0085], inconclusive | `sec08f_label.json → contrasts.H4c_shuf_vs_P` |
| 26 | H4b identifier control | D_FID 0.4638 vs D 0.4555 | `sec08h_h4b.json → results.{D_FID,D}` |
| 27 | D-μ residual R² | P 0.7937, CSF-1 0.6034; CertGrip-full 0.0105/0.0452/0.2142/0.5655; CSF-μ̂σ0.2 0.0054 | `sec08f_dmu.json → results.*.cvR2` |
| 28 | H2-M no mass (descriptive) | D_nm 0.4598; change 0.0042 [−0.0446, 0.0399] | `sec08f_label.json → contrasts.H2M_*` |
| 29 | H2-M mass noise (descriptive) | D_mn 0.4603; COMP_mn RE 0.7991; change +0.0312 | `sec08h_massnoise.json → results.{D_mn,RE.COMP_mn,change}` |
| 30 | H4d F4 − F1 | 0.0342 [−0.0424, 0.1138], inconclusive | `sec08g.json → H4d.full_rd` |

### Validity rows (text, §5.4)
| # | Row | Value(s) | Evidence |
|---|---|---|---|
| 31 | H1-M gate | 8 / 800, CP upper 0.02115 > 0.02, D2 7 | `h1m_analysis.json → {non_monotone,cp_upper_98.75,by_dist,max_rel_above_F_hi}` |
| 32 | H1-V | Δ −0.00429 … −0.00143, all pass | `h1v_analysis.json → {CertGrip@0.1,CertGrip@0.05,CSF-1@0.1,CSF-1@0.05}.Delta` |
| 33 | UT3 | 160/160; informative 140/140; worst CSF-1 D3 0.01034 | `sec08f_ut3.json → n_pass, worst_cell, cells` |
| 34 | H1c raw targeters | RAW-Q/RAW-G over-slip; miss_at_0.05 false | `sec08h_h1c.json → results, miss_at_0.05` |

### Table 3: Online calibration under shift (window 1,001–2,000, 20 orderings)
| # | Row | Value(s) | Evidence |
|---|---|---|---|
| 35 | OQT-CertGrip window slip / RE | S1 0.1016/0.4763, S2 0.0999/0.4262, S3 0.1000/0.5067 | `h3_analysis.json → shifts.{S1,S2,S3}.arms.OQT-CertGrip` |
| 36 | OQT-COMP RE | S1 0.8087, S2 0.7398, S3 0.8635 | `h3_analysis.json → shifts.*.arms.OQT-COMP.RE_window` |
| 37 | Frozen-CertGrip / Frozen-COMP slip | S1 0.3056/0.5101; S2 0.1017/0.1051; S3 0.2461/0.1910 | `h3_analysis.json → shifts.*.arms.Frozen-*.slip_label_window` |
| 38 | Oracle-CertGrip RE / slip | S1 0.5426/0.0751; S2 0.3631/0.1346; S3 0.5262/0.0863 | `h3_analysis.json → shifts.*.arms.Oracle-CertGrip` |
| 39 | **H3 R_E** | 0.8778 [0.7404, 1.1204]; 1.1739 [1.0234, 1.4283]; 0.9629 [0.8363, 1.1449]: all inconclusive | `h3_analysis.json → shifts.*.{R_E,R_E_CI**}`, `H3_primary` |
| 40 | Matched-rate (physical) | S1 0.032, S2 −0.035 (fail), S3 0.009 | `h3_analysis.json → audit.{S1,S2,S3}|matched_physical` |
| 41 | Physical audit OQT-CertGrip 1,001–2,000 | S1 0.103, S2 0.092, S3 0.101 | `h3_analysis.json → audit.*|OQT-CertGrip|1001-2000.slip_direct` |
| 42 | S1m (not primary) | R_E 0.8871 [0.7723, 1.0265]; label diff 0.0248 > 0.02 | `h3_analysis.json → shifts.S1m.{R_E,R_E_CI**,matched_label_window_diff}` |
| 43 | H3-L | S1 +0.0857 [−0.0444, 0.1859] (TOST ±0.05 not met); S2 +0.0637; S3 +0.0820 | `h3_analysis.json → shifts.*.{rho_minus_rhoID,rho_minus_rhoID_CI**}` |
| 44 | H3-S decay − constant η | ΔC S1 58.15 [48.20, 70.20], S3 42.40 [32.40, 49.35]; S2/S1m inconclusive | `sec08h_h3s.json → results.*` |
| 45 | Anti-windup | capped_window 0.0 everywhere | `h3_analysis.json → shifts.*.arms.*.capped_window` |

**Space plan (5 pages):**
- Fig. 1 ≈ 0.33 page.
- Table 1 + Table 2 merged into one two-block table ≈ 0.45 page. Rows 1, 11, 13, 25–30 move to text if space is short.
- Table 3 ≈ 0.25 page.
- σ figure ≈ 0.2 page.
- Text ≈ 3,300 words.
