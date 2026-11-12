# p2 Stage 20 QUALITY_GATE [v4] — plan (run 48, 2026-11-12)
- Template `quality_gate.md` verbatim, threshold 7.5, via `build_stage20.py paper/mypaper/draft_v4.md _v4`.
- Fresh opus subagent, paper only → `paper/mypaper/20_quality_gate_v4.json`.
- Decision by the template table: ≥ 7.5 → auto-approve (AUTOPILOT §1, evidence recorded) → stage 21; below with
  evidence-level weaknesses → stage 13 is unavailable (refine cycles 3 / 3) → stop and ask the owner (OWNER_TODO);
  paper-level only → stage 19.
