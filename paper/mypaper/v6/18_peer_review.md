# Stage 18 PEER_REVIEW [v6] — merged record and triage (run 50, 2026-11-13)

Draft reviewed: `paper/mypaper/sections/draft_v6.md` (stage 17 [v6]). Template `peer_review.md` verbatim
(`paper/mypaper/prompts/build_stage18_v6.py` → `stage18_v6_{system,user}.txt`); two fresh opus subagents.
The v5 record is at `paper/mypaper/v5/18_peer_review.md`.

| Run | File | Reviewer A | Reviewer B | Fabrication |
|---|---|---|---|---|
| 1 | `18_review_v6_run1.md` | 5 / 10 (method & statistics) | 4 / 10 (significance) | **none found**; headline contrasts recomputed from raw jsonl, trial counts correct |
| 2 | `18_review_v6_run2.md` (RSS / CoRL pair) | 3 / 10 (robot-learning significance) | 4 / 10 (methodology) | **none found**; H6a / H6b / H6c point estimates recomputed exactly |

**Decision rule:** no CRITICAL FABRICATION → stage 19.

## Checks done by the main session after the reviews

- **Script-before-data order** (both reviewers could not check it on the shallow clone): history deepened with
  `git fetch --shallow-since=2026-11-09`. `code/analysis_v6.py` was added in `ae3c3899` (2026-11-10 01:47 UTC, "committed
  before any v6 record exists") and never modified since; the first v6 result commits are 02:06–02:09 UTC the same day;
  `code/touchbed/stats.py` last changed 2026-11-09. Confirmed.
- **Post-hoc checks requested by the reviewers** — `code/analysis_v6_posthoc.py` → `results/v6/18_posthoc_v6.json`
  (report-only, not pre-registered, frozen loaders and statistics reused unchanged):
  - P1 E12 grid shift of student − G\* (sub 16 − sub 8, episodes 0–99) with ci95: S2 −0.016 [−0.086, 0.052];
    S4 0.046 [−0.022, 0.116]; S8 0.05 [−0.006, 0.11]; S12 −0.046 [−0.094, −0.002]; A16-2 −0.006 [−0.03, 0.012].
    Only S12 excludes 0. Reviewer 1's statement reproduced.
  - P2 H6b bootstrap-seed sensitivity (Holm over 10): 0–499 → 7 rejections under seeds 0 (registered) to 9, 5 under
    seed 10; 300–499 → 2 under all 11 seeds. Reviewer 2's statement reproduced.
  - P3 kept-checkpoint epochs: copied from `results_v5.json > 16_report_rows.json > student_checkpoint_sensitivity`.
  - DAgger warm start confirmed in code (`code/tools_v5_manifests.py`: each round `--init` from the previous round).

## Triage for stage 19 (paper-level; no new experiments — refine cap 5 / 5 used)

1. **H6b fragility and fresh window up front:** abstract and C1 state 7 / 10 on 0–499 (5 / 10 under one of 11
   bootstrap seeds, post hoc) and 2 / 10 on the fresh 300–499 window; single runs of two same-budget reduced planners.
2. **C3 (DAgger vs BC) softened:** disclose the warm start and the kept-checkpoint epochs in Algorithm 1 / §method;
   C3 becomes "no DAgger benefit detected under this recipe".
3. **C4 (E12) with uncertainty:** report the P1 ci95 (only S12 excludes 0); reword "moves by 4.6–5.0 pp" accordingly.
4. **TOST power framing (§6.2):** remove any statement that 500 episodes sufficed for a 4 pp equivalence test; report
   the ci90 half-widths instead.
5. **Number wording:** "7–8 pp" → "5–8 pp" where the ci95 lower bounds say so; disclose the S12 strongest-comparator tie
   (g500_512_4 = b_cov = 0.39); label "0.15–1.16 pp" unadjusted; define TouchBED at first use.
6. **External reader / length:** remove the "previous round" project-history narrative (one sentence of history at
   most), abstract < 200 words, keep the 3 [CITE-MISSING] markers for stage 23 (no knowledge card), Figure 1 data panels
   to be rendered in stage 22.
7. **Limitations add:** no comparator near the student's latency other than heuristics / RL; reduced planners single
   run; no task-time or hardware model; G\* only 2 runs; bootstrap-seed sensitivity of H6b.

## Evidence-level requests (not executable: refine cap used; for the owner / a later Stage 2 loop)

- Comparators near the student's latency (pruned / accelerated G\*, a cheap information heuristic); second runs of the
  reduced planners; G\* runs 3–4; E12 extended to the reduced planners; last-epoch or student-visited-regret DAgger
  checkpoints; a task-time model or small hardware check.
