# p2 (CertGrip) — Stage 14 v4 analysis, pass 2 (independent area-chair check)

Scope: every number and claim in "Stage 14 analysis, v4 (amendment 11), pass 1" checked against `results/v4/v4_analysis.json`, `results/v3/a7_integrated.json` and the run context (amendment v4, completeness note) as given verbatim in the prompt.

**Overall:** I checked every table cell in §1.1, §1.2, §2.2 (S4), §2.3, §2.5, §2.6 and §2.7 against the JSON at 4 significant figures. All of them match. The consistency rebuilds in §1.2 also hold: C1 1 − 0.42751/0.75182 = 0.43137 and C4 1 − 0.42290/0.26742 = −0.58143. I also verified C2 (0.01117), C5 (−0.54606) and S5_C4_crc (−0.5166, from the RE column), which confirms that the "RE" column is the CRC route. The problems are in the interpretation, plus one statistical/numeric error in §3.1.

Legend: **[NUMERIC]** marks a numeric error. All other findings are unsupported or overstated claims.

---

## Findings (most severe first)

1. **[NUMERIC] §3.1, Holm validity: "Even on the most conservative reading, each p is below 1/2,000, so the smallest Holm-adjusted bound is still far below 0.05."**
   - *Evidence:* The registered p is p = min(1, 2·min(share ≤ 0, share ≥ 0)). For the two-sided superiority rows (C1, C3, C4, C5), one crossing draw already gives p = 2/2,000 = 0.001. So p = 0.0 means p < 0.001, not p < 1/2,000. Only the one-sided TOST p of C2 has resolution 1/2,000. Also, Holm's worst case is set by the *largest* adjusted bound, not the smallest: 5 × 0.001 = 0.005.
   - *Rewrite:* "With p reported as 0.0 (no draw crossed the null), each two-sided p is < 0.001 (C2's one-sided TOST p < 0.0005), so even the largest Holm-adjusted bound (5 × 0.001 = 0.005) is below 0.05."

2. **§2.5 / §5, the mechanism claim: "Once friction uncertainty is narrower than the probe noise, the probe is a net cost" / "The probe pays off only when friction uncertainty exceeds probe noise." The same mechanism is also asserted for C4/C5.**
   - *Evidence:* No quantity in the data puts friction width and σ on a common scale, and no threshold is estimated. S3 only shows D falling as w shrinks: plug-in 0.4314 → 0.2414 → −0.1094 → −0.6967. The sign change falls between w 0.75 and w 0.5 at the single noise level σ 0.2. S3 is run on f4 and does not involve CSF-fam. So the claim that C4/C5 share this mechanism is an untested interpretation.
   - *Rewrite:* "On f4 at σ 0.2, D(plug-in vs CSF-1) falls monotonically as the friction window narrows (0.4314 at w 1.0 to −0.6967 at w 0.25), crossing 0 between w 0.75 and w 0.5. We hypothesise, but did not test, that this reflects friction spread relative to probe noise."

3. **§2.1 summary: "The v3 exploratory attribution ('… probe + plug-in + CRC suffices') is now confirmed on 700 fresh test objects at σ 0.2."**
   - *Evidence:* The "learner adds nothing" part (C2) is established only on the matched-slip route. On the CRC route (S5_C2_crc), D is −0.06291 with CI** [−0.1226, 0.08396]. That interval crosses the −0.10 margin, so equivalence is not shown "with CRC". §3.3 admits this, but the summary sentence and §5 drop the qualifier.
   - *Rewrite:* "At σ 0.2 on 700 fresh f4 test objects, the registered matched-slip tests confirm that the plug-in beats CSF-1 (C1) and that the learner is equivalent to the plug-in within ±0.10 (C2). On the unmatched CRC route the equivalence is not established (CI** [−0.1226, 0.08396])."

4. **§5, recommended framing: "a tactile probe plus a calibrated plug-in gives a *certified* grip-force saving."**
   - *Evidence:* The analysis itself calls the certificate marginal. In S7 (CRC), the plug-in exceeds α in 0.08 of re-splits, and 0.645 of re-splits have at least one stratum above α (D1 share 0.47). "Certified" without the qualifier "marginal" overstates the guarantee. The framing also generalises from one simulated design and one σ.
   - *Rewrite:* "In simulation at σ 0.2, a tactile probe plus a CRC-calibrated plug-in reduces relative excess grip force against a pooled prior (D 0.4314) while keeping pooled slip near α on average (S7 mean 0.08513), with per-stratum exceedances common."

5. **§3.4: "Sign and size agree across routes."**
   - *Evidence:* This is true for C1, C4 and C5, but not for C2. The matched D is +0.01117 and the CRC D is −0.06291: the sign flips and the gap is about 0.074, which is large relative to the 0.10 SESOI.
   - *Rewrite:* "C1, C4 and C5 keep sign and similar size across routes (0.4314/0.4482, −0.5814/−0.5166, −0.5461/−0.4733). C2 does not: +0.01117 matched vs −0.06291 CRC."

6. **§4: "The C4/C5 size depends on band width relative to σ, as the S3 sweep shows."**
   - *Evidence:* S3 varies the friction window on f4 at a fixed σ 0.2 against CSF-1. It never varies the c4 band width, never varies σ on c4, and never uses CSF-fam. No data show how C4/C5 depend on band width or σ.
   - *Rewrite:* "C4/C5 were measured for one band layout and one σ (0.2). How their size depends on band width or σ was not tested."

7. **§2.3: "At σ 0.4 it is clearly better, *because it is robust to a noisy μ̂*."**
   - *Evidence:* D(full_rd@0.4 vs CSF-muhat@0.4) = 0.3238 [0.2778, 0.3817] supports "better". The causal explanation is not tested; there is no ablation of the learner's μ̂ dependence.
   - *Rewrite:* "At σ 0.4 the learner outperforms the plug-in (D 0.3238, CI** [0.2778, 0.3817]; secondary, unadjusted)."

8. **§3.2: "The two-sided p of 0.915 confirms there is no detectable difference."**
   - *Evidence:* A large two-sided p is absence of evidence, not confirmation. Equivalence is carried only by the TOST p (0.0) and the CI** lying inside ±0.10.
   - *Rewrite:* "Equivalence rests on the TOST (p 0.0) and the CI** inside ±0.10; the two-sided p of 0.915 is consistent with this but is not itself evidence of equivalence."

9. **§3.7: "Most arms are badly mis-calibrated within individual families."**
   - *Evidence:* Exceedances above α occur only in F1: CSF-1 0.3157, full_rd 0.2014, plug-in 0.1143. In F2–F4, every arm's slip is ≤ 0.09. The S4 values are also single-split point values without CIs, at about 175 test objects per family.
   - *Rewrite:* "In c4 family F1, three of four arms exceed α (CSF-1 0.3157, full_rd 0.2014, plug-in 0.1143); in F2–F4 all arms are ≤ 0.09. Only CSF-fam stays ≤ α in every family (max 0.09286). These are single-split points without CIs."

10. **§2.2: "The practical meaning: most of the v1–v4 saving is a saving against an uninformed pooled prior (CSF-1)."**
    - *Evidence:* The v1–v3 results are not in the provided data, apart from the a7 break-even. The v4 data show only that on c4 the tactile arms beat CSF-1 (0.4285, 0.4412) and lose to CSF-fam (−0.5814, −0.5461). "Most of the saving" is not quantified anywhere.
    - *Rewrite:* "In v4, the tactile saving is measured against CSF-1. On c4 it persists against CSF-1 (D 0.4285 and 0.4412) but reverses against the family prior CSF-fam (D −0.5814 and −0.5461)."

11. **§2.2 heading / §5: "The tactile saving does not survive a friction-informative prior."**
    - *Evidence:* On c4, the saving against CSF-1 *does* survive (S5 match: 0.4285 [0.3648, 0.4741] and 0.4412 [0.3876, 0.4817]). What fails is superiority over CSF-fam. Read literally, the heading contradicts the data.
    - *Rewrite:* "On c4 the tactile arms still beat CSF-1 but are not superior to the family prior CSF-fam, whose CI** lies wholly in its favour (C4 −0.5814, C5 −0.5461)."

12. **§2.5: "The cause is CSF-1, not the tactile arms… The plug-in stays at roughly 0.41–0.46 RE across the whole sweep."**
    - *Evidence:* The D column in the table is matched-slip, but the explanation quotes CRC-route RE. The plug-in's CRC RE is 0.4317, 0.4620, 0.4192, 0.4064; its RE_match is 0.4275, 0.4130, 0.4051, 0.3915. The direction holds on both routes. The 0.41–0.46 range is CRC only, while CSF-1's RE_match falls 0.7518 → 0.2307. These are descriptive single-split values.
    - *Rewrite:* "Across the sweep, CSF-1's matched RE falls from 0.7518 to 0.2307 while the plug-in's stays between 0.3915 and 0.4275, so the decline in D is driven mainly by CSF-1 improving."

13. **§2.4: "Frozen v3 OLS shrinkage therefore improves on the raw plug-in."**
    - *Evidence:* The CI** [0.04864, 0.1449] excludes 0, but its lower end is below the 0.10 SESOI, and TOST p is 0.477. So an improvement of practically relevant size (≥ SESOI) is not established. The row is also secondary and unadjusted.
    - *Rewrite:* "CSF-shrunk@0.2 improves on the raw plug-in (D 0.1119, CI** [0.04864, 0.1449]; secondary, unadjusted), though whether the gain exceeds the 0.10 SESOI is unresolved."

14. **§3.6: "S7 shows such exceedances are expected under CRC" (said of CSF-muhat@0.4, slip 0.1014).**
    - *Evidence:* S7 covers only full_rd@0.2#0, CSF-muhat@0.2 and CSF-1. No re-splits were run for the σ 0.4 arm.
    - *Rewrite:* "For the σ 0.2 arms and CSF-1, S7 shows single-split pooled exceedances in 8–14.5 % of re-splits; CSF-muhat@0.4 was not re-split."

15. **§5: "individual strata and families regularly exceed it."**
    - *Evidence:* "Regularly" over strata comes from S7 (f4, 200 re-splits; 0.315–0.7 with any stratum above α). The family exceedance is from S4 (c4, one split, only F1). The sentence merges two designs and implies a re-split frequency for families that was never measured.
    - *Rewrite:* "Across 200 f4 re-splits, 31.5–70 % have at least one disturbance stratum above α; on the single c4 split, family F1 exceeds α for three of four arms."

16. **§1.1: "no row hit the grid edge (`edge: false` everywhere). The C1–C5 results are therefore all interpretable under the 'grid floor / ceiling' rule."**
    - *Evidence:* The registered rule is about λ̂ landing on index 0 or 80 in any stratum. The JSON gives per-stratum λ̂ indices only for noprobe CSF-1 (41). For the other arms there is only a boolean `edge` whose definition is not in the provided material. The conclusion is plausible but rests on an assumed meaning of the flag.
    - *Rewrite:* "All rows report 2,000 valid draws and `edge: false`, which we take, per the read-out code's flag, as no λ̂ at grid index 0 or 80."

---

## Numeric errors

- **Finding 1 is the only numeric error.** The resolution of the two-sided bootstrap p is 2/2,000 = 0.001, not 1/2,000, and the worst-case Holm bound is the largest adjusted value (0.005), not the smallest. The Holm conclusion survives the correction.
- All other numbers in the analysis match the JSON at the stated rounding. That includes the derived ranges 8–14.5 %, 31.5–70 %, 0.0–0.01, 0.06818–0.07141 and 0.41–0.46, as well as the v3 comparators 16.56, 28.61, 32.99, 57.02 and 259.2.

## Fabricated numbers

**No.** Every number in the analysis appears in, or is a correct rounding or range of, values in `v4_analysis.json`, `a7_integrated.json` or the run context (for example ±0.10 SESOI, 1/2,000 resolution, μ̄ 0.379/0.496/0.677/0.852, pool sizes 4,800). The "1/2,000" in §3.1 is a real context number, but it is misapplied (finding 1), not invented.
