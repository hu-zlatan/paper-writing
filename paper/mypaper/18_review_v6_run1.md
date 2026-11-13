# Stage 18 Peer Review (v6, run 1)

Paper: "Amortizing a Cost-Aware Information-Gain Touch Planner: A Pre-Registered Accuracy–Latency Study in TouchBED" (Stage 17 v6 draft, 2026-11-13).
Reviewer stance: balanced, strict about whether the methods match the evidence.

## 0. Verification performed

I checked every number below against the JSON of record and recomputed the headline contrasts from the raw per-episode jsonl records.

- **JSON cross-check.** I dumped every H6a/H6b/H6c/E12/frontier/v5_row_updates/H2/H5b field of `results/v6/14_v6_analysis.json` for all 5 cells × 2 windows, plus `results/v6/15_derived_v6.json` and the v5 blocks the paper cites in `results/v5/results_v5.json` (`14_e6_analysis`, `12_e7_analysis`, `12_d5_analysis`, `12_cal_analysis`, `12_base_hstar`, `12_rl_sweep_selection`, `16_report_rows`, `14_test5_analysis`). I compared them with Tables 0/1/2/3, Table S, the Figure 1 data table and every inline number in Sections 1, 5, 6, 7 and 8.
- **Independent recomputation from raw jsonl.** My own loader and crossed episode × seed bootstrap (4,000 resamples, different RNG) over `results/v5/test5` (episodes 0–299) and `results/v6/test5` (300–499) reproduced the following:
  - Every method has exactly 500 episodes in every cell.
  - Student 5-seed means: 0.4988 / 0.4576 / 0.4188 / 0.4144 / 0.4832.
  - G\* run 1 / run 2: 0.518/0.532, 0.496/0.494, 0.432/0.464, 0.434/0.434, 0.474/0.498.
  - H6a Δ: −0.0262 / −0.0374 / −0.0292 / −0.0196 / −0.0028. The ci95 and ci90 match to within ±0.003 of bootstrap noise; S4 ci90 is [−0.071, −0.002] against the paper's [−0.0716, −0.0036].
  - H6b Δ (R-125 / R-500): +0.0928/+0.0368, +0.0556/+0.0676, +0.0628/+0.0468, +0.0564/+0.0244, +0.1532/+0.1092.
  - H6c Δ: +0.0132 / +0.0084 / +0.0072 / +0.0004 / −0.0052.
  - First-decision agreement: 0.274 / 0.402 / 0.452 / 0.426 / 0.314.
- **E12 recomputation from raw sub-16 records** (`results/v5/e5`, `results/v6/e12`). Shifts of −1.6 / +4.6 / +5.0 / −4.6 / −0.6 pp reproduced exactly. I also computed a post hoc episode-bootstrap ci95 of the shift, which the paper does not report (see A-W2).
- **Derived arithmetic I re-did:**
  - Latency ratios: 19–47×, 62–389×, 2,544–9,767×.
  - Cost of shrinking: 4.4–14.4 pp.
  - Seed spread: 2.8–6.2 pp.
  - 90 % half-widths 2.84–3.85 pp, giving the "required |gap| 0.15–1.16 pp".
  - Holm step-downs: 7/10 rejected on 0–499 (cut-off at rank 8, 0.0314 > 0.05/3) and 2/10 on 300–499.
  - v5 gate thresholds of −1.23 to −1.72 pp.
  - v5 single-run gap range of 0.2–2.5 pp.
  - Strongest comparator margins; heuristic margins; travel ranges; "RL 2.0 of 3 probes in 4/5 A16 seeds".
  - 9/10 success-reward runs `EARLY_STOP_AT_80_PCT_BUDGET`; all main RL runs `max_episodes` at 200,192.
  - 75 identical distillation configs (lr 0.001, batch 256, hidden 128, β_T 4, λ 0.5, 200 epochs); training-set sizes 2,700/3,500/4,300.
  - 733 CPU-h estimate (amendment v6.1); latency n = 1,000 (S) / 500 (A16-2); half-width rule met only in A16-2 (`job1_complete` true only there).
  - E7 look-ahead headroom S2 +0.0658 [0.0297, 0.1084] and S12 +0.0422 [0.0250, 0.0614].
- **Statistical code.** `code/analysis_v6.py` uses `crossed_bootstrap_diff` and `holm` as described. The TOST is implemented as two shifted one-sided bootstraps, which is consistent with Section 4. No t-test or ANOVA is claimed, and none is in the code.
- **Pre-registration text.** `docs/07c_amendment_v6_0.md` with addendum v6.1 matches Section 4: the H6a/H6b/H6c rules, δ = 0.04, the Holm families, E12 as report-only, Random not extended, first-decision agreement only, and no new timing.

**TRIAL / RUN COUNT.** The paper claims 500 test episodes per method per cell (200 of them fresh), 5 student seeds, 5 BC seeds, 5 RL seeds, 2 G\* runs, 1 run per reduced planner and heuristic, 75 training runs, and 27/22 evaluated policy instances per cell. All of these match `episodes_per_method`, `n_seeds` and the training logs exactly.

**CRITICAL FABRICATION: none found.** Every number I checked traces to a results field or to arithmetic on one. The only inaccuracies are minor phrasing and rounding issues, listed under A-W5.

---

## Reviewer A (methodology and statistics)

### Summary
The paper is a pre-registered measurement study in a planar tactile-localization simulator, using five cells (S2, S4, S8, S12, A16-2). It compares three things against a cost-aware greedy EIG planner G\*:
- a DeepSets student distilled from G\* (BC, then DAgger);
- two reduced planners with the same Monte Carlo budget N·M = 2,000;
- RL and heuristic comparators.

The registered findings are:
- The student beats R-125 in 5/5 cells and R-500 in 2/5 (Holm), at 62–389× lower per-decision latency.
- Parity with G\* is neither shown nor refuted under TOST at 4 pp.
- DAgger shows no detectable gain over BC.
- A report-only evaluator-grid check and the teacher's run-to-run agreement show that few-pp contrasts are fragile.

### Strengths
1. **Exemplary consistency between methods and evidence.** I reproduced every headline number from raw records, and the methods text matches the registered amendment line for line. This is rare.
2. **Honest inference.** The paper does not convert non-rejection into equivalence. It reports TOST p-values, the ci90 and the gap each cell would have needed. It labels everything that was not registered as report-only, exploratory or post hoc. It states that the fresh window replicates the direction of the effects but not their significance.
3. **Teacher variance is included in the parity contrast.** Running G\* twice with salted policy streams and showing 25–45 % first-decision agreement is a useful and under-reported observation for imitation of Monte Carlo planners.
4. **A real component ablation (H6c)** with matched seeds, plus a cautious reading of it (R̄ is measured on G\*-visited states, and no equivalence test was run).
5. **The limitations section is thorough** and maps one-to-one onto the gaps I would otherwise raise.

### Weaknesses
- **A-W1. The DAgger ablation (H6c) is weaker than presented, because of an implementation detail the paper omits.**
  - `code/tools_v5_manifests.py:72` starts every DAgger round from the previous round's weights (`--init ..._r{r-1}.npz`). Algorithm 1 says only "repeat step 2" and never mentions this warm start.
  - Combined with "keep the checkpoint with the lowest held-out R̄", the kept round-2 checkpoints are often very early. `16_report_rows.json › student_checkpoint_sensitivity` gives round-2 best epochs of 0, 4, 5, 7, 8 and 10 in 6 of 25 cell-seeds (median ≈ 30 of 200). Round 1 is similar: median ≈ 27, with 2, 2, 3 and 4 among them.
  - So the round-2 student is, in many seeds, the round-1 (or round-0) network after a few epochs on aggregated data, chosen by a metric the paper itself says cannot see DAgger's benefit.
  - H6c therefore tests "DAgger with early stopping on teacher-visited regret" more than DAgger itself.
  - **Required:** state the warm start in Algorithm 1, report the best-epoch distribution, and soften C3 accordingly. A post hoc check would also help: last-epoch round-2 checkpoints, or checkpoints selected on student-visited regret.
- **A-W2. The C4 "methods note" rests on point estimates from 100 episodes and one G\* run.**
  - The text "moves student − G\* by 4.6–5.0 pp ... comparable to the 4 pp margin" carries no uncertainty.
  - My post hoc episode bootstrap of the per-episode shift on the raw E12 records gives:
    - S2 −1.6 [−8.0, +4.6]
    - S4 +4.6 [−1.8, +11.0]
    - S8 +5.0 [−0.2, +10.6]
    - S12 −4.6 [−9.0, −0.6]
    - A16-2 −0.6 [−3.0, +0.8] pp
  - Only S12 excludes zero. Much of each shift comes from G\* run 1's own flips, which run at 7–10 %.
  - The qualitative point stands: a thresholded read-out flips 4–13 % of outcomes. But "comparable to the margin" should be presented as an upper-range point value, with its interval.
  - C4 is listed as a contribution, so it needs a CI (report-only) or a clear downgrade to "illustration".
- **A-W3. The crossed bootstrap with two G\* "seeds" is crude.**
  - Resampling 2 runs with replacement means about half the replicates use a single run twice.
  - That inflates the G\* variance term in a poorly calibrated way. The paper acknowledges this ("poorly estimated", Lim. 1).
  - It feeds directly into the TOST verdict, which is conservative with respect to equivalence. The TOST failures may therefore be partly an artefact of the resampling scheme.
  - **Suggested:** report a sensitivity analysis that treats G\* runs 1 and 2 as fixed (episode-only bootstrap of the average of the two runs).
- **A-W4. The primary window is not fully confirmatory.**
  - Episodes 0–299 and the student/G\*/heuristic outcomes on them were known when v6 was designed. The design pivoted to the frontier question after the v5 parity gate failed.
  - H6b is cleanly prospective, because the reduced planners were never run on test5 before. H6a on 0–499 is not.
  - The paper discloses the overlap, but the abstract should say "500 test episodes, 300 previously evaluated". The fresh-window results, where only 2/10 H6b contrasts survive, deserve equal billing.
  - In addition, the claim "committed before the first new record was read" cannot be verified from the repository: it is a shallow clone, and `code/analysis_v6.py` first appears in commit 121cd907 dated 2026-11-12, which is a results commit. The authors should cite the original commit hash or timestamp.
- **A-W5. Minor numerical and phrasing inaccuracies (none fabricated).**
  - "deficits of up to about 7–8 pp (ci95) cannot be excluded" (Abstract, C2, §5.2, §6.2, §8). The primary-window ci95 lower bounds are 6.9 / 7.8 / 7.0 / 5.3 / 5.0 pp, so 7–8 pp holds only for S2/S4/S8. Write "about 5–8 pp depending on the cell".
  - "Strongest comparator ... B-cov in S12". B-cov and R-500 tie at 0.390 in S12 (`15_derived_v6.json` picks B-cov by order). State the tie.
  - "E12 ci95 half-widths are 7–10 pp". S12 is ≈ 6.8 pp; write "about 7–10".
  - The latency ratio "G\* 2,544–9,767× slower" is a ratio of medians. `14_e6_analysis` also stores the registered paired median-of-ratios (9,933 in S2). Say which one is used and why.
  - The latency CIs are highly asymmetric: G\* S4 median is 3.37 s with ci95 [2.45, 3.45]. The point medians on the frontier hide this, so give the intervals in a supplementary table.
- **A-W6. Each reduced planner was run once.** R-500 versus R-125 orderings flip between cells (S4), and the marginal H6b rejections have lower bounds near +1.3 pp. One rerun per reduced planner, about 33 CPU-h per the P6 figures, would be cheap and would turn Limitation 2 into evidence.

### Actionable revisions (Reviewer A)
1. Disclose the DAgger warm start and the checkpoint epochs (A-W1). Add a last-epoch or student-visited-regret sensitivity check, or explicitly weaken C3.
2. Add uncertainty to the E12 shift (A-W2) and reword C4 so that "comparable to the margin" is a point-estimate statement.
3. Add an episode-only bootstrap sensitivity for H6a/TOST that holds the two G\* runs fixed (A-W3).
4. In the abstract and C1, state the 300/200 seen/fresh split and the fresh-window 2/10 result next to the 7/10.
5. Fix "7–8 pp" → "5–8 pp", state the S12 tie, and say which latency ratio definition is used.
6. Cite the commit that froze `analysis_v6.py`.

**Score (Reviewer A): 5/10 (Borderline).** The methodological rigour is excellent and every claim checks out against the data. The positive result is narrow, though: 7/10 on a partly seen window and 2/10 fresh. The ablation has an undisclosed confound, and the methods-note contribution lacks its own uncertainty.

---

## Reviewer B (significance, novelty and presentation for NeurIPS/ICML)

### Summary
The paper asks a practitioner's question: whether to distil or shrink an expensive information-gain touch planner. It answers with a carefully hedged simulation study.

### Strengths
1. A clear and useful framing. Comparing an amortized policy against reduced versions of its own teacher on an accuracy–latency frontier, rather than only against heuristics, is a good evaluation habit, and the related-work section argues reasonably that it is rarely done.
2. The C1 latency gap is large and practically meaningful: sub-millisecond for the student against tens to hundreds of ms for the reduced planners. In this setting the student is never significantly worse than either reduced planner.
3. The teacher-stochasticity and evaluator-sensitivity observations are transferable lessons for the amortized-BOED and imitation-of-planners communities.
4. The paper is transparent about failure: it reports parity not established, DAgger not detected and RL under-tuned rather than spinning them.

### Weaknesses
- **B-W1. Limited novelty and significance for a 9-page main-track paper.**
  - There is no new method. The single positive finding is that a distilled network is more accurate than two specific reduced planners in 7/10 contrasts, and only the direction replicates on fresh data.
  - The setting is a planar simulator with one fingertip on a fixed circle and 3–4 probes per episode.
  - The authors' own conclusion ("preliminary") is accurate, which makes the work better suited to a workshop, a datasets-and-benchmarks or reproducibility track, or a robotics venue's short-paper format.
- **B-W2. Baselines are thin on the frontier.**
  - There are only two reduced planners, both at N·M = 2,000 and both with all 512 candidates. Natural competitors are missing:
    - candidate subsampling (C < 512), the obvious first knob;
    - a reduced planner tuned toward the student's latency or toward the R-500 accuracy;
    - a cheap information-based heuristic;
    - the student plus a small online re-ranking step.
  - RL is tuned on S2 only with one sweep seed, and in A16-2 it collapses to 2 of 3 probes. The paper admits this.
  - Without these, "distil beats shrink" is established only against a narrow shrink family.
- **B-W3. The paper reads like a lab notebook in places, and drifts off topic.** The topic is respected overall. The sections are on the stated question and environment issues are not presented as contributions. But several passages are process history rather than science:
  - "the previous round", "v6 update of the previous single-run row", "Why TOST replaces the previous gate", "Comparison with the previous round";
  - runner and time-guard disclosures in the main text;
  - the repeated report-only rows for RL and heuristics.

  These should be compressed into one "Relation to an earlier pre-registered analysis" paragraph and an appendix. A reader of a conference paper has not seen the "previous round".
- **B-W4. Length and format.**
  - Body text is about 7,900 words. By section: Abstract 245, Intro 803, Related 563, Method 1,715, Experiments 1,122, Results 1,999, Discussion 857, Limitations 415, Conclusion 214.
  - There are also four tables, Algorithm 1 and a 6-panel figure. No section is under the minimum lengths, but the paper is clearly **over** the 9-page limit and must be cut by about 30 %.
  - The abstract (245 words) is dense with qualifiers and should go below 200.
  - Three `[CITE-MISSING]` placeholders remain: DeepSets, Efron's bootstrap, Holm 1979.
  - Figure 1 is only a prompt. Panels B–F should be rendered from the JSON before submission.
- **B-W5. The headline contrast is hard to read.** "Neither a difference nor equivalence within 4 pp" in all five cells is the expected outcome given the power analysis in §4: equivalence was possible only if the gap was under 0.15–1.16 pp. The design was under-powered for H6a by construction, and the paper's own power paragraph says so. It is then odd to list "parity is not established" as a claimed contribution (C2). Either drop C2 to a result or frame it as an informative bound (deficit ≤ about 5–8 pp at 95 %).
- **B-W6. External validity.** One evaluator family, a likelihood shared by planner, filter and evaluator, and no task-time model mean the latency gains are not shown to translate into episode-time or accuracy-per-wall-clock gains. The paper is honest about this (Lim. 4, 11), but it caps the practical significance of C1.

### Actionable revisions (Reviewer B)
1. Add at least one more shrink axis (candidate subsampling) and one reduced planner placed so that it matches the student's accuracy, so that the frontier is actually traced. Otherwise retitle C1 as "against two reduced planners".
2. Rewrite for a reader who never saw earlier rounds: move the version history, gate history and runner details to an appendix.
3. Cut to 9 pages: merge Table S into the appendix, shorten §5.3 (RL, heuristics, behaviour), and shorten the abstract to under 200 words.
4. Fill the three missing citations and render Figure 1.
5. Reframe C2 as a bound rather than a "claim", and lead the abstract with C1 plus the fresh-window caveat.

**Score (Reviewer B): 4/10 (Borderline reject).** It is a careful, honest measurement, but the novelty and significance are below the NeurIPS/ICML bar in its current scope (planar simulation, narrow baseline family, one positive result that does not replicate in significance on fresh data). It would be a good fit for a workshop or a robotics short-paper venue after trimming.

---

## Consolidated findings

| Check | Verdict |
|---|---|
| On topic | Yes. There is no unrelated drift, and environment issues are disclosed, not claimed. Version-history passages are excessive (B-W3). |
| Method ↔ evidence | Consistent. Every number checked against JSON and raw jsonl. One omitted implementation detail: the DAgger warm start and early kept epochs (A-W1). |
| Trial count | Correct: 500 episodes/method/cell, 5 seeds, 2 G\* runs, 1 run per reduced planner, 75 training runs. |
| Statistical tests | Crossed bootstrap, TOST and Holm all present in code as described. No unclaimed tests. |
| Length | Not under-length: about 7.9k words, which is over the 9-page budget. Abstract 245 words is too long. |
| CRITICAL FABRICATION | **None found.** |

**Overall: Reviewer A 5/10, Reviewer B 4/10 (mean 4.5, Borderline / not yet ready for NeurIPS/ICML).**

### Top 5 actions
1. Disclose the DAgger warm start and the kept-checkpoint epochs, add a sensitivity check, and soften C3.
2. Put uncertainty on the E12 grid shift (only S12 excludes 0 post hoc) and reword C4.
3. Broaden or qualify the frontier: add candidate subsampling or an accuracy-matched reduced planner, rerun the reduced planners once, and give the fresh-window 2/10 result equal billing with the seen/fresh split in the abstract.
4. Rewrite for an external reader and cut to 9 pages: remove the "previous round" narrative, shorten the abstract to under 200 words, fill the 3 CITE-MISSING placeholders and render Figure 1.
5. Fix minor numbers ("7–8 pp" → "5–8 pp", the S12 tie, the latency-ratio definition) and cite the commit that froze `analysis_v6.py`.
