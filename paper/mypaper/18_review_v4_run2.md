# Stage 18 review (v4, run 2): two strict reviewers (RSS/CoRL standard, robot learning and active perception)

**Paper:** Cost-Aware Information-Gain Touch Selection under Travel Cost: Look-Ahead Headroom and Learnability in a
Stay-and-Probe and a Travelling Regime

**CRITICAL_FABRICATION: no.**
No claimed trial count, episode count, seed set, statistical test or hyperparameter contradicts the code or the result
files. Every number I checked in Tables 1–6, Figure 1 (panel D values), the abstract, the introduction and Sections 5–8
matches `results/v3/results_v3.json` / `results/v4/results_v4.json` and the underlying files (within rounding). I
recomputed the S2 test3 sub-8 rows from the raw `results/v4/test3_sub8/*.jsonl` files and they match exactly. The
mismatches I found are minor: one wording error, one gate outcome reported as "pass" without its verification run, one
stale count, and some disclosure gaps (listed in Section 0.3). None of them is fabricated evidence.

**Scores:** Reviewer A **4/10** (borderline, leaning reject). Reviewer B **3/10** (reject).

---

## 0. Verification log (shared by both reviewers)

### 0.1 Checked and matching

| Claim (location) | Evidence | Verdict |
|---|---|---|
| H3: G(12) = 0.01624, UB95 0.0221, LB 0.01148; gap 0.0414 nats; V_LA 2.548, V_G* 2.506; frac LA≠G* 0.62; no-budget 1 (§5.1, Table 3, abstract, Fig. 1D) | 12_g2_analysis.k12 | match |
| κ=0 and κ=2 rows of Table 3 (all 8 columns each) | 12_g2_analysis.k0/k2 | match |
| κ=2 H3 row measured at S, κ=2, τ=4.7, n*=4, C1=32 (§3.1) | headers of results/v3/g2/S_k2_*.jsonl (`kappa 2.0, tau 4.7, n_star 4, C1 32, M_outer 64`) | match |
| Ordering G(0) ≤ G(2) ≤ G(12) | `ordering_G0<=G2<=G12: true` | match |
| Instrument checks: notch 0.8290 in band [0.573, 0.860]; travel-notch 0.7438 vs exact 0.7166; zero-gap bank 0.00254 (UB 0.00374), 100 beliefs | 12_g1_analysis a/b/c | match |
| Bias check 1.940 vs 2.026 nats, ratio 0.957, 20 beliefs, Hold not downgraded | 12_g2_analysis.bias_check, H3.downgraded=false | match |
| Cal′: S12 τ=4.9, 3.96 probes over 200 episodes; S2 τ=4.7, mean travel 0.7257 | 12_cal_analysis.tau / verify.S_k12 | match (but see M2 below for S2) |
| Sub-4 vs sub-8 success flip 7.5 % on 200 set-S calibration episodes | n_star_sub8.S.success_flip_rate_vs_sub4 = 0.075 | match |
| E′: 16 episodes, 1 counted flip, mean abs dBI 0.0126, max 0.0523, fail | 12_e_analysis | match |
| G5′ S12 pilot: G* 0.426 (n=500), random 0.075 (n=200), D_c 0.351, H★ = B-fan | 12_g5_analysis.cells.S12 | match |
| Lat′: full G* 0.9135 s, student 0.408 ms, ratio ≈ 2,200× (2238), full/pruned-16 = 3.22; components 0.0402 / 0.0967 / 0.7169 s; 1,000 decisions on 253 episodes; two files | 12_lat_analysis | match |
| Lat′ components do not sum to the total (0.854 vs 0.9135); pruning ceiling < 10× under either total (≈6.2–6.7×) | arithmetic | match |
| D3 first attempt: −5.87 pp (thr −1.43), BI −0.199 (thr −0.15), seeds −4.2/−8.0/−5.4 | 12_d3_analysis | match |
| D3 remedy: −4.40 pp (thr −1.68), BI −0.096 pass, seeds −4.6/−4.6/−4.0 | 12_d3_analysis_rem | match |
| D3-B belief input: 300 episodes, −20.1 pp (thr −0.75), −1.02 nats, seeds −21.7/−17.3/−21.3 | 12_d3_analysis_belief_student | match |
| D4: −2.80 pp (thr −1.46), BI −0.105 (SE 0.039) pass, seeds −3.6/−2.8/−2.0 pass, gate fail | 12_d4_analysis | match |
| D-gate threshold formula max(−2 pp, −δ + 1.645·SE·√0.5); BI −0.15 floor only in S2 | code/analysis_d4_v4.py; recomputed −0.04 + 1.645·0.02180·0.7071 = −0.01464 | match |
| D3/D4 SE = SD of an episode × student-seed bootstrap, B = 10,000 | analysis_d4_v4.boot_sd | match |
| H2 S12: Δ = +0.0002, bounds [−0.3103, +0.3034]; student 5.368, RL 5.368 | 14_h2_analysis | match |
| H2-S2: Δ = −0.4452, LB −0.7485, UB −0.1616, p 0.0064; 500 episodes, 3×3 seeds, B=10,000 | 14_s2_analysis.h2 | match |
| "LB is 0.85 nats below threshold, about 2.9 one-sided half-widths (0.293)" | (0.3033 + 0.2836)/2 = 0.293; 0.848/0.293 = 2.9 | match |
| S2 per-seed g_T: RL 5.832–6.179 above student 5.450–5.612; G* 5.397, B-fan 5.263, random 3.510 | 14_s2_analysis.h2 | match |
| S12 instrument ordering: G* 5.299 vs learners 5.368; 3 of 6 learner seeds below G* (501: 5.279; 512: 5.271; 513: 5.178) | 14_h2_analysis | match |
| g_T cap saturation: G* 5.8 %, learners 0.4–3.4 % | 14_behaviour gT_saturated_frac | match |
| Table 4 S12 (travel 6.13; 1.52/2.05/1.88; 23.02/25.76/25.65; 1.454; 38.45; probes; zero moves 79.3 %, 97.7–99.7 %, 0.0–21.9 %, 100 %, 33.0 %) | 14_behaviour | match |
| Table 4 S2 (46.91, 39.14, 136.8, 1.454, 172.2; probes 3.873, 3.926, 3.0, 4.0, 2.367) | 14_s2_analysis.behaviour | match |
| S2 student vs G* travel r = 0.162, 0.238, 0.141; 0 identical action sequences per seed | 14_s2_analysis.behaviour | match |
| RL travels 2.9× G* in S2 and about 4× in S12 | 136.8/46.9 = 2.92; ≈24.8/6.13 = 4.0 | match |
| Table 5 S12 rows and all S12 paired contrasts (ci90 and ci95) | 14_m4_analysis incl. exploratory_b_fan | match |
| Table 5 S2 rows and all S2 paired contrasts | 14_s2_analysis.test3_sub8; **recomputed from raw test3_sub8 files**: G* 0.5533/6.673, B-fan 0.37/5.962, student per seed 0.4633/0.4133/0.4767, RL 0.3967/0.42/0.4533 | match |
| Long student: −1.7 pp [−6.8, +3.4]; long − remedied +2.8 pp [−1.0, +6.7] | exploratory_long_student | match |
| S12 RL − B-fan −0.3 pp [−6.9, +6.3] | exploratory_b_fan.rl-b_fan | match |
| S2 val→test shift: per-seed widening 5.4/11.2/5.7 pp; G* +3.9 pp, student −3.5 pp; ≈2.0 combined SE | val per seed vs test per seed; √(0.0218² + 0.0312²) = 0.038; 0.074/0.038 = 1.95 | match |
| Label fit: six S12 history students train top-1 0.511–0.534, train R̄ 0.169–0.206, held-out top-1 0.483–0.507; belief students top-1 0.327–0.362, under-fit | 14_labelfit | match |
| S2 training: 2,700 episodes / 10,499 decisions at r0; 4,300 / 16,729–16,793 at r2; held-out R̄ 0.300–0.312 (r0), 0.298–0.322 (r2); every round at 200-epoch cap; train R̄ not logged | students_S2_training; results/v4/d4/*.json logs (200 entries each, only train_loss logged) | match |
| DAgger β = 0.5 (r1) then 0 (r2), 800 episodes per round per seed | results/v4/d4/S_k2_s60?_r?_*.json args | match |
| Distillation hp: Adam lr 1e-3, β_T 4, λ 0.5, batch 256, hidden 128, ρ 0.05; S2 hp index 0 reused, fixed_epochs 200 | distill.py HP_GRID[0], RHO; d4 distill_config | match (see M5 on what "batch" means) |
| PPO: clip 0.2, 4 epochs, critic, γ = 1 returns-to-go; config 2 lr 1.09e-3, ent 1.33e-4, batch 128, critic lr 1.43e-3; L = 4095, J = 16; S2 seeds 611–613; 200,064 episodes; plateau rule recorded, not used to stop (`plateau_stop: false`); plateau at 102,400 for each S2 seed | train.py; results/v4/rl/*.json; 14_s2_analysis.rl_training | match |
| PPO sweep: 4 configs, 1 seed, 50,048 episodes each, selected on val_v2; config 2 at upper edge of lr grid | 12_rl_sweep_selection | match |
| RL per-seed g_T SD ratio 3.29×; success range 7.7 vs 1.0 pp; S2 last-batch g_T 5.989–6.340 | 14_derived; rl_training | match |
| E5 (Table 6): all rows, latencies 20.8 / 46.0 ms, all 12 paired contrasts | 14_e5_analysis | match |
| Pilot frontier: n = 186/177, 0.382/0.390 success at 18.2/44.1 ms | 14_rb_frontier | match |
| Statistics: crossed episode × seed bootstrap, B = 10,000; one-sided α = 0.05 for H2, two-sided ci95 via α = 0.025 | touchbed/stats.py; analysis_*_v4.py | match |
| Holm and TOST implemented but not executed (§7) | stats.py has holm/tost; no analysis calls them | match |
| Noise σ_p = 1.0 mm, σ_n = 5°; prior box ±15 mm; orientation tolerance 5° | likelihood.py, pf.py (XY_HALF = 15), ball.py (R_TH) | match |
| Head context (cos, sin of relative angle; τ_rem/τ; cos, sin φ_t), finger-frame touch encoding | relframe.rel_ctx, rel_features | match |
| Section lengths: Abstract 244, Intro 904, Related 623, Method 1,655, Experiments 1,272, Results 2,182 words; total ≈ 7,970 | word count | all above thresholds |

### 0.2 Not verifiable from code/results (outside the allowed scope)
- That the hypotheses, thresholds and outcome map were frozen before any S12 run, and that the v4 amendment was written
  before any S2 run (needs docs/ and git history, which I was told not to read).
- That H3 "replicates the previous design iteration's estimate".

### 0.3 Mismatches and disclosure gaps found

- **M1 (wording error, §3.1).** "shape library S (K = 8 near-symmetric base/variant pairs)". In `touchbed/shapes.py:make_set_S`
  set S is 4 near-symmetric bases plus one symmetry-breaking variant of each, so K = 8 identities in **4** pairs. As
  written, the sentence reads as 8 pairs (16 shapes).
- **M2 (gate outcome without its measurement, Table 2 R1 / §1 / §3.1).** R1 reports Cal′ as "pass" for both cells, and
  §1 says the S2 budget was "recalibrated so that the planner still executes four probes". Cal′ requires G* to execute
  n* ± 0.3 probes when the budget is enforced (`analysis_cal_v3.py`). That verification was run only for S_k12 and
  A_k12: `results/v3/cal/verify_*` and `12_cal_analysis.verify` have no S_k2 entry. For S2 the only probe count is the
  post hoc test3 value of 3.873. That value would pass, but no S2 calibration run measured it. R1 should say this.
- **M3 (stale count, §4 after Table 2, §7, Table 5 PENDING, Fig. 1D note).** The paper says "215 of 300 episodes have run"
  for the S2 random anchor, and the evidence JSON (`random_on_available.n = 215`) agrees. The repository now holds
  245 distinct random episodes in `results/v4/test3_sub8/`, including ten single-episode re-runs (`*_rNN.jsonl`)
  written after the JSON. The count is out of date, not fabricated. Re-run the analysis or state the snapshot date.
- **M4 (undisclosed definition, Table 4, §5.2, Fig. 1B).** The start angle φ0 is drawn continuously from U(0, 2π)
  (`v3.state_v3`), and `TravelState.step` adds the first move onto the 5.625° grid to logged travel. So every
  policy pays an unavoidable "snap" of about 1.4° on average. This is why B-fan, with 100 % zero between-probe moves,
  logs 1.454°. The S12 headline of "6.1° per episode" therefore includes about 1.4° that no policy chooses. G*'s
  chosen S12 travel is closer to 4.7°, which makes the stay-and-probe case even stronger. The paper notes the
  identical B-fan figure but never explains it.
- **M5 (ambiguous hyperparameter, Table 1).** "batch 256" for distillation is a decisions-equivalent batch. The code
  uses `episodes per step = max(1, batch // T)`, about 64 episodes at T = 4. Say so.
- **M6 (pipeline asymmetry not named as a candidate cause, §5.3 / §7).** S2 val3 (D4) was scored inline by `eval3`
  with sub 8. All S2 test3 rows are `regrid3` re-reads of no-grid runs. §5.3 calls the cause of the val/test widening
  "untested", and §7 mentions "more than one machine and pipeline", but neither names this val-vs-test asymmetry. The
  same asymmetry exists in S12, where 281 of 331 test files are regrid3 re-reads and val/test agreed, so it is
  probably not the cause. A one-day regrid of val3 (or an inline eval3 of a test3 subset) would rule it out.

---

## Reviewer A (robot learning; amortized planning and imitation)

### Summary
The paper studies active tactile localization of planar polygons, using a joint identity × pose particle belief and a
fingertip on a stand-off circle that pays a travel cost. It asks three questions. (i) How much does one-step
look-ahead gain over cost-aware greedy EIG/cost (G*)? (ii) Can G* be amortized by a belief-free DeepSets head trained
by DAgger on G*'s score vectors, or by PPO on a contrastive ball-sPCE return? (iii) Is distillation better than RL on
RL's own objective? There are two cells, S12 (κ=12, the planner barely moves) and S2 (κ=2, the planner travels). The
answers are: headroom is small (G(12) UB 2.2 %); neither learner reaches G* (gates D3 ×2 and D4 fail); distillation
is not shown to beat RL on g_T, and in S2 RL is ahead on g_T; and reduced-size G* at 21–46 ms does not beat the
students on BI. The paper is framed as a pre-registered characterization with no method claim.

### Strengths
1. **Rigor and honesty are well above the norm.** Gates, thresholds and outcome routing are stated up front. Failed
   gates are reported as failures, exploratory rows are labelled, and limitations are extensive and specific. I
   checked more than 100 numbers against the result files and found no inflated claim (Section 0.1).
2. **A controlled comparison of training signals.** Head, action set, input and evaluator are fixed, and only the
   learning signal changes (dense 512-way G* score labels vs telescoped contrastive return). This is the right
   design for the question "distill or RL?".
3. **A useful methods finding.** The RL objective (g_T) ranks G* below both learners in both cells, while the grid
   posterior ranks it above, and RL collapses to exactly 3 probes. This is a concrete warning against using
   contrastive information bounds as the only yardstick for learned active-sensing policies.
4. **The second regime answers a real objection.** Adding S2 after S12 turned out to be stay-and-probe addresses the
   obvious objection that travel coupling never mattered. The behavioural diagnostics (r = 0.14–0.24, zero identical
   sequences) are a careful way to show that "travels a similar amount" is not "imitates travel decisions".
5. **Fair amortization baseline.** Comparing against reduced-size G* (E5), rather than only full G*, is the comparison
   practitioners need.

### Weaknesses
1. **Significance for RSS/CoRL is low.** Everything is planar, simulated and noise-idealized, with 8 shapes, 4 probes
   and no hardware or held-out shapes. Both main findings are negative or null: headroom is small, and learnability
   is not shown. With one cell per regime and three seeds, the null results cannot be turned into "greedy is enough"
   or "distillation does not work"; the paper says so itself.
2. **The learners are under-explored, so "not learnable" may mean "not learned here".** The S2 student reused the S12
   hyperparameters with no grid. Held-out regret did not improve across DAgger rounds (0.300–0.312 → 0.298–0.322),
   and train R̄ was not logged in S2, so under-fitting cannot be ruled out. The architecture is a single
   hidden-128 DeepSets with no belief input that works (the belief-input control is itself under-fit, top-1
   0.33–0.36). A CoRL reviewer will ask for at least one larger/attention head, a learning-rate sweep in S2, and
   train-set fit numbers before accepting a learnability conclusion.
3. **The RL comparator is degenerate.** All six PPO policies end at exactly 3 probes with near-zero entropy
   (0.002–0.013 in S12), travel 3–4× as far as G*, and were not re-tuned for S2. The selected config sits at the
   edge of the lr grid. The H2 comparison is therefore between a reasonable student and an RL policy that exploited
   a capped proxy. The paper notes this, but it weakens C3 considerably.
4. **The S2 validation/test discrepancy is unresolved and central.** The D4 gap is −2.8 pp, but the test gap is
   −10.2 pp and widens for every seed. The headline S2 learnability sentence rests on a test split that is now reused
   by many exploratory rows. See M6 for a cheap check.
5. **Evaluator resolution is comparable to the effects.** Success flips on 7.5 % of calibration episodes between
   sub 4 and sub 8, and no finer grid was checked. Several contrasts (student − B-fan +8.1 pp; E5 success) are of
   that order.
6. **Minor reporting issues:** M1, M2, M4, M5 above.

### Actionable revisions
1. Add an S2 learning-rate/width sweep (even 3–4 configs, 1 seed) and log train R̄/top-1 in S2, so the capacity vs
   generalization question can be read in the travelling cell.
2. Report regret on student-visited states (the open question in §6). It is the direct test of the covariate-shift
   story and costs only G* labelling of states already visited.
3. Either re-tune PPO in S2 or add a probe-count-matched RL variant (e.g. a penalty or constraint that prevents
   3-probe collapse), and report its success/BI. Without this, C3 compares against a broken baseline.
4. Rule out the pipeline explanation of the S2 val/test gap (M6), and give val3 BI/success intervals so the two
   splits can be compared on equal footing.
5. Fix M1 (4 pairs, K = 8), M2 (state that there is no S2 verification run, or run it), M3 (update 215 → current n,
   or date the snapshot), M4 (define travel to include the initial snap, or subtract it), M5 (define batch).
6. Shorten the contribution list. C4 and C5 are methods notes and an exploratory comparison, and presenting them as
   contributions inflates a characterization paper.

### Recommendation
**Score: 4/10 (borderline, leaning reject).** The work is careful, the claims are calibrated, and I found no
fabrication. But the evidence base (one cell per regime, three seeds, untuned S2 learners, a degenerate RL baseline,
simulation only) is too thin for a top robotics venue to accept null learnability results as a contribution. With
the revisions above, especially the S2 sweep, on-policy regret and a non-degenerate RL comparator, it would be a
solid workshop paper or a TMLR/RA-L-style negative-results paper.

---

## Reviewer B (active perception and tactile exploration)

### Summary
The paper measures whether one-step look-ahead helps over cost-aware greedy next-best-touch, and whether that greedy
planner can be replaced by a learned policy, in two travel-cost regimes on a planar simulated testbed.

### Strengths
1. A clean active-touch formulation: an ε-softened likelihood shared by all methods, a joint identity × pose
   particle belief, explicit travel cost and feasibility, and a paired-episode design with shared observation streams.
2. The H3 estimator is validated on a construction with a known gap and on a bank with zero gap, and its bias is
   checked against an independent rollout. It is also scoped honestly ("one deviating step among 32 screened
   actions", not a gap to the optimum).
3. The finding that the S12 cell is stay-and-probe (79.3 % zero moves) is reported plainly, and the paper changes
   design (S2) rather than over-interpreting S12.
4. The latency decomposition (assimilation + neighbour lists ≈ 0.14 s independent of C) is a useful, verifiable
   result. It shows that candidate pruning alone cannot reach 10×, consistent with the measured 3.22×.

### Weaknesses
1. **The headroom result is weak evidence about non-myopic planning.** Only 32 of up to 512 first actions are
   screened: G*'s own action, 3 structured moves and about 28 random ones. Completions use a reduced greedy, and the
   upward selection bias of V_LA is not measured (the notch checks over-read the exact gap by +0.11 and +0.03). A
   small G restricted to random screens says little about whether a structured travel-then-probe plan would help. In
   S12 the planner barely moves, so the coupling the paper motivates has almost no room to act. The κ=2 row is the
   relevant one, and it is descriptive only.
2. **The task is too easy and too stylized to inform real tactile exploration.** It is planar, uses a single fingertip
   on a fixed circle, 4 probes, Gaussian point and normal noise, and no contact dynamics. Real touch has object
   motion on contact, friction, sensor-specific failure modes and 3D geometry. There is no held-out-shape test and no
   hardware. The related work cites hardware systems (Tac2Pose, TANDEM3D, TactFUL) that this study does not approach.
3. **The success metric is fragile.** E′ failed, sub 8 is used without convergence evidence, and the 5 mm / 5° ball
   with near-symmetric shapes makes success hinge on posterior mass near 0.25–0.5 (cf. ball_mass ≈ 0.25 and
   identity_mass_true ≈ 0.5 in the logs). The 7.5 % flip rate is the same order as most success contrasts. BI is the
   more trustworthy metric, and the paper should lead with it.
4. **Baselines in S2 are not chosen fairly.** H★ = B-fan was selected on S12 pilot data. In S2 there is no pilot, and
   B-spread and B-cov are not run, so "the student exceeds the best heuristic in S2" is not shown. Only one
   travel-nearest heuristic, which is badly matched to a travelling regime, is beaten. The random anchor is incomplete
   (M3).
5. **Travel numbers include a fixed snap (M4).** The headline regime separation (6.1° vs 46.9°) is still clear, but
   the S12 number is inflated by about 1.4° that is not the planner's choice. Without the definition, "B-fan travels
   1.454°" reads as a contradiction of "B-fan stays".
6. **Calibration for S2 was not verified (M2)** before the test runs, although the paper reports it as passing.
7. **Too many hedges and a dense presentation.** Almost every sentence carries a qualifier, which makes the paper hard
   to read. The core message (greedy is near-sufficient one step ahead; a small history head does not match it; the
   contrastive proxy misranks policies) gets lost.

### Actionable revisions
1. Screen all feasible first actions (512) at κ = 2, at least on a subset of beliefs. Add a structured two-step "move
   then fan" candidate family. Measure V_LA selection bias, e.g. by re-estimating the selected action on fresh
   common random numbers.
2. Run the remaining heuristics (B-spread, B-cov) on S2 test3, and pre-select an S2 H★ on pilot data, before claiming
   that learning beats heuristics in the travelling regime.
3. Report BI as the primary metric. Add a sub-16 check on a subset to bound evaluator error on success.
4. Define travel precisely, and report discretionary travel (excluding the initial snap) alongside logged travel.
5. Run (or report as missing) the Cal′ verification for S2, and fix the K = 8 "pairs" wording.
6. Add at least one step toward realism: held-out shapes, a 3D or contact-dynamics variant, or a small hardware probe
   study. Otherwise the paper belongs in a venue for simulation-based methodology.
7. Consolidate the hedging into the Limitations section and state each result once in plain terms.

### Recommendation
**Score: 3/10 (reject for RSS/CoRL).** The paper is methodologically honest, and its numbers check out
(CRITICAL_FABRICATION: no). But its contributions are a narrow empirical bound on one-step headroom among randomly
screened actions, and null learnability results in two simulated planar cells with fragile success metrics and
incomplete baselines. That does not reach the significance bar of a top robotics venue.

---

## Topic adherence
The paper stays on topic: one-step headroom over cost-aware greedy, distillation vs RL, S12 vs S2. Environment issues
(free runners, a separate sandbox runtime, incomplete Lat′, machines/pipelines) appear only in Implementation and
Limitations and are not presented as contributions. C4 ("methods note") and C5 (latency) are framed as contributions,
but they come from the study itself, not from infrastructure. That framing is acceptable but inflates the
contribution list.
