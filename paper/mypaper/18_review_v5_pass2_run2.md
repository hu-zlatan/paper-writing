<!-- Stage 18 PEER_REVIEW [v5] pass 2 run 2, run 41, 2026-11-09; fresh-context subagent; template peer_review.md verbatim; RSS/CoRL pair -->

# Peer review: "Amortizing a Cost-Aware Information-Gain Touch Planner under Travel Cost: A Pre-Registered Five-Cell Characterisation"

Two independent perspectives are given, written as a demanding RSS / CoRL reviewer pair:

- **Reviewer A** covers significance and positioning for robotics.
- **Reviewer B** covers methodology–evidence consistency. Reviewer B checked the draft against `results/v5/`, `results/v4/`, `results/v3/`, `code/`, `experiments/` and `docs/07c_amendment_v5_{0,1}.md`.

The spot-check log (35 items) is in Section 3. The answers to checks 1–5 of the review instructions are in Section 4.

---

## 1. Reviewer A: significance and positioning for robotics

### Summary
The paper asks whether a DeepSets policy distilled by DAgger from a cost-aware greedy ball-EIG/c touch planner (G\*) matches that planner. It also compares the policy with PPO trained on a ball-sPCE reward using the same head, and with three probing heuristics. There are five pre-registered cells: one planar library S at κ = 2/4/8/12, and A16 at κ = 2. The primary gate D5 fails in all five cells. On test5 the student is 0.2–2.5 pp below G\*, with CIs about 10–12 pp wide. It beats the pilot-chosen heuristic in 4/5 cells under Holm. It beats RL on RL's own objective only where RL collapses (A16-2). No trend of the gap with travel is detected. The student is 2,523–9,933× faster per decision.

### Strengths
1. **Rigour of a kind rarely seen in robot-learning papers.** The amendments were written before the runs. The reduction order was frozen before sizing. Weight hashes were recorded before test5 (I verified two of them). The Holm families are declared, and the deviations are stated openly (Section 4, items a–d). The paper does not over-claim, and its headline is a negative result.
2. **The same head is used for both learners.** The DAgger student and the PPO policy share `RelDeepSets`, the action set and the masking (`code/touchbed/train_v2.py:99-100`, `code/touchbed/distill.py:136-146`). So the "training signal is the isolated variable" claim holds at the code level.
3. **The contrastive bound and the posterior read-out are reported together.** In the S cells G\* has the lowest g_T but the highest success. That is a useful caution for the amortized-BED community, and the paper correctly frames it as an observation, not a finding.
4. **The limitations section is honest and specific** (13 items). Teacher variance, evaluator resolution, the time-guarded `rl_success` arm, and the DAgger rounds being indistinguishable from BC on the selection metric are all stated.

### Weaknesses
1. **The robotics contribution is too narrow for RSS/CoRL.** The setting is a planar polygon, a single fingertip on a fixed 100 mm circle (`code/touchbed/geometry.py:12`) and 3–4 probes per episode. The world is simulated with exactly the softened likelihood the planner and filter use (`code/touchbed/likelihood.py:1-8`, 64-73), so there is no model mismatch, no contact dynamics, no 3D and no hardware. The related systems the paper cites (Tac2Pose, TACTFUL, Zheng et al., Gordon et al.) all deal with at least one of these. With a 3–4 step horizon and a 512-action set, the problem is close to a contextual bandit with budget coupling. The paper's own result (no regime dependence detected, small gaps) suggests the setting is not hard enough to separate the routes.
2. **The motivating premise is not established.** The paper argues for amortization because G\* takes "up to seconds" per decision (median 0.91–4.88 s, Table 4). But no physical probe-time model is used. More importantly, the obvious alternative, a smaller planner, is called "unevaluated" (Section 5.2, Discussion, Limitation 7). That is not quite right: the repository already holds reduced-planner accuracy (see Reviewer B, M1). On S12 test3 in v4, `g125_512_16` was −6.7 pp below G\* (ci95 [−12, −1]) and `g500_512_4` was −5.0 pp ([−11, +1.3]). Neither was better than the v4 students. This is the one comparison a robotics reader most wants, and the paper sets it aside.
3. **Significance of the negative result.** "A distilled policy is 1–3 pp below its greedy teacher, the CIs cannot tell, and RL is worse" is not surprising. Prior DAgger/BC-of-planner work (e.g. Choudhury et al. 2017, Nguyen et al. 2024) would predict it. The registered gate (an effective −1.2 to −1.7 pp threshold) is so tight that failing it carries little practical information. A practitioner would likely accept a 2–3 pp loss for a 10³–10⁴× speed-up. The paper does not say what margin matters for a robot task.
4. **The RL comparator is weak by construction.** One configuration was swept on S2 with one seed and reused everywhere. It collapses to 2 probes in A16-2 (4/5 seeds). On the sampled-policy metric the selection rule's winner (cfg 6) is not even the best (cfg 1: 6.316 vs 6.205). "Distillation vs RL" therefore reduces to "distillation vs an untuned RL outside S2". The authors acknowledge this, but it removes most of C3's value.
5. **The A16 "second library" is less independent than presented.** `make_set_A(0, 16)` contains the v3 library A (K = 8) as its first 8 shapes (`code/touchbed/shapes.py:98-99, 192-199`). A16 also changes K, n\* and the shape family at once and is run at one κ, so it adds little evidence about generalisation.
6. **Length and presentation.** The draft has about 10,760 words plus 7 tables and a 4-panel figure, well over the 8-page RSS / 9-page CoRL budget. The abstract (269 words) is over typical limits. There are three `[CITE-MISSING]` placeholders (DeepSets, Holm, Efron). Much of the text reads like a pre-registration audit log ("report-only", "PH", "DEC", "GATE") rather than a paper.

### Actionable revisions
1. Add the reduced-planner comparison:
   - Report the existing v4 E5 S12 accuracy rows and the v3 `14_rb_frontier` rows as prior-round evidence, which addendum v5.1f designates as the accuracy side of the frontier.
   - Or run `g125_512_16` / `g500_512_4` on test5 in at least two cells.
   - Without this, the case for learning over a smaller planner is unsupported.
2. State a task-level margin: what success loss is acceptable for what saving in time. Then convert latency into episode time under at least one explicit probe-time model (for example 1–2 s per probe stroke, planning in series).
3. Re-position the contribution as a "measurement / negative-result" short paper, or extend it to a setting where amortization plausibly matters: longer horizons, 3D, or model mismatch between simulator and planner likelihood.
4. Tune RL per cell, or remove the "distillation versus RL" framing from the title and contributions.
5. Cut the paper to the page budget. Move the decision-record minutiae, E7 and the checkpoint/DAgger audit to an appendix. Fix the three missing citations.

### Score and verdict (Reviewer A)
**Score: 3 / 10 (Reject).** The study is careful and honest, but the robotics significance is low: planar simulation, no model mismatch, 3–4 probes, a negative primary result and an untuned RL comparator. The key practical alternative (a cheaper planner) is set aside even though data exist. Not recommended for RSS / CoRL in this form. It could suit a workshop or a negative-results / reproducibility track.

---

## 2. Reviewer B: methodology–evidence consistency

### Summary of verification
I re-derived the headline numbers from the analysis JSON. I recomputed the S4 and A16-2 student − G\* success contrasts and the G\* travel from the raw test5 JSONL (`results/v5/test5/`). I read the statistics code and the D5, test5 and E6 analysis scripts. I checked the run manifests in `experiments/` against the described hyper-parameters, and two weight hashes against `13_freeze.json`. **The numbers in the paper match the evidence almost everywhere.** Trial counts, seeds, tests and hyper-parameters are as stated. I found no fabricated results. The problems are omissions and a few imprecise descriptions, listed as M1–M5 below.

### Strengths
1. **Trial counts and seeds are exactly as claimed.**
   - test5: 300 episodes for every method in every cell, and g_T is complete (`14_test5_analysis.json > <cell> > episodes_per_method`, `gt_episodes_per_method`).
   - val3: 500 episodes (`12_d5_analysis.json`).
   - Students use seeds 701–705, RL 711–715 and `rl_success` 711–715.
   - 25/25 RL cfg-6 runs reached 200,192 episodes (`16_report_rows.json > rl_main_cfg6`).
2. **The statistical tests exist and are implemented as described.** The crossed episode × seed bootstrap uses 10,000 resamples (`code/touchbed/stats.py:13-31`). Holm step-down is applied to two families (`code/analysis_test5_v5.py:171-177`). H5b is a WLS with inverse-bootstrap-variance weights (`analysis_test5_v5.py:123-151`). H2-v5 uses a one-sided α = 0.05 lower bound (`:106`). D5 uses the 1.645·√0.5 = 1.163 factor (`code/analysis_d5_v5.py:46`).
3. **Deviations are disclosed rather than hidden.** These are the test5 cut (consistent with addendum v5.1e), the missing frontier, flip rates for only one seed, and the `rl_success` truncation (training lengths match `16_report_rows.json` exactly).

### Factual mismatches and imprecisions (ranked)
- **M1 (substantive omission). Reduced-planner accuracy is described as "unevaluated" / "not measured", and deviation (b) misstates the registration.**
  - Addendum v5.1f (`docs/07c_amendment_v5_1.md:115-116`) says: "the accuracy side of the frontier is test5 success / BI (G\*, students) and, for the reduced configs, the v4 E5 rows only where they exist (S12); no new reduced-G\* accuracy runs are added in v5."
  - Those rows exist in evidence (a2), `results/v4/results_v4.json > 14_e5_analysis.json`. On S12 test3 (n = 300): `g125_512_16` − G\* = −0.0667 [−0.12, −0.01]; `g500_512_4` − G\* = −0.05 [−0.11, +0.013]. Both are 2–5 pp below the v4 students. There are also v3 `14_rb_frontier` pilot rows.
  - The draft instead says "No reduced-G\* accuracy was measured on test5, so the reduced configurations were timed only and no frontier is reported" (Section 4 (b)). It also says "the most obvious cheap alternative to learning unevaluated" (Section 5.2), "this study cannot say whether learning is needed" (Section 6), and "the cheapest alternative to learning, a smaller planner, is unevaluated" (Limitation 7).
  - The registered frontier did not need test5 reduced-G\* runs. A frontier (S12, prior-round accuracy) was deliverable but not delivered, and the existing evidence bears directly on the paper's main practical question.
- **M2 (description vs code). The inversion check tests only one direction.**
  - The paper says the check asks "whether g_T and the posterior success read-out order the student and RL in opposite directions".
  - The code claims inversion only if `rl_minus_student_gT` ci95 > 0 **and** `student_minus_rl` success ci95 > 0 (`code/analysis_test5_v5.py:110-112`). This matches the docstring ("RL higher g_T, lower success") but not the bidirectional wording.
  - No cell would flip, because there is no student-higher-g_T / RL-higher-success cell. The wording should still match the code.
- **M3 (undisclosed overlap). A16 contains the earlier library A.**
  - `make_set_A(0, 16)` generates from the same seed stream as library A (K = 8) of v3, so A16's first 8 identities are the v3 library A (`code/touchbed/shapes.py:98-99, 192-199`). Library A was used in v3 calibration (`results/v3/results_v3.json > 12_cal_analysis > n_star.A`, `tau.A_k12_*`).
  - Section 3.1 presents A16 as "the second library". It should say that half of its identities are the earlier A library.
- **M4 (undisclosed reuse). S2 and S12 round-0 labels are reused from v4 and v3.**
  - The r0 distillation commands read `results/v4/labels/S_k2_r0_*` (60 shards) and `results/v3/labels/S_k12_r0_*` (30 shards), with the held-out block from the same files (`experiments/v5_d5_r0_S2_S12_rerun.json`).
  - Amendment v5.0 E1 allows this. But the paper discloses only the reuse of G\* *validation* rows, while Algorithm 1 / Table S read as 3,000 fresh labels per cell.
- **M5 (minor numeric rounding). Student latency spread.**
  - "differ by up to about 24 % within a cell": the largest within-cell spread, including seed 701, is 24.8 % (A16-2: 0.3261 vs 0.407 ms; `14_e6_analysis.json`). Write "about 25 %".
  - "Other seeds' student medians (0.36–0.51 ms)": job-2 medians are 0.363–0.513 ms. That is correct.

### Methodological weaknesses (not mismatches)
1. **The primary comparison is under-powered by design.** CIs of 9.6–12.3 pp against δ = 4 pp, together with an effective D5 threshold of −1.2 to −1.7 pp, mean that neither "match" nor "worse" could be decided on test5. That should have been predictable from the v4 SEs before the 500 → 300 cut. Counting m = 0 as the registered answer while test5 shows 0.2–2.5 pp gaps makes the headline ("matching is not supported") depend mostly on the gate design.
2. **Teacher variance is excluded.** G\* was run once per cell (`n_seeds` [5, 1]). G\* uses nested-MC scores (M = 64), so its run-to-run variance is part of the comparison and the CIs are too narrow. The authors say so, but one rerun in one cell would bound it.
3. **The validation G\* rows are mixed across rounds** (S2 from v4, S12 from v3; `12_d5_analysis.json > gstar_source`). Addendum v5.1b justifies this as the same code path. Still, the v4 S2 gate with seeds 601–603 gave Δ̂ = −0.028, and the v5 S2 gate with the new best-checkpoint recipe gives −0.0328. The pre-declared remedy did not help S2, and the paper does not say this.
4. **The DAgger selection metric is blind to DAgger.** Checkpoints are selected on G\*-visited held-out decisions, and several r1/r2 rounds keep epoch 0–5 (verified: A16-2 s701 r2 epoch 0, S2 s705 r2 epoch 5, S12 s703 r2 epoch 4). The "DAgger" student is effectively BC plus fine-tuning. The paper discloses this. An on-policy regret read-out is the obvious fix.
5. **Unused evidence that would help C2 and C4.** The E6 job-1 logs record the action each method picks on the same states (`results/v5/lat/*_s701_gstar_d1000.jsonl > actions`). I computed top-1 agreement with full G\* (reviewer computation, exploratory, not in the paper):
   - student 0.18 / 0.30 / 0.46 / 0.51 / 0.33 (S2 / S4 / S8 / S12 / A16-2);
   - `g125_512_16` 0.10 / 0.18 / 0.24 / 0.31 / 0.15;
   - `g500_512_4` 0.07 / 0.12 / 0.21 / 0.24 / 0.09.

   On G\*'s own states, the student agrees with G\* more often than either reduced planner does in every cell, and agreement rises as κ grows. This is cheap, already-recorded evidence for the "student vs smaller planner" question and for the travel story. It should at least be reported as report-only.
6. **Multiplicity and many report-only rows.** More than 30 uncorrected contrasts are reported. That is acknowledged, but the main text should keep only the registered ones.
7. **"RL on the same objective" is imprecise.** G\* greedily maximises ball-EIG per unit cost, while RL maximises the terminal ball-sPCE g_T under the budget. The figure caption calls PPO's reward "G\*'s information objective". These are related but not the same objective.

### Actionable revisions
1. Correct deviation (b) and Section 5.2 / Section 6 / Limitation 7 to report the registered prior-round S12 frontier (v4 E5) with its caveats: different split (test3), v4 students. Add the action-agreement read-out from the E6 logs as report-only.
2. Reword the inversion definition to "RL higher on g_T and lower on success (both ci95 excluding 0)", or implement the symmetric check.
3. Disclose that A16 ⊃ v3 library A, and that S2/S12 round-0 labels and held-out blocks were reused from v4/v3.
4. State that the v5 recipe did not improve the S2 validation gap over v4 (−2.8 → −3.3 pp, different seeds).
5. Run one G\* rerun in one cell (cheap at test5 scale), or add a G\*-vs-G\* paired difference, to bound teacher variance.
6. Fix the three `[CITE-MISSING]` placeholders and the 24 % → about 25 % rounding.

### Score and verdict (Reviewer B)
**Score: 4 / 10 (Borderline, leaning reject).** The evidence is internally consistent and honestly reported, and I found no fabrication. But the primary comparison is under-powered by design. The main practical comparator (reduced planner) is called unevaluated although registered prior-round evidence exists. Several reuse and overlap facts are not disclosed. The DAgger and RL arms are each weakened by acknowledged design choices. As a methods/measurement record it is exemplary; as an RSS/CoRL contribution it does not yet answer a question a roboticist would act on.

---

## 3. Spot-check log (35 checks)

| # | Claim in paper | Evidence (file > field / line) | Result |
|---|---|---|---|
| 1 | test5 = 300 episodes per method per cell, g_T complete | `results/v5/14_test5_analysis.json > <cell> > episodes_per_method`, `gt_complete` | match (all 300, true) |
| 2 | Raw S4 student − G\* success −0.02533 | recomputed from `results/v5/test5/S_k4_{gstar,student_s70x}_*.jsonl` (300 eps, no duplicates) | match (−0.025333) |
| 3 | Raw A16-2 student − G\* −0.002; G\* travel 21.22° | recomputed from `results/v5/test5/A16_k2_*` | match |
| 4 | test5 CI widths 9.6–12.3 pp; tightest LB S8 −6.1, S4 −8.3 | `14_test5_analysis.json > student_minus_gstar.success.ci95` | match (0.096–0.1233) |
| 5 | Holm: 0/5 vs G\*, 4/5 vs H\* (S2 not) | `holm_reject_5cells`; `code/touchbed/stats.py:34-44` | match |
| 6 | Bootstrap 10,000 resamples, two-sided p resolution 0.0002 | `code/analysis_test5_v5.py:42,62-65` | match |
| 7 | `n_seeds` [5,1] vs G\*/H\*, [5,5] vs RL | `14_test5_analysis.json > n_seeds` | match |
| 8 | D5 clause (i) = max(−0.02, −δ + 1.163·SE); S2 threshold −0.01454 | `code/analysis_d5_v5.py:46`; `12_d5_analysis.json > S2.succ.threshold` | match (−0.014538) |
| 9 | D5 seeds ok 3/1/4/3/0; per-seed range −0.068 to −0.01 | `12_d5_analysis.json > seeds_ok, per_seed` | match |
| 10 | D5 validation means and Δ̂ (Table 1) | `12_d5_analysis.json > succ.student_mean/gstar_mean/delta_hat` | match |
| 11 | G\* validation sources S2 v4, S12 v3 | `12_d5_analysis.json > gstar_source`; `docs/07c_amendment_v5_1.md:55-58` | match |
| 12 | H\* = B-cov/B-fan/B-cov/B-fan/B-fan with pilot success | `results/v5/12_base_hstar.json` | match |
| 13 | Best test5 heuristic and post-hoc margins +3.5 to +14.5 pp | `results/v5/15_posthoc_derived.json > margin_student_minus_best_test5_heuristic` | match |
| 14 | B-spread below Random in 4/5 (not S4) | `14_test5_analysis.json > means` | match |
| 15 | H5b slope −0.0157/rad [−0.104, 0.073]; per 100° −0.02741; weights 1469.5…1047.6 | `14_test5_analysis.json > H5b` | match |
| 16 | Span translation −0.07393 to +0.05167 | `15_posthoc_derived.json > H5b_span_translation` | match |
| 17 | H2-v5 LBs −0.4971/−0.6555/−0.4861/−0.3044/+0.5964; inversion false 5/5 | `14_test5_analysis.json > H2_v5` | match |
| 18 | Inversion wording ("opposite directions") | `code/analysis_test5_v5.py:110-112` | **imprecise (M2)**: one direction only |
| 19 | Table 3 g_T means and contrasts | `H2_v5 > means_gT, rl_minus_student_gT, gstar_minus_*` | match |
| 20 | `rl_success` lengths 123,392 / 124,672 / 181,760 / 200,192 / 125,440 (S2); 184,576 / 113,408 / 111,104 / 162,304 / 165,888 (S12); 9/10 time-guarded | `results/v5/16_report_rows.json > rl_success` | match |
| 21 | RL cfg 6 reached 200,192 episodes in every run; clip 0.2, 4 epochs, width 128 | `16_report_rows.json > rl_main_cfg6` (25/25); `code/touchbed/train_v2.py:77-79` | match |
| 22 | RL sweep: 8 cfgs, seed 719, 10⁵ episodes, cfg 6 selected (6.300 vs 6.241); cfg 1 sampled 6.316 | `experiments/v5_rl_sweep_S2.json`; `results/v5/12_rl_sweep_selection.json` | match |
| 23 | Same head for RL and student | `code/touchbed/train_v2.py:99-100` (RelDeepSets when `--frame rel`); `experiments/v5_e3_rl_S.json` (`--frame rel`) | match |
| 24 | hp 0: lr 1e-3, β_T 4, λ 0.5, batch 256, width 128, 200 fixed epochs, best checkpoint | `code/touchbed/distill.py:25-30`; `code/touchbed/cli3.py:224-225,239`; `experiments/v5_distill2_S2_S12.json` (`--fixed-epochs 200 --keep best`); `16_report_rows.json > student_distill_configs` | match |
| 25 | Loss and floored regret formulas, ρ = 0.05 | `code/touchbed/distill.py:1-11,57-83` | match |
| 26 | DAgger: 2 × 800 episodes, β 0.5 then 0; 2,700/3,500/4,300 training episodes | `experiments/v5_dag2_S2_S12.json` (`--beta 0`, 20 × 40 eps per seed); `16_report_rows.json > student_train_episodes` | match |
| 27 | Kept R̄ ranges per cell, r0 vs r2 ranges, kept epochs 0–187, last − kept 0.0002753–0.03172 | `16_report_rows.json > student_checkpoint_sensitivity` (recomputed) | match |
| 28 | Action grid 64 × 8, ψ −35°…+35° in 10° steps; cost 1 + κ\|Δφ\|/π; radius 100 mm | `code/touchbed/travel.py:16-20,49-50`; `code/touchbed/geometry.py:12` | match |
| 29 | G\* N = 2,000, M = 64; label s = max(0, EIG)/c | `code/touchbed/cli3.py:184-187`; `code/touchbed/policies_v2.py:79` | match |
| 30 | E5 flip rates 8 / 7 / 7.5 / 6.5 %, success shifts, mean \|ΔBI\| ≤ 0.004034 | `results/v5/14_e5_analysis.json` | match |
| 31 | E7 numbers; 500-particle look-ahead; 256 independent samples | `results/v5/12_e7_analysis.json`; `code/touchbed/g2.py:3,48,63-71` | match |
| 32 | E6 medians, ratios, CIs, B = 2,000, CI rule met only in A16-2, n = 1000/500 | `results/v5/14_e6_analysis.json`; `code/analysis_e6_v5.py:2-30` | match |
| 33 | "differ by up to about 24 %" | `14_e6_analysis.json > job2` + job1 student | **rounding (M5)**: 24.8 % |
| 34 | Reduced-G\* accuracy "not measured" / "unevaluated" | `docs/07c_amendment_v5_1.md:115-116`; `results/v4/results_v4.json > 14_e5_analysis.json`; `results/v3/results_v3.json > 14_rb_frontier` | **omission (M1)** |
| 35 | Weight hashes recorded (15/10 per cell) and unchanged | `results/v5/13_freeze.json` vs `sha256sum results/v5/d5/S_k2_s701_r2.npz`, `results/v5/rl/A16_k2_rel_cfg6_sd715.npz` | match |
| 36 | A16 "second library", 8–14 vertices, edge and self-confusability rejection | `code/touchbed/shapes.py:80-110,192-199` | vertices/rejection match; **overlap with v3 A undisclosed (M3)** |
| 37 | Labels per cell | `experiments/v5_d5_r0_S2_S12_rerun.json` (v4/v3 label shards) | **reuse undisclosed (M4)** |
| 38 | Prior gates: S12 −0.05867 (thr −0.01435), −0.044 (thr −0.01681); S2 −0.028 (thr −0.01464); v4 test3 −10.2 [−16.6, −4.3] | `results/v3/results_v3.json > 12_d3_analysis, 12_d3_analysis_rem`; `results/v4/results_v4.json > 12_d4_analysis.json, 14_s2_analysis.json` | match |
| 39 | Table 0 G\* travel times and τ; A16 n\* rule 0.975, keep 0.8 | `results/v5/12_cal_analysis.json`; `results/v3/results_v3.json > 12_cal_analysis.tau` | match |
| 40 | 8,158 files under results/v5 | `find results/v5 -type f \| wc -l` | match |

---

## 4. Answers to the specific checks

1. **On topic?** Yes. Every section addresses amortizing G\* across the five cells. Environment issues (truncated `rl_success` runs, runner differences, the A16 packing bug) are reported as deviations or limitations, not as contributions. C5 ("methods notes") is the closest the paper comes to drifting, and it is correctly kept out of the decision rows.
2. **Methodology–evidence consistency.** It is consistent on numbers, tests, seeds and hyper-parameters (Section 3). Discrepancies are M1 (reduced-planner accuracy evidence omitted, and the frontier deviation misdescribed), M2 (inversion wording), M3 (A16/A overlap), M4 (label reuse) and M5 (rounding). None is a fabricated number.
3. **Trial count.** The paper claims 300 test5 episodes per method per cell, 500 val3 episodes, 5 student, 5 RL and 5 `rl_success` seeds, and 200 E5 episodes. The evidence shows exactly these. **No trial-count fabrication.**
4. **Length.** Section word counts (approximate): Abstract 269, Introduction 1,001, Related Work 719, Method 1,941, Experiments 2,356, Results 2,883, Discussion 771, Limitations 579, Conclusion 224, total about 10,760. No section is under the minimum. The paper is substantially **over** the 9-page budget, and the abstract exceeds typical limits. It needs cutting, not expansion.
5. **Top-conference assessment.**
   - Novelty: narrow. It is a measurement of known techniques (DAgger from an information-gathering expert, PPO on an sPCE reward) in a toy planar setting.
   - Baselines: the heuristics are adequate. RL is untuned outside S2. The reduced-planner baseline is timed only, although prior accuracy exists.
   - Ablations: the checkpoint and DAgger-round audits are present but uninformative on the selection metric.
   - Claims: all supported, and conservatively stated.
   - Limitations: honest.
   - Recommendation: not for RSS / CoRL main track in this form (scores 3 and 4).

---

## 5. Consolidated verdict
- Reviewer A (significance / robotics positioning): **3 / 10, Reject.**
- Reviewer B (methodology–evidence consistency): **4 / 10, Borderline (leaning reject).**

CRITICAL_FABRICATION: no
