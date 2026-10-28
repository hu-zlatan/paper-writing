# Stage 8 v2 · Pass 1 — Proposer (fresh opus subagent, 2026-10-28)

> System: "You formulate testable scientific hypotheses."
> Task: "This is iteration v2. Previous results (v1 pre-run manipulation checks) showed no measurable look-ahead value
> for touch selection when every probe is reachable at equal cost, and no-contact outcomes were rarely
> decision-relevant; the research lead decided to PIVOT to (1) amortization as the guaranteed core claim and (2) a
> gated test of look-ahead under a travel/time-budget action model. Read results/v1/14_analysis.md and
> results/v1/15_decision.md for the evidence and the decision. Generate at least 2 falsifiable hypotheses from
> synthesis. Output markdown and for each hypothesis provide rationale, measurable prediction, failure condition.
> Synthesis: {synthesis}"
> `{synthesis}` = full content of `docs/06_synthesis.md`. Also read for feasibility: `docs/00_topic_init.md`,
> `docs/07c_amendment_v1_1.md`, `code/README.md`. No prior involvement in this project.

**Scope rule ("sushi, not curry").** Two core ideas, nothing more:
1. **Idea 1 — Amortization (guaranteed core):** H1 (H1a non-inferiority, H1b latency at matched accuracy).
2. **Idea 2 — Look-ahead pays when touches cost travel (gated):** H2 (H2a dose–response in κ, H2b mechanism).

Everything else (NC-input ablation, objective ablation total-state vs goal-oriented, L ablation, encoder ablation,
RL-success baseline, MuJoCo transfer) is a component row or supporting experiment, not a hypothesis. v1's H3
(planning for no-contact outcomes) is dropped as a claim: R_NC(S) = 0.03 < R_NC(A) = 0.07 (14_analysis §1.2).

---

## 0. Shared v2 setting

**Unchanged from v1** (existing code in `code/touchbed/`): planar SE(2) × identity state; known library sets **A**
(asymmetric) and **S** (near-symmetric); ε-softened contact/no-contact likelihood (`likelihood.py`); evaluation PF with
resample-move (`pf.py`); greedy PF-EIG and coverage baselines (`policies.py`); DeepSets policy + PPO with γ = 1 (total)
/ γ = 0 (myopic) (`train.py`); crossed episode × seed bootstrap and Holm (`stats.py`). L = 4095, E_train = 10⁵ with the
plateau rule, 6 core seeds (amendment A1).

**New in v2 (code to be written at stage 10):**
- **Action model.** The finger rests on a stand-off circle of radius R_s = 100 mm. Action a = (Δφ, ψ): travel Δφ along
  the circle, then probe with offset ψ. Cost c(a) = κ·|Δφ|·R_s / v_travel + stroke_time(hit/miss). An episode ends when
  a time budget τ is exhausted (an action whose cost exceeds the remaining time is not executed).
- **κ grid:** κ ∈ {0, κ_mid, κ_hi}, fixed once by a pilot so that ≈ 8–10 / 4–6 / 2–3 probes fit in τ. **κ = 0 is the v1
  free-repositioning model** (unit test: bit-identical outputs to v1 at κ = 0).
- **Policy input** for every learned method: belief-free touch history (as v1) + current finger angle φ + remaining
  time. Same input for total and myopic variants.
- **Objective / co-primary metric:** goal-oriented. Training reward = sPCE on the success-region ("ball") event;
  co-primary evaluation metrics = success rate and **ball information** (A2). Total-state sPCE is an ablation row.
- **Comparators:** random; coverage; **greedy PF-EIG** (κ = 0); **cost-aware greedy** (argmax EIG(a)/c(a), same nested
  MC, κ > 0); **online rollout planner** (2-step look-ahead completed by cost-aware greedy rollout; upper reference,
  200 episodes at κ_hi only); **sPCE-total** (ours); **sPCE-myopic** (γ = 0, same input, same cost-aware action space).
- **Evaluation:** paired episode states across methods; ≥ 1,000 test episodes per cell for primary cells; evaluation
  PF size fixed by gate G4 of 15_decision §4.2.

**Why this pair of ideas, and not more (feasibility).** Costs from A4 / the task brief: greedy PF-EIG ≈ 0.65 s per
decision; training ≈ 30–60 ms per episode at L = 4095 on CI runners (65–80 ms in the sandbox). One run at E_train = 10⁵
≈ 0.8–1.7 CPU-h. Minimum run set: H1 = sPCE-total × {A, S} × {κ = 0, κ_hi} × 6 seeds = 24 runs; H2 adds sPCE-total at
κ_mid and sPCE-myopic at {0, κ_mid, κ_hi}, on **set A only**, × 6 seeds = 24 runs. 48 runs ≈ 40–80 CPU-h of training,
plus greedy evaluation ≈ 8 cells × 1,000 episodes × ≤ 6 decisions × 0.65 s ≈ 9 CPU-h. If over budget, the H2 seed
count drops to 5 (the seed-robustness rule then becomes ≥ 4 of 5), never H1. This fits sharded GitHub Actions jobs
before the 2026-11-22 analysis date. MuJoCo transfer (H4) is not in the extended abstract.

---

## H1 — An amortized, goal-oriented sPCE policy is non-inferior to the strongest online greedy comparator and ≥ 100× cheaper per decision at matched accuracy (Idea 1)

**Rationale.**
- Gap 1 and Gap 3 of the synthesis: information-driven touch selection (hebert2013next, javdani2012efficient,
  gordon2026active, murali2022active) re-optimizes EIG on the belief at every decision, with cost ∝ particles ×
  candidates × outcome samples. No tactile card reports per-decision compute. Policy-based BED (foster2021deep,
  blau2022optimizing, vincent2022policy, hedman2025step) amortizes design selection into a forward pass, but has only
  been shown on scientific toy models.
- v1 evidence makes greedy the right opponent and non-inferiority the right claim. Greedy beats random by +64.3 pp (A)
  and +28.7 pp (S) at T = 3. No positive two-step gap over greedy was detected (G(S) = −0.033). So there is little
  accuracy headroom above greedy at κ = 0, but a lot of latency headroom: 0.65 s per decision for greedy against an
  O(d²) ≈ 3·10⁴ multiply-add forward pass (07b §2).
- The objective has to be goal-oriented. Total-state information is dominated by fine pose (mean max EIG₁ 3.07 nats
  for the full state vs 0.92 for identity, on the same S beliefs). L = 4095 caps the bound near −log P(success region)
  ≈ 8.1 nats (A1), so the bound is calibrated to the decision.
- Testing H1 at κ_hi as well as at κ = 0 makes the claim about amortizing *cost-aware* information gathering. Greedy
  becomes costlier there (EIG/c has to be evaluated over a travel-dependent candidate set), and that is the setting
  robots actually face.

**Measurable prediction.** Primary cells = {A, S} × {κ = 0, κ_hi} (4 cells). The comparator G* is greedy PF-EIG at
κ = 0 and cost-aware greedy at κ_hi, both at full size (N = 2,000 particles, C = 64 candidates as in v1).
1. **H1a (non-inferiority).** In every primary cell, success(sPCE-total) − success(G*) has a one-sided 95 % lower
   confidence bound > −4 pp (crossed episode × seed bootstrap). The ball-information ratio sPCE-total / G* has a lower
   bound > 0.95.
2. **H1a (beats naïve baselines).** In every primary cell, sPCE-total beats random and coverage on success (Holm-corrected
   p < 0.05 over the 8 comparisons), with ≥ 10 pp point difference.
3. **H1b (latency at matched accuracy).** Define G*_match as the smallest (N, C, outcome samples) configuration of G*
   whose success is within 1 pp of full-size G* (searched on a pre-registered grid on validation episodes). Median
   per-decision wall-clock on one CPU core at batch size 1: latency(G*_match) / latency(sPCE-total) ≥ 100 on both sets,
   at κ = 0 and at κ_hi. Also reported, without a threshold: the full-size ratio, the online rollout planner's latency,
   and break-even episodes (training CPU-time / per-episode saving).
4. **Seed robustness.** H1a holds for ≥ 5 of 6 seeds individually (point estimate > −4 pp).

**Failure condition.** H1 is rejected if any of these holds:
- (a) In ≥ 1 primary cell, the lower bound on success(sPCE-total) − success(G*) is ≤ −4 pp, or the ball-information
  ratio has a lower bound ≤ 0.95.
- (b) The matched-accuracy latency ratio is < 100× in any primary cell. This includes the case where a shrunk greedy
  stays within 1 pp of full-size greedy at a latency within 100× of the policy's.
- (c) sPCE-total does not significantly beat random and coverage in some primary cell.
- (d) Fewer than 5 of 6 seeds satisfy H1a.

If H1 fails only at κ_hi, the paper reports amortization as holding for free repositioning only. That is a partial
result and is labelled as such.

---

## H2 — Under a travel/time budget, a non-myopically trained policy beats the strongest myopic selector, and the advantage grows with travel cost κ while vanishing at κ = 0 (Idea 2, gated)

**Gate.** H2 is tested only if gates G1 (estimator recovers the exact notch gap within ±20 % and shows no negative bias
beyond −0.01 on zero-gap beliefs) and G2 (validated estimator on 100 cost-aware-greedy beliefs per κ: G(κ_hi) ≥ 0.10 with
one-sided 95 % lower bound > 0.05; G(0) ≤ 0.03; G monotone in κ) pass by **2026-11-12**. One attempt at the
pre-registered κ grid, plus at most one pre-registered κ_hi escalation. **Fallback (pre-registered):** if either gate
fails, H2 is not run. The paper reports, as a characterisation result with its CI, the validated look-ahead headroom
G(κ) at each κ ("look-ahead headroom over cost-aware greedy is ≤ X at κ = 0 and ≤ Y at κ_hi").

**Rationale.**
- Gap 2 (the myopic vs non-myopic gap for touch has never been measured) and Cluster 6 (greedy is near-optimal under
  adaptive submodularity, javdani2012efficient; adaptivity and non-myopia matter when hypotheses cannot be separated
  in one step, chen2015submodular, esfandiari2019adaptivity).
- v1 explains *why* no gap appeared. With free repositioning and precise contacts, any information a planner could
  "set up" with probe 1 can be bought by greedy at probe 2 at the same price. Actions do not constrain the future, so
  the problem is close to the adaptive-submodular regime where greedy is near-optimal. This is an informal argument, to
  be written up in the stage 8.5 note.
- Travel breaks this structure. The value of a probe now depends on where the finger will be afterwards. A myopic
  selector gets the most immediate EIG per unit time, but it can end up zig-zagging across the object or stranding the
  finger far from the region that distinguishes the remaining hypotheses (e.g. the two symmetry modes of an A shape).
  A total-objective policy that sees the remaining time can trade a lower-EIG nearby probe now for a cheaper route to
  the discriminating region. This is the budgeted / orienteering structure of informative path planning, where greedy
  is known to be weak. The literature for that claim is not in the 56 cards and has to be verified (≥ 3 references)
  in the skeptic pass before it is cited.
- **Proposer's addition: test against the strongest myopic opponent.** A γ = 0 policy trained on raw per-step EIG
  ignores cost, so beating it would be easy and uninformative. The pre-registered myopic reference M* is therefore the
  better (on validation episodes, chosen before test) of: (i) sPCE-myopic with γ = 0; (ii) cost-aware greedy PF-EIG.
  sPCE-myopic stays the primary *ablation*: same network, same input, only credit assignment differs. M* is the
  primary *claim* opponent.
- κ = 0 is a built-in negative control: it reproduces v1, where no gap is expected. A dose–response over κ is a
  stronger and more falsifiable claim than one contrast.

**Measurable prediction.** Set A, κ ∈ {0, κ_mid, κ_hi}, 6 seeds, ≥ 1,000 paired test episodes per cell.
Δ(κ) = metric(sPCE-total) − metric(M*).
1. **H2a (effect at κ_hi).** Success: Δ(κ_hi) ≥ 3 pp (point estimate) with one-sided 95 % lower bound > 0. Ball
   information: lower bound > 0. Both against M*. The same contrast against sPCE-myopic is reported as an ablation.
2. **H2a (dose–response).** The OLS slope of Δ_success on κ ∈ {0, κ_mid, κ_hi} (crossed bootstrap) has a lower bound > 0.
   Δ(κ_mid) lies between Δ(0) and Δ(κ_hi) (point estimates).
3. **H2a (negative control).** At κ = 0, Δ_success is equivalent to 0 under TOST with ±3 pp margins (both one-sided
   p < 0.05).
4. **H2b (mechanism, three predictions).**
   - P1: on 100 shared beliefs at κ_hi, the first action of sPCE-total has a lower immediate EIG₁ (per unit time) than
     cost-aware greedy, but a higher remaining-budget value under the G1-validated estimator, by ≥ 0.05 nats on average
     (lower bound > 0).
   - P2: on the analytic notch control, computed exactly on the 401-point grid, sPCE-total reaches ≥ 80 % of the exact
     optimum, while sPCE-myopic reaches ≤ the exact greedy value + 10 %.
   - P3: at κ_hi, sPCE-total travels less per nat of ball information than M* (lower bound of the difference > 0), and
     its routes have fewer direction reversals of Δφ (Wilcoxon, p < 0.05).
5. **Transparency (no threshold):** R_NC per κ, number of probes executed per episode, and the rollout planner's
   success and latency at κ_hi, as an upper reference for how much look-ahead headroom exists.

**Failure condition.** With the gates passed, H2 is rejected if any of these holds:
- (a) At κ_hi, the success lower bound of Δ is ≤ 0, or the point estimate is < 3 pp against M*.
- (b) The slope lower bound is ≤ 0. A gap that does not grow with κ is not attributable to travel.
- (c) TOST at κ = 0 fails *and* Δ(0) > 3 pp. Then the effect is not specific to travel, and a confound (e.g. the
  remaining-time input or the γ = 1 training dynamics) is the more likely cause. The objective ablation then decides.
- (d) H2b P1 or P3 fails while H2a passes. The advantage then exists but the proposed mechanism is not supported, and
  the paper must say so.
- (e) sPCE-total beats sPCE-myopic but not cost-aware greedy. The paper then claims only "non-myopic credit assignment
  helps a learned policy", not "learned look-ahead beats the best myopic selector".

If the gates fail, H2 is neither confirmed nor rejected. The fallback characterisation is reported instead (see Gate).

---

## Mapping to synthesis gaps, success criteria and dates

| item | synthesis gap | 00_topic_init success criterion | in extended abstract (2026-12-04)? |
|---|---|---|---|
| H1a | Gap 1 | SC1 (match greedy, beat random/coverage) | yes |
| H1b | Gap 3 | SC1 (≥ 100× lower latency) | yes |
| H2a / H2b (or the fallback characterisation) | Gap 2, Cluster 6 | SC2 ("or the paper reports honestly that it does not") | yes, as one of the two |
| NC-input ablation (former H3) | Gap 4 (reframed) | SC3 component row | ablation table |
| objective / L / encoder ablations | — | SC3 | ablation table |
| MuJoCo transfer (former H4) | Gap 5 | SC4 | full paper only (2027-04-16) |

**Risks the skeptic pass should attack.**
1. **Greedy per unit cost may stay near-optimal.** Under budgeted adaptive submodularity, cost-benefit greedy has
   constant-factor guarantees, so G2 may fail. The fallback covers this.
2. **Novelty against informative path planning.** The contribution is the amortized sPCE policy for joint
   identity × pose touch under travel, not non-myopic IPP as such. This needs verified IPP and cost-aware BED
   references.
3. **Confounds in H2.** The remaining-time input and γ = 1 PPO variance differ in more than "credit assignment". This
   is mitigated by giving both variants the same input and by the κ = 0 TOST control.
4. **Evaluation PF convergence** (8k fails A3 in 6/6 cells in v1). G4 must pass before any H1/H2 number is reported.
5. **Matched-accuracy greedy search** must be pre-registered as a grid. Otherwise H1b is open to tuning the
   comparator down.
