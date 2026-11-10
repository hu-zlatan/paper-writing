# p2 · Stage 18 PEER_REVIEW [v3] pass 2 — merged record (run 46, 2026-11-10)

Two fresh opus subagents on the stage-19 pass-1 draft (`v3/draft_v3_stage19pass1.md`; prompt
`stage18_v3_pass2_user.txt`). Run 1: A (robotics) 4, B (statistics / conformal) 5. Run 2 (RSS pair): A 4, B 5.
Mean 4.5. **CRITICAL_FABRICATION: no** (≈ 30 numbers each recomputed with independent CRC re-implementations from raw
replays and labels — D 0.4168, σ / seed rows, hold forces, frontier, quintiles, sub-pools, online windows all match).

## Paper-level must-fix (stage 19 pass 2) — P1–P8
- P1 Fig. 1 caption: the lower end of the CSF-1 curve is "compressed", not "flat" (both runs).
- P2 Table 4: S3 matched-rate co-requirement = 0.009, pass (`v1/h3_analysis.json` audit `S3|matched_physical`); say the
  co-requirement comes from a single direct-replay audit, not the 20-ordering average.
- P3 REACT-probe: its threshold r_safe = 0.8 μ̂ uses a raw μ̂ whose log bias is +0.3186 (`19_report_rows.json`
  detector_id_sigma0 / bias_mean_diff), so its failure is at least partly a design artefact; say so, keep it labelled a
  registered negative control, never a stand-in for prior reactive work.
- P4 Abstract / conclusion qualifiers: the mid-friction (H2-R) reversal passes Holm within its family (0.03) but not
  over all 52 secondaries (0.12) (`a3_holm.json`); online intervals are over orderings only.
- P5 Break-even: state that it assumes a no-probe CSF-1 grasp would hold the same 7.606 N, which was not simulated.
- P6 Headline D is a point on an independent-friction, log-uniform [0.3, 1.0] design; say "by construction" and that
  the sign flips on [0.5, 0.8]; preload 32.7 N and 1.5 F₀ squeeze vs median F\*_mid 3.184 N contradict a
  "minimal force" reading — narrow wording.
- P7 "Plug-in suffices" and the sub-pool reversal rest on post hoc, unadjusted, unmatched-slip rows (primary grid
  floors the plug-in and CSF-1 in D1 / D2) — one consistent hedge.
- P8 Length: tighten (≈ 9.7k main-text words); the 5-page RSS Stage-1 version is stage 22.

## Evidence-level (not to be simulated in text; limitations / future work)
E1 correlated-friction / deployable-prior pool and a pre-specified friction-width sweep; E2 low / adaptive preload;
E3 one-outcome-per-grasp (replay-free) calibration; E4 no-probe CSF-1 grasp run; E5 pre-specified wide per-stratum
grid + fresh-object replication at matched slip; E6 corrected REACT-probe design; E7 hardware σ.
