# p2 · Stage 16 PAPER_OUTLINE [v2]: RSS 2027 Stage 1 extended abstract

**Format:** at most 5 content pages plus 1 page of references, no supplementary material (deadline 2026-12-04 AoE). Methods are complete; experiments may be preliminary. Main body target is **3,300 words** (range 3,000–3,500), abstract excluded. **Stated deviation:** the 9-page word floors of hard_constraints §3 do not apply. A longer master draft is allowed, and stage 22 condenses it.
**Binding inputs:** `results/15_decision_v2.md` (re-scoped story: the claim is *friction-onset probe + conformal calibration*; the learned tactile model adds no demonstrated gain; H1-M failed; H3 inconclusive; the H2-R scope limit appears in abstract-level claims) and the audit rewrites of `results/14_analysis_v2.md` (pass 2, findings 1–17) and `results/14_analysis.md` (Part B, findings 1–23). Where 15_decision_v2 and an audit rewrite differ in wording, the audit wording is used (see "Wording rules" below).
**Revision of:** `sections/00_outline.md` (v1). v1 primary verdicts are unchanged. All v2 rows (amendment 09: A1 frontier, A2 Learn-then-Test, A3 extra contrasts, B1 / H5 CSF-proxy, B2 probe + fixed margin, B3 online physical feedback) are **secondary** (B2 and B3 descriptive).
**Evidence notation:** `v1:block → key path` refers to `results/v1/results_v1.json`; `v2:block → key path` refers to `results/v2/results_v2.json`. Example: `v2:a_analysis_08e.json → point."D_match:full_rd@0.2#0"`.
**Number convention:** every value is copied from those two JSON files (or the prompt) and **rounded** to 4 decimals, the v1 outline convention. The Stage-14 v2 tables *truncate*, so a few v2 values here are 0.0001 higher than in 14_analysis_v2.md (e.g. D_ltt 0.4043 vs 0.4042; B2 D2 slip 0.0229 vs 0.0228). The paper uses the values in this outline. No new arithmetic is introduced.
**Naming in the paper (replaces internal pipeline codes; v1 gate action 4):**

| Internal code | Name used in the paper |
|---|---|
| 08b | pre-registration |
| 07 / pilot amendment | pilot amendment (introduced the probe arm) |
| 08c grids | primary CRC grid (20 points per stratum) |
| 08e grids | post hoc refined grid (41 points per stratum) |
| 08d | online protocol |
| amendment 09 / v2 | second-round analyses (all secondary) |
| edge rule | grid-edge rule (re-run on the refined grid when λ̂ hits index 0 or 19) |
| full_rd@0.2#0 | CertGrip-full (σ 0.2, seed 0) |
| P_onset@0.2#0 | onset-only |
| CSF-muhat@σ | CSF-μ̂ (physics plug-in on the same noisy onset) |
| CSF-proxy@σ_p | CSF-proxy (physics plug-in on a non-tactile noisy friction prior) |
| CSF-1 | COMP, the strongest non-tactile conformal baseline |

*RE* = mean relative excess (F − F\*_mid)/F\*_mid. *D* = 1 − RE(target)/RE(comparator). *CI\*\** = 97.5 % two-sided object-cluster bootstrap interval, 2,000 draws, λ̂ refitted in each draw.

**Wording rules (binding audit rewrites, collected once):**
- Never: "learned tactile model improves grasping"; "matches", "as efficient as", "does as well" (no equivalence test was run for any v2 pair); "robust" / "reproduced" / "replicated" for v2 routes (they re-analyse the seed-0 replays: say "route robustness, not replication"); "confirmed" for H5 (say "held as predicted, secondary"); "calibration is necessary" (say "within B2, no single uniform margin brings every stratum near α"); "holds α" for B3 without "descriptive, 5 orderings, no interval"; "guaranteed in the real world"; "holds on every check".
- Learned vs plug-in: "At σ 0.2, a learned model shows no demonstrated gain over a plug-in using the same onset estimate. In secondary, unadjusted analyses it is better at σ 0.4 and worse at σ 0."
- σ (onset-detection noise) and σ_p (log-normal noise on a non-tactile friction prior) are different noise models; never put them on one scale.
- Use the refined grid / edge-rule rows for CSF-μ̂ and CSF-proxy at σ / σ_p 0.2 (they sit at grid index 0 on the primary grid in D1/D2).

---

## What changed vs v1 (summary for the writer)
1. **Identity of the method.** The contribution is restated as *probe + simple force rule + CRC*; the learner is optional. Contributions and abstract say so. A headline secondary row gives CSF-μ̂ vs CSF-1 and onset-only vs CSF-1 with their own CI\*\* (gate action 3).
2. **Matched-risk comparison** (A1 risk-efficiency frontier) replaces the informal "unequal slip makes D conservative" argument (gate action 1).
3. **High-probability certificate** (A2 Learn-then-Test, δ 0.1) is reported next to the in-expectation CRC result (gate action 2).
4. **Stronger baselines:** non-tactile CSF-proxy (H5, B1) and probe + hand-set margin (B2) (gate evidence action 9, in part; the reactive slip-tightening controller and a correlated-μ pool were not run, 15_decision_v2 → limitations).
5. **Online study with the CRC λ̂ warm start and physical feedback** on 5 orderings (B3) (gate evidence action 10, in part; H3 itself is not re-decided).
6. **Per-stratum test slip** of the four CRC arms is now reported (`v1:19_report_rows.json`), which shows the two CSF-1 strata above α that the gate mentioned.
7. **Readability:** descriptive names for pipeline codes, a hypothesis glossary (Table 0), each caveat stated once in full (§6) and referenced elsewhere; Table 2's label-route H2b row renamed "within ±0.10, secondary, not decision-bearing" (gate actions 4–5).
8. **Figure 1(b)** is drawn from real data (the A1 frontier), not a schematic (gate action 7).
9. **Related work** gains a sentence on classic incipient-slip friction reading and human grip-force regulation, and a precise novelty statement (gate action 6; see citation gap note in §2).
10. **Not done, stated as such:** exploratory stratification of the H2-R loss by detector error / family and of D3 margins by hidden amplitude (gate action 8) — no such rows exist in either JSON; hardware σ grounding (gate action 11). Both go to §6.

---

## Title
**Probe, Then Certify: A Tactile Friction-Onset Probe with Conformal Risk Control for Certified-Slip Minimal-Force Grasping**

Alternative: *Certified-Slip Grip Regulation from a Friction-Onset Probe: Where the Force Saving Comes From*.

---

## Abstract (≈ 200 words, outside the 3,300 count)
- **Goal:** State the problem (smallest grip force whose *physical* slip rate is ≤ α, from robot-measurable information), the method as *probe + force rule + CRC*, the one confirmed result, the attribution, the scope limit, and the online study, in one paragraph.
- **Content, in order:**
  1. Problem: non-tactile conformal baselines are calibrated but friction-blind, so the calibrated force must cover the whole friction range.
  2. Method: a ramp-down friction-onset probe after a friction-free preload; any force rule fed with the onset estimate (a physics plug-in or a learned quantile model) is calibrated by conformal risk control (CRC) on the monotonised binary physical-slip loss, per disturbance stratum.
  3. Main result (pre-registered): vs the strongest non-tactile conformal baseline, selected beforehand, at α 0.10: D = 0.4168, CI\*\* [0.3484, 0.4778]; test physical slip 0.0829 (baseline 0.1021).
  4. Secondary support in one clause: the saving persists at matched slip (D 0.4563) and under a high-probability Learn-then-Test certificate (D 0.4043).
  5. Attribution: the saving comes from the probe. The plug-in on the same onset reaches D 0.4149 vs the baseline (refined grid); at σ 0.2 the learned model shows no demonstrated gain over it (H2b not confirmed). Against a non-tactile friction prior of log-noise 0.2, no advantage is shown.
  6. Scope limit (mandatory): in a narrow-friction (μ ∈ [0.5, 0.8]), mid-amplitude sub-pool the method is worse than the baseline: D −0.2614, CI\*\* [−0.5320, −0.0325].
  7. Online: binary-feedback quantile tracking keeps window slip near α under shift while frozen calibration breaks; efficiency vs oracle recalibration is inconclusive.
  8. Setting: simulation only (MuJoCo), modelled tactile detector, assumed onset noise.
- **Evidence:** `v1:crc_analysis.json → contrasts.H2a.{D.mid, "CI**".mid, decision}`; `v1:crc_analysis.json → arms."full_rd@0.2#0".slip_phys`, `arms."CSF-1".slip_phys`; `v2:a_analysis.json → point."D_match:full_rd@0.2#0"`, `point."D_ltt:full_rd@0.2#0"`; `v2:a_analysis_08e.json → point."D_crc:CSF-muhat@0.2"`; `v1:crc_analysis.json → contrasts.H2b.decision`; `v2:b_analysis_edge.json → H5."H5@0.2_08e"`; `v1:sec08g.json → H2R.{D, "CI**"}`; `v1:h3_analysis.json → H3_primary`. cite: `angelopoulos2022conformal`, `angelopoulos2023conformala`.

---

## Table 0: Hypothesis glossary (≈ 0.12 page; the paper uses descriptive names, codes only in this table and in table rows)
| Code | Question | Status | Outcome |
|---|---|---|---|
| H1 (H1-M, H1-V) | Is the simulator's slip label monotone in force and faithful to physics? | primary | not confirmed (H1-M gate failed) |
| H2a | Probe arm vs strongest non-tactile conformal baseline (efficiency at α) | primary | superiority |
| H2b | Learned model vs physics plug-in on the same onset (σ 0.2) | co-primary | not confirmed |
| H3 | Online tracking vs oracle recalibration under shift (efficiency ratio R_E) | primary | inconclusive (S1, S2, S3) |
| H4a / H4e / H4c | Feature chain: static touch, squeeze, onset; touch on top of onset; shuffled touch | secondary | see Table 2 |
| H5 | Probe arm vs non-tactile friction prior of noise σ_p | secondary (v2) | held as predicted |
| H2-R | Same contrast as H2a in a narrow-friction, mid-amplitude sub-pool | secondary, no prediction | reversal |
| H1c | Do uncalibrated targeters miss α? | secondary | not confirmed (inconclusive) |
| A1 / A2 / B2 / B3 | Matched-slip frontier / Learn-then-Test / probe + fixed margin / online physical feedback | secondary (v2); B2, B3 descriptive | see Tables 1–3 |

---

## 1 Introduction (≈ 500 words)
- **Goal:** Motivate certified minimal-force grasping, name the missing ingredient (friction information read online), state the research question, and give contributions that each map to a confirmed or explicitly scoped result. Connect every paragraph to the core question: can a short tactile probe make a certified physical-slip bound cheaper in force?
- **Paragraphs:**
  1. **Why minimal force with a slip certificate.** Fragile objects, prosthetics, gentle grasping. Tactile grip controllers react to slip or estimate friction, but give no distribution-free slip-rate bound. Cite `dong2019maintaining`, `khamis2021real`, `boonstra2024estimate`, `niu2026synchronized`, `veiga2020grip`, `berman2025autonomous`, `willemet2024grip`.
  2. **Why conformal methods alone are not enough.** CRC can certify any force rule (`angelopoulos2022conformal`, `lei2017distribution`); without friction information the calibrated multiplier must cover the whole μ range. Hence the comparison against the *strongest* non-tactile conformal baseline, selected on a disjoint split: CSF-1 RE_mean 0.7686 vs Mondrian-CSF 0.8294 and CertGrip-P 0.8335.
  3. **Research question.** Can a ramp-down probe supply enough friction information to cut excess grip force at a certified physical slip rate ≤ α? Which component carries the saving? Does calibration survive shift when only binary slip feedback is available?
  4. **Contributions (4 bullets, restated around probe + rule + CRC):**
     - (C1) *Method.* A grasp protocol in which a friction-free preload makes a ramp-down onset probe the only friction channel, and CRC on the monotonised *physical* binary slip loss turns any probe-fed force rule into one with expected slip ≤ α per stratum. The learned quantile model is optional. CRC on the physical loss is needed because the label rule is not exactly monotone in force (8 of 800 instances).
     - (C2) *Pre-registered evaluation* against the best non-tactile conformal comparator: D = 0.4168, CI\*\* [0.3484, 0.4778]; secondary checks at matched slip and under a high-probability certificate.
     - (C3) *Attribution.* Ablations and stronger baselines that locate the saving in the probe: the plug-in on the same onset already captures it; static touch, squeeze and the learned model add no demonstrated gain at σ 0.2; a sufficiently good non-tactile friction prior leaves no shown advantage; and a sub-pool where the method loses.
     - (C4) *Online calibration under shift* from binary feedback: frozen calibration breaks, quantile tracking keeps slip near α (also under physical feedback, descriptive); efficiency vs oracle recalibration is inconclusive.
  5. **Status sentence (one line, details in §6).** Of four pre-registered core decisions one is confirmed (H2a); H1 and H2b are not; H3 is inconclusive.
- **Evidence:** `v1:comp_selection.json → candidates.{"CSF-1","Mondrian-CSF","CertGrip-P"}.RE_mean, COMP`; `v1:h1m_analysis.json → {non_monotone, n}`; `v1:crc_analysis.json → contrasts.H2a`; `v2:a_analysis.json → point."D_match:full_rd@0.2#0"`, `point."D_ltt:full_rd@0.2#0"`; `v1:h3_analysis.json → H3_primary`.

## 2 Related Work (≈ 380 words, three compact paragraphs + one novelty sentence)
- **Goal:** Position the paper between tactile grip-force control and conformal safety in robotics; show that no prior work certifies a *physical slip rate* of a *minimal* grip force, and say precisely what is new relative to "lower the force until slip to read friction".
  1. **Tactile slip, friction reading and grip control.** Incipient-slip sensing and friction estimation from slip onset are established (`chen2018tactile`, `romeo2020methods`, `khamis2021real`, `dong2019maintaining`); so is human grip–load coupling under friction change (`willemet2024grip`). Learned and reactive controllers: `james2020slip`, `grover2022detect`, `boonstra2024estimate`, `niu2026synchronized`, `kuo2025tracing`, `feng2026tactilereflex`, `lach2024zero`, `ayral2026reactive`, `almohammed2022switched`, `veiga2020grip`, `shang2026exp`. Gap: margins are reactive or estimated; no coverage guarantee.
  2. **Robust and safe grasping under uncertainty.** `cloutier2018examining`, `cortez2019control`, `kim2024robust`, `enwerem2026firmgrasp`, `enwerem2026variational`: model-based margins that depend on assumed uncertainty sets.
  3. **Conformal prediction and risk control in robotics.** Foundations `vovk2005algorithmic`, `romano2019conformalized`, `angelopoulos2023conformal`, `angelopoulos2022conformal`, `angelopoulos2026conformal`, `bian2023training` (training-conditional coverage, motivates the high-probability certificate), `ding2023class`. Shift / online: `gibbs2021adaptive`, `gibbs2022conformal`, `angelopoulos2023conformala`, `angelopoulos2024online`, `farinhas2023non`, `ge2024stochastic`. Robotics: `lekeufack2024conformal`, `lindemann2025formal`, `dixit2022adaptive`, `marques2026particle`, `lindemann2023conformal`, `ren2023robots`, `huang2023conformal`, `strawn2023conformal`, `zhang2024bayesian`, `zhao2024conformalized`, `kumar2026learnable`. Gap: none certifies a contact outcome as a binary loss in force space.
  - **Novelty sentence:** reading friction from slip onset is not new; what is new is (i) a protocol where the onset is the *only* friction channel, so its value can be isolated, (ii) a distribution-free per-stratum bound on the *physical* slip rate of the resulting minimal force, and (iii) evidence that the calibrated saving comes from the probe, not from the learned model.
  - Simulators (one sentence in §4): `wang2022tacto`, `akinola2025tacsl`, `leins2025hydroelastictouch`, `luu2025manifeel`, `birtalan2026impact`.
- **Citation gap (TODO before stage 17, do not invent keys):** the 52 available cite_keys contain no Johansson/Westling-style human grip–load paper, no early incipient-slip friction paper, and no Learn-then-Test paper (Angelopoulos et al.). Add them to `docs/05_knowledge_cards.json` first; until then the text uses only the keys above and §3.4 cites LTT as "[LTT, to be added]".

## 3 Problem Formulation and Method (≈ 800 words)
- **Goal:** Self-contained technical description of the approach (not a workflow). Every symbol in Results is defined here. The method is presented as *probe → force rule → certificate*, with the learned model as one option for the force rule.
- **3.1 Problem (≈ 130 w).** Instance x: object, pose, disturbance type D1–D4. F\*(x): minimal no-slip force under a slip criterion (2 mm tangential displacement, 3° rotation, or contact loss). Goal: choose F(x) minimising E[(F − F\*)/F\*] subject to P(slip at F(x)) ≤ α. Labels F\*_lo / F\*_hi / F\*_mid from 11-replay log-space bisection on [0.1, 100] N; they exist only in simulation (hence §3.4 and §3.5).
- **3.2 Grasp protocol and friction-onset probe (≈ 180 w).** Fixed preload F₀ = 32.7 N for every instance (encodes neither m nor μ); lift and hold; squeeze F₀ → 1.5 F₀ → F₀. **Ramp-down probe:** decrease force at a fixed rate; a touch-only detector on the pad shear/normal ratio stops at incipient slip, giving F_onset and the Coulomb reading μ̂ = m g / (2 F_onset). Onset noise model log F_onset + σ ε, σ ∈ {0, 0.1, 0.2, 0.4}; primary σ 0.2 (assumed), σ 0 is an upper bound. Then ramp to the chosen F and run the disturbance window; a slip during the probe counts as a slip. One-line input table: which inputs each arm receives.
- **3.3 Force rules (≈ 170 w).** All rules have the form F(x; λ) = min(F_max, F_base(x) e^λ).
  - **Probe-fed plug-in CSF-μ̂:** F_base = m(g + a_cmd)/(2 μ̂). *This is the simplest instance of the method.*
  - **Probe-fed learned model:** gradient-boosted quantile predictor ĝ(x) with feature sets P (proprioception) ⊂ S (+ static touch) ⊂ full (+ squeeze) ⊂ CertGrip-full (+ onset); onset-only = P + onset.
  - **Non-tactile baselines:** CSF-1, F_base = m(g + a_cmd)/(2 μ̄); Mondrian-CSF (one λ per family × disturbance cell, privileged family ID); **CSF-proxy (new)**: the same formula with a non-tactile friction prior μ̃ = clip(μ·exp(σ_p ε_p), 0.1, 3.0), σ_p ∈ {0.2, 0.4, 0.8}; it is an oracle-side construction that asks how good a friction prior must be, not a deployable estimator.
  - **Probe + fixed margin (new, uncalibrated):** CSF-μ̂ force with a single hand-set margin m ∈ {0, 0.25, 0.5, 1.0}, no calibration.
  - COMP is selected on the selection split before any calibration or test access.
- **3.4 Certificates on the physical binary loss (≈ 220 w).**
  - Loss L_i(λ) = 1{physical slip in direct replay}; monotonised L̃_i(λ) = max_{λ' ≥ λ} L_i(λ').
  - **In-expectation (CRC, primary):** per stratum, λ̂ = min{λ ∈ Λ : (n R̃_n(λ) + 1)/(n + 1) ≤ α} (`angelopoulos2022conformal`) ⇒ E[slip] ≤ α for an exchangeable test instance (marginal, per stratum; not per deployment).
  - **High-probability (Learn-then-Test, secondary, new):** per stratum, choose λ so that the slip risk is ≤ α with probability ≥ 1 − δ over the calibration draw, δ = 0.1 (`bian2023training` for the training-conditional view; LTT reference to be added). The guarantee is per stratum at δ 0.1, not family-wise across strata.
  - Λ: 20-point primary grid centred on the selection-split quantile; 41-point post hoc refined grid as a sensitivity route; grid-edge rule as registered.
  - Motivation for the physical loss: H1-M failed (8 / 800 non-monotone, CP upper 0.02115 > 0.02, 7 of 8 in D2), so split conformal on labels is not guaranteed; the label-rule CQR route (`romano2019conformalized`) is reported as secondary.
- **3.5 Online calibration from binary feedback (≈ 100 w).** Score-space online quantile tracking (OQT, `angelopoulos2023conformala`): q_{t+1} = q_t + η (slip_t − α), one tracker per stratum, η = 0.03412 (frozen), anti-windup at F_max. Score space rather than ACI (`gibbs2021adaptive`) because a friction drop can move scores beyond the calibration support. References: decaying step (`angelopoulos2024online`), frozen, oracle recalibration. Two feedback variants: label-rule feedback with the label-route q̂ warm start (pre-registered H3), and physical direct-replay feedback with the CRC λ̂ warm start (new, B3).
- **Evidence:** `v1:h1m_analysis.json → {non_monotone, "cp_upper_98.75", threshold_count, by_dist}`; `v1:h3_analysis.json → eta`; `v2:b3_analysis.json → eta, purpose`; `v2:a_analysis.json → {alpha, delta, slip_match}`; `v1:crc_analysis.json → {n_cal_instances, n_test_instances, draws}`.

## 4 Experimental Setup (≈ 400 words)
- **Goal:** Enough detail to reproduce and to read the decisions: simulator, objects, shifts, splits, statistics, the pre-registration and every deviation (listed once, here).
- **Content:**
  - Simulator: MuJoCo 4.0.0, physics parameters identical across families and shifts; parallel-jaw gripper with pad touch grids. Families F1 boxes, F2 cylinders, F3 ellipsoids/capsules, F4 off-CoM composites; F5 thin plates/disks for shift. Static-touch consistency check: max |pad normal − F₀| 0.1597 N, preload slip count 0, so static touch carries no friction information by construction (one sentence).
  - Ranges: μ log-uniform [0.3, 1.0], m [0.05, 1.0] kg; disturbances D1 lift acceleration, D2 shake, D3 lateral pull, D4 payload.
  - Splits by object: n_cal 2,000, n_test 2,800 instances (700 per stratum); selection split (objects 150–199 per family) for COMP and λ grids.
  - Shifts: S1 μ × 0.6, S1m μ × 0.9 (not primary), S3 disturbance amplitude × 1.5, S2 new family F5. Pre-registered streams T = 2,000, shift at step 501, window 1,001–2,000, 20 orderings, label-rule feedback. B3 streams: 500 in-distribution steps then 1,500 shifted steps, 5 orderings, S1 and S3 only.
  - Statistics: Bonferroni over 4 core decisions (one-sided 0.0125, CI\*\* 97.5 %), object-cluster bootstrap with λ̂ recomputed per draw, SESOI 0.10 for D, F\*_lo / F\*_hi robustness. Secondaries (including all v2 rows) are unadjusted and labelled; the refined grid can mark a primary-grid result unreliable but cannot upgrade it. Matched slip uses one target (0.10), by linear interpolation between adjacent grid offsets k; every matched-slip CI\*\* has 2,000 / 2,000 valid draws.
  - **Deviation list (one compact paragraph, stated once):**
    1. The CRC route was written after the H1-M counts were seen, before any predictor existed.
    2. The primary-grid floor defect (CSF-μ̂ λ̂ index 0 in D1/D2; CSF-1 index 1) was fixed post hoc by the refined grid.
    3. The pre-registration text gives selection objects 200–249 in one place and 150–199 elsewhere; the JSON uses 150–199.
    4. H3-B probe arm untested; D-μ computed on cal + test; H2-M mass noise drawn only in a later addendum; H3-L TOST computed after the read-out.
    5. All second-round analyses (A1, A2, A3, B1–B3) were registered after the v1 read-out and review; they are secondary and cannot change a v1 decision. CSF-proxy σ_p 0.2 hit the grid edge and was re-run under the registered edge rule.
  - Compute: 14.50 logged CPU hours for the CRC runs (one clause, if space).
- **Evidence:** `v1:crc_analysis.json → {n_cal_instances, n_test_instances, draws}`; `v1:comp_selection.json → objects`; `v1:19_report_rows.json → static_touch_check.{max_abs_normal_minus_F0, preload_slip_count}`, `compute_logged_cpu_hours.total`, `per_stratum_test_slip_crc08c."CSF-1".D1.n`; `v1:crc_analysis.json → arms."CSF-muhat@0.2".lam_idx`, `arms."CSF-1".lam_idx`; `v2:a_analysis.json → "CI**".*.n_valid`; `v2:b_analysis.json → grid_edge_lam_idx`; `v2:b_analysis_edge.json → grid_edge_lam_idx`; `v2:b3_analysis.json → windows`.

## 5 Results (≈ 950 words; Table 1, Table 2, Table 3, Fig. 1, small σ figure)
- **Goal:** Quantitative outcomes in this order: main comparison and its certificate variants → where the saving comes from → stronger baselines → where it fails → validity of the certificate → online shift. Each subsection opens with the result sentence, then the numbers; caveats are referenced to §6, not repeated.

### 5.1 Main comparison and certificate variants (≈ 260 w; Table 1, Fig. 1b–c)
- **Primary (H2a):** D = 0.4168, CI\*\* [0.3484, 0.4778], superiority; F\*_lo / F\*_hi 0.4150 / 0.4186. Test physical slip CertGrip-full 0.0829, CSF-1 0.1021.
- **Per-stratum test slip (new, report-only):** CertGrip-full D1–D4 0.0871 / 0.0714 / 0.0757 / 0.0971, all ≤ α; CSF-1 0.1157 / 0.0886 / 0.1057 / 0.0986, above α in D1 and D3 — consistent with an in-expectation guarantee on 700 test instances per stratum. This motivates 5.1's high-probability row.
- **Matched-risk comparison (A1, secondary):** at matched test slip 0.10, RE CertGrip-full 0.4290 [0.4099, 0.4560] vs CSF-1 0.7891 [0.7329, 0.8422]; D_match 0.4563 [0.4096, 0.4896] (refined grid 0.4475 [0.4111, 0.4880]), superiority. This replaces the informal "D is conservative" argument: at equal slip the saving is the same size or larger than at the CRC operating points.
- **High-probability certificate (A2, secondary):** Learn-then-Test (δ 0.1) moves CertGrip-full from test slip 0.0829 to 0.0696 and RE_mid from 0.4567 to 0.4895; CSF-1 to slip 0.0907, RE 0.8216. D_ltt 0.4043 [0.3362, 0.4561] (refined 0.4015 [0.3391, 0.4594]), superiority. No LTT stratum flag fired.
- **Route robustness (one sentence; audit rewrite):** across the CRC, matched-slip and LTT routes on both grids, D(CertGrip-full vs CSF-1) ranges from 0.4015 to 0.4563, every CI\*\* lower bound above 0 (smallest 0.3362); these re-analyse the seed-0 replays, so they are route robustness, not replication. Replication evidence remains the per-seed rows: seeds 1–4 primary grid 0.4343 / 0.4197 / 0.3932 / 0.4494, label route 0.4145–0.4442, all superiority. Also holds for the label route (0.4292), refined grid (0.4289), all 16 family × disturbance cells (pooled 0.4388; three of the four smallest cells are D3), n_cal 50 (0.4146), and vs Mondrian-CSF (0.4381). It **reverses in H2-R** (§5.4) and its lower limit falls below 0.10 at σ 0.4.
- Tail (one clause): P95 ratio T 0.5918 [0.5540, 0.6564]. Oracle gap closed 0.5172 (text only if space).

### 5.2 Where the saving comes from (≈ 260 w; Table 2, σ figure)
- **Headline attribution rows (gate action 3, secondary):** vs CSF-1 on the CRC route,
  - CSF-μ̂ (plug-in on the same onset): D_crc 0.4149 [0.3322, 0.4890] on the refined grid (primary grid 0.3816 [0.2965, 0.4505], biased against CSF-μ̂ by the grid floor);
  - onset-only: D_crc 0.4464 [0.3776, 0.4906] (refined 0.4412 [0.3846, 0.4942]);
  - all superiority. Statement: *probe + a simple force rule + CRC already captures the saving.*
- **Learned vs plug-in (H2b, co-primary, not confirmed):** D 0.0569 [−0.0399, 0.1454]; refined grid 0.0240 (CI\*\* upper 0.1001, misses equivalence by 0.0001); label route [−0.0850, 0.0814], "within ±0.10, secondary, not decision-bearing". Equivalence is **not** claimed. v1 point comparison mixed slip levels (CertGrip-full 0.0829 vs CSF-μ̂ 0.0657); at matched slip on the refined grid the CSF-μ̂ RE (0.4045 [0.3892, 0.4369]) is below CertGrip-full's (0.4292 [0.4074, 0.4522]) with overlapping CI\*\*, consistent with "not confirmed". Across routes CSF-μ̂'s D vs CSF-1 is larger than CertGrip-full's at matched slip (0.4690 / 0.4793 vs 0.4563 / 0.4475) but smaller on LTT (0.3704 / 0.4040 vs 0.4043 / 0.4015) and CRC (0.3816 / 0.4149 vs 0.4168 / 0.4289); no direct contrast was computed, so the ordering is unresolved.
- **Feature chain (H4a, H4e, H4c):** static touch equivalent to P within ±0.05 (D −0.0084); no evidence the squeeze helps (D −0.0263, equivalence ±0.03 not shown); adding the onset gives D 0.4739. Full pipeline vs onset-only: no advantage shown (H4e D −0.0534 [−0.1233, 0.0508], not confirmed); onset-only's point D vs CSF-1 is the larger one on all six v2 route × grid rows (e.g. D_match 0.4736 vs 0.4563). Shuffled touch inconclusive (D −0.0253).
- **σ dependence (small figure):** H2a D 0.6789 / 0.5825 / 0.4168 / 0.1401 at σ 0 / 0.1 / 0.2 / 0.4 (σ\* = 0.4). Learned vs plug-in, secondary label route: plug-in better at σ 0 (D −0.2022) and σ 0.1 (D −0.0753), within ±0.10 at σ 0.2, learned better at σ 0.4 (D 0.3275); refined grid agrees in direction (σ 0 −0.1522, σ 0.4 0.3315). Primary-grid σ 0 / 0.1 H2b superiority rows are unreliable (grid floor).
- **Friction-information diagnostic (text, one sentence each):** D-μ residual R² of log μ: no-probe arms P 0.7937, CSF-1 0.6034; CertGrip-full 0.0105 / 0.0452 / 0.2142 / 0.5655 by σ; CSF-μ̂ σ 0.2 0.0054. Detector at σ 0: correlation with log μ 0.9480, bias +0.3186, SD 0.1103 (F3 SD 0.1965). Identifier control H4b: D_FID 0.4638 vs D 0.4555 (unadjusted). H2-M descriptive only (onset confounds m and μ).

### 5.3 Stronger baselines (≈ 160 w; Table 2 lower block)
- **Non-tactile friction prior (H5, B1, secondary):** consistent with the registered prediction, D(CertGrip-full vs CSF-proxy) falls from 0.8361 [0.8137, 0.8573] (σ_p 0.8) to 0.5042 [0.4362, 0.5635] (σ_p 0.4) to −0.0299 [−0.1903, 0.0816] (σ_p 0.2, edge-rule grid; primary-grid row 0.0514 superseded). The CI\*\* first includes 0 at σ_p 0.2: against a non-tactile prior of log-noise 0.2, CertGrip shows no efficiency advantage; no equivalence test was registered. σ_p 0.8 proxy RE 2.7859 [2.5273, 3.0700] vs CSF-1 0.7832 [0.6968, 0.8583]; σ_p 0.4 RE 0.9213 overlaps CSF-1; neither is a registered contrast. Interpretation (one sentence, §6): the value of the probe is that it delivers a friction estimate of this quality from touch alone; the paper does not compare against a deployable vision/category prior.
- **Probe + hand-set margin (B2, descriptive):** with one uniform margin on the CSF-μ̂ force, no margin tested brings every stratum near α: m ≤ 0.5 under-grips (RE −0.3829, −0.2287, −0.0744; overall slip 0.9582 / 0.8257 / 0.6182); at m = 1.0 overall slip 0.3350, D1 / D2 over-protected (0.0414 / 0.0229) while D3 / D4 stay at 0.6571 / 0.6186. The calibrated arm reaches overall test slip 0.0829 (CRC) and 0.0696 (LTT). Calibration sets stratum-specific margins.

### 5.4 Where it fails (≈ 80 w)
- H2-R sub-pool (μ ∈ [0.5, 0.8] and mid-amplitude disturbances; n_cal 352, n_test 548): D −0.2614, CI\*\* [−0.5320, −0.0325]; secondary, no registered prediction. Whether the narrow friction range causes it is **not tested**; the planned stratification by detector error and family was not run (§6). H4d (CoM mechanism) inconclusive (F4 − F1 0.0342 [−0.0424, 0.1138]).

### 5.5 Validity of the certificate (≈ 90 w)
- H1 not confirmed (H1-M 8 / 800; violations small, max relative excess over F_hi 0.00904). H1-V passes for all four arm × α combinations; the label rule slightly over-counts slips (Δ −0.00429 to −0.00143). UT3: 160 / 160 cells pass, 20 degenerate (α 0.01, n 50), informative 140 / 140. H1c not confirmed (inconclusive): RAW-Q / RAW-G over-slip at every α (0.0096–0.0507 above α, every CI\*\* > 0), but at α 0.05 their CIs ([0.020, 0.045], [0.016, 0.042]) do not exclude +0.025.

### 5.6 Online calibration under shift (≈ 200 w; Table 3)
- **Pre-registered (label-rule feedback, 20 orderings):** OQT-CertGrip window label slip 0.0999–0.1016 (physical, ordering 0: 0.092–0.103); Frozen-CertGrip 0.3056 (S1) and 0.2461 (S3), Frozen-COMP 0.5101 (S1); neither frozen arm breaks in S2. **H3 inconclusive** in S1 / S2 / S3: R_E 0.8778 / 1.1739 / 0.9629, realised half-widths 0.15–0.20 vs projected ≈ 0.12. Matched-rate co-requirement fails in S1 (0.032) and S2 (−0.035); the R_E direction is consistent with the slip mismatch, so R_E is not like-for-like there. S1m: R_E upper < 1.10 but label slip difference 0.0248 > 0.02. OQT-CertGrip lower window RE than OQT-COMP in every shift (S1 0.4763 vs 0.8087). H3-L not confirmed (S1 +0.0857 [−0.0444, 0.1859]). H3-S (unadjusted): constant η beats decaying η (ΔC 58.15 S1, 42.40 S3). capped_window 0.0 everywhere.
- **Physical feedback with CRC warm start (B3, descriptive, new):** in the shifted windows (1,001–2,000 and 1,501–2,000), mean physical slip over 5 orderings lies between 0.0936 and 0.1032 for CertGrip and CSF-1 on S1 and S3 (per-ordering 0.082–0.112); D_RE (CertGrip vs CSF-1) 0.4115–0.4216 in those windows. Steps 1–500 are pre-shift. Physical- and label-feedback trackers give close window means (S1 CertGrip 1,001–2,000: slip 0.1002 vs 0.1008, RE 0.4633 vs 0.4729). No interval was registered; this is the online analogue of H2a, not a test of H3.

## 6 Discussion and Limitations (≈ 250 words; each caveat stated here once in full)
- **What the evidence licenses:** the friction information comes from the probe, and CRC makes the saving certifiable; a plain physics plug-in on the onset already captures it (D_crc 0.4149 refined grid). At σ 0.2 the learned model shows no demonstrated gain; in secondary, unadjusted analyses it is better at σ 0.4 and worse at σ 0. The saving survives at matched slip and under a high-probability certificate (secondary). Against a non-tactile friction prior of log-noise 0.2 no advantage is shown: the probe's contribution is a friction estimate of that quality obtained from touch.
- **Limits (full statements, referenced from elsewhere):**
  - Simulation only, one simulator, rigid contact, 5 families; modelled detector; σ 0.2 is assumed and the effect's lower limit falls below the SESOI at σ 0.4 (D 0.1401). Hardware σ grounding not done.
  - Friction is drawn independently of all non-tactile inputs; the ≈ 42 % figure is tied to this distribution. CSF-proxy is an oracle-side construction; no correlated-μ pool, deployable vision/category prior, or reactive slip-tightening controller was evaluated.
  - F\* labels exist only in simulation: offline CRC is not deployable as is; online tracking with physical feedback is the hardware route (B3: 5 orderings, S1 / S3, no interval).
  - H1 failed; validity rests on the post-failure CRC route, and the grid fix is post hoc. Certificates are marginal per stratum; LTT holds per stratum at δ 0.1, not family-wise.
  - H2b unresolved; no direct CertGrip vs CSF-μ̂ contrast at matched slip or under LTT. H3 underpowered; its 20-ordering feedback is the label rule with label-route warm start.
  - H2-R is a regime where the method loses; its cause, the D2 concentration of non-monotone instances and the weak D3 cells are untested (the exploratory stratifications requested in review were not run).
  - All secondaries, including all v2 rows, are unadjusted.
- **Future work (one line):** hardware probe-noise measurement and online physical-feedback calibration on a real gripper.

## 7 Conclusion (≈ 80 words)
- **Goal:** Restate the one confirmed claim with its number (D 0.4168 [0.3484, 0.4778]) and its scope limit (H2-R D −0.2614), the method identity (probe + simple rule + CRC; learner optional), and the online finding with its inconclusive efficiency verdict. Evidence: as in the Abstract.

---

## Figure 1 plan (full width, three panels, ≈ 0.33 page; rendered from data, gate action 7)
- **Story:** "Probe, then certify." The probe turns a friction-blind grasp into one with friction information; CRC turns any probe-fed force rule into one whose physical slip rate is ≤ α; at equal slip the probe arms need far less excess force.
- **(a) Protocol timeline** (schematic, the only schematic panel): grip force vs time — preload F₀ = 32.7 N, lift-and-hold, squeeze to 1.5 F₀, **ramp-down probe** with F_onset marked (inset: shear/normal ratio crossing the detector rule), ramp to F = F_base · e^λ̂, disturbance window (D1–D4 icons). Shade the probe as "only friction channel".
- **(b) Risk-efficiency frontier (real data, replaces v1's schematic risk curve):** test physical slip (x) vs RE_mid (y) over grid offsets k = −4 … +4 for CertGrip-full, onset-only, CSF-μ̂ (refined grid) and CSF-1; vertical dashed line at α = 0.10; mark the CRC operating point (k = 0) of each arm. Data: primary grid for CertGrip-full, onset-only, CSF-1 (e.g. CertGrip-full k = 0: 0.0829 / 0.4567; CSF-1 k = 0: 0.1021 / 0.7832); refined grid for CSF-μ̂ (k = 0: 0.0750 / 0.4551; k = −4: 0.2414 / 0.2399). Annotate "D_match = 0.4563".
- **(c) Result bars** (primary CRC route, test set, α 0.10): RE_mid with CI\*\* for CSF-1 0.7832, CSF-μ̂ σ 0.2 0.4843, CertGrip-full 0.4567, onset-only 0.4336; dots for physical slip (0.1021 / 0.0657 / 0.0829 / 0.0857) against a dashed α line; annotation "D = 0.4168 [0.3484, 0.4778]"; grey footnote marker "narrow-μ sub-pool: D −0.2614".
- **Evidence:** `v2:a_analysis.json → frontier.{"full_rd@0.2#0","P_onset@0.2#0","CSF-1"}[k].{slip_phys, RE_mid}`; `v2:a_analysis_08e.json → frontier."CSF-muhat@0.2"[k]`; `v2:a_analysis.json → point."D_match:full_rd@0.2#0"`; `v1:crc_analysis.json → arms.{"CSF-1","CSF-muhat@0.2","full_rd@0.2#0","P_onset@0.2#0"}.{RE_mid, RE_mid_CI, slip_phys}`; `v1:crc_analysis.json → contrasts.H2a`; `v1:sec08g.json → H2R.D`.
- **Draft caption:** *Probe, then certify. (a) Every grasp starts from the same 32.7 N preload, so only the ramp-down probe's incipient-slip onset carries friction information. (b) Test physical slip vs relative excess force over the calibration grid: at matched slip 0.10 the probe-fed arms need far less excess force than the strongest non-tactile conformal baseline CSF-1 (D_match 0.4563). (c) Conformal risk control at α = 0.10: D = 0.4168, CI\*\* [0.3484, 0.4778], test physical slip 0.0829. A physics plug-in on the same onset (CSF-μ̂) is not distinguishable from the learned model (H2b not confirmed). In a narrow-friction, mid-amplitude sub-pool the probe arm is worse (D −0.2614). Simulation (MuJoCo), modelled detector, onset noise σ = 0.2.*

## Secondary figure (small, half column): σ curve
- H2a D (primary grid) at σ 0 / 0.1 / 0.2 / 0.4: 0.6789 / 0.5825 / 0.4168 / 0.1401 with CI\*\*, SESOI 0.10 line, σ\* = 0.4 marked; overlay H2b label route −0.2022 / −0.0753 / 0.0134 / 0.3275. Optional third series (if legible): H5 D vs σ_p 0.2 / 0.4 / 0.8 on a separate inset axis (never on the σ axis).
- **Evidence:** `v1:crc_analysis.json → contrasts."H2a_sigma@{0.0,0.1,0.2,0.4}"`, `sigma_star`; `v1:h2_label_rule.json → contrasts."H2b_sigma@{0.0,0.1,0.2,0.4}"`; `v2:b_analysis.json → H5."H5@0.4", H5."H5@0.8"`; `v2:b_analysis_edge.json → H5."H5@0.2_08e"`.

---

## Every comparison / ablation row in Results → evidence path

### Table 1: Main comparison, certificate variants and robustness (primary CRC route unless stated)
| # | Row | Value(s) | Evidence |
|---|---|---|---|
| 1 | COMP selection | CSF-1 0.7686, Mondrian-CSF 0.8294, CertGrip-P 0.8335 → CSF-1 | `v1:comp_selection.json → candidates.*.RE_mean, COMP` |
| 2 | CertGrip-full arm | RE 0.4567 [0.4079, 0.5033]; slip_phys 0.0829; λ̂ idx 10/10/11/10 | `v1:crc_analysis.json → arms."full_rd@0.2#0"` |
| 3 | CSF-1 arm | RE 0.7832 [0.6968, 0.8583]; slip_phys 0.1021; λ̂ idx 1/1/15/14 | `v1:crc_analysis.json → arms."CSF-1"` |
| 4 | **H2a (primary)** | D 0.4168 [0.3484, 0.4778], superiority | `v1:crc_analysis.json → contrasts.H2a.{D.mid,"CI**".mid,decision}` |
| 5 | H2a F\*_lo / F\*_hi | 0.4150 / 0.4186 | `v1:crc_analysis.json → contrasts.H2a.D.{lo,hi}` |
| 6 | Per-stratum test slip (report-only) | CertGrip-full 0.0871/0.0714/0.0757/0.0971; CSF-1 0.1157/0.0886/0.1057/0.0986; CSF-μ̂ 0.0586/0.0386/0.0800/0.0857; onset-only 0.0914/0.0871/0.0714/0.0929 | `v1:19_report_rows.json → per_stratum_test_slip_crc08c.*.{D1..D4}.slip_phys` |
| 7 | A1 RE at matched slip 0.10 (primary grid) | CertGrip-full 0.4290 [0.4099, 0.4560]; onset-only 0.4154 [0.3969, 0.4375]; CSF-1 0.7891 [0.7329, 0.8422] | `v2:a_analysis.json → point."RE_match@*"`, `"CI**"."RE_match@*".ci` |
| 8 | A1 RE at matched slip (refined grid) | CertGrip-full 0.4292 [0.4074, 0.4522]; onset-only 0.4173 [0.3968, 0.4393]; CSF-μ̂ 0.4045 [0.3892, 0.4369]; CSF-1 0.7769 [0.7305, 0.8363] | `v2:a_analysis_08e.json → point."RE_match@*"`, `"CI**"."RE_match@*".ci` |
| 9 | **A1 D_match CertGrip-full vs CSF-1** | 0.4563 [0.4096, 0.4896]; refined 0.4475 [0.4111, 0.4880]; superiority | `v2:a_analysis.json → point."D_match:full_rd@0.2#0"`, `"CI**"."D_match:full_rd@0.2#0"`; same in `v2:a_analysis_08e.json` |
| 10 | A2 LTT arms (primary grid) | CertGrip-full slip 0.0696, RE 0.4895, λ̂ 10/10/12/11; onset-only 0.0639 / 0.4808; CSF-μ̂ 0.0529 / 0.5173 (λ̂ 0/0/15/13); CSF-1 0.0907 / 0.8216 | `v2:a_analysis.json → ltt_arms.*.{lam,slip_phys,RE_mid}` |
| 11 | A2 LTT arms (refined grid) | CertGrip-full 0.0707 / 0.4879; onset-only 0.0743 / 0.4643; CSF-μ̂ 0.0654 / 0.4858; CSF-1 0.0911 / 0.8151 | `v2:a_analysis_08e.json → ltt_arms.*.{slip_phys,RE_mid}` |
| 12 | **A2 D_ltt CertGrip-full vs CSF-1** | 0.4043 [0.3362, 0.4561]; refined 0.4015 [0.3391, 0.4594]; superiority; no LTT flag | `v2:a_analysis.json → point."D_ltt:full_rd@0.2#0"`, `"CI**"."D_ltt:full_rd@0.2#0"`, `ltt_arms.*.lam.*[1]`; same in `v2:a_analysis_08e.json` |
| 13 | A3 refined-grid CRC D CertGrip-full | 0.4289 [0.3577, 0.4770] | `v2:a_analysis_08e.json → point."D_crc:full_rd@0.2#0"`; = `v1:crc_analysis_v2.json → contrasts.H2a` |
| 14 | H2a label route | 0.4292 [0.3654, 0.4822] | `v1:h2_label_rule.json → contrasts.H2a` |
| 15 | H2a seeds 1–4 (replication) | primary grid 0.4343 / 0.4197 / 0.3932 / 0.4494; label 0.4145–0.4442; all superiority | `v1:crc_analysis.json → contrasts.H2a_seed{1..4}`; `v1:h2_label_rule.json → contrasts.H2a_seed{1..4}` |
| 16 | H2-C vs Mondrian-CSF | 0.4381 [0.3733, 0.4872] | `v1:sec08g.json → H2C_vs_Mondrian` |
| 17 | H2-H 16 cells | pooled 0.4388, τ 0.0511; smallest F1D3 0.2979, F3D3 0.3115, F4D3 0.3348, F1D4 0.3753; every cell CI\*\* lower > 0.16 | `v1:sec08g.json → H2H.{pooled_D_RE,tau,cells}` |
| 18 | H2-n (n_cal 50) | α 0.10 0.4146; α 0.20 0.4654 | `v1:sec08g.json → H2n` (values as in 14_analysis.md §1.3) |
| 19 | H2-T tail | T 0.5918 [0.5540, 0.6564] | `v1:sec08f_tail.json → routes.crc_08c` |
| 20 | Oracle gap closed | 0.5172 [0.4489, 0.5762] | `v1:sec08g.json → oracle_decomposition` |
| 21 | **H2-R (scope limit)** | D −0.2614 [−0.5320, −0.0325]; n_cal 352, n_test 548 | `v1:sec08g.json → H2R` |

### Table 2: Attribution and stronger baselines
| # | Row | Value(s) | Evidence |
|---|---|---|---|
| 22 | **A3 CSF-μ̂ vs CSF-1 (headline secondary)** | refined 0.4149 [0.3322, 0.4890]; primary grid 0.3816 [0.2965, 0.4505] (grid-floor biased); superiority | `v2:a_analysis_08e.json → point."D_crc:CSF-muhat@0.2"`, `"CI**"."D_crc:CSF-muhat@0.2"`; same in `v2:a_analysis.json` |
| 23 | **A3 onset-only vs CSF-1** | 0.4464 [0.3776, 0.4906]; refined 0.4412 [0.3846, 0.4942]; superiority | `v2:a_analysis.json → point."D_crc:P_onset@0.2#0"`; `v2:a_analysis_08e.json` same key |
| 24 | A1 / A2 D for CSF-μ̂ and onset-only vs CSF-1 | D_match CSF-μ̂ 0.4690 / 0.4793, onset-only 0.4736 / 0.4629; D_ltt CSF-μ̂ 0.3704 / 0.4040, onset-only 0.4148 / 0.4303 (primary / refined) | `v2:a_analysis.json`, `v2:a_analysis_08e.json → point."D_match:*"`, `point."D_ltt:*"` |
| 25 | H4a S vs P (±0.05) | D −0.0084, equivalence | `v1:h4a_label_rule.json → contrasts.H4a_S_vs_P` |
| 26 | H4a squeeze: full vs S (±0.03) | D −0.0263 [−0.0558, 0.0149], not confirmed | `v1:h4a_label_rule.json → contrasts.H4a_squeeze_full_vs_S` |
| 27 | H4a + onset: full_rd vs full | D 0.4739 [0.4148, 0.5229] | `v1:h4a_label_rule.json → contrasts.H4a_onset_full_rd_vs_full` |
| 28 | H4e full vs onset-only | CRC D −0.0534 [−0.1233, 0.0508], not confirmed; refined −0.0219; label −0.0417 "within ±0.05, secondary" | `v1:crc_analysis.json → contrasts.H4e_vs_onset_only`; `v1:crc_analysis_v2.json`, `v1:h2_label_rule.json` same key |
| 29 | Onset-only arm | RE 0.4336; slip_phys 0.0857 | `v1:crc_analysis.json → arms."P_onset@0.2#0"` |
| 30 | **H2b (co-primary)** | D 0.0569 [−0.0399, 0.1454], not confirmed | `v1:crc_analysis.json → contrasts.H2b` |
| 31 | H2b refined / label | 0.0240 (upper 0.1001) / 0.0134 [−0.0850, 0.0814], **"within ±0.10, secondary, not decision-bearing"** | `v1:crc_analysis_v2.json → contrasts.H2b`; `v1:h2_label_rule.json → contrasts.H2b` |
| 32 | CSF-μ̂ arm | RE 0.4843; slip_phys 0.0657; λ̂ idx 0/0/14/12 | `v1:crc_analysis.json → arms."CSF-muhat@0.2"` |
| 33 | H2a σ curve | 0.6789 / 0.5825 / 0.4168 / 0.1401; σ\* 0.4 | `v1:crc_analysis.json → contrasts."H2a_sigma@*"`, `sigma_star` |
| 34 | H2b σ curve (label; refined) | −0.2022 / −0.0753 / 0.0134 / 0.3275; refined σ0 −0.1522, σ0.4 0.3315 | `v1:h2_label_rule.json → contrasts."H2b_sigma@*"`; `v1:crc_analysis_v2.json → contrasts."H2b_sigma@*"` |
| 35 | H4c shuffled touch vs P | D −0.0253 [−0.0526, 0.0085], inconclusive | `v1:sec08f_label.json → contrasts.H4c_shuf_vs_P` |
| 36 | H4b identifier control | D_FID 0.4638 vs D 0.4555 (unadjusted) | `v1:sec08h_h4b.json → results.{D_FID,D}` |
| 37 | D-μ residual R² | P 0.7937, CSF-1 0.6034; CertGrip-full 0.0105/0.0452/0.2142/0.5655; CSF-μ̂ σ0.2 0.0054 | `v1:sec08f_dmu.json → results.*.cvR2` |
| 38 | Detector error at σ 0 (text) | r 0.9480, bias 0.3186, SD 0.1103; F3 SD 0.1965; r(err, log μ) −0.2529 | `v1:19_report_rows.json → detector_id_sigma0`, `detector_error_structure` |
| 39 | H2-M (descriptive) | D_nm 0.4598, change 0.0042 [−0.0446, 0.0399]; mass noise D_mn 0.4603, COMP_mn RE 0.7991, change +0.0312 | `v1:sec08f_label.json → contrasts.H2M_*`; `v1:sec08h_massnoise.json → results` |
| 40 | **H5 vs CSF-proxy σ_p 0.2 (edge rule, row of record)** | D −0.0299 [−0.1903, 0.0816], not shown | `v2:b_analysis_edge.json → H5."H5@0.2_08e".{D.mid,"CI**".mid,decision_09}` |
| 41 | H5 σ_p 0.2 primary grid (superseded) | 0.0514 [−0.0673, 0.1660] | `v2:b_analysis.json → H5."H5@0.2"` |
| 42 | H5 σ_p 0.4 / 0.8 | 0.5042 [0.4362, 0.5635] / 0.8361 [0.8137, 0.8573], superiority | `v2:b_analysis.json → H5."H5@0.4"`, `H5."H5@0.8"` |
| 43 | CSF-proxy arms | σ_p 0.2 edge: RE 0.4312 [0.3906, 0.4759], slip 0.0825, λ̂ 20/21/20/20; σ_p 0.4: 0.9213 [0.8423, 1.0024], slip 0.0911; σ_p 0.8: 2.7859 [2.5273, 3.0700], slip 0.0971 | `v2:b_analysis_edge.json → arms."CSF-proxy@0.2"`; `v2:b_analysis.json → arms."CSF-proxy@0.4"`, `arms."CSF-proxy@0.8"` |
| 44 | Edge-rule target arm | CertGrip-full λ̂ 20/20/21/21, slip 0.0900, RE 0.4442 [0.4064, 0.4973] | `v2:b_analysis_edge.json → arms."full_rd@0.2#0"` |
| 45 | **B2 probe + fixed margin (test)** | m 0 / 0.25 / 0.5 / 1.0: slip 0.9582 / 0.8257 / 0.6182 / 0.3350; RE −0.3829 / −0.2287 / −0.0744 / 0.2341; m 1.0 strata 0.0414 / 0.0229 / 0.6571 / 0.6186 | `v2:b_analysis.json → B2_margin."{0.0,0.25,0.5,1.0}".test.{slip_phys,RE_mid,by_stratum_slip}` |
| 46 | H4d F4 − F1 | 0.0342 [−0.0424, 0.1138], inconclusive | `v1:sec08g.json → H4d.full_rd` |

### Validity rows (text, §5.5)
| # | Row | Value(s) | Evidence |
|---|---|---|---|
| 47 | H1-M gate | 8 / 800, CP upper 0.02115 > 0.02, D2 7; max rel. above F_hi 0.00904 | `v1:h1m_analysis.json → {non_monotone,"cp_upper_98.75",by_dist,max_rel_above_F_hi}` |
| 48 | H1-V | Δ −0.00429 … −0.00143, all pass | `v1:h1v_analysis.json → {"CertGrip@0.1","CertGrip@0.05","CSF-1@0.1","CSF-1@0.05"}.Delta` |
| 49 | UT3 | 160/160; informative 140/140; worst CSF-1 D3 0.01034 | `v1:sec08f_ut3.json → n_pass, worst_cell, cells` |
| 50 | H1c raw targeters | RAW-Q / RAW-G over-slip; miss_at_0.05 false | `v1:sec08h_h1c.json → results, "miss_at_0.05"` |

### Table 3: Online calibration under shift
| # | Row | Value(s) | Evidence |
|---|---|---|---|
| 51 | OQT-CertGrip window slip / RE (label feedback) | S1 0.1016 / 0.4763, S2 0.0999 / 0.4262, S3 0.1000 / 0.5067 | `v1:h3_analysis.json → shifts.{S1,S2,S3}.arms."OQT-CertGrip"` |
| 52 | OQT-COMP RE | S1 0.8087, S2 0.7398, S3 0.8635 | `v1:h3_analysis.json → shifts.*.arms."OQT-COMP".RE_window` |
| 53 | Frozen-CertGrip / Frozen-COMP slip | S1 0.3056 / 0.5101; S2 0.1017 / 0.1051; S3 0.2461 / 0.1910 | `v1:h3_analysis.json → shifts.*.arms."Frozen-*".slip_label_window` |
| 54 | Oracle-CertGrip RE / slip | S1 0.5426 / 0.0751; S2 0.3631 / 0.1346; S3 0.5262 / 0.0863 | `v1:h3_analysis.json → shifts.*.arms."Oracle-CertGrip"` |
| 55 | **H3 R_E** | 0.8778 [0.7404, 1.1204]; 1.1739 [1.0234, 1.4283]; 0.9629 [0.8363, 1.1449]: all inconclusive | `v1:h3_analysis.json → shifts.*.{R_E,"R_E_CI**"}`, `H3_primary` |
| 56 | Matched-rate (physical) | S1 0.032, S2 −0.035 (fail), S3 0.009 | `v1:h3_analysis.json → audit."{S1,S2,S3}|matched_physical"` |
| 57 | Physical audit OQT-CertGrip 1,001–2,000 (ordering 0) | S1 0.103, S2 0.092, S3 0.101 | `v1:h3_analysis.json → audit."*|OQT-CertGrip|1001-2000".slip_direct` |
| 58 | S1m (not primary) | R_E 0.8871 [0.7723, 1.0265]; label diff 0.0248 > 0.02 | `v1:h3_analysis.json → shifts.S1m.{R_E,"R_E_CI**",matched_label_window_diff}` |
| 59 | H3-L | S1 +0.0857 [−0.0444, 0.1859] (TOST ±0.05 not met); S2 +0.0637; S3 +0.0820 | `v1:h3_analysis.json → shifts.*.{rho_minus_rhoID,"rho_minus_rhoID_CI**"}` |
| 60 | H3-S decay − constant η | ΔC S1 58.15 [48.20, 70.20], S3 42.40 [32.40, 49.35]; S2 / S1m inconclusive | `v1:sec08h_h3s.json → results.*` |
| 61 | Anti-windup | capped_window 0.0 everywhere | `v1:h3_analysis.json → shifts.*.arms.*.capped_window` |
| 62 | **B3 physical feedback, shifted windows (descriptive)** | S1 CertGrip 1,001–2,000 0.1002 / RE 0.4633, 1,501–2,000 0.1032 / 0.4626; S1 CSF-1 0.1016 / 0.7915, 0.0988 / 0.7998; S3 CertGrip 0.1010 / 0.5127, 0.0992 / 0.5135; S3 CSF-1 0.1010 / 0.8719, 0.0936 / 0.8726; per-ordering range 0.082–0.112 | `v2:b3_analysis.json → shifts.{S1,S3}.physical_feedback.{CertGrip,CSF1}."{1001-2000,1501-2000}".{slip_phys,RE_mid}.{mean,min,max}` |
| 63 | B3 D_RE (CertGrip vs CSF-1) | S1 0.4387 / 0.4146 / 0.4216; S3 0.4438 / 0.4120 / 0.4115 (windows 1–500 pre-shift / 1,001–2,000 / 1,501–2,000) | `v2:b3_analysis.json → shifts.{S1,S3}.D_RE` |
| 64 | B3 physical vs label feedback | S1 CertGrip 1,001–2,000 slip 0.1002 vs 0.1008, RE 0.4633 vs 0.4729 | `v2:b3_analysis.json → shifts.S1.{physical_feedback,label_feedback_08d}.CertGrip."1001-2000"` |

**Space plan (5 pages):**
- Fig. 1 ≈ 0.33 page; σ figure ≈ 0.18 page.
- Table 0 (glossary) ≈ 0.12 page.
- Tables 1 + 2 merged into one three-block table (main / certificate variants; attribution; stronger baselines) ≈ 0.5 page. In the printed table keep rows 4, 6, 9, 12, 21, 22, 23, 27, 28, 30, 31, 40, 42, 45; rows 1–3, 5, 7, 8, 10, 11, 13–20, 24–26, 29, 32–39, 41, 43, 44, 46 go to text or are dropped if space is short.
- Table 3 ≈ 0.25 page: rows 51, 53, 55, 56, 62, 63; the rest to text.
- Text ≈ 3,300 words (Intro 500, Related 380, Method 800, Setup 400, Results 950, Discussion 250, Conclusion 80, ≈ 3,360).
