"""Episode generation and evaluation of touch-selection methods (docs/07_hypotheses.md §1.3-1.5).

Every method is scored by the same evaluation particle filter (N_eval particles) on the same fixed test states; methods
differ only in which probes they choose. Methods that need a belief to decide (coverage, greedy PF-EIG) keep their own
decision PF of N_dec particles, fed with the same observations.
"""
from __future__ import annotations

import hashlib
import math
import time

import numpy as np

from .geometry import Library
from .likelihood import ObsModel, sample_obs
from .pf import ParticleFilter, Prior, success
from .shapes import get_set

SPLIT_SALT = {"pilot": 11, "val": 23, "test": 37, "g2": 53}  # g2: fresh G2/H2b-P1 belief episodes


def stream(*keys) -> np.random.Generator:
    """Deterministic RNG stream from string/int keys (stable across processes and machines)."""
    h = hashlib.sha256("|".join(map(str, keys)).encode()).digest()
    return np.random.default_rng(int.from_bytes(h[:8], "little"))


def make_states(setname: str, split: str, n: int):
    lib = Library(get_set(setname))
    prior = Prior(lib.K)
    # one independent stream per episode index, so episode i is the same state whatever n or shard is requested
    states = []
    for i in range(n):
        k, x, y, th = prior.sample(stream("state", setname, split, SPLIT_SALT[split], i), 1)
        states.append((int(k[0]), float(x[0]), float(y[0]), float(th[0])))
    return lib, prior, states


def run_episode(policy_factory, lib, prior, om: ObsModel, s0, T: int, ep_key, n_eval: int = 10000,
                n_dec: int = 2000, needs_belief: bool = True, refine_iters: int = 30, obs_fn=None, pf_kwargs=None):
    """Run one episode of T touches. policy_factory(rng) -> object with .act(pf) -> (phi, psi) (or .act(history) for
    learned policies via an adapter). Returns per-episode metrics and per-decision latencies (seconds)."""
    obs_rng = stream("obs", *ep_key)
    pol = policy_factory(stream("policy", *ep_key))
    pf_eval = ParticleFilter(lib, om, prior, n_eval, stream("pf_eval", *ep_key), **(pf_kwargs or {}))
    pf_dec = ParticleFilter(lib, om, prior, n_dec, stream("pf_dec", *ep_key)) if needs_belief else None
    lat = []
    k0, x0, y0, t0 = s0
    n_contact = 0
    for t in range(T):
        t_start = time.perf_counter()
        phi, psi = pol.act(pf_dec if needs_belief else pf_eval)
        lat.append(time.perf_counter() - t_start)
        if obs_fn is None:
            obs = tuple(v[0] for v in sample_obs(om, lib, obs_rng, np.array([k0]), x0, y0, t0, phi, psi))
        else:  # e.g. MuJoCo contact (H4); same noise model, different contact geometry
            obs = obs_fn(om, obs_rng, s0, phi, psi)
        n_contact += int(obs[0])
        pf_eval.update(phi, psi, obs)
        if pf_dec is not None:
            pf_dec.update(phi, psi, obs)
    est = pf_eval.estimate(refine_iters)
    out = success(lib, est, s0)
    out["ig"] = pf_eval.realized_ig_evidence(s0)
    out["ig_kde"] = pf_eval.realized_ig(s0)
    out["ball_info"] = pf_eval.ball_info(s0)
    out["n_contact"] = n_contact
    out["latency_median_s"] = float(np.median(lat))
    return out, lat
