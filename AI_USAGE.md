# AI Usage Record

The research in this repository — topic selection, literature review, experiment code, experiment runs, analysis and the manuscript — is produced by an autonomous AI pipeline (Claude, running as a scheduled task) under the direction of the repository owner. The owner is responsible for reviewing and verifying everything before any submission.

## Target venue policy on LLM use

Target venue: **RSS 2027** (Robotics: Science and Systems). Official policy, from the call for papers at https://roboticsconference.org/information/cfp/ (checked 2026-10-28):

- "The use of LLMs is permitted for both authors and reviewers."
- Disclosure of LLM use is not mandatory but is strongly encouraged.
- Papers with hallucinated citations or references are desk-rejected; RSS runs automated checks.
- Authors are fully responsible for all submitted text (plagiarism, ethics) and for the reproducibility of results.

Recommendation for the owner: disclose in the submission that the research and manuscript were produced by an autonomous AI pipeline under the owner's direction, and check every reference before submitting.

## Scope of AI involvement

Kept current as the pipeline progresses: which artifacts were AI-generated, which were checked or edited by the owner, and which tools produced them.

- 2026-10-28 (run 1, stages 1–10 partial): topic, venue choice, MEGA_PROMPT.md, design docs, search plan, screening decisions, synthesis, theory notes, experiment plan and all code in `code/` written by Claude (scheduled run). Literature metadata come from the OpenAlex API (GitHub Actions run 40654783282). Knowledge cards (stage 6) and the stage-8 hypothesis debate were produced by fresh-context Claude subagents (sonnet for cards; opus for proposer / skeptic / methodologist). Nothing has been checked or edited by the owner yet.
- 2026-10-28 (runs 2–4, v2 gates → v3 hypotheses): all v2/v3 code, gate analyses and amendments written by Claude; experiments run on GitHub Actions from this repository's code. Stage 14 (analyst + area-chair pass), stage 15 decision and the v3 stage-8 debate were produced by fresh-context opus subagents. Nothing has been checked or edited by the owner yet.
- 2026-10-29 (run 5, stages 8.5–12 v3): theory note (stage 8.5) and experiment plan (stage 9) by fresh-context opus subagents with the template prompts; reference verification by a fresh subagent using web search/fetch; amendments v3.0/v3.1, all v3 code and analysis scripts written by Claude; experiments run on GitHub Actions from this repository's code. Nothing has been checked or edited by the owner yet.
