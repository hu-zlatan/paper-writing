# Project Progress Log

> **This file is the single source of truth for what stage you are at, what version you are on, and what was decided when.**
> Append-only. Every stage writes one entry. Every loop (REFINE / PIVOT) writes a `LOOP MARKER` entry.
> See `pipeline/references/progress_tracking.md` for full conventions, and `AUTOPILOT.md` for how the scheduled runs operate.

**Project:** paper-writing
**Target venue:** RSS 2027 — Stage 1 extended abstract 2026-12-04 23:59 AoE; Stage 2 full paper (invited) 2027-04-16 23:59 AoE (verified 2026-10-28 at https://roboticsconference.org/information/cfp/)
**Topic:** Amortized, non-myopic active tactile localization (TouchBED)
**Initialised:** 2026-10-28T07:56:44Z
**Current version:** v6
**Latest stage:** Stage 17 PAPER_DRAFT [v6] (run 50, 2026-11-13); next stage 18 [v6]

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

---

## Stage 18 (pass 2) + Stage 19 (pass 2)     [v3]

- **Run 8.** D3-B complete (300/300; −20.1 pp, all criteria fail, report-only). Long-training row complete (reading
  (b); long − G\* −1.7 pp, ci95 [−6.8, +3.4]; status note in amendment v3.0). Both filled into the draft.
- Stage 18 pass 2 (required: pass-1 revision added > 30 %): two fresh opus reviewer pairs, `18_review_pass2_run{1,2}.md`.
  Scores 4 / 3 and 3 / 4; **CRITICAL_FABRICATION: no**. Found: R_b (reduced G\*) pilot rows exist though the paper said
  "not measured" → new report-only `code/analysis_rb_v3.py` → `results/v3/14_rb_frontier.json` (pilot3, incomplete
  155–186 / 200; e.g. g125_512_16 −4.3 pp success [−11.8, +3.2], −0.30 nats BI vs full G\* at 18 ms median); undisclosed
  second runtime (all distillation training in the sandbox: Python 3.13.18 / numpy 2.5.3); tie-fraction definition is a
  flat-score statistic; stale "(running)"; long row must be "exploratory, post-freeze".
- Stage 19 pass 2 (fresh opus subagent, template verbatim + facts block; snapshot `paper/mypaper/v3/draft_v3_stage19pass1.md`):
  all fixed. Body now 11,247 words (length-protected revision); condensed 5-page / 8-page exports are stage 22's job.
  Number audit: 0 unmatched apart from the version string "3.13"; never-write list clean; no placeholders.
- **Decision:** PROCEED → stage 20.

---

## Stage 20. QUALITY_GATE     [v3]  — FAIL (cycle 1 of 3)

- **Run 8.** Template verbatim (fresh opus subagent, json mode; prompt `paper/mypaper/prompts/stage20_*.txt`, threshold
  7.5 from RESTRICTS). Output `paper/mypaper/20_quality_gate.json` (copy in `paper/mypaper/v3/`).
- **Score 5.5 < 7.5.** Required actions 1–6 evidence-level (a cell where travel binds; budget-matched learners under the
  registered rule; reduced G\* paired on test; H3 instrument; seeds/sweeps; covariate shift), 7–11 paper-level.
- **Not auto-approved** (the gate failed; the owner's auto-approve directive covers passing gates only).
- **Decision (template decision table): evidence-level → loop to stage 13.**

---

## LOOP MARKER — REFINE from stage 20 → stage 13     [version v3 → v4]

- **Reason:** stage 20 v3 (5.5 / 10): the only learner cell S12 is a stay-and-probe regime (G\* travel 6.1° per
  episode), the amortization answer is open after the exploratory long-training row, and the cost claim lacks a
  reduced-G\* comparison on test. Refine cycle 3 of 3 (`RESTRICTS.yaml` max_refine_cycles) — the last allowed.
- **Snapshot taken:** `results/v3/` (unchanged, v4 writes to `results/v4/`), `paper/mypaper/v3/` (draft_v3_final.md,
  stage-17 and stage-19 snapshots, 20_quality_gate.json).
- **Design:** `docs/07c_amendment_v4_0.md` (written before any v4 run): learner cell S2 (κ = 2, τ = 4.7; design pilot:
  budgeted G\* travels 62° per episode on 6 pilot3 episodes), budget-matched student recipe (fixed 200 epochs per round,
  remedy-size DAgger, seeds 601–603), RL seeds 611–613, rule D4 (= D3 form, δ 4 pp), H2-S2; E5 reduced G\* on S12 test3.
- **Next stage:** 13 ITERATIVE_REFINE → 12-style runs (E1–E5) → 14 → 15 → 16–20.
- **Resuming under version:** v4
- **Where to resume (run 9, v4 stage 13):** dispatched in run 8: `v4_label_S2` (60 jobs), `v4_rl_S2` (3), `v4_e5_rb_test3`
  (100), plus v3 `v3_sub8_g5_r8` (61, report-only). Next: follow-ups for early-stopped label shards
  (`tools_resume_manifest.py` handles label3? — check; else re-issue missing indices), then E2 round 0 in the sandbox
  (write outputs to the scratchpad and copy into results/ afterwards: a git rebase during a sandbox run lost one output
  in run 8), DAgger r1/r2 manifests from `v3_d3rem_r1/r2.json`, then E4. Generalise the analyses with a `--cell` flag
  (default = v3 behaviour). The v3 paper text (`paper/mypaper/v3/draft_v3_final.md`) is the base for the v4 paper.
- **Run 8 end (≈ 22:15 UTC):** G5′ sub-8 re-reads 2 episodes short (A12 B-cov 198/200; follow-up manifest
  `experiments/v3_sub8_g5_r9.json`, not yet dispatched); `12_g5_analysis.json` re-run (all cells pass; S12 flat screen,
  H★ unchanged). Queue: `v4_rl_S2` running; `v4_label_S2`, `v4_e5_rb_test3` queued.

---

## Stage 13. ITERATIVE_REFINE     [v4]   (IN PROGRESS)

- **Run 9 (2026-11-01, from ≈ 09:5x UTC).** No open issues; no new owner directives. No commits between 10-29 23:14 and
  this run (the intervening scheduled runs left no trace).
- All run-8 dispatches finished (E1 labels 60/60, E3 RL 3/3, E5 100/100). **Defect found:** `.gitignore` excludes `*.npz`
  outside v2/v3, so the E1 label shards and E3 RL weights were not committed (JSON summaries only). Fixed by whitelisting
  `results/v4/**/*.npz`; E1 and E3 re-dispatched with the unchanged manifests (same seeds). The re-run JSONs are compared
  with the run-8 JSONs (git history) as a determinism check.
- **Run 9 progress (≈ 09:10 UTC).** E1 re-run: 60/60 shards, actions and summaries **identical** to run 8 (determinism
  check passed). E3 re-run: RL histories differ from run 8 from the first log row in the last bits (runner image glibc
  2.39 → 2.43; same Python 3.12.15 / numpy 2.5.4), final g_T within ≈ 0.01 nats (e.g. sd612 6.243 vs 6.234): RL is not
  bitwise reproducible across runner images; the re-run weights (committed) are the models of record.
  E2 round 0 (sandbox, Python 3.13.18 / numpy 2.5.3, as all v3 distillation): seeds 601–603, 200 fixed epochs, 2,700
  training episodes, held-out R̄ 0.308 / 0.300 / 0.312 (`results/v4/d4/`, script `code/dev/v4_distill_r0.sh`).
  `dagger_index` extended to seeds 601–699 in a range disjoint from v3 (test extended; suite 60 passed). DAgger r1
  dispatched (`experiments/v4_dag_S2_r1.json`, 60 × 40 episodes). E4 teacher/baseline side complete: val3 0–499 sub-8
  G\* (500/500), test3 0–499 no-grid G\*/B-fan/random (500 each); g_T (gt3, sandbox) for those three in `results/v4/h2/`;
  sub-8 re-read of test3 0–299 G\*/B-fan dispatched (`v4_e4_rg_base.json`), random queued for later (`v4_e4_rg_random.json`).
  **E5 complete** (300/300 paired, `code/analysis_e5_v4.py` → `results/v4/14_e5_analysis.json`): g125_512_16 success
  0.360, BI 5.97 nats at 21 ms median logged latency; g500_512_4 0.377, 6.04 at 46 ms; full G\* 0.427, 6.25; remedied
  students 0.382, 6.20; long students 0.410, 6.24. Reduced G\* − remedied student: success −2.2 pp [−6.9, +2.4] and
  −0.6 pp [−5.8, +4.8]; BI −0.23 [−0.32, −0.15] and −0.16 [−0.26, −0.06] nats (reading per amendment: reported, no
  claim beyond "at its logged latency").
- **Run 9 progress (≈ 10:45 UTC).** E2 complete: DAgger r1 and r2 60/60 shards each (Actions, β 0.5 / 0); students
  retrained 200 fixed epochs per round with warm start (sandbox): held-out R̄ r1 0.319 / 0.305 / 0.315, r2 (final)
  0.322 / 0.298 / 0.310 (3,500 → 4,300 training episodes; R̄ is on label-distribution validation shards).
  E3 RL S2 test3 0–499 no-grid + g_T (sandbox). Behaviour on test3 0–299 (logged travel per episode): G\* 46.9°,
  students 39.1°, RL 136.8° (always 3 probes), B-fan 1.5°, random 172.2° — S2 is a travelling regime as designed (S12
  G\* 6.1°). **H2-S2 complete (pre-registered rule):** g_T student − RL −0.445 nats, one-sided 95 % LB −0.749 < +0.10 →
  "not detected"; RL scores higher on its own objective in S2 (RL 5.979, student 5.534, G\* 5.397, B-fan 5.263,
  random 3.510). Pending: D4 val3 students (75 jobs), sub-8 test3 re-reads of students (36 jobs) and random (100 jobs, ~30 done).
- **Stage 13 [v4] finished (run 9, ≈ 12:30 UTC)** except the random anchor's sub-8 re-read (190/300, still running;
  it enters no contrast). **D4 (pre-registered, val3 0–499 sub 8, complete 500/500): FAIL** — (i) Δ̂_succ −2.8 pp <
  threshold −1.46 pp (student 0.486, G\* 0.514; SE 2.2 pp); (ii) Δ̂_BI −0.105 ≥ −0.15 passes; (iii) every seed > −4 pp
  passes (−3.6 / −2.8 / −2.0). Reading fixed in the amendment: "not shown to reach G\* in S2 either" (no remedy round).
  S2 test3 0–299 sub 8 (complete 300/300 paired): success G\* 0.553, students 0.451, RL 0.423, B-fan 0.370; student − G\*
  −10.2 pp [−16.6, −4.3], student − RL +2.8 pp [−4.1, +9.6], G\* − RL +13.0 pp [+6.4, +19.4], student − B-fan +8.1 pp
  [+1.7, +14.7]; BI student − RL +0.18 [+0.09, +0.27]. Note the val/test gap of the student − G\* contrast (−2.8 vs
  −10.2 pp): both are pre-registered read-outs, both reported. All in `results/v4/results_v4.json`.

---

## Stage 14. RESULT_ANALYSIS     [v4]

- **Finished:** 2026-11-01 run 9. Template verbatim, two fresh opus subagents (pass 1 analyst, pass 2 adversarial AC);
  merged `results/v4/14_analysis.md` (pass-2 items binding).
- Verdicts: D4 FAIL (clause i only), H2-S2 not detected, E5 reported (reduced G\* lower BI than both students at
  21 / 46 ms logged latency, success differences unresolved), v3 verdicts unchanged. Pass 2: S12 student already beat
  B-fan on BI in v3 (+0.226 [+0.141, +0.311]) — "first such evidence" wording withdrawn; "student imitates travel" and
  "RL loses ground because it travels" unsupported; val/test gap widens on all seeds.
- **Next (run 10): stage 15 RESEARCH_DECISION [v4]** with `results/v4/14_analysis.md`. v4 was the last refine cycle
  (3 of 3): a non-PROCEED decision goes to the owner (OWNER_TODO) rather than a new loop. Random anchor re-read
  (`v4_e4_rg_random.json`) may still need a follow-up: `python code/tools_regrid_followup.py experiments/v4_e4_rg_random.json …`.

---

## Stage 15. RESEARCH_DECISION     [v4]

- **Finished:** 2026-11-01 run 9. Template verbatim with the REFINE option (fresh opus subagent; prompts
  `results/v4/prompts/stage15_*.txt`) → `results/v4/15_decision.md`.
- **Decision: PROCEED → stage 16, characterisation sense only (outcome row 4 + S2 cell as exploratory evidence; no
  method claim).** The template's method-sense PROCEED rule is not met (D4 fails; student vs RL success +2.8 pp, ci95
  contains 0; H2-S2 not detected) and is stated as such. REFINE/PIVOT are not available (refine cycle 3 of 3 used) and
  would not fit (REFINE presumes the hypothesis holds; a fourth design is outside the pre-registration). Not a gate
  stage, so no auto-approval was needed.
- **Report-only tasks before stage 17 claims (by ≈ 11-08):** complete the random anchor re-read; add pass-2 per-episode
  checks (student/G\* travel correlation, per-seed test3 g_T) to `results_v4.json` via code; optional ≤ 4 CPU-h
  val3/test3 pipeline check. Pass-2 rewrites bind the wording. If stage 20 fails again → owner decides (no loop left).
- **Where to resume (run 10):** stage 16 PAPER_OUTLINE [v4] (base: `paper/mypaper/v3/draft_v3_final.md` + S2/E5 rows;
  RSS 2027 Stage 1 extended-abstract target), plus the report-only tasks above.

---

## Stage 16. PAPER_OUTLINE     [v4]

- **Finished:** 2026-11-01 run 9. Template verbatim (fresh opus subagent; prompts `paper/mypaper/prompts/stage16_*`),
  {feedback} = v3 stage-18 summary + v3 stage-20 gate JSON. Output `paper/mypaper/sections/00_outline.md` (v3 outline
  snapshotted in `paper/mypaper/v3/00_outline_v3.md`). RSS Stage 1 format, body ≈ 3,420 words, contributions C1–C5,
  results rows R1–R24 mapped to JSON keys, Figure 1 "same planner, two regimes"; no missing citations.
- **Where to resume (run 10): stage 17 PAPER_DRAFT [v4]** from the v3 final draft + outline; before it: (1) random
  anchor follow-up (`python code/tools_regrid_followup.py experiments/v4_e4_rg_random.json experiments/v4_e4_rg_random_r1.json "…"`,
  dispatch, then re-run `code/analysis_s2_v4.py` and `code/tools_results_v4.py`); (2) check G2′ κ = 2 τ in
  `docs/07c_amendment_v3_0.md`; (3) put the "do not cite yet" pass-2 checks into code/JSON or leave them out.
- **Run 9 end (≈ 12:25 UTC).**

---

## Stage 17. PAPER_DRAFT     [v4]

- **Run 10 (2026-11-01, from ≈ 13:50 UTC).** No open issues; no new owner directives.
- Pre-work: random-anchor sub-8 follow-up dispatched (`experiments/v4_e4_rg_random_r1.json`, 53 jobs / 66 episodes,
  Actions run 41313613262); G2′ κ = 2 row confirmed to be the S2 cell (τ 4.7, n\* 4, set S, from the shard header).
- **Finished:** template verbatim, fresh opus subagent (`paper/mypaper/prompts/stage17_v4_*`), output
  `paper/mypaper/sections/draft_v4.md` (body 7,706 words, all RESTRICTS floors met), Figure 1 prompt updated.
  Number audit: 0 unexplained numbers (2 benign derived/constant). Plan + checks: `plans/stage_17_paper_draft_v4.md`.
- **Next: stage 18 PEER_REVIEW [v4]** (two fresh-context reviewers + adversarial pass, as v3), then 19 → 20.

---

## Stage 18. PEER_REVIEW     [v4]

- **Finished:** 2026-11-01 run 10. Two fresh opus reviewers (template verbatim). Scores 4/3 and 4/3;
  **CRITICAL_FABRICATION: no** (both). Nine incidental mismatches (M1–M9, e.g. "K = 8 pairs" → 4 pairs; S2 Cal′
  "pass" without a verify run; travel includes the initial grid snap) → fixed in stage 19 (option b). Merged record and
  triage: `paper/mypaper/18_peer_review.md`.
- **Next:** report-only diagnostics (S_k2 Cal′ verify; val3 re-read through the test pipeline), then stage 19.

---

## Stage 19. PAPER_REVISION     [v4]

- **Run 10.** Report-only diagnostics for review items (allowed by `results/v4/15_decision.md`): travel split
  (`code/analysis_travel_split_v4.py` → `results/v4/14_travel_split.json`; G\* between-probe travel 4.3° in S12 vs
  44.8° in S2 on test3 0–299; B-fan's 1.454° is the unavoidable first grid snap); S2 Cal′ verify and the val3 pipeline
  check (`experiments/v4_diag_s2.json`, step 2 `v4_diag_s2_rg.json`; `code/analysis_diag_s2_v4.py` →
  `results/v4/14_diag_s2.json`). First reading: the no-grid (test-pipeline) val3 0–49 action sequences are identical
  to the inline D4 runs for G\* and student s601 (50/50 each), so the val/test gap is not an action-generation
  artefact; the sub-8 re-read comparison is running.
- Pass 1 of the revision done (template verbatim, fresh opus subagent; snapshot `paper/mypaper/v4/draft_v4_stage17.md`).
  Body +43 % → a second stage-18 pass after the PENDING markers (random anchor, Cal′ S2, pipeline check) are filled.
- Duplicate Actions run 41313609610 (an MCP dispatch that reported a network error but had queued) was cancelled.
- **Diagnostics complete:** S2 Cal′ verify 3.875 probes on cal3 0–199 (pass, run after the S2 experiments); val3 0–49
  through the test pipeline: identical actions, success and BI (50/50) for G\* and student s601 → the S2 val/test gap
  is not a scoring-pipeline artefact.
- **Second stage-18 pass** (body had grown > 30 %): two fresh opus reviewers, 4/3 and 4/3, CRITICAL_FABRICATION no;
  P1–P14 (`paper/mypaper/18_peer_review.md`). New report-only checks `results/v4/14_review2_checks.json` (S2 students
  over-fit under the registered fixed-200-epoch recipe: held-out R̄ lowest at epochs 22–130, +0.007–0.026 by epoch 200).
- **Pass 2 of the revision done** (snapshot `paper/mypaper/v4/draft_v4_stage19pass1.md`): P1–P13 fixed; body ≈ 12,000
  words (master draft; Stage 1 extended abstract is condensed in stage 22).
- Random anchor: 293/300 re-read; last 7 episodes in Actions (`v4_e4_rg_random_r2.json` + one r1 job). It enters no
  contrast; the marker is filled when complete.
- **Next: stage 20 QUALITY_GATE [v4].** No refine cycle left: a FAIL goes to the owner (OWNER_TODO).

---

## Stage 20. QUALITY_GATE     [v4]  — FAIL (escalated to the owner)

- **Run 10.** Template verbatim (fresh opus subagent, json mode; prompts `paper/mypaper/prompts/stage20_v4_*`,
  threshold 7.5). Output `paper/mypaper/20_quality_gate.json`. **Score 5.0 < 7.5** (v3: 5.5).
- Required actions: 1 paper-level (fill the random row / Figure 1), 1 writing; 9 evidence-level (more cells and seeds,
  g_T inversion intervals and an S2-tuned / probe-aware RL, 512-action H3 screen + V_LA bias, sub-16 evaluator, fresh
  test split, S2 val/test gap + early stopping, S2 B-spread/B-cov, belief/attention head, Lat′ frontier).
- **Not auto-approved** (the gate failed). Decision table → evidence-level → stage 13, but the refine cap (3 of 3,
  `RESTRICTS.yaml`) is used up; per AUTOPILOT §5 and the stage-15 v4 pre-commitment the decision goes to the owner
  (OWNER_TODO, 2026-11-01 run 10). No new loop is opened by the pipeline.
- **Until the owner decides (default):** only low-risk work — fill the random anchor row when its re-read finishes,
  paper-level tightening that changes no claim, stage 21 knowledge archive. No stage 22 export, no DONE mark.
- **Run 10 end (low-risk follow-up).** S2 random anchor re-read complete (300/300; success 0.1167, BI 3.622; no
  contrast) → JSON regenerated, the three PENDING markers in `draft_v4.md` replaced (0 left; number audit unchanged:
  7 benign). The duplicate MCP dispatch had committed 11 of the follow-up outputs first, so 11 jobs of the original run
  failed only at "Commit outputs" (no data loss).
- **Where to resume (run 11):** read the owner's answer to the stage-20 escalation in OWNER_TODO / AUTOPILOT §1.
  No answer → low-risk only: stage 21 KNOWLEDGE_ARCHIVE [v4] (`docs/21_retrospective.md`), wording tightening that
  changes no claim; Figure 1 is still a placeholder (prompt in `paper/mypaper/figures/figure1_prompt.txt`).

---

## Stage 21. KNOWLEDGE_ARCHIVE     [v4]

- **Run 11 (2026-11-01, from ≈ 19:50 UTC).** No open issues; AUTOPILOT §1 has no new owner directive; `RESTRICTS.yaml`
  max_refine_cycles still 3 → the stage-20 escalation is unanswered, so only low-risk work (OWNER_TODO default).
- **Finished:** template `knowledge_archive.md` verbatim (prompts `docs/prompts/stage21_v4_{system,user}.txt`;
  {decision} = `results/v4/15_decision.md`, {analysis} = `results/v4/14_analysis.md`, {revised} =
  `paper/mypaper/sections/draft_v4.md`), fresh opus subagent → `docs/21_retrospective.md`. Changes no claim or number;
  states the paper is NOT done.
- **Checks:** all 142 numeric tokens in the archive occur in the prompt or in the cited repo files (PROGRESS hardware
  line, requirements, workflow, amendments v3.0/v3.1/v4.0, `results_v4.json`); all cited paths exist. Two facts written
  as "not recorded" (runner CPU model, measured total v4 wall clock). Noted: `code/requirements.txt` has lower bounds
  only (no exact pins) — listed as an open item, not changed now.
- **Not done (by design):** no stage 22 export, no new loop, no DONE mark.
- **Where to resume (run 12):** read the owner's answer to the stage-20 escalation (OWNER_TODO / AUTOPILOT §1 / issues).
  No answer → low-risk only (wording that changes no claim; Figure 1 remains a placeholder prompt). With (a)/(b) → stage
  21 is done, go to stage 22 under the chosen target; with (c) → LOOP MARKER v4 → v5 at stage 13 after the owner raises
  the cap; with (d) → stage 8.

- **Run 12 (2026-11-02).** No open issues; AUTOPILOT §1 has no new owner directive; `max_refine_cycles` still 3 → the
  stage-20 escalation is still unanswered, so low-risk work only (OWNER_TODO default).
- **Environment record (plan `plans/stage_21b_env_record_v4.md`):** `code/requirements-lock.txt` copied from the pip log
  of Actions job 124884356660 (numpy 2.5.4, scipy 1.18.1, shapely 2.2.0, mujoco 3.17.0, CPython 3.12.15; all four
  versions confirmed on PyPI from the sandbox); `code/tools_env_census.py` → `results/v4/env_census.json` (all 590 v4
  shards carry an env header: 574 runner Py 3.12.15 / numpy 2.5.4, 16 sandbox Py 3.13.18 / numpy 2.5.3). Addendum in
  `docs/21_retrospective.md`. Workflows unchanged; no claim or number in the paper changed.
- **Where to resume (run 13):** unchanged — read the owner's answer (OWNER_TODO / AUTOPILOT §1 / issues). No answer →
  low-risk only. RSS Stage 1 deadline 2026-12-04 AoE: if (b) arrives, stage 22 needs the ≤ 5-page condensation.

- **Run 13 (2026-11-02, from ≈ 07:54 UTC).** No open issues; AUTOPILOT §1 has no new owner directive; `max_refine_cycles`
  still 3 → the stage-20 escalation is still unanswered, so low-risk work only. The `add_repo` tool was not available
  this run; the session started with a pre-cloned (shallow, stale) checkout, so `git fetch --unshallow` then ff to
  origin/main. The fetch's "forced update" note was a shallow-clone artefact: the old ref is an ancestor of main, no
  history was rewritten.
- **Figure 1 panel D inset (plan `plans/stage_21c_figure1_panelD_v4.md`):** `code/plot_figure1_panelD.py` reads the
  values from the v3/v4 results JSONs, asserts them against the numbers printed in `figure1_prompt.txt`, and writes
  `paper/mypaper/figures/figure1_panelD.{pdf,png}`. Stale "random row incomplete" line in the prompt corrected. No
  experiment, claim or number changed; panels A–C remain a generator prompt, `draft_v4.md` still shows the placeholder.
- **Where to resume (run 14):** unchanged — read the owner's answer (OWNER_TODO / AUTOPILOT §1 / issues). No answer →
  low-risk only. RSS Stage 1 deadline 2026-12-04 AoE: if (b) arrives, stage 22 needs the ≤ 5-page condensation.

- **Run 14 (2026-11-02, from ≈ 14:49 UTC).** No open issues; AUTOPILOT §1 has no new owner directive; `max_refine_cycles`
  still 3 → the stage-20 escalation is still unanswered, so low-risk work only. No stage advanced, no claim, number or
  draft text changed. `add_repo` again unavailable; same stale shallow checkout as run 13 (`git fetch --unshallow`, ff to
  origin/main; dabde70 confirmed an ancestor, 720 commits behind, no rewrite). Read the pipeline state from origin/main,
  not from the local `main` ref, which is stale at session start.
- **Health checks on main (no code change):** `tools_number_audit.py` on `draft_v4.md`: 7 unmatched, same as run 10; each
  re-derived by hand (97.5 quantile, 1.16, 0.842 and 0.189 are constants or arithmetic on reported values); 0 PENDING
  markers. Unit tests: every file in `code/tests/` passes run on its own (60 tests, sandbox Py 3.13 / numpy 2.5.3).
  Caveat: one all-files `pytest tests` call was killed at its 500 s limit with no output and was not retried, so a full
  single-process pass is not established (per-file times sum to ≈ 170 s; cause unknown). `run_checks.py` not re-run.
- **RSS CFP re-read (WebFetch):** Stage 1 2026-12-04 AoE, 6 pages (5 content + 1 references); Stage 2 2027-04-16 AoE,
  8 pages excluding references; "use of LLMs is permitted for both authors and reviewers", disclosure encouraged,
  hallucinated citations → desk reject. Unchanged. The older authorinfo page contradiction remains an owner item.
- **Owner notified by push once this run** (32 days to Stage 1). Later runs: stay silent on this unless something new
  happens; the next reminder is at the 2026-11-20 decision date proposed in OWNER_TODO.
- **Where to resume (run 15):** unchanged — read the owner's answer (OWNER_TODO / AUTOPILOT §1 / issues). No answer →
  low-risk only; there is little low-risk work left, so short runs are expected. With (a)/(b) → stage 22; with (c) →
  LOOP MARKER v4 → v5 at stage 13 after the owner raises the cap; with (d) → stage 8.

- **Run 15 (2026-11-02, from ≈ 19:50 UTC).** No open issues (GitHub MCP; WebFetch of the issues page was refused this run);
  AUTOPILOT §1 has no new owner directive; `max_refine_cycles` still 3 → the stage-20 escalation is still unanswered, so
  low-risk work only. No stage advanced; no claim, number or draft text changed. `add_repo` again unavailable; checkout
  was shallow but already at origin/main (13cd849), detached HEAD.
- **Closed run 14's test caveat:** with `code/requirements-lock.txt` installed (numpy 2.5.4, shapely 2.2.0, mujoco 3.17.0;
  sandbox Python 3.13, not the runner's 3.12) and `OMP/OPENBLAS/MKL_NUM_THREADS=1`, `pytest tests` in one process:
  60 passed in 106 s. Why run 14's call hit its 500 s limit is not established: the thread limit and the numpy version
  both differed, and neither was tested alone. `run_checks.py` not re-run.
- **No push notification** (nothing new, per run 14). Next reminder stays at the 2026-11-20 date proposed in OWNER_TODO.
- **Where to resume (run 16):** unchanged — read the owner's answer (OWNER_TODO / AUTOPILOT §1 / issues). No answer →
  low-risk only; short runs expected. With (a)/(b) → stage 22; with (c) → LOOP MARKER v4 → v5 at stage 13 after the owner
  raises the cap; with (d) → stage 8.

- **Run 16 (2026-11-03, from ≈ 01:50 UTC).** No open issues (GitHub MCP; WebFetch of the issues page was refused again);
  AUTOPILOT §1 has no new owner directive; `max_refine_cycles` still 3 → the stage-20 escalation is still unanswered, so
  low-risk work only. No stage advanced; the master `draft_v4.md`, every claim and every number are unchanged. `add_repo`
  again unavailable; shallow checkout already at origin/main (f99af6a), detached HEAD.
- **Condensed draft (plan `plans/stage_21d_condensation_v4.md`):** `paper/mypaper/sections/draft_v4_condensed.md`, about
  2,500 words, under the OWNER_TODO default's "text condensation that changes no conclusion". Preparation for (a)/(b) only;
  NOT a stage 22 output: no template, no LaTeX, page count unknown (only a compiled PDF decides), and the file header says
  the gate failed and it is not cleared for submission. Below the `section_floors` by design; master keeps those.
- **Checks:** no numeric token or cite key absent from the master; `tools_number_audit.py` 0 unmatched. A fresh subagent
  compared the two texts in full: no numeric errors, 12 status/strength findings and 2 borderline ones (for example D4 worded
  as testing H1, report-only labels dropped, the 7.5 % flip rate read as an error bar). All 14 fixed, then the token and
  audit checks were re-run; the fixes were not re-reviewed by a second subagent.
- **Correction:** commit 9760b87 logged these fixes as done, but its fix script had aborted, so that commit holds the unfixed
  text. The next commit applies all 14 and re-runs the checks; read this entry against that commit.
- **No push notification for this** (nothing the owner must act on sooner; run 14's rule). Next reminder stays at 2026-11-20.
- **Where to resume (run 17):** unchanged — read the owner's answer (OWNER_TODO / AUTOPILOT §1 / issues). No answer →
  low-risk only; short runs expected. With (a)/(b) → stage 22, starting from `draft_v4_condensed.md`; with (c) → LOOP MARKER
  v4 → v5 at stage 13 after the owner raises the cap; with (d) → stage 8.

- **Run 17 (2026-11-03, from ≈ 07:50 UTC).** No open issues (GitHub MCP; WebFetch of the issues page was refused again);
  AUTOPILOT §1 has no new owner directive; `max_refine_cycles` still 3 → the stage-20 escalation is still unanswered, so
  low-risk work only. No stage advanced; the master `draft_v4.md`, every claim and every number are unchanged. `add_repo`
  again unavailable; shallow checkout already at origin/main (ef14d8f), detached HEAD. No workflow running or queued in the
  latest list (last run 2026-11-01).
- **Closed run 16's caveat on the condensed draft:** a second fresh subagent, given only the two texts, compared them after
  the 14 fixes: no must-fix, 7 borderline (5 dropped qualifiers or scope, 1 citation attached to a firmer claim than the
  master, 1 loose gate description), plus the header comment's "adds no number" not covering the comment itself. I checked each
  against the master and applied all 8 to `draft_v4_condensed.md` (now about 2,540 words). Re-run: no numeric token or cite
  key absent from the master; `tools_number_audit.py` 0 unmatched. These last edits were not reviewed by a third subagent.
- **No push notification** (nothing new, per run 14). Next reminder stays at 2026-11-20.
- **Where to resume (run 18):** unchanged — read the owner's answer (OWNER_TODO / AUTOPILOT §1 / issues). No answer →
  low-risk only; little is left, so a run with nothing to do should only check and log. With (a)/(b) → stage 22, starting
  from `draft_v4_condensed.md`; with (c) → LOOP MARKER v4 → v5 at stage 13 after the owner raises the cap; with (d) → stage 8.

- **Run 18 (2026-11-03, from ≈ 13:50 UTC).** Check-and-log only. No open issues (GitHub MCP; WebFetch of the issues page was
  refused again); AUTOPILOT §1 has no new owner directive; `max_refine_cycles` still 3 → the stage-20 escalation is still
  unanswered. No stage advanced; no draft, claim or number changed. `add_repo` again unavailable; checkout already at
  origin/main (fa068e0), detached HEAD; the fetch's "forced update" on dabde70 is the same stale-ref artefact as runs 13–14.
  No workflow running (last run 2026-11-01). `tools_number_audit.py`: `draft_v4_condensed.md` 0 unmatched, `draft_v4.md` 7
  (same as run 14). CFP not re-read this run (last read run 14).
- **No push notification** (nothing new, per run 14). Next reminder stays at 2026-11-20.
- **Where to resume (run 19):** unchanged from run 17's entry above: read the owner's answer; none → check and log only.

- **Run 19 (2026-11-03, from ≈ 19:59 UTC).** Check-and-log only. No open issues (GitHub MCP; WebFetch of the issues page was
  refused again); AUTOPILOT §1 has no new owner directive; `max_refine_cycles` still 3 → the stage-20 escalation is still
  unanswered. No stage advanced; no draft, claim or number changed. `add_repo` again unavailable; checkout already at
  origin/main (7523694), detached HEAD. No workflow running (last run 2026-11-01). `tools_number_audit.py`:
  `draft_v4_condensed.md` 0 unmatched, `draft_v4.md` 7 (same as runs 14 and 18). CFP not re-read this run (last read run 14).
- **No push notification** (nothing new, per run 14). Next reminder stays at 2026-11-20.
- **Where to resume (run 20):** unchanged from run 17's entry: read the owner's answer; none → check and log only.

- **Run 20 (2026-11-04, from ≈ 01:49 UTC).** Check-and-log only. No open issues (GitHub MCP; WebFetch of the issues page was
  refused again); AUTOPILOT §1 has no new owner directive; `max_refine_cycles` still 3 → the stage-20 escalation is still
  unanswered. No stage advanced; no draft, claim or number changed. `add_repo` again unavailable; checkout already at
  origin/main (92a0d25), detached HEAD. No workflow running (last run 2026-11-01). `tools_number_audit.py`:
  `draft_v4_condensed.md` 0 unmatched, `draft_v4.md` 7 (same as runs 14, 18, 19). CFP not re-read this run (last read run 14).
- **No push notification** (nothing new, per run 14). Next reminder stays at 2026-11-20.
- **Where to resume (run 21):** unchanged from run 17's entry: read the owner's answer; none → check and log only.

- **Run 21 (2026-11-04, from ≈ 07:49 UTC).** Check-and-log only. No open issues (GitHub MCP; WebFetch of the issues page was
  refused again); AUTOPILOT §1 has no new owner directive; `max_refine_cycles` still 3 → the stage-20 escalation is still
  unanswered. No stage advanced; no draft, claim or number changed. `add_repo` again unavailable; checkout already at
  origin/main (dda939a), detached HEAD; the fetch's "forced update" on dabde70 is the same stale-ref artefact as earlier runs.
  No workflow running (last run 2026-11-01). `tools_number_audit.py`: `draft_v4_condensed.md` 0 unmatched, `draft_v4.md` 7
  (same as runs 14, 18–20). CFP not re-read: WebFetch of the CFP page was refused this run (last read run 14).
- **No push notification** (nothing new, per run 14). Next reminder stays at 2026-11-20.
- **Where to resume (run 22):** unchanged from run 17's entry: read the owner's answer; none → check and log only.

- **Run 22 (2026-11-04, from ≈ 13:49 UTC).** Check-and-log only. No open issues (GitHub MCP; WebFetch of the issues page was
  refused again); AUTOPILOT §1 has no new owner directive; `max_refine_cycles` still 3 → the stage-20 escalation is still
  unanswered. No stage advanced; no draft, claim or number changed. `add_repo` again unavailable; checkout already at
  origin/main (2893ed9), detached HEAD; the fetch's "forced update" on dabde70 is the same stale-ref artefact as earlier runs.
  No workflow running (last run 2026-11-01). `tools_number_audit.py`: `draft_v4_condensed.md` 0 unmatched, `draft_v4.md` 7
  (same as runs 14, 18–21). CFP not re-read this run (last read run 14).
- **No push notification** (nothing new, per run 14). Next reminder stays at 2026-11-20.
- **Where to resume (run 23):** unchanged from run 17's entry: read the owner's answer; none → check and log only.

- **Run 23 (2026-11-04, log written ≈ 19:55 UTC).** Check-and-log only. No open issues (GitHub MCP; WebFetch of the issues page
  not attempted this run); AUTOPILOT §1 has no new owner directive; `max_refine_cycles` still 3 → the stage-20 escalation is
  still unanswered. No stage advanced; no draft, claim or number changed. `add_repo` again unavailable; checkout already at
  origin/main (7cf4fdf), detached HEAD; the fetch's "forced update" on dabde70 is the same stale-ref artefact as earlier runs.
  No workflow running (last run 2026-11-01). `tools_number_audit.py`: `draft_v4_condensed.md` 0 unmatched, `draft_v4.md` 7
  (same as runs 14, 18–22). CFP not re-read: fetch of the RSS site was refused at the permission step (last read run 14).
- **No push notification** (nothing new, per run 14). Next reminder stays at 2026-11-20.
- **Where to resume (run 24):** unchanged from run 17's entry: read the owner's answer; none → check and log only.

- **Run 24 (2026-11-05, from ≈ 01:49 UTC).** Check-and-log only. No open issues (GitHub MCP; WebFetch not available as a direct
  tool this run); AUTOPILOT §1 has no new owner directive; `max_refine_cycles` still 3 → the stage-20 escalation is still
  unanswered. No stage advanced; no draft, claim or number changed. `add_repo` again unavailable; checkout already at
  origin/main (02e1a74), detached HEAD; the fetch's "forced update" on dabde70 is the same stale-ref artefact as earlier runs.
  No workflow running (last run 2026-11-01). `tools_number_audit.py`: `draft_v4_condensed.md` 0 unmatched, `draft_v4.md` 7
  (same as runs 14, 18–23). CFP page not re-read; one WebSearch returned no RSS 2027 CFP page, so the deadline is neither
  re-confirmed nor contradicted (last read run 14).
- **No push notification** (nothing new, per run 14). Next reminder stays at 2026-11-20.
- **Where to resume (run 25):** unchanged from run 17's entry: read the owner's answer; none → check and log only.

- **Run 25 (2026-11-05, log written ≈ 07:50 UTC).** Check-and-log only. No open issues (GitHub MCP; WebFetch not available as a direct
  tool this run); AUTOPILOT §1 has no new owner directive; `max_refine_cycles` still 3 → the stage-20 escalation is still
  unanswered. No stage advanced; no draft, claim or number changed. `add_repo` again unavailable; checkout already at
  origin/main (cadb3ec), detached HEAD. No workflow running (last run 2026-11-01). `tools_number_audit.py`:
  `draft_v4_condensed.md` 0 unmatched, `draft_v4.md` 7 (same as runs 14, 18–24). CFP page not re-read; one WebSearch returned
  no RSS 2027 CFP page, so the deadline is neither re-confirmed nor contradicted (last read run 14).
- **No push notification** (nothing new, per run 14). Next reminder stays at 2026-11-20.
- **Where to resume (run 26):** unchanged from run 17's entry: read the owner's answer; none → check and log only.

- **Run 26 (2026-11-05, from ≈ 13:50 UTC).** Check-and-log only. No open issues, and no issue closed since 10-25 (GitHub MCP;
  WebFetch not available as a direct tool this run); AUTOPILOT §1 has no new owner directive; `max_refine_cycles` still 3 → the
  stage-20 escalation is still unanswered. No stage advanced; no draft, claim or number changed. `add_repo` again unavailable;
  checkout already at origin/main (6088053), detached HEAD. No workflow running (last run 2026-11-01). `tools_number_audit.py`:
  `draft_v4_condensed.md` 0 unmatched, `draft_v4.md` 7 (same as runs 14, 18–25). CFP page not re-read; one WebSearch returned
  no RSS 2027 CFP page, so the deadline is neither re-confirmed nor contradicted (last read run 14).
- **No push notification** (nothing new, per run 14). Next reminder stays at 2026-11-20.
- **Where to resume (run 27):** unchanged from run 17's entry: read the owner's answer; none → check and log only.

- **Run 27 (2026-11-05, from ≈ 19:50 UTC).** Check-and-log only. No open issues (GitHub MCP); AUTOPILOT §1 has no new owner
  directive; `max_refine_cycles` still 3 → the stage-20 escalation is still unanswered. No stage advanced; no draft, claim or
  number changed. `add_repo` again unavailable; checkout on main, level with origin/main (03666db). No workflow running (last
  run 2026-11-01). `tools_number_audit.py`: `draft_v4_condensed.md` 0 unmatched, `draft_v4.md` 7 (same as runs 14, 18–26).
  CFP page not re-read; one WebSearch returned no RSS 2027 CFP page, so the deadline is neither re-confirmed nor contradicted
  (last read run 14).
- **No push notification** (nothing new, per run 14). Next reminder stays at 2026-11-20.
- **Where to resume (run 28):** unchanged from run 17's entry: read the owner's answer; none → check and log only.

- **Run 28 (2026-11-06, from ≈ 01:50 UTC).** Check-and-log only. No open issues (GitHub MCP); AUTOPILOT §1 has no new owner
  directive; `max_refine_cycles` still 3 → the stage-20 escalation is still unanswered. No stage advanced; no draft, claim or
  number changed. `add_repo` again unavailable; checkout on main, level with origin/main (c57c2be). No workflow running (last
  run 2026-11-01). `tools_number_audit.py`: `draft_v4_condensed.md` 0 unmatched, `draft_v4.md` 7 (same as runs 14, 18–27).
  CFP page not re-read: the fetch was blocked at the permission step (not answered in time); one WebSearch returned no RSS 2027
  CFP page, so the deadline is neither re-confirmed nor contradicted (last read run 14).
- **No push notification** (nothing new, per run 14). Next reminder stays at 2026-11-20.
- **Where to resume (run 29):** unchanged from run 17's entry: read the owner's answer; none → check and log only.

- **Run 29 (2026-11-06, from ≈ 07:50 UTC).** Check-and-log only. No open issues and none updated since 11-01 (GitHub MCP);
  AUTOPILOT §1 has no new owner directive; `max_refine_cycles` still 3 → the stage-20 escalation is still unanswered. No stage
  advanced; no draft, claim or number changed. `add_repo` not available as a tool this run; checkout moved onto main, level with
  origin/main (461a5c1). `tools_number_audit.py`: `draft_v4_condensed.md` 0 unmatched, `draft_v4.md` 7 (same as runs 14,
  18–28). CFP page not re-read (last read run 14).
- **No push notification** (nothing new, per run 14). Next reminder stays at 2026-11-20.
- **Where to resume (run 30):** unchanged from run 17's entry: read the owner's answer; none → check and log only.

## OWNER DECISION — 2026-11-06 (in chat, after run 29)
- The owner read the run-29 summary and the stage-20 v4 weaknesses and instructed: improve the evidence ("那你提升这里啊")
  → option (c). Also accepted the RSS LLM-policy reading (2027 CFP permits LLM use; the conflicting page is a stale 2025
  page, verified 2026-11-06, see `AI_USAGE.md`). Recorded in AUTOPILOT §1; `RESTRICTS.yaml` `max_refine_cycles` 3 → 4.

## LOOP MARKER — REFINE from stage 20 → stage 13     [version v4 → v5]

- **Reason:** stage 20 v4 5.0 / 10 (`paper/mypaper/v4/20_quality_gate.json`); evidence-level actions (one cell per
  regime, 3 seeds, untuned S2 RL, re-used test split, evaluator unchecked below sub 8, S2 baselines = B-fan only).
  Refine cycle 4 of 4 (cap raised by the owner).
- **Snapshot taken:** `results/v4/` (unchanged; v5 writes `results/v5/`), `paper/mypaper/v4/` (draft_v4_final.md,
  draft_v4_condensed.md, 18_peer_review.md, 20_quality_gate.json, earlier stage snapshots).
- **Design:** `docs/07c_amendment_v5_0.md` (written before any v5 run): cells S2/S4/S8/S12 + A16-2, one student recipe
  (fixed 200 epochs, best held-out-R̄ checkpoint), 5 student seeds (701–705), RL tuned on S2 then 5 seeds (711–715) +
  `rl_success` control, fresh split test5 evaluated once after a recorded freeze, 4 heuristic baselines, sub-16 check,
  Lat′ timing, optional H3 full screen. Rules D5, H5a, H5b, H2-v5; Holm over cells. Estimate ≈ 800–860 CPU-h.
- **Next stage:** 13 ITERATIVE_REFINE (code: test5 salt, best-checkpoint distillation, `--sub 16`) → P0 pilot →
  amendment v5.1 → E1–E7 → 14 → 15 → 16–20.
- **Resuming under version:** v5

## Stage 13 · ITERATIVE_REFINE · v5 (started 2026-11-06 ≈ 08:30 UTC, in the owner's chat session)
- **Plan:** `plans/stage_13_iterative_refine_v5.md`.
- **Code (aeb3165):** split `test5` (salt 107; tests show it is disjoint from test3/val3/pilot3/cal3 and paired across
  κ); DAgger index range for seeds 701–799 (≥ 2,000,000, disjoint from v3/v4); `distill3 --keep best` (keeps the
  lowest held-out-R̄ checkpoint, also saves `<out>_last.npz`; default `last` so v3/v4 commands reproduce); grid
  read-out batch scaled for sub > 8 (sub 16 was OOM-killed in the sandbox; sub ≤ 8 paths unchanged). Full test suite 63
  passed + 3 new v5 tests.
- **Amendment v5.0 edits before any v5 job:** A16 n\* by the unchanged v3 Cal′ rule (not an ad-hoc scan); RL sweep
  selection by the v3 D9 rule (trainer-validation ball-sPCE), sweep cfg 0 = the v3/v4 config.
- **Timing (sandbox, report-only):** G\* on A16 κ 0 τ 4, sub 8: 23 s per cal3 episode; `regrid3 --sub 16`: 109 s per
  episode (S2 test3 ep 0) → E5 ≈ 25 CPU-h (estimate was 15).
- **Dispatched on Actions:** `v5_p0_cal` (26 jobs: Cal′ τ for S κ 4 / κ 8, A16 n\* scan), `v5_rl_sweep_S2` (8 configs,
  seed 719, 10⁵ episodes), `v5_d5_r0_S2_S12` (10 jobs: round-0 students, seeds 701–705, re-using v4 S2 / v3 S12 labels).
- **Where to resume:** when P0 lands → `analysis_cal_v3.py`-style analysis for S4, S8, A16 (write
  `results/v5/12_cal_analysis.json`); if A16 n\* ≠ 4, run 200 cal3 at τ = n\* to check the [0.30, 0.90] keep rule; then
  amendment v5.1 (τ per cell, sizes) → labels for S4, S8, A16-2 → DAgger r1/r2 (copy `v4_dag_S2_r1/r2.json`, seeds
  701–705, `--keep best` in the distill steps) → RL sweep selection → RL 5 seeds × 5 cells + rl_success S2/S12 → val3 D5.

- **Run 30 (2026-11-06, from ≈ 13:51 UTC, scheduled) — stage 13 v5 continued.** No open issues; AUTOPILOT §1 unchanged
  since the owner's (c) directive. All three P0 dispatches of the chat session had landed (cal 26/26 jobs, RL sweep 8/8,
  round-0 students 10/10).
  - **P0 read-out** (`code/analysis_cal_v5.py` → `results/v5/12_cal_analysis.json`): S4 τ = 4.8 (mean G\* travel time
    0.797), S8 τ = 4.8 (0.834); A16 G\* sub-8 success at κ 0, τ 4 = 0.975 > 0.88 → **n\*(A16) = 3** by the v3 rule; the
    keep check ([0.30, 0.90] at κ 0, τ = 3, reading fixed in amendment v5.1 before the run) and the A16 κ 2 τ
    calibration are running (`experiments/v5_p0_a16.json`).
  - **RL sweep** (`code/analysis_rl_sweep_v5.py` → `results/v5/12_rl_sweep_selection.json`): v3 D9 rule → **cfg 6**
    (final val ball-sPCE 6.300 vs 6.241 for the v3/v4 cfg 0; outside the 0.02 tie band).
  - **Incident:** the round-0 students and the sweep had committed JSON but no `.npz` (`*.npz` ignored outside v2–v4,
    same slip as v4 run 8). Fixed `.gitignore`; round 0 re-run with identical commands. Determinism check against the
    first JSONs (`results/v5/prev_r0_json/`): same best epoch in 10/10, identical held-out R̄ in 9/10; S2 seed 705
    differs by 0.0012 (0.2793 → 0.2805; likely a different runner CPU / BLAS path). The re-run weights are the models
    of record.
  - **Amendment v5.1** (`docs/07c_amendment_v5_1.md`): cells, τ, n\*, RL cfg 6, no size reduction (estimate still
    < 1,000 CPU-h). **Addendum v5.1a:** `rl_success` added to the relative-frame trainer (v1 definition: terminal
    1[success] of a 1,000-particle PF; validation PF-free on the spce_total stream); test added, full suite 64 passed;
    smoke run 512 episodes in 27 s.
  - Pilot TIME_ESTIMATE S4 / S8 in the sandbox (`results/v5/pilot/`).
  - **Dispatched:** round-0 re-run (done), A16 keep + τ (18 jobs), RL cfg 6 × seeds 711–715 × S2/S12/S4/S8 (20),
    labels S4/S8 0–2,999 (120), rl_success S2/S12 × 5 seeds (10), DAgger r1 S2/S12 × 5 seeds × 800 episodes (200).
  - **Later in run 30:** A16 keep check complete: G\* sub-8 success 0.800 at κ 0, τ 3 (200 episodes) → **A16-2 kept**;
    τ(A16, κ 2) = 3 + 0.351 = **3.4** (amendment v5.1 updated). Dispatched A16-2 labels (60) + RL cfg 6 × 5 seeds,
    G\* val3 0–499 in S4/S8/A16-2 (75 jobs; S2/S12 re-use v4/v3 G\* val3 records, addendum v5.1b, stated before any
    v5 val3 job), heuristic baselines B-fan/B-spread/B-cov on pilot3 0–199 in all 5 cells (150 jobs, shards of 20
    because one A16 sub-8 episode took > 2 min in the sandbox). Pre-written: `code/analysis_d5_v5.py` (D5 per cell),
    `code/tools_v5_manifests.py` (round-0 / dag2 / distill1 / distill2 manifests with input-existence checks; it
    reproduces the dispatched S2/S12 round-0 manifest exactly).
  - **Queue at run end (≈ 640 jobs, 20 concurrent):** RL S-cells (20), S4/S8 labels (120), rl_success (10), DAgger r1
    S2/S12 (200), A16 labels + RL (65), G\* val3 new cells (75), baselines (150). Expect ≈ 12–15 h of wall time.
  - **Where to resume (run 31):** (1) DAgger r1 S2/S12 landed → `python tools_v5_manifests.py distill1 S2 S12` → dispatch
    → then `dag2 S2 S12` → `distill2`. (2) S4/S8 labels landed → `tools_v5_manifests.py r0 S4 S8`; A16 labels landed →
    `r0 A16-2`; then r1 DAgger for those cells (adapt the r1 manifest: weights `_r0.npz`, β 0.5, `--round 1`). (3) Any
    shard that hit its time budget → follow-up manifest (`code/tools_resume_manifest.py`). (4) Baselines landed → H\*
    per cell (write `analysis_base_v5.py`). (5) Students r2 → val3 eval (students, sub 8, 20-episode shards) →
    `analysis_d5_v5.py`. test5 stays untouched until the freeze commit.

- **Run 31 (2026-11-06, from ≈ 19:30 UTC, scheduled) — stage 13 v5 continued.** No open issues; AUTOPILOT §1 unchanged.
  All run-30 dispatches had finished (last at 18:56 UTC).
  - **Audit of landed outputs:** S4/S8 labels 120/120 complete; DAgger r1 S2/S12 200/200 complete; RL cfg 6 × 5 seeds
    in all 5 cells reached 2 × 10⁵ episodes; 9 of 10 `rl_success` runs were stopped by the time guard at 111k–185k
    episodes (no resume in the trainer → recorded in addendum v5.1c before any evaluation; the saved weights are the
    models of record, episode counts reported with every number). G\* val3 new cells 1,370 / 1,500 episodes; baselines
    on pilot3 2,037 / 3,000 episodes (per-episode wall time up to ≈ 24 min for B-cov at sub 8).
  - **Incident:** Actions run 42233537062 failed in all 60 A16-2 label jobs (`episode_arrays` belief buffer fixed at 48
    wide; A16 has K = 16 → 96). Fixed in `touchbed/distill.py` (width follows the labels; S outputs unchanged), test
    added (suite 65 passed), sandbox check: A16 label3 2 episodes + 3-epoch distill3 OK. Re-dispatched with identical
    commands (`experiments/v5_a16_label_rerun.json`).
  - **Dispatched:** r1 students S2/S12 (`v5_distill1_S2_S12`, 10), round-0 students S4/S8 (`v5_r0_S4_S8`, 10), A16
    labels (60), baseline follow-ups (`v5_base_pilot_f1`, 246 shards ≈ 15 min each), G\* val3 follow-ups
    (`v5_val_gstar_new_f1`, 42 shards).
  - **Code:** `code/analysis_base_v5.py` (H\* per cell by the v5 Baselines rule, v3 tie-break; not run to a result
    yet — inputs incomplete); `tools_v5_manifests.py` gains `dag1` (reproduces the dispatched S2/S12 r1 manifest
    exactly, 200/200 jobs).
  - **Where to resume (run 32):** (1) r1 students S2/S12 landed → `python tools_v5_manifests.py dag2 S2 S12` → dispatch
    → later `distill2 S2 S12`. (2) r0 S4/S8 landed → `dag1 S4 S8` → `distill1` → `dag2` → `distill2`. (3) A16 labels
    landed (check all `complete`) → `r0 A16-2` → same chain. (4) Baseline follow-ups landed → `analysis_base_v5.py`
    (check `complete` in every cell; another follow-up via `tools_resume_manifest.py` if not) → commit
    `results/v5/12_base_hstar.json`. (5) G\* val3 complete → students r2 val3 eval → `analysis_d5_v5.py`. test5 stays
    untouched until the freeze commit.

- **Run 32 (2026-11-07, from ≈ 01:50 UTC, scheduled) — stage 13 v5 continued.** No open issues; AUTOPILOT §1 unchanged.
  All run-31 dispatches had finished without failures (last at 22:30 UTC). `add_repo` not available as a tool; the
  existing checkout was moved onto origin/main (the fetch's "forced update" is the same stale-ref artefact as before).
  - **Inputs checked:** r1 students S2/S12 and r0 students S4/S8 all `max_epochs` with `.npz`; A16-2 labels 60/60
    `complete`; G\* val3 S4 / S8 / A16-2 500/500 episodes each (follow-up 1 closed the gap).
  - **Dispatched:** DAgger r2 S2/S12 (`v5_dag2_S2_S12`, 200), DAgger r1 S4/S8 (`v5_dag1_S4_S8`, 200), round-0
    students A16-2 (`v5_r0_A162`, 5), baseline pilot3 follow-up 2 (`v5_base_pilot_f2`, 14 jobs for the 21 missing
    episodes: S2 1, S8 6, S12 2, A16-2 12; H\* not read out yet — S4 is complete, the other cells are not).
  - **E7 decided (addendum v5.1d, before any E7 job):** sandbox timing `g2v3` C1 32 → 15 s, C1 512 → 20 s per belief,
    so the full 512-action screen costs ≈ 1 CPU-h ≪ 60 → full screen, g2v3 beliefs 0–31, S2 and S12, C1 32 and 512
    paired. New opt-in `--indep-M` (default 0; v3/v4 commands unchanged, checked on belief 0) re-values the selected
    and greedy actions on a fresh stream (M 256) to measure the selection bias of V_LA; the sandbox check showed the
    absolute values move with the seed (common to both actions), so the read-out is on gaps. Test added (test_v5 5
    passed). Dispatched `v5_e7_h3` (16 jobs); `code/analysis_e7_v5.py` pre-written.
  - **Code:** `tools_v5_manifests.py val <cell>` writes the D5 read-out manifest (round-2 students, val3 0–499, sub 8,
    20-episode shards, ≤ 125 jobs per cell).
  - **Where to resume (run 33):** (1) DAgger r2 S2/S12 landed (all 200 shards with `.npz`) → `distill2 S2 S12` →
    then `val S2`, `val S12` → `analysis_d5_v5.py`. (2) DAgger r1 S4/S8 landed → `distill1 S4 S8` → `dag2` → `distill2`
    → `val`. (3) A16-2 r0 landed this run (5/5 `max_epochs`, held-out R̄ 0.113–0.118) and `dag1 A16-2` (`v5_dag1_A162`, 100 jobs) is dispatched → when it lands, `distill1 A16-2` → same chain. (4) Baseline f2
    landed → `analysis_base_v5.py` → if every cell `complete`, commit `results/v5/12_base_hstar.json`. (5) E7 landed →
    `analysis_e7_v5.py` → commit `results/v5/12_e7_analysis.json`. (6) Any shard stopped by its time guard →
    `tools_resume_manifest.py`. test5 stays untouched until the freeze commit.

- **Run 33 (2026-11-07, from ≈ 07:50 UTC, scheduled) — stage 13 v5 continued.** No open issues; AUTOPILOT §1 unchanged.
  All run-32 dispatches had finished without failures (last at 03:23 UTC).
  - **Inputs checked:** DAgger r2 S2/S12 and r1 S4/S8/A16-2: 100/100 shards `complete` with `.npz` in every cell.
  - **Dispatched:** `v5_distill2_S2_S12` (10, round-2 students → then D5 val3), `v5_distill1_S4_S8_A162` (15),
    `v5_e7_h3_f1` (11: the S2 C1-512 beliefs the 60-min time guard stopped; one belief per job, 90-min budget).
  - **H\* per cell (pilot3 0–199, sub 8; `results/v5/12_base_hstar.json`, every cell complete):** S2 B-cov 0.445,
    S4 B-fan 0.43, S8 B-cov 0.405, S12 B-fan 0.41, A16-2 B-fan 0.33 (B-spread ≤ 0.075 everywhere). These pick the
    comparator only; the paper's baseline numbers come from test5.
  - **E7 interim (`results/v5/12_e7_analysis.json`, report-only):** S12 complete (C1 512: independent look-ahead gap
    0.042 nats, ci95 [0.025, 0.062]; selection bias −0.002 [−0.016, 0.012]); S2 C1 512 has 21/32 beliefs — the
    follow-up completes it, numbers not final.
  - **E4 tooling:** `code/tools_v5_test5.py` (freeze record with sha256 of every student/RL weight; test5 manifests
    refuse to build unless the cell is frozen and hashes match). RL eval3 path smoke-tested on pilot3 ep 0 (41 s).
  - **Addendum v5.1e (before any test5 job, before any round-2 student exists):** recorded v5 CPU so far ≈ 266 CPU-h;
    test5 sized at ≈ 690 CPU-h for 500 episodes → projected total ≈ 1,250 > 1,000 → frozen reduction order step (2):
    **test5 500 → 300 episodes per cell**; projected ≈ 975 CPU-h; steps (3)/(4) not applied.
  - **Where to resume (run 34):** (1) distill2 S2/S12 landed (10 × `.npz`, `max_epochs`) → `tools_v5_manifests.py val
    S2` and `val S12` → dispatch → `analysis_d5_v5.py` when complete. (2) distill1 S4/S8/A16-2 landed → `dag2 S4 S8
    A16-2` (300 jobs > 256: split per cell or two manifests) → `distill2` → `val`. (3) E7 f1 landed → re-run
    `analysis_e7_v5.py`, commit. (4) A cell's students r2 + RL all present → `tools_v5_test5.py freeze <cell>`, commit
    the freeze and log it here **before** `manifest <cell>` and dispatch (test5 0–299). E5 (sub 16 re-read of test5
    0–199, G\* and student 701, S2/S12) and E6 latency (sandbox) follow. test5 untouched so far.

- **Run 34 (2026-11-07, from ≈ 13:50 UTC, scheduled) — stage 13 v5 continued.** No open issues; AUTOPILOT §1 unchanged.
  All run-33 dispatches had finished without failures (last at 09:18 UTC).
  - **Inputs checked:** round-2 students S2/S12 and round-1 students S4/S8/A16-2: 25/25 `max_epochs` with `.npz`.
  - **E7 complete** (`results/v5/12_e7_analysis.json`, report-only, 32/32 beliefs in every cell × C1): independent
    look-ahead gap at C1 512 — S2 0.066 nats, S12 0.042 nats; paired gap 512 − 32: S2 0.048, S12 0.018. Selection bias of
    V_LA at C1 512: S2 0.022, S12 −0.002 nats. CIs in the JSON.
  - **Dispatched:** `v5_val_S2`, `v5_val_S12` (125 + 125: D5 read-out on val3 0–499), `v5_dag2_S4_S8` (200),
    `v5_dag2_A162` (100).
  - **Order kept from amendment v5.0 l. 87:** D5 on val3 → freeze → test5. The S2/S12 freeze waits for the D5 read-out.
  - **D5 read-out S2 / S12** (`results/v5/12_d5_analysis.json`; val3 0–499 complete after follow-ups `v5_val_S2_f1` /
    `v5_val_S12_f1` for 22 time-guarded shards): **D5 fails in both cells.** S2: Δ_succ(student − G\*) = −3.28 pp (SE
    2.19, threshold −1.45), Δ_BI = −0.068 nats (passes ii), seeds within δ 3/5 (fails iii). S12: Δ_succ = −3.24 pp (SE
    1.96, threshold −1.72), Δ_BI = −0.063 (passes ii), seeds 3/5. Per amendment v5.0, D5 has no remedy step: it is
    reported as H5a ("within δ on validation in m of 5 cells") with the test5 contrasts. No student is retrained.
  - **FREEZE S2, S12** (`results/v5/13_freeze.json`, sha256 of 5 students r2 + 5 RL cfg 6 + 5 rl_success per cell),
    committed in this commit, before any test5 job. test5 manifests (`tools_v5_test5.py manifest`, test5 0–299):
    `v5_test5_S2_p0/p1` (320 jobs), `v5_test5_S12_p0/p1` (349 jobs). Dispatched right after this push.
  - `v5_distill2_S4_S8_A162` (15 round-2 students) dispatched at 16:01 UTC; DAgger r2 S4/S8/A16-2 300/300 complete.
  - **Dispatched (16:26 UTC):** `v5_test5_S2_p0`, `_p1`, `v5_test5_S12_p0`, `_p1` (669 jobs ≈ 15 min each; expect
    ≈ 8–9 h wall with the 20-runner cap, sharing it with distill2).
  - **Where to resume (run 35):** (1) distill2 S4/S8/A16-2 landed (15 × `.npz`, `max_epochs`) → `tools_v5_manifests.py
    val S4` / `val S8` / `val A16-2` → dispatch → follow-ups via `tools_resume_manifest.py` → `analysis_d5_v5.py` →
    then `tools_v5_test5.py freeze <cell>`, commit + log, then `manifest <cell>` → dispatch. (2) test5 S2/S12 landed →
    follow-up manifests for time-guarded shards (`tools_resume_manifest.py` per p0/p1 manifest). (3) When S2/S12 test5
    is complete: E5 (sub 16 re-read of G\* and student 701, test5 0–199) and the test5 read-out script (H5a/H5b/H2-v5,
    student − H\*, Holm) — write it before reading any test5 number. (4) E6 latency in the sandbox once all 25 round-2
    students exist (one session).

- **Run 35 (2026-11-07, from ≈ 19:50 UTC, scheduled) — stage 13 v5 continued.** No open issues; AUTOPILOT §1 unchanged.
  `add_repo` not available as a tool; the existing checkout was reset onto origin/main (the local branch held a stale
  copy of old run-26 commits; nothing of it was pushed). Plan: `plans/stage_13_v5_run35_e6_readout.md`.
  - **Inputs checked:** round-2 students S4 / S8 / A16-2 15/15 `max_epochs` with `.npz` (A16-2 seed 701 kept its
    round-1 init, best epoch 0 — the recipe's best-checkpoint rule, logged). test5 S2/S12 still running (runs 157/159;
    counts only: S2 4,253 / 6,000, S12 3,886 / 6,000 method-episodes at 20:00 UTC).
  - **Dispatched:** `v5_val_S4`, `v5_val_S8`, `v5_val_A162` (125 each: D5 read-out, val3 0–499, sub 8). Freeze of these
    cells waits for D5 (amendment v5.0 order).
  - **Addendum v5.1f** (before any test5 number is read): E6 moves from the sandbox to runners (sandbox full-G\* decision
    ≈ 3.7 s; 25 students × 520 decisions ≈ 27 h ≫ one session) with "same machine" kept per cell job; new opt-in
    `latency3 --configs … --no-pruned` (defaults unchanged, test added); `experiments/v5_e6_lat.json` (10 jobs)
    dispatched. g_T for H2-v5 is cheap (≈ 0.08 s / episode) → sandbox (`code/tools_v5_gt.py` → `results/v5/test5_gt/`).
  - **Read-out code written before any test5 number:** `code/analysis_test5_v5.py` (H5a / H5b / H2-v5 / H\* / Holm;
    H5b weights = 1 / bootstrap variance per cell; synthetic test `tests/test_v5_test5_analysis.py`, 2 passed),
    `code/analysis_e5_v5.py` (sub-16 flip rate), `code/analysis_e6_v5.py` (latency medians, ratio, L_final),
    `code/tools_v5_e5.py` (E5 manifest; refuses until G\* and student 701 have test5 0–199 — S12 G\* still lacks 3).
    Sandbox timing for E5: sub-16 re-read ≈ 45–70 s per episode (val3 record).
  - **Where to resume (run 36):** (1) D5 val3 S4/S8/A16-2 landed → follow-ups via `tools_resume_manifest.py` →
    `analysis_d5_v5.py` → `tools_v5_test5.py freeze <cell>`, commit + log **before** `manifest <cell>` → dispatch.
    (2) test5 S2/S12: follow-up manifests for time-guarded shards; `python tools_v5_e5.py` once 0–199 exist → dispatch.
    (3) `python tools_v5_gt.py` in the sandbox for new test5 files (commit `results/v5/test5_gt/`, never the
    dot-prefixed temp files). (4) E6 landed → `analysis_e6_v5.py`. (5) All cells complete → `analysis_test5_v5.py` →
    stage 14. `analysis_test5_v5.py --check` prints counts only.

- **Run 36 (2026-11-08, from ≈ 01:40 UTC, scheduled) — stage 13 v5 continued.** No open issues; AUTOPILOT §1 unchanged.
  `add_repo` not available as a tool; the sandbox checkout was a shallow stale copy → reset onto origin/main and
  unshallowed (nothing local was lost; the old run-22–26 commits are on origin). All run-35 dispatches had finished
  without failures (last at 00:02 UTC). Plan: `plans/stage_13_v5_run36_followups.md`.
  - **Follow-ups dispatched:** `v5_val_S4_S8_A162_f1` (79 shards: S4 4 / 14 ep, S8 10 / 31 ep, A16-2 65 / 360 ep, all
    time-guarded) and `v5_test5_S2_S12_f1` (141 shards: S2 38 / 369 ep, S12 103 / 651 ep; frozen weights unchanged).
  - **E6 landed** (`results/v5/14_e6_analysis.json`, report-only): all 10 jobs complete (500 decisions each). The v3
    Lat′ completeness rule (CI half-width ≤ 10 % of every median) holds in A16-2 only; in S2/S4/S8/S12 the full-G\*
    decision times are multimodal across steps, so the median CI is wide. Student latency CIs pass everywhere (seed
    medians 0.3–0.5 ms). **Addendum v5.1g:** the existing v3 rule "500 more decisions" applied as one 1,000-decision
    job per cell (same runner keeps job 1's same-machine property) → `v5_e6_lat_d1000` (4 jobs) dispatched;
    `analysis_e6_v5.py` prefers the `_d1000` record when present. No further extension whatever it shows.
  - **g_T** (`tools_v5_gt.py`, sandbox, after `pip install -r code/requirements.txt` — the fresh sandbox lacked
    shapely): 148 new test5 files → `results/v5/test5_gt/` (464 total; not read).
  - **E5** still blocked: `tools_v5_e5.py` reports S12 G\* missing 3 of test5 0–199 (in the follow-up).
  - **D5 read-out S4 / S8** (`results/v5/12_d5_analysis.json`; val3 0–499 complete after the follow-up): **D5 fails in
    both cells.** S4: Δ_succ(student − G\*) = −5.48 pp (SE 2.15, threshold −1.50), Δ_BI = −0.133 nats (passes ii),
    seeds within δ 1/5. S8: Δ_succ = −3.64 pp (SE 2.03, threshold −1.64), Δ_BI = −0.046 (passes ii), seeds 4/5 (passes
    iii; fails i). S2/S12 unchanged. D5 has no remedy step → reported as H5a with the test5 contrasts; no retraining.
    A16-2 val3 still incomplete (422 / 500; 11 follow-up shards running).
  - **FREEZE S4, S8** (`results/v5/13_freeze.json`, sha256 of 5 students r2 + 5 RL cfg 6 per cell), committed in
    df338d3 before any test5 job of these cells.
  - **test5 S4 / S8 dispatched** (02:17 UTC): `v5_test5_S4_p0/p1` (267 jobs), `v5_test5_S8_p0/p1` (300 jobs).
  - **A16-2 val3 follow-up 2** (`experiments/v5_val_A162_f2.json`, 2 shards / 4 episodes of seed 705): the Actions run
    was queued behind ≈ 700 test5 jobs, so it was cancelled before starting and the two identical commands were run in
    the sandbox (only `--budget-minutes` 25 → 50, a time guard that does not touch results; 186 s / 152 s, no early stop).
  - **D5 read-out A16-2** (val3 0–499 complete): **fails** — Δ_succ = −5.96 pp (SE 2.38, threshold −1.23), Δ_BI =
    −0.063 nats (passes ii), seeds within δ 0/5. **H5a on validation: 0 of 5 cells within δ.** No remedy step, no
    retraining (amendment v5.0).
  - **FREEZE A16-2** (`results/v5/13_freeze.json`, 5 students r2 + 5 RL cfg 6), committed before its test5 manifest.
  - **test5 A16-2 dispatched** (≈ 03:05 UTC): `v5_test5_A162_p0/p1` (485 jobs). All 5 cells are now frozen and on test5.
    Queue ≈ 1,200 jobs (S2/S12 f1 141, S4 267, S8 300, A16-2 485, E6 d1000 4) at the 20-runner cap → expect ≈ 15 h
    wall plus follow-ups. No test5 outcome has been read.
  - **Where to resume (run 37):** (1) test5 runs landed → follow-up manifests per cell via `tools_resume_manifest.py`
    (for S2/S12 run it on `v5_test5_S2_S12_f1.json`; for S4/S8/A16-2 on their p0/p1 manifests); combine per wave.
    (2) `python tools_v5_gt.py --workers 4` for new test5 files (needs `pip install -r code/requirements.txt` in a fresh
    sandbox). (3) `python tools_v5_e5.py` once S12 G\* has test5 0–199 → commit + dispatch E5. (4) E6 d1000 landed →
    `analysis_e6_v5.py`, commit. (5) A cell with every method at 300 test5 episodes → `analysis_test5_v5.py --check`,
    then the read-out once all cells are complete → stage 14. If an eval run is queued behind long test5 waves and has
    only a few episodes, running the identical command in the sandbox is fine (log it).

- **Run 37 (2026-11-08, from ≈ 07:50 UTC, scheduled) — stage 13 v5 continued, then paper 2 (AUTOPILOT §7).** No open
  issues; AUTOPILOT §1 unchanged since the 11-08 paper-2 directive. Checkout was shallow → unshallowed and fast-forwarded.
  Plan: `plans/stage_13_v5_run37_followups.md`.
  - **Finished since run 36:** test5 S2/S12 f1 (run 166), S4_p1 (169), S8_p1 (171), E6 d1000 (167). Still running:
    S4_p0 (168), S8_p0 (170), A16-2 p0/p1 (173/174).
  - **Dispatched:** `v5_test5_f2` (42 follow-up shards: S2 14, S12 17, S4 3, S8 8; frozen weights unchanged) and
    `v5_e5_sub16` (56 shards: sub-16 re-read of test5 0–199, G\* and student 701, S2/S12 — `tools_v5_e5.py` passed).
  - **E6 d1000 read-out** (`results/v5/14_e6_analysis.json`, report-only): the 1,000-decision jobs still leave the
    full-G\* median CI > 10 % in S2/S4/S8/S12 (multimodal decision times); student CIs pass everywhere. Per addendum
    v5.1g no further extension; reported as is (full-G\* / student median ratio ≈ 7,000–10,000× in S2/S4).
  - **g_T** (`tools_v5_gt.py`, sandbox): outputs for the test5 files committed so far are in `results/v5/test5_gt/`
    (stopped at the end of the run; temp files removed; the tool resumes on the remaining files). Not read.
  - No test5 outcome read.
  - **Paper 2 this run:** stages 2–9 done (gates 5 and 9 auto-approved, evidence in `papers/p2/PROGRESS.md`), stage 10
    increment 1 (simulator + pilot smoke). WebFetch was unavailable this run (permission prompt unanswered), so the
    RSS CFP re-check is still pending; literature came through the Actions collector.
  - **Where to resume (run 38):** (1) runs 168/170/173/174 (test5 S4_p0, S8_p0, A16-2 p0/p1), 175 (test5 f2), 176
    (E5 sub 16) → follow-up manifests via `tools_resume_manifest.py` on each finished manifest (S4_p0, S8_p0, A162_p0/p1,
    and `v5_test5_f2.json`); (2) `pip install -r code/requirements.txt` then `python code/tools_v5_gt.py --workers 2`
    in the background, commit outputs (never dot-prefixed temps); (3) E5 landed → `analysis_e5_v5.py`, commit;
    (4) all cells complete → `analysis_test5_v5.py --check`, then the read-out → stage 14. Then paper 2 stage 10
    increment 2 (`papers/p2/plans/stage_10_code_generation.md`).

- **Run 38 (2026-11-08, from ≈ 13:50 UTC, scheduled) — stage 13 v5 continued, then paper 2.** No open issues;
  AUTOPILOT §1 unchanged. `add_repo` not available as a tool; the existing checkout was reset onto origin/main and
  unshallowed. Plan: `plans/stage_13_v5_run38_followups.md`.
  - **Finished since run 37 (all `success`):** test5 S4_p0 (168), S8_p0 (170), A16-2 p0/p1 (173/174), f2 (175), E5 (176).
  - **Dispatched:** `v5_test5_f3a` (126: S4 52, S8 45, f2 29) and `v5_test5_f3b` (187: A16-2) — time-guarded /
    missing shards only, frozen weights unchanged; `v5_e5_sub16_f1` (111 jobs / 444 episodes: E5 regrid3 shards stop
    at ≈ 7 of 15 episodes, so the new `code/tools_resume_e5.py` re-runs each shard's `remaining` episodes, 5 per job).
  - **g_T:** 94 more test5 files → `results/v5/test5_gt/` (worker pool stalled late in the run; stopped, temps removed;
    the tool resumes on the rest). Not read.
  - A partial `results/v5/14_e5_analysis.json` written by a completeness check was deleted unread (E5 incomplete:
    S2 G\* 127 / student 95, S12 68 / 66 of 200). No test5 outcome read.
  - **Where to resume (run 39):** (1) f3a / f3b / e5_f1 landed → `tools_resume_manifest.py` on f3a / f3b (and
    `tools_resume_e5.py` on `v5_e5_sub16_f1.json` if any shard stopped) → dispatch; (2) `python code/tools_v5_gt.py
    --workers 2` for new test5 files; (3) E5 complete → `analysis_e5_v5.py`, commit; (4) all cells at 300 →
    `analysis_test5_v5.py --check`, then the read-out → stage 14. Paper 2: the probe design decision, then the freeze.

- **Run 39 (2026-11-08, from ≈ 19:50 UTC, scheduled) — stage 13 v5 continued, then paper 2.** No open issues;
  AUTOPILOT §1 unchanged. `add_repo` not available as a tool; the existing checkout was reset onto origin/main.
  Plan: `plans/stage_13_v5_run39_followups.md`.
  - **Finished since run 38 (all `success`):** f3a (177), e5_f1 (178), f3b (179); p2 timing (180).
  - **Remaining test5 work:** 93 time-guarded shards, almost all the random baseline (≈ 900 episodes over 5 cells;
    ≈ 700 s / episode under sub 8, so a 25-min job finished only ≈ 2 episodes) plus 13 RL A16-2 episodes.
    New `code/tools_split_manifest.py` splits each random shard into 3-episode jobs with `--budget-minutes 60` (a time
    guard only — same precedent as run 36); method, frozen weights and episode indices unchanged.
  - **Dispatched (≈ 20:00 UTC):** `v5_test5_f4a` / `v5_test5_f4b` (166 + 166 jobs) and `v5_e5_sub16_f2` (25 jobs /
    45 episodes). Expected ≈ 9–10 h wall at the 20-runner cap.
  - **g_T:** 121 + 49 more test5 files → `results/v5/test5_gt/` (sandbox; stopped at the end of the run, temps removed;
    the tool resumes on the rest). Not read.
  - No test5 or E5 outcome read (counts only).
  - **Where to resume (run 40):** (1) f4a / f4b / e5_f2 landed → `tools_resume_manifest.py` on f4a / f4b (random
    leftovers → `tools_split_manifest.py` again) and `tools_resume_e5.py` on `v5_e5_sub16_f2.json` → dispatch;
    (2) `python code/tools_v5_gt.py --workers 2`; (3) E5 complete → `analysis_e5_v5.py`; (4) all cells at 300 →
    `analysis_test5_v5.py --check`, then the read-out → stage 14.
  - **Paper 2 this run** (details in `papers/p2/PROGRESS.md`): stage 10 done (amendment 08a implemented, re-pilot,
    pre-registration `papers/p2/docs/08b_preregistration.md` FROZEN), stage 11 done, stage 12 started — 18,600
    main-pool labels; **the pre-registered H1-M design gate failed (8 / 800 non-monotone, limit 7)** → pre-registered
    switch to the conformal-risk-control route (addendum 08c, written before any cal / test statistic); offline fits
    dispatched (`experiments/p2_fit_a010.json`, Actions run 185).

- **Run 40 (2026-11-09, from ≈ 01:50 UTC, scheduled) — stage 13 v5 continued, then paper 2.** No open issues;
  AUTOPILOT §1 unchanged. `add_repo` not available as a tool; the existing checkout was reset onto origin/main.
  Plan: `plans/stage_13_v5_run40_followups.md`.
  - **Finished since run 39 (all `success`):** f4a (182), f4b (183), e5_f2 (181); p2 fits (185).
  - **test5:** 11 time-guarded random-baseline episodes left → `experiments/v5_test5_f5.json` (same commands,
    frozen inputs) dispatched (Actions run 186).
  - **E5 complete → read-out** (`results/v5/14_e5_analysis.json`, report-only, amendment v5.0 E5): sub-8 → sub-16
    success flip rate on test5 0–199: S2 G\* 8.0 % (8 gains / 8 losses), student 701 7.0 %; S12 G\* 7.5 %, student
    6.5 %. Success means move by ≤ 2.5 pp; the student − G\* contrast changes by +2.0 pp (S2) and −3.0 pp (S12).
    So the evaluator grid alone moves a cell's student − G\* contrast by up to ≈ 3 pp — the same size as the D5 gaps
    (3–6 pp); this must sit next to every test5 success contrast.
  - **g_T moved to runners** (operational addendum v5.1h in the run plan): the sandbox pace (≈ 1 file / min, 483 files
    left) would not finish in a run; same `gt3` command, one job per file (`experiments/v5_gt_r0.json` /
    `v5_gt_r1.json`, runs 187 / 188), plus two sandbox-computed files recomputed into `results/v5/test5_gt_check/`.
  - **Stage 14 v5 plan written before any test5 outcome** (`plans/stage_14_result_analysis_v5.md`) and a collector
    `code/tools_results_v5.py`. No test5 outcome read (counts only).
  - **test5 complete** (f5 run 186 landed; g_T: runner jobs + the last 2 files in the sandbox; the 2-file
    runner/sandbox check agrees to 1e-14) → **frozen read-out** `code/analysis_test5_v5.py` (written run 35) →
    `results/v5/14_test5_analysis.json`; collector → `results/v5/results_v5.json`.
    **H5a (test5, 300 episodes, 5 student seeds):** student − G\\* success S2 −2.5 pp [−7.6, 2.7], S4 −2.5 [−8.3, 3.3],
    S8 −1.3 [−6.1, 3.7], S12 −1.5 [−6.3, 3.3], A16-2 −0.2 [−6.3, 6.1]; no Holm rejection in any cell (validation:
    0 / 5 cells within δ, gaps 3–6 pp). **H5b:** slope −2.7 pp per 100° [−18.2, 12.7] → no trend detected over 5 cells.
    **Student vs best heuristic H\\*:** +5.9 (S2, n.s.), +9.8 (S4), +7.1 (S8), +6.1 (S12), +16.8 pp (A16-2), Holm rejects
    in 4 / 5. **Student vs RL (cfg 6) success:** +8.5 (S2), +5.5 (S4, CI touches 0), +3.2 (S8, n.s.), +7.3 (S12),
    +26.6 pp (A16-2). **H2-v5** (g_T student − RL, LB > +0.10): only A16-2 (+0.83, LB 0.60); no inversion anywhere.
    E5 (sub-16) flip rate 6.5–8 % moves the student − G\\* contrast by up to 3 pp — the size of every test5 gap.

## Stage 14. RESULT_ANALYSIS     [v5]

- **Finished:** 2026-11-09 (run 40). Plan `plans/stage_14_result_analysis_v5.md`.
- Pass 1 (fresh subagent, template verbatim, data = unaltered `results/v5/results_v5.json`) → `results/v5/14_analysis_pass1.md`;
  pass 2 (fresh subagent, adversarial area-chair prompt) → `14_analysis_pass2.md` (3 S / 8 M / 8 m; no pre-registered
  verdict wrong); merged `results/v5/14_analysis.md` (pass-2 items binding). Prompts in `results/v5/prompts/`.
- Key binding corrections: the gap is not "small" on validation (S4 −5.5, A16-2 −6.0 pp); test5 does not contradict
  D5; the pilot-chosen H\* is not the best test5 heuristic in 4 / 5 cells (margin over the best test5 heuristic
  +3.5 to +14.5 pp); H5b = "no trend detected", not "no dependence"; latency ratio 2,523× (S12) – 9,933× (S2) on one
  student seed per cell; A16-2's H2-v5 pass is mostly RL collapse (4 / 5 seeds use 2 probes).

## Stage 15. RESEARCH_DECISION     [v5]

- **Finished:** 2026-11-09 (run 40). Fresh subagent, template with the REFINE option verbatim (prompts
  `results/v5/prompts/stage15_*.txt`) → `results/v5/15_decision.md`.
- **Decision: PROCEED to stage 16 as a measurement / characterisation paper only** (same resolution as v4). The
  method-sense PROCEED rule is not met (D5 0 / 5; no contrast vs the strongest per-cell baseline significant), REFINE
  is unavailable (refine cap 4 / 4 used, owner-authorised maximum; D5 has no remedy step), PIVOT not warranted.
  Escalation items filed in `OWNER_TODO.md` (run 40). Target: RSS 2027 Stage 1 extended abstract (12-04 AoE), draft
  ≈ 11-22, in `paper/` by 12-01; the owner submits or not.
- **Next:** stage 16 PAPER_OUTLINE [v5] (`results/v5/15_decision.md` §4 lists the allowed / disallowed claims).
- **Where to resume (run 41):** stage 16 PAPER_OUTLINE [v5] for the RSS Stage 1 extended abstract (≤ 5 pages body),
  from `results/v5/14_analysis.md` + `15_decision.md` §4 (allowed / disallowed claims) with
  `pipeline/references/topic_constraint_block.md`; the v4 condensed draft `paper/mypaper/sections/draft_v4_condensed.md`
  is earlier material only (its numbers are v4). Then paper 2: read `p2_crc_v2` (Actions) via
  `python papers/p2/code/analysis_crc.py --v2` once `--check`-complete, then H4 / D-μ / H2-T / H3-B secondaries → stage 14.

- **Run 41 (2026-11-09, from ≈ 07:50 UTC, scheduled) — paper 2 read-out, then stage 16 v5.** No open issues;
  AUTOPILOT §1 unchanged. `add_repo` not available as a tool; the existing checkout was reset onto origin/main.
  - **Paper 2 first** (AUTOPILOT §7; paper 1 had nothing on Actions): 08e CRC grid sensitivity read
    (`papers/p2/results/v1/crc_analysis_v2.json`; details in `papers/p2/PROGRESS.md`).
  - **Stage 15 §4.1 task 1 (report-only):** `code/tools_posthoc_v5.py` → `results/v5/15_posthoc_derived.json`
    (arithmetic on existing fields, no CI), collected into `results_v5.json`. Margins vs the best test5 heuristic:
    S2 +5.87, S4 +5.13, S8 +6.07, S12 +3.47, A16-2 +14.47 pp; full-G\* / job-2 student latency ratios S12 ≈ 2,083–2,150×,
    S8 ≈ 3,356–3,397×, A16-2 ≈ 6,640–6,688×, S4 ≈ 8,060–8,123×, S2 ≈ 9,521–9,569×; H5b span 0.1112–0.8213 rad →
    slope × span −1.1 pp, CI [−7.4, +5.2] pp. Task 2 (OWNER_TODO correction) was already done in run 40.

## Stage 16. PAPER_OUTLINE     [v5]

- **Finished:** 2026-11-09 (run 41). Plan `plans/stage_16_paper_outline_v5.md`.
- Template `paper_outline.md` verbatim; fresh-context subagent (opus); prompts `paper/mypaper/prompts/stage16_v5_*.txt`
  (builder `build_stage16_v5.py`; feedback = v4 stage-18 review + v4 stage-20 gate). v4 outline snapshotted to
  `paper/mypaper/v4/00_outline_v4.md`.
- **Output:** `paper/mypaper/sections/00_outline.md` (≈ 7,700 words; body target 3,430 words for the 5-page Stage 1
  abstract; C1–C5 in the decision's order; Table 1 / Table 2 / X1–X10 row map with JSON keys and DEC/GATE/REP/EXPL/PH/PRIOR
  tags; Figure 1 = schematic panels A–C + data panel D, student − G\* vs G\* travel over the five cells). 33 cite_keys,
  all present in `docs/05_knowledge_cards.json`; 3 [CITE-MISSING] (DeepSets, Holm 1979, Efron bootstrap); 12 [NEED]
  (design constants / records not in the analysis JSON — to be filled in stage 17 from the frozen amendments or dropped).
- **Erratum to binding stage-14 item m8 (main-session check):** m8 says v4's −10.2 pp test3 gap has no interval; it does
  (`results/v4/results_v4.json` → `14_s2_analysis.json.test3_sub8.diffs["student-gstar:success"]` = −0.1022,
  ci95 [−0.1656, −0.0433]). Approved wording keeps m8's scope (no formal comparison claim) and adds the interval.
- **Open for stage 17** (flagged by the outline subagent): amendment v5.1c requires per-seed `rl_success` episode counts
  next to every `rl_success` number; amendment v5.0 E2 pre-declared a last-checkpoint sensitivity row for students —
  neither is in `results_v5.json` yet (report-only extraction from existing files, no new runs); no claim scope exists
  for a latency–accuracy frontier → only reduced-planner timings are reported.
- **Report-only extractions done (same run):** `code/tools_report_rows_v5.py` → `results/v5/16_report_rows.json`
  (collected into `results_v5.json`): `rl_success` training episodes per seed (S2 711–715: 123,392 / 124,672 /
  181,760 / 200,192 / 125,440; S12: 184,576 / 113,408 / 111,104 / 162,304 / 165,888; 9 / 10 time-guard stops — matches
  addendum v5.1c) and the E2 last-checkpoint sensitivity row (held-out label regret R̄ of the kept vs last-epoch
  checkpoint, every cell / seed / round; the last-epoch R̄ is higher in every one of the 75 rows). No success
  evaluation of last checkpoints exists and none is run.
- **Where to resume (run 42):** stage 17 PAPER_DRAFT [v5] (template `paper_draft.md`, fresh subagent, outline +
  `results_v5.json` + knowledge cards). Paper 2: remaining secondaries →
  stage 13/14.

## Stage 17. PAPER_DRAFT     [v5]

- **Finished:** 2026-11-09 (run 41). Plan `plans/stage_17_paper_draft_v5.md`.
- Template `paper_draft.md` verbatim (system + user extracted by `paper/mypaper/prompts/build_stage17_v5.py`); fresh
  opus subagent; v5 / v4 / v3 results JSONs pasted in full, 60 cite_keys, outline, v4 final draft as wording source.
- **Output:** `paper/mypaper/sections/draft_v5.md` (master draft; main body ≈ 6,785 prose words, all RESTRICTS floors met,
  above the 4,300–5,000 aim → Method / Experiments are the first cuts in stage 22), `paper/mypaper/figures/figure1_prompt.txt`
  (panels A–C schematic, panel D data plot spec).
- **Checks (main session):** `code/tools_number_audit.py` now also loads `results_v5.json` (one added block); against
  v5 + v4 + v3 JSONs and amendments v5.0 / v5.1 → 2 unmatched decimals, both mantissas of scientific-notation RL
  hyperparameters (ent 9.504e-4, critic lr 4.925e-4), verified against `results/v5/rl/*.json` config → 0 unsourced
  numbers. 33 cite_keys, all in `docs/05_knowledge_cards.json`. Never-write list grep: only negated / qualified uses.
  Markers left: 14 [NEED] in the body (design constants not in any results field: action grid, cost-formula source,
  A16 identity count / keep range, `g2000_512_64` meaning, label / DAgger / epoch budgets, cfg-6 RL episodes per seed,
  D5 clause-1 floor and per-seed count, bootstrap resample count) and 3 [CITE-MISSING] (DeepSets, Holm, Efron).
- **[NEED] markers filled (same run, 0 left):** values from amendment v5.0 (D5 clause floor −2 pp and ≥ 4 / 5 seeds,
  label / DAgger / epoch budgets, A16 K = 16 and keep range [0.30, 0.90]), code constants (`travel.py` 64 × 8 action
  grid, cost formula; `geometry.py` 100 mm start radius; `distill.py` ρ = 0.05, Adam; `latency3.py` gN_C_M naming;
  `analysis_test5_v5.py` 10,000 resamples) and run logs, the latter now extracted into `16_report_rows.json`
  (cfg-6 RL: every run reached the 2 × 10⁵-episode cap, 200,192 logged, clip 0.2, 4 epochs; student distill config
  identical in all 75 runs; training episodes 2,700 / 3,500 / 4,300 per round). Number audit: still only the two
  scientific-notation mantissas.
- **Where to resume (run 42):** stage 18 PEER_REVIEW [v5] (two independent runs, fresh
  subagents, evidence audit). Paper 2: remaining secondaries → stage 13/14.

## Stage 18. PEER_REVIEW     [v5]

- **Finished:** 2026-11-09 (run 41). Plan `plans/stage_18_peer_review_v5.md`; template `peer_review.md` verbatim
  (builder `paper/mypaper/prompts/build_stage18_v5.py`); two fresh opus subagents (run 2 as an RSS / CoRL pair).
- **Scores:** run 1 A 4 / B 3; run 2 A 4 / B 5 (mean 4.0). **CRITICAL_FABRICATION: no** in both (40 + 38 spot-checks;
  test5 contrasts and G\* means recomputed from raw episode files, exact; 60 weight hashes match).
- **Must-fix (merged record `paper/mypaper/18_peer_review.md`):** E7 mis-described (it is look-ahead headroom over greedy
  and that screen's selection bias, not G\*'s own value noise — verified in `code/analysis_e7_v5.py`); H5b weights are
  test5-derived (only the rule was fixed); "D5 on test5 fails in ~4 / 5" is approximate post hoc, exception A16-2;
  inversion-rule paraphrase; unstated deviations (E6 frontier not produced, reduction-order history, latency B = 2,000,
  RL sweep seed 719, rl_success time-guard stops, A16 description); 3 [CITE-MISSING].
- **Decision:** PROCEED → stage 19 PAPER_REVISION [v5].
- **Where to resume (run 42):** stage 19 [v5] (template `paper_revision.md`, fresh subagent, draft_v5 + merged review;
  length-protected; then a second review/revision pass as in v4), then stage 20 QUALITY_GATE. Paper 2: remaining
  secondaries → stage 13/14.

## Stage 19. PAPER_REVISION     [v5] — pass 1

- **Finished:** 2026-11-09 (run 41). Plan `plans/stage_19_paper_revision_v5.md`; snapshot before revision
  `paper/mypaper/v5/draft_v5_stage17.md`, after `v5/draft_v5_stage19pass1.md`. Template `paper_revision.md` verbatim
  (builder `build_stage19_v5.py`; reviews = merged record + both reviews + binding block), fresh opus subagent, targeted edits.
- All merged items 1–7 and S1–S6 addressed: E7 rewritten as report-only look-ahead headroom over greedy (S2 +0.0658
  [0.0297, 0.1084], S12 +0.04216 [0.02503, 0.06138] nats at C1 = 512) in §4 / §5.1 / §6 / Limitation 2; H5b weights
  test5-derived; D5-on-test5 sentence labelled post hoc approximate with A16-2 named; inversion rule exact; new
  "Deviations from the registration" paragraph (reduction-order history, E6 frontier not produced, E5 coverage,
  rl_success time-guard stops); latency B = 2,000; sweep seed 719; A16 described; DAgger R̄ report-only paragraph.
- Words: file 9,943 → 12,191 (+22.6 %); no section shorter; Conclusion now ≥ 200. Number audit: 2 unmatched (the known
  scientific-notation mantissas). [CITE-MISSING] ×3 kept.
- Substantive rewrites (E7, deviations) → **second stage-18 pass** (as in v4) before stage 20.
- **Where to resume (run 42):** stage 18 pass 2 [v5] on `draft_v5.md` (two fresh subagents, same template/evidence;
  builder `build_stage18_v5.py`, outputs `18_review_v5_pass2_run{1,2}.md`), then stage 19 pass 2, then stage 20.

## Stage 18. PEER_REVIEW     [v5] — pass 2

- **Finished:** 2026-11-09 (run 41) on `v5/draft_v5_stage19pass1.md`; same template / evidence (prompt
  `stage18_v5_pass2_user.txt`); two fresh opus subagents. Scores: run 1 A 4 / B 3; run 2 A 3 / B 4 (mean 3.5).
  **CRITICAL_FABRICATION: no** (45 + 40 spot-checks).
- Merged record `paper/mypaper/18_peer_review_v5_pass2.md` (P1–P8). Main one, verified: the reduced-G\* accuracy side
  of the frontier exists for S12 (v4 E5 rows, designated by addendum v5.1f) — the draft wrongly called it unevaluated.
  Also: RL-sweep validation-stream size, one-directional inversion check, latency spread is a between-job difference,
  label re-use and A16 ⊃ v3 set A disclosures.
- New report-only row computed by the pipeline: `code/tools_lat_agreement_v5.py` → `results/v5/19_lat_agreement.json`
  (action agreement with full G\* on the E6 states; student 0.182–0.513 vs reduced G\* 0.072–0.312; caveat: G\* is
  sampled, self-agreement not measured, agreement ≠ accuracy).
- **Next:** stage 19 pass 2 (prompt `stage19_v5_pass2_user.txt`), then stage 20.

## Stage 19. PAPER_REVISION     [v5] — pass 2

- **Finished:** 2026-11-09 (run 41). Prompt `stage19_v5_pass2_user.txt` (builder `build_stage19_v5.py --pass2`), fresh
  opus subagent, targeted edits for P1–P8. Snapshot after: `paper/mypaper/v5/draft_v5_stage19pass2.md`.
- P1: S12 reduced-G\* PRIOR accuracy rows from `v4:14_e5_analysis.json` (g125_512_16 −0.06667 [−0.12, −0.01],
  g500_512_4 −0.05 [−0.11, +0.01333] vs G\*, 300 episodes) + Table 4b; P2–P6 wording / disclosures; P7 action-agreement
  rows with caveat; P8 S2 PRIOR comparison (v4 last-checkpoint recipe confirmed in `docs/07c_amendment_v4_0.md` l.20).
  Main session reverted a reviewer-derived "≈ 25 %" to the analysis's binding "about 24 %".
- Words ≈ 13,700 (file), no section shorter; number audit 2 unmatched (known mantissas); 33 cite keys all in cards.
- Note: `code/analysis_rl_sweep_v5.py` docstring says the last validation was at 40,960 episodes, the JSON says 92,160;
  the JSON (code output) is used; docstring left as is (no code change without re-run).
- **Next:** stage 20 QUALITY_GATE [v5].

## Stage 20. QUALITY_GATE     [v5]

- **Finished:** 2026-11-09 (run 41). Plan `plans/stage_20_quality_gate_v5.md`; template `quality_gate.md` verbatim
  (threshold 7.5), fresh opus subagent, paper only → `paper/mypaper/20_quality_gate.json`.
- **Score 5.5 / 10 (v3 5.5, v4 5.0) → FAIL. Not auto-approved** (AUTOPILOT §1 auto-approves a gate only with evidence; a
  score below threshold is no such evidence). 15 weaknesses (8 evidence-level) and 13 required actions (8
  evidence-level: reduced G\* accuracy on test5 in all cells + frontier, more test5 power / TOST, a second G\* run per
  cell, per-cell RL tuning, DAgger-vs-BC on success, E5 in all cells / seeds, an information-based heuristic, A16 at more κ).
  The gate found the numbers internally consistent.
- **Decision (template table):** below threshold with evidence-level weaknesses → stage 13, which is unavailable
  (`max_refine_cycles` 4 / 4, owner-authorised maximum; 15_decision §4.5 d). → **Stop the loop and ask the owner**
  (OWNER_TODO, run 41): RSS Stage 2 full paper / CoRL 2027 / RA-L / workshop, or a further RESTRICTS override.
- **Meanwhile (low-risk, paper-level only, no new experiments):** resolve the 3 [CITE-MISSING] with verified entries,
  render Figure 1 panel D from `results_v5.json`, rewrite internal identifiers for an external reader, gate-calibration
  paragraph. These do not change any number or verdict.
- **Where to resume (run 42):** read AUTOPILOT §1 / issues for the owner's choice. Without one: the paper-level items
  above on `draft_v5.md`, then paper 2 (remaining secondaries → stage 13/14), which has its own cap and is the active
  research thread.

## Run 43 (2026-11-09) — paper 1 check

- No open issues and no new owner directive in AUTOPILOT §1 → paper 1 stays stopped at the v5 stage-20 decision
  (OWNER_TODO run 41). No paper-1 files changed this run; the run went to paper 2 (stages 16–20, loop to v2 stage 13).
- Note: on this run's start the local clone's main had diverged from origin/main (origin had been force-updated
  before this run); the run reset its local copy to origin/main and pushed only fast-forward commits.
- **Where to resume (run 44):** paper 1 — owner decision; meanwhile the low-risk items (3 [CITE-MISSING], Figure 1
  panel D, internal identifiers). Paper 2 — `papers/p2/PROGRESS.md` (v2 stage 13: B3 pilot, then 14–20).

## LOOP MARKER — REFINE from stage 20 → stage 13     [version v5 → v6]

- **Reason:** stage 20 [v5] 5.5 / 10 < 7.5 with evidence-level required actions (`paper/mypaper/v5/20_quality_gate.json`).
  The refine cap was used (4 / 4); on 2026-11-10 the owner chose, in chat, to open v6 for new experiments ("开 v6") and
  raised `max_refine_cycles` to 5 (AUTOPILOT §1, RESTRICTS.yaml, OWNER_TODO). Refine cycle 5.
- **Snapshot taken:** `results/v5/` stays as is (v6 writes to `results/v6/`); paper → `paper/mypaper/v5/`
  (`draft_v5_final.md`, `00_outline_v5.md`, `18_peer_review.md`, `20_quality_gate.json`, plus the stage-17/19 drafts).
- **Design (written before any v6 run):** `docs/07c_amendment_v6_0.md` — E8 test5 300–499 (fresh), E9 reduced G\* on
  test5 0–499, E10 second G\* run (`eval3 --run-salt`, new opt-in flag, default reproduces v5 exactly:
  `code/tests/test_v6.py`, 2 passed; `test_v5.py` + `test_v3_streams.py` 10 passed), E11 round-0 (BC) students, E12
  sub-16 check in all cells; rules H6a (student vs G\* with both G\* runs, difference + TOST at 4 pp, Holm), H6b
  (student vs reduced planners, Holm over 10), H6c (r2 vs r0, Holm over 5). ≈ 645 CPU-h estimate; P6 timing pilot and
  a frozen reduction order before the main dispatch.
- **Next stage:** 13 ITERATIVE_REFINE [v6] (P6 pilot → addendum v6.1 → dispatch).
- **Resuming under version:** v6

## Stage 13. ITERATIVE_REFINE     [v6]

- **Started:** 2026-11-10 (owner's chat session, right after the owner chose v6). Plan
  `plans/stage_13_v6_p6_and_dispatch.md`.
- **P6 timing pilot** (Actions run 193, `results/v6/p6/`, pilot3 only) → addendum v6.1 in `docs/07c_amendment_v6_0.md`:
  ≈ 733 CPU-h ≤ 800, no reduction. Read-out code `code/analysis_v6.py` + `code/tests/test_analysis_v6.py` (2 passed)
  committed before any E8–E12 record existed.
- **Manifests** (`code/tools_v6_manifests.py`): E8 `v6_e8_p0–p4` (1,169 jobs), E9 `v6_e9_p0` (250), E10 `v6_e10_p0` (125),
  E11 `v6_e11_p0–p2` (590), E12 `v6_e12_p0–p2` (650).
- **Wave 1 dispatched (2026-11-10 ≈ 02:10 UTC):** `v6_e9_p0`, `v6_e10_p0`, `v6_e8_p0` (625 jobs, ≈ 9 h at 20 runners).
- **Where to resume (next run):** when wave 1 has finished, (1) `python code/tools_resume_manifest.py
  experiments/<m>.json experiments/<m>_f1.json "<purpose>"` for each finished manifest (time-guard stops / failures)
  and dispatch the follow-ups; (2) dispatch the next wave in this order, keeping ≤ ~650 queued jobs (GitHub drops jobs
  queued > 24 h; paper 2 shares the runners): `v6_e8_p1`, `v6_e8_p2`, `v6_e8_p3`, `v6_e8_p4`, then `v6_e11_p0–p2`,
  then `v6_e12_p0–p2`; (3) g_T: one `gt3` job per new `results/v6/test5/` file of G\*, students, RL, rl_success
  (same command as `experiments/v5_gt_r0.json`, outputs `results/v6/test5_gt/`); (4) `python code/analysis_v6.py --check`
  (counts only) until complete, then the read-out → stage 14 [v6]. Do not read any v6 outcome before `--check` is complete.

## Run 45 (2026-11-10, ≈ 07:50 UTC) — stage 13 [v6] wave 2 dispatch

- Wave 1 finished (Actions runs 194 E9, 195 E10, 196 E8; run 194 marked failure: one job left no output,
  `A16_k2_g125_512_16_168`). `--check` counts only, no outcome read.
- Follow-ups (`code/tools_resume_manifest.py`): `v6_e9_p0_f1` (96 jobs: 95 time-guard resumes + the missing one),
  `v6_e10_p0_f1` (13), `v6_e8_p0_f1` (33). Dispatched with `v6_e8_p1`, `v6_e8_p2` → 642 jobs queued (≤ 650 rule).
- **Where to resume:** when these finish: follow-ups for `v6_e8_p1/p2` (and `_f2` for the `_f1` manifests if any
  stop again), then `v6_e8_p3`, `v6_e8_p4`, `v6_e11_p0–p2`, `v6_e12_p0–p2` in ≤ 650-job waves; then g_T (`gt3`)
  jobs; then `analysis_v6.py --check` until complete → read-out → stage 14 [v6].
- (run 45, 09:35 UTC) `v6_e10_p0_f1` complete (0 left); `v6_e8_p0_f1` left 2 time-guard stops → `v6_e8_p0_f2` (2 jobs)
  dispatched. `v6_e9_p0_f1`, `v6_e8_p1`, `v6_e8_p2` still queued / running.

## Run 46 (2026-11-10, ≈ 14:00 UTC) — stage 13 [v6] wave 3 dispatch

- Wave 2 finished (Actions runs 197–202, all success; runners idle since ≈ 11:45 UTC). `--check` counts only, no outcome read.
- Follow-ups (`tools_resume_manifest.py`): `v6_e9_p0_f2` (4), `v6_e8_p1_f1` (33), `v6_e8_p2_f1` (33); `v6_e8_p0_f2` and
  `v6_e10_p0_f1` left 0 → E10 and E8 p0 complete.
- **Wave 3 dispatched:** the three follow-ups + `v6_e8_p3` (250) + `v6_e8_p4` (169) + `v6_e11_p0` (250) = 739 jobs.
  Decision: slightly above the ≈ 650 guideline, because wave 2 (642 jobs) cleared in < 4 h, so 739 is far from GitHub's
  24 h queue limit, and without `e11_p0` the runners would sit idle ≈ 3 h before the next scheduled run. Paper 2 is
  currently sandbox-only (no queued paper-2 jobs).
- g_T: `code/tools_v6_gt.py` (copy of `tools_v5_gt.py` with v6 paths; gt3 ≈ 1–2 s per file) runs in the sandbox on
  committed v6 test5 files of G\*, students, RL, rl_success → `results/v6/test5_gt/`; re-run it each run for new files.
- **Where to resume:** when wave 3 finishes: follow-ups for `v6_e8_p3`, `v6_e8_p4`, `v6_e11_p0` (and `_f3` / `_f2` for
  the follow-up manifests if any stop again), then `v6_e11_p1`, `v6_e11_p2`, `v6_e12_p0–p2`; `tools_v6_gt.py` for new
  files; then `analysis_v6.py --check` until complete → read-out → stage 14 [v6].
- (run 46, ≈ 15:45 UTC) `v6_e9_p0_f2`, `v6_e8_p1_f1`, `v6_e8_p2_f1` complete (0 left) → **E9, E10, E8 p0–p2
  complete**. `v6_e8_p3`, `v6_e8_p4`, `v6_e11_p0` running. g_T: `tools_v6_gt.py` ran in the sandbox on all v6 test5
  files committed before ≈ 14:00 (533+ outputs committed; files landing later need a re-run). Paper 2's 80 v4 replay
  jobs were dispatched behind these.

## Run 47 (2026-11-10, ≈ 19:50 UTC) — stage 13 [v6] wave 4 dispatch

- Wave 3 finished (Actions runs 203–208, all success; paper 2's v4 runs 209–211 also done; runners idle).
  `--check` counts only, no outcome read.
- Follow-ups (`tools_resume_manifest.py`): `v6_e8_p3_f1` (27), `v6_e8_p4_f1` (12), `v6_e11_p0_f1` (36).
- **Wave 4 dispatched:** the three follow-ups + `v6_e11_p1` (250) + `v6_e11_p2` (90) + `v6_e12_p0` (250) = 665 jobs
  (≈ the 650 guideline; `v6_e12_p1`, `v6_e12_p2` held for the next wave).
- g_T: `tools_v6_gt.py` on all newly committed test5 files → 886 outputs in `results/v6/test5_gt/`.
- `--check` now: test5 0–499 rows S2 10,972 / 13,500, S4 8,466 / 11,000, S8 8,485 / 11,000, S12 12,430 / 13,500,
  A16-2 10,924 / 11,000 (rest = E11 students, in this wave); E12 started (S2 / S12 gstar + s701 100 each).
- **Where to resume:** when wave 4 finishes: follow-ups for `v6_e11_p1`, `v6_e11_p2`, `v6_e12_p0` and `_f2` for the
  three `_f1` manifests; then `v6_e12_p1`, `v6_e12_p2`; `tools_v6_gt.py` for new files; `analysis_v6.py --check`
  until complete → read-out → stage 14 [v6].

## Run 48 (2026-11-12, ≈ 14:00 UTC) — stage 13 [v6] wave 5 dispatch

- No open issues, no new owner directive. Wave 4 (Actions runs 212–217) finished 2026-11-11 01:48 UTC, all success;
  the runners then sat idle ≈ 36 h (no scheduled run between run 47 and this one). `--check` counts only, no outcome read.
- Follow-ups: `v6_e11_p1_f1` (35), `v6_e11_p2_f1` (10); `v6_e8_p3_f1`, `v6_e8_p4_f1`, `v6_e11_p0_f1` left 0 → **E8 and
  E11 p0 complete**. E12 p0: 118 / 250 regrid3 jobs stopped at the 25-min guard (≈ 2.9 of 4 episodes per job); new
  helper `code/tools_resume_regrid.py` (same command, `--episodes` = the guard's `remaining`, `--out …_r<first>`) →
  `v6_e12_p0_f1` (118). Plan `plans/stage_13_v6_wave5.md`.
- **Wave 5 dispatched:** the three follow-ups + `v6_e12_p1` (250) + `v6_e12_p2` (150) = 563 jobs.
- g_T: `tools_v6_gt.py` on 32 new test5 files → 918 outputs.
- `--check`: test5 0–499 S2 13,409 / 13,500, S4 10,916 / 11,000, S8 10,920 / 11,000, S12 13,467 / 13,500, A16-2
  11,000 / 11,000; E12 S12 / A16-2 partial, S4 / S8 not started (p1 / p2), S2 students 702–705 not started.
- **Where to resume:** when wave 5 finishes: `tools_resume_manifest.py` for the two E11 `_f1` manifests (→ `_f2`),
  `tools_resume_regrid.py` for `v6_e12_p0_f1` (→ `_f2`), `v6_e12_p1`, `v6_e12_p2` (→ `_f1`); `tools_v6_gt.py`;
  `analysis_v6.py --check` until complete → read-out → stage 14 [v6].
- (run 48, ≈ 14:45 UTC) `v6_e11_p1_f1`, `v6_e11_p2_f1` finished (runs 218–219); `v6_e11_p2_f1` left 0, `v6_e11_p1_f1`
  left 1 time-guard stop (4 episodes) → `v6_e11_p1_f2` (1 job) dispatched. **test5 0–499 complete in every cell except
  S4 (10,996 / 11,000, the 4 episodes above); g_T complete.** E12 waves (`v6_e12_p0_f1`, `p1`, `p2`) running.
- Paper 2 this run: stages 18 → 19 → 18 / 19 pass 2 → 20 [v4]; gate 6.5 / 10 FAIL, refine cap 3 / 3 → owner decision
  (`papers/p2/PROGRESS.md`, `papers/p2/OWNER_TODO.md`).
- **Where to resume (run 49):** paper 1 as in the run-48 entry above (E12 follow-ups via `tools_resume_regrid.py`, then
  `--check` → read-out → stage 14 [v6]); paper 2 waits for the owner (meanwhile paper-level text only).

## Run 49 (2026-11-12, ≈ 19:50 UTC) — stage 13 [v6] wave 6 dispatch

- No open issues, no new owner directive. Wave 5 done except one `v6_e12_p1` job stuck ≈ 2 h in one episode → run 221
  cancelled so its partial output (2 / 4 episodes) was committed. `v6_e11_p1_f2` left 0 → **E8–E11 complete**; g_T
  complete (`tools_v6_gt.py`: 0 new files). Counts only, no outcome read. Plan `plans/stage_13_v6_wave6.md`.
- **Wave 6 dispatched:** `v6_e12_p0_f2` (20), `v6_e12_p1_f1` (32), `v6_e12_p2_f1` (26) = 78 regrid3 jobs.
- **Where to resume:** when wave 6 finishes: `tools_resume_regrid.py` on the three manifests (→ `_f3` / `_f2`) until
  0 left; `analysis_v6.py --check` complete → read-out → stage 14 [v6]. Paper 2 waits for the owner.
- (run 49, ≈ 21:00 UTC) Wave 6 mostly landed: E12 now 100 / 100 in S12 and for G\* in every cell; 11 student episodes
  left in 6 jobs (S2 s702 ep 85–87, S4 s702 / s705 ep 93+, S8 s703 / s705, A16-2 s702 ep 99), some still running in
  Actions runs 224 / 225 (long single episodes). **Where to resume (run 50):** once runs 224–226 are complete,
  `tools_resume_regrid.py` on `v6_e12_p0_f2`, `v6_e12_p1_f1`, `v6_e12_p2_f1` (→ `_f3`, `_f2`, `_f2`) and dispatch;
  when `--check` shows E12 100 everywhere → `python code/analysis_v6.py` read-out → stage 14 [v6] (fresh subagent).

## Run 50 (2026-11-13, ≈ 00:00–03:00 UTC) — stage 13 [v6] complete → stage 14 [v6]

- No open issues, no new owner directive. Wave 6 (runs 224–226) all success; last 9 E12 episodes re-run one episode per
  job (`v6_e12_p0_f3`, `v6_e12_p1_f2`, `v6_e12_p2_f2`; job split only, no setting changed; plan
  `plans/stage_13_v6_wave7.md`). `--check` complete: test5 0–499 + g_T + E12 100 / 100 in every cell. **Stage 13 [v6]
  done.**

## Stage 14. RESULT_ANALYSIS     [v6]

- **Finished:** 2026-11-13 (run 50). Plan `plans/stage_14_result_analysis_v6.md` (written before the read-out).
- Frozen read-out `code/analysis_v6.py` → `results/v6/14_v6_analysis.json` (committed unaltered).
- Pass 1 (fresh opus subagent, template verbatim, data = amendment v6.0 rules + unaltered JSON) →
  `results/v6/14_analysis_pass1.md`; pass 2 (fresh opus subagent, adversarial area-chair prompt) →
  `14_analysis_pass2.md` (2 S / 11 M / 8 m; no pre-registered verdict misreported); merged `results/v6/14_analysis.md`
  (binding summary + pass-1 body + pass 2 as binding appendix). Prompts in `results/v6/prompts/`.
- **Pre-registered results:** H6a — no difference and no equivalence within 4 pp in any cell or window; student point
  estimate 0.3–3.7 pp below G\* (both G\* runs) in all 5 cells on 0–499; S4 ci90 entirely below 0. H6b — student beats
  g125_512_16 in 5 / 5 cells and g500_512_4 in S4 / A16-2 (7 / 10 Holm on 0–499; 2 / 10 on fresh 300–499), 62–389×
  faster. H6c — DAgger vs BC: no difference detected. E12 (report-only): sub 8 → 16 flips 4–13 % of S-cell outcomes and
  moves student − G\* by ≈ 4 pp or more in 3 / 4 S cells.
- **Next:** stage 15 [v6] (fresh subagent; refine cap 5 / 5 used).

## Stage 15. RESEARCH_DECISION     [v6]

- **Finished:** 2026-11-13 (run 50). Plan `plans/stage_15_research_decision_v6.md`; template with REFINE augmentation
  verbatim (`results/v6/prompts/stage15_*.txt`), fresh opus subagent → `results/v6/15_decision.md`.
- **Decision: PROCEED → stage 16, as a pre-registered measurement paper with one narrow positive claim (H6b frontier:
  student vs reduced planners, Holm-qualified per planner and cell).** Not a parity or method paper: H6a shows neither
  difference nor equivalence; H6c licenses no "effective component"; against the strongest non-oracle comparator the
  student clears the registered bar only in A16-2. REFINE / PIVOT not executable (refine cap 5 / 5) and not recommended
  before Stage 1. §4.4 / §4.5 list exactly what the paper may / may not claim.
- §4.1 derived values: `code/tools_results_v6.py` → `results/v6/15_derived_v6.json` (arithmetic on the read-out only,
  not pre-registered, no CI); reproduces the decision's margins (+3.68 / +4.16 / +2.56 / +2.44 / +10.92 pp vs the
  strongest comparator) and latency ratios (G\* 2,544–9,767×; reduced planners 62–389× slower than the student).
- Gate note: stage 15 is not an owner gate; no gate was auto-approved this run.
- **Next:** stage 16 PAPER_OUTLINE [v6] (RSS 2027 Stage 1 extended abstract, 5 pages body); stage 20 by 12-01 or the
  target becomes Stage 2 / CoRL 2027 (owner directive 2026-11-10).

## Stage 16. PAPER_OUTLINE     [v6]

- **Finished:** 2026-11-13 (run 50). Plan `plans/stage_16_paper_outline_v6.md`; template verbatim via
  `paper/mypaper/prompts/build_stage16_v6.py`, fresh opus subagent → `paper/mypaper/sections/00_outline.md`
  (v5 outline kept at `paper/mypaper/v5/00_outline_v5.md`).
- RSS Stage 1 frame (≈ 3,350 body words, Figure 1 = schematic + five accuracy–log-latency small multiples, Table 1 H6a
  both windows, Table 2 H6b with Holm flags, H6c rows); contribution order C1 frontier (H6b), C2 parity not established
  (H6a), C3 DAgger ≈ BC not detected (H6c), C4 evaluator / teacher note. Every row mapped to keys of
  `results/v6/14_v6_analysis.json`, `15_derived_v6.json` (post hoc, no CI) or `results_v5.json`.
- Self-check: `code/tools_number_audit.py` (now also reads the v6 read-out and derived JSON) on the outline with only
  the amendment as design doc → **0 unmatched**; no §4.5 disallowed claim. Open: 3 [CITE-MISSING] (DeepSets, Holm,
  bootstrap) for stage 23.
- **Next:** stage 17 PAPER_DRAFT [v6].

## Stage 17. PAPER_DRAFT     [v6]

- **Finished:** 2026-11-13 (run 50). Plan `plans/stage_17_paper_draft_v6.md`; template verbatim via
  `paper/mypaper/prompts/build_stage17_v6.py`, fresh opus subagent → `paper/mypaper/sections/draft_v6.md`
  (Figure 1 prompt with JSON keys per data panel; Tables 1 H6a, 2 H6b, 3 H6c; ≈ 7,700 body words incl. tables, abstract
  246 → condensed to 5 pages in stage 22).
- Checks: number audit 0 unmatched (design doc = amendment v6.0 only); 29 cite keys used, all in the 60 cards;
  3 [CITE-MISSING] (DeepSets, Holm, bootstrap) left for stage 23; no §4.5 disallowed claim found by grep.
- **Next:** stage 18 PEER_REVIEW [v6] (two fresh reviewers, two passes).

## Stage 18. PEER_REVIEW     [v6]

- **Finished:** 2026-11-13 (run 50). Plan `plans/stage_18_peer_review_v6.md`; two fresh opus subagents →
  `paper/mypaper/18_review_v6_run1.md` (5 / 4), `18_review_v6_run2.md` (RSS/CoRL pair, 3 / 4). **No fabrication**;
  headline H6a / H6b / H6c recomputed from raw jsonl, exact. Merged record + triage `paper/mypaper/18_peer_review.md`.
- Main-session checks: analysis script committed (ae3c3899, 01:47 UTC 11-10) before the first v6 record (02:06 UTC),
  unchanged since. Post-hoc (report-only) `code/analysis_v6_posthoc.py` → `results/v6/18_posthoc_v6.json`: E12 shift
  ci95 excludes 0 only in S12; H6b Holm count 7 / 10 under bootstrap seeds 0–9 but 5 / 10 under seed 10 (fresh window
  2 / 10 under all); DAgger warm start confirmed.
- **Next:** stage 19 PAPER_REVISION [v6] with the 7-item paper-level triage; evidence-level requests deferred (cap).
