# Stage 15 · Research decision (v4)

> System (verbatim, `results/v4/prompts/stage15_system.txt`): "You are a research program lead making go/no-go
> decisions."
> Task (verbatim, `results/v4/prompts/stage15_user.txt`): "Make a PROCEED, REFINE, or PIVOT decision from analysis. …
> Output markdown with: Decision, Justification, Evidence (with cited numbers from the analysis), Next Actions (specific
> stage and tasks)." `{analysis}` = `results/v4/14_analysis.md` (merged pass 1 + binding pass-2 items S1–S3, M1–M3,
> m1–m9).
>
> Fresh subagent, 2026-11-01 (run 10). Context read: `RESTRICTS.yaml`, `results/v3/15_decision.md`,
> `docs/07c_amendment_v4_0.md`, `pipeline/references/stage_prompts/research_decision.md` (hard rules),
> `OWNER_TODO.md`, the stage 13/14 [v4] entries of `PROGRESS.md`, and the summary of `paper/mypaper/v3/20_quality_gate.json`.
> No run was made for this decision. Every number is quoted from `14_analysis.md`. Where pass 2 rewrote a pass-1
> sentence, the pass-2 wording is used. Numbers marked *(derived)* are my own arithmetic on listed values.

---

## 1. Decision

**PROCEED to stage 16, in the characterisation sense only.** The paper is the outcome-row-4 measurement paper (v3),
with the S2 rows added as one-cell exploratory evidence. It is **not** a method paper, and the template's PROCEED rule
is **not met in its method sense** (§2.1).

The other two options cannot be executed, and they would not be the right call even if they could (§2.2–§2.3):
- `RESTRICTS.yaml` sets `loops.max_refine_cycles: 3`, and v4 was cycle 3 of 3 (v1→v2, v2→v3, v3→v4; amendment v4.0
  "Why"). Because `escalate_on_cap_hit: true`, a REFINE or PIVOT would go to the owner as a request. It would not start
  a v5 loop.
- REFINE's precondition ("hypothesis is correct") is false. H1 is dead (v3), and D4 failed in S2.
- A PIVOT would be a fourth design. The v3 pre-registration excludes that ("no outcome triggers a fourth design").

**Escalation note (for the main session to file in `OWNER_TODO.md`; this decision modifies no other file).** The
refine-cycle cap has been reached without any method claim converging. The record therefore ends in row 4 for good. The
owner should know three things:
- (a) No further experiment loop is possible without the owner explicitly overriding `RESTRICTS.yaml`.
- (b) The default target stays the RSS 2027 Stage 1 extended abstract (due 2026-12-04 AoE, ≤ 5 content pages + 1
  reference page), unless the owner says otherwise.
- (c) Submission is still blocked by the open RSS LLM-policy question in `OWNER_TODO.md`.

---

## 2. Justification

### 2.1 The template's PROCEED hard rules, applied as written

| Hard rule (`research_decision.md`) | Status | Reason |
|---|---|---|
| Primary metric difference between proposed method and best baseline is statistically meaningful (p < 0.05, or effect > 0.5σ across seeds) | **Not met (method sense)** | See below. |
| Every claimed "effective component" has a non-degenerate ablation | Vacuous, so met | The paper claims no effective component. No sentence may claim one (§4.3). |
| No CRITICAL FABRICATION flags from stage 14 | Met | Pass 2 checked every v4 number against `results_v4.json` and the code. It reproduced all arithmetic and found "None" of the pre-registered verdicts wrong. Its items S1–S3, M1–M3 and m1–m9 concern interpretation, not fabrication. |

**Why the first rule fails in the method sense.**

1. **The student against its reference, G\*.** The pre-registered primary contrast is D4, the student against G\*. It
   fails clause (i): Δ̂_succ −2.80 pp against a threshold of −1.46 pp, a shortfall of 0.61 SE. On test3 the point
   estimate goes further in the wrong direction: −10.2 pp, ci95 [−16.6, −4.3].
2. **The student against the best non-oracle baseline, RL.** RL is the best baseline on S2 test3 success (0.4233,
   above B-fan's 0.3700).
   - The pre-registered H2-S2 contrast is not detected (LB −0.749 ≤ +0.10). Its point estimate favours RL by
     0.445 nats.
   - The paired success contrast is unresolved: +2.8 pp, ci95 [−4.1, +9.6].
3. **The effect-size disjunct, checked so it cannot be used selectively.** On test3 success the student − RL
   difference is +2.78 pp. The pooled per-seed sample SD is 3.10 pp (student 3.34, RL 2.84; *derived* from the per-seed
   values in §1.3). That makes the effect ≈ 0.9σ, which is formally above 0.5σ.
   - I do **not** count this as meeting the rule. It is not the pre-registered primary metric. It rests on 3 seeds per
     arm, so the SD estimate is very noisy. The paired crossed bootstrap, which accounts for episodes, contains 0. And
     it is one of 22 uncorrected exploratory intervals (analysis §3.4).
   - Picking the one favourable disjunct after seeing the data would break `forbid_unsupported_claims`.
4. **The student against B-fan.** This success contrast does exclude 0: +8.1 pp, ci95 [+1.7, +14.7]. But B-fan is not
   the best baseline, the contrast is exploratory, and its LB is the smallest margin in the block (pass 2 S1).

**The sense in which I do proceed.** I use the same standard as v3 (`results/v3/15_decision.md` §2.1). Every claim in
the paper must:
- be the outcome of a pre-registered rule, evaluated as written;
- not depend on incomplete data or a stale parameter;
- be worded within what that outcome licenses.

Otherwise the claim must be labelled as an exploratory observation with its interval. Checked for v4:

| Claim | Rule and outcome | Settled? |
|---|---|---|
| D4 → "not shown to reach G\* in S2 either" | (i) −2.80 pp < −1.46 pp ✗; (ii) −0.105 ≥ −0.15 ✓; (iii) −3.6 / −2.8 / −2.0 pp > −4 pp ✓. n = 500, complete, no remedy round | Yes. The failing clause is decided on complete data, and the amendment allows no remedy. (A true Δ = 0 would pass with probability ≈ 0.75 under this rule, analysis §3.2. That makes "not shown" the only licensed wording; "worse" is not.) |
| H2-S2 → not detected | LB −0.749 vs +0.10 | Yes. The LB is 0.85 nats, ≈ 2.9 one-sided half-widths, below the threshold (pass 2 m5). |
| E5 → reported at logged latency | No verdict by design | Yes, as a report. |
| v3 verdicts (row 4, H1 dead, H1-fb withdrawn, H2 rejected in S12, H3 Hold) | Unchanged (analysis §5) | Yes. |

All decision-bearing items are settled. The four open items carried from stage 14 are wording or report items, not
decision inputs (§2.4). Under this standard, a measurement paper is licensed. The template's PROCEED rule, read
literally, is not met. The paper must say so implicitly: it must contain no method claim.

### 2.2 Why not REFINE

- **The precondition fails.** REFINE assumes the hypothesis is correct. The amortisation hypothesis has now failed its
  learnability gate in two cells:
  - D3 in S12, twice;
  - D4 in S2, where the remedy recipe of 200 fixed epochs per round, the budget-matched recipe that stage 20 [v3] asked
    for, was used from the start.
- **The template default does point here.** The template makes REFINE the default when evidence is thin, and it is
  thin: one S2 cell, three seeds, no HP grid, and a val3/test3 gap that has no explanation (−2.8 vs −10.2 pp, widening
  on every seed; pass 2 M3).
- **But it cannot run.** The cap is reached (3 of 3), so a REFINE would only be an escalation.
- **And it would not change a label.** The fixes available inside a REFINE (more seeds, an S2 HP grid, a remedy round)
  are what the v4 amendment ruled out before the run ("No remedy round in v4"; "no new HP grid: deviation"). Adding them
  now would mean re-deciding D4 after seeing it fail.

### 2.3 Why not PIVOT

- The results do not reveal a new hypothesis to test. They extend the characterisation. v4 is in fact the answer to the
  v3 reviewers' central objection that S12 is stay-and-probe:
  - S2 travels as designed: G\* 46.9° per episode against 6.1° in S12.
  - The student is not confined to stay-and-probe (39.1°).
  - Learning still does not reach G\*.
- The more interesting question in the record is why g_T (ball-sPCE) and grid BI rank G\* differently in both cells. It
  is a methods observation for the paper, not a design to pivot to. It would also need a new pre-registration and a v5
  loop, which the cap and the v3 header forbid.

### 2.4 The four open items: none blocks drafting, each binds the wording

1. **The val3/test3 gap** (−2.8 vs −10.2 pp; widens on all seeds by 5.4 / 11.2 / 5.7 pp; G\* +3.9 pp and student
   −3.5 pp both move).
   - D4 is decided on val3 alone. It fails in either reading, so the gap cannot change a verdict.
   - The paper reports both splits side by side, using the pass-2 M3 sentence and the m6 caveat ("≈ 2.0 combined SE
     under independence, conservative; untested").
   - A cheap pipeline-vs-split diagnostic is optional (§4.1, task 3).
2. **The random anchor re-read** (190 of 300). It enters no contrast and no rule (analysis §3.2). Finish it, or report
   it with its n.
3. **"Student imitates travel."** Withdrawn. The pass-2 S3 wording is used: the student travels a similar *amount*, and
   its per-episode travel is weakly correlated with G\*'s (r 0.14–0.24). Those r values come from per-episode files, not
   from `results_v4.json`, so they must enter the JSON before they are cited (§4.1, task 2).
4. **The reverse-direction g_T contrast.** No test is run, since no rule was pre-registered for it. The paper uses the
   pass-2 M2 sentence (point estimate favours RL by 0.445 nats, one-sided 95 % UB −0.162, bootstrap p 0.0064, not
   pre-registered). It must never use "RL scores higher on its own objective", which reads as a verdict.

---

## 3. Evidence (from `results/v4/14_analysis.md`)

### 3.1 Pre-registered v4 decisions
- **D4**, val3 0–499, S2, sub 8, n = 500, complete.
  - Success: student 0.486 vs G\* 0.514, Δ̂ −0.0280, SE 0.02180, threshold −0.01464, so it **fails (i)**.
  - BI: Δ̂ −0.1049 ≥ −0.15, so (ii) passes.
  - Per seed: −0.036 / −0.028 / −0.020 > −0.04, so (iii) passes.
- **H2-S2**, test3 0–499.
  - g_T: student 5.5341 vs RL 5.9793. Δ −0.4452, LB −0.7485, UB −0.1616, p_greater 0.9936.
  - Result: **not detected**.
- **E5**, S12 test3 0–299, at logged median 20.8 / 46.0 ms per decision.
  - Success: g125 / g500 − student_rem −2.2 / −0.6 pp; − student_long −5.0 / −3.3 pp. All ci95 contain 0.
  - BI: g125 −0.231 / −0.271; g500 −0.162 / −0.203. All ci95 exclude 0.
  - Against full G\*: g125 −6.7 pp, ci95 [−12.0, −1.0]; g500 −5.0 pp, ci95 [−11.0, +1.3].

### 3.2 Exploratory S2 rows (test3 0–299, sub 8, ci95, uncorrected; one cell)

| Contrast | Success | BI (nats) |
|---|---|---|
| Student − G\* | −10.2 pp [−16.6, −4.3] | −0.183 [−0.269, −0.094] |
| Student − RL | +2.8 pp [−4.1, +9.6] | +0.180 [+0.091, +0.273] |
| G\* − RL | +13.0 pp [+6.4, +19.4] | +0.363 [+0.263, +0.467] |
| Student − B-fan | +8.1 pp [+1.7, +14.7] | +0.528 [+0.420, +0.637] |
| B-fan − G\* | −18.3 pp [−24.7, −12.0] | −0.711 [−0.830, −0.594] |

- **Behaviour** (no-grid, test3 0–299; travel per episode, mean probes):

  | Policy | Travel | Probes |
  |---|---|---|
  | G\* | 46.9° | 3.87 |
  | Student | 39.1° | 3.93 |
  | RL | 136.8° | 3.0 |
  | B-fan | 1.45° | 4.0 |
  | Random | 172.2° | 2.37 |

  For comparison, S12 G\* travelled 6.1° on 0–499 (pass 2 m3).
- **Student vs B-fan across cells** (pass 2 S1). In S12 the student already exceeded B-fan on BI (+0.23, ci95 [+0.14,
  +0.31]) but not on success (+2.2 pp, ci95 [−2.8, +7.3]). What S2 adds is a success separation, and no cross-cell test
  of it exists.
- **Instrument disagreement** (pass 2 M1).
  - g_T order: RL 5.979 > student 5.534 > G\* 5.397 > B-fan 5.263.
  - BI order: G\* 6.673 > student 6.490 > RL 6.310 > B-fan 5.962.
  - In S12, g_T(G\*) was below both learners only marginally (5.30 vs 5.37; 3 of 6 learner seeds below G\*). No
    interval exists in either cell.

### 3.3 Weaknesses (stated, not fixable inside the cap)
- **Design.** One S2 cell. δ is borrowed from S12, and S2 has no ε_c.
- **Students.**
  - There was no S2 HP grid. Every round ended at `max_epochs`.
  - Held-out val_R̄ does not improve over DAgger: 0.300–0.312 at r0, 0.298–0.322 at r2.
  - No train R̄ or top-1 is reported, so the v3 label-fit diagnosis cannot be applied in S2.
- **RL.** It was not re-tuned for S2 (v3 config 2 selected on `val_v2`).
- **Evaluator.** Sub-8 convergence is still unshown (E′ failed in v3). The test3 rows mix machines and pipelines.

---

## 4. Next actions

### 4.1 Record completion (report-only; stage-13 tooling, no new design; finish by 2026-11-08)

These tasks change no threshold, cell, seed, metric or verdict, and none of them is a REFINE. Each gets a dated status
note in `docs/07c_amendment_v4_0.md` before it runs, with both readings written in advance.

1. **Finish the random anchor re-read.** Run `python code/tools_regrid_followup.py experiments/v4_e4_rg_random.json …`
   until it reaches 300/300, then regenerate `14_s2_analysis.json`. If it does not finish by 11-08, report it at its n.
2. **Move the pass-2 per-episode checks into `results_v4.json`, with provenance.** These are pass-2 checks (a)–(d):
   - per-seed travel r with G\*, first-action agreement and medians;
   - RL 900/900 at 3 probes;
   - B-fan sequence identity across the two cells;
   - the g125-vs-v3-B-fan comparison.

   Add **per-seed g_T on test3** from the existing `results/v4/h2/S_k2_*_s6xx.jsonl` files (no new run). Until these
   values are in the JSON, the paper does not cite them.
3. **Optional, ≤ 4 CPU-h, owner-visible:** a val3/test3 pipeline diagnostic. Re-read G\* and the three students on a
   val3 subset (e.g. episodes 0–99) through the test3 no-grid → `regrid3 --sub 8` path, and compare it with the direct
   val3 sub-8 values on the same episodes.
   - Pre-written readings:
     - (a) the values agree, so the gap is a split or sampling effect;
     - (b) they differ, so the pipeline contributes, and the test3 S2 rows get a pipeline caveat.
   - Neither reading changes D4.
   - If it is not run, the paper carries the gap as an untested limitation.
4. **Not to be run:**
   - a one-sided test of RL > student on g_T, or any other post-hoc test;
   - an S2 remedy round, new seeds, an HP grid, or RL re-tuning;
   - an H3 rerun;
   - Lat′ latency for the reduced G\*.

   Each of these goes in the limitations.

### 4.2 Stage 16 (paper outline), from 2026-11-01 in parallel with §4.1

- **Base and frame.** The base is the v3 text (`paper/mypaper/v3/`), with the S2 rows added (amendment v4.0 "Order").
  The frame is a pre-registered characterisation of cost-aware information-gain touch selection under travel cost, in
  two cells.
- **Contributions:**
  - **C1, H3 Hold at κ = 12.** The pass-2 v3 wording, "reduced greedy completion", (S, n\* = 4).
  - **C2, learnability in a stay-and-probe cell and in a travelling cell.** The S12 D3 failure (twice) plus the S2 D4
    failure. With the same relative DeepSets head, the distilled student was not shown to reach G\* in either cell. It
    also travels a G\*-like amount in S2 without tracking G\*'s per-episode decisions.
  - **C3, distillation vs RL.** H2 is rejected in S12 and not detected in S2. Two exploratory observations go with it:
    the instrument-dependent ordering (BI favours the student, g_T favours RL), and the S2 student − B-fan success
    separation.
  - **C4, a methods note.** Evaluator resolution (E′, sub-4→8), the g_T / BI disagreement about G\*, and the val3/test3
    discrepancy.
  - **C5, cost.** Per-decision latency, plus E5: at 20.8 / 46.0 ms logged latency, reduced G\* is lower on BI than both
    students and unresolved on success. There is no cross-protocol ratio.
- **Wording binding.** Every interpretive sentence uses the pass-2 rewrites: v4 S1–S3, M1–M3, m1–m9, and the v3
  rewrites that remain in force. D4 is always quoted next to the test3 −10.2 pp figure.

### 4.3 Not to be written
- Any method claim: "learned policy matches / beats G\*", or "distillation beats RL".
- Any sentence that uses the 0.9σ seed effect size, or the 21 % gap share, as a result.
- "The student imitates G\*'s travel".
- "RL scores higher on its own objective" as a verdict.
- "Travel explains RL's deficit".
- Any cross-cell comparison worded as a finding.

### 4.4 Venue and schedule (owner)
- **Default target.** The RSS 2027 Stage 1 extended abstract, ≤ 5 content pages + 1 reference page, which allows
  preliminary experiments. Lead with C2 (two cells) and C1. C3 gets one paragraph, and C4 and C5 share a short
  methods/limitations paragraph.
- **Schedule.** Stages 16–20 run to a draft by 2026-11-20. The stage 20 gate and citation audit follow, and the
  camera-ready abstract goes in `paper/` by 2026-12-01, so the owner can check and submit by 2026-12-04 AoE.
- **Stage 20 risk.** If the v4 draft again scores below 7.5 on evidence-level grounds, it cannot loop to stage 13, since
  the cap is reached. That outcome is escalated to the owner, with RA-L / a workshop as the fallback, rather than run as
  a v5.
