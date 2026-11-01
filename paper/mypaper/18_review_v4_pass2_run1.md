# Stage 18 review (v4, pass 2, run 1)

Paper: "Cost-Aware Information-Gain Touch Selection under Travel Cost: Look-Ahead Headroom and Learnability in a
Stay-and-Probe and a Travelling Regime"

**CRITICAL_FABRICATION: no.**

Reasons:
- Every trial count in the draft matches the evidence. That covers D3/D4 on 500 val3 episodes × 3 student seeds;
  test3 success/BI rows on 300 episodes; g_T on 500; H3 on 100 beliefs per κ plus a 20-belief bias check; E′ on 16
  episodes; Cal′ on 200 calibration episodes; PPO at 200,064 episodes per seed with 3 seeds per cell; and the
  PPO sweep (4 configurations × 50,048 episodes).
- The statistics the paper describes (crossed episode × seed bootstrap with B = 10,000, one-sided 5/95 % bounds for H2,
  2.5/97.5 % for ci95, the D-gate SE as a bootstrap SD with the √0.5 factor) are implemented exactly as described in
  `code/touchbed/stats.py` and `code/analysis_d4_v4.py`. Holm and TOST exist in the code, and the paper correctly says
  that neither was executed.
- I recomputed these from the raw logs, and all of them reproduce:
  - S2 test3 sub-8 success/BI rows for G\*, the three students, the three RL seeds and B-fan;
  - the S2 H2 crossed bootstrap (Δ = −0.4452, LB −0.7485, UB −0.1616, p_less 0.0064);
  - D4 val3 means and per-seed deficits (−3.6 / −2.8 / −2.0 pp);
  - the S2 Cal′ verification (3.875 probes on 200 episodes);
  - S2 G\* logged travel (46.91°) and probes (3.873).
- The derived and post-hoc quantities are labelled as such: the post-hoc sensitivity of the D gates and of H2, the
  "BI first" reading rule, the after-the-fact S2 Cal′ verification, "26 % (derived)", the "ratio derived", the
  "49× / 98× (derived)" and the "bootstrap p not pre-registered". The few unlabelled ones are listed under Mismatches and
  are minor.
- The one real overreach is in wording, not in numbers. The abstract, discussion and conclusion state the g_T-versus-grid
  ordering inversion more strongly than the S12 evidence supports (see M1).

---

## Methodology-evidence mismatches found

| # | Location | Claim | Evidence | Severity |
|---|---|---|---|---|
| M1 | Abstract ("which ranks G\* below both learners, unlike the grid posterior"); §6 "$g_T$ as a yardstick" ("ranks G\* below both learners in both cells, whereas the grid posterior ranks it above"); §8 | The ordering inversion holds in both cells | S12: g_T(G\*) = 5.299 vs 5.368 for both learners (Δ ≈ 0.069). 3 of 6 S12 learner seeds lie *below* G\* (student s501 5.279; RL s512 5.271, s513 5.178), and no interval exists. On the grid side, S12 student − G\* BI = −0.049 with ci95 [−0.114, +0.019], which includes 0. In S12 the "inversion" is therefore two non-significant point-estimate orderings. §5.4 itself calls the S12 g_T ordering "marginal", but the abstract and discussion drop that qualifier. Only S2 supports it (every S2 learner seed is above 5.397, and the G\*−student BI ci95 excludes 0). | Moderate (overclaim of the headline "most transferable" finding) |
| M2 | §1 "Two regimes": "79.3 % of the planner's between-probe moves are zero, and the finger moves on average 4.3° per episode between probes (test3 episodes 0–299)" | 79.3 % is on test3 0–299 | 79.3 % comes from `14_behaviour` on test3 0–**499**. Recomputed on 0–299 it is 80.9 %. 4.3° is on 0–299. The two figures come from different episode ranges but carry one range label. Table 4's caption gets this right. | Minor |
| M3 | §5.3 (S2 D4): "the difference is ≈ 2.0 combined SE under independence" | Presented as a fact | This is derived (val SE 0.0218, test SE ≈ 0.031 back-computed from the ci95 width, 0.074 / 0.038 ≈ 1.95). Unlike the other post-hoc figures it is not labelled "derived, post hoc". The arithmetic is correct. | Minor (labelling) |
| M4 | §4 "Reading rule: BI first" (7.5 pp) | The rule is conservative and "changes no gate verdict" | It is labelled as fixed in this revision and not pre-registered, which is correct. The concerns: (a) a 7.5 % per-episode flip rate between sub-4 and sub-8 is a discordance rate, not a bound on the error of a paired contrast between methods scored by the same evaluator. (b) The threshold sits just below the one success contrast it lets through as "just above resolution" (S2 student − B-fan +8.1 pp). (c) It is applied unevenly: S12 G\* − RL success +7.0 pp (ci95 [+0.2, +13.7]) is below 7.5 but is reported in §5.4 without the "within resolution" tag that the student contrasts get. | Moderate (post-hoc rule, labelled, but its threshold is close to a key reported contrast) |
| M5 | §4 end, Table 5, §7 "[PENDING:v4:14_s2_analysis.test3_sub8.rows.random]" | S2 random anchor incomplete | Confirmed: `results_v4.json` has random n = 215. On disk, `results/v4/test3_sub8` now holds 291/300 random episodes (success 0.120, BI 3.656), newer than the JSON. The placeholders must be resolved before submission, and Figure 1 is also still a placeholder. | Minor (unfinished manuscript; nothing wrong in the numbers) |
| M6 | §1 Findings: E5 "trail the distilled student on ball information by 0.16–0.23 nats"; §5.6 "both are lower on BI by 0.16–0.27 nats" | Two ranges for the same contrast | Both are correct. The first covers the remedied student only (0.162, 0.231). The second also covers the long student (0.203, 0.271). The scope should be stated in §1. | Cosmetic |
| M7 | §5.2: Random has "most of its travel in its first leg" | Applies to both cells | S12: first leg 31.0° of 39.0° (true). S2: first leg 89.8° of 172.2° (52 %), only barely "most". | Cosmetic |

No other mismatch was found. I checked every number in Tables 2–6 and every in-text number in §§1, 3.1, 3.4, 4 and
5.1–5.6 against `results_v3.json` and `results_v4.json`. I also checked these by hand and found them correct:
- D-gate thresholds −1.43 / −1.68 / −0.75 / −1.46 pp;
- the sensitivity figures (+0.4 pp, 0.0 pp, −0.12 nats; 0.41 / 0.57 nats; 0.40 / 0.56 nats);
- the per-seed val→test widening (5.4 / 11.2 / 5.7 pp);
- G\* +3.9 pp and student −3.5 pp;
- the LB 0.85 nats below threshold (≈ 2.8 half-widths);
- logged travel ratios 2.9× and ≈ 4×;
- 2,238× full/student, 3.22× full/pruned-16, and the pruning ceiling (6.2–6.7×) below 10×;
- the S2 training decision counts and held-out R̄ ranges;
- label-fit ranges;
- RL entropy 0.002–0.013, cap-saturation fractions and the SD ratio of 3.29×.

Code checks: the hyperparameters in Table 1 match `touchbed/distill.py` (lr 1e-3, β_T 4, λ 0.5, batch 256 → ⌊256/T⌋ episodes) and
`touchbed/train_v2.py` (clip 0.2, 4 epochs, L = 4095, J = 16). The H3 κ = 2 rows were run with τ = 4.7 and C1 = 32
(`results/v3/g2/S_k2_*.jsonl` headers). The S12 stopping rule is on held-out R̄ (stop_tol 0.005, patience 3), as stated.

---

## Reviewer A (methodology and evidence)

**Summary.** The paper studies cost-aware greedy information-gain touch selection (G\*) on a planar, simulated
identity × pose localization task, in two cells that differ only in travel price (κ = 12 and κ = 2). It makes three
measurements:
1. One-step look-ahead headroom over G\* (H3: small, UB 2.2 %).
2. Whether a DAgger-distilled belief-free DeepSets student reaches G\*. It fails the non-inferiority gate in both cells.
3. Whether distillation beats PPO on PPO's contrastive objective. No advantage is detected, and the paper reports that
   this objective orders policies differently from the grid posterior.

The study is pre-registered, with an explicit outcome map, amendments and a record of descoped analyses.

**Strengths.**
1. *Unusually high methodology-evidence fidelity.* Every number I checked reproduces from the results files, and the key S2
   numbers reproduce from the raw logs (see the mismatch section). Trial counts, seeds, bootstrap scheme and gate formulas match
   the code exactly.
2. *Honest pre-registration bookkeeping.* Failed gates (D3 twice, D4), withdrawn hypotheses (H1-fb), descoped analyses
   (Holm, TOST, BC rows), deviations (S12 hyperparameters reused in S2, borrowed δ, post-hoc S2 Cal′ verification, RL
   selected on val_v2) and test-split reuse are all disclosed and placed in the right part of the paper.
3. *Instrument checks.* H3 has a known-gap construction checked twice, a zero-gap bank and an on-belief bias check. The
   evaluator gate failed and the consequence is reported. The S2 val/test discrepancy is investigated with a pipeline
   equivalence check (50/50 identical actions and successes, BI difference below 1e-14).
4. *The travel decomposition* (grid snap vs between-probe travel) cleanly fixes an earlier ambiguity. The code
   (`analysis_travel_split_v4.py`) asserts that the legs sum to the logged travel.
5. *Post-hoc power figures* for H2 and the D gates are given and labelled. They show that H2 could only detect advantages
   of about half a nat and that the D gates effectively demand parity. This is useful context that most papers omit.

**Weaknesses.**
1. *The headline "transferable lesson" is overstated (M1).* The g_T vs grid-posterior inversion is solid only in S2. In
   S12, both sides of the inversion are non-significant point estimates, and half the learner seeds sit below G\* on
   g_T. The abstract and §6/§8 say "in both cells" without qualification. With one cell of real support, this is an
   observation, not a lesson.
2. *The post-hoc "BI first" rule (M4)* is defended as conservative, but its 7.5 pp threshold is a per-episode
   discordance rate, not a contrast-level error bound, and it is applied unevenly. Its main effect on the narrative is
   that the S2 student-vs-B-fan success separation (+8.1 pp) clears it by 0.6 pp. That separation is exploratory, on a
   reused test split, and against a heuristic selected on S12. I would not lean on it in the abstract.
3. *The S2 validation/test discrepancy is unresolved.* The per-seed deficit grows by 5–11 pp from val3 to test3. G\*
   rises by 3.9 pp while the student falls by 3.5 pp. The test3 deficit (−10.2 pp, ci excludes 0) is the main evidence
   that S2 learnability fails "clearly", and it is the number least consistent with the gate data. Only 50 episodes and
   two policies were pipeline-checked.
4. *The learners are not shown to be tuned or converged.*
   - In S12 the registered stopping rule ends rounds after 4–16 epochs.
   - In S2, held-out R̄ never improves across DAgger rounds and training R̄ was not logged.
   - RL uses one configuration at the edge of the learning-rate grid, chosen on a different validation stream. All six
     RL policies collapse to exactly 3 probes, which is a degenerate solution of the budgeted contrastive return.
   H2/H2-S2 therefore compare against a weak and possibly mis-specified RL setup, as the authors concede.
5. *The evaluator is not shown converged.* E′ failed, and sub-16 was never checked.
6. *Unfinished items:* the [PENDING] random anchor (the data on disk is now 291/300), the Figure 1 placeholder, and M2/M3
   labelling.

**Actionable revisions.**
1. Rewrite the abstract, §6 and §8 so that the g_T/grid inversion is claimed for S2. Describe S12 as "marginal,
   not resolved (3/6 seeds below G\*; BI ci includes 0)". Add a paired bootstrap interval for g_T(learner) − g_T(G\*) in
   both cells. The data exist (`h2/*.jsonl`) and the analysis is descriptive.
2. Either justify the 7.5 pp rule with a contrast-level estimate (for example, re-score the key contrasts at sub-4 and
   report the change in each paired difference), or drop the rule and report all success contrasts with their CIs.
   Apply it uniformly, including to S12 G\* − RL (+7.0 pp).
3. Label the "≈ 2.0 combined SE" figure as derived/post hoc (M3). Fix the episode-range label for 79.3 % in §1 (M2).
4. Complete the S2 random row (291/300 on disk) or state n explicitly, and remove all [PENDING] tokens and the figure
   placeholder.
5. Extend the pipeline check, or at least report the val3 vs test3 G\* success rates per 100-episode block, so readers
   can judge split-to-split variation.
6. Log training R̄ in S2, or state plainly in §5.3 that S2 under-fitting is as plausible as covariate shift.

**Score: 4/10 (Borderline reject).** The execution and reporting are exemplary for a negative-results
characterisation and contain no fabrication. But the evidence supports less than the abstract claims, the learners
are not shown to be competitive, and the transferable claim rests on one cell.

---

## Reviewer B (significance, novelty, positioning)

**Summary.** This is a pre-registered characterisation paper (row 4 of its own outcome map: no method claim) about
greedy cost-aware touch selection and its amortization in a 2D simulated domain.

**Topic adherence.** The paper stays on topic. Instrument issues (evaluator resolution, the S2 val/test gap, the
pipeline check) are explicitly moved out of the contributions and into methods notes and limitations. The g_T/grid
disagreement is kept inside C3 with a stated reason. Nothing drifts into unrelated material, and no environment problem
is presented as a contribution.

**Length.** About 11,200 words (abstract ≈ 250, intro ≈ 1,230, related work ≈ 760, method ≈ 2,190, experiments ≈ 1,910,
results ≈ 3,070). No section is under the minimum. The risk runs the other way: the draft is well above a 9-page
NeurIPS/ICML body and dense with qualifiers, and will need aggressive compression (move §4 protocol details and Table 2
detail to the appendix).

**Strengths.**
1. The questions are well posed: does greedy leave headroom under travel cost, and can a planner be amortized by
   distillation vs RL with the same head?
2. Adding a travelling regime (S2) after finding that S12 is stay-and-probe is the right scientific move, and it is
   carried out under a written amendment.
3. The g_T-versus-posterior disagreement (at least in S2) is a potentially useful caution for amortized BED work that
   reports sPCE-type bounds as policy quality.
4. Limitations are thorough and honest.

**Weaknesses.**
1. *Limited novelty and significance.*
   - The H3 result (small one-step headroom) is what adaptive-submodularity theory predicts, and the paper says so. It
     is a replication of the authors' own earlier estimate.
   - The learnability results are negative for one specific belief-free head, with no architecture variation, and a
     belief-input control that is itself under-fit.
   - The RL comparator collapses to a degenerate 3-probe policy.
   None of this shows that amortization is hard in general, only that this setup did not reach the planner.
2. *Scope is a toy.* The domain is planar polygons, one shape library, a fixed stand-off circle and Gaussian noise. It
   has no contact dynamics, no 3D and no hardware. The related-work section cites hardware systems that the study does
   not engage with.
3. *One cell per regime.* All regime-dependent statements (B-fan separation, travel behaviour, the g_T inversion) are
   two-point anecdotes, as §7 admits.
4. *The g_T finding is under-analysed.* If this is "the most transferable lesson", it needs a mechanism or at least a
   controlled check, for example g_T under matched probe counts, or with L varied. Here g_T is evaluated on policies
   with different probe counts (RL always 3, others about 4) and different travel. A bound whose value depends on the
   history length and the contrast set may simply reward RL's degenerate behaviour. As written, the claim cannot be
   separated from "RL found a way to inflate the proxy".
5. *Cost comparison* (E5) is exploratory, on a reused test split, with logged rather than protocol latencies, and
   without matched accuracy. The practical conclusion ("a frontier only partly mapped") is correct but slight.

**Actionable revisions.**
1. Recast the paper around the strongest, cleanest result. Either make it a short, rigorous negative-results or
   benchmark paper, or invest in the g_T mechanism: g_T at matched probe counts, g_T(G\*) vs g_T(G\* truncated to 3
   probes), and sensitivity to L.
2. Add at least one more cell per regime (for example, κ = 6, or set A at κ = 2), even descriptively, so that the
   regime claims are not two-point comparisons.
3. Run one probe-count-aware or S2-tuned RL variant. Without it, H2/H2-S2 are statements about one degenerate RL policy.
4. Run a second architecture (an attention head, or a belief-input head trained to fit) before claiming anything about
   learnability.
5. Compress §4 and Table 2 to fit 9 pages, and replace Figure 1's placeholder.

**Would I recommend presentation at NeurIPS/ICML?** Not in its current form. It is a careful and honest study whose
answers are mostly "not shown" in a narrow simulated setting. Its one positive, transferable observation is supported
in only one of two cells, and its mechanism is not examined. It would suit a workshop or a venue for reproducible negative
results.

**Score: 3/10 (Reject).** The rigour and transparency are commendable, but the contribution is incremental, the
scope is narrow, and the headline claim is not yet established.

---

## Scores
- Reviewer A: **4/10**
- Reviewer B: **3/10**
- CRITICAL_FABRICATION: **no**
