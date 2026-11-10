# p2 (CertGrip) — Stage 14 analysis, v4 (amendment 11), pass 1

Sources: `results/v4/v4_analysis.json` (2,000 bootstrap draws, α 0.1) and, for comparison only, `results/v3/a7_integrated.json`.
D(a vs b) = 1 − RE(a)/RE(b); D > 0 means arm a needs less excess grip force than arm b. CI** is the 97.5 % object-cluster bootstrap interval. Numbers are rounded to 4 significant figures. v1–v3 verdicts are not re-decided here.

---

## 1. Metrics Summary

### 1.1 Confirmatory decisions C1–C5 (Holm at 5 %)

| Row | Pool | Contrast (route) | Point D | CI** | p used | p_holm | Code decision | Registered prediction | Outcome vs registration |
|---|---|---|---|---|---|---|---|---|---|
| C1 | f4 | CSF-muhat@0.2 vs CSF-1 (matched) | 0.4314 | [0.3824, 0.4835] | 0.0 | 0.0 | superiority | superiority | **Prediction met** |
| C2 | f4 | full_rd@0.2#0 vs CSF-muhat@0.2 (matched) | 0.01117 | [−0.05552, 0.05686] | 0.0 (TOST; two-sided p 0.915) | 0.0 | equivalence | equivalence | **Prediction met** |
| C3 | f4 | full_rd@0.2#0 vs CSF-1 (CRC) | 0.4135 | [0.3578, 0.4903] | 0.0 | 0.0 | superiority | superiority | **Prediction met** |
| C4 | c4 | CSF-muhat@0.2 vs CSF-fam (matched) | −0.5814 | [−0.7208, −0.4563] | 0.0 | 0.0 | "inferiority" | none | **Not superior**; CI** wholly below 0 |
| C5 | c4 | full_rd@0.2#0 vs CSF-fam (matched) | −0.5461 | [−0.6590, −0.4290] | 0.0 | 0.0 | "inferiority" | none | **Not superior**; CI** wholly below 0 |

All 2,000 draws were valid for every row, and no row hit the grid edge (`edge: false` everywhere). The C1–C5 results are therefore all interpretable under the "grid floor / ceiling" rule.

### 1.2 Arm-level metrics

**f4 (n_cal 500 objects, n_test 700 objects)**

| Arm | Test slip | RE (CRC) | RE_match | Mean hold force (N) |
|---|---|---|---|---|
| CSF-1 | 0.08786 | 0.7823 | 0.7518 | 7.125 |
| CSF-shrunk@0.2 | 0.08321 | 0.4140 | 0.3797 | 6.181 |
| CSF-muhat@0.1 | 0.0825 | 0.2824 | 0.2642 | 5.784 |
| CSF-muhat@0.2 | 0.09786 | 0.4317 | 0.4275 | 6.463 |
| CSF-muhat@0.4 | **0.1014** | 0.8987 | 0.9071 | 8.598 |
| full_rd@0.1#0 | 0.06929 | 0.3377 | 0.2926 | 5.890 |
| full_rd@0.2#0 | 0.08107 | 0.4588 | 0.4227 | 6.115 |
| full_rd@0.4#0 | 0.08536 | 0.6513 | 0.6134 | 6.650 |

**c4 (n_cal 500, n_test 700; CSF-fam μ̄ F1 0.379, F2 0.496, F3 0.677, F4 0.852)**

| Arm | Test slip | RE (CRC) | RE_match | Mean hold force (N) |
|---|---|---|---|---|
| CSF-1 | 0.08214 | 0.8043 | 0.7399 | 7.506 |
| CSF-muhat@0.2 | 0.08607 | 0.4542 | 0.4229 | 6.646 |
| full_rd@0.2#0 | 0.08821 | 0.4413 | 0.4134 | 6.256 |
| CSF-fam | 0.05929 | 0.2995 | 0.2674 | 5.933 |

As a consistency check, the confirmatory points can be rebuilt from the RE_match column. For C1, 1 − 0.4275/0.7518 gives 0.4314. For C4, 1 − 0.4229/0.2674 gives −0.5814.

---

## 2. Comparative Findings

### 2.1 On independent friction (f4), the probe plus plug-in is enough at σ 0.2 (C1–C3)
- **Probe sufficiency (C1).** The plug-in CSF-muhat@0.2 cuts relative excess force against CSF-1 by D 0.4314 (CI** [0.3824, 0.4835]).
- **The learner adds nothing at σ 0.2 (C2).** D(full_rd vs plug-in) is 0.01117. Its CI** [−0.05552, 0.05686] lies inside the ±0.10 SESOI, and the TOST p is 0.0.
- **H2a replicates on fresh objects (C3).** On the CRC route, full_rd@0.2#0 beats CSF-1 by D 0.4135 (CI** [0.3578, 0.4903]).
- **Summary.** The v3 exploratory attribution ("the saving comes from the probe; probe + plug-in + CRC suffices") is now **confirmed on 700 fresh test objects at σ 0.2.**

### 2.2 The tactile saving does not survive a friction-informative prior (C4, C5)
On c4, friction is predictable from the visible family. There the non-tactile prior CSF-fam beats both tactile arms:
- **Plug-in vs CSF-fam (C4):** D −0.5814 (CI** [−0.7208, −0.4563]).
- **Learner vs CSF-fam (C5):** D −0.5461 (CI** [−0.6590, −0.4290]).

CSF-fam reaches the lowest RE_match (0.2674) and the lowest test slip (0.05929) of all c4 arms. Against CSF-1 it gives D 0.6386 (CI** [0.6043, 0.6620]). That is larger than the gain of either tactile arm over CSF-1: plug-in 0.4285 [0.3648, 0.4741] and learner 0.4412 [0.3876, 0.4817].

The CRC-route versions (S5) agree:
- **Plug-in vs CSF-fam:** −0.5166 [−0.7461, −0.3859].
- **Learner vs CSF-fam:** −0.4733 [−0.6822, −0.3683].

Under the registered rule, **C4 and C5 are "not superior".** The "inferiority" label comes from the read-out code, not from amendment 11, so the paper should state the registered outcome and describe the CI** below 0 as a descriptive fact. The practical meaning: most of the v1–v4 saving is a saving against an **uninformed pooled prior** (CSF-1). When the friction class can be seen, a one-number family prior beats a noisy probe at σ 0.2.

**Per family (S4, c4; CRC-route point values, no CIs):**

| Family | D(muhat vs fam) | D(full vs fam) |
|---|---|---|
| F1 | −0.4441 | 0.1102 |
| F2 | −0.3420 | −0.1378 |
| F3 | −0.5557 | −0.6591 |
| F4 | −0.7373 | −1.218 |

- The plug-in loses to CSF-fam in all four families.
- The learner wins only in F1, where its slip (0.2014) is far above CSF-fam's (0.09286). That "win" therefore comes with much higher slip, and is not a like-for-like efficiency gain.

### 2.3 The σ band (S1, f4, unadjusted)

| σ | C1-type D(muhat vs CSF-1) | C2-type D(full vs muhat) | C3-type D(full vs CSF-1, CRC) |
|---|---|---|---|
| 0.1 | 0.6486 [0.6100, 0.6733] | −0.1076 [−0.1819, −0.02922] | 0.5683 [0.5217, 0.6374] |
| 0.2 | 0.4314 [0.3824, 0.4835] | 0.01117 [−0.05552, 0.05686] | 0.4135 [0.3578, 0.4903] |
| 0.4 | −0.2065 [−0.3280, −0.1112] | 0.3238 [0.2778, 0.3817] | 0.1675 [0.1064, 0.2560] |

- **The probe's value drops steeply as noise rises.** At σ 0.4 the plug-in is worse than CSF-1. Its test slip there is 0.1014, which is above α.
- **"The learner adds nothing" holds only at σ 0.2.**
  - At σ 0.1 the learner is worse than the plug-in. The CI** excludes 0, and p_tost is 0.5445.
  - At σ 0.4 it is clearly better, because it is robust to a noisy μ̂.
- The C2 equivalence is a property of one noise level, not a general claim. The registration already says "the σ curve is reported as the result", and the paper should follow that.

### 2.4 Shrunk plug-in (S2)
- **Against the raw plug-in:** CSF-shrunk@0.2 gives D 0.1119 (CI** [0.04864, 0.1449]; two-sided p 0.0, TOST p 0.477).
- **Against CSF-1:** D 0.4950 [0.4514, 0.5273].
- Frozen v3 OLS shrinkage therefore improves on the raw plug-in. This is secondary and unadjusted.

### 2.5 Friction-width sweep (S3, f4; prediction: D shrinks with w and is ≤ 0 near w 0.25)

| w | μ window | n_cal / n_test | D(muhat vs CSF-1) | D(full vs CSF-1) |
|---|---|---|---|---|
| 1.0 | [0.3, 1.0] | 500 / 700 | 0.4314 [0.3824, 0.4835] | 0.4377 [0.3967, 0.4761] |
| 0.75 | [0.3487, 0.8603] | 386 / 532 | 0.2414 [0.1547, 0.3059] | 0.2793 [0.2149, 0.3393] |
| 0.5 | [0.4054, 0.7401] | 262 / 361 | −0.1094 [−0.2383, 0.01393] (p 0.044) | −0.01792 [−0.1375, 0.08984] (p 0.747) |
| 0.25 | [0.4712, 0.6367] | 134 / 179 | −0.6967 [−0.9507, −0.4238] | −0.5039 [−0.8153, −0.3222] |

- **The prediction holds.** D falls monotonically with w and is clearly below 0 at w 0.25.
- **The cause is CSF-1, not the tactile arms.** CSF-1's RE falls from 0.7823 to 0.2326. The plug-in stays at roughly 0.41–0.46 RE across the whole sweep.
- **This is the same mechanism as C4/C5.** Once friction uncertainty is narrower than the probe noise, the probe is a net cost.

### 2.6 Measured no-probe break-even (S6)
The no-probe CSF-1 grasp:
- Uses λ̂ index 41 in all four strata (not at the grid edge).
- Has test slip 0.08714.
- Has mean hold force 7.125 N, the same value as rd CSF-1.

**Integrated force-time (N·s)**

| Arm | T 1 s | T 5 s | T 30 s | Break-even T |
|---|---|---|---|---|
| no-probe CSF-1 | 22.20 | 50.70 | 228.8 | — |
| full_rd@0.2#0 | 39.10 | 63.57 | 216.4 | **17.74 s** |
| CSF-muhat@0.2 | 39.47 | 65.32 | 226.9 | **27.07 s** |
| CSF-1 (rd) | 40.17 | 68.67 | 246.8 | never (null) |

- **Short holds favour skipping the probe.** For holds of 1 s and 5 s, no-probe CSF-1 uses the least force-time of any arm. Only at 30 s do full_rd and the plug-in pull ahead.
- **The measured break-even for full_rd@0.2#0 (17.74 s) sits near the v3 probe-phases estimate (16.56 s).** It is well below the v3 all-phases estimate (28.61 s). For the plug-in, the measured 27.07 s compares with the v3 values of 32.99 s (probe phases) and 57.02 s (all phases).
- **The v3 and v4 figures come from different test sets** (v3 08c split vs f4). For example, CSF-1 at T 30 s is 259.2 N·s in v3 and 246.8 N·s in v4. Treat the comparison as indicative only.
- The rd shared phases measured in v4 are preload 13.08, squeeze 12.91, rampdown 1.444, return 0.3480 and rehold 3.27 N·s.

### 2.7 Certificate check over 200 re-splits (S7, f4, seed 3031)

| Rule | Arm | Mean slip | Share > α | q90 slip | Max slip | Share with any stratum > α |
|---|---|---|---|---|---|---|
| CRC | full_rd@0.2#0 | 0.08360 | 0.095 | 0.09968 | 0.1146 | 0.7 |
| CRC | CSF-muhat@0.2 | 0.08513 | 0.08 | 0.09893 | 0.1104 | 0.645 |
| CRC | CSF-1 | 0.08670 | 0.145 | 0.1044 | 0.1271 | 0.315 |
| LTT | full_rd@0.2#0 | 0.06818 | 0.0 | 0.08 | 0.09893 | 0.16 |
| LTT | CSF-muhat@0.2 | 0.07141 | 0.0 | 0.08036 | 0.09643 | 0.07 |
| LTT | CSF-1 | 0.06929 | 0.01 | 0.08936 | 0.1093 | 0.08 |

- **CRC behaves as a marginal-in-expectation guarantee.** Mean pooled slip is below 0.10 for every arm. Individual splits exceed α in 8–14.5 % of re-splits.
- **Per-stratum exceedance is common under CRC:** 0.7, 0.645 and 0.315 of splits have at least one stratum above α. Some per-stratum shares reach 0.47 (plug-in, D1).
- **LTT is markedly more conservative:** pooled share above α is 0.0–0.01, with mean slip 0.06818–0.07141.

---

## 3. Statistical Checks

1. **Holm validity.** All five confirmatory p are reported as 0.0, meaning no bootstrap draw crossed the null (resolution 1/2,000). Even on the most conservative reading, each p is below 1/2,000, so the smallest Holm-adjusted bound is still far below 0.05. The C1–C3 decisions, and the "not superior" outcomes for C4/C5, are robust to that resolution limit.
2. **TOST and CI consistency for C2.** The 97.5 % CI** [−0.05552, 0.05686] lies inside ±0.10, which agrees with TOST p 0.0. The two-sided p of 0.915 confirms there is no detectable difference.
3. **Route sensitivity of C2.** On the CRC route (S5_C2_crc), D is −0.06291 with CI** [−0.1226, 0.08396], which crosses the −0.10 margin, and p_tost is 0.037. The equivalence claim therefore depends on the matched-slip route, which is the registered one. The paper should report this.
4. **Sign and size agree across routes.**
   - C1 is 0.4314 matched and 0.4482 on CRC.
   - C4 is −0.5814 matched and −0.5166 on CRC.
   - C5 is −0.5461 matched and −0.4733 on CRC.
   - The c4 CSF-1 contrasts match the f4 ones closely: plug-in 0.4285 vs 0.4314, learner 0.4412 vs the S3 w 1.0 value of 0.4377.
5. **p vs CI level.** At S3 w 0.5, the two-sided p of 0.044 sits next to a 97.5 % CI** that includes 0 ([−0.2383, 0.01393]). This is consistent: the 97.5 % interval matches a 2.5 % two-sided test. The row is not significant at that level and is secondary and unadjusted in any case.
6. **Calibration on the test split.** Every f4 and c4 arm has test slip ≤ 0.10 except CSF-muhat@0.4 (0.1014). This is one split, and S7 shows such exceedances are expected under CRC.
7. **Per-family slip (S4).** Most arms are badly mis-calibrated within individual families: CSF-1 F1 0.3157, full_rd F1 0.2014, plug-in F1 0.1143. Their F3/F4 slips fall as low as 0.0 for CSF-1. Only CSF-fam stays ≤ 0.09286 in every family. The per-family RE comparisons are therefore confounded by unequal slip, and the CRC guarantee is marginal over families, not conditional on family.
8. **Registered vs code labels.** C4/C5 "inferiority" is a code label outside the registered rule (see §2.2). Report it as "not superior; CI** below 0 (descriptive)".
9. **Integrity notes from the run context.**
   - The read-out code was committed before any v4 replay and run once.
   - There are 0 duplicates.
   - The pools are complete: f4 4,800, c4 4,800 cal + test, noprobe 4,800.
   - No model was re-trained.

---

## 4. Limitations

- **σ is simulated probe noise.** There is no hardware, and the conclusions change sign across σ ∈ {0.1, 0.2, 0.4} (C1-type: 0.6486 → 0.4314 → −0.2065).
- **c4 is a stylised correlated design.** It uses narrow, mostly non-overlapping family bands. The C4/C5 size depends on band width relative to σ, as the S3 sweep shows. Real material-class priors may be weaker or stronger.
- **No hybrid arm was tested.** Nothing combined the family prior with the probe (for example, a prior-centred shrinkage). C4/C5 do not show that touch is useless where a prior exists, only that a raw or learned probe estimate without that prior loses to it.
- **The guarantee is marginal.** S7 shows 31.5–70 % of CRC re-splits with at least one disturbance stratum above α. S4 shows family-level slip up to 0.3157.
- **S1–S7 are secondary and unadjusted.** S4 has no CIs, and the narrow S3 windows rest on small samples (134 cal / 179 test objects at w 0.25).
- **The S6 break-even depends on the replay.** It uses commanded profiles and a different test set from v3, so the v3/v4 comparison is indicative.
- **Not done:** the REACT-probe re-design, hardware σ, adaptive or low preload, replay-free calibration, and published-controller baselines (registered limitations).

---

## 5. Conclusion

- **Probe sufficiency is confirmed on fresh objects at σ 0.2.** All three predicted confirmatory results hold on f4:
  - C1: the plug-in beats CSF-1 by D 0.4314.
  - C2: the learner is equivalent to the plug-in, D 0.01117, CI** inside ±0.10.
  - C3: the learner beats CSF-1 by D 0.4135.
- **The saving does not survive a friction-informative prior.** On c4, CSF-fam beats the plug-in (C4, D −0.5814) and the learner (C5, D −0.5461). Under the registered rule both rows are "not superior", and both CIs** lie entirely below 0.
- **The benefit is conditional on two things.** The friction width sweep (D falls from 0.4314 to −0.6967 as w drops from 1.0 to 0.25) and the σ band (the plug-in turns negative at σ 0.4) show this. The probe pays off only when friction uncertainty exceeds probe noise.
- **The probe pays only for longer holds.** The measured break-evens against a no-probe grasp are 17.74 s for the learner and 27.07 s for the plug-in. For holds of 5 s or less, skipping the probe is cheaper.
- **The certificate is marginal, not conditional.** CRC keeps mean pooled slip below α over 200 re-splits, but individual strata and families regularly exceed it. LTT is the conservative alternative.
- **Recommended framing.** "Under friction uncertainty that a pooled prior cannot resolve, a tactile probe plus a calibrated plug-in gives a certified grip-force saving. A learner adds value only at high probe noise, and a visible-class prior dominates when friction is class-predictable."
