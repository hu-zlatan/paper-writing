# Project Progress Log

> **This file is the single source of truth for what stage you are at, what version you are on, and what was decided when.**
> Append-only. Every stage writes one entry. Every loop (REFINE / PIVOT) writes a `LOOP MARKER` entry.
> See `pipeline/references/progress_tracking.md` for full conventions, and `AUTOPILOT.md` for how the scheduled runs operate.

**Project:** paper-writing
**Target venue:** RSS 2027 — Stage 1 extended abstract 2026-12-04 23:59 AoE; Stage 2 full paper (invited) 2027-04-16 23:59 AoE (verified 2026-10-28 at https://roboticsconference.org/information/cfp/)
**Topic:** Amortized, non-myopic active tactile localization (TouchBED)
**Initialised:** 2026-10-28T07:56:44Z
**Current version:** v2
**Latest stage:** Stage 10 CODE_GENERATION [v2] (in progress) — resume from plans/stage_10_code_generation_v2.md

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
