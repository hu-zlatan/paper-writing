# Project Progress Log

> **This file is the single source of truth for what stage you are at, what version you are on, and what was decided when.**
> Append-only. Every stage writes one entry. Every loop (REFINE / PIVOT) writes a `LOOP MARKER` entry.
> See `pipeline/references/progress_tracking.md` for full conventions, and `AUTOPILOT.md` for how the scheduled runs operate.

**Project:** paper-writing
**Target venue:** RSS 2027 — Stage 1 extended abstract 2026-12-04 23:59 AoE; Stage 2 full paper (invited) 2027-04-16 23:59 AoE (verified 2026-10-28 at https://roboticsconference.org/information/cfp/)
**Topic:** Amortized, non-myopic active tactile localization (TouchBED)
**Initialised:** 2026-10-28T07:56:44Z
**Current version:** v1
**Latest stage:** Stage 1 TOPIC_INIT — next: stage 2 PROBLEM_DECOMPOSE

---

## Stage 0. PROJECT_INIT     [v1]

- **Started:** 2026-10-28T07:56:44Z
- **Finished:** 2026-10-28T07:56:44Z
- **Inputs used:** the owner's pipeline template (now `pipeline/MEGA_PROMPT.template.md`).
- **Outputs produced:**
  - Project skeleton at the repository root (`code/`, `data/`, `docs/`, `paper/mypaper/`, `plans/`, `results/`)
  - `RESTRICTS.yaml` (project fields filled in stage 1)
  - `AUTOPILOT.md` (run charter), `OWNER_TODO.md`, `AI_USAGE.md`
  - `pipeline/` (stage guide, stage prompt templates, hard constraints, helper scripts)
  - `MEGA_PROMPT.md` is not created yet: stage 1 fills the template's placeholders and saves it.
- **Decision:** PROCEED → stage 1.
- **Summary:** Repository bootstrapped for a scheduled run every 6 hours. Per the owner's directives, Claude chooses the topic (dexterous manipulation, tactile / visuotactile sensing, embodied AI and robot learning) and the target venue in stage 1; compute is CPU-first; gates 5, 9 and 20 auto-approve with logged reasons.
- **Commit:** bootstrap commit (first commit on `main`)

---

<!--
Append further stage entries below this line, in the format:

## Stage <N>. <STAGE_NAME>     [v<version>]

- **Started:** 2026-10-28T07:56:44Z
- **Finished:** 2026-10-28T07:56:44Z
- **Inputs used:**
  - path/to/input1
  - path/to/input2
- **Outputs produced:**
  - path/to/output1 (one-line summary)
  - path/to/output2
- **Decision (if applicable):** PROCEED  [or REFINE → N, or PIVOT → N]
- **Summary:** One paragraph describing what changed and why.
- **Commit:** <git short SHA>

For loop markers (REFINE / PIVOT), use:

## LOOP MARKER — <REFINE|PIVOT> from stage <X> → stage <Y>     [version v<a> → v<b>]

- **Reason:** ...
- **Snapshot taken:** ...
- **Next stage:** <Y> <STAGE_NAME>
- **Resuming under version:** v<b>
-->


## Planned route (non-linear; loop points marked)

1 → 2 → 3 → 4 → 5[GATE] → 6 → 7 → 8 → 8.5 → 9[GATE] → 10 → 11 → 12 → 13 ⇄ 14 → 15 {PROCEED→16 | REFINE→13 | PIVOT→8} → 16 → 17 → 18 → 19 → 20[GATE, fail→19, 3× fail→13] → 21 → 22 → 23[red flag→19] → 24 → 25 {REFINE→13 | PIVOT→16}. At least two full loops before DONE.
Milestones: v1 experiments ≈ 2026-11-20; extended-abstract-ready draft (5 pages) ≈ 2026-12-01 (owner decides whether to submit by 2026-12-04 AoE); full paper loops until 2027-04-01.

---

## Stage 1. TOPIC_INIT     [v1]

- **Started:** 2026-10-28T07:59:00Z
- **Finished:** 2026-10-28T08:20:00Z
- **Inputs used:** AUTOPILOT.md, pipeline/MEGA_PROMPT.template.md, RESTRICTS.yaml, pipeline/references/stage_prompts/topic_init.md, open issues (none), RSS 2027 CFP, web scan of recent active-tactile papers.
- **Outputs produced:**
  - docs/00_topic_init.md (SMART goal; sections Topic, Scope, SMART Goal, Constraints, Success Criteria, Generated)
  - MEGA_PROMPT.md (all template placeholders filled; cloud adaptations noted)
  - RESTRICTS.yaml (project block; pages_target 8, pages_extended_abstract 5)
  - docs/整体构想.md, docs/实验构想.md, docs/文献与问题.md (design docs, v1)
  - AI_USAGE.md (RSS 2027 LLM policy)
  - plans/stage_01_topic_init.md
- **Hardware detection (stage 1+):** pure CPU — 2 vCPU, 7 GB RAM, no NVIDIA/MPS GPU. Python 3.13, NumPy 2.5.3, SciPy 1.18.1, matplotlib 3.11.2, MuJoCo 3.17.0 (pip). Stage 10 will use numpy + a small CPU network; long sweeps can go to GitHub Actions CPU runners.
- **Decision:** PROCEED → stage 2.
- **Venue choice & reasons:** RSS 2027 (robot-learning venue that fits tactile localization; official dates verified; full-paper deadline 2027-04-16 leaves time for ≥2 full loops). ICML 2027 rejected for now: CFP not published, deadline only an estimate (~2027-01-22 AoE). Note RSS 2027's two-stage process: the full paper is open only to papers invited after a Stage 1 extended abstract (2026-12-04 AoE) — submitting is the owner's decision (OWNER_TODO).
- **Summary:** Topic: TouchBED — cast active tactile localization (object identity + pose from sparse probe contacts, including no-contact outcomes) as sequential Bayesian experimental design and train an amortized, non-myopic touch-selection policy on the sPCE lower bound of total EIG; compare with random, coverage and greedy particle-filter EIG; ablate the non-myopic objective, negative information and the history encoder; test transfer from a geometric probe model to MuJoCo physical contacts. Two core novelties only. Gap evidence from Gordon et al. 2025 (local Fisher-EIG) and Shahidzadeh et al. 2025 (RL exploration without an information objective); all literature still to be verified in stage 4.
- **Commit:** see git log ("stage 1 TOPIC_INIT")
