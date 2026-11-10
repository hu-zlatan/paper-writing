# p2 Stage 13 [v2] — B3 online study with physical feedback (run 44, 2026-11-10)

Template `pipeline/references/stage_prompts/iterative_refine.md` (13c not used: pre-registered rows only).
Registered design: `docs/09_amendment_v2.md` §B3. Details fixed here **before any B3 replay or metric** (only the
existing 08c λ̂ indices and 08d pool sizes have been read):

- Pools, pre/stream roles and orderings exactly as `h3_streams.py` (08d §2): T = 2,000 (500 id + 1,500 shifted),
  `orderings()` with seed `[4242, SHIFTS.index(s), o]`, o ∈ {0,…,4}; shifts S1 and S3.
- Arms: OQT-P-CertGrip (log g = `a010_full_rd_s0.2_seed0` prediction) and OQT-P-CSF1 (log g = log f_nom), the same
  bases as the 08c arms `full_rd@0.2#0` / `CSF-1` and as 08d.
- Tracker per stratum, initial q_d = 08c CRC λ̂ of that arm and stratum (`crc_grids.json` grid at
  `crc_analysis.json` lam_idx; 08c route, as registered). η = the 08d η (0.1 × IQR of CertGrip's pooled cal
  label-rule scores). F_t = min(F_max, g_t e^{q}); feedback = physical slip of a protocol-rd replay at F_t
  (`Sim.run`, same SLIP settings as `main.py`); update q_d += η (slip_t − α) unless F_t was capped (08d anti-windup).
- Read-out (descriptive, no hypothesis test was registered): per arm and shift, mean over the 5 orderings (and min /
  max) of physical slip and RE (avoidable rows, F\*_mid) on steps 1–500 and steps 1,501–2,000 (registered windows),
  plus steps 1,001–2,000 (the 08d window, added for comparability with v1 H3). D = 1 − RE_CertGrip / RE_CSF1 per
  window. The label-rule OQT (08d simulator, same orderings, its own offline q̂ start) is printed alongside.
- Pilot rule: ≤ 5 min of replays of one stream → per-replay time × 40,000 replays (2 shifts × 5 orderings × 2 arms ×
  2,000) ≤ 6 CPU-h → run all; else downscale orderings 0–2 → S1 only → not run.
- Execution: sandbox (2 cores) or Actions; one JSONL per (shift, ordering, arm) in `results/v2/b3/`; code + test
  committed before the first stream.
