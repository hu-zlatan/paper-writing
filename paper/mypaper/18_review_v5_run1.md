<!-- Stage 18 PEER_REVIEW [v5] run 1, run 41, 2026-11-09; fresh-context subagent; template peer_review.md verbatim -->

# Stage 18 (v5) peer review, run 1

**CRITICAL_FABRICATION: no.** I checked 40 claims. Every trial and episode count, seed set, statistical test and
hyperparameter matched the evidence JSONs, the pre-registration documents or the code. I recomputed two test5 cells,
S4 and A16-2, from the raw per-episode logs with `crossed_bootstrap_diff` (B = 10,000, seed 0, α/2 = 0.025). The
student − G\* success diff, ci95, two-sided p and the G\* $g_T$ mean all came out exactly as published. The paper
names no test that the code does not run. `tost` exists in `code/touchbed/stats.py`, and the paper correctly says that
no equivalence test was run.

The mismatches I found are minor and change no verdict:
- The paper says the H5b weights were "fixed before test5". Only the weighting rule was fixed in advance. The weight
  values are computed from test5 itself.
- The claim that "the D5 rule applied to test5 would fail in about 4 of 5 cells" is a post-hoc approximation that the
  paper does not label as one. The paper also does not say which cell would pass (A16-2).
- The pre-registered latency–accuracy frontier was dropped without being called a deviation.
- The bootstrap behind the latency ci95 has a different size (B = 2,000) from the one in Table S (10,000).
- Three `[CITE-MISSING]` placeholders remain.
- One sentence about the reduced G\* configurations is duplicated.

**Scores: Reviewer A 4/10 (borderline, leaning reject); Reviewer B 3/10 (reject).**

---

## Verification log (claim vs evidence), 40 spot-checks

### Trial / episode / seed counts
| # | Claim (location) | Evidence | Match |
|---|---|---|---|
| 1 | D5 on val3 0–499, 500 paired episodes per cell, 5 student seeds (§4, Table 1) | `results/v5/12_d5_analysis.json` `<cell>.n_episodes` = 500, `per_seed` keys 701–705, all five cells `complete: true` | yes |
| 2 | Test5 0–299, 300 episodes per method per cell; every test5 and $g_T$ block complete (§4, Table S) | `results/v5/14_test5_analysis.json` `<cell>.episodes_per_method` all 300, `complete`/`gt_complete` true in all 5 cells; raw recount of `results/v5/test5/S_k4_*` and `A16_k2_*` gives 300 for G\* and each student | yes |
| 3 | Test5 cut 500 → 300 by addendum v5.1e, under the reduction order, before any test5 episode (§4, §7.1) | `docs/07c_amendment_v5_1.md` addendum v5.1e (step 2 of the v5.0 reduction order; projection ≈ 1,250 CPU-h) | yes (but see A-W4) |
| 4 | Seeds: students 701–705, RL 711–715, `rl_success` 711–715 in S2/S12 only (§3.3) | `results/v5/13_freeze.json` file names; `14_test5_analysis.json` `rlsucc_*` keys present only in S2 and S12 | yes |
| 5 | Weight hashes: 15 per cell in S2/S12, 10 in S4/S8/A16-2 (§4) | `13_freeze.json`: 15 / 15 / 10 / 10 / 10 sha256 entries | yes |
| 6 | H\* chosen on pilot3 0–199, 200 episodes per heuristic; choices B-cov, B-fan, B-cov, B-fan, B-fan (§3.4, Table 1) | `results/v5/12_base_hstar.json` `n` = 200; `H_star` per cell; pilot success values 0.445 / 0.43 / 0.405 / 0.41 / 0.33 | yes |
| 7 | τ from 200 cal3 episodes; S4 0.7967 → 4.8, S8 0.8335 → 4.8, A16 0.3514 → 3.4 (Table 0) | `results/v5/12_cal_analysis.json` `tau.*.mean_travel_time`, `n_episodes` 200 | yes |
| 8 | S2 0.7257 → 4.7 and S12 0.9388 → 4.9 come from earlier rounds (Table 0) | `results/v3/results_v3.json` `12_cal_analysis.tau.S_k2_nstar4` 0.72566, `S_k12_nstar4` 0.93884 | yes |
| 9 | A16 n\* = 3 (rule reading 0.975); keep check 0.8 at κ 0, τ = 3, 200 episodes (§3.1, Table 1) | `12_cal_analysis.json` `n_star.A16.gstar_success_sub8` 0.975, `keep.A16.gstar_success_sub8_at_nstar` 0.8, keep true; `docs/07c_amendment_v5_1.md` "Cells" | yes |
| 10 | DAgger budgets: 3,000 label episodes, 300 held out, training episodes 2,700 / 3,500 / 4,300 (Alg. 1) | `results/v5/16_report_rows.json` `student_train_episodes` (75 runs, exact values); `docs/07c_amendment_v5_0.md` E1 held-out 1,200–1,499 | yes |
| 11 | E5: 200 single-seed episodes, G\* and student 701, S2 and S12, sub 16 (§4) | `results/v5/14_e5_analysis.json` `n_episodes` 200 / 200 | yes |
| 12 | E6: job 1 n = 1000 in the S cells and 500 in A16-2; job 2 n = 500 per seed (§4) | `results/v5/14_e6_analysis.json` `job1.*.n`, `job2.*.n`; addendum v5.1g | yes |
| 13 | E7: 32 beliefs per cell; mean candidates 29.0 / 302.0 (S2), 30.5 / 85.75 (S12) (§4) | `results/v5/12_e7_analysis.json` `n_beliefs` 32, `mean_candidates` | yes |
| 14 | RL sweep: 8 configs, 100,096 episodes (100,032 at batch 64), validation stream 92,160 (§3.3) | `results/v5/12_rl_sweep_selection.json` rows 0–7 | yes |
| 15 | cfg-6 RL: 200,192 episodes logged for every run (§3.3) | `16_report_rows.json` `rl_main_cfg6`: 25 runs, all 200,192, `max_episodes` 200,000 | yes |
| 16 | `rl_success` training lengths, S2 123,392 / 124,672 / 181,760 / 200,192 / 125,440; S12 184,576 / 113,408 / 111,104 / 162,304 / 165,888; 9 of 10 runs stopped before the cap (§5.3, §7.5) | `16_report_rows.json` `rl_success` (9 × `EARLY_STOP_AT_80_PCT_BUDGET`, 1 × `max_episodes`) | yes |

### Statistics (code)
| # | Claim | Evidence | Match |
|---|---|---|---|
| 17 | Crossed episode × seed bootstrap with 10,000 resamples, two-sided ci95 (§4) | `code/touchbed/stats.py:13` `crossed_bootstrap_diff`; `code/analysis_test5_v5.py` `N_BOOT = 10000`, `ALPHA2 = 0.025` | yes |
| 18 | p-value resolution 0.0002, so p = 0 is printed as p < 0.0002 (§4) | `analysis_test5_v5.py` `two_sided`: p = 2·min(p_greater, p_less), so the smallest non-zero value is 2/10,000 | yes |
| 19 | Holm over 5 cells, two families only (student − G\* and student − H\* success) (§4) | `analysis_test5_v5.py` `main()` loops only over those two names; `stats.py:34` `holm` | yes |
| 20 | D5 threshold max(−0.02, −δ + 1.163 SE); BI ≥ −0.15; ≥ 4/5 seeds (§4) | `code/analysis_d5_v5.py:49` `-DELTA + 1.645*se*sqrt(0.5)` (1.645·√0.5 = 1.163); `docs/07c_amendment_v5_0.md` D5 | yes |
| 21 | H2-v5: one-sided 95 % LB > +0.10 nats (§4) | `analysis_test5_v5.py` `crossed_bootstrap_diff(gS, gR, alpha=0.05)`, `lb["lower"] > 0.10` | yes |
| 22 | Inversion needs both orderings resolved (§4) | `analysis_test5_v5.py`: `inv_g.ci95[0] > 0 and inv_s.ci95[0] > 0` | yes |
| 23 | H5b: WLS slope "with weights fixed in advance"; "the weights were fixed before test5" (§4, §5.4) | `analysis_test5_v5.py` `h5b()`: `w = 1/reps[:, :, 0].var()`, the bootstrap variance of each cell's **test5** Δ_succ. Only the rule was fixed in advance (addendum v5.1f) | **wording mismatch** (rule fixed in advance; values come from test5) |
| 24 | Latency ratios reported "with bootstrap ci95" (§4, Table 4), next to "10,000 resamples" in Table S | `code/analysis_e6_v5.py` `B = 2000` | **ambiguous**: E6 uses B = 2,000, and Table S does not say so |

### Hyperparameters and design constants (code)
| # | Claim | Evidence | Match |
|---|---|---|---|
| 25 | hp 0: Adam, lr 0.001, batch 256, width 128, β_T 4.0, λ 0.5, 200 epochs, identical in every cell (Alg. 1, Table S) | `16_report_rows.json` `student_distill_configs`: one config × 75 runs | yes |
| 26 | Regret floor ρ = 0.05; median-based denominator (§3.3) | `code/touchbed/distill.py:9,23` | yes |
| 27 | 64 × 8 = 512 actions; ψ from −35° to +35° in 10° steps; probe radius 100 mm (§3.1) | `code/touchbed/travel.py:18` `PSI_GRID`; `geometry.py:12` `RHO = 100.0`; `16_report_rows.json` `student_env` "64x8/A=512"; test5 log header `action_set 64x8` | yes |
| 28 | cfg 6 = lr 1.257e-3, ent 9.504e-4, batch 256, critic lr 4.925e-4; 6.300 vs 6.241 (cfg 0); cfg 1 higher on the sampled metric (6.316 vs 6.205) (§3.3) | `12_rl_sweep_selection.json` rows 0, 1, 6 | yes |
| 29 | PPO clip 0.2, 4 epochs, hidden 128 (§3.3) | `16_report_rows.json` `rl_main_cfg6` | yes |
| 30 | B-fan cycles the approach offset and stays put; it logs only the first-leg snap of 1.422° (§3.4, Table 5) | `code/touchbed/heuristics.py:22,65` `FAN_CYCLE`; `14_test5_analysis.json` `b_fan.travel_deg` 1.4217 (S cells), 1.4452 (A16-2) | yes |
| 31 | E7 beliefs are "G\*-reached" (§4) | `code/touchbed/g2.py:2`: G\* runs for u_i ~ U{0..n\*−1} steps | yes |

### Reported numbers (spot-checked; all present in the evidence)
| # | Claim | Evidence | Match |
|---|---|---|---|
| 32 | Table 1 D5 values (Δ̂_succ, thresholds, Δ̂_BI, seeds ok 3/1/4/3/0; 25 per-seed diffs from −0.068 to −0.01) | `12_d5_analysis.json` | yes |
| 33 | Table 2a/2b, all test5 success and BI contrasts, Holm flags, student/RL seed ranges | `14_test5_analysis.json`; `15_posthoc_derived.json`; raw recomputation for S4 and A16-2 | yes |
| 34 | Student − G\* CI widths 9.6–12.3 pp; tightest lower bound −6.1 pp (S8); worst −8.3 pp (S4) | computed from `14_test5_analysis.json` | yes |
| 35 | Best test5 heuristic ≠ H\* in 4/5 cells; post-hoc margins +3.5 to +14.5 pp | `15_posthoc_derived.json` `best_test5_heuristic`, `margin_student_minus_best_test5_heuristic` | yes |
| 36 | Table 3 $g_T$ means and contrasts; H2-v5 LBs −0.4971 / −0.6555 / −0.4861 / −0.3044 / +0.5964 | `14_test5_analysis.json` `<cell>.H2_v5` | yes |
| 37 | H5b slope −0.0157/rad, ci95 [−0.104, 0.073]; per 100° −0.02741; span translation −0.0739 to +0.0517 | `14_test5_analysis.json` `H5b`; `15_posthoc_derived.json` `H5b_span_translation` | yes |
| 38 | E5 flip rates 8 / 7 / 7.5 / 6.5 %; contrast shifts +0.02 / −0.03; mean abs ΔBI ≤ 0.004034 | `14_e5_analysis.json` | yes |
| 39 | Table 4 latency medians, ratios and CIs; CI rule met only in A16-2; job-2 ratio ranges; job-2 student medians 0.36–0.51 ms | `14_e6_analysis.json`; `15_posthoc_derived.json` `latency` | yes |
| 40 | Prior gates: S12 −0.05867 (−0.01435), −0.044 (−0.01681); S2 −0.028 (−0.01464); v4 test3 gap −10.2 pp [−16.6, −4.3] | `results/v3/results_v3.json` `12_d3_analysis`, `12_d3_analysis_rem`; `results/v4/results_v4.json` `12_d4_analysis`, `14_s2_analysis.test3_sub8` | yes |

Other numbers checked without a separate row, all matching:
- the checkpoint-sensitivity ranges (0.0002753–0.03172, kept R̄ per cell, held-out decision counts 1161 / 1180 / 1179
  / 1196 / 880, kept epochs 0–187; `16_report_rows.json`);
- the E7 selection bias and paired gaps;
- Table 5 travel and probe ranges;
- the A16-2 RL probe counts (2.0 in seeds 712–715, 2.773 in seed 711).

### Other evidence-level issues
- **"Applying the D5 rule to test5 would still fail in about 4 of 5 cells"** (§5.1). The source is
  `results/v5/14_analysis.md` M1. That derivation approximates each test5 SE as CI half-width / 1.96 and applies only
  clause (i). It is post hoc and approximate, but the paper does not label it so. The cell that would pass is A16-2,
  where test5 Δ̂ is −0.002 and all five seeds are above −δ. On validation, A16-2 is the worst cell (−0.0596, 0/5 seeds).
  This val/test reversal is the most striking split disagreement in the paper, and it goes unmentioned.
- **The pre-registered latency–accuracy frontier was not delivered.** `docs/07c_amendment_v5_0.md` E6 promises a
  "latency–accuracy frontier figure". Addendum v5.1f reads the frontier within job 1, using v4 E5 accuracy rows in S12.
  The paper instead says the table "supports no latency–accuracy frontier". That is honest, but it is not flagged as a
  departure from the registration.
- **Reduction-order ordering.** Step (1) of the frozen order was "E7 skipped". E7 was decided and run in addendum
  v5.1d (run 32), one run before the first real test5 sizing in v5.1e (run 33). That made step (1) unavailable and
  forced step (2), the test5 cut. The documents record this transparently, and the cut was made blind to outcomes.
  Still, an optional ≈ 1 CPU-h characterisation ran while the primary hypothesis lost 40 % of its test episodes. The
  paper's phrase "under the frozen reduction order" is literally true but hides this sequence.
- **Freeze before test5 is not independently verifiable.** The repository history is squashed: `git log` on
  `results/v5/test5` and `13_freeze.json` shows one commit. The paper correctly says the ordering "is taken from the
  run context".
- **Placeholders.** There are three `[CITE-MISSING]` placeholders (DeepSets, Holm 1979, Efron bootstrap).
- **Editorial.** In §3.2 the reduced configurations are introduced twice.

### Length check
The section word counts, computed from the draft including tables and equations, are: Abstract 263, Introduction 915,
Related Work 677, Method 1,721, Experiments 1,622, Results 2,237, Discussion 527, Limitations 341, Conclusion 199.
The total is about 8,500. Every section is above its minimum, so nothing is under-length. The opposite risk applies:
with six tables, a four-panel figure and an algorithm box, this draft is very unlikely to fit 9 pages. Table S,
the checkpoint-sensitivity paragraph, the E7 note and Table 4 are candidates for the appendix.

### Topic check
The paper stays on topic: amortizing G\* across five pre-registered cells, compared with RL and heuristics, and the gap
versus travel. The methods notes (E5 evaluator resolution, E7 selection bias, the sPCE vs posterior ordering) are
explicitly fenced off as measurement notes, not contributions (C5, §4), which is appropriate. Runner and infrastructure
details appear only under Implementation and Limitations, not as contributions. No drift.

---

## Reviewer A (methodology and evidence)

**Summary.** This is a pre-registered five-cell study (S at κ = 2/4/8/12, plus A16 at κ = 2) of whether a DeepSets
student trained by DAgger on a cost-aware greedy EIG planner's score vectors matches that planner. It also compares the
student with PPO on a ball-sPCE reward and with three heuristics, and regresses the student − G\* gap on G\* travel.
The headline is negative: the validation gate fails in 5/5 cells. The secondary findings are a Holm-corrected win over
pilot-chosen heuristics in 4/5 cells, and an RL comparison that resolves only where RL collapses.

**Strengths.**
1. **Exemplary bookkeeping.** Every number I traced (40 checks) is in a named JSON field, and two cells reproduce
   exactly from raw logs. Decision rows, post-hoc rows and exploratory rows are labelled consistently (DEC / EXPL / PH),
   and the D5 and H5a/H5b/H2-v5 rules in the code match the amendment text.
2. **Honest reporting of a negative headline.** The paper does not convert the small test5 point gaps (0.2–2.5 pp)
   into a "match" claim. It states the CI widths (9.6–12.3 pp), notes that no equivalence test was run, and checks that
   test5 does not overturn D5.
3. **Caveats are quantified, not asserted.** E5 bounds the evaluator's effect on single-seed contrasts (0.8× to 2× the
   test5 gap). The checkpoint-sensitivity rows, the RL under-tuning (cfg 1 higher on the sampled metric) and the
   `rl_success` truncation are all reported next to the results they qualify.
4. **Comparison under shared conditions.** The paired design over all methods (same episodes, start angle and
   observation stream), with a fixed head and action set across learners, isolates the training signal as intended.

**Weaknesses.**
1. **The primary contrast cannot discriminate.** At 300 episodes and a run-once G\*, the student − G\* CIs are
   ±5–6 pp against a δ of 4 pp, so neither "matches" nor "is worse than" is resolvable on test5. The paper says this
   clearly, but it means C1 rests entirely on the validation gate. That gate (a) mixes G\* rows from three rounds and
   (b) is close in two cells: S8 and S12 miss the threshold by 2.0 and 1.5 pp, and S8 passes clauses (ii) and (iii).
   "Fails in 5/5" is correct under the rule, but the effect behind it is about 3–6 pp on validation and about 0–2.5 pp
   on test5.
2. **The D5-on-test5 statement is unlabelled and hides a reversal.** See the evidence-level issues: the "about 4 of 5"
   claim is a post-hoc approximation, and the passing cell, A16-2, is the worst cell on validation. That is either a
   meaningful split-dependence (G\* validation rows were new for A16-2, so this is not a G\*-source artefact) or noise
   of about ±6 pp. Either way, the reader should be told.
3. **H5b is very low-powered.** Five points, one of them from another library, and a slope CI spanning roughly ±7 pp
   over the travel range. "No trend detected" is the correct reading, but a regime question cannot be answered with
   this design. The weights are also data-derived (1/test5 bootstrap variance), contrary to the wording "fixed before
   test5".
4. **The teacher's variance is missing from every student − G\* interval.** The paper acknowledges this (G\* was run
   once; n_seeds = [5, 1]), but it biases every CI to be too narrow, in the same direction as the C1 headline.
5. **The RL comparator is weak outside S2.** One config tuned on S2 collapses in A16-2, which is the only cell where
   H2-v5 is met. The RL comparison (C3) is therefore close to uninformative. The authors say so, but C3 is still listed
   as a contribution.
6. **The reduction-order sequence.** The optional E7 ran first, and that forced the test5 cut. This is documented but
   not discussed.

**Actionable revisions.**
1. Label the D5-on-test5 sentence as post hoc and approximate, say how SE was approximated, and name A16-2 as the cell
   that would pass. Discuss the A16-2 val/test reversal in one or two sentences.
2. Replace "weights fixed before test5" with "weighting rule (1 / bootstrap variance of each cell's test5 Δ_succ)
   fixed before test5".
3. Add a line to §4 or §7 stating that the pre-registered latency–accuracy frontier was not produced, and why.
4. State the E6 bootstrap size (B = 2,000) in Table 4 or Table S.
5. Report the per-cell D5 margin (Δ̂ − threshold) in Table 1, so readers can see that S8 and S12 are near misses.
6. In §7, briefly note that E7 ran before the test5 sizing, and that this sequence led to step (2) of the reduction
   order.
7. Resolve the three `[CITE-MISSING]` placeholders and remove the duplicated reduced-config sentence in §3.2.

**Score: 4/10 (borderline, leaning reject).** The paper is rigorous and honest, but its only resolved primary result
is a gate failure of a few pp, and the secondary contrasts are either post hoc (best heuristic) or confounded (RL).

---

## Reviewer B (novelty, significance and fit for NeurIPS/ICML)

**Summary.** The paper measures how well a distilled policy reproduces a greedy cost-aware EIG touch planner in a
simulated planar 2D task, across travel costs and two shape libraries. It makes no method claim.

**Strengths.**
1. **Pre-registered negative results are rare** in learned active perception. The multi-round record (S12 twice, S2,
   then five v5 cells, all failing the gate) is a useful data point against assuming that planner distillation is
   lossless.
2. **The same-head, same-action-set comparison** of planner distillation and RL on RL's own objective is a fair design
   choice. The observation that the sPCE-type bound and the posterior read-out can rank policies differently (G\* has
   the lowest $g_T$ but the highest success in every S cell) is a worthwhile caution for amortized BED work, even though
   it is not statistically resolved.
3. **The latency numbers are concrete and appropriately hedged** (2,523–9,933×, CI rule met in 1/5 cells, runners
   differ).

**Weaknesses.**
1. **Limited novelty and significance.** DAgger distillation of an information-gathering expert is established
   (Choudhury et al. 2017; Nguyen et al. 2024). The contribution is a measurement, and the measurement's central answer
   is "slightly worse than the teacher, not resolvable at this sample size". For a NeurIPS/ICML audience, a negative
   answer has to be decisive or explanatory to carry a paper. This one is neither: the shortfall is 0–6 pp, and the
   paper explicitly claims no mechanism.
2. **Narrow scope.** The setting is simulation only, with planar polygons, one fingertip on a fixed circle, a sub-8
   grid read-out, and two libraries with one κ for A16. The related-work section itself notes that comparable systems
   run on hardware with 3D geometry. Generalisation to any real tactile setup is untested.
3. **The "regime" question is not answered.** Four κ values on one library plus one cell from a second library cannot
   separate travel effects from library effects. H5b's CI admits a change of about 7 pp either way.
4. **The secondary wins are modest or qualified.** Against the best test5 heuristic the margin is 3.5–14.5 pp, with no
   CI. The RL wins come where RL fails. What is left is "a cheap policy between heuristics and planner", which is useful
   to practitioners but expected.
5. **Presentation density.** About 8,500 words, six tables, three methods notes and many decision labels make the
   paper hard to read and well over 9 pages. A reader has to work to find the one-paragraph answer.

**Actionable revisions.**
1. Reframe for a venue that values pre-registered negative or replication results (e.g. a workshop, TMLR, or the RSS
   Stage-1 track the amendment mentions). Alternatively, add an explanatory analysis: the paper's own open question,
   label regret measured on student-visited states versus G\*-visited states, would turn "it is a bit worse" into "it
   is worse because of X".
2. Add at least one more κ on A16, or a third library, so that H5b separates travel cost from library.
3. Move Table S, E7, checkpoint sensitivity and the job-2 latency column to an appendix. Put a single summary figure
   (panel D) up front.
4. Either tune RL per cell or drop C3 as a contribution and present it as a control.
5. Spend the saved budget on more test5 episodes, or a second G\* run, so that the primary contrast can be resolved.

**Score: 3/10 (reject for NeurIPS/ICML).** It is careful work, but the contribution is incremental, the scope is narrow
and the primary result is unresolved at the chosen sample size.

---

## Consolidated mismatch list (none critical)

1. **H5b weights** (§4 "weights fixed in advance", §5.4 "the weights were fixed before test5"). In
   `code/analysis_test5_v5.py` `h5b()`, `w = 1 / var` of the bootstrap replicates of each cell's test5 Δ_succ. The
   values in `14_test5_analysis.json` `H5b.weights` (1469.5, 1144.1, 1593.9, 1643.4, 1047.6) are test5-derived. Only
   the rule was fixed (addendum v5.1f).
2. **"D5 rule applied to test5 would still fail in about 4 of 5 cells"** (§5.1). This is a post-hoc approximation
   (`results/v5/14_analysis.md` M1: SE ≈ CI half-width / 1.96, clause (i) only) that the paper does not label. The
   passing cell (A16-2) is not named, although it is the worst validation cell (`12_d5_analysis.json` A16-2 Δ̂ −0.0596,
   seeds ok 0/5).
3. **Pre-registered latency–accuracy frontier dropped** without a deviation statement (`docs/07c_amendment_v5_0.md`
   E6; addendum v5.1f) versus §5.2 "supports no latency–accuracy frontier".
4. **The E6 bootstrap size is unstated.** `code/analysis_e6_v5.py` uses `B = 2000`, while Table S lists 10,000
   resamples under Statistics.
5. **Reduction-order sequencing is not disclosed.** E7 was run in addendum v5.1d (run 32) before the test5 sizing in
   v5.1e (run 33), which made step (1) unavailable and triggered step (2), the test5 cut (`docs/07c_amendment_v5_1.md`).
6. **Unresolved placeholders.** Three `[CITE-MISSING]` (DeepSets, Holm, Efron).
7. **Editorial duplication.** The reduced G\* configurations are introduced twice in §3.2.

No trial count, seed count, statistical test, hyperparameter or metric in the paper is unsupported by the code or the
results.

CRITICAL_FABRICATION: no
