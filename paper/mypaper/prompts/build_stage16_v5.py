"""Build the stage-16 [v5] prompt from the verbatim template (pipeline/references/stage_prompts/paper_outline.md)."""
import os
R = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..")
rd = lambda p: open(os.path.join(R, p)).read()
topic = ("Amortizing a cost-aware greedy information-gain touch planner (G*) for active tactile localization under "
         "travel cost: a pre-registered five-cell characterisation (travel cost kappa = 2/4/8/12 on one shape library "
         "and a second shape library A16 at kappa = 2) of whether a policy distilled from the planner matches it, how "
         "it compares with reinforcement learning on the same objective and with hand-designed probing heuristics, "
         "and how the gap behaves as travel cost changes")
block = f"""=== HARD TOPIC CONSTRAINT ===

The paper MUST be about: {topic}

PROHIBITED content (unless user explicitly specifies case-study mode):

- Do NOT treat environment setup, dependency installation, or infrastructure failures as a research contribution.

- Do NOT present debugging logs, system errors, or configuration issues as experimental findings.

- Do NOT drift to tangential topics not directly related to the stated topic.

- Every section MUST connect back to the core research question.

- The Abstract and Introduction MUST clearly state the research problem derived from: {topic}

- The Method section MUST describe a technical approach, not a workflow.

- The Results section MUST report quantitative outcomes of experiments, not environment status.

=== END CONSTRAINT ===
"""
preamble = ("Target: RSS 2027 Stage 1 extended abstract (deadline 2026-12-04 AoE): <= 5 content pages + 1 page of "
            "references; methods complete, experiments may be preliminary. Paper type: measurement / characterisation "
            "paper only (results/v5/15_decision.md sections 4.2-4.4 give the frame, the contribution order C1-C5, and the "
            "allowed and disallowed claims; they are binding). Word targets scaled to 5 pages (about 3,000-3,500 words "
            "main body), a stated deviation from the 9-page floors of hard_constraints section 3; a master draft may be "
            "longer and is condensed in stage 22. This is the v5 revision of the v4 outline (paper/mypaper/v4/00_outline_v4.md) "
            "and draft (paper/mypaper/v4/draft_v4_final.md); v3 (S12) and v4 (S2) gate results enter as prior cells. "
            "Evidence links must name keys of results/v5/results_v5.json (blocks 12_d5_analysis.json, 14_test5_analysis.json, "
            "14_e5_analysis.json, 14_e6_analysis.json, 12_e7_analysis.json, 12_base_hstar.json, 12_rl_sweep_selection.json, "
            "13_freeze.json, 15_posthoc_derived.json) or results/v4/results_v4.json / results/v3/results_v3.json, and "
            "cite_keys from docs/05_knowledge_cards.json. Values from 15_posthoc_derived.json must be labelled post hoc, no CI.")
feedback = ("Prior feedback (v4 stage 18 peer review summary and v4 stage 20 quality gate, 5.0/10, which led to the "
            "owner-authorised v5 loop; v5 was designed to answer its evidence-level items):\n\n"
            + rd("paper/mypaper/v4/18_peer_review.md") + "\n\n" + rd("paper/mypaper/v4/20_quality_gate.json") + "\n\n")
analysis = rd("results/v5/14_analysis.md") + "\n\nPost-hoc derived values (results/v5/15_posthoc_derived.json):\n\n" \
    + rd("results/v5/15_posthoc_derived.json")
decision = rd("results/v5/15_decision.md")
user = f"""{preamble}


Create a detailed paper outline in markdown.

Include per-section goals and evidence links.

{block}{feedback}Analysis:

{analysis}


Decision:

{decision}
"""
d = os.path.dirname(os.path.abspath(__file__))
open(os.path.join(d, "stage16_v5_system.txt"), "w").write("You are an academic writing planner.\n")
open(os.path.join(d, "stage16_v5_user.txt"), "w").write(user)
print(len(user.split()), "words")
