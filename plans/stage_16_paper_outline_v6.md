# Stage 16 PAPER_OUTLINE [v6] — plan (run 50, 2026-11-13)

- Pre-step (stage-15 [v6] §4.1): `code/tools_results_v6.py` → `results/v6/15_derived_v6.json` (done; post hoc, no CI).
- Template `pipeline/references/stage_prompts/paper_outline.md` verbatim, fresh opus subagent; prompt files
  `paper/mypaper/prompts/stage16_v6_{system,user}.txt` built by `paper/mypaper/prompts/build_stage16_v6.py`.
- {preamble}: RSS 2027 Stage 1 extended abstract (≤ 5 content pages + 1 reference page), measurement paper with the
  narrow H6b frontier claim per `results/v6/15_decision.md` §4.3–4.5; evidence keys from `results/v6/14_v6_analysis.json`,
  `15_derived_v6.json`, `results/v5/results_v5.json`; cite_keys from `docs/05_knowledge_cards.json`.
- {topic_constraint}: block verbatim, topic updated to the v6 frontier framing.
- {feedback}: v5 stage-18 merged review + v5 stage-20 gate JSON. {analysis}: `results/v6/14_analysis.md` + derived JSON;
  {decision}: `results/v6/15_decision.md`.
- v5 outline already snapshotted at `paper/mypaper/v5/00_outline_v5.md`. Output `paper/mypaper/sections/00_outline.md`.
- Self-check (`hard_constraints.md`): every number traceable to a JSON key; none of the §4.5 disallowed claims; Figure 1
  plan; row map with JSON keys.
