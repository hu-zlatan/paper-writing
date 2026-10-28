"""Particle filter over (identity, planar pose) with resample-move, point estimation and realized information gain.

Implements docs/07_hypotheses.md §1.3-1.4: stratified initialization (N/K particles per identity, poses from a scrambled
Sobol sequence over the prior box), sequential assimilation with the epsilon-softened likelihood, systematic resampling
when ESS < N/2 followed by resample-move (Metropolis-Hastings steps invariant to the posterior, evaluated on the full
history), MAP-identity + refined pose estimate, success criterion and IG_T.
"""
from __future__ import annotations

import math
from dataclasses import dataclass

import numpy as np
from scipy.optimize import minimize
from scipy.special import logsumexp
from scipy.stats import qmc

from .likelihood import ObsModel, loglik, wrap

XY_HALF = 15.0  # mm, prior x, y ~ U[-15, 15]


@dataclass
class Prior:
    K: int
    xy_half: float = XY_HALF

    def sample(self, rng: np.random.Generator, n: int):
        return (rng.integers(0, self.K, n), rng.uniform(-self.xy_half, self.xy_half, n),
                rng.uniform(-self.xy_half, self.xy_half, n), rng.uniform(-np.pi, np.pi, n))

    def inside(self, x, y):
        return (np.abs(x) <= self.xy_half) & (np.abs(y) <= self.xy_half)

    def log_density(self) -> float:
        """log p(s) for a state inside the support (identity uniform, pose uniform)."""
        return -math.log(self.K) - math.log((2 * self.xy_half) ** 2) - math.log(2 * math.pi)


class ParticleFilter:
    def __init__(self, lib, om: ObsModel, prior: Prior, n: int, rng: np.random.Generator, mh_steps: int = 3,
                 rw_xy: float = 0.5, rw_th: float = math.radians(0.5), p_indep: float = 0.1,
                 contact_proposal: bool = True, q_sigma_xy: float = 1.0, q_sigma_th: float = math.radians(3.0),
                 q_defensive: float = 0.1):
        self.lib, self.om, self.prior, self.rng = lib, om, prior, rng
        self.n, self.mh_steps, self.rw_xy, self.rw_th, self.p_indep = n, mh_steps, rw_xy, rw_th, p_indep
        self.contact_proposal, self.q_sxy, self.q_sth, self.q_beta = contact_proposal, q_sigma_xy, q_sigma_th, q_defensive
        e = lib.p1 - lib.p0
        self._elen = np.where(lib.mask, np.linalg.norm(e, axis=-1), 0.0)        # (K, V)
        self._perim = self._elen.sum(axis=1)                                    # (K,)
        K = prior.K
        per = int(math.ceil(n / K))
        sob = qmc.Sobol(d=3, scramble=True, seed=rng).random(1 << int(math.ceil(math.log2(per))))[:per]
        k = np.repeat(np.arange(K), per)[:n]
        u = np.tile(sob, (K, 1))[:n]
        self.k = k
        self.x = (u[:, 0] * 2 - 1) * prior.xy_half
        self.y = (u[:, 1] * 2 - 1) * prior.xy_half
        self.th = (u[:, 2] * 2 - 1) * np.pi
        self.logw = np.full(n, -math.log(n))
        self.hist = []          # list of (phi, psi, (c, px, py, n))
        self.loglik_hist = np.zeros(n)  # sum of per-step log-likelihoods of each particle (for MH)
        self.n_resample = 0
        self.log_evidence = 0.0  # log Z_t = sum_t log sum_i w_{t-1,i} p(y_t | s_i)  (SMC evidence estimate of log p(h_t))

    # ---- core recursion -------------------------------------------------------------------------------------------
    def _hist_loglik(self, k, x, y, th):
        tot = np.zeros(np.shape(k))
        for phi, psi, obs in self.hist:
            tot += loglik(self.om, self.lib, obs, k, x, y, th, phi, psi)
        return tot

    def ess(self) -> float:
        w = np.exp(self.logw - logsumexp(self.logw))
        return 1.0 / np.sum(w ** 2)

    def update(self, phi: float, psi: float, obs) -> None:
        ll = loglik(self.om, self.lib, obs, self.k, self.x, self.y, self.th, phi, psi)
        self.hist.append((phi, psi, obs))
        self.loglik_hist += ll
        self.logw = self.logw + ll
        lz = logsumexp(self.logw)  # previous weights are normalized, so this is log p_hat(y_t | h_{t-1})
        self.log_evidence += float(lz)
        self.logw -= lz
        if self.ess() < self.n / 2:
            self._resample_move()

    def _resample_move(self) -> None:
        self.n_resample += 1
        w = np.exp(self.logw - logsumexp(self.logw))
        # systematic resampling
        pos = (self.rng.random() + np.arange(self.n)) / self.n
        idx = np.searchsorted(np.cumsum(w), pos)
        idx = np.minimum(idx, self.n - 1)
        self.k, self.x, self.y, self.th = self.k[idx], self.x[idx], self.y[idx], self.th[idx]
        self.loglik_hist = self.loglik_hist[idx]
        self.logw = np.full(self.n, -math.log(self.n))
        # MH moves invariant to p(s | h): random walk (symmetric, prior ratio = support indicator) or independent prior
        # proposal (acceptance = likelihood ratio). Both kernels are individually posterior-invariant.
        contacts = [(o[1], o[2], o[3]) for _, _, o in self.hist if o[0]]
        if self.contact_proposal and contacts:
            self._mh_contact(np.asarray(contacts))
            return
        for _ in range(self.mh_steps):
            indep = self.rng.random(self.n) < self.p_indep
            kp, xp, yp, tp = self.prior.sample(self.rng, self.n)
            xr = self.x + self.rw_xy * self.rng.standard_normal(self.n)
            yr = self.y + self.rw_xy * self.rng.standard_normal(self.n)
            tr = wrap(self.th + self.rw_th * self.rng.standard_normal(self.n))
            k2 = np.where(indep, kp, self.k)
            x2, y2, t2 = np.where(indep, xp, xr), np.where(indep, yp, yr), np.where(indep, tp, tr)
            ins = self.prior.inside(x2, y2)
            ll2 = self._hist_loglik(k2, x2, y2, t2)
            log_acc = np.where(ins, ll2 - self.loglik_hist, -np.inf)
            acc = np.log(self.rng.random(self.n)) < log_acc
            self.k = np.where(acc, k2, self.k)
            self.x, self.y, self.th = np.where(acc, x2, self.x), np.where(acc, y2, self.y), np.where(acc, t2, self.th)
            self.loglik_hist = np.where(acc, ll2, self.loglik_hist)

    # ---- contact-conditioned independence proposal ----------------------------------------------------------------
    def _q_sample(self, C, n):
        """Defensive mixture: prior w.p. beta, else align a random perimeter point of a random identity (edge chosen
        proportional to length) with a random observed contact (position and outward normal), plus Gaussian noise."""
        lib, rng = self.lib, self.rng
        kp, xp, yp, tp = self.prior.sample(rng, n)
        j = rng.integers(0, len(C), n)
        k = rng.integers(0, lib.K, n)
        cum = np.cumsum(self._elen[k], axis=1) / self._perim[k][:, None]
        e = np.minimum((cum < rng.random(n)[:, None]).sum(axis=1), lib.V - 1)
        u = rng.random(n)
        pl = lib.p0[k, e] + u[:, None] * (lib.p1[k, e] - lib.p0[k, e])
        th = wrap(C[j, 2] - lib.normal_ang[k, e] + self.q_sth * rng.standard_normal(n))
        c, s = np.cos(th), np.sin(th)
        x = C[j, 0] - (c * pl[:, 0] - s * pl[:, 1]) + self.q_sxy * rng.standard_normal(n)
        y = C[j, 1] - (s * pl[:, 0] + c * pl[:, 1]) + self.q_sxy * rng.standard_normal(n)
        use_prior = rng.random(n) < self.q_beta
        return (np.where(use_prior, kp, k), np.where(use_prior, xp, x), np.where(use_prior, yp, y),
                np.where(use_prior, tp, th))

    def _q_logpdf(self, C, k, x, y, th):
        """log q(s) of the defensive contact-conditioned mixture (closed form: Gaussian in theta per edge times a
        Gaussian-blurred uniform segment in translation)."""
        lib = self.lib
        from scipy.special import log_ndtr
        a = lib.p0[k]                                  # (N, V, 2)
        b = lib.p1[k]
        alpha = lib.normal_ang[k]                      # (N, V)
        m = lib.mask[k]
        c, s = np.cos(th)[:, None], np.sin(th)[:, None]
        out = []
        for cx, cy, cn in C:
            dth = wrap(th[:, None] - (cn - alpha))
            lth = -0.5 * (dth / self.q_sth) ** 2 - math.log(math.sqrt(2 * math.pi) * self.q_sth)
            Ax = cx - (c * a[..., 0] - s * a[..., 1]); Ay = cy - (s * a[..., 0] + c * a[..., 1])
            Dx = -(c * (b[..., 0] - a[..., 0]) - s * (b[..., 1] - a[..., 1]))
            Dy = -(s * (b[..., 0] - a[..., 0]) + c * (b[..., 1] - a[..., 1]))
            ln = np.where(m, np.hypot(Dx, Dy), 1.0)
            ex, ey = Dx / ln, Dy / ln
            vx, vy = x[:, None] - Ax, y[:, None] - Ay
            along = vx * ex + vy * ey
            perp = -vx * ey + vy * ex
            lperp = -0.5 * (perp / self.q_sxy) ** 2 - math.log(math.sqrt(2 * math.pi) * self.q_sxy)
            # log[Phi(along/s) - Phi((along-len)/s)] computed stably
            # log[Phi(a) - Phi(b)], a = along/s > b = (along-len)/s. When b > 0 both CDFs are ~1 and the difference
            # underflows; use the mirrored tail Phi(-b) - Phi(-a) there (root-cause fix of a log1p(-1) warning).
            a_, b_ = along / self.q_sxy, (along - ln) / self.q_sxy
            upper = b_ > 0
            hi = np.where(upper, log_ndtr(-b_), log_ndtr(a_))
            lo = np.where(upper, log_ndtr(-a_), log_ndtr(b_))
            lseg = hi + np.log1p(-np.exp(lo - hi))
            term = np.where(m, lth + lperp + lseg, -np.inf)
            out.append(logsumexp(term, axis=1) - np.log(self._perim[k]) - math.log(lib.K))
        lq_contact = logsumexp(np.stack(out, 0), axis=0) - math.log(len(C))
        lp = np.where(self.prior.inside(x, y), self.prior.log_density(), -np.inf)
        return np.logaddexp(math.log(self.q_beta) + lp, math.log(1 - self.q_beta) + lq_contact)

    def _mh_contact(self, C):
        """Mixture of two posterior-invariant MH kernels per particle: random walk, or independence sampler with the
        contact-conditioned proposal q (acceptance uses pi(s') q(s) / (pi(s) q(s')))."""
        lq_cur = self._q_logpdf(C, self.k, self.x, self.y, self.th)
        for _ in range(self.mh_steps):
            use_q = self.rng.random(self.n) < 0.5
            kq, xq, yq, tq = self._q_sample(C, self.n)
            xr = self.x + self.rw_xy * self.rng.standard_normal(self.n)
            yr = self.y + self.rw_xy * self.rng.standard_normal(self.n)
            tr = wrap(self.th + self.rw_th * self.rng.standard_normal(self.n))
            k2 = np.where(use_q, kq, self.k)
            x2, y2, t2 = np.where(use_q, xq, xr), np.where(use_q, yq, yr), np.where(use_q, tq, tr)
            ins = self.prior.inside(x2, y2)
            ll2 = self._hist_loglik(k2, x2, y2, t2)
            lq_new = self._q_logpdf(C, k2, x2, y2, t2)
            log_acc = ll2 - self.loglik_hist + np.where(use_q, lq_cur - lq_new, 0.0)
            log_acc = np.where(ins, log_acc, -np.inf)
            acc = np.log(self.rng.random(self.n)) < log_acc
            self.k = np.where(acc, k2, self.k)
            self.x, self.y, self.th = np.where(acc, x2, self.x), np.where(acc, y2, self.y), np.where(acc, t2, self.th)
            self.loglik_hist = np.where(acc, ll2, self.loglik_hist)
            lq_cur = np.where(acc, lq_new, lq_cur)

    # ---- read-outs ------------------------------------------------------------------------------------------------
    def weights(self) -> np.ndarray:
        return np.exp(self.logw - logsumexp(self.logw))

    def identity_mass(self) -> np.ndarray:
        return np.bincount(self.k, weights=self.weights(), minlength=self.prior.K)

    def estimate(self, refine_iters: int = 30):
        """MAP identity; pose = highest-posterior particle of that identity refined by Nelder-Mead on the log-posterior."""
        mass = self.identity_mass()
        kh = int(np.argmax(mass))
        sel = np.flatnonzero(self.k == kh)
        if len(sel) == 0:
            return kh, 0.0, 0.0, 0.0
        logpost = self.loglik_hist[sel]
        i = sel[np.argmax(logpost)]
        z0 = np.array([self.x[i], self.y[i], self.th[i]])

        def negpost(z):
            if not self.prior.inside(z[0], z[1]):
                return 1e12
            return -float(self._hist_loglik(np.array([kh]), np.array([z[0]]), np.array([z[1]]), np.array([z[2]]))[0])

        if refine_iters > 0 and self.hist:
            res = minimize(negpost, z0, method="Nelder-Mead",
                           options={"maxiter": refine_iters, "initial_simplex": z0 + np.array(
                               [[0, 0, 0], [0.5, 0, 0], [0, 0.5, 0], [0, 0, math.radians(0.5)]])})
            if res.fun <= negpost(z0):
                z0 = res.x
        return kh, float(z0[0]), float(z0[1]), float(wrap(z0[2]))

    def log_post_density(self, s0, bw_xy: float = 1.0, bw_th: float = math.radians(1.0)) -> float:
        """log p_hat(s0 | h): identity mass x weighted Gaussian KDE over that identity's particles, with rotation folded
        modulo the shape's symmetry group (density on the folded space)."""
        k0, x0, y0, t0 = s0
        w = self.weights()
        sel = self.k == k0
        if not sel.any():
            return -np.inf
        g = self.lib.sym[k0]
        dth = wrap(t0 - self.th[sel][:, None] - g[None, :])           # (n_sel, |G|)
        # folded density: sum over symmetric images, then the folded space has measure 2 pi / |G|
        lk_th = logsumexp(-0.5 * (dth / bw_th) ** 2, axis=1) - math.log(math.sqrt(2 * math.pi) * bw_th)
        lk_xy = (-0.5 * ((x0 - self.x[sel]) ** 2 + (y0 - self.y[sel]) ** 2) / bw_xy ** 2
                 - math.log(2 * math.pi * bw_xy ** 2))
        return float(logsumexp(np.log(w[sel]) + lk_xy + lk_th))

    def realized_ig_evidence(self, s0) -> float:
        """Primary IG_T estimator: log p(h_T | s0) - log p_hat(h_T), with p_hat(h_T) the SMC evidence estimate.
        Its expectation over (s0, h_T) under a policy is the policy's total EIG I(s; h_T) (up to the small, positive
        bias of the log-evidence estimate). Exact likelihood of the true state; no kernel density, so it does not
        degrade when the posterior is broad (deviation D3 from docs/07_hypotheses.md §1.3)."""
        k0, x0, y0, t0 = s0
        ll0 = float(self._hist_loglik(np.array([k0]), np.array([x0]), np.array([y0]), np.array([t0]))[0])
        return ll0 - self.log_evidence

    def ball_info(self, s0, r_xy: float = 5.0, r_th: float = math.radians(5.0)) -> float:
        """Decision-relevant information: log P_hat(B(s0) | h) - log P(B(s0)), where B(s0) is the success region
        (same identity, translation < r_xy, symmetry-folded rotation error < r_th). Bounded above by -log P(B); computed
        from PF masses only (no density estimate). Floored at log(1/n) on the posterior side."""
        k0, x0, y0, t0 = s0
        w = self.weights()
        g = self.lib.sym[k0]
        inb = ((self.k == k0) & (np.hypot(self.x - x0, self.y - y0) < r_xy)
               & (np.min(np.abs(wrap(self.th[:, None] - t0 - g[None, :])), axis=1) < r_th))
        post = max(float(w[inb].sum()), 1.0 / self.n)
        prior_mass = (1.0 / self.prior.K) * (math.pi * r_xy ** 2 / (2 * self.prior.xy_half) ** 2) * min(
            1.0, len(g) * 2 * r_th / (2 * math.pi))
        return math.log(post) - math.log(prior_mass)

    def realized_ig(self, s0, floor: float = 1e-3) -> float:
        """IG_T = log p_hat(s0 | h_T) - log p(s0) on the symmetry-folded space; floored at log(floor) (>= -6.9 nats)."""
        g = self.lib.sym[s0[0]]
        log_prior_folded = self.prior.log_density() + math.log(len(g))  # folded theta space has measure 2 pi / |G|
        lp = self.log_post_density(s0)
        return max(lp - log_prior_folded, math.log(floor))


def rot_err(lib, k0: int, t_hat: float, t0: float) -> float:
    g = lib.sym[k0]
    return float(np.min(np.abs(wrap(t_hat - t0 - g))))


def success(lib, est, s0, tol_xy: float = 5.0, tol_th: float = math.radians(5.0)) -> dict:
    kh, xh, yh, th = est
    k0, x0, y0, t0 = s0
    terr = math.hypot(xh - x0, yh - y0)
    rerr = rot_err(lib, k0, th, t0)
    ok_id = kh == k0
    return {"success": bool(ok_id and terr < tol_xy and rerr < tol_th), "identity_ok": bool(ok_id),
            "trans_err_mm": terr, "rot_err_deg": math.degrees(rerr)}
