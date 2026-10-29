"""G2' bias check (07_hypotheses_v3 §3.4, amendment v3.0 C12): independent full-G* reference value on a g2v3 belief.

The H3 estimator (g2.py -> lookahead.lookahead_gap) values G*'s first action by completing each rollout with the
reduced greedy (500 resampled particles, no MH, 128 candidates, M = 16). The bias check asks whether that estimate
V_G* over-reads the value of the *actual* G* policy. Reference, on the same belief (same g2v3 index i, same G*-reached
decision PF, same remaining travel budget):
  V_ref = E[ log P_T(B(s)) - log P_0(B(s)) ],  s ~ decision PF,
where the episode from the belief on is run by full G* (decision PF N = 2,000 with its own resample-move, all
feasible actions of 512, M = 64) and P_t(B(s)) is the PF's weight mass in the success ball around s, floored at 1/N as
in ParticleFilter.ball_info (the number of floored rollouts is recorded). n_roll = 256 rollouts = the estimator's
re-estimation sample count (reest 4 x M_outer 64), each with its own observation, PF and G* streams.
Decision recorded in PROGRESS (run 6): the pre-registered text says "independent 4x-sample G* rollout estimate"
without a sample count; 4 x 64 = 256 is used, fixed before any G2' number was seen."""
import copy
import math

import numpy as np

from .ball import in_ball
from .evaluate import stream
from .g2 import g2_belief
from .likelihood import sample_obs
from .policies_v2 import GStar
from .travel import PHI, PSI


def _logmass(pf, s):
    w = pf.weights()
    m = in_ball(pf.lib, pf.k, pf.x, pf.y, pf.th, *s)
    mass = float(w[m].sum())
    floor = 1.0 / pf.n
    return math.log(max(mass, floor)), mass < floor


def bias_reference(setname, kappa, tau, n_star, i, n_roll=256, split="g2v3"):
    lib, om, pf0, ts0, u = g2_belief(setname, kappa, tau, n_star, i, split=split)
    base = {"set": setname, "kappa": kappa, "tau": tau, "n_star": n_star, "index": i, "steps_before": u,
            "tau_rem": ts0.tau_rem, "split": split, "n_roll": n_roll}
    if ts0.done() or not ts0.feasible().any():
        return {**base, "no_budget_left": True, "v_ref": 0.0, "se_ref": 0.0, "n_floored": 0}
    w0 = pf0.weights()
    rs = stream(split, "bias_ref_states", setname, kappa, i)
    S = rs.choice(len(w0), size=n_roll, p=w0)
    vals, floored, n_steps = [], 0, []
    for m in range(n_roll):
        j = int(S[m])
        s = (int(pf0.k[j]), float(pf0.x[j]), float(pf0.y[j]), float(pf0.th[j]))
        lm0, _ = _logmass(pf0, s)
        pf = copy.deepcopy(pf0)
        pf.rng = stream(split, "bias_ref_pf", setname, kappa, i, m)
        ts = copy.deepcopy(ts0)
        pol = GStar(stream(split, "bias_ref_pol", setname, kappa, i, m), M=64)
        orng = stream(split, "bias_ref_obs", setname, kappa, i, m)
        k = 0
        while not ts.done() and ts.feasible().any():
            a = pol.act(pf, ts)
            ts.step(a)
            obs = tuple(v[0] for v in sample_obs(om, lib, orng, np.array([s[0]]), s[1], s[2], s[3], float(PHI[a]),
                                                 float(PSI[a])))
            pf.update(float(PHI[a]), float(PSI[a]), obs)
            k += 1
        lmT, fl = _logmass(pf, s)
        floored += int(fl)
        vals.append(lmT - lm0)
        n_steps.append(k)
    v = np.array(vals)
    return {**base, "v_ref": float(v.mean()), "se_ref": float(v.std(ddof=1) / math.sqrt(len(v))),
            "n_floored": floored, "mean_steps": float(np.mean(n_steps))}
