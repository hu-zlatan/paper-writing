# Stage 12 (v3) — main runs under outcome row 4 (plan, written before any test3 episode)

**Trigger.** D3 remedy fails (status note in `docs/07c_amendment_v3_0.md`, run 7): H1 dead, H1-fb withdrawn
(Lat′: pruned-16 only 3.2× faster) → outcome row 4 of `docs/07_hypotheses_v3.md` §5 (characterisation paper).
Per v3.1 D8 no new students are trained.

**What row 4 needs** (paper statement of row 4): H3 (look-ahead headroom, G2′ — gate data, complete for κ = 12,
κ = 0 follow-ups running); learnability of RL and of distillation with the same encoder, with the label-fit / belief-input
diagnosis (D3 first attempt + remedy on val3, D3-B on val3, RL success row); the H2 result; the evaluator methods note
(E′, v2 14_analysis §2.5).

## Frozen main-run set (S12 only; test3 untouched until the freeze commit)
| ID | Run | Episodes | Read-out |
|---|---|---|---|
| M1 | RL-relative training, sweep config 2, seeds 511–513, 2 × 10⁵ episodes, plateau recorded not used | — | `results/v3/rl/` |
| M2 | `eval3 --no-grid` (actions only) on test3 0–499: G\*, random, remedied students 501–503, RL 511–513 | 500 each | `results/v3/test3/` |
| M3 | `gt3` on M2 (fixed per-episode contrastive draws, J 16, L 4,095) → H2 rule: crossed-bootstrap one-sided 95 % LB of g_T(student) − g_T(RL) > +0.10 nats (`code/analysis_h2_v3.py`) | 500 | `results/v3/h2/` |
| M4 | `regrid3 --sub 8` on M2 actions, test3 0–299: G\*, students 501–503, RL 511–513 → success / BI rows (reported, no new test) | 300 each | `results/v3/test3_sub8/` |

M2 + M4 reuse one set of rollouts: `--no-grid` G\* actions re-read with `regrid3` are bit-identical to an `eval3`
with the grid (checked on val3 episode 3 in the sandbox: same actions, same success and BI).

**Students used everywhere:** the remedied round-2 students (`results/v3/d3rem/S_k12_hp0_s50{1,2,3}_r2.npz`),
the final D3 recipe. The first-attempt students are reported only in the learnability diagnosis on val3.

**Dropped (served only H1 / H1-fb):** S0 / A12 labels, DAgger and students; seeds 504–505; the 1,000-episode
student test grid; H★ test and the H1c power rule; R_b selection (its follow-up run was cancelled) and the R_b test;
BC, absolute-frame, Gen-κ and success-vs-probe rows; power-rule enlargements; the final latency benchmark (Lat′ gate
values are reported as measured, with their CI caveat).

**Still running for the record (gate data):** D3 remedy validation (seeds 502/503), D3-B validation, G5′ sub-8
re-reads (heuristics vs G\* context), G2′ κ = 0 follow-ups, first-D3 fill (s503, 13 episodes).

**Compute.** M2 ≈ 1.1 CPU-h (G\* 500 × ≈ 7.5 s), M3 < 0.2, M4 ≈ 2,100 × ≈ 30 s ≈ 17.5 CPU-h, M1 ≈ 3 × 0.75 h.
Main ≈ 21 CPU-h instead of the 126.6–149 of the full plan.

**Not allowed after the run** (07_hypotheses_v3 §5): switching the H2 metric or threshold, choosing between RL and
distillation on test data, adding cells, promoting exploratory seeds.
