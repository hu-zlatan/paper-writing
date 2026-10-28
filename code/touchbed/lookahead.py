"""Fixed Monte-Carlo look-ahead (rollout) estimator of gate G1 / G2 (docs/07_hypotheses_v2.md §4, amendment B6).

For a belief b (weighted particles) and a remaining budget, the value of a first action a is
    V(a) = E_{s ~ b, y_1 ~ p(.|s,a)} [ U(h_T; s) ],  U = log P(target(s) | h_T) - log P_b(target(s)),
where after a the episode is completed by the greedy comparator (G*) until the budget ends. Estimation:
  * common random numbers: the same outer states s_m and the same per-step random streams for every candidate;
  * screen: C1 candidates (G*'s own first action, the problem's structured set-up moves, the rest uniformly drawn) with
    M_outer outer samples each;
  * re-estimate: the top `top` candidates and G*'s first action with `reest` x M_outer fresh outer samples (new CRN set);
  * V_LA = max of the re-estimated candidate values (G*'s action included), V_G* = re-estimated value of G*'s action.
The relative gap is (V_LA - V_G*) / V_LA (per belief; G2 uses the ratio of means over a belief bank).
The problem object supplies: n_actions, sample_obs(a, s, rng), loglik(a, obs) over particles, target_logmass(logw, s),
greedy(logw, budget, rng), step_budget(budget, a), budget_left(budget), and optionally setup_moves(logw, budget)."""
import numpy as np


def rollout_value(problem, logw0, budget0, a_first, s, seed: int, greedy_M: int = 64):
    rng = np.random.default_rng(seed)
    logw = logw0.copy()
    budget = budget0
    a = a_first
    while True:
        obs = problem.sample_obs(a, s, rng)
        logw = logw + problem.loglik(a, obs)
        logw -= logw.max()
        budget = problem.step_budget(budget, a)
        if not problem.budget_left(budget):
            break
        a = problem.greedy(logw, budget, rng, M=greedy_M) if greedy_M else problem.greedy(logw, budget, rng)
    return problem.target_logmass(logw, s) - problem.target_logmass(logw0, s)


def value_estimates(problem, logw, budget, actions, M_outer: int, seed: int, greedy_M: int = 64):
    """CRN Monte-Carlo values of each first action; returns (len(actions), M_outer) per-sample values."""
    w = np.exp(logw - logw.max()); w /= w.sum()
    rs = np.random.default_rng(seed)
    S = rs.choice(len(w), size=M_outer, p=w)
    seeds = rs.integers(0, 2**63 - 1, size=M_outer)
    out = np.empty((len(actions), M_outer))
    for i, a in enumerate(actions):
        for m in range(M_outer):
            out[i, m] = rollout_value(problem, logw, budget, int(a), int(S[m]), int(seeds[m]), greedy_M)
    return out


def lookahead_gap(problem, logw, budget, seed: int, C1: int = 32, M_outer: int = 64, top: int = 4, reest: int = 4,
                  greedy_M: int = 64):
    rng = np.random.default_rng(seed)
    a_g = problem.greedy(logw, budget, np.random.default_rng(seed + 1), M=greedy_M)
    cand = [a_g]
    for a in getattr(problem, "setup_moves", lambda lw, b: [])(logw, budget):
        if a not in cand:
            cand.append(int(a))
    pool = [a for a in rng.permutation(problem.n_actions) if a not in cand]
    cand += [int(a) for a in pool[:max(0, C1 - len(cand))]]
    scr = value_estimates(problem, logw, budget, cand, M_outer, seed + 2, greedy_M).mean(1)
    order = np.argsort(-scr)
    best = [cand[i] for i in order[:top]]
    if a_g not in best:
        best.append(a_g)
    re = value_estimates(problem, logw, budget, best, reest * M_outer, seed + 3, greedy_M)
    vals = re.mean(1)
    v_la = float(vals.max())
    v_g = float(vals[best.index(a_g)])
    return {"a_greedy": int(a_g), "candidates": [int(a) for a in cand], "screen": scr.tolist(), "reestimated": best,
            "re_values": vals.tolist(), "v_la": v_la, "v_greedy": v_g, "a_la": int(best[int(np.argmax(vals))]),
            "gap_abs": v_la - v_g, "gap_rel": (v_la - v_g) / v_la if v_la > 0 else float("nan")}
