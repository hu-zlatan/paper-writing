# p2 · Stage 18 PEER_REVIEW [v2] — merged record (run 44, 2026-11-10)

Two fresh opus subagents on `paper/mypaper/draft_v2.md` (template verbatim, `prompts/stage18_v2_user.txt`):
- Run 1 (`18_review_v2_run1.md`): A (ML / statistics) 5, B (robotics / tactile) 4 → 4.5 / 10. 40 numbers
  spot-checked, 26 recomputed with the repo's analysis code from raw replays, all digits match.
- Run 2 (`18_review_v2_run2.md`, RSS pair): A (tactile manipulation) 4, B (conformal / statistics) 6 → 5 / 10.
  ≈ 60 numbers checked, > 20 recomputed by independent scripts (all B3 windows from `results/v2/b3/*.jsonl`, H2a from
  v1 replays, CSF-proxy@0.2 from `crc09e`), all match.
- **CRITICAL_FABRICATION: no** (both runs). Mean score 4.75 (v1 pass 2: 4.5).

## Paper-level must-fix (stage 19)
1. **Wrong / selective statements:** §5.2 says the plug-in's D is smaller under LTT, but on the refined grid it is
   larger (0.4040 vs 0.4015); H1c says "every CI above 0" but the registered validation-tuned RAW-Qv has intervals
   containing 0 at every α — report it.
2. **Like-for-like grids:** abstract / Discussion compare plug-in 0.4149 (refined) with learned 0.4168 (primary);
   give same-grid pairs (refined 0.4149 vs 0.4289; primary 0.3816 vs 0.4168). Figure 1(b) on a single grid.
3. **One hedge for learned vs plug-in** everywhere: "not confirmed / no demonstrated gain"; never "the plug-in
   already captures it"; note the grid-floor bias; no equivalence test.
4. **Headline conditional:** state D 0.42 as conditional on assumed onset noise σ 0.2 and the friction range; put
   the σ curve (D falls to the σ 0.4 value) and the narrow-friction reversal next to the headline.
5. **"Certified" re-scoped:** offline CRC / LTT needs simulator replays (labels) per calibration grasp — simulation
   only; online tracking is the deployable route (5 orderings, descriptive, no intervals). LTT guarantee is per
   stratum.
6. **Force accounting:** the minimal-force claim concerns the holding force after the probe; state the preload /
   probe phase force explicitly (protocol constants from the design docs) and drop or qualify fragile-object /
   prosthetics framing.
7. **Route / interval type** named for every secondary number (pooled cells, oracle share, H2-C, H4 chain, H2-M);
   matched-slip D labelled as chosen using test slip; S2 online efficiency ratio flagged (oracle itself slips above α).
8. **Small factual fixes:** static touch "reads m g/2" overstated (use the report-only row as recorded); report D-FID
   (registered secondary, in results_v1.json); compute figure = logged replay jobs only; RE excludes unavoidable
   instances; Holm adjustment as registered or the drop stated as a deviation.
9. **B2 framing:** a uniform margin cannot see stratum load (D3 / D4), so it is a weak, descriptive comparison, not
   evidence that calibration is "necessary".
10. **Density:** move ledger / deviations / compute / LTT and matched-slip tables / diagnostics / B2 / B3 detail to an
   appendix section at the end, so the main body reads as a paper; total length may stay (condensed at stage 22).

## Evidence-level (stage 20; not to be simulated in text)
E1 reactive slip-tightening baseline and a friction-estimate + tuned per-stratum margin baseline at matched slip;
E2 σ grounding with real sensor data; E3 direct learned-vs-plug-in contrast at matched slip / LTT and conditional
slip tables (family × stratum, friction quintile); E4 hardware / online study with intervals.
