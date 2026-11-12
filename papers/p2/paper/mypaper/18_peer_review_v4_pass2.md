# Stage 18 PEER_REVIEW [v4] pass 2 — merged record (run 48, 2026-11-12)

Inputs: `prompts/stage18_v4_pass2_{system,user}.txt` (template verbatim via `build_stage18_v4.py _v4_pass2`, on the
stage-19 pass-1 draft). Two fresh opus subagents, told not to read earlier reviews: `18_review_v4_pass2_run1.md`
(A 4 / B 5), `18_review_v4_pass2_run2.md` (RSS lens, A 4 / B 5). Mean 4.5 (pass 1: 4.5).

## Evidence audit

- **No CRITICAL FABRICATION.** Both re-derived C1–C5 and every Table 1 arm value from the raw v4 replays (exact),
  re-ran the bootstrap (agrees), traced ≈ 90–100 earlier-round numbers to named keys; git order confirmed.
- **Post-hoc rows computed in code (main session, after both reviews):** three of four v4 reviews asked for absolute
  forces and per-friction slip. These are re-reads of existing replays, not new experiments, so they were computed by
  committed code rather than quoted from reviewers: `code/analysis_v4_posthoc.py` → `results/v4/v4_posthoc.json`
  (report-only, not pre-registered, same split / CRC / matched recipe, 2,000 object-cluster draws, seed 2027). The arm
  slips reproduce `v4_analysis.json` exactly. Headlines: D_abs at matched slip — plug-in vs CSF-1 0.2372
  [0.1401, 0.3328]; learned vs plug-in 0.2667 [0.198, 0.3196]; shrunk vs learned −0.0505 [−0.1226, 0.0103]. Hold force
  vs CSF-1 (CRC point): plug-in −0.66 N (−9.3 %), learned −1.01 N (−14.2 %), shrunk −0.94 N. Test slip by friction
  tercile (low / mid / high μ): CSF-1 0.264 / 0 / 0, plug-in 0.131 / 0.088 / 0.075, learned 0.173 / 0.062 / 0.009.
  Unavoidable instances: 1 cal + 1 test (f4), 1 cal (c4).

## Must-fix for stage 19 pass 2

P1. **"The probe, not the learner" is metric-dependent.** On relative excess at matched slip the learner adds nothing
    (C2 equivalence); on absolute excess force (post hoc) the learner beats the plug-in by 0.2667 [0.198, 0.3196], about
    as large as the plug-in's own gain over CSF-1, and the shrunk plug-in is close to the learner. Report both metrics
    with labels; reword title / abstract / contribution / §6 / conclusion so no claim rests on one metric silently.
    State why the metrics differ (RE weights low-F\* instances more).
P2. **Per-friction slip** (post hoc P3): report the tercile table; the marginal guarantee concentrates slip on
    low-friction objects for every arm, most for CSF-1 and the learner; say what "marginal" means here.
P3. **Absolute savings** next to D (P2 rows: 0.66 N / 9.3 %, 1.01 N / 14.2 %), against the probe's force-time cost.
P4. **Factual fixes:** the preload (32.7 N) does not exceed every instance's minimal force (only the squeeze does;
    check against `results/v4/labels` via the reviewers' figures only if they are in a results file, otherwise state it
    qualitatively); the learned model is re-fitted deterministically from stored settings with a reproduction check, not
    "not re-trained"; Limitation (10)'s "per-family tables not run" is wrong (S4 has per-family slip; P3 now has
    per-tercile).
P5. **Route labels** on every effect size in abstract, Table 1 and conclusion (σ 0.4: −0.2065 matched vs 0.1675 CRC);
    give C1 / C2 on both routes where the JSON has them (S5 rows); C2 equivalence holds on the matched route and for
    one trained model only. Drop "passes at 5 %" for the CRC-route TOST p 0.037 next to a CI** outside ±0.10 — say the
    two criteria disagree.
P6. **Deviation record:** S6 was registered as a "measured break-even" but is computed in closed form (squeeze term from
    pad readings) → add to Deviations; state the Clopper–Pearson level used (read it from code); disclose that
    unavoidable instances count as slips and are excluded from RE (P4 counts); note S3's registered prediction outcome
    as the JSON gives it.
P7. **H3 online study:** do not mix metrics in the co-requirement; report the family-shift efficiency ratio and its
    interval as given in the v1–v3 results (tracking less efficient than the oracle there) if it is in a results file.
P8. **Figure 2** is referenced but has no prompt / file: add a figure prompt or data-figure spec (stage 22 renders), or
    remove references. Long-hold tension: keep "slip over 17–27 s holds is untested" prominent and soften any advice to
    "probe when holds are long" to a conditional.

## Deferred (new experiments; owner decision if the gate needs them)

Learned seeds 1–4 on the v4 pools; family prior + probe hybrid arm; probe-only (no squeeze) protocol; long-hold
simulation; hardware-grounded σ. p2 refine cycles are 3 / 3.
