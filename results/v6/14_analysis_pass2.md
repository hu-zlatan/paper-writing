# Stage 14 (v6), pass 2: area-chair scrutiny of `14_analysis_pass1.md`

Source checked: the full read-out JSON and pre-registered rules in `results/v6/prompts/stage14_pass1_user.txt`. All arithmetic below was recomputed from that JSON. Keys are written as `cell.window.path`.

Severity: **S** = changes a conclusion, **M** = misstated number or overreach, **m** = wording.

Overall, the tables are transcribed correctly. Every success, CI, p-value, TOST, Holm flag, travel, agreement, flip-rate and latency value in the tables matches the JSON. The derived r0/RL means, the latency ratios (G\*/student 2,544–9,767×, G\*/reduced 19.0–47.0×, reduced/student 62–389×) and the Holm step-downs also reproduce. The problems are in the prose, the summaries and the bottom line.

---

1. **[S] Bottom line: "approaches G\* to within a few pp, with no detectable cost".**
   - *Evidence:*
     - "Within a few pp" is true only of the point estimates (0.28–3.74 pp). The intervals reach much further: `S4.0-499.H6a.success.ci95` = [−0.0784, 0.0024], and the fresh window reaches −0.1165 (`S4.300-499.H6a.success.ci95`). The registered TOST could not exclude gaps beyond 4 pp in any cell.
     - "No detectable cost" contradicts the analysis's own BI section. `H6a.ball_info.p_two_sided` is 0.0 in S4, 0.0048 in S8 and 0.0206 in S2, all with negative diffs.
     - It also contradicts the success data: `S4.0-499.H6a.success.tost.ci90` = [−0.0716, −0.0036] lies entirely below 0, and so does the fresh ci90 [−0.106, −0.0005].
   - *Rewrite:* "The student's success point estimate is 0.3–3.7 pp below G\* in every cell, with no registered difference and no registered equivalence; deficits of up to about 7–8 pp (ci95) cannot be excluded, and its ball-info is significantly lower in S4 and S8."

2. **[S] Bottom line: "a distilled student dominates reduced planners".**
   - *Evidence:*
     - Holm rejects only 7/10 contrasts. Student − g500_512_4 is not rejected in S2 (p 0.1378), S8 (0.0314) or S12 (0.2688) (`*.0-499.holm.H6b_g500_512_4` = false).
     - On the fresh window, only 2/10 contrasts survive (`S4/A16-2.300-499.holm.H6b_g125_512_16`). Student − g500 there is +0.004 in S2 (p 0.9268) and −0.011 in S12 (p 0.7368).
     - The registered wording permits "more accurate than a reduced planner" only where Holm rejects.
   - *Rewrite:* "The student is faster than both reduced planners in every cell (62–389×, v5 point medians) and, by Holm, more accurate than g125_512_16 in all 5 cells and g500_512_4 in S4 and A16-2; against g500_512_4 in S2/S8/S12 no accuracy difference is shown."

3. **[M] §2.1 and §5: "The point estimate is negative in 4/5 cells on 0–499 … 0.28 to 3.74 pp" and "0.3–3.7 pp below G\* in 4/5 cells and level in A16-2".**
   - *Evidence:* `*.0-499.H6a.success.diff` is −0.0262, −0.0374, −0.0292, −0.0196 and −0.0028, so all five are negative. The stated range 0.28–3.74 itself includes A16-2, which makes the "4/5" wording internally inconsistent. (4/5 is correct only for the fresh window, where A16-2 is +0.001.)
   - *Rewrite:* "On 0–499 the point estimate is negative in all 5 cells (−0.28 to −3.74 pp, A16-2 essentially level); on 300–499 it is negative in 4/5 and +0.1 pp in A16-2."

4. **[M] §2.4 and Limitation 5: "on test5 0–499 [H\*] is not the best heuristic in two cells (S8, S12)".**
   - *Evidence:*
     - In S4, H\* = b_fan (`S4.0-499.v5_row_updates.H_star`) with success 0.368, but `S4.0-499.means.b_cov.success` = 0.416. That makes three cells.
     - A16-2 is also not strictly best: b_fan 0.312 vs b_cov 0.314.
     - Against the best heuristic, the student's margin in S4 shrinks from +8.96 to about +4.2 pp (derived: 0.4576 − 0.416).
   - *Rewrite:* "H\* is not the best test5 heuristic in S4 (b_cov 0.416 vs b_fan 0.368), S8 and S12 (and trivially A16-2); against the best heuristic the student's untested point margin would be about +4.2 (S4), +5.1 (S8) and +2.4 pp (S12)."

5. **[M] §2.1: the BI deficit is "measurably less informative … in S2/S4/S8"; §5: "Ball-info shows a clearer deficit in S2, S4 and S8".**
   - *Evidence:*
     - The analysis's own Holm step-down over the 5 BI p-values keeps only S4 and S8. S2 is 0.0206 × 3 = 0.062 > 0.05.
     - The S2 BI result also fails on the fresh window: `S2.300-499.H6a.ball_info.p_two_sided` = 0.1612, ci95 [−0.256, 0.044].
     - BI is not a registered decision family.
   - *Rewrite:* "Student BI is lower than G\*'s in S4 and S8 even after an (unregistered) Holm adjustment and on the fresh window; S2 is nominally lower on 0–499 only (p = 0.0206)."

6. **[M] §2.1: the run-1-only gaps "match v5's '0.2–2.5 pp below, not significant' pattern, except that S4 widens on the fresh window".**
   - *Evidence:*
     - On 0–499, S4 is already −3.84 pp (`S4.0-499.v5_row_updates.student_minus_gstar_run1_success.diff` = −0.0384), outside 0.2–2.5.
     - A16-2 flips sign to +0.92 pp (`A16-2.0-499…diff` = +0.0092). v5 had the student below in all five cells.
   - *Rewrite:* "Against G\* run 1 alone, the gaps are −1.92, −3.84, −1.32, −1.96 and +0.92 pp (none significant). S4 now exceeds v5's 0.2–2.5 pp range, and A16-2 has changed sign."

7. **[M] §3 "Fresh vs reused": "Every primary conclusion has the same direction on 300–499 … H6b: all positive except the S12 g500 point."**
   - *Evidence:*
     - The H6b conclusion (7 Holm rejections) does not replicate. Only 2/10 are rejected fresh: `S2.300-499.holm.H6b_g125_512_16` = false, `S8` false, `S12` false, and g500 false everywhere.
     - S2 student − g500 is +0.004 fresh, effectively zero.
     - For H6a, the A16-2 point sign changes from −0.0028 to +0.001.
   - *Rewrite:* "On 300–499 the point signs mostly agree (all H6b points positive except S12 g500, −1.1 pp), but only 2/10 H6b contrasts survive Holm, so the fresh window replicates the direction, not the significance, of H6b."

8. **[M] §5: "The student is reliably *not more than 4 pp better* (upper margin rejected everywhere)".**
   - *Evidence:* This holds on 0–499 (p_upper 0.0003–0.0348). On the fresh window, `A16-2.300-499.H6a.success.tost.p_upper_margin` = 0.1557 is not rejected. These are also per-cell, unadjusted one-sided tests.
   - *Rewrite:* "On 0–499 the +4 pp upper margin is rejected in every cell (unadjusted p_upper ≤ 0.0348), so the student is not shown to be more than 4 pp better anywhere; on 300–499 this fails in A16-2 (p = 0.1557)."

9. **[M] §2.4 H5b: "The CI is about 15 pp per 100° wide".**
   - *Evidence:* `H5b_update_0_499.ci95_per_100deg` = [−0.1366, 0.1239]. That is about 26 pp wide (half-width about 13 pp).
   - *Rewrite:* "The 95% CI spans about 26 pp per 100° (−13.7 to +12.4 pp), so the test is uninformative."

10. **[M] Limitation 3: "flips 0–13 % of episode outcomes in the S cells".**
    - *Evidence:* In the S cells, `E12.flip_rate` has a minimum of 0.04 (S2 s704; S12 s701/s702) and a maximum of 0.13. The 0.00 values occur only in A16-2.
    - *Rewrite:* "The sub-8 → sub-16 change flips 4–13 % of episode outcomes in the S cells and 0–1 % in A16-2."

11. **[M] §2.5: "In the 4 S cells, the size of the shift (1.6–5.0 pp) is comparable to or larger than the 4 pp equivalence margin."**
    - *Evidence:* The derived shifts are S2 −1.6, S4 +4.6, S8 +5.0 and S12 −4.6 pp. S2's 1.6 pp is well under half the margin, so the claim holds in 3 of the 4 S cells. These are also 100-episode, G\*-run-1-only contrasts, with ci95 half-widths of 7–10 pp (`E12.student_minus_gstar_success_sub8.ci95`).
    - *Rewrite:* "In S4, S8 and S12 the grid change moves the 100-episode student − G\* contrast by 4.6–5.0 pp, comparable to the 4 pp margin; in S2 (1.6 pp) and A16-2 (0.6 pp) the shift is small."

12. **[M] §2.3 and §5: "the data do bound any DAgger benefit to below about 5 pp per cell".**
    - *Evidence:* This is true on 0–499 (max ci95 upper 0.048). On the fresh window, `S2.300-499.H6c.success.ci95` = [−0.049, 0.071], so the upper bound is 7.1 pp. Bounds are also per cell and unadjusted.
    - *Rewrite:* "On 0–499 the per-cell 95% upper bounds on the DAgger gain are at most 4.8 pp (up to 7.1 pp on the fresh window); no equivalence test was registered."

13. **[M] §5: "Shrinking G\* by about 20–45× in latency costs 4–14 pp of success, more than the student loses."**
    - *Evidence:* The derived G\*/reduced ratios are 19.0–47.0× (A16-2 g125 47.0, S12 g500 19.0). "More than the student loses" compares point estimates only, and in 3 g500 cells the student − g500 difference is not significant (see item 2).
    - *Rewrite:* "The reduced planners are 19–47× faster than G\* and lose 4.4–14.4 pp against G\* run 1 (point values), versus a student point loss of −0.9 to 3.8 pp; the difference is Holm-significant in 7/10 contrasts."

14. **[m] Limitation 4: "δ = 4 pp and 500 episodes gave the expected 90 % half-widths of 2.8–3.9 pp."**
    - *Evidence:* The design note expected "roughly 3.5–4 pp". The figures 2.84–3.85 are the observed half-widths (derived from `H6a.success.tost.ci90`). S4 (3.40) and S12 (2.84) came out narrower than predicted, so §2.1's "the power prediction held" is approximately but not exactly true.
    - *Rewrite:* "The design note expected 90 % half-widths of about 3.5–4 pp; the observed half-widths were 2.84–3.85 pp, at or below that."

15. **[m] §2.1: "equivalence needed point gaps of at most about 0.2–1.2 pp. Only A16-2 had such a gap".**
    - *Evidence:* Per cell, the requirement 0.04 − half-width is 0.46, 0.60, 0.50, 1.16 and 0.15 pp. A16-2's gap (0.28 pp) exceeds its own requirement (0.15 pp), so no cell met its threshold. That is consistent with p_TOST 0.0548.
    - *Rewrite:* "Equivalence required |gap| ≤ 0.15–1.16 pp depending on the cell; no cell met its own threshold, with A16-2 closest (0.28 vs 0.15 pp)."

16. **[m] Limitation 4: "the S4 ci90 excludes 0, so a small deficit there cannot be ruled out".**
    - *Evidence:* A ci90 entirely below 0 is the opposite of "cannot be ruled out". It means no deficit is rejected at the one-sided 5 % level (unregistered, unadjusted).
    - *Rewrite:* "In S4 the ci90 lies entirely below 0 on both windows, an unregistered one-sided indication of a small student deficit."

17. **[m] §5: "The student stays above … RL in 4/5 cells."**
    - *Evidence:* The point estimates of `student_minus_rl_success` are positive in 5/5 cells. The S8 ci95 [−0.0104, 0.0624] includes 0. On the fresh window, S8 (p 0.5744) and S12 (p 0.22) are also not significant.
    - *Rewrite:* "The student is significantly above RL cfg 6 in 4/5 cells on 0–499 (S8 not significant), and in 3/5 on the fresh window."

18. **[m] §3 Multiplicity: "Single unadjusted p-values near 0.02–0.05 … Examples are S8 fresh G\* − student g_T".**
    - *Evidence:* `S8.300-499.v5_row_updates.H2_v5_update.gstar_minus_student_gT.p_two_sided` = 0.0068, which is not in 0.02–0.05.
    - *Rewrite:* "Unadjusted p-values in these unregistered families (e.g. S8 fresh G\* − student g_T, p = 0.0068; S12 fresh student − rl_success, p = 0.05) should not be read as findings."

19. **[m] Limitation 3: "success contrasts of a few pp sit within evaluator noise".**
    - *Evidence:* E12 re-reads the same episodes on a different grid. It measures evaluator *sensitivity*, a systematic read-out dependence, not random noise, and it covers only 100 episodes of G\* run 1.
    - *Rewrite:* "On episodes 0–99, changing the read-out grid alone moves student − G\* contrasts by up to 5 pp, so contrasts of a few pp are sensitive to the evaluator choice."

20. **[m] Limitation 1: "first-decision agreement is only 0.27–0.45".**
    - *Evidence:* This is correct for 0–499. On the fresh window, `S2.300-499.gstar_first_decision_agreement_run2_vs_run1` = 0.245.
    - *Rewrite:* "First-decision agreement is 0.25–0.45 across cells and windows."

21. **[m] §5 H6c: "Most of the student's accuracy comes from behaviour cloning on G\*."**
    - *Evidence:* r0 is within 1.3 pp of r2 (`H6c.success.diff`). No baseline without BC was run, so "most of the accuracy" is an attribution the design does not test.
    - *Rewrite:* "The round-0 (BC-only) students already reach the round-2 success level (|r2 − r0| ≤ 1.3 pp), so the DAgger rounds add no detectable accuracy."

---

## Verdict

None of the pre-registered verdicts is misreported. The JSON `holm` flags and the analysis agree on every point:

- **H6a:** "neither a difference nor equivalence shown" in all 5 cells and both windows.
- **H6b:** 7/10 Holm rejections, all positive, on 0–499 (2/10 fresh).
- **H6c:** "not detected" everywhere.
- **Report-only rows:** H5b "no trend detected" and the inversion flags (S2/S4) are copied correctly.

The defects are in the interpretation:

- The bottom line ("dominates reduced planners", "within a few pp, no detectable cost") overstates H6b and ignores the BI and S4 one-sided evidence (items 1–2).
- The 0–499 sign count is wrong: all five cells are negative, not four (item 3).
- The stale-H\* caveat misses S4 (item 4).
- Several ranges are misstated (items 9–13).
