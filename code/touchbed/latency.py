"""Latency protocol for H1b (docs/07_hypotheses_v2.md §2.3).
Trajectories are driven by full-size G* (rung R0) on test episodes; at every decision the policy and every ladder rung
are timed on the same decision state, interleaved (rotating order), single thread. Primary scope = time from receiving
y_t to emitting a_{t+1}: for a rung, its own PF (N_r particles) assimilates y_t (incl. resample-move) and scores its
candidates; for the policy, the forward pass over the history plus the feasibility mask. Selection-only time is
recorded too. The first `warmup` decisions are discarded. Multiply-add counts are computed analytically."""
import time

import numpy as np

from .evaluate import stream
from .evaluate_v2 import make_states_v2
from .likelihood import ObsModel, sample_obs
from .nn import FEAT_DIM
from .pf import ParticleFilter
from .policies_v2 import GStar
from .travel import PHI, PSI, TravelState, rung_subset

RUNGS = {  # name: (N, (n_phi, n_psi) or None for all 256, M)
    "R0": (2000, None, 64), "R1": (1000, None, 32), "R2": (1000, (16, 8), 32), "R3": (500, (16, 8), 16),
    "R4": (500, (16, 4), 16), "R5": (250, (16, 4), 8), "R6": (250, (8, 4), 8), "R7": (125, (8, 4), 4)}


def macs_policy(hidden: int, n_touch: int, ctx_dim: int = 3, n_act: int = 256) -> int:
    """MACs of one CategoricalDeepSets forward as implemented (the history is re-encoded each decision)."""
    psi = n_touch * (FEAT_DIM * hidden + hidden * hidden)
    rho = (hidden + ctx_dim) * hidden + hidden * hidden + hidden * n_act
    return int(psi + rho)


def lik_evals_rung(N: int, C: int, M: int) -> int:
    """Likelihood evaluations of one ball-EIG scoring call: M outcomes x N particles x C candidates (+ N x C casts)."""
    return int(M * N * C + N * C)


def run_latency(setname, kappa, tau, policy, start, n_episodes, warmup=20, max_decisions=520):
    lib, prior, eps = make_states_v2(setname, "test", start + n_episodes)
    om = ObsModel()
    recs = []
    order = ["policy"] + list(RUNGS)
    dec = 0
    for i in range(start, start + n_episodes):
        s0, phi0 = eps[i]
        key = ("lat", setname, kappa, tau, i)
        pfs = {r: ParticleFilter(lib, om, prior, N, stream("lat_pf", r, *key)) for r, (N, _, _) in RUNGS.items()}
        gs = {r: GStar(stream("lat_g", r, *key), M=M, subset=None if g is None else rung_subset(*g))
              for r, (N, g, M) in RUNGS.items()}
        ts = TravelState(phi0, kappa, tau)
        obs_rng = stream("lat_obs", *key)
        last = None
        hist = []
        t = 0
        while not ts.done() and dec < max_decisions:
            times, sel = {}, {}
            rot = order[dec % len(order):] + order[:dec % len(order)]
            acts = {}
            for m in rot:
                if m == "policy":
                    t0 = time.perf_counter()
                    a = policy.act(_HistView(list(hist)), ts)
                    times[m] = sel[m] = time.perf_counter() - t0
                else:
                    t0 = time.perf_counter()
                    if last is not None:
                        pfs[m].update(*last)
                    t1 = time.perf_counter()
                    a = gs[m].act(pfs[m], ts)
                    t2 = time.perf_counter()
                    times[m], sel[m] = t2 - t0, t2 - t1
                acts[m] = int(a)
            if dec >= warmup:
                recs.append({"episode": i, "step": t, "latency_s": times, "selection_s": sel, "actions": acts,
                             "n_touch": t})
            a = acts["R0"]
            ts.step(a)
            phi, psi = float(PHI[a]), float(PSI[a])
            obs = tuple(v[0] for v in sample_obs(om, lib, obs_rng, np.array([s0[0]]), s0[1], s0[2], s0[3], phi, psi))
            last = (phi, psi, obs)
            hist.append(last)
            t += 1
            dec += 1
        if dec >= max_decisions:
            break
    return recs


class _HistView:
    def __init__(self, hist):
        self.hist = hist
