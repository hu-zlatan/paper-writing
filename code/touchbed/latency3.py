"""v3 latency protocol (docs/07_hypotheses_v3.md §1.8; amendment v3.0 C11).

Decision states come from trajectories driven by full-size G* (2,000, 512, 64) on `pilot3` (Lat′) or `test3` (final
benchmark) episodes. At every decision every method is timed on the same state, interleaved in a rotating order,
single thread (OMP/MKL/OPENBLAS = 1 set by the caller). Per-decision latency L_dec = time from receiving y_t to emitting
a_{t+1}, split into components:
  greedy (N, C, M):  t_assim (its own PF, N particles, assimilates y_t incl. resample-move), t_nb (ball neighbour
                     lists, O(N²)), t_score (EIG_B over C candidates × M outcomes), t_select (feasibility, ÷ cost, argmax)
  student:           t_feat (relative re-encoding inputs), t_fwd (network forward, 512 logits), t_mask (mask + argmax)
  pruned-16:         student components + G* (2,000, ·, 64) assimilation, neighbour lists and scoring of the student's
                     top-16 (random-16: 16 uniformly drawn feasible actions)
L_final (student's deployable estimate): one PF (N = 2,000) pass over the whole history + MAP identity + 30 Nelder–Mead
iterations. The first `warmup` decisions are discarded.
"""
from __future__ import annotations

import itertools
import time

import numpy as np

from .ball import ball_eig, neighbours
from .evaluate import stream
from .likelihood import ObsModel, sample_obs
from .pf import ParticleFilter
from .relframe import rel_ctx, rel_features
from .travel import A, PHI, PSI, TravelState, rung_subset

GRID_N = (2000, 500, 125)
GRID_C = (512, 128, 32)
GRID_M = (64, 16, 4)
CONFIGS = [f"g{N}_{C}_{M}" for N, C, M in itertools.product(GRID_N, GRID_C, GRID_M)]


def subset_for(C: int) -> np.ndarray:
    """Nested candidate subsets on 64 x 8 (amendment v3.0 C1): 512 all, 128 = rung(32, 4), 32 = rung(16, 2)."""
    if C == A:
        return np.arange(A)
    return {128: rung_subset(32, 4), 32: rung_subset(16, 2)}[C]


def parse(cfg: str):
    N, C, M = map(int, cfg[1:].split("_"))
    return N, C, M


def timed_greedy(pf, ts, rng, M, subset, last=None):
    """One greedy decision with component timers. Same computation (and RNG use) as GStar(M, subset).act after
    pf.update(*last). Returns (action, {t_assim, t_nb, t_score, t_select})."""
    t0 = time.perf_counter()
    if last is not None:
        pf.update(*last)
    t1 = time.perf_counter()
    feas = ts.feasible()
    cand = subset[feas[subset]]
    if len(cand) == 0:
        cand = np.flatnonzero(feas)
    w = pf.weights()
    nb = neighbours(pf.lib, pf.k, pf.x, pf.y, pf.th)
    t2 = time.perf_counter()
    e = ball_eig(pf, PHI[cand], PSI[cand], M, rng, particles=(pf.k, pf.x, pf.y, pf.th, w), nb=nb)
    t3 = time.perf_counter()
    a = int(cand[int(np.argmax(e / ts.costs()[cand]))])
    t4 = time.perf_counter()
    return a, {"t_assim": t1 - t0, "t_nb": t2 - t1, "t_score": t3 - t2, "t_select": t4 - t3}


def timed_student(student, hist, ts):
    """Student.act with component timers; returns (action, logits over feasible set, timers)."""
    t0 = time.perf_counter()
    t = len(hist)
    RAW = np.zeros((1, t + 1, 6)); PHIT = np.full((1, t + 1), ts.phi); TAUR = np.full((1, t + 1), ts.tau_rem)
    for i, (phi, psi, o) in enumerate(hist):
        RAW[0, i] = [phi, psi, float(o[0]), float(o[1]), float(o[2]), float(o[3])]
    valid = np.zeros((1, t + 1), dtype=bool); valid[0, :t] = True
    Fr, Mk = rel_features(RAW, PHIT, valid)
    ctx, sh = rel_ctx(PHIT, TAUR, student.tau)
    t1 = time.perf_counter()
    out, _ = student.net.forward(Fr, Mk, ctx, sh)
    t2 = time.perf_counter()
    z = np.where(ts.feasible(), out[0, t], -np.inf)
    a = int(np.argmax(z))
    t3 = time.perf_counter()
    return a, z, {"t_feat": t1 - t0, "t_fwd": t2 - t1, "t_mask": t3 - t2}


def timed_pruned(student, hist, pf, ts, rng, k=16, M=64, last=None, random_rng=None):
    """Pruned-k: student top-k (or k random feasible actions if random_rng is given) re-scored by G* at the PF's size."""
    a_s, z, ts_ = timed_student(student, hist, ts)
    t0 = time.perf_counter()
    feas = np.flatnonzero(np.isfinite(z))
    if random_rng is None:
        top = feas[np.argsort(-z[feas], kind="stable")[:k]]
    else:
        top = random_rng.choice(feas, size=min(k, len(feas)), replace=False)
    t_prop = time.perf_counter() - t0
    a, tg = timed_greedy(pf, ts, rng, M, np.sort(top), last)
    tg["t_select"] += t_prop
    return a, {**ts_, **tg}


def final_estimate_time(lib, om, prior, hist, key, n=2000, refine_iters=30):
    t0 = time.perf_counter()
    pf = ParticleFilter(lib, om, prior, n, stream("lat_final", *key))
    for h in hist:
        pf.update(*h)
    pf.estimate(refine_iters)
    return time.perf_counter() - t0


def run_latency3(setname, kappa, tau, student, indices, split="pilot3", warmup=20, max_decisions=520, configs=None,
                 pruned=True):
    from .v3 import states_v3
    lib, prior, eps = states_v3(setname, split, indices)
    om = ObsModel()
    configs = list(CONFIGS if configs is None else configs)
    methods = ["student"] + configs + (["pruned16", "random16"] if pruned else [])
    recs, finals = [], []
    dec = 0
    for i, (s0, phi0) in zip(indices, eps):
        key = ("lat3", setname, kappa, tau, int(i))
        Ns = {m: parse(m)[0] for m in configs}
        Ns.update({"pruned16": 2000, "random16": 2000, "driver": 2000})
        pfs = {m: ParticleFilter(lib, om, prior, N, stream("lat_pf", m, *key)) for m, N in Ns.items()}
        rngs = {m: stream("lat_g", m, *key) for m in Ns}
        rand16 = stream("lat_r16", *key)
        ts = TravelState(phi0, kappa, tau)
        obs_rng = stream("lat_obs", *key)
        last, hist, t = None, [], 0
        while not ts.done() and dec < max_decisions:
            rot = methods[dec % len(methods):] + methods[:dec % len(methods)]
            times, acts = {}, {}
            for m in rot:
                if m == "student":
                    a, _, tm = timed_student(student, hist, ts)
                elif m in ("pruned16", "random16"):
                    a, tm = timed_pruned(student, hist, pfs[m], ts, rngs[m], last=last,
                                         random_rng=rand16 if m == "random16" else None)
                else:
                    N, C, M = parse(m)
                    a, tm = timed_greedy(pfs[m], ts, rngs[m], M, subset_for(C), last)
                tm["L_dec"] = sum(tm.values())
                times[m], acts[m] = tm, a
            # trajectory driver: full-size G* on its own PF (not timed)
            a_drv, _ = timed_greedy(pfs["driver"], ts, rngs["driver"], 64, np.arange(A), last)
            if dec >= warmup:
                recs.append({"episode": int(i), "step": t, "timers": times, "actions": acts, "n_touch": t,
                             "driver_action": a_drv})
            ts.step(a_drv)
            phi, psi = float(PHI[a_drv]), float(PSI[a_drv])
            obs = tuple(v[0] for v in sample_obs(om, lib, obs_rng, np.array([s0[0]]), s0[1], s0[2], s0[3], phi, psi))
            last = (phi, psi, obs)
            hist.append(last)
            t += 1
            dec += 1
        finals.append({"episode": int(i), "L_final_s": final_estimate_time(lib, om, prior, hist, key),
                       "n_touch": len(hist)})
        if dec >= max_decisions:
            break
    return recs, finals


def macs_student(hidden: int, n_touch: int, n_act: int = A, ctx_dim: int = 5, feat_dim: int = 9) -> int:
    """MACs of one Student forward as implemented: the (T+1) x (T+1) relative grid is encoded by psi, rho runs on all
    T+1 rows (07b_theoretical_bounds_v3 §2.2)."""
    rows = n_touch + 1
    psi = rows * rows * (feat_dim * hidden + hidden * hidden)
    rho = rows * ((hidden + ctx_dim) * hidden + hidden * hidden + hidden * n_act)
    return int(psi + rho)


def lik_evals(N: int, C: int, M: int) -> int:
    """Likelihood evaluations of one greedy scoring call: M x N x C (+ N x C casts) — as latency.lik_evals_rung."""
    return int(M * N * C + N * C)
