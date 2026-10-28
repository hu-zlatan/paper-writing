# Stage 8 · HYPOTHESIS_GEN (multi-agent debate) · v1

## Goal
≥2 falsifiable hypotheses with rationale, measurable prediction (metric + threshold), failure condition (metric + threshold) and experiment sketch → docs/07_hypotheses.md.

## Tasks
- [ ] Pass 1 Proposer: fresh opus subagent, `stage_prompts/hypothesis_gen.md` pass-1 prompt verbatim, {synthesis} = docs/06_synthesis.md → docs/07a_proposer.md
- [ ] Pass 2 Skeptic: a different fresh opus subagent, pass-2 prompt verbatim on the proposer output → docs/07b_skeptic.md
- [ ] Pass 3 Methodologist: a third fresh opus subagent, pass-3 prompt verbatim → docs/07_hypotheses.md (canonical)
- [ ] Main session checks: every hypothesis falsifiable with numeric thresholds; feasible on CPU; consistent with the two core novelties; update docs/实验构想.md if the design changes.

## Inputs
- docs/06_synthesis.md, docs/00_topic_init.md (constraints only)

## Expected outputs
- docs/07a_proposer.md, docs/07b_skeptic.md, docs/07_hypotheses.md

## Hard-constraint checks
- [ ] Subagents get only the files they need, not this session's reasoning (AUTOPILOT §3).
- [ ] No hypothesis is trivially true; failure conditions quantitative.

---

## Output Summary  (filled in AFTER the stage runs)
- Three fresh opus subagents (proposer → skeptic → methodologist), each given only the prompt and the files it needed.
- Proposer: 5 hypotheses. Skeptic: H1–H4 REVISE, H5 REJECT (true by construction); top problems — myopic control could equal the total objective via the MI chain rule; underpowered "not significant = support" failure rules; saturating success metric and unspecified evaluation PF.
- Methodologist (canonical docs/07_hypotheses.md): H1a non-inferiority to full greedy PF-EIG (4 pp margin) + beats random/coverage; H1b ≥100× latency at matched accuracy (greedy Pareto sweep); H1c beats sparse success-reward RL; H2a non-myopic > myopic on ambiguous set S at T∈{3,5}; H2b mechanism (two-step oracle EIG on shared beliefs + analytic notch-rectangle positive control); H2c (secondary) gap shrinks with T; H3 planning for no-contact outcomes (two ablations + miss-information share); H4 MuJoCo transfer under a measured contact shift; H5′ (secondary) amortization cost vs library size K.
- Objectives: identical per-step sPCE increments r_t (L=255); non-myopic = PPO with full returns-to-go (γ=1); myopic control = γ=0 advantage (credit only for the immediate increment). Paired test over 2,000 shared test episodes per cell, crossed episode×seed bootstrap, Holm correction, saturation rule, manipulation check G(S) ≥ 0.10 and G(A) ≤ 0.03 on the myopia gap before main runs; evaluation PF 10k particles with resample-move + convergence check.
- Compute estimate ≈ 71 CPU-h (training ≈ 44), to be re-checked by pilots; planned on GitHub Actions shards.
- Main-session check: falsifiable, numeric thresholds, CPU-feasible. Sushi note — the paper's claims will centre on H1a/H1b, H2a/H2b, H3 (core novelties) with H4 as the transfer defence; H1c, H2c, H5′ are secondary/appendix.
- **Decision:** PROCEED → stage 8.5.
