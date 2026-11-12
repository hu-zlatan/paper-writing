# Stage 18 PEER_REVIEW [v4] — merged record (run 48, 2026-11-12)

Inputs: `prompts/stage18_v4_system.txt`, `prompts/stage18_v4_user.txt` (template `peer_review.md` verbatim via
`build_stage18_v4.py`). Two fresh opus subagents, no main-session reasoning given:
`18_review_v4_run1.md` (A 5 / B 4), `18_review_v4_run2.md` (RSS lens; A 4 / B 5). Mean 4.5.

## Evidence audit

- **No CRITICAL FABRICATION** in either run. Both reviewers re-implemented CRC independently and recomputed C1–C5,
  S1, S3, the σ band, the width sweep, the no-probe grasp and the CSF-fam μ̄ from the raw v4 replays: exact match.
  Run 1 traced all 283 decimals; run 2 checked > 120 earlier-round values. Counts (700 test objects / 2,800 instances,
  500 calibration objects, 2,000 bootstrap draws, 200 re-splits, 20 orderings) match. Git order (amendment → code →
  read-out → labels → replays) confirmed.
- Reporting discrepancies (no fabrication) → must-fix list below.

## Must-fix for stage 19 (merged, both runs)

1. **Break-even attribution** (run 1 #1; run 2 E6): 17.74 s is the learned arm, 27.07 s the plug-in; the abstract /
   conclusion attribute 17.74 s to the plug-in. Drop "measured": it is a closed-form computation from commanded force
   profiles; holds longer than the 0.6 s disturbance window are not simulated — say so.
2. **σ 0.4 / "probe, not learner" overclaim** (run 2 E3; run 1 #2): the reversal at σ 0.4 holds for the plug-in only;
   the learned arm still beats CSF-1 there and beats the plug-in. Restrict "the probe, not the learner, carries the
   saving" to σ 0.2 and to the relative-excess metric of the matched route. Run 1's own absolute-force recomputation is
   not in the repo's results, so it is not cited as a number; the text instead states that C2 is on relative excess only.
3. **Route mixing** (run 1 #4/#5; run 2 E2, E8): Fig. 2a and the feature-chain sentence mix matched-route and CRC-route
   (and label-route) values; label each value's route or use one route per comparison.
4. **CSF-fam sentence** (run 2 E1; run 1 #6): matched RE 0.2674 is at slip 0.10, not 0.05929; at its CRC point
   (slip 0.05929) RE is 0.2995 — check both against `v4_analysis.json` before editing.
5. **Decision rule as registered** (run 2 E4; run 1 #6): Holm-adjusted bootstrap p < 0.05 with a positive point
   estimate, not "CI lower limit > 0". **C2 CRC-route row** (run 2 E5): use the same TOST criterion as the other rows
   (code reports p 0.037 there). **"p 0.915 consistent with equivalence"** → remove (a non-significant difference test
   is not evidence of equivalence; the TOST is).
6. **Method facts** (run 1 #3, #7; run 2 E10): σ is noise added on top of the simulator's taxel model (detector bias
   +0.32, SD 0.11 at σ 0) — "simulated touch is clean" is wrong; CSF-1's μ is the hard-coded geometric mean
   √(0.3·1.0), the selection split only picked the baseline type; all rules get the true mass and the disturbance
   stratum; mass is log-uniform; all v4 learned rows use one training seed (seed 0).
7. **Mid-friction sub-pool** (run 1 #4; run 2 E7): also restricted to mid amplitude, compares learned vs CSF-1, and its
   sign is grid-dependent — state all three; no flat claim in the abstract.
8. **Length / presentation**: Introduction 441, Related Work 298, Setup 397 words — expand within the 5-page budget;
   replace pipeline jargon ("v4 row", "edge: false", "read-out code"). Figures are prompts / captions only (stage 22
   renders data figures).

## Deferred (need new experiments; not done in stage 19)

Learned seeds 1–4 on the fresh pool; per-μ / per-family slip tables; a family-prior + probe hybrid arm; a probe-only
(no squeeze) protocol; long-hold simulation at the certified force; a hardware-grounded σ. These are evidence-level
items for stage 20 to weigh; p2's refine cycles are 3 / 3, so they go to the owner if the gate asks for them.
