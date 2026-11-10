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
