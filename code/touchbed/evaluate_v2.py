"""v2 episode runner (travel action model, time budget) — shared evaluation PF, paired episodes."""
from __future__ import annotations

import math
import time

import numpy as np

from .ball import R_TH, R_XY
from .evaluate import SPLIT_SALT, stream
from .geometry import Library
from .likelihood import ObsModel, sample_obs
from .pf import ParticleFilter, Prior, success
from .shapes import get_set
from .travel import PHI, PSI, TravelState


def make_states_v2(setname: str, split: str, n: int):
    """Like evaluate.make_states but also draws the finger start angle phi0 per episode (same for all methods)."""
    lib = Library(get_set(setname))
    prior = Prior(lib.K)
    out = []
    for i in range(n):
        rng = stream("state", setname, split, SPLIT_SALT[split], i)
        k, x, y, th = prior.sample(rng, 1)
        phi0 = float(stream("phi0", setname, split, i).uniform(0, 2 * math.pi))
        out.append(((int(k[0]), float(x[0]), float(y[0]), float(th[0])), phi0))
    return lib, prior, out


def prior_ball_mass(lib, prior, s0, n_grid: int = 200) -> float:
    """P(B(s0)) = (1/K) * area(disc_5mm(x0,y0) ∩ box)/area(box) * min(1, |G| * 2*5deg / 360deg); area by a fine grid."""
    k0, x0, y0, _ = s0
    u = (np.arange(n_grid) + 0.5) / n_grid * 2 - 1
    gx, gy = np.meshgrid(x0 + R_XY * u, y0 + R_XY * u)
    inside_disc = np.hypot(gx - x0, gy - y0) < R_XY
    frac_box = np.mean(prior.inside(gx, gy)[inside_disc])
    area = math.pi * R_XY ** 2 * frac_box
    return (1.0 / prior.K) * area / (2 * prior.xy_half) ** 2 * min(1.0, len(lib.sym[k0]) * 2 * R_TH / (2 * math.pi))


def ball_information(pf, s0, prior_mass: float) -> float:
    from .ball import in_ball
    w = pf.weights()
    post = float(w[in_ball(pf.lib, pf.k, pf.x, pf.y, pf.th, *s0)].sum())
    return math.log(max(post, 1.0 / (2 * pf.n))) - math.log(prior_mass)


def run_episode_v2(policy_factory, lib, prior, om: ObsModel, s0, phi0, kappa, tau, ep_key, n_eval=32000, n_dec=2000,
                   needs_belief=True, pf_kwargs=None, refine_iters=30, final_mh=0, actions=None):
    obs_rng = stream("obs", *ep_key)
    pol = policy_factory(stream("policy", *ep_key))
    pf_eval = ParticleFilter(lib, om, prior, n_eval, stream("pf_eval", *ep_key), **(pf_kwargs or {}))
    pf_dec = ParticleFilter(lib, om, prior, n_dec, stream("pf_dec", *ep_key)) if needs_belief else None
    phis, psis = (PHI, PSI) if actions is None else actions
    ts = TravelState(phi0, kappa, tau, phis=phis)
    lat = []
    k0, x0, y0, t0 = s0
    actions = []
    while not ts.done():
        t_start = time.perf_counter()
        a = pol.act(pf_dec if needs_belief else pf_eval, ts)
        lat.append(time.perf_counter() - t_start)
        ts.step(a)
        actions.append(a)
        phi, psi = float(phis[a]), float(psis[a])
        obs = tuple(v[0] for v in sample_obs(om, lib, obs_rng, np.array([k0]), x0, y0, t0, phi, psi))
        pf_eval.update(phi, psi, obs)
        if pf_dec is not None:
            pf_dec.update(phi, psi, obs)
    pf_eval.rejuvenate(final_mh)
    out = success(lib, pf_eval.estimate(refine_iters), s0)
    pm = prior_ball_mass(lib, prior, s0)
    out.update({"ball_info": ball_information(pf_eval, s0, pm), "ball_cap": -math.log(pm), "n_probes": ts.n_probes,
                "travel_rad": ts.travel, "tau_left": ts.tau_rem, "actions": actions,
                "latency_median_s": float(np.median(lat)) if lat else 0.0, "latencies_s": lat})
    return out
