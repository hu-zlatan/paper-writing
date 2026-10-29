# Stage 18 PEER_REVIEW — evidence audit, pass 2 (run 1)

Paper: "Can Cost-Aware Information-Gain Touch Selection Be Amortized? Look-Ahead Headroom and Learnability under Travel Cost"

The draft was judged only on the prompt's paper text and on the repository's `code/`, `results/v3/` and `docs/`.

---

## Reviewer A — methodology and evidence consistency

**Score: 4 / 10 (Borderline: significant weaknesses)**

### Summary
The paper is a pre-registered characterisation in one cell (shape set S, κ = 12, n\* = 4). It reports three things.
(i) One-step rollout headroom over the cost-aware greedy planner G\*, computed over 32 screened first actions with a reduced-greedy completion, is small (UB95 G(12) = 0.0221, Hold).
(ii) A DAgger-distilled belief-free DeepSets student failed its learnability gate D3, and PPO with the same head trails G\* on test.
(iii) H2 is rejected: no student-vs-RL difference was detected on RL's own objective g_T.
It also adds behaviour diagnostics, a latency split and two exploratory rows (B-fan, and a long-trained student).

### Strengths
- **Numbers trace to the record.** Almost every number traces exactly to `results/v3/results_v3.json` or to the per-run files. I found no inflated trial counts. Seeds (3 + 3), episode counts (val3 500, test3 300/500), bank size (100 beliefs), notch runs (5), bias beliefs (20), RL episodes (200,064) and latency decisions (1,000 on 253 episodes) all match.
- **Disclosure is unusually thorough.** The paper reports the routing to outcome row 4 and the remedy. It discloses that the earlier G(12) estimate was known before the threshold was set, and that the bias guard is one-sided. It also says the RL sweep validated on the trainer's stream rather than val3, that sub-8 rows are incomplete, and that the latency protocol is incomplete.
- **Statistics match the code.** The described statistics are the ones implemented: a crossed episode × seed bootstrap with B = 10,000 (`touchbed/stats.py`), percentile ratio-of-means bounds for H3 (`analysis_g2_v3.py`), and the D3 rule exactly as in `analysis_d3_v3.py`.
- **The exploratory readings were written before the runs.** For the B-fan row and the long-student row I verified this against `docs/07c_amendment_v3_0.md`, and the reported reading (b) follows the pre-written rule.
- **The behavioural diagnosis (Table 2d) is informative.** It shows that the cell is a stay-and-probe regime, and that RL settles on a qualitatively different three-probe strategy.

### Weaknesses
1. **Factual error: the reduced-G\* (R_b) accuracy runs exist.**
   - The paper says reduced-size G\* configurations "were timed but their accuracy was not measured". Section 4 also lists the R_b candidates among the items where "None was run".
   - The repository contradicts both statements. `results/v3/rb/` holds sub-8 pilot3 runs of all five frozen R_b candidates, as `docs/07c_amendment_v3_0.md` (Lat′ frozen note) required. Each has 155–186 of its 200 episodes.
   - Pilot success, with G\* on the same episodes in parentheses:
     - g500_512_4 (median 40 ms, about 98× the student): 0.390 (0.441)
     - g125_512_16 (20 ms, about 49×): 0.382 (0.425)
     - g500_128_16: 0.325 (0.436)
     - g500_32_64: 0.335 (0.475)
     - g125_128_64: 0.284 (0.419)
   - These are incomplete and unpaired with the val3/test3 student numbers. Even so, they bear directly on the paper's own caveat that "the record does not show whether learning beats simply shrinking the filter". A 50–100× cheaper planner appears to reach roughly the student's success level (student 0.40 on val3, 0.38 on test3).
   - The text must be corrected. The rows should be reported as provisional, or their exclusion explained.
2. **Stale or contradictory statements left from the previous revision:**
   - The Conclusion lists "a longer-trained student (running)", but Section 5.2 reports it as complete.
   - The Conclusion says "All hypotheses, thresholds and readings were fixed before the runs". The B-fan row (stage 15) and the long-student row (stage 18) were added after the test3 freeze. Their readings were written before they ran, but not before the main runs. The sentence needs that qualifier.
   - Limitations says "the per-episode latency was not measured", yet Table 2c reports L_final, the student's per-episode read-out (0.204 s). Per-episode G\* time is what is missing.
   - The teacher "tie fraction" is described as showing that "exact ties in G\*'s scores do not depress top-1". The logged statistic (`distill.regret`, `val_tie_fraction`) is the fraction of decisions with s_max − s_med < 0.05·s_max, a flat-score-vector criterion, not exact ties.
   - The pre-registered top-2 near-tie fraction ((s_max − s_(2))/s_max < 0.05, `07_hypotheses_v3` §1.6) and the noise floor are not reported. These are exactly what would decide the "near-tie" reading the paper offers for H3 (LA ≠ G\* on 62 % of beliefs) and for top-1 ≈ 0.5.
3. **The H3 instrument is thinner than the Hold label suggests.**
   - Only 32 of up to 512 first actions are screened.
   - The completion (`lookahead_tb.TouchbedProblem`, rung (16, 8)) restricts candidates to 16 target angles 22.5° apart. In a stay-and-probe regime, the completion therefore cannot "stay" whenever φ_t is off that sub-grid. It must spend part of the 0.9-unit slack moving onto it.
   - This handicap affects V_LA and V_G\* through the same completion, but it may interact with first actions that land on the sub-grid. The paper should say this and quantify it.
   - The bias reference (`bias3.py`) differs from the estimator in two ways at once: it uses a 2,000-particle PF with resample-move and a 1/N floor (3 of 20 rollouts floored). The 0.957 ratio therefore mixes a policy difference with an estimator difference.
4. **The learner comparison is confounded by optimisation budget.**
   - Student rounds ran 4–16 epochs (3.2–27.6 s). RL ran 200,064 episodes per seed.
   - The long-trained student moved success by +2.8 pp, to long − G\* = −1.7 pp with ci95 [−6.8, +3.4]. On test3 that interval includes 0.
   - The headline "neither learner was shown to reach G\*" is literally true. But read alongside the long-student row, it is weaker evidence against distillation than the abstract implies. The abstract should mention the long-student row.
5. **H2 has little power and its instrument conflicts with the grid evaluator.**
   - The test required an observed Δ > 0.41 nats. g_T orders G\* below both learners, while grid BI orders G\* above both.
   - Rejecting H2 on an instrument that mis-ranks the teacher supports little. The paper acknowledges this, but C3 still lists it as a contribution.
6. **Gate design.** The D3 success threshold max(−2 pp, −δ + 1.645·SE·√0.5) becomes stricter as SE grows. This is pre-registered and the paper applies it correctly. It should still be noted as a design choice that makes the gate fail more easily under noise.
7. **Minor points.**
   - Training decisions are 7,957/7,959 and 17,083/17,089 per seed (s503 differs).
   - "τ_rem/τ" uses τ = 4.9, which I verified in the distill JSONs (OK).
   - The distillation grid has only one config with a smaller lr. "Largest learning rate in the grid" is correct, but three of the four configs share lr 1e-3.

### Methodology–evidence discrepancies (summary)
| Claim in paper | Evidence | Status |
|---|---|---|
| Reduced-size G\* accuracy "not measured"; R_b "None was run" | `results/v3/rb/`: 5 configs × 155–186 pilot3 episodes, sub 8, with success/BI | **Contradicted: must fix** |
| Long student "(running)" in Conclusion | `14_m4_analysis.exploratory_long_student` complete (300 eps × 3 seeds) | Stale |
| Per-episode latency not measured | L_final 0.2043 s measured (student only) | Imprecise |
| Tie fraction shows "exact ties" absent | Statistic is s_max − s_med < 0.05·s_max | Mis-described |
| All readings fixed before the runs | B-fan and long-student readings written after test3 freeze | Needs qualifier |

### Actionable revisions (Reviewer A)
1. Correct the R_b statements. Report the five R_b pilot rows (provisional, n per config, G\* on the same episodes), or state exactly why they are excluded. Re-word the latency paragraph and Discussion "for practitioners" accordingly.
2. Remove the stale "(running)" and qualify "fixed before the runs". Fix the latency limitation sentence and the tie-fraction description.
3. Report the pre-registered top-2 near-tie fraction and teacher noise floor, or list them explicitly as missing pre-registered items.
4. Discuss the 16-angle completion sub-grid in the stay-and-probe regime and the estimator mismatch in the bias check.
5. Mention the long-student row in the abstract and conclusion, wherever "neither learner reached G\*" is stated.

---

## Reviewer B — significance, novelty and presentation (top-conference lens)

**Score: 3 / 10 (Reject in current form; honest but narrow negative characterisation)**

### Summary
The question is interesting: is cost-aware greedy touch selection enough, and can it be amortized? The answer, however, comes from a single cell that turned out to be degenerate for the motivating question. The planner moves the finger 6.1° per episode on average, and 79 % of its moves are zero. Travel cost therefore barely shapes behaviour, so the "under travel cost" framing in the title is not what the experiments test.

### Strengths
- **Transparent pre-registration.** The outcome map and gate record are explicit, and the paper reports the outcome row it reached instead of reframing it.
- **Careful hedging.** Statements such as "not shown to", "no difference detected; equivalence not tested" and "not at matched accuracy" are used throughout. Claims are generally no stronger than the evidence.
- **Two genuinely useful observations for practitioners:**
  - PF assimilation and neighbour lists take 15 % of G\*'s per-decision time, which caps any candidate-pruning speed-up at about 6.7×.
  - RL with a contrastive reward collapses to a deterministic three-probe strategy that trades a probe for travel.
- **Related work is adequate and positions the work correctly** relative to adaptive submodularity, DAD-style amortized BED and imitation of information-gathering experts.

### Weaknesses
1. **Topic drift between title and evidence.**
   - The title and C1 promise look-ahead headroom "under travel cost". The only tested cell is one where travel does not bind, and the paper says itself that the result "says little about regimes in which travel binds".
   - No cell where travel binds was run. The amortization question is answered for one cell with three seeds and a negative or inconclusive outcome.
   - For NeurIPS/ICML this is a workshop-level contribution.
2. **Novelty is low.**
   - Greedy cost-aware EIG is established. Small one-step headroom is expected from submodularity arguments and was already measured in the previous design iteration (G(12) = 0.0146).
   - "Distillation does not beat RL" rests on a low-power test with an instrument that mis-ranks the teacher.
   - None of the four contributions changes how someone would build a tactile localizer, except the pruning-cap observation (C4).
3. **Baselines are not shown to be competitive.**
   - Both learners' learning rates sit at the edge of four-configuration, one-seed grids.
   - The optimisation budgets are wildly unmatched.
   - The most relevant cheap baseline, a shrunken particle filter (R_b), has partial accuracy data in the repository that the paper says does not exist. That data suggests a 50–100× cheaper planner reaches the student's success range, which would undercut the "2,200× per decision" framing further.
   - B-fan, a belief-free heuristic, is statistically indistinguishable from both learners.
4. **Ablations are limited.**
   - The pre-registered BC-only, absolute-frame, Gen-κ and success-vs-probe rows were all descoped by routing.
   - The only remaining ablations are the belief-input control, which is under-fit and so isolates nothing, and the long-student row.
5. **The paper is over-length and gate-heavy.**
   - The paper's own count is 9,007 main-body words, well beyond a 9-page NeurIPS/ICML budget. Roughly 6,000–6,500 words would fit with the tables.
   - Sections 4 and 5 read as a gate log: D3 arithmetic, ε provenance notes, partial-n footnotes.
   - The paper should move the gate bookkeeping, the belief-input control and the D3 details to the appendix, and lead with a figure of behaviour (travel/probe distributions) and the headroom bound.
6. **Presentation.**
   - Contribution C1 bundles four qualifiers into one sentence.
   - The abstract (249 words) is dense with numbers. "−4.40 pp against −1.68 pp" is meaningless without the rule.
   - The Figure 1 prompt specifies a "0.91 s / decision" label. That is fine, but panel C plots G\* versus learners without the long-student bar, which is now the most informative learner row.
7. **Section lengths** (prompt's thresholds): all sections meet the minimums (Abstract 249, Intro 964, Related 587, Method 1,880, Protocol 1,064, Results 2,914). The problem is excess, not deficiency.

### Would I recommend acceptance at NeurIPS/ICML?
No. The study is honest and reproducible. But the tested regime cannot answer the motivating travel-cost question, the learnability result is inconclusive and confounded by optimisation budget, and the contribution is incremental. It fits a workshop or an RA-L short paper once a cell where travel binds is added.

### Actionable revisions (Reviewer B)
1. Either run one cell where travel binds (lower κ with a larger τ, or a higher n\*), or retitle and reframe as "a stay-and-probe regime" characterisation (the Fallback B title plus the regime qualifier).
2. Report the R_b accuracy rows and compare learners against a shrunken filter at matched latency. That is the practically relevant amortization baseline.
3. Match optimisation budgets, or at least report the student with ≥ 200 epochs as the main row. Extend both lr grids beyond the edge.
4. Cut to about 9 pages. Move the gate record, D3 arithmetic, belief-input control and provenance notes to the appendix, and make Table 2d into a figure.
5. Demote C3 (H2) to a reported observation, given the g_T/BI inversion and the 0.41-nat pass requirement.

---

## Verified spot-checks

I checked 22 claims. "✓" means the paper's claim matches the evidence.

| # | Claim in paper | Where verified | Result |
|---|---|---|---|
| 1 | σ_p = 1.0 mm, σ_n = 5°, ε = 10⁻³ | `code/touchbed/likelihood.py` ObsModel defaults | ✓ |
| 2 | 64 target angles × 8 offsets {−35…+35}, \|A\| = 512, c(a) = 1 + κ\|Δφ\|/π, episode ends at τ_rem < 1 | `code/touchbed/travel.py`; every v3 job asserts NPHI = 64 (`v3.py`) | ✓ |
| 3 | Distillation: lr 1e-3, β_T 4, λ 0.5, batch 256, stop < 0.005 over 3 evals, cap 50, last checkpoint | `touchbed/distill.py` (HP_GRID, DistillConfig, train_round) | ✓ |
| 4 | Adam, gradient-norm clip 1.0; Adam re-initialised each round | `touchbed/nn.py` Adam(max_grad_norm = 1.0); `cli3.cmd_distill3` creates new Adam per call | ✓ |
| 5 | 5-d context including absolute cos/sin φ_t; τ_rem/τ with the episode τ | `relframe.rel_ctx`; distill JSONs record tau = 4.9 | ✓ |
| 6 | Belief-input control: 48 features (8 × 6) + relative context | `distill.belief_features`, BeliefStudent MLP input BELIEF_DIM + REL_CTX_DIM | ✓ |
| 7 | PPO clip 0.2, 4 epochs, γ = 1, L = 4095, J = 16; RL cfg2 lr 1.09e-3, entropy 1.33e-4, batch 128, critic lr 1.43e-3; κ = 12, τ = 4.9, plateau recorded but not stopping | `touchbed/train_v2.py`; `results/v3/rl/S_k12_rel_cfg2_sd51{1,2,3}.json` configs | ✓ |
| 8 | Sweep: 4 configs × 50,048 episodes, 1 seed (519), selected cfg 2 by trainer val stream; margin 0.919 nats | `results/v3/rl/sweep_*`, `12_rl_sweep_selection`, `14_derived` | ✓ |
| 9 | H3 estimator: C1 = 32 (G\* action + 3 set-up moves + random), M_outer = 64, top 4 + G\* re-estimated with 4 × 64, completion N_LA = 500, 128 candidates, M = 16 | `touchbed/lookahead.py`, `lookahead_tb.py`, `g2.py` (greedy_M = 0 → M = 16) | ✓ (note: 128 = 16 φ′ × 8 ψ sub-grid) |
| 10 | Beliefs at a uniform step in {0..n\*−1}; 100 per κ; G(12) = 0.01624, UB 0.02210; Hold; bias ratio 0.957 on 20 beliefs | `g2.g2_belief`; `12_g2_analysis` | ✓ (bias reference uses a different PF estimator, `bias3.py`) |
| 11 | Crossed episode × seed bootstrap, B = 10,000, paired; ci90/ci95 via α = 0.05/0.025 | `touchbed/stats.py`, `analysis_m4_v3.py`, `analysis_h2_v3.py` | ✓ |
| 12 | D3 rule (i)–(iii) with √(500/1000) and −2 pp / −0.15 floors; thresholds −1.43/−1.68 pp; per-seed −4.2/−8.0/−5.4 and −4.6/−4.6/−4.0 pp | `analysis_d3_v3.py`; `12_d3_analysis*.json` | ✓ |
| 13 | H2: Δ = +0.00023, bounds [−0.3103, +0.3034]; pass needs Δ > 0.41; 80 % power at ≈ 0.57 (SE ≈ 0.19) | `14_h2_analysis`; arithmetic 0.10 + 0.31; 0.10 + 2.485 × 0.19 | ✓ |
| 14 | Test3 rows: G\* 0.4267, student 0.3822, RL 0.3567, B-fan 0.36, all CIs | `14_m4_analysis` | ✓ |
| 15 | Behaviour: G\* 6.1° mean travel, 79.3 % zero, 6.3 % > 1 step, 481/500 four-probe; RL exactly 3 probes; B-fan travel ≤ half grid step before first probe | `14_behaviour`; `TravelState.step` logs \|wrap\| including the first move from continuous φ0 (B-fan max 2.80° ≈ 5.625°/2) | ✓ |
| 16 | Student rounds 4–16 epochs, 3.2–27.6 s over 27 rounds | `14_behaviour.student_rounds_summary` (includes 9 belief-student rounds) | ✓ |
| 17 | Long student: from scratch (init None), fixed 200 epochs, remedied round-2 data (17,083/17,089 decisions); success 0.41; long − remedied +2.8 pp [−1.0, +6.7]; long − G\* −1.7 pp [−6.8, +3.4] | `results/v3/d3long/*.json`; `14_m4_analysis.exploratory_long_student`; readings pre-written in `07c_amendment_v3_0.md` | ✓ |
| 18 | Latency: student 0.408 ms, G\* 0.9135 s, ratio 2,238; assimilation + neighbour lists = 15.0 % → ≤ 6.7×; full/pruned-16 = 3.22 | `12_lat_analysis` (0.1369/0.9135 = 0.150) | ✓ |
| 19 | Python 3.12.15, numpy 2.5.4, BLAS threads 1 | log header of `results/v3/lat/S_k12_pilot.jsonl` | ✓ |
| 20 | Success ball 5 mm / 5°, 30 Nelder–Mead iterations, BI floor 1/(2·32,000) | `touchbed/ball.py`, `gridpost.py` estimate/readout | ✓ |
| 21 | B-fan cycle +5, −5, +15, …, −35; budget reservation max(0, n\* − t − 1) | `touchbed/heuristics.py` | ✓ |
| 22 | "Reduced-size G\* … accuracy was not measured"; R_b "None was run" | `results/v3/rb/` holds sub-8 pilot3 runs of all 5 R_b candidates (155–186/200 episodes each; success 0.284–0.390) | **✗ contradicted** |

Other checks:
- **Round-0 split:** 1,200 train + 300 held out (shards 12–14 = episodes 1,200–1,499); the remedy uses 2,700 + the same held-out shards. ✓ (`results/v3/d3/`, `d3rem/` JSONs)
- **Bootstrap direction:** the bootstrap "lower" is the α-quantile, so "one-sided 95 %" for H2/D3 is correct. ✓
- **Teacher tie fraction:** the tie statistic comes from `val_tie_fraction` (s_max − s_med < ρ·s_max), not exact ties. Mis-described in the paper.

---

## Required revisions (consolidated, priority order)
1. **R_b accuracy:** delete "accuracy was not measured" and "None was run" for R_b. Report the five partial R_b pilot rows (provisional, with n and G\* on the same episodes), or justify excluding them. Revise the 2,200× framing and the "smaller filter" discussion in light of them.
2. **Stale and inaccurate statements:** fix the Conclusion's "longer-trained student (running)"; qualify "all readings fixed before the runs"; correct the per-episode latency limitation and the tie-fraction description; report or flag the missing pre-registered top-2 near-tie fraction and teacher noise floor.
3. **Regime and title:** either add a cell where travel binds, or align the title and C1 with the stay-and-probe regime. Discuss the 16-angle completion sub-grid and the bias-check estimator mismatch as H3 instrument limits.
4. **Learner comparison:** bring the long-student row into the abstract and conclusion, and match or bound the optimisation budgets. Present H2 as a low-power observation, since g_T mis-ranks G\* relative to BI.
5. **Length:** cut the main body from about 9,000 words to a 9-page budget. Move the gate record, D3 arithmetic, provenance notes and the belief-input control to the appendix.

CRITICAL_FABRICATION: no
- Every trial, seed, episode and bootstrap count in the paper matches the code and results; no invented statistical tests or metrics.
- Non-critical factual error that must still be fixed: the claim that reduced-size G\* accuracy was "not measured" and that R_b was "not run", while partial R_b pilot accuracy data exists in `results/v3/rb/` (5 configurations, 155–186 of 200 episodes each).
- Stale internal inconsistency: "longer-trained student (running)" in the Conclusion versus the completed row in Section 5.2.
