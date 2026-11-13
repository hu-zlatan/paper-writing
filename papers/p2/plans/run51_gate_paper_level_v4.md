# Run 51 · p2 paper-level revision of draft_v4 from the stage-20 [v4] gate (owner decision still pending)

- Why: run-48 default in papers/p2/OWNER_TODO.md ("你不回复时") — paper-level items only; no new experiments, no LaTeX.
- Input: the 4 [paper-level] weaknesses and 4 [paper-level] required actions of paper/mypaper/20_quality_gate_v4.json
  (crisp conditional answer up front; relative + absolute + force-time as one cost picture, attribution stated as
  unresolved; each caveat once in Limitations with cross-references; 2–3 significant figures in prose; earlier-round
  material §5.4 + mid-friction sub-pool to an appendix). Figure rendering is out of scope (Figure 2 already rendered
  run 50; Figure 1 is a schematic prompt).
- How: template stage_prompts/paper_revision.md verbatim via paper/mypaper/prompts/build_gatefix_v4.py; the reviews slot
  holds the gate's paper-level items + a binding block. Fresh opus subagent writes paper/mypaper/draft_v4.md;
  snapshot before → paper/mypaper/v4/draft_v4_pre_run51.md.
- Checks: tools_number_audit.py 0 unmatched; section word floors (RESTRICTS); Limitations not shortened or softened;
  no new number; evidence-level items appear only as limitations.
- Not a new gate pass: stage 20 status stays FAIL until the owner decides; no stage-20 rerun this run.
