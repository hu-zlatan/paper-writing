# p2 · Addendum 08e — CRC grid sensitivity (post hoc, run 40, 2026-11-09)

**Status:** written **after** the 08c CRC read-out (`results/v1/crc_analysis.json`) and the label-rule secondary
(`results/v1/h2_label_rule.json`) were seen, and before any replay of this addendum exists. It is a **post hoc
sensitivity analysis**; it does not replace the pre-registered 08c decisions, which stand as computed and are reported
with the defect below.

**Defect.** 08c centred each arm's 20-point grid on the pooled selection q̂ (±0.4). For the physics plug-ins the
per-stratum CRC solution in D1 / D2 lies at or below the grid floor (λ̂ index 0 for CSF-μ̂ at σ ≤ 0.2, index 1 for CSF-1),
so those arms over-protect and their RE is inflated; the CRC-route D(H2b) is biased towards CertGrip.

**Sensitivity design.** Per-stratum grids Λ_arm,d = q̂_sel,d + linspace(−0.8, 0.8, 41), q̂_sel,d the label-rule conformal
quantile at α of the arm's scores on the selection split within stratum d (objects 150–199; no cal / test data).
Arms: CertGrip-full seed 0 at σ 0 / 0.1 / 0.2 / 0.4, CSF-1, CSF-μ̂ at the four σ, onset-only σ 0.2.
Grids: `results/v1/crc_grids_v2.json` (`python crc_grids.py --v2`); replays `main.py crc --grids crc_grids_v2.json`
→ `results/v1/crc_v2/`; read-out `python analysis_crc.py --v2` → `results/v1/crc_analysis_v2.json`, the same CRC rule,
bootstrap and decision code as 08c. A floor- or ceiling-bound λ̂ is reported per arm and stratum.

**Reporting rule (fixed now).** The paper reports the 08c CRC decisions as pre-registered, the label-rule route, and this
sensitivity side by side. If the sensitivity changes a decision, the paper says so and treats the pre-registered CRC
result for that contrast as unreliable because of the grid defect; no decision is upgraded on the strength of a post
hoc analysis alone.
