# p2 · Stage 14 RESULT_ANALYSIS [v2] — merged (run 44, 2026-11-10)

Pass 1 (fresh opus subagent, template verbatim): `14_analysis_v2_pass1.md`. Pass 2 (fresh opus subagent, area-chair
prompt verbatim): `14_analysis_v2_pass2.md`, 17 findings, 1 numeric (truncation of 0.0976 / 0.0936 to 0.0975 / 0.0935),
no fabricated number. **Main-session adjudication: all 17 accepted.** The pass-2 rewrites are binding where they
differ from pass 1. Statements of record for stages 15–19 (all v2 rows secondary / descriptive):

1. vs CSF-1, CertGrip-full σ 0.2 is superior on every v2 route (matched slip 0.10, LTT δ 0.10, CRC) on both the 08c
   and 08e grids; these re-use the seed-0 replays, so they are route / grid sensitivity rows, not new replication
   (the v1 per-seed rows remain the seed evidence).
2. CertGrip-full vs CSF-μ̂ (the same noisy onset probe in the physics formula): no v2 contrast shows a difference
   either way and no equivalence test was run; say "no demonstrated gain of the learned model", not "matches".
   v1 H2b (σ 0.2) was not shown; the v1 08c rows show CertGrip superior to CSF-μ̂ at σ 0.0 / 0.1 / 0.4, but on the
   08c grids CSF-μ̂ sits at grid index 0 (biased against it, 08e), so those rows are not evidence of a learned gain.
3. H5 (CSF-proxy): superiority at σ_p 0.8 and 0.4; at σ_p 0.2 the value of record is the edge-rule row
   D −0.0299 [−0.1903, 0.0816] (not shown). The registered prediction's direction held; wording "held as predicted
   (secondary)", not "confirmed". No proxy-vs-CSF-1 contrast was computed, so no claim that a poor prior is worse
   than none beyond the point RE values with their slip levels.
4. Onset-only vs CertGrip-full: no direct v2 test; v1 H4e interval [−0.1233, 0.0508] → "not distinguishable".
5. B2: with one uniform margin, per-stratum test slip is far from α in some strata at every m tested (at m 1.0,
   D1 0.0414 / D2 0.0228 are below α while D3 / D4 are far above); calibration sets stratum-specific margins.
   Descriptive.
6. B3: window slip under physical feedback stayed between 0.0936 and 0.1052 (means over 5 orderings) and D_RE
   0.41–0.44; steps 1–500 are pre-shift. Descriptive, 5 orderings, no interval; not comparable one-to-one with the
   v1 label-rule audit.

---

## Pass 1 (superseded where items 1–6 above differ)

# p2 (CertGrip) · Stage 14 [v2] analysis, pass 1

Scope: every v2 row is **secondary** under amendment 09. The v1 primary verdicts (H2a superiority, H2b not confirmed,
H3 inconclusive on S1 / S2 / S3) are quoted below and are **not re-decided**.

Number convention: every value is copied from the JSON in the prompt. Long decimals are **truncated** (not rounded) to
4 decimals, so each printed value is a prefix of the stored value. No new arithmetic (differences, ratios) is
reported. When a comparison is made, both source values are given side by side.

Common settings (from the files): α = 0.1, δ = 0.1, matched slip = 0.1, draws = 2000, n_cal_instances = 2000,
n_test_instances = 2800, CI\*\* = 97.5 % object-cluster bootstrap with λ̂ refitted inside each draw.

---

## 1. Metrics Summary

### 1.1 v1 reference read-outs (results/v1/crc_analysis.json, 08c CRC route)

| Arm | lam_idx D1/D2/D3/D4 | test slip_phys | slip_label | RE_mid | RE_mid_CI |
|---|---|---|---|---|---|
| full_rd@0.2#0 (CertGrip) | 10/10/11/10 | 0.0828 | 0.0846 | 0.4567 | [0.4079, 0.5033] |
| P_onset@0.2#0 (onset-only) | 10/10/11/10 | 0.0857 | 0.0896 | 0.4335 | [0.3982, 0.4832] |
| CSF-muhat@0.2 | 0/0/14/12 | 0.0657 | 0.0678 | 0.4842 | [0.4435, 0.5219] |
| CSF-1 | 1/1/15/14 | 0.1021 | 0.1035 | 0.7831 | [0.6967, 0.8582] |

| v1 contrast | D mid | CI\*\* mid | decision |
|---|---|---|---|
| H2a (full_rd@0.2#0 vs CSF-1) | 0.4168 | [0.3483, 0.4777] | superiority |
| H2b (full_rd@0.2#0 vs CSF-muhat@0.2) | 0.0569 | [-0.0399, 0.1453] | not confirmed |
| H4e (full_rd@0.2#0 vs P_onset@0.2#0) | -0.0534 | [-0.1233, 0.0508] | not confirmed |

v1 H3 (results/v1/h3_analysis.json): H3_primary S1 / S2 / S3 = inconclusive / inconclusive / inconclusive
(R_E S1 0.8778 [0.7404, 1.1203]; S2 1.1738 [1.0233, 1.4283]; S3 0.9629 [0.8363, 1.1449]).

### 1.2 A1 — risk–efficiency frontier, matched test slip 0.1

| Arm | RE_match 08c | CI\*\* 08c | RE_match 08e | CI\*\* 08e |
|---|---|---|---|---|
| full_rd@0.2#0 | 0.4290 | [0.4099, 0.4559] | 0.4292 | [0.4074, 0.4521] |
| P_onset@0.2#0 | 0.4153 | [0.3968, 0.4374] | 0.4173 | [0.3967, 0.4392] |
| CSF-muhat@0.2 | 0.4190 | [0.4005, 0.4410] | 0.4045 | [0.3891, 0.4369] |
| CSF-1 | 0.7890 | [0.7329, 0.8422] | 0.7769 | [0.7304, 0.8362] |

| D_match (arm vs CSF-1) | 08c D | 08c CI\*\* | 08e D | 08e CI\*\* | decision (both) |
|---|---|---|---|---|---|
| full_rd@0.2#0 | 0.4563 | [0.4095, 0.4896] | 0.4475 | [0.4110, 0.4879] | superiority |
| P_onset@0.2#0 | 0.4735 | [0.4309, 0.5041] | 0.4628 | [0.4273, 0.5013] | superiority |
| CSF-muhat@0.2 | 0.4689 | [0.4173, 0.5096] | 0.4793 | [0.4240, 0.5189] | superiority |

Selected frontier points (08c grids, test slip_phys / RE_mid):

| k | full_rd@0.2#0 | P_onset@0.2#0 | CSF-muhat@0.2 | CSF-1 |
|---|---|---|---|---|
| -4 | 0.2660 / 0.2309 | 0.2785 / 0.2113 | 0.1417 / 0.3654 | 0.1710 / 0.6036 |
| -1 | 0.12 / 0.3966 | 0.1321 / 0.3744 | 0.0778 / 0.4526 | 0.1292 / 0.7096 |
| 0 | 0.0828 / 0.4567 | 0.0857 / 0.4335 | 0.0657 / 0.4842 | 0.1021 / 0.7831 |
| +1 | 0.0567 / 0.5193 | 0.0567 / 0.4952 | 0.045 / 0.5481 | 0.0742 / 0.8598 |
| +4 | 0.0135 / 0.7239 | 0.0157 / 0.6965 | 0.0171 / 0.7565 | 0.01 / 1.1102 |

On the 08e grids the CSF-muhat@0.2 frontier at k = -4 reaches slip 0.2414 (RE 0.2399), against 0.1417 (RE 0.3654) on
the 08c grids, consistent with the 08c CSF-muhat λ̂ sitting at grid index 0 in D1 / D2 (clipping blocks k < 0 there).

### 1.3 A2 — Learn-then-Test (δ = 0.1) high-probability certificate

| Arm | 08c λ̂_LTT D1/D2/D3/D4 | 08c slip_phys | 08c RE_mid | 08e λ̂_LTT | 08e slip_phys | 08e RE_mid |
|---|---|---|---|---|---|---|
| full_rd@0.2#0 | 10/10/12/11 | 0.0696 | 0.4894 | 21/21/22/21 | 0.0707 | 0.4878 |
| P_onset@0.2#0 | 11/10/12/11 | 0.0639 | 0.4807 | 21/21/22/21 | 0.0742 | 0.4643 |
| CSF-muhat@0.2 | 0/0/15/13 | 0.0528 | 0.5172 | 20/22/22/21 | 0.0653 | 0.4857 |
| CSF-1 | 2/1/16/14 | 0.0907 | 0.8216 | 21/21/21/22 | 0.0910 | 0.8150 |

No stratum was flagged (every LTT flag is `false`).

| D_ltt (arm vs CSF-1) | 08c D | 08c CI\*\* | 08e D | 08e CI\*\* | decision (both) |
|---|---|---|---|---|---|
| full_rd@0.2#0 | 0.4042 | [0.3361, 0.4561] | 0.4014 | [0.3390, 0.4594] | superiority |
| P_onset@0.2#0 | 0.4148 | [0.3619, 0.4737] | 0.4303 | [0.3726, 0.4856] | superiority |
| CSF-muhat@0.2 | 0.3704 | [0.2952, 0.4425] | 0.4039 | [0.3111, 0.4630] | superiority |

### 1.4 A3 — extra CRC-route contrasts vs CSF-1

| D_crc (arm vs CSF-1) | 08c D | 08c CI\*\* | 08e D | 08e CI\*\* | decision (both) |
|---|---|---|---|---|---|
| full_rd@0.2#0 | 0.4168 | [0.3483, 0.4777] | 0.4289 | [0.3576, 0.4770] | superiority |
| P_onset@0.2#0 | 0.4463 | [0.3776, 0.4905] | 0.4411 | [0.3845, 0.4942] | superiority |
| CSF-muhat@0.2 | 0.3816 | [0.2965, 0.4504] | 0.4148 | [0.3321, 0.4889] | superiority |

### 1.5 B1 — H5, CertGrip-full σ 0.2 vs CSF-proxy σ_p

| Read-out | D mid | CI\*\* mid | D lo / hi | decision_09 |
|---|---|---|---|---|
| H5@0.2 (08c grid) | 0.0514 | [-0.0673, 0.1659] | 0.0510 / 0.0518 | not shown |
| H5@0.2_08e (edge rule) | -0.0299 | [-0.1903, 0.0815] | -0.0297 / -0.0301 | not shown |
| H5@0.4 | 0.5042 | [0.4361, 0.5635] | 0.5024 / 0.5061 | superiority |
| H5@0.8 | 0.8360 | [0.8136, 0.8572] | 0.8350 / 0.8370 | superiority |

| CSF-proxy arm | lam_idx | slip_phys | RE_mid | RE_mid_CI |
|---|---|---|---|---|
| σ_p 0.2 (08c) | 0/0/13/12 (grid edge D1, D2) | 0.0617 | 0.4815 | [0.4427, 0.5219] |
| σ_p 0.2 (08e edge rule) | 20/21/20/20 | 0.0825 | 0.4312 | [0.3905, 0.4758] |
| σ_p 0.4 | 1/1/15/13 | 0.0910 | 0.9212 | [0.8422, 1.0023] |
| σ_p 0.8 | 2/2/14/13 | 0.0971 | 2.7858 | [2.5273, 3.0700] |

Target in the edge-rule run (08e recipe): full_rd@0.2#0 lam_idx 20/20/21/21, slip_phys 0.09, RE_mid 0.4441
[0.4063, 0.4973]. After the edge rule no arm is at a grid edge (`grid_edge_lam_idx` empty).

### 1.6 B2 — probe + fixed margin, no calibration (test split)

| m | slip_phys | RE_mid | D1 | D2 | D3 | D4 |
|---|---|---|---|---|---|---|
| 0.0 | 0.9582 | -0.3829 | 0.9271 | 0.9128 | 0.9957 | 0.9971 |
| 0.25 | 0.8257 | -0.2286 | 0.7114 | 0.6257 | 0.9771 | 0.9885 |
| 0.5 | 0.6182 | -0.0744 | 0.3685 | 0.2657 | 0.9114 | 0.9271 |
| 1.0 | 0.335 | 0.2341 | 0.0414 | 0.0228 | 0.6571 | 0.6185 |

Calibration-split values track the test values (e.g. m = 1.0: cal slip 0.3395, RE 0.2472).

### 1.7 B3 — online OQT with physical slip feedback (5 orderings, descriptive)

| Shift / arm | window | phys. feedback slip mean [min, max] | phys. RE_mid mean | label (08d) slip mean | label RE_mid mean |
|---|---|---|---|---|---|
| S1 CertGrip | 1-500 | 0.0984 [0.092, 0.104] | 0.4273 | 0.1048 | 0.4223 |
| S1 CertGrip | 1001-2000 | 0.1002 [0.096, 0.105] | 0.4633 | 0.1008 | 0.4728 |
| S1 CertGrip | 1501-2000 | 0.1032 [0.1, 0.106] | 0.4626 | 0.1012 | 0.4722 |
| S1 CSF1 | 1-500 | 0.1052 [0.1, 0.11] | 0.7614 | 0.1096 | 0.7478 |
| S1 CSF1 | 1001-2000 | 0.1016 [0.096, 0.105] | 0.7914 | 0.1014 | 0.7946 |
| S1 CSF1 | 1501-2000 | 0.0988 [0.082, 0.11] | 0.7997 | 0.0984 | 0.8042 |
| S3 CertGrip | 1-500 | 0.0975 [0.092, 0.102] | 0.4191 | 0.1044 | 0.4150 |
| S3 CertGrip | 1001-2000 | 0.101 [0.095, 0.106] | 0.5127 | 0.1012 | 0.5145 |
| S3 CertGrip | 1501-2000 | 0.0992 [0.09, 0.112] | 0.5134 | 0.1008 | 0.5150 |
| S3 CSF1 | 1-500 | 0.1032 [0.098, 0.106] | 0.7536 | 0.1080 | 0.7418 |
| S3 CSF1 | 1001-2000 | 0.101 [0.094, 0.11] | 0.8719 | 0.1006 | 0.8796 |
| S3 CSF1 | 1501-2000 | 0.0935 [0.088, 0.1] | 0.8725 | 0.094 | 0.8801 |

D_RE = 1 − RE_CertGrip / RE_CSF1 (physical feedback): S1 0.4387 / 0.4146 / 0.4215; S3 0.4438 / 0.4119 / 0.4115
for windows 1-500 / 1001-2000 / 1501-2000.

---

## 2. Comparative Findings

1. **CertGrip vs the friction-blind baseline (CSF-1) is robust across every v2 route.** The v1 H2a superiority
   (D 0.4168, CI\*\* [0.3483, 0.4777]) is reproduced by the matched-slip frontier (0.4563 on 08c, 0.4475 on 08e), by
   the high-probability LTT certificate (0.4042 / 0.4014) and by the 08e CRC route (0.4289). Every CI\*\* lower bound
   is above 0; the smallest across all A rows is 0.2952 (D_ltt CSF-muhat, 08c).

2. **CertGrip vs friction-informed baselines: no advantage is shown, in v1 or v2.** v1 H2b was not confirmed
   (D 0.0569, CI\*\* [-0.0399, 0.1453]). In v2, at matched slip 0.1 the CSF-muhat@0.2 RE (0.4190 on 08c, 0.4045 on 08e)
   is at or below the CertGrip RE (0.4290 / 0.4292), with overlapping intervals, and D_match vs CSF-1 is 0.4689 /
   0.4793 for CSF-muhat against 0.4563 / 0.4475 for CertGrip. B1 tells the same story with a non-tactile friction
   proxy: at σ_p 0.2 the H5 contrast is not shown on either grid (0.0514, CI\*\* [-0.0673, 0.1659]; edge rule -0.0299,
   CI\*\* [-0.1903, 0.0815]). No direct matched-slip or LTT contrast CertGrip vs CSF-muhat was computed, so this is
   a reading of separate intervals, not a test.

3. **The v1 H2b point comparison mixed slip levels.** At k = 0 on the 08c grids CertGrip ran at test slip 0.0828 and
   CSF-muhat@0.2 at 0.0657 (λ̂ at grid index 0 in D1 / D2). Matching slip removes the apparent 0.0569 CertGrip edge:
   the two RE_match values are close (0.4290 vs 0.4190) with overlapping CI\*\* ([0.4099, 0.4559] vs [0.4005, 0.4410]).

4. **Onset-only matches or beats the full tactile pipeline.** v1 H4e was not confirmed (D -0.0534). In v2 the onset-only
   arm has RE_match 0.4153 / 0.4173 against 0.4290 / 0.4292 for CertGrip-full, and its D vs CSF-1 is the larger one
   on every route (D_match 0.4735 / 0.4628, D_ltt 0.4148 / 0.4303, D_crc 0.4463 / 0.4411). The extra tactile
   features beyond onset carry no measurable efficiency gain here.

5. **H5 prediction confirmed in direction.** Registered prediction: superiority at σ_p 0.8, margin shrinking as σ_p
   falls. Observed D: 0.8360 (σ_p 0.8) → 0.5042 (σ_p 0.4) → 0.0514 (σ_p 0.2). The CI\*\* first includes 0 at
   **σ_p 0.2**, on both the 08c grid and the edge-rule grid. Note that the σ_p 0.4 proxy (RE 0.9212) and σ_p 0.8 proxy
   (RE 2.7858) are less efficient than CSF-1 itself (RE 0.7831): a poor friction prior is worse than none.

6. **Cost of the high-probability certificate is modest.** Moving CertGrip from CRC (slip 0.0828, RE 0.4567) to LTT
   (slip 0.0696, RE 0.4894) lowers test slip and raises force; D vs CSF-1 goes from 0.4168 to 0.4042 and stays
   superiority.

7. **Calibration is necessary (B2).** No fixed margin brings all strata to α = 0.1: at m = 1.0 overall slip is 0.335,
   with D1 / D2 already below α (0.0414 / 0.0228) while D3 / D4 stay at 0.6571 / 0.6185. For m ≤ 0.5 RE is negative
   (-0.3829, -0.2286, -0.0744), i.e. under-gripping. Calibrated arms reach slip 0.0828 at RE 0.4567 (CertGrip CRC).

8. **Online physical feedback holds slip near α (B3).** Window slip means under physical feedback lie between 0.0935
   and 0.1052 for both arms and both shifts; per-ordering values span 0.082 to 0.112. Physical and label-rule
   feedback give close values (e.g. S1 CertGrip 1001-2000: 0.1002 vs 0.1008 slip, 0.4633 vs 0.4728 RE), in line
   with the v1 audit, where slip_direct and slip_label differ by Delta between -0.008 and 0.0. CertGrip keeps a
   D_RE vs CSF1 of 0.4115 to 0.4438 in every window. This is the online analogue of H2a, not a test of v1 H3, which
   used a different read-out (R_E, 20 orderings).

---

## 3. Statistical Checks

- **Reproduction / internal consistency (pass).** D_crc:full_rd@0.2#0 on 08c (0.4168210498118554, CI\*\*
  [0.3483925859894733, 0.4777919839082863]) equals v1 H2a exactly. The B1 file's full_rd@0.2#0 arm equals the v1 arm
  (lam_idx 10/10/11/10, slip_phys 0.08285714285714285, RE_mid 0.4567326634839066). Frontier k = 0 points equal the
  CRC arms for all four arms on 08c. On 08e the full_rd k = 0 point (slip 0.09, RE 0.44415834262450105) equals the
  full_rd arm of b_analysis_edge.json.
- **Bootstrap validity.** Every A-part CI\*\* has n_valid = 2000 of 2000 draws, so the matched-slip interpolation
  never failed inside a draw.
- **lo / hi sensitivity (F\* bounds).** For every H5 row the lo and hi D values bracket mid closely
  (e.g. H5@0.4: lo 0.5024 / mid 0.5042 / hi 0.5061), and the lo and hi CI\*\* give the same decision as mid.
- **Grid edges.** CSF-muhat@0.2 on 08c has λ̂ index 0 in D1 / D2 (CRC and LTT); its 08c frontier is clipped for k < 0,
  so the 08e rows are the fair ones for that arm. CSF-proxy@0.2 hit index 0 in D1 / D2 and was re-run under the
  registered edge rule; afterwards no edge remains. `at_max` is false for every stratum of every arm.
- **Risk control at the operating point.** CRC test slip: CertGrip 0.0828, onset-only 0.0857, CSF-muhat 0.0657,
  CSF-1 0.1021 (slightly above α = 0.1; label slip 0.1035). LTT test slip: 0.0696 / 0.0639 / 0.0528 / 0.0907 on 08c,
  all ≤ α.
- **Multiplicity.** All v2 rows are secondary; no correction across the A, B1 rows was registered, and the 97.5 %
  intervals are the only error control. Read the decisions as descriptive support, not as new confirmatory claims.
- **B3** has no registered interval or test; only means and min / max over 5 orderings are reported.

---

## 4. Limitations

- Simulation only (MuJoCo 4.0.0); the onset-noise σ is not grounded on hardware (amendment C).
- All v2 results are secondary; they cannot overturn v1 H2b (not confirmed) or v1 H3 (inconclusive).
- No direct CertGrip vs CSF-muhat contrast at matched slip or under LTT was registered or computed; the "no tactile
  advantage" reading rests on overlapping separate intervals plus v1 H2b and H5@0.2.
- Matched slip uses one target (0.1) by linear interpolation between adjacent k; shape of the frontier away from that
  point is only described.
- CSF-proxy is an oracle-side construction (uses true μ through a noisy proxy), so H5 calibrates "how good a friction
  prior must be" rather than comparing against a deployable estimator.
- LTT guarantees hold per stratum at δ = 0.1, not family-wise across strata.
- B2 is one replay per instance per margin, with no interval.
- B3: 5 orderings (v1 H3 used 20), S1 and S3 only, no interval; window slip ranges overlap α, so "holds α" is a
  descriptive statement.
- 08c and 08e grids give slightly different point values (e.g. CSF-muhat RE_match 0.4190 vs 0.4045); conclusions are
  stated only where both agree.

---

## 5. Conclusion

- The efficiency gain of calibrated tactile grip selection over a friction-blind CSF-1 is robust: superiority on the
  CRC, matched-slip and LTT routes, on both grid recipes (D from 0.4014 to 0.4563 for CertGrip-full).
- The gain is not specific to tactile sensing: a friction estimate of σ 0.2 quality (CSF-muhat, or the non-tactile
  CSF-proxy at σ_p 0.2) matches CertGrip at matched slip (RE 0.4190 vs 0.4290) and H5@0.2 is not shown
  (CI\*\* [-0.0673, 0.1659]; edge rule [-0.1903, 0.0815]). CertGrip is superior only to proxies of σ_p 0.4 or worse
  (D 0.5042, 0.8360).
- Onset-only is as efficient as the full pipeline (RE_match 0.4153 vs 0.4290).
- Calibration itself is what delivers per-stratum risk control: fixed margins miss α in every stratum
  (B2), while CRC / LTT and the online physical-feedback tracker keep slip near 0.1.
- Recommended framing for the paper: CertGrip as a calibration layer that turns any friction signal (tactile onset
  included) into a slip-rate guarantee, not as evidence that tactile features beat a good friction prior.


---

## Pass 2 audit (binding)

# p2 (CertGrip) · Stage 14 [v2] analysis, pass 2: area-chair audit of pass 1

Source checked: `results/14_analysis_v2_pass1.md`, against the JSON and amendment 09 in
`docs/prompts/stage14_v2_user.txt` (v1 `crc_analysis.json`, `h3_analysis.json`; v2 `a_analysis.json`,
`a_analysis_08e.json`, `b_analysis.json`, `b_analysis_edge.json`, `b3_analysis.json`; `docs/09_amendment_v2.md`;
B3 plan).

## Number audit (summary)

I checked every table cell and every number in the text against the JSON. Every value is a correct 4-decimal
truncation of the stored value, with two exceptions caused by floating-point artifacts (finding 16). No value is
mistranscribed. The problems are in interpretation: claims that go beyond the numbers, routes reported selectively,
and secondary or descriptive rows described in confirmatory language.

## Findings

Ordered by severity. Each finding gives (a) the unsupported claim, (b) the contradicting or missing evidence, and
(c) a rewrite that the numbers support.

### 1. Section 5, bullet 2: "The gain is not specific to tactile sensing: a friction estimate of σ 0.2 quality (CSF-muhat, or the non-tactile CSF-proxy at σ_p 0.2) matches CertGrip"
- **Evidence.** The files never describe CSF-muhat as non-tactile. It is indexed by the onset-noise σ, which is the tactile
  noise parameter shared with CertGrip ("CSF-μ̂ σ 0.2"), and amendment B2 calls its force the "Probe" force. Only CSF-proxy
  is described as non-tactile. Also, "σ 0.2 quality" treats two different noise models as one scale: σ is onset-detection
  noise, while σ_p is the log-normal noise on μ̃ = clip(μ·exp(σ_p ε_p), 0.1, 3.0). For the non-tactile arm, the only
  evidence is H5@0.2 = not shown (registered edge-rule row D −0.0299, CI\*\* [−0.1903, 0.0815]). That is a failure to show
  a difference. It does not show that the two arms are equivalent.
- **Rewrite.** "Against a non-tactile friction proxy with σ_p 0.2, CertGrip shows no efficiency advantage (H5@0.2, edge
  rule: D −0.0299, CI\*\* [−0.1903, 0.0815], not shown). No equivalence test was registered, so this does not establish that
  the two are equally efficient."

### 2. Section 2.2: "CertGrip vs friction-informed baselines: no advantage is shown, in v1 or v2"
- **Evidence.** v1 does show an advantage over CSF-muhat at the other σ levels. In `crc_analysis.json`, H2b_sigma@0.0 has
  D 0.2460, CI\*\* [0.1617, 0.2952]; H2b_sigma@0.1 has D 0.1071, CI\*\* [0.0333, 0.1919]; and H2b_sigma@0.4 has D 0.3181,
  CI\*\* [0.2286, 0.4059]. All three are labelled superiority. Only σ 0.2 (the primary row, plus per-seed rows 1–4) is
  not confirmed.
- **Rewrite.** "At onset noise σ 0.2, v1 H2b was not confirmed (D 0.0569, CI\*\* [−0.0399, 0.1453]) and no v2 row shows
  a CertGrip advantage over CSF-muhat@0.2. v1 did label CertGrip superior to CSF-muhat at the same σ for σ 0.0, 0.1
  and 0.4 (σ-curve rows)."

### 3. Section 2.2 and Section 5, bullet 2: the CertGrip vs CSF-muhat reading cites only the matched-slip route
- **Evidence.** On the other two A routes, the point values favour CertGrip:
  - LTT 08c: RE 0.4894 for CertGrip vs 0.5172 for CSF-muhat; D_ltt 0.4042 vs 0.3704.
  - LTT 08e: RE 0.4878 vs 0.4857 (about level).
  - CRC: D_crc 0.4168 / 0.4289 for CertGrip vs 0.3816 / 0.4148 for CSF-muhat.

  Section 2.2 leaves all of these out, and they weaken "matches / at or below".
- **Rewrite.** "CSF-muhat@0.2's D vs CSF-1 is larger than CertGrip's on the matched-slip route (0.4689 / 0.4793 vs 0.4563 /
  0.4475) but smaller on the LTT (0.3704 / 0.4039 vs 0.4042 / 0.4014) and CRC (0.3816 / 0.4148 vs 0.4168 / 0.4289)
  routes. No direct contrast was computed, so the ordering is unresolved."

### 4. Section 5, bullet 2: "CSF-muhat ... matches CertGrip at matched slip (RE 0.4190 vs 0.4290)"
- **Evidence.** "Matches" is a claim of equivalence, but no equivalence margin or test was registered. No paired CertGrip
  vs CSF-muhat contrast at matched slip was computed (pass 1, Section 4, says so itself). Overlapping marginal intervals
  of paired arms say little about their difference. The value also comes from the 08c grid, which pass 1 and the run
  context both call unfair for CSF-muhat.
- **Rewrite.** "At matched slip 0.1 the CSF-muhat@0.2 RE (08e 0.4045, CI\*\* [0.3891, 0.4369]) and the CertGrip RE (08e
  0.4292, CI\*\* [0.4074, 0.4521]) have overlapping intervals. No direct contrast was computed."

### 5. Section 2.3: "Matching slip removes the apparent 0.0569 CertGrip edge"
- **Evidence.** There are three problems:
  - (a) v1 never showed an edge. H2b CI\*\* [−0.0399, 0.1453] already contains 0, so there was nothing for matching to
    remove.
  - (b) The support is 08c-only (0.4290 vs 0.4190). For CSF-muhat, the 08c matched point falls between k = −3 (slip
    0.1192) and k = −2 (slip 0.0975). That is exactly the region where D1 and D2 are clipped at grid index 0, which pass 1
    itself says makes the 08e rows the fair ones.
  - (c) No matched contrast or interval exists for this pair.
- **Rewrite.** "The v1 H2b point comparison was made at different test slips (CertGrip 0.0828, CSF-muhat@0.2 0.0657).
  At matched slip 0.1 on the fair 08e grids, the CSF-muhat RE (0.4045) is below the CertGrip RE (0.4292) with overlapping
  CI\*\*, which is consistent with the v1 not-confirmed verdict."

### 6. Section 4, last bullet: "conclusions are stated only where both [08c and 08e] agree"
- **Evidence.** This rule is broken in three places:
  - Section 2.3 uses 08c values only.
  - Section 5, bullet 2 quotes 08c RE_match only (0.4190 vs 0.4290).
  - Section 2.5 builds the H5 sequence on the 08c σ_p 0.2 row (D +0.0514), while the edge-rule row has the opposite sign
    (−0.0299).
- **Rewrite.** "08c and 08e give slightly different point values (e.g. CSF-muhat RE_match 0.4190 vs 0.4045). For
  CSF-muhat and CSF-proxy@0.2, which sit at a grid edge on 08c, only the 08e / edge-rule values are used."

### 7. Section 2.5: "H5 prediction confirmed in direction. Observed D: 0.8360 → 0.5042 → 0.0514 (σ_p 0.2)"
- **Evidence.** Amendment B1 says that when a stratum's λ̂ lands on grid index 0 or 19, the 08e recipe "is used for that
  arm". CSF-proxy@0.2 hit index 0 in D1 and D2, so the registered σ_p 0.2 read-out is H5@0.2_08e: D −0.0299, CI\*\*
  [−0.1903, 0.0815]. The 08c value 0.0514 is superseded. "Confirmed" is confirmatory language for a row that amendment 09
  makes secondary, which pass 1, Section 3, Multiplicity, also says. The same applies to "CertGrip is superior only to
  proxies of σ_p 0.4 or worse" (Section 5): "or worse" extrapolates beyond the largest σ_p tested (0.8).
- **Rewrite.** "Consistent with the registered (secondary) prediction, D falls from 0.8360 (σ_p 0.8) to 0.5042 (σ_p
  0.4) to −0.0299 (σ_p 0.2, edge-rule grid). The CI\*\* first includes 0 at σ_p 0.2."

### 8. Section 2.5: "the σ_p 0.4 proxy (RE 0.9212) and σ_p 0.8 proxy (RE 2.7858) are less efficient than CSF-1 itself (RE 0.7831): a poor friction prior is worse than none"
- **Evidence.**
  - No proxy-vs-CSF-1 contrast was registered or computed.
  - At σ_p 0.4 the RE_mid_CI [0.8422, 1.0023] overlaps CSF-1's [0.6967, 0.8582].
  - The arms run at different test slips (0.0910 / 0.0971 vs 0.1021). Pass 1 itself (Section 2.3) flags this mixed-slip
    confound.
  - Only σ_p 0.8 is clearly separated ([2.5273, 3.0700]).
- **Rewrite.** "The σ_p 0.8 proxy has a much higher RE than CSF-1 (2.7858, CI [2.5273, 3.0700] vs 0.7831, CI [0.6967,
  0.8582]). The σ_p 0.4 proxy's RE (0.9212) has an interval that overlaps CSF-1's. Neither comparison was a registered
  contrast."

### 9. Section 2.4 and Section 5, bullet 3: "Onset-only matches or beats the full tactile pipeline"; "The extra tactile features beyond onset carry no measurable efficiency gain"; "Onset-only is as efficient as the full pipeline"
- **Evidence.** The only direct test is v1 H4e, which was not confirmed (D −0.0534, CI\*\* [−0.1233, 0.0508]). An interval
  that wide rules out neither "beats" nor a CertGrip advantage of up to 0.0508. The v2 statements come from comparing
  separate D-vs-CSF-1 point values. No v2 onset-only vs full contrast exists, and there is no equivalence test.
- **Rewrite.** "No efficiency advantage of the full pipeline over onset-only is shown. v1 H4e was not confirmed (D −0.0534,
  CI\*\* [−0.1233, 0.0508]), and onset-only's point D vs CSF-1 is the larger one on all six v2 route × grid rows (e.g.
  D_match 0.4735 vs 0.4563)."

### 10. Section 2.1: "CertGrip vs ... CSF-1 is robust across every v2 route. The v1 H2a superiority ... is reproduced by ..."
- **Evidence.** The 08c D_crc (0.4168210498118554) is the same calculation as v1 H2a. It is an internal-consistency check,
  not a reproduction. All v2 A routes re-analyse the same seed-0 replays and the same test split, so they show robustness
  to the analysis route, not replication. The A rows are secondary. The only independent replication available is the v1
  per-seed H2a rows: seeds 1–4 give D 0.4343, 0.4196, 0.3932 and 0.4493, all superiority. Pass 1 does not cite them.
- **Rewrite.** "Across the CRC, matched-slip and LTT routes on both grid recipes (secondary), D(CertGrip vs CSF-1) ranges
  from 0.4014 to 0.4563, with every CI\*\* lower bound above 0 (smallest 0.3361, D_ltt 08c). These rows re-analyse the v1
  seed-0 replays and so show route robustness, not new replication."

### 11. Section 5, bullet 4: "Calibration itself is what delivers per-stratum risk control: fixed margins miss α in every stratum (B2), while CRC / LTT and the online physical-feedback tracker keep slip near 0.1"
- **Evidence.**
  - "Every stratum" is contradicted by B2 at m = 1.0, where D1 is 0.0414 and D2 is 0.0228, both ≤ α. Pass 1's own Section
    2.7 says so.
  - No per-stratum test slip is reported for any CRC or LTT arm, or for B3: the JSON gives only overall `slip_phys` and
    window means. Per-stratum control by the calibrated arms is therefore not shown by any cited number.
  - The LTT per-stratum statement is a design guarantee, not an observed result.
- **Rewrite.** "None of the four uniform margins tested brings every stratum near α. At m = 1.0, D1 and D2 are
  over-protected (0.0414 / 0.0228) while D3 and D4 remain at 0.6571 / 0.6185. The calibrated CertGrip arm reaches
  overall test slip 0.0828 (CRC) and 0.0696 (LTT)."

### 12. Section 2.7: "Calibration is necessary (B2). No fixed margin brings all strata to α"
- **Evidence.** B2 tests one uniform margin on one base force (f_nom_muhat) at four values (0, 0.25, 0.5, 1.0). It says
  nothing about per-stratum hand-set margins or about other values of m. The amendment registers B2 as "Descriptive".
- **Rewrite.** "Within B2 (a single uniform margin m ∈ {0, 0.25, 0.5, 1.0} on the CSF-μ̂ force), no margin brings all
  four strata near α. m ≤ 0.5 under-grips (RE −0.3829, −0.2286, −0.0744), and m = 1.0 leaves overall slip at 0.335."

### 13. Section 2.8: physical vs label feedback are "in line with the v1 audit, where slip_direct and slip_label differ by Delta between −0.008 and 0.0"
- **Evidence.** The two comparisons measure different things:
  - The v1 audit compares the physical and label slip of the same forces in one stream.
  - B3 compares two different trackers, each fed a different signal (physical feedback vs the 08d label-rule OQT with its
    own offline q̂ start).

  The agreement of one does not follow from the other. One audit Delta also has an interval that excludes 0: S2
  OQT-CertGrip 1001-2000, Delta −0.008, CI\*\* [−0.0149, −0.0028].
- **Rewrite.** "Physical- and label-feedback trackers give close window means (e.g. S1 CertGrip 1001-2000: slip 0.1002 vs
  0.1008, RE 0.4633 vs 0.4728; 5 orderings, no interval)."

### 14. Section 2.8: "Online physical feedback holds slip near α ... for both arms and both shifts"
- **Evidence.** Under the B3 plan, the stream is T = 2,000, with 500 id steps followed by 1,500 shifted steps. The 1-500
  window is therefore the pre-shift in-distribution segment, and only 1001-2000 and 1501-2000 measure behaviour under
  shift. "Holds α" has no registered tolerance, test or interval, and it rests on 5 orderings.
- **Rewrite.** "In the shifted windows (1001-2000, 1501-2000), mean physical slip over 5 orderings lies between 0.0936 and
  0.1032 for both arms on S1 and S3 (per-ordering 0.082–0.112). This is descriptive; no interval was registered."

### 15. Section 2.6: "Cost of the high-probability certificate is modest"
- **Evidence.** "Modest" is a judgement. No CRC-vs-LTT contrast or interval was computed, and the LTT RE has no CI in
  the JSON.
- **Rewrite.** "Moving CertGrip from CRC to LTT lowers test slip from 0.0828 to 0.0696 and raises RE_mid from 0.4567 to
  0.4894. D vs CSF-1 goes from 0.4168 to 0.4042 and stays superiority (secondary)."

### 16. Sections 1.7 and 2.8, numeric: "0.0975" (S3 CertGrip 1-500) and "0.0935" (S3 CSF1 1501-2000; also the lower end of the Section 2.8 range)
- **Evidence.** The stored values are 0.09759999999999999 and 0.09359999999999999. These are floating-point
  representations of 0.0976 and 0.0936: means of 5 values recorded to 3 decimals, e.g. (0.098 + 0.1 + 0.092 + 0.088 +
  0.09) / 5 = 0.0936. Truncating the float understates both values by 0.0001. The other float-artifact values
  (0.09880000000000001 → 0.0988, 0.10800000000000001 → 0.1080, 0.09840000000000002 → 0.0984) are not affected.
- **Rewrite.** "S3 CertGrip 1-500 physical slip mean 0.0976; S3 CSF1 1501-2000 0.0936; window means lie between 0.0936
  and 0.1052."

### 17. Section 3, Grid edges: "`at_max` is false for every stratum of every arm"
- **Evidence.** `at_max` appears only in v1 `crc_analysis.json` and the B1 files. The A-part files (frontier and LTT arms,
  08c and 08e) have no `at_max` field. They carry only the LTT flag, which is `false` everywhere and is a different
  property. So the claim cannot be checked for the A arms.
- **Rewrite.** "`at_max` is false for every stratum of every arm in the v1 CRC and B1 files. Every LTT flag in the A files
  is false."

## Secondary / descriptive vs confirmatory: summary

Pass 1, Section 3 correctly says that all v2 rows are secondary and should be read as descriptive support. Sections 2
and 5 then use confirmatory language that conflicts with this:
- "robust" (finding 10);
- "confirmed" (finding 7);
- "superior only to" (finding 7);
- "necessary" (finding 12);
- "matches" and "as efficient" (findings 4 and 9).

B2 and B3 are registered as descriptive, with no test. Every claim built on them (findings 11–14) should be worded
descriptively.
