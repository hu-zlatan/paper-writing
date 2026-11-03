# Plan: condensed draft (preparation only) [v4]

**Why now.** The stage-20 escalation is still unanswered, so only the OWNER_TODO default applies: low-risk work,
including "text condensation that changes no conclusion", and no LaTeX export or new loop. Options (a) and (b) both need
a much shorter text than the 12,000-word master, and (b) has a hard date (RSS Stage 1, 2026-12-04 AoE). Doing the
condensation now costs nothing if the owner picks (c) or (d), and removes the main bottleneck if they pick (a) or (b).

**What this is not.** Not stage 22: no template, no LaTeX, no page count, no stage advanced, no gate re-scored. The
master `draft_v4.md` stays unchanged and stays the source of truth.

**Output.** `paper/mypaper/sections/draft_v4_condensed.md`, about 3,000 words, one results table, a limitations section.

**Rules.**
- No new number, claim, citation or derived figure: every numeric token and cite key must occur in `draft_v4.md`.
- Keep every verdict's qualifier: failed gates, exploratory status, reused test split, one cell per regime, RL setup only.
- The page limit can only be confirmed on a compiled PDF, so no page claim is made.

**Checks.** Token and cite-key comparison against the master; `tools_number_audit.py`; one fresh subagent comparing the
two texts for lost qualifiers or changed meaning, given only those two files.
