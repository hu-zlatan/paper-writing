# Stage 18 Peer Review (run 1): evidence audit

Paper: "Can Cost-Aware Information-Gain Touch Selection Be Amortized? Look-Ahead Headroom and Learnability under Travel Cost"

Reviewer stance (system prompt): a balanced conference reviewer who is rigorous about whether the methods match the evidence.

---

## Summary of the submission

The paper is a pre-registered characterisation study of active tactile localization with a joint identity × planar-pose
particle belief and travel cost c(a) = 1 + κ|Δφ|/π on 512 actions. It asks two things. (H3) How much headroom does
one-step look-ahead leave over the cost-aware greedy planner G\*? (H1/H2) Can G\* be amortized by a belief-free DeepSets
head trained by DAgger distillation or by PPO on a ball-sPCE reward? All learning results come from one cell (set S,
κ = 12, n\* = 4). Headline results: UB95 G(12) = 0.0221 (Hold). The distilled student fails the D3 non-inferiority gate
(−4.40 pp against −1.68 pp). RL trails G\* by 7.0 pp on test. H2 is rejected (Δg_T = +0.0002 nats, LB −0.31). Per
decision, the student is about 2,200× faster than full G\*. H1-fb was withdrawn because the latency split caps pruning
at about 6.7×.

---

## Reviewer A (methodology and evidence consistency)

### Strengths
1. **Unusually high agreement between the numbers and the results files.** Every headline number I checked in
   Tables 1, 2a, 2b and 2c matches `results/v3/results_v3.json` and the per-analysis JSONs to the stated precision
   (see "Verified spot-checks"). I found no invented metric, test or trial count.
2. **The statistical machinery matches the claims.** The paper claims a crossed episode × seed bootstrap with
   B = 10,000, one-sided 95 % bounds and no multiplicity correction. `touchbed/stats.py::crossed_bootstrap_diff` and
   `analysis_h2_v3.py`, `analysis_m4_v3.py`, `analysis_d3_v3.py` and `analysis_g2_v3.py` do exactly that. TOST and
   Holm exist in the code, and the paper correctly says they were not used for H2. The paper claims no ANOVA or
   t-test it did not run.
3. **The gate logic is reproducible.** For example, the D3 thresholds −0.014345 (first attempt) and −0.016806
   (remedy) follow exactly from −δ + 1.645·SE·√0.5 with the stored SEs. The H3 region logic in `analysis_g2_v3.py`
   (Kill takes precedence over Hold, plus the bias-ratio guard) matches §4 and the frozen `docs/07_hypotheses_v3.md`
   (lines 381–393, 412–415).
4. **Negative results are reported honestly.** H2 is called a non-detection, not equivalence, with an explicit power
   statement. Gap closure is withheld by rule. The flat-task clause is dropped because the evidence contradicts it.
   The off-protocol RL sweep is disclosed in Limitations.

### Weaknesses
1. **The H3 headline claim says more than the estimator measures.** The abstract and §5.1 say "one-step rollout gains
   ≤ 2.2 % of the remaining expected ball information". The estimator (`touchbed/lookahead.py::lookahead_gap`,
   C1 = 32) screens only G\*'s action, three structured set-up moves and random actions up to 32 candidates out of as
   many as 512 feasible ones (about 6 %), and then re-estimates the top 4. G(κ) is therefore a lower bound on the
   one-step-deviation headroom over a random subset of first actions, and the UB95 bounds that quantity, not the
   best one-step deviation. Instrument checks (a) and (c) do not cover this gap. In every notch and travel-notch run
   the winning action is the structured set-up move (action 71 is always `candidates[1]`; `a_la` = 71 in all 5 v2 (a)
   runs). So the checks show the estimator can find a gap when the right move is in the structured list, not when it
   must be found by random screening. The paper needs to state this scope in the abstract and in C1, or add a
   full-512 screen on a subset of beliefs.
2. **(a) and (c) are not independent instrument checks.** By construction (`touchbed/travel_notch.py` docstring), the
   travel-notch is the notch problem with its actions placed on the circle. Both report the identical exact gap
   0.7166450192088315. The paper already says (a) and (b) are byte-identical to v2 (`results/v2/12_g1_analysis.json`,
   confirmed), so all three checks rest on one construction. "Three instrument checks" overstates the validation.
3. **The direction of the bias check is unguarded.** The pre-registered guard only catches over-reading of V_G\*
   (ratio > 1.02). The measured ratio, 0.957, means a 4.3 % under-reading (0.087 nats). That is about twice the
   κ = 12 absolute gap of 0.041 nats. The paper notes this but still treats Hold as clean. V_LA uses the same reduced
   completion and is also a max over noisy re-estimates (upward selection bias). A symmetric check on V_LA, or at
   least a bias-corrected G, is needed before "Hold" can carry the weight that C1 and §6 put on it ("a greedy teacher
   is therefore a defensible amortization target").
4. **The students barely train, and the paper does not report it.** The `results/v3/d3*/S_k12_hp0_*_r*.json` logs show
   that the pre-registered stopping rule (improvement < 0.005 over 3 evaluations) stops every student after 4–16
   epochs. Wall time per round is 3–28 s (round 0: 5 epochs, 3.2 s; remedy round 2: 6–7 epochs, about 15–18 s). By
   contrast, each RL seed trains for 200,064 episodes and 48–68 min. Combined with train top-1 of only 0.51–0.53, the
   label-fit rule's "generalisation, not capacity" verdict is weak: a 0.25 R̄ / 0.50 top-1 threshold cannot tell
   "fits" from "stopped early". The paper lists training compute as a missing pre-registered item. It must report it,
   and it should add one non-binding run with a longer patience or a fixed epoch budget.
5. **The tuning of both learners lands on the edge of the grid.** The RL sweep's selected configuration (cfg 2,
   lr 1.09e-3) is the largest learning rate in a 4-point sweep with 1 seed, won by 0.919 nats on the trainer's own
   validation stream (not val3). The distillation HP grid (`distill.py::HP_GRID`, 4 configurations, seed 501,
   round 0) picked hp0 (lr 1e-3, also the largest) with held-out R̄ 0.3827, against hp2 0.3832 and hp3 0.3872. That
   is a near tie on one seed and one round. Neither comparator is shown to be tuned, which weakens C2 and C3 ("neither
   route reached the planner"). In addition, the distillation HP grid is not described in the paper at all. §3.4 only
   says "Hyperparameters were selected on held-out floored normalised regret".
6. **The paper still contains placeholder and stale values for numbers that exist.**
   - Table 0: `[CONST?:ppo_clip_epsilon]` and `[CONST?:ppo_epochs]`. The RL run configs
     (`results/v3/rl/S_k12_rel_cfg2_sd51x.json`) give clip 0.2 and 4 epochs.
   - §4: `[CONST?:python_numpy_versions]`. The latency header gives Python 3.12.15 and numpy 2.5.4.
   - Table 1, R3: `[PENDING:...random.success]` and `[PENDING:...D_c]`. The JSON already holds provisional values
     (random 0.0754, n = 199; D_c 0.3506).
   - Table 1, R5c: D3-B is PENDING, yet partial values exist (n = 298 of 300: Δ̂_succ −19.9 pp, Δ̂_BI −1.01 nats,
     fail).
   - **Stale footnote 2 and §7:** "n = 62 / 199 / 161 of 200". `results/v3/12_g5_analysis.json` gives random
     n = 162 / 199 / 197 (S0 / S12 / A12). These numbers must be corrected.
7. **Small mismatches between the stated protocol and the code.**
   - "One pinned core" (§4). CPU affinity is set only in the v2 `main.py::cmd_latency`. The v3 path
     (`cli3.py::cmd_latency3`) does not pin. Only the thread variables are 1 (in the workflow and the header).
   - Table 1, R2 is headed "S12 unless stated", but E′ used 16 episodes across S12 and A12. The single counted flip is
     A12/B-fan, episode 1.
   - The Lat′ student timing used the round-0 checkpoint `S_k12_hp0_s501_r0.npz`, not the remedied student. Because
     the architecture is identical this is harmless, but it should be stated.
8. **RL behaviour is not diagnosed.** RL executes exactly 3.0 probes on test, and its final training entropy is 0.0045
   (`S_k12_rel_cfg2_sd511.json`). That is a collapsed, near-deterministic policy that gives up a probe for travel.
   This is the main behavioural difference from the student, and it could explain why g_T ties while BI differs, yet
   travel is "not reported". Report travel per episode and the action distribution.

### Actionable revisions (Reviewer A)
- A1. Rewrite the scope of H3/C1. State that the bound covers G\*'s action, 3 structured set-up moves and random
  actions up to 32 screened first actions, out of up to 512. Either add a full-512 screen on 20 or more beliefs, or
  remove "one-step look-ahead headroom is small" from the title and headline.
- A2. Report the student training epochs and wall time and the RL compute (Limitations already concedes this is a
  missing pre-registered item). Add a non-binding longer-training student to test the "generalisation, not capacity"
  reading.
- A3. Fill every `[CONST?]` and `[PENDING]` that the repository already supports. Fix the stale 62/199/161 counts.
  Describe the 4-configuration distillation HP grid and its near-tie.
- A4. Add a V_LA bias check, or report a bias-adjusted G. Call (a)/(b)/(c) one construction (re-used from v2) plus
  one zero-gap bank, not three independent checks.
- A5. Correct the "pinned core" statement, the E′ cell label and the latency checkpoint note.
- A6. Report RL travel and probe counts with their distribution, and the final policy entropy.

**Score (Reviewer A): 4 / 10 (Borderline, leaning reject).** The evidence is honest and traceable, but the main
positive claim (H3) is broader than the estimator supports, and the learnability conclusions rest on comparators
that are undertrained or tuned at the edge of their grids.

---

## Reviewer B (significance, novelty and presentation)

### Strengths
1. **The questions matter.** Whether myopic cost-aware selection leaves headroom under travel coupling, and whether
   dense planner labels beat RL with the same head, are practical questions for active-touch systems. The
   controlled "same head, same actions, same objective" framing of C2 and C3 is a clean design idea.
2. **Pre-registration is real and auditable.** The thresholds in the paper (H2 LB > 0.10 nats, H3 UB < 0.03 and
   Kill LB > 0.05, D3 (i)–(iii), the bias guard of 1.02) match `docs/07_hypotheses_v3.md`. The outcome-map routing
   to row 4 is applied without spin.
3. **The latency decomposition (C4) is a useful negative result.** Assimilation plus neighbour lists take 15.0 % of
   G\*'s time (0.0402 + 0.0967 of 0.9135 s), which caps any candidate-pruning scheme at about 6.7×. This explains
   cleanly why H1-fb was withdrawn, and the argument carries over to other PF-in-the-loop amortization schemes.
4. **Related work is adequate**, and the paper places itself correctly between amortized BED and imitation of
   information-gathering experts.

### Weaknesses
1. **The contribution is thin for a main-track venue.** The paper has one cell (S, κ = 12, n\* = 4), planar polygons,
   simulation only and 3 seeds. Every learning claim is a failure to reach a teacher or a non-detection. No
   alternative design shows how amortization could succeed. The paper calls its results "preliminary", which is
   accurate, and that also argues against acceptance in its current form.
2. **The comparison is under-powered by design, and the paper only states this after the fact.** H2 had about 80 %
   power only for a true Δ of about 0.57 nats, against a test threshold of 0.10. A design with 3 RL seeds, whose
   per-seed g_T SD is 0.253, could not plausibly detect the effect the hypothesis was about. The stated contribution
   C3 ("a test of distillation against RL on RL's own objective") therefore adds little.
3. **The two instruments disagree, and the paper does not resolve it.** Student − RL BI is +0.289 nats (ci95
   [+0.117, +0.465]), while g_T is tied, and G\* ranks below both learners on g_T (5.299 against 5.368) but above them
   on BI. The ordering on the paper's own reward contradicts the ordering on its evaluation metric. That calls into
   question either ball-sPCE (L = 4095, capped at 8.32 nats) as RL's objective or the grid BI. A short analysis of
   when sPCE saturates (per-episode g_T against the cap), or of the sat fraction in the RL logs (0.31), is needed
   before the H2 reading means anything.
4. **The evaluator is not converged.** E′ failed, and switching from sub 4 to sub 8 flips 7.5 % of S0 calibration
   successes. No finer grid was checked. The success differences of interest (4–7 pp) are about the same size as the
   evaluator's own flip rate. The paper discloses this, but the success-based conclusions (D3, test rows) inherit the
   uncertainty, and BI is the more trustworthy metric. A sub-16 re-read on a subset would help.
5. **Presentation.** The paper is heavy with gate codes (R1–R9, E′, Lat′, G5′, D3-B, H1-fb), so it reads like an
   internal audit log rather than a paper. A reader has to rebuild the outcome map to follow §4. The figure prompt,
   title-choice comments and placeholders must be removed. Some phrases repeat verbatim across the Abstract,
   Introduction, §5.2 and §6 ("neither learner was shown to reach G\*", "fit the teacher's training labels to the
   pre-registered criterion but fail validation").
6. **Length meets the target.** My recount gives Abstract 270, Introduction 767, Related Work 509, Method 1,516,
   Protocol 1,059, Results 1,725 and total 6,847 words, so every section is above its minimum. If anything, the
   paper is long for its content. §4 and Table 1 could be compressed, freeing space for the missing diagnostics
   (RL travel, student compute, full-action screen).
7. **The paper stays on topic.** No section drifts. The evaluator-grid note (C4) is environment and measurement
   material presented as a contribution. It is useful as a methods note but should not be listed as a contribution.

### Actionable revisions (Reviewer B)
- B1. Add at least one more cell (S0 or A12, already piloted) for the learners, or at least more RL and student seeds,
  so that H2 has meaningful power. Alternatively, re-frame H2 explicitly as a feasibility probe.
- B2. Explain the disagreement between g_T and BI (sPCE saturation analysis, per-seed RL behaviour) before reading H2.
- B3. Move the gate bookkeeping (Table 1, the routing text) to an appendix. Lead §5 with the scientific findings.
- B4. Demote "the evaluator's grid resolution moves success outcomes" from contribution to methods note, as
  `07_hypotheses_v3` §5 itself labels it.
- B5. Remove the figure prompt, the title HTML comments and all placeholders before submission.

**Score (Reviewer B): 3 / 10 (Reject).** The study is careful, and the reported numbers are honest, but its scope is
one cell, it reports mostly non-detections from under-powered comparisons, and its evaluation instruments disagree.
It is not ready for NeurIPS or ICML. With multiple cells and the diagnostics above, it could suit a workshop or a
robotics venue.

---

## Consolidated required revisions (priority order)
1. **Restrict or extend the H3 claim.** The estimator screens only 32 of up to 512 first actions, and the instrument
   checks succeed through the structured set-up move. Re-word the abstract, C1 and §5.1, or add a full-512 screen.
2. **Report and fix the training asymmetry.** Students stop after 4–16 epochs (seconds), while RL runs 200k episodes.
   Report compute, and add a longer-trained student before making the "generalisation, not capacity" claim.
   Acknowledge that both learners' tuning sits at the edge of the grid (lr 1e-3 and 1.09e-3).
3. **Remove every placeholder and stale number.** Use PPO clip 0.2 and 4 epochs, Python 3.12.15 and numpy 2.5.4, and
   the provisional G5′ random and D_c values. Report the partial D3-B result (n = 298, Δ̂_succ −19.9 pp). Correct
   "62 / 199 / 161" to 162 / 199 / 197.
4. **Address the instrument problems.** Explain why g_T and BI disagree (sPCE saturation). Add a V_LA bias check or a
   bias-adjusted G. Describe the instrument checks as one construction re-used from v2.
5. **Fix the small protocol mismatches** (no CPU pinning in v3 latency, E′ covers S12 and A12, the latency student
   checkpoint is round 0). Report RL travel and probe behaviour. Increase seeds or cells so H2 has real power.

---

## Verified spot-checks

| # | Claim in paper | Where checked | Result |
|---|---|---|---|
| 1 | Action set 64 × 8 = 512, ψ ∈ {−35°, …, +35°}, c(a) = 1 + κ\|Δφ\|/π, episode ends when τ_rem < 1 | `code/touchbed/travel.py` (N_PHI from TOUCHBED_NPHI=64, PSI_GRID, `cost`, `TravelState.done`); latency header `action_set: 64x8` | Match |
| 2 | σ_p = 1.0 mm, σ_n = 5°, ε = 10⁻³, R_s = 100 mm, 200 mm stroke | `likelihood.py::ObsModel`, `geometry.py` (RHO = 100, STROKE = 200) | Match |
| 3 | Distillation loss −Σq log π − λ log π(a\*), q = softmax(β_T s/σ_s), uniform over argmax if σ_s < 1e-6; floored regret with ρ = 0.05 | `touchbed/distill.py::soft_target`, `loss_and_grad`, `regret` | Match |
| 4 | Adam lr 1e-3, β_T 4, λ 0.5, batch 256, grad clip 1.0, no weight decay, stop < 0.005 / 3 evaluations / ≤ 50 epochs | `DistillConfig`; `nn.py::Adam` (max_grad_norm 1.0, no decay); `results/v3/hp/*_hp0_*.json` `distill_config` | Match. **Not reported in the paper:** a 4-configuration HP grid with near-tied R̄ (0.3827 vs 0.3832), and 4–16 training epochs per round |
| 5 | Shared head: DeepSets, 2 × 128 MLPs, 5-dim relative context, 512 masked logits; τ_rem/τ uses the episode budget | `relframe.py` (REL_CTX_DIM = 5, psi [F,128,128], rho [133,128,128,512]); hp JSON `tau: 4.9` | Match |
| 6 | Training data 7,957 → 17,083 decisions; held-out episodes 1,200–1,499; DAgger 400 → 800 episodes per round | `14_labelfit` and `d3/`, `d3rem/` JSONs (1,200/1,600/2,000 and 2,700/3,500/4,300 train episodes) | Match |
| 7 | PPO: γ = 1, critic, 200,064 episodes per seed, seeds 511–513, plateau at 102,400 / 102,400 / 112,640; sweep of 4 configurations × 1 seed × 50,048 episodes; cfg 2 lr 1.09e-3, entropy 1.33e-4, batch 128, critic lr 1.43e-3; margin 0.919 | `results/v3/rl/*.json`, `12_rl_sweep_selection`, `14_derived` | Match. Clip 0.2 and epochs 4 exist but appear in the paper as [CONST?] |
| 8 | ball-sPCE L = 4095, J = 16 | `train_v2.py` TrainConfig (L = 4095, J = 16) | Match |
| 9 | H2: crossed bootstrap, B = 10,000, one-sided 95 %, LB > +0.10; Δ = +0.00023, bounds [−0.3103, +0.3034], p_greater 0.4883 | `analysis_h2_v3.py`, `stats.py` (alpha 0.05 quantiles), `14_h2_analysis.json` | Match |
| 10 | D3 thresholds −1.43 / −1.68 pp, seeds −4.2/−8.0/−5.4 and −4.6/−4.6/−4.0 pp, BI −0.199 / −0.096 | `analysis_d3_v3.py` formula recomputed: −0.04 + 1.645·0.022056·√0.5 = −0.014344; −0.04 + 1.645·0.019940·√0.5 = −0.016805 | Match |
| 11 | H3: G(12) = 0.01624, UB95 0.0221 (ratio-of-means bootstrap over 100 beliefs, B = 10,000); Hold; bias ratio 0.957 | `analysis_g2_v3.py`, `12_g2_analysis.json` | Numbers match. **Scope caveat:** only C1 = 32 first actions are screened (`lookahead.py`) |
| 12 | H3 estimator: C1 = 32, M_outer 64, top 4 re-estimated × 4·64; completion with N_LA = 500, 128 candidates, M = 16 | `lookahead.py::lookahead_gap` defaults; `lookahead_tb.py` (rung (16, 8) = 128, M = 16); `g2.py` n_la = 500 | Match |
| 13 | Instrument checks (a) 0.8290 in [0.573, 0.860]; (b) 0.00254, UB 0.00374; (c) 0.7438 against exact 0.7166; (a) and (b) identical to the previous iteration | `12_g1_analysis.json`; `results/v2/12_g1_analysis.json` | Match. (a) and (c) share the same exact construction and value |
| 14 | Test3 rows: G\* 0.4267, student 0.3822, RL 0.3567; ci90/ci95 of the differences; B-fan exploratory rows | `analysis_m4_v3.py` (ci90 = alpha 0.05, ci95 = alpha 0.025), `14_m4_analysis.json` | Match |
| 15 | Latency: student 0.408 ms, G\* 0.9135 s, ratio 2,238; pruned-16 3.22×; components 15.0 % → ≤ 6.7×; 1,000 decisions, 253 episodes, 6 configurations with too-wide CIs | `12_lat_analysis.json`, `analysis_lat_v3.py`, `latency3.py` (all configurations timed on each state in rotating order) | Match. **Mismatch:** "one pinned core" is not implemented in v3 `cmd_latency3`. The student timed is the round-0 checkpoint |
| 16 | Calibration τ = 4.0 / 4.7 / 4.9, mean probes 3.96, sub 4 → 8 flip rate 7.5 % | `12_cal_analysis` | Match |
| 17 | E′: 16 episodes, mean \|ΔBI\| 0.0126, 1 counted flip, tie band [0.45, 0.55] | `analysis_e_v3.py`, `12_e_analysis` | Match. The counted flip is in A12/B-fan, not S12 (Table 1 heading) |
| 18 | Footnote 2 and §7: random rows n = 62 / 199 / 161 of 200 | `results/v3/12_g5_analysis.json` | **Mismatch:** 162 / 199 / 197 |
| 19 | Pre-registered thresholds (H2 0.10, H3 0.03 / 0.05, guard 1.02, D3 rules, G1′ bands) | `docs/07_hypotheses_v3.md` lines 200, 343, 381–393, 412–415 | Match |
| 20 | Section word counts (Abstract 268, total 6,817) | Recounted by whitespace tokens with HTML comments removed: 270 / 6,847 (headings included) | Match within heading words. Every section is above its minimum |

**Trial and episode counts.** Every count in the paper agrees with the files: 100 beliefs per κ, 20 bias beliefs,
5 notch runs, 500 val3, 300 and 500 test3, 3 seeds per learner, 1,000 latency decisions, and 200,064 RL episodes.
No trial count is inflated.

**Statistical tests.** Every test the paper uses (the crossed bootstrap, percentile bounds, the ratio-of-means
bootstrap for G, the bootstrap of the median for latency) exists in the code. TOST and Holm exist but are correctly
described as unused.

CRITICAL_FABRICATION: no
