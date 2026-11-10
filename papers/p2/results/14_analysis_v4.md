# p2 · Stage 14 RESULT_ANALYSIS [v4] — merged (run 47, 2026-11-10)

Pass 1 (fresh opus subagent, template verbatim via `docs/prompts/build_stage14_v4.py`): `14_analysis_v4_pass1.md`.
Pass 2 (fresh opus subagent, area-chair prompt verbatim, `docs/prompts/stage14_v4_pass2_*.txt`):
`14_analysis_v4_pass2.md` — 16 findings, 1 numeric (p bound: two-sided bootstrap p = 0.0 means p < 0.001, not
< 1/2,000; Holm worst case 0.005 — decisions unchanged), **no fabricated number** (every table cell re-checked at 4
s.f.). The main session spot-checked 13 pass-1 numbers against `results/v4/v4_analysis.json`; all match.
**Adjudication: all 16 pass-2 findings accepted; the pass-2 rewrites are binding where they differ from pass 1.**

Statements of record for stages 15–19 (C1–C5 confirmatory, Holm at 5 % over five p; S rows secondary; v1–v3 verdicts
not re-decided). Source for every number: `results/v4/v4_analysis.json`.
1. **C1 (probe sufficiency, fresh pool f4, σ 0.2, matched slip): superiority** — D(CSF-muhat@0.2 vs CSF-1) 0.4314,
   CI\*\* [0.3824, 0.4835], Holm p < 0.005. Prediction met.
2. **C2 (learner adds nothing, f4, σ 0.2, matched slip): equivalence at ±0.10** — D(full_rd@0.2#0 vs CSF-muhat@0.2)
   0.01117, CI\*\* [−0.05552, 0.05686]. Prediction met **on the registered matched-slip route only**: the CRC-route
   version (S5) is −0.06291 [−0.1226, 0.08396], which crosses −0.10 → not shown equivalent there. Do not write
   "probe + plug-in + CRC suffices" without this qualifier.
3. **C3 (H2a replication on fresh objects, CRC route): superiority** — D(full_rd@0.2#0 vs CSF-1) 0.4135, CI\*\*
   [0.3578, 0.4903]. Prediction met.
4. **C4 / C5 (friction-correlated pool c4, deployable family prior CSF-fam): not superior; the CI\*\* lies below 0** —
   C4 D(CSF-muhat@0.2 vs CSF-fam) −0.5814 [−0.7208, −0.4563]; C5 D(full_rd@0.2#0 vs CSF-fam) −0.5461 [−0.6590,
   −0.4290]. No prediction was registered. When friction is predictable from the visible family, a non-tactile
   family prior beats both tactile arms (CSF-fam RE_match 0.2674, slip 0.05929). The registered rule defines only
   superiority for C4 / C5; "inferiority" is the read-out code's label for CI\*\* < 0 and must be described as such.
5. **σ band (S1):** D(CSF-muhat vs CSF-1) 0.6486 / 0.4314 / −0.2065 at σ 0.1 / 0.2 / 0.4 (plug-in test slip 0.1014 > α
   at σ 0.4). D(learner vs plug-in) −0.1076 at σ 0.1 to 0.3238 at σ 0.4 → C2's equivalence is a σ 0.2 result; the
   mechanism behind the σ 0.4 learner advantage is not tested (v3 B1: a shrunk plug-in beat the learner at σ 0.4).
6. **Friction-width sweep (S3, f4, σ 0.2 only):** D(CSF-muhat vs CSF-1) 0.4314 → 0.2414 → −0.1094 → −0.6967 as the
   log-μ window shrinks from w 1.0 to 0.25 (prediction "shrinks with w, ≤ 0 near 0.25" met). The sweep does not vary
   σ and has no family prior, so it does **not** establish "pays off only when friction uncertainty exceeds probe
   noise" and does not explain C4 / C5 — state it as a descriptive trend.
7. **No-probe grasp (S6, f4):** no-probe CSF-1 slip 0.08714, hold 7.125 N. Measured break-even hold time vs it:
   full_rd@0.2#0 17.74 s, CSF-muhat@0.2 27.07 s (point values, no interval); for 1 s and 5 s holds the no-probe grasp
   uses the least force-time (22.20 / 50.70 N·s vs 39.10 / 63.57 for the learner). This replaces the v3 arithmetic
   break-even (16.56 / 28.61 s in `a7_integrated.json`, different test split).
8. **Certificate (S7, 200 re-splits of f4, σ 0.2 arms):** mean slip 0.0836–0.0867 ≤ α; 8–14.5 % of splits exceed α
   overall and 31.5–70 % have at least one stratum above α (plug-in 64.5 %); on c4 per-family slip reaches 0.3157
   (CSF-1, F1; exceedances concentrated in F1). The guarantee is marginal over the pool, not per stratum / family;
   "certified saving" must say marginal. Not re-split at σ 0.4.
9. Secondary details (S2 shrunk plug-in, S4 per-family, S5 routes) as in pass 1 with the pass-2 rewrites; the shrunk
   plug-in gain is not shown to exceed the 0.10 margin; a two-sided p of 0.915 is "no difference detected", not
   "confirmed equal".

Implication for stage 15: the attribution (probe drives the saving; the learner is not needed at σ 0.2) is now
confirmatory on fresh objects, but the saving is **conditional**: it vanishes or reverses with high probe noise, a
narrow friction range, a friction-informative family prior, or short holds. The paper must be framed around these
conditions, not around a general saving.
