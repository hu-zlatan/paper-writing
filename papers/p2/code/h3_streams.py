"""H3 streams (07_hypotheses H3 / H3-x, addendum 08d): per-stratum score-space OQT with anti-windup, decaying-step OQT,
frozen offline q-hat and oracle recalibration, on label-rule feedback slip_t = 1{F_t < F*_hi,t} (unavoidable -> slip,
capped). Vectorised over (bootstrap draw x ordering) streams.

  python h3_streams.py schedules    -> results/v1/h3/schedule_<shift>.json (ordering 0 force schedules for the direct-
                                       replay audits of 08d §3; no metric is printed)
  python h3_streams.py analyse [--draws 2000] [--audit]
                                    -> results/v1/h3_analysis.json (20 orderings, bootstrap CI**, H3 decision; with
                                       --audit also joins results/v1/h3/replay/*.jsonl, refusing if incomplete)
"""
import argparse
import glob
import json
import math
import os

import numpy as np

from certgrip.baselines import f_nom
from certgrip.conformal import qhat
from certgrip.data import h3_role
from certgrip.io import ROOT, key, load_rows

ALPHA, F_MAX, T_PRE, T_SHIFT, N_ORD = 0.10, 100.0, 500, 1500, 20
WIN = slice(1000, 2000)                    # steps 1,001-2,000 (0-based 1000..1999)
STRATA = ("D1", "D2", "D3", "D4")
SHIFTS = ("S1", "S2", "S3", "S1m", "ID")
CERT_PRED = "a010_full_rd_s0.2_seed0"
LO_P, HI_P, MARGIN = 1.25, 98.75, 1.10


# ---------------------------------------------------------------- data
def _arr(rows, lg_cert, lg_comp):
    return {"key": [key(r) for r in rows], "obj": [(r["family"], r["obj"], r["pool"]) for r in rows],
            "st": np.array([STRATA.index(r["dist"]) for r in rows]),
            "lg": np.stack([lg_cert, lg_comp], 1),
            "fhi": np.array([r["F_hi"] if not r["unavoidable"] else np.inf for r in rows]),
            "fmid": np.array([r["F_mid"] if not r["unavoidable"] else np.nan for r in rows]),
            "avoid": np.array([not r["unavoidable"] for r in rows])}


def load_pools():
    rows = load_rows("v1/labels/*.jsonl")
    p = json.load(open(os.path.join(ROOT, "v1/preds", CERT_PRED + ".json")))
    import hashlib
    assert p["keys_sha256"] == hashlib.sha256(json.dumps([list(key(r)) for r in rows]).encode()).hexdigest()
    lc = dict(zip([key(r) for r in rows], p["log_pred"]))
    comp = {key(r): math.log(f_nom(r["inst"]["mass"], r["dist"], r["inst"]["amp"], r["inst"]["freq"])) for r in rows}

    def pool(sel):
        rs = [r for r in rows if sel(r)]
        return _arr(rs, np.array([lc[key(r)] for r in rs]), np.array([comp[key(r)] for r in rs]))

    cal = [r for r in rows if r["pool"] == "id" and r["shift"] is None and r["split"] == "cal"]
    out = {"cal": pool(lambda r: r in cal)}
    pre = pool(lambda r: r["pool"] == "id" and r["shift"] is None and h3_role("id", r["obj"]) == "oracle")
    for s in SHIFTS:
        if s == "S2":
            orc = pool(lambda r: r["pool"] == "s2" and r["split"] == "oracle")
            stm = pool(lambda r: r["pool"] == "s2" and r["split"] == "stream")
        elif s == "ID":
            orc = pre
            stm = pool(lambda r: r["pool"] == "id" and r["shift"] is None and h3_role("id", r["obj"]) == "stream")
        else:
            orc = pool(lambda r, s=s: r["pool"] == "id" and r["shift"] == s and h3_role("id", r["obj"]) == "oracle")
            stm = pool(lambda r, s=s: r["pool"] == "id" and r["shift"] == s and h3_role("id", r["obj"]) == "stream")
        out[s] = {"pre": pre, "oracle": orc, "stream": stm}
    return out


def offline(cal):
    """Per-stratum offline label-rule q-hat for both arms, and eta = 0.1 x IQR of CertGrip's pooled cal scores."""
    a = cal["avoid"]
    sc = np.log(cal["fhi"][a])[:, None] - cal["lg"][a]
    q = np.array([[qhat(sc[cal["st"][a] == k, j], ALPHA) for j in range(2)] for k in range(4)])   # (4 strata, 2 arms)
    q75, q25 = np.percentile(sc[:, 0], [75, 25])
    return q, float(0.1 * (q75 - q25))


def oracle_q(orc, idx):
    a = orc["avoid"][idx]
    sc = np.log(orc["fhi"][idx][a])[:, None] - orc["lg"][idx][a]
    st = orc["st"][idx][a]
    return np.array([[qhat(sc[st == k, j], ALPHA) for j in range(2)] for k in range(4)])


# ---------------------------------------------------------------- simulation
def run_streams(lg, fhi, st, q0, eta, decay=False):
    """lg, fhi, st: (B, T); q0: (B, 4) initial per-stratum q. Returns F (B, T), slip (B, T), capped (B, T)."""
    B, T = lg.shape
    q = q0.copy()
    n_upd = np.zeros((B, 4))
    F = np.empty((B, T)); slip = np.empty((B, T), bool); cap = np.empty((B, T), bool)
    rb = np.arange(B)
    for t in range(T):
        s = st[:, t]
        qs = q[rb, s]
        f = np.exp(lg[:, t] + qs)
        c = f >= F_MAX
        f = np.minimum(f, F_MAX)
        sl = f < fhi[:, t]
        F[:, t], slip[:, t], cap[:, t] = f, sl, c
        step = eta / np.sqrt(n_upd[rb, s] + 1) if decay else eta
        upd = ~c
        q[rb[upd], s[upd]] = qs[upd] + (step if np.isscalar(step) else step[upd]) * (sl[upd] - ALPHA)
        n_upd[rb[upd], s[upd]] += 1
    return F, slip, cap


def fixed_streams(lg, fhi, st, q_pre, q_post):
    """Frozen / oracle: q_pre (B, 4) for steps < T_PRE, q_post (B, 4) after."""
    B, T = lg.shape
    rb = np.arange(B)[:, None]
    q = np.where(np.arange(T)[None, :] < T_PRE, q_pre[rb, st], q_post[rb, st])
    F = np.exp(lg + q)
    cap = F >= F_MAX
    F = np.minimum(F, F_MAX)
    return F, F < fhi, cap


def orderings(n_pre, n_stm, shift_i, n_ord=N_ORD, rng=None, ordering_offset=0):
    """Index arrays (n_ord, T) into concat(pre, stream) pools; without replacement within each segment."""
    out = []
    for o in range(n_ord):
        g = rng if rng is not None else np.random.default_rng([4242, shift_i, o + ordering_offset])
        pre = g.choice(n_pre, T_PRE, replace=False)
        stm = g.choice(n_stm, T_SHIFT, replace=False) + n_pre
        out.append(np.concatenate([pre, stm]))
    return np.array(out)


def metrics(F, slip, cap, fmid, avoid):
    w = slice(WIN.start, WIN.stop)
    Fw, mw, aw = F[:, w], fmid[:, w], avoid[:, w]
    re = np.where(aw, (Fw - np.where(aw, mw, 1.0)) / np.where(aw, mw, 1.0), 0.0).sum(1) / aw.sum(1)
    return {"RE_window": re, "slip_label_window": slip[:, w].mean(1), "capped_window": cap[:, w].mean(1),
            "slip_label_all": slip.mean(1)}


ARMS = ("OQT-CertGrip", "OQT-COMP", "OQTdecay-CertGrip", "Frozen-CertGrip", "Frozen-COMP", "Oracle-CertGrip",
        "Oracle-COMP")


def simulate(P, qoff, eta, qorc, idx):
    """P: dict pre/stream pools concatenated arrays; idx: (B, T) indices; qorc: (B, 4, 2). Returns per-arm streams."""
    lg, fhi, st = P["lg"][idx], P["fhi"][idx], P["st"][idx]
    B = idx.shape[0]
    q0 = np.broadcast_to(qoff, (B, 4, 2))
    res = {}
    res["OQT-CertGrip"] = run_streams(lg[..., 0], fhi, st, q0[..., 0], eta)
    res["OQT-COMP"] = run_streams(lg[..., 1], fhi, st, q0[..., 1], eta)
    res["OQTdecay-CertGrip"] = run_streams(lg[..., 0], fhi, st, q0[..., 0], eta, decay=True)
    res["Frozen-CertGrip"] = fixed_streams(lg[..., 0], fhi, st, q0[..., 0], q0[..., 0])
    res["Frozen-COMP"] = fixed_streams(lg[..., 1], fhi, st, q0[..., 1], q0[..., 1])
    res["Oracle-CertGrip"] = fixed_streams(lg[..., 0], fhi, st, q0[..., 0], qorc[..., 0])
    res["Oracle-COMP"] = fixed_streams(lg[..., 1], fhi, st, q0[..., 1], qorc[..., 1])
    return res


def concat(pre, stm):
    return {k: (np.concatenate([pre[k], stm[k]]) if isinstance(pre[k], np.ndarray) else pre[k] + stm[k]) for k in pre}


def shift_summary(pools, s, qoff, eta, n_ord=N_ORD):
    """Point estimate over the 20 fixed orderings."""
    pr, orc, stm = pools[s]["pre"], pools[s]["oracle"], pools[s]["stream"]
    P = concat(pr, stm)
    idx = orderings(len(pr["st"]), len(stm["st"]), SHIFTS.index(s), n_ord)
    qo = np.broadcast_to(oracle_q(orc, np.arange(len(orc["st"]))), (n_ord, 4, 2))
    res = simulate(P, qoff, eta, qo, idx)
    fmid, avoid = P["fmid"][idx], P["avoid"][idx]
    return {a: {k: float(v.mean()) for k, v in metrics(*res[a], fmid, avoid).items()} for a in ARMS}, res, idx, P


def bootstrap(pools, s, qoff, eta, draws, chunk=50, seed=777, n_ord=N_ORD):
    """Object-cluster bootstrap within family: pre+oracle objects resampled together (same id objects for paired
    shifts), stream objects separately; orderings regenerated; oracle q-hat refitted. Returns per-draw ordering-averaged
    RE_window per arm."""
    pr, orc, stm = pools[s]["pre"], pools[s]["oracle"], pools[s]["stream"]
    rng = np.random.default_rng([seed, SHIFTS.index(s)])

    def by_obj(pool):
        d = {}
        for i, o in enumerate(pool["obj"]):
            d.setdefault((o[0], o[1]), []).append(i)
        return d

    po, oo, so = by_obj(pr), by_obj(orc), by_obj(stm)
    fam_objs = lambda keys: {f: sorted(k for k in keys if k[0] == f) for f in sorted({k[0] for k in keys})}
    po_f, oo_f, so_f = fam_objs(po), fam_objs(oo), fam_objs(so)
    paired = s in ("S1", "S3", "S1m", "ID")
    out = {a: [] for a in ARMS}
    out["slip_phys_proxy"] = []
    done = 0
    while done < draws:
        n = min(chunk, draws - done)
        idx_all, qorc_all, Pjoin = [], [], []
        lg_l, fhi_l, st_l, fmid_l, av_l = [], [], [], [], []
        for _ in range(n):
            if paired:
                pick = {f: [ks[j] for j in rng.integers(0, len(ks), len(ks))] for f, ks in po_f.items()}
                pi = [i for ks in pick.values() for k in ks for i in po[k]]
                oi = [i for ks in pick.values() for k in ks for i in oo.get(k, [])]
            else:
                pi = [i for f, ks in po_f.items() for j in rng.integers(0, len(ks), len(ks)) for i in po[ks[j]]]
                oi = [i for f, ks in oo_f.items() for j in rng.integers(0, len(ks), len(ks)) for i in oo[ks[j]]]
            si = [i for f, ks in so_f.items() for j in rng.integers(0, len(ks), len(ks)) for i in so[ks[j]]]
            qo = oracle_q(orc, np.array(oi))
            pi, si = np.array(pi), np.array(si)
            for o in range(n_ord):
                a = pi[rng.choice(len(pi), T_PRE, replace=False)]
                b = si[rng.choice(len(si), T_SHIFT, replace=False)]
                lg_l.append(np.concatenate([pr["lg"][a], stm["lg"][b]]))
                fhi_l.append(np.concatenate([pr["fhi"][a], stm["fhi"][b]]))
                st_l.append(np.concatenate([pr["st"][a], stm["st"][b]]))
                fmid_l.append(np.concatenate([pr["fmid"][a], stm["fmid"][b]]))
                av_l.append(np.concatenate([pr["avoid"][a], stm["avoid"][b]]))
                qorc_all.append(qo)
        P = {"lg": np.array(lg_l), "fhi": np.array(fhi_l), "st": np.array(st_l)}
        idx = None
        B = len(lg_l)
        qoffB = np.broadcast_to(qoff, (B, 4, 2))
        qorcB = np.array(qorc_all)
        res = {}
        res["OQT-CertGrip"] = run_streams(P["lg"][..., 0], P["fhi"], P["st"], qoffB[..., 0], eta)
        res["OQT-COMP"] = run_streams(P["lg"][..., 1], P["fhi"], P["st"], qoffB[..., 1], eta)
        res["OQTdecay-CertGrip"] = run_streams(P["lg"][..., 0], P["fhi"], P["st"], qoffB[..., 0], eta, decay=True)
        res["Frozen-CertGrip"] = fixed_streams(P["lg"][..., 0], P["fhi"], P["st"], qoffB[..., 0], qoffB[..., 0])
        res["Frozen-COMP"] = fixed_streams(P["lg"][..., 1], P["fhi"], P["st"], qoffB[..., 1], qoffB[..., 1])
        res["Oracle-CertGrip"] = fixed_streams(P["lg"][..., 0], P["fhi"], P["st"], qoffB[..., 0], qorcB[..., 0])
        res["Oracle-COMP"] = fixed_streams(P["lg"][..., 1], P["fhi"], P["st"], qoffB[..., 1], qorcB[..., 1])
        fmid, av = np.array(fmid_l), np.array(av_l)
        for a in ARMS:
            m = metrics(*res[a], fmid, av)
            out[a].append(np.stack([m["RE_window"].reshape(n, n_ord).mean(1),
                                    m["slip_label_window"].reshape(n, n_ord).mean(1)], 1))
        done += n
    return {a: np.concatenate(out[a]) for a in ARMS}


# ---------------------------------------------------------------- commands
def cmd_schedules(pools, qoff, eta):
    os.makedirs(os.path.join(ROOT, "v1/h3"), exist_ok=True)
    plan = {"S1": [("OQT-CertGrip", "OQT-COMP", 500, 1000), ("OQT-CertGrip", "Oracle-CertGrip", 1000, 2000)],
            "S2": [("OQT-CertGrip", "OQT-COMP", 500, 1000), ("OQT-CertGrip", "Oracle-CertGrip", 1000, 2000)],
            "S3": [("OQT-CertGrip", "OQT-COMP", 500, 1000), ("OQT-CertGrip", "Oracle-CertGrip", 1000, 2000)],
            "S1m": [("OQT-CertGrip", "OQT-COMP", 500, 1000)]}
    for s, audits in plan.items():
        _, res, idx, P = shift_summary(pools, s, qoff, eta, n_ord=1)
        rows = {}
        for (x, y, a0, a1) in audits:
            for arm in (x, y):
                for t in range(a0, a1):
                    k = P["key"][idx[0, t]]
                    rows.setdefault((arm, t), {"arm": arm, "step": t, "key": list(k), "F": round(float(res[arm][0][0, t]), 9),
                                               "slip_label": bool(res[arm][1][0, t])})
        json.dump({"shift": s, "ordering": 0, "eta": eta, "audits": [list(a) for a in audits],
                   "rows": list(rows.values())}, open(os.path.join(ROOT, f"v1/h3/schedule_{s}.json"), "w"))
        print(f"{s}: {len(rows)} audit replays scheduled")


def decide(ci):
    if ci[1] < MARGIN:
        return "non-inferior"
    if ci[0] > MARGIN:
        return "failure"
    return "inconclusive"


def cmd_analyse(pools, qoff, eta, draws, audit):
    out = {"purpose": "p2 H3 streams (07 H3, addendum 08d): label-rule feedback, 20 orderings, bootstrap CI** 97.5 %",
           "eta": eta, "q_offline": qoff.tolist(), "draws": draws, "shifts": {}}
    for s in SHIFTS:
        point, *_ = shift_summary(pools, s, qoff, eta)
        bs = bootstrap(pools, s, qoff, eta, draws)
        rr = bs["OQT-CertGrip"][:, 0] / bs["Oracle-CertGrip"][:, 0]
        RE = point["OQT-CertGrip"]["RE_window"] / point["Oracle-CertGrip"]["RE_window"]
        ci = [float(np.percentile(rr, LO_P)), float(np.percentile(rr, HI_P))]
        rho = math.log(point["OQT-CertGrip"]["RE_window"] / point["OQT-COMP"]["RE_window"])
        rho_b = np.log(bs["OQT-CertGrip"][:, 0] / bs["OQT-COMP"][:, 0])
        out["shifts"][s] = {"arms": point, "R_E": RE, "R_E_CI**": ci, "decision": decide(ci),
                            "rho": rho, "rho_boot": rho_b.tolist(),
                            "matched_label_window_diff": point["OQT-CertGrip"]["slip_label_window"]
                            - point["Oracle-CertGrip"]["slip_label_window"],
                            "arms_RE_CI**": {a: [float(np.percentile(bs[a][:, 0], LO_P)),
                                                 float(np.percentile(bs[a][:, 0], HI_P))] for a in ARMS}}
    for s in ("S1", "S2", "S3", "S1m"):
        d = np.array(out["shifts"][s]["rho_boot"]) - np.array(out["shifts"]["ID"]["rho_boot"])
        out["shifts"][s]["rho_minus_rhoID"] = out["shifts"][s]["rho"] - out["shifts"]["ID"]["rho"]
        out["shifts"][s]["rho_minus_rhoID_CI**"] = [float(np.percentile(d, LO_P)), float(np.percentile(d, HI_P))]
    for s in SHIFTS:
        out["shifts"][s].pop("rho_boot")
    out["H3_primary"] = {s: out["shifts"][s]["decision"] for s in ("S1", "S2", "S3")}
    if audit:
        out["audit"] = join_audit()
    json.dump(out, open(os.path.join(ROOT, "v1/h3_analysis.json"), "w"), indent=1)
    for s in ("S1", "S2", "S3"):
        print(f"{s}: R_E {out['shifts'][s]['R_E']:.3f} CI** {out['shifts'][s]['R_E_CI**']} -> {out['shifts'][s]['decision']}")


def join_audit():
    res = {}
    rep = {}
    for f in glob.glob(os.path.join(ROOT, "v1/h3/replay/*.jsonl")):
        for line in open(f):
            r = json.loads(line)
            if "arm" in r:
                rep[(r["shift"], r["arm"], r["step"])] = r
    for f in sorted(glob.glob(os.path.join(ROOT, "v1/h3/schedule_*.json"))):
        S = json.load(open(f))
        s = S["shift"]
        miss = [r for r in S["rows"] if (s, r["arm"], r["step"]) not in rep]
        if miss:
            raise SystemExit(f"audit incomplete for {s}: {len(miss)} missing")
        for (x, y, a0, a1) in S["audits"]:
            for arm in (x, y):
                rs = [r for r in S["rows"] if r["arm"] == arm and a0 <= r["step"] < a1]
                d = np.array([rep[(s, arm, r["step"])]["slip"] for r in rs], float)
                lab = np.array([r["slip_label"] for r in rs], float)
                objs = [(r["key"][1], r["key"][2]) for r in rs]
                res[f"{s}|{arm}|{a0 + 1}-{a1}"] = {"n": len(rs), "slip_direct": float(d.mean()),
                                                     "slip_label": float(lab.mean()),
                                                     "Delta": float((d - lab).mean()),
                                                     "Delta_CI**": cluster_ci(d - lab, objs)}
    for s in ("S1", "S2", "S3"):
        a, b = res.get(f"{s}|OQT-CertGrip|1001-2000"), res.get(f"{s}|Oracle-CertGrip|1001-2000")
        if a and b:
            res[f"{s}|matched_physical"] = {"diff": a["slip_direct"] - b["slip_direct"],
                                            "matched": abs(a["slip_direct"] - b["slip_direct"]) <= 0.02}
    return res


def cluster_ci(v, objs, draws=2000, seed=99):
    rng = np.random.default_rng(seed)
    g = {}
    for i, o in enumerate(objs):
        g.setdefault(o, []).append(i)
    ks = list(g)
    sums = np.array([v[g[k]].sum() for k in ks]); cnt = np.array([len(g[k]) for k in ks])
    b = []
    for _ in range(draws):
        j = rng.integers(0, len(ks), len(ks))
        b.append(sums[j].sum() / cnt[j].sum())
    return [float(np.percentile(b, LO_P)), float(np.percentile(b, HI_P))]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["schedules", "analyse"])
    ap.add_argument("--draws", type=int, default=2000)
    ap.add_argument("--audit", action="store_true")
    a = ap.parse_args()
    pools = load_pools()
    qoff, eta = offline(pools["cal"])
    if a.cmd == "schedules":
        cmd_schedules(pools, qoff, eta)
    else:
        cmd_analyse(pools, qoff, eta, a.draws, a.audit)


if __name__ == "__main__":
    main()
