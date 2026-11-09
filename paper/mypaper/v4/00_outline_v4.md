# Paper outline (stage 16, v4, outcome row 4: characterisation paper, two cells)

**Venue (default until the owner decides; OWNER_TODO).** RSS 2027 Stage 1 extended abstract: ≤ 5 content pages + 1 page
of references, no supplementary. Methods complete; experiments may be preliminary. **Main body ≈ 3,400 words** (abstract
not counted), 2 tables, 2 figures. This is a stated deviation from the 9-page floors of `hard_constraints.md` §3; the
master draft may run longer and is condensed in stage 22.

**Paper type.** Pre-registered row-4 characterisation (`docs/07_hypotheses_v3.md` §5) with the v4 S2 cell and E5 added as
exploratory evidence (`docs/07c_amendment_v4_0.md`). No method claim. v4 changes no v3 verdict.

**Base.** v3 outline (`paper/mypaper/v3/00_outline_v3.md`) and draft (`paper/mypaper/v3/draft_v3_final.md`, which already
carries the stage-19 fixes: 32-screened-action H3 scope, stay-and-probe reframing, long student, B-fan reading (b)).

**Sources (only these may supply numbers).**
- v4: `results/v4/results_v4.json`, cited `v4:<block>.<path>`; top-level blocks are literally named
  `12_d4_analysis.json`, `14_s2_analysis.json`, `14_e5_analysis.json`, `students_S2_training` (abbreviated below as
  `d4`, `s2`, `e5`, `stS2`).
- v3: `results/v3/results_v3.json`, cited `v3:<key>.<path>`.
- Binding wording: `results/v4/14_analysis.md` (pass-2 S1–S3, M1–M3, m1–m9) and the v3 rewrites still in force
  (v3 outline §0.3, as corrected in the v3 final draft).
- Citations: `cite_key` from `docs/05_knowledge_cards.json` only. **All keys named below were checked against the 60
  cards and exist. No `[CITE-MISSING]` remains.**

---

## 0. Global constraints

### 0.1 Title
**Proposed:** *Cost-Aware Information-Gain Touch Selection under Travel Cost: Look-Ahead Headroom and Learnability in a
Stay-and-Probe and a Travelling Regime*
- Declarative, regime-qualified (v3 review S1, gate weakness "title promises an answer"). No "near-optimal", no
  "Can … Be Amortized?".
- **Owner check:** 07_hypotheses_v3 §3 lets the outcome map only shorten the working title. Strict fallback: *Cost-Aware
  Information-Gain Touch Selection: Look-Ahead Headroom and the Learnability of Amortized Policies*.

### 0.2 Labels (unchanged v3 + v4)
| Claim | Label | Key |
|---|---|---|
| H1 (S12 student non-inferior) | dead at D3 (failed twice) | `v3:12_d3_analysis_rem.passes` = false |
| H1-fb | withdrawn (Lat′ ratio < 10) | `v3:12_lat_analysis.ratio_full_over_pruned16` (3.22), `.H1_fb_active` |
| H2 (S12) | rejected (non-detection) | `v3:14_h2_analysis.passes`, `.bootstrap.lower` (−0.3103) |
| H3 | Hold | `v3:12_g2_analysis.H3.region`, `.k12.ub95` (0.0221) |
| **D4 (S2)** | **FAIL → "not shown to reach G\* in S2 either"** | `v4:d4.passes` = false, `.succ.passes` = false |
| **H2-S2** | **not detected** | `v4:s2.h2.passes` = false, `.bootstrap.lower` (−0.7485) |
| **E5** | reported at logged latency, no verdict | `v4:e5.rows.*.decision_latency_median_s` |

### 0.3 Binding v4 sentences (use verbatim or tighter; never the pass-1 forms)
- **D4 + split gap (M3, m6; always together):** "The S2 student was not shown to reach G\* (val3 Δ̂_succ −2.80 pp vs
  threshold −1.46 pp; BI and per-seed clauses pass). On test3 0–299 the gap is −10.2 pp (ci95 [−16.6, −4.3]); it is wider
  than on val3 for every seed (by 5.4, 11.2 and 5.7 pp), both the G\* (+3.9 pp) and student (−3.5 pp) rows move, the
  difference is ≈ 2.0 combined SE under independence (conservative given shared students), and its cause is untested."
- **S3 (travel):** "In S2 the student travels a similar amount to G\* on average (39.1° vs 46.9° per episode, test3
  0–299), unlike S12 (1.5–2.1° vs 6.1°), but its per-episode travel is only weakly correlated with G\*'s (r 0.14–0.24 by
  seed), so S2 shows the student is not confined to stay-and-probe, not that it reproduces G\*'s travel decisions."
- **S1 (B-fan):** "On S2 test3 the student exceeds B-fan on success (+8.1 pp, ci95 [+1.7, +14.7]) and BI (+0.53, ci95
  [+0.42, +0.64]); in S12 it exceeded B-fan on BI (+0.23, ci95 [+0.14, +0.31]) but not on success (+2.2 pp, ci95
  [−2.8, +7.3]), so S2 adds a success separation, exploratory, uncorrected and untested across cells."
- **S2 (G\* vs RL):** "G\* − RL success is +13.0 pp (ci95 [+6.4, +19.4]) in S2 and +7.0 pp (ci95 [+0.2, +13.7]) in S12;
  RL ends at 3 probes and travels several times G\*'s distance in both cells (2.9× in S2, about 4× in S12), so the record
  does not identify why the gap differs, and no cross-cell test of it exists."
- **M2 (H2-S2):** "H2-S2 is not detected (LB −0.749 ≤ +0.10); in exploratory terms the crossed-bootstrap point estimate
  favours RL by 0.445 nats on g_T (one-sided 95 % UB of student − RL −0.162, bootstrap p 0.0064, not pre-registered)."
- **M1 (g_T vs BI ordering):** "On seed-averaged point estimates g_T(G\*) is below both learned policies in S2 (5.40 vs
  5.53 / 5.98) and marginally in S12 (5.30 vs 5.37, with 3 of 6 S12 learner seeds below G\*); no interval exists for these
  contrasts." (S2 per-seed g_T is now in the JSON, `v4:s2.h2.per_seed_student|per_seed_rl`; every S2 learner seed is
  above 5.397. The draft may add this, still with "no interval".)
- **m2:** "On S2 test3 the student − G\* BI ci95 [−0.269, −0.094] excludes 0; on val3 the deficit is −0.105 (SE 0.039),
  with no interval computed."
- **m3:** S2 numbers are test3 0–299; S12 travel numbers are test3 0–499. Say so whenever both appear.
- **m4 (B-fan identity):** B-fan action sequences are identical across cells (per-episode check, **not yet in
  `results_v4.json`** → may be stated only after 15_decision §4.1 task 2 lands; until then only the identical travel
  1.454° in both blocks is cited).
- **m5:** "The LB (−0.749) is 0.85 nats below the threshold, about 2.9 one-sided half-widths (0.293), so the
  non-detection is not near the margin."
- **m7:** H2 bounds = 5 % / 95 % crossed-bootstrap quantiles; ci95 contrasts = 2.5 % / 97.5 %; D4 SE = SD of an episode ×
  student-seed bootstrap (`code/analysis_d4_v4.py`).
- **m8:** D4, test3, H2, E5 blocks are `complete: true`; test3 completeness excludes random (now n = 215 of 300,
  `v4:s2.test3_sub8.n_per_row.random`; the analysis's 190 is stale; the JSON value governs).
- **m9 (E5 vs pilot):** "On a different split (pilot3, n = 186 / 177, incomplete) the same configurations scored
  0.382 / 0.390 success at 18.2 / 44.1 ms, against 0.360 / 0.377 at 20.8 / 46.0 ms here; unpaired."
- **E5 reading:** "At logged median per-decision latencies of 20.8 and 46.0 ms (eval3, free runners), neither reduced
  G\* exceeds the distilled students: both are lower on BI (ci95 exclude 0) and success is unresolved." No cost ratio.

### 0.4 Never write (15_decision §4.3 + v3 §0.4)
Any method claim; "near-optimal"; "learned policy matches/beats G\*"; "distillation beats RL"; "the student imitates
G\*'s travel"; "RL scores higher on its own objective" as a verdict; "travel explains RL's deficit"; any cross-cell
comparison worded as a finding; the 0.9σ seed effect or the 21 % gap share; gap closure; any latency ratio without
"per decision" or across protocols (E5 vs Lat′); "RL is unstable"; "zero-travel heuristic"; CPU-h; infrastructure
events (RL re-run, early-stop completion) as findings.

---

## 1. Abstract (≈ 190 words, not counted)
**Goal.** State the problem (topic constraint wording), the two regimes, and the outcomes once each, in plain terms.
**Order.** (1) problem: headroom of one-step look-ahead over cost-aware greedy G\*, and amortization by distillation vs RL
on the same objective; (2) setting: identity × pose particle belief, stand-off finger, c(a) = 1 + κ|Δφ|/π; two cells,
S12 (stay-and-probe, G\* travel 6.1°/episode) and S2 (travelling, 46.9°); (3) H3: ≤ 2.2 % headroom at κ = 12 over 32
screened first actions (one-sided 95 % UB); (4) neither learner shown to reach G\* in either cell (D3 S12, D4 S2);
(5) distillation not shown better than RL on RL's objective in either cell; in S2 the student exceeds a stay-and-fan
heuristic (exploratory); (6) reduced-size G\* at 21–46 ms/decision does not exceed the students (exploratory);
(7) "pre-registered; one cell per regime; preliminary".
**Evidence links.** `v3:12_g2_analysis.k12.ub95`; `v3:14_behaviour.methods.gstar.travel_deg_mean`;
`v4:s2.behaviour.gstar.travel_deg_mean`; `v3:12_d3_analysis_rem.passes`; `v4:d4.passes`; `v3:14_h2_analysis.passes`;
`v4:s2.h2.passes`; `v4:s2.test3_sub8.diffs["student-b_fan:success"]`; `v4:e5.diffs.*`.
**Cards.** None in the abstract.

## 2. Introduction (500 words)
**Goal.** Motivate both questions, show why a travelling regime is needed, state findings once, list contributions.
1. (110 w) Active tactile localization, belief, EIG, travel cost. Cards: `petrovskaya2011global`, `hebert2013next`,
   `zheng2024bayesian`, `zheng2026bayesian`, `ottenhaus2018active`, `seminara2019active`.
2. (90 w) Depth: submodularity, travel coupling. Cards: `javdani2012efficient`, `vien2015touch`, `chen2015submodular`,
   `esfandiari2019adaptivity`.
3. (90 w) Amortization: BED policies, tactile RL, DAgger on dense scores. Cards: `foster2021deep`, `blau2022optimizing`,
   `ivanova2021implicit`, `hedman2025step`, `rainforth2024modern`, `riou2024reinforcement`, `niemann2024when`,
   `ross2011reduction`, `schulman2017proximal`, `choudhury2017adaptive`.
4. (130 w) Two regimes: S12 turned out stay-and-probe (79.3 % zero between-probe moves); S2 was added so the planner
   travels. Findings: H3 S5 sentence; D3 + D4 (S7 short + D4 sentence, test3 gap in the same sentence); H2 in both cells
   (non-detections); B-fan S1 sentence short form; E5 reading.
5. (80 w) Contributions (15_decision §4.2):
   - **C1** H3 headroom bound at κ = 12 over the screened set ("reduced greedy completion"), with κ = 0 / 2 rows.
   - **C2** learnability of the same belief-free relative head in a stay-and-probe and a travelling cell (D3 ×2, D4) with
     behavioural diagnosis.
   - **C3** distillation vs RL on RL's objective in both cells, plus the instrument-dependent ordering and the S2
     student − B-fan separation (exploratory).
   - **C4** methods note: evaluator resolution, g_T / BI disagreement about G\*, val3/test3 discrepancy.
   - **C5** cost: per-decision latency decomposition and E5 (reduced G\* at logged latency).
   - Pre-registration sentence (row 4 written before the runs).
**Evidence links.** `v3:14_behaviour.methods.gstar.frac_between_probe_moves_eq_0` (0.7934);
`v4:s2.behaviour.gstar.travel_deg_mean` (46.91); `v4:d4.succ.delta_hat` / `.threshold`;
`v4:s2.test3_sub8.diffs["student-gstar:success"]`; plus abstract keys.

## 3. Related work (280 words, three paragraphs, each ending with the gap)
1. Tactile localization / next-best touch: `petrovskaya2011global`, `koval2015pose`, `bauza2023tac2pose`, `hebert2013next`,
   `zheng2024bayesian`, `zheng2026bayesian`, `gordon2026active`, `kamtikar2026tactful`, `ottenhaus2018active`,
   `seminara2019active`. Gap: myopic selection is the norm; its headroom under travel cost and regime are rarely measured.
2. Greedy vs non-myopic: `javdani2012efficient`, `vien2015touch`, `chen2015submodular`, `esfandiari2019adaptivity`.
   Gap: guarantees assume structure travel breaks; measure headroom directly.
3. Amortized / learned active sensing: `foster2021deep`, `ivanova2021implicit`, `blau2022optimizing`, `hedman2025step`,
   `iqbal2024recursive`, `huang2026aline`, `nguyen2024amortized`, `rainforth2024modern`, `riou2021seeing`,
   `riou2024reinforcement`, `niemann2024when`, `xu2023tandem3d`, `fleer2020efficient`, `schneider2025tactile`; imitation
   of information-gathering oracles `choudhury2017adaptive`, `ross2011reduction`. Gap: planner distillation vs RL on the
   RL objective with one head, across regimes.
**Evidence links.** Cards only.

## 4. Problem and methods (800 words; technical approach, constants copied from frozen design docs)
**Goal.** Complete description of task, G\*, headroom estimator, both learners, baselines, and the two cells.
- **4.1 Task, belief, metrics (190 w).** s = (k, x, y, θ); finger on stand-off circle at φ_t; a = (φ′, ψ), 64 × 8;
  c(a) = 1 + κ|Δφ|/π; feasibility c(a) ≤ τ_rem; PF belief; success and BI equations. **Cells:** S12 = (S, κ = 12,
  τ = 4.9, n\* = 4) and S2 = (S, κ = 2, τ = 4.7, n\* = 4); τ from Cal′.
  Evidence: `v3:12_cal_analysis.tau.S_k12_nstar4`, `.tau.S_k2_nstar4` (τ 4.7, mean unbudgeted travel 0.7257 strokes),
  `v3:12_cal_analysis.verify.S_k12`.
- **4.2 G\* (110 w).** argmax EIG_B/c; (N, C, M) = (2,000, 512, 64); exported score vector s(a). Reduced configurations
  g125_512_16, g500_512_4 named here (used in E5).
- **4.3 Headroom estimator (140 w).** G(κ) definition; reduced greedy completion; CRN; 32 screened first actions;
  checks (a) notch / (b) zero-gap bank / (c) travel-notch, (a)/(c) one construction re-used from v2; bias check.
  Evidence: `v3:12_g1_analysis.a|b|c`, `v3:12_g2_analysis.bias_check.ratio` (0.9573).
- **4.4 Shared head and learners (280 w).** Belief-free finger-relative DeepSets; context incl. absolute φ_t (cos, sin);
  512 masked logits. Distillation: soft-CE to tempered scores + λ·CE to argmax; DAgger 2 rounds (β 0.5, 0). S12: remedy
  sizes, registered stopping rule (round-0 checkpoint for latency); exploratory 200-epoch student. **S2 recipe:** S12 hp 0
  reused (no new grid, deviation), fixed 200 epochs per round, last checkpoint, seeds 601–603. PPO: same head, reward
  telescoping to ball-sPCE g_T, clip 0.2, 4 epochs, v3 config 2, 200,064 episodes per seed, plateau recorded not used
  (S2 seeds 611–613). Belief-input control (S12 only).
  Evidence: `v4:stS2.s60x_r{0,1,2}.n_train_decisions|status`; `v4:s2.rl_training.61x.episodes|status|plateau_at`;
  `v3:14_h2_analysis.rl_training`; `v3:12_rl_sweep_selection.selected_cfg`. Cards: `ross2011reduction`,
  `schulman2017proximal`, `foster2021deep`.
- **4.5 Baselines (80 w).** Random (masked); B-spread, **B-fan** (travel-nearest stay-and-fan, H★ for S12), B-cov.
  Evidence: `v3:12_g5_analysis.cells.S12.H_star`.

## 5. Experimental protocol (300 words)
**Goal.** Every claim traces to a frozen rule; one gate table.
- Pre-registration: v3 freeze; amendment v4.0 written before any v4 run (D4, H2-S2, E5 readings, no remedy round).
- Splits: pilot3, val3 0–499 (D3, D4), test3 0–499 (g_T), test3 0–299 (success/BI rows, E5); paired episodes.
- Evaluator: E′ failed → sub 8 everywhere (`v3:12_e_analysis.passes`, `.counted_flips`); flip rate m3
  (`v3:12_cal_analysis.n_star_sub8.S.success_flip_rate_vs_sub4` = 0.075).
- Statistics: crossed episode × seed bootstrap B = 10,000 (`v4:s2.h2.bootstrap.n_boot`); m7 quantile note; no
  multiplicity correction; S2 test rows and E5 descriptive.
- D3/D4 rule formula; δ = 0.04 (`v4:d4.delta`, `v3:12_d3_analysis_rem.delta_S12`); S2 has no G5′ cell, so δ is borrowed
  and only the −0.15 BI floor applies.
- Table 1 placed here (rows R1–R9, §9).

## 6. Results (1,050 words)

### 6.1 H3: one-step headroom is small (180 w)
**Goal.** Answer question 1. Hold at κ = 12 (S5 sentence; G 0.0162, UB 0.0221 < 0.03); κ = 0 / 2 rows and ordering;
the κ = 2 row is the headroom evidence nearest to S2 (amendment v4.0: "H3 at κ = 2 already exists"), reported, not a
separate test (**drafting check:** confirm in `docs/07c_amendment_v3_0.md` that G2′ κ = 2 used τ = 4.7 before calling it
"the S2 cell"). 32-action scope; v2 replication; S4 bias sentence.
**Evidence.** `v3:12_g2_analysis.k12.{G,ub95,abs_gap_nats}`, `.k2.{G,ub95}` (0.0142, 0.0197), `.k0.{G,ub95}`,
`.H3["ordering_G0<=G2<=G12"]`, `.bias_check`; `v3:12_g1_analysis`. Cards: `javdani2012efficient`, `chen2015submodular`.

### 6.2 Two regimes: what the planner does (150 w)
**Goal.** Establish that S12 is stay-and-probe and S2 travels, before any learning result (m3 ranges stated).
- G\* 6.13° (S12, 0–499) vs 46.91° (S2, 0–299); probes 3.962 vs 3.873. RL 3.0 probes both cells (136.8° S2;
  23.0–25.8° S12). B-fan 1.454° both. Random 172.2° (S2).
- S3 travel sentence for the student (r 0.162 / 0.238 / 0.141; 0 identical sequences of 300).
**Evidence.** `v3:14_behaviour.methods.{gstar,student_rem_s50x,rl_*,b_fan,random}.travel_deg_mean|probes_mean`;
`v4:s2.behaviour.{gstar,student,rl,b_fan,random}`; `v4:s2.behaviour.student_vs_gstar_travel_pearson_r`,
`.student_identical_action_sequence_to_gstar`. First-action agreement and RL 900/900 probe counts: **not in JSON, not
cited** until 15_decision §4.1 task 2.

### 6.3 Learnability against G\* in both regimes (330 w)
**Goal.** Answer question 2a. Lead with the registered decisions; test3 descriptive.
1. S12 D3 first attempt and remedy (v3 values; M1 sentence); test3 S7 sentence; exploratory 200-epoch student
   (−1.7 pp, ci95 [−6.8, +3.4]) as "budget left open in S12".
2. **S2 D4** binding sentence (§0.3) with test3 gap and per-seed widening. Note the S2 recipe *was* the budget-matched
   200-epoch recipe, so the S12 budget explanation does not rescue S2 (15_decision §2.2).
3. S2 student training: val_R̄ does not improve over DAgger (0.300–0.312 at r0 → 0.298–0.322 at r2), every round at
   max_epochs, no train R̄ → label-fit rule not applicable in S2.
4. S12 label-fit/encoder sentence (weak form) and belief-input control (one sentence each).
**Evidence.** `v3:12_d3_analysis.{succ,bi,seeds_ok}`; `v3:12_d3_analysis_rem.{succ,bi,seeds_ok,passes}`;
`v3:14_m4_analysis.diffs["student-gstar:success"]`, `.exploratory_long_student["student_long-gstar:success"]`;
`v4:d4.{succ,bi,seeds_ok,passes}`; `v4:s2.test3_sub8.rows.{gstar,student}.per_seed_success`,
`.diffs["student-gstar:success|ball_info"]`; `v4:stS2.*.val_R_bar|status`; `v3:14_labelfit.groups.*`;
`v3:12_d3_analysis_belief_student`.

### 6.4 Distillation vs RL, and the instrument ordering (230 w)
**Goal.** Answer question 2b in both cells.
- S12 H2: Δ +0.0002, bounds [−0.310, +0.303] → rejected; M3 power; no TOST.
- S2 H2: M2 sentence; m5 margin.
- Success/BI on test3: S12 student − RL +2.6 pp (ci95 [−3.7, +8.8]), BI +0.289; S2 +2.8 pp (ci95 [−4.1, +9.6]), BI +0.180
  (ci95 [+0.091, +0.273]). G\* − RL: S2 sentence (§0.3).
- Ordering: M1 sentence (C4 methods observation; no mechanism).
**Evidence.** `v3:14_h2_analysis.{student_mean,rl_mean,bootstrap,g_T_gstar,per_seed_*}`; `v4:s2.h2.{student_mean,rl_mean,
bootstrap,g_T_gstar,g_T_b_fan,g_T_random,per_seed_student,per_seed_rl}`; `v3:14_m4_analysis.diffs["student-rl:*"]`,
`["gstar-rl:*"]`; `v4:s2.test3_sub8.diffs["student-rl:*"]`, `["gstar-rl:*"]`. Cards: `blau2022optimizing`,
`foster2021deep`.

### 6.5 Learned policies vs the stay-and-fan heuristic (100 w, exploratory)
S1 sentence; B-fan − G\* −18.3 pp (S2) / −6.7 pp (S12) stated as values, no cross-cell claim; RL − B-fan S12 −0.3 pp
(ci95 [−6.9, +6.3]); S2 RL − B-fan has no interval → not reported as a contrast.
**Evidence.** `v4:s2.test3_sub8.diffs["student-b_fan:*"]`, `["b_fan-gstar:*"]`;
`v3:14_m4_analysis.exploratory_b_fan.{student-b_fan,b_fan-gstar,rl-b_fan}:*`.

### 6.6 Cost: per-decision latency and reduced planners (60 w + Table 2 rows)
M5 sentence (≈ 2,200× per decision vs full G\*, not at matched accuracy); S6 pruning ceiling (state both attributions:
the components do not sum to the total; v3 gate weakness); E5 reading + m9.
**Evidence.** `v3:12_lat_analysis.{ratio_full_over_student,ratio_full_over_pruned16,methods.g2000_512_64.component_medians,
L_final}`; `v4:e5.rows.*`, `v4:e5.diffs.*`; `v3:14_rb_frontier.rows`.

## 7. Discussion and limitations (400 words)
**Discussion (150 w).** Headroom small in the cell where it was tested and at κ = 2 → greedy is a defensible teacher.
Making the planner travel (S2) did not make it learnable to non-inferiority with the budget-matched recipe; the student
moves a G\*-like amount but not when G\* moves, and beats the no-learning stay-and-fan heuristic only where staying is
costly (exploratory). The contrastive training objective ranks G\* below both learners while the grid posterior ranks
it above, so g_T is a questionable yardstick for localization (observation). Next steps as questions: student-visited
regret, more cells/seeds, a full-512 screen, Lat′ for reduced G\*. Cards: `hedman2025step`, `iqbal2024recursive`.
**Limitations (250 w, one sentence each).** (1) one cell per regime; δ borrowed for S2, no ε_c; (2) evaluator not shown
converged, test3 S2 mixes machines/pipelines; (3) val3/test3 S2 gap untested (§0.3); (4) no S2 HP grid, RL not re-tuned
for S2 (config 2 chosen on `val_v2`, edge of lr grid), 3 seeds, H2 powered only for large effects; (5) H3 scope (32
actions, reduced completion, V_LA bias unchecked); (6) latency protocol incomplete, E5 latency not Lat′; (7) random
anchor incomplete (n = 215 of 300); (8) test3 reused by exploratory rows; (9) pre-registered items not executed (Holm,
TOST, BC/abs-frame rows, R_b) with routing reason.

## 8. Conclusion (90 words)
Four clauses: small one-step headroom; neither learner shown to reach G\* in either regime; distillation not shown
better than RL on RL's objective; reduced G\* and the student trade similarly at tens of ms, nothing at matched accuracy.
Pre-registered, one cell per regime. No new numbers.

---

## 9. Every results row, mapped to results-JSON keys
Tags: DEC = pre-registered decision; GATE; REP = reported, no test; EXPL = exploratory (ci95, uncorrected); INC = incomplete.

### Table 1: gates and decisions (Section 5)
| Row | Item | Keys | Tag |
|---|---|---|---|
| R1 | Cal′ n\* and τ for S12 and S2 (τ 4.9 / 4.7) | `v3:12_cal_analysis.n_star.S`, `.tau.S_k12_nstar4`, `.tau.S_k2_nstar4`, `.verify.S_k12` | GATE |
| R2 | E′ fail → sub 8 | `v3:12_e_analysis.{mean_abs_dBI,counted_flips,passes}` | GATE |
| R3 | G5′ S12 (provisional) | `v3:12_g5_analysis.cells.S12.{gstar,random,D_c,delta_c,eps_c,passes,complete}` | GATE, INC |
| R4 | Lat′ / H1-fb withdrawn | `v3:12_lat_analysis.ratio_full_over_pruned16`, `.H1_fb_active` | DEC |
| R5a | D3 first attempt | `v3:12_d3_analysis.{succ,bi,seeds_ok,passes}` | DEC |
| R5b | D3 remedy → H1 dead | `v3:12_d3_analysis_rem.{succ,bi,seeds_ok,passes}` | DEC |
| R5c | D3-B belief input | `v3:12_d3_analysis_belief_student.{succ,bi,n_episodes,complete}` | REP, INC |
| **R5d** | **D4 S2: −0.0280 vs −0.01464 ✗; BI −0.1049 ✓; seeds −0.036 / −0.028 / −0.020 ✓ → FAIL** | `v4:d4.succ.{delta_hat,se,threshold,per_seed,student_mean,gstar_mean}`, `.bi.*`, `.seeds_ok`, `.passes` | DEC |
| R6 | H2 S12: Δ +0.00023, LB −0.3103 → rejected | `v3:14_h2_analysis.bootstrap`, `.threshold_nats`, `.passes` | DEC |
| **R6b** | **H2-S2: Δ −0.4452, LB −0.7485, UB −0.1616 → not detected** | `v4:s2.h2.bootstrap.{diff,lower,upper,p_greater,p_less}`, `.threshold_nats`, `.passes` | DEC (reverse direction EXPL) |
| R7 | H3 Hold: UB95 G(12) 0.0221; bias ratio 0.957 | `v3:12_g2_analysis.k12.ub95`, `.H3.region`, `.bias_check.ratio` | DEC |

### Table 2: test rows, two regime blocks (Section 6)
| Row | Item | Keys | Tag |
|---|---|---|---|
| R8a–c | S12 test3 0–299: G\* / student / RL success, BI, probes | `v3:14_m4_analysis.rows.{gstar,student,rl}` | REP |
| R8d–i | S12 paired diffs (student−G\*, student−RL, G\*−RL; success, BI) | `v3:14_m4_analysis.diffs[*]` | REP |
| R8j | S12 long student 0.41; −G\* −1.7 pp | `v3:14_m4_analysis.exploratory_long_student` | EXPL |
| R9 | S12 B-fan 0.36; student−B-fan, B-fan−G\*, RL−B-fan | `v3:14_m4_analysis.exploratory_b_fan.*` | EXPL |
| R8k | S12 g_T column (5.3678 / 5.3676 / G\* 5.2993 / random 2.6182) | `v3:14_h2_analysis.{student_mean,rl_mean,g_T_gstar,g_T_random}` | DEC / REP |
| **R20a–d** | **S2 test3 0–299: G\* 0.5533 / 6.6731; student 0.4511 / 6.4901; RL 0.4233 / 6.3103; B-fan 0.3700 / 5.9619; per-seed success** | `v4:s2.test3_sub8.rows.{gstar,student,rl,b_fan}` | EXPL |
| R20e | S2 random (n = 215, unpaired): 0.1256 / 3.6501 | `v4:s2.test3_sub8.random_on_available`, `.n_per_row.random` | REP, INC |
| **R21a–j** | **S2 paired diffs: student−G\*, student−RL, G\*−RL, student−B-fan, B-fan−G\* (success, BI; ci95)** | `v4:s2.test3_sub8.diffs[*]` | EXPL |
| R22 | S2 g_T column: student 5.5341, RL 5.9793, G\* 5.3972, B-fan 5.2631, random 3.5100; per seed | `v4:s2.h2.{student_mean,rl_mean,g_T_gstar,g_T_b_fan,g_T_random,per_seed_student,per_seed_rl}` | DEC / REP |
| **R23a–e** | **E5 (S12 test3 0–299): g125_512_16 0.36 / 5.9690 @ 0.02076 s; g500_512_4 0.3767 / 6.0373 @ 0.04599 s; paired with G\*, student_rem, student_long** | `v4:e5.rows.*`, `v4:e5.diffs[*]` (12 contrasts, ci95) | EXPL |

### In-text rows
| Row | Item | Keys | Tag |
|---|---|---|---|
| R10 | S12 label fit (9 students) | `v3:14_labelfit.groups.*` | DEC input |
| R11 | H3 κ = 0 / 2 / 12, frac LA ≠ G\*, ordering | `v3:12_g2_analysis.k0|k2|k12`, `.H3` | REP |
| R12 | G1′ (a)(b)(c) | `v3:12_g1_analysis.a|b|c` | GATE |
| R13 | Latency medians, component split, L_final | `v3:12_lat_analysis.methods.*`, `.L_final`, `.ratio_full_over_student` | REP |
| R14 | RL training S12 / S2 (status, plateau, episodes, final g_T, wall) | `v3:14_h2_analysis.rl_training`, `v4:s2.rl_training` | REP |
| R15 | RL sweep selection (`val_v2` deviation) | `v3:12_rl_sweep_selection.{selected_cfg,rows,validation_stream}` | REP |
| R16 | Behaviour S12 (travel, zero-move fraction, saturation) | `v3:14_behaviour.methods.*` | REP |
| R17 | Behaviour S2 (travel, probes, travel r, identical sequences) | `v4:s2.behaviour.*` | REP |
| R18 | S2 student training (val_R̄, decisions, status per round) | `v4:stS2.s60x_r{0,1,2}` | REP |
| R19 | Evaluator flip rate 0.075 | `v3:12_cal_analysis.n_star_sub8.S.success_flip_rate_vs_sub4` | REP |
| R24 | E5 vs pilot3 frontier (m9, unpaired) | `v3:14_rb_frontier.rows` | REP |

**Not in either JSON (do not cite until added):** pass-2 checks (first-action agreement, per-seed travel medians, RL
900/900 three probes, B-fan sequence identity, g125-vs-v3-B-fan episode comparison).

---

## 10. Figure plan

### Figure 1 (full width, top of page 1, ≈ 1/3 page; schematic + small JSON-drawn inset)
**Story.** Same planner, same learners, two regimes. When travel is expensive (S12) G\* stays and fans its probe offset;
when it is cheap (S2) G\* travels. In both, one-step look-ahead adds little, and neither learned policy reaches G\*.
**Visual elements.**
- **Panel A, task.** Top-down grey polygon in a dashed uncertainty box; faint ghost outlines (particle belief over
  identity × pose); stand-off circle; fingertip at φ_t; orange travel arrow to φ′ labelled "c(a) = 1 + κ|Δφ|/π"; blue probe
  arrow tilted by ψ ending at a contact marker with a normal tick.
- **Panel B, two regimes (schematic traces).** Two small copies of the circle side by side: "S12, κ = 12" with probes
  clustered at one angle (fan of blue probes, almost no orange arc) and "S2, κ = 2" with probes spread around the circle
  joined by orange arcs. Under each, the logged G\* mean travel: "6.1° / episode" (`v3:14_behaviour.methods.gstar.
  travel_deg_mean`) and "46.9° / episode" (`v4:s2.behaviour.gstar.travel_deg_mean`). Traces are illustrative, labelled
  "schematic".
- **Panel C, three selectors.** Belief → (i) G\* (EIG/c over 512 actions, argmax); (ii) one-step look-ahead (rollout tree
  completed by a reduced greedy); (iii) DeepSets head on the finger-frame touch history → 512 masked logits, with a solid
  arrow "DAgger: G\* score labels" and a dashed arrow "PPO: reward = ball-sPCE".
- **Panel D, headline inset (plotted from JSON, not generated).** Grouped bars of test3 success, two groups (S12, S2), bars
  G\* / student / RL / B-fan (hatched, "exploratory"); whiskers = paired ci95 vs G\* where available
  (`v3:14_m4_analysis.rows.*`, `.diffs["student-gstar:success"]`, `["gstar-rl:success"]`, `.exploratory_b_fan`;
  `v4:s2.test3_sub8.rows.*`, `.diffs[*]`). A tiny side strip: H3 UB95 at κ = 12 (0.0221) and κ = 2 (0.0197) vs the 0.03
  line (`v3:12_g2_analysis.k12|k2.ub95`).
- Style: flat vector, blue = information, orange = travel, greys for objects; dataviz skill for Panel D.
**Draft caption.**
> **Figure 1.** *Cost-aware touch selection in two travel regimes.* (A) A finger on a stand-off circle chooses where to
> move, paying travel cost proportional to |Δφ|, and which way to probe; the belief is a particle set over identity and
> planar pose. (B) At κ = 12 the cost-aware greedy planner G\* mostly stays and fans its probes (6.1° travel per
> episode); at κ = 2 it travels (46.9°). Traces are schematic. (C) We compare G\*, a one-step look-ahead over a reduced
> greedy completion, and one belief-free DeepSets policy trained by DAgger on G\*'s scores or by PPO on ball-sPCE.
> (D) One-step look-ahead gains ≤ 2.2 % at κ = 12 (one-sided 95 % bound), and neither learned policy was shown to
> reach G\* in either regime (test success, paired ci95; one cell per regime, preliminary; B-fan exploratory).

### Figure 2 (one column, two panels)
- (a) H3 G(κ) with [lb95, ub95] for κ ∈ {0, 2, 12}, 0.03 line (`v3:12_g2_analysis.k0|k2|k12`).
- (b) Paired-difference forest plot, two colour-coded blocks (S12 / S2): student−G\*, student−RL, G\*−RL,
  student−B-fan (success pp; BI nats on a second axis), plus Δg_T rows with one-sided bounds and the +0.10 line for both
  cells (`v3:14_m4_analysis.diffs`, `.exploratory_b_fan`, `v3:14_h2_analysis.bootstrap`, `v4:s2.test3_sub8.diffs`,
  `v4:s2.h2.bootstrap`). Caption: "descriptive except H2; uncorrected; no cross-cell test".

---

## 11. Word budget
| Section | Words |
|---|---|
| Abstract | 190 (not counted) |
| 1 Introduction | 500 |
| 2 Related work | 280 |
| 3 Problem and methods | 800 |
| 4 Experimental protocol | 300 |
| 5 Results | 1,050 |
| 6 Discussion and limitations | 400 |
| 7 Conclusion | 90 |
| **Body total** | **3,420** |

(Outline sections 2–8 = paper sections 1–7.) Appendix A (gate record) lives in the master draft only and is cut in
stage 22 for the 5-page abstract.
