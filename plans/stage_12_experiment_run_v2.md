# Stage 12 EXPERIMENT_RUN [v2] — pre-run gates G0–G5 (plan + record)

Plan (written run 3, recorded here in run 4): run the pre-registered gates of docs/07_hypotheses_v2.md §4 on CPU
(GitHub Actions), with every change written into docs/07c_amendment_v2_0.md before a check is re-run; no main run
starts before G0, G3, G4 and G5 pass. Gate decision → stage 15.

Record (run 4):
- G0 done (C(A) = 0.802 marginal fail, B7). G1 PASS. G2 FAIL after escalation → Idea 2 refuted for κ ≤ 12.
- G3 (i) hp1; (ii) FAIL 0.204 vs 0.410 (remedy read-out running); (iii) FAIL incl. remedy.
- G4 → B8: grid posterior adopted as the evaluation (no SMC kernel passes in every cell).
- G5: +10 pp everywhere; A0 degenerate (removed); flatness fails at κ = 6 and 12 (→ 64 × 8).
- Outcome: G3 failed → per §4 the gate routes to stage 15 (after the remedy read-out).
