# Stage 2 · PROBLEM_DECOMPOSE — problem tree (v1)

> Prompt: `pipeline/references/stage_prompts/problem_decompose.md` (system: "You are a senior research strategist."), with
> `{topic}` = RESTRICTS.yaml `project.topic` and `{goal_text}` = full contents of `docs/00_topic_init.md`. Generated 2026-10-28.

## Source

- Topic: Amortized, non-myopic active tactile localization — learning touch-selection policies that maximize the expected information gain about an object's pose and identity from sparse contacts.
- Goal context: `docs/00_topic_init.md` (SMART goal, RSS 2027 timeline, CPU-only constraint), design docs `docs/整体构想.md`, `docs/实验构想.md`, `docs/文献与问题.md`.
- Root question: *Can a policy trained offline on a bound of the total information gained over a touch budget localize objects by touch with fewer touches than myopic information-gain selection, at a fraction of its online compute, and does that advantage survive physically simulated contact?*

## Sub-questions

**SQ1 — Non-myopic benefit.** Under a fixed touch budget T, does a policy trained on the sPCE bound of total EIG reach lower pose error / higher identity accuracy than (a) the same network trained on one-step EIG and (b) greedy one-step EIG computed online with a particle filter? For which budgets and object sets (symmetric, near-symmetric, non-convex) does the gap appear, and when does it vanish (e.g. large T, where adaptive submodularity makes greedy near-optimal)?
- Evidence: E1 + ablation A1 in `docs/实验构想.md`.

**SQ2 — Amortization cost/benefit.** What is the per-decision latency of the amortized policy versus greedy EIG at matched accuracy, and how does greedy EIG's accuracy degrade when its particle / candidate budget is cut to match the policy's latency? What does training cost on CPU, and after how many deployments does it pay off?
- Evidence: E4, Greedy-EIG vs Greedy-EIG-fast in E1.

**SQ3 — Negative information and multimodality.** How much of the gain comes from conditioning on no-contact outcomes, and from representing multimodal beliefs (identity × pose, symmetries)? Does removing negative information hurt more on object sets with symmetric / similar shapes?
- Evidence: ablation A2 on object sets O1 vs O2; posterior-mode counts.

**SQ4 — Fidelity transfer and robustness.** Does a policy trained on the geometric probe model keep its ranking when contacts are produced by a MuJoCo fingertip moving until a contact sensor fires, and under train/test noise and prior mismatch?
- Evidence: E3; E0 geometric-vs-physics contact discrepancy.

**SQ5 — Objective fidelity.** How tight is the sPCE bound with L contrastive samples in this domain, and does a looser training bound (small L) change the learned policy's quality? Can the bound be validated against an exact grid posterior on small problems?
- Evidence: ablation A4; E0 exact-posterior check.

**SQ6 (stretch) — Dimensional scaling.** Does the approach extend from SE(2) to a subset of SE(3) with the same architecture, and how do the costs of the policy versus particle-filter EIG scale with pose dimension?
- Evidence: optional extension after v1 loop.

## Priority Ranking

| Rank | Sub-question | Why this rank |
|---|---|---|
| 1 | SQ1 Non-myopic benefit | Core novelty #1; the paper fails without a clear, honestly reported answer. |
| 2 | SQ3 Negative information & multimodality | Core novelty #2; distinguishes the work from a direct port of DAD / RL-BED. |
| 3 | SQ2 Amortization cost/benefit | The practical argument for robots (real-time selection); cheap to measure. |
| 4 | SQ4 Fidelity transfer & robustness | Main defence against "simulation-only, simplified contact" criticism. |
| 5 | SQ5 Objective fidelity | Needed for methodological soundness and the L ablation; mostly appendix. |
| 6 | SQ6 SE(3) scaling | Stretch goal; only if v1 converges early (Stage 2 full paper). |

## Risks

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| R1: Greedy EIG matches the non-myopic policy at all budgets (adaptive submodularity), erasing novelty #1. | Medium | High | Design budgets/object sets where look-ahead matters (symmetric objects, ambiguity resolvable only by two coordinated touches) and report honestly; the amortization/latency result (SQ2) still stands as a contribution. |
| R2: RL training on the sPCE reward is high-variance and unstable on CPU. | Medium | High | Use the per-step sPCE increment reward, baselines/advantage normalization, moderate L, and convergence checks; fall back to a differentiable surrogate (smoothed contact likelihood) with DAD-style direct gradients if RL fails after 3 repair iterations. |
| R3: Particle filter used for evaluation is itself inaccurate (degeneracy with sharp contact likelihoods). | Medium | Medium | Validate against exact grid posterior on small problems (E0); use systematic resampling + jitter with documented parameters. |
| R4: Geometric-to-MuJoCo transfer gap dominates results. | Low–Medium | Medium | Measure contact discrepancy first (E0) and, if large, add matching noise during training; report the gap as a result, not hide it. |
| R5: Novelty challenge — close prior work in policy-based BED or active tactile RL (2024–2026) already does this. | Medium | High | Stage 4–6 literature search targeted at "policy-based BED + touch/tactile"; if a direct precursor exists, PIVOT the framing at stage 8 toward the uncovered piece (e.g. negative information or multimodal identity×pose). |
| R6: CPU budget exceeded by large sweeps. | Low | Medium | Pilot + TIME_ESTIMATE, downscale seeds to 3–5 when conditions > 100, move long sweeps to GitHub Actions. |
| R7: Timeline — extended-abstract milestone (2026-12-04) arrives before v1 is mature. | Medium | Low | Extended abstract only needs complete methods + preliminary results; the full paper deadline (2027-04-16) carries the two full loops. |
