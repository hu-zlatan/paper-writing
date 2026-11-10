# p2 · Stage 18 PEER_REVIEW [v2] — pass 2, merged record (run 45, 2026-11-10)

Two fresh opus subagents on the revised `paper/mypaper/draft_v2.md` (= `v2/draft_v2_stage19pass1.md`), template
verbatim (`prompts/stage18_v2_pass2_user.txt`, builder `build_stage18_v2.py _v2_pass2`):
- Run 1 (`18_review_v2_pass2_run1.md`): A (robotics) 4, B (conformal / methods) 5 → 4.5. ≈ 190 numbers checked
  (abstract, all Fig. 1 values, Tables 1–3, D1, F1, F2, App. C, E), some recomputed from raw labels — all match.
- Run 2 (`18_review_v2_pass2_run2.md`, RSS pair): A (tactile) 4, B (conformal / statistics) 5 → 4.5. ≈ 240 numbers
  checked, ≈ 35 recomputed by an independent script from raw replays / labels (H2a D 0.416821, every λ̂ index,
  per-stratum slips on both grids) — all match.
- **CRITICAL_FABRICATION: no** (both runs). Mean 4.5 (pass 1: 4.75).

## Paper-level must-fix (stage 19 pass 2)
P1. **H2b equivalence test misdescribed (both runs; verified by the main session).** The draft says "no equivalence
    test was registered" for learned vs plug-in (C3, §5.2 ×2, Table 2 caption, §6 / §8). `docs/08b_preregistration.md`
    §4 item 3 registers a TOST at ±0.10, 0.0125 per side, and `code/analysis_crc.py` implements it (l. 16). Correct
    account: the registered TOST was run and not met on the primary route (upper 0.1454) and on the refined grid
    (upper 0.1001); state the label-route row as secondary. The CSF-proxy@0.2 sentence ("no equivalence test was
    registered") must be checked against 09_amendment_v2 and kept only if true.
P2. **RAW-Qv ledger wording:** point slip is above α at every level; only the interval contains 0. Use the file's
    decision ("partly confirmed / not confirmed"); soften "lands near α" (§5.5, §6).
P3. **16-cell heterogeneity "pass":** say what "pass" means (no harmful cell); report Q / df / p only if they are in
    the results JSONs.
P4. **Slip above α where it occurs:** per-seed slip (run 1: seed 4 0.1018) and refined-grid per-stratum slips (run 2:
    CertGrip-full D1 0.1043, D2 0.1014; CSF-1 D3 0.1100, D4 0.1057) — print them only from the results JSONs
    (they are there per the reviewers; check), and say the guarantee is marginal / per stratum accordingly.
P5. **σ vs σ_p scale claim:** "never on one scale" is wrong — μ̂ = m g / (2 F_onset), so onset noise is friction-
    estimate noise. Remove the claim; describe the relation qualitatively. Reviewer-computed error SDs / correlations
    are NOT in the results files and must not be printed.
P6. **Weak comparators:** CSF-proxy at σ_p 0.4 / 0.8 and the plug-in at σ 0.4 are worse than CSF-1 (RE 0.92, 2.79,
    0.99 vs 0.78, all in results); say these superiority rows are against unshrunk noisy estimates and carry little
    weight; the learner's σ 0.4 advantage may reflect shrinkage (stated as an untested reading).
P7. **Force accounting:** the preload (32.7 N) and squeeze peak (49 N) are protocol constants larger than most minimal
    hold forces; say the saving is on the post-probe holding force and is small in newtons relative to the preload;
    no reviewer-computed N statistics. Note in §5.6 that the frozen tactile arm slips more than the frozen baseline
    under S3 if (and as) the results file reports it.
P8. **Narrow-friction reversal** in the abstract: label route, unadjusted, ≈ 88 calibration instances per stratum
    (only if derivable from the design / results); the grid-floor bias makes the registered H2b estimate
    uninformative — say so once.
P9. **Length / redundancy:** §6 repeats §5; tighten §6 without going below the floors (main-body cut happens at
    stage 22).

## Evidence-level (stage 20; not to be simulated in text)
E1 tactile competitors at calibration-selected matched slip (per-stratum tuned margin, reactive slip-tightening,
friction estimate + tuned margin); E2 shrinkage plug-in / proxy; E3 narrow-friction sub-pool on the CRC route with
existing replays; E4 repeated calibration / test re-splits (empirical certificate check), LTT at δ/4; E5 σ grounding
from published sensor data; E6 adaptive / low preload, force–time integral; E7 online physical-feedback study with
intervals, S2 and the post-shift transient; E8 a pool where friction correlates with non-tactile inputs.
Several (E2–E4) need no new simulation (full-grid replays exist) — candidate v3 rows if stage 20 loops.
