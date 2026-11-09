<!-- Stage 18 PEER_REVIEW [v5] run 2, run 41, 2026-11-09; fresh-context subagent; template peer_review.md verbatim; RSS/CoRL pair -->

# Stage 18 review (v5, run 2): two demanding RSS / CoRL reviewers

**Paper:** Amortizing a Cost-Aware Information-Gain Touch Planner under Travel Cost: A Pre-Registered Five-Cell
Characterisation

**Reviewer A** (significance and positioning for the robotics community): **4/10**, borderline, leaning reject.
**Reviewer B** (methodology–evidence consistency): **5/10**, borderline.

**CRITICAL_FABRICATION: no.** (The machine-readable line is at the end of this file.) I checked every trial count,
episode count, seed set, statistical test and hyperparameter I could trace, and none contradicts the code or the result
files. I recomputed the test5 G\* means, the E5 sub-8 baselines and the duplicate-episode status from the raw
`results/v5/test5/*.jsonl` files, and I re-hashed all 60 frozen weight files. Everything matched. The mismatches I found
are interpretive or concern wording and disclosure (Section 0.2). One of them is substantive: the paper attributes E7 to
G\*'s value estimates, but E7 does not measure those.

---

## 0. Verification log (shared by both reviewers)

### 0.1 Spot-checks (38): claim, then evidence file, then verdict

| # | Claim (paper location) | Evidence | Verdict |
|---|---|---|---|
| 1 | test5 has 300 episodes per method and cell, and every block is complete, g_T included (§4, Table S) | `results/v5/14_test5_analysis.json` `<cell>.episodes_per_method` (all 300), `gt_episodes_per_method` (all 300), `complete`/`gt_complete` true | match |
| 2 | No duplicate or cherry-picked re-run episodes in test5 | recomputed over all 2,560 files in `results/v5/test5/` (including `_rN`/`_cN` follow-up shards): 0 duplicate (method, episode) keys | match |
| 3 | G\* test5 success S2 0.5333, S4 0.4967, S8 0.4567, S12 0.4567, A16-2 0.49 (Table 2a) | recomputed from the raw `results/v5/test5/*_gstar_*.jsonl`; `14_test5_analysis.json <cell>.means.gstar.success` | match |
| 4 | Student and RL 5-seed means (Table 2a, PH) | `results/v5/15_posthoc_derived.json` `student_success_mean_*`, `rl_success_mean_from_diff`; per-seed means in `14_test5_analysis.json` | match |
| 5 | Student − G\* success diff, ci95 and p in all 5 cells; Holm 0/5 (Table 2b) | `14_test5_analysis.json <cell>.student_minus_gstar.success` | match |
| 6 | Student − H\* success in 5 cells; Holm 4/5, with S2 p 0.0558 (Table 2b) | `...student_minus_hstar.success`; Holm recomputed from p = [0.0558, 0, 0.0098, 0.0178, 0] gives 4 rejections | match |
| 7 | Bootstrap p resolves to 0.0002; p = 0 is printed as < 0.0002 (§4) | `code/analysis_test5_v5.py` `two_sided()`: p = 2·min(p_greater, p_less) with N_BOOT 10,000 | match |
| 8 | Crossed episode × seed bootstrap with n_seeds [5,1] vs G\*/H\* and [5,5] vs RL; 10,000 resamples (§4) | `code/touchbed/stats.py` `crossed_bootstrap_diff`; `n_seeds` fields in the JSON | match |
| 9 | Holm over 5 cells applies to only two families (§4) | `code/analysis_test5_v5.py` `main()` loops over `student_minus_gstar` and `student_minus_hstar` only | match |
| 10 | D5 threshold max(−0.02, −δ + 1.163 SE); S2 example −0.01454 (§4) | `code/analysis_d5_v5.py` uses 1.645·SE·√0.5 = 1.163·SE; `12_d5_analysis.json S2.succ.threshold` −0.014538 | match |
| 11 | D5 Δ̂_succ, thresholds, Δ̂_BI and seeds-ok counts (3/5, 1/5, 4/5, 3/5, 0/5); m = 0 (Table 1) | `results/v5/12_d5_analysis.json` | match |
| 12 | All 25 per-seed validation diffs are negative, ranging from −0.068 to −0.01 (§5.1) | `12_d5_analysis.json <cell>.succ.per_seed` | match |
| 13 | The G\* validation sources are v4 (S2), v3 (S12) and v5 (others), with the same 64×8 action set and sub 8 | `12_d5_analysis.json gstar_source`; headers of `results/v3/d3_val/S_k12_gstar_000.jsonl`, `results/v4/d4_val/S_k2_gstar_000.jsonl` and `results/v5/d5_val/S_k4_gstar_000.jsonl` (all `64x8`, `sub 8`, `val3`) | match |
| 14 | τ and n\* per cell, including S4 0.7967 → 4.8, S8 0.8335 → 4.8 and A16 0.3514 → 3.4 (Table 0) | `results/v5/12_cal_analysis.json tau`; `docs/07c_amendment_v5_1.md` cell table | match |
| 15 | The S2 (0.7257, τ 4.7) and S12 (0.9388, τ 4.9) rows come from the earlier rounds | `results/v3/results_v3.json 12_cal_analysis.tau.S_k2_nstar4 / S_k12_nstar4` | match |
| 16 | A16 n\* = 3 (rule reading 0.975) and keep check 0.8 ∈ [0.30, 0.90] | `12_cal_analysis.json n_star.A16`, `keep.A16`; amendment v5.1 | match |
| 17 | H\* per cell and pilot success (B-cov 0.445, B-fan 0.43, B-cov 0.405, B-fan 0.41, B-fan 0.33), 200 episodes each, tie rule | `results/v5/12_base_hstar.json` | match |
| 18 | H\* is not the best test5 heuristic in 4/5 cells; post-hoc margins +3.5 to +14.5 pp | `15_posthoc_derived.json best_test5_heuristic`, `margin_student_minus_best_test5_heuristic` | match (but in S2 the margin does not "fall"; it is equal) |
| 19 | H5b slope −0.0157/rad with ci95 [−0.104, 0.073]; per-100° values; verdict "no trend detected" | `14_test5_analysis.json H5b` | match |
| 20 | "About 7 pp not excluded": span translation −0.07393 to +0.05167 | `15_posthoc_derived.json H5b_span_translation` | match |
| 21 | H2-v5 lower bounds −0.4971, −0.6555, −0.4861, −0.3044, +0.5964; met only in A16-2 | `14_test5_analysis.json <cell>.H2_v5.student_minus_rl_gT.lower_one_sided_95`, `claim_student_higher_on_rl_objective` | match |
| 22 | Table 3 g_T means and the three contrasts per cell, including G\* − RL = +0.8541 in A16-2 | `...H2_v5.means_gT`, `rl_minus_student_gT`, `gstar_minus_rl_gT`, `gstar_minus_student_gT` | match |
| 23 | Inversion is false in 5/5 cells and in both `rl_success` checks | `...H2_v5.inversion`, `check_rlsucc.inversion` | match (rule wording: see M4) |
| 24 | The `rl_success` per-seed training lengths and "9 of 10 ended before the cap" | `results/v5/16_report_rows.json rl_success` (`EARLY_STOP_AT_80_PCT_BUDGET` × 9, one `max_episodes`) | match (cause not stated: see M6) |
| 25 | cfg-6 RL ran 200,192 episodes in every run, with clip 0.2, 4 epochs and width 128 | `16_report_rows.json rl_main_cfg6` (25 runs) | match |
| 26 | RL sweep: 8 configs, 100,096 episodes (100,032 at batch 64), cfg 6 6.300 vs cfg 0 6.241; on the sampled metric cfg 1 6.316 vs cfg 6 6.205 | `results/v5/12_rl_sweep_selection.json` | match (the sweep used a single seed, 719, which the paper does not state; see `experiments/v5_rl_sweep_S2.json`) |
| 27 | Student hp 0: Adam, lr 0.001, batch 256, width 128, β_T 4.0, λ 0.5, 200 epochs, in all 75 runs | `16_report_rows.json student_distill_configs` (one config × 75) | match |
| 28 | Training episodes 2,700 / 3,500 / 4,300 (r0 / r1 / r2) | `16_report_rows.json student_train_episodes` | match |
| 29 | DAgger β 0.5 in r1 and 0 in r2, 800 episodes | `experiments/v5_dag_r1_S2_S12.json` (`--beta 0.5`), `experiments/v5_dag2_S2_S12.json` (`--beta 0`) | match |
| 30 | Regret floor ρ = 0.05; soft target with β_T s/σ_s; loss with a hard λ term | `code/touchbed/distill.py` l. 6–23, 57–69 | match |
| 31 | Kept R̄ ranges per cell, held-out decision counts, last-minus-kept range 0.0002753–0.03172, kept epochs 0–187 | recomputed from `16_report_rows.json student_checkpoint_sensitivity` | match |
| 32 | Action grid of 64 angles × 8 offsets from −35° to +35° (512 actions); probe radius 100 mm | `code/touchbed/travel.py` l. 16–21; `code/touchbed/geometry.py` l. 12 (`RHO = 100.0`) | match |
| 33 | Belief-free DeepSets head in the finger frame, with context (relative angle, τ_rem/τ, φ_t) | `code/touchbed/distill.py` `Student` (`needs_belief = False`); `code/touchbed/relframe.py` docstring and `rel_ctx` | match |
| 34 | Heuristic definitions for B-spread, B-fan and B-cov, plus budget reservation | `code/touchbed/heuristics.py` | match |
| 35 | Weight hashes recorded before test5: 15 per cell in S2/S12 and 10 in the others | `results/v5/13_freeze.json`; re-hashed all 60 `.npz` files, 60/60 identical; the test5 headers point at the frozen files (e.g. `S_k4_s705_r2.npz`) | match (the ordering itself rests on the `PROGRESS.md` log, because the repository history is squashed) |
| 36 | E5 flip rates, gains and losses, sub-8 and sub-16 success, mean \|ΔBI\| ≤ 0.004034, and contrast shifts of +0.02 and −0.03 | `results/v5/14_e5_analysis.json`; sub-8 values recomputed from raw test5 episodes 0–199 (G\* 0.54 / 0.48, student 701 0.465 / 0.455) | match |
| 37 | E6 medians, ratios, CIs, CI rule met only in A16-2, 1,000 vs 500 decisions, job-2 ranges, student medians 0.36–0.51 ms and "up to about 24 %" | `results/v5/14_e6_analysis.json`; `15_posthoc_derived.json latency`; A16-2 0.4069 / 0.3261 = 1.247 | match |
| 38 | E7 numbers (paired gap +0.04838 and +0.01830, selection bias values, mean candidates 29/302 and 30.5/85.75) | `results/v5/12_e7_analysis.json` | numbers match; **interpretation does not** (M1) |

Prior-round numbers also match. The S2 gate is −0.028 against a threshold of −0.01464, and the S2 test3 result is −10.2 pp
with ci95 [−16.6, −4.3] (`results/v4/results_v4.json 12_d4_analysis.json`, `14_s2_analysis.json`). The S12 gate is −0.05867
against −0.01435, and −0.044 against −0.01681 after the remedy (`results/v3/results_v3.json 12_d3_analysis`, `12_d3_analysis_rem`).
Table 5 travel and probe ranges, the A16-2 RL collapse to 2.0 probes in seeds 712–715, and the `rl_success` per-seed
success ranges all match `14_test5_analysis.json <cell>.means`. The Figure 1 panel D values match the JSON paths they cite.

### 0.2 Mismatches and disclosure gaps (none is fabricated evidence)

**M1. E7 is attributed to G\*'s value estimates, but it measures a look-ahead screen (substantive).** C5 says "an upward
selection bias in G\*'s value estimates", and §5.1 says "E7 shows noisy, upward-biased value estimates in S2" to argue
that the student − G\* CIs are too narrow. E7 does not estimate that. In `code/analysis_e7_v5.py` (docstring l. 1–7) and
`code/touchbed/lookahead.py` (l. 1–14), E7 screens C1 first actions with a rollout look-ahead that is completed by a
greedy comparator. It then measures the bias of **V_LA = max over screened candidates** (selected minus independent
estimate). The look-ahead PF uses `n_la = 500` particles (`code/touchbed/g2.py` l. 48–60), not the deployed
`g2000_512_64`. The quantity the paper calls the "independent-estimate gap" is `indep_gap_nats` = independent V_LA − V_G\*,
which is the **one-step look-ahead headroom over G\***. At C1 = 512 it is +0.0658 nats (ci95 [0.0297, 0.1084]) in S2 and
+0.0422 (ci95 [0.0250, 0.0614]) in S12, both excluding 0 (`12_e7_analysis.json`). The paper never says this in words.
So E7 does show that G\* is beatable in nats in both cells, but it does not show that G\*'s own EIG/c scores are biased.
The §5.1 inference and the C5 wording should be corrected. The real headroom result should be stated, because it bears
on "G\* is a reference, not an optimum".

**M2. "The D5 rule applied to test5 would still fail in about 4 of 5 cells" is never computed, and it hides which cell
passes.** I ran `code/analysis_d4_v4.boot_sd` with the D5 formula on the raw test5 records. S2, S4, S8 and S12 fail
clause (i): −0.0247 vs −0.0095, −0.0253 vs −0.0056, −0.0127 vs −0.0106 and −0.0153 vs −0.0116. **A16-2 passes all three
clauses:** Δ̂ −0.0020 ≥ −0.0040, BI +0.085 ≥ −0.15, and 5/5 seeds > −δ. The statement appears only as "about 4/5" in
`results/v5/15_decision.md` l. 129/313 and `14_analysis.md` l. 240, and no results file contains it. The paper should
give the exact count, name A16-2, and keep it labelled post hoc. A16-2 is the second-library cell, so this matters for
the "every cell tested" framing.

**M3. The H5b weights are described as "fixed before test5" (§5.4) and "fixed in advance" (§4).** What was fixed in
advance (addendum v5.1f, before any test5 number was read) is the *rule*: inverse bootstrap variance of each cell's
Δ_succ. The *values* (1469.5, 1144.1, 1593.9, 1643.4, 1047.6; `14_test5_analysis.json H5b.weights`) are computed from
test5 bootstrap replicates (`code/analysis_test5_v5.py` `h5b()`: `w = 1/reps[:,:,0].var`). This is legitimate, but it
should say "weight rule fixed in advance; weights estimated from test5".

**M4. The inversion rule is paraphrased loosely.** §4 says "opposite directions with a resolved g_T contrast". Both
the pre-registration (`docs/07c_amendment_v5_0.md`, H2-v5: "both orderings have intervals excluding 0") and the code
(`analysis_test5_v5.py`: `inv_g.ci95[0] > 0 and inv_s.ci95[0] > 0`) require the success contrast to be resolved too. The
outcome does not change, but the rule as printed is not the rule that was run.

**M5. Pre-registered deliverables were dropped without a line in the protocol.** Amendment v5.0 E6 promised a
"latency–accuracy frontier figure", and v5.1f kept the frontier "read within that job". E5 promised that "every success
contrast is reported next to the measured flip rate". The paper honestly says that no frontier is supported, and it
gives a generic E5 caveat. It should state explicitly that these were pre-registered and not delivered, and why: no
reduced-G\* accuracy on test5, and no per-contrast flip rate.

**M6. Small disclosure and wording items.**
(a) The `rl_success` runs stopped at the trainer's **wall-clock time guard** (80 % of 330 min; addendum v5.1c,
`16_report_rows.json` status `EARLY_STOP_AT_80_PCT_BUDGET`), and the paper says only "ended before the episode cap".
(b) The RL sweep used one seed (719), which is not stated.
(c) Table S says "the remaining design constants are marked" and Limitation 11 says they "are marked in the text", but
no markers appear.
(d) Three `[CITE-MISSING]` placeholders remain: DeepSets, Holm and the bootstrap.
(e) A16 is never described beyond "K = 16". In `code/touchbed/shapes.py` (`make_set_A`) it is a family of 16
*asymmetric irregular* polygons with 8–14 vertices, unlike S, which has near-symmetric shapes plus notched variants. The
second cell therefore changes shape family, K and n\* at the same time.
(f) "Against the best test5 heuristic the post-hoc margin falls": in S2 it does not fall, because H\* is the best.

---

## 1. On topic?

Yes. Every section concerns the amortization of G\*, the RL comparison, the heuristics, and the travel-cost
characterisation over the five pre-registered cells. Infrastructure appears only in §4 Implementation and the
Limitations: runners, CPU model not logged, time guards, the test5 reduction. None of it is presented as a
contribution. C5 ("methods notes") is a list of measurement caveats, and the paper explicitly places it outside the
results. That is acceptable, although listing it as a contribution inflates the contribution count.

## 2. Methodology–evidence consistency

The paper is unusually well aligned with its evidence. Every table cell I checked traces to a named JSON field. The
statistical procedures described exist in code: a crossed bootstrap, Holm, WLS with a bootstrap CI, a one-sided LB, and
the D5 gate. No test is claimed that is not implemented: `tost` exists in `stats.py` and is correctly reported as not
used. The discrepancies are M1–M6. M1 is the only one that changes a scientific statement.

## 3. Trial count

The trial counts in the paper match the files: test5 has 300 episodes per method and cell, five student seeds
(701–705) and five RL seeds (711–715); val3 has 500; pilot3 has 200 per heuristic; cal3 has 200; E5 covers 200 episodes
× 2 cells × 2 methods; E7 uses 32 beliefs × 2 cells × 2 settings; E6 times 1,000 or 500 decisions in job 1 and 500 per
seed in job 2; RL runs 200,192 episodes per run; the sweep runs 100,096 or 100,032. The reduction from 500 to 300 is
documented before any test5 episode (addendum v5.1e) and is disclosed. **No trial-count fabrication.**

## 4. Length

Word counts are approximate and include tables. Abstract 263, Introduction 915, Related Work 677, Method 1,721,
Experiments 1,622, Results 2,237, Discussion 527, Limitations 341, Conclusion 199. The total is about 8,500. No section
is under its threshold. For RSS or CoRL (8 pages plus references), the paper is if anything **over-length and
over-dense**: Tables 1, 2b, 3 and 4 have 10–11 columns of 4-significant-figure numbers, which will not survive a
two-column layout.

---

## Reviewer A: significance and positioning for the robotics community (RSS / CoRL)

**Summary.** The paper asks whether a cheap DeepSets policy distilled by DAgger from a cost-aware greedy EIG touch
planner (G\*) can match it, across four travel costs on one planar shape library and one cell on a second library. It
also compares the student with PPO on a contrastive objective and with three hand-designed heuristics. The main result
is negative and is stated as such: the pre-registered gate fails in 5/5 cells. The student beats the pilot-chosen
heuristic in 4/5 cells and is 2,500–9,900× faster per decision.

**Strengths.**
1. Exemplary scientific hygiene for robot learning. The protocol is pre-registered with dated addenda. A fresh test
   split is evaluated once after a hash-verified freeze; I re-hashed all 60 files and they match. The design is paired,
   the multiplicity families are declared in advance, and post-hoc numbers are clearly labelled. A negative result is
   reported as a negative result. RSS and CoRL rarely see this, and the community benefits from it.
2. The framing of the question is sound. Planner distillation and RL use the same head, the same action set and the
   same objective, and both are scored on RL's own metric as well as on a posterior read-out. That is the right control
   to separate the training signal from the architecture.
3. Limitations are candid and specific: G\* is run once, evaluator resolution is limited, one RL configuration is used,
   heuristic selection is noisy, and the latency runners vary.

**Weaknesses.**
1. **The practical motivation is not quantified, so significance for robotics is unclear.** The case for amortization
   is that G\* is "slow", at 0.9–4.9 s per decision. But an episode has n\* = 3–4 probes, so G\* costs about 4–20 s
   per episode, and a real tactile probe (approach, contact, retract) also takes on the order of seconds. The paper
   never states a physical time model in which planning time competes with the probe budget. Without one, a speed-up
   of 2,500–9,900× does not translate into any task benefit. Worse, the two reduced G\* configurations
   (`g125_512_16` at 22–116 ms and `g500_512_4` at 48–194 ms; Table 4) are already fast enough for most robots. They
   are the obvious engineering baseline, yet their accuracy was never measured on test5 (M5). A roboticist would ask
   first whether a 20× cheaper G\* loses anything, and the paper cannot answer.
2. **The setting is too small to say much about amortization.** The horizon is 3–4 decisions. The motivation that
   "dense per-action scores remove long-horizon credit assignment" (§1) hardly applies at T ≤ 4. The task is planar,
   with a fixed stand-off circle, Gaussian contact and normal noise, and a model-matched likelihood (planner, filter and
   evaluator share p_ε). It has no contact dynamics, no object motion and no sim-to-real component. Absolute success
   for G\* is only 0.45–0.53. The paper says it uses this setting "to isolate the selection question". That is fair,
   but then the contribution is a characterisation of one simulator, and the generality claimed in the title ("across
   travel costs") rests on five points, one of which changes the shape family (M6e).
3. **The "second library" changes three things at once.** A16 is a family of asymmetric irregular polygons with
   K = 16 and n\* = 3, at κ = 2 only. It therefore confounds library type, K and probe count. It is also the cell where
   RL collapses and where test5 would pass the D5 rule (M2). Conclusions about generality across libraries cannot be
   drawn from it.
4. **The comparators are weak or under-tuned.** B-spread scores below Random in S2, S8, S12 and A16-2 (Table 2a),
   which suggests a degenerate baseline (fixed ψ = +5°, maximum angular spread) rather than a credible heuristic. B-cov
   uses only the MAP particle. RL is tuned once, in S2, with a single seed (719), and collapses in A16-2. "The student
   beats heuristics" is then a modest statement, and the student − RL comparison is, as the authors say, about this RL
   setup only. No belief-input student, capacity ablation or student-visited-state regret is reported in v5, so the
   paper cannot say *why* the student falls short. The paper raises this only as an open question.
5. **The novelty is thin as positioned.** DAgger distillation of an information-gathering expert (Choudhury 2017,
   Nguyen 2024) and RL-based amortized design (Foster 2021, Blau 2022) are both established. The claimed gap is a
   pre-registered, multi-cell head-to-head. That is a methodological contribution, and it is valuable, but it is a
   better fit for a workshop, a reproducibility track or a journal "negative results" format than for the RSS or CoRL
   main track, where reviewers expect either a new capability or a hardware demonstration.
6. **Presentation.** The paper is dense with gate jargon (D5, H5a, H5b, H2-v5, test5, val3, pilot3, cal3, sub 8, DEC,
   GATE, PH, EXPL). A robotics reader has to decode the provenance tags before reaching the findings. Tables 1–4 are not
   printable at RSS width.

**Actionable revisions.**
- A1. Add a physical time model, for example probe duration t_p and planning in series or in parallel, and report
  the success of G\*, the reduced G\* configurations and the student at equal *wall-clock* budgets. At minimum, run
  `g125_512_16` and `g500_512_4` on test5 in two cells so that a latency–accuracy frontier exists, as pre-registered.
- A2. Either describe A16 fully and explain that it changes the family, or add an S16 or A8 cell so that library and K
  are not confounded.
- A3. Replace or justify B-spread. Add one information-based cheap heuristic, for example single-sample EIG or
  EIG with M = 1.
- A4. Report one diagnostic of the shortfall: regret on student-visited states, a width or capacity sweep, or a
  belief-input student. One cell is enough.
- A5. Move gate tags and provenance to the appendix. Lead each results subsection with one plain-language sentence.
- A6. Reconsider the venue: a workshop or reproducibility track, or a journal short paper, unless A1 and a hardware
  check are added.

**Questions.** What is the physical time per probe on a representative platform? Does `g125_512_16` lose success
relative to `g2000_512_64`? Why was κ varied only on S, and not on A16?

**Score: 4/10 (borderline, leaning reject).** The paper is rigorous and honest, but its significance for robotics is
not established. It reports a negative result in a small planar simulator, without the cheap-planner baseline that
would show whether amortization is needed at all.

---

## Reviewer B: methodology–evidence consistency

**Summary.** I audited the paper against `results/v5/results_v5.json`, the underlying `results/v5/*` files, the v3/v4
prior files, the analysis code and amendments v5.0/v5.1. The 38 spot-checks are in Section 0.1.

**Strengths.**
1. Numerical fidelity is very high. Every number in the abstract, Tables 0–5 and Figure 1D that I traced matches the
   JSON or the raw episodes. I independently recomputed the G\* test5 means, the E5 sub-8 baselines, the duplicate
   status of every test5 shard and the freeze hashes.
2. The statistics are implemented as described: a paired crossed bootstrap, Holm on exactly two declared families, a
   one-sided LB for H2-v5, and WLS with bootstrap replicates for H5b. The D5 gate is implemented with the
   pre-registered constant 1.645·√0.5. Analysis code was written before test5 was read (`analysis_test5_v5.py`
   docstring; PROGRESS run-35 entry), and the test5 reduction follows the frozen reduction order.
3. The verdicts are worded conservatively: "not supported", "no trend detected", "not excluded" and "uncorrected".
   Equivalence is correctly not claimed, because the CIs are 9.6–12.3 pp wide against δ = 4 pp.

**Weaknesses.**
1. **M1 (substantive).** E7 is misattributed. It measures the max-selection bias of a 500-particle rollout
   look-ahead screen and the look-ahead's headroom over G\*. It does not measure bias in G\*'s EIG/c estimates.
   The §5.1 argument that "E7 shows noisy, upward-biased value estimates" of G\*, so the student − G\* CIs "may be too
   narrow", therefore lacks support from E7. The real result, that the look-ahead headroom over G\* excludes 0 in both
   cells, is not stated. It weakens G\* as a reference and should be reported.
2. **M2.** The "about 4 of 5" claim about test5 is uncomputed and incomplete. The exact figure is 4/5, and the passing
   cell is A16-2. The paper's repeated line "the student is below G\* in every cell on both splits" is true as a sign
   statement (−0.002 in A16-2). Readers should still be told that, on test5, the gate rule itself would pass there.
3. **The G\* side of every student − G\* contrast has n_seeds = 1**, and the validation rows of G\* come from three code
   rounds. Both points are acknowledged. Together they mean that the validation gaps (3.2–6.0 pp) and the test5 gaps
   (0.2–2.5 pp) are not comparable as "the same story at different magnitudes" (§6) without a G\* rerun. The gap
   between the splits (1–6 pp) is about the size of the E5 resolution effect (0.8–2× the test5 gap), so the cleanest
   reading is "undetermined within ±8 pp". The abstract and conclusion lean harder on "below G\* in every cell" than the
   intervals justify.
4. **The D5 design is strict in an unusual way, and the paper should say so plainly.** The threshold
   −δ + 1.163·SE is a non-inferiority bound at about 88 % one-sided confidence. With SE ≈ 0.02, it requires
   Δ̂ ≥ −1.5 pp, much tighter than the nominal 4 pp margin. A reader skimming "within δ = 4 pp" will misread the gate.
   S8 on validation (−3.6 pp, 4/5 seeds OK) fails only clause (i).
5. **M3, M4, M5 and M6** are wording and disclosure items. H5b uses weights estimated from test5, the inversion rule
   is paraphrased loosely, the frontier and per-contrast flip-rate deliverables were dropped, the `rl_success`
   time-guard truncation is not named, the sweep used a single seed, no design-constant markers appear, three
   placeholder citations remain, and A16 is undefined.
6. **The DAgger rounds have no measurable effect on the selection metric.** Across 25 seed × cell runs, the kept R̄
   changes from r0 to r2 by −0.0069 to +0.0052 (`16_report_rows.json`), and several r1/r2 kept epochs are 0–5. Because
   R̄ is measured on G\*-visited held-out decisions, the selection metric cannot register DAgger's intended benefit. The
   student is therefore effectively selected as a behaviour-cloning model. The paper describes the recipe as DAgger
   without noting this. A sentence and a pointer to the open question about student-visited regret are needed.

**Actionable revisions.**
- B1. Rewrite the E7 paragraph, C5 and §5.1 (M1): "a one-step look-ahead screen over G\* shows positive headroom in
  nats (S2 +0.066, S12 +0.042 at C1 = 512, CIs exclude 0) and an upward max-selection bias in the screen (S2 only)". Drop
  the claim that E7 shows G\*'s own estimates are biased, or support it with a separate measurement.
- B2. Replace "about 4 of 5" with the exact computation: fail in S2/S4/S8/S12, pass in A16-2. Mark it post hoc, and add
  it to `15_posthoc_derived.json` so that it is citable.
- B3. Correct the H5b weight wording (M3) and print the inversion rule as pre-registered and coded (M4).
- B4. Add a "deviations from pre-registration" paragraph: the dropped frontier figure and the per-contrast flip rates,
  E6 moved to runners (v5.1f), the test5 reduction (v5.1e), and `rl_success` truncated by the time guard (v5.1c).
- B5. State the effective D5 margin (about −1.5 pp at the observed SE) next to "δ = 4 pp".
- B6. Report the r0 → r2 R̄ change, and add one sentence noting that the selection metric cannot see DAgger's benefit.
- B7. Fill in the three citations, describe A16, and remove or apply the "marked constants" promise.

**Score: 5/10 (borderline).** The paper is internally honest and numerically faithful, and it has no fabrication. One
interpretive error (E7) and one under-specified post-hoc claim (test5 D5) must be fixed. The evidence supports a
careful negative characterisation, not more.

---

## Consolidated must-fix list (before stage 19)

1. M1: correct the E7 attribution in C5, §4, §5.1 and Limitation 2, and state the look-ahead headroom result.
2. M2: give the exact test5 D5 re-application (A16-2 passes) and record it in a results file.
3. M3 and M4: correct the H5b weight wording and the inversion rule wording.
4. M5 and M6: add a deviations paragraph; resolve the `[CITE-MISSING]` placeholders, the missing constant markers and
   the A16 description; disclose the sweep seed and the `rl_success` time guard.
5. Reviewer A A1, if the venue stays RSS or CoRL: measure the accuracy of the reduced G\* configurations on test5 in at
   least two cells.

CRITICAL_FABRICATION: no
