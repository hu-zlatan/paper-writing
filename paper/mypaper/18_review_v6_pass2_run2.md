# Stage 18 [v6] pass 2, run 2: peer review (RSS / CoRL reviewer pair)

Draft reviewed: the revised draft embedded in `paper/mypaper/prompts/stage18_v6_pass2_user.txt` (identical in body to
`paper/mypaper/v6/draft_v6_stage19pass1.md`, stage 19 pass 1). System role: balanced reviewer, strict on
methodology-evidence consistency. Reviewer A judges robot-learning significance and novelty; Reviewer B judges method,
statistics and claim support. Both reviewers read the whole prompt (instructions, draft, evidence a1-a3, b, c, d),
the amendment `docs/07c_amendment_v6_0.md` (with addendum v6.1), `code/analysis_v6.py`, `code/analysis_v6_posthoc.py`
and `code/touchbed/stats.py`, and the first-pass triage `paper/mypaper/18_peer_review.md`.

**CRITICAL FABRICATION: none found.**

| Reviewer | Focus | Score |
|---|---|---|
| A | robot-learning significance and novelty (RSS / CoRL) | **4 / 10** (borderline reject) |
| B | methodology, statistics, evidence-claim consistency | **5 / 10** (borderline) |

---

## 0. Independent verification (both reviewers, read-only)

### 0.1 Recomputed from raw jsonl

The reviewers wrote their own loader: `results/v6/test5/*.jsonl` merged with `results/v5/test5/*.jsonl` for episodes
< 300, the same rule as `analysis_v6.load`. It asserts 500 episodes for every method used. All values below match the
paper and `14_v6_analysis.json` exactly.

| Cell | G\* r1 / r2 | R-125 / R-500 | student (5 seeds) | r0 (BC) | H6a Δ | H6c Δ | first-action agreement |
|---|---|---|---|---|---|---|---|
| S2 | 0.518 / 0.532 | 0.406 / 0.462 | 0.4988 | 0.4856 | −0.0262 | +0.0132 | 0.274 |
| S4 | 0.496 / 0.494 | 0.402 / 0.390 | 0.4576 | 0.4492 | −0.0374 | +0.0084 | 0.402 |
| S8 | 0.432 / 0.464 | 0.356 / 0.372 | 0.4188 | 0.4116 | −0.0292 | +0.0072 | 0.452 |
| S12 | 0.434 / 0.434 | 0.358 / 0.390 | 0.4144 | 0.4140 | −0.0196 | +0.0004 | 0.426 |
| A16-2 | 0.474 / 0.498 | 0.330 / 0.374 | 0.4832 | 0.4884 | −0.0028 | −0.0052 | 0.314 |

- The H6b bootstrap was re-run with the frozen `crossed_bootstrap_diff`. S4 − R-125 gives +0.0556 [0.014, 0.098],
  p = 0.0072, and S12 − R-125 gives +0.0564 [0.013, 0.099], p = 0.0098. A16-2 − R-125 has p < 1e-4. All match Table 2.
- Under bootstrap seed 10, the reviewers get S4 − R-125 p = 0.0102 and S12 − R-125 p = 0.0104. Both match P2.
- Travel numbers were recomputed. S2 G\* is 0.820 rad, and the five students range 0.487–0.674 rad. S12 G\* is
  0.110 rad, and the students range 0.044–0.056 rad. Both match §5.3.
- Heuristics, RL and the strongest comparator were recomputed from the means. Every margin quoted in §5.1 and §5.3
  matches: +3.68 / +4.16 / +2.56 / +2.44 pp; best-heuristic margins +4.16 / +5.08 / +2.44 / +16.92 pp; B-spread
  0.006–0.074. The S12 tie R-500 = B-cov = 0.390 is real.

### 0.2 Post-hoc numbers (`results/v6/18_posthoc_v6.json`, `analysis_v6_posthoc.py` logic)

- **P1.** The JSON and the paper agree: S2 −1.6 [−8.6, +5.2], S4 +4.6 [−2.2, +11.6], S8 +5.0 [−0.6, +11.0],
  S12 −4.6 [−9.4, −0.2] and A16-2 −0.6 [−3.0, +1.2] pp. Only S12 excludes 0. The sub-8 and sub-16 point contrasts in
  `14_v6_analysis.json > E12` give the same shifts by subtraction: S4 −0.036 → +0.010 and S12 +0.008 → −0.038.
- **P2.** 7/10 under seeds 0–9 and 5/10 under seed 10 on 0–499, and 2/10 under all 11 seeds on 300–499. These are
  reproduced. Under seed 10, the S4 − R-125 p-value (0.0102) misses its rank-6 Holm cut (0.01). Step-down then stops,
  so S12 (0.0104) also falls, which explains why exactly these two drop out. The p ranges 0.0072–0.0124 and
  0.0076–0.0104 match.
- **Reviewer-run convergence check (new, post hoc, independent RNG, not a registered result).** The two marginal
  contrasts and the next one were re-run at **B = 100,000**: S12 − R-125 p = 0.0091, S4 − R-125 p = 0.0107, and
  S8 − R-500 p = 0.0316. With these values Holm rejects S12 at rank 6 (cut 0.01) and then S4 at rank 7 (cut 0.0125),
  giving **7/10**. A better-converged bootstrap therefore *supports* the 7/10. But the count still turns on whether
  min(p_S4, p_S12) ≤ 0.01, and the two values sit about one Monte Carlo SE either side of it. The paper says "a larger
  number of resamples was not run" (Limitation 3). This costs seconds of CPU and should simply be reported.
- **P3.** Table 4 matches `P3_checkpoint_epochs` cell by cell. The S2 held-out R̄ ranges (0.2803–0.2848 for r0,
  0.2776–0.2857 for r2) are correct.

### 0.3 Other checks

- **Latency.** The ratios match the E6 job-1 medians: G\*/R 19.0–47.0×, R/student 62–389×, and G\*/student
  2,544–9,767× as a ratio of medians. Per-component `half_width_ok` flags in `results/v5/14_e6_analysis.json` show the
  pre-registered half-width rule fails in S cells for G\* *and* for some reduced-planner medians (g125 in S2/S4/S8, g500
  in S4). The paper mentions only the G\*/student ratio. E6's own registered ratio field (a median of per-decision
  ratios) is 2,523–9,932×. The paper correctly calls its figure a ratio of medians, but should say it is not the
  registered statistic.
- **TOST.** The ci90 deficit bounds (−4.12 to −7.16 pp) and upper-margin p values (0.0014 … 0.0348) were checked, along
  with the fresh A16-2 upper-margin p (0.1557) and the 90 % half-widths. The half-widths are 2.84–3.86 pp: the A16-2
  upper half-width is 3.86 and the paper prints 3.85, which is trivial.
- **Other report-only numbers.** These all check out: the H5b slope (−0.0070 per 100°, ci95 [−0.137, 0.124]), the S8
  fresh G\* − student g_T p = 0.0068, the BI p-values, the H6c ci95 and fresh p range, and the S2/S12 look-ahead headroom
  (0.0658, 0.0422 in `results_v5.json`).
- **Trial counts.** 500 episodes per method per cell on 0–499 and 200 on 300–499. There are 5 student, 5 BC, 5 RL and
  5 success-RL seeds, 2 G\* runs and 1 run per reduced planner and heuristic, giving 27 / 22 policy instances. These
  match `episodes_per_method`. No inflated trial count was found.
- **Order of commits** (`git log`). The amendment v6.0 and the `--run-salt` change came at 01:44 UTC, then
  `analysis_v6.py` at 01:47 and addendum v6.1 at 01:57. The first v6 result commits are at 02:06–02:09 on 2026-11-10.
  The script-before-data claim holds.
- **Statistics actually in the code.** Only `crossed_bootstrap_diff`, the margin-shifted bootstrap TOST and `holm` are
  used. The paper claims nothing else, so there are no phantom tests.
- **DAgger warm start.** Confirmed in `code/tools_v5_manifests.py:72`: `--init … _r{r-1}.npz`.

---

## Reviewer A: robot-learning significance (RSS / CoRL)

### Summary
The paper measures whether a DeepSets policy, distilled by BC plus two DAgger rounds from a cost-aware greedy
EIG touch planner, is a better fast policy than two "shrunken" versions of that planner. It works in a planar
simulator over five cells (κ = 2/4/8/12 on library S, κ = 2 on library A16). The student beats the smaller reduced
planner in 5/5 cells and the larger one in 2/5. Parity with the full planner is undecided. DAgger adds nothing
detectable over BC. Success outcomes are sensitive to the evaluator grid and to the planner's own Monte Carlo noise.

### Strengths
1. **Unusually honest reporting.** Every weakness raised in the first pass is now disclosed in the abstract, C1–C4 or the
   limitations: the bootstrap-seed fragility, the fresh window only replicating direction, single-run reduced planners,
   the DAgger warm start with early checkpoints, and the TOST power. Robotics papers rarely do this.
2. **Teacher variance is treated as part of the target.** The second independent G\* run and the 25–45 % first-action
   agreement are a useful, transferable observation for anyone distilling a sampling-based planner. Two planner runs
   differ by up to 3.2 pp, which is as large as the student − teacher gaps.
3. **Paired design.** Within a window, every method shares state, start angle and observation stream, and the
   pre-registered read-out script was committed before any data existed. Both were verified.
4. **The comparison is framed correctly.** Measuring a distilled policy against cheaper versions of its own teacher is
   the comparison a practitioner needs, and the related work rarely reports it.

### Weaknesses
1. **The practical stakes of the latency axis are not established.** R-500 already decides in 48–194 ms, and even full
   G\* takes 0.9–4.9 s. A physical probe (approach, contact, retract, plus travel) on a real arm takes on the order of a
   second or more. Without even a crude task-time model, the reader cannot tell whether "62–389× faster than a reduced
   planner" changes episode time at all. Planning could also overlap with motion. For RSS / CoRL this is the central
   significance gap. Limitation 6 discloses it, but disclosure does not supply the missing evidence.
2. **The shrink baseline is weak.** It is single-threaded numpy, the 512 candidates are fixed, and there are two points
   with the same N·M. There is no vectorised or GPU G\*, no candidate subsampling, no pruning, and no cheap
   information-based heuristic. A competent robotics engineer would try these before training a student. "Distillation
   beat these two reduced planners" is true, but these are the easiest reduced planners to beat. The paper says so
   (§6.2) but cannot repair it.
3. **Novelty is thin for a robot-learning venue.** Distilling an information-gathering expert with DAgger is established
   (Choudhury 2017; Nguyen 2024). The positive result here is narrow: 7/10 contrasts, 2/10 on fresh data, and only one
   of five cells beats the strongest non-oracle comparator. The two methods findings (evaluator sensitivity and teacher
   stochasticity) are the most transferable content, but the evaluator finding rests on 100 episodes, and only 1/5 cells
   has an interval that excludes 0.
4. **Low absolute performance and a narrow task.** Every policy succeeds on only 0.21–0.53 of episodes. The setup is one
   planar fingertip on a fixed circle, with the planner, filter and evaluator all sharing one likelihood. So the
   "frontier" is measured in a regime where every method usually fails. Neither library (8 or 16 planar polygons)
   speaks to 3D or real-contact generalisation.
5. **The DAgger ablation does not test DAgger.** Checkpoints are selected by regret on *teacher*-visited states, which
   by construction cannot see covariate shift. Several kept round-2 networks are within 0–10 epochs of their
   initialisation. C3 now says exactly this, but the result therefore carries little information for practitioners.
6. **The framing came after the null.** Appendix A discloses that the frontier framing (H6b) was adopted after the
   earlier phase failed its parity gate in 5/5 cells. The v6 tests were prospective, and the reviewers verified the
   commit order. But the title's "Pre-Registered" refers to an internal, git-timestamped registration made in the fifth
   refine cycle of a pipeline, not to an external registry. The wording should say so.
7. **Length and presentation.** The body is about 10,500 words, and the revision grew the draft from about 8,900 to
   about 11,600 words. That is far over an 8-page RSS / CoRL limit. Figure 1 is still a prompt, not a figure, and three
   `[CITE-MISSING]` markers remain (DeepSets, Efron, Holm). The text is saturated with qualifiers ("post hoc, no CI,
   report-only, derived") to the point that the main result is hard to extract on a first read.

### Actionable revisions
1. Add a task-time model, even a back-of-envelope one: probe stroke duration × κ travel, compared with decision latency,
   with and without overlap. State in which cells R-500 or G\* latency would actually lengthen an episode. If R-500 is
   already below the probe time, say plainly that the frontier gain is computational, not operational.
2. Reframe the contribution as a measurement and methods note. Lead with C4 and teacher variance, which transfer beyond
   this task. Present C1 as a bounded comparison against one shrink family.
3. Cut to 8 pages. Move Table 4, Appendix A, the strongest-comparator paragraph and most of the RL/heuristic rows to the
   supplement. Bring the abstract under 200 words (it is 240).
4. Render Figure 1 and fill the three citations.
5. Retitle or qualify "Pre-Registered", for example "internally pre-registered (time-stamped commits)".

**Recommendation:** not ready for RSS / CoRL. The work is sound as a measurement, but its robotics significance is
unestablished, the baselines are narrow, and the positive claim is small. **Score: 4 / 10.**

---

## Reviewer B: methodology and evidence-claim consistency

### Summary
The revised draft is now accurate. Every headline number the reviewers recomputed matches the raw records or the
frozen read-out, and every number quoted from the post-hoc file matches it. The decisions follow the registered rules
in `docs/07c_amendment_v6_0.md`: H6a difference and TOST with Holm over 5, H6b with Holm over 10, and H6c with Holm
over 5, separately per window. Report-only and post hoc labelling is consistent. The remaining issues are about
statistical robustness and wording, not discrepancies.

### Strengths
1. **Method matches evidence.** The bootstrap, TOST, Holm, windows, seeds and episode counts in §4 and Table S
   match the code and JSON exactly. There is no statistical test in the paper that the code does not run.
2. **The fragility of the headline count is disclosed and quantified.** P2 is reported in the abstract, C1, §5.1,
   Limitation 3 and Appendix B, and the reason the two contrasts drop out is correct.
3. **The TOST power is reported honestly.** The pre-registered design note is quoted, and the observed half-widths and
   the unadjusted reachable gap (0.15–1.16 pp) are given. The deficit-side ci90 bound is offered as the informative
   quantity. This is the right treatment of a designed-in null.
4. **The E12 shift now has uncertainty.** "Comparable to the margin" is now limited to point values, and the interval
   excludes zero only in S12.

### Weaknesses
1. **The Holm count still hangs on Monte Carlo resolution.** The reviewers' B = 100,000 run (§0.2) gives 7/10, but the
   decisive p-values (0.0091 and 0.0107) straddle the rank-6 cut of 0.01. The paper should report a converged bootstrap
   p, for example B = 10⁵–10⁶ for the H6b family, as a post-hoc robustness row. Saying a cheap analysis "was not run"
   is not a limitation the authors need to carry.
2. **Variance components are missing from H6b and poorly estimated in H6a.** The reduced planners contribute one
   "seed", so their intervals ignore run-to-run variance. The paper's own G\* rerun shows that variance is up to 3.2 pp,
   which is half the lower H6b effect sizes. H6a resamples over two G\* runs, so about half of the resamples use one run
   twice. Both points are disclosed. A simple sensitivity check would bound the H6b consequence: inflate the
   reduced-planner variance by G\*'s observed run-to-run variance and recompute. It needs no new runs.
3. **Wording errors that remain.**
   - The abstract says "every method runs the same 500 test episodes", but Random was not extended. §4 states this
     correctly.
   - "The student clears it at the registered level in 1/5 cells" (§5.1, C1) applies a registered test to a
     comparator chosen post hoc. Better: "the registered H6b contrast against that comparator is rejected in 1/5 cells".
   - The latency half-width failure also affects reduced-planner medians in S2, S4 and S8, not only the G\*/student
     ratio. The ratios of medians differ from E6's registered ratio field (2,523–9,932×), which should be noted.
   - "Half-widths 2.84–3.85 pp": the A16-2 upper half-width is 3.86. This is trivial.
4. **Sensitivity of H6b to the evaluator grid is unknown.** E12 did not re-read the reduced planners. Because the
   evaluator shifts student − G\* by up to 5 pp at point level, the 5–15 pp H6b effects are probably robust, but this is
   not shown. This is disclosed.
5. **Reuse of seen data.** H6a on 0–499 reuses 300 episodes already seen for the students and G\* run 1, and H\* comes
   from a pilot of the earlier phase. Both are disclosed. The fresh-window numbers are the clean prospective result and
   could be given more weight in C2.
6. **Topic discipline.** The paper mostly stays on topic. Residual process and environment material does not belong in
   a paper body and should move to a reproducibility appendix: "refinement budget was used" (Limitation 15),
   "time-guarded and resumed", "GitHub-hosted 2-core runners", the 733 CPU-h pilot and Appendix A's phase narrative.
   None of it is presented as a contribution.
7. **Length check (task rubric).** No section is under length. The words per section are: Abstract 240, Introduction
   1,103, Related Work 709, Method 2,170, Experiments 1,334, Results 2,352, Discussion 1,194, Limitations 706,
   Conclusion 296, Appendices 449. The body totals about 10,500 words. The problem is the opposite of under-length: the
   draft is roughly 1.4–1.6× a 9-page budget.

### Actionable revisions
1. Report the H6b family at B ≥ 10⁵ (post hoc), using the reviewers' numbers or the authors' own, and state the count
   it gives.
2. Add the variance-inflation sensitivity for H6b, which needs no new runs. State how many of the 7 rejections survive
   when the reduced-planner term carries G\*-sized run-to-run variance.
3. Fix the four wording items in Weakness 3.
4. Move the process and environment material to a reproducibility appendix.
5. Shorten to venue length without dropping any qualifier that bears on a claim. Remove repetition instead: the
   7/10, 5/10, 2/10 statement appears at least six times.

**Recommendation:** borderline. The paper is now methodologically clean and claim-accurate, but the evidence is thin
for a top venue. **Score: 5 / 10.**

---

## Status of the first-pass triage (`paper/mypaper/18_peer_review.md`)

| # | Triage item | Status in the revised draft |
|---|---|---|
| 1 | H6b fragility and fresh window up front | **Fixed.** The abstract, C1, §5.1, Appendix B and the Figure 1 caption all give 7/10, 5/10 under one of 11 seeds, and 2/10 fresh, and call the reduced planners single-run with the same budget. |
| 2 | C3 softened; warm start and kept epochs disclosed | **Fixed.** This is covered in Algorithm 1 step 3, §3.3 qualifiers, Table 4, §5.3, Limitation 9 and the wording "no DAgger benefit detected under this recipe". |
| 3 | C4 with P1 ci95 | **Fixed.** §6.1, C4, the abstract and Limitation 5 now say "point values … ci95 excludes 0 in S12 only". |
| 4 | TOST power framing | **Fixed.** The design note is quoted, observed half-widths are given, and there is no "500 sufficed" claim. |
| 5 | Number wording (5–8 pp, S12 tie, "unadjusted" label, TouchBED defined) | **Fixed.** TouchBED appears in the title before its definition in §1, which is acceptable. |
| 6 | External reader / length (history to one sentence, abstract < 200 words, CITE-MISSING, Figure 1) | **Not fixed / partly fixed.** History is one sentence in §1 but still 369 words in Appendix A and 19 mentions of "earlier/first phase". The abstract is 240 words, still over 200. The draft *grew* from about 8.9k to 11.6k words. Three CITE-MISSING markers remain and Figure 1 is unrendered; both were deferred to stages 22–23 by plan. |
| 7 | Limitations additions | **Fixed.** Limitations 1–4 and 6 cover every listed item. |
| — | Evidence-level requests | **Not addressed, by design** (the refine cap was used). They remain the main barrier: a comparator near the student's latency, reduced-planner reruns, E12 on the reduced planners, and a task-time model. |

## Top remaining actions (priority order)
1. Add a task-time model (probe and travel duration against decision latency), or recast the latency gain as purely
   computational.
2. Report H6b at a converged bootstrap (B ≥ 10⁵; the reviewers get 7/10, with p = 0.0091 and 0.0107 at the margin),
   plus a reduced-planner variance-inflation sensitivity. Neither needs new runs.
3. Cut to venue length: an abstract under 200 words and a body of about 7–8k words, with history and process material
   moved to the supplement.
4. Render Figure 1 and fill the three CITE-MISSING references.
5. Fix the wording items: "every method" in the abstract, "registered level" for the post-hoc strongest comparator, the
   latency half-width scope and ratio statistic, and "pre-registered" qualified as internal.
