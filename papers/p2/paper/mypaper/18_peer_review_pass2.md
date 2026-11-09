# p2 · Stage 18 PEER_REVIEW [v1] — pass 2 merged record (run 43, 2026-11-09)

Two fresh opus runs of the same template on `v1/draft_v1_stage19pass1.md` (prompt `prompts/stage18_pass2_user.txt`).
Full reviews `18_review_pass2_run1.md` (A 4 / B 5; 31 + ~15 spot-checks), `18_review_pass2_run2.md` (A 4 / B 5;
36 spot-checks, independent CRC loop). **CRITICAL_FABRICATION: no** in both: H2a / H2b / H4e D, λ̂ indices, per-stratum
slip, 08e values, label-route values, detector rows all recomputed from raw files and exact.

## Verified by the main session
- 0.4739 is `h4a_label_rule.json → H4a_onset_full_rd_vs_full` (vs the squeeze arm *full*), not vs P → abstract wrong.
- Holm within secondary families and the Holm-adjusted H2-H guard are in `docs/07_hypotheses.md` (l.223, l.445);
  08f / 08g say Holm not applied → an undisclosed deviation.
- F4: `sim.py` writes an explicit `<inertial pos="0 0 com" mass=m>` for every family, so the sphere's mass / position do
  not set the CoM; the CoM offset is the sampled `com`.
- New report-only rows in `19_report_rows.json`: detector error correlates with log μ (r −0.253); SD by family
  F1 0.062, F2 0.045, F3 0.196, F4 0.063 (bias 0.31–0.33 in all); static touch: normal = F0 within 0.16 N, pad shear =
  m g / 2 to a relative 3.1e-4 at the 99th percentile (24 / 8,000 rows deviate > 1 %), preload slip 0 / 8,000.

## Must-fix for stage 19 pass 2 (paper-level)
P1 Abstract: 0.4739 is vs *full*; fix Table 2 caption (not every row vs P). Abstract ≤ 250 words.
P2 §3.4: CRC precondition (loss at the top grid point ≤ α; fallback λ̂ = max Λ voids the bound); state that no stratum
   used the fallback (λ̂ indices in `per_stratum_test_slip_crc08c` ≤ 15 of 0–19).
P3 Deviations list: Holm (07) not applied in 08f–08h; the probe arm, CSF-μ̂ and the H2a / H2b split come from the
   pilot-driven amendment 08a, which replaced 07's static / squeeze CertGrip.
P4 Realised slip: report label-route test slip of both arms and the direct-replay audit values that are in the JSON;
   unequal realised slip (0.0829 vs 0.1021) makes D conservative; explain the missing efficiency frontier (E1).
P5 Detector error is not constant: r −0.253 with log μ, F3 SD 0.196 vs ≤ 0.063 elsewhere; discuss for D-μ, D3 cells,
   H2-R; bias plausibly detection latency (label as a reading, untested).
P6 H4a recast: in this rigid-contact simulator static touch reads F0 and m g / 2 (static_touch_check), preload slip
   never occurs, so "static touch / squeeze add nothing" is a simulator consistency check, not a sensor finding.
P7 Online study: CertGrip tracker warm-started from the label-route q̂ with label feedback; H3-B result; 08a's note on
   S1 instances outside the probe's training friction range (quote the design doc).
P8 CI levels / draws: D-μ, D-FID and pooled H2-H intervals use the levels and draw counts in their JSON blocks; fix the
   blanket "97.5 %, 2,000 draws" claim.
P9 Framing: the operative method is probe + Coulomb plug-in or learner + CRC (H2b: learner adds no demonstrated gain);
   Algorithm 1 includes the probe step; drop "post hoc grid checks" from C2.

## Evidence-level (stage 20 / loop; carried from pass 1)
E1 high-probability (LTT / UCB) certificate + risk–efficiency frontier from the existing replays (report-only);
E2 friction-proxy non-tactile baseline / correlated-μ pool; E3 σ grounding; E4 practitioner baselines (probe + fixed
margin, reactive tightening); E5 classic grip-force literature.

**Decision:** no fabrication → stage 19 pass 2 on P1–P9, then stage 20.
