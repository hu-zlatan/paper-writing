# Stage 8.5 · THEORETICAL_BOUNDS · v3  (run 5, 2026-10-29)

## Goal
Preliminary theory for the v3 hypotheses (docs/07_hypotheses_v3.md) → docs/07b_theoretical_bounds_v3.md, plus the
reference verification that 07_hypotheses_v3 §8 assigns to this stage → docs/07d_reference_check_v3.md.

## Tasks
- [ ] Fresh strongest-model subagent, prompt template `pipeline/references/stage_prompts/theoretical_bounds.md`
      verbatim (system + user), {hypotheses} = docs/07_hypotheses_v3.md, {method_sketch} = §2 of that file + the
      measured unit costs it quotes + code paths (code/touchbed/{relframe,policies_v2,gridpost,latency,lookahead}.py).
      Focus the reviewer-facing questions: per-decision cost of the 27-config greedy grid vs the student
      (O(N·C·M + N²) vs O(T·d·h + d·A)), what DAgger gives (and does not give) for a soft-label surrogate with a
      cost-normalised teacher, and why no approximation guarantee of greedy carries over under order-dependent travel.
- [ ] Verify every reference in 07_hypotheses_v3 §8 (arXiv abs pages via WebFetch / WebSearch); find a verifiable
      identifier for DAgger (Ross, Gordon, Bagnell, AISTATS 2011) and for any bound cited by the subagent; one targeted
      novelty search ("distilled greedy information gain tactile localisation"). Unverified → not cited.
- [ ] Self-check against pipeline/references/hard_constraints.md (no fabricated proof; honesty section; baseline
      comparison present; no unverified citation).
- [ ] PROGRESS.md entry; commit + push.

## Output Summary
(filled at the end)
