"""Gate G2 belief bank and headroom estimation at (S, kappa) (docs/07_hypotheses_v2.md §4, amendment B6).
Belief i: fresh 'g2' episode i (own split key), G* (full size, decision PF N = 2000) runs for u_i ~ U{0..n*-1} steps;
the estimator then works on 500 particles resampled from that decision PF with the remaining travel budget."""
import numpy as np

from .evaluate import stream
from .evaluate_v2 import make_states_v2
from .geometry import Library
from .likelihood import ObsModel, sample_obs
from .lookahead import lookahead_gap
from .lookahead_tb import TouchbedProblem
from .pf import ParticleFilter, Prior
from .policies_v2 import GStar
from .shapes import get_set
from .travel import PHI, PSI, TravelState


def _k(split, *keys):
    """v2 keys unchanged for split 'g2'; any other split (v3: 'g2v3', amendment v3.0 C12) is added to every key."""
    return keys if split == "g2" else (split,) + keys


def g2_belief(setname, kappa, tau, n_star, i, n_dec=2000, M=64, split="g2"):
    om = ObsModel()
    if split == "g2":
        lib, prior, eps = make_states_v2(setname, "g2", i + 1)
        s0, phi0 = eps[i]
    else:
        from .v3 import state_v3
        lib = Library(get_set(setname))
        prior = Prior(lib.K)
        s0, phi0 = state_v3(setname, split, i, prior=prior)
    u = int(stream(*_k(split, "g2_steps", setname, kappa, i)).integers(0, n_star))
    pf = ParticleFilter(lib, om, prior, n_dec, stream(*_k(split, "g2_pf", setname, kappa, i)))
    ts = TravelState(phi0, kappa, tau)
    pol = GStar(stream(*_k(split, "g2_pol", setname, kappa, i)), M=M)
    obs_rng = stream(*_k(split, "g2_obs", setname, kappa, i))
    for _ in range(u):
        if ts.done():
            break
        a = pol.act(pf, ts)
        ts.step(a)
        obs = tuple(v[0] for v in sample_obs(om, lib, obs_rng, np.array([s0[0]]), s0[1], s0[2], s0[3], float(PHI[a]), float(PSI[a])))
        pf.update(float(PHI[a]), float(PSI[a]), obs)
    return lib, om, pf, ts, u


def g2_gap(setname, kappa, tau, n_star, i, n_la=500, C1=32, M_outer=64, split="g2"):
    lib, om, pf, ts, u = g2_belief(setname, kappa, tau, n_star, i, split=split)
    if ts.done() or not ts.feasible().any():
        # budget exhausted before the drawn step: no decision is left, V_LA = V_G* = 0 (contributes nothing to either
        # mean in the ratio-of-means G); recorded and counted
        return {"no_budget_left": True, "v_la": 0.0, "v_greedy": 0.0, "a_la": -1, "a_greedy": -1, "gap_abs": 0.0,
                "gap_rel": float("nan"), "set": setname, "kappa": kappa, "tau": tau, "n_star": n_star, "index": i,
                "steps_before": u, "tau_rem": ts.tau_rem}
    rng = stream(*_k(split, "g2_la", setname, kappa, i))
    prob = TouchbedProblem.from_pf(pf, n_la, rng)
    g_full = GStar(stream(*_k(split, "g2_first", setname, kappa, i)), M=64)
    prob.first_greedy = lambda logw, budget, r: g_full.act(pf, budget)
    r = lookahead_gap(prob, np.zeros(n_la), ts, seed=int(rng.integers(1 << 30)), C1=C1, M_outer=M_outer, greedy_M=0)
    r.update({"set": setname, "kappa": kappa, "tau": tau, "n_star": n_star, "index": i, "steps_before": u,
              "tau_rem": ts.tau_rem, "split": split})
    return r
