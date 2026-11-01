# Stage 18 review, v4 pass 2, run 2

Paper: "Cost-Aware Information-Gain Touch Selection under Travel Cost: Look-Ahead Headroom and Learnability in a
Stay-and-Probe and a Travelling Regime"

Review stance: two strict RSS/CoRL reviewers (A: active perception / tactile localization; B: robot learning,
imitation and RL). Every number in the paper was checked against the evidence in the prompt (results_v4.json and
results_v3.json). Selected numbers were also recomputed from raw files under results/v4 and code/: the S2 test3 sub-8
rows, the H2-S2 crossed bootstrap, the S2 Cal′ probe count, the D4 gate formula, the S2 distillation logs and the H3
κ = 2 configuration.

**CRITICAL_FABRICATION: no.**
Reasons:
- Every trial and episode count in the paper matches the evidence:
  - val3: 500 episodes × 3 seeds (D3, D4).
  - test3 0–299 sub-8: 300 episodes.
  - g_T: test3 0–499, 500 episodes.
  - H3: 100 beliefs per κ, bias check on 20.
  - PPO: 200,064 episodes per seed; sweep 4 × 50,048.
  - Bootstrap: B = 10,000.
  - Lat′: 1,000 decisions on 253 episodes.
  - Calibration: 200 cal3 episodes.
- The statistics claimed (crossed episode × seed bootstrap, percentile bounds, no multiplicity correction) are the ones
  implemented in code/touchbed/stats.py. TOST and Holm exist in code, and the paper correctly says they were not run.
- I recomputed H2-S2 from results/v4/h2 and reproduced it exactly: Δ −0.4452, bounds [−0.7485, −0.1616], p 0.0064.
- I recomputed the S2 G\* and per-seed student success from results/v4/test3_sub8 and reproduced it exactly.
- The S2 Cal′ verification (3.875 probes, 200 episodes, cal3 0–199) reproduces from results/v4/cal.
- Derived or after-the-fact quantities are almost all labelled as such:
  - the BI-first reading rule ("fixed in this revision rather than pre-registered");
  - the post-hoc sensitivity of the D gates and of H2 ("derived, not pre-registered");
  - the bootstrap p-value ("not pre-registered");
  - the 26 % first-move share ("derived");
  - the ~10× travel ratio ("ratio derived");
  - the 49× and 98× latency ratios ("derived");
  - the S2 Cal′ verification ("verified post hoc / report-only");
  - the R8 pipeline check ("report-only").
- The mismatches below are mis-attributions, unlabelled derivations, selective omissions or inconsistently applied
  rules. None is an invented number.

---

## Summary of the submission

The paper studies greedy cost-aware ball-EIG touch selection (G\*) for planar identity × pose localization with a
finger on a stand-off circle and a travel cost of 1 + κ|Δφ|/π. It reports four results:

1. **C1 (headroom).** A pre-registered bound on one-step look-ahead headroom over G\*: UB95 G(12) = 0.0221, with
   κ = 0 and κ = 2 rows.
2. **C2 (learnability).** DAgger distillation of G\* into a belief-free DeepSets head fails the non-inferiority gate
   twice in S12 (κ = 12) and once in S2 (κ = 2).
3. **C3 (distillation vs RL).** PPO on a ball-sPCE return and the distilled student show no detected difference on
   g_T. g_T ranks G\* below both learners, whereas the grid posterior ranks G\* above both.
4. **C4 (cost).** A latency decomposition, plus an exploratory comparison of reduced-size G\* with the students.

The paper is framed as a pre-registered characterisation (outcome-map row 4) with no method claim.

---

## Reviewer A (active perception / tactile localization)

### Strengths

1. **Unusually careful bookkeeping.** Pre-registered gates, a decision table (Table 2), and explicit labelling of
   report-only, exploratory and post-hoc items. I checked the headline numbers against the evidence and they match.
   Examples:
   - D4: −2.80 pp (thr −1.46), BI −0.105 (SE 0.039).
   - H3: G(12) = 0.01624, UB 0.0221.
   - All Table 5 contrasts.
   - Travel split: 4.26° vs 44.79° between-probe.
2. **The headroom estimator comes with instrument checks.** These are a notch construction with a known exact gap, a
   zero-gap bank and a one-sided bias guard. The paper is explicit that G is one-step headroom over a *reduced*
   completion among 32 screened actions, not a gap to the optimum.
3. **The travel decomposition is a useful correction.** It separates logged travel into the unavoidable first-leg grid
   snap (1.454°) and between-probe travel. It shows S12 is even more stay-and-probe than earlier drafts claimed.
4. **The S2 cell honestly tests the obvious objection** ("the planner never travels"). The κ = 2 headroom row was
   measured in exactly the S2 configuration; I confirmed κ = 2, τ = 4.7, C1 = 32 in results/v3/g2 headers.
5. **The S2 validation/test discrepancy is investigated, not hidden.** The R8 pipeline re-read reproduces actions,
   success and BI exactly on val3 0–49.
6. **Limitations are extensive and specific.**

### Weaknesses

1. **Thin novelty for an active-perception venue.** Greedy cost-aware EIG touch selection is established
   (Ottenhaus 2018; Hebert 2013; Javdani 2012). Measuring that one-step look-ahead adds ~2 % is, as the paper itself
   says, "expected from the theory". The headroom result is a replication on a coarser action set of a number known
   before the 0.03 threshold was registered (Section 4). The threshold was therefore set with the answer in view.
2. **The estimator is validated only at large gaps.** The notch checks validate it at an exact gap of 0.717 and it
   over-reads by 4–16 % relative (0.829 and 0.744). The bank checks only a zero gap. There is no check in the 0.02–0.05
   region where the decision is made. Further issues:
   - The selection bias of V_LA was not measured.
   - 29 of the 32 screened candidates are random.
   - "Small headroom" may therefore partly reflect a weak screen (no structured travel-then-fan family). The paper
     admits this, but it limits C1.
3. **Scope is narrow for RSS/CoRL.** The setup is a planar 2D simulation with one shape library (K = 8), Gaussian
   point/normal noise, no contact dynamics, no hardware and no held-out shapes. There is one cell per regime.
   Regime-level statements ("S2 adds a success separation") rest on comparisons of two cells, with no cross-cell test.
4. **The evaluator is not shown converged, and the remedy rule is post hoc.**
   - E′ failed. The 7.5 % success-flip rate between sub-4 and sub-8 is of the order of most contrasts.
   - The "BI-first" rule threshold of 7.5 pp was fixed in this revision. The S2 student − B-fan success contrast
     (+8.1 pp) clears it by 0.6 pp and is called "just above the evaluator's resolution". The abstract reports it
     without that qualifier.
   - The rule is also applied inconsistently. G\* − RL in S12 is +7.0 pp, which is below 7.5 pp, yet it is reported
     in Section 5.4 with ci95 [+0.2, +13.7] and no "within resolution" note.
   - The paper does not say that E′'s single counted flip came from set A (A12 B-fan, episode 1), a cell outside this
     study. Half of E′'s 16 episodes are from set A.
5. **g_T vs grid-posterior "inversion" is presented as the most transferable lesson, but is weakly evidenced.**
   - There is no interval for g_T(G\*) − g_T(learner). In S12 the difference is 5.30 vs 5.37, and 3 of 6 learner
     seeds are below G\*.
   - Cap saturation is dismissed as "rare" (0.4–3.4 % of learner episodes at exactly the cap). The RL training logs
     (14_behaviour.rl_final.sat_frac) show 23–31 % of end-of-training S12 episodes within 0.5 nats of the cap. Near-cap
     compression, not only exact saturation, could drive the ordering.
   - The claim should be restricted to "in S2 on point estimates, with no interval" until a G\*-vs-learner g_T
     bootstrap is run.
6. **The S2 baseline is a carry-over.** Only B-fan (the S12 H★) was run in S2. "The student beats the stay-and-fan
   heuristic in the travelling regime" is close to tautological: in that regime B-fan is −0.71 nats and −18.3 pp
   behind G\*. A travel-aware heuristic (B-spread or B-cov) is the relevant comparator.
7. **The paper is over-length.** It runs to about 11,100 words: Results ~3,070, Method ~2,190 and Experiments ~1,910.
   That is well above a 9-page budget, so the problem is not under-length. Section 4's methods notes and the repeated
   qualifiers in Sections 1, 5 and 7 could be cut substantially.

### Actionable revisions

1. Add a notch or synthetic check with an exact gap in 0.01–0.05, and report the estimator's bias there.
2. Add a structured "travel-then-fan" candidate family to the H3 screen, at least for the κ = 2 row.
3. Apply the BI-first rule uniformly or drop it:
   - Mark S12 G\* − RL success (+7.0 pp) as within resolution.
   - In the abstract, mark the S2 +8.1 pp as exploratory, on a reused split, and 0.6 pp above a post-hoc threshold.
4. Run sub-16 on the S2 student − G\* and student − B-fan contrasts (300 episodes), or at least on the 16 E′ episodes
   plus S2.
5. Bootstrap g_T(G\*) − g_T(student) and g_T(G\*) − g_T(RL) in both cells. Report near-cap fractions (within 0.5 nats)
   on test as well as exact-cap fractions.
6. Run B-spread and B-cov in S2, or explicitly retitle the S2 heuristic comparison.
7. State in the abstract and conclusion that E5 (reduced planners) is S12-only.
8. Resolve or remove the [PENDING] random anchor before submission. The raw S2 sub-8 random files on disk now hold 291
   of 300 episodes, so this is close to done.

### Score: 4 / 10 (Borderline reject)

The work is rigorous and honest, but the contribution is a careful negative characterisation in a toy planar
simulation. The headroom result was anticipated, and the most "transferable" observation lacks an interval.

---

## Reviewer B (robot learning: imitation, DAgger, RL)

### Strengths

1. **The learner comparison is properly controlled.** The two learners share the same head, action set, masking and
   budget; only the training signal differs. The paper is careful not to generalise from one PPO configuration to RL.
2. **Negative results are reported straight.** H1 is dead, D4 failed and H2 / H2-S2 are "not detected". The paper adds
   post-hoc power figures, labelled as such, showing that H2 could detect only ~0.5-nat advantages. I verified the
   arithmetic:
   - S12: 0.10 + 0.311 + 0.842 × 0.189 ≈ 0.57.
   - S2: 0.403 + 0.842 × 0.184 ≈ 0.56.
   - The S2 LB is 2.80 half-widths below the threshold.
3. **The behavioural diagnosis adds explanatory value.** RL collapses to exactly 3 probes with near-zero entropy
   (0.002–0.013) and travels 2.9–4× as far as G\*. The S2 student travels a G\*-like amount (37.7° vs 44.8°) but is
   only weakly correlated with G\* per episode (r 0.14–0.24) and reproduces none of G\*'s 300 action sequences.
4. **Label-fit analysis (S12) and the honest caveat about it.** Held-out top-1 sits close to train top-1, so the
   "generalisation, not capacity" reading is weak. The paper says so.

### Weaknesses

1. **The S2 training record contradicts the "budget-matched" framing, and the paper omits it.**
   - Section 5.3 says "under-fitting in S2 cannot be ruled out from the record". Section 6 says S2 "was trained with
     that budget-matched recipe from the start and still failed", which it presents as removing the
     optimisation-budget explanation.
   - The per-epoch logs in results/v4/d4/S_k2_s60x_r{0,1,2}.json tell a different story. Held-out R̄ reaches its
     minimum at epochs 22–130 in all nine rounds (e.g. s601 r0: 0.288 at epoch 34; s602 r0: 0.277 at epoch 74;
     s603 r0: 0.286 at epoch 29). It then rises by 0.007–0.034 to the epoch-200 value that the last-checkpoint rule
     keeps (0.308, 0.300, 0.312).
   - Training loss is still falling at epoch 200 (e.g. s601 r0: 4.93 → 4.46 between epochs 60 and 199).
   - The record therefore shows mild over-fitting to the teacher labels plus a last-checkpoint penalty. It does not
     show an unresolved under-fitting question.
   - This changes the reading of "making the planner travel did not make it learnable": the 200-epoch fixed recipe
     was not budget-neutral in S2. It overshot the held-out optimum.
2. **The non-inferiority gate is effectively an ~88 % one-sided bound, and the teacher's variance is ignored.**
   - The code (analysis_d4_v4.py:51) uses −δ + 1.645·SE·√(500/1000). That is z ≈ 1.16 on the observed SE, i.e. a
     projected-to-n = 1000 bound. The paper reproduces the formula correctly, but calling it a "non-inferiority gate"
     without noting the √0.5 projection will mislead readers.
   - G\* is a Monte Carlo planner run once per episode (one "seed"). The crossed bootstrap resamples learner seeds
     but cannot capture teacher MC variance.
   - Neither point changes a verdict, because the gates failed, but both should be stated.
3. **The comparators are not shown tuned.**
   - PPO config 2 was selected in S12 on a non-registered validation stream (val_v2) at the edge of the lr grid
     (1.09e-3 is the largest), and was not re-tuned for S2.
   - Every PPO policy collapses to exactly 3 probes. That is a pathology of the reward/budget interaction (no
     probe-count term), not a property of RL on this objective.
   - The distillation hyperparameters in S2 are reused from S12 without a grid. I confirmed hp 0 = (1e-3, β_T 4,
     λ 0.5, batch 256) in the S2 round configs.
   - The H2 comparison is therefore between one under-tuned RL and one un-tuned DAgger, with three seeds each. Its
     power is ~0.5 nats by the paper's own estimate.
4. **The S2 validation/test discrepancy remains unexplained and is large.**
   - The test deficit exceeds the val deficit by 5.4–11.2 pp per seed (≈ 2.0 combined SE under independence).
   - The pipeline check covers 50 episodes and two policies.
   - The derived "≈ 2.0 combined SE" figure is not labelled post hoc or derived, unlike the paper's other derived
     figures. The arithmetic does check: 0.074 / √(0.0218² + 0.031²) ≈ 1.95.
   - Since every S2 test row lies on a reused split, all S2 learner conclusions should be treated as exploratory, and
     the abstract does not do this.
5. **The amortization claim has no robotics-relevant cost axis.** The latency comparisons are:
   - 0.408 ms vs 913 ms for the student vs full G\*.
   - 20–46 ms for reduced G\*, with only the S12 E5 run.

   None of this is placed against actuation time. A probe stroke on a real finger is typically 0.5–2 s, so a 20–46 ms
   reduced planner is already negligible. The practical case for amortization is therefore unclear and should be
   discussed.
6. **The headline regime measure was changed after review.** The between-probe travel split (14_travel_split.json,
   "stage 18 v4 M4, report-only") now drives the abstract's regime definitions (4.3° / 44.8°). Table 4 labels it
   report-only, but the abstract and introduction do not say that the decomposition was added after the results.
7. **The belief-input control is under-fit** (train top-1 0.33–0.36), so the representation question is untested.
   The paper says so.

### Actionable revisions

1. Report the S2 held-out R̄ curves, and re-evaluate D4 (as a report-only row) with the min-R̄ checkpoint or an
   early-stopping rule. Revise Section 5.3 ("under-fitting cannot be ruled out") and Section 6 ("budget-matched
   recipe") to reflect the observed over-fitting.
2. Add one sentence explaining the √(500/1000) factor in gate (i), and that teacher MC variance is not in the SE.
3. Add a probe-count-aware or budget-aware PPO variant, or at least an S2 lr sweep, before drawing any H2-S2
   conclusion.
4. Label the "≈ 2.0 combined SE" figure as derived and post hoc. Run a fresh, untouched test split for S2 (or
   increase seeds to ≥ 5) to resolve the val/test gap.
5. Place latency against actuation time per probe.
6. Mark in the abstract that the between-probe travel figures come from a report-only decomposition added in this
   revision.
7. Trim to the page budget. The paper is ~11k words; move instrument notes and the Table 2 detail to an appendix.

### Score: 3 / 10 (Reject)

There is no new method, and the learnability conclusion rests on a recipe whose own logs show it overshot the
held-out optimum in S2. The RL comparator is a single collapsed configuration. The paper is honest, but for CoRL/RSS
it is a preliminary negative characterisation in a planar simulator.

---

## Checklist answers

1. **Topic adherence.** The paper stays on topic. The instrument notes (evaluator resolution, pipeline check) are
   correctly demoted to methods notes and limitations rather than contributions. The g_T/BI disagreement is kept
   inside C3 and is on-topic, but it is overstated as "the most transferable lesson".
2. **Methodology-evidence consistency.** Overall high; see the mismatch list below. No unsupported statistical test,
   metric or method was found.
3. **Trial count.** Consistent everywhere. No fabrication.
4. **Length.** Every section exceeds its minimum (Abstract 249 words, Introduction 1,229, Related Work 757, Method
   2,185, Experiments 1,909, Results 3,070). The total of ~11,100 words is over-length for 9 pages; it is not
   under-length.
5. **Top-conference verdict.** Not ready. The novelty is limited, and there is one cell per regime and three seeds.
   The comparators are untuned, the planar simulation has no hardware, and the S2 training record (checkpoint
   selection) undercuts the learnability reading.

## Mismatches found (claim vs evidence, with location)

| # | Location | Claim | Evidence | Severity |
|---|---|---|---|---|
| M1 | Section 1, "Two regimes" paragraph | "79.3 % of the planner's between-probe moves are zero, and the finger moves on average 4.3° … (test3 episodes 0–299)" | 79.3 % (frac_between_probe_moves_eq_0 = 0.7934) is from 14_behaviour on test3 0–499 (n = 500); only the 4.3° figure is on 0–299. Section 5.2 attributes the split correctly. | minor |
| M2 | Section 5.3 "S2 training record"; Section 6 para 2; Section 7 "Comparators not shown tuned" | "under-fitting in S2 cannot be ruled out from the record"; the S2 200-epoch recipe is treated as removing the optimisation-budget explanation | results/v4/d4/*.json per-epoch logs: held-out R̄ is minimal at epochs 22–130 in all 9 rounds and then rises by 0.007–0.034 to the kept epoch-200 value, while training loss keeps falling. This is over-fitting with a last-checkpoint penalty, and the paper omits it. | moderate (omission that changes the interpretation) |
| M3 | Section 5.4 "Success and BI" | G\* − RL S12 success +7.0 pp (ci95 [+0.2, +13.7]) reported without qualification | The paper's own BI-first rule (Section 4) puts any success contrast below 7.5 pp within the evaluator's resolution, so the rule is applied inconsistently. | minor |
| M4 | Section 5.3 "S2 (D4)" | "the difference is ≈ 2.0 combined SE under independence" | This is a derived, post-hoc statistic, not in any results file, and is unlabelled, unlike the paper's other derived figures. The arithmetic does check (≈ 1.95). | minor (labelling) |
| M5 | Abstract; Section 5.5 | S2 student > B-fan on success (+8.1 pp), stated in the abstract without "exploratory" | 14_s2_analysis is "exploratory", on a reused test split, and clears the post-hoc 7.5 pp resolution threshold by 0.6 pp (ci95 lower bound +1.7 pp). | minor (overstatement in abstract) |
| M6 | Abstract; Section 8 | "Reduced-size G\* at 21–46 ms per decision trails the students" (no cell named) | E5 (14_e5_analysis) is S12 test3 only; nothing was run in S2. | minor (scope omission) |
| M7 | Section 4 "Evaluator"; Table 2 R2 | E′ "failed: one counted success flip" (implied to be about this study's set S) | 12_e_analysis: the one counted flip is set A, B-fan, episode 1. The set-S flip did not count, and half of the 16 episodes are from set A. | minor (omitted context) |
| M8 | Section 5.4 "Instrument ordering" | "cap saturation of g_T is rare … so the cap alone is unlikely to explain the inversion" | This uses the exact-cap definition (≥ cap − 1e-6; analysis_behaviour_v3.py:69). End-of-training RL sat_frac within 0.5 nats of the cap is 0.23–0.31 (14_behaviour.rl_final; train_v2.py:241). Near-cap compression is not examined. | minor (under-supported) |
| M9 | Abstract; Section 1; Section 5.2 | Regimes defined by between-probe travel 4.3° / 44.8° | 14_travel_split.json is "report-only (stage 18 v4 M4)", added after the results in response to review. Table 4 labels it, but the abstract and introduction do not. | minor (labelling) |
| M10 | Section 4 "Gates D3 and D4" | Gate called "pre-registered non-inferiority" with margin 1.645·SE·√0.5 | analysis_d4_v4.py:51 uses √(500/1000), i.e. z ≈ 1.16 (≈ 88 % one-sided) on the observed SE. The G\* row has one run, so teacher MC variance is excluded. The formula is quoted correctly, but its meaning is not explained. | minor (methodological transparency) |
| M11 | Table 2 / Table 5 / Section 7 | S2 random row [PENDING] | Consistent with the evidence JSON (n = 215 of 300). The raw files on disk now hold 291 of 300, so the evidence JSON is stale. The placeholder must not reach submission. | presentation |
| M12 | Section 4 "H2 and H3 rules"; Section 5.1 | H3 called a pre-registered test with threshold 0.03 | The paper itself admits a near-identical estimate was known when 0.03 was registered. It is labelled, but it weakens "pre-registered" for C1. | labelled, noted |

No CRITICAL fabrication: no trial count, test, metric or method is claimed that the code and results do not support.
