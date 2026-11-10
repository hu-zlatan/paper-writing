# p2 Stage 20 QUALITY_GATE [v2] — plan (run 45, 2026-11-10)

- Template `quality_gate.md` verbatim, threshold 7.5, via `build_stage20.py paper/mypaper/draft_v2.md _v2`.
- Fresh opus subagent, paper only → `paper/mypaper/20_quality_gate_v2.json` (v1 gate stays at `20_quality_gate.json`).
- Decision by the template table: ≥ 7.5 → auto-approve (AUTOPILOT §1, record evidence) → stage 21; below with
  evidence-level weaknesses → stage 13 (refine cycle 2 / 3 available); paper-level only → stage 19.
