# p2 CertGrip: Stage-14 analysis v3, pass 2 (area-chair audit of pass 1)

Scope: `results/14_analysis_v3_pass1.md`, checked number by number against the JSON blocks and the run context in `docs/prompts/stage14_v3_user.txt` (v1 `crc_analysis.json` and `h3_analysis.json`, v3 `a3_holm.json`, `a_analysis.json`, `a_analysis_08e.json`, `b1_analysis*.json`, `b2_analysis.json`, `b3_analysis.json`, amendment 10 / addendum 10a).

Every table value in §1 (A1–A7, B1–B3, the v1 anchors) matches the files at the stated precision. So do the derived quantities: the D re-derivations, 1.085 N, 1.003 N, 0.541 N, 0.083 N, 25.3 s, 3.1 %, 12.7 %, 0.5059, 4.6×, 2.2 and Δ 0.0142. The findings below are claims that go beyond, or disagree with, what those numbers support.

---

## Findings

**1. "H2a … survives every v3 robustness row" (F1) / "H2a is robust" (Conclusion 1).**
- *Evidence:* A4 is the H2a contrast itself (CertGrip-full σ 0.2 vs CSF-1), re-run inside sub-pools. On 08e it gives **inferiority** for μ ∧ amp (−0.3152 [−0.5231, −0.0172]) and for μ only (−0.1717 [−0.4275, −0.01539]). Not every v3 row survives. The analysis reports these rows itself in F2, but it does not reconcile them with F1.
- *Supported rewrite:* "H2a holds at the pool level in every v3 row (CRC, empirical margin, refined grid, B3 windows), but it reverses to inferiority inside the 08e μ ∈ [0.5, 0.8] sub-pools (A4)."

**2. "about 0.41–0.44 in online physical feedback" (Conclusion 1). Numeric error.**
- *Evidence:* the B3 D_RE points span 0.3107 (S1 501–1000) to 0.4432 (S1 1–500). F1 itself quotes 0.3107–0.4432. The S1 transient window [0.2893, 0.3293] lies wholly outside 0.41–0.44.
- *Supported rewrite:* "B3 gives D_RE between 0.3107 and 0.4432 across shifts and windows (0.4152–0.4432 outside the S1 transient)."

**3. "CSF-1 … is over-conservative because the coarse grid cannot tighten" (F2, mechanism).**
- *Evidence:* no sub-pool λ̂ index or edge flag is reported for A4. The only λ̂ data for CSF-1 on 08c are pool-level (indices 1 / 1 / 15 / 14), and none of them is at the edge. The files show only the outcome (sub-pool slip 0.03285 on 08c, 0.1004 on 08e), not the grid-resolution cause.
- *Supported rewrite:* "Inside the sub-pool, CSF-1 runs far below α on 08c (slip 0.03285, RE 0.566) and near α on 08e (0.1004, RE 0.2633). This is consistent with grid coarseness, but no sub-pool λ̂ is reported to confirm it."

**4. "the loss is driven by friction … a friction-blind constant with a fine enough margin grid beats the learned rule" (F2; Conclusion 3).**
- *Evidence:* (a) Slip is not matched. On 08e, CSF-1 slips 0.1004 (above α) against full 0.08394, so part of CSF-1's RE advantage is bought with slip budget. The analysis's own check 7 flags this, but F2 and Conclusion 3 omit it. (b) The μ-only pool (cal 724) is the μ restriction without the amplitude restriction, so it contains the μ ∧ amp cells (cal 352). Its inferiority is not independent evidence. (c) No row tests "friction causes" directly.
- *Supported rewrite:* "On 08e, CSF-1 has lower RE than CertGrip-full in the μ ∈ [0.5, 0.8] sub-pools (−0.3152 μ ∧ amp; −0.1717 μ only, which contains it) but not in the amplitude-only pool (+0.4929), at a higher CSF-1 slip (0.1004 vs 0.08394)."

**5. "none of the 9 direct learned-against-plug-in contrasts …" and "the v3 rows push the point estimates towards zero or below" (F3); "decision-labelled v3 rows number … 34" (check 4).**
- *Evidence:* the A6 CRC 08c row (`D_crc:full_vs_muhat`, 0.05692 [−0.03992, 0.1454]) is the v1 H2b row reproduced exactly, not a new v3 estimate. That leaves 8 new σ 0.2 contrasts and 33 new decision rows. Also, the LTT 08c point (0.05379) is essentially the v1 value (0.05692), not pushed towards zero.
- *Supported rewrite:* "None of the 8 new σ 0.2 learned-vs-plug-in contrasts (A6 LTT and matched-slip on both grids, A6 CRC on 08e, three B1 variants) is shown. Their points range from −0.06463 to 0.05379, and 6 of the 8 are below the v1 H2b point of 0.05692."

**6. "The v1 σ-curve superiority of learned over plug-in does not survive v3" (F4 headline).**
- *Evidence:* σ 0.4: the v1 H2b row (vs the unshrunk CSF-μ̂ 0.4, 0.3182 [0.2287, 0.406]) is not re-estimated. B1 introduces a *different* comparator (shrunk plug-in), which beats the learned arm (−0.1395 [−0.1832, −0.01264]). σ 0.0 / 0.1: the analysis states itself that no D with CI** exists on 08e. Amendment 10 also says v3 does not re-decide v1 rows.
- *Supported rewrite:* "v3 qualifies the v1 σ-curve rather than overturning it. At σ 0.4 a shrunk plug-in beats the learned arm (−0.1395, inferiority). At σ 0.0 / 0.1 the v1 comparator sat at λ̂ index 0 in D1–D2 on 08c, and on 08e its arm-level RE (0.208, 0.2915) is below the learned arm's (0.2397, 0.3212), with no contrast CI."

**7. "The v1 σ 0.0 and 0.1 superiorities rest on a plug-in held at the 08c grid floor, and on 08e the plug-in has the lower arm-level RE" (Conclusion 2; F4(b) says "indicate").**
- *Evidence:* the files show λ̂ index 0 in D1 and D2 and test slip 0.007143 / 0.002857 (σ 0.0) and 0.01571 / 0.007143 (σ 0.1) for that comparator. "Rest on" is a causal claim that would need an 08e D with CI**, and none exists. Conclusion 2 states as fact what F4(b) correctly hedged.
- *Supported rewrite:* "The v1 σ 0.0 / 0.1 comparator was at the 08c grid edge in D1 and D2 (slip ≤ 0.01571 there), and its 08e arm-level RE is lower than the learned arm's, which suggests, without testing it, that those superiorities depend on the grid."

**8. "With 500 calibration rows per stratum, the (n+1) correction is smaller than one grid step" (F6) / "A5 shows the (n+1) correction is free at this calibration size" (Conclusion 4); "the empirical λ̂ equals the CRC λ̂ for all arms on 08c".**
- *Evidence:* on 08e, plug-in 0.2 changes operating point under the empirical margin (slip 0.075 → 0.07964; RE 0.4551 → 0.4409). So for that arm the correction is at least one grid step, and it costs 0.0142 RE. Also, no λ̂_emp indices are reported. λ̂ equality on 08c is inferred from identical test points, not read from the files.
- *Supported rewrite:* "On 08c the empirical margin reproduces the CRC test points for all three arms, and on 08e for full and CSF-1. For plug-in 0.2 on 08e the correction costs 0.0142 RE (0.4551 vs 0.4409) at 0.075 vs 0.07964 slip."

**9. "With r_safe = 0.8 μ̂ the detector rarely fires before slip has already counted" and "a purely reactive scheme fails by construction" (F7).**
- *Evidence:* B2 reports only slip, RE, mean steps, cap share and F_end. It has no detection timing relative to slip onset. The data show that the probe variants trigger about 0.5 times per instance (0.4964, 0.5079) while 95–99 % of instances slip. That is consistent with the detector firing rarely, not with an established before/after ordering. "By construction" is also contradicted by REACT-blind c 0.75 reaching 0.3086 in D2: the data show failure at these settings, not an inevitability.
- *Supported rewrite:* "The probe variants step up only about 0.5 times per instance yet slip in 0.9514–0.9921 of instances. Detection timing is not reported, so B2 shows that this registered design fails (slip ≥ 0.3086 in every arm and stratum), not why."

**10. "The force-time benefit is real but modest" (F9); "the mean hold-force saving against CSF-1 is 1.085 N" presented as an H2a robustness row (F1).**
- *Evidence:* A7 reports point means and medians only, with no CI** for any newton difference. "Real" (that is, distinguishable from zero) is therefore not supported by A7. The integrated-force and break-even numbers are reconstructions, as Limitations admits.
- *Supported rewrite:* "On the single 08c test split, CertGrip-full's mean hold force is 1.085 N below CSF-1's (6.521 vs 7.606 N; medians 4.473 vs 5.476 N). No interval is reported."

**11. "preload 13.08, squeeze 12.91 and ramp-down 1.439 N·s, which sum to 27.429 N·s" (§1.8, F9). Numeric error, minor.**
- *Evidence:* the unrounded file values are 13.08 + 12.906776 + 1.438997 = 27.4258 N·s. 27.429 is the sum of the rounded parts, and the analysis quotes it to five significant figures as if exact. The downstream ratios change only in the 4th digit (25.28 s; 3.10 %; 12.73 %).
- *Supported rewrite:* "The shared phases total 27.43 N·s (13.08 + 12.91 + 1.439, unrounded 27.4258)."

**12. "The reported p = 0.0 means no draw crossed 0, so p < 0.0005" (check 3). Numeric error.**
- *Evidence:* amendment A3 defines p = min(1, 2 · min(share ≤ 0, share ≥ 0)) over 2,000 draws. The smallest non-zero p is therefore 2 / 2,000 = 0.001, and every reported non-zero p is a multiple of 0.001 (0.01, 0.079, 0.101, 0.11, 0.119, …). The 1 / 2,000 resolution applies to the share, not to p.
- *Supported rewrite:* "p = 0.0 means no draw fell on the far side of 0. Given the two-sided doubling, this implies p < 0.001, not p = 0."

**13. "The RE agrees with the 08d label route; for example, S1 RE is 0.4746 (physical) against 0.4763 (label)" (F8).**
- *Evidence:* the files do not say which window `RE_window` in `h3_analysis.json` covers, so the like-for-like window is not established. The B3 table in §1.11 also omits the 1001–2000 window, which the file reports (S1 CertGrip RE 0.4702, slip 0.1015; D_RE 0.4154). The claim holds for either window, but the specific pairing is asserted, not shown.
- *Supported rewrite:* "For S1 the physical-feedback RE in the late windows (1001–2000: 0.4702; 1501–2000: 0.4746) is within 0.007 of the 08d label-route RE_window (0.4763), whose window the files do not state."

**14. "B3 confirms that physical feedback converges to α" (Conclusion 5).**
- *Evidence:* B3 is registered as descriptive. Its 95 % intervals cover orderings only, over fixed object pools, as the analysis's own check 9 notes. The late-window CIs contain 0.10 (S1 [0.0969, 0.1033]; S2 [0.0974, 0.1043]; S3 [0.098, 0.1055]), which is consistency, not confirmation.
- *Supported rewrite:* "In B3 the 1501–2000 CertGrip slip is 0.1001 / 0.1008 / 0.1018 (S1 / S2 / S3), with ordering-only intervals that contain α, which is consistent with convergence to α."

**15. "Two of the decisive v3 reversals have CI bounds close to 0 … Under any Holm-type adjustment across these 34 rows, they are at risk" (check 4).**
- *Evidence:* a third reversal is equally close to 0 and is omitted: A4 08e μ-only, upper bound −0.01539. No p-values are computed for any v3 row, so "at risk" is not quantified (and the 34 includes the v1 H2b row; see finding 5).
- *Supported rewrite:* "Three v3 inferiority rows have upper CI** bounds within 0.02 of 0 (A4 08e μ ∧ amp −0.0172, μ-only −0.01539; B1 σ 0.4 −0.01264). v3 rows carry no multiplicity-adjusted p-values, so whether they survive adjustment is not known."

---

## Verdict

- 15 findings. Three are numeric errors (#2 the B3 range in Conclusion 1; #11 the phase total 27.429 vs 27.4258; #12 the p-value bound). One is a labelling and count error (#5: a v1 row counted as a v3 contrast). The remaining 11 are causal or strength-of-claim overreach: unsupported mechanisms (#3, #9), headline claims contradicted by rows reported elsewhere in the same analysis (#1, #6, #8), and hedges dropped between Findings and Conclusion (#7, #14).
- **No fabricated number was found.** Every quoted value is present in the files at the stated precision or is a correct derivation from them. The one inexact derived value (#11) comes from summing rounded parts, not from invention. The most consequential problems are #1 and #2, because Conclusion 1 ("H2a is robust", "0.41–0.44") is the analysis's headline and is directly contradicted by A4 08e and by the B3 S1 transient window.
