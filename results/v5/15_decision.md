# Stage 15 · Research decision (v5)

> System (verbatim, `results/v5/prompts/stage15_system.txt`): "You are a research program lead making go/no-go
> decisions."
> Task (verbatim opening and output spec, `results/v5/prompts/stage15_user.txt`): "Make a PROCEED, REFINE, or PIVOT
> decision from analysis. … Output markdown with: Decision, Justification, Evidence (with cited numbers from the
> analysis), Next Actions (specific stage and tasks)." `{analysis}` = the merged stage-14 [v5] report (pass 1 body plus
> pass 2, whose items S1–S3, M1–M8 and m1–m8 are binding and replace the pass-1 sentences they cite).
>
> Fresh subagent, 2026-11-09. Inputs read: `results/v5/prompts/stage15_system.txt`,
> `results/v5/prompts/stage15_user.txt` (in full), `pipeline/references/stage_prompts/research_decision.md` (hard rules),
> `RESTRICTS.yaml`, `results/v4/15_decision.md`, `OWNER_TODO.md`. No other file was read and no code was run. Every
> number below is quoted from the stage-14 analysis. Where pass 2 rewrote a pass-1 sentence, the pass-2 wording is used.
> Numbers marked *(derived)* are my own arithmetic on quoted values; they have no CI.

---

## 1. Decision

**PROCEED to stage 16, in the characterisation (measurement-paper) sense only, as in v4.** The paper reports a
pre-registered, five-cell measurement. Its headline is that the distilled student is **not shown to match G\***. It is
**not** a method paper. The template's PROCEED hard rule is **not met in its method sense** (§2.1).

**How the conflict is resolved.** The PROCEED rule is not met, but REFINE is not available:
- `RESTRICTS.yaml` sets `loops.max_refine_cycles: 4`, raised from 3 on the owner's instruction for v5. v5 is the 4th
  loop, so the cap is used up. With `escalate_on_cap_hit: true`, a REFINE or PIVOT can only go to the owner as a
  request. It cannot start a v6.
- REFINE would also be the wrong call on its own terms (§2.2). PIVOT is not warranted (§2.3).

So I take the only executable option that keeps the record honest. That option is a measurement paper whose claims are
limited to settled, pre-registered verdicts plus labelled exploratory rows (§4.3–§4.4). Alongside it, the fact that the
method-sense PROCEED rule failed goes to the owner (§4.5). This is the same resolution as v4 §1, applied to the larger
v5 record.

---

## 2. Justification

### 2.1 The PROCEED hard rules, applied as written

| Hard rule (`research_decision.md`) | Status | Reason |
|---|---|---|
| Primary metric difference between proposed method and best baseline is statistically meaningful (p < 0.05, or effect > 0.5σ across seeds) | **Not met (method sense)**. Partly met only against the pre-registered pilot-chosen H\* | See below. |
| Every claimed "effective component" has a non-degenerate ablation | Vacuous, so met | The paper claims no effective component, and no sentence may claim one (§4.4). |
| No CRITICAL FABRICATION flags from stage 14 | Met | Pass 2 checked "all tables in pass 1 (sections 1.1–1.4, 2.1–2.4) … cell by cell" and found that they "match the JSON". It found **no** pre-registered verdict wrong. Its S/M/m items concern interpretation, not fabrication. |

**Why the first rule fails in the method sense.**

1. **The pre-registered primary contrast is the student against G\* (D5 / H5a), and it fails.**
   - D5 fails in 5 of 5 cells, so m = 0.
   - Validation Δ̂_succ ranges from −3.24 to −5.96 pp. S4 (−5.48) and A16-2 (−5.96) already lie beyond δ = 4 pp.
   - All 25 per-seed differences are negative.
   - On test5 the student is below G\* in every cell, by −0.2 to −2.53 pp, with no Holm rejection. Every ci95 lower bound
     lies beyond −δ (−6.13 to −8.33 pp).
   - So the primary contrast is neither a match nor a shown difference. Per pass 2 S1, "matching G\* is not supported."
2. **The student against the pilot-chosen heuristic H\* (pre-registered).** This success contrast is Holm-significant
   in 4 of 5 cells (S2 is not: p 0.0558).
   - It meets the letter of the p < 0.05 disjunct, but only against the *pilot-chosen* heuristic.
   - In 4 of 5 cells H\* is **not** the best heuristic on test5 (pass 2 M2). Against the best test5 heuristic the
     post-hoc margin falls to +3.5 to +14.5 pp, with no CI and no test.
3. **The student against the best non-oracle baseline on test5, cell by cell.** Recovered *(derived)* from G\*
   success + student−G\* diff, and student − student−RL diff:

   | Cell | Student mean *(derived)* | Best non-oracle baseline on test5 | Margin | Test? |
   |---|---|---|---|---|
   | S2 | 0.5087 | b_cov 0.45 (= H\*) | +5.87 pp | ci95 [−0.13, +11.8], p 0.0558, **not significant** |
   | S4 | 0.4713 | b_cov 0.42 (RL ≈ 0.4167 *(derived)*) | +5.13 pp *(derived)* | none (post-hoc) |
   | S8 | 0.4440 | cfg-6 RL ≈ 0.412 *(derived)* (b_fan 0.3833) | +3.2 pp | ci95 [−1.47, +7.93], p 0.19, **not significant** |
   | S12 | 0.4413 | b_cov 0.4067 (RL ≈ 0.3687 *(derived)*) | +3.47 pp *(derived)* | none (post-hoc) |
   | A16-2 | 0.488 | b_cov 0.3433 (RL ≈ 0.222 *(derived)*) | +14.47 pp *(derived)* | none (post-hoc) |

   So against the strongest non-oracle comparator in each cell, no tested contrast clears p < 0.05. In the two cells
   where a test exists (S2, S8), it does not.
4. **The effect-size disjunct (> 0.5σ across seeds).** It cannot be evaluated from the analysis, because per-seed SDs of
   the contrasts are not reported. As in v4, I do not reach for it after the fact; doing so would break
   `forbid_unsupported_claims`.

**The sense in which I proceed** is the same standard as v3 and v4 (`results/v4/15_decision.md` §2.1). Every claim in
the paper must:
- be the outcome of a pre-registered rule, evaluated as written on complete data;
- be worded within what that outcome licenses.

Anything else is labelled exploratory and given its interval. All decision-bearing items in v5 are settled:
- D5: 0/5, no remedy step by pre-registration.
- H5a test5: 0/5 Holm.
- Student − H\*: 4/5 Holm.
- H2-v5: 1/5 (A16-2).
- Inversion: 0/5.
- H5b: no trend detected.
- test5 complete in all cells; weights hashed in `13_freeze.json`.

The remaining open items are wording or report items (§2.4). A measurement paper is therefore licensed. A method claim
is not.

### 2.2 Why not REFINE

- **It cannot run.** The cap is 4/4, and v5 is the owner-authorised maximum. Without the owner, a REFINE is only an
  escalation (§4.5).
- **Its precondition fails.** REFINE assumes "the hypothesis is correct". The amortisation hypothesis (the student
  matches G\* within δ) has now failed its pre-registered gate in every cell tested across v3–v5:
  - S12 (D3, twice);
  - S2 (D4);
  - all five v5 cells (D5, 0/5, with 5 seeds per cell and a fresh test set).
  These were exactly the fixes that v4's gate review asked for ("more seeds, more conditions").
- **The fixes left on the table would re-decide D5 after seeing it fail.** v5 pre-registered "no remedy step" for D5.
  Retraining students, re-tuning RL per cell, or raising test5 from 300 to 500 episodes after unblinding would all be
  post-hoc. The weaknesses that remain all bear on *secondary* rows, not on the primary verdict, which fails on
  validation regardless of test5:
  - RL is transferred from S2 and collapses in A16-2;
  - H\* was chosen on a 200-episode pilot;
  - G\* was run once per cell;
  - the latency CI rule is met in only 1/5 cells.
  They go into the limitations.

### 2.3 Why not PIVOT

- **The hypothesis is not "clearly wrong across the board".** The student beats the pilot-chosen H\* in 4/5 cells
  (Holm). It sits 0.2–2.5 pp below G\* on test5, and it decides 2,523–9,933× faster on seed-701 timings. What failed is
  the *matching* claim, not the existence of a useful amortised policy.
- **No new hypothesis emerges that could be tested before 2026-12-04.**
  - The most interesting open questions are why the student travels less than G\* in every cell, and why g_T and BI rank
    policies differently. They are methods observations for the paper.
  - A pivot means a new pre-registration and new runs (stage 8 onward). That is outside the cap and outside the time
    left: 25 days to the deadline *(derived: 2026-11-09 → 2026-12-04)*.

### 2.4 Open items: none blocks drafting, each binds the wording

1. **Validation vs test5 gap** (validation −3.2 to −6.0 pp, test5 −0.2 to −2.5 pp).
   - D5 is decided on validation. Pass 2 M1 shows the D5 rule applied to test5 would still fail in about 4/5 cells, so
     test5 does not contradict D5.
   - Report both splits separately with their intervals (pass 2 S2). Note that S2 and S12 validation use v4 and v3 G\*
     files.
2. **Latency.** The CI completeness rule is met only in A16-2. The ratios rest on seed 701, with about 24 % within-cell
   spread (M4, m2). Report the range with that caveat. No re-timing.
3. **Heuristic-selection optimism** (M2). Report the pre-registered H\* contrast as the verdict. Report the margins
   against the best test5 heuristic beside it, labelled post-hoc, with no CI.
4. **RL in A16-2** (M7, m6). Any student-vs-RL statement about A16-2 carries the collapse caveat (2.0 of n\* = 3 probes
   in 4/5 seeds).
5. **E5 / E7** are report-only, worded per M8 and M6.

---

## 3. Evidence (quoted from the stage-14 [v5] analysis)

### 3.1 Pre-registered gate D5 (val3, 500 episodes, δ = 0.04)

| Cell | Student | G\* | Δ̂_succ | Threshold | Δ̂_BI (≥ −0.15 passes) | Cell |
|---|---|---|---|---|---|---|
| S2 | 0.4812 | 0.514 | −0.0328 | −0.01454 | −0.0682 ✓ | fail |
| S4 | 0.4492 | 0.504 | −0.0548 | −0.01503 | −0.1334 ✓ | fail |
| S8 | 0.4116 | 0.448 | −0.0364 | −0.01639 | −0.0465 ✓ | fail |
| S12 | 0.4136 | 0.446 | −0.0324 | −0.01722 | −0.0635 ✓ | fail |
| A16-2 | 0.4124 | 0.472 | −0.0596 | −0.01229 | −0.0629 ✓ | fail |

- m = 0 of 5.
- Per-seed differences run from −0.068 to −0.01, and all are negative. No A16-2 seed passes.
- G\* sources: S2 from v4, S12 from v3, the other cells from v5.

### 3.2 test5 (300 episodes per method, crossed episode × seed bootstrap)

**Student − G\*, success.**

| Cell | Diff | ci95 | p | Holm |
|---|---|---|---|---|
| S2 | −0.02467 | [−0.076, +0.02667] | 0.3526 | no |
| S4 | −0.02533 | [−0.08333, +0.03267] | 0.3888 | no |
| S8 | −0.01267 | [−0.06133, +0.03733] | 0.63 | no |
| S12 | −0.01533 | [−0.06333, +0.03267] | 0.5378 | no |
| A16-2 | −0.002 | [−0.06267, +0.06067] | 0.9572 | no |

- CI widths are 9.6–12.3 pp (m1).
- A shortfall of up to 6.1 pp is consistent with the data in every cell, and up to 8.3 pp in S4 (M3).

**Student − G\*, BI.** The ci95 excludes 0 in S4 (−0.1314) and S12 (−0.0910). These are uncorrected. A16-2 is
+0.08477, with a CI that includes 0.

**Student − H\*, success.**

| Cell | H\* | Diff | ci95 | Holm |
|---|---|---|---|---|
| S2 | b_cov | +0.05867 | [−0.00133, 0.118] | no |
| S4 | b_fan | +0.098 | [0.04667, 0.1487] | yes |
| S8 | b_cov | +0.07067 | [0.01667, 0.1247] | yes |
| S12 | b_fan | +0.06133 | [0.01067, 0.112] | yes |
| A16-2 | b_fan | +0.168 | [0.106, 0.23] | yes |

H\* is not the best test5 heuristic in S4, S8, S12 and A16-2. Against the best test5 heuristic, the post-hoc margins are
+5.13 / +6.07 / +3.47 / +14.47 pp, with no CI.

**Student − RL (cfg 6, tuned on S2), success, uncorrected.**

| Cell | Diff | ci95 |
|---|---|---|
| S2 | +0.08467 | [0.03067, 0.1373] |
| S4 | +0.05467 | [−0.002, 0.11] |
| S8 | +0.032 | [−0.01467, 0.07933] |
| S12 | +0.07267 | [0.02467, 0.1207] |
| A16-2 | +0.266 | [0.1993, 0.33] |

In A16-2, RL seeds 712–715 use 2.0 probes against n\* = 3, with success 0.1833–0.2267.

**H2-v5 (one-sided 95 % LB of student − RL on g_T, against +0.10).**

| Cell | LB |
|---|---|
| S2 | −0.4971 |
| S4 | −0.6555 |
| S8 | −0.4861 |
| S12 | −0.3044 |
| A16-2 | +0.5964, met |

- In A16-2, G\* also beats RL by 0.854 nats [0.567, 1.144] (M7).
- Inversion is false in all cells.

**H5b.**
- Slope −0.01571 per rad, ci95 [−0.1041, 0.07277]. The verdict is "no trend detected over 5 cells".
- Across the observed travel span of 0.1112–0.8213 rad, a change of about −7.4 to +5.2 pp cannot be excluded (S3,
  derived in the analysis).

**Behaviour.**
- The student travels less than G\* in every cell. For example, in S2 the student travels 0.500–0.668 rad against
  0.8213 for G\*.
- RL travels more than both.
- Probe counts: student 2.9–4.0, G\* 2.93–3.97.

### 3.3 Cost and report-only checks

- **E6 latency.**
  - Student median: 0.326–0.500 ms (seed 701).
  - Full-G\* / student median ratios: S2 9,933×, S4 6,990×, S8 3,463×, S12 2,523×, A16-2 8,301×.
  - The half-width rule is met only in A16-2.
  - Other seeds' student medians differ by up to about 24 % within a cell (M4).
- **E5 (sub-8 → sub-16).**
  - The flip rate is 6.5–8 % for one seed, on 200 episodes in 2 cells.
  - The student−G\* contrast shifts by +0.02 (S2) and −0.03 (S12).
  - Mean |ΔBI| is at most 0.004 nats.
- **E7.** The 512-minus-32 independent-estimate gap is +0.048 nats in S2 and +0.018 in S12 (n = 32 beliefs). It is not
  linked to the deployed G\* or to success (M6).
- **Bootstrap resolution.** p = 0.0 means p < 0.0002 (m3).

### 3.4 Weaknesses (stated, not fixable inside the cap)

- **G\*.** Run once per cell, so its run-to-run variance is missing from the CIs (M5).
- **H\*.** Chosen on a 200-episode pilot (M2).
- **RL.** One S2-selected configuration reused everywhere. It visibly fails only in A16-2 (m6). RLsucc was run only in
  S2 and S12.
- **test5 size.** Cut from 500 to 300 episodes (addendum v5.1e).
- **Multiplicity.** More than 30 uncorrected BI, RL and g_T contrasts.
- **Scope.** Simulation only (TouchBED), two shape sets, one κ for A16, sub-8 read-out.

---

## 4. Next actions

### 4.1 Record completion (report-only, no new runs, by 2026-11-12)

These tasks change no threshold, cell, seed, metric or verdict, and none of them is a REFINE.

1. Write the post-hoc derived values into `results_v5.json`, with provenance ("arithmetic on existing fields, not
   pre-registered, no CI"), so the paper can cite them:
   - the margins against the best test5 heuristic (M2);
   - the student means recovered from the diffs (§2.1);
   - the latency ratios against the job-2 student medians (M4);
   - the H5b span translation (S3).
2. Correct the owner-facing summary in `OWNER_TODO.md` (run-36 update). It currently reads "稳定落后 G\* 约 3–6 个百分点"
   ("consistently 3–6 pp behind G\*"). That range is validation-only. Replace it with the S1 wording: validation 3.2–6.0
   pp; test5 0.2–2.5 pp, with CIs down to −8.3 pp; gate failed in all cells. Filing this is for the main session; this
   decision edits no other file.
3. **Not to be run:**
   - any retraining or remedy round;
   - per-cell RL re-tuning;
   - more test5 episodes;
   - a G\* rerun for seed variance;
   - latency re-timing;
   - a CI or test for the post-hoc best-heuristic margins;
   - any new test of BI or g_T.
   Each of these goes into the limitations.

### 4.2 Stage 16 (paper outline), from 2026-11-09, in parallel with §4.1

- **Frame.** A pre-registered, five-cell characterisation of amortising a cost-aware information-gain touch planner (G\*)
  by distillation, across travel cost κ = 2/4/8/12 and a second shape set. The v3/v4 record (S12 D3, S2 D4) enters as
  prior cells.
- **Contributions, in order:**
  - **C1, learnability across five cells.** D5 fails in 5/5. The student is below G\* in every cell on both splits and is
    not shown within δ. Pair this with the v3/v4 gate failures.
  - **C2, a cheap policy that beats pilot-chosen heuristics.**
    - The student beats the pre-registered H\* in 4/5 cells (Holm).
    - Beside it go the post-hoc best-test5-heuristic margins and the latency range with its caveats.
  - **C3, distillation vs RL.**
    - H2-v5 is met only in A16-2, where RL collapses.
    - Inversion is false everywhere.
    - The student−RL success rows are uncorrected.
  - **C4, travel cost and behaviour.**
    - H5b: no trend detected, about 7 pp not excluded.
    - The student travels less than G\* in every cell.
  - **C5, methods note.** E5 evaluator resolution, E7, the g_T / BI ordering difference, and the val/test reporting.
- **Venue.** RSS 2027 Stage 1 extended abstract, ≤ 5 content pages + 1 reference page. Preliminary experiments are
  allowed. Lead with C1 and C2. C3 and C4 get one paragraph each. C5 goes into methods and limitations.
- **Schedule (pipeline estimate, not official).**
  - Stages 16–20 produce a draft by 2026-11-22.
  - The stage 20 gate and the citation audit follow.
  - The abstract is in `paper/` by 2026-12-01, so the owner can check and submit by 2026-12-04 AoE.
  - This follows owner choice (c): "若 12-01 前走完第 20 阶段就准备 RSS Stage 1" ("if stage 20 is done before 12-01,
    prepare RSS Stage 1"). Otherwise the target becomes the Stage 2 full paper or CoRL 2027, decided by the owner.

### 4.3 What the paper may claim (exact scope)

- **D5.** "The pre-registered gate failed in all five cells (m = 0). The student is below G\* in every cell on both splits
  (validation 3.2–6.0 pp, with S4 and A16-2 beyond the 4 pp margin; test5 0.2–2.5 pp, CIs down to −8.3 pp), so matching
  G\* is not supported." (S1)
- **Splits.** Report them separately, with intervals. No pooled estimate. (S2)
- **D5 on test5.** Test5 does not contradict D5: the D5 rule would still fail in about 4/5 cells. (M1)
- **Heuristics.** The student beats the pilot-chosen H\* in 4/5 cells after Holm (+6.1 to +16.8 pp). Against the best
  test5 heuristic, the post-hoc margin is +3.5 to +14.5 pp, with no CI. (M2)
- **RL.** Uncorrected student−RL success CIs exclude 0 in S2, S12 and A16-2. A16-2 is confounded by RL collapse. (m7)
- **H2-v5.** Met only in A16-2, and it reflects RL failing to transfer. (M7)
- **H5b.** No trend detected, and a change of up to about 7 pp across the observed travel range cannot be excluded. (S3)
- **Latency.** Full G\* is 2,523–9,933× slower per decision (seed-701 median ratios; CI rule met only in A16-2; about
  24 % within-cell seed uncertainty). (M4, m2)
- **Report-only items.** E5, E7 and the v4 comparison use the M8, M6 and m8 wording.

### 4.4 What the paper may not claim

- "The student matches / reaches / is equivalent to G\*", or any wording that the gap to G\* is "small" or "negligible".
- A pooled "true gap of 1–5 pp".
- "Consistently 3–6 pp behind" as a headline, because it is validation-only.
- "Test5 contradicts / overturns D5".
- "No dependence on travel cost".
- "The student beats the best heuristic" without the pilot-choice qualifier and the post-hoc margins.
- "Distillation beats RL", or "the student beats RL" without the multiplicity and A16-2 caveats.
- A16-2 H2-v5 as a student advantage.
- "G\* is deterministic". "G\* is sub-optimal" or "G\* has headroom in success terms".
- A blanket "~7,000–10,000× faster".
- "A 6–8 pp shortfall is consistent in every cell".
- "RL is under-tuned in S4/S8/S12".
- "p = 0".
- Any "effective component" claim.
- Any cross-cell comparison worded as a finding beyond H5b.
- Any claim that v4's −10.2 pp was formally refuted.

### 4.5 Escalation to the owner (for the main session to file in `OWNER_TODO.md`)

The owner should be told five things:
- (a) The refine-cycle cap (4, owner-authorised) is used up. The method-sense PROCEED rule is still not met: D5 fails in
  0/5 cells, and no tested contrast against the strongest per-cell non-oracle baseline is significant. The pipeline is
  therefore proceeding with a measurement paper, not a method paper.
- (b) No further experiment loop happens without an explicit owner override of `RESTRICTS.yaml`.
- (c) The default target stays the RSS 2027 Stage 1 extended abstract (2026-12-04 AoE), with a draft by about 11-22.
  The owner registers and submits; the pipeline does not.
- (d) If the stage 20 gate again fails on evidence-level grounds, it cannot loop. The pipeline will stop and ask, with
  the RSS Stage 2 full paper, CoRL 2027, RA-L or a workshop as the options.
- (e) The run-36 "3–6 pp behind" summary is validation-only and is being corrected (§4.1, task 2).
