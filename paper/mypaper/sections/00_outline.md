<!-- Stage 16 PAPER_OUTLINE [v5], run 41, 2026-11-09; fresh-context subagent; template paper_outline.md verbatim; prompts paper/mypaper/prompts/stage16_v5_*.txt -->

# Paper outline (stage 16, v5): pre-registered five-cell characterisation of amortizing G\*

**Venue (default until the owner decides; `results/v5/15_decision.md` §4.2, §4.5 c).** RSS 2027 Stage 1 extended
abstract (deadline 2026-12-04 AoE): ≤ 5 content pages + 1 page of references. Methods complete, experiments may be
preliminary. **Main body target ≈ 3,400 words** (abstract not counted), 2 tables, 2 figures. This is a stated deviation
from the 9-page floors of `hard_constraints` §3. The master draft may be longer and is condensed in stage 22.

**Paper type (binding, `15_decision.md` §1, §4.2–§4.4).** Measurement / characterisation paper only. Headline: the
distilled student is **not shown to match G\***. No method claim, no "effective component".

**Base.** v4 outline (`paper/mypaper/v4/00_outline_v4.md`) and v4 final draft (`paper/mypaper/v4/draft_v4_final.md`).
What changes against v4:
- one cell per regime → five cells (S2, S4, S8, S12 on set S; A16-2 on set A16);
- 3 → 5 seeds per learner;
- fresh test split test5;
- RL swept on S2, then fixed;
- all three heuristics in every cell, with a pilot-chosen H\*;
- best-held-out-checkpoint student recipe (pre-declared answer to the v4 P8 over-fitting item);
- E5 at sub 16, E6 latency, E7 512-action screen with an independent re-estimate.

The v3 S12 D3 and v4 S2 D4 results enter as **prior cells**. The v3 H3 headroom result is cited only as background to
E7. It is not a v5 contribution.

**Sources (only these may supply numbers).**
- v5: `results/v5/results_v5.json`. Paths are written `<block> > <key> > …`, where `<block>` is the literal top-level
  key: `12_d5_analysis.json`, `14_test5_analysis.json`, `14_e5_analysis.json`, `14_e6_analysis.json`,
  `12_e7_analysis.json`, `12_base_hstar.json`, `12_rl_sweep_selection.json`, `12_cal_analysis.json`,
  `13_freeze.json`, `15_posthoc_derived.json`. `<cell>` ∈ {S2, S4, S8, S12, A16-2}.
- **Every value from `15_posthoc_derived.json` is printed with the label "post hoc, no CI"** (its own `provenance`
  field). These values are: the student and RL means recovered from the diffs, the best-test5-heuristic margins, the
  job-2 latency ratios, and the H5b span translation.
- v4 / v3: `results/v4/results_v4.json` (cited `v4:`), `results/v3/results_v3.json` (cited `v3:`).
- Binding wording: `results/v5/14_analysis.md` (pass 2 S1–S3, M1–M8, m1–m8 replace the pass-1 sentences they cite) and
  `results/v5/15_decision.md` §4.3 / §4.4.
- Citations: `cite_key` from `docs/05_knowledge_cards.json` only. Every key below was checked against the 60 cards.
  Missing items are marked `[CITE-MISSING: …]`.

---

## 0. Global constraints

### 0.1 Title
**Proposed:** *Amortizing a Cost-Aware Information-Gain Touch Planner under Travel Cost: A Pre-Registered Five-Cell
Characterisation*
- The title names the question and the design and promises no answer: no "near-optimal", no "matches", no "Can … ?".
- **Fallback (shorter):** *Distilling a Cost-Aware Touch Planner across Travel Costs: A Pre-Registered Characterisation*.

### 0.2 Labels of every decision-bearing item (`15_decision.md` §2.1 list)
| Item | Label for the paper | Key |
|---|---|---|
| D5 (validation gate, per cell) | **fails in 5 / 5 cells, m = 0**; no remedy step (pre-registered) | `12_d5_analysis.json > H5a_validation > cells_pass` = [] ; `12_d5_analysis.json > <cell> > passes` = false |
| H5a (test5 student − G\*, Holm over 5) | 0 / 5 Holm rejections; equivalence not shown | `14_test5_analysis.json > <cell> > student_minus_gstar > success > holm_reject_5cells` |
| Student − H\* (pilot-chosen, Holm over 5) | 4 / 5 Holm rejections (S2 not) | `14_test5_analysis.json > <cell> > student_minus_hstar > success > holm_reject_5cells` |
| H2-v5 (g_T, LB > +0.10 nats) | met only in A16-2, where cfg-6 RL collapses | `14_test5_analysis.json > <cell> > H2_v5 > claim_student_higher_on_rl_objective` |
| Inversion (g_T vs posterior ordering) | false in every cell, incl. both `rl_success` checks | `14_test5_analysis.json > <cell> > H2_v5 > inversion`, `… > H2_v5 > check_rlsucc > inversion` (S2, S12) |
| H5b (trend of Δsucc on G\* travel) | "no trend detected over 5 cells" | `14_test5_analysis.json > H5b > verdict` |
| E5, E6, E7 | report-only, no verdict | `14_e5_analysis.json`, `14_e6_analysis.json`, `12_e7_analysis.json` |
| Prior: v3 S12 D3 (twice) | failed | `v3:12_d3_analysis.passes`, `v3:12_d3_analysis_rem.passes` = false |
| Prior: v4 S2 D4 | failed | `v4:12_d4_analysis.json.passes` = false |

### 0.3 Binding sentences (from `15_decision.md` §4.3; use verbatim or tighter)
- **D5 / headline (S1).** "The pre-registered gate failed in all five cells (m = 0). The student is below G\* in every
  cell on both splits (validation 3.2–6.0 pp, with S4 and A16-2 beyond the 4 pp margin; test5 0.2–2.5 pp, CIs down to
  −8.3 pp), so matching G\* is not supported."
- **Splits (S2).** "Validation point gaps are 3.2–6.0 pp and test5 point gaps are 0.2–2.5 pp (test5 95% CIs from −8.3 to
  +6.1 pp); no pooled estimate was computed." Always report both splits separately, each with its interval.
- **D5 on test5 (M1).** "Test5 point gaps are smaller than the validation gaps in every cell, but applying the D5 rule
  to test5 would still fail in about 4 of 5 cells, so test5 does not contradict the D5 verdict."
- **Shortfall (M3).** "A shortfall of up to 6.1 pp (the tightest lower bound, S8) is consistent with the data in every
  cell, and up to 8.3 pp in S4."
- **Heuristics (M2).** "The student beats the pilot-chosen H\* in 4/5 cells after Holm (+6.1 to +16.8 pp). In 4/5 cells,
  though, H\* is not the best heuristic on test5, and against the best test5 heuristic the post-hoc margin falls to
  +3.5 to +14.5 pp, with no CI."
- **RL (m7).** "Without multiplicity correction, the student beats cfg-6 RL on success with CIs excluding 0 in S2, S12
  and A16-2 (A16-2 confounded by RL collapse)."
- **H2-v5 (M7).** "H2-v5 is met only in A16-2 (LB 0.596 > 0.10), where cfg-6 RL collapses to 2 of 3 probes in 4/5 seeds
  and G\* also beats RL by 0.85 nats, so the result reflects RL failing to transfer rather than a student advantage."
- **RL tuning (m6).** "One RL configuration chosen on S2 was reused everywhere; it visibly fails in A16-2, and whether
  it is under-tuned in S4, S8 or S12 was not tested."
- **H5b (S3).** "H5b detects no trend of Δsucc on G\* travel over 5 cells (slope −0.0157/rad, ci95 [−0.104, 0.073]), but a
  change of up to about 7 pp across the observed travel range cannot be excluded."
- **Latency (M4, m2).** "With seed-701 timings, full G\* is 2,523–9,933× slower per decision (median paired ratio, CI
  rule met only in A16-2). Other seeds' student medians (0.36–0.51 ms) differ by up to about 24% within a cell, so each
  per-cell ratio is uncertain at about that level." Only S2 (9,933×) and A16-2 (8,301×) lie in the 7,000–10,000× band.
- **G\* run once (M5).** "G\* was run once per cell (n_seeds = [5, 1]), so any run-to-run variability of G\* (E7 shows
  noisy, upward-biased value estimates in S2) is missing from the student−G\* CIs, and those CIs may be too narrow."
- **E7 (M6).** "In S2 and S12, a 512-candidate G\* setting gives a larger independent-estimate gap than a 32-candidate
  setting (+0.048 and +0.018 nats per belief, n = 32). Whether the deployed G\* has headroom in success terms was not
  measured."
- **E5 (M8, m5).** "Re-reading at sub-16 flips 6.5–8% of single-seed outcomes and shifts the seed-701 student−G\*
  contrast by +0.02 (S2) and −0.03 (S12) on 200 episodes; its effect on the 5-seed test5 contrast was not measured."
  The change is about 0.8× the test5 gap in S2 and about 2× in S12.
- **v4 comparison (m8).** "v4's test3 gap (−10.2 pp, run context only) lies outside the v5 S2 test5 ci95 [−7.6, +2.7]
  pp, but without v4's interval the two cannot be formally compared."
  - **Flag for the main session.** `results_v4.json` does hold the v4 interval:
    `v4:14_s2_analysis.json.test3_sub8.diffs["student-gstar:success"]` = −0.1022, ci95 [−0.1656, −0.0433]. The premise
    "without v4's interval" is therefore stale.
  - **Proposed text, same claim scope:** "v4's test3 gap (−10.2 pp, ci95 [−16.6, −4.3]; different split, 3 seeds,
    last-checkpoint recipe) lies outside the v5 S2 test5 ci95 [−7.6, +2.7] pp; the two were not formally compared."
  - Use the proposed text only if the main session approves it. Otherwise drop the v4 comparison from the abstract-length
    paper.
  - **Main-session ruling (run 41):** approved, verified against `results/v4/results_v4.json` (diff −0.10222, ci95
    [−0.16556, −0.04333]); erratum to binding item m8 logged in `PROGRESS.md`. Use this wording (the seed-count and
    recipe qualifiers are trimmed until stage 17 checks them against the v4 amendment): "v4's test3 gap (−10.2 pp, ci95
    [−16.6, −4.3]; different test split and training recipe) lies outside the v5 S2 test5 ci95 [−7.6, +2.7] pp; the two
    were not formally compared." Row X10 is therefore in.
- **Bootstrap resolution (m3).** "p = 0.0" is printed as "p < 0.0002".
- **Freeze (m4).** `13_freeze.json` records 15 (S2, S12) or 10 (S4, S8, A16-2) weight hashes per cell. The statement
  that they were recorded before test5 comes from the run context.

### 0.4 Never write (`15_decision.md` §4.4, plus the v4 items still in force)
- That the student "matches", "reaches" or "is equivalent to" G\*, or that its gap is "small" or "negligible".
- A pooled "true gap of 1–5 pp".
- "Consistently 3–6 pp behind" as a headline.
- That test5 "contradicts" or "overturns" D5.
- "No dependence on travel cost".
- "The student beats the best heuristic" without the pilot-choice qualifier and the post-hoc margins.
- "Distillation beats RL", or "the student beats RL" without the multiplicity and A16-2 caveats.
- The A16-2 H2-v5 result framed as a student advantage.
- "G\* is deterministic", "G\* is sub-optimal", or "G\* has headroom in success terms".
- A blanket "~7,000–10,000× faster".
- "A 6–8 pp shortfall is consistent in every cell".
- "RL is under-tuned in S4/S8/S12".
- "p = 0".
- Any effective-component claim.
- Any cross-cell comparison worded as a finding beyond H5b.
- Any claim that v4's −10.2 pp was formally refuted.
- Carried from v4: "near-optimal"; "the student imitates G\*'s travel"; latency ratios without "per decision";
  infrastructure events (label packing failure, time-guard stops, re-dispatches) as findings.
- **Number homes (v4 gate weakness "numbers repeated across sections").** Each number has one home: Table 1, Table 2 or
  its Results paragraph. The abstract, introduction and conclusion use only the §0.3 ranges, and never a new split of
  them.

---

## 1. Abstract (≈ 190 words, not counted)
**Goal.** State the research problem in the words of the topic constraint, give the design once, and give the outcomes
once in their §0.3 forms.

**Order.**
1. **Problem.** Online cost-aware greedy information-gain touch planning (G\*) is slow per decision. Can a policy
   distilled from it match it? How does it compare with RL on the same objective and with hand-designed probing
   heuristics? Does the gap change with travel cost?
2. **Design.** A pre-registered five-cell study: travel cost κ = 2/4/8/12 on one shape library, plus a second library
   A16 at κ = 2. It uses 5 seeds per learner and a fresh test split, with the earlier S12 and S2 cells as prior
   evidence.
3. **Primary result.** The D5 gate fails in all five cells. Use the S1 sentence, short form.
4. **Heuristics.** The student beats the pilot-chosen heuristic in 4/5 cells (Holm). Use the M2 short form with the
   post-hoc margin range.
5. **RL.** Distillation scores higher on RL's own objective only in A16-2, where RL collapses. No g_T/posterior
   inversion is detected.
6. **Travel cost.** No trend detected; about 7 pp is not excluded.
7. **Latency.** 2,523–9,933× faster per decision, seed-701 timings.
8. **Scope.** "Simulation, planar shapes, preliminary."

**Evidence links.** The same keys as the §0.3 sentences:
- `12_d5_analysis.json > H5a_validation > cells_pass`; `12_d5_analysis.json > <cell> > succ > delta_hat`;
- `14_test5_analysis.json > <cell> > student_minus_gstar > success > {diff, ci95}`;
- `14_test5_analysis.json > <cell> > student_minus_hstar > success > holm_reject_5cells`;
- `15_posthoc_derived.json > cells > <cell> > margin_student_minus_best_test5_heuristic` (post hoc, no CI);
- `14_test5_analysis.json > <cell> > H2_v5 > {claim_student_higher_on_rl_objective, inversion}`;
- `14_test5_analysis.json > H5b > {slope_per_rad, ci95_per_rad, verdict}`;
- `15_posthoc_derived.json > H5b_span_translation > ci95_times_span` (post hoc);
- `14_e6_analysis.json > <cell> > job1 > ratio_full_gstar_over_student > median`.

**Cards.** None in the abstract.

---

## 2. Introduction (480 words)
**Goal.** Motivate amortization of a cost-aware information-gain touch planner. Say why one cell per regime (v4) could
not answer the regime question. State the findings once and list C1–C5 in the decision's order.

1. **(110 w) Active tactile localization under travel cost.** Particle belief over identity and planar pose. Next touch
   chosen by expected information gain per unit cost. Each decision is expensive.
   Cards: `petrovskaya2011global`, `hebert2013next`, `javdani2012efficient`, `zheng2024bayesian`, `zheng2026bayesian`,
   `ottenhaus2018active`, `seminara2019active`.
2. **(100 w) Amortization.** Policy-based BED learns a fast policy from a contrastive bound; tactile RL; imitation of
   information-gathering oracles. The open question is whether distilling a cost-aware greedy planner keeps its quality
   when travel cost changes, compared with RL trained on the same objective.
   Cards: `foster2021deep`, `ivanova2021implicit`, `blau2022optimizing`, `hedman2025step`, `rainforth2024modern`,
   `riou2024reinforcement`, `niemann2024when`, `ross2011reduction`, `choudhury2017adaptive`, `nguyen2024amortized`.
3. **(90 w) Why five cells.** Earlier gates failed in one cell per regime: S12 D3 (twice) and S2 D4. The v4 review asked
   for "more cells per regime (several kappa values and at least one more shape library) and more learner seeds" and
   for a fresh test split, S2-tuned RL, all heuristics and an evaluator check (prior-feedback required actions). v5
   pre-registered all of these before any run (amendments v5.0 / v5.1), including the gate D5 with no remedy step.
   No numbers here.
4. **(110 w) Findings, once each.**
   - S1 sentence.
   - M2 sentence, short form.
   - H2-v5 / inversion, one clause each.
   - H5b (S3 short form).
   - Latency range (M4 short form).
5. **(70 w) Contributions (order from `15_decision.md` §4.2).**
   - **C1. Learnability across five cells.** D5 fails 5/5. The student is below G\* in every cell on both splits and is
     not shown within δ. Paired with the v3/v4 gate failures.
   - **C2. A cheap policy that beats pilot-chosen heuristics.** 4/5 cells under Holm, with the post-hoc best-heuristic
     margins and the latency range beside it.
   - **C3. Distillation vs RL.** H2-v5 holds only in A16-2 (RL collapse). The inversion is false everywhere. The
     student−RL success rows are uncorrected.
   - **C4. Travel cost and behaviour.** H5b: no trend detected, about 7 pp not excluded. The student travels less than G\*
     in every cell.
   - **C5. Methods note.** E5 evaluator resolution, E7 selection bias, the g_T / BI ordering, and reporting the two
     splits separately. Placed in §4–§5 and §7, not in Results (decision §4.2 "C5 goes into methods and limitations").

**Evidence links.**
- `v3:12_d3_analysis.passes`, `v3:12_d3_analysis_rem.passes`, `v4:12_d4_analysis.json.passes`;
- `12_d5_analysis.json > H5a_validation > cells_pass`;
- the abstract keys above.

---

## 3. Related work (260 words, three paragraphs, each ending with the gap)
1. **Tactile localization and next-best touch** (90 w).
   Cards: `petrovskaya2011global`, `koval2015pose`, `bauza2023tac2pose`, `hebert2013next`, `zheng2024bayesian`,
   `zheng2026bayesian`, `gordon2026active`, `kamtikar2026tactful`, `ottenhaus2018active`, `seminara2019active`.
   Gap: cost-aware greedy selection is common but runs online. How well it can be amortized, and how that changes with
   travel cost, is rarely measured.
2. **Greedy information gathering and its guarantees** (70 w).
   Cards: `javdani2012efficient`, `vien2015touch`, `chen2015submodular`, `esfandiari2019adaptivity`.
   Gap: the guarantees concern the greedy planner itself, not a learned copy of it. We treat G\* as the reference, not as
   an optimum (M6).
3. **Amortized and learned active sensing** (100 w).
   - BED policies: `foster2021deep`, `ivanova2021implicit`, `blau2022optimizing`, `hedman2025step`,
     `iqbal2024recursive`, `huang2026aline`, `rainforth2024modern`, `shen2023reinforcement`, `asano2022sequential`.
   - Tactile RL: `riou2021seeing`, `riou2024reinforcement`, `niemann2024when`, `xu2023tandem3d`, `fleer2020efficient`,
     `schneider2025tactile`.
   - Imitation of information-gathering oracles: `choudhury2017adaptive`, `nguyen2024amortized`, `ross2011reduction`.
   - Gap: no pre-registered, multi-cell comparison of planner distillation and RL on the same head and the RL objective,
     with the posterior-success read-out reported next to the contrastive bound.

**Evidence links.** Cards only.

---

## 4. Problem and methods (750 words; a technical approach, with constants from JSON or marked)
**Goal.** Give a complete description of the task, the planner G\*, the shared head and the two learners, the
heuristics, and the five cells.

### 4.1 Task, belief, cost, metrics (190 w)
- State s = (identity k, x, y, θ). The finger sits on a stand-off circle at angle φ_t. An action is (φ′, ψ), drawn from a
  discrete grid.
  [NEED: action-grid size and stand-off geometry, copied from the frozen design doc into a citable source; the v4
  outline states the grid, but no v5 JSON field holds it.]
- Travel cost c(a) = 1 + κ|Δφ|/π (the v4 definition) [NEED: cite the frozen design-doc line for the cost formula].
  Feasibility c(a) ≤ τ_rem. Probe budget n\*. Particle-filter belief.
- **Metrics.**
  - Success (sub-8 grid posterior read-out).
  - Ball information BI (nats).
  - g_T (ball-sPCE, the RL objective, computed without the grid).
  - Travel: `travel_rad`, also `travel_deg`. Define travel as in v4 M4, including the initial snap.
  - Probe count.
- Shape library S has K = 8 identities (4 base/variant pairs) (v4 review M1). A16 is set A with K = [NEED: A16 identity count in a citable
  results/doc field; it is stated in `docs/07c_amendment_v5_0.md` P0, not in JSON].
- **Table 0 (in-text): the five cells**, with κ / n\* / τ.

  | Cell | κ | n\* | τ |
  |---|---|---|---|
  | S2 | 2 | 4 | 4.7 |
  | S4 | 4 | 4 | 4.8 |
  | S8 | 8 | 4 | 4.8 |
  | S12 | 12 | 4 | 4.9 |
  | A16-2 | 2 | 3 | 3.4 |

  - A16 n\* = 3, with A16 keep-check G\* success 0.8 inside the pre-registered keep range:
    `12_cal_analysis.json > keep > A16 > gstar_success_sub8_at_nstar` = 0.8.
  - [NEED: the keep range, stated in amendment v5.0 P0, in a citable field.]
- **Evidence.**
  - `v3:12_cal_analysis.tau.S_k2_nstar4.tau` (4.7), `v3:12_cal_analysis.tau.S_k12_nstar4.tau` (4.9);
  - `12_cal_analysis.json > tau > S_k4 > tau` (4.8), `… > tau > S_k8 > tau` (4.8), `… > tau > A16_k2 > {n_star, tau}`
    (3, 3.4);
  - `12_cal_analysis.json > n_star > A16 > {n_star, gstar_success_sub8}` (3, 0.975);
  - `12_cal_analysis.json > keep > A16 > {gstar_success_sub8_at_nstar, keep}` (0.8, true).
- Cards: `petrovskaya2011global`, `koval2015pose`.

### 4.2 Planner G\* (100 w)
- G\* takes the argmax of expected information gain over cost, over the feasible candidates. It is deployed as
  configuration `g2000_512_64` (the E6 key). Its exported per-action score vector is the distillation label.
- The reduced configurations `g125_512_16` and `g500_512_4` are named here because they are timed in E6.
- Say once that G\* is a greedy reference, not an optimum (M6 scope). E7 is described in §5.
- [NEED: meaning of the three numbers in `g2000_512_64` (particles / candidates / inner samples), from the frozen design
  doc.]
- Cards: `ottenhaus2018active`, `javdani2012efficient`.

### 4.3 Shared head and learners (330 w)
- **Head.** A belief-free, finger-relative DeepSets head over the touch history, with masked logits over the action set.
  It is the same for both learners, so the training signal is the isolated variable (a v4 strength).
  [CITE-MISSING: DeepSets (Zaheer et al. 2017).]
- **Distillation (E2).**
  - Soft cross-entropy to the tempered G\* scores plus a CE term to the argmax.
  - DAgger rounds with a decaying mixing coefficient β.
  - Every round trains a fixed number of epochs and **keeps the checkpoint with the lowest held-out label regret R̄**.
    This is the pre-declared answer to the v4 over-fitting finding (prior feedback P8).
  - Seeds 701–705, the same hyper-parameters (hp 0) in every cell.
  - [NEED: label episodes per cell, number of DAgger rounds and β schedule, episodes per round and epochs per round,
    from `docs/07c_amendment_v5_0.md` E2, in a citable field.]
  - [NEED: the last-checkpoint sensitivity row, pre-declared in amendment v5.0 E2, is not in `results_v5.json` or the
    analysis. Cite it only if it is added; otherwise say "logged, not analysed".]
  - Cards: `ross2011reduction`, `choudhury2017adaptive`.
- **RL (E3).**
  - PPO on the same head, with a reward that telescopes to g_T.
  - Sweep on S2 only: 8 configurations, selected by the v3 D9 rule (highest final trainer-validation ball-sPCE; ties
    within 0.02 nats go to the lower index).
  - Selected **cfg 6** (6.300 vs 6.241 for cfg 0, the v3/v4 configuration). On the sampled-policy metric cfg 1 scores
    higher (6.316 vs 6.205). State this, as in analysis §4 item 7.
  - cfg 6 is reused in every cell with seeds 711–715.
  - Control arm `rl_success`: terminal-success reward, S2 and S12 only.
  - [NEED: RL episodes per seed and the per-seed `rl_success` episode counts; amendment v5.1c requires the latter next
    to every `rl_success` number (it records time-guard truncation), and neither is in `results_v5.json`.]
  - **Evidence.**
    - `12_rl_sweep_selection.json > {rule, selected_cfg, validation_stream}`;
    - `12_rl_sweep_selection.json > rows[6] > {lr, ent_coef, batch, critic_lr, final_val_ball_spce, final_val_ball_spce_sampled}`;
    - `12_rl_sweep_selection.json > rows[0] > final_val_ball_spce`;
    - `12_rl_sweep_selection.json > rows[1] > final_val_ball_spce_sampled`.
  - Cards: `schulman2017proximal`, `blau2022optimizing`, `foster2021deep`.

### 4.4 Heuristics (80 w)
- **Random** (masked).
- **B-spread.**
- **B-fan**: travel-nearest stay-and-fan.
- **B-cov.**
- **H\*** in each cell is the best of the three on pilot3 0–199 (sub 8; ties B-spread < B-fan < B-cov). The pilot picks
  b_cov for S2 and S8 and b_fan for S4, S12 and A16-2.
- **Evidence.**
  - `12_base_hstar.json > rule`;
  - `12_base_hstar.json > cells > <cell> > {H_star, H_star_success, b_fan, b_spread, b_cov}`;
  - `14_test5_analysis.json > <cell> > H_star`.

### 4.5 Decision rules (50 w; full statement in §5)
- D5, H5a, H5b, H2-v5, inversion and Holm are named here, with a pointer to Table 1.

---

## 5. Experimental protocol (330 words)
**Goal.** Every claim traces to a frozen rule. The section also carries the C5 methods notes on the evaluator and on the
planner estimate.

- **Pre-registration (60 w).**
  - Amendment v5.0, written before any v5 run, fixes the cells, seeds, test5, D5, H5a, H5b, H2-v5, H\* selection and Holm.
  - Amendment v5.1 fills in values the rules produce: τ, A16 n\*, cfg 6.
  - Addendum v5.1e cuts test5 from 500 to 300 episodes under the frozen reduction order, before any test5 episode.
  - No number here except the 500 → 300 cut (analysis §4 item 1).
- **Splits (60 w).**
  - val3 0–499 for D5 (`12_d5_analysis.json > <cell> > n_episodes` = 500).
  - test5 0–299, 300 episodes per method per cell (`14_test5_analysis.json > <cell> > {n_required, episodes_per_method, complete, gt_complete}`).
  - pilot3 0–199 for H\*.
  - The G\* validation sources differ: S2 from v4 files, S12 from v3 files, the other cells from v5
    (`12_d5_analysis.json > <cell> > gstar_source`). State this in the same sentence as the D5 result.
  - Freeze: m4 wording (`13_freeze.json > rule`, `13_freeze.json > cells > <cell> > sha256`).
- **D5 rule (60 w).**
  - Pass iff three clauses hold:
    1. Δ̂_succ ≥ the SE-dependent threshold, −0.04 + 1.163·se, e.g. S2 −0.01454 (analysis pass 2 M1);
    2. Δ̂_BI ≥ −0.15;
    3. enough seeds pass the per-seed clause, δ = 0.04.
  - Evidence: `12_d5_analysis.json > <cell> > {delta, succ > {se, threshold}, bi > threshold, seeds_ok}`.
  - [NEED: the per-seed clause count and the lower floor of clause 1 in a citable field; they are stated in amendment
    v5.0, not in JSON.]
- **Statistics (70 w).**
  - Crossed episode × seed bootstrap ci95 and two-sided p, with `n_seeds` [5, 1] vs G\*/H\* and [5, 5] vs RL.
  - The p-values resolve to 0.0002 (m3). [NEED: resample count; not in JSON.]
  - Holm over 5 cells, for student−G\* and student−H\* success only.
  - One-sided 95 % LB for H2-v5 against +0.10.
  - WLS slope for H5b, with weights fixed (`14_test5_analysis.json > H5b > weights`).
  - BI, RL, `rl_success` and g_T contrasts are uncorrected (analysis §4 item 9).
  - [CITE-MISSING: Holm (1979) step-down procedure.] [CITE-MISSING: bootstrap confidence intervals (Efron).]
- **C5 notes (80 w).**
  - **E5 (evaluator resolution).** M8 + m5 sentence. Evidence: `14_e5_analysis.json > <S2|S12> > <gstar|student_s701> > {flip_rate, flips_8to16_gain, flips_8to16_loss, success_sub8, success_sub16, mean_abs_dBI}`, `… > contrast_change_student_minus_gstar`, `… > n_episodes`.
  - **E7 (planner estimate).** M6 sentence plus the analysis §2.6 selection-bias clause: positive with a CI excluding 0 in
    S2, null in S12. Evidence: `12_e7_analysis.json > design`, `12_e7_analysis.json > cells > <S2|S12> > paired_indep_gap_512_minus_32 > {est, ci95, n}`, `… > <C1_32|C1_512> > selection_bias_nats`.
  - **E6 protocol.** Job 1 times student 701, full G\* and the two reduced G\* configurations interleaved on the same
    states: n = 1000 in the S cells and 500 in A16-2. Job 2 times students 702–705, n = 500. Evidence:
    `14_e6_analysis.json > <cell> > {job1_source, job1 > * > n, job1_complete}`.
- **Table 1 is placed here** (rows in §9).

---

## 6. Results (1,100 words; C1 and C2 lead, C3 and C4 one paragraph each, per `15_decision.md` §4.2)

### 6.1 C1. Does the student match G\*? (400 w)
**Goal.** Answer the primary question with the registered decision first, then the test5 description. Report the two
splits separately.

1. **(120 w) D5 on validation.**
   - S1 sentence.
   - Per-cell Δ̂_succ vs threshold, from Table 1.
   - BI passes in 5/5.
   - All 25 per-seed differences are negative, from −0.068 to −0.01. No A16-2 seed passes.
   - The G\* sources differ (§5).
   - Evidence: `12_d5_analysis.json > <cell> > succ > {student_mean, gstar_mean, delta_hat, se, threshold, passes, per_seed}`, `… > bi > {delta_hat, passes}`, `… > seeds_ok`, `… > passes`, `12_d5_analysis.json > H5a_validation`.
2. **(130 w) H5a on test5.**
   - Student − G\* success in every cell: Table 2, with the per-cell diff, ci95, p and Holm flag.
   - "0/5 Holm; equivalence not shown."
   - CI widths are 9.6–12.3 pp (m1).
   - M3 sentence.
   - M1 sentence: test5 does not contradict D5.
   - Evidence: `14_test5_analysis.json > <cell> > student_minus_gstar > success > {diff, ci95, p_two_sided, n_seeds, holm_reject_5cells}`, `14_test5_analysis.json > H5a`.
3. **(70 w) BI on test5 (uncorrected).**
   - The ci95 excludes 0 in S4 (−0.1314) and S12 (−0.0910).
   - A16-2 is +0.08477, with a CI that includes 0.
   - Evidence: `14_test5_analysis.json > <cell> > student_minus_gstar > ball_info > {diff, ci95, p_two_sided}`.
4. **(80 w) Prior cells and the v4 split gap.**
   - v3 S12 D3 failed twice: `v3:12_d3_analysis.succ.delta_hat` (−0.0587), `v3:12_d3_analysis_rem.succ.delta_hat`
     (−0.044).
   - v4 S2 D4 failed: `v4:12_d4_analysis.json.succ.{delta_hat, threshold}` (−0.0280 vs −0.01464).
   - v4 comparison: §0.3 m8 item, with the main-session flag.
   - Close with: "the amortization hypothesis has now failed its pre-registered gate in every cell tested across three
     rounds" (decision §2.2 scope; no new number).
   - G\* run once (M5) goes here as one sentence.

### 6.2 C2. Against heuristics, and at what cost (300 w)
**Goal.** Give the one positive pre-registered result together with its qualifiers.

1. **(150 w) Student − H\* (Holm).**
   - Table 2 row: diff, ci95, Holm.
   - S2 is the exception: lower bound −0.001333, p 0.0558.
   - M2 sentence.
   - Next to it, the post-hoc best-test5 heuristic and margin per cell (labelled post hoc, no CI):
     S2 b_cov +0.0587 (= H\*); S4 b_cov +0.0513; S8 b_fan +0.0607; S12 b_cov +0.0347; A16-2 b_cov +0.1447.
   - BI vs H\*: ci95 excludes 0 in all 5 cells (uncorrected).
   - Evidence:
     - `14_test5_analysis.json > <cell> > student_minus_hstar > {success, ball_info} > {diff, ci95, p_two_sided, holm_reject_5cells}`;
     - `15_posthoc_derived.json > cells > <cell> > {best_test5_heuristic, margin_student_minus_best_test5_heuristic, margin_student_minus_H_star, heuristic_success}` (post hoc, no CI);
     - `14_test5_analysis.json > <cell> > means > {b_fan, b_spread, b_cov, random} > success`.
2. **(150 w) Latency (E6, report-only).**
   - M4 sentence.
   - Per-cell ratios with ci95 and `half_width_ok`: S2 9,933× [8,179, 10,224]; S4 6,990× [4,747, 7,270]; S8 3,463×
     [2,680, 3,645]; S12 2,523× [2,068, 2,675]; A16-2 8,301× [8,080, 8,472]. Only A16-2 meets the rule.
   - Student medians 0.326–0.500 ms (seed 701). Full G\* 0.910–4.880 s. Most of the cross-cell spread comes from G\*
     time (M4).
   - The job-2 ratios as a sensitivity column (post hoc, no CI, "ratio of medians, not paired").
   - Reduced G\* medians (`g125_512_16`, `g500_512_4`) in one clause as timings only. No accuracy was measured for them on
     test5, so no frontier claim and no "matched-accuracy" claim.
   - Hardware: 2-core runners (analysis §4 item 8).
   - Never use the blanket "7,000–10,000×".
   - Evidence:
     - `14_e6_analysis.json > <cell> > job1 > {student, g2000_512_64, g125_512_16, g500_512_4} > {median, ci95, n, half_width_ok}`;
     - `14_e6_analysis.json > <cell> > job1 > ratio_full_gstar_over_student > {median, ci95, half_width_ok}`;
     - `14_e6_analysis.json > <cell> > job2 > <702..705> > median`;
     - `15_posthoc_derived.json > cells > <cell> > latency > ratio_full_gstar_median_over_job2_student_medians` (post hoc).

### 6.3 C3. Distillation vs RL on the same objective (200 w)
**Goal.** Report H2-v5 and the inversion check as registered, and keep the RL-collapse caveat attached.

- H2-v5 per cell: LB vs +0.10 (Table 1). M7 sentence for A16-2.
- In S2/S4/S8, RL has the higher g_T as a point estimate while the student has the higher success. No RL-higher CI
  excludes 0, so the inversion is false everywhere (analysis §2.4). The `rl_success` check is also false in S2 and S12.
- Student − RL success, uncorrected: m7 sentence. Values in Table 2.
- Student − `rl_success`: S2 +0.1087 [0.0593, 0.158]; S12 +0.0793 [0.022, 0.134]. Attach the [NEED] on `rl_success`
  episode counts.
- RL behaviour in A16-2: seeds 712–715 use 2.0 probes against n\* = 3, success 0.1833–0.2267. m6 sentence.
- Evidence:
  - `14_test5_analysis.json > <cell> > H2_v5 > {student_minus_rl_gT > {diff, lower_one_sided_95}, claim_student_higher_on_rl_objective, rl_minus_student_gT, gstar_minus_rl_gT, gstar_minus_student_gT, means_gT, inversion}`;
  - `… > H2_v5 > check_rlsucc` (S2, S12);
  - `14_test5_analysis.json > <cell> > student_minus_rl > {success, ball_info}`;
  - `14_test5_analysis.json > <S2|S12> > student_minus_rlsucc > success`;
  - `14_test5_analysis.json > A16-2 > means > <rl_s711..rl_s715> > {n_probes, success}`;
  - `12_cal_analysis.json > n_star > A16 > n_star`.
- Cards: `blau2022optimizing`, `foster2021deep`.

### 6.4 C4. Travel cost and behaviour (200 w)
**Goal.** Give the one cross-cell test, H5b, and the behavioural description. No other cross-cell finding.

- **H5b (S3 sentence).**
  - Slope −0.01571 per rad, ci95 [−0.1041, 0.07277], or per 100°.
  - The span translation is −7.4 to +5.2 pp (post hoc, no CI).
  - State that the regressor is G\* mean test5 travel, not κ, and that A16-2 is one of the 5 points.
  - Evidence: `14_test5_analysis.json > H5b > {cells, delta_succ, gstar_mean_travel_rad, weights, slope_per_rad, ci95_per_rad, slope_per_100deg, ci95_per_100deg, verdict}`; `15_posthoc_derived.json > H5b_span_translation`.
- **Behaviour (descriptive).**
  - In every cell the student travels less than G\*, and RL travels more than both.
  - G\* travel ranges from 0.1112 rad (S12) to 0.8213 rad (S2).
  - Probe counts: student 2.9–4.0, G\* 2.93–3.97, RL near 3 in the S cells.
  - No mechanism is claimed. "Why the student travels less" is posed as an open question (decision §2.3).
  - Evidence: `14_test5_analysis.json > <cell> > means > <method> > {travel_rad, travel_deg, n_probes}`.

---

## 7. Discussion and limitations (420 words)
**Discussion (150 w).**
- Across five travel costs and two libraries, a cheap distilled policy sits below its teacher in every cell and is
  not shown within the 4 pp margin. Validation and test5 are reported separately, with no pooled estimate.
- Against the hand-designed heuristics chosen on a pilot, it wins in 4/5 cells, with the margin over the best test5
  heuristic stated beside it.
- RL on the same objective, tuned once on S2, does not transfer to A16-2.
- **C5 g_T / BI note.** On test5 point estimates G\* has the lowest mean g_T of the three policies in all four S cells,
  while it has the highest success. Every G\*−learner g_T CI includes 0 in the S cells. The observation is that the
  contrastive bound and the posterior read-out can rank policies differently. It is not a finding (inversion false; no
  interval excludes 0).
  Evidence: `14_test5_analysis.json > <cell> > H2_v5 > {means_gT, gstar_minus_rl_gT, gstar_minus_student_gT}`.
  Cards: `foster2021deep`, `hedman2025step`, `iqbal2024recursive`.
- Close with next steps phrased as questions: student-visited regret, per-cell RL tuning, a G\* rerun for seed variance.

**Limitations (270 w, one sentence each).**
1. **Power and equivalence.** test5 has 300 episodes (cut from 500, addendum v5.1e). The CIs are 9.6–12.3 pp wide. No
   equivalence test was run.
2. **G\* run once** (M5). E7 is in nats and is not linked to the deployed G\* or to success (M6).
3. **Evaluator** (M8). E5 covers 2 cells, 200 episodes and one seed.
4. **Heuristic selection** came from a 200-episode pilot (M2).
5. **RL** (m6, M7). `rl_success` exists only in S2/S12, and its runs were budget-truncated
   (`[NEED: episode counts]`).
6. **Multiplicity.** More than 30 uncorrected BI, RL and g_T contrasts (analysis §4 item 9).
7. **Latency.** The CI rule is met in 1/5 cells, the ratios rest on one seed, and the runners differ across cells
   (M4, m2).
8. **Validation G\* sources** are heterogeneous (S2 v4, S12 v3).
9. **Scope.** Simulation only (TouchBED), planar shapes, two shape sets, one κ for A16, sub-8 read-out, H5b on 5 points.
10. **Not run, by decision §4.1 item 3** (each stated here): retraining or remedy rounds, per-cell RL re-tuning, more
    test5 episodes, a G\* rerun, latency re-timing, a test of the post-hoc margins, any new BI or g_T test.

---

## 8. Conclusion (90 words)
Four clauses, no new numbers:
1. The pre-registered gate fails in all five cells, so matching G\* is not supported.
2. The student beats pilot-chosen heuristics in 4/5 cells and decides 2,523–9,933× faster per decision (seed-701
   timings). Use the M4 range only, no blanket band.
3. Distillation scores higher on RL's objective only where RL collapses.
4. No travel-cost trend is detected, and about 7 pp is not excluded.

Close with "pre-registered; simulation; preliminary".

---

## 9. Every results row, mapped to results-JSON keys
**Tags.**
- DEC: pre-registered decision.
- GATE: calibration or completeness gate.
- REP: reported, no test.
- EXPL: exploratory (ci95, uncorrected).
- PH: post hoc, from `15_posthoc_derived.json`, no CI.
- PRIOR: v3/v4 cell.

### Table 1: decisions and gates (Section 5)
| Row | Item (values as printed) | Keys | Tag |
|---|---|---|---|
| T1.1 | Cells: κ, n\*, τ; A16 keep (0.8) | `v3:12_cal_analysis.tau.{S_k2_nstar4,S_k12_nstar4}.tau`; `12_cal_analysis.json > tau > {S_k4,S_k8,A16_k2} > {n_star,tau}`; `12_cal_analysis.json > n_star > A16`; `12_cal_analysis.json > keep > A16` | GATE |
| T1.2 | RL selection: cfg 6, 6.300 vs 6.241 (cfg 0); sampled metric cfg 1 6.316 vs 6.205 | `12_rl_sweep_selection.json > {rule, selected_cfg, validation_stream}`, `> rows[0] > final_val_ball_spce`, `> rows[1] > final_val_ball_spce_sampled`, `> rows[6] > {final_val_ball_spce, final_val_ball_spce_sampled}` | GATE |
| T1.3 | H\* per cell (S2 b_cov, S4 b_fan, S8 b_cov, S12 b_fan, A16-2 b_fan) | `12_base_hstar.json > cells > <cell> > {H_star, H_star_success}` | GATE |
| T1.4a–e | D5 per cell: student, G\*, Δ̂_succ, threshold, Δ̂_BI, seeds, pass. S2 0.4812 / 0.514 / −0.0328 / −0.01454 / −0.0682; S4 0.4492 / 0.504 / −0.0548 / −0.01503 / −0.1334; S8 0.4116 / 0.448 / −0.0364 / −0.01639 / −0.0465; S12 0.4136 / 0.446 / −0.0324 / −0.01722 / −0.0635; A16-2 0.4124 / 0.472 / −0.0596 / −0.01229 / −0.0629; all fail | `12_d5_analysis.json > <cell> > succ > {student_mean, gstar_mean, delta_hat, se, threshold, passes, per_seed}`, `> bi > {delta_hat, threshold, passes}`, `> seeds_ok`, `> passes`, `> gstar_source` | DEC |
| T1.5 | H5a validation: m = 0 of 5 | `12_d5_analysis.json > H5a_validation > {cells_complete, cells_pass}`; `14_test5_analysis.json > H5a > validation_cells_within_delta` | DEC |
| T1.6 | H5a test5 Holm: 0/5 | `14_test5_analysis.json > <cell> > student_minus_gstar > success > holm_reject_5cells` | DEC |
| T1.7 | Student − H\* Holm: 4/5 (S2 not) | `14_test5_analysis.json > <cell> > student_minus_hstar > success > holm_reject_5cells` | DEC |
| T1.8a–e | H2-v5 LB: S2 −0.4971, S4 −0.6555, S8 −0.4861, S12 −0.3044, A16-2 +0.5964 (met) | `14_test5_analysis.json > <cell> > H2_v5 > {student_minus_rl_gT > lower_one_sided_95, claim_student_higher_on_rl_objective}` | DEC |
| T1.9 | Inversion: false in 5/5; rl_success check false in S2, S12 | `14_test5_analysis.json > <cell> > H2_v5 > inversion`; `> H2_v5 > check_rlsucc > inversion` | DEC |
| T1.10 | H5b: slope −0.01571 /rad, ci95 [−0.1041, 0.07277]; "no trend detected over 5 cells" | `14_test5_analysis.json > H5b > {slope_per_rad, ci95_per_rad, verdict}` | DEC |
| T1.11 | Prior S12 D3: first attempt −0.0587, remedy −0.044; both fail | `v3:12_d3_analysis.{succ,passes}`, `v3:12_d3_analysis_rem.{succ,passes}` | PRIOR DEC |
| T1.12 | Prior S2 D4: −0.0280 vs −0.01464; fail | `v4:12_d4_analysis.json.{succ,bi,seeds_ok,passes}` | PRIOR DEC |
| T1.13 | Freeze: 15 / 10 hashes per cell | `13_freeze.json > {rule, cells > <cell> > sha256}` | GATE |
| T1.14 | test5 completeness (300 per method; g_T complete) | `14_test5_analysis.json > <cell> > {n_required, episodes_per_method, complete, gt_episodes_per_method, gt_complete}` | GATE |

### Table 2: test5 per cell (Section 6), 300 episodes per method
| Row | Item | Keys | Tag |
|---|---|---|---|
| T2.1 | G\* success / BI / travel / probes (S2 0.5333; S4 0.4967; S8 0.4567; S12 0.4567; A16-2 0.49) | `14_test5_analysis.json > <cell> > means > gstar > {success, ball_info, travel_rad, n_probes}` | REP |
| T2.2 | Student seed range (min–max of 701–705) | `14_test5_analysis.json > <cell> > means > student_s70{1..5} > {success, travel_rad, n_probes}` | REP |
| T2.3 | Student 5-seed mean (S2 0.5087; S4 0.4713; S8 0.444; S12 0.4413; A16-2 0.488) | `15_posthoc_derived.json > cells > <cell> > student_success_mean_from_diff` | PH |
| T2.4 | RL seed range and 5-seed mean (S2 0.424; S4 0.4167; S8 0.412; S12 0.3687; A16-2 0.222) | `14_test5_analysis.json > <cell> > means > rl_s71{1..5}`; `15_posthoc_derived.json > cells > <cell> > {rl_success_mean_from_diff, rl_seed_means_listed}` | REP / PH |
| T2.5 | Heuristics: random, b_fan, b_spread, b_cov success | `14_test5_analysis.json > <cell> > means > {random, b_fan, b_spread, b_cov} > success` | REP |
| T2.6 | Student − G\* success: diff, ci95, p, Holm (see §0.3) | `14_test5_analysis.json > <cell> > student_minus_gstar > success > *` | DEC (H5a) |
| T2.7 | Student − G\* BI | `14_test5_analysis.json > <cell> > student_minus_gstar > ball_info > {diff, ci95, p_two_sided}` | EXPL |
| T2.8 | Student − H\* success, Holm; BI | `14_test5_analysis.json > <cell> > student_minus_hstar > {success, ball_info} > *` | DEC / EXPL |
| T2.9 | Student − best test5 heuristic (S2 +0.0587, S4 +0.0513, S8 +0.0607, S12 +0.0347, A16-2 +0.1447) | `15_posthoc_derived.json > cells > <cell> > {best_test5_heuristic, margin_student_minus_best_test5_heuristic}` | PH |
| T2.10 | Student − RL success and BI (S2 +0.08467, S4 +0.05467, S8 +0.032, S12 +0.07267, A16-2 +0.266) | `14_test5_analysis.json > <cell> > student_minus_rl > {success, ball_info} > {diff, ci95, p_two_sided}` | EXPL |
| T2.11 | Student − rl_success (S2, S12) | `14_test5_analysis.json > <S2\|S12> > student_minus_rlsucc > {success, ball_info}` | EXPL |
| T2.12 | g_T means: student / RL / G\* | `14_test5_analysis.json > <cell> > H2_v5 > means_gT > {student, rl, gstar}`; `> check_rlsucc > means_gT_rlsucc` | DEC input / REP |
| T2.13 | g_T contrasts: RL − student, G\* − RL, G\* − student (ci95) | `14_test5_analysis.json > <cell> > H2_v5 > {rl_minus_student_gT, gstar_minus_rl_gT, gstar_minus_student_gT}` | EXPL |

### In-text rows (diagnostics and report-only items; no ablation is claimed, decision §4.4)
| Row | Item | Keys | Tag |
|---|---|---|---|
| X1 | E5 sub 8 → sub 16: flip rates 0.065–0.08; G\* 0.54 → 0.54 (S2), 0.48 → 0.505 (S12); student 701 0.465 → 0.485, 0.455 → 0.45; contrast change +0.02 / −0.03; gains/losses; mean \|ΔBI\| ≤ 0.004034 | `14_e5_analysis.json > <S2\|S12> > {n_episodes, complete, gstar, student_s701, contrast_change_student_minus_gstar}` | REP |
| X2 | E7: paired 512 − 32 independent gap S2 0.04838 [0.01681, 0.08697], S12 0.01830 [0.004013, 0.03652]; selection bias S2 0.01926 [0.001030, 0.04193] (C1_32), 0.02179 [0.004270, 0.04013] (C1_512); S12 0.004470 [−0.007718, 0.01884], −0.002040 [−0.01574, 0.01258] | `12_e7_analysis.json > design`; `12_e7_analysis.json > cells > <S2\|S12> > {paired_indep_gap_512_minus_32, C1_32 > selection_bias_nats, C1_512 > selection_bias_nats}` | REP |
| X3 | E6 latency (§6.2 values) | `14_e6_analysis.json > <cell> > {job1_source, job1 > *, job1_complete, job2 > *}` | REP |
| X4 | E6 job-2 ratio sensitivity | `15_posthoc_derived.json > cells > <cell> > latency > ratio_full_gstar_median_over_job2_student_medians` | PH |
| X5 | H5b span translation (−0.0739, +0.0517) | `15_posthoc_derived.json > H5b_span_translation > {travel_span_rad, span_rad, ci95_times_span}` | PH |
| X6 | Behaviour: travel and probes, all methods | `14_test5_analysis.json > <cell> > means > <method> > {travel_rad, travel_deg, n_probes}` | REP |
| X7 | RL collapse in A16-2 (2.0 probes, seeds 712–715) | `14_test5_analysis.json > A16-2 > means > rl_s71{2..5} > {n_probes, success}`; `12_cal_analysis.json > n_star > A16 > n_star` | REP |
| X8 | D5 per-seed differences (25, all negative) | `12_d5_analysis.json > <cell> > succ > per_seed` | DEC input |
| X9 | H\* pilot values (200 episodes per heuristic) | `12_base_hstar.json > cells > <cell> > {b_fan, b_spread, b_cov} > {n, success, se_success}` | GATE input |
| X10 | v4 test3 S2 gap −0.1022 [−0.1656, −0.0433] (only if the main session approves the §0.3 m8 proposal) | `v4:14_s2_analysis.json.test3_sub8.diffs["student-gstar:success"]` | PRIOR REP |

**Not in any results JSON. Do not cite as numbers until added:**
- the last-checkpoint sensitivity row;
- per-seed `rl_success` episode counts;
- RL / DAgger / label budgets;
- the bootstrap resample count.

---

## 10. Figure plan

### Figure 1 (full width, top of page 1, ≈ 1/3 page; schematic panels A–C plus a JSON-plotted panel D)
**Story.** One planner, one learned head, five travel regimes. As travel cost falls, G\* travels more, from a few
degrees per episode at κ = 12 to tens of degrees at κ = 2. Across all five cells the distilled student stays below G\*
on success on both splits, without a detectable trend in travel. The pre-registered gate fails everywhere, so the
figure shows a measured gap, not a match.

**Visual elements.**
- **Panel A, task (schematic).**
  - Top-down grey polygon in a dashed uncertainty box, with faint ghost outlines for the particle belief over identity
    × pose.
  - Stand-off circle, fingertip at φ_t.
  - Orange travel arrow to φ′, labelled "c(a) = 1 + κ|Δφ|/π".
  - Blue probe arrow tilted by ψ, ending at a contact marker.
- **Panel B, five cells ordered by G\* test5 travel (JSON-labelled schematic).**
  - A row of five small circles, each with schematic probe marks. Fanned probes with little orange arc at the right
    (S12); probes spread around the circle and joined by orange arcs at the left (S2). A16-2 is marked with a different
    outline colour (second library).
  - Label under each circle, from `14_test5_analysis.json > <cell> > means > gstar > travel_deg`: S12 6.37°, S8 9.40°,
    A16-2 21.22°, S4 23.18°, S2 47.06°.
  - Traces are labelled "schematic".
- **Panel C, the comparison (schematic).** Belief → three branches:
  - (i) G\*: EIG/c over the feasible actions, argmax;
  - (ii) the DeepSets head on the finger-frame touch history → masked logits, with a solid arrow "DAgger on G\* scores (best held-out checkpoint)" and a dashed arrow "PPO, reward = ball-sPCE (g_T)";
  - (iii) heuristics B-fan / B-spread / B-cov, with "H\* chosen on pilot".
  - No timing or ratio is printed on the panel. They live in §6.2.
- **Panel D, headline (plotted from JSON with the dataviz skill; not generated).**
  - x axis: G\* mean test5 travel (rad), from `14_test5_analysis.json > H5b > gstar_mean_travel_rad`.
  - y axis: student − G\* success (pp).
  - Filled points with ci95 whiskers: test5 diffs (`14_test5_analysis.json > <cell> > student_minus_gstar > success > {diff, ci95}`).
  - Hollow points at the same x: validation Δ̂_succ (`12_d5_analysis.json > <cell> > succ > delta_hat`). They have no
    whiskers, because the D5 SE is a gate input, not a CI.
  - Horizontal dashed lines at 0 and at −δ = −4 pp.
  - Point labels: S2 / S4 / S8 / S12 / A16-2, with A16-2 in the second-library colour.
  - Corner text: "D5: 0/5 pass · H5b slope −0.0157/rad, ci95 [−0.104, 0.073], no trend detected".
  - No fitted line: the WLS intercept is not in the JSON. [NEED: WLS intercept, only if a fitted line is wanted.]

**Draft caption.**
> **Figure 1.** *Amortizing a cost-aware touch planner across travel costs.* (A) A finger on a stand-off circle chooses
> where to move, paying travel cost proportional to |Δφ|, and which way to probe; the belief is a particle set over
> identity and planar pose. (B) The five pre-registered cells, ordered by the planner G\*'s mean travel per test
> episode (6.37° at κ = 12 to 47.06° at κ = 2 on shape set S; A16-2 is a second shape set at κ = 2); traces are
> schematic. (C) One belief-free DeepSets policy is trained by DAgger on G\*'s scores or by PPO on G\*'s
> information objective, and is compared with hand-designed probing heuristics. (D) Student − G\* success: test5 mean
> with paired 95 % CI (filled; 300 episodes, 5 student seeds) and validation point estimate (hollow; 500 episodes). The
> student is below G\* in every cell on both splits, and the pre-registered gate fails in all five cells, so a match
> within δ = 4 pp (dashed) is not supported; no trend with travel is detected. Simulation; preliminary.

(Caption numbers: `14_test5_analysis.json > S12 > means > gstar > travel_deg` and `… > S2 > means > gstar > travel_deg`.)

### Figure 2 (one column, two stacked panels; dataviz skill)
- **(a) Comparator forest plot, success (pp).** For each cell (5 rows), plot:
  - student − H\* with ci95 (filled; Holm-significant marked);
  - student − best test5 heuristic as a hollow diamond with no whisker, labelled "post hoc";
  - student − RL with ci95 (grey, "uncorrected");
  - in S2 and S12, student − `rl_success`.
  A16-2 RL is annotated "RL collapse: 2 of 3 probes, 4/5 seeds".
  Keys: T2.8, T2.9, T2.10, T2.11, X7.
- **(b) g_T vs success ordering (C5 note).** Per cell, plot:
  - g_T(student) − g_T(RL) with its one-sided LB and the +0.10 line;
  - g_T(G\*) − g_T(RL) with ci95.
  Caption: "inversion not detected in any cell; uncorrected". Keys: T1.8, T2.13.

### Tables
- **Table 1:** §9 Table 1, condensed to one row per cell plus a decision column.
- **Table 2:** §9 Table 2, condensed to G\*, student, RL, b_fan, b_cov, random success per cell, plus the student − G\*
  and student − H\* contrasts. BI goes to the master draft appendix if space is short.

---

## 11. Word budget
| Section | Words |
|---|---|
| Abstract | 190 (not counted) |
| 1 Introduction | 480 |
| 2 Related work | 260 |
| 3 Problem and methods | 750 |
| 4 Experimental protocol | 330 |
| 5 Results (C1 400, C2 300, C3 200, C4 200) | 1,100 |
| 6 Discussion and limitations | 420 |
| 7 Conclusion | 90 |
| **Body total** | **3,430** |

Outline sections 2–8 are paper sections 1–7. The full gate record (E6 500-decision records, pilot tables,
amendment-by-amendment log) is kept only in the master draft appendix and cut in stage 22.

## 12. Open markers
**[NEED] markers (12).** Each one is an item the analysis, the decision and the JSONs do not hold. None blocks drafting.
1. Action-grid size and geometry (§4.1).
2. Cost-formula source line (§4.1).
3. A16 identity count in a citable field (§4.1).
4. The A16 keep range in a citable field (§4.1).
5. The meaning of `g2000_512_64` (§4.2).
6. Label, DAgger and epoch budgets (§4.3).
7. The last-checkpoint sensitivity row (§4.3).
8. RL episodes per seed and `rl_success` episode counts (§4.3; referred to again in §6.3).
9. The D5 per-seed count and floor (§5).
10. The bootstrap resample count (§5).
11. The `rl_success` episode counts, in the limitations (§7).
12. The WLS intercept, optional (§10).

**[CITE-MISSING] markers (3).**
1. DeepSets.
2. Holm step-down.
3. Bootstrap CIs.
