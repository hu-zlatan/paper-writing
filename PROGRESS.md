# Project Progress Log

> **This file is the single source of truth for what stage you are at, what version you are on, and what was decided when.**
> Append-only. Every stage writes one entry. Every loop (REFINE / PIVOT) writes a `LOOP MARKER` entry.
> See `pipeline/references/progress_tracking.md` for full conventions, and `AUTOPILOT.md` for how the scheduled runs operate.

**Project:** paper-writing
**Target venue:** RSS 2027 — Stage 1 extended abstract 2026-12-04 23:59 AoE; Stage 2 full paper (invited) 2027-04-16 23:59 AoE (verified 2026-10-28 at https://roboticsconference.org/information/cfp/)
**Topic:** Amortized, non-myopic active tactile localization (TouchBED)
**Initialised:** 2026-10-28T07:56:44Z
**Current version:** v1
**Latest stage:** Stage 9 EXPERIMENT_DESIGN [GATE] — next: stage 10 CODE_GENERATION

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
- **Finished:** 2026-10-28T08:07:19Z
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

---

## Stage 2. PROBLEM_DECOMPOSE     [v1]

- **Started:** 2026-10-28T08:07:20Z
- **Finished:** 2026-10-28T08:07:56Z
- **Inputs used:** docs/00_topic_init.md, design docs.
- **Outputs produced:** docs/01_problem_tree.md (6 prioritized sub-questions, 7 risks with mitigations); plans/stage_02_problem_decompose.md
- **Decision:** PROCEED → stage 3.
- **Summary:** Root question: does a policy trained on the total-EIG bound beat myopic EIG and match it at far lower online compute, and does this survive physical contact? Priorities: SQ1 non-myopic benefit, SQ3 negative information/multimodality, SQ2 amortization cost, SQ4 transfer, SQ5 bound tightness, SQ6 SE(3) (stretch). Biggest risks: greedy EIG may already be near-optimal (adaptive submodularity) and a close precursor may exist — both checked in stages 4–8.
- **Commit:** see git log ("stage 2 PROBLEM_DECOMPOSE")

---

## Stage 3. SEARCH_STRATEGY     [v1]

- **Started:** 2026-10-28T08:07:57Z
- **Finished:** 2026-10-28T08:08:31Z
- **Inputs used:** docs/01_problem_tree.md
- **Outputs produced:** docs/02_search_plan.yaml (5 strategies, 22 queries + 4 seminal queries), docs/02_sources.json (4 sources); plans/stage_03_search_strategy.md
- **Decision:** PROCEED → stage 4.
- **Summary:** Strategies cover direct active-tactile localization, tactile pose estimation/sensing, Bayesian experimental design (DAD, EIG bounds, RL-BED), active perception/information gathering (submodularity, belief-space planning), and dexterous manipulation with touch. Pre-2018 seminal touch-localization work is collected separately without the year filter.
- **Commit:** see git log ("stage 3 SEARCH_STRATEGY")

---

## Stage 4. LITERATURE_COLLECT     [v1]

- **Started:** 2026-10-28T08:08:32Z
- **Finished:** 2026-10-28T08:56:35Z
- **Inputs used:** docs/02_search_plan.yaml
- **Outputs produced:** code/literature/collect.py, .github/workflows/literature.yml (GitHub Actions; push of the workflow was accepted), docs/03_candidates.jsonl (681 unique real records from 800 raw hits), docs/03_collect_log.json
- **Decision:** PROCEED → stage 5.
- **Summary:** Real-API collection on GitHub Actions. OpenAlex answered all 26 queries; arXiv (all) and Semantic Scholar (20/26) were rate-limited (HTTP 429) on shared runner IPs — logged, not hidden. cite_keys generated once here and treated as immutable. Collector hardened (time budget, failing-source skip) and the workflow now only re-runs when the search plan changes.
- **Commit:** fa5bf90 (Actions) + this stage commit

---

## Stage 5. LITERATURE_SCREEN  [GATE]     [v1]

- **Started:** 2026-10-28T08:56:36Z
- **Finished:** 2026-10-28T08:58:42Z
- **Inputs used:** docs/03_candidates.jsonl
- **Outputs produced:** code/literature/screen.py, code/literature/screen_decisions_v1.py, docs/04_prefiltered.tsv, docs/04_screen_decisions.json, docs/04_shortlist.jsonl (56 papers)
- **Decision:** PROCEED → stage 6. **GATE auto-approved** (AUTOPILOT §1). Evidence: 56 ≥ 30 entries; all search themes covered; every entry has an OpenAlex/DOI/arXiv identifier; original fields preserved (merge asserts identical titles); year filter applied with 7 explicit seminal exceptions; off-topic matches (human touch neuroscience, touch screens, whisker biology) rejected.
- **Summary:** The screen surfaced a near precursor — Zheng et al. 2026 (arXiv:2603.21410) — that already uses contact + free-space evidence for joint class/pose belief with greedy next-touch selection; together with Koval et al. 2015 this means negative information alone is not a novelty. Core novelty #2 must be reframed in stage 7/8 (risk R5 partly realized). Also: RL-DAD (Lim et al. 2022) already does policy-based BED for non-differentiable simulators, so the contribution is the tactile formulation, its analysis (myopic vs non-myopic, amortization cost), and transfer evidence.
- **Commit:** see git log ("stage 5 LITERATURE_SCREEN")

---

## Stage 6. KNOWLEDGE_EXTRACT     [v1]

- **Started:** 2026-10-28T08:58:43Z
- **Finished:** 2026-10-28T09:01:13Z
- **Inputs used:** docs/04_shortlist.jsonl
- **Outputs produced:** docs/05_knowledge_cards.json (56 cards), code/literature/build_cards_v1.py
- **Decision:** PROCEED → stage 7.
- **Summary:** Abstract-level evidence cards (fresh sonnet subagent, stage prompt verbatim; identifiers filled by script). Validation: cite_keys/titles identical to the shortlist; no number absent from the source abstract. Main gap signals: all tactile touch-selection work is greedy/one-step and online; learned tactile exploration policies optimize task rewards, not information bounds; policy-based BED has not been evaluated on tactile/robot problems; no per-decision latency reported for touch selection.
- **Commit:** see git log ("stage 6 KNOWLEDGE_EXTRACT")

---

## Stage 7. SYNTHESIS     [v1]

- **Started:** 2026-10-28T09:01:14Z
- **Finished:** 2026-10-28T09:02:53Z
- **Inputs used:** docs/05_knowledge_cards.json; full text of arXiv:2603.21410v1 (WebFetch)
- **Outputs produced:** docs/06_synthesis.md (7 clusters, 5 falsifiable gaps, ranked opportunities)
- **Decision:** PROCEED → stage 8.
- **Summary:** Touch selection in the literature is online and one-step (greedy EIG, Fisher-EIG, submodular surrogates) or heuristic (Zheng 2026: max–min distance on the MAP shape); learned tactile policies use task rewards; policy-based BED is untested on touch. Ranked gaps: (1+2) amortized non-myopic information-bound policy and the myopic vs non-myopic measurement, (3) decision latency, (4) planning for no-contact outcomes inside the policy — core novelty #2 reframed because no-contact evidence in beliefs is prior art (Koval 2015, Zheng 2026), (5) fidelity transfer.
- **Commit:** see git log ("stage 7 SYNTHESIS")

---

> Note: timestamps of stages 1–8 were corrected to the git commit times (earlier entries had estimated times).

## Stage 8. HYPOTHESIS_GEN (multi-agent debate)     [v1]   ← PIVOT target of stage 15

- **Started:** 2026-10-28T09:03:00Z
- **Finished:** 2026-10-28T09:16:55Z
- **Inputs used:** docs/06_synthesis.md, docs/00_topic_init.md
- **Outputs produced:** docs/07a_proposer.md, docs/07b_skeptic.md, docs/07_hypotheses.md (canonical)
- **Decision:** PROCEED → stage 8.5.
- **Summary:** Debate by three independent fresh-context opus subagents. Final set: H1a non-inferiority to full greedy PF-EIG + beats random/coverage; H1b ≥100× lower latency at matched accuracy; H1c information objective beats sparse task-reward RL; H2a non-myopic > myopic control on the ambiguous set at small budgets; H2b set-up-move mechanism + analytic positive control; H3 planning for no-contact outcomes; H4 MuJoCo transfer under a measured contact shift; secondary H2c, H5′. Myopic control differs from ours only in credit assignment (γ=0 vs full returns-to-go on identical sPCE increments, L=255), which removes the MI chain-rule confound flagged by the skeptic. Pre-registered paired-episode statistics with crossed bootstrap and Holm correction; manipulation check on a quantitative myopia gap before main runs. Compute estimate ≈ 71 CPU-h.
- **Commit:** see git log ("stage 8 HYPOTHESIS_GEN")

---

## Stage 8.5. THEORETICAL_BOUNDS     [v1]

- **Started:** 2026-10-28T09:18:00Z
- **Finished:** see commit time ("stage 8.5 THEORETICAL_BOUNDS")
- **Inputs used:** docs/07_hypotheses.md
- **Outputs produced:** docs/07b_theoretical_bounds.md
- **Decision:** PROCEED → stage 9.
- **Summary:** Selection cost: greedy PF-EIG O(N·C·(V+M)) per decision vs policy O(d²), independent of belief resolution; training O(E·T·(L+1)·V). No convergence guarantee claimed for PPO (informal only). Key finding: the sPCE bound is capped at log(L+1) = 5.55 nats for L = 255, below the ≈ 8.1 nats needed for the success criterion, so the experiment design must raise L (or use a justified alternative) and measure saturation in the pilot.
- **Commit:** see git log

---

## Stage 9. EXPERIMENT_DESIGN  [GATE]     [v1]

- **Started:** 2026-10-28T09:19:00Z
- **Finished:** see commit time ("stage 9 EXPERIMENT_DESIGN")
- **Inputs used:** docs/07_hypotheses.md, docs/07b_theoretical_bounds.md
- **Outputs produced:** docs/08_experiment_plan.yaml; docs/实验构想.md v1.1 note
- **Decision:** PROCEED → stage 10. **GATE auto-approved** (AUTOPILOT §1). Evidence: all required keys present and every effective component (non-myopic credit assignment, planning for no-contact outcomes, DeepSets encoder, contrastive count L, budget input) has an ablation row (script-checked); every baseline has an equal-effort tuning protocol (12-config search for learned methods, 18-config Pareto sweep for greedy PF-EIG, C sweep for coverage); metrics have formulas; compute is pilot-gated and sharded on GitHub Actions.
- **Summary:** Deviation D1 — the contrastive count L is chosen by a pre-registered pilot rule from {255, 1023, 4095} because sPCE ≤ log(L+1) (stage 8.5); D2 — if L = 4095, core seeds 10 → 6 before any primary episode count is cut. Side note: the second literature workflow run (40657337558) failed and did not overwrite the stage-4 candidates, so all cite_keys remain those of run 40654783282.
- **Commit:** see git log
