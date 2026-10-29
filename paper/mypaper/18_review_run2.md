# Stage 18 Peer Review (run 2): evidence audit

Paper: "Can Cost-Aware Information-Gain Touch Selection Be Amortized? Look-Ahead Headroom and Learnability under Travel Cost"
Reviewers: A (robotics significance and framing, RSS/CoRL lens) and B (methodology–evidence consistency).
Audit basis: `prompts/stage18_user.txt` (draft and evidence), plus direct inspection of `code/touchbed/*`, `code/analysis_*_v3.py`, `results/v3/**` and `docs/07_hypotheses_v3.md`.

---

## Summary of the submission

The paper takes one simulated planar tactile-localization cell (8 near-symmetric polygons, κ = 12, 4 probes) and asks two things. First, how much one-step look-ahead adds over a cost-aware ball-EIG greedy planner G\*. The answer is H3 "Hold", UB95 G(12) = 0.0221. Second, whether G\* can be amortized by DAgger distillation or by PPO into a belief-free DeepSets head. Neither learner reaches G\*. On the ball-sPCE objective (H2) the two learners do not differ: Δ = +0.0002 nats, bounds ±0.31. Everything is pre-registered, and the paper reports itself as outcome-map row 4, a characterisation with no method claim.

---

## Topic adherence (check 1)

The paper stays on topic. Two places come close to presenting the environment or instruments as contributions:
- **C4** ("evaluator grid resolution moves success outcomes"; latency split). The grid-resolution note is an evaluator-validation problem: gate E′ *failed*. It is a limitation, not a contribution. The latency split is relevant, but only as a reason to withdraw H1-fb.
- **Table 1 and §4** spend a large share of the paper on gate routing: R1–R7, PENDING cells, ε provenance footnotes. Readers need this audit trail, but it belongs in an appendix. As written it pushes the scientific content into a minority of the main text.

## Length (check 4)

Every section meets the thresholds (author counts: Abstract 268, Intro 764, RW 505, Methods 1511, Protocol 1055, Results 1722; total about 6.8k). Length is not the problem. Density is: much of §4/§5 is gate bookkeeping.

---

## Reviewer A: robotics significance and framing

**Score: 3 / 10 (Reject).**

### Strengths
1. The pre-registration discipline is unusually strong. The outcome map, gate rules and fail-branch readings were frozen before the runs, and the paper reports negative results and failed gates (E′, D3 twice) without spinning them.
2. The controlled comparison is the right *kind* of experiment: same head, same action set, same episodes, only the training signal differs. Paired episodes with a crossed episode × seed bootstrap is the correct design.
3. The limitations section is candid and specific: one cell, unconverged evaluator, off-protocol RL sweep, teacher-visited held-out set.
4. The latency decomposition is clean. Assimilation plus neighbour lists take 15 % of G\*'s time, which caps any candidate-pruning speed-up at about 6.7×. The result is useful and checkable.

### Weaknesses
1. **The single cell barely exercises travel, the paper's motivating coupling.** With τ₁₂ = 4.9 and four unit-cost probes, the whole episode has 0.9 strokes of travel, i.e. at most about 13.5° of finger motion at κ = 12. I measured from `results/v3/test3/*.jsonl` that G\* travels **6.1° per episode on average**, the remedied student 1.5°, and RL 23–26° (RL buys that travel by giving up a probe: 3.0 probes). So in S12 the problem is mostly "pick an approach offset ψ near where the finger already is". The introduction's story, that greedy "may strand the finger far from the region that separates the remaining hypotheses", has almost no room to happen at this budget. A small one-step headroom (H3) is close to expected in this regime and says little about travel-coupled planning in general. The title and abstract ("under travel cost") overstate what the cell tests.
2. **A trivial heuristic matches both learned policies.** B-fan stays put and cycles ψ. It reaches 0.36 test success against the student's 0.382 (Δ +2.2 pp, ci95 [−2.8, +7.3]) and RL's 0.357. Combined with point 1, a reader can fairly conclude that the learners recovered "don't move, vary ψ" and nothing of G\*'s belief-dependent selection. The paper reports this, but only as an "exploratory" §5.4. It is central to interpreting C2/C3 and should be in the abstract.
3. **H3 was close to a foregone replication.** `docs/07_hypotheses_v3.md` §0.3 records that the previous iteration (32 × 8 action set) had already measured G(12) = 0.0146 (UB95 0.0208), and the Hold threshold was then set at UB < 0.03 (tightened from 0.05). The design document itself calls this a "low-risk replication". Pre-registering a threshold after seeing a near-identical estimate is legitimate, but the paper does not say so in §5.1 or the contributions. C1 is presented as a new measurement, and the prior estimate must be disclosed next to it.
4. **The amortization framing omits the obvious baseline: a cheaper G\*.** The latency table in `12_lat_analysis` already contains G\* variants with 125–500 particles at 4–40 ms per decision (e.g. g125_128_16 at 7.7 ms, g500_32_4 at 16.5 ms). The pre-registration even lists them as R_b candidates for H1b. Against these, the "about 2,200× cheaper" figure for the student shrinks to roughly 10–50×. No accuracy number is reported for any reduced G\*, so the reader cannot tell whether learning beats simply shrinking the filter. For a robotics audience, that comparison decides whether amortization matters at all. The 2,200× figure appears in the abstract and should not, unless it sits next to the reduced-planner baseline.
5. **No real-robot or MuJoCo-contact validation, and planar objects only.** `code/touchbed/mujoco_eval.py` exists but is not used. At an RSS/CoRL venue, a characterisation result on one simulated planar cell, with no held-out shapes, falls below the bar for significance.
6. **The novelty is incremental.** Greedy EIG/cost touch selection is established (Ottenhaus 2018, Hebert 2013). "Imitation of an information-gathering expert vs RL" has precedent (Choudhury 2017; Nguyen 2024). The new element is the controlled comparison in one cell, and its answer is "neither works, no difference detected". Without mechanism, that is a weak contribution.

### Actionable revisions (A)
- A1. Add at least one cell where travel actually binds: a larger τ at κ = 12, or κ ∈ {2, 6} with probe-matched budgets that allow more than 1 stroke of travel. Report G\* travel per episode in every cell, and the fraction of decisions where G\* moves more than one grid step.
- A2. Report test accuracy for 2–3 reduced-G\* configurations from the existing latency grid (e.g. g125_128_16, g500_32_4), and restate the latency claim as a cost–accuracy frontier: student, reduced G\*, full G\*.
- A3. Move the B-fan comparison into the abstract and §6. State plainly that both learners are statistically indistinguishable from a belief-free stay-and-fan heuristic.
- A4. Disclose the previous-iteration G(12) = 0.0146 (UB 0.0208) next to C1, and call H3 a replication on the 64 × 8 action set.
- A5. Tone the title and abstract down to the tested regime ("at a four-probe budget with ≤ 1 stroke of travel").

---

## Reviewer B: methodology–evidence consistency

**Score: 4 / 10 (Borderline reject).**

### Strengths
1. Almost every number checks out. I matched more than 40 reported values to `results_v3.json` and found no fabricated metric. The trial counts are right: 500 val3, 300/500 test3, 100 beliefs per κ, 20 bias beliefs, 3 + 3 seeds, 200,064 RL episodes.
2. The statistics are what the paper says: a crossed episode × seed percentile bootstrap, B = 10,000, one-sided 95 % (`touchbed/stats.py::crossed_bootstrap_diff`). The ci90/ci95 labels match α = 0.05/0.025 in `analysis_m4_v3.py`.
3. The method descriptions match the code. The G\* ball-EIG formula, the score-vector label, the distillation loss and σ_s rule, the regret floor, the 64 × 8 action set, the travel cost and feasibility, the D3 thresholds and the H3 ratio-of-means estimator all match (see the spot-checks).

### Weaknesses
1. **The student is barely trained, and the paper's "generalisation, not capacity" reading does not follow.** The training logs (`results/v3/d3/S_k12_hp0_s50x_r{0,1,2}.json`, `d3rem/…`) show:
   - round 0 stops after **5 epochs and about 3 s of wall time**;
   - round 2 after 7 epochs (8.6 s);
   - the remedy round 2 after 6 epochs (15 s).

   Train loss is still falling monotonically when the patience-3 / tol-0.005 rule fires on a noisy held-out R̄. Round 1 drops held-out R̄ from 0.385 to 0.22 mostly through continued optimisation, which shows round 0 had not converged. Meanwhile train top-1 is only 0.51–0.53 against held-out top-1 of 0.48–0.51, a train–held-out gap of about 0.02–0.03. A model at 52 % on its *own training labels*, with almost no generalisation gap, looks under-optimised, not generalisation-limited. The pre-registered label-fit rule (top-1 ≥ 0.50) is too lax to support the §5.2/§6 "generalisation rather than capacity" sentence. That sentence should go. The student also gets seconds of compute while RL gets about 1 h per seed (`wall_s` 2,880–4,069 s). "Only the training signal differs" is therefore not true of the *optimisation budget*.
2. **RL tuning is thin, and the chosen configuration sits at the edge of the sweep.** The sweep has 4 configs on 1 seed. Three of them vary only lr and one varies only entropy; batch and critic lr are fixed. The winner is the *largest* lr tested (1.09e-3) and wins by 0.92 nats. A winner at the grid edge by a large margin means the optimum may lie beyond the grid. The final RL policies have collapsed entropy (0.0045 at 200k episodes, `rl/S_k12_rel_cfg2_sd511.json`) and always execute exactly 3 probes. The RL arm of C2/C3 is therefore not shown to be competitive.
3. **H2 is tested on a saturating metric.** ball-sPCE is capped at log(4096) = 8.32 nats. On test3 0–499, 26 % of G\* episodes, 22 % of student episodes and 15 % of RL episodes lie within 0.05 nats of the cap (computed from `results/v3/h2/*.jsonl`). On this metric G\* (5.299) also scores *below* both learners (5.368), the opposite of the success and BI ordering. That inversion means g_T is not a faithful proxy for the task. "RL's own objective" may be a poor arbiter, and the ceiling compresses differences, which helps produce the non-detection. Report the saturation fraction, and either raise L or discuss the cap as a cause of low power.
4. **The H3 instrument checks do not validate sensitivity in-domain.**
   - (a) and (c) share the identical exact gap 0.7166450192… (`12_g1_analysis.json`). The travel-notch is the notch problem with travel added, and its own docstring says it "does not by itself show that travel creates headroom on the touchbed task". Presenting them as two independent checks is misleading.
   - The estimator over-reads the notch gap by 16 % (0.829 vs 0.717). V_LA is the max over 4–5 noisy re-estimates (`lookahead.py::lookahead_gap`), a winner's-curse upward bias.
   - The only in-domain check (b) tests false positives (gap 0). Nothing shows that the 500-particle, 128-candidate, M = 16 completion *could* detect a real touchbed gap.
   - At κ = 12 the completion's candidate subset has 22.5° angle spacing (`rung_subset(16, 8)`), coarser than the ≤ 13.5° of travel available. The reduced greedy is therefore structurally different from G\* in exactly the regime tested.

   Add an in-domain positive control, or at least discuss these issues.
5. **Some numbers are stale or under-reported where data already exist.**
   - Footnote 2 and §7 give random-row counts "n = 62 / 199 / 161 of 200". `12_g5_analysis` (sub 8) shows 162 / 199 / 197, and sub 4 shows 160 / 200 / 200. The paper matches neither.
   - [PENDING] cells for R3 random/D_c and R5c belief-student can be filled from the current JSON: S12 random 0.0754 (n = 199), D_c 0.3506; D3-B Δ̂_succ −19.9 pp, Δ̂_BI −1.01 nats on 298/500 episodes (marked incomplete).
   - [CONST?] placeholders for the PPO clip and epochs are known from the run configs: clip 0.2, 4 epochs. Python 3.12.15 and numpy 2.5.4 are recorded in every run header.
   - §7 says the teacher tie fraction "is not reported", but every distillation log records `val_tie_fraction` = 0.0 under the paper's own tie definition, so it can be reported.
6. **Pre-registered report items were dropped silently.** The §1.9 test table registers Holm-corrected reported rows (student vs BC, vs abs-frame, vs random) and a secondary TOST of student vs G\* at ±δ_c. Neither appears, and no note says they were descoped by the row-4 routing. The paper's statement "there is no correction across claims" is consistent with the pre-registration, but the Holm family should be listed as not run.
7. **Statistical power is weak overall.** Three seeds per learner with seed resampling makes every learner interval seed-dominated (RL per-seed SD of g_T is 3.3× the student's). Success CIs of ±5–7 pp at n = 300 cannot resolve the 2–4 pp differences the paper discusses. The test3 success rows use 300 episodes because sub-8 grid read-out costs 40.6 s per episode. That is an engineering limit, but it does mean C2 is underpowered.
8. **Minor issues:**
   - E′'s single counted flip is in A12 B-fan, yet Table 1 is headed "S12 unless stated" and does not say so.
   - The "finger-relative" context also includes absolute cos/sin φ_t (`relframe.rel_ctx`), and the paper should say so.
   - Adam state is re-initialised at every DAgger round (`cli3.cmd_distill3`), which is undocumented.

### Actionable revisions (B)
- B1. Retrain the students with a non-trivial optimisation budget, e.g. a fixed 50 epochs or patience on a smoothed metric. Report train/held-out loss curves, and drop the "generalisation rather than capacity" sentence unless train top-1 rises well above held-out.
- B2. Extend the RL sweep beyond lr 1.09e-3, with at least 2 seeds per config and entropy and batch variation. Report the entropy at convergence and the probe-count distribution.
- B3. Report the g_T saturation fraction per method and the G\* < learner inversion on g_T. Discuss the cap's effect on H2 power, or re-run with larger L.
- B4. Merge instrument checks (a) and (c) into one, with a note that they share the exact gap. Add an in-domain positive control for the H3 estimator, or soften C1 accordingly. Discuss the max-selection bias and the 22.5° completion grid.
- B5. Fix the stale n = 62/161 counts. Fill all [PENDING]/[CONST?] cells from the current JSON and run headers, marking incomplete rows. Report the tie fraction.
- B6. List the pre-registered but unexecuted items (Holm family, TOST, BC/abs-frame rows, R_b) with the routing reason.

---

## Verified spot-checks

| # | Claim in paper | Where checked | Verdict |
|---|---|---|---|
| 1 | 64 target angles × 8 offsets ψ ∈ {−35°,…,+35°}, \|A\| = 512; c(a) = 1 + κ\|Δφ\|/π; feasible iff c ≤ τ_rem; ends when τ_rem < 1 | `touchbed/travel.py` (`PSI_GRID`, `cost`, `TravelState`), `v3.require_v3_actions`; run headers `action_set: 64x8` | Match |
| 2 | Ball-EIG nested MC formula; G\* = argmax EIG_B/c on feasible; score vector s = max(0, EIG)/c, zero elsewhere | `touchbed/ball.py::ball_eig`, `policies_v2.py::GStar._scores/score_vector` | Match |
| 3 | Full G\* = (N, C, M) = (2000, 512, 64) | `cli3._label_loop` n_dec = 2000; `GStar(M=64)` default; latency key `g2000_512_64` | Match |
| 4 | Distillation loss CE(q) + λ·CE(onehot), q = softmax(β_T s/σ_s), uniform over argmax if σ_s < 1e-6; floored regret ρ = 0.05 | `touchbed/distill.py::soft_target, loss_and_grad, regret` | Match |
| 5 | HP selection on held-out R̄; chosen lr 1e-3, β_T 4, λ 0.5, batch 256 | `distill.HP_GRID`; `results/v3/hp/*.json` final R̄: hp0 0.3827 (lowest), hp2 0.3832, hp3 0.3872, hp1 0.4194 | Match (single seed, round 0 only) |
| 6 | Stopping: < 0.005 R̄ improvement over 3 evaluations, cap 50 | `distill.train_round`; logs show stops at 5–14 epochs, 3–15 s wall | Match, but see B-W1 (severe under-training) |
| 7 | DAgger: 1,500 label episodes, hold-out 1,200–1,499; 2 rounds × 400, β = 0.5 then 0; warm start; remedy 7,957 → 17,083 decisions | `d3/*_r0.json` n_train_episodes 1200, val 1196 decisions; shard args `beta 0.5/0.0`, 4 × 100 episodes; `--init` warm start; `14_labelfit` 7957/17083 | Match |
| 8 | Shared head: DeepSets 2 × 128 encoder, 2 × 128 head, 512 masked logits, 5-d context incl. τ_rem/τ | `relframe.RelDeepSets` (psi [F,128,128], rho [133,128,128,512]); `rel_ctx` (cos δ, sin δ, τ_rem/τ, cos φ_t, sin φ_t), τ = 4.9 in meta | Match (context also has absolute φ_t; undocumented) |
| 9 | PPO-clip, γ = 1, critic; lr 1.09e-3, ent 1.33e-4, batch 128, critic lr 1.43e-3; 200,064 episodes; plateau 102,400/102,400/112,640 | `train_v2.TrainConfigV2`; `rl/S_k12_rel_cfg2_sd51x.json` config (clip 0.2, epochs 4, plateau_stop False) | Match; clip/epochs are known, so the [CONST?] placeholders are unnecessary |
| 10 | ball-sPCE reward with L = 4095, J = 16; capped at log(L+1) = 8.32 | `gt3.py`, `train_v2._states` | Match; 15–26 % of test episodes saturate (not reported) |
| 11 | H3 estimator: C₁ = 32 incl. set-up moves, M_outer = 64, top 4 + G\* re-estimated with 4 × 64; completion N_LA = 500, 128 candidates, M = 16 | `lookahead.lookahead_gap`, `lookahead_tb.TouchbedProblem` (rung (16,8) = 128), `g2.g2_gap` (n_la = 500) | Match; V_LA = max of noisy estimates (upward bias) |
| 12 | G(κ) ratio of means, one-sided 95 % bootstrap over 100 beliefs; bias ratio 0.957; no duplicate beliefs | `analysis_g2_v3.py`; I scanned all 149 g2 shards: 320 unique keys, 0 duplicates | Match |
| 13 | Instrument checks (a) 0.829 in [0.573, 0.860]; (b) 0.00254, UB 0.00374; (c) 0.7438 vs 0.7166 | `12_g1_analysis.json`, `analysis_g1_v3.py`, `travel_notch.py` | Numbers match; (a) and (c) share the identical exact gap (not independent) |
| 14 | D3 thresholds max(−2 pp, −δ + 1.645·SE·√0.5), BI floor −0.15, seed rule | `analysis_d3_v3.py` l.52–61; recomputed −0.04 + 1.645·0.02206·0.7071 = −0.01434 | Match |
| 15 | Bootstrap: crossed episode × seed, B = 10,000, one-sided 95 %; ci95 two-sided | `stats.crossed_bootstrap_diff`; `analysis_h2_v3.py`; `analysis_m4_v3.py` α = 0.05/0.025 | Match |
| 16 | Evaluator: adaptive grid sub 8, 30 Nelder–Mead iterations, floor 1/(2·32,000), tie band [0.45, 0.55] | `gridpost.py` (refine_iters = 30, n_floor = 32000), `analysis_e_v3.py` | Match |
| 17 | B-fan: stay at φ_t, ψ cycles +5, −5, +15, …, −35; reservation c ≤ τ_rem − max(0, n\*−t−1) | `heuristics.py` FAN_CYCLE, `allowed_mask` | Match |
| 18 | Latency: student 0.408 ms, G\* 0.9135 s, components 0.040/0.097/0.717 s, ratio 2,238, full/pruned 3.22, 1,000 decisions, 253 episodes | `12_lat_analysis` | Match; reduced-G\* rows (4–40 ms) not discussed |
| 19 | τ₁₂ = 4.9 = n\* + mean unbudgeted G\* travel (0.94) | `analysis_cal_v3.py`, `12_cal_analysis.tau` | Match |
| 20 | Test3 rows (G\* 0.4267, student 0.3822, RL 0.3567, B-fan 0.36, all CIs); H2 Δ +0.00023 [−0.3103, +0.3034]; per-seed SD ratio 3.29 | `14_m4_analysis`, `14_h2_analysis`, `14_derived` | Match |
| 21 | Random-row counts "n = 62 / 199 / 161 of 200" | `12_g5_analysis` sub 8: 162 / 199 / 197; sub 4: 160 / 200 / 200 | **Mismatch (stale)** |
| 22 | Teacher tie fraction "not reported" | every `d3/*.json` log has `val_tie_fraction` = 0.0 | Data exist; should be reported |
| 23 | Travel "not reported" | computed from test3: G\* 6.1°, student 1.5°, RL 23–26°, random 38° per episode | Should be reported (central to framing) |

---

## Overall recommendation

- **Reviewer A: 3 / 10.** The tested regime does not exercise the travel coupling that motivates the paper, both learners are indistinguishable from a stay-and-fan heuristic, the H3 result replicates an estimate known before registration, and the amortization claim omits the reduced-planner baseline.
- **Reviewer B: 4 / 10.** The reporting is accurate and honest, but the student arm is under-optimised (seconds of training), the RL arm is under-tuned (winner at the sweep edge), H2 is tested on a saturating proxy that inverts the G\* ordering, and the H3 instrument checks lack an in-domain positive control.

Neither reviewer would recommend acceptance at RSS/CoRL (or NeurIPS/ICML) in the current form. The work fits a workshop as a pre-registered negative-results report.

CRITICAL_FABRICATION: no
