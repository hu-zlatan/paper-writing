# Stage 18 (v4) peer review, run 1

**CRITICAL_FABRICATION: no.** Every trial and episode count, seed set, statistical test and hyperparameter I checked
matches the evidence JSONs and the code. I recomputed the S2 test rows, the S2 behaviour block, H2-S2 (crossed
bootstrap, B = 10,000, seed 0) and the E5 rows from the raw per-episode logs, and they reproduce exactly. The paper
names no test that the code does not run. TOST and Holm exist in `code/touchbed/stats.py`, and the paper correctly
says they were not run. The mismatches I found are minor: a wording error about the shape library, one gate row
reported as "pass" without a measurement, an imprecise half-width figure, a random-row count that is now out of date,
and two unresolved `[PENDING]` placeholders. None of them changes a verdict.

**Scores: Reviewer A 4/10 (borderline, leaning reject); Reviewer B 3/10 (reject).**

---

## Verification log (claim vs evidence)

### Trial / episode / seed counts
| Claim (location) | Evidence | Match |
|---|---|---|
| D3/D4 on 500 paired val3 episodes, 3 student seeds (§4, Table 2) | `12_d3_analysis*.n_episodes` 500; `12_d4_analysis.n_episodes` 500; seeds 501–503 / 601–603 | yes |
| D3-B belief input on 300 episodes (Table 2 R5c) | `12_d3_analysis_belief_student.n_episodes` 300 | yes |
| S2 test3 0–299 rows, n = 300 per row (Table 5) | `14_s2_analysis.test3_sub8.n_per_row`: 300 for G\*, 3×300 student, 3×300 RL, 300 B-fan; recomputed from `results/v4/test3_sub8` | yes |
| S2 random row 215 of 300 (§4, §7) | JSON `n_per_row.random` = 215. Raw files now hold 245 episodes; the analysis JSON predates them | matches JSON; out of date vs disk |
| H2 / H2-S2 on test3 0–499 (§4) | `14_h2_analysis.n_episodes` 500; `14_s2_analysis.h2.n_episodes` 500; recomputed | yes |
| E5 on S12 test3 0–299, n = 300 (Table 6) | `14_e5_analysis.n_per_row` all 300; recomputed from `results/v4/e5` | yes |
| H3: 100 beliefs per κ; bias check 20 beliefs (§3.3, Table 3) | `12_g2_analysis.k*.n_beliefs` 100; `bias_check.n_beliefs` 20 | yes |
| Gate E′: 16 episodes, 1 counted flip, mean 0.0126, max 0.0523 (§4) | `12_e_analysis` | yes |
| Flip rate 7.5 % on 200 calibration episodes (§4) | `n_star_sub8.S.success_flip_rate_vs_sub4` 0.075, n = 200 | yes |
| G\* 3.96 probes over 200 calibration episodes at τ = 4.9 (§3.1) | `verify.S_k12` 3.96, n = 200 | yes |
| S2 τ = 4.7; mean travel time 0.7257 (§3.1) | `tau.S_k2_nstar4` | yes |
| Lat′: 1,000 decisions on 253 pilot episodes, two jobs (§4) | `12_lat_analysis` n_decisions 1000, n_episodes 253, 2 files | yes |
| PPO 200,064 episodes per seed; S2 plateau at 102,400 for every seed (§3.4, §5.4) | `rl_training` | yes |
| PPO sweep: 4 configurations, 1 seed, 50,048 episodes (Table 1) | `12_rl_sweep_selection` | yes |
| S2 training: 2,700 episodes / 10,499 decisions at round 0; 4,300 episodes / 16,729–16,793 after round 2 (§3.4) | `students_S2_training`; `dev/v4_distill_r0.sh` (54 shards × 50) | yes |
| Pilot3 rows n = 186 / 177 (§5.6) | `14_rb_frontier` | yes |

### Statistics
| Claim | Evidence | Match |
|---|---|---|
| Crossed episode × seed bootstrap, B = 10,000; one-sided 5 %/95 % for H2; 2.5 %/97.5 % for ci95 | `stats.crossed_bootstrap_diff` (n_boot 10000); `analysis_s2_v4.py`/`analysis_e5_v4.py` use alpha = 0.025; H2 uses the default 0.05 | yes |
| No multiplicity correction; TOST and Holm not run (§4, §7) | `holm` and `tost` are defined but not called by any analysis script | yes (stated honestly) |
| D4 threshold −1.46 pp | −0.04 + 1.645 · 0.02180 · √0.5 = −0.01464 | yes |
| H2-S2: Δ −0.4452, LB −0.7485, UB −0.1616, p 0.0064 | recomputed from `results/v4/h2`: identical | yes |
| "LB … about 2.9 one-sided half-widths (0.293)" (§5.4) | lower half-width = diff − LB = 0.303 (0.849/0.303 = 2.8); 0.293 is the mean of the lower and upper half-widths | **minor mismatch** |
| S2 val→test widening "≈ 2.0 combined SE" (§5.3) | √(0.0218² + 0.0312²) = 0.038; 0.074/0.038 = 1.95 | yes |
| Per-seed widening 5.4 / 11.2 / 5.7 pp; G\* +3.9, student −3.5 (§5.3) | test per-seed vs val per-seed; 0.5533 − 0.514; 0.4511 − 0.486 | yes |

### Hyperparameters (code)
| Claim (Table 1 / §3) | Code / config | Match |
|---|---|---|
| Distillation: Adam lr 1e-3, β_T 4, λ 0.5, batch 256, ρ 0.05 | `distill.py` HP_GRID[0], RHO; `d4/*.json distill_config` | yes |
| S2: 200 fixed epochs per round, hp 0 reused | `distill_config.max_epochs` 200, status `max_epochs`; scripts `--fixed-epochs 200 --hp 0` | yes |
| PPO clip 0.2, 4 epochs; config 2 lr 1.09e-3, ent 1.33e-4, batch 128, critic lr 1.43e-3 | `train_v2.py` defaults; sweep row cfg 2 | yes |
| ball-sPCE L = 4095, J = 16, cap 8.318 | `gt3.py`, `train_v2.py`; log(4096) = 8.318 | yes |
| σ_p = 1.0 mm, σ_n = 5°, ±15 mm box | `likelihood.py`, `pf.py XY_HALF` | yes |
| 64 × 8 = 512 actions, 5.625° step | `travel.py` with TOUCHBED_NPHI = 64 (recorded in log headers) | yes |
| H3: 32 screened first actions | `g2.py C1 = 32`; log header `C1: 32` | yes |
| H3 κ = 2 row run at τ = 4.7 (§3.1) | `results/v3/g2/S_k2_000.jsonl` header: kappa 2.0, tau 4.7 | yes |
| "K = 8 near-symmetric base/variant **pairs**" (§3.1) | `shapes.make_set_S`: "Four near-symmetric bases + one symmetry-breaking variant each (K = 8)", i.e. 4 pairs and 8 identities | **mismatch (wording)** |

### Reported numbers (spot-checked, all in the evidence JSONs)
Table 2 rows R1–R7; Table 3 (all 9 columns × 3 rows); Table 4 (the G\*, student, RL, B-fan and random travel, probe and
zero-move columns); Table 5 (rows, per-seed successes, and 20 paired contrasts with ci95); Table 6 (6 contrasts × 2
configurations, latencies 20.8/46.0 ms recomputed as medians of the logged per-decision latencies); §5.1 instrument
checks (0.8290, 0.7438, 0.7166, 0.00254/0.00374, bias ratio 0.957); §5.3 label fit (train top-1 0.511–0.534, R̄
0.169–0.206, held-out top-1 0.483–0.507, belief top-1 0.327–0.362); §5.4 (SD ratio 3.29, success range 7.7 vs 1.0 pp,
cap saturation 5.8 % and 0.4–3.4 %, "3 of 6 S12 learner seeds below G\*"); §5.6 latency decomposition (0.408 ms, 0.9135
s, ratio 2238, 0.0402/0.0967/0.7169 s, 3.22); Pearson r 0.162/0.238/0.141; 0 identical action sequences. **All match.**

### Other evidence-level issues
- **Table 2 R1 marks S2 "pass" with no measurement.** The rule is "n\* = 4 probes", but `12_cal_analysis.verify`
  holds a probe count for S_k12 (3.96) and A_k12 only. No S_k2 count exists. The only S2 probe figure is the test
  value of 3.873 (Table 4), which is lower than S12's 3.96. The introduction's "budget recalibrated so that the
  planner still executes four probes" is not supported by a calibration verification.
- **Unresolved placeholders.** `[PENDING:v4:14_s2_analysis.test3_sub8.rows.random]` appears in Table 5 (two cells)
  and in the Figure 1 inset note.
- **Image-generation prompt in the draft.** The draft opens with a full image-generation prompt for Figure 1. It must
  not appear in a submission.
- **Out-of-date random row (for information).** The JSON says 215 episodes and the raw files now hold 245
  (success 0.118 on the available episodes). The paper is consistent with the JSON but will be out of date once the
  analysis is re-run.

### Length check
Words per section: Abstract 244, Introduction 904, Related Work 623, Method 1,655, Experiments 1,272, Results 2,182,
Discussion 549, Limitations 290, Conclusion 231. Total about 7,970. Every section is above its threshold. The paper
is more likely to run *over* a 9-page limit, given six dense tables.

### Topic check
The paper stays on topic: look-ahead headroom over cost-aware greedy, and distillation vs RL in S12 and S2. Two
borderline items:
- **C4 (evaluator resolution, the g_T/BI disagreement, the validation/test discrepancy)** presents instrument
  problems as a contribution. The g_T/BI disagreement is an informative methods finding. The failure of evaluator
  gate E′ and the unexplained validation/test gap are limitations, not contributions.
- **C5 (latency)** is on topic, because amortization needs a cost comparison.

---

## Reviewer A (methodology and evidence)

**Summary.** The paper measures one-step look-ahead headroom over a cost-aware greedy information-gain touch planner
(G\*) and asks whether a belief-free DeepSets head can amortize G\*, trained either by DAgger on G\*'s per-action scores
or by PPO on a contrastive ball-information bound. It does this in a stay-and-probe cell (κ = 12) and a travelling
cell (κ = 2). Headroom is small (UB 2.2 % at κ = 12). Neither learner passes its non-inferiority gate. Distillation
does not beat RL on RL's objective, and in S2 the point estimate favours RL. The study is pre-registered, and every
outcome is negative or exploratory.

**Strengths.**
1. **Exceptional traceability.** Every number I checked, more than 150 values, matches the result JSONs, and the key
   S2 and E5 rows recompute exactly from the raw per-episode logs. Seeds, episode ranges and splits are stated
   precisely.
2. **Real pre-registration discipline.** Gates, thresholds, the outcome map and the v4 amendment are respected. Failed
   gates are reported as failures (D3 twice, D4 once, E′), and the descoped items (Holm, TOST, BC rows) are listed.
3. **Paired design with a crossed episode × seed bootstrap.** The design suits a setting with three seeds, and the
   paper is candid that the seed dimension is coarse.
4. **A validated headroom estimator.** It has a known-gap construction checked twice, a zero-gap bank and an
   independent bias check. Its scope is stated precisely: one deviating step, screened candidates, reduced completion.
5. **Clear limitations.** These include test-split reuse, the unconverged evaluator, the borrowed δ, untuned RL in S2
   and the incomplete Lat′ protocol.

**Weaknesses.**
1. **Statistical power.** Three seeds per learner, one cell per regime and no equivalence test mean that every
   learner comparison except "G\* > learners" is uninformative. H2 at S12 has one-sided bounds of ±0.31 nats against a
   +0.10 margin, so the test could detect only very large effects. Calling H2 "rejected" (§5.4, Table 2 R6)
   overstates the result. The correct verdict is "not supported" or "not detected", the term already used for H2-S2.
2. **Unexplained validation/test discrepancy in S2.** The gap widens by 5–11 pp per seed between val3 and test3, about
   2 combined SE. It is the paper's largest S2 effect, and its cause is untested. The test rows were produced on more
   than one machine and pipeline (the logs show different Python and numpy versions). Before the S2 test contrast is
   interpreted, a reviewer needs a check that the same G\* code and grid re-read produce the val3 rows (for example,
   re-run 50 val3 episodes through the test pipeline).
3. **Evaluator resolution.** Gate E′ failed. Success flips on 7.5 % of episodes between sub-4 and sub-8, and no finer
   grid was checked. Many success contrasts are a few points wide (student − RL +2.6/+2.8 pp; E5 −0.6 to −2.2 pp), so
   they are within the evaluator's own resolution.
4. **The S2 calibration is not verified.** Table 2 R1 says "pass" for S2, but no probe-count verification exists. On
   test, G\* executes 3.873 probes in S2.
5. **Test-split reuse.** test3 0–299 now carries the long student, B-fan, all S2 rows and E5. The exploratory claims,
   especially the S2 student > B-fan separation highlighted in the abstract, rest on a reused split.
6. **The "half-width 0.293" figure is imprecise** (the lower half-width is 0.303). This is minor.
7. **Shape-library wording.** "K = 8 … base/variant pairs" should read "K = 8 identities (4 base/variant pairs)".

**Actionable revisions.**
- Replace "H2 is rejected" with "H2 not supported (not detected)". Add a post-hoc minimum detectable effect for H2
  and D3/D4 given the observed SE.
- Diagnose the S2 validation/test gap. Re-evaluate a val3 subset through the test pipeline and machine, report G\*'s
  val3 vs test3 success on a common grid, or move the S2 test contrast to the appendix as unresolved.
- Add the missing S_k2 calibration-verify row (mean probes at τ = 4.7 over the 200 calibration episodes), or change
  R1 to "τ set; probe count not verified".
- Resolve the `[PENDING]` cells, ideally with the complete 300-episode random row, and remove the Figure 1 generation
  prompt from the manuscript.
- Fix the K = 8 wording and the 0.293 half-width.
- Report success contrasts together with the evaluator's flip rate, or add a sub-16 check on a subset.

**Score: 4/10 (borderline, leaning reject).** The paper is methodologically honest and fully traceable, but its
evidence base (three seeds, one cell per regime, an evaluator that failed its gate, an unexplained validation/test
gap) cannot support the comparative conclusions it draws.

---

## Reviewer B (novelty, significance and fit for NeurIPS/ICML)

**Summary.** The paper characterizes greedy cost-aware touch selection and two amortization routes in a planar
simulation, and it reports mostly null or negative findings.

**Strengths.**
1. **A useful question, framed carefully.** The paper asks whether myopic greedy selection is near-optimal under
   travel cost, and whether planner distillation beats RL on RL's own objective. Its answers (small one-step headroom;
   no detectable distillation advantage) are useful negative evidence for practitioners.
2. **The two-regime design.** Adding S2 after finding that S12 is stay-and-probe is good scientific practice. The
   behavioural diagnosis (travel, zero moves, the Pearson coupling of student and G\* travel) explains what each
   policy actually does.
3. **The g_T vs grid-posterior ordering inversion.** The contrastive objective ranks G\* below both learners, while
   the grid posterior ranks it above. This is a valuable caution for amortized BOED work that reports sPCE-type
   bounds as the quality metric.
4. **A comparison against reduced planners (E5).** The paper compares the students with shrunken planners, not only
   with full-size G\*. Amortization papers often omit this comparison.

**Weaknesses.**
1. **Limited novelty.** The paper proposes no new method (it says so). The headroom result replicates the previous
   iteration's estimate, and greedy near-optimality is expected from (adaptive) submodularity. The outcome is a
   characterization paper with null results in a single simulated planar domain.
2. **Limited generality.** The study covers one shape library, two κ values, one head architecture, three seeds per
   learner, simulation only, and no held-out shapes or hardware. The S12 → S2 contrast is "one cell per regime" with
   no cross-cell test, so the regime-dependence story (for example, "the student separates from B-fan only when the
   planner travels") is anecdotal.
3. **The learners are not shown to be well tuned.** RL was not re-tuned for S2, and its configuration sits at the edge
   of the learning-rate grid. The S2 student reuses S12 hyperparameters. RL ends at exactly 3 probes in both cells,
   and it travels 2.9× (S2) to about 4× (S12) as far as G\*. This suggests a degenerate optimum of the contrastive
   reward under the travel budget, not a fair comparator. The H2 comparison therefore says more about this RL setup
   than about RL.
4. **The belief-input control is uninformative.** It is under-fit (train top-1 0.33–0.36), so the representation
   question (belief-free head vs belief input) stays open. It is the most natural explanation for the learnability
   failure.
5. **Presentation.** The paper is dense and has six large tables. Several contributions (C4, C5) are instrument
   or cost notes. The headline claims are hedged so heavily ("not shown", "exploratory", "uncorrected") that a
   NeurIPS/ICML reader has few positive takeaways. A Figure 1 generation prompt and `[PENDING]` placeholders remain in
   the draft.
6. **Topic drift.** C4 turns instrument problems (the failed evaluator gate, the validation/test discrepancy) into a
   listed contribution. These belong under limitations or a methods appendix.

**Actionable revisions.**
- Broaden the evidence. Use at least 2–3 cells per regime (other κ values or shape sets), 5+ seeds per learner, and a
  registered cross-cell test for the regime claims.
- Make the comparators credible. Run a small S2 RL sweep that extends the learning-rate grid past its edge, add a
  probe-count-aware reward or constraint so RL does not collapse to 3 probes, and fix the belief-input student's
  under-fit (wider head or longer training) so the representation question can be answered.
- Measure regret on student-visited states, to test the covariate-shift explanation the discussion raises.
- Reframe the contributions. Fold C4 into limitations or a methods appendix. Make C1 (bounded headroom) and the
  g_T-vs-posterior inversion the headline, and consider a venue suited to careful negative results (for example, a
  robotics venue, a workshop, or TMLR).
- Time E5's reduced planners and the students under Lat′, and plot a latency–accuracy frontier.

**Score: 3/10 (reject for NeurIPS/ICML in its current form).** The work is rigorous and honest, but it makes an
incremental, domain-narrow, largely null contribution with under-powered learner comparisons. With broader cells,
tuned comparators and a resolved validation/test gap, it could make a solid TMLR or robotics-venue paper.

---

## Consolidated mismatch list
1. §3.1: "K = 8 near-symmetric base/variant pairs". The code (`touchbed/shapes.py: make_set_S`) has 4 base/variant
   pairs, which is K = 8 identities.
2. Table 2 R1 and §1 ("budget recalibrated so that the planner still executes four probes"): S2 is marked pass, but
   `12_cal_analysis.verify` has no S_k2 probe count. Only S_k12 (3.96) and A_k12 are verified, and the S2 test G\*
   executes 3.873 probes.
3. §5.4: "about 2.9 one-sided half-widths (0.293)". The lower one-sided half-width is diff − LB = 0.303, so the ratio
   is 2.8. The figure 0.293 is the mean of the lower (0.303) and upper (0.284) half-widths.
4. §4 and §7, "215 of 300 episodes": consistent with `14_s2_analysis.json`, but `results/v4/test3_sub8` now holds 245
   random episodes, so the reported count is out of date.
5. Table 5 (S2 random success/BI) and the Figure 1 inset: unresolved `[PENDING:v4:14_s2_analysis.test3_sub8.rows.random]`
   placeholders.
6. Table 2 R6 and §5.4, "H2 is rejected": the evidence (LB −0.31 ≤ +0.10) shows only that H2 was not detected, not
   that it was rejected. This is a wording issue, and it is inconsistent with the "not detected" verdict for H2-S2.
