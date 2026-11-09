<!-- Stage 18 PEER_REVIEW [v5] pass 2 run 1, run 41, 2026-11-09; fresh-context subagent; template peer_review.md verbatim -->

# Stage 18 (v5) peer review, pass 2, run 1

**Summary verdict.** I found no critical fabrication. Every trial, episode and seed count matches the results JSONs
and the raw logs. So do the statistical tests, the hyper-parameters and the decision outcomes. I checked 45 claims
(log below). I recounted five test5 rows and two val3 rows from the raw per-episode `.jsonl` files, and they
reproduce the published means. The remaining problems are factual mismatches of moderate size, five of them:

1. The paper says reduced-G\* accuracy is "unknown" and "unevaluated", and that "no frontier" was possible. The prior
   round did measure it (S12, test3). Addendum v5.1f names exactly those rows as the accuracy side of the frontier.
2. The RL-sweep "validation stream (92,160 episodes)" is a misreading. 92,160 is the number of training episodes at
   which the last validation ran. The stream itself has 500 episodes.
3. Limitation 11 says the RL episodes per seed and the label and DAgger budgets are not in a citable results field.
   They are: `results_v5.json > 16_report_rows.json`.
4. The inversion check is described as two-directional ("opposite directions"). The code tests only one direction.
5. The latency "seed spread of up to about 24 % within a cell" mixes seed with job and runner. The job-2 seeds differ
   by at most 3 % among themselves.

None of these changes a registered verdict. Items 1 and 3 change what the paper may say about the cheap-planner
alternative and about provenance.

**Scores: Reviewer A 4/10 (borderline, leaning reject); Reviewer B 3/10 (reject).**

---

## Verification log: 45 spot-checks (claim vs evidence)

### A. Counts, seeds, splits (trial-count audit)
| # | Claim (paper location) | Evidence (file > field) | Match |
|---|---|---|---|
| 1 | D5 on val3 0–499, 500 paired episodes, seeds 701–705 (§4, Table 1) | `results/v5/12_d5_analysis.json` > `<cell>.n_episodes` = 500, `per_seed` 701–705, `complete` true ×5 | yes |
| 2 | Test5 0–299, 300 per method per cell, $g_T$ complete (§4, Table S, Table 1 summary) | `results/v5/14_test5_analysis.json` > `episodes_per_method` all 300, `complete`/`gt_complete` true ×5 | yes |
| 3 | Raw recount: S2 G\* test5 success 0.5333 and probes 3.863; S4 B-cov 0.42; A16 RL s713 0.1833 at 2.0 probes; S12 student s704 0.46; S8 Random 0.09667 (Tables 2a, 5) | recomputed from `results/v5/test5/<tag>_<method>_*.jsonl`: 300 episodes each (indices 0–299); values identical | yes |
| 4 | Raw recount of val3: A16-2 G\* 0.472; S4 student s702 per-seed −0.032 (Table 1) | `results/v5/d5_val/A16_k2_gstar_*.jsonl` (500 ep., 0.472); `S_k4_student_s702_r2_*` 0.472 vs G\* 0.504 | yes |
| 5 | Weight hashes: 15 per cell (S2, S12), 10 per cell (others) (§4) | `results/v5/13_freeze.json`; freeze-before-test5 logged in `PROGRESS.md` l. 1404–1406 | yes |
| 6 | Test5 cut 500 → 300 by step (2) of the frozen reduction order, because E7 had already run (§4 Deviation a) | `docs/07c_amendment_v5_1.md` addendum v5.1e (≈1,250 → ≈975 CPU-h); E7 decided in v5.1d (run 32) before v5.1e (run 33) | yes |
| 7 | H\* on pilot3 0–199, 200 per heuristic; pilot success 0.445 / 0.43 / 0.405 / 0.41 / 0.33 (Table 1) | `results/v5/12_base_hstar.json` > `n` 200, `H_star`, `H_star_success` | yes |
| 8 | Table 0 τ: S4 0.7967 → 4.8, S8 0.8335 → 4.8, A16 0.3514 → 3.4; S2 0.7257 → 4.7, S12 0.9388 → 4.9 from earlier rounds | `results/v5/12_cal_analysis.json` > `tau`; `results/v3/12_cal_analysis.json` > `tau.S_k2_nstar4`, `S_k12_nstar4` | yes |
| 9 | A16 n\* = 3 (rule reading 0.975), keep check 0.8 ∈ [0.30, 0.90] (§3.1) | `12_cal_analysis.json` > `n_star.A16`, `keep.A16`; `docs/07c_amendment_v5_1.md` "Cells" | yes |
| 10 | Student training episodes 2,700 / 3,500 / 4,300 (Alg. 1) | `results/v5/16_report_rows.json` > `student_train_episodes` (75 runs) | yes |
| 11 | E5: 200 episodes, G\* and student 701, S2 and S12 (§4) | `results/v5/14_e5_analysis.json` > `n_episodes` 200/200 | yes |
| 12 | E6: job 1 n = 1000 (S cells), 500 (A16-2); job 2 n = 500 per seed; `job1_complete` true only in A16-2 (§4, Table 4) | `results/v5/14_e6_analysis.json` > `job1.*.n`, `job2.*.n`, `job1_complete`; `docs/07c_amendment_v5_1.md` addendum v5.1g | yes |
| 13 | E7: 32 beliefs per cell; mean candidates 29.0 / 302.0 (S2), 30.5 / 85.75 (S12) (§4) | `results/v5/12_e7_analysis.json` > `n_beliefs`, `mean_candidates` | yes |

### B. Statistical procedures vs code
| # | Claim | Evidence | Match |
|---|---|---|---|
| 14 | Crossed episode × seed bootstrap, 10,000 resamples, two-sided ci95; `n_seeds` [5,1] vs G\*/H\*, [5,5] vs RL (§4) | `code/analysis_test5_v5.py` (`N_BOOT` 10000, `ALPHA2` 0.025), `code/touchbed/stats.py::crossed_bootstrap_diff`; JSON `n_seeds` fields | yes |
| 15 | p-values resolve to 0.0002 (§4) | `p_two_sided = 2·min(p_greater, p_less)` with B = 10,000 → step 2/10,000 | yes |
| 16 | Holm over 5 cells, two families only (H5a, student − H\*) (§4) | `analysis_test5_v5.py` `main()` loops over `student_minus_gstar`, `student_minus_hstar`; `stats.holm` α 0.05 | yes |
| 17 | Student − H\* Holm 4/5 (S2 no, p 0.0558) | Holm by hand on p = (0.0558, 0, 0.0098, 0.0178, 0): thresholds 0.01, 0.0125, 0.0167, 0.025, 0.05 → 4 rejections | yes |
| 18 | H2-v5 = one-sided 95 % LB > +0.10 nats (§4) | `crossed_bootstrap_diff(gS, gR, alpha=0.05)["lower"]` = 5 % quantile; S2 LB −0.4971 lies inside the two-sided ci95 of RL − student, as it should | yes |
| 19 | D5 clause (i) threshold max(−0.02, −δ + 1.163·SE), with SE = SD of the episode × seed bootstrap (§4) | `code/analysis_d5_v5.py` (`1.645·se·√0.5` = 1.163·se); `analysis_d4_v4.boot_sd`; S2: −0.04 + 1.163 × 0.021889 = −0.01454 | yes |
| 20 | D5 seeds clause "Δ_succ > −δ", strict (S2 seed 704 at −0.040 counts as a fail) | `analysis_d5_v5.py` `v > -DELTA`; `12_d5_analysis.json` > `S2.seeds_ok.704` false | yes |
| 21 | H5b WLS slope; only the weighting rule fixed in advance (v5.1f); weights estimated from test5 (§4, §5.4) | `analysis_test5_v5.py::h5b` (w = 1 / bootstrap variance of each cell's test5 replicates); `docs/07c_amendment_v5_1.md` addendum v5.1f | yes |
| 22 | H5b span translation −0.07393 to +0.05167 (§5.4) | `results/v5/15_posthoc_derived.json` > `H5b_span_translation.ci95_times_span` | yes |
| 23 | Inversion claimed "where both orderings are resolved … in opposite directions" (§4) | `analysis_test5_v5.py` l. ~107: `inversion = ci95(RL − student g_T)[0] > 0 and ci95(student − RL success)[0] > 0`, so one direction only | **partial** (mismatch 4) |
| 24 | Latency bootstrap B = 2,000 (§4, Table 4) | `code/analysis_e6_v5.py` `B = 2000` | yes |
| 25 | E7 bootstrap and the "500 particles resampled from G\*'s decision filter" (§4) | `code/analysis_e7_v5.py` (B 10,000, rng 7); `code/touchbed/g2.py` docstring and `n_la=500` | yes |
| 26 | No equivalence test run (§7.1) | `stats.tost` exists but is not called in any v5 analysis script (grep evidence (c)) | yes |

### C. Method description vs code
| # | Claim | Evidence | Match |
|---|---|---|---|
| 27 | 64 × 8 actions, ψ ∈ {−35°, …, +35°} in 10° steps (§3.1) | `code/touchbed/travel.py` `PSI_GRID = arange(-35, 36, 10)`, `TOUCHBED_NPHI=64`; test5 log header `action_set 64x8, A 512` | yes |
| 28 | Loss: soft CE to softmax(β_T s/σ_s) + λ·hard CE; floored regret with ρ = 0.05 (§3.3) | `code/touchbed/distill.py` docstring, `soft_target`, `loss_and_grad`, `RHO = 0.05` | yes |
| 29 | hp 0: lr 0.001, batch 256, width 128, β_T 4.0, λ 0.5, 200 epochs (Alg. 1) | `16_report_rows.json` > `student_distill_configs` (75 runs, one config); every round `status: max_epochs` | yes |
| 30 | Context = relative angle, τ_rem/τ, absolute φ_t (§3.3) | `code/touchbed/relframe.py::rel_ctx` (cos/sin d, `tau_rem/tau`, cos/sin φ_t); `cli3.py` l. 413 passes the cell τ | yes |
| 31 | Teacher label s(a) = max(0, EIG_B)/c(a) (§3.2) | `code/touchbed/policies_v2.py` l. 79 | yes |
| 32 | A16: star-shaped, 8–14 vertices, trivial symmetry, minimum-edge and self-confusability rejection (§3.1) | `code/touchbed/shapes.py::make_irregular`, `make_set_A` | yes (unstated: A16 contains the v3 set A, K = 8, as its first 8 shapes, and that set was at ceiling, 0.985) |
| 33 | Heuristics: B-fan stays at φ_t and cycles ψ; B-spread maximises angular distance; B-cov coverage on the MAP particle (§3.4) | `code/touchbed/heuristics.py` class docstrings | yes |
| 34 | PPO clip 0.2, 4 epochs, width 128; cfg 6 lr/ent/batch/critic lr; 200,192 episodes in every main run (§3.3, Table S) | `16_report_rows.json` > `rl_main_cfg6` (25 runs); `results/v5/rl/S_k4_rel_cfg6_sd711.json` config | yes |
| 35 | Sweep: 8 configs, seed 719, 100,096 episodes (100,032 at batch 64); cfg 6 6.300 vs cfg 0 6.241; sampled metric favours cfg 1 (6.316 vs 6.205) (§3.3) | `results/v5/12_rl_sweep_selection.json` > `rows` | yes |
| 36 | Sweep selected "on the trainer's validation stream (92,160 episodes)" (§3.3) | `code/analysis_rl_sweep_v5.py` l. 3–4, 17: `final_val_episodes = vals[-1]["episodes"]` is the training-episode count at the last validation; the stream has `val_episodes: 500` (`results/v5/rl/*.json` config) | **no** (mismatch 2) |
| 37 | `rl_success` lengths per seed; 9/10 runs stopped by the time guard at 80 % of 330 min (§5.3) | `16_report_rows.json` > `rl_success` (`wall_s` ≈ 15,854 s = 264 min = 80 % of 330; S2 s714 `max_episodes`) | yes |

### D. Reported numbers
| # | Claim | Evidence | Match |
|---|---|---|---|
| 38 | Validation gaps 3.2–6.0 pp; per-seed −0.068 to −0.01; seeds-ok 3/1/4/3/0 (§5.1, Table 1) | `12_d5_analysis.json` > `succ.delta_hat`, `per_seed`, `seeds_ok` | yes |
| 39 | Test5 gaps 0.2–2.5 pp, CIs −8.3 to +6.1, widths 9.6–12.3 pp, tightest LB −6.1 (S8) (§5.1) | `14_test5_analysis.json` > `student_minus_gstar.success` (widths 10.27 / 11.60 / 9.87 / 9.60 / 12.33 pp) | yes |
| 40 | Post-hoc D5-on-test5 check fails in "about 4 of 5" (§5.1) | Recomputed: SE ≈ half-width / 1.96 gives thresholds −0.0095 / −0.0056 / −0.0107 / −0.0115 / −0.0034, so exactly 4/5 fail and A16-2 passes | yes ("about" is unnecessary) |
| 41 | Best-test5-heuristic margins +3.5 to +14.5 pp; H\* is not best in 4/5 cells (§5.2) | `results/v5/15_posthoc_derived.json` > `margin_student_minus_best_test5_heuristic`, `best_test5_heuristic` | yes |
| 42 | E5 flips 8 / 7 / 7.5 / 6.5 %; contrast shifts +0.02 and −0.03 (≈0.8× and ≈2× the test5 gap); mean abs ΔBI ≤ 0.004034 (§4) | `14_e5_analysis.json`; 0.02/0.02467 = 0.81, 0.03/0.01533 = 1.96 | yes |
| 43 | Latency ratios 2,523–9,933×, job-2 ranges, reduced-config timings 22.05–115.6 / 48.04–194.3 ms (Table 4) | `14_e6_analysis.json`; `15_posthoc_derived.json` > `latency` | yes |
| 44 | "Other seeds' student medians (0.36–0.51 ms) differ by up to about 24 % within a cell" (§5.2) | `14_e6_analysis.json` > `job2`: within-cell spread across seeds 702–705 ≤ 3 % (for example S12 0.423–0.437 ms). The ≈25 % gap (A16-2 0.4069 / 0.3261 = 1.248) is seed 701 in job 1 against seeds 702–705 in job 2, on different runners | **partial** (mismatch 5) |
| 45 | Prior S2 gate −0.028 (thr −0.01464); prior S12 −0.05867 (thr −0.01435) and −0.044 (thr −0.01681); v4 test3 gap −10.2 [−16.6, −4.3] (Table 1, §5.1) | `results/v4/results_v4.json` > `12_d4_analysis`, `14_s2_analysis.test3_sub8.diffs`; `results/v3/results_v3.json` > `12_d3_analysis`, `12_d3_analysis_rem` | yes |

### E. Claims contradicted by prior-round evidence or by the results record
| # | Claim | Evidence | Match |
|---|---|---|---|
| E1 | "their accuracy was not measured in this round"; "whether they lose success against full G\* is unknown" (§5.2); "the cheapest alternative to learning, a smaller planner, is unevaluated" (§7.7); "this study cannot say whether learning is needed" (§6); deviation (b): "addendum v5.1f kept the frontier as a read-out of the job-1 timings … no frontier is reported" | `results/v4/14_e5_analysis.json` (also in evidence a2): on S12 test3 0–299, sub 8, g125_512_16 has success 0.36 against G\* 0.4267, diff −0.0667, ci95 [−0.12, −0.01]; g500_512_4 has 0.3767, diff −0.05, ci95 [−0.11, +0.013]. `docs/07c_amendment_v5_1.md` addendum v5.1f: "The accuracy side of the frontier is test5 success / BI (G\*, students) and, for the reduced configs, the v4 E5 rows only where they exist (S12); no new reduced-G\* accuracy runs are added in v5." | **no** (mismatch 1) |
| E2 | Limitation 11 and §4 Implementation: "RL episodes per seed … label and DAgger budgets … are not yet in a citable results field" | `results/v5/results_v5.json` > `16_report_rows.json` > `rl_main_cfg6.*.episodes_trained` / `max_episodes` / `clip` / `epochs` / `hidden`, `student_train_episodes`, `student_distill_configs`, `student_env` (`64x8/A=512`) | **no** (mismatch 3) |

---

## Reviewer A (methodology and evidence audit)

**Summary.** The paper is a pre-registered, five-cell measurement. It asks whether a DeepSets policy distilled by
DAgger from a cost-aware greedy EIG/c touch planner (G\*) matches that planner, and how it compares with PPO on the
same head and with three heuristics. The cells are κ ∈ {2, 4, 8, 12} on library S and κ = 2 on a 16-shape library
A16. The registered gate D5 fails in all five cells. On test5 the student is 0.2–2.5 pp below G\*, with CIs about
10–12 pp wide. The student beats the pilot-chosen heuristic in 4/5 cells under Holm. H2-v5 holds only where RL
collapses (A16-2), and no trend with travel is detected.

**Strengths.**
1. The pre-registration discipline is real and auditable. The rules in `docs/07c_amendment_v5_0.md` are implemented
   line for line in `code/analysis_d5_v5.py` and `code/analysis_test5_v5.py`: the D5 threshold, Holm families, the
   H2-v5 one-sided LB, the H5b WLS and the H\* tie order. The freeze hashes and their place in `PROGRESS.md` precede
   the test5 dispatch.
2. The reporting is unusually candid. There is a Deviations paragraph, validation and test are reported separately,
   the G\* sources are mixed across rounds and flagged, the `rl_success` truncation is printed per seed, the D5
   threshold is shown to be tighter than δ, and the DAgger rounds are shown not to move the selection metric.
3. Every headline number I checked reproduces from the JSON and, where I recounted them, from the raw logs (checks
   3–4, 38–43).
4. The design is paired (shared episodes, start angle and observation stream), and the bootstrap crosses episodes
   and seeds, so student-seed variance is in the CIs.

**Weaknesses.**
1. **The reduced-planner question is misstated (mismatch 1, major).** The paper says four times that the accuracy of
   `g125_512_16` and `g500_512_4` is unknown, and it calls the missing frontier a deviation forced by missing data.
   Addendum v5.1f, which the paper cites for this point, says the opposite. The v4 E5 S12 rows are the registered
   accuracy side of the frontier, and those rows exist. They show both reduced planners 5–7 pp below full G\* on S12
   test3, with the g125 CI excluding 0. They also show both within about 3 pp of the v4 students on the same
   episodes. The split, round and student recipe all differ from v5, so these rows cannot be compared like for like
   with the v5 student. They are still exactly the evidence the Discussion says does not exist. They bear directly
   on whether learning is needed, rather than a cheaper planner.
2. **The RL tuning is thin, and the description of it is inaccurate (mismatch 2).** The sweep has 8 configurations,
   one seed and 10⁵ episodes, and selection rests on a 500-episode validation read at 92,160 training episodes, not
   on "a 92,160-episode stream". The cfg 6 vs cfg 0 margin, 0.059 nats on a single seed, is barely above the
   0.02-nat tie band. On the sampled metric cfg 1 would win. With RL collapsing in A16-2 and using about 3 probes in
   every S cell, the comparison of distillation against RL is against a weakly tuned comparator, outside S2 at least.
   The paper acknowledges this, but the C3 framing still reads as a comparison of two routes.
3. **The gate cannot pass where the paper's language suggests it could.** With SE ≈ 0.02, clause (i) needs a deficit
   of about −1.5 pp or better. That is stricter than the "4 pp margin" named in the abstract and contributions. The
   paper explains this in §4, but the abstract still says "beyond the 4 pp margin" as if 4 pp were the bar. Report
   the effective thresholds (−1.2 to −1.7 pp) in the abstract, or drop the δ framing there.
4. **The G\* run-to-run variance is missing from every student − G\* CI.** The paper says so, and it is the dominant
   unquantified term: G\* is nested Monte Carlo with M = 64 and one run per cell. The validation G\* rows also come
   from three rounds. The gap between validation and test5 point estimates is consistent across cells (test5 smaller
   in 5/5), so a G\* rerun on val3 in one cell would be cheap and informative.
5. **Smaller inaccuracies.** The inversion definition is two-sided in the text but one-directional in the code
   (mismatch 4). The latency seed spread is confounded with job and runner (mismatch 5). Limitation 11 is wrong about
   provenance (mismatch 3). "About 4 of 5" in §5.1 should read "4 of 5 (A16-2 would pass)". Three
   `[CITE-MISSING]` placeholders remain (DeepSets, Holm, Efron bootstrap). The $g_T$ estimator sizes (J = 16,
   L = 4,095; `code/touchbed/gt3.py`) are not stated.
6. **Length.** About 10,700 words with tables is well beyond 9 NeurIPS pages. §4 (2,356 words) and §5 (2,883 words)
   carry many report-only items (checkpoint sensitivity, DAgger regret ranges, E7 in full) that belong in an
   appendix. No section is under-length.

**Actionable revisions.**
- A1. In §5.2, §6, §7.7 and deviation (b), report the v4 E5 S12 reduced-G\* rows (success, ci95, n = 300, test3,
  prior recipe) as registered prior evidence, as addendum v5.1f specifies. Replace "unknown" and "unevaluated" with
  "measured once in the prior round on S12 only (−5.0 and −6.7 pp vs full G\*); not measured on test5 or in other
  cells". Correct the paraphrase of v5.1f.
- A2. In §3.3, replace "validation stream (92,160 episodes)" with "500-episode trainer validation stream, last read
  at 92,160 training episodes".
- A3. Delete or correct Limitation 11 and the matching §4 sentence. Cite `results_v5.json > 16_report_rows.json`
  for the RL episodes, the distillation config and the student training episodes. Only the action grid, planner
  sizes and bootstrap sizes remain code-only.
- A4. State the inversion rule as in the code: "RL higher on $g_T$ and student higher on success, both ci95
  excluding 0".
- A5. In §5.2 say the ≈20–25 % difference is seed 701 (job 1) against seeds 702–705 (job 2, another runner). Among
  seeds 702–705 the spread is ≤ 3 %.
- A6. Put the effective D5 threshold range in the abstract and the C1 bullet.
- A7. Move the checkpoint sensitivity, DAgger regret ranges and the E7 detail to an appendix to fit 9 pages. Fill the
  three citations.

**Score: 4/10 (borderline, leaning reject).** The methodology and transparency are above the norm, and the evidence
audit is clean of fabrication. The primary result is a well-documented negative in a narrow planar simulator, with a
weak RL comparator and one evidential misstatement about cheap planners.

---

## Reviewer B (significance, novelty, positioning)

**Summary.** The paper asks whether amortizing a cost-aware greedy touch planner by distillation keeps the planner's
quality across travel costs, and compares it with RL and heuristics. The answer is "not shown, and probably not
within 1.5 pp", plus a 2,500–9,900× per-decision speed-up.

**Strengths.**
1. It is on topic throughout. No environment or infrastructure issue is presented as a contribution, and E5 and E7
   are labelled methods notes.
2. The negative result is reported honestly, with explicit power statements: "not detected", not "absent", and
   about 7 pp not excluded.
3. Using the same head and action set for DAgger and PPO isolates the training signal, which is the right control.

**Weaknesses.**
1. **The novelty is narrow, as the paper concedes.** Distilling an information-gathering expert via DAgger
   (Choudhury et al. 2017; Nguyen et al. 2024) and amortizing design with RL (Foster et al. 2021; Blau et al. 2022)
   are both established. The contribution is a measurement on a 2D, 3–4-probe, shared-likelihood simulator. With
   horizons this short, the long-horizon credit-assignment argument for distillation is barely exercised.
2. **The practical claim is not demonstrated.** No physical time model exists, so the speed-up is not shown to
   matter for a probing cycle. The reduced planners, which run in 22–194 ms, are already fast enough for many
   robots. Prior evidence (S12, v4) says they lose 5–7 pp against full G\*, about the same as the v4 student. The
   paper omits this, so the reader cannot judge whether the student buys anything over a smaller planner
   (mismatch 1).
3. **The heuristic baselines are weak and noisily chosen.** The pilot choice of H\* is wrong in 4/5 cells on test5.
   B-spread is below Random in 4/5 cells, and no information-based cheap heuristic is included (for example, EIG
   with a handful of particles). "Beats heuristics in 4/5 cells" therefore says little about the frontier of cheap
   policies.
4. **The regime question is unresolved by design.** Five points, one of them a different library that changes K,
   n\* and shape family at once, cannot carry a slope estimate. The CI spans about ±7 pp over the travel range.
5. **The RL comparison is confounded.** One S2-tuned configuration collapses in A16-2, and it under-uses probes
   (about 3 of 4) in every S cell. The only cell where H2-v5 holds is the cell where RL failed, so C3 says almost
   nothing about RL as an approach.

**Actionable revisions.**
- B1. Add the v4 reduced-G\* rows to Table 4 or a side table, and frame C2 against cheap planners as well as
  heuristics.
- B2. Add one cheap information-based heuristic or a reduced-particle G\* on test5 in at least one cell if compute
  allows; otherwise state the omission in the abstract.
- B3. Retitle or reframe toward "a pre-registered negative result on amortizing a greedy touch planner", and move
  C5 out of the contribution list (it is methods notes).
- B4. Give a physical time model, even a parametric one (probe duration T_p, planning in series), so the latency
  result can be read in task terms.

**Score: 3/10 (reject).** It is a rigorous and honest measurement, but its significance for NeurIPS/ICML is limited:
the setting is planar and simulated, horizons are very short, the RL comparator is weak, and the practical
alternative (a smaller planner) is mis-described as unevaluated. It would fit a workshop or a registered-report track
better.

---

## Top factual mismatches (ranked)

1. **Reduced-G\* accuracy described as unmeasured or unknown; v5.1f misparaphrased.** §5.2, §6, §7.7 and deviation
   (b) contradict `results/v4/14_e5_analysis.json` (S12 test3: g125_512_16 −0.0667 [−0.12, −0.01]; g500_512_4
   −0.05 [−0.11, +0.013] vs full G\*). They also contradict `docs/07c_amendment_v5_1.md` addendum v5.1f, which
   designates those rows as the frontier's accuracy side.
2. **RL sweep "validation stream (92,160 episodes)".** `code/analysis_rl_sweep_v5.py` l. 3–4 and 17 show that
   `final_val_episodes` is the training-episode count at the last validation. The stream is 500 episodes
   (`results/v5/rl/*.json` config `val_episodes: 500`).
3. **Limitation 11 and §4 Implementation on provenance.** The paper says the RL episodes per seed and the label and
   DAgger budgets are not in a results field. They are in `results/v5/results_v5.json > 16_report_rows.json`
   (`rl_main_cfg6`, `student_train_episodes`, `student_distill_configs`).
4. **Inversion rule stated as two-directional.** `code/analysis_test5_v5.py` (inversion = RL − student $g_T$ ci95 > 0
   AND student − RL success ci95 > 0) tests one direction only. The outcome (false ×5, plus false in both
   `rl_success` checks) is unaffected.
5. **"Seed" latency spread of about 24 % within a cell.** In `results/v5/14_e6_analysis.json` > `job2`, seeds
   702–705 differ by ≤ 3 % within each cell. The ≈20–25 % differences (S4, S12, A16-2) are between seed 701 (job 1)
   and job 2, which ran on different runners, so they are not seed variation.

Minor items: "about 4 of 5" should be exactly 4/5 with A16-2 passing. Three `[CITE-MISSING]` placeholders remain.
The $g_T$ J/L sizes are not stated. A16's first 8 shapes are the ceiling-level v3 set A, which is unstated.

## Trial-count verdict

The evidence has 300 test5 episodes per method per cell, 500 val3 episodes, 5 student seeds (701–705), 5 RL seeds
(711–715), 5 `rl_success` seeds in S2 and S12, 200 pilot and calibration episodes, 32 E7 beliefs, 200 E5 episodes,
and 1,000 or 500 latency decisions. The paper states these same numbers everywhere they appear. No claimed
statistical test is absent from the code: the crossed bootstrap, Holm, WLS slope and one-sided LB are all
implemented, and the paper claims no ANOVA or t-test.

CRITICAL_FABRICATION: no
