# Stage 15 · Research decision (v6)

> System (verbatim, `results/v6/prompts/stage15_system.txt`): "You are a research program lead making go/no-go
> decisions."
> Task: the full content of `results/v6/prompts/stage15_user.txt` ("Make a PROCEED, REFINE, or PIVOT decision from
> analysis. … Output markdown with: Decision, Justification, Evidence (with cited numbers from the analysis), Next
> Actions (specific stage and tasks)."). `{analysis}` is the merged stage-14 [v6] report. Its "Binding summary" and
> Appendix A (pass 2, items 1–21) override the pass-1 sentences they correct, and that wording is used here.
>
> Fresh subagent, 2026-11-13. Inputs read: `results/v6/prompts/stage15_system.txt`,
> `results/v6/prompts/stage15_user.txt` (in full), `pipeline/references/stage_prompts/research_decision.md` (hard
> rules), `RESTRICTS.yaml` (loops section), `AUTOPILOT.md` (§1 owner directives), `OWNER_TODO.md`,
> `results/v5/15_decision.md` (format and continuity). No other file was read and no code was run. Every number is
> quoted from the stage-14 analysis. Numbers marked *(derived)* are my own arithmetic on quoted values and have no CI.

---

## 1. Decision

**PROCEED to stage 16, as a pre-registered measurement paper with one narrow positive result (H6b), not as a method
paper claiming parity with G\*.** The template's PROCEED hard rule is met in a narrow sense only (§2.1).

The headline the evidence licenses:
- **H6b.** On the accuracy–latency frontier, the distilled student is more accurate than a shrunken planner in 7 of 10
  pre-registered Holm contrasts, and it is 62–389× faster than both reduced planners.
- **H6a.** The student is **not shown** to match G\*, and not shown to differ from it.
- **H6c.** DAgger adds no detectable accuracy over behaviour cloning.

**REFINE and PIVOT cannot run.** `RESTRICTS.yaml` sets `loops.max_refine_cycles: 5` (raised 4 → 5 on 2026-11-10 by the
owner for v6), and v6 is the 5th loop. With `escalate_on_cap_hit: true`, either option could only go to the owner as a
request. On the merits I do not recommend either one before the Stage 1 deadline (§2.2, §2.3). The owner escalation
items are in §4.6.

---

## 2. Justification

### 2.1 The PROCEED hard rules, applied as written

| Hard rule (`research_decision.md`) | Status | Reason |
|---|---|---|
| Primary-metric difference between proposed method and best baseline is statistically meaningful (p < 0.05, appropriate test) | **Met only for the pre-registered H6b family. Not met against G\* (H6a). Not met against the strongest per-cell non-oracle comparator in 4/5 cells.** | See below. |
| Every claimed "effective component" has a non-degenerate ablation | Met by restriction | The one component ablation (H6c, DAgger vs BC) shows no effect, so the paper may claim **no** effective component: not DAgger, and not "distillation from G\*" as a cause (pass 2 item 21). |
| No CRITICAL FABRICATION flags from stage 14 | Met | Pass 2 recomputed the tables from the JSON and states that "every success, CI, p-value, TOST, Holm flag … matches the JSON" and that "none of the pre-registered verdicts is misreported". Its 2 S / 11 M / 8 m items are interpretation errors, and all are adopted here. |

**Rule 1 in detail.**

1. **H6b, pre-registered, Holm over 10 contrasts.** 7/10 contrasts are rejected on 0–499, all positive. The student
   beats g125_512_16 in all 5 cells, and g500_512_4 in S4 (+6.76 pp, p 0.0016) and A16-2 (+10.92 pp, p ≈ 0). This is a
   registered p < 0.05 result against a real baseline class, the cheaper planners. It is the new evidence v6 adds over
   v5. Two qualifications apply:
   - On the fresh 300–499 window only 2/10 contrasts survive Holm (S4 and A16-2 vs g125). The fresh window "replicates
     the direction, not the significance" (pass 2 item 7).
   - The reduced planners and H\* each have a single run, so their run-to-run variance is missing from these CIs
     (Limitation 2).
2. **H6a, pre-registered primary contrast against G\*.** In every cell and on both windows the result is "neither a
   difference nor equivalence shown" under Holm. This rule is about parity, not superiority, so it cannot satisfy
   rule 1. It also blocks any parity claim.
3. **Against the strongest non-oracle comparator in each cell** (0–499 means from the analysis; selection and margins
   *(derived)*):

   | Cell | Student | Strongest non-oracle comparator | Margin *(derived)* | Test |
   |---|---|---|---|---|
   | S2 | 0.4988 | g500_512_4 0.462 | +3.68 pp | p 0.1378, not Holm-rejected |
   | S4 | 0.4576 | b_cov 0.416 (not the pre-registered H\*) | +4.16 pp | none (post-hoc, pass 2 item 4) |
   | S8 | 0.4188 | RL cfg 6 0.3932 | +2.56 pp | ci95 [−0.010, 0.062], not significant, unregistered |
   | S12 | 0.4144 | g500_512_4 0.390 = b_cov 0.390 | +2.44 pp | vs g500 p 0.2688, not Holm-rejected |
   | A16-2 | 0.4832 | g500_512_4 0.374 | +10.92 pp | Holm-rejected (p ≈ 0) |

   So the student clears the strongest comparator at the registered level in 1/5 cells. A sentence such as "the student
   is the best non-oracle policy" is not licensed in S2, S4, S8 or S12.

**The sense in which I proceed.** I apply the same standard as v3–v5: every claim must be the outcome of a pre-registered
rule, evaluated on complete data and worded within what that outcome licenses. Everything else is labelled exploratory.

All v6 decision items are settled:
- `complete` and `gt_complete` are true everywhere.
- Episode counts equal `n_required` (500 / 200 / 100).
- No outcome was read before completeness.
- H6a, H6b and H6c are verified against the JSON `holm` flags.

A measurement paper with a narrow frontier claim is therefore licensed. A parity or method-superiority claim is not.

### 2.2 Why not REFINE (even if the owner lifted the cap)

- **It cannot run.** The cap is 5/5. A REFINE is only an escalation to the owner.
- **The fixable weaknesses would not change the decision-bearing verdicts before the deadline:**
  - **H6a is power- and evaluator-limited.** Equivalence needed per-cell |gap| ≤ 0.15–1.16 pp, and no cell met its own
    threshold (pass 2 item 15).
  - **Point gaps are below teacher variance.** The observed point gaps (0.28–3.74 pp) are about the size of G\*'s own
    run-to-run difference (up to +3.2 pp on 0–499 and +5 pp fresh).
  - **The grid alone moves the contrast by the margin.** Switching sub 8 → sub 16 moves student − G\* by 4.6–5.0 pp in
    S4, S8 and S12 (pass 2 item 11).
  - So more episodes would not settle H6a while the evaluator choice moves the contrast by as much as the margin.
- **Changing the read-out would be post-hoc.** Re-deciding H6a on sub 16, or re-running G\* or the reduced planners
  after unblinding, would rewrite a registered result after seeing it.
- **Time.** 21 days remain to 2026-12-04 AoE *(derived)*. The owner's directive says that if stage 20 is not done by
  12-01, the target becomes Stage 2 / CoRL 2027. A further loop would forfeit Stage 1.

### 2.3 Why not PIVOT

- **The hypothesis family is not "clearly wrong across the board":**
  - H6b is supported in 7/10 Holm contrasts, with no negative point estimate on 0–499.
  - The student is above H\* in all cells (report-only).
  - The student is significantly above RL cfg 6 in 4/5 cells on 0–499.
- **What failed is parity with G\* (H6a, and D3/D4/D5 earlier), plus the DAgger-over-BC claim (H6c).** These are
  findings to report, not reasons to change question.
- **The interesting open questions are methods observations for the discussion, not a pre-registrable pivot in 21 days:**
  - why the student travels less than G\* in every cell;
  - why ball-info is lower in S4/S8 while success is not distinguishable;
  - why the RL-objective inversion appears in S2/S4.

---

## 3. Evidence (quoted from the stage-14 [v6] analysis; Appendix A wording where it applies)

### 3.1 H6a: student (5 seeds) − G\* (runs 1+2), success, sub 8

| Cell | Δ 0–499 [ci95] | ci90 | p_TOST | Δ 300–499 [ci95] |
|---|---|---|---|---|
| S2 | −0.0262 [−0.0688, 0.0168] | [−0.0616, 0.0092] | 0.2621 | −0.036 [−0.114, 0.042] |
| S4 | −0.0374 [−0.0784, 0.0024] | [−0.0716, −0.0036] | 0.4559 | −0.053 [−0.1165, 0.0095] |
| S8 | −0.0292 [−0.0704, 0.0136] | [−0.0640, 0.0060] | 0.2908 | −0.034 [−0.095, 0.028] |
| S12 | −0.0196 [−0.0532, 0.0148] | [−0.0480, 0.0088] | 0.1157 | −0.016 [−0.067, 0.035] |
| A16-2 | −0.0028 [−0.0496, 0.0436] | [−0.0412, 0.0358] | 0.0548 | +0.001 [−0.077, 0.080] |

- **Signs.** All 5 point estimates are negative on 0–499. On 300–499, 4/5 are negative and A16-2 is +0.1 pp (item 3).
- **Margins.** On 0–499 the +4 pp upper margin is rejected in every cell (unadjusted p_upper ≤ 0.0348). On 300–499 it
  is not rejected in A16-2 (p 0.1557) (item 8).
- **S4.** The ci90 lies entirely below 0 on both windows. This is an unregistered, one-sided indication of a small
  deficit (item 16).
- **Ball-info.** BI is lower in S4 (−0.138, p ≈ 0) and S8 (−0.103, p 0.0048) after an unregistered Holm and on the
  fresh window. S2 is nominally lower on 0–499 only (p 0.0206) (item 5).
- **G\* run variance.**
  - Run 2 − run 1 differences are +0.014 / −0.002 / +0.032 / 0.000 / +0.024 on 0–499, none significant.
  - First-decision agreement between the two runs is 0.25–0.45 (item 20).

### 3.2 H6b: student − reduced planners (Holm over 10), 0–499

| Cell | − g125_512_16 | Holm | − g500_512_4 | Holm |
|---|---|---|---|---|
| S2 | +0.0928 [0.044, 0.140] | yes | +0.0368 [−0.012, 0.087], p 0.1378 | no |
| S4 | +0.0556 [0.014, 0.098] | yes | +0.0676 [0.024, 0.112] | yes |
| S8 | +0.0628 [0.022, 0.104] | yes | +0.0468 [0.004, 0.090], p 0.0314 | no |
| S12 | +0.0564 [0.013, 0.099] | yes | +0.0244 [−0.018, 0.067], p 0.2688 | no |
| A16-2 | +0.1532 [0.102, 0.204] | yes | +0.1092 [0.058, 0.159] | yes |

- **Fresh window.** 2/10 contrasts survive (S4 and A16-2 vs g125). Student − g500 is +0.004 in S2 and −0.011 in S12.
- **Latency.** These are v5 E6 job-1 point medians, not re-timed in v6:
  - The student is 62–389× faster than the reduced planners.
  - The reduced planners are 19–47× faster than G\*.
  - G\* is 2,544–9,767× slower than the student.
- **Cost of shrinking the planner.** The reduced planners lose 4.4–14.4 pp against G\* run 1 (point values). The
  student's point loss is −0.9 to 3.8 pp (item 13).

### 3.3 H6c: DAgger round 2 − BC round 0, success

- Diffs are +0.0132 / +0.0084 / +0.0072 / +0.0004 / −0.0052, with p 0.453–0.997. Fresh-window p is 0.5372–0.9208.
- Per-cell 95 % upper bounds are ≤ 4.8 pp on 0–499 and up to 7.1 pp on the fresh window.
- No equivalence test was registered (item 12).

### 3.4 Report-only rows

**E12 (evaluator grid, episodes 0–99, G\* run 1).**
- Sub 8 → sub 16 flips 4–13 % of episode outcomes in the S cells and 0–1 % in A16-2 (item 10).
- The student − G\* shift is −1.6 / +4.6 / +5.0 / −4.6 / −0.6 pp, and the sign changes in 3/5 cells.

**Student − H\*.**
- +6.68 / +8.96 / +7.48 / +5.64 / +17.12 pp, with all ci95 excluding 0 on 0–499.
- On the fresh window, S2 (p 0.0694) and S12 (p 0.0672) do not reach p < 0.05.
- H\* is not the best test5 heuristic in S4, S8 or S12 (and only trivially in A16-2). Against the best heuristic, the
  untested point margins are about +4.2 / +5.1 / +2.4 pp (item 4).

**Student − RL cfg 6.** The student is significantly above RL in 4/5 cells on 0–499 (S8 is not) and in 3/5 cells on the
fresh window (item 17).

**H2-v5 g_T.**
- "Student higher on the RL objective" holds only in A16-2.
- The inversion is true in S2 and S4.

**H5b slope.** −0.0070 per 100°, with ci95 [−0.137, 0.124]. The CI spans about 26 pp, so the test is uninformative
(item 9).

### 3.5 Weaknesses (stated, not fixable inside the cap or the deadline)

- G\* has only 2 runs, so its bootstrap component is poorly estimated.
- The reduced planners and H\* have one run each.
- The evaluator is sensitive at the size of the margin (E12), and E12 itself covers only 100 episodes of G\* run 1.
- Latency comes from v5 point medians without dispersion.
- Episodes 0–299 were already seen in v5.
- BI, g_T and the fresh-window replications are not multiplicity-controlled.
- Scope: simulation only, 5 cells, frozen v5 policies, no hardware.

---

## 4. Next actions

### 4.1 Before stage 16 (main session, report-only, no new runs)

1. Write the *(derived)* values above into a v6 results JSON with provenance ("arithmetic on existing fields, not
   pre-registered, no CI"), so that the paper can cite them:
   - the per-cell strongest-comparator margins (§2.1);
   - the best-heuristic margins (item 4);
   - the r0 and RL means.
2. Update `PROGRESS.md` with the v6 stage-15 outcome, and update `OWNER_TODO.md` per §4.6.
3. **Not to be run:**
   - extra G\* or reduced-planner runs;
   - re-reading H6a on sub 16;
   - latency re-timing;
   - RL re-tuning;
   - retraining students;
   - new tests on BI or g_T.

   Each of these goes into the limitations.

### 4.2 Stages 16–20 (outline → draft → peer review → revision → quality gate)

Schedule (pipeline estimate, not official):
- stage 16 outline by 11-14;
- stage 17 draft by 11-18;
- stage 18 review and stage 19 revision by 11-24;
- stage 20 gate, then stages 22–23 (LaTeX, citation audit), by 12-01.

Per the owner directive of 2026-11-10, if stage 20 is not passed by 12-01, the target becomes RSS Stage 2 / CoRL 2027.
The owner registers and submits; the pipeline does not.

### 4.3 What the paper should look like (RSS 2027 Stage 1 extended abstract, 5 pages body + 1 page references)

**Frame.** "Amortizing a cost-aware information-gain touch planner: a pre-registered accuracy–latency study in TouchBED."

**Contributions, in order:**
- **(C1) Frontier.** A distilled student versus shrinking the planner (H6b).
- **(C2) Parity is not established.** Student versus G\*, with teacher variance included (H6a), plus the v3–v5 gate
  history in one sentence.
- **(C3) DAgger adds nothing detectable over BC** (H6c).
- **(C4) Methods note.** Evaluator-grid sensitivity (E12) and teacher stochasticity.

**Page budget (approximate):**
- ~0.75 p introduction and related work.
- ~1.0 p setup and method: TouchBED, the cost-aware G\*, the reduced planners, the student and the BC/DAgger rounds.
- ~0.5 p pre-registration and statistics: windows, Holm families, TOST with δ = 4 pp, the crossed bootstrap.
- ~2.0 p results:
  - **Fig. 1:** accuracy vs log latency per cell (G\*, the two reduced planners, the student, H\*, RL), the main
    figure.
  - **Table 1:** H6a, both windows, with ci90/ci95.
  - **Table 2:** H6b with the Holm flags and a fresh-window column.
  - One paragraph for H6c and the baseline rows.
- ~0.75 p limitations and the evaluator note.

**Reporting rules:**
- Report 0–499 as primary and 300–499 as the fresh check, side by side.
- Put the E12 caveat beside every student − G\* number.

### 4.4 What the paper MAY claim (exact wording scope)

- **H6b.** "By Holm, the student is more accurate than g125_512_16 in all 5 cells and than g500_512_4 in S4 and A16-2;
  against g500_512_4 in S2/S8/S12 no accuracy difference is shown. It is 62–389× faster than both reduced planners (v5
  point medians)." Always add: "on the fresh 300–499 window only 2/10 contrasts survive Holm".
- **H6a.** "The student's success point estimate is 0.3–3.7 pp below G\* in every cell on 0–499, with no registered
  difference and no registered equivalence; deficits of up to about 7–8 pp (ci95) cannot be excluded; in S4 the ci90
  lies below 0 on both windows; ball-info is significantly lower in S4 and S8." Pair it with G\*'s run-to-run difference
  (up to 3.2 pp on 0–499).
- **Upper bound.** "On 0–499 the student is not more than 4 pp better than G\* in any cell" (unadjusted, per cell).
- **H6c.** "Round-0 (BC-only) students already reach the round-2 success level (|r2 − r0| ≤ 1.3 pp); DAgger adds no
  detectable accuracy (95 % upper bounds ≤ 4.8 pp on 0–499, ≤ 7.1 pp fresh; no equivalence test)."
- **Latency.** "Full G\* is about 2,500–9,800× slower per decision (v5 point medians, no dispersion)."
- **Baselines (report-only).**
  - The student is above the pre-registered H\* in all cells on 0–499. State the stale-H\* qualifier and the
    best-heuristic margins of about +4.2 / +5.1 / +2.4 pp (untested).
  - The student is above RL cfg 6 in 4/5 cells on 0–499 and 3/5 fresh.
- **E12.** "Changing only the read-out grid moves student − G\* by 4.6–5.0 pp in S4/S8/S12, comparable to the 4 pp
  margin."
- **Behaviour.** The student travels less than G\* in every cell (descriptive).

### 4.5 What the paper MAY NOT claim

- "The student matches / approaches / is equivalent to G\*", "within a few pp", "no detectable cost", or any "small" or
  "negligible" gap wording (item 1).
- "The student dominates the reduced planners", or "beats the reduced planners" without the per-planner and per-cell
  Holm qualification (item 2).
- "The student is the best non-oracle / fast policy" in general (§2.1, only 1/5 cells).
- "The student beats the best heuristic" without the pilot-choice qualifier.
- "H6b replicates on fresh episodes" (only the direction does).
- "DAgger helps", "DAgger is needed", "most accuracy comes from BC on G\*", or any "effective component" claim.
- "DAgger and BC are equivalent".
- "No dependence on travel cost" (H5b is uninformative).
- "The student is reliably not more than 4 pp better" on the fresh window, or "student BI lower in S2" as a finding.
- "Contrasts of a few pp are within evaluator noise" (say *sensitivity* instead, per item 19).
- "p = 0" (write p < 1e-4, the bootstrap resolution).
- Fresh-window numbers or latency ratios without their stated caveats.
- Any hardware or real-robot claim.

### 4.6 Escalation to the owner (for the main session to file in `OWNER_TODO.md`)

- **(a) Cap and decision.** The refine-cycle cap (5, owner-authorised) is used up. Stage 15 decided PROCEED with a
  measurement paper plus the narrow H6b frontier claim.
- **(b) Results in brief.**
  - H6a: parity with G\* is not shown, and no difference is shown.
  - H6b: 7/10 Holm contrasts, 2/10 on the fresh window.
  - H6c: DAgger shows no benefit over BC.
- **(c) Target and schedule.** The target stays RSS 2027 Stage 1 (2026-12-04 AoE). The stage-20 gate is due by 12-01,
  otherwise the target becomes Stage 2 / CoRL 2027 per the 11-10 directive.
- **(d) No further loops.** No further experiment loop is recommended before Stage 1. If the owner later wants a v7 for
  the Stage 2 full paper (2027-04-16 AoE), the candidates are:
  - more G\* runs;
  - second runs of the reduced planners and H\*;
  - a pre-registered sub-16 read-out;
  - re-timed latency with dispersion.

  These would need an explicit `RESTRICTS.yaml` override.
- **(e) If the gate fails again.** If stage 20 fails on evidence-level grounds, the pipeline stops and asks, with
  Stage 2 / CoRL 2027 / RA-L / a workshop as the options.
