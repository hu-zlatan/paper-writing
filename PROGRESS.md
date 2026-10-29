# Project Progress Log

> **This file is the single source of truth for what stage you are at, what version you are on, and what was decided when.**
> Append-only. Every stage writes one entry. Every loop (REFINE / PIVOT) writes a `LOOP MARKER` entry.
> See `pipeline/references/progress_tracking.md` for full conventions, and `AUTOPILOT.md` for how the scheduled runs operate.

**Project:** paper-writing
**Target venue:** RSS 2027 — Stage 1 extended abstract 2026-12-04 23:59 AoE; Stage 2 full paper (invited) 2027-04-16 23:59 AoE (verified 2026-10-28 at https://roboticsconference.org/information/cfp/)
**Topic:** Amortized, non-myopic active tactile localization (TouchBED)
**Initialised:** 2026-10-28T07:56:44Z
**Current version:** v3
**Latest stage:** Stage 16 PAPER_OUTLINE [v3] done (row-4 characterisation paper) → stage 17 next; see the end of this file

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

---

## Stage 10. CODE_GENERATION     [v1]   (IN PROGRESS — no Finished timestamp yet)

- **Started:** 2026-10-28T09:21:00Z
- **Done so far:** code/touchbed/{shapes,geometry,likelihood,pf,policies,evaluate}.py + tests (code/tests, 10 passing): procedurally generated sets A/S/PC, vectorized ray casting, ε-softened observation model, particle filter with resample-move, random / coverage / greedy PF-EIG baselines, episode runner. Dev smoke test in results/v1/dev/pilot0_baselines.md (timing only).
- **Environment:** PyTorch not installable (download.pytorch.org blocked by the egress proxy; PyPI torch pulls GB-scale CUDA deps) → the policy network and PPO are written in numpy with hand-written backprop (gradient-checked). shapely 2.2 and pytest installed via pip.
- **Deviation D3 (from docs/07_hypotheses.md §1.3):** primary IG_T estimator is now the SMC-evidence form log p(h|s0) − log Ẑ(h) (no KDE); the KDE version is kept as a diagnostic because it is strongly biased low for broad posteriors. The evidence form is biased high when particles are sparse — to be quantified by the N vs 4N check.
- **Added:** code/touchbed/nn.py (numpy DeepSets/MLP with hand-written backprop, Adam; finite-difference gradient tests pass), code/touchbed/train.py (batched sPCE rollouts with L contrastive samples, PPO with γ=1 / γ=0 credit assignment, No-NC ablations, RL-success baseline, plateau rule, 80 % time_guard), dev pilots code/dev/pilot{1,2}_*.py.
- **BLOCKERS found by dev pilots (docs/10_dev_findings_v1.md):** F1 (critical) the evaluation particle filter is far from converged — same 20 episodes give success 0.50 at N=4k vs 0.90 at N=40k, IG 25.6 vs 12.6 nats; needs contact-conditioned proposals / tempering and a grid reference before any comparison. F2 total-state sPCE saturates (L=255 cap 5.55 nats reached by an untrained policy in 75–97 % of episodes; L=4095 still 29–97 %) and total-state information is misaligned with the success criterion → re-open the stage-9 design: decision-relevant (identity/symmetry-mode) information objective or L=4095 at small budgets. F3 measured costs.
- **F1 progress (same run):** contact-conditioned MH proposals added to the PF (closed-form density, unit-tested); on the same 20 episodes success/identity are stable from N=2k (0.80/0.85) to 32k (0.75/0.85) vs 0.50/0.55 for the old PF at 4k. Evidence-based IG still drifts with N (15.9 → 11.8) → replaced as metric candidate by "ball information" (log posterior/prior mass of the success region; 7.70 at 8k vs 7.73 at 32k). See docs/10_dev_findings_v1.md.
- **Next (resume here):** formal N vs 4N convergence check (≥300 episodes) for the new PF, decide F2 (objective) and the metric change, decide F2 and amend docs/07_hypotheses.md / docs/08_experiment_plan.yaml with a dated v1.1 note, then finish stage 10 (learned-policy evaluation adapter, stats.py, main.py with TIME_ESTIMATE + results.json, MuJoCo eval, numpy2 check, README/requirements).
- **Finished:** 2026-10-28 (run 2, see commit "stage 10 CODE_GENERATION: complete")
- **Run-2 additions:** learning sanity pilot (val success 0.14 → 0.48 within 3·10⁴ episodes at L=1023, results/v1/dev/pilot3_learning.md); dated amendment docs/07c_amendment_v1_1.md (A1 L=4095 per the pre-registered D1 rule with seeds 6 and E_train cap 10⁵; A2 ball information co-primary instead of IG_T; A3 contact-conditioned PF; A4 cost re-estimates; A5 GRU variant dropped); stats.py; main.py CLI; per-index episode streams; experiments workflow for Actions. MuJoCo evaluation deferred until H4 work (documented).
- **Decision:** PROCEED → stage 11.

---

## Stage 11. RESOURCE_PLANNING     [v1]

- **Started:** 2026-10-28T09:56:00Z
- **Finished:** 2026-10-28T10:10:00Z
- **Inputs used:** docs/08_experiment_plan.yaml, docs/07c_amendment_v1_1.md, pilot logs from Actions run 40668209040
- **Outputs produced:** docs/11_schedule.json; experiments/pfcheck_v1.json (launched), experiments/hpsearch_v1.json; MuJoCo probe (code/touchbed/mujoco_eval.py, tested) added at the end of stage 10
- **Decision:** PROCEED → stage 12.
- **Summary:** Mandatory pilot ran on the actual runners and printed TIME_ESTIMATE: training 0.8–1.6 CPU-h per run at L=4095, greedy evaluation ≈ 21–31 CPU-h for the full grid. Total ≈ 150–200 CPU-h, feasible with ~20 concurrent GitHub Actions jobs over several runs; seeds per amendment A1 / RESTRICTS scaling rules. rl_success uses a training PF with N=500 / 2 MH steps (0.08 s per episode) to fit the equal 1e5-episode budget.
- **Commit:** see git log ("stage 11 RESOURCE_PLANNING")

---

## Stage 12. EXPERIMENT_RUN     [v1]   (partial: pre-run checks only)

- **Started:** 2026-10-28T10:08:00Z
- **Finished:** 2026-10-28T10:40:00Z (stopped after the manipulation checks, as pre-registered)
- **Inputs used:** docs/11_schedule.json, experiments/pfcheck_v1.json, code/run_checks.py
- **Outputs produced:** results/v1/pfcheck/ (Actions run 40668209040), results/v1/12_pfcheck_analysis.json, results/v1/checks/{confusability,myopia}_*.json, results/v1/12_manipulation_checks.md
- **Summary:** Confusability passes (C(S)=0.971, C(A)=0.772). **Myopia-gap manipulation check fails**: G(S) = −0.033 (mean abs. gap −0.110 ± 0.035 nats), G(A) = −0.020; identity-only exploratory gap on S +0.005 ± 0.012 nats — no evidence that look-ahead beats greedy one-step EIG in this action space. Evaluation PF not converged at 8k (success up to 6 pp and ball information 0.1–0.4 nats below 32k). Greedy beats random strongly at T=3 (A 0.767 vs 0.123, S 0.420 vs 0.133). The hyperparameter-search run (40669782607) was cancelled before completion because the pre-registration requires passing manipulation checks before main runs; its partial logs in results/v1/logs/hp_* are not used.
- **Commit:** see git log

---

## Stage 13. ITERATIVE_REFINE     [v1]

- **Started:** 2026-10-28T10:40:00Z
- **Finished:** 2026-10-28T10:46:00Z
- **Outputs produced:** code/touchbed/pf.py (root-cause fix of the log1p underflow warning); plans/stage_13_iterative_refine_v1.md
- **Decision:** PROCEED → stage 14.
- **Summary:** One numerical warning repaired at its root cause (mirrored normal tail); no non-finite results. PF mixing and the failed myopia check are design questions forwarded to stages 14–15.

---

## Stage 14. RESULT_ANALYSIS     [v1]   (pre-run checks)

- **Started:** 2026-10-28T10:47:00Z
- **Finished:** 2026-10-28T10:52:00Z
- **Inputs used:** results/v1/12_manipulation_checks.md, results/v1/12_pfcheck_analysis.json, results/v1/checks/*.json, docs/07_hypotheses.md, docs/07c_amendment_v1_1.md
- **Outputs produced:** results/v1/14_analysis.md (fresh opus subagent + area-chair pass)
- **Decision:** PROCEED → stage 15.
- **Summary:** G(S) = −0.033 [−0.054, −0.014] fails; G estimator not validated and run at reduced C/M (undocumented deviation, now flagged); PF at 8k not converged in all 6 cells; confusability per-shape rule broken for A2/A4/A6 and S self-symmetry entries are an artefact; H3 untestable (R_NC(S)=0.03); H1 untested. Main runs remain blocked by the pre-registration.

---

## Stage 15. RESEARCH_DECISION     [v1]

- **Started:** 2026-10-28T10:53:00Z
- **Finished:** see commit "loop v2: PIVOT from stage 15 to stage 8"
- **Inputs used:** results/v1/14_analysis.md, results/v1/12_manipulation_checks.md (incl. PC addendum)
- **Outputs produced:** results/v1/15_decision.md (fresh opus subagent)
- **Decision:** PIVOT → 8.
- **Summary:** No main experiment ran, but the pre-registered manipulation checks contradict the premise of H2a/H3 in this action space (any probe is reachable at equal cost): no measurable look-ahead value on S, A or PC, and no-contact outcomes are rarely decision-relevant. Rather than re-designing S until the check passes, v2 re-centres on (1) amortization — non-inferiority to greedy PF-EIG at ≥ 100× lower latency with a goal-oriented objective — and (2) a gated test of look-ahead under a realistic travel/time-budget action model (κ sweep, κ = 0 = v1 as control). Pre-run gates G0–G5 (hygiene, estimator validation against an exactly computed notch gap, travel manipulation check, learnability, PF convergence on ≥ 600 paired episodes, comparator strength).

---

## LOOP MARKER — PIVOT from stage 15 → stage 8     [version v1 → v2]

- **Reason:** pre-run manipulation checks failed the premise of the non-myopic hypothesis (G(S) = −0.033 [−0.054, −0.014] vs required ≥ 0.10; identity-only +0.003; PC bank also no gap) and of H3 (R_NC(S) = 0.03); see results/v1/14_analysis.md and results/v1/15_decision.md.
- **Snapshot taken:** results/v1/ (all v1 artefacts stay there unchanged); no paper files exist yet (paper/mypaper/v1/ not needed). docs/07_hypotheses.md, docs/07c_amendment_v1_1.md and docs/08_experiment_plan.yaml remain as the v1 record; v2 writes docs/07_hypotheses_v2.md and docs/08_experiment_plan_v2.yaml.
- **Next stage:** 8 HYPOTHESIS_GEN
- **Resuming under version:** v2
- **Still valid for v2:** code/touchbed (geometry, likelihood, contact-conditioned PF, greedy/coverage/random, numpy PPO, stats, MuJoCo probe), literature (docs/03–06), the decision-calibrated L=4095 finding and ball-information metric (amendment A1/A2), measured costs.

---

## Stage 8. HYPOTHESIS_GEN (multi-agent debate)     [v2]

- **Started:** 2026-10-28T10:57:00Z
- **Finished:** see commit "stage 8 v2 HYPOTHESIS_GEN"
- **Inputs used:** docs/06_synthesis.md, results/v1/14_analysis.md, results/v1/15_decision.md, docs/07c_amendment_v1_1.md
- **Outputs produced:** docs/07a_proposer_v2.md, docs/07b_skeptic_v2.md, docs/07_hypotheses_v2.md (canonical)
- **Decision:** PROCEED → stage 8.5 (v2).
- **Summary:** Two core ideas. H1 (guaranteed): an amortized policy trained on decision-calibrated sPCE is non-inferior to cost-aware greedy PF-EIG on the same ball-information target and same 256-action set, at ≥ 100× lower latency at matched accuracy. H2 (gated): with a travel cost κ between probes under a time budget, look-ahead beats both greedy and a cost-aware myopic policy at κ_hi on set S, with a κ×method interaction test and a κ = 0 negative control; a failed headroom gate is recorded as a refutation in the tested range. Pre-run gates G0–G5 (hygiene incl. a κ=0 bit-identity unit test, estimator validation on an exact notch gap, headroom, learnability, PF convergence 32k vs 128k on 600 episodes, comparator strength); gate decision 2026-11-12.

---

## Stage 8.5. THEORETICAL_BOUNDS     [v2]

- **Started:** 2026-10-28T11:15:00Z
- **Finished:** see commit "stage 8.5 v2"
- **Outputs produced:** docs/07b_theoretical_bounds_v2.md; docs/03_supplement_queries.yaml + code/literature/supplement.py + .github/workflows/literature-supplement.yml (targeted OpenAlex lookups for the budgeted-information-gathering references, append-only cite_keys; dispatched)
- **Decision:** PROCEED → stage 9 (v2).
- **Summary:** Cost-aware greedy costs O(N·A·(V+M)) per decision vs O(d² + d·A) for the policy; informal argument that order-dependent travel costs turn the problem into an adaptive orienteering-type problem where ratio-greedy loses its guarantees (references pending verification); exact notch enumeration defined as the G1 estimator reference.

---

## Stage 9. EXPERIMENT_DESIGN  [GATE]     [v2]

- **Started:** 2026-10-28T11:22:00Z
- **Finished:** see commit "stage 9 v2"
- **Inputs used:** docs/07_hypotheses_v2.md, docs/07b_theoretical_bounds_v2.md, docs/07c_amendment_v1_1.md
- **Outputs produced:** docs/08_experiment_plan_v2.yaml
- **Decision:** PROCEED → stage 10 (v2). **GATE auto-approved** (AUTOPILOT §1). Evidence: required keys present; every effective component (non-myopic credit assignment, ball-information objective, no-contact input, amortization) has an ablation; every baseline has a tuning protocol (script check); comparators share the target and the action set; H1 never downscaled; gates G0–G5 block main runs until PF convergence, learnability and comparator strength are shown.
- **Summary:** v2 = travel-cost action model (κ ∈ {0, 6}, G2 also at 2; one escalation to 12) with probe-matched time budgets, ball-information target for every method, 256 shared discrete actions, G* (cost-aware ball greedy) as comparator, sPCE-myopic(rate) as the credit-assignment ablation. Timeline: code by 11-08, gates by 11-12, main runs 11-12 → 11-18, extended abstract by 12-03.

---

## Stage 10. CODE_GENERATION     [v2]   (IN PROGRESS — no Finished timestamp yet)

- **Started:** 2026-10-28T11:20:00Z
- **Done so far:** docs/07c_amendment_v2_0.md; code/touchbed/{travel,ball,policies_v2,evaluate_v2,train_v2}.py; main.py train2 / eval2; stats.tost; tests (23 passing, incl. exact two-hypothesis ball-EIG, categorical-head and masked-softmax gradient checks, budget accounting).
- **Measured:** training ≈ 68 ms/episode (sandbox, L=4095, κ=6, τ=10, 3.3 probes; untrained ball-sPCE 3.98 nats vs cap 8.32); G* ≈ 2.3 s/decision at M=32.
- **Started early (labelled):** gate G4, κ = 0 part (experiments/v2_g4_k0.json; random and G* at τ=4, N_eval 32k vs 128k, 600 pilot episodes per set × method) on GitHub Actions — it exercises only the unchanged evaluation PF. Outputs will land in results/v2/g4/ (logs in results/v1/logs/ — the workflow's log folder name is version-agnostic).
- **Remaining for stage 10 v2:** G0 unit tests (κ=0/τ=3 v1 reproduction, ball-sPCE toy agreement), exact notch reference + G1 look-ahead estimator, rollout planner, τ_κ/n* calibration script (G5), latency-ladder protocol; then stage 11 (TIME_ESTIMATE on runners) and stage 12 gates.
- **Run-2 late additions:** G0 (vi) κ=0/τ=3 reproduction test passes (v2 runner == v1 runner given the same actions and streams); G0 (ii) self-symmetry search fixed (amendment B3): C(S)=0.971 passes, **C(A)=0.802 misses ≤ 0.80 by 0.002** (recorded in docs/07c_amendment_v2_0.md, unresolved); `main.py calib` (G5 τ calibration) + experiments/v2_calib.json launched; early G4 κ=0 result for (A, random, 600 episodes): success 0.312 vs 0.315 (32k vs 128k) but ball information +0.13 nats at 128k → fails the 0.05-nat rule, so the pre-registered fallback check (10 vs 30 MH steps at 32k, experiments/v2_g4_fallback_random.json) was launched; dev sanity run shows the sampled policy improving while argmax validation does not yet (results/v2/dev/README.md).
- **Actions jobs still running at the end of run 2** (their commits land in results/v2/{g4,calib,g4_fallback}/): run 40679933995 (G4 κ=0), run 40680312831 (calibration), and the G4 fallback run. Next run: `python code/analysis_g4.py`, aggregate calibration, then continue stage 10 v2 remaining items.
- **Run-3 additions (2026-10-28 ~14:00–):**
  - **G4 as pre-registered: FAIL** in all 4 κ=0 cells on ball information (128k − 32k, 3 MH: +0.06 to +0.18 nats;
    results/v2/12_g4_analysis.json). **Pre-registered fallback (10 vs 30 MH): FAIL** on success (A +1.1 pp, S +3.7 pp)
    though ΔBI ≤ 0.05 (results/v2/12_g4_fallback_analysis.json). Diagnostic: 32k × 30 MH ≈ 128k × 3 MH on BI → the
    error is MCMC mixing. Amendment **B5** (final rejuvenation of the evaluation PF; R ∈ {10, 30} vs a 32k × 30 MH +
    60 final reference) written before re-checking; experiments/v2_g4_b5.json dispatched (144 jobs → results/v2/g4_b5/).
  - **G5 calibration aggregated** (results/v2/12_calib_analysis.json, code/analysis_calib.py): n*(A) = 3 (G* success
    0.96 on 200 pilot eps), n*(S) = 4 (0.665); τ: A 3.3/3.2/3.3, S 4.8/5.0/5.1 at κ = 2/6/12. G* travels little
    (mean travel time 0.17–1.14). Budget-enforced verification dispatched (experiments/v2_calib_verify.json →
    results/v2/calib_verify/).
  - **G1 instrument built** (amendment B6): exact notch reference code/touchbed/notch.py (exact gap 0.717 at the prior),
    generic look-ahead estimator code/touchbed/lookahead.py, `main.py g1`. Zero-gap bank generation in progress.
  - **C(A) = 0.802** decided: keep A, report as marginal fail (amendment B7).
  - **G5 τ verification: PASS** in all six cells (mean executed probes A 2.85/2.75/2.97 vs n*=3; S 3.89/3.95/4.10 vs
    n*=4). τ frozen: A κ0 3.0, κ6 3.2 (κ12 3.3); S κ0 4.0, κ2 4.8, κ6 5.0 (κ12 5.1).
  - **G1 (a): PASS** — mean estimated relative gap 0.829 over 5 seeds vs exact 0.717 (band [0.573, 0.860]); upward
    bias comes from the MC comparator's noisier first action (V_G* 0.08–0.15 vs exact greedy 0.174). G1 (b) running.
  - **G2** (S, κ ∈ {0, 2, 6}, 100 beliefs each) and **G3 (i)** (4 PPO configs) dispatched; notch-control learner and
    the H1b latency protocol written (dev smoke tests in results/v2/dev/).
  - **Evaluation posterior (B8):** partial B5 results show every SMC kernel moves BI by ≥ 0.08 nats relative to the
    next heavier one. A deterministic adaptive grid posterior (0.25 mm / 0.5° where it matters) is introduced as the
    reference; on S/random ep. 0 it equals the full fine grid (5.905) while PF kernels give 5.27–5.88. Grid-vs-kernel
    comparison on 200 pilot episodes per κ=0 cell dispatched (experiments/v2_grid_ref.json). No main run before G4
    passes under B8.
  - **G1 (b): PASS** (100 zero-gap beliefs: mean 0.0025, UB 0.0037) → **G1 PASS**.
  - **G2:** G(0) = 0.005, G(2) = 0.008, G(6) = 0.017 (95/100 beliefs; LB 0.011, UB 0.024) → magnitude fails, ordering
    holds → the pre-registered escalation κ_hi = 12 is used (κ_hi = 12 replaces 6 in every κ_hi cell and in G3).
    G(12) = 0.015 on 90/100 beliefs (UB 0.022) → heading to **Idea 2 refuted in the tested range (κ ≤ 12)**.
  - **G3 (i):** hp1 selected (final val ball-sPCE 5.592). **G3 (iii) notch: FAIL** (28 % of the exact optimum, all
    seeds greedy-like; remedy 2× E_train unchanged) → per §4 the gate routes to stage 15 at the gate decision.
    G3 (ii) at κ = 12 dispatched (experiments/v2_khi12.json; the κ = 6 pilot seeds are superseded).
  - **G5 (provisional, 3-MH read-outs):** κ = 6: A G* 0.457 vs random 0.037, S 0.417 vs 0.033; flatness S κ6:
    Δsuccess +1.3 pp, ΔBI −0.015 (pass). Re-run at κ = 12 dispatched; A κ = 0 at τ = 3 dispatched.
  - **B8 grid reference:** agrees with the heavy 30 + 60 SMC kernel (ΔBI 0.011–0.019) while 32k × 3 MH under-reads BI by
    0.07–0.21 nats; grid sub 4 vs 8 on G* episodes: mean |ΔBI| 0.007. A printing bug in analysis_g4_b5.py (success column
    showed the identity rate) was found and the B8 rationale corrected.
  - **G2 complete: FAIL after the escalation** — G(0) 0.005, G(2) 0.008, G(6) 0.018, G(12) 0.015 (LB 0.010, UB 0.021;
    absolute gap 0.04 nats on ≈ 2.7 nats). With G1 passed this is **"Idea 2 refuted in the tested range (κ ≤ 12)"**
    (§3 gate table); H2 policies are not trained. 15 beliefs whose budget was exhausted before the drawn step crashed
    the first pass; fixed (recorded as V_LA = V_G* = 0) and re-run.
  - **B8: grid adopted as the evaluation** (no SMC kernel passes in every cell; grid sub 4 vs 8 self-check passes:
    mean |ΔBI| 0.004, no flips). Remaining B5 jobs cancelled.
  - **G5 provisional** (see amendment status note): +10 pp / D ≥ 20 pp hold everywhere; **A0 BI saturation 75 %**
    (rule < 50 %, n* cannot go lower) and **flatness fails at κ_hi = 12** (Δsuccess +7.7 pp, ΔBI +0.19). Grid
    re-evaluation of all G5 pilots and flatness runs dispatched (experiments/v2_grid_g5_{gstar,random}.json).
- **Where to resume (run 4):** stage 12 v2 gates, then the **gate decision → stage 15** (G3 (iii) failed; §4 routes
  there). Before it: (1) `python code/analysis_b8.py` (grid_ref now complete?) and grid-based G5 numbers from
  results/v2/grid_g5, grid_g5_flat (write code/analysis_g5.py); (2) G3 (ii) at κ = 12 (results/v2/g3/pilot_S_k12_*):
  evaluate the 3 seeds + G* on 500 validation episodes (eval2 --split val, then evalgrid) for the "≥ G* − 5 pp" rule
  and (iv) the ball-sPCE vs BI bias; (3) stage 14/15 with fresh subagents on the complete gate record. Expected
  stage-15 question: REFINE toward H1 (amortization) with Idea 2 reported as refuted, handling the flatness failure
  (𝒜 → 64 × 8) and the A0 saturation as pre-registered.
  - **G3 (ii) provisional (S, κ = 12):** the 3 pilot seeds execute ≈ 2.4 probes vs G*'s ≈ 4 (they spend the budget on
    travel); validation success with a 2k-particle read-out 0.15–0.17 vs G* 0.41 on the grid → likely **FAIL**
    (rule: ≥ G* − 5 pp). Training-objective saturation 8.7–9.9 % (< 10 %, pass). Grid read-outs of the policies and the
    pre-registered remedy (E_train 2 × 10⁵, experiments/v2_g3_remedy.json) dispatched. Flatness at κ = 12 on the grid
    (225 eps): Δsuccess +3.1 pp, ΔBI +0.22 → fail confirmed so far.
- **Run 3 ended ~17:55 UTC.** Actions still running: grid_g5 (random part), grid_g5_flat, grid_g3_val (policies),
  G3 remedy training, grid_ref (random part). Resume as described above; add the remedy seeds' validation evaluation
  (eval2 --split val --n-eval 2000, then evalgrid) before the gate decision.

---

## Stage 12. EXPERIMENT_RUN (pre-run gates G0–G5)     [v2]   (run 4 record; stages 10–11 v2 were completed in runs 2–3, see above)

- **Started:** 2026-10-28T11:20:00Z (gates run inside the stage-10 v2 entry above, runs 2–3)
- **Run 4 (2026-10-28 ~19:50 UTC →):** all Actions runs from run 3 had finished (no run in progress).
  - `analysis_b8.py`: grid adopted (no SMC kernel passes every cell) — unchanged conclusion.
  - `analysis_g5.py` on the grid: +10 pp rule passes everywhere; **A0 degenerate** (G* BI saturation 81.5 %) → removed
    from the primary set; **flatness fails at κ = 6 (Δsuccess −2.7 pp) and κ = 12 (ΔBI +0.17)** → 𝒜 → 64 × 8 required.
  - New `code/analysis_g3.py`: **G3 (ii) FAIL** — policy seed-mean success 0.204 vs G* 0.410 on the same 500 validation
    episodes (grid); policies execute ≈ 2.4 probes vs 4.2. Remedy seeds (E_train 2 × 10⁵) read-out dispatched
    (experiments/v2_g3_remedy_val.json, eval2 + grid in one job).
  - Exploratory (labelled, not a gate): policies use only 4 absolute first angles and ignore φ0 → travel 0.54–0.63 rad
    vs G* 0.13; candidate root cause = absolute-action head. Diagnostic runs at κ = 0 / 6 dispatched
    (experiments/v2_diag_k0k6.json → results/v2/diag/).
  - Recorded in docs/07c_amendment_v2_0.md (status note run 4) and plans/stage_12_experiment_run_v2.md.
- **Decision:** G3 failed (iii and ii) → per §4 the gate goes to **stage 15** (via 13 → 14) once the remedy read-out is in.
- **Remedy read-out (run 4):** remedy seeds 0.243 seed-mean vs G* 0.410 → **G3 (ii) FAIL after the one remedy** (results/v2/12_g3_analysis.json).
- **Exploratory diagnostics (results/v2/12_diag_analysis.json, labelled):** the absolute-head policy is also 23.5–25 pp
  below G* at κ = 0 (equal probe counts) and 13.5–19.5 pp at κ = 6 → the shortfall is a learnability problem, not
  travel-specific. A finger-relative dev head (touchbed/relframe.py, exploratory) reaches 0.305 vs G* 0.440 at κ = 12
  (seed 400; 2 more seeds running).
- **Commit:** see git log ("stage 12 v2", "G3 remedy read-out complete").

---

## Stage 13. ITERATIVE_REFINE     [v2]

- **Started / Finished:** 2026-10-28 run 4 (~20:20 UTC)
- **Outputs:** plans/stage_13_iterative_refine_v2.md; tests/test_train_v2.py (0·(−inf) in a test helper fixed at the root).
- **Summary:** numpy2 check clean, 26 → 30 tests pass; no open runtime bug in the Actions logs (all earlier warnings /
  tracebacks traced to fixed code or cancelled inputs). No iterative_improve before stage 15 (would be post-hoc).
- **Decision:** PROCEED → stage 14.

---

## Stage 14. RESULT_ANALYSIS     [v2]

- **Finished:** 2026-10-28 run 4 (~21:30 UTC)
- **Outputs:** results/v2/14_analysis.md (fresh opus analyst, template verbatim; second fresh opus area-chair pass with
  4 in-place [AC-corrected] fixes and a 17-row unsupported-claims table)
- **Summary:** G1 pass; G2 fail after escalation (G(12) = 0.0146, UB 0.0208); G3 fail (S12 0.204 / remedy 0.243 vs
  ≥ 0.360; notch 27.9 % of optimum); G4 fail as pre-registered (grid adopted, B8); G5: G* ≫ random, A0 degenerate,
  flatness fails (→ 64 × 8). Integrity items to fix in v3: B5 note sign (+0.007 vs JSON −0.0066), G4/B8 note figures,
  G5 S0 cell n = 150, notch / hp-selection files have no producing script, G3 (iv) missing.

---

## Stage 15. RESEARCH_DECISION     [v2]

- **Finished:** 2026-10-28 run 4 (~21:45 UTC)
- **Outputs:** results/v2/15_decision.md (fresh opus subagent, template with REFINE augmentation verbatim)
- **Decision:** **PIVOT → 8.**
- **Summary:** Idea 2 refuted by its own pre-registered rule (G1 pass, G2 fail); the pre-registered H1 learner failed
  G3 after its one remedy, and no main run was allowed. v3 direction: (C1) the validated look-ahead headroom over
  cost-aware greedy is small — re-measured once on the 64 × 8 action set; (H1′) a finger-relative policy *distilled from
  G** (DAgger on G*'s score vectors) is non-inferior to G* at ≥ 100× lower per-decision cost; RL on the information
  objective stays as a comparator row. Amendment v3.0 must freeze 64 × 8, the grid evaluator, cells (S0, S12, A12) and
  the distillation recipe before any run. Learnability gate by 11-12 (student ≥ G* − 5 pp and ≥ G* − 0.30 nats at S12,
  one remedy by 11-14); if it fails, the extended abstract becomes the pre-registered fallback (headroom measurement +
  negative learnability results). If the v3 stage-15 decision is not PROCEED, escalate to the owner before a third loop.

---

## LOOP MARKER — PIVOT from stage 15 → stage 8     [version v2 → v3]

- **Reason:** see results/v2/14_analysis.md and results/v2/15_decision.md (G2 refutes Idea 2 in the tested range; G3
  learnability failure of the pre-registered H1 learner after the one remedy).
- **Snapshot taken:** results/v2/ (all v2 artefacts stay there unchanged); no paper files yet. docs/07_hypotheses_v2.md,
  docs/07c_amendment_v2_0.md and docs/08_experiment_plan_v2.yaml remain as the v2 record; v3 writes
  docs/07_hypotheses_v3.md, docs/07c_amendment_v3_0.md, docs/08_experiment_plan_v3.yaml and results/v3/.
- **Next stage:** 8 HYPOTHESIS_GEN
- **Resuming under version:** v3
- **Still valid for v3:** code/touchbed (geometry, likelihood, travel model, G*, grid evaluator, lookahead estimator +
  notch reference, numpy PPO, relframe dev head), literature (docs/03–06 + supplement), G1-validated estimator, G5
  calibration (to be redone on 64 × 8), measured costs.
- **Loop count:** 2 of RESTRICTS loops.max_refine_cycles = 3 used (v1 → v2, v2 → v3).

---

## Stage 8. HYPOTHESIS_GEN (multi-agent debate)     [v3]

- **Started:** 2026-10-28T22:00:00Z (run 4)
- **Finished:** 2026-10-28T23:00:00Z approx. (see commit "stage 8 v3 HYPOTHESIS_GEN")
- **Inputs used:** docs/06_synthesis.md, results/v2/14_analysis.md, results/v2/15_decision.md, docs/07_hypotheses_v2.md,
  results/v2/12_diag_analysis.json (exploratory)
- **Outputs produced:** docs/07a_proposer_v3.md, docs/07b_skeptic_v3.md, docs/07_hypotheses_v3.md (canonical; three
  fresh opus subagents, template prompts verbatim); plans/stage_08_hypothesis_gen_v3.md
- **Decision:** PROCEED → stage 8.5 (v3).
- **Summary:** Two core ideas. **Idea A / H1:** a belief-free, finger-relative student distilled from G* by DAgger on
  G*'s score vectors (512-action 64 × 8 set) is non-inferior to G* in every informative cell of {S0, S12, A12}
  (success LB > −δ_c ≤ 4 pp, BI LB > −ε_c, ≥ 4/5 seeds) — H1a; at ≥ 100× lower per-decision cost against the best of a
  27-point greedy grid (particles × candidates × outcome samples; belief update vs scoring time measured) — H1b; and the
  best of three non-random heuristics must fall outside the margin (else "flat task", learning claim dropped) — H1c.
  H1-fb (top-16 proposal + G* re-scoring, ≥ 10× measured latency ratio, random-16 control). **H2** (mechanism): student
  vs retrained RL on RL's own ball-sPCE objective (LB > +0.10 nats), with label-fit and belief-input controls before any
  "encoder is the limit" sentence. **Idea B / H3:** validated one-step look-ahead headroom over G* on 64 × 8 has UB < 0.03
  (kill if LB > 0.05). Gates G0′ (11-05) … D3 learnability (11-12, one remedy by 11-14) with D3 tied to the test's own
  margin; pre-written outcome table incl. a characterisation-paper fallback. Compute ≈ 260–300 CPU-h (public repo →
  standard GitHub-hosted runners are free; concurrency ~20 jobs). Skeptic novelty threats to verify: Choudhury et al.
  RSS 2017 (arXiv:1705.07834), Nguyen et al. arXiv:2405.15031; no prior greedy-EIG distillation for tactile
  localisation found in a limited search. Exploratory finger-relative RL seeds (0.305/0.365/0.290 vs G* 0.440 at S12)
  are context only.
- **Where to resume (run 5):** stage 8.5 v3 (cost model of student vs greedy grid; verify the novelty references),
  then write docs/07c_amendment_v3_0.md freezing everything listed in 07_hypotheses_v3 §6.1 *before* any v3 run, then
  stage 9 v3 (docs/08_experiment_plan_v3.yaml, gate auto-approval with evidence), then stage 10 v3 code (64 × 8 action
  set, DAgger trainer, heuristics, greedy grid, latency split).

---

## Stage 8.5. THEORETICAL_BOUNDS     [v3]

- **Started / Finished:** 2026-10-29 run 5
- **Inputs used:** docs/07_hypotheses_v3.md, code/touchbed/*, docs/07b_theoretical_bounds_v2.md
- **Outputs produced:** docs/07b_theoretical_bounds_v3.md (fresh opus subagent, template verbatim);
  docs/07d_reference_check_v3.md (fresh subagent, WebSearch/WebFetch; 12 references + novelty search);
  plans/stage_08_5_theoretical_bounds_v3.md
- **Decision:** PROCEED → amendment v3.0, then stage 9 (v3).
- **Summary:** Per-decision cost of greedy (N, C, M) = O(N·C·(V+M) + N² + PF assimilation); student O(T·H² + H·A)
  (as implemented O(T²·H² + T·H·A), ≈ 5.5× more at T = 4). The ≥ 100× ratio is a constants statement at these sizes, not
  an asymptotic separation (op counts: full G* ≈ 510× minimal student, 92× as implemented). Small grid configurations
  are within 1–10× of the student on op counts, so Q (§1.8) is likely non-empty and H1b rests on their accuracy;
  pruned-16 ≈ 11× on op counts (N² neighbour lists dominate) — close to the 10× H1-fb threshold, decided by Lat′.
  DAgger's guarantee does not apply as stated (soft-CE surrogate, noisy approximate teacher, non-convex learner,
  3 rounds); greedy guarantees do not transfer under travel costs (informal; Singh et al. JAIR 2009 verified for the
  "greedy can be arbitrarily bad with path costs" sentence). Early ball-EIG has an action-dependent self-inclusion bias
  that grows as N shrinks (relevant to the small-N grid configurations).
- **References:** 1, 3–11, 12a VERIFIED; #2 author list corrected (no Scherer); javdani2012efficient → arXiv:1208.6067
  (figshare DOI unconfirmed); 12b partial. Novelty search (3 queries): no prior distillation of a greedy-EIG planner into
  a tactile localisation policy found; closest APPLE (arXiv:2505.06182, RL) and Gordon et al. (online greedy EIG).
- **Discrepancies found (to be resolved in amendment v3.0, not silently):** (1) H3 text says the look-ahead rollouts
  complete with G* at M = 64, but the B6/G1/G2 code path (`g2.py` → `lookahead_gap(..., greedy_M=0)` →
  `TouchbedProblem` defaults) completes with N_LA = 500 particles, rung (16, 8), M = 16 — as the `lookahead_tb.py`
  docstring states; (2) two informal G* latency figures disagree (0.840 s per decision on 256 in 15_decision §3.4 vs
  "≈ 2.3 s at M = 32" in the stage 10 v2 entry); neither was taken under the latency protocol — Lat′ supersedes both.

---

## Amendment v3.0 (pre-registration freeze)     [v3]

- **Committed:** 2026-10-29 run 5, **pre-registration commit a1de0fc** (docs/07c_amendment_v3_0.md). No v3 run or v3 code
  change exists before this commit.
- **Content:** C1–C15 = 07_hypotheses_v3 §6.1 items 1–15: 64 × 8 via `TOUCHBED_NPHI` flag (default 32 bit-reproducible),
  nested subsets; grid evaluator sub 4 with tie band pre-registered; cells/I-rules; calibration; split salts cal3 61,
  pilot3 67, val3 71, test3 79, label3 83, dagger3 89, g2v3 97, bank3 101; margins; distillation recipe incl. label
  format and HP grid (4 configs, seed 501); seeds 501–505 (student), 511–513 (RL), 521–523 (belief-input), 531–533
  (abs-frame), BC = round-0 checkpoints; heuristics; greedy grid/latency/R_b/H1-fb; H3; tests and labels; integrity
  corrections 1–9; deviations.
- **Correction recorded (C12):** H3 rollouts are completed by the reduced greedy actually used in v2 G1/G2 (N_LA 500,
  128 candidates, M = 16), not "G*, M = 64"; documentation fix, no code change.

---

## Stage 9. EXPERIMENT_DESIGN  [GATE]     [v3]

- **Started / Finished:** 2026-10-29 run 5 (commit 725880c)
- **Inputs used:** docs/07_hypotheses_v3.md, docs/07c_amendment_v3_0.md (a1de0fc), docs/07b_theoretical_bounds_v3.md
- **Outputs produced:** docs/08_experiment_plan_v3.yaml (fresh opus subagent, template verbatim with the PIVOT preamble);
  docs/07c_amendment_v3_1.md (main session; closes the plan's 11 listed inconsistencies before any v3 run);
  plans/stage_09_experiment_design_v3.md
- **Decision:** PROCEED → stage 10 (v3). **GATE auto-approved** (AUTOPILOT §1). Evidence (script check): all 8 required
  keys; 10 effective components C1–C10 each with a matching ablation whose `removes` names it (distillation vs RL,
  DAgger vs BC-only, relative vs absolute frame, belief-free vs belief-input, soft labels → HP-grid regret only, amortization
  vs 27-config grid/R_b, learned selection vs H★, learned pruning vs random-16, greedy teacher vs H3 look-ahead, per-cell
  training vs Gen-κ); all 6 baselines have a tuning protocol (RL now gets an equal 4-config sweep, v3.1 D9); all 22
  metrics have a formula + code pointer; compute = gates 96 (+13 remedy) + main 149 (126.6 after downscale; core ≈ 117)
  + reserve ≤ 42 CPU-h, every sweep preceded by a ≤ 5-min TIME_ESTIMATE.
- **Amendment v3.1 (D1–D10):** disjoint DAgger/label indices with κ in the key; H1c power rule funded first from the
  reserve; A0 enters only if the reserve covers it; power rule for S0/A12 via scaled S12 SD; E′-failure costing;
  no soft-label efficacy claim; D3-fail-branch students defined; RL 4-config sweep (seed 519, own objective);
  RESTRICTS compute fields read as in v1 (12 h = saturated-runner wall-clock ≈ 6.2–7.5 h; sweeps sharded ≤ 30 min;
  declared exception for RL/DAgger training processes, time_guard + checkpoint) — owner informed in OWNER_TODO.md.
- **Where to resume:** stage 10 v3 code, in this order: (1) `TOUCHBED_NPHI` flag + relative `rung_subset` + 32 × 8
  bit-reproduction test; (2) split salts / κ-keyed label streams; (3) `GStar.score_vector()` + test; (4) heuristics
  B-spread/B-fan/B-cov with reservation rule; (5) `distill.py` (loss, regret, DAgger driver) + soft-label CE gradient
  check; (6) greedy grid + component timers; (7) belief-summary features; (8) travel-notch; (9) provenance scripts
  analysis_g3_notch.py / analysis_g3_hp.py; (10) main.py subcommands + manifests; G0′ green by 11-05.

---

## Stage 10. CODE_GENERATION     [v3]   (IN PROGRESS — no Finished timestamp yet)

- **Started:** 2026-10-29 run 5
- **Done so far (each with tests; full suite was 29/29 green before v3 changes):** (1) `TOUCHBED_NPHI` flag, 64 × 8 =
  512, `rung_subset` relative, 32 × 8 bit-identity test; (2) v3 split salts + κ-keyed label/DAgger streams
  (`touchbed/v3.py`), disjointness tests; (3) `GStar.score_vector()` (argmax = act test); (4) heuristics
  B-spread/B-fan/B-cov with reservation rule (`touchbed/heuristics.py`); (5) `run_episode_v3` (teacher labelling,
  DAgger β-mixing, grid read-out) and `touchbed/distill.py` (soft-label CE with finite-difference gradient check,
  floored regret, Student, training round with the R̄ stop rule).
- **Remaining:** (6) 27-config greedy grid + component timers; (7) belief-summary features; (8) travel-notch;
  (9) provenance scripts; (10) main.py subcommands + manifests + TIME_ESTIMATE pilots; numpy2 / forbidden-pattern checks.
- **Finished (run 5):** all 10 items. (6) `latency3.py` (27 configs, component timers, pruned-16/random-16, L_final);
  (7) belief-input student (48 features); (8) `travel_notch.py` (exact gap 0.717 — equals the κ = 0 notch gap; the control
  checks the estimator's travel/feasibility handling, it does not show travel-created headroom); (9) provenance scripts
  reproduce `12_g3_notch_analysis.json` and `12_g3_hp_selection.txt` exactly (15_decision §3.5 item 4 closed); (10)
  `touchbed/cli3.py` + main.py: eval3, calib3, label3, dagger3, distill3, latency3, g1c, g2v3, pilot3, train3rl (v3
  commands imply TOUCHBED_NPHI=64). Pre-run implementation change: `ball_eig` uses a plain-numpy log-sum-exp (≈ 20 %
  faster G*; equivalence test to 1e-10 with identical argmax). numpy2 check: 0 errors; no subprocess/eval/exec in
  v3 code; 55 tests pass (+ g2v3/rl additions, 28 targeted tests pass).
- **Decision:** PROCEED → stage 11.

---

## Stage 11. RESOURCE_PLANNING     [v3]

- **Finished:** 2026-10-29 run 5
- **Outputs:** docs/11_schedule_v3.json; results/v3/pilot/time_estimate_{S_k12,S_k0,A_k12}.json (Actions run
  40807921186; TIME_ESTIMATE lines in results/v1/logs/v3_pilot_*.log)
- **Summary:** measured on runners: G*-labelled episode 7.5 s (S12, 5 decisions, τ 6 uncalibrated), 22.2 s (S0,
  ≈ 5.5 s per decision with all 512 actions feasible), 2.0 s (A12); grid read-out 3.6–5.4 s. Total ≈ 273 CPU-h (gates
  ≈ 113, main ≈ 160 > 150 → frozen downscale order at the freeze commit if confirmed after calibration). κ = 0 G* is
  ≈ 3× the planning value.
- **Decision:** PROCEED → stage 12 gates.

---

## Stage 12. EXPERIMENT_RUN (pre-run gates)     [v3]   (IN PROGRESS)

- **Started:** 2026-10-29 run 5
- **G0′:** unit tests green; TIME_ESTIMATE pilots done (above).
- **Dispatched:** experiments/v3_cal.json (Cal′: n* at κ = 0/τ = 4 on 200 cal3 episodes per set with grid read-out;
  τ_12 with n* = 4 — speculative, re-run if the n* rule changes n*); experiments/v3_g1.json (G1′ a/b/c).
- **Run 6 (2026-10-29):** Cal′: S n* = 4, A n* = 3; τ: S0 4, S12 4.9, A12 3.3 (A12 re-calibrated with n* = 3);
  S12 verification 3.96 probes (pass); A12 verification dispatched. G1′ (a)(b)(c) all pass (status note in amendment
  v3.0). Fixed `analysis_cal_v3.py` (n* = 3 shards were not globbed) and output-dir creation in `save_shard` /
  `save_student` (label3 crashed on a fresh directory; I/O only, 56 tests pass). Dispatched: A12 verification,
  S12 round-0 labels (label3 0–1,499), G5′ S12 and S0 (G* 500, random 200, 3 heuristics × 200, pilot3, grid sub 4).
- **Run 6, later:** A12 verification 2.98 probes (pass) → **Cal′ complete**. τ_2 = 4.7 (descriptive H3 level).
  S12 round-0 labels: 1,500 episodes complete (shard 09 re-run in the sandbox after its Actions push failed; .gitignore
  now keeps results/v3/**/*.npz — the first label run lost its .npz files and was cancelled/re-run). HP grid dispatched.
  **E′ FAILED** (1 counted success flip in 16; mean |ΔBI| 0.0126) → sub = 8 for every v3 number (C2); sub-8 re-read of
  Cal′ n* and G5′ pilot episodes dispatched (`regrid3`, time guard added; `code/tools_regrid_manifest.py`). Compute
  re-estimate ≈ 526 CPU-h (gates ≈ 190, main after full downscale ≈ 336) → owner informed (OWNER_TODO) with a default.
  G2′ (S0, S12, κ = 2) + bias check dispatched; bias check implemented (`touchbed/bias3.py`, 256 full-G* rollouts per
  belief — sample count chosen before any G2′ number, since the pre-registered text gives none).
- **Run 6, D3 path:** HP config 0 selected (held-out R̄ 0.3827; cfg 2/3 within 0.01). Round-0 students 502/503 and
  every distill3 step run in the sandbox (seconds each; data from runners). DAgger r1 done (3 × 400, β 0.5) → round-1
  R̄ 0.234 / 0.229 / 0.227; DAgger r2 (β 0) dispatched. D3-B round 0 (seeds 521–523) + DAgger r1 dispatched. RL sweep
  (v3.1 D9) dispatched; deviation noted (trainer's own validation stream, not val3). Lat′ dispatched (one job).
  G* on val3 0–499 at sub 8 dispatched. Sub-8 re-reads: Cal′ n*, A12, S12 dispatched; S0 after its sub-4 pilot ends.
  Queue juggling: several runs were cancelled and re-dispatched for D3 priority; follow-up manifests (`*_r1`, `*_r2`)
  resume from the recorded episode — every partial output is labelled by its file name and nothing is double counted
  (analyses key on episode index).
- **Run 6, later:** round-2 students R̄ 0.210 / 0.225 / 0.207; val3 evaluation at sub 8 running (students are slow at
  sub 8: 20-episode jobs hit the 80 % budget → follow-ups needed). Partial read (seed 501, 363 episodes): student 0.394
  vs G* 0.438 — points to a D3 fail; the remedy (round 0 doubled with label3 1,500–2,999; DAgger rounds of 800 from
  fresh remedy students; held-out set unchanged) was started speculatively: labels done, remedy round-0 students
  (R̄ 0.231 / 0.209 / 0.226), remedy DAgger r1 dispatched. Used only if D3 fails. Cal′ n* at sub 8 unchanged.
  Lat′ first pass: G* full 709 ms vs student 0.38 ms (1,850×); pruned-16 ratio 3.65 → H1-fb inactive unless the
  pooled 1,000 decisions change it; 500 more decisions running. D3-B DAgger crashed (belief student got no PF) →
  fixed in `_label_loop`, re-dispatched. G2′ partial: G(0) 0.008 (68 beliefs), G(2) 0.017 (29).
- **Run 6, end state (≈ 12:30 UTC):**
  - **D3 first attempt FAILS** (468/500 paired val3 episodes, sub 8): Δsucc −6.8 pp, ΔBI −0.19 nats, all 3 seeds
    ≤ −δ → the one remedy runs (status note in amendment v3.0). Remedy: labels 1,500–2,999 done; remedy r0 students
    (R̄ 0.231/0.209/0.226), DAgger r1 800/seed done → r1 students (R̄ 0.203/0.197/0.191); DAgger r2: 20/24 shards from
    runners, s503 shards 400–700 re-run in the sandbox (the runner jobs sat queued; that run was cancelled).
  - **Lat′ frozen** (pooled 1,000 decisions): G* full / student 2,238×; G* full / pruned-16 3.2 → **H1-fb withdrawn**;
    Q = 14 configs; 5 R_b candidates → R_b selection runs dispatched (`v3_rb.json`, sub 8).
  - **E′ FAIL** → sub 8 everywhere; Cal′ n* unchanged at sub 8.
  - G5′ sub-8 re-reads in progress (S12 `v3_sub8_S12_r2`, A12 `v3_sub8_A12_r3`, S0 `v3_sub8_S0`); G2′ in progress
    (`v3_g2_r4`, `v3_g2_k2_r4`; bias check inside `v3_g2*`); D3-B r2 dispatched; RL sweep dispatched (cfg2 done).
- **Where to resume (run 7):**
  1. Done in run 6: remedy DAgger r2 complete (s503 400–700 in the sandbox), remedy round-2 students trained
     (R̄ 0.187 / 0.184 / 0.201), remedy validation dispatched (`experiments/v3_d3rem_val.json`, 126 jobs, sub 8).
     Check it with the resume tool and complete early-stopped shards.
  2. When the remedy validation is complete: `python code/analysis_d3_v3.py --tag rem` → pass → H1 alive (freeze
     commit after G5′ sub-8 + R_b); fail → **H1 dead; H1-fb already withdrawn → outcome row 4** (characterisation
     paper) → tell the owner (OWNER_TODO) and proceed to stage 13/14 with the fallback plan, not a fourth design.
  3. Re-run the follow-up tool on every manifest still incomplete (`code/tools_resume_manifest.py`,
     `code/tools_regrid_manifest.py`); complete the first D3 read (`analysis_d3_v3.py`) for the record.
  4. D3-B: after r2, train round 2 (`--kind belief`), evaluate 300 val3 episodes (sub 8), `analysis_d3_v3.py --kind
     belief_student` (report-only). RL sweep: select per v3.1 D9 when the 4 configs are in.
  5. G5′ decision on sub-8 values (`analysis_g5_v3.py`), G2′/H3 (`analysis_g2_v3.py`), then the gate decision and
     the freeze commit (status notes with commit hashes). The 64 × 16 S12 report
  (report-only) needs a ψ-count flag that does not exist yet — deferred.
- **Run 7 (2026-10-29, from 14:01 UTC):**
  - No open issues; no new owner directives.
  - Queue priority for the D3 remedy: runs 73/80/81 (G5′ sub-8 re-reads, 129 jobs queued ahead of the remedy
    validation) cancelled at ≈ 14:05; their follow-up `experiments/v3_sub8_g5_r4.json` (214 jobs, already re-read
    episodes skipped) dispatched behind the remedy. The remedy validation then ran 20 jobs in parallel.
  - D3-B: round-2 belief-input students trained in the sandbox (held-out R̄ 0.402 / 0.394 / 0.384 vs 0.21 for the
    history students); val3 0–299 sub-8 evaluation dispatched (`v3_d3b_val.json`, report-only).
  - RL sweep (v3.1 D9) selected: **config 2 (lr × 3)**, final validation ball-sPCE 5.67 vs 4.75 / 4.68 / 4.63
    (`code/analysis_rl_sweep_v3.py` → `results/v3/12_rl_sweep_selection.json`; deviation kept: trainer's own
    validation stream, not val3). The trainer stopped at plateaus by default, but the 08 plan says the plateau rule is
    "recorded but not used to stop early" for the H2 runs → added `--no-plateau-stop` (default behaviour unchanged;
    new test). H2 RL runs dispatched: seeds 511–513, 2 × 10⁵ episodes (`v3_rl_main.json`).
  - Follow-ups dispatched: R_b selection (`v3_rb_r1.json`, 31 early-stopped shards), G2′ (`v3_g2_r5.json`, 5).
  - Sandbox: remedy val shards s503 480–499 run locally (one process at a time: sub-8 read-out peaks ≈ 3.7 GB).
  - **D3 remedy FAILS → H1 dead (H1-fb already withdrawn) → outcome row 4** (status note in amendment v3.0): seed 501's
    remedied student complete on 500 paired val3 episodes, Δ̂_succ −4.6 pp ≤ −δ_S12 (4 pp cap) → rule (iii) fails
    regardless of seeds 502/503 (their validation continues for the record). First-attempt read kept in
    `12_d3_analysis.json`; remedy read will be `12_d3_analysis_rem.json`.
  - **FREEZE commit 671c14e** (row-4 main-run set, `plans/stage_12_experiment_run_v3_main_row4.md`, before any test3
    episode): M1 RL training (running); M2 no-grid test3 0–499 actions for G*, random, remedied students, RL; M3 g_T →
    H2 (`gt3`, `analysis_h2_v3.py`); M4 sub-8 success/BI re-read on test3 0–299. Dropped: everything that served only
    H1/H1-fb (S0/A12 students, student test grid, H★, R_b, BC/abs-frame/Gen-κ/curve rows, final latency). Main ≈ 21 CPU-h.
  - New code: `touchbed/gt3.py` + `gt3` command (H2 g_T on fixed per-episode contrastive draws; equals the trainer reward
    in a test); `analysis_h2_v3.py`; `regrid3` accepts no-grid eval3 outputs (no-grid G* actions + regrid sub 8 reproduce
    the val3 grid eval bit-for-bit, checked on one episode). 60 tests pass.
  - Interim H3: κ = 12 complete (100 beliefs): G = 0.016, UB95 0.022 < 0.03 → region **Hold**; κ = 0 follow-ups running.
  - Dispatched M2 (`v3_t3_m2.json`); re-dispatched D3-B validation (`v3_d3b_val_r1.json`) and G5′ re-reads
    (`v3_sub8_g5_r5.json`) after cancelling them for queue priority; R_b follow-up cancelled (H1-only).
  - Owner told (OWNER_TODO + push): row 4, venue decision (default: RSS Stage 1 extended abstract written honestly as a
    measurement / diagnosis paper).
  - **Results so far (run 7):**
    - D3 remedy complete (500 paired val3, sub 8; `12_d3_analysis_rem.json`): Δ̂_succ −4.4 pp (threshold −1.7),
      Δ̂_BI −0.096 nats (passes −0.15), per seed −4.6 / −4.6 / −4.0 pp → FAIL confirmed. First attempt complete:
      −5.9 pp / −0.20 nats (`12_d3_analysis.json`).
    - M1: RL 511–513 trained to 2 × 10⁵ (plateau rule met at 1.02–1.13 × 10⁵, recorded only).
    - M2/M3 → **H2 FAILS** (`14_h2_analysis.json`): g_T student 5.368 vs RL 5.368 nats, diff +0.0002, 90 % CI
      [−0.31, +0.30] (rule: LB > +0.10). G\* 5.30, random 2.62. RL seeds vary (5.65 / 5.27 / 5.18).
    - Label fit (`14_labelfit.json`): history students not under-fit (train R̄ 0.17–0.21, top-1 0.51–0.53);
      belief-input students under-fit (train R̄ 0.34–0.38, top-1 0.33–0.36).
    - M4 partial (151 of 300 episodes): student ≈ G\* in success on test3 (−0.2 pp, 90 % CI ±5.5 pp); RL success
      similar with 3 probes but BI 0.25 nats lower. Follow-up `v3_t3_m4_r1.json` running.
    - D3-B partial (147 of 300): belief students −17 pp success vs G\*; follow-up `v3_d3b_val_r2.json`.
  - Stage 13 (v3) recorded in `plans/stage_13_iterative_refine_v3.md`: no open runtime bug (1,398 logs scanned).
- **Finished (run 7, ≈ 17:50 UTC):** row-4 main runs M1–M4 complete. M4 (`14_m4_analysis.json`, test3 0–299,
  sub 8): G\* 42.7 %, remedied student 38.2 % (−4.4 pp, ci95 [−9.3, +0.6]), RL 35.7 % with 3.0 probes (G\* − RL
  ci95 [+0.2, +13.7] pp); student − RL success +2.6 pp (ci95 [−3.7, +8.8]) → pre-written H2 fail reading "dense
  supervision does not improve on RL with this head"; student − RL BI +0.29 nats (ci95 [+0.12, +0.47]); gap closure not
  reported (LB(G\* − RL) < δ). Still running (report-only): G5′ sub-8 re-reads, D3-B to 300/300.
- **Decision:** PROCEED → stage 13 (v3).

---

## Stage 13. ITERATIVE_REFINE     [v3]

- **Finished:** 2026-10-29 run 7. Record: `plans/stage_13_iterative_refine_v3.md` (numpy2 0 errors; 60 tests; 1,398
  v3 logs scanned, no NaN/Inf/traceback; 5 root-caused fixes during v3; iterative_improve not applied — D3/H2 are
  pre-registered decisions).
- **Decision:** PROCEED → stage 14.

---

## Stage 14. RESULT_ANALYSIS     [v3]

- **Finished:** 2026-10-29 run 7. Outputs: `results/v3/14_analysis.md` (merged), `14_analysis_pass1.md` (fresh opus
  analyst, template verbatim, data context `results/v3/results_v3.json` from `code/tools_results_v3.py`),
  `14_analysis_pass2.md` (fresh opus adversarial area chair: 22 unsupported sentences, all rewrites binding; no verdict
  changes). Key: row 4; H2 rejected as a non-detection (≈ 80 % power only for Δ ≈ 0.57 nats); H3 Hold (with the
  bias-direction caveat); encoder sentence "generalisation / covariate shift, not capacity" weakly supported; no paired
  heuristic row; latency 2,238× is per decision only.

---

## Stage 15. RESEARCH_DECISION     [v3]

- **Finished:** 2026-10-29 run 7. Output: `results/v3/15_decision.md` (fresh opus subagent, template with the REFINE
  option verbatim).
- **Decision: PROCEED → stage 16 (conditional; row-4 characterisation paper, no method claim).** The PROCEED rule is
  applied in its characterisation sense (every claim is a pre-registered rule's outcome decided by a margin incomplete
  data cannot flip); no stage-8/13 loop (v3 is the last design; v1→v2 and v2→v3 were the two full loops).
- **Conditions before stage 17 claims:** (1) exploratory paired B-fan row on test3 0–299 (readings written first in the
  amendment status note; `experiments/v3_t3_bfan.json` dispatched; compute ≤ 7 CPU-h on free runners, recorded as
  over the 12-h reading per the owner's default); (2) companion rows in the JSON (done: g_T G\* 5.299, random 2.618; RL
  plateau status); (3) G5′ sub-8 and D3-B completion; optional ≤ 2 CPU-h checks (H3 V_LA bias direction, H2 variance
  decomposition, paired first-attempt-vs-remedy bootstrap).
- **Where to resume (run 8):** check `v3_t3_bfan`, `v3_d3b_val_r2`, `v3_sub8_g5_r7` with the follow-up tools
  (`tools_regrid_followup.py` for regrid3, `tools_resume_manifest.py` for eval3, `tools_regrid_manifest.py` for G5′);
  re-run `analysis_m4_v3.py`, `analysis_d3_v3.py --kind belief_student`, `analysis_g5_v3.py`, `tools_results_v3.py`;
  then stage 16 PAPER_OUTLINE for the row-4 paper (RSS Stage 1 extended-abstract format by default; owner decides).

---

## Stage 16. PAPER_OUTLINE     [v3]

- **Finished:** 2026-10-29 run 7. Output: `paper/mypaper/sections/00_outline.md` (fresh opus subagent, template
  verbatim with the topic-constraint block; plan `plans/stage_16_paper_outline_v3.md`). RSS Stage 1 extended-abstract
  format by default (≈ 3,450 body words; Abstract 180, Intro 550, Related 300, Problem & methods 850, Protocol 300,
  Results 950, Discussion & limitations 400, Conclusion 100); Figure 1 plan; row map R1–R17 → results_v3.json keys;
  pass-2 binding sentences and a never-write list. Title candidates: "Can Cost-Aware Information-Gain Touch Selection
  Be Amortized? Look-Ahead Headroom and Learnability under Travel Cost" or the shortening-only fallback
  "Cost-Aware Information-Gain Touch Selection: Look-Ahead Headroom and the Learnability of Amortized Policies"
  (07_hyp_v3 §4 says outcomes can only shorten the working title → the fallback is the rule-compliant default).
- **Gaps:** no knowledge cards for DAgger, PPO and two related works → `[CITE-MISSING]` markers; they must be collected
  and verified (stage 4/23 procedure) before stage 17 cites them. B-fan row (R9) pending.
- **Decision:** PROCEED → stage 17 after the B-fan row and the missing citations (run 8).

---

## Stage 17. PAPER_DRAFT     [v3]

- **Run 8 (2026-10-29, from 19:50 UTC).** No open issues; no new owner directives.
- **Stage-15 conditions:** (1) B-fan test3 row complete (300/300, Actions run 40927313419): B-fan success 36.0 %;
  student − B-fan +2.2 pp, ci95 [−2.8, +7.3] → pre-written **reading (b)**; its "task may be flat" clause is **not
  supported** (B-fan − G\* −6.7 pp, ci95 [−12.0, −1.0]) and is dropped (status note in amendment v3.0, c004577).
  (3) still running, report-only: G5′ sub-8 re-reads (463 episodes left in run 40916248950), D3-B (2 episodes) →
  `[PENDING:…]` markers in the draft.
- **Citations:** cards C57–C60 added (`ross2011reduction`, `schulman2017proximal`, `choudhury2017adaptive`,
  `nguyen2024amortized` arXiv-only/title-level); PPO verified on arXiv abs this run, the others in 07d (run 5).
- **Length decision:** master draft meets `RESTRICTS.yaml` floors (Stage 2 full paper); the 5-page RSS Stage 1 extended
  abstract will be a separate condensed export in stage 22 (`plans/stage_17_paper_draft_v3.md`).
- **Output:** `paper/mypaper/sections/draft_v3.md` (fresh opus subagent, template verbatim; prompt files kept in
  `paper/mypaper/prompts/stage17_*.txt`), `paper/mypaper/figures/figure1_prompt.txt`. Body 6,549 words (+ abstract 268,
  over the 250 ceiling → stage 19). All floors met.
- **Checks:** `code/tools_number_audit.py` → 0 unmatched decimal numbers (derived spreads moved into code:
  `code/analysis_derived_v3.py` → `results/v3/14_derived.json`); 31 cite keys, all in the cards; never-write list
  clean. Open markers: 4 `[CONST?:…]` (runner CPU model, numpy versions, PPO clip/epochs — the code has clip 0.2 and
  4 epochs; to be filled from code in stage 19), `[PENDING:…]` for G5′ and D3-B.
- **Decision:** PROCEED → stage 18.

---

## Stage 18. PEER_REVIEW     [v3]

- **Finished:** 2026-10-29 run 8. Record `plans/stage_18_peer_review_v3.md`, merged `paper/mypaper/18_peer_review.md`
  (runs `18_review_run1.md`, `18_review_run2.md`; template verbatim, two fresh opus reviewer pairs with repo access).
- Scores 4 / 3 and 3 / 4 (reject / borderline). **CRITICAL_FABRICATION: no** (43 spot-checks). Factual text mismatches
  (stale random-row counts, "pinned core", E′ scope, latency checkpoint, CONSTs) fixed in stage 19 (option b, incidental).
- Main substantive point: **in the tested cell (S, κ = 12, τ = 4.9) the planner barely travels** — G\* moves the finger
  between probes in 21 % of decisions (> 1 grid step 6 %), mean logged travel 6.1° per episode; students 1.5–2.0°,
  B-fan 1.5°, RL 23–26° with always 3 probes (`code/analysis_behaviour_v3.py` → `results/v3/14_behaviour.json`).
  Other asks: under-trained students (4–16 epochs), H3 screens 32 of ≤ 512 first actions, thin RL sweep, H2 power,
  reduced-G\* accuracy, disclose v2 G(12) = 0.0146.
- New exploratory row (readings written first, amendment v3.0): long-training students, 200 fixed epochs, same data
  (`distill3 --fixed-epochs`, new flag, default unchanged): held-out R̄ 0.181 / 0.164 / 0.173 (remedied 0.187 / 0.184 /
  0.201); test3 0–299 sub-8 re-read dispatched (`experiments/v3_t3_long.json`, 114 jobs); block
  `exploratory_long_student` in `analysis_m4_v3.py`.
- **Decision:** PROCEED → stage 19 (no fabrication). Items needing new design → OWNER_TODO.

---

## Stage 19. PAPER_REVISION     [v3]

- **Finished:** 2026-10-29 run 8. Pre-revision snapshot `paper/mypaper/v3/draft_v3_stage17.md`. Template verbatim
  (fresh opus subagent, prompt files `paper/mypaper/prompts/stage19_*.txt`); a data block with the new JSON keys
  (14_behaviour, 14_derived, provisional G5′/D3-B, v2 G values, run-config facts) was appended to {reviews} because the
  reviews ask for diagnostics computed after the draft.
- Output `paper/mypaper/sections/draft_v3.md`: Abstract 249, Intro 964, Related 587, Method 1,880, Protocol 1,064,
  Results 2,914, Discussion 756, Limitations 552, Conclusion 290, Appendix A (gate record) 500; body 9,007 words
  (> 8 pages: the Stage 1 extended abstract and the Stage 2 paper will be condensed exports in stage 22).
- Checks: number audit 0 unmatched (audit now also accepts results/v2/12_g2_analysis.json and rad→deg); never-write list
  clean; one placeholder `[PENDING:long_student]`.
- Revision added > 30 % words → per template, **second stage-18 pass** after the long-student row is filled.
- **Where to resume (run 9):** (1) check `v3_t3_long` (follow-ups with `code/tools_regrid_followup.py
  experiments/v3_t3_long.json …`), then `python code/analysis_m4_v3.py && python code/tools_results_v3.py`, read the
  pre-written reading, fill `[PENDING:long_student]` in draft_v3.md (and the labelfit numbers if added); (2) G5′ sub-8
  (`v3_sub8_g5_r7` follow-ups) and D3-B (1 job) completion → replace provisional values; (3) stage 18 pass 2 → 19 → 20.
