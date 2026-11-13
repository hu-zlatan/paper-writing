"""Build the stage-16 [v6] prompt from the verbatim template (pipeline/references/stage_prompts/paper_outline.md)."""
import os
R = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..")
rd = lambda p: open(os.path.join(R, p)).read()
topic = ("Amortizing a cost-aware greedy information-gain touch planner (G*) for active tactile localization under "
         "travel cost: a pre-registered five-cell characterisation (travel cost kappa = 2/4/8/12 on one shape library "
         "and a second shape library A16 at kappa = 2) of where a policy distilled from the planner sits on the "
         "accuracy-latency frontier relative to the full planner (with its run-to-run variance) and to reduced planners, "
         "whether DAgger adds anything over behaviour cloning, and how the evaluator grid affects these contrasts")
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
            "references; methods complete, experiments may be preliminary. Paper type: pre-registered measurement paper "
            "with one narrow positive claim (H6b frontier); results/v6/15_decision.md sections 4.3-4.5 give the frame, the "
            "contribution order C1-C4, the page budget, and the allowed and disallowed claims; they are binding. Word "
            "targets scaled to 5 pages (about 3,000-3,500 words main body), a stated deviation from the 9-page floors of "
            "hard_constraints section 3; a master draft may be longer and is condensed in stage 22. This is the v6 "
            "revision of the v5 outline (paper/mypaper/v5/00_outline_v5.md) and draft (paper/mypaper/v5/draft_v5_final.md); "
            "v6 supersedes the v5 test5 0-299 contrasts with 0-499 (primary) and 300-499 (fresh). Evidence links must name "
            "keys of results/v6/14_v6_analysis.json (cells.<cell>.<window>.H6a / H6b / H6c / v5_row_updates / holm / means, "
            "cells.<cell>.frontier, cells.<cell>.E12, H5b_update_0_499) or results/v6/15_derived_v6.json (post hoc, no CI) "
            "or results/v5/results_v5.json (validation D5, RL sweep, E6 latency, E7), and cite_keys from "
            "docs/05_knowledge_cards.json. Values from 15_derived_v6.json must be labelled post hoc, no CI.")
feedback = ("Prior feedback (v5 stage 18 peer review and v5 stage 20 quality gate, 5.5/10, which led to the "
            "owner-authorised v6 loop; v6 was designed to answer its evidence-level items):\n\n"
            + rd("paper/mypaper/v5/18_peer_review.md") + "\n\n" + rd("paper/mypaper/v5/20_quality_gate.json") + "\n\n")
analysis = rd("results/v6/14_analysis.md") + "\n\nPost-hoc derived values (results/v6/15_derived_v6.json):\n\n" \
    + rd("results/v6/15_derived_v6.json")
decision = rd("results/v6/15_decision.md")
user = f"""{preamble}


Create a detailed paper outline in markdown.

Include per-section goals and evidence links.

{block}{feedback}Analysis:

{analysis}


Decision:

{decision}
"""
d = os.path.dirname(os.path.abspath(__file__))
open(os.path.join(d, "stage16_v6_system.txt"), "w").write("You are an academic writing planner.\n")
open(os.path.join(d, "stage16_v6_user.txt"), "w").write(user)
print(len(user.split()), "words")
