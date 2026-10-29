# Stage 16 PAPER_OUTLINE [v3] — plan (run 7, 2026-10-29)

- Template: `pipeline/references/stage_prompts/paper_outline.md`, verbatim, fresh-context opus subagent.
- {preamble}: target RSS 2027 Stage 1 extended abstract (default until the owner decides; OWNER_TODO): ≤ 5 content
  pages + 1 page of references, no supplementary; methods complete, experiments may be preliminary; outcome row 4
  (characterisation paper, no method claim). Word targets scaled to 5 pages (≈ 3,000–3,500 words main body) and stated
  as a deviation from the 9-page floors of hard_constraints §3.
- {topic_constraint}: the block of `pipeline/references/topic_constraint_block.md` verbatim with {topic} =
  "Active tactile localization under travel cost: how much headroom one-step look-ahead leaves over greedy cost-aware
  information-gain touch selection, and whether that greedy planner can be amortized by a learned policy (distillation
  from the planner vs reinforcement learning on the same objective)".
- {feedback}: empty (first pass). {analysis}: `results/v3/14_analysis.md`. {decision}: `results/v3/15_decision.md`.
- Output: `paper/mypaper/sections/00_outline.md`; evidence links must name keys of `results/v3/results_v3.json` and
  `cite_key`s from `docs/05_knowledge_cards.json`. The exploratory B-fan row is still running: the outline carries both
  pre-written readings.
