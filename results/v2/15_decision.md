# Stage 15 · RESEARCH_DECISION (v2), fresh opus subagent, 2026-10-28

> System: "You are a research program lead making go/no-go decisions."
> Task (verbatim template): "Make a PROCEED, REFINE, or PIVOT decision from analysis. PROCEED: results are strong enough
> to write the paper. Proceed to stage 16. REFINE: hypothesis is correct but the experimental evidence has fixable
> weaknesses (more seeds, more conditions, an additional ablation, a baseline tuning pass). Stay on the same hypothesis;
> loop back to stage 13 with specific code changes. PIVOT: results contradict the hypothesis or reveal a more
> interesting question. Loop back to stage 8 with a new hypothesis informed by what was learned. Output markdown with:
> Decision, Justification, Evidence (with cited numbers from the analysis), Next Actions (specific stage and tasks)."
>
> `{analysis}` = `results/v2/14_analysis.md` (full), plus the **exploratory** addendum `results/v2/12_diag_analysis.json`
> → `k12.rel_sd400`. This is a finger-relative policy head (`code/touchbed/relframe.py`), 1 of 3 seeds finished, not
> pre-registered.
>
> Context read: `docs/07_hypotheses_v2.md`, `docs/07c_amendment_v2_0.md`, `results/v1/15_decision.md`,
> `docs/00_topic_init.md`, `AUTOPILOT.md` §1, `RESTRICTS.yaml`, `PROGRESS.md` (tail), `experiments/v2_dev_rel.json`,
> `experiments/v2_diag_k0k6.json`, `code/analysis_diag.py`, and the raw logs cited in §3.4.
>
> Numbers marked **[derived here]** were computed for this decision from raw result files already in the repository.
> No new run was made. They are descriptive and exploratory, and the file paths are given.

---

## 1. Decision

**PIVOT: loop back to stage 8 (v3).** This is the second loop decision of the project. The previous one was the
PIVOT v1 → v2.

**What is retired**
- **Idea 2 (learned look-ahead under travel).** It is *refuted in the tested range* by its own pre-registered gate row
  (G1 pass, G2 fail after the one escalation).
- **Training the amortized policy by RL on ball-sPCE.** As pre-registered, this is the method of H1. It failed
  learnability gate G3 after its one remedy. §4 then routes to "halt and go to stage 15 with learnability failure as
  the finding".

**What v3 tests.** Two core ideas, both informed by what v2 measured:

1. **C1, a measurement claim (characterisation, re-measured on the corrected action set).** The validated look-ahead
   estimator finds **almost no rollout-improvable headroom over cost-aware ball greedy G\***, even under travel cost.
   The same estimator does recover the exact headroom on a constructed notch control. "Plan ahead" therefore buys
   little in this task. G* is near the right target to amortize.
2. **H1′, amortized greedy.** A finger-relative DeepSets policy is **distilled from G\*** with supervised DAgger on G*'s
   full EIG_B/c score vectors. It is **non-inferior to G\*** in every informative cell and **≥ 100× cheaper per
   decision at its own accuracy**.
   - RL-on-sPCE (finger-relative head) stays in the paper as a pre-registered comparator row.
   - Its v2 failure (−20.6 pp at S12; f ≈ −0.005 on the notch) is reported as a finding, not hidden.

This keeps the owner's success criterion 1 (match greedy at ≥ 100× lower latency) as the headline. It answers criterion
2 honestly ("non-myopic training does not help here, and here is the validated reason"). It stays CPU-feasible and keeps
one or two clear ideas.

---

## 2. Justification

### 2.1 Why not PROCEED

All three hard requirements fail:

- **No statistically meaningful primary-metric difference against the best baseline exists.**
  - No v2 main run and no test episode exist (14_analysis §4.1).
  - The only learned-vs-G* evidence points the wrong way. At S12 the policy reaches 0.204 against G* 0.410 on 500
    paired validation episodes. Per-seed paired CIs are [−0.268, −0.170], [−0.228, −0.132] and [−0.270, −0.168].
- **No ablation has been run** for any component.
- **The gates that must pass before a main run do not pass.**
  - "No main run starts before G0, G3, G4 and G5 pass." None of the four passed cleanly as pre-registered
    (14_analysis §1.1).
  - G3 failed after its remedy. G4 failed as pre-registered and its fallback failed too. G5 failed flatness and lost
    A0. G0 records C(A) = 0.802 > 0.80.
- **No fabrication flags were raised.** The area-chair pass found no invented numbers. It did find integrity items that
  must be closed (§3.5), so the record is not paper-ready.

### 2.2 Why not REFINE

REFINE assumes the hypothesis is correct and the evidence is thin. Neither part holds.

**H2 (Idea 2) is refuted under its own rule.**
- G1 passed. G2 failed after the single permitted escalation, with G(12) = 0.0146 and UB 0.0208.
- The UB lies below even the 0.05 LB requirement, so more beliefs or seeds cannot rescue it (14_analysis §3.2).
- The pre-registered consequence is "refuted in the tested range; H2 policies are not trained".
- Re-measuring G2 to look for a pass would be a forking path.

**H1 as pre-registered is contradicted, not under-powered.**
- The H1 policy is the RL-trained sPCE-total policy. At S12 its success shortfall is 20.6 pp against a margin of
  δ_c = 4 pp, about 5×.
- Its BI shortfall is 1.19 nats against ε_c ≤ 0.32, at least 3.7×.
- The 2× remedy closes only +3.9 pp.
- The exploratory κ = 0 policies trail G* by 23.5–25.0 pp at equal probe counts (4.0 vs 4.0). The "free repositioning
  only" fallback label is not supported either.

**The single exploratory "fix" seed does not reach the gate.**
- The finger-relative head, seed 400, reaches 0.305 against G* 0.440 on 200 validation episodes:
  Δ = −13.5 pp, CI [−21.0, −6.5].
- Its BI is 5.789 against 6.380.
- The G3 (ii) threshold on these episodes would be 0.390 [derived here], so the seed misses it by 8.5 pp.
- It is one seed, not pre-registered, and it hit the E_train cap (`results/v2/dev_rel/rel_S_k12_sd400.json`:
  `status: max_episodes`).

**A REFINE would not be a seeds, conditions or tuning pass.** It would need all of the following:
- a new policy parametrisation;
- a new action set (the flatness failure forces 𝒜 = 64 × 8);
- an evaluator that §1.6/§4 never anticipated;
- re-calibration of n* and τ_κ, plus re-runs of G2, G3 (ii) and G5.

That is a re-design of the experiment. Under the routing rules it belongs at stage 8, not stage 13.

### 2.3 Why PIVOT, and why this pivot

Both PIVOT triggers apply:

- **The predicted phenomenon did not appear.** There is no look-ahead headroom, and no learned policy matches G*.
- **A more useful question emerged, with evidence behind it.**
  - The validated instrument says G* is within about 1.5 % of rollout-improvable value at κ = 12. Absolute gaps are
    0.015–0.049 nats on 2.6–3.0 nats of remaining value.
  - So the right amortization target is G* itself, not a non-myopic objective that RL cannot optimise on this budget
    (notch f ≈ −0.005, identical after 2× training).
  - Supervised distillation of a known-good teacher removes the failure modes v2 measured: credit assignment over the
    whole budget, 256- or 512-way exploration, and objective saturation. It keeps the latency story intact. G* has a
    recorded median of 0.84 s per decision on 32 × 8 against about 0.5 ms for a policy forward pass (§3.4).

**Options considered**

| Option | Verdict | Reason |
|---|---|---|
| (a) REFINE: keep RL-sPCE (H1 as titled), switch to the finger-relative head and 𝒜 = 64 × 8, retrain | **rejected as the primary route; kept as a comparator row** | The best available version is still 8.5 pp short of the gate and 13.5 pp short of G* on one seed. The κ = 0 deficit (−24 pp) shows RL fails even without travel. Betting the extended abstract on closing about 10 pp by 11-12 is not justified. It also requires the same re-design work as a pivot. |
| (b) **PIVOT to C1 + H1′ (distilled cost-aware greedy)** | **adopted** | Supported by validated measurements, and it targets owner criterion 1 directly. It reuses about 90 % of v2 code: the environment, G*, the grid evaluator, the relframe head, the look-ahead estimator and the stats. The teacher is the comparator, so non-inferiority is the natural claim. Risk: novelty against imitation-based information gathering (see §4.1). |
| (c) PIVOT to a measurement-only / negative-results paper (C1 + the RL learnability failure) | **pre-registered fallback** if the H1′ learnability gate D3 fails (§4.3) | Honest and fully supported by existing data. It is weak for RSS on its own, and it drops the amortization contribution. |
| (d) Change the topic or problem setting (new sensing model, 3D, MuJoCo) | rejected | It throws away validated infrastructure 37 days before the extended abstract. Nothing in the data asks for it. |

**Loop budget.**
- A PIVOT does not consume `loops.max_refine_cycles` (cap 3, which counts stage 13 ↔ 15 loops).
- This is still the second loop decision. If the v3 stage 15 is a third non-PROCEED decision, the main session should
  escalate to the owner (`escalate_on_cap_hit` spirit; see §4.6).

---

## 3. Evidence (numbers cited from 14_analysis unless marked)

### 3.1 Idea 2: refuted in the tested range (this becomes claim C1)

**G1 instrument passes.**
- (a) Mean relative gap 0.829, inside [0.573, 0.860]. The five runs are 0.8409, 0.7603, 0.8384, 0.8629 and 0.8425;
  the single run at 0.8629 is above the band.
- (b) On the zero-gap bank the mean is 0.00254 with UB 0.00374, n = 100.
- Exact notch values: V_opt = 0.615 and V_greedy = 0.174.
- The estimator gets V_LA nearly right (0.981 of exact) but under-reads V_greedy at 0.597 of exact. This bias inflates
  G, so the G2 refutation is conservative in that direction (§3.2).

**G2 headroom on S, 𝒜 = 32 × 8, 100 beliefs per κ.**

| κ | G | LB | UB | Absolute gap (nats) |
|---|---|---|---|---|
| 0 | 0.00494 | 0.00320 | 0.00714 | 0.0150 |
| 2 | 0.00797 | 0.00506 | 0.01183 | 0.0211 |
| 6 | 0.01849 | 0.01214 | 0.02660 | 0.0495 |
| 12 | 0.01462 | 0.00977 | 0.02081 | 0.0392 |

- The rule was G ≥ 0.10 with LB > 0.05. It fails on magnitude after the escalation.
- The look-ahead's selected action differs from G*'s on 41–58 % of beliefs, with a mean gain of only 0.015–0.049
  nats.
- The record does not separate near-ties from argmax-selection noise (AC row 3).

**Caveat that v3 must close.**
- The flatness failure voids 𝒜 = 32 × 8: at S12, ΔBI = +0.170 > 0.10.
- So the refutation formally holds only on the set that G5 rejected (14_analysis §5).
- C1 is therefore re-measured once on 64 × 8 with the frozen B6 estimator (§4.3, gate G2′). This is not a fishing
  re-run: its pre-registered outcome rule is written below before the run.

### 3.2 H1 as pre-registered: learnability failure

**G3 (ii), S12, 500 paired validation episodes, grid evaluation.**
- Policy success is 0.190 / 0.230 / 0.192, mean 0.204, against G* 0.410. The rule was ≥ 0.360.
- Under the 2× remedy it is 0.224 / 0.258 / 0.248, mean 0.243. Still FAIL.
- BI is 5.150 against 6.337. The policy executes 2.25–2.59 probes against G*'s 4.158.
- The 1× runs hit the 10⁵ cap. Under 2×, two seeds met the plateau rule (163,840 and 174,080 episodes) and one hit the
  cap (AC row 11).

**G3 (iii), notch.**
- v_π = 0.1770 / 0.1698 / 0.1688, which is 27.9 % of V_opt. The rule was ≥ 0.492.
- f = −0.005. All six policies (1× and 2×) choose a vertical first probe, and doubling training leaves the values
  identical.
- RL on the total objective did not learn the one set-up move whose value is exactly known.

**Exploratory diagnostics (absolute head, 200 validation episodes; κ = 0 policies are separate, undocumented-training
seeds 300/301).**
- κ = 0: −23.5 pp [−32.0, −14.5] and −25.0 pp [−34.0, −16.0] at 4.0 vs 4.0 probes.
- κ = 6: −13.5 / −19.5 / −17.5 pp.
- So travel overhead is not the only cause (AC row 2). This cannot be reported as confirmatory.

**Margin context.**
- δ_c(S12) = min(4 pp, 0.15 × 0.300) = 4 pp.
- ε_c ≤ 0.05 × 6.379 ≈ 0.32 nats.

### 3.3 Gates that bound what any next run must fix

**G4 / evaluator.**
- The pre-registered 32k × 3 MH kernel under-reads BI against the 128k reference by +0.063 to +0.177 nats in all four
  κ = 0 cells.
- The fallback fails on success: S +3.67 pp, CI [+0.83, +6.50].
- The grid was adopted under B8, which was not pre-registered. Its self-check passed: n = 8, mean |ΔBI| 0.0042,
  max 0.0259, 0 flips outside the tie band. That tie-band rule was relaxed after one observation.
- **The grid has never been checked at κ > 0.**

**G5.**
- Comparator strength passes everywhere. D(200) is A6 0.440, A12 0.365, S0 0.460, S6 0.415 and S12 0.300.
- A0 is degenerate: BI saturation 0.815 ≥ 0.50, and n*(A) = 3 cannot be lowered.
- Flatness fails at S12 (ΔBI +0.170) and at S6 (Δsucc −2.67 pp).
- **G5 S0 has n = 150, not 300.** G* success at S12 is 0.385 on the first 200 and 0.55 on the last 100 pilot episodes
  (AC row 8).

**G0.** C(A) = 0.802 (rule ≤ 0.80). B7 keeps the value and reports it.

**Missing pre-registered outputs:**
- G3 (iv), the ball-sPCE vs BI bias;
- G5 rollout-planner latency;
- G0 items (i) and (iv)–(viii) with commit hash;
- G4 pilot-policy and κ_hi cells.

### 3.4 Exploratory addendum: finger-relative head, seed 400 (S12, E_train 10⁵, hp1). Not confirmatory.

From `12_diag_analysis.json` (`k12.rel_sd400`, n = 200 validation episodes, the first 200):
- success 0.305 against G* 0.440, Δ −0.135 [−0.210, −0.065];
- BI 5.789 against 6.380;
- probes 3.0 against 4.175;
- 32 distinct first φ, against 4 for every absolute seed.

**[derived here]** On the same episodes 0–199, from `results/v2/grid_g3_val/S_k12_sd20{0,1,2}_sh*.jsonl`,
`..._2x_...` and `results/v2/dev_rel/val_rel_S_k12_sd400_grid.jsonl`:
- Absolute-head 1× seeds score 0.170 / 0.235 / 0.190. The relative − absolute paired differences are +0.135
  [+0.060, +0.210], +0.070 [−0.005, +0.140] and +0.115 [+0.040, +0.190] (percentile bootstrap, B = 10,000).
- The absolute 2× remedy seeds score 0.225 / 0.265 / 0.240.
- The relative seed always executes exactly 3 probes (200/200 episodes), against G*'s 4.175 mean.
  - **One probe is still lost to travel.** The parametrisation fixed the ignored-φ₀ symptom, not the budget use.

**[derived here]** From `results/v2/dev_rel/rel_S_k12_sd400.json`:
- Validation ball-sPCE is flat at 5.437–5.462 from 20,480 episodes onward.
- The run nonetheless ended with `status: max_episodes`.
- Training-objective saturation at the last logs is 0.164–0.320, above the G3 rule of < 10 %.
- **Reading.** The relative frame lifts success by about 7–13 pp on this seed, but RL still plateaus well below G*. This
  supports keeping the relative frame as the student architecture, and it does not support betting on RL.

**[derived here, informal]** G* decision latency:
- The median of `latencies_s` over 8,359 recorded G* decisions in `results/v2/g5/*gstar*.jsonl` is 0.840 s on 32 × 8.
- A learned policy's `latency_median_s` in `results/v2/g3_val/` is about 0.53 ms.
- This is not the pre-registered §2.3 protocol (no interleaving, no pinning). It is used only for costing §4.

**Seeds 401/402.**
- **Their read-out does not change this decision or its routing.**
- They are recorded as exploratory and enter v3 only through the pre-registered RL-relative comparator row (§4.1),
  which is retrained under v3 settings.

### 3.5 Integrity items (no fabrication; must be closed in amendment v3.0 before any v3 run)

1. B5 quotes the S diagnostic as +0.007. The JSON gives **−0.0066** (`S_k0_random_30mh_vs_128k3mh`).
2. The G4 note uses a 2 pp point tolerance. The rule is 1 pp, and all four success CIs leave ±2 pp.
3. The B8 note quotes 0.006–0.019 from partial data. The final JSON gives 0.006–0.014. It also states "S random 250"
   while the JSON has 300.
4. No script writes `12_g3_notch_analysis.json` or `12_g3_hp_selection.txt`. These are provenance gaps.
5. Run-4 numbers that are absent from any JSON:
   - validation ball-sPCE 4.85 / 5.03 / 4.96;
   - travel 0.54–0.63 rad;
   - the remedy plateau episodes. These are verifiable only from the raw logs.
6. Two post-observation rule relaxations:
   - the B2 per-shape rule;
   - the B8 tie band.

   Both are disclosed, and both must be stated in the paper as post hoc.
7. The 14_analysis AC rewrites (rows 1–17) are binding wording for any v3 text that cites v2 numbers.

---

## 4. Next actions

### 4.1 Stage 8 v3 (2026-10-29 → 10-31): `docs/07_hypotheses_v3.md`

Run the proposer → skeptic → methodologist debate with fresh subagents. Keep `07_hypotheses_v2.md` untouched as the
record and add a v2 → v3 change log citing this file. Start from the following.

**Global changes (all methods, frozen in amendment v3.0 before any v3 run)**
- **Action set.** 𝒜 = **64 φ′ × 8 ψ = 512** for all methods. This is the pre-registered flatness consequence, applied
  once.
  - The 64 × 8 vs 64 × 16 comparison at S12 is measured on 300 pilot episodes and reported. There is no further change.
- **Evaluator.** The adaptive grid posterior `gridpost.AdaptiveGridPosterior`, sub = 4, is pre-registered as *the*
  evaluation for v3. The tie-band flip rule is written into the pre-registration this time.
- **Cells.** {S0, S12, A12} are primary.
  - A0 is re-checked once under §1.7 on the 64 × 8 calibration and enters only if informative (expected: not).
  - **A cell that fails §1.7 is excluded from both success and BI parts.** This settles AC row 13.
- **κ_hi = 12.** There are no κ = 6 cells.
- **n\*, τ_κ** are re-calibrated on 64 × 8 with the §1.2 rule. S0 is topped up to 300 pilot episodes.

**C1: measured headroom claim (reported as a characterisation, with a kill condition)**
- **Instrument.** The B6-frozen G1 estimator, unchanged.
- **Measurement.** G(κ) on 100 G*-reached beliefs per κ ∈ {0, 2, 12}, S, 𝒜 = 64 × 8.
- **C1 holds iff** UB95(G(12)) < **0.05** **and** UB95(G(0)) < **0.03**.
- **Kill condition.** If G(12) ≥ 0.10, or its LB > 0.05, the paper may not say "greedy is near-enough". It reports the
  headroom and reopens Idea 2 for the full paper only.
- In the in-between case (UB ≥ 0.05 but LB ≤ 0.05) C1 is "inconclusive" and is stated with its interval.
- **Also reported.** The 32 × 8 values (§3.1), the notch control (exact 0.615 vs 0.174, estimator 0.829 relative gap),
  and the RL learnability finding (f = −0.005).

**H1′: amortized cost-aware greedy (primary hypothesis)**
- **Student.** The finger-relative DeepSets head (`relframe.py`) over the 512-action 𝒜 with the feasibility mask.
- **Teacher.** Full-size G* (N = 2,000, C = 512, M = 64).
- **Loss.** Cross-entropy to softmax(β · EIG_B(a)/c(a)) over feasible a, plus a top-1 term with weight λ.
- **Data.**
  - Round 0: 1,500 G* rollouts per cell, shared across seeds.
  - Then 2 DAgger rounds × 400 student-rollout episodes per seed, labelled by G* at every visited belief.
  - Mixing β_DAgger = 1, 0.5, 0.
- **Seeds.** 5 per cell. Seed rule: **≥ 4 of 5**. The reduction from 6 is justified by grid-evaluation cost (§4.5).
- **Hyperparameters.** At most 4 configurations of (lr, β, λ, batch), 1 seed each at S12. Selection on **validation
  top-1 agreement with G\*** only, never on success. Ties within 1 pp go to the lower index.
- **Measurable predictions** (v2 H1a/H1b machinery kept verbatim except where noted):
  - **H1′a, success.** In every informative cell, the one-sided 95 % LB of success(student) − success(G*) is
    **> −δ_c**, with δ_c = min(4 pp, 0.15·D_c) from the v3 pilot.
  - **H1′a, BI.** The LB of the BI difference is **> −ε_c**, with ε_c = min(0.05·BI_c(G*), 0.15·D_c^BI).
  - **H1′a, seeds.** ≥ 4 of 5 seeds have point Δ_success > −δ_c.
  - **H1′b, latency.** The boundary rung R_b (the most expensive ladder rung within 100× the student's measured
    latency, ladder rescaled to 𝒜 = 512) is worse than the student: the UB of success(R_b) − success(student) is < 0,
    with the §2.3 latency protocol.
- **Failure conditions.** H1′ is rejected if any of these holds:
  - (a) any informative cell has success LB ≤ −δ_c, or BI LB ≤ −ε_c;
  - (b) fewer than 4 of 5 seeds pass;
  - (c) any cell has R_b UB ≥ 0;
  - (d) fewer than 2 of the 3 primary cells are informative, in which case H1′ is "inconclusive on success".
  - A κ_hi-only failure means "rejected as titled". The paper then drops "cost-aware".

**Ablation and comparator rows (S12, 3 seeds, 500 test episodes, reported, no threshold)**
- (i) Absolute-frame student, same DAgger recipe. This is the ablation for the relative frame.
- (ii) Behaviour cloning only (round 0, no DAgger). This is the ablation for DAgger.
- (iii) RL sPCE-total with the relative head (hp1, E_train 10⁵, plateau rule). This is the v2 method, kept as a
  comparator.
- (iv) Random (200 test episodes per cell) and coverage, as Holm-corrected sanity checks.

An ablation row counts as "non-degenerate" only if its success differs from the student's by a paired 95 % CI that
excludes 0, or is reported as "no measurable contribution".

**Literature (stage 8 must do this).**
- Verify, then position against, imitation-learning approaches to information gathering. A candidate is "adaptive
  information gathering via imitation learning" (Choudhury et al., RSS 2017). **It is unverified, so do not cite it
  until it is checked.**
- Also verify DAgger (Ross et al., AISTATS 2011) and budgeted adaptive submodularity.
- If a verified prior work already distils greedy EIG for touch, H1′'s novelty statement must narrow to "cost-aware,
  validated-near-optimal teacher + latency at matched accuracy". The stage 8 skeptic decides this.

### 4.2 Amendment `docs/07c_amendment_v3_0.md`: frozen before any v3 run (commit hash in PROGRESS.md)

1. 𝒜 = 64 × 8; grid evaluator sub = 4 with the tie-band rule; the cell list and the A0 rule above.
2. The distillation recipe (round sizes, β schedule, loss, λ, HP grid, selection metric, label cap); the RL comparator
   settings; seeds; test sizes (1,000 paired per primary cell; 500 for rows; random 200).
3. Margins (δ_c, ε_c) are computed from the v3 pilot and frozen before test. The ladder is rescaled to C = 512
   (R0 512 → R7 32, nested).
4. The C1 rules (§4.1), and that the B6 estimator settings are unchanged.
5. Corrections of every item in §3.5, and two provenance scripts:
   - `analysis_g3_notch.py`, which regenerates `12_g3_notch_analysis.json`;
   - `analysis_g3_hp.py`, which regenerates `12_g3_hp_selection.txt`.

   Each must reproduce the existing file byte-for-byte or report the difference.
6. A statement that every v2 learned-policy number is a validation/pilot number, and that the κ = 0/6 diagnostics and
   relative seeds 400–402 are exploratory.

### 4.3 Gates (stage 11–12 v3, 11-05 → 11-12). No main run before G0′, E′, Cal′, G5′ and D3 pass.

| Gate | Check | Pass rule | If it fails |
|---|---|---|---|
| **G0′** hygiene | v2 G0 items (i) and (iv)–(viii) with commit hash; unit tests: 64 × 8 masks, relative ↔ absolute permutation round trip, soft-label CE gradient check, G* score-vector export equals G*'s argmax | All green in CI | Nothing downstream starts |
| **E′** grid at κ_hi | sub 4 vs sub 8 on 8 S12 and 8 A12 pilot episodes (4 G*, 4 student) | Mean \|ΔBI\| ≤ **0.02**; no success flips outside true-identity mass [0.45, 0.55] | sub = 8 becomes the evaluator; cost enters the downscale order |
| **Cal′** n*, τ on 64 × 8 | §1.2 rule, 200 pilot episodes per set (S0 topped up to 300 for G5′) | Verified probes within n* ± 0.3 | ≤ 3 bisection steps (as v2) |
| **G5′** comparator / non-degeneracy | G* vs random on 300 pilot episodes per primary cell; §1.7; 64 × 8 vs 64 × 16 at S12 reported | G* ≥ random + 10 pp; §1.7 (success ∈ [0.15, 0.90], D ≥ 20 pp, BI saturation < 50 %) | Cell removed (reported). Flatness is report-only, no second 𝒜 change. |
| **G2′** C1 measurement | §4.1 C1 | C1 rule as stated (a finding either way) | Kill or inconclusive label as stated; does not block H1′ |
| **D3** student learnability | S12, 3 seeds, chosen HP, full DAgger recipe; 500 validation episodes, grid | Seed-mean success ≥ success(G*) − **5 pp** **and** seed-mean BI ≥ BI(G*) − **0.30** nats; seed-mean top-1 agreement reported | **One remedy:** double round 0 and the DAgger rounds once (re-check by 11-14). If it still fails, **H1′ is dead**: switch to fallback (c), no main runs, stage 15 with learnability failure of both RL and distillation as the finding |
| **Lat′** | G* (512) and student latency, §2.3 protocol, 20 warm-up + 500 timed decisions | Recorded (it fixes R_b) | — |

### 4.4 Code changes (stage 10 v3, 11-01 → 11-05)

- `travel.py`: N_PHI 32 → 64 behind a flag. 32 remains reproducible, with a unit test.
- `policies_v2.py` / G*:
  - `score_vector()` export of EIG_B/c over feasible 𝒜 at every decision, written to the label shards (`.npz`);
  - the ladder rescaled to 512.
- New `touchbed/distill.py`:
  - dataset aggregation;
  - the soft-target CE + top-1 loss on the relframe head (backward pass reuses `RelDeepSets`);
  - the DAgger driver with `time_guard`;
  - a plateau rule on validation agreement (< 0.5 pp over 3 evaluations), with a hard epoch cap.
- `main.py`:
  - `label` (G* scoring of given beliefs/rollouts, sharded for Actions);
  - `distill`;
  - `eval2 --method student`.
- `analysis_c1.py` (G2′), `analysis_d3.py`, `analysis_v3_main.py`. The main analysis uses the existing
  `stats.crossed_bootstrap_diff`, `holm` and `seed_robustness` with B = 10,000.
- `analysis_gridcheck.py` extended to κ_hi (gate E′).
- The provenance scripts of §4.2-5.
- A TIME_ESTIMATE pilot (≤ 5 min) for labelling, distillation and grid evaluation before each sweep (RESTRICTS).

### 4.5 Compute envelope (CPU-h; re-checked by TIME_ESTIMATE)

**Unit costs.**
- G* label cost at 512 is about 1.7 s per decision. That is 2 × the recorded 0.84 s median on 256 [derived here].
- Grid evaluation costs about 7.4 s per G* episode and about 10.6–26.4 s per policy episode at S12 [derived here from
  the `wall_s` fields of `grid_g3_val` and `dev_rel`].
- Random grid episodes cost about 66–76 s (07c).

**Gates (≈ 45).**

| Item | CPU-h |
|---|---|
| Cal′ / G5′ | ≈ 10 |
| G2′ (3 κ × 100 beliefs at 2 × v2 cost) | ≈ 15 |
| D3 labels + training + validation | ≈ 12 |
| D3 remedy | ≈ 6 |
| E′ | ≈ 1 |

**Main (≤ 125).**

| Item | CPU-h |
|---|---|
| Labels: 3 cells × (round 0 + 5 seeds × 2 DAgger rounds) | ≈ 32 |
| Student training | ≈ 5 |
| Test grid evaluation, students (5 seeds × 3 cells × 1,000) | ≈ 50 |
| G* test (3 × 1,000) | ≈ 12 |
| Ladder R_b | ≈ 10 |
| Ablation / comparator rows | ≈ 15 |
| Random sanity (200 per cell) | ≈ 12 |

**Downscale order:**
1. random 200 → 100;
2. rows 500 → 300 episodes;
3. drop the report-only ladder walk;
4. drop coverage.

Primary seeds, cells and test sizes are never reduced.

### 4.6 Dated timeline (today 2026-10-28; extended abstract due 2026-12-04 AoE; full paper 2027-04-16 AoE)

| Dates | Stage | Work |
|---|---|---|
| 10-28 | 15 → loop | LOOP MARKER v2 → v3 in PROGRESS.md; snapshot per progress_tracking. Let relative seeds 401/402 finish; record them as exploratory only. |
| 10-29 → 10-31 | 8 | `07_hypotheses_v3.md` (debate) and `07c_amendment_v3_0.md` (§4.2), including the §3.5 corrections. Literature verification of imitation-based information gathering, DAgger and budgeted adaptive submodularity. |
| 11-01 | 9 | `08_experiment_plan_v3.yaml` and the compute envelope (§4.5). |
| 11-01 → 11-05 | 10 | Code (§4.4); G0′ unit tests green in CI. |
| 11-05 → 11-12 | 11–12 | Cal′ → G5′ / E′ → G2′ (C1) in parallel with D3. **Gate decision on 11-12**, or 11-14 if the D3 remedy is used. |
| 11-13 → 11-19 | 13 | Main runs. Freeze margins, R_b and test sizes first, with a commit hash. |
| 11-20 → 11-22 | — | Buffer: one re-run or one power enlargement. |
| 11-23 → 11-25 | 14–15 | v3 analysis and decision. |
| 11-26 → 12-03 | 16+ | Extended abstract (5 pages + 1 of references; method complete; v3 test results, or C1 + negative findings under the fallback). |
| 12-03 | — | Owner decides on submission (OWNER_TODO). |

**Fallback branch (pre-registered now).** If D3 fails after the remedy, i.e. on 11-14:
- No further pivot before the extended abstract.
- The abstract is written as fallback (c): C1 + the RL and distillation learnability results + the evaluator finding
  (SMC under-reads BI by 0.07–0.18 nats against the grid).
- The main session adds an OWNER_TODO item. The owner decides whether to submit that to RSS Stage 1 or retarget the
  venue.
- **Escalation rule.** If the v3 stage 15 returns anything but PROCEED, escalate to the owner before a third loop.

### 4.7 Not to be done

- **Re-running G2 on 32 × 8, or adding beliefs or κ levels, to look for headroom.** G2′ on 64 × 8 is a single
  pre-registered measurement.
- **Choosing between RL and distillation on test data, or promoting relative seeds 401/402 to confirmatory.**
- **Quoting v2 validation numbers as test results.** Also: never mix the three G* S12 success numbers (0.410 / 0.440 /
  0.385, different episode sets), and never cite `12_diag_analysis.json` k12 absolute entries as a replication of G3.
- **Starting any v3 main run before G0′, E′, Cal′, G5′ and D3 pass.**
