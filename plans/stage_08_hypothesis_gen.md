# Stage 8 · HYPOTHESIS_GEN (multi-agent debate) · v1

## Goal
≥2 falsifiable hypotheses with rationale, measurable prediction (metric + threshold), failure condition (metric + threshold) and experiment sketch → docs/07_hypotheses.md.

## Tasks
- [ ] Pass 1 Proposer: fresh opus subagent, `stage_prompts/hypothesis_gen.md` pass-1 prompt verbatim, {synthesis} = docs/06_synthesis.md → docs/07a_proposer.md
- [ ] Pass 2 Skeptic: a different fresh opus subagent, pass-2 prompt verbatim on the proposer output → docs/07b_skeptic.md
- [ ] Pass 3 Methodologist: a third fresh opus subagent, pass-3 prompt verbatim → docs/07_hypotheses.md (canonical)
- [ ] Main session checks: every hypothesis falsifiable with numeric thresholds; feasible on CPU; consistent with the two core novelties; update docs/实验构想.md if the design changes.

## Inputs
- docs/06_synthesis.md, docs/00_topic_init.md (constraints only)

## Expected outputs
- docs/07a_proposer.md, docs/07b_skeptic.md, docs/07_hypotheses.md

## Hard-constraint checks
- [ ] Subagents get only the files they need, not this session's reasoning (AUTOPILOT §3).
- [ ] No hypothesis is trivially true; failure conditions quantitative.

---

## Output Summary  (filled in AFTER the stage runs)
