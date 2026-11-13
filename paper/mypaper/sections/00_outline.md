<!-- Stage 16 PAPER_OUTLINE [v6], 2026-11-13; fresh-context subagent; template paper_outline.md verbatim; prompts paper/mypaper/prompts/stage16_v6_{system,user}.txt. Previous version: paper/mypaper/v5/00_outline_v5.md -->

# Paper outline (stage 16, v6): amortizing a cost-aware touch planner, a pre-registered accuracy–latency study

**Venue.** RSS 2027 Stage 1 extended abstract (deadline 2026-12-04 AoE): ≤ 5 content pages + 1 page of references.
Methods must be complete; experiments may be preliminary. **Main body target ≈ 3,350 words** (abstract not counted),
1 figure, 2 tables, plus an optional second figure that is cut first. Floors are scaled to 5 pages, a stated deviation
from the 9-page floors of `hard_constraints.md` §3. The master draft may be longer and is condensed in stage 22.

**Paper type (binding: `results/v6/15_decision.md` §1, §4.3–§4.5).** A pre-registered measurement paper with **one
narrow positive claim**: the H6b frontier, i.e. the distilled student against shrunken planners. There is no parity
claim, no method-superiority claim and no "effective component" claim. Contribution order: C1 frontier (H6b), C2 parity
not established (H6a), C3 DAgger adds nothing detectable over BC (H6c), C4 methods note (evaluator-grid sensitivity and
teacher stochasticity).

**What changes against v5** (the v5 outline and `draft_v5_final.md` are the base):
- The v5 test contrasts on episodes 0–299 are superseded by **0–499 (primary)** and **300–499 (fresh check)**.
- A second, independent G\* run (run 2) enters every student − G\* interval.
- A registered TOST at δ = 4 pp is added.
- The two reduced planners are evaluated for accuracy in all five cells (H6b).
- The round-0 (behaviour-cloning) students are evaluated (H6c).
- The evaluator-grid check E12 now covers all cells and all five student seeds, on episodes 0–99.
- The v5 D5 gate, H5a, student − H\*, RL and H5b rows become history or report-only "v6 updates of v5 rows".

**Sources (only these may supply numbers).** Key prefixes used below:
- `A:` = `results/v6/14_v6_analysis.json`. Paths are written `cells.<cell>.<window>.…`, with `<cell>` ∈ {S2, S4, S8,
  S12, A16-2} and `<window>` ∈ {0-499, 300-499}. Also `cells.<cell>.frontier.…`, `cells.<cell>.E12.…` and
  `H5b_update_0_499.…`.
- `D:` = `results/v6/15_derived_v6.json`. **Every `D:` value is printed "post hoc, no CI"**, as its `note` field requires.
- `v5:` = `results/v5/results_v5.json`, written `v5:<block> > <key> > …`. Its blocks are `14_e6_analysis.json` (latency),
  `12_d5_analysis.json` (validation gate), `12_rl_sweep_selection.json`, `12_e7_analysis.json`, `12_cal_analysis.json`,
  `12_base_hstar.json`, `13_freeze.json` and `16_report_rows.json`.
- **Analysis-derived values** (arithmetic printed in `results/v6/14_analysis.md`, Appendix A binding) are tagged
  "(derived)" and have no CI. Examples: latency ratios G\*/reduced, reduced-planner loss vs G\* run 1, ci90 half-widths,
  E12 shifts.
- **Citations:** `cite_key` values from `docs/05_knowledge_cards.json` only (60 cards; every key below was checked against
  the list). DeepSets, Holm (1979) and the bootstrap (Efron) have **no card** and stay `[CITE-MISSING]` for the
  stage-23 lookup.
- **Method constants** that no results field holds (particle counts, stand-off geometry, cost formula, label/round sizes,
  bootstrap resamples) are carried over **verbatim from `draft_v5_final.md` §3 and its provenance table**, keeping the
  provenance note there ("taken from the code and the amendments, not from a results field"). They are not new numbers
  and are not re-derived here.

---

## 0. Global constraints

### 0.1 Title
**Proposed:** *Amortizing a Cost-Aware Information-Gain Touch Planner: A Pre-Registered Accuracy–Latency Study in
TouchBED* (the frame from `15_decision.md` §4.3).
- **Fallback:** *Distilled Policy or Smaller Planner? A Pre-Registered Accuracy–Latency Study of Cost-Aware Touch
  Planning*.
- Neither title promises parity.

### 0.2 Naming map for an external reader (v5 gate weakness: "reads like an internal lab record")
Main-text names are on the left. Internal identifiers appear only in the provenance table of the appendix.

| Paper name | Internal identifier |
|---|---|
| planner G\*, runs 1 and 2 | `gstar`, `gstar2` (`--run-salt r1`) |
| reduced planners R-125 and R-500 | `g125_512_16`, `g500_512_4` (`g`N`_`C`_`M = particles, candidates scored, outcome samples; v5 draft provenance table) |
| student (DAgger round 2) / BC student (round 0) | `student_s701..705` / `r0student_s701..705` |
| RL (PPO, configuration selected on S2) | `rl_s711..715`, cfg 6 |
| success-reward RL control | `rlsucc_s711..715` (S2, S12 only) |
| primary test episodes 0–499 / fresh episodes 300–499 | test5 0–499 / 300–499 |
| evaluator-grid check | E12 (sub 8 → sub 16) |
| pilot-chosen heuristic H\* | `v5_row_updates.H_star` |

### 0.3 Labels of every decision-bearing item
| Item | Label for the paper | Key |
|---|---|---|
| H6a difference (Holm over 5) | 0 / 5 rejected, both windows | `A:cells.<cell>.<window>.holm.H6a_difference` (all false) |
| H6a TOST, δ = 4 pp (Holm over 5) | 0 / 5 rejected, both windows | `A:cells.<cell>.<window>.holm.H6a_tost` (all false); `….H6a.success.tost.{delta, p_tost}` |
| H6a verdict | "neither a difference nor equivalence shown", every cell, both windows | as above |
| H6b (Holm over 10) | 7 / 10 rejected on 0–499, all positive; 2 / 10 on 300–499 | `A:cells.<cell>.<window>.holm.{H6b_g125_512_16, H6b_g500_512_4}` |
| H6c (Holm over 5) | 0 / 5, "not detected" | `A:cells.<cell>.<window>.holm.H6c` |
| E12 | report-only | `A:cells.<cell>.E12` |
| v5 row updates (student − H\*, − RL, − rl_success, H2-v5 g_T, inversion, student − G\* run 1) | report-only, labelled "v6 update of a v5 row" | `A:cells.<cell>.<window>.v5_row_updates.*` |
| H5b update | "no trend detected over 5 cells", which is uninformative (CI spans about 26 pp per 100°) | `A:H5b_update_0_499.{slope_per_100deg, ci95_per_100deg, verdict}` |
| History: v5 validation gate D5 | failed in 5 / 5 cells | `v5:12_d5_analysis.json > H5a_validation > cells_pass` = [] |
| Completeness | 500 / 200 / 100 episodes; g_T complete | `A:cells.<cell>.<window>.{n_required, complete, gt_complete}`; `A:cells.<cell>.E12.complete` |

### 0.4 Binding sentences (from `15_decision.md` §4.4 and analysis Appendix A; use verbatim or tighter)
- **H6b (C1).** "By Holm, the student is more accurate than R-125 in all 5 cells and than R-500 in S4 and A16-2; against
  R-500 in S2/S8/S12 no accuracy difference is shown. It is 62–389× faster than both reduced planners (v5 point
  medians)." It is **always** followed by: "on the fresh 300–499 window only 2/10 contrasts survive Holm (S4 and A16-2
  vs R-125), so the fresh window replicates the direction, not the significance."
- **H6a (C2).** "The student's success point estimate is 0.3–3.7 pp below G\* in every cell on 0–499, with no registered
  difference and no registered equivalence; deficits of up to about 7–8 pp (ci95) cannot be excluded; in S4 the ci90
  lies below 0 on both windows; ball-info is significantly lower in S4 and S8." This is always paired with G\*'s
  run-to-run difference (up to 3.2 pp on 0–499, 5 pp on 300–499).
- **Upper margin.** "On 0–499 the student is not more than 4 pp better than G\* in any cell (unadjusted, per cell,
  p_upper ≤ 0.0348); on 300–499 this fails in A16-2 (p = 0.1557)."
- **Why TOST fails.** "Equivalence required |gap| ≤ 0.15–1.16 pp depending on the cell; no cell met its own threshold,
  with A16-2 closest (0.28 vs 0.15 pp)." (derived, pass 2 item 15)
- **H6c (C3).** "Round-0 (BC-only) students already reach the round-2 success level (|r2 − r0| ≤ 1.3 pp); DAgger adds no
  detectable accuracy (95 % upper bounds ≤ 4.8 pp on 0–499, ≤ 7.1 pp fresh; no equivalence test)."
- **E12 (C4).** "Changing only the read-out grid moves student − G\* by 4.6–5.0 pp in S4/S8/S12, comparable to the 4 pp
  margin; in S2 (1.6 pp) and A16-2 (0.6 pp) the shift is small." Flip rates: "4–13 % of episode outcomes in the S
  cells and 0–1 % in A16-2." It is described as *sensitivity* of the read-out (pass 2 item 19).
- **Teacher stochasticity (C4).** "First-decision agreement between two G\* runs from the same state is 0.25–0.45
  across cells and windows; no run-2 − run-1 success difference is significant."
- **Latency.** "Full G\* is about 2,500–9,800× slower per decision than the student (v5 point medians, no dispersion);
  the reduced planners are 19–47× faster than G\* and lose 4.4–14.4 pp of success against G\* run 1 (point values)."
  No physical task-time model is used.
- **Heuristics (report-only).** "The student is above the pilot-chosen H\* in all cells on 0–499 (ci95 excludes 0), but
  H\* is not the best test heuristic in S4, S8 and S12; against the best heuristic the untested point margins are about
  +4.2 / +5.1 / +2.4 pp (post hoc, no CI)."
- **RL (report-only).** "The student is significantly above the S2-tuned RL configuration in 4/5 cells on 0–499 (S8
  not) and in 3/5 on the fresh window." In A16-2 that configuration uses 2 of 3 probes in 4/5 seeds. In S2/S4 RL is
  ahead on its own objective g_T while the student is ahead on success (inversion flag true).
- **H5b.** "Slope −0.0070 per 100° (ci95 [−0.137, 0.124]); the CI spans about 26 pp, so the test is uninformative."
- **Bootstrap resolution.** A reported `p_two_sided` of 0.0 is printed "p < 1e-4" (B = 10,000).

### 0.5 Never write (`15_decision.md` §4.5 applies in full; summarised by category here)
The writer reads §4.5 itself. The categories are:
1. Any wording that the student is at, near, close to or equivalent with G\*, or that the gap is minor or costless.
2. Any wording that the student is uniformly superior to the reduced planners, or "beats the reduced planners" without
   the per-planner, per-cell Holm qualifier.
3. "Best non-oracle / best fast policy" in general (licensed in 1/5 cells only).
4. "Beats the best heuristic" without the pilot-choice qualifier.
5. That H6b replicates on fresh episodes. Only the direction replicates.
6. Any positive DAgger claim, any attribution of accuracy to BC, any DAgger/BC equivalence, or any "effective component".
7. Any travel-cost independence claim (H5b is uninformative).
8. The upper-margin result on the fresh window, or S2 BI as a finding.
9. "Noise" for the evaluator-grid result (write "sensitivity").
10. "p = 0".
11. Fresh-window numbers or latency ratios without their caveats.
12. Any hardware or real-robot claim.

Carried from v5:
- "near-optimal";
- G\* is deterministic or sub-optimal;
- G\* has success headroom;
- latency without "per decision";
- infrastructure events (time-guard stops, resumptions) as findings;
- E7 described as noise or bias of G\*'s own value estimates (v5 review item 1).

**Number homes.** Each number lives in exactly one of Table 1, Table 2, Figure 1, or its Results paragraph. The
abstract, introduction and conclusion use only the §0.4 ranges.

### 0.6 Response to the v5 review and gate (for the writer; the paper states what was and was not done)
| v5 required action | v6 status | Where |
|---|---|---|
| Evaluate the reduced planners on test in all cells; draw the frontier | done (H6b, frontier) | §4.1, Fig. 1, Table 2 |
| Restore 500 episodes; run TOST | done (0–499, δ = 4 pp) | §3, Table 1 |
| Rerun G\* with an independent seed | done (run 2) | Table 1, §4.4 |
| r0 (BC) vs deployed student on success | done (H6c) | §4.3 |
| Evaluator check in all cells and all seeds | done on episodes 0–99, G\* run 1 only | §4.4 |
| Gate-calibration discussion | superseded: TOST replaces the v5 gate; the v5 gate's clause-(i) thresholds of −1.23 to −1.72 pp are stated once in the history sentence | §1, §3 |
| Resolve [CITE-MISSING] ×3 | open (no cards) | stage 23 |
| Real Figure 1 | planned and plotted from JSON (§9) | §9 |
| Rewrite for an external reader | naming map §0.2 | all |
| Per-cell RL tuning; a cheap information heuristic; A16 at more κ; student-visited regret | **not done** (`15_decision.md` §4.1 item 3) | Limitations |

---

## 1. Abstract (≈ 170 words, not counted)
**Goal.** State the research problem in the topic's words, give the design once, and give the C1–C4 outcomes once, in
their §0.4 short forms.

**Order.**
1. **Problem (2 sentences).** A cost-aware greedy information-gain touch planner (G\*) for active tactile localization
   under travel cost is accurate but costs seconds per decision. Should one distil it into a policy, or shrink the
   planner?
2. **Design (1 sentence).**
   - A pre-registered five-cell study: travel cost κ = 2/4/8/12 on one shape library and a second library A16 at κ = 2.
   - 500 test episodes per method (200 of them fresh).
   - Two independent G\* runs, two reduced planners, BC and DAgger students (5 seeds), and an evaluator-grid check.
3. **C1.** The H6b sentence in short form, with the fresh-window qualifier.
4. **C2.** "Not shown to differ from G\*, and not shown equivalent within 4 pp". Point estimates 0.3–3.7 pp below; ~7–8 pp
   deficits not excluded.
5. **C3.** DAgger adds no detectable accuracy over BC.
6. **C4.** The read-out grid alone moves student − G\* by up to 5 pp, and two planner runs agree on only 25–45 % of first
   decisions.
7. **Scope.** "Simulation; planar shapes; preliminary."

**Evidence links.**
- `A:cells.<cell>.0-499.holm.*` and `A:cells.<cell>.300-499.holm.H6b_*`;
- `A:cells.<cell>.0-499.H6a.success.{diff, ci95}`;
- `A:cells.<cell>.0-499.H6c.success.ci95`;
- `A:cells.<cell>.E12.{student_minus_gstar_success_sub8, student_minus_gstar_success_sub16}.diff`;
- `A:cells.<cell>.<window>.gstar_first_decision_agreement_run2_vs_run1`;
- `D:cells.<cell>.latency_ratio.*` (post hoc).

**Cards.** None.

---

## 2. Introduction and related work (≈ 650 words; decision budget ~0.75 p)

### 2.1 Introduction (≈ 420 words)
**Goal.** Motivate the amortization question as a practical choice (learn a policy vs shrink the planner). Say why
parity is the wrong headline at this power. State C1–C4 once each.

1. **(100 w) Active tactile localization under travel cost.**
   - Particle belief over identity and planar pose.
   - The next touch maximises expected information gain per unit cost.
   - Every decision costs seconds of planner time.
   - Cards: `petrovskaya2011global`, `hebert2013next`, `javdani2012efficient`, `zheng2024bayesian`, `ottenhaus2018active`,
     `seminara2019active`.
2. **(100 w) Two ways to make it fast.**
   - (a) Amortize. Learn a policy, either by imitating the planner (DAgger/BC) or by policy-based experimental design
     on an information bound.
   - (b) Shrink the planner: fewer particles and samples.
   - The practitioner's question is which of the two buys more accuracy per millisecond, and whether the DAgger rounds
     matter.
   - Cards: `ross2011reduction`, `choudhury2017adaptive`, `foster2021deep`, `blau2022optimizing`, `rainforth2024modern`,
     `riou2024reinforcement`.
3. **(90 w) Why a pre-registered frontier, not a parity test.**
   - The previous round's gate against G\* failed in 5/5 cells, as did earlier single-cell gates. Its test contrasts
     could not decide (v5 review S1).
   - v6 pre-registers three families before any run: the frontier (H6b), parity with teacher variance via TOST (H6a),
     and DAgger vs BC (H6c).
   - It also adds a fresh window and an evaluator-grid check.
   - Numbers: only "5/5" (`v5:12_d5_analysis.json > H5a_validation > cells_pass` = []).
4. **(130 w) Contributions, decision order.**
   - **C1. Frontier.** The H6b sentence plus the fresh qualifier, with the latency ratios.
   - **C2. Parity not established.** H6a short form, with teacher variance included and the upper margin rejected on
     0–499.
   - **C3. DAgger.** H6c short form.
   - **C4. Methods note.** The E12 short form and the teacher-agreement range. Contrasts of a few pp in this setting
     depend on the read-out grid and on teacher stochasticity, which is a reporting lesson for amortized-BED evaluations.

**Evidence links.** The abstract keys above.

### 2.2 Related work (≈ 230 words, three short paragraphs, each ending with the gap)
1. **Tactile localization and next-best touch (80 w).**
   - Cards: `petrovskaya2011global`, `koval2015pose`, `bauza2023tac2pose`, `hebert2013next`, `zheng2024bayesian`,
     `zheng2026bayesian`, `gordon2026active`, `kamtikar2026tactful`, `ottenhaus2018active`.
   - Gap: cost-aware selection runs online, and its amortization is rarely measured against cheaper planners.
2. **Greedy information gathering (50 w).**
   - Cards: `javdani2012efficient`, `chen2015submodular`, `esfandiari2019adaptivity`, `vien2015touch`.
   - Gap: the guarantees concern the planner, not a learned copy. G\* is our reference, not an optimum.
3. **Amortized active sensing (100 w).**
   - BED policies: `foster2021deep`, `ivanova2021implicit`, `blau2022optimizing`, `hedman2025step`,
     `iqbal2024recursive`, `huang2026aline`.
   - Tactile RL: `riou2021seeing`, `riou2024reinforcement`, `niemann2024when`, `xu2023tandem3d`.
   - Imitation of information-gathering oracles: `choudhury2017adaptive`, `nguyen2024amortized`, `ross2011reduction`.
   - Gap: no pre-registered comparison of a distilled policy against reduced versions of its own teacher on an
     accuracy–latency frontier, with teacher variance and evaluator sensitivity reported.

**Evidence links.** Cards only.

---

## 3. Setup and method (≈ 650 words; decision budget ~1.0 p; a technical approach, not a workflow)
**Goal.** Give a complete, reproducible description of the task, G\*, the reduced planners, the shared head, the
BC/DAgger rounds, the RL comparator, the heuristics and the five cells.

### 3.1 Task, belief, cost, metrics (180 w)
- State (identity k, x, y, θ); stand-off circle; action (φ′, ψ).
- Action set A = 512 = 64 × 8 (`v5:16_report_rows.json > student_env` = {"64x8/A=512": 75}).
- Travel cost c(a) = 1 + κ|Δφ|/π, budget τ, probe budget n\*. Text and geometry carried from `draft_v5_final.md` §3.
- Metrics:
  - **success** (posterior read-out on the sub-8 grid, the registered evaluator);
  - **ball information BI** (nats);
  - **g_T** (ball-sPCE, the RL objective);
  - travel (rad);
  - probes.
- Libraries:
  - S: K = 8 identities, as base/variant pairs.
  - A16: K = 16 irregular asymmetric polygons. It changes family, K and n\* at once (v5 review item 6), and shares 8
    identities with the earlier library A. Description text from `draft_v5_final.md` §3.
- **Table 0 (in text): cells.**

  | Cell | κ | n\* | τ |
  |---|---|---|---|
  | S2 | 2 | 4 | 4.7 |
  | S4 | 4 | 4 | 4.8 |
  | S8 | 8 | 4 | 4.8 |
  | S12 | 12 | 4 | 4.9 |
  | A16-2 | 2 | 3 | 3.4 |

  Keys: `v5:12_cal_analysis.json > tau > {S_k4, S_k8, A16_k2} > {n_star, tau}` and `v5:12_cal_analysis.json > n_star > A16`.
  S2 and S12 τ (4.7, 4.9) are carried from the v5 Table 0 (v3 calibration, cited there).
- Cards: `petrovskaya2011global`, `koval2015pose`.

### 3.2 Planner G\* and the reduced planners (120 w)
- G\* takes the argmax of expected information gain per unit cost over the feasible candidates. Deployed as
  `g2000_512_64`; the configuration meaning is in the v5 provenance table.
- **Run-to-run stochasticity.** G\* is Monte Carlo, so v6 runs it twice with independent seeds (run 1 = v5 record plus
  the 300–499 extension; run 2 = `--run-salt r1`). Both runs enter H6a.
- **Reduced planners** R-125 (`g125_512_16`) and R-500 (`g500_512_4`) keep the 512 candidates and cut particles and
  outcome samples. Each is run once per cell.
- G\* is a reference, not an optimum.
- Cards: `javdani2012efficient`, `ottenhaus2018active`.

### 3.3 Student: shared head, BC round and DAgger rounds (200 w)
- **Head.** A belief-free, finger-frame DeepSets head over the touch history, with masked logits over A. It is the same
  head for RL. [CITE-MISSING: DeepSets (Zaheer et al. 2017)]
- **Loss.** Soft cross-entropy to tempered G\* scores plus CE to the argmax. Hyper-parameters (one setting, 75 runs):
  `v5:16_report_rows.json > student_distill_configs` (batch 256, β_T 4.0, hidden 128, λ 0.5, lr 0.001, max_epochs 200).
- **Rounds.**
  - Round 0 = behaviour cloning on G\*-visited states.
  - Rounds 1–2 = DAgger with decaying mixing.
  - Training episodes per round: 2,700 / 3,500 / 4,300 (`v5:16_report_rows.json > student_train_episodes > <cell>_s70x_r{0,1,2}`).
  - Each round keeps the checkpoint with the lowest held-out label regret R̄
    (`v5:16_report_rows.json > student_checkpoint_sensitivity > <cell> > <seed> > r{0,1,2} > {R_bar_kept, R_bar_last}`).
  - Seeds 701–705, frozen before any test episode (`v5:13_freeze.json > rule`).
  - The deployed student is round 2. The **BC student is round 0 of the same seeds**: the H6c ablation row.
  - The β schedule and label sizes are carried from the v5 provenance table.
- Cards: `ross2011reduction`, `choudhury2017adaptive`.

### 3.4 Comparators (150 w)
- **RL.**
  - PPO on the same head, with reward telescoping to g_T.
  - One configuration selected on S2 by a pre-registered rule from 8 candidates (`v5:12_rl_sweep_selection.json > {rule, selected_cfg, validation_stream}`). Single sweep seed 719 (v5 draft).
  - Reused in every cell: 200,000-episode cap, clip 0.2, 4 epochs, hidden 128 (`v5:16_report_rows.json > rl_main_cfg6 > <run> > {max_episodes, clip, epochs, hidden}`).
- **Success-reward RL control** (S2, S12). 9 of 10 runs stopped at the 80 % wall-clock guard
  (`v5:16_report_rows.json > rl_success > <run> > {status, episodes_trained}`). State it as a disclosure, not a finding.
- **Heuristics.**
  - Random, B-spread, B-fan (travel-nearest stay-and-fan) and B-cov.
  - H\* is the best of the three on a 200-episode pilot (`v5:12_base_hstar.json > {rule, cells > <cell> > H_star}`).
  - H\* is b_cov in S2 and S8, and b_fan in S4, S12 and A16-2 (`A:cells.<cell>.0-499.v5_row_updates.H_star`).
- Cards: `schulman2017proximal`, `blau2022optimizing`, `foster2021deep`.

---

## 4. Pre-registration and statistics (≈ 320 words; decision budget ~0.5 p)
**Goal.** Make every claim traceable to a frozen rule, and state the deviations.

- **Pre-registration (70 w).**
  - Amendment v6.0 (`A:amendment` = `docs/07c_amendment_v6_0.md`) plus addendum v6.1 were written before any v6
    episode. They fix the windows, H6a/H6b/H6c, δ, the Holm families and E12.
  - The read-out script was committed first, and no outcome was read before 100 % completeness (analysis §3).
  - Policies are frozen v5 weights.
- **Windows (60 w).**
  - **0–499 primary.** Episodes 0–299 were already seen in v5.
  - **300–499 fresh.**
  - Both are reported side by side.
  - 500 / 200 episodes per method (`A:cells.<cell>.<window>.{n_required, complete, gt_complete}`).
- **Tests (130 w).**
  - Paired episodes across methods; crossed episode × seed bootstrap, B = 10,000 (`n_seeds` per contrast, e.g.
    `A:cells.<cell>.0-499.H6a.success.n_seeds` = [5, 2]); two-sided p.
    [CITE-MISSING: bootstrap CI (Efron)]
  - **H6a.** Student (5 seeds) − G\* (runs 1 + 2). Difference test, plus TOST with δ = 0.04
    (`….H6a.success.tost.{delta, p_lower_margin, p_upper_margin, p_tost, ci90}`), with p_TOST = max of the two one-sided
    p-values.
  - **H6b.** Student − R-125 and student − R-500.
  - **H6c.** Round 2 − round 0.
  - **Holm.** Over 5 cells for the H6a difference test, the H6a TOST and H6c; over 10 contrasts for H6b. [CITE-MISSING:
    Holm (1979)]
  - Not Holm-controlled: BI, g_T, the fresh-window replications, E12 and the v5 row updates.
- **Power (30 w).** "The design expected 90 % half-widths of about 3.5–4 pp; the observed half-widths were 2.84–3.85 pp"
  (derived, pass 2 item 14). Failing to show equivalence is therefore largely a power outcome.
- **History (30 w).** One sentence: the v5 validation gate failed in 5/5 cells. Its clause-(i) thresholds were −1.23 to
  −1.72 pp against a nominal δ = 4 pp (`v5:12_d5_analysis.json > <cell> > succ > threshold`). This is why v6 adopts TOST.
- **Deviations.**
  - Latency is not re-timed (v5 E6 job-1 medians).
  - E12 uses G\* run 1 and episodes 0–99 only.
  - Each reduced planner and H\* is run once.

---

## 5. Results (≈ 1,150 words; decision budget ~2.0 p incl. Fig. 1, Tables 1–2)

### 5.1 C1. Distilled student vs shrunken planner: the frontier (≈ 400 w; Fig. 1, Table 2)
**Goal.** Present the one positive registered result, with every qualifier attached.

1. **(120 w) Latency axis.**
   - Per cell (v5 point medians, no dispersion): G\* 0.910–4.880 s, R-500 0.048–0.194 s, R-125 0.022–0.116 s, student
     0.326–0.500 ms (`A:cells.<cell>.frontier.latency_median_s.*`).
   - The reduced planners are 19–47× faster than G\* (derived).
   - The student is 62–389× faster than both reduced planners (`D:cells.<cell>.latency_ratio.{g125_512_16_over_student, g500_512_4_over_student}`, post hoc, no CI).
   - Full G\* is ≈ 2,544–9,767× slower (`D:…gstar_over_student`).
   - The v5 CI half-width rule for the G\*/student ratio is met only in A16-2
     (`v5:14_e6_analysis.json > <cell> > job1 > ratio_full_gstar_over_student > half_width_ok`).
   - Runners differ across cells, and there is no task-time model.
2. **(80 w) Cost of shrinking.**
   - The reduced planners lose 4.4–14.4 pp against G\* run 1 (point values, derived; smallest S12 R-500, largest A16-2
     R-125).
   - In S4, R-500 (0.390) is below R-125 (0.402).
   - Keys: `A:cells.<cell>.frontier.success_0_499.*`.
3. **(150 w) H6b (Table 2).**
   - Binding H6b sentence.
   - 7/10 rejected on 0–499, all positive. The largest rejected p is 0.0098 (S12 R-125); the next, S8 R-500
     (p = 0.0314), is not rejected.
   - R-500 in S2 (p 0.1378), S8 (p 0.0314) and S12 (p 0.2688) is not shown different.
   - Fresh window: 2/10 survive (S4 R-125 +0.112, p 0.0002; A16-2 R-125 +0.136, p 0.0012). S12 R-500 has a negative
     point estimate, −0.011 [−0.072, 0.051].
   - Single-run reduced planners: their variance is missing from these CIs, and the marginal rejections (S12 R-125, S4
     R-125, lower bounds ≈ +1.3/+1.4 pp) could be sensitive to it.
4. **(50 w) Strongest comparator per cell.** One sentence (post hoc, no CI):
   - The student clears the strongest non-oracle comparator at the registered level in 1/5 cells (A16-2).
   - Otherwise the strongest comparator is R-500 (S2), b_cov (S4, S12) or RL (S8).
   - Keys: `D:cells.<cell>.0-499.{strongest_non_oracle, strongest_value, margin_vs_strongest}`.

### 5.2 C2. Parity with G\* is not established (≈ 400 w; Table 1)
**Goal.** Answer the parity question honestly with teacher variance included. The E12 caveat sits beside every
number.

1. **(150 w) H6a.**
   - Binding H6a sentence.
   - All five 0–499 point estimates are negative, from −0.28 pp (A16-2) to −3.74 pp (S4). On 300–499, 4/5 are negative
     and A16-2 is +0.1 pp.
   - No pooled estimate (rule).
   - Upper-margin sentence.
   - Why-TOST-fails sentence.
   - A16-2 comes closest (p_TOST 0.0548, ci90 lower bound −4.12 pp). S4 is the weakest cell (ci90 [−0.0716, −0.0036];
     fresh [−0.106, −0.0005]), an unregistered one-sided indication of a deficit.
2. **(80 w) Ball-info.**
   - S4 −0.138 [−0.202, −0.075], p < 1e-4; S8 −0.103 [−0.172, −0.033], p 0.0048.
   - Both survive an unregistered Holm over the 5 BI p-values, and both are below 0.05 on the fresh window (S4 p 0.0206,
     S8 p 0.0354).
   - S2 is nominally lower on 0–499 only (p 0.0206), not a finding.
   - Keys: `A:cells.<cell>.<window>.H6a.ball_info.{diff, ci95, p_two_sided}`.
3. **(100 w) Teacher variance.**
   - G\* run 2 − run 1: +0.014 / −0.002 / +0.032 / 0.000 / +0.024 on 0–499, none significant (half-widths ≈ 4–5 pp).
   - Up to +5 pp fresh (S2, A16-2).
   - First-decision agreement 0.25–0.45.
   - Student seed spread 2.8–6.2 pp (derived).
   - Point gaps are therefore of the same magnitude as the teacher's own run-to-run variation.
   - Keys: `A:cells.<cell>.<window>.H6a.gstar_run2_minus_run1_success.{diff, ci95, p_two_sided}`;
     `A:cells.<cell>.<window>.gstar_first_decision_agreement_run2_vs_run1`.
4. **(70 w) v6 update of the v5 run-1 row.**
   - "Against G\* run 1 alone the gaps are −1.92, −3.84, −1.32, −1.96 and +0.92 pp (none significant); S4 now exceeds
     v5's 0.2–2.5 pp range and A16-2 has changed sign" (pass 2 item 6).
   - Key: `A:cells.<cell>.0-499.v5_row_updates.student_minus_gstar_run1_success`.

### 5.3 C3. DAgger vs behaviour cloning, and the baseline rows (≈ 350 w)
**Goal.** Report the one component ablation and the report-only baselines in one paragraph each.

1. **(130 w) H6c (ablation row).**
   - Binding H6c sentence.
   - Diffs +0.0132 / +0.0084 / +0.0072 / +0.0004 / −0.0052, p 0.453–0.997; fresh p 0.5372–0.9208.
   - BI r2 − r0 is not significant either (p 0.0564–0.8056).
   - Held-out regret of the kept checkpoints r0 vs r2, report-only, one clause:
     `v5:16_report_rows.json > student_checkpoint_sensitivity > <cell> > <seed> > {r0, r2} > R_bar_kept`.
   - Regret on student-visited states was not measured.
   - Keys: `A:cells.<cell>.<window>.H6c.{success, ball_info}`; r0 means `D:cells.<cell>.<window>.r0student_mean`
     (post hoc).
2. **(220 w) Baseline rows (report-only, "v6 update of a v5 row").**
   - **H\*.** Student − H\* +6.68 / +8.96 / +7.48 / +5.64 / +17.12 pp, all ci95 excluding 0. Fresh: S2 (p 0.0694) and S12
     (p 0.0672) are not < 0.05. Then the heuristics binding sentence, with best-heuristic margins from
     `D:cells.<cell>.0-499.{best_heuristic, registered_H_star, margin_vs_best_heuristic}` (S4 +0.0416, S8 +0.0508, S12
     +0.0244; post hoc, no CI).
   - **B-spread** is near zero everywhere (0.006–0.074).
   - **RL.**
     - RL binding sentence. Student − RL: S2 +0.0856, S4 +0.0612, S8 +0.0256 [−0.010, 0.062], S12 +0.0568, A16-2 +0.2688.
     - Student − success-reward RL: S2 +0.1096 [0.066, 0.153], S12 +0.0708 [0.024, 0.116], with the time-guard
       disclosure.
     - H2-v5 g_T: "student higher on the RL objective" holds only in A16-2 (+0.709, one-sided LB 0.479), where RL uses
       2.0 of 3 probes in 4/5 seeds (`A:cells.A16-2.0-499.means.rl_s71{2..5}.n_probes`).
     - RL − student g_T is significantly positive in S2 / S4 / S8, and the inversion flag is true in S2 and S4.
     - The RL configuration was tuned once on S2. Whether it is under-tuned elsewhere was not tested.
   - **Behaviour (descriptive).** The student travels less than G\* in every cell (e.g. S2 0.487–0.674 vs 0.820 rad;
     S12 0.044–0.056 vs 0.110). RL travels the most. No mechanism is claimed.
   - Keys: `A:cells.<cell>.<window>.v5_row_updates.{student_minus_hstar_success, student_minus_rl_success, student_minus_rlsucc_success, H2_v5_update.*}`;
     `A:cells.<cell>.0-499.means.<method>.{success, travel_rad, n_probes}`.

---

## 6. Limitations and evaluator note (≈ 480 words; decision budget ~0.75 p)

### 6.1 C4. Methods note: evaluator-grid sensitivity and teacher stochasticity (≈ 200 w)
**Goal.** Give the reporting lesson. It sits here, not in Results, per the decision's page budget, but it is named as
C4.

- **E12 (episodes 0–99, G\* run 1, all 5 student seeds).**
  - Binding E12 sentence.
  - Per-cell student − G\* on sub 8 vs sub 16: S2 −0.026 → −0.042, S4 −0.036 → +0.010, S8 −0.020 → +0.030, S12
    +0.008 → −0.038, A16-2 +0.050 → +0.044. Neither grid shows a significant difference (100-episode ci95 half-widths
    7–10 pp).
  - The sign changes in 3/5 cells, and the shifts do not favour either policy systematically.
  - Flip rates: G\* 0.10 / 0.08 / 0.07 / 0.07 / 0.01.
  - Keys: `A:cells.<cell>.E12.{flip_rate.*, student_minus_gstar_success_sub8, student_minus_gstar_success_sub16, episodes_per_method, complete}`.
- **Teacher stochasticity.** Binding sentence, referring back to §5.2.3.
- **Lesson.** In this setting, success contrasts of a few pp depend on the read-out grid and on the teacher's own
  Monte Carlo variation at the size of the equivalence margin. Parity claims for amortized planners therefore need
  teacher reruns and an evaluator check registered in advance. Re-deciding H6a on sub 16 would be post hoc and was not
  done.
- Cards: `foster2021deep`, `rainforth2024modern` (bound vs read-out evaluation in BED).

### 6.2 Limitations (≈ 280 w, one sentence each)
1. **Teacher variance.** It comes from only two G\* runs, so the G\* bootstrap component is poorly estimated.
2. **Single runs.** The reduced planners and H\* are run once each, so their variance is missing from the H6b CIs.
3. **Evaluator.** E12 covers 100 episodes and G\* run 1 only, and cannot correct the 0–499 contrasts.
4. **Latency.** Point medians from v5 job 1, without dispersion. The CI rule is met in 1/5 cells, the runners differ,
   and there is no task-time model.
5. **Windows.** Episodes 0–299 were seen in v5. The fresh window (200 episodes) has CIs about 1.6× wider (derived).
6. **Multiplicity.** BI, g_T, the fresh replications and the baseline rows are not Holm-controlled. For example, S8
   fresh G\* − student g_T, p = 0.0068, should not be read as a finding.
7. **DAgger.** Regret on student-visited states was not measured, and no equivalence test was registered for H6c.
8. **Comparators.**
   - The RL configuration was tuned once on S2 with one sweep seed.
   - Success-reward RL was time-guard truncated.
   - H\* is stale.
   - No cheap information-based heuristic was included.
9. **A16-2.** It confounds family, K and n\*, sits at one κ, and shares 8 identities with library A. H5b is
   uninformative: H5b binding sentence (`A:H5b_update_0_499.*`).
10. **G\* is a greedy reference.** A one-step look-ahead screen shows report-only headroom in nats at 512 candidates (S2
    +0.0658 [0.0297, 0.1084], S12 +0.0422 [0.0250, 0.0614]; `v5:12_e7_analysis.json > cells > <S2|S12> > C1_512 > indep_gap_nats`).
    Success-terms headroom was not measured.
11. **Scope.** Planar simulation (TouchBED), 5 cells, frozen v5 policies, no hardware. Jobs were time-guarded and
    resumed with identical commands; resumption is assumed outcome-neutral.
12. **Not run** (decision §4.1 item 3): extra G\* or reduced-planner runs, a sub-16 re-read of H6a, latency re-timing,
    RL re-tuning, retraining, new BI/g_T tests.

---

## 7. Conclusion (≈ 100 words)
Four clauses with no new numbers. Then: "pre-registered; simulation; preliminary".
1. As a fast policy, distilling G\* gave more accuracy than shrinking it in 7/10 registered contrasts, at 62–389× lower
   per-decision latency; on fresh episodes only the direction held.
2. Parity with G\* is neither shown nor refuted, and deficits of ~7–8 pp are not excluded.
3. The DAgger rounds added no detectable accuracy over BC.
4. Evaluator choice and teacher stochasticity move the contrasts by as much as the margin.

---

## 8. Every results row and ablation row, mapped to JSON keys
**Tags.**
- DEC: pre-registered decision (Holm).
- GATE: completeness or calibration.
- REP: reported, no test.
- EXPL: ci95, not multiplicity-controlled.
- PH: `15_derived_v6.json` or analysis-derived, post hoc, no CI.
- HIST: v5 record.

### Table 1: H6a, student (5 seeds) − G\* (runs 1 + 2), success, both windows (§5.2)
Columns: Δ 0–499 [ci95] · ci90 · p_TOST · Holm · Δ 300–499 [ci95] · ci90 fresh · p_TOST fresh · G\* run 2 − run 1
(0–499) · E12 shift (derived).

| Row | Cell | Values (copied) | Keys | Tag |
|---|---|---|---|---|
| T1.1 | S2 | −0.0262 [−0.0688, 0.0168] · [−0.0616, 0.0092] · 0.2621 · no · −0.036 [−0.114, 0.042] · [−0.102, 0.029] · 0.4524 · +0.014 · −1.6 pp | `A:cells.S2.{0-499,300-499}.H6a.success.{diff, ci95, tost.ci90, tost.p_tost}`; `….holm.{H6a_difference, H6a_tost}`; `A:cells.S2.0-499.H6a.gstar_run2_minus_run1_success.diff`; `A:cells.S2.E12.*` | DEC / REP |
| T1.2 | S4 | −0.0374 [−0.0784, 0.0024] · [−0.0716, −0.0036] · 0.4559 · no · −0.053 [−0.1165, 0.0095] · [−0.106, −0.0005] · 0.6561 · −0.002 · +4.6 pp | same paths, S4 | DEC / REP |
| T1.3 | S8 | −0.0292 [−0.0704, 0.0136] · [−0.0640, 0.0060] · 0.2908 · no · −0.034 [−0.095, 0.028] · [−0.085, 0.017] · 0.4211 · +0.032 · +5.0 pp | same paths, S8 | DEC / REP |
| T1.4 | S12 | −0.0196 [−0.0532, 0.0148] · [−0.0480, 0.0088] · 0.1157 · no · −0.016 [−0.067, 0.035] · [−0.0585, 0.026] · 0.1659 · 0.000 · −4.6 pp | same paths, S12 | DEC / REP |
| T1.5 | A16-2 | −0.0028 [−0.0496, 0.0436] · [−0.0412, 0.0358] · 0.0548 · no · +0.001 [−0.077, 0.080] · [−0.064, 0.0665] · 0.1557 · +0.024 · −0.6 pp | same paths, A16-2 | DEC / REP |
| T1.6 | all | upper-margin p (0–499): 0.0014 / 0.0003 / 0.0004 / 0.0009 / 0.0348; fresh A16-2 0.1557 | `A:cells.<cell>.<window>.H6a.success.tost.p_upper_margin` | EXPL (per cell, unadjusted) |
| T1.7 | all | BI diff (0–499): −0.093 / −0.138 / −0.103 / −0.055 / +0.024 (p 0.0206 / < 1e-4 / 0.0048 / 0.0664 / 0.638) | `A:cells.<cell>.<window>.H6a.ball_info.*` | EXPL |
| T1.8 | all | first-decision agreement 0–499: 0.274 / 0.402 / 0.452 / 0.426 / 0.314; fresh 0.245 / 0.415 / 0.445 / 0.420 / 0.305 | `A:cells.<cell>.<window>.gstar_first_decision_agreement_run2_vs_run1` | REP |
| T1.9 | all | student − G\* run 1 (0–499): −0.0192 / −0.0384 / −0.0132 / −0.0196 / +0.0092 | `A:cells.<cell>.0-499.v5_row_updates.student_minus_gstar_run1_success` | REP (v5 row update) |

### Table 2: H6b, student − reduced planners, success (§5.1)
Columns: R-125 Δ [ci95], p, Holm · R-500 Δ [ci95], p, Holm · fresh R-125 Δ, p, Holm · fresh R-500 Δ, p, Holm · latency
R-125/student, R-500/student (PH).

| Row | Cell | Values (copied) | Keys | Tag |
|---|---|---|---|---|
| T2.1 | S2 | +0.0928 [0.044, 0.140], p < 1e-4, yes · +0.0368 [−0.012, 0.087], 0.1378, no · +0.094, 0.0198, no · +0.004, 0.9268, no · 231×, 389× | `A:cells.S2.{0-499,300-499}.H6b.{g125_512_16, g500_512_4}.{diff, ci95, p_two_sided}`; `….holm.{H6b_g125_512_16, H6b_g500_512_4}`; `D:cells.S2.latency_ratio.*` | DEC / PH |
| T2.2 | S4 | +0.0556 [0.014, 0.098], 0.0072, yes · +0.0676 [0.024, 0.112], 0.0016, yes · +0.112, 0.0002, yes · +0.077, 0.0198, no · 163×, 285× | same paths, S4 | DEC / PH |
| T2.3 | S8 | +0.0628 [0.022, 0.104], 0.0022, yes · +0.0468 [0.004, 0.090], 0.0314, no · +0.066, 0.055, no · +0.026, 0.4638, no · 84×, 171× | same paths, S8 | DEC / PH |
| T2.4 | S12 | +0.0564 [0.013, 0.099], 0.0098, yes · +0.0244 [−0.018, 0.067], 0.2688, no · +0.019, 0.5484, no · −0.011, 0.7368, no · 62×, 134× | same paths, S12 | DEC / PH |
| T2.5 | A16-2 | +0.1532 [0.102, 0.204], p < 1e-4, yes · +0.1092 [0.058, 0.159], p < 1e-4, yes · +0.136, 0.0012, yes · +0.086, 0.032, no · 176×, 299× | same paths, A16-2 | DEC / PH |
| T2.6 | all | success 0–499 of G\* r1 / G\* r2 / R-500 / R-125 / student (frontier points, Fig. 1) | `A:cells.<cell>.frontier.success_0_499.*`; `A:cells.<cell>.0-499.means.gstar2.success` | REP |
| T2.7 | all | latency medians (s) of G\*, R-500, R-125, student | `A:cells.<cell>.frontier.latency_median_s.*` (= `v5:14_e6_analysis.json > <cell> > job1 > * > median`) | REP |
| T2.8 | all | G\*/student 9,767 / 6,829 / 3,450 / 2,544 / 8,284× | `D:cells.<cell>.latency_ratio.gstar_over_student` | PH |

### Ablation row (the only one; §5.3)
| Row | Item | Values | Keys | Tag |
|---|---|---|---|---|
| AB.1 | H6c: DAgger round 2 − BC round 0, success, 0–499 | +0.0132 [−0.0224, 0.0480] / +0.0084 [−0.0228, 0.0400] / +0.0072 [−0.0196, 0.0336] / +0.0004 [−0.0280, 0.0304] / −0.0052 [−0.0316, 0.0208]; Holm 0/5 | `A:cells.<cell>.0-499.H6c.success.*`; `….holm.H6c` | DEC |
| AB.2 | H6c fresh window | p 0.715 / 0.9206 / 0.9208 / 0.5372 / 0.7826; S2 ci95 upper 0.071 | `A:cells.<cell>.300-499.H6c.success.*` | DEC (replication) |
| AB.3 | H6c BI | p 0.0564 / 0.1764 / 0.3078 / 0.6188 / 0.8056 | `A:cells.<cell>.0-499.H6c.ball_info.*` | EXPL |
| AB.4 | r0 and r2 5-seed means | e.g. S2 0.4856 vs 0.4988 | `D:cells.<cell>.<window>.{r0student_mean, student_mean}` | PH |
| AB.5 | kept-checkpoint held-out regret per round | as logged | `v5:16_report_rows.json > student_checkpoint_sensitivity > <cell> > <seed> > r{0,1,2} > R_bar_kept` | REP |

No other component is claimed effective, so no other ablation row is required (`hard_constraints.md` §3 "Mandatory
ablations"; decision §2.1 rule 2).

### In-text rows (report-only)
| Row | Item | Keys | Tag |
|---|---|---|---|
| X1 | E12 flip rates and sub-8/sub-16 contrasts (§6.1) | `A:cells.<cell>.E12.*` | REP |
| X2 | Student − H\*, both windows | `A:cells.<cell>.<window>.v5_row_updates.{H_star, student_minus_hstar_success}` | EXPL (v5 row update) |
| X3 | Best-heuristic and strongest-comparator margins | `D:cells.<cell>.<window>.{best_heuristic, registered_H_star, margin_vs_best_heuristic, strongest_non_oracle, strongest_value, margin_vs_strongest}` | PH |
| X4 | Student − RL; student − success-reward RL | `A:cells.<cell>.<window>.v5_row_updates.{student_minus_rl_success, student_minus_rlsucc_success}`; RL means `D:cells.<cell>.<window>.rl_mean` | EXPL / PH |
| X5 | H2-v5 g_T update and inversion | `A:cells.<cell>.<window>.v5_row_updates.H2_v5_update.{student_minus_rl_gT, claim_student_higher_on_rl_objective, rl_minus_student_gT, gstar_minus_student_gT, inversion}` | EXPL |
| X6 | Heuristic, B-spread and Random successes | `A:cells.<cell>.<window>.means.{b_fan, b_spread, b_cov}.success` | REP |
| X7 | Behaviour: travel and probes per method | `A:cells.<cell>.<window>.means.<method>.{travel_rad, n_probes}` | REP |
| X8 | RL probe collapse in A16-2 | `A:cells.A16-2.0-499.means.rl_s71{1..5}.n_probes` | REP |
| X9 | H5b update | `A:H5b_update_0_499.{cells, delta_succ, gstar_mean_travel_rad, weights, slope_per_rad, ci95_per_rad, slope_per_100deg, ci95_per_100deg, verdict}` | REP (v5 row update) |
| X10 | Completeness | `A:cells.<cell>.<window>.{n_required, episodes_per_method, complete, gt_episodes_per_method, gt_complete}` | GATE |
| X11 | History: v5 validation gate | `v5:12_d5_analysis.json > H5a_validation > cells_pass`; `v5:12_d5_analysis.json > <cell> > succ > {delta_hat, threshold}` | HIST |
| X12 | RL selection and training caps; success-reward RL truncation | `v5:12_rl_sweep_selection.json > {rule, selected_cfg}`; `v5:16_report_rows.json > {rl_main_cfg6, rl_success}` | GATE / REP |
| X13 | Look-ahead headroom in nats (Limitation 10) | `v5:12_e7_analysis.json > cells > <S2\|S12> > C1_512 > indep_gap_nats` | REP |
| X14 | Latency CI rule | `v5:14_e6_analysis.json > <cell> > job1 > ratio_full_gstar_over_student > {median, ci95, half_width_ok}` | REP |

**Optional, master draft only:** `v5:19_lat_agreement.json > cells > <cell> > {student, g125_512_16, g500_512_4}`
(agreement with G\* on the latency states). It uses a different state set from T1.8, so the two are not compared.

---

## 9. Figure plan

### Figure 1 (full width, top of page 2, ≈ 0.4 page): "Distil or shrink? The accuracy–latency frontier in five cells"
**Story.** The reader should see three things without the prose:
1. Shrinking the planner buys speed (19–47×) at a visible accuracy cost.
2. The distilled student is 62–389× faster still, and on 0–499 sits above both reduced planners in every cell as a
   point estimate. Stars mark only the Holm-confirmed contrasts.
3. Its vertical position relative to G\* is undecided, because the two G\* runs bracket a band as wide as the
   student–G\* gap.

The figure therefore carries C1 and shows the limit of C2.

**Visual elements.**
- **Panel A (left, ≈ 20 % width; schematic, image-generator prompt in a LaTeX comment).**
  - Top-down planar polygon with a ghost-outline particle belief; a stand-off circle with the fingertip at φ_t; an
    orange travel arc labelled "cost 1 + κ|Δφ|/π"; a blue probe arrow.
  - Below it, three arrows leave a box "G\* (EIG / cost, argmax)":
    - "shrink → R-500, R-125" (grey);
    - "distil (BC round 0 → DAgger rounds 1–2) → student" (blue);
    - "PPO on g_T → RL" (dashed).
  - No numbers on this panel.
- **Panels B–F (right, five small multiples, one per cell, ordered S2, S4, S8, S12, A16-2; plotted from JSON with the
  dataviz skill).**
  - x axis: median per-decision latency, log10 seconds, shared range 1e-4 to 1e1.
  - y axis: success on test episodes 0–499, shared range 0.20–0.56.
  - Markers:
    - G\* run 1 (filled black circle) and run 2 (hollow black circle), at the same x and joined by a thin vertical
      segment labelled "teacher run-to-run";
    - R-500 (grey square) and R-125 (grey triangle);
    - student 5-seed mean (blue diamond), with a vertical bar for the min–max over seeds.
  - Thin grey arrows from R-125 and R-500 to the student, with a star where Holm rejects (S2: R-125; S4: both; S8:
    R-125; S12: R-125; A16-2: both).
  - H\* and RL as horizontal dashed lines labelled "H\* (latency not timed)" and "RL (latency not timed)". **No latency
    is plotted for them** because none was measured.
  - A16-2 panel title in the second-library colour.
- **Data (all copied).**

  | Cell | x: G\* / R-500 / R-125 / student (s) | y: G\* r1 / G\* r2 / R-500 / R-125 / student [seed min–max] | H\* / RL (lines) |
  |---|---|---|---|
  | S2 | 4.880 / 0.194 / 0.116 / 0.000500 | 0.518 / 0.532 / 0.462 / 0.406 / 0.4988 [0.464–0.526] | 0.432 / 0.4132 |
  | S4 | 3.375 / 0.141 / 0.080 / 0.000494 | 0.496 / 0.494 / 0.390 / 0.402 / 0.4576 [0.432–0.482] | 0.368 / 0.3964 |
  | S8 | 1.234 / 0.061 / 0.030 / 0.000358 | 0.432 / 0.464 / 0.372 / 0.356 / 0.4188 [0.408–0.436] | 0.344 / 0.3932 |
  | S12 | 0.910 / 0.048 / 0.022 / 0.000358 | 0.434 / 0.434 / 0.390 / 0.358 / 0.4144 [0.398–0.428] | 0.358 / 0.3576 |
  | A16-2 | 2.702 / 0.098 / 0.058 / 0.000326 | 0.474 / 0.498 / 0.374 / 0.330 / 0.4832 [0.464–0.496] | 0.312 / 0.2144 |

  Keys:
  - x: `A:cells.<cell>.frontier.latency_median_s.*`;
  - y: `A:cells.<cell>.frontier.success_0_499.*`, `A:cells.<cell>.0-499.means.gstar2.success`;
  - seed range: `A:cells.<cell>.0-499.means.student_s70{1..5}.success`;
  - H\*: `A:cells.<cell>.0-499.means.<H_star>.success`;
  - RL: `D:cells.<cell>.0-499.rl_mean` (post hoc);
  - stars: `A:cells.<cell>.0-499.holm.H6b_*`.
- **Not on the figure:** fresh-window points (Table 2 carries them), the CIs of the contrasts (Tables 1–2), and any
  fitted frontier curve.

**Draft caption.**
> **Figure 1.** *Distil or shrink a cost-aware touch planner?* (A) Task and the three ways to make the planner G\*
> fast: shrink it (reduced planners R-500, R-125), distil it into a belief-free policy (behaviour cloning, then DAgger),
> or train the same policy with RL. (B–F) Success on 500 test episodes against median per-decision latency (log scale;
> timings from the previous round, point medians without dispersion) for travel cost κ = 2, 4, 8, 12 on shape library S
> and κ = 2 on library A16. Filled and hollow circles are two independent G\* runs. Diamonds are the 5-seed student mean,
> with the seed range. Stars mark student-vs-reduced-planner contrasts confirmed by Holm (7 of 10; 2 of 10 on the 200
> fresh episodes). Dashed lines show the pilot-chosen heuristic H\* and RL, whose latency was not timed. The student's
> position relative to G\* is undecided: neither a difference nor equivalence within 4 pp is shown (Table 1), and
> changing the evaluator grid alone moves that contrast by up to 5 pp. Simulation; preliminary.

### Figure 2 (optional, one column; cut first in stage 22): "How large is a few pp here?"
- Per cell, three horizontal bars (pp):
  - |student − G\*| on 0–499 (`A:…H6a.success.diff`);
  - |G\* run 2 − run 1| on 0–499 (`A:…H6a.gstar_run2_minus_run1_success.diff`);
  - |E12 shift| (derived, from `A:cells.<cell>.E12.*`).
- A vertical line at δ = 4 pp.
- Caption: "Point magnitudes only; no CIs; E12 is on 100 episodes."
- This carries C4 visually.

### Tables
- **Table 1** = §8 Table 1 rows T1.1–T1.5, with T1.6–T1.7 as footnotes.
- **Table 2** = §8 Table 2 rows T2.1–T2.5.
- Table 0 (cells) stays in-text in §3.1.

---

## 10. Word budget
| Section | Words |
|---|---|
| Abstract | 170 (not counted) |
| 1 Introduction + related work | 650 |
| 2 Setup and method | 650 |
| 3 Pre-registration and statistics | 320 |
| 4 Results (C1 400, C2 400, C3 350) | 1,150 |
| 5 Limitations and evaluator note (C4 200, limitations 280) | 480 |
| 6 Conclusion | 100 |
| **Body total** | **3,350** |

Outline sections 2–7 are paper sections 1–6. The provenance table (internal identifiers, amendment labels, file paths)
goes to the master-draft appendix and is cut or moved to supplementary material in stage 22.

## 11. Open markers
**[CITE-MISSING] (3, no card in `05_knowledge_cards.json`):**
1. DeepSets (Zaheer et al. 2017), §3.3.
2. Holm (1979), §4.
3. Bootstrap CIs (Efron), §4.

**Carried constants.** The following are carried verbatim from `draft_v5_final.md` (code and amendment provenance, not
a results field), and stage 17 keeps that provenance note:
- the cost formula and geometry;
- the S2/S12 τ;
- the `g`N`_`C`_`M meaning;
- the label size and β schedule;
- B = 10,000;
- the RL sweep seed 719.

No other [NEED] marker remains. Every other constant has a JSON key above.
