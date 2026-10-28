"""Manipulation checks of docs/07_hypotheses.md §1.2 (run before main experiments).

- Geometric confusability c(k, k') = max_{x,y,theta} IoU(shape k, T shape k') and self near-symmetry c_self(k);
  set level C(O) = mean_k max(c_self(k), max_{k'!=k} c(k, k')). Requirement C(S) >= 0.90, C(A) <= 0.80.
  Optimisation: multi-start Nelder-Mead over (x, y, theta) from 36 rotations at zero offset (both shapes centred at
  their centroids) — a local search, so values are lower bounds of the true maxima.
- Myopia gap G(O): on a bank of beliefs (prior + posteriors after 1-2 random probes), the relative gap between the
  optimal two-step EIG and the two-step EIG of the greedy first action, with nested Monte Carlo. Requirement
  G(S) >= 0.10, G(A) <= 0.03.
- NC-relevance R_NC(O): fraction of bank beliefs whose EIG1-maximising action has predicted P(no contact) in [0.2, 0.8].
"""
from __future__ import annotations

import math

import numpy as np
from scipy.optimize import minimize
from scipy.special import logsumexp
from shapely import affinity
from shapely.geometry import Polygon

from .geometry import Library, cast
from .likelihood import ObsModel, loglik_from_pred, sample_obs
from .pf import ParticleFilter, Prior
from .policies import eig_candidates, sobol_candidates
from .shapes import get_set
from .evaluate import stream


def _iou(p: Polygon, q: Polygon, z) -> float:
    qq = affinity.translate(affinity.rotate(q, z[2], origin=(0, 0), use_radians=True), z[0], z[1])
    u = p.union(qq).area
    return p.intersection(qq).area / u if u > 0 else 0.0


def pair_confusability(vk, vj, exclude_sym=None, min_sep=math.radians(10)) -> float:
    p, q = Polygon(vk), Polygon(vj)
    best = 0.0
    for a0 in np.linspace(0, 2 * math.pi, 36, endpoint=False):
        if exclude_sym is not None and min(abs((a0 - g + math.pi) % (2 * math.pi) - math.pi) for g in exclude_sym) < min_sep:
            continue
        res = minimize(lambda z: -_iou(p, q, z), np.array([0.0, 0.0, a0]), method="Nelder-Mead",
                       options={"xatol": 0.05, "fatol": 1e-4, "maxiter": 200})
        z = res.x
        if exclude_sym is not None and min(abs((z[2] - g + math.pi) % (2 * math.pi) - math.pi) for g in exclude_sym) < min_sep:
            continue
        best = max(best, -res.fun)
    return best


def confusability(setname: str) -> dict:
    shapes = get_set(setname)
    K = len(shapes)
    M = np.zeros((K, K))
    for i in range(K):
        for j in range(K):
            if i == j:
                M[i, j] = pair_confusability(shapes[i].verts, shapes[i].verts, exclude_sym=shapes[i].sym)
            elif j > i:
                M[i, j] = M[j, i] = pair_confusability(shapes[i].verts, shapes[j].verts)
    per = [max(M[i, i], max(M[i, j] for j in range(K) if j != i)) for i in range(K)]
    return {"set": setname, "matrix": M.tolist(), "per_shape": per, "C": float(np.mean(per)),
            "names": [s.name for s in shapes]}


def _reweight(k, x, y, th, w, lib, om, phi, psi, obs):
    hit, qx, qy, qn = cast(lib, k, x, y, th, phi, psi)
    lw = np.log(w) + loglik_from_pred(om, obs[0], obs[1], obs[2], obs[3], hit, qx, qy, qn)
    return np.exp(lw - logsumexp(lw))


def myopia_gap_belief(pf: ParticleFilter, rng, C1=16, Y1=8, C2=16, M=16, target="state"):
    """Returns EIG2*, EIG2_greedy, max EIG1, P(NC) of the EIG1-maximiser for the PF belief."""
    lib, om = pf.lib, pf.om
    k, x, y, th, w = pf.k, pf.x, pf.y, pf.th, pf.weights()
    phi1, psi1 = sobol_candidates(rng, C1)
    eig1 = eig_candidates(pf, phi1, psi1, M, rng, particles=(k, x, y, th, w), target=target)
    def two_step(c, n_out, eig1_c):
        j = rng.choice(len(w), size=n_out, p=w)
        cont = []
        for m in range(n_out):
            obs = tuple(v[0] for v in sample_obs(om, lib, rng, np.array([k[j[m]]]), x[j[m]], y[j[m]], th[j[m]],
                                                  phi1[c], psi1[c]))
            w2 = _reweight(k, x, y, th, w, lib, om, phi1[c], psi1[c], obs)
            phi2, psi2 = sobol_candidates(rng, C2)
            cont.append(np.max(eig_candidates(pf, phi2, psi2, M, rng, particles=(k, x, y, th, w2), target=target)))
        return eig1_c + float(np.mean(cont))

    two = np.array([two_step(c, Y1, eig1[c]) for c in range(C1)])
    c_opt = int(np.argmax(two))
    cg = int(np.argmax(eig1))
    # re-estimate both selected first actions with fresh, independent samples (removes the max-selection bias)
    e1_fresh = eig_candidates(pf, phi1[[c_opt, cg]], psi1[[c_opt, cg]], 4 * M, rng, particles=(k, x, y, th, w),
                              target=target)
    v_opt = two_step(c_opt, 2 * Y1, float(e1_fresh[0]))
    v_greedy = two_step(cg, 2 * Y1, float(e1_fresh[1])) if cg != c_opt else v_opt
    hit, *_ = cast(lib, k, x, y, th, phi1[cg], psi1[cg])
    p_nc = float(np.sum(w * (~hit)))
    return v_opt, v_greedy, float(eig1.max()), p_nc


def myopia_bank(setname: str, start: int, count: int, n_particles: int = 1000, **kw) -> list:  # kw: C1,Y1,C2,M,target
    lib = Library(get_set(setname))
    om = ObsModel()
    prior = Prior(lib.K)
    out = []
    for b in range(start, start + count):
        rng = stream("bank", setname, b)
        pf = ParticleFilter(lib, om, prior, n_particles, rng)
        n_probe = 0 if b == 0 else int(rng.integers(1, 3))
        s0 = tuple(v[0] for v in prior.sample(rng, 1))
        for _ in range(n_probe):
            phi, psi = float(rng.uniform(-math.pi, math.pi)), float(rng.uniform(-0.6, 0.6))
            obs = tuple(v[0] for v in sample_obs(om, lib, rng, np.array([s0[0]]), s0[1], s0[2], s0[3], phi, psi))
            pf.update(phi, psi, obs)
        e2s, e2g, e1, pnc = myopia_gap_belief(pf, rng, **kw)
        out.append({"belief": b, "n_probe": n_probe, "eig2_opt": e2s, "eig2_greedy": e2g, "eig1_max": e1,
                    "p_nc_greedy": pnc, "rel_gap": (e2s - e2g) / e2s if e2s > 0 else 0.0})
    return out
