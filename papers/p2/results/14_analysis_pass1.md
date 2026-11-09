# p2 (CertGrip) v1 — Stage 14 result analysis, pass 1

Scope: every number below is copied (rounded) from the JSON outputs and run-context documents quoted in the stage-14
prompt (`results/v1/*.json`, docs 08a–08h). No new analysis was run. Results are grouped by evidential status:

- **Primary (08b §4, Bonferroni over four decisions, one-sided 0.0125 each, CI\*\* = 97.5 %):** H1, H2a, H2b, H3.
  For H2a / H2b the primary route is the 08c CRC route (`crc_analysis.json`).
- **Secondary / diagnostic (pre-registered in 07 / 08b, operationalised in 08c, 08f, 08g, 08h before computation):**
  H1-V, label-route H2, per-seed D, σ curve, H4a, H4e, H2-T, H4c, H2-M, H3-B, D-μ, UT3, H2-C, H2-n, H2-H, H2-R, H4d,
  D-loc, oracle decomposition, H1c, H3-S, H4b, D-FID, H2-M mass-noise. Holm is not applied to these.
- **Post hoc sensitivity (08e, written after the 08c read-out was seen):** CRC with per-stratum 41-point grids
  (`crc_analysis_v2.json`). Under the 08e reporting rule it can mark a pre-registered CRC result as unreliable but
  cannot upgrade a decision.

---

## 1. Metrics Summary

### 1.1 Setup facts
- COMP selection (selection split, 800 instances, 0 unavoidable excluded): CSF-1 RE_mean **0.7686** (even 0.7921 / odd
  0.7450), Mondrian-CSF 0.8294, CertGrip-P 0.8335 → **COMP = CSF-1**.
- CRC read-out: n_cal 2,000, n_test 2,800 instances, 2,000 bootstrap draws.
- Frozen η = 0.03412 (pilot planning value 0.035).

### 1.2 Primary results

| Decision | Statistic | Point | CI\*\* (97.5 %) | Rule outcome |
|---|---|---|---|---|
| **H1-M** (gate) | non-monotone / 800 | 8 (threshold ≤ 7) | CP upper 98.75 % = 0.02115 (> 0.02) | **fail** |
| **H1** | H1-M and H1-V | — | — | **not confirmed** |
| **H2a** (CRC 08c) | D = 1 − RE(CertGrip-full σ0.2)/RE(CSF-1) | 0.4168 | [0.3484, 0.4778] | **superiority** |
| H2a robustness | D_lo / D_hi | 0.4150 / 0.4186 | [0.3468, 0.4758] / [0.3501, 0.4798] | superiority on both |
| **H2b** (CRC 08c) | D = 1 − RE(CertGrip-full)/RE(CSF-μ̂), σ 0.2 | 0.0569 | [−0.0399, 0.1454] | **not confirmed** |
| **H3, S1** | R_E | 0.8778 | [0.7404, 1.1204] | **inconclusive** |
| **H3, S2** | R_E | 1.1739 | [1.0234, 1.4283] | **inconclusive** |
| **H3, S3** | R_E | 0.9629 | [0.8363, 1.1449] | **inconclusive** |

Primary-route arm values (08c CRC, test set):

| Arm | RE_mid | RE_mid CI\*\* | slip_phys | slip_label | λ̂ index D1/D2/D3/D4 |
|---|---|---|---|---|---|
| CertGrip-full σ0.2 seed 0 | 0.4567 | [0.4079, 0.5033] | 0.0829 | 0.0846 | 10/10/11/10 |
| CSF-1 (COMP) | 0.7832 | [0.6968, 0.8583] | 0.1021 | 0.1036 | 1/1/15/14 |
| CSF-μ̂ σ0.2 | 0.4843 | [0.4435, 0.5219] | 0.0657 | 0.0679 | **0/0**/14/12 |
| onset-only σ0.2 | 0.4336 | [0.3983, 0.4833] | 0.0857 | 0.0896 | 10/10/11/10 |

No λ̂ is at the grid maximum (`at_max` false everywhere), but CSF-μ̂ sits on the grid floor (index 0) in D1/D2 and
CSF-1 one step above it (index 1) — the 08e defect.

H1-M detail: by family F1 3, F2 2, F3 2, F4 1; by disturbance D1 1, **D2 7**, D3 0, D4 0; shift pools S1 0/100,
S2 1/100, S3 1/100. The flickers are tiny: max (slip force above F_hi − F_hi)/F_hi = 0.00904, and six of the ten
listed violations lie below F_hi (rel_above_F_hi ≈ −0.0067), i.e. inside the bisection bracket.

H3 arm values (label-rule feedback, window steps 1,001–2,000, mean of 20 orderings):

| Shift | OQT-CertGrip RE / slip | Oracle-CertGrip RE / slip | OQT-COMP RE / slip | Frozen-CertGrip slip | Frozen-COMP slip | matched-rate (physical diff, ≤ 0.02) |
|---|---|---|---|---|---|---|
| S1 | 0.4763 / 0.1016 | 0.5426 / 0.0751 | 0.8087 / 0.1030 | 0.3056 | 0.5101 | 0.032 → **not matched** |
| S2 | 0.4262 / 0.0999 | 0.3631 / 0.1346 | 0.7398 / 0.0998 | 0.1017 | 0.1051 | −0.035 → **not matched** |
| S3 | 0.5067 / 0.1000 | 0.5262 / 0.0863 | 0.8635 / 0.1004 | 0.2461 | 0.1910 | 0.009 → matched |
| S1m (not primary) | 0.4288 / 0.1012 | 0.4834 / 0.0764 | 0.8085 / 0.1020 | 0.1158 | 0.1916 | — (R_E 0.8871 [0.7723, 1.0265], "non-inferior") |
| ID (reference) | 0.4386 / 0.0995 | 0.4587 / 0.0897 | 0.8114 / 0.0998 | 0.1017 | 0.1149 | — (R_E 0.9561 [0.8260, 1.0909], "non-inferior") |

capped_window = 0.0 in every arm and shift (anti-windup never triggered).

### 1.3 Secondary results (pre-registered)

| Item | Statistic | Point | Interval | File decision |
|---|---|---|---|---|
| H1-V CertGrip α 0.10 | Δ = direct − label slip | −0.00429 | [−0.0075, −0.00143] | pass (τ 0.02) |
| H1-V CertGrip α 0.05 | Δ | −0.00143 | [−0.00393, 0.00071] | pass |
| H1-V CSF-1 α 0.10 | Δ | −0.00321 | [−0.00607, −0.00071] | pass |
| H1-V CSF-1 α 0.05 | Δ | −0.00286 | [−0.00536, −0.00071] | pass |
| H2a label route | D | 0.4292 | [0.3654, 0.4822] | superiority |
| H2b label route | D | 0.0134 | [−0.0850, 0.0814] | **equivalence** |
| H4e CRC 08c (full vs onset-only) | D | −0.0534 | [−0.1233, 0.0508] | not confirmed |
| H4e label route | D | −0.0417 | [−0.0990, 0.0128] | equivalence |
| H4a S vs P (margin 0.05) | D | −0.0084 | [−0.0360, 0.0128] | equivalence |
| H4a squeeze: full vs S (margin 0.03) | D | −0.0263 | [−0.0558, 0.0149] | not confirmed |
| H4a onset: full_rd vs full | D | 0.4739 | [0.4148, 0.5229] | report only |
| H2-T (CRC 08c route, primary) | T = P95 ratio | 0.5918 | [0.5540, 0.6564] | pass (upper < 1.10) |
| H2-T label / CRC 08e | T | 0.6014 / 0.6019 | [0.5521, 0.6459] / [0.5486, 0.6485] | pass / pass |
| H4c shuffled touch vs P | D | −0.0253 | [−0.0526, 0.0085] | inconclusive |
| H2-M no mass (full_rd vs P) | D_nm | 0.4598 | [0.3968, 0.5061] | report only |
| H2-M with-mass reference | D | 0.4555 | [0.4018, 0.5072] | report only |
| H2-M change (nm − with) | — | 0.0042 | [−0.0446, 0.0399] | — |
| H2-M mass-noise: D_mn vs COMP_mn (= CSF-1) | D | 0.4603 | [0.4106, 0.5050] | no prediction |
| H2-M mass-noise change vs D_H2a (0.4292) | — | 0.0312 | [−0.0077, 0.0707] | — |
| H2-C vs Mondrian-CSF | D | 0.4381 | [0.3733, 0.4872] | superiority |
| H2-n α 0.10 (n_cal 50) | D_mean | 0.4146 | [0.2585, 0.5477] | confirmed |
| H2-n α 0.20 | D_mean | 0.4654 | [0.2786, 0.5984] | confirmed |
| H2-H (16 cells, DL) | pooled D | 0.4388 | 95 % [0.4036, 0.4741]; τ 0.0511, Q 31.04 | pass (no guard cell) |
| H2-R (μ ∈ [0.5, 0.8], mid amplitude; n_cal 352, n_test 548) | D | **−0.2614** | [−0.5320, −0.0325] | no prediction |
| H4d full_rd: D_F4 − D_F1 | — | 0.0342 | [−0.0424, 0.1138] | inconclusive |
| H4d full (squeeze only): D_F4 − D_F1 | — | 0.0021 | [−0.0174, 0.0213] | inconclusive |
| Oracle decomposition: share of CSF-1 → oracle gap closed | — | 0.5172 | [0.4489, 0.5762] | — |
| H3-S S1: ΔC (decay − constant η) | — | 58.15 | [48.20, 70.20] | confirmed |
| H3-S S3 | — | 42.40 | [32.40, 49.35] | confirmed |
| H3-S S2 / S1m | — | 2.90 / 2.75 | [−6.65, 7.00] / [−2.05, 11.85] | inconclusive / inconclusive |
| H4b identifier control | D_FID − 0.5·D | 0.2361 | [0.1957, 0.2607] | confirmed (D_FID 0.4638, D 0.4555) |
| H1c | — | see §3.6 | — | "partly confirmed / not confirmed" |

Diagnostics:
- **D-μ** (CV R² of log μ → residual, n 4,800): P 0.7937, S 0.7882, full 0.7787, CSF-1 0.6034 (all le_0.05 false);
  CertGrip-full σ 0 / 0.1 / 0.2 / 0.4: 0.0105 / 0.0452 / 0.2142 / 0.5655; onset-only σ0.2 0.1974; CSF-μ̂ 0.0062 /
  0.0064 / 0.0054 / 0.0034; oracle 0.0163.
- **D-loc:** paired S1 − ID Δlog F\* mean 0.5091, SD 0.0093 (Coulomb 0.511, SD 0; 2,794 pairs); mean |Δĝ|/ĝ: P
  5.1e-6, S 0.00136, full 0.00190, CertGrip-full **0.4469**; preload slip rate 0.0 in every pool.
- **D-FID:** family accuracy from touch only 0.7257 [0.7014, 0.7514], with onset 0.7296 [0.7079, 0.7545]; chance 0.25.
- **H3-B** (frozen offline q̂, no-probe arms): S1 p_obs 0.501–0.523 vs p_pred 0.503–0.525, |diff| ≤ 0.0036, all
  "pass"; S1m p_obs 0.179–0.193, all "pass"; S3 p_obs 0.193–0.211 (up as predicted); S2 p_obs 0.094–0.096 ("no break
  shown"). Probe arm (not tested, 08f deviation): S1 p_obs 0.3039, S1m 0.1246, S3 0.25, S2 0.0936.
- **UT3:** 160 / 160 cells pass; worst cell CSF-1, D3, α 0.01, n 500: mean miss 0.01034 in band [0.00734, 0.01066].
- **Label-route RE** (test): CertGrip-full σ0.2 0.4264, CSF-1 0.7469, CSF-μ̂ σ0.2 0.4321, onset-only 0.4093, P 0.7831,
  S 0.7897, full 0.8104, oracle 0.1271.

### 1.4 Post hoc sensitivity (08e, CRC per-stratum 41-point grids)

| Contrast | 08c (pre-registered) D [CI\*\*] → decision | 08e (post hoc) D [CI\*\*] → decision | Label route (secondary) |
|---|---|---|---|
| H2a σ0.2 | 0.4168 [0.3484, 0.4778] superiority | 0.4289 [0.3577, 0.4770] superiority | 0.4292 superiority |
| **H2b σ0.2** | 0.0569 [−0.0399, 0.1454] not confirmed | 0.0240 [−0.0949, **0.1001**] not confirmed | 0.0134 [−0.0850, 0.0814] equivalence |
| H4e | −0.0534 [−0.1233, 0.0508] not confirmed | −0.0219 [−0.1208, 0.0369] not confirmed | −0.0417 equivalence |
| H2b σ0 | 0.2460 [0.1617, 0.2953] **superiority** | −0.1522 [−0.3028, −0.0596] **inferiority** | −0.2022 inferiority |
| H2b σ0.1 | 0.1072 [0.0333, 0.1919] **superiority** | −0.1019 [−0.1911, 0.0218] not confirmed | −0.0753 [−0.1653, −0.0241] inferiority |
| H2b σ0.4 | 0.3182 [0.2287, 0.4060] superiority | 0.3315 [0.2339, 0.4064] superiority | 0.3275 superiority |

In 08e all λ̂ indices are interior (20–22 of 41, no at_max); CSF-μ̂ σ0.2 RE falls from 0.4843 (08c) to 0.4551, CSF-1
from 0.7832 to 0.7778, CertGrip-full σ0.2 from 0.4567 to 0.4442.

---

## 2. Comparative Findings

### 2.1 Primary
1. **H2a is the one confirmed core claim, and it is robust.** CertGrip-full (σ 0.2) reduces relative excess grip
   force versus the selected non-tactile comparator CSF-1 by D = 0.4168, CI\*\* [0.3484, 0.4778]; the lower limit is far
   above both 0 and the 0.10 SESOI. The decision is unchanged on every route and check in the files: F\*_lo / F\*_hi
   (0.4150 / 0.4186), the post hoc grids (0.4289), the label route (0.4292), seeds 1–4 (08c: 0.4343, 0.4197, 0.3932,
   0.4494, all superiority; label route 0.4245–0.4442), small calibration n (H2-n 0.4146 at α 0.10), cells (H2-H: all
   16 cell D between 0.2979 and 0.5340, pooled 0.4388) and Mondrian-CSF as comparator (0.4381). The grid defect hardly
   touches CSF-1 (RE 0.7832 → 0.7778). The pre-registered power projection (D ≈ 0.43, SE ≈ 0.040) was accurate.
2. **H2b (co-primary) is not confirmed: learned touch does not beat the physics plug-in that uses the same onset
   estimate, and equivalence is not shown on the pre-registered route.** The 08c CI\*\* [−0.0399, 0.1454] crosses both
   0 and +0.10. This was the stated expectation (08b §5: superiority "very unlikely", equivalence ≈ 17 %, inferiority
   ≈ 40 %); inferiority did not occur. The 08c point estimate is biased towards CertGrip by the grid floor (CSF-μ̂ λ̂
   index 0 in D1 / D2). The post hoc grid gives D 0.0240 with upper limit 0.1001 — equivalence missed by the third
   decimal — and the label route gives equivalence ([−0.0850, 0.0814]). Under the 08e rule the paper may not upgrade
   H2b to "equivalence"; the accurate wording is "not confirmed; point estimates 0.013–0.057 across routes; a secondary
   route and a post hoc route place D within or just at ±0.10".
3. **H1 is not confirmed** because H1-M failed by one instance (8 vs ≤ 7; CP upper 0.02115 vs 0.02). The violations are
   small (≤ 0.9 % of F_hi) and concentrated in D2 (7 / 8). This triggered the CRC validity route for H2 (08c).
4. **H3 is inconclusive in all three shifts**, as pre-registered (08b §5: reduced power, half-width ≈ 0.12). Point
   estimates are below 1 for S1 (0.8778) and S3 (0.9629) and above 1 for S2 (1.1739; lower limit 1.0234 > 1 but
   < 1.10). The matched-rate co-requirement fails in S1 (0.032) and S2 (−0.035), so H3 could not have passed in those
   shifts even with a narrower CI. The direction of the mismatch explains the R_E values: in S1 the oracle over-protects
   (window slip 0.0751 vs OQT 0.1016), so OQT spends less force; in S2 the oracle under-protects (0.1346), so it looks
   cheaper than OQT. R_E is therefore not a like-for-like efficiency comparison in S1 and S2.

### 2.2 Secondary (what explains H2a)
- **The gain comes from the ramp-down onset probe, not from static touch or the squeeze.** H4a: S vs P equivalence
  (D −0.0084), squeeze adds nothing (D −0.0263; not confirmed only because the CI lower −0.0558 passes −0.03), onset adds
  D 0.4739. H4e: CertGrip-full vs onset-only is not distinguishable (08c −0.0534, label route equivalence); the point
  estimates favour onset-only. H4c: shuffled touch gives RE 0.8029 vs P 0.7831 (no gain). D-loc: only the onset arm's
  prediction moves under the friction shift (mean |Δĝ|/ĝ 0.4469 vs ≤ 0.0019 for P / S / full).
- **The gain is a friction-information effect.** D-μ: no-probe arms leave R² 0.60–0.79 of log μ in their residuals;
  CertGrip-full leaves 0.0105 / 0.0452 / 0.2142 / 0.5655 at σ 0 / 0.1 / 0.2 / 0.4. H2-M (no mass) leaves D unchanged
  (change 0.0042), as does 10 % mass noise (change 0.0312, CI includes 0). H4b: adding family one-hot keeps D_FID 0.4638
  vs D 0.4555 — family identity does not explain the gain, although touch-only features identify family well (D-FID
  0.7257 vs chance 0.25).
- **Where it fails:** H2-R. In the restricted sub-pool (μ ∈ [0.5, 0.8], mid-amplitude disturbances) CertGrip is worse
  than CSF-1: D −0.2614, CI\*\* [−0.5320, −0.0325] (upper < 0). No prediction was registered, but the paper must report
  it: when friction varies little, the probe's information is worth less than its noise, and the fixed-friction
  plug-in wins. The sub-pool is small (n_cal 352, n_test 548), hence the wide interval.
- **Noise dependence (σ curve, H2a):** D 0.6789 / 0.5825 / 0.4168 / 0.1401 at σ 0 / 0.1 / 0.2 / 0.4 (08c); σ\* = 0.4
  (lower limit 0.0832 < 0.10; 08e 0.0868, label 0.0983 — σ\* = 0.4 on every route). At σ 0.4 the decision label is
  still "superiority" (D 0.1401 ≥ 0.10, lower > 0).
- **Learned vs plug-in by σ (H2b σ curve; secondary at σ ≠ 0.2):** on the two unbiased routes the plug-in wins at
  σ 0 (inferiority) and at σ 0.1 (label route inferiority; 08e not confirmed), the two tie at σ 0.2, and the learned arm
  wins at σ 0.4 (D 0.3275–0.3315; CSF-μ̂ RE 0.9371–0.9876). The D-μ values are consistent with an explanation (an
  interpretation, not a tested claim): the plug-in uses μ̂ at face value (residual R² with log μ ≈ 0.003–0.006 at every
  σ, but RE grows with σ), while the learned arm shrinks the noisy onset feature, leaving friction in the residual
  (R² up to 0.5655) but with lower RE at high noise.
- **Tail and safety secondaries pass:** H2-T T 0.5918 (upper 0.6564 < 1.10); H2-H guard no flagged cell; H2-n
  confirmed at both α.
- **Oracle gap:** CertGrip closes 0.5172 [0.4489, 0.5762] of the CSF-1 → oracle RE gap (oracle RE 0.1271).
- **H4d (CoM mechanism) is inconclusive** for both arms (CIs include 0).
- **Online adaptation (H3 secondaries):** OQT restores window slip to ≈ α in every shift (0.0999–0.1016) while frozen
  arms break (Frozen-CertGrip S1 0.3056, S3 0.2461; Frozen-COMP S1 0.5101). OQT-CertGrip keeps its RE advantage over
  OQT-COMP in each shift (e.g. S1 0.4763 vs 0.8087), and ρ − ρ_ID CIs include 0 in S1, S2, S3 and S1m (no formal H3-L
  decision appears in the files). H3-S: constant η beats decaying η in S1 (ΔC 58.15) and S3 (42.40); inconclusive in S2
  and S1m. H3-B: the Coulomb location prediction matches observed offline breakage for every no-probe arm (S1 |diff|
  ≤ 0.0036); the probe arm breaks less (S1 p_obs 0.3039 vs ≈ 0.50–0.52 for no-probe arms), but no prediction was
  specified for it.

---

## 3. Statistical Checks

1. **Multiplicity.** Four core decisions at one-sided 0.0125 each (CI\*\* 97.5 %): 1 / 4 confirmed (H2a), H1 failed, H2b
   not confirmed, H3 inconclusive (×3). All secondaries are reported unadjusted (08f–08h: Holm not applied); several
   secondaries "confirmed" (H2-n, H3-S S1 / S3, H4b) should be presented as unadjusted.
2. **Validity of the CRC route.** Test physical slip rates of the primary arms: CertGrip-full σ0.2 0.0829, CSF-μ̂ 0.0657,
   onset-only 0.0857, CSF-1 0.1021 (08c); the CertGrip arm is below α 0.10 (monotonised loss and (n+1) correction are
   conservative), CSF-1 and seed 4 (0.1018) are marginally above α, consistent with an expectation guarantee on a finite
   test set. CRC RE is higher than label-route RE for the same arm (0.4567 vs 0.4264), so CRC D values are not
   interchangeable with label-route D values in the text.
3. **Label rule vs physics.** H1-V Δ is negative for all four arms (−0.00143 to −0.00429; disagree_down 6–13 vs
   disagree_up 0–2), with CIs inside τ 0.02; three of four CIs exclude 0. The H3 audits show the same direction (Δ 0 to
   −0.008; S2 OQT-CertGrip 1,001–2,000 Δ −0.008 [−0.0149, −0.0029]). The label rule slightly over-counts slips, i.e. it
   is conservative; the H1-M failure does not translate into a material label-to-physics gap.
4. **Split-conformal calibration (UT3):** 160 / 160 cells pass; CertGrip label-route test slip at α 0.10 0.1057
   (direct 0.1014, CI [0.0864, 0.1168]).
5. **Uncalibrated targeters (H1c):** RAW-Q and RAW-G over-slip at every α (slip − α 0.0096–0.0507, every CI\*\* above
   0); RAW-Qv also over-slips but its CIs include 0. The pre-registered "miss" rule at α 0.05 (CI excludes ±0.025) is not
   met (RAW-Q CI [0.020, 0.045], RAW-G [0.0161, 0.0421]); the H1c failure rule (all inside ±0.25α) is not met either →
   "partly confirmed / not confirmed". Conformal calibration measurably matters, but the registered miss criterion was
   not reached.
6. **Grid floor (08e defect).** 08c λ̂ index 0 for CSF-μ̂ (σ ≤ 0.2) in D1 / D2 and 1 for CSF-1. The defect matters for
   H2b and flips the H2b σ 0 and σ 0.1 secondaries (superiority → inferiority / not confirmed). Per 08e those 08c
   σ 0 / σ 0.1 H2b results are unreliable; the 08c H2b primary decision ("not confirmed") does not change.
7. **Seed variability (08c, secondary):** CertGrip-full σ0.2 RE 0.4312–0.4752 over seeds 0–4; D(H2a) 0.3932–0.4494, all
   superiority; D(H2b) 0.0188–0.1095, all not confirmed. Label-route D(H2b) by seed: 0.0053 and 0.0104 equivalence,
   0.0394 and −0.0120 not confirmed — the label-route H2b equivalence is seed-fragile.
8. **Heterogeneity (H2-H):** τ 0.0511, Q 31.04 over 16 cells; D3 cells have the smallest D (0.2979–0.3868) but all cell
   lower limits are > 0.16.
9. **Numerical health:** 0 / 194 logs with NaN / Inf / RuntimeWarning; no capped stream steps. A tiny cross-file
   discrepancy: CSF-1 label-route RE is 0.7469103493600249 in `h2_label_rule.json` and 0.7469102044808502 in
   `sec08g.json` / `sec08h_massnoise.json` (D_H2a 0.42915688 vs 0.42915677) — immaterial, but the two code paths should
   be reconciled before the numbers are quoted to more than 6 digits.
10. **Documentation inconsistency:** 08b §3 says the COMP selection split is objects 200–249, while 08b §5 (`split_of`),
    08c and `comp_selection.json` use objects 150–199. The JSON and 08c agree; 08b §3 is the stale text from before the
    split change and should be flagged in the paper's deviation list.

---

## 4. Limitations

- **Simulation only** (MuJoCo 4.0.0) with a modelled tactile detector; the detector constants were tuned on pilot
  objects 0–24, and at σ 0 the onset estimate is near-perfect (pilot corr 0.988), which is why σ 0 is only an upper
  bound. The primary σ 0.2 is an assumed noise level, and the advantage shrinks to D 0.1401 (lower 0.0832) at σ 0.4.
- **H1 failed**, so validity rests on the post-failure CRC route (08c) — designed after the H1-M counts were seen but
  before any predictor or test statistic existed.
- **The 08c CRC grid had a defect** that biases the CRC-route H2b towards CertGrip; the fix (08e) is post hoc.
- **H2b is unresolved:** the pre-registered route cannot separate "no difference" from a gain of up to ≈ 0.145, and
  equivalence on the post hoc route is missed by 0.0001 on the upper limit.
- **H3 was underpowered by design** and its matched-rate co-requirement fails in S1 and S2; the stream feedback is the
  label rule, with direct-replay audits only for ordering 0.
- **H2-R shows a regime where CertGrip loses** (narrow friction range); the overall gain depends on the friction spread
  of the object distribution.
- **Several secondaries carry stated deviations** (H3-B probe arm untested; D-μ on cal + test instead of train; RAW-Qv
  log-shift variant; H1c small-n arm dropped; H2-M mass-noise draw fixed only in 08h).
- **Secondaries are unadjusted** for multiplicity.
- The violations in H1-M are concentrated in D2 (7 / 8), which the files do not explain.

---

## 5. Conclusion

Of the four pre-registered core decisions, only **H2a** is confirmed: CertGrip-full at σ 0.2 needs substantially less
excess grip force than the best non-tactile comparator CSF-1 (D 0.4168, CI\*\* [0.3484, 0.4778]). The result holds on
every robustness, route, seed, cell and comparator check in the files. The secondaries show where the gain comes from:
the ramp-down onset probe's friction estimate. Static touch and the squeeze add nothing (H4a, H4c, H4e), mass and
family identity do not explain it (H2-M, H4b), and the gain falls with onset noise (σ\* = 0.4) and turns negative when
friction varies little (H2-R, D −0.2614). **H2b is not confirmed:** learned touch does not beat a physics plug-in using
the same onset estimate (08c D 0.0569, CI\*\* [−0.0399, 0.1454]). Equivalence appears only on the secondary label route
and is missed narrowly on the post hoc grid (upper 0.1001), so it may not be claimed. **H1 failed** narrowly (8 / 800
non-monotone vs ≤ 7), with a small and conservative label-to-physics gap (H1-V pass). **H3 is inconclusive** in S1, S2
and S3, as the reduced-power design expected, and the matched-rate requirement fails in S1 and S2. Online OQT still
restores slip to ≈ α under shift where the frozen arms break. The defensible headline is: "a tactile friction probe
plus conformal calibration cuts the relative excess force of a calibrated physics baseline by D ≈ 0.42. The probe's onset
estimate carries the friction information, and a learned model adds no demonstrated value over a plug-in that uses the
same estimate."
