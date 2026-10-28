"""Brute-force grid posterior: the reference evaluation of amendment B8.
After an episode the evaluation only needs p(s | h_T) for the full history (decisions never read it), so the posterior
can be computed deterministically on a grid instead of by SMC: k in 1..K, (x, y) cell midpoints of the prior box
(spacing h_xy), theta cell midpoints (spacing h_th). The log posterior is the prior (uniform) plus the sum of the shared
eps-softened log-likelihoods of every probe (touchbed/likelihood.py), evaluated in theta chunks. Read-outs mirror the
evaluation PF exactly: MAP identity from the identity marginal; pose = highest-posterior grid state of that identity
refined by the same Nelder-Mead on the exact log-posterior; ball mass = grid mass inside B(s0) (symmetry-folded);
BI = log max(mass, 1/(2 n_floor)) - log P(B(s0)) with the PF's floor convention (n_floor = 32,000)."""
import math

import numpy as np
from scipy.optimize import minimize
from scipy.special import logsumexp

from .ball import R_TH, R_XY
from .likelihood import loglik, wrap
from .pf import success


class GridPosterior:
    def __init__(self, lib, prior, om, history, h_xy: float = 0.5, h_th_deg: float = 1.0, chunk_th: int = 24):
        self.lib, self.prior, self.om, self.hist = lib, prior, om, list(history)
        half = prior.xy_half
        nxy = int(round(2 * half / h_xy))
        self.gx = -half + h_xy * (np.arange(nxy) + 0.5)
        nth = int(round(360.0 / h_th_deg))
        self.gt = wrap(-math.pi + math.radians(h_th_deg) * (np.arange(nth) + 0.5))
        K = prior.K
        LP = np.empty((K, nxy, nxy, nth))
        X, Y = np.meshgrid(self.gx, self.gx, indexing="ij")
        for k in range(K):
            for t0 in range(0, nth, chunk_th):
                th = self.gt[t0:t0 + chunk_th]
                xs = np.broadcast_to(X[..., None], (nxy, nxy, len(th))).ravel()
                ys = np.broadcast_to(Y[..., None], (nxy, nxy, len(th))).ravel()
                ts = np.broadcast_to(th[None, None, :], (nxy, nxy, len(th))).ravel()
                ks = np.full(xs.shape, k)
                tot = np.zeros(xs.shape)
                for phi, psi, obs in self.hist:
                    tot += loglik(om, lib, obs, ks, xs, ys, ts, phi, psi)
                LP[k, :, :, t0:t0 + chunk_th] = tot.reshape(nxy, nxy, len(th))
        self.LP = LP
        self.logZ = float(logsumexp(LP))
        self.W = np.exp(LP - self.logZ)

    def identity_mass(self):
        return self.W.sum(axis=(1, 2, 3))

    def ball_mass(self, s0):
        k0, x0, y0, t0 = s0
        g = self.lib.sym[k0]
        dxy = np.hypot(self.gx[:, None] - x0, self.gx[None, :] - y0) < R_XY
        dth = np.min(np.abs(wrap(self.gt[:, None] - t0 - g[None, :])), axis=1) < R_TH
        return float(self.W[k0][dxy[:, :, None] & dth[None, None, :]].sum())

    def _hist_ll(self, k, x, y, th):
        tot = 0.0
        for phi, psi, obs in self.hist:
            tot += float(loglik(self.om, self.lib, obs, np.array([k]), np.array([x]), np.array([y]), np.array([th]),
                                phi, psi)[0])
        return tot

    def estimate(self, refine_iters: int = 30):
        kh = int(np.argmax(self.identity_mass()))
        i, j, t = np.unravel_index(int(np.argmax(self.LP[kh])), self.LP[kh].shape)
        z0 = np.array([self.gx[i], self.gx[j], self.gt[t]])

        def negpost(z):
            if not self.prior.inside(z[0], z[1]):
                return 1e12
            return -self._hist_ll(kh, z[0], z[1], z[2])

        if refine_iters > 0 and self.hist:
            res = minimize(negpost, z0, method="Nelder-Mead",
                           options={"maxiter": refine_iters, "initial_simplex": z0 + np.array(
                               [[0, 0, 0], [0.5, 0, 0], [0, 0.5, 0], [0, 0, math.radians(0.5)]])})
            if res.fun <= negpost(z0):
                z0 = res.x
        return kh, float(z0[0]), float(z0[1]), float(wrap(z0[2]))

    def readout(self, s0, prior_mass: float, n_floor: int = 32000):
        out = success(self.lib, self.estimate(), s0)
        m = self.ball_mass(s0)
        out.update({"ball_info": math.log(max(m, 1.0 / (2 * n_floor))) - math.log(prior_mass), "ball_mass": m,
                    "identity_mass_true": float(self.identity_mass()[s0[0]])})
        return out


def rebuild_history(lib, om, s0, actions, ep_key, phis=None, psis=None):
    """The observation sequence of a recorded episode: run_episode_v2 draws y_t from stream('obs', *ep_key) in order."""
    from .evaluate import stream
    from .likelihood import sample_obs
    from .travel import PHI, PSI
    phis = PHI if phis is None else phis
    psis = PSI if psis is None else psis
    rng = stream("obs", *ep_key)
    k0, x0, y0, t0 = s0
    hist = []
    for a in actions:
        phi, psi = float(phis[a]), float(psis[a])
        obs = tuple(v[0] for v in sample_obs(om, lib, rng, np.array([k0]), x0, y0, t0, phi, psi))
        hist.append((phi, psi, obs))
    return hist


class AdaptiveGridPosterior(GridPosterior):
    """Coarse grid (h_xy, h_th) everywhere; every coarse cell whose log posterior is within `prune` nats of the maximum
    (dilated by one cell in x, y and theta) is subdivided into sub^3 fine cells. Unrefined cells keep their coarse
    midpoint value (their total mass is below ~exp(-prune) of the peak cell each). Fine resolution = h / sub."""

    def __init__(self, lib, prior, om, history, h_xy: float = 1.0, h_th_deg: float = 2.0, sub: int = 4,
                 prune: float = 25.0, batch: int = 20000):
        super().__init__(lib, prior, om, history, h_xy=h_xy, h_th_deg=h_th_deg)
        self.sub, self.h_xy, self.h_th = sub, h_xy, math.radians(h_th_deg)
        LPc = self.LP
        sel = LPc > LPc.max() - prune
        # dilation (x, y non-periodic; theta periodic)
        d = sel.copy()
        d[:, 1:, :, :] |= sel[:, :-1, :, :]; d[:, :-1, :, :] |= sel[:, 1:, :, :]
        e = d.copy()
        e[:, :, 1:, :] |= d[:, :, :-1, :]; e[:, :, :-1, :] |= d[:, :, 1:, :]
        f = e | np.roll(e, 1, axis=3) | np.roll(e, -1, axis=3)
        self.refined = f
        idx = np.argwhere(f)                                       # (n_sel, 4): k, ix, iy, it
        o = (np.arange(sub) + 0.5) / sub - 0.5                     # sub-cell offsets in units of the coarse cell
        ox, oy, ot = np.meshgrid(o, o, o, indexing="ij")
        ox, oy, ot = ox.ravel(), oy.ravel(), ot.ravel()            # (sub^3,)
        fk, fx, fy, ft, flp = [], [], [], [], []
        for b0 in range(0, len(idx), batch):
            I = idx[b0:b0 + batch]
            ks = np.repeat(I[:, 0], len(ox))
            xs = (self.gx[I[:, 1]][:, None] + ox[None, :] * h_xy).ravel()
            ys = (self.gx[I[:, 2]][:, None] + oy[None, :] * h_xy).ravel()
            ts = wrap(self.gt[I[:, 3]][:, None] + ot[None, :] * self.h_th).ravel()
            tot = np.zeros(xs.shape)
            for phi, psi, obs in self.hist:
                tot += loglik(om, lib, obs, ks, xs, ys, ts, phi, psi)
            fk.append(ks); fx.append(xs); fy.append(ys); ft.append(ts); flp.append(tot)
        self.fk, self.fx, self.fy, self.ft = (np.concatenate(v) if v else np.zeros(0) for v in (fk, fx, fy, ft))
        self.flp = np.concatenate(flp) if flp else np.zeros(0)
        # masses: fine cells have volume 1/sub^3 of a coarse cell
        lv = -3 * math.log(sub)
        un = ~f
        self.c_lp = np.where(un, LPc, -np.inf)
        self.logZ = float(np.logaddexp(logsumexp(self.c_lp), logsumexp(self.flp + lv) if len(self.flp) else -np.inf))
        self.Wc = np.exp(self.c_lp - self.logZ)
        self.Wf = np.exp(self.flp + lv - self.logZ)
        self.n_refined = int(f.sum())

    def identity_mass(self):
        m = self.Wc.sum(axis=(1, 2, 3))
        return m + np.bincount(self.fk.astype(int), weights=self.Wf, minlength=self.prior.K)

    def ball_mass(self, s0):
        k0, x0, y0, t0 = s0
        g = self.lib.sym[k0]
        dxy = np.hypot(self.gx[:, None] - x0, self.gx[None, :] - y0) < R_XY
        dth = np.min(np.abs(wrap(self.gt[:, None] - t0 - g[None, :])), axis=1) < R_TH
        mc = float(self.Wc[k0][dxy[:, :, None] & dth[None, None, :]].sum())
        sel = self.fk == k0
        inb = (np.hypot(self.fx[sel] - x0, self.fy[sel] - y0) < R_XY) & (
            np.min(np.abs(wrap(self.ft[sel][:, None] - t0 - g[None, :])), axis=1) < R_TH)
        return mc + float(self.Wf[sel][inb].sum())

    def estimate(self, refine_iters: int = 30):
        kh = int(np.argmax(self.identity_mass()))
        sel = np.flatnonzero(self.fk == kh)
        if len(sel):
            i = sel[np.argmax(self.flp[sel])]
            z0 = np.array([self.fx[i], self.fy[i], self.ft[i]])
        else:
            i, j, t = np.unravel_index(int(np.argmax(self.LP[kh])), self.LP[kh].shape)
            z0 = np.array([self.gx[i], self.gx[j], self.gt[t]])

        def negpost(z):
            if not self.prior.inside(z[0], z[1]):
                return 1e12
            return -self._hist_ll(kh, z[0], z[1], z[2])

        if refine_iters > 0 and self.hist:
            res = minimize(negpost, z0, method="Nelder-Mead",
                           options={"maxiter": refine_iters, "initial_simplex": z0 + np.array(
                               [[0, 0, 0], [0.5, 0, 0], [0, 0.5, 0], [0, 0, math.radians(0.5)]])})
            if res.fun <= negpost(z0):
                z0 = res.x
        return kh, float(z0[0]), float(z0[1]), float(wrap(z0[2]))
