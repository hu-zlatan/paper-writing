"""Build the p2 stage-16 prompt from the verbatim template (pipeline/references/stage_prompts/paper_outline.md)."""
import json
import os
P2 = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..")
rd = lambda p: open(os.path.join(P2, p)).read()
topic = ("Certified-slip tactile grip regulation: a ramp-down friction-onset probe combined with distribution-free "
         "conformal risk control so that the physical slip rate of a minimal-force grasp is <= alpha, compared "
         "against the strongest non-tactile conformal baseline, with ablations showing where the force saving comes "
         "from (the probe, not the learned tactile model) and an online binary-feedback calibration study under "
         "distribution shift")
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
cards = json.load(open(os.path.join(P2, "docs/05_knowledge_cards.json")))
cards = cards.get("cards", cards) if isinstance(cards, dict) else cards
keys = "\n".join(f"- {c['cite_key']}: {c['title']}" for c in cards)
preamble = ("Target: RSS 2027 Stage 1 extended abstract (deadline 2026-12-04 AoE): <= 5 content pages + 1 page of "
            "references, no supplementary; methods complete, experiments may be preliminary. The re-scoped story in "
            "the Decision below (results/15_decision.md) is binding: the claim is the friction-onset probe plus "
            "conformal calibration, the learned tactile model adds no demonstrated gain (H2b), H1-M failed, H3 is "
            "inconclusive, and the H2-R scope limit must appear in abstract-level claims; the audit rewrites in the "
            "Analysis are binding. Word targets scaled to 5 pages (about 3,000-3,500 words main body), a stated "
            "deviation from the 9-page floors of hard_constraints section 3; a master draft may be longer and is "
            "condensed in stage 22. Evidence links must name blocks / keys of results/v1/results_v1.json (each block is "
            "an unchanged analysis file of results/v1/, e.g. crc_analysis.json, crc_analysis_v2.json, h2_label_rule.json, "
            "h4a_label_rule.json, h3_analysis.json, h1m_analysis.json, h1v_analysis.json, comp_selection.json, "
            "sec08f_*.json, sec08g.json, sec08h_*.json) and cite_keys from docs/05_knowledge_cards.json; the 52 "
            "available cite_keys are:\n" + keys)
feedback = ""
analysis = rd("results/14_analysis.md")
decision = rd("results/15_decision.md")
user = f"""{preamble}


Create a detailed paper outline in markdown.

Include per-section goals and evidence links.

{block}{feedback}Analysis:

{analysis}


Decision:

{decision}
"""
d = os.path.dirname(os.path.abspath(__file__))
open(os.path.join(d, "stage16_system.txt"), "w").write("You are an academic writing planner.\n")
open(os.path.join(d, "stage16_user.txt"), "w").write(user)
print(len(user.split()), "words")
