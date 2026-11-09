# p2 (CertGrip) v1 — Stage 14 result analysis, pass 2 (area-chair audit of pass 1)

Role: top-conference area chair. Source checked: `14_analysis_pass1.md` against `results/v1/*.json` (excluding
`crc_grids*.json`, `13_freeze.json`) and addenda 08a–08h. No new analysis was run. The only arithmetic is on numbers
already in the files (CI widths, rank order, counts). Findings are ordered by severity: violations of a
pre-registered rule or status come first, then unsupported or wrong numbers, then wording.

---

## Findings

### A. Pre-registration, status and decision-rule violations

1. **H2-M is used for the friction story, which 08a/08b forbid.**
   - *Claim (§2.2 "The gain is a friction-information effect"; §5):* "H2-M (no mass) leaves D unchanged … mass and
     family identity do not explain it (H2-M, H4b)."
   - *Evidence:* 08a item 8 and 08b §6 both say: "H2-M (no mass) reported but not used for the friction story (onset
     confounds m and μ)". F_onset depends on m/μ jointly, so a no-mass model can recover mass from the onset feature.
     The no-mass contrast is also against P_nomass, not CSF-1 (`sec08f_label.json`). In addition, "unchanged" has no
     registered equivalence margin. The change is 0.0042 with CI\*\* [−0.0446, 0.0399].
   - *Supported rewrite:* "H2-M is reported descriptively (D_nm = 0.4598 vs P without mass, change from the with-mass
     contrast 0.0042, CI\*\* [−0.0446, 0.0399]). As pre-registered, it is not used to argue about friction vs mass,
     because the onset feature confounds m and μ."

2. **S1m is labelled "non-inferior" although the H3 matched-rate co-requirement is not met (or not assessed) there.**
   - *Claim (§1.2 table, S1m row):* "R_E 0.8871 [0.7723, 1.0265], 'non-inferior'".
   - *Evidence:* The 08d §4 rule needs both CI\*\* upper < 1.10 and matched slip rates (point difference ≤ 0.02).
     `h3_analysis.json` S1m `matched_label_window_diff` = 0.0248 (> 0.02). There is no physical audit (b) for S1m:
     the matched-physical entries exist only for S1, S2 and S3. The "non-inferior" label checks the R_E bound only.
     ID passes both (0.0098).
   - *Supported rewrite:* "S1m (not primary): R_E 0.8871, CI\*\* [0.7723, 1.0265] (upper < 1.10), but the label-rule
     window slip rates differ by 0.025 (> 0.02), so the full H3 criterion is not met for S1m."

3. **UT3 "160 / 160 cells pass" counts 20 degenerate cells as passes.**
   - *Claim (§1.3, §3.4):* "160 / 160 cells pass".
   - *Evidence:* In `sec08f_ut3.json`, all 20 cells with α 0.01 and n 50 have mean_miss = 0.0 and SD = 0. At n = 50,
     α = 0.01 the conformal quantile is unbounded, the force is F_max and nothing slips. The lower band limit is
     negative (e.g. −0.0096), so these cells pass by construction and test nothing.
   - *Supported rewrite:* "All 160 cells pass. 20 of them (α 0.01, n 50) are degenerate (q̂ = ∞, miss 0), so the
     informative result is 140 / 140. The worst cell is CSF-1, D3, α 0.01, n 500: mean miss 0.01034 in
     [0.00734, 0.01066]."

4. **H3-L, a pre-registered secondary decision, is not run, yet its conclusion is stated informally.**
   - *Claim (§2.2 online adaptation):* "OQT-CertGrip keeps its RE advantage over OQT-COMP in each shift … (no formal
     H3-L decision appears in the files)."
   - *Evidence:* 08a item 7 and 08b §6 pre-register H3-L with a two-sided TOST for the probe arm.
     `h3_analysis.json` reports only ρ and ρ − ρ_ID with CI\*\* (S1 [−0.044, 0.186], S2 [−0.058, 0.188],
     S3 [−0.025, 0.191], S1m [−0.144, 0.081]) and no decision. Under any plausible TOST margin, CIs this wide
     (≈ 0.23 units) could not establish "preserved". "Keeps its advantage" is therefore the H3-L claim stated without
     the H3-L test.
   - *Supported rewrite:* "OQT-CertGrip has lower window RE than OQT-COMP in every shift (e.g. S1 0.4763 vs 0.8087).
     The pre-registered H3-L TOST was not computed. ρ − ρ_ID CIs include 0 but are wide (up to ≈ 0.19), so
     preservation of the advantage is not shown. This omission goes in the deviation list."

5. **The H1c status is ambiguous; under the 08h rule the result is "not confirmed".**
   - *Claim (§1.3, §3.5):* "partly confirmed / not confirmed" and "Conformal calibration measurably matters".
   - *Evidence:* The 08h §1 rule has two outcomes. Confirmation needs RAW-Q and RAW-G to "miss" (CI\*\* of
     slip − α excludes ±0.025 at α 0.05). Failure needs all three CIs inside ±0.25α at every α. `sec08h_h1c.json`:
     `miss_at_0.05` is false for both, and the failure rule is not met. So neither branch fires, and there is no
     "partly confirmed" state. "Measurably matters" is stronger than the registered criterion allows.
   - *Supported rewrite:* "H1c is not confirmed (inconclusive under 08h). RAW-Q and RAW-G over-slip at every α
     (slip − α 0.0096–0.0507, every CI\*\* > 0), but at α 0.05 their CIs ([0.020, 0.045], [0.016, 0.042]) do not
     exclude +0.025, as the registered miss criterion requires."

6. **The H2b σ-curve paragraph treats the post hoc route as an "unbiased" decision route and claims a tie.**
   - *Claim (§2.2 "Learned vs plug-in by σ"):* "on the two unbiased routes the plug-in wins at σ 0 (inferiority) and
     at σ 0.1 …, the two tie at σ 0.2, and the learned arm wins at σ 0.4 (D 0.3275–0.3315; CSF-μ̂ RE
     0.9371–0.9876)."
   - *Evidence:*
     - "Unbiased" is not established anywhere. 08e only documents the 08c grid-floor defect. The 08e route is post
       hoc, and under its own rule (08e) it cannot by itself support a decision.
     - σ 0.2 is not a tie: the label route gives equivalence, but 08e gives "not confirmed" (upper 0.1001).
     - σ 0.1: inferiority holds on the label route only (08e: not confirmed, CI [−0.1911, 0.0218]).
     - The CSF-μ̂ σ 0.4 RE range mixes in the 08c value (0.9876), which comes from the route the sentence excludes.
       The label and 08e values are 0.9371 and 0.9763.
   - *Supported rewrite:* "Secondary label route: plug-in better at σ 0 (D −0.2022) and σ 0.1 (D −0.0753, inferiority),
     equivalent at σ 0.2, learned arm better at σ 0.4 (D 0.3275). The post hoc 08e grids agree in direction (σ 0
     inferiority, σ 0.1 and σ 0.2 not confirmed, σ 0.4 superiority, D 0.3315). CSF-μ̂ σ 0.4 RE is 0.9371 (label) and
     0.9763 (08e). The 08c σ 0 and σ 0.1 superiority results are unreliable under 08e."

7. **H2-T is labelled "primary".**
   - *Claim (§1.3 table):* "H2-T (CRC 08c route, primary)".
   - *Evidence:* 08f §1 calls H2-T secondary, and "primary" there refers only to the route
     (`sec08f_tail.json` `primary_route: crc_08c`).
   - *Supported rewrite:* "H2-T (secondary; on the 08c CRC route) T = 0.5918, CI\*\* [0.5540, 0.6564], pass."

### B. Wrong or unsupported numbers

8. **The label-route H2a seed range is wrong.**
   - *Claim (§2.1.1):* "seeds 1–4 … label route 0.4245–0.4442".
   - *Evidence:* `h2_label_rule.json`: seed 1 0.4245, seed 2 0.4442, **seed 3 0.4145**, seed 4 0.4275.
   - *Supported rewrite:* "label route, seeds 1–4: 0.4145–0.4442, all superiority."

9. **The claim that "the power projection was accurate" is not supported for the SE.**
   - *Claim (§2.1.1):* "The pre-registered power projection (D ≈ 0.43, SE ≈ 0.040) was accurate."
   - *Evidence:* The point estimate is close (0.4168 vs 0.43). The CI\*\* [0.3484, 0.4778] implies
     SE ≈ 0.129 / (2 × 2.24) ≈ 0.029, well below 0.040. That projection also predates the 08b §5 move of 50 objects
     per family to test.
   - *Supported rewrite:* "The point estimate (0.4168) is close to the projected D ≈ 0.43. The realised CI\*\* is
     narrower than projected (implied SE ≈ 0.029 vs 0.040)."

10. **The realised H3 CIs are wider than the pre-registered half-width the analysis cites.**
    - *Claim (§2.1.4):* "inconclusive in all three shifts, as pre-registered (08b §5: reduced power, half-width
      ≈ 0.12)."
    - *Evidence:* `h3_analysis.json` CI\*\* half-widths are S1 (1.1204 − 0.7404)/2 = 0.190, S2 0.202 and S3 0.154,
      all well above 0.12.
    - *Supported rewrite:* "Inconclusive in all three shifts, as 08b §5 expected. Realised CI\*\* half-widths
      (0.15–0.20) are wider than the projected ≈ 0.12."

11. **The H2-H claim that "D3 cells have the smallest D" is not strictly true.**
    - *Claim (§3.8):* "D3 cells have the smallest D (0.2979–0.3868)".
    - *Evidence:* `sec08g.json`: F1D4 = 0.3753 < F2D3 = 0.3868. The four smallest cells are F1D3 0.2979,
      F3D3 0.3115, F4D3 0.3348 and F1D4 0.3753.
    - *Supported rewrite:* "Three of the four smallest cell D are D3 cells (F1D3 0.2979, F3D3 0.3115, F4D3 0.3348);
      every cell has CI\*\* lower > 0.16."

12. **"RAW-Qv also over-slips" is not supported.**
    - *Claim (§3.5):* "RAW-Qv also over-slips but its CIs include 0."
    - *Evidence:* RAW-Qv slip − α is positive at every α (0.0029–0.0396), but every CI\*\* includes 0
      (e.g. α 0.05 [−0.0089, 0.0464]).
    - *Supported rewrite:* "RAW-Qv point estimates are above α (by 0.003–0.040), but no CI\*\* excludes 0."

13. **The size of the H2b equivalence miss is misstated, and the CI is called "D".**
    - *Claim (§2.1.2):* "equivalence missed by the third decimal" and "a secondary route and a post hoc route place D
      within or just at ±0.10".
    - *Evidence:* The 08e upper limit is 0.100118, a miss of 0.00012, which is at the fourth decimal (§4 correctly
      says 0.0001). It is the CI\*\*, not D, that lies within or at ±0.10. The D values are 0.0134 and 0.0240.
    - *Supported rewrite:* "The post hoc grid gives D 0.0240 with CI\*\* upper 0.1001, missing equivalence by 0.0001.
      The label-route CI\*\* [−0.0850, 0.0814] lies inside ±0.10."

14. **The seed RE range is misrounded.**
    - *Claim (§3.7):* "CertGrip-full σ0.2 RE 0.4312–0.4752 over seeds 0–4".
    - *Evidence:* The seed 4 RE_mid is 0.431255, which rounds to 0.4313 (`crc_analysis.json`).
    - *Supported rewrite:* "RE 0.4313–0.4752 over seeds 0–4."

15. **The mass-noise comparator is misnamed, and the source of the change is not stated.**
    - *Claim (§1.3):* "D_mn vs COMP_mn (= CSF-1)"; §2.2 says D is unchanged by 10 % mass noise.
    - *Evidence:* COMP_mn is CSF-1 re-run with noisy mass (RE 0.7991 vs 0.7469 noise-free). CertGrip moves only from
      0.4264 to 0.4312 (`sec08h_massnoise.json`). The +0.0312 change (CI [−0.0077, 0.0707]) comes almost entirely
      from the comparator getting worse. With no equivalence margin, "unchanged" is not established.
    - *Supported rewrite:* "With 10 % mass noise, D_mn = 0.4603 [0.4106, 0.5050] against CSF-1-with-noisy-mass
      (RE 0.7991). The change from the noise-free D is +0.0312, CI [−0.0077, 0.0707], driven by the comparator's RE."

16. **A number cannot be verified from the allowed sources.**
    - *Claim (§3.9):* "0 / 194 logs with NaN / Inf / RuntimeWarning".
    - *Evidence:* No permitted JSON or addendum contains this count (it would come from `results/v1/logs/`, which
      this audit was not allowed to read).
    - *Supported rewrite:* "No capped stream steps (`capped_window` = 0 everywhere). The log-health count is to be
      cited from its own source file."

### C. Interpretation presented as finding

17. **"Static touch and the squeeze add nothing" is stated as an established result.**
    - *Claim (§2.2 bullet 1, §5):* "squeeze adds nothing … Static touch and the squeeze add nothing (H4a, H4c, H4e)."
    - *Evidence:*
      - H4a squeeze step: D −0.0263, CI\*\* [−0.0558, 0.0149]. Equivalence (±0.03) is not confirmed, and the point
        estimate favours dropping the squeeze.
      - H4c is inconclusive (CI\*\* [−0.0526, 0.0085]).
      - H4e is "not confirmed" on its designated CRC route; equivalence holds only on the label route.
      - Only S vs P shows equivalence (±0.05).
    - *Supported rewrite:* "Static touch is equivalent to P within ±0.05 (H4a, D −0.0084). There is no evidence that
      the squeeze helps (D −0.0263, equivalence within ±0.03 not shown). Adding touch to the onset feature does not
      improve on onset-only (H4e CRC D −0.0534, not confirmed; label-route equivalence)."

18. **The headline generalises the "learned model adds nothing" finding beyond σ 0.2.**
    - *Claim (§5 headline):* "a learned model adds no demonstrated value over a plug-in that uses the same estimate."
    - *Evidence:* At σ 0.4, D(H2b) is superiority on all three routes: 08c 0.3182 [0.2287, 0.4060],
      08e 0.3315 [0.2339, 0.4064], label 0.3275 [0.2399, 0.4019]. These are secondary and unadjusted, but they are
      the opposite of "no value".
    - *Supported rewrite:* "At the primary noise level (σ 0.2), a learned model shows no demonstrated gain over a
      plug-in using the same onset estimate. In secondary, unadjusted analyses it is better at σ 0.4 and worse at
      σ 0."

19. **The H2-R mechanism is asserted, not tested.**
    - *Claim (§2.2 "Where it fails"; §4):* "when friction varies little, the probe's information is worth less than
      its noise, and the fixed-friction plug-in wins"; "the overall gain depends on the friction spread".
    - *Evidence:*
      - 08g §4 restricts the sub-pool on two things, μ ∈ [0.5, 0.8] and the middle-50 % disturbance amplitude, so the
        friction range is not isolated.
      - q̂ is recalibrated on 352 cal instances (≈ 88 per stratum).
      - No prediction was registered, and no analysis varies friction spread.
      - `sec08g.json` contains only D −0.2614, CI\*\* [−0.5320, −0.0325].
    - *Supported rewrite:* "In the H2-R sub-pool (μ ∈ [0.5, 0.8] and mid-amplitude disturbances; n_cal 352,
      n_test 548), CertGrip is worse than CSF-1 (D −0.2614, CI\*\* [−0.5320, −0.0325]; secondary, no registered
      prediction). Whether this is caused by the narrow friction range is not tested."

20. **"Holds on every … check" ignores H2-R and the σ 0.4 SESOI.**
    - *Claim (§5):* "The result holds on every robustness, route, seed, cell and comparator check in the files."
    - *Evidence:* H2-R (a sub-pool check of the same contrast) reverses the sign. At σ 0.4 the lower limit (0.0832)
      is below the 0.10 SESOI (`crc_analysis.json`).
    - *Supported rewrite:* "H2a superiority holds for F\*_lo / F\*_hi, the label and post hoc routes, seeds 1–4, all
      16 cells, H2-n and Mondrian-CSF. It reverses in the restricted H2-R sub-pool, and its lower limit falls below
      0.10 at σ 0.4."

21. **The S1/S2 "explanation" of R_E is causal language for a descriptive pattern.**
    - *Claim (§2.1.4):* "The direction of the mismatch explains the R_E values".
    - *Evidence:* The slip-rate pattern matches the R_E direction (S1 oracle 0.0751 vs OQT 0.1016; S2 0.1346 vs
      0.0999, label window). No analysis separates the slip mismatch from efficiency.
    - *Supported rewrite:* "The R_E direction is consistent with the slip mismatch (S1 oracle under-slips, 0.0751 vs
      0.1016; S2 over-slips, 0.1346 vs 0.0999), so R_E is not a like-for-like efficiency comparison in S1 and S2."

22. **"OQT restores slip to ≈ α" is measured by the label rule, not physically.**
    - *Claim (§2.2, §5):* "OQT restores window slip to ≈ α in every shift (0.0999–0.1016)".
    - *Evidence:* These are label-rule rates over 20 orderings, and the tracker is driven by the same label rule.
      Physical rates exist only for ordering 0 (audit b): S1 0.103, S2 0.092, S3 0.101. Frozen arms do not break in
      S2 (Frozen-CertGrip 0.1017, Frozen-COMP 0.1051).
    - *Supported rewrite:* "Window label-rule slip of OQT-CertGrip is 0.0999–0.1016 across shifts (physical, ordering
      0: 0.092–0.103), while Frozen-CertGrip reaches 0.3056 (S1) and 0.2461 (S3) and Frozen-COMP 0.5101 (S1). Neither
      frozen arm breaks in S2."

23. **The cause of the 08b §3 split inconsistency is unverified.**
    - *Claim (§3.10):* "08b §3 is the stale text from before the split change".
    - *Evidence:* The inconsistency is real (08b §3 says "objects 200–249"; 08b §5, 08c and `comp_selection.json`
      say 150–199). Nothing in the permitted files documents why.
    - *Supported rewrite:* "08b §3 says 200–249, while 08b §5, 08c and `comp_selection.json` say 150–199. The JSON
      and 08c agree, and the discrepancy should be listed as a documentation deviation."

---

## Numbers verified as correct (spot list)

- **COMP:** CSF-1 0.7686 (0.7921 / 0.7450), Mondrian 0.8294, CertGrip-P 0.8335; 800 instances, 0 excluded.
  η 0.03412. n_cal 2,000, n_test 2,800, 2,000 draws.
- **H1-M:** 8 / 800, CP upper 0.02115. By family 3/2/2/1, by disturbance 1/7/0/0. Shift pools 0/1/1. Six of ten
  violations at rel ≈ −0.0067; max 0.00904.
- **H2a (08c):** 0.4168 [0.3484, 0.4778]; lo / hi 0.4150 / 0.4186 with CIs as quoted. Seeds 1–4: 0.4343, 0.4197,
  0.3932, 0.4494. σ curve 0.6789 / 0.5825 / 0.4168 / 0.1401; σ\* 0.4. σ 0.4 lower limits 0.0832 / 0.0868 (08e) /
  0.0983 (label).
- **H2b (08c):** 0.0569 [−0.0399, 0.1454]; seeds 0.0188–0.1095, all not confirmed. σ 0 / 0.1 / 0.4: 0.2460 /
  0.1072 / 0.3182 with CIs as quoted.
- **CRC arm table:** all RE_mid, CIs, slip_phys, slip_label and λ̂ indices correct, including CSF-μ̂ 0/0/14/12 and
  CSF-1 1/1/15/14. No at_max.
- **08e:** H2a 0.4289 [0.3577, 0.4770]; H2b 0.0240 [−0.0949, 0.1001]; H4e −0.0219 [−0.1208, 0.0369]; H2b σ 0 / 0.1 /
  0.4 as quoted. λ̂ indices 20–22 of 41. RE 0.4551 / 0.7778 / 0.4442.
- **Label route:** H2a 0.4292 [0.3654, 0.4822]; H2b 0.0134 [−0.0850, 0.0814]; H4e −0.0417 [−0.0990, 0.0128]; H2b
  seeds 0.0053 / 0.0394 / −0.0120 / 0.0104. All arm REs (0.4264, 0.7469, 0.4321, 0.4093, 0.7831, 0.7897, 0.8104,
  oracle 0.1271). The 0.74691035 vs 0.74691020 discrepancy is real.
- **H3:** R_E and CIs for S1 / S2 / S3 / S1m / ID. All arm RE and slip values in the H3 table. Matched physical
  0.032 / −0.035 / 0.009. capped_window 0. ρ − ρ_ID CIs include 0. Audit S2 Δ −0.008 [−0.0149, −0.0029].
- **H1-V:** all four Δ and CIs; disagree counts; 3 / 4 CIs exclude 0. CertGrip slip direct 0.1014
  [0.0864, 0.1168], label 0.1057.
- **H4a:** −0.0084 [−0.0360, 0.0128]; −0.0263 [−0.0558, 0.0149]; 0.4739 [0.4148, 0.5229].
- **H4c:** −0.0253 [−0.0526, 0.0085]; RE 0.8029.
- **H2-T:** 0.5918 / 0.6014 / 0.6019 with CIs.
- **H2-M:** 0.4598, 0.4555, 0.0042 and CIs. Mass noise 0.4603, 0.0312 and CIs.
- **H2-C:** 0.4381 [0.3733, 0.4872].
- **H2-n:** 0.4146 / 0.4654 with intervals.
- **H2-H:** pooled 0.4388 [0.4036, 0.4741], τ 0.0511, Q 31.04; cell range 0.2979–0.5340; minimum lower limit
  0.1602 (> 0.16).
- **H2-R:** −0.2614 [−0.5320, −0.0325], n 352 / 548.
- **H4d:** 0.0342 [−0.0424, 0.1138]; 0.0021 [−0.0174, 0.0213].
- **Oracle decomposition:** 0.5172 [0.4489, 0.5762].
- **H3-S:** 58.15 [48.20, 70.20], 42.40 [32.40, 49.35], 2.90, 2.75 with CIs.
- **H4b:** 0.2361 [0.1957, 0.2607], D_FID 0.4638, D 0.4555. **D-FID:** 0.7257 / 0.7296 with CIs.
- **D-μ:** all 14 values. **D-loc:** 0.5091, SD 0.0093, 2,794 pairs; |Δĝ|/ĝ values; preload slip 0.
- **H3-B:** all ranges (S1 0.501–0.523 / 0.503–0.525, |diff| ≤ 0.0036; S1m; S3; S2); probe arm 0.3039 / 0.1246 /
  0.25 / 0.0936.
- **H1c:** RAW-Q / RAW-G slip − α range 0.0096–0.0507, all CI\*\* > 0; α 0.05 CIs as quoted.
- **Addenda facts:** 08b §5 power figures (D ≈ 0.43, SE ≈ 0.040; H2b 17 % / 40 %); 08a pilot corr 0.988; detector
  tuned on objects 0–24; MuJoCo 4.0.0.
