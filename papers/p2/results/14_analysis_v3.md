# p2 · Stage 14 RESULT_ANALYSIS [v3] — merged (run 46, 2026-11-10)

Pass 1 (fresh opus subagent, template verbatim via `docs/prompts/build_stage14_v3.py`): `14_analysis_v3_pass1.md`.
Pass 2 (fresh opus subagent, area-chair prompt verbatim): `14_analysis_v3_pass2.md` — 15 findings, 3 numeric (B3 D_RE
range, phase total 27.4258 not 27.429, p bound < 0.001 not < 0.0005), no fabricated number.
**Main-session adjudication: all 15 accepted; the pass-2 rewrites are binding where they differ from pass 1.**
One pass-1 statement is corrected by the main session: the B3 oracle reference is not missing — `b3_analysis.json`
carries the 08d label-route rows (Oracle-CertGrip / Oracle-COMP) as its reference, as the B3 code's docstring states;
what is absent is a physical-replay oracle. A7's integrated-force / break-even quantities registered in amendment A7
were **not produced by code**; pass 1 reconstructed them by hand → they must not enter the paper until computed by a
script (stage 16/17 rows, or stated as not produced).

Statements of record for stages 15–19 (all v3 rows secondary / descriptive; v1 / v2 verdicts not re-decided):
1. H2a (CertGrip-full σ 0.2 vs CSF-1) holds at pool level in every v3 row (CRC, empirical margin, refined grid, B3
   windows), but reverses to **inferiority inside the 08e μ ∈ [0.5, 0.8] sub-pools** (A4: μ ∧ amp −0.3152 [−0.5231,
   −0.0172]; μ only −0.1717 [−0.4275, −0.01539], which contains it) at a higher CSF-1 slip (0.1004 vs 0.08394); on
   08c the same sub-pool shows superiority (0.3754). Grid-dependent; mechanism not established.
2. B3 D_RE 0.3107–0.4432 across shifts and windows (0.4152–0.4432 outside the S1 transient); late-window slip
   0.1001 / 0.1008 / 0.1018 (S1 / S2 / S3) with ordering-only intervals containing α → "consistent with convergence".
3. Learned vs plug-in: none of the 8 new σ 0.2 contrasts is shown (points −0.06463 to 0.05379). At σ 0.4 a **shrunk
   one-line plug-in beats the learned arm** (B1 −0.1395 [−0.1832, −0.01264]); the registered prediction was wrong in
   direction. The v1 σ-curve is qualified, not overturned. Same-grid σ 0.2 row: −0.0353 [−0.1688, 0.0103] not shown.
4. Certificate: mean re-split slip ≤ α; per-stratum exceedance frequent (A1); empirical margin = CRC on 08c, costs
   0.0142 RE for plug-in 0.2 on 08e.
5. B2 registered reactive designs fail (slip ≥ 0.3086 in every arm and stratum); detection timing not reported → no
   mechanism claim.
6. A3 Holm (v1 secondaries, 52 rows, all reproduced exactly): no v1 verdict changes; v3 rows carry no adjusted p.
7. Force: on the 08c test split CertGrip-full mean hold force is 1.085 N below CSF-1 (6.521 vs 7.606 N), no interval.
