# Paper outline (stage 16, v3, outcome row 4: characterisation paper)

**Venue (default until the owner decides, 15_decision §4.3):** RSS 2027 Stage 1 extended abstract: at most 5 content
pages plus 1 page of references, double-column, no supplementary material. The method must be complete; experiments
may be preliminary. **Main-body target: about 3,400 words** (abstract not counted), plus 2 tables and 2 figures.
If the owner picks RA-L or a workshop (option b), expand the same structure (§11 at the end lists what grows).

**Paper type.** This is the pre-registered **row-4 characterisation** of `docs/07_hypotheses_v3.md` §5. There is no
method claim. Every claim is the outcome of a pre-registered decision rule, or it is a labelled descriptive or
exploratory row.

**Sources (the only ones the draft may quote numbers from).**
- `results/v3/results_v3.json`, cited below as `key.path` (top-level key first).
- `results/v3/14_analysis.md`. Its pass-2 rewrites (S1–S7, M1–M8, m1–m7) are **binding** wording; see §0.3.
- `results/v3/15_decision.md`: labels, the PROCEED conditions and the pre-written readings of the B-fan row.
- Citations come only from `docs/05_knowledge_cards.json`, using the exact `cite_key`.

---

## 0. Global constraints for the draft

### 0.1 Title

**Proposed title:** *Can Cost-Aware Information-Gain Touch Selection Be Amortized? Look-Ahead Headroom and
Learnability under Travel Cost*

- The title and abstract contain no "near-optimal" (07_hypotheses_v3 §3, "Working title"; 15_decision §4.2).
- The question form is deliberate. Row 4 has no amortization result, so the title asks rather than asserts.
- **Owner check:** 07_hypotheses_v3 §3 says "the outcome map can only shorten" the working title. A strict reading of
  that rule allows only:
  - **Fallback B:** *Cost-Aware Information-Gain Touch Selection: Look-Ahead Headroom and the Learnability of
    Amortized Policies*. This drops "Amortizing", which row 4 does not support.
  - The owner chooses between the proposed title and Fallback B.

### 0.2 Labels the paper must carry (15_decision §1)

| Claim | Label | Key |
|---|---|---|
| H1 (distilled student non-inferior to G\*) | **dead at D3** (never tested on test3) | `12_d3_analysis_rem.passes` = false |
| H1-fb (student-pruned greedy) | **withdrawn** (Lat′ ratio 3.22 < 10) | `12_lat_analysis.ratio_full_over_pruned16`, `.H1_fb_active` |
| H2 (student beats RL on g_T by > 0.10 nats) | **rejected**. Fail-branch reading: "dense supervision does not improve on RL with this head". This is a non-detection, not equality. | `14_h2_analysis.passes`, `.bootstrap.lower` |
| H3 (small one-step headroom) | **Hold** | `12_g2_analysis.H3.region`, `.k12.ub95` |
| Encoder sentence | "generalisation / covariate shift, not capacity". Rule-permitted but weakly supported: covariate shift is inferred, not observed. | `14_labelfit.groups.*[].under_fit` |

### 0.3 Binding phrasing (pass-2 rewrites; the draft must use these and never the pass-1 sentences)

- **S5 (H3 headline):** "One-step rollout over the reduced greedy completion gains ≤ 2.2 % of the remaining expected
  ball information at κ = 12 (S, n\* = 4; one-sided 95 % UB of G(12) = 0.0221)."
- **S4 (H3 bias):** "On 20 separate beliefs the estimator reads V_G\* 0.087 nats (4.3 %, no CI) below an independent
  full-G\* rollout, comparable in size to the 0.041-nat κ = 12 gap; this direction alone would inflate G, and Hold could
  be affected only if V_LA were under-read by more, which was not checked."
- **S7 (learned vs G\*):** "Neither learned policy was shown to reach G\*: the student failed the D3 non-inferiority rule
  on val3 (Δ̂_succ −4.40 pp vs threshold −1.68 pp), and on test3 it trails by −4.4 pp (significant one-sided only) while
  RL trails by −7.0 pp (ci95 [+0.2, +13.7] for G\* − RL)."
- **S1 (student vs RL):** "No difference between the two learned policies was detected on g_T (Δ = +0.0002 nats,
  one-sided 95 % bounds [−0.31, +0.30]) or on test success (ci95 [−3.7, +8.8] pp); equivalence was not tested."
- **S3 (BI vs g_T):** "Student − RL BI is +0.289 nats (ci95 [+0.117, +0.465]) on test3 0–299, while the g_T difference
  on 0–499 is undetected with bounds wide enough (±0.31 nats) to include a gap of that size; RL executes 3.0 probes
  against the student's 4.0."
- **S2 (heuristic, unpaired):** "On unpaired splits the travel-nearest heuristic b_fan (0.403 ± 0.040, n = 154 of 200
  pilot3 episodes) has a point success comparable to the remedied student (0.402 val3, 0.382 test3); no paired
  comparison exists, so nothing in the record shows the student beats it." This sentence is superseded by the paired
  row if that row completes (§9, row R9).
- **S6 (H1-fb):** "PF assimilation and neighbour lists account for 15.0 % of G\*'s per-decision time (component
  medians), so pruning candidates cannot exceed about 6.7× and cannot give 10×; measured full / pruned-16 = 3.22."
- **M1 (remedy):** "After the one remedy (round 0 and both DAgger rounds doubled; 7,957 → 17,083 training decisions),
  the point estimates moved from −0.199 to −0.096 nats BI and from −5.87 to −4.40 pp success; this change was not
  tested."
- **M3 (H2 power):** "Passing required an observed Δ > 0.41 nats; with SE ≈ 0.19, the test had about 80 % power only for
  a true Δ near 0.57 nats."
- **M5 (latency):** "Per decision, the student's median latency is about 2,200× below full-size G\* (pooled-machine
  Lat′, protocol incomplete; G\* median CI alone ≈ 1,900–2,300×), not compared at equal accuracy."
- **M4 (per episode, optional):** "Assuming 3–4 decisions per episode and no greedy read-out cost, Σ L_dec(G\*) /
  (Σ L_dec(student) + L_final) ≈ 13–18×; the protocol L_ep was not measured and would be lower."
- **M6 (D3-B):** "The 5 missing episodes can raise Δ̂_succ by at most 2.0 pp (to −18.1 pp), still 17 pp below the
  threshold, so the D3-B verdict cannot flip."
- **M7 (E′ flip):** "The one counted flip occurred with the true-identity mass unchanged (0.228) and outside the
  [0.45, 0.55] tie band; the JSON does not record which part of the success criterion changed."
- **M8 (sub-8 cost):** "Sub-8 read-out costs 40.6 s per episode, which limited the grid-scored rows (G5′ re-reads,
  D3/D3-B, M4 on 300 episodes)."
- **m2 / m5 (RL seeds):** "RL varies more across its 3 seeds than the student (test success range 7.7 vs 1.0 pp; g_T
  range 0.48 vs 0.14 nats)"; "The RL per-seed SD of g_T is about 3.3× the student's (0.253 vs 0.077 nats; range ratio
  3.5)."
- **m3 (evaluator):** "Sub 4 → 8 flips the success outcome of 7.5 % of the 200 S0 calibration episodes."
- **m6 (TOST):** "No equivalence test (TOST) was pre-registered or run for H2."
- **m7 (G5′):** "Provisional PASS in all 3 cells on incomplete random rows (n = 62 / 199 / 161 of 200); D_c ≥ 0.35
  everywhere, so δ_c = 0.04 (cap) is unlikely to move."

### 0.4 Never write

- Any method claim, or any phrasing implying that H1, H1-fb or H2 passed.
- "near-optimal".
- "indistinguishable", "same sPCE", or "RL and distillation are equal".
- "2,000× per episode"; any latency ratio without "per decision".
- "the remedy cut/halved" (causal wording).
- "objective mismatch". The H2 fail branch excludes it because the success ci95 contains 0.
- "RL is unstable".
- "zero-travel heuristic". B-fan is travel-nearest.
- A learning-vs-heuristic sentence beyond the pre-written readings of §9 R9.
- A number from PROGRESS.md or from the 07c notes that the JSON contradicts. The first-attempt values are the JSON's
  −5.87 pp, not the note's −6.8 pp.
- Gap closure (`14_m4_analysis.gap_closure_reported` = false).
- CPU-h. It is not in the JSON.
- Environment, CI or infrastructure problems presented as findings. Compute only limits n; it is mentioned once, in
  Limitations, through the M8 sentence.

---

## 1. Abstract (about 180 words, not counted in the body target)

**Goal.** State the research problem (active tactile localization under travel cost):
- (i) how much headroom one-step look-ahead leaves over greedy cost-aware information-gain touch selection;
- (ii) whether that greedy planner can be amortized by a learned policy, comparing distillation from the planner with RL
  on the same objective.

Then give the four headline outcomes with numbers, and say that the experiments are preliminary: one cell (S, κ = 12),
n\* = 4.

**Content, in order.**
1. Problem and setting: a joint identity × planar-pose belief, travel cost on a stand-off circle, and the cost-aware
   greedy G\*.
2. H3: the S5 sentence, shortened to "≤ 2.2 % (one-sided 95 % UB)".
3. Learnability: neither DAgger distillation nor PPO with the same relative DeepSets head was shown to reach G\* (the S7
   sentence, short form).
4. H2: on RL's own objective, no improvement of distillation over RL was detected (pre-registered test rejected;
   non-detection).
5. Per-decision cost: about 2,200× lower median latency for the learned head, not at equal accuracy (the M5 short form).
6. "Pre-registered; single cell; preliminary."

**Evidence links.** `12_g2_analysis.k12.ub95`; `12_d3_analysis_rem.succ.delta_hat` / `.threshold`;
`14_m4_analysis.diffs["student-gstar:success"]`; `14_m4_analysis.diffs["gstar-rl:success"]`;
`14_h2_analysis.bootstrap.diff` / `.lower` / `.upper`; `12_lat_analysis.ratio_full_over_student`.

**Constraint.** No "near-optimal". No learning-vs-heuristic sentence unless R9 reading (a) occurs. In that case add
one clause, labelled exploratory.

---

## 2. Introduction (target 550 words)

**Goal.** Motivate the two coupled questions behind every information-driven touch selector under travel cost:
- (1) Is greedy cost-aware EIG selection good enough, or is planning depth worth paying for?
- (2) Can the per-decision cost of online belief-based selection be amortized into a network?

Then state that this is a pre-registered characterisation with an honest negative core.

**Paragraph plan.**
1. **(about 130 words) Active tactile localization.**
   - Touches are sparse and ambiguous, so a belief over identity and pose is maintained, and the next touch is chosen
     by expected information gain.
   - Moving the finger costs time, so selection must be cost-aware.
   - Cite: `petrovskaya2011global`, `hebert2013next`, `zheng2024bayesian`, `zheng2026bayesian`, `ottenhaus2018active`,
     `seminara2019active`.
2. **(about 120 words) Question 1, depth.**
   - Greedy selection is backed by (adaptive) submodularity, yet it can be weak when actions constrain the future.
     Travel cost is exactly such a coupling.
   - Cite: `javdani2012efficient`, `vien2015touch`, `chen2015submodular`, `esfandiari2019adaptivity`.
3. **(about 120 words) Question 2, amortization.**
   - Online PF-based EIG re-optimises at every decision.
   - Amortized experimental design learns a policy instead, through RL on contrastive bounds or through other
     approaches.
   - The question is whether supervising the policy with the planner's dense per-action scores (DAgger distillation)
     beats RL on the same objective with the same head.
   - Cite: `foster2021deep`, `blau2022optimizing`, `ivanova2021implicit`, `hedman2025step`, `rainforth2024modern`;
     tactile RL: `riou2024reinforcement`, `niemann2024when`.
4. **(about 180 words) What we did and found.**
   - Pre-registered design (hypotheses, thresholds and outcome map frozen before any test episode).
   - One-step rollout headroom over G\* is small: the S5 sentence.
   - With the same relative DeepSets head, neither DAgger distillation nor PPO was shown to reach G\*: the S7 sentence.
     A label-fit diagnosis assigns the student's shortfall to generalisation rather than capacity, in the weak form of
     §0.2.
   - On RL's training objective no advantage of distillation was detected (H2 rejected; the M3 power caveat).
   - The learned head is about 2,200× cheaper per decision, not at equal accuracy (M5).
5. **Contributions list.** Exactly C1–C4. C5 is folded into C2 and C4.
   - **C1** a measured, pre-registered bound on one-step look-ahead headroom over cost-aware greedy touch selection
     under travel cost (H3);
   - **C2** a controlled learnability comparison of planner distillation (DAgger) vs RL (PPO) with an identical
     belief-free relative head, including a label-fit / belief-input diagnosis;
   - **C3** a test of distillation vs RL on RL's own objective (H2: rejected);
   - **C4** two measurement notes: evaluator grid resolution moves success outcomes, and per-decision latency with its
     component split.
   - A one-line pre-registration statement goes at the end: the row-4 outcome was written before the run.

**Evidence links.** `12_g2_analysis.k12` (G, ub95, abs_gap_nats); `12_d3_analysis_rem.succ`;
`14_m4_analysis.diffs["student-gstar:success"]`, `["gstar-rl:success"]`; `14_h2_analysis.bootstrap`;
`14_labelfit.groups.remedy`; `12_lat_analysis.ratio_full_over_student`.

---

## 3. Related work (target 300 words; three compact paragraphs)

**Goal.** Place C1 against the greedy-vs-planning literature, C2/C3 against amortized experimental design and tactile
RL, and the task against tactile localization. Every paragraph ends with the gap that this paper's question fills.

1. **Tactile localization and next-best-touch (about 100 words).**
   - Estimation: `petrovskaya2011global`, `koval2015pose`, `bauza2023tac2pose`.
   - Information-driven selection: `hebert2013next`, `zheng2024bayesian`, `zheng2026bayesian`, `gordon2026active`,
     `kamtikar2026tactful`.
   - Cost-aware IG: `ottenhaus2018active`.
   - Survey: `seminara2019active`.
   - **Gap:** per-step (myopic) selection is the norm; its headroom under travel cost and its per-decision compute are
     rarely measured.
2. **Greedy vs non-myopic information gathering (about 80 words).**
   - `javdani2012efficient`, `vien2015touch`, `chen2015submodular`, `esfandiari2019adaptivity`.
   - **Gap:** guarantees assume submodular structure that travel cost can break, so we measure headroom directly (H3).
3. **Amortized and learned active sensing (about 120 words).**
   - BED amortization: `foster2021deep`, `ivanova2021implicit`, `blau2022optimizing`, `hedman2025step`,
     `iqbal2024recursive`, `huang2026aline`, `rainforth2024modern`.
   - Tactile RL: `riou2021seeing`, `riou2024reinforcement`, `niemann2024when`, `xu2023tandem3d`, `fleer2020efficient`.
   - Benchmark: `schneider2025tactile`.
   - **Gap:** RL vs supervised distillation of a validated planner, compared on the RL objective with the same head.

**Missing cards (must not be cited until added and verified in stage 8.5/23).**
- DAgger (Ross et al.).
- PPO (Schulman et al.).
- Imitation of information-gathering oracles (Choudhury et al., RSS 2017).
- arXiv:2405.15031 (named in 07_hypotheses_v3 §3.1).

Until a card exists, the draft writes "DAgger"/"PPO" without a citation and leaves a `[CITE-MISSING]` marker.

---

## 4. Problem and methods (target 850 words)

**Goal.** Give a complete technical description of the task, the cost-aware greedy planner, the headroom estimator and
the two amortized learners. Describe the technical approach, not a workflow.

**Constants.** Design constants (object geometry, noise, success tolerances, contrastive L/J, DAgger round sizes,
learning rates) are quoted from the frozen design documents (`docs/07_hypotheses_v2.md` §1.1–§1.4,
`docs/07_hypotheses_v3.md` §1.2, §1.6, §2.1, §2.2, `docs/07c_amendment_v3_0.md`). They are design inputs, not results.
The drafter copies them verbatim from those sections.

### 4.1 Task and belief (about 200 words)

- **State:** s = (k, x, y, θ), a planar polygon of identity k from a library (set S, near-symmetric pairs), with an
  unknown planar pose.
- **Finger:** sits on a stand-off circle at angle φ_t.
- **Action:** a = (φ′, ψ) on a 64 φ′ × 8 ψ grid (512 actions). The finger travels to φ′ and then probes in direction
  φ′ + π + ψ.
- **Travel cost:** c(a) = 1 + κ·|Δφ|/π strokes. The episode has a time budget τ_κ, an action is feasible iff
  c(a) ≤ τ_rem, and the episode ends when τ_rem < 1.
- **Probe matching:** budgets are probe-matched so that G\* executes n\* probes on average at every κ. Cal′ verification:
  `12_cal_analysis.verify.S_k12` (mean probes 3.96 for n\* = 4).
- **Observation:** a contact point and normal with Gaussian noise, or a miss, under an ε-softened likelihood.
- **Belief:** a particle filter over (k, x, y, θ).
- **Metrics (equations):**
  - success = correct MAP identity ∧ position and rotation within tolerance, modulo symmetry;
  - ball information BI = log P̂(B(s₀) | h) − log P(B(s₀)), in nats.
- **Equations:** c(a); the feasibility mask; the BI definition.

### 4.2 Cost-aware greedy planner G\* (about 120 words)

- G\*(b) = argmax over feasible a of EIG_B(a; b) / c(a). EIG_B is the expected gain in ball information, estimated by
  nested Monte Carlo on an online PF.
- Full-size configuration (N, C, M) = (2,000, 512, 64).
- At each decision G\* exports the full score vector s(a) = max(0, EIG_B)/c(a). This vector is the distillation target.
- **Equations:** the G\* argmax; s(a).

### 4.3 One-step look-ahead headroom estimator (about 150 words)

- G(κ) = (mean V_LA − mean V_G\*) / mean V_LA over G\*-reached beliefs.
  - V is the expected remaining-budget ball information.
  - V_LA takes the best first action under rollouts completed by a **reduced greedy** (N_LA = 500, 128 candidates,
    M = 16; 07c C12) and uses common random numbers.
- G(κ) is dimensionless. It is **one-step-deviation headroom over a reduced greedy completion**, not the gap to the
  optimum (binding, S5).
- **Instrument checks** (all must pass for Hold):
  - (a) a notch construction with a known exact gap;
  - (b) a zero-gap bank;
  - (c) a travel-notch;
  - a bias check of V_G\* against an independent full-G\* rollout.
- **Equation:** G(κ).

### 4.4 Amortized policies with one shared head (about 280 words)

- **Shared architecture.**
  - A belief-free, finger-relative DeepSets head. Input: the touch history in the finger frame, the finger angle and the
    remaining-budget fraction.
  - Output: 512 masked logits.
  - Identical for both learners. This is the controlled variable of C2/C3.
- **Distillation (student).**
  - Loss: soft cross-entropy to softmax(β_T·s(a)/σ_s) over feasible a, plus λ·CE to G\*'s argmax.
  - Data: round 0 on G\* rollouts, then two DAgger rounds (mixing β = 0.5, then 0) with G\* labels at student-visited
    beliefs.
  - Hyperparameters were selected on held-out floored normalised regret R̄; the stopping rule also uses R̄. No
    success-based selection.
  - Remedy (pre-registered, applied once): round 0 and both DAgger rounds doubled. End-of-round-2 training decisions
    went from 7,957 to 17,083 (`14_labelfit.groups.first_attempt[].train_decisions`, `.remedy[].train_decisions`).
- **RL (PPO).**
  - Same head and action set. The reward telescopes to ball-sPCE g_T, a contrastive lower bound on terminal ball
    information, so **g_T is RL's own objective**.
  - Training length: 200,064 episodes per seed (`14_h2_analysis.rl_training.*.episodes`).
  - Learning rate selected from a 4-config sweep (`12_rl_sweep_selection`, selected cfg 2). That selection was made on
    the trainer's `val_v2` stream, which is stated as a deviation.
- **Belief-input control.** The same recipe with a 48-feature PF summary replacing the history encoder, trained on
  first-attempt-size data. It is used only by the encoder sentence.
- **Equations:** the distillation loss; the floored normalised regret r = r_u / max(s_max − s_med, ρ·s_max); the g_T
  definition (refer to the BED card `foster2021deep` for sPCE).

### 4.5 Baselines (about 100 words)

- **Random** with the feasibility mask.
- **Three heuristics** with a budget-reservation rule:
  - B-spread (belief-free, angular spread);
  - **B-fan** (belief-free, **travel-nearest**: stays at φ_t when allowed, cycles ψ, otherwise moves to the nearest
    allowed φ′);
  - B-cov (belief-using coverage).
- H★ for S12 is B-fan (`12_g5_analysis.cells.S12.H_star`), selected on pilot3 and frozen.

---

## 5. Experimental protocol (target 300 words)

**Goal.** Show that every claim comes from a frozen, pre-registered rule, and give the reader the gates in one table.

**Content.**
- **Pre-registration.**
  - The hypotheses, thresholds, outcome map (rows 1–4) and not-allowed list were frozen before any test3 episode
    (07c freeze note).
  - Row 4 was reached through the gates: D3 failed twice, and H1-fb was withdrawn at Lat′.
- **Cell.** Set S, κ = 12, n\* = 4 (`12_cal_analysis.n_star.S.n_star`). H3 also uses κ ∈ {0, 2}.
- **Splits.**
  - pilot3: G5′ margins and H★.
  - val3: 500 episodes, for D3 and the D3 remedy.
  - test3 0–499: H2 g_T.
  - test3 0–299: the M4 success and BI rows.
  - All splits are disjoint, and all methods are paired on the same episodes.
- **Evaluator.**
  - An adaptive grid posterior. E′ failed (`12_e_analysis.counted_flips` = 1, `.passes` = false), so sub = 8 is used
    everywhere.
  - Each read-out costs `12_e_analysis.mean_wall_s_sub8` (40.6 s); use the M8 sentence.
- **Statistics.**
  - Crossed episode × seed bootstrap, B = 10,000 (`14_h2_analysis.bootstrap.n_boot`). One-sided 95 % bounds unless
    labelled.
  - One test per claim. There is no correction across claims; the analysis §3.3 justification is one sentence.
  - The M4 intervals are descriptive, not tests.
- **D3 rule.** One sentence plus a formula: (i) Δ̂_succ ≥ max(−2 pp, −δ + 1.645·SE·√0.5); (ii) the same for BI with the
  −0.15 floor; (iii) every seed > −δ. δ_S12 = 0.04 (`12_d3_analysis_rem.delta_S12`).
- **Margins.**
  - ε_S12 from `12_g5_analysis.cells.S12.eps_c`.
  - Footnote: the D3 files carry a stale `eps_S12` (0.314266 vs 0.314507). It cannot move the −0.15 floor.

**Table 1 (gate and decision table)** is placed in this section. Its rows are listed in §9 (R1–R5).

---

## 6. Results (target 950 words)

### 6.1 H3: one-step look-ahead headroom is small (about 250 words)

**Goal.** Answer research question (1) with the pre-registered Hold verdict and its instrument support, and state the
bias caveat honestly.

**Content.**
- Hold, using the S5 sentence: G(12) = 0.01624, UB95 0.02210 < 0.03, margin 0.0079.
- The absolute gap is 0.041 nats on a mean V_G\* of 2.506.
- The ordering G(0) ≤ G(2) ≤ G(12) holds.
- "LA differs from G\*" is not headroom: LA ≠ G\* in 0.62 of beliefs while the mean gain is small, a pattern that fits
  near-ties among the top actions. Phrase this as "consistent with", not "shows".
- Instrument checks:
  - G1′ (a) 0.8290 in band;
  - (b) 0.00254, UB 0.00374;
  - (c) 0.7438 vs exact 0.7166.
  - Note that (a) and (b) are identical to v2, so they are not independent evidence.
- The bias sentence S4, verbatim.

**Evidence links.**
- `12_g2_analysis.k0` / `.k2` / `.k12`: `G`, `lb95`, `ub95`, `abs_gap_nats`, `mean_v_la`, `mean_v_greedy`,
  `frac_la_differs`, `n_no_budget_left`.
- `12_g2_analysis.H3`: `region`, `downgraded`, `ordering_G0<=G2<=G12`.
- `12_g2_analysis.bias_check`: `ratio`, `mean_estimator_v_greedy`, `mean_reference_v`, `n_floored_rollouts`.
- `12_g1_analysis.a.mean`, `.a.band`; `.b.mean`, `.b.ub95`; `.c.mean`, `.c.exact`.
- Cards: `javdani2012efficient`, `chen2015submodular` (the interpretation of greedy competitiveness).

**Figure 2(a)** plots this subsection (see §10).

### 6.2 Learnability: distillation and RL vs the greedy teacher (about 350 words)

**Goal.** Answer research question (2), part 1: can the greedy planner be amortized by either learner with this head?

**Content.**
1. **D3 (val3, 500 paired episodes, the binding evidence).**
   - First attempt: Δ̂_succ −5.87 pp vs threshold −1.43 pp; Δ̂_BI −0.199 vs −0.15; seeds −4.2 / −8.0 / −5.4 pp.
   - Remedy: −4.40 pp vs −1.68 pp ✗; BI −0.096 vs −0.15 ✓; seeds −4.6 / −4.6 / −4.0 pp ✗.
   - Seed 503 sits exactly at −δ. The verdict does not hinge on it, because rule (i) fails by 2.7 pp.
   - The change between attempts uses the M1 sentence (not tested).
2. **Test3 0–299 (descriptive).**
   - Success, BI and probes for G\*, the student and RL; paired diffs.
   - Student − G\*: use S7 ("significant one-sided only").
   - G\* − RL: +7.0 pp, ci95 [+0.22, +13.67].
3. **Label-fit diagnosis and encoder sentence.**
   - All six history students fit by the rule: train top-1 0.511–0.534, R̄ 0.169–0.206.
   - Held-out top-1 is below 0.50 for 4 of 6.
   - Use the analysis §2.2 "Allowed wording" verbatim: "Students fit the teacher's training labels to the
     pre-registered criterion (top-1 0.51–0.53) but fail validation; the label-fit rule assigns this to generalisation
     rather than capacity. The held-out regret is measured on teacher-visited states, so covariate shift is inferred,
     not observed."
4. **Belief-input control.**
   - Under-fit (train top-1 0.327–0.362) and D3-B fails (−20.1 pp, −1.01 nats, on 295 of 300 episodes; use the M6
     bound).
   - It isolates nothing about the representation. It shows only that this 48-feature summary, trained on
     first-attempt-size data, is a worse input than the relative history.

**Evidence links.**
- `12_d3_analysis.succ.delta_hat` / `.threshold` / `.per_seed`; `12_d3_analysis.bi.*`; `12_d3_analysis.seeds_ok`.
- `12_d3_analysis_rem.succ.*`, `.bi.*`, `.seeds_ok`, `.passes`.
- `12_d3_analysis_belief_student.succ.delta_hat`, `.bi.delta_hat`, `.n_episodes` (295), `.complete` (false).
- `14_m4_analysis.rows.gstar|student|rl` (`success`, `ball_info`, `probes`, `per_seed_success`).
- `14_m4_analysis.diffs["student-gstar:success"]`, `["student-gstar:ball_info"]`, `["gstar-rl:success"]`,
  `["gstar-rl:ball_info"]`.
- `14_m4_analysis.gap_closure_reported` (false; state that it is withheld by rule).
- `14_labelfit.groups.first_attempt`, `.remedy`, `.belief_input` (`train_top1`, `train_R_bar`, `heldout_top1`,
  `heldout_R_bar`, `under_fit`).

**Table 2** carries items 1–2. The label fit goes into the text, or into a 3-row compact sub-table if space allows.

### 6.3 H2: distillation vs RL on RL's own objective (about 200 words)

**Goal.** Answer research question (2), part 2: does dense planner supervision beat RL on the objective RL optimises?

**Content.**
- g_T: student 5.3678, RL 5.3676; Δ +0.00023 nats; one-sided 95 % bounds [−0.3103, +0.3034]. H2 is rejected.
- Fail-branch reading: "dense supervision does not improve on RL with this head", justified by the success ci95
  [−3.67, +8.78] pp containing 0.
- The M3 power sentence and m6 (no TOST).
- S1 for the overall comparison.
- S3 for BI (+0.289 nats, ci95 excludes 0) vs g_T. Present this as an observation, not a mechanism.
- Seed spread: use m2/m5. This is the likely source of the interval width, inferred from the per-seed SDs; no variance
  decomposition was done.
- **Report-only companion rows (now in the JSON, pre-registered as "reported with the test"):**
  - g_T(G\*) = 5.2993 and g_T(random) = 2.6182 on the same test3 0–499 episodes.
  - These carry **no interval and no test**. The draft states the values and does not rank G\* against the learned
    policies on g_T.
  - Reason: ball-sPCE is a contrastive bound, and grid BI orders G\* above both learned policies.
- RL plateau status: all three seeds ran to max episodes (200,064); the plateau rule fired at 102,400 / 102,400 /
  112,640 episodes.

**Evidence links.**
- `14_h2_analysis.student_mean`, `.rl_mean`, `.bootstrap` (`diff`, `lower`, `upper`, `p_greater`, `n_boot`,
  `n_seeds`), `.threshold_nats`, `.passes`.
- `14_h2_analysis.per_seed_student`, `.per_seed_rl`.
- `14_h2_analysis.g_T_gstar`, `.g_T_random`.
- `14_h2_analysis.rl_training.{511,512,513}.status|plateau_at|episodes`.
- `14_m4_analysis.diffs["student-rl:success"]`, `["student-rl:ball_info"]`.
- `14_m4_analysis.rows.rl.probes`, `.rows.student.probes`.
- Cards: `blau2022optimizing`, `foster2021deep` (RL / contrastive-bound BED context).

### 6.4 Learned policies vs a travel-nearest heuristic (exploratory, about 100 words; paired row still running)

**Goal.** Bound every "learning" sentence. The paired B-fan row on test3 0–299 is still running, so the draft carries
both pre-written readings and keeps only the one that occurs.

**Content.**
- Context, always included:
  - G5′ flat screen in S12 (`flat_screen: true`).
  - B-fan pilot3 success 0.4026 ± 0.0396 (n = 154 of 200), within its SE of G\*'s pilot3 0.426 (m4 wording: unpaired).
- **If the paired row completes** (`14_m4_analysis.exploratory_b_fan.complete` = true), use exactly one reading
  (15_decision §4.1, 07c note):
  - **(a)** if `exploratory_b_fan["student-b_fan:success"].ci95` excludes 0 in the student's favour: "the distilled
    student exceeds a travel-nearest heuristic on test3 (exploratory)".
  - **(b)** otherwise: "on test3 the learned policies were not shown to exceed a travel-nearest heuristic; at n\* = 4
    the S12 task may be flat (exploratory, cf. G5′ flat screen)".
- **If the row does not complete** before the draft freeze: use the S2 sentence and move the gap into Limitations.
- Either way, the subsection states that this is **not** the dropped H1c test and does not change row 4.

**Evidence links.**
- `12_g5_analysis.cells.S12.b_fan` (`success`, `se_success`, `n`), `.cells.S12.gstar.success`, `.cells.S12.flat_screen`.
- Planned keys, written by `code/analysis_m4_v3.py`, not yet in the JSON:
  - `14_m4_analysis.exploratory_b_fan.success`, `.ball_info`, `.n_episodes`, `.complete`;
  - `exploratory_b_fan["student-b_fan:success"].ci95`, `["b_fan-gstar:success"].ci95`, `["rl-b_fan:success"].ci95`;
  - the same contrasts for `:ball_info`.

### 6.5 Per-decision cost (about 50 words, plus a footnote)

**Goal.** Quantify the amortization payoff that would exist if accuracy were matched, and explain why H1-fb was
withdrawn.

**Content.**
- M5 sentence: student 0.408 ms vs G\* full 0.9135 s per decision (about 2,200×, not at equal accuracy).
- S6 sentence: the 15.0 % PF floor bounds candidate pruning at about 6.7×; measured full / pruned-16 = 3.22.
- The M4 per-episode sentence is optional. Drop it first if space is short.

**Evidence links.**
- `12_lat_analysis.student_median_s`; `.methods.student.median|ci`; `.methods.g2000_512_64.median|ci|component_medians`
  (`t_assim`, `t_nb`, `t_score`).
- `.methods.pruned16.median|component_medians`; `.ratio_full_over_student`; `.ratio_full_over_pruned16`;
  `.H1_fb_active`; `.L_final.median`; `.protocol_complete` (false); `.ci_too_wide`.

---

## 7. Discussion and limitations (target 400 words)

**Goal.** Interpret C1–C4 together for the research question, and list every limitation that bounds the wording.

**Discussion (about 150 words).**
- Small one-step headroom (C1) means that a greedy teacher is a defensible amortization target at this budget. Yet
  neither learner was shown to recover it (C2), and dense supervision bought no detectable advantage on RL's objective
  (C3).
- The remaining gap is attributed to generalisation, in the weak form only.
- Possible next steps, framed as questions and not as results:
  - student-visited held-out evaluation;
  - a TOST for H2;
  - a variance decomposition;
  - more cells.
- Cards: `hedman2025step` (semi-amortization as a direction), `iqbal2024recursive`.

**Limitations (about 250 words; one sentence each, from analysis §4 and 15_decision §4.2).**
1. **Single cell.**
   - S12 only, n\* = 4.
   - S0 and A12 appear only as incomplete G5′ rows (m7).
2. **Evaluator not shown converged.**
   - E′ failed: M7 sentence; m3 flip rate (`12_cal_analysis.n_star_sub8.S.success_flip_rate_vs_sub4`).
   - No finer grid was checked.
   - M8 cost sentence.
3. **RL comparator selected off-protocol.**
   - The sweep was selected on the `val_v2` stream, with 50,048-episode sweep runs.
   - The selected config won by 0.919 nats (`12_rl_sweep_selection.rows[*].final_val_ball_spce`, `.validation_stream`).
4. **RL probe use differs.** RL executes 3.0 probes vs 4.0; travel is not reported.
5. **H3 scope.**
   - It measures a reduced greedy completion, not the optimum.
   - The bias direction of V_LA was not checked (S4).
   - G1′ (a)/(b) are identical to v2.
6. **Label-fit thresholds are coarse,** and the held-out set is teacher-visited.
7. **Latency.**
   - The Lat′ protocol is incomplete (six CIs > 10 %, two machines pooled).
   - L_ep was not measured.
8. **Cross-split comparisons are unpaired.** G\* success is 0.426 on pilot3 and 0.446 on val3 (`12_d3_analysis_rem.succ.gstar_mean`),
   against 0.4267 on test3.
9. **Missing pre-registered report items:** CPU-h including labelling; teacher noise-floor R̄ and tie fraction.
10. **The heuristic gap,** if R9 has not completed.

---

## 8. Conclusion (target 100 words)

**Goal.** Restate the answer to the research problem in four clauses:
- greedy leaves little one-step headroom (S5, short form);
- neither amortization route was shown to reach it (S7, short form);
- distillation did not improve on RL on RL's objective (non-detection);
- the learned head is far cheaper per decision but not at equal accuracy.

End with the pre-registration and single-cell scope. No new numbers.

---

## 9. Results rows and tables (every row that will appear, mapped to `results_v3.json`)

Legend: **[DEC]** = pre-registered decision; **[GATE]** = gate datum; **[REP]** = reported row, no test;
**[EXPL]** = exploratory; **[INC]** = incomplete at outline time.

### Table 1: pre-registered gates and decisions (Section 5; one row each)

| Row | Item | Keys | Tag |
|---|---|---|---|
| R1 | Cal′ n\* and verification (S: 0.605 → n\* 4; verify 3.96) | `12_cal_analysis.n_star.S`, `.n_star_sub8.S`, `.verify.S_k12` | GATE |
| R2 | E′ (mean \|ΔBI\| 0.0126; 1 counted flip; FAIL → sub 8) | `12_e_analysis.mean_abs_dBI`, `.counted_flips`, `.passes`, `.flips[0].mass_sub4/_sub8` | GATE |
| R3 | G5′ S12 (G\* 0.426, random 0.0754, D_c 0.351, δ 0.04, ε 0.3145; provisional) | `12_g5_analysis.cells.S12.{gstar,random,D_c,delta_c,eps_c,passes,complete}` | GATE, INC |
| R4 | Lat′ / H1-fb (3.22 < 10 → withdrawn) | `12_lat_analysis.ratio_full_over_pruned16`, `.H1_fb_active` | DEC |
| R5a | D3 first attempt (−5.87 pp vs −1.43; −0.199 vs −0.15; seeds) | `12_d3_analysis.succ`, `.bi`, `.seeds_ok`, `.passes` | DEC |
| R5b | D3 remedy (−4.40 pp vs −1.68 ✗; −0.096 vs −0.15 ✓; seeds ✗ → H1 dead) | `12_d3_analysis_rem.succ`, `.bi`, `.seeds_ok`, `.passes` | DEC |
| R5c | D3-B belief input (−20.1 pp; −1.01 nats; 295 of 300) | `12_d3_analysis_belief_student.succ`, `.bi`, `.n_episodes`, `.complete` | REP, INC |
| R6 | H2 (Δg_T +0.00023, LB −0.3103 vs > +0.10 → rejected) | `14_h2_analysis.bootstrap`, `.threshold_nats`, `.passes` | DEC |
| R7 | H3 (UB95 G(12) 0.0221 < 0.03 → Hold; bias ratio 0.957) | `12_g2_analysis.k12.ub95`, `.H3.region`, `.bias_check.ratio` | DEC |

### Table 2: test-set rows (Section 6.2–6.4)

| Row | Item | Keys | Tag |
|---|---|---|---|
| R8a | test3 0–299: G\* success 0.4267 / BI 6.2483 / probes 3.963 | `14_m4_analysis.rows.gstar` | REP |
| R8b | Student (remedied, 3 seeds): 0.3822 / 6.1996 / 4.0; per seed | `14_m4_analysis.rows.student` | REP |
| R8c | RL-relative (3 seeds): 0.3567 / 5.9102 / 3.0; per seed | `14_m4_analysis.rows.rl` | REP |
| R8d | student − G\* success −0.0444, ci90 [−0.0856, −0.0033], ci95 [−0.0933, +0.0056] | `14_m4_analysis.diffs["student-gstar:success"]` | REP |
| R8e | student − G\* BI −0.0487, ci90 / ci95 | `14_m4_analysis.diffs["student-gstar:ball_info"]` | REP |
| R8f | student − RL success +0.0256, ci95 [−0.0367, +0.0878] | `14_m4_analysis.diffs["student-rl:success"]` | REP |
| R8g | student − RL BI +0.2893, ci95 [+0.1170, +0.4652] | `14_m4_analysis.diffs["student-rl:ball_info"]` | REP |
| R8h | G\* − RL success +0.0700, ci95 [+0.0022, +0.1367] | `14_m4_analysis.diffs["gstar-rl:success"]` | REP |
| R8i | G\* − RL BI +0.3380, ci95 [+0.1585, +0.5196] | `14_m4_analysis.diffs["gstar-rl:ball_info"]` | REP |
| R8j | g_T column, test3 0–499: student 5.3678, RL 5.3676, G\* 5.2993, random 2.6182 (G\* and random: no interval) | `14_h2_analysis.student_mean`, `.rl_mean`, `.g_T_gstar`, `.g_T_random` | DEC (student/RL), REP |
| **R9** | **B-fan (H★) on test3 0–299, paired:** success, BI; student − b_fan, b_fan − G\*, RL − b_fan (ci95) | `14_m4_analysis.exploratory_b_fan.*` (planned keys, §6.4) | **EXPL, INC (running)**. Reading (a) or (b) pre-written; if not complete at freeze, the row is omitted and the S2 sentence plus a limitation are used |

### In-text rows (no table)

| Row | Item | Keys | Tag |
|---|---|---|---|
| R10 | Label fit, 9 students (train / held-out R̄, top-1, decisions, under_fit) | `14_labelfit.groups.*` | DEC input (encoder sentence) |
| R11 | H3 κ = 0 / 2 values, ordering, frac LA ≠ G\*, no-budget-left | `12_g2_analysis.k0`, `.k2`, `.k12`, `.H3["ordering_G0<=G2<=G12"]` | REP |
| R12 | G1′ (a)(b)(c) | `12_g1_analysis.a`, `.b`, `.c` | GATE |
| R13 | Latency medians and CIs: student, G\* full, pruned-16, L_final; component split | `12_lat_analysis.methods.{student,g2000_512_64,pruned16}`, `.L_final`, `.ratio_full_over_student` | REP (protocol incomplete) |
| R14 | RL training status and plateau | `14_h2_analysis.rl_training` | REP |
| R15 | RL sweep selection (cfg 2; `val_v2` deviation) | `12_rl_sweep_selection.selected_cfg`, `.rows`, `.validation_stream` | REP (limitation) |
| R16 | Pilot3 heuristic context: S12 b_fan, b_cov, b_spread, random; flat_screen | `12_g5_analysis.cells.S12.*` | EXPL, INC |
| R17 | Evaluator flip rate S0 sub 4 → 8 (0.075) | `12_cal_analysis.n_star_sub8.S.success_flip_rate_vs_sub4` | REP (methods note) |

---

## 10. Figure plan

### Figure 1 (schematic plus headline; full-width top of page 1, about 1/3 page height)

**The story.** One picture that sets the two research questions side by side:
- the depth question: how much does one-step look-ahead add over greedy cost-aware EIG?
- the amortization question: can a network replace the greedy planner, trained by distillation or by RL?

It also previews the answers: a small headroom bar, and two learned policies both short of the teacher.

**Visual elements (left to right; an image-generation prompt can be written from this).**
1. **Panel A, the task (schematic).**
   - Top-down view of a flat polygonal object (grey) inside a dashed square uncertainty box.
   - A thin circle around it is the finger's stand-off circle, with the fingertip as a small dark dot at angle φ_t.
   - A curved orange arrow along the circle leads to a new angle φ′, labelled "travel cost c(a) = 1 + κ|Δφ|/π".
   - A straight blue probe arrow points inward from φ′ toward the object, tilted by ψ, and ends at a contact marker
     with a short normal tick.
   - Faint semi-transparent ghost outlines of the object at alternative poses and identities show the particle belief.
2. **Panel B, three ways to pick the next touch (schematic block diagram).**
   - A belief cloud icon feeds three parallel lanes:
     - **(i) "Greedy G\*"**: particle filter → EIG/c scored over all 512 actions → argmax. Clock icon "0.91 s / decision" (`12_lat_analysis.methods.g2000_512_64.median`).
       Optional; only if the draft keeps the latency sentence; label it "per decision".
     - **(ii) "One-step look-ahead"**: the same scores plus a short rollout tree whose leaves are completed by a
       "reduced greedy".
     - **(iii) "Learned policy"**: the touch history (points in the finger frame) → DeepSets block → 512 masked logits.
       Two training arrows enter the block: a solid arrow "DAgger: dense score labels from G\*" and a dashed arrow
       "PPO: reward = ball-sPCE (g_T)".
   - Clean flat-vector style, two accent colours (blue = information, orange = travel), no text beyond the labels.
3. **Panel C, headline answers (small data inset, drawn from JSON, not generated).**
   - Left mini-plot: G(12) point and one-sided 95 % UB (`12_g2_analysis.k12.G`, `.ub95`) against a dashed line at the
     pre-registered 0.03 Hold threshold.
   - Right mini-plot: test3 success with paired-difference whiskers, three bars:
     - G\* (`14_m4_analysis.rows.gstar.success`);
     - student (`.rows.student.success`, whisker from `.diffs["student-gstar:success"].ci95`);
     - RL (`.rows.rl.success`, whisker from `.diffs["gstar-rl:success"].ci95`, sign-flipped).
   - If R9 completes, a hatched fourth bar for B-fan (`14_m4_analysis.exploratory_b_fan.success`), labelled
     "exploratory".

**Draft caption.**
> **Figure 1.** *Two questions about cost-aware touch selection.* (A) A finger on a stand-off circle chooses where to
> move (paying travel cost proportional to |Δφ|) and in which direction to probe; the belief is a particle set over
> object identity and planar pose. (B) We compare the cost-aware greedy planner G\* (EIG per unit cost), a one-step
> look-ahead that rolls out a reduced greedy completion, and a belief-free DeepSets policy trained either by DAgger on
> G\*'s dense scores or by PPO on ball-sPCE. (C) At κ = 12 (set S, n\* = 4), one-step rollout gains ≤ 2.2 % of the
> remaining expected ball information (one-sided 95 % UB), and neither learned policy was shown to reach G\*'s test
> success (paired intervals; single cell, preliminary).

### Figure 2 (data; one column, two stacked panels)

- **(a) H3 headroom vs κ.**
  - Points G(κ) with [lb95, ub95] for κ ∈ {0, 2, 12}, from `12_g2_analysis.k0|k2|k12.{G,lb95,ub95}`.
  - A dashed line at the 0.03 Hold threshold; a secondary marker for `frac_la_differs`.
  - Caption mentions the S4 bias caveat in one clause.
- **(b) Paired-difference forest plot (test3).**
  - Six rows from `14_m4_analysis.diffs.*` (success in pp, BI in nats, in two sub-axes), showing ci90 (thick) and ci95
    (thin).
  - Plus one row for H2 Δg_T with its one-sided bounds (`14_h2_analysis.bootstrap.diff|lower|upper`) and the +0.10
    threshold line.
  - Optional R9 rows in grey, labelled "exploratory".
  - Caption: "descriptive intervals except H2; no multiplicity correction; not tests".
- The dataviz skill is applied at plotting time.

---

## 11. Word budget and venue switch

| Section | Words |
|---|---|
| Abstract | 180 (not counted) |
| 1 Introduction | 550 |
| 2 Related work | 300 |
| 3 Problem and methods | 850 |
| 4 Experimental protocol | 300 |
| 5 Results | 950 |
| 6 Discussion and limitations | 400 |
| 7 Conclusion | 100 |
| **Body total** | **3,450** |

(Numbering in this table follows the paper. Outline sections 2–8 above correspond to paper sections 1–7.)

**If the owner picks RA-L or a workshop (15_decision §4.3 b), these parts grow:**
- the full label-fit table;
- G5′ context for all three cells;
- the latency Pareto over the greedy grid;
- the §4.1 task-4 analyses, if they were run;
- the per-episode latency paragraph.

The claims stay the same.
