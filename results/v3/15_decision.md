# Stage 15 · RESEARCH_DECISION (v3), fresh subagent, 2026-10-29

> System: "You are a research program lead making go/no-go decisions."
> Task (verbatim template): "Make a PROCEED, REFINE, or PIVOT decision from analysis. PROCEED: results are strong enough
> to write the paper. Proceed to stage 16. REFINE: hypothesis is correct but the experimental evidence has fixable
> weaknesses (more seeds, more conditions, an additional ablation, a baseline tuning pass). Stay on the same hypothesis;
> loop back to stage 13 with specific code changes. PIVOT: results contradict the hypothesis or reveal a more
> interesting question. Loop back to stage 8 with a new hypothesis informed by what was learned. Output markdown with:
> Decision, Justification, Evidence (with cited numbers from the analysis), Next Actions (specific stage and tasks)."
>
> `{analysis}` = `results/v3/14_analysis.md` (full; merged pass 1 + binding pass-2 corrections S1–S7, M1–M8, m1–m7).
>
> Context read: `docs/07_hypotheses_v3.md` (header, §1.7, §1.9, §4, §5, §6), `plans/stage_12_experiment_run_v3_main_row4.md`,
> `docs/08_experiment_plan_v3.yaml` (H★ entries), the status notes at the end of `docs/07c_amendment_v3_0.md`,
> `RESTRICTS.yaml` (compute), `PROGRESS.md` (tail), `results/v2/15_decision.md` (format).
> No run was made for this decision. Every number below is quoted from `14_analysis.md`; where pass 2 rewrote a pass-1
> sentence, the pass-2 wording is used.

---

## 1. Decision

**PROCEED to stage 16 with the pre-registered outcome-row-4 paper (characterisation), not a method paper.**

This is a conditional PROCEED. Before drafting, a short **record-completion step** (§4.1) must finish. It adds one paired,
exploratory heuristic row on test3 and moves report items that already exist into the JSON. It reopens no
pre-registered decision, adds no cell, κ level or seed, and trains no model.

**Labels the paper must carry** (from §5 / §6.2 of `07_hypotheses_v3.md` and the analysis conclusion):

| Claim | Label |
|---|---|
| H1 | dead at D3 (not tested on test3) |
| H1-fb | withdrawn (Lat′ ratio 3.22 < 10) |
| H2 | rejected (fail-branch reading: "dense supervision does not improve on RL with this head"; non-detection, not equality) |
| H3 | Hold |
| Encoder sentence | "generalisation / covariate shift, not capacity" (rule-permitted, weakly supported; covariate shift inferred, not observed) |

**Escalation.** Per the v3 header and §5, v3 is the last loop. The owner is told that row 4 occurred (already done in
run 7, per PROGRESS.md) and **decides the venue**:
- (a) RSS 2027 Stage 1 extended abstract (due 2026-12-04 AoE, ≤ 5 pages + references; methods complete, experiments may
  be preliminary);
- (b) RA-L / workshop.

This decision does not choose the venue. It makes the draft venue-neutral until the owner answers, and §4.3 says which
parts change with the venue.

---

## 2. Justification

### 2.1 How the stage-15 PROCEED hard rule is applied to a pre-registered characterisation paper

The stage-15 rule "primary metric difference statistically meaningful" is written for a method paper, where the primary
claim is "method X beats baseline Y". **In that literal sense it is not met, and no paper claiming a method is
justified.** No learned policy was shown to match or beat G\*, and H2 found no difference between student and RL.

Row 4 has no single primary metric difference. Its claims are the outcomes of pre-registered decision rules, each with
its own test, α and threshold (§1.9). I therefore apply the rule as follows. **Every claim in the paper must be the
outcome of a pre-registered decision rule that was evaluated as written, at its pre-registered α. The outcome must not
depend on incomplete data or a stale parameter. Its wording must stay within what the result licenses** (a non-detection
is reported as a non-detection, and a failed non-inferiority test as a failure, not as "worse").

Checked claim by claim:

| Claim | Pre-registered rule and outcome | Decisive? |
|---|---|---|
| H3 Hold | UB95 G(12) = 0.0221 < 0.03 (margin 0.0079); bias ratio 0.957 ≤ 1.02; G1′ (a)–(c) pass | Yes. The margin is outside the CI rule, and the bias guard is passed. |
| H1 dead (D3) | Remedy: Δ̂_succ −4.40 pp vs threshold −1.68 pp (rule i); seeds −4.6 / −4.6 / −4.0 pp vs > −4 pp (rule iii). First attempt −5.87 pp vs −1.43 pp | Yes. Rule (i) fails by 2.7 pp, so the verdict does not hinge on seed 503's tie. The stale ε_S12 (0.314266 vs 0.314507) cannot move the BI floor of −0.15. |
| H1-fb withdrawn | full / pruned-16 = 3.22 vs ≥ 10 | Yes. The structural bound is ≈ 6.7× even at zero scoring cost (pass-2 S6). |
| H2 rejected | LB(Δg_T) = −0.3103 vs > +0.10 | Yes as a rejection. It licenses only "no improvement detected"; 80 % power needed a true Δ ≈ 0.57 nats (pass-2 M3). |
| Encoder sentence | All six history students not under-fit (train top-1 0.511–0.534, R̄ 0.169–0.206) while D3 fails | It follows the rule mechanically. The paper must use the weak wording of analysis §2.2. |
| D3-B (report-only) | −20.1 pp on 295/300 | Yes. At most +2.0 pp can be added by the missing 5 episodes (pass-2 M6). |

Under this application the rule is **satisfied**. Every decision in the row-4 paper is settled, and each is settled by a
margin that the remaining incomplete inputs cannot change. What is *not* satisfied is any sentence of the form "learning
helps". The paper must not contain one unless the paired heuristic row of §4.1 supports it, and then only as an
exploratory observation.

### 2.2 Why not REFINE

REFINE requires "hypothesis is correct but evidence has fixable weaknesses". That does not hold here:
- **The primary hypothesis (H1) is dead by its own rule, after the one pre-registered remedy.** The remedy (round 0 and
  both DAgger rounds doubled) was the only allowed fix. v3.1 D8 forbids training new students.
- **More seeds, conditions or tuning are excluded.** "Promoting exploratory seeds", "adding cells", "changing H★ / R_b"
  and "choosing between RL and distillation on test data" are all on the not-allowed list (§5; frozen plan).
- **H2 is rejected, not under-powered by a fixable amount.** A design with enough power for the +0.10-nat rule would need
  a much smaller RL seed variance (per-seed SD 0.253 vs 0.077 nats). Changing the H2 design after the run is forbidden.
- **The weaknesses that remain are reporting gaps, not evidence gaps for a decision.** They are the missing companion
  rows, the paired heuristic row, the V_LA bias direction and the incomplete G5′ rows. None of them is a decision input
  (§3.3), so a stage-13 loop would add rows without changing any label.

### 2.3 Why not PIVOT

- **The pre-registration rules it out.** "No outcome triggers a fourth design" (v3 header, §5). Row 4 is the
  pre-written paper for exactly this outcome. A PIVOT would be a fourth design, which the programme has said goes to the
  owner, not to stage 8.
- **The results do not contradict the row-4 paper; they are its content.** The more interesting question in the record
  is whether the task is "flat" at this budget, i.e. whether a heuristic is as good as the learned policies. It is a
  characterisation question, and the row-4 paper can carry it as an exploratory observation (§4.1). It is not a new
  hypothesis that needs a new design.

### 2.4 What makes PROCEED sufficient for this paper, and what still blocks drafting

The row-4 paper is assembled from four pieces:
- H3 (settled);
- learnability of RL and distillation with the same encoder, with the label-fit / belief-input diagnosis (settled; D3,
  D3 remedy, D3-B, label fit and the M4 rows all exist);
- the H2 result (settled);
- the evaluator methods note (E′ failure, sub-4→8 flip rate).

All four are in hand. The analysis lists one item that blocks a specific family of sentences ("No learning claim of any
kind should be written until a paired heuristic row exists"; analysis §5, pass-2 S2). It is cheap, sits inside the
frozen cell, and is answered by §4.1, task 1. Without it the paper simply omits every learning-vs-heuristic sentence.

---

## 3. Evidence (numbers from `results/v3/14_analysis.md`)

### 3.1 Outcome routing to row 4
- D3 first attempt: Δ̂_succ −0.0587 vs threshold −0.0143; Δ̂_BI −0.1988 vs −0.15; seeds −0.042 / −0.080 / −0.054 →
  FAIL (i), (ii), (iii).
- D3 remedy: Δ̂_succ −0.0440 vs −0.0168 ✗; Δ̂_BI −0.0962 vs −0.15 ✓; seeds −0.046 / −0.046 / −0.040 ✗ → H1 dead.
- Lat′: G\* full / pruned-16 = 3.224 < 10 → H1-fb withdrawn. PF assimilation + neighbour lists = 15.0 % of G\*'s
  per-decision time, so pruning is bounded at ≈ 6.7× (pass-2 S6).

### 3.2 Pre-registered decisions still open under row 4, all now resolved
- **H3 Hold.** G(12) = 0.01624, UB95 0.02210 < 0.03. Ordering G(0) 0.00637 ≤ G(2) 0.01418 ≤ G(12) holds. Bias ratio
  0.9573 (20 beliefs, 3 floored). G1′ (a) 0.8290 in [0.573, 0.860]; (b) 0.00254, UB 0.00374; (c) 0.7438 vs exact 0.7166.
  Required wording (pass-2 S5): "one-step rollout over the reduced greedy completion gains ≤ 2.2 % of the remaining
  expected ball information at κ = 12 (S, n\* = 4; one-sided 95 % UB of G(12) = 0.0221)". The V_G\* under-read (0.087
  nats, no CI, different belief set) goes next to it with the pass-2 S4 sentence.
- **H2 rejected.** g_T student 5.3678 vs RL 5.3676; Δ +0.00023 nats; one-sided 95 % bounds [−0.3103, +0.3034];
  p_greater 0.4883. Student − RL success ci95 [−3.67, +8.78] pp contains 0 → fail-branch reading "dense supervision does
  not improve on RL with this head".
- **Encoder sentence.** History students: train top-1 0.511–0.534, R̄ 0.169–0.206 (not under-fit); held-out top-1 below
  0.50 for 4 of 6 (0.4833–0.4916). Belief-input students under-fit (train top-1 0.327–0.362) and fail D3-B (−20.1 pp,
  −1.01 nats).

### 3.3 Reported rows (no test; descriptive)
- M4, test3 0–299: G\* 0.4267 / 6.2483 nats / 3.963 probes; student 0.3822 / 6.1996 / 4.0; RL 0.3567 / 5.9102 / 3.0.
  - Student − G\* success −4.44 pp, ci90 [−8.56, −0.33], ci95 [−9.33, +0.56]. This is significant one-sided only (pass-2
    S7).
  - G\* − RL success +7.0 pp, ci95 [+0.22, +13.67].
  - Student − RL BI +0.289 nats, ci95 [+0.117, +0.465].
  - Gap closure is not reported (LB 0.0122 < 0.04).
- Latency, per decision: student 0.408 ms vs G\* full 0.9135 s (≈ 2,200×; G\* CI alone ≈ 1,900–2,300×). The Lat′
  protocol is incomplete (six CIs > 10 %; two machines pooled). L_ep was not measured.

### 3.4 The open weakness that bounds the paper's wording
- S12 b_fan (travel-nearest heuristic): 0.4026 ± 0.0396, n = 154 of 200 on pilot3 at sub 8. The student is 0.402 (val3)
  and 0.3822 (test3). These numbers are unpaired. "Nothing in the record shows the student beats it" (pass-2 S2).
  `flat_screen: true` in S12.
- G5′ sub-8 rows are incomplete: random n = 62 / 199 / 161 of 200; A12 b_fan and b_cov n = 0; S0 `H_star_success = −1.0`.
  The G5′ PASS is provisional (pass-2 m7). D_c ≥ 0.35 everywhere, so δ_c = 0.04 is unlikely to move.
- The evaluator is not shown converged: E′ FAIL (1 counted flip in 16), and the S0 sub-4→8 success flip rate is 7.5 % of
  200 episodes. This is the methods note.

---

## 4. Next actions

### 4.1 Record completion before drafting (stage-12 scope, no new design; target 2026-10-30 → 11-01)

These tasks add **report-only rows**. Each must be labelled exploratory or "report item" in the paper. Each is checked
against the not-allowed list:
- no metric, threshold, k, H★ or R_b change;
- no new cell or κ level;
- no RL-vs-distillation choice;
- no seed promotion.

Each goes into a short dated status note in `docs/07c_amendment_v3_0.md` **before** it runs, with both possible readings
written in advance.

1. **Paired heuristic row on test3 0–299 (S12, sub 8), the item the analysis names as most damaging.**
   - Run B-fan (the S12 H★ at G5′, unchanged) on the same test3 0–299 episodes. Use `eval3 --no-grid`, then
     `regrid3 --sub 8`, the same path as M2/M4.
   - Add `heuristic(b_fan) − student` and `heuristic(b_fan) − G\*` paired crossed-bootstrap rows to the M4 analysis
     (`code/analysis_m4_v3.py`, new contrast only).
   - Budget: about 300 × 40.6 s ≈ 3.4 CPU-h. It needs a 5-min pilot (RESTRICTS). The total budget is already above the
     12 h reading, so tell the owner before it runs.
   - **This is not the dropped H★ test (H1c).** H1c is defined only in cells where H1a passes. H1a was never reached, so
     no H1c decision exists to be made, and none is made.
   - Pre-written readings:
     - (a) if the student − b_fan ci95 excludes 0 in the student's favour: "the distilled student exceeds a
       travel-nearest heuristic on test3 (exploratory)";
     - (b) otherwise: "on test3 the learned policies were not shown to exceed a travel-nearest heuristic; at n\* = 4 the
       S12 task may be flat (exploratory, cf. G5′ flat screen)".
   - Either reading enters the paper as an observation, and neither changes row 4.
   - If the owner declines the compute, the paper omits every learning-vs-heuristic sentence and states the gap as a
     limitation.
2. **Move the existing pre-registered companion rows into `results_v3.json`, with provenance.** These are g_T(G\*) on
   test3 0–499 (from the M2 G\* actions via `gt3`; PROGRESS.md quotes 5.30), RL plateau status (PROGRESS.md quotes
   1.02–1.13 × 10⁵), and CPU-h including labelling. Until they are in the JSON they are not cited (analysis §1.3). The
   numbers in PROGRESS.md must not be quoted directly.
3. **Finish the gate data that is still running, without changing any verdict.**
   - G5′ sub-8 re-reads (random to 200 per cell; S12/A12 heuristics).
   - D3-B to 300/300.
   - Regenerate `12_d3_analysis*.json` with the current ε_S12 (0.314507), or footnote it.
   - If a G5′ completion changes δ_c or H★, the frozen values stand and the change is reported (§5 not-allowed list).
4. **Optional, only if cheap (≤ 2 CPU-h each); otherwise list as limitations.**
   - H3 V_LA bias direction on the same 20 bias-check beliefs (report-only; Hold is not re-decided).
   - A variance decomposition of the H2 bootstrap (episode-only vs seed-only).
   - A paired first-attempt-vs-remedy bootstrap on val3, so the wording can say "moved" with an interval (pass-2 M1).
   - Not to be run: a TOST for H2 or the student-visited held-out set (not pre-registered; state as limitations); L_ep
     and the final latency benchmark (dropped at freeze; the paper says "per decision" only); a sub-16 grid check
     (methods-note limitation).

### 4.2 Stage 16 (paper outline → draft), from 2026-11-01

- **Frame.** A characterisation of cost-aware information-gain touch selection under travel cost, with these
  contributions:
  - (C1) H3: small one-step headroom over the reduced greedy completion at κ = 12;
  - (C2) learnability: with the same relative DeepSets head, neither DAgger distillation nor PPO was shown to reach G\*,
    with the label-fit / belief-input diagnosis;
  - (C3) H2: no improvement of dense supervision over RL on RL's own objective;
  - (C4) the methods note on evaluator resolution;
  - (C5) the per-decision latency characterisation, with its caveats.
- **Wording binding.** Every interpretive sentence uses the pass-2 rewrites (S1–S7, M1–M8, m1–m7). In particular:
  - no "indistinguishable" or "same sPCE";
  - no "near-optimal";
  - no "2,000× per episode";
  - "significant one-sided only" for student − G\* on test3;
  - the encoder sentence in its weak form;
  - the H3 sentence with "reduced greedy completion" and "(S, n\* = 4)".
- **Limitations section** (from analysis §4): single cell, evaluator convergence, off-protocol RL selection stream
  (`val_v2`), incomplete Lat′ protocol, coarse label-fit thresholds, G1′ (a)/(b) identical to v2 (so not independent
  evidence), and cross-split comparisons.
- **Not to be written.**
  - A method claim of any kind, or any phrasing that implies H1, H1-fb or H2 passed.
  - "RL and distillation are equal".
  - A learning-vs-heuristic claim beyond the pre-written reading of §4.1, task 1.

### 4.3 Owner decision (escalation, requested now; needed by 2026-11-05 to keep the RSS option)

- **(a) RSS Stage 1 extended abstract (2026-12-04 AoE, ≤ 5 pp + refs).**
  - Lead with C1 and C2, and put C3 in one paragraph. C4 and C5 go in a short methods/limitations paragraph.
  - The "experiments may be preliminary" allowance covers the single-cell scope, and the abstract must say so.
- **(b) RA-L / workshop.**
  - The same content at full length, with all M4 rows, the label-fit table and the G5′ context.
  - Use the §4.1 task 4 analyses if they were run.
- **Default if the owner does not answer by 11-05:** draft for (a). It is the shorter document, and it can be expanded
  to (b) without new runs.

### 4.4 Not to be done
- No stage-8 loop and no fourth design. No REFINE loop to stage 13 for new students, seeds, cells, κ levels or an H2
  redesign.
- No re-running of H3 on another grid. No change to any frozen value (n\*, δ_c, ε_c, H★, R_b, thresholds).
- No promotion of any exploratory row (b_fan test3 row, D3-B, M4 diffs, the §4.1 task 4 analyses) to a decision.
