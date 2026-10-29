"""v3 episode streams (amendment v3.0 C5, v3.1 D1).

Evaluation splits (cal3, pilot3, val3, test3, g2v3, bank3) use the v2 key without kappa, so episode i is the same
initial state in every cell of a set (paired across kappa). Training splits (label3, dagger3) put kappa in the key, so
S0 and S12 training states are disjoint. Every v3 job runs with TOUCHBED_NPHI=64 and records `action_set` below.
"""
from __future__ import annotations

import math

from .evaluate import SPLIT_SALT, stream
from .geometry import Library
from .pf import Prior
from .shapes import get_set
from .travel import A, N_PHI, N_PSI

V3_SALTS = {"cal3": 61, "pilot3": 67, "val3": 71, "test3": 79, "label3": 83, "dagger3": 89, "g2v3": 97, "bank3": 101}
TRAIN_SPLITS = ("label3", "dagger3")
for _k, _v in V3_SALTS.items():           # register without touching the v1/v2 entries
    assert SPLIT_SALT.get(_k, _v) == _v
    SPLIT_SALT[_k] = _v
assert len(set(SPLIT_SALT.values())) == len(SPLIT_SALT)

ACTION_SET = f"{N_PHI}x{N_PSI}"


def require_v3_actions():
    if A != 512:
        raise RuntimeError("v3 runs need TOUCHBED_NPHI=64 (amendment v3.0 C1); got action set " + ACTION_SET)


def dagger_index(round_: int, seed: int, j: int) -> int:
    """Amendment v3.1 D1: index = 100,000·r + 1,000·(seed − 500) + j, r ∈ {1, 2}, j ∈ [0, 800)."""
    if round_ not in (1, 2) or not 0 <= j < 800 or not 501 <= seed <= 599:
        raise ValueError((round_, seed, j))
    return 100_000 * round_ + 1_000 * (seed - 500) + j


def state_v3(setname: str, split: str, i: int, kappa: float | None = None, prior=None):
    """Initial state s0 = (k, x, y, theta) and finger start angle phi0 of episode i."""
    if split not in V3_SALTS:
        raise ValueError(split)
    if prior is None:
        prior = Prior(Library(get_set(setname)).K)
    if split in TRAIN_SPLITS:
        if kappa is None:
            raise ValueError("training splits are kappa-keyed (amendment v3.1 D1)")
        rng = stream("state", setname, split, V3_SALTS[split], float(kappa), i)
        phi_rng = stream("phi0", setname, split, float(kappa), i)
    else:
        rng = stream("state", setname, split, V3_SALTS[split], i)
        phi_rng = stream("phi0", setname, split, i)
    k, x, y, th = prior.sample(rng, 1)
    return (int(k[0]), float(x[0]), float(y[0]), float(th[0])), float(phi_rng.uniform(0, 2 * math.pi))


def states_v3(setname: str, split: str, indices, kappa: float | None = None):
    lib = Library(get_set(setname))
    prior = Prior(lib.K)
    return lib, prior, [state_v3(setname, split, int(i), kappa, prior) for i in indices]


def ep_key_v3(setname: str, split: str, kappa: float, tau: float, i: int):
    """Key of the observation / policy / decision-PF streams of one episode (v2 convention, v3 split names)."""
    return (setname, split, float(kappa), float(tau), int(i))


# ─── v3 episode runner ────────────────────────────────────────────────────────────────────────────────────────────────
class History:
    """Belief-free view of an episode for policies that read only the touch history (`.hist`, as ParticleFilter)."""

    def __init__(self):
        self.hist = []

    def update(self, phi, psi, obs):
        self.hist.append((phi, psi, obs))


def run_episode_v3(policy, lib, prior, om, s0, phi0, kappa, tau, ep_key, needs_belief=True, n_dec=2000,
                   teacher=None, beta=0.0, mix_rng=None, evaluate=True, grid_sub=4):
    """One v3 episode. The policy acts on the decision PF (needs_belief) or on the touch history. Observations come from
    stream('obs', *ep_key), so histories are rebuilt exactly by gridpost.rebuild_history.

    teacher: optional GStar; if given, the decision PF is always run and every visited decision is labelled with
    teacher.score_vector (amendment v3.0 C7). beta: probability that the teacher's action is executed instead of the
    policy's (DAgger mixing, v3.0 C7); mix_rng draws that coin. evaluate: grid-evaluator read-out (v3.0 C2)."""
    import time

    import numpy as np

    from .evaluate import stream
    from .evaluate_v2 import prior_ball_mass
    from .likelihood import sample_obs
    from .pf import ParticleFilter
    from .travel import PHI, PSI, TravelState

    obs_rng = stream("obs", *ep_key)
    run_pf = needs_belief or teacher is not None
    pf = ParticleFilter(lib, om, prior, n_dec, stream("pf_dec", *ep_key)) if run_pf else None
    hview = History()
    ts = TravelState(phi0, kappa, tau)
    k0, x0, y0, t0 = s0
    actions, lat, labels, executed_teacher = [], [], [], []
    while not ts.done():
        lab = None
        if teacher is not None:
            s, mask, a_t = teacher.score_vector(pf, ts)
            lab = {"t": ts.n_probes, "phi_t": ts.phi, "tau_rem": ts.tau_rem, "s": s, "mask": mask, "a_teacher": a_t,
                   "feasible": ts.feasible().copy()}
        t_start = time.perf_counter()
        a = int(policy.act(pf if needs_belief else hview, ts)) if policy is not None else None
        lat.append(time.perf_counter() - t_start)
        use_t = teacher is not None and (policy is None or (beta > 0 and mix_rng.random() < beta))
        if use_t:
            a = lab["a_teacher"]
        if lab is not None:
            lab["a_policy"] = -1 if policy is None else a
            labels.append(lab)
        executed_teacher.append(bool(use_t))
        ts.step(a)
        actions.append(a)
        phi, psi = float(PHI[a]), float(PSI[a])
        obs = tuple(v[0] for v in sample_obs(om, lib, obs_rng, np.array([k0]), x0, y0, t0, phi, psi))
        hview.update(phi, psi, obs)
        if pf is not None:
            pf.update(phi, psi, obs)
    out = {"actions": actions, "n_probes": ts.n_probes, "travel_rad": ts.travel, "tau_left": ts.tau_rem,
           "latencies_s": lat, "executed_teacher": executed_teacher, "history": hview.hist}
    if labels:
        out["labels"] = labels
    if evaluate:
        from .gridpost import AdaptiveGridPosterior
        G = AdaptiveGridPosterior(lib, prior, om, hview.hist, s0, sub=grid_sub)
        out.update(G.readout(s0, prior_ball_mass(lib, prior, s0)))
    return out
