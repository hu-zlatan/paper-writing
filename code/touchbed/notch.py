"""Exact notch control (docs/07_hypotheses.md §H2b-P2, docs/07b_theoretical_bounds_v2.md §4.4, gate G1).

Problem. Two shapes: P0 = 80 x 30 mm rectangle (object frame x in [-40, 40], y in [-15, 15]); P1 = the same rectangle
with a 6 mm wide, 4 mm deep notch in the top edge centred 20 mm from the left end (x in [-23, -17], floor at y = 11).
Known theta = 0, y = 0; unknown offset x on a 401-point grid over [-20, 20] mm; k uniform. Target: identity k.
Actions: vertical probes from above at world abscissa u (U_GRID), and one horizontal probe from the left (all
horizontal probes at heights |v| < 15 hit the identical left edge, so one representative suffices).
Observation (1-D informative coordinate; the remaining contact coordinates are identical for every state that hits and
are dropped): vertical -> NC if |u - x| > 40, else contact height z ~ N(15 or 11, sigma^2); horizontal -> z ~ N(x - 40,
sigma^2). eps-softened like the main model: p(y | s, a) = (1 - eps) p_geom + eps u, u = 1/2 on NC and 1/2 uniform
density on z in [-100, 100].

`exact_values` computes, by enumeration over the grid posterior and a fixed fine quadrature over z (trapezoid on 0.25 mm
grids covering every geometric value +- 6 sigma; outside that region the posterior equals the prior belief exactly),
the one-step EIG of every action and the optimal / greedy two-step identity information. These are the G1 references.
`NotchProblem` exposes the same model through the generic interface used by the Monte-Carlo look-ahead estimator
(touchbed/lookahead.py)."""
import math

import numpy as np

SIGMA = 1.0
EPS = 1e-3
ZLO, ZHI = -100.0, 100.0
X_GRID = np.linspace(-20.0, 20.0, 401)
U_GRID = np.arange(-70.0, 70.0 + 1e-9, 2.0)          # 71 vertical probes
N_ACT = len(U_GRID) + 1                               # + 1 horizontal probe (index N_ACT - 1)
H_ACT = N_ACT - 1
STATE_K = np.repeat([0, 1], len(X_GRID))
STATE_X = np.tile(X_GRID, 2)
NS = len(STATE_K)


def geom(a: int, k=STATE_K, x=STATE_X):
    """Geometric outcome: (hit bool array, z array)."""
    k, x = np.asarray(k), np.asarray(x, dtype=float)
    if a == H_ACT:
        return np.ones(x.shape, bool), x - 40.0
    p = U_GRID[a] - x
    hit = np.abs(p) <= 40.0
    z = np.where((k == 1) & (p >= -23.0) & (p <= -17.0), 11.0, 15.0)
    return hit, z


def lik_matrix(a: int, z_nodes: np.ndarray):
    """Likelihood of each z node (contact) and of NC under every state: (len(z) x NS), (NS,)."""
    hit, zg = geom(a)
    dens = np.exp(-0.5 * ((z_nodes[:, None] - zg[None, :]) / SIGMA) ** 2) / (math.sqrt(2 * math.pi) * SIGMA)
    Lz = (1 - EPS) * hit[None, :] * dens + EPS * 0.5 / (ZHI - ZLO)
    Lnc = (1 - EPS) * (~hit) + EPS * 0.5
    return Lz, Lnc


def z_nodes(a: int, step: float = 0.25, width: float = 6.0):
    """Trapezoid nodes covering every geometric z of action a +- width*sigma, and their weights."""
    _, zg = geom(a)
    lo, hi = float(zg.min()) - width * SIGMA, float(zg.max()) + width * SIGMA
    if a != H_ACT:   # two clusters (11, 15) overlap -> one interval
        lo, hi = 11.0 - width * SIGMA, 15.0 + width * SIGMA
    z = np.arange(lo, hi + 1e-9, step)
    w = np.full(len(z), step)
    w[0] = w[-1] = step / 2
    return z, w


class _Tables:
    def __init__(self, step=0.25, width=6.0):
        self.z, self.zw, self.Lz, self.Lnc, self.far = [], [], [], [], []
        for a in range(N_ACT):
            z, w = z_nodes(a, step, width)
            Lz, Lnc = lik_matrix(a, z)
            self.z.append(z); self.zw.append(w); self.Lz.append(Lz); self.Lnc.append(Lnc)
            self.far.append((ZHI - ZLO) - (z[-1] - z[0]))  # length of the region where only the eps branch lives
        self.step, self.width = step, width


def _H(p0, p1):
    s = p0 + p1
    q0 = np.where(s > 0, p0 / np.where(s > 0, s, 1), 0.5)
    q1 = 1 - q0
    with np.errstate(divide="ignore", invalid="ignore"):
        h = -(np.where(q0 > 0, q0 * np.log(q0), 0) + np.where(q1 > 0, q1 * np.log(q1), 0))
    return h


def eig_batch(W: np.ndarray, T: _Tables):
    """Exact one-step identity EIG of every action for a batch of beliefs W (B x NS, rows sum to 1): (B x N_ACT)."""
    W0 = W * (STATE_K == 0)
    W1 = W * (STATE_K == 1)
    Hb = _H(W0.sum(1), W1.sum(1))
    out = np.empty((W.shape[0], N_ACT))
    for a in range(N_ACT):
        m0 = W0 @ T.Lz[a].T
        m1 = W1 @ T.Lz[a].T                                # (B x nodes) joint densities p(k, z)
        Ez = ((m0 + m1) * _H(m0, m1) * T.zw[a][None, :]).sum(1)
        n0, n1 = W0 @ T.Lnc[a], W1 @ T.Lnc[a]
        Enc = (n0 + n1) * _H(n0, n1)
        far_mass = EPS * 0.5 / (ZHI - ZLO) * T.far[a]       # posterior = prior there (all states equal likelihood)
        out[:, a] = Hb - (Ez + Enc + far_mass * Hb)
    return out


def posteriors(w: np.ndarray, a: int, T: _Tables):
    """All quadrature posteriors after action a from belief w: (P x NS) posteriors, (P,) probabilities (incl. NC and
    the far region whose posterior is w itself)."""
    Lz, Lnc = T.Lz[a], T.Lnc[a]
    J = w[None, :] * Lz                                    # nodes x NS
    pz = J.sum(1) * T.zw[a]
    post = [J / J.sum(1, keepdims=True)]
    probs = [pz]
    jn = w * Lnc
    post.append((jn / jn.sum())[None, :]); probs.append(np.array([jn.sum()]))
    post.append(w[None, :]); probs.append(np.array([EPS * 0.5 / (ZHI - ZLO) * T.far[a]]))
    return np.concatenate(post, 0), np.concatenate(probs)


def two_step(w: np.ndarray, T: _Tables, greedy_first=None, chunk: int = 512):
    """Exact optimal and greedy two-step identity information from belief w.
    Returns dict(eig1 (N_ACT,), v2 (N_ACT,) = EIG(a1) + E_y1 max_a2 EIG(a2 | y1), v_opt, a_opt, a_greedy, v_greedy,
    prob_mass_check (N_ACT,) = total quadrature probability per a1, ideally 1)."""
    eig1 = eig_batch(w[None, :], T)[0]
    v2 = np.empty(N_ACT)
    mass = np.empty(N_ACT)
    for a in range(N_ACT):
        P, pr = posteriors(w, a, T)
        best = np.empty(len(P))
        for i in range(0, len(P), chunk):
            best[i:i + chunk] = eig_batch(P[i:i + chunk], T).max(1)
        v2[a] = eig1[a] + float((pr * best).sum())
        mass[a] = float(pr.sum())
    ag = int(np.argmax(eig1)) if greedy_first is None else int(greedy_first)
    ao = int(np.argmax(v2))
    return {"eig1": eig1, "v2": v2, "v_opt": float(v2[ao]), "a_opt": ao, "a_greedy": ag, "v_greedy": float(v2[ag]),
            "prob_mass_check": mass}


def prior_belief():
    return np.full(NS, 1.0 / NS)


# ---- generic interface for the Monte-Carlo look-ahead estimator ----------------------------------------------------
class NotchProblem:
    """Particles = the NS grid states (so belief updates are exact Bayes); target = identity; unit cost per probe,
    kappa = 0. Observations are (nc: bool, z: float)."""
    n_actions = N_ACT

    def __init__(self):
        self.k, self.x = STATE_K, STATE_X
        self._geo = [geom(a) for a in range(N_ACT)]

    def sample_obs(self, a: int, s: int, rng):
        hit, zg = self._geo[a]
        if rng.random() < EPS:      # eps branch
            if rng.random() < 0.5:
                return (True, 0.0)
            return (False, float(rng.uniform(ZLO, ZHI)))
        if not hit[s]:
            return (True, 0.0)
        return (False, float(zg[s] + SIGMA * rng.standard_normal()))

    def loglik(self, a: int, obs):
        hit, zg = self._geo[a]
        nc, z = obs
        if nc:
            return np.log((1 - EPS) * (~hit) + EPS * 0.5)
        dens = np.exp(-0.5 * ((z - zg) / SIGMA) ** 2) / (math.sqrt(2 * math.pi) * SIGMA)
        return np.log((1 - EPS) * hit * dens + EPS * 0.5 / (ZHI - ZLO))

    def target_logmass(self, logw: np.ndarray, s: int) -> float:
        w = np.exp(logw - logw.max()); w /= w.sum()
        return float(math.log(max(w[self.k == self.k[s]].sum(), 1e-300)))

    def sample_obs_batch(self, a: int, S: np.ndarray, rng):
        hit, zg = self._geo[a]
        n = len(S)
        e = rng.random(n) < EPS
        e_nc = rng.random(n) < 0.5
        zu = rng.uniform(ZLO, ZHI, n)
        zn = zg[S] + SIGMA * rng.standard_normal(n)
        nc = np.where(e, e_nc, ~hit[S])
        z = np.where(e, zu, zn)
        return nc, z

    def loglik_batch(self, a: int, nc: np.ndarray, z: np.ndarray):
        """(n_obs x NS) log-likelihoods."""
        hit, zg = self._geo[a]
        dens = np.exp(-0.5 * ((z[:, None] - zg[None, :]) / SIGMA) ** 2) / (math.sqrt(2 * math.pi) * SIGMA)
        lc = np.log((1 - EPS) * hit[None, :] * dens + EPS * 0.5 / (ZHI - ZLO))
        ln = np.log((1 - EPS) * (~hit) + EPS * 0.5)[None, :]
        return np.where(nc[:, None], ln, lc)

    def _mc(self, logw, actions, M, rng, full_state: bool):
        w = np.exp(logw - logw.max()); w /= w.sum()
        lw = np.log(np.maximum(w, 1e-300))
        lpk = np.log(np.array([w[self.k == 0].sum(), w[self.k == 1].sum()]) + 1e-300)
        out = np.empty(len(actions))
        for j, a in enumerate(actions):
            S = rng.choice(NS, size=M, p=w)
            nc, z = self.sample_obs_batch(a, S, rng)
            L = self.loglik_batch(a, nc, z) + lw[None, :]
            L -= L.max(1, keepdims=True)
            P = np.exp(L)
            Z = P.sum(1)
            if full_state:
                out[j] = float(np.mean(np.log(P[np.arange(M), S] / Z) - lw[S]))
            else:
                same = self.k[None, :] == self.k[S][:, None]
                out[j] = float(np.mean(np.log((P * same).sum(1) / Z) - lpk[self.k[S]]))
        return out

    def mc_eig(self, logw: np.ndarray, actions, M: int, rng):
        """Monte-Carlo identity EIG (M joint samples (s, y) per action, exact marginalisation over the particles)."""
        return self._mc(logw, list(actions), M, rng, full_state=False)

    def setup_moves(self, logw, budget, M: int = 64):
        """Structured set-up candidate (generic rule, amendment B6): the action of maximal full-state EIG."""
        rng = np.random.default_rng(12345)
        return [int(np.argmax(self._mc(logw, range(N_ACT), M, rng, full_state=True)))]

    def greedy(self, logw, budget_state, rng, M: int = 64):
        e = self.mc_eig(logw, range(N_ACT), M, rng)
        return int(np.argmax(e))

    # budget: number of probes left (unit costs)
    def step_budget(self, budget_state, a):
        return budget_state - 1

    def budget_left(self, budget_state) -> bool:
        return budget_state > 0


# ---- G1 helpers ----------------------------------------------------------------------------------------------------
def belief_after(history):
    """Exact grid posterior after a list of (action, (nc, z)) pairs, starting from the uniform prior."""
    P = NotchProblem()
    lw = np.log(prior_belief())
    for a, obs in history:
        lw = lw + P.loglik(a, obs)
    lw -= lw.max()
    w = np.exp(lw)
    return w / w.sum()


def make_zero_gap_bank(n: int = 100, seed: int = 2026, tol: float = 1e-3, max_tries: int = 400):
    """G1(b) bank: beliefs reached by one horizontal probe on a random true state (x localised to ~1 mm), with two
    probes left. A candidate is kept iff its EXACT relative gap (v_opt - v_greedy) / v_opt <= tol."""
    rng = np.random.default_rng(seed)
    P = NotchProblem()
    T = _Tables()
    bank, tried = [], 0
    while len(bank) < n and tried < max_tries:
        tried += 1
        s = int(rng.integers(NS))
        obs = P.sample_obs(H_ACT, s, rng)
        w = belief_after([(H_ACT, obs)])
        r = two_step(w, T)
        rel = (r["v_opt"] - r["v_greedy"]) / r["v_opt"] if r["v_opt"] > 0 else 0.0
        if rel <= tol:
            bank.append({"true_state": s, "history": [[H_ACT, [bool(obs[0]), float(obs[1])]]], "exact_v_opt": r["v_opt"],
                         "exact_v_greedy": r["v_greedy"], "exact_gap_rel": rel, "a_opt": r["a_opt"], "a_greedy": r["a_greedy"]})
    return {"seed": seed, "tol": tol, "tried": tried, "bank": bank}
