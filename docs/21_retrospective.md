# Stage 21 · Retrospective archive (v4)

**Project:** paper-writing / TouchBED — active tactile localization under travel cost (target: RSS 2027 Stage 1 extended abstract).
**Final version:** v4. **Calendar span:** 2026-10-28T07:56Z to 2026-11-01T19:50Z (about 108 h over 11 scheduled runs).

> **Status: the paper is NOT done.** The stage 20 v4 quality gate scored 5.0/10 against a 7.5 threshold (v3 had scored
> 5.5). All 3 of 3 refine cycles allowed by `RESTRICTS.yaml` are used, so no v5 loop can start on its own. The direction
> has been escalated to the owner, and the owner's decision is pending. This archive changes no claim, number or verdict.

---

## Executive summary

Across four design iterations the project moved from a non-myopic amortized-design method paper to a pre-registered
characterisation paper (outcome row 4), because the non-myopic premise failed before running (v1), Idea 2 was refuted
and the H1 learner failed its gate (v2), and the only learner cell turned out to be stay-and-probe (v3). Version 4 added
a travelling cell S2 (κ = 2), which behaves as designed (G\* travels 46.9° per episode against 6.1° in S12), but the
distilled student again failed its learnability gate (D4: −2.80 pp against a −1.46 pp threshold), H2-S2 was not
detected, and one-step headroom (H3) stayed Hold. The v4 draft then failed the stage 20 gate at 5.0/10 with the refine
cap exhausted, so the record is complete as a characterisation but the paper is not submittable without an owner
decision.

---

## What worked

- **Pre-registration held up under pressure.** Every decision rule for v4 (D4, H2-S2, E5) was written in
  `docs/07c_amendment_v4_0.md` before any v4 run, and the stage 14 adversarial pass found no pre-registered verdict
  wrong. Because the readings were fixed in advance, a failed gate produced a licensed sentence ("not shown to reach G\*
  in S2 either") rather than a post-hoc rescue.
- **Two-pass analysis with binding rewrites.** The fresh-context adversarial pass caught real over-reach in the pass-1
  reading: the student–B-fan contrast across cells (S1), an asserted travel mechanism for G\*'s lead over RL (S2), and
  "the student imitates G\*'s travel", which per-episode data contradicted (Pearson r 0.14–0.24 by seed, 0 of 300
  identical action sequences) (S3). Making every pass-2 rewrite binding kept those claims out of the draft.
- **The S2 cell answered the v3 reviewers' main objection.** G\* moves 44.8° between probes in S2 against 4.3° in S12,
  so the learnability failure is no longer confined to a regime where the planner barely moves.
- **Cheap diagnostics resolved candidate confounds.** The val3 0–49 re-read through the test pipeline gave identical
  actions and success on 50 of 50 episodes, which ruled out the scoring path as the cause of the S2 val/test gap. The
  post-hoc Cal′ verification for S2 (3.875 probes on 200 calibration episodes) confirmed the budget rule.
- **Provenance checks caught coincidences before they became errors.** The g125 reduced planner and the v3 B-fan row
  share an identical success total (108 of 300) but agree on only 230 of 300 episodes and 1 of 300 BI values, so the row
  is not a mislabelled copy.
- **H3 instrument checks.** The notch construction, its travel form and the zero-gap bank all passed, and the bias ratio
  (0.957) stayed inside the guard, so Hold rests on a validated estimator.
- **Free compute was enough.** About 100 CPU-h for v4 ran on free GitHub Actions CPU runners plus a 2-vCPU sandbox.

## What didn't (and why)

- **The method hypothesis never survived.** v1's pre-run manipulation check gave G(S) = −0.033 [−0.054, −0.014] against
  a required ≥ 0.10, so the non-myopic premise failed before any main run. In v2, G2 refuted Idea 2 in the tested range
  and the H1 learner failed after one remedy. In v3, D3 failed on the first attempt and after its remedy. In v4, D4 failed
  clause (i). The common thread is that one belief-free DeepSets head, distilled from G\*, was not shown to reach G\* in
  either regime.
- **The S2 training recipe over-fit rather than under-fit.** The fixed 200-epoch, last-checkpoint recipe was chosen to
  answer v3's under-training concern. The per-epoch record showed held-out R̄ was lowest between epochs 22 and 130 and
  then rose by 0.007–0.026 by epoch 200, while training loss was still falling. Held-out R̄ also did not improve across
  DAgger rounds (0.300–0.312 at r0, 0.298–0.322 at r2). Fixing the recipe in advance was correct; choosing a recipe that
  answered the previous review rather than one validated on S2 was the cost.
- **An unexplained val3/test3 gap.** Student − G\* success was −2.8 pp on val3 but −10.2 pp on test3, wider for every
  seed (by 5.4, 11.2 and 5.7 pp), about 2.0 combined SE under independence. The pipeline was ruled out on 50 episodes;
  the cause remains unidentified.
- **The RL comparator was weak in a specific way.** All six PPO policies collapse to exactly 3 probes and travel several
  times G\*'s distance. RL used S12's config 2 without S2 re-tuning. H2 is therefore a comparison against this setup only.
- **RL's objective and the localization metric disagree.** In S2, g_T ranks G\* below both learners while grid BI ranks
  it above both; in S12 the g_T ordering is marginal. This makes H2 ("advantage on RL's own objective") less informative
  about localization than intended.
- **Thin evidence by design.** One cell per regime, three seeds per learner, no multiplicity correction, a reused test
  split, and an evaluator whose convergence gate (E′) failed. These limits were declared, but they keep the stage 20 score
  low on evidence-level grounds, and the refine cap leaves no room to fix them.
- **Stage 20 failed twice for evidence reasons.** v3 scored 5.5 and v4 5.0. Adding a cell did not move the score
  because the gate's concerns are about depth (cells, seeds, tuning) rather than breadth.

---

## Loop log

| # | Transition | Type | From → to stage | Reason |
|---|---|---|---|---|
| 1 | v1 → v2 | PIVOT | 15 → 8 | Pre-run manipulation checks failed the non-myopic premise: G(S) = −0.033 [−0.054, −0.014], required ≥ 0.10. |
| 2 | v2 → v3 | PIVOT | 15 → 8 | G2 refuted Idea 2 in the tested range; G3 learnability failure of the pre-registered H1 learner after one remedy. |
| 3 | v3 → v4 | REFINE | 20 → 13 | Stage 20 v3 scored 5.5/10: the only learner cell S12 was stay-and-probe (G\* travel 6.1° per episode); the amortization answer was open; no reduced-G\* comparison on test. Refine cycle 3 of 3. |
| — | v4 stage 15 | PROCEED (characterisation sense only) | 15 → 16 | All decision-bearing items settled (D4 FAIL, H2-S2 not detected, E5 reported, v3 verdicts unchanged); REFINE precondition false and cap reached; PIVOT would be a fourth design, which the v3 pre-registration excludes. |
| — | v4 stage 20 | FAIL, escalated | — | Quality gate 5.0/10 < 7.5; refine cap 3 of 3 used, so no loop to stage 13; escalated to the owner (decision pending). |

The refine-cap rule is `loops.max_refine_cycles: 3` with `escalate_on_cap_hit: true` (quoted in the stage 15 decision;
cycle counting in `docs/07c_amendment_v4_0.md`, "Why").

---

## Reproducibility notes

### Final hyperparameters per condition

**Cells** (prompt, Section 3.1; `docs/07c_amendment_v4_0.md`):
- S12 = set S, κ = 12, τ = 4.9, n\* = 4.
- S2 = set S, κ = 2, τ = 4.7, n\* = 4 (τ from Cal′; S2 Cal′ verification 3.875 probes, run after the S2 experiments).
- Action set 64 angles × 8 offsets = 512; sensor noise σ_p 1.0 mm, σ_n 5°.

**G\* (teacher / reference):** N = 2,000 particles, C = 512 candidates, M = 64 outcome samples (prompt, Table 1).
E5 reduced planners: g125_512_16 and g500_512_4 (prompt, Table 1; `docs/07c_amendment_v4_0.md`, E5).

**Distilled student (shared DeepSets relative head):**
- Loss and optimiser: Adam, lr 1e-3, β_T = 4, λ = 0.5, batch 256 decisions-equivalent, ρ = 0.05 in R̄ (prompt, Table
  1). This is HP config 0 from the v3 grid, with no weight decay and gradient-norm clip 1.0 (`docs/07c_amendment_v3_0.md`,
  C7 and the HP-config entry).
- S12 recipe: stop when validation R̄ improves by < 0.005 over 3 consecutive evaluations, hard cap 50 epochs, last
  checkpoint (`docs/07c_amendment_v3_0.md`, C7); one registered remedy doubling round 0 and both DAgger rounds.
- S2 recipe: hp 0 reused (no new grid; stated deviation); fixed 200 epochs per round (`--fixed-epochs 200`); DAgger 2
  rounds × 800 episodes, β 0.5 then 0; round 0 on label3 0–1,199 plus label episodes 1,500–2,999; last checkpoint
  (`docs/07c_amendment_v4_0.md`, E2). Held-out shards label3 1,200–1,499.

**RL (PPO, same head):** v3 config 2 — lr 1.09e-3, entropy 1.33e-4, batch 128, critic lr 1.43e-3; PPO-clip 0.2, 4
epochs per update, critic baseline; 200,064 episodes per seed; plateau recorded, not used (`--no-plateau-stop`)
(`docs/07c_amendment_v4_0.md`, E3; prompt, Table 1). The S12 sweep was 4 configurations on 1 seed at 50,048 episodes
each (prompt, Table 1). S2 wall time per seed: 3,601 / 3,544 / 3,051 s (`results/v4/results_v4.json`,
`14_s2_analysis.json.rl_training`).

**Reward / g_T:** ball-sPCE with L = 4,095 contrastive states and J = 16 ball states; cap 8.318 nats (prompt, Table 1).

**Evaluator and statistics:** adaptive grid posterior at subdivision 8; crossed episode × seed bootstrap, B = 10,000,
seed 0; δ = 0.04; BI floor −0.15 nats; H2 margin +0.10 nats; H3 threshold 0.03 (prompt, Scope note and Table 1). H2
bounds use 5 % / 95 % quantiles; ci95 contrasts use 2.5 % / 97.5 % (pass-2 m7).

### Random seeds used

| Role | Seeds | Source |
|---|---|---|
| S12 students (D3) | 501–503 | prompt, Table 1 |
| S12 belief-input control | 521–523 | prompt, Table 1 |
| S2 students (D4) | 601–603 | prompt, Table 1; `docs/07c_amendment_v4_0.md` |
| S12 RL | 511–513 | prompt, Table 1 |
| S2 RL | 611–613 | prompt, Table 1; `docs/07c_amendment_v4_0.md` |
| S12 HP grid (students) | 501 | `docs/07c_amendment_v3_0.md`, C7 |
| S12 RL sweep | 519 | `docs/07c_amendment_v3_1.md`, D9 |
| Bootstrap | 0 | prompt, Scope note |
| v2 seeds (never reused) | 100–102, 200–202, 300–301, 400–402 | `docs/07c_amendment_v3_0.md`, C8 |

Episode streams are keyed by split and (for label/DAgger) by cell, so evaluation episodes are paired across methods and
cells; DAgger indices follow the formula in `docs/07c_amendment_v3_1.md`, D1.

### Hardware

- Sandbox (stage 1 detection): pure CPU, 2 vCPU, 7 GB RAM, no GPU; Python 3.13, NumPy 2.5.3, SciPy 1.18.1, matplotlib
  3.11.2, MuJoCo 3.17.0 (`PROGRESS.md`, stage 1 hardware line).
- GitHub Actions runners: `ubuntu-latest`, Python 3.12 via `actions/setup-python@v5`, job timeout 350 min, at most 20
  parallel matrix jobs, `OMP_NUM_THREADS` / `OPENBLAS_NUM_THREADS` / `MKL_NUM_THREADS` = 1
  (`.github/workflows/experiments.yml`). CPU model: not recorded.
- The S2 test3 rows mix machines: student actions in the sandbox (Python 3.13.18 / numpy 2.5.3), G\*'s on runners
  (Python 3.12.15 / numpy 2.5.4) (prompt, analysis §3.3).

### Wall-clock and compute

- Calendar time: about 108 h, 2026-10-28T07:56Z to 2026-11-01T19:50Z (prompt header).
- v4 compute: about 100 CPU-h (prompt, analysis §4.10; matching the ≈ 100 CPU-h estimate and ≈ 6–8 h wall on 20 runners
  in `docs/07c_amendment_v4_0.md`, "Compute").
- Measured total wall-clock for all v4 jobs: not recorded.

### Package versions

`code/requirements.txt` does **not** pin versions; it lists lower bounds only: `numpy>=2.0`, `scipy>=1.11`,
`shapely>=2.0`, `mujoco>=3.0`, and unversioned `pytest`. Runners install from this file at job time, so the exact runner
versions depend on the install date. The only concrete versions on record are the sandbox ones above (`PROGRESS.md`)
and the two interpreter / numpy pairs quoted in the analysis. Pinning (a lock file) is an open action.

### Where each artefact lives

- **Aggregated v4 results:** `results/v4/results_v4.json` (blocks `12_d4_analysis.json`, `14_s2_analysis.json`,
  `14_e5_analysis.json`, `14_travel_split.json`, `14_diag_s2.json`, `14_review2_checks.json`, `students_S2_training`);
  the per-block files sit beside it in `results/v4/`.
- **Per-episode records:** `results/v4/test3/`, `results/v4/test3_sub8/`, `results/v4/e5/`, `results/v4/h2/`,
  `results/v4/d4/`, `results/v4/d4_val/`, `results/v4/cal/`, `results/v4/pipe/`, `results/v4/rl/`,
  `results/v4/labels/`, `results/v4/pilot/`.
- **Analysis and decision:** `results/v4/14_analysis.md` (merged; pass files `14_analysis_pass1.md`,
  `14_analysis_pass2.md`), `results/v4/15_decision.md`, prompts in `results/v4/prompts/`.
- **Earlier versions:** `results/v1/`, `results/v2/`, `results/v3/` (v3 aggregate `results/v3/results_v3.json`).
- **Paper:** current draft `paper/mypaper/sections/draft_v4.md` and outline `paper/mypaper/sections/00_outline.md`;
  intermediate v4 drafts in `paper/mypaper/v4/`; archived v3 paper and gate in `paper/mypaper/v3/`; v4 reviews
  `paper/mypaper/18_review_v4_*.md`; quality gate `paper/mypaper/20_quality_gate.json`; stage prompts in
  `paper/mypaper/prompts/`.
- **Figures:** `paper/mypaper/figures/` holds only `figure1_prompt.txt`; Figure 1 is still a placeholder in the draft.
- **Code:** entry point `code/main.py`; library `code/touchbed/` (bootstrap in `code/touchbed/stats.py`); v4 analyses
  `code/analysis_d4_v4.py`, `analysis_s2_v4.py`, `analysis_e5_v4.py`, `analysis_travel_split_v4.py`,
  `analysis_diag_s2_v4.py`, `analysis_review2_v4.py`; aggregation `code/tools_results_v4.py`; re-read tooling
  `code/tools_regrid_followup.py`, `code/tools_regrid_manifest.py`.
- **Pre-registration:** `docs/07c_amendment_v3_0.md`, `docs/07c_amendment_v3_1.md`, `docs/07c_amendment_v4_0.md`.
- **Runner workflow:** `.github/workflows/experiments.yml` (manifest-driven; commits outputs under `results/`).

---

## Lessons for future projects

1. **Test the premise cheaply before building the method.** v1 died on a manipulation check, and H3 later showed small
   one-step headroom in both regimes. A headroom pilot before the v1 design was built would have pointed to a characterisation paper
   three loops earlier.
2. **Check that a design cell exercises the mechanism.** S12 turned out to be stay-and-probe, which only became visible
   in the v3 behaviour log. Logging between-probe travel (not just total travel, which includes the grid snap) at pilot
   time would have caught it.
3. **Validate a training recipe on the cell where it runs.** The S2 recipe answered the previous review (under-training)
   and then over-fit. Pre-register a selection rule (e.g. held-out checkpoint choice) rather than a fixed epoch count
   borrowed from another cell.
4. **Do not let the trained comparator's objective be the only yardstick.** g_T and grid BI rank G\* differently in S2.
   Any "advantage on RL's own objective" hypothesis should be paired with a posterior-based metric in the rule itself.
5. **Keep the adversarial pass binding.** It removed three serious and three moderate over-claims in v4 alone.
6. **Count power before the run.** Post hoc, H2 could only detect about half a nat of true advantage, and the D gates
   effectively demanded near-parity with G\*. Those facts were computable from pilot SEs.
7. **Budget the refine cap for depth.** Both stage 20 failures were about evidence depth (cells, seeds, tuning). Spending
   the last refine cycle on breadth (one new cell) did not raise the score.
8. **Pin the environment.** Unpinned requirements and mixed machines (sandbox vs runners, different Python / numpy) left
   a live candidate confound until a diagnostic ruled it out.
9. **Keep provenance in the aggregate JSON.** Pass-2 per-episode checks had to be moved into `results_v4.json` before
   they could be cited; writing them there first saves a round.

---

## Open questions / future work

Owner decision first: whether to override the refine cap, submit the v4 characterisation as it stands (RSS 2027 Stage
1, 2026-12-04 AoE, still blocked by the open RSS LLM-policy question in `OWNER_TODO.md`), or fall back to RA-L or a
workshop, as the stage 15 decision anticipated.

Scientific questions left open by the record (none answered here):
- What causes the S2 val3/test3 gap, given that the scoring pipeline is ruled out on val3 0–49?
- Would early stopping on held-out R̄ change D4 in S2?
- Does regret on student-visited states confirm covariate shift?
- Do the findings hold with more cells per regime and more seeds?
- Would a full 512-action screen or a structured travel-then-fan candidate family change H3?
- Would a probe-count-aware RL objective or an S2-tuned RL configuration change H2-S2?
- Why do g_T and grid BI order G\* differently, and does near-cap compression of g_T contribute?
- Would a belief-input head that actually fits its labels close the learnability gap?
- Where do the learners and reduced planners sit on a latency–accuracy frontier timed under Lat′?
- Do the results transfer beyond planar simulation (3D objects, held-out shapes, hardware)?

Housekeeping before any further work: pin package versions, record runner CPU models, produce Figure 1, and record a
measured total wall-clock for the v4 jobs.

---

## Addendum (2026-11-02, run 12): environment record

The "pin the environment" housekeeping item is partly closed, without changing any result or the workflows:

- `code/requirements-lock.txt` lists the exact versions from the install log of Actions job 124884356660 (run
  41318760187, 2026-11-01; CPython 3.12.15, ubuntu-26.04 image 20261025.179.1). The experiments workflow still installs
  `code/requirements.txt`.
- `code/tools_env_census.py` → `results/v4/env_census.json` counts the `env` header of every result shard. All 590 v4
  shards carry one: 574 runner shards (Python 3.12.15, numpy 2.5.4) and 16 sandbox shards (Python 3.13.18, numpy 2.5.3).
  v1/v2 shards and 62 v3 shards predate the header.
- Still open: versions of scipy / shapely / mujoco for runner jobs before 2026-11-01 are not recorded; runner CPU models
  are not recorded.
