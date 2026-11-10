"""Amendment 09 §B3 (plan `plans/stage_13_v2_b3_online_physical.md`): online quantile tracking with PHYSICAL slip
feedback. Per-stratum tracker warm-started from the 08c CRC lambda-hat; each step replays the instance (protocol rd)
at the issued force and feeds the replayed slip back. Pools / orderings / eta exactly as h3_streams.py (08d).

  python b3_online.py run --shift S1 --ordering 0 --arm CertGrip [--steps 2000] --out ../results/v2/b3/S1_o0_CertGrip
  python b3_online.py analyse      -> ../results/v2/b3_analysis.json (refuses unless all 20 streams are complete)
"""
import argparse
import glob
import json
import math
import os
import time

import numpy as np

import h3_streams as H
from certgrip.data import make_instance
from certgrip.io import ROOT
from certgrip.sim import Sim, preload_force
from main import SLIP

ARMS = {"CertGrip": ("full_rd@0.2#0", 0), "CSF1": ("CSF-1", 1)}     # crc arm name, column of pools[...]["lg"]
SHIFTS_B3, ORDS = ("S1", "S3"), (0, 1, 2, 3, 4)
WINDOWS = {"1-500": (0, 500), "1001-2000": (1000, 2000), "1501-2000": (1500, 2000)}


def crc_q0(arm):
    G = json.load(open(os.path.join(ROOT, "v1/crc_grids.json")))
    C = json.load(open(os.path.join(ROOT, "v1/crc_analysis.json")))
    A, li = G["arms"][arm], C["arms"][arm]["lam_idx"]
    return np.array([(A["grids"][d] if "grids" in A else A["grid"])[li[d]] for d in H.STRATA])


def stream_inputs(pools, shift, o):
    P = H.concat(pools[shift]["pre"], pools[shift]["stream"])
    idx = H.orderings(len(pools[shift]["pre"]["st"]), len(pools[shift]["stream"]["st"]), H.SHIFTS.index(shift), n_ord=o + 1)[o]
    return P, idx


def tracker(lg, st, q0, eta, feedback):
    """Generic per-stratum OQT. feedback(t, F) -> bool slip. Returns F, slip, capped, q-before-step arrays."""
    q = q0.astype(float).copy()
    T = len(lg)
    F, slip, cap, qs = np.empty(T), np.empty(T, bool), np.empty(T, bool), np.empty(T)
    for t in range(T):
        s = st[t]
        qs[t] = q[s]
        f = math.exp(lg[t] + q[s])
        c = f >= H.F_MAX
        f = min(f, H.F_MAX)
        sl = bool(feedback(t, f))
        F[t], slip[t], cap[t] = f, sl, c
        if not c:
            q[s] += eta * (sl - H.ALPHA)
    return F, slip, cap, qs


def cmd_run(a):
    pools = H.load_pools()
    _, eta = H.offline(pools["cal"])
    crc_arm, col = ARMS[a.arm]
    q0 = crc_q0(crc_arm)
    P, idx = stream_inputs(pools, a.shift, a.ordering)
    idx = idx[:a.steps]
    lg, st = P["lg"][idx, col], P["st"][idx]
    os.makedirs(os.path.dirname(os.path.abspath(a.out)), exist_ok=True)
    t0 = time.time()
    f = open(a.out + ".jsonl", "w")
    f.write(json.dumps({"header": True, "cmd": "b3", "shift": a.shift, "ordering": a.ordering, "arm": a.arm,
                        "crc_arm": crc_arm, "q0": q0.tolist(), "eta": eta, "steps": len(idx)}) + "\n")

    def feedback(t, F):
        pool, fam, obj, d, sh = P["key"][idx[t]]
        sim = Sim(make_instance(pool, fam, obj, d, sh), preload_force(), delta_t=SLIP["delta_t"],
                  rot_t_deg=SLIP["rot_t_deg"], protocol="rd")
        out = sim.run(F)
        f.write(json.dumps({"step": t, "key": list(P["key"][idx[t]]), "F": round(F, 9), "slip": bool(out["slip"]),
                            "capped": F >= H.F_MAX}) + "\n")
        f.flush()
        return out["slip"]

    tracker(lg, st, q0, eta, feedback)
    f.close()
    print(f"steps: {len(idx)}")
    print(f"seconds: {time.time() - t0:.1f}")


def load_stream(path):
    rows = [json.loads(l) for l in open(path)]
    return rows[0], rows[1:]


def cmd_analyse(a):
    pools = H.load_pools()
    qoff, eta = H.offline(pools["cal"])
    out = {"purpose": "p2 amendment 09 B3: online OQT with physical slip feedback, 08c CRC warm start (descriptive)",
           "eta": eta, "windows": list(WINDOWS), "shifts": {}}
    for s in SHIFTS_B3:
        res = {arm: {w: {"slip_phys": [], "RE_mid": []} for w in WINDOWS} for arm in ARMS}
        lab = {arm: {w: {"slip_label": [], "RE_mid": []} for w in WINDOWS} for arm in ARMS}
        for o in ORDS:
            P, idx = stream_inputs(pools, s, o)
            fmid, avoid = P["fmid"][idx], P["avoid"][idx]
            for arm, (_, col) in ARMS.items():
                path = os.path.join(ROOT, f"v2/b3/{s}_o{o}_{arm}.jsonl")
                if not os.path.exists(path):
                    raise SystemExit(f"missing {path}")
                hd, rows = load_stream(path)
                if len(rows) != H.T_PRE + H.T_SHIFT or [r["step"] for r in rows] != list(range(len(rows))):
                    raise SystemExit(f"incomplete {path}: {len(rows)} rows")
                assert [tuple(r["key"]) for r in rows] == [P["key"][i] for i in idx]
                F = np.array([r["F"] for r in rows]); sl = np.array([r["slip"] for r in rows], float)
                # label-rule OQT on the same ordering (08d simulator, offline label-rule q-hat start), for reference
                Fl, sll, _ = H.run_streams(P["lg"][idx, col][None], P["fhi"][idx][None], P["st"][idx][None],
                                           qoff[None, :, col], eta)
                for w, (t0, t1) in WINDOWS.items():
                    av = avoid[t0:t1]
                    res[arm][w]["slip_phys"].append(float(sl[t0:t1].mean()))
                    res[arm][w]["RE_mid"].append(float(((F[t0:t1][av] - fmid[t0:t1][av]) / fmid[t0:t1][av]).mean()))
                    lab[arm][w]["slip_label"].append(float(sll[0, t0:t1].mean()))
                    lab[arm][w]["RE_mid"].append(float(((Fl[0, t0:t1][av] - fmid[t0:t1][av]) / fmid[t0:t1][av]).mean()))
        summ = lambda v: {"mean": float(np.mean(v)), "min": float(np.min(v)), "max": float(np.max(v)), "per_ordering": v}
        S = {"physical_feedback": {arm: {w: {k: summ(v) for k, v in d.items()} for w, d in res[arm].items()} for arm in ARMS},
             "label_feedback_08d": {arm: {w: {k: summ(v) for k, v in d.items()} for w, d in lab[arm].items()} for arm in ARMS},
             "D_RE": {w: 1 - np.mean(res["CertGrip"][w]["RE_mid"]) / np.mean(res["CSF1"][w]["RE_mid"]) for w in WINDOWS}}
        out["shifts"][s] = S
    json.dump(out, open(os.path.join(ROOT, "v2/b3_analysis.json"), "w"), indent=1)
    for s in SHIFTS_B3:
        for arm in ARMS:
            for w in WINDOWS:
                r = out["shifts"][s]["physical_feedback"][arm][w]
                print(f"{s} {arm} {w}: slip_phys {r['slip_phys']['mean']:.4f} RE {r['RE_mid']['mean']:.4f}")
        print(f"{s} D_RE: " + ", ".join(f"{w} {v:.4f}" for w, v in out["shifts"][s]["D_RE"].items()))


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    r = sub.add_parser("run")
    r.add_argument("--shift", required=True, choices=SHIFTS_B3)
    r.add_argument("--ordering", type=int, required=True, choices=ORDS)
    r.add_argument("--arm", required=True, choices=list(ARMS))
    r.add_argument("--steps", type=int, default=H.T_PRE + H.T_SHIFT)
    r.add_argument("--out", required=True)
    sub.add_parser("analyse")
    a = ap.parse_args()
    cmd_run(a) if a.cmd == "run" else cmd_analyse(a)


if __name__ == "__main__":
    main()
