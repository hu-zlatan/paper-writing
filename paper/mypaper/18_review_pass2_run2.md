# Stage 18 PEER_REVIEW, evidence audit, pass 2 (after revision), run 2

Paper: "Can Cost-Aware Information-Gain Touch Selection Be Amortized? Look-Ahead Headroom and Learnability under Travel Cost"

Evidence used: the prompt's evidence block (results_v3.json, the latency log head, the grep of the stats code) and direct
inspection of `code/` (`analysis_behaviour_v3.py`, `analysis_m4_v3.py`, `analysis_h2_v3.py`, `touchbed/lookahead.py`,
`touchbed/lookahead_tb.py`, `touchbed/g2.py`, `touchbed/distill.py`, `touchbed/stats.py`), `results/v3/` (raw `g2/`,
`d3long/`, `d3rem/`, `test3/`, `rl/`), `results/v2/12_g2_analysis.json`, `docs/07c_amendment_v3_0.md` and git history.

---

## Reviewer A (robotics / active perception; significance and framing)

**Summary.** The paper studies cost-aware greedy expected-information-gain touch selection (G\*) for planar tactile
localization, with a joint identity × pose particle belief and a travel cost on a stand-off circle. It asks (H3) how much
one-step look-ahead adds over G\* and (H1/H2) whether G\* can be amortized by DAgger distillation or by PPO with the
same DeepSets head. The study is pre-registered, and the record reaches the pre-written "characterisation" outcome. The
revision adds a behaviour table showing that the single tested cell (S, κ = 12, n\* = 4) is a stay-and-probe regime, an
exploratory 200-epoch student, a B-fan comparison and an appendix gate record.

**Strengths.**
1. The paper is unusually honest. Gates, failed remedies, descoped items, provisional rows and the instrument limits are
   all reported, and the outcome-map routing is easy to audit. The numbers I checked match the JSON to the reported
   precision.
2. The new behaviour diagnostics (Table 2d) change how the paper should be read, and the authors take them seriously.
   Under this budget the planner hardly moves, so the "stranded finger" motivation hardly applies. The paper now says
   this in the abstract, introduction, discussion and limitations.
3. The latency decomposition (C4) is a small but real and useful result. Assimilation plus neighbour lists take 15 % of
   G\*'s time, which caps the speed-up from candidate pruning at about 6.7×. It is measured and explains the H1-fb
   withdrawal.
4. Using the same head, action set and objective for DAgger and PPO is the right design for the question in C2/C3.

**Weaknesses.**
1. **Significance is low for RSS/CoRL, and the revision makes this clearer.** All learning results come from one
   simulated planar cell, and that cell turns out not to exercise the paper's central coupling. With τ₁₂ = 4.9, any move
   above about 13.5° costs a probe. G\* travels 6.1° per episode, the students 1.5–2.0° (about 1.4° of which is the
   initial snap to the 5.625° grid; see the B-fan row). The title promises "under travel cost", but what is answered is
   "when travel is effectively forbidden". In that regime a belief-free stay-and-fan rule (B-fan) is statistically
   indistinguishable from both learners, and G\* beats it by only 6.7 pp. There is no hardware, no real tactile sensor,
   no 3-D objects and no held-out shapes. Four contributions sit on one κ, one shape set and one budget, and the
   necessary next design (a cell where travel binds) "was not run". At a robotics venue this reads as a well-documented
   pilot study, not a paper.
2. **The negative amortization headline is weaker than the abstract suggests.** The new long-training row reports
   long − G\* = −1.7 pp, ci95 [−6.8, +3.4], and BI −0.008 nats, ci95 [−0.083, +0.066]. Held-out R̄ improved for all
   three seeds (0.187/0.184/0.201 → 0.181/0.164/0.173). After 200 epochs (about 6.5 min instead of about 10 s per round)
   the student is therefore statistically indistinguishable from G\* on test, and the held-out metric improves with more
   optimisation. Neither fact is in the abstract or the conclusion. The abstract still leads with "neither DAgger
   distillation nor PPO was shown to reach G\*". That sentence is technically true, but read alone it misleads. The fair
   summary for distillation is "inconclusive, with optimisation budget a live explanation". It is not "fails".
3. **The Discussion reads the long-training row in the wrong direction.** It says the row "fits the generalisation
   reading better than a capacity limit" and that held-out top-1 "stayed at 0.503–0.530". The remedied students'
   held-out top-1 was 0.4916–0.5067, so it rose, and held-out R̄ improved on every seed. More training improving
   held-out fit is evidence for under-optimisation. The sentence should say so.
4. **H3 extrapolates beyond what it measures.** The Discussion says "there is little evidence that a deeper planner would
   have been a better one at this budget". H3 measures a single deviating first step, followed by a *reduced* greedy
   completion, over 32 screened actions. It says nothing about deeper planning. In this regime the alternatives that
   matter are the other approach offsets at or near φ_t. I counted from the raw `results/v3/g2/S_k12_*.jsonl`: on
   average only 2.96 of the 7 other offsets at G\*'s angle were screened (min 0, max 7). An exhaustive screen of the
   local neighbourhood is cheap and is what this regime calls for.
5. **H2/C3 rests on an objective that misorders the methods.** g_T(G\*) = 5.299 lies below both learners (5.368), while
   grid BI puts G\* clearly above both. The revision correctly shows that cap saturation is rare (0.4–5.8 %), but that
   leaves the ball-sPCE estimate (L = 4095, J = 16) as a noisy or biased proxy for the evaluation target. RL learns a
   distinct 3-probe, high-travel strategy that ties the student on g_T yet loses 0.29 nats BI. "Dense supervision did
   not beat RL on RL's own objective" is then a statement about a proxy that does not track localization. C3 should be
   presented as a finding about the objective, not about the learners.
6. **The practical baseline is still missing.** Reduced G\* configurations were timed but never scored. For example,
   g500_512_16 takes 0.073 s (12× faster than full G\*) and g125_32_4 takes 4.2 ms (only about 10× slower than the
   student). Without their accuracy, the 2,200× figure is not informative for a practitioner. The paper says this
   itself, but then the latency claim should be dropped from the abstract.
7. **Presentation.** The main body is about 9,000 words plus eight tables, well beyond a 9-page (or RSS 8-page) limit.
   Results (about 2,900 words) repeats D3 numbers in Sections 1, 5.2, 7 and Appendix A. The Conclusion still lists "a
   longer-trained student (running)", which is stale.

**Actionable revisions (A).**
- A1. Put the long-training result in the abstract and conclusion with its intervals (−1.7 pp, [−6.8, +3.4] vs G\*).
  Rephrase the distillation finding as inconclusive, rewrite the Discussion paragraph on "why the student falls short",
  and remove "(running)" and "stayed".
- A2. Either run a travel-binding cell (larger τ or smaller κ such that G\* moves, for example κ = 2 learners or a budget
  allowing 1–2 strokes of travel), or retitle and reframe the paper around the stay-and-probe regime ("... in a
  Stay-and-Probe Regime"). Also drop "under travel cost" as an implied general claim.
- A3. Re-run H3 with an exhaustive screen of all feasible actions (≤ 168 at step 0), or at least all ψ at φ_t ± 2 grid
  steps. Delete the "deeper planner" sentence.
- A4. Score 2–3 reduced-G\* configurations (for example N = 500, C = 512, M = 16 and N = 125, C = 128, M = 16) on test3
  0–299 and compare them with the students at matched latency, or remove the speed-up from the abstract.
- A5. Cut about 30 %. Move Table 0 details, the evaluator note and the per-seed text into the appendix, and keep one
  statement of each D3 number.

**Score: 3 / 10 (Reject).** The work is careful and honest, but its significance is low: one simulated cell that does
not exercise the motivating trade-off, and conclusions that are mostly non-detections. I would not recommend
presentation at RSS/CoRL (or NeurIPS/ICML) in this form.

---

## Reviewer B (methodology–evidence consistency; statistics)

**Summary of audit.** I compared every new or revised number against `results_v3.json` and the code, and re-derived
several from raw files. Trial counts are consistent throughout: 3 student seeds, 3 RL seeds, 500 val3 episodes, 300 for
D3-B, test3 0–499 for g_T and behaviour, 0–299 for success and BI, 100 beliefs per κ for H3, 20 for the bias check, and
1,000 latency decisions over 253 episodes. There is no inflation of trials or seeds. The statistical machinery claimed
(crossed episode × seed bootstrap, B = 10,000, one-sided bounds, ci90/ci95) exists in `touchbed/stats.py` and is the one
used by `analysis_m4_v3.py` and `analysis_h2_v3.py`. TOST and Holm exist in code, and the paper correctly says they were
not run. I found no fabricated results. I did find several description and interpretation mismatches.

**Strengths.**
1. The numbers I checked are faithful to the JSON: Tables 2a–2d, A1, the D3 thresholds and the H2 bounds.
2. The pre-specification of the long-training readings is genuine. The readings in `docs/07c_amendment_v3_0.md` were
   committed in 1b77b63 (20:25 UTC). The only `d3long` files in that commit were empty logs. The trained models and
   test3 reads arrived later (cee374f 20:35, ff5e48a 21:43). The run follows the description: `init: None` (from
   scratch), `fixed_epochs: 200`, and exactly the remedied student's 43 shards and held-out shards.
3. Scope wording for H3 is now consistently "over the 32 screened first actions / reduced greedy completion" in the
   Abstract, C1, Sections 3.3, 5.1, 7 and 8. The v2 estimate known at registration is disclosed.
4. The D3 threshold arithmetic reproduces: −0.04 + 1.645·SE·√0.5 gives −1.43, −1.68 and −0.75 pp. The BI threshold
   floors at −0.15.

**Weaknesses / discrepancies.**
1. **The teacher tie fraction is misdescribed (Sections 5.2, 7).** The paper says the "teacher tie fraction ... is 0.0
   in all 210 logged evaluations, so exact ties in G\*'s scores do not depress top-1". In code, `regret()` in
   `touchbed/distill.py` defines `tie = (s_max − s_med < ρ·s_max)`, which flags decisions where the whole score vector
   is flat (max within 5 % of the median). It does not flag several actions tied at the argmax. A value of 0.0 therefore
   says nothing about exact or near ties at the top, which is the quantity that would depress top-1. The sentence should
   be corrected. A top-2 margin statistic (for example the fraction of decisions with (s₁ − s₂)/s₁ < 0.05) is easy to
   compute from the stored label shards and would test the near-tie explanation that Sections 5.1 and 6 lean on.
   Minor: the 210 count predates the long-training logs, which add 600 more evaluations that are also 0.0.
2. **The runtime disclosure is incomplete (Section 4, Table 0).** The paper states one runtime, Python 3.12.15 /
   numpy 2.5.4. The remedied and long students were trained under Python 3.13.18 / numpy 2.5.3 (`env` in
   `results/v3/d3rem/*.json` and `d3long/*.json`), with MKL_NUM_THREADS unset. RL, test3 evaluation and latency used
   3.12.15 / 2.5.4. This is not a fabrication, but it is a reproducibility mismatch and should be stated.
3. **The long-training row is labelled "pre-registered readings" (Section 5.2 heading).** The readings were written
   before the run, but after the freeze and after test3 results for every other arm were known. Two exploratory rows
   (B-fan, long student) have now been added on the same test3 episodes after unblinding. "Pre-specified exploratory
   readings (post-freeze)" is the accurate label, and test-set reuse should be listed in Limitations.
4. **The long-training interpretation does not follow from the numbers (Section 6).** See Reviewer A, weakness 3.
   Held-out top-1 rose from 0.4916–0.5067 to 0.5033–0.5301, and held-out R̄ improved on all three seeds. "Stayed" is
   inaccurate, and the evidence favours the optimisation explanation more than the text admits.
5. **Selection bias is non-zero, and the bias check is the same size as the effect.** The zero-gap bank reads 0.00254,
   about 16 % of G(12). This follows from V_LA being a max over re-estimates that always include G\*'s action (per-belief
   gap ≥ 0 by construction: 38 of 99 beliefs have gap 0 and none are negative). V_G\* is under-read by 0.087 nats
   (4.3 %) on 20 beliefs, against a 0.041-nat gap. The paper discloses both, but Hold is then a statement that the bound
   on a quantity of uncertain bias is below 0.03. A bias-corrected G (for example subtracting the zero-gap-bank mean)
   should be shown.
6. **The v2 history is only partly reported.** The paper cites v2 G(12) = 0.0146 and G(0) = 0.0049. The same v2 file
   also has G(6) = 0.0185 (UB 0.0266), above G(12). The descriptive ordering G(0) ≤ G(2) ≤ G(12) should not be read as
   monotone in κ, and the v2 κ = 6 value should be mentioned if v2 is used as the replication anchor.
7. **Inference with three seeds.** The crossed bootstrap resamples 3 seeds with replacement. With 3 seeds, the percentile
   intervals on the seed dimension are coarse and probably anti-conservative (RL success per seed 0.367/0.390/0.313).
   The paper says the seed dimension dominates, which is fair, but the G\* − RL ci95 lower bound of +0.2 pp should not
   be described as RL "trailing", without qualification.
8. **Stale text.** The Conclusion says "a longer-trained student (running)". The HTML word-count comment still lists
   `[PENDING:long_student]` as remaining, and the change log describes D3-B as "298 episodes, −19.9 pp". The body
   correctly uses 300 / −20.1.
9. **Length.** 9,007 main-body words. No section is under-length, but the paper is well over a 9-page budget.

**Actionable revisions (B).**
- B1. Fix the tie-fraction sentence, and add a top-2 near-tie statistic from the label shards.
- B2. Report both runtimes in Table 0 and Section 4.
- B3. Relabel the long-training and B-fan rows as post-freeze exploratory analyses on test3, and add test-split reuse to
  Limitations.
- B4. Correct the "stayed" wording and rewrite the generalisation-versus-optimisation paragraph. State in the abstract
  that the long student is within −1.7 pp [−6.8, +3.4] of G\*.
- B5. Report a bias-adjusted G(12) (minus the zero-gap-bank mean) next to the raw estimate, and mention the v2 κ = 6
  value.
- B6. Remove the stale "(running)" text and clean the HTML comments before export.

**Score: 4 / 10 (Borderline, leaning reject).** Evidence consistency is good and there is no fabrication. The remaining
mismatches are descriptive (the tie statistic, the runtime) and interpretive (the long-training reading). The study's
conclusions are mostly non-detections in one cell, and its main new result (the long student matching G\* within the
noise) undercuts its own headline.

---

## Verified spot-checks

| # | Claim in paper | Source checked | Verdict |
|---|---|---|---|
| 1 | G\* travel 6.1 / 6.3 / 24.9°, 79.3 % zero moves, 6.3 % > 1 step, 3: 19 / 4: 481 | `14_behaviour.json` gstar; definitions in `analysis_behaviour_v3.py` (between-probe φ-index moves, > 1 means ≥ 2 grid steps) | Match |
| 2 | Students 1.5–2.0° travel, 97.7–99.7 % zero, all 4 probes; RL 23.0–25.8°, 3 probes, 47.3–54.9 % > 1 step, zero 0.0/21.9/18.4 % | `14_behaviour.json` | Match |
| 3 | B-fan travel 1.5° occurs before the first probe | 100 % zero between-probe moves; `phi_moves` skips the start angle; 1.45° ≈ the expected snap to the 5.625° grid | Consistent (inference) |
| 4 | g_T at cap: G\* 5.8 %, students 2.4–3.4 %, RL 0.4–1.2 %; trainer sat_frac 22.7–31.3 %; RL entropy 0.0020–0.0125 | `14_behaviour.json` methods / rl_final | Match |
| 5 | Long student: train top-1 0.602–0.628, held-out 0.503–0.530, held-out R̄ 0.181/0.164/0.173 vs 0.187/0.184/0.201 | `14_labelfit.json` | Match. The "stayed" wording in Section 6 is inaccurate (remedied held-out top-1 was 0.492–0.507) |
| 6 | Long success 41.0 % (40.7/43.3/39.0), long − remedied +2.8 pp [−1.0, +6.7], long − G\* −1.7 pp [−6.8, +3.4], BI −0.008 [−0.083, +0.066] | `14_m4_analysis.json` exploratory_long_student | Match |
| 7 | Long student trained from scratch, fixed 200 epochs, on exactly the remedied round-2 data; readings written before the run | `d3long/S_k12_long200_s50*.json` (init None, fixed_epochs 200, 43 shards identical to `d3rem/..._r2.json`, 17,083 decisions); git 1b77b63 (readings, empty logs) before cee374f / ff5e48a | Verified |
| 8 | H3 Table 2a k12: G 0.01624, UB 0.02210, V_LA 2.548, V_G\* 2.506, frac differs 0.62, no budget 1 | `12_g2_analysis.json`; re-derived means 2.5476 / 2.5062 from raw `results/v3/g2/S_k12_*.jsonl` (100 beliefs; 38 zero-gap) | Match |
| 9 | 32 screened = G\*'s full-size action + 3 structured set-up moves + random feasible; top 4 + G\* re-estimated with 4 × 64; completion N_LA 500, 128 candidates, M 16 | `touchbed/lookahead.py`, `lookahead_tb.py`, `g2.py` | Match. 7 of 99 beliefs had only 24 feasible candidates; on average 2.96 of the 7 other same-angle offsets were screened |
| 10 | Previous iteration G(12) = 0.0146 (UB 0.0208), G(0) 0.0049 | `results/v2/12_g2_analysis.json` | Match. Not reported: v2 G(6) = 0.0185 (UB 0.0266) |
| 11 | Instrument checks: notch 0.8290 (band [0.573, 0.860]), travel-notch 0.7438 vs exact 0.7166, zero-gap 0.00254 (UB 0.00374); bias ratio 0.957, 0.087 nats | `12_g1_analysis.json`, `12_g2_analysis.json` bias_check (2.0261 − 1.9396 = 0.0865) | Match |
| 12 | Appendix A R5a/R5b/R5c thresholds and per-seed deficits; seed 503 exactly at −δ | `12_d3_analysis*.json`; threshold recomputed −0.04 + 1.645·SE·√0.5 → −1.43 / −1.68 / −0.75 pp | Match |
| 13 | Appendix note 1: ε_S12 0.314266 in D3 files vs 0.314507 current | `12_d3_analysis.json` vs `12_g5_analysis.json` S12 eps_c | Match |
| 14 | H2: Δ +0.00023, bounds [−0.3103, +0.3034], p_greater 0.4883; SE ≈ 0.19, pass needs Δ > 0.41, 80 % power at about 0.57 | `14_h2_analysis.json`; arithmetic (0.31/1.645; 0.10 + 2.485·0.19) | Match |
| 15 | Teacher tie fraction 0.0 in 210 evaluations "so exact ties in G\*'s scores do not depress top-1" | `touchbed/distill.py` `regret()`: tie := s_max − s_med < ρ·s_max | **Mismatch in description**: the number matches, the meaning does not |
| 16 | Runtime "Python 3.12.15, numpy 2.5.4" for everything | `env` in `d3rem/*.json`, `d3long/*.json`: Python 3.13.18, numpy 2.5.3; `rl/*.json`, `test3/*.jsonl`: 3.12.15 / 2.5.4 | **Partial mismatch** (undisclosed second runtime) |
| 17 | Latency: student 0.408 ms, G\* 0.9135 s, ratio about 2,200×, components 15.0 % → ≤ 6.7×, pruned-16 3.22×, 6 configurations with CI half-width > 10 % | `12_lat_analysis` (ratio 2238.2; (0.0402 + 0.0967)/0.9135 = 0.150; ci_too_wide has 6 entries) | Match |
| 18 | Student rounds 4–16 epochs, 3.2–27.6 s, 27 rounds; RL plateau 102,400 / 102,400 / 112,640, cap 200,064 | `14_behaviour.json` student_rounds_summary; `14_h2_analysis.json` rl_training | Match |
| 19 | B-fan rows R9 (student − B-fan +2.2 pp [−2.8, +7.3], B-fan − G\* −6.7 pp [−12, −1], RL − B-fan −0.3 pp) | `14_m4_analysis.json` exploratory_b_fan | Match |
| 20 | Conclusion: "a longer-trained student (running)" | Section 5.2 and `14_m4_analysis.json` (complete: true) | **Stale text** |

## Summary of required revisions (merged)
1. Rebalance the distillation conclusion around the long-training row: abstract and conclusion should state long − G\*
   −1.7 pp [−6.8, +3.4], with held-out R̄ improved on all seeds. Fix "stayed" and the generalisation reading, and remove
   "(running)".
2. Correct the tie-fraction description (it measures flat score vectors, not argmax ties) and add a top-2 near-tie
   statistic.
3. H3: screen all feasible actions, or at least the full local neighbourhood of φ_t. Report a bias-adjusted G. Delete
   the "deeper planner" extrapolation and mention the v2 κ = 6 value.
4. Either add a travel-binding cell or retitle and reframe the paper to the stay-and-probe regime. Present C3 as a
   finding about the ball-sPCE proxy, which misorders G\* against BI.
5. Score reduced-G\* accuracy, or drop the 2,200× figure from the abstract. Disclose the second runtime. Relabel the
   post-freeze test3 rows as exploratory with test reuse noted. Cut about 30 % for length.

CRITICAL_FABRICATION: no. Items: none critical. Non-critical mismatches: (i) the teacher tie-fraction statistic is
misdescribed as testing exact ties; (ii) the student training runtime (Python 3.13.18 / numpy 2.5.3) is not disclosed;
(iii) "a longer-trained student (running)" in the Conclusion is stale; (iv) "held-out top-1 stayed at 0.503–0.530"
misstates a rise from 0.492–0.507; (v) the "pre-registered readings" label on a post-freeze test3 row.
