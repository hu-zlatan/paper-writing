"""Amendment 10 §B3 (p2 v3): the 09 B3 online study with physical feedback, extended to shifts S1 / S2 / S3 and
orderings 0-19 (08d orderings, seed [4242, shift, o]), same arms, warm start, eta and tracker as code/b3_online.py.
Streams (S1 | S3, o 0-4) are identical by construction to the v2 runs in results/v2/b3/ and are reused (the run
command refuses to overwrite and the analysis reads them from v2); all other streams go to results/v3/b3/.

  python b3v3_online.py run --shift S2 --ordering 7 --arm CertGrip --out ../results/v3/b3/S2_o7_CertGrip
  python b3v3_online.py analyse   -> ../results/v3/b3_analysis.json (refuses unless all 120 streams are complete)

Read-out (descriptive): per arm, shift and window (1-500, 501-1000 transient, 1001-2000, 1501-2000) the mean over the
20 orderings of physical slip and RE (avoidable rows, F*_mid), with 95 % ordering-bootstrap intervals (2,000 draws,
seed 1010); D_RE = 1 - mean RE_CertGrip / mean RE_CSF1 with its paired ordering-bootstrap interval. The 08d label-route
oracle rows (results/v1/h3_analysis.json) are printed alongside as the reference, as registered."""
import argparse
import json
import os
import sys

import numpy as np

import b3_online as B
import h3_streams as H
from certgrip.io import ROOT

SHIFTS3, ORDS3 = ("S1", "S2", "S3"), tuple(range(20))
WINDOWS3 = {"1-500": (0, 500), "501-1000": (500, 1000), "1001-2000": (1000, 2000), "1501-2000": (1500, 2000)}


def path_of(s, o, arm):
    if s in B.SHIFTS_B3 and o in B.ORDS:
        return os.path.join(ROOT, f"v2/b3/{s}_o{o}_{arm}.jsonl")
    return os.path.join(ROOT, f"v3/b3/{s}_o{o}_{arm}.jsonl")


def cmd_run(a):
    if a.shift in B.SHIFTS_B3 and a.ordering in B.ORDS:
        sys.exit("stream already run in v2 (results/v2/b3); reused, not re-run")
    B.cmd_run(a)


def boot_ci(v, draws=2000, seed=1010):
    v = np.asarray(v, float)
    rng = np.random.default_rng(seed)
    m = [v[rng.integers(0, len(v), len(v))].mean() for _ in range(draws)]
    return [float(np.percentile(m, 2.5)), float(np.percentile(m, 97.5))]


def cmd_analyse(a):
    pools = H.load_pools()
    _, eta = H.offline(pools["cal"])
    out = {"purpose": "p2 amendment 10 B3: online OQT with physical feedback, S1-S3 x 20 orderings (descriptive)",
           "eta": eta, "windows": list(WINDOWS3), "shifts": {}}
    for s in SHIFTS3:
        res = {arm: {w: {"slip_phys": [], "RE_mid": []} for w in WINDOWS3} for arm in B.ARMS}
        for o in ORDS3:
            P, idx = B.stream_inputs(pools, s, o)
            fmid, avoid = P["fmid"][idx], P["avoid"][idx]
            for arm in B.ARMS:
                p = path_of(s, o, arm)
                if not os.path.exists(p):
                    raise SystemExit(f"missing {p}")
                _, rows = B.load_stream(p)
                if len(rows) != H.T_PRE + H.T_SHIFT or [r["step"] for r in rows] != list(range(len(rows))):
                    raise SystemExit(f"incomplete {p}: {len(rows)} rows")
                assert [tuple(r["key"]) for r in rows] == [P["key"][i] for i in idx]
                F = np.array([r["F"] for r in rows]); sl = np.array([r["slip"] for r in rows], float)
                for w, (t0, t1) in WINDOWS3.items():
                    av = avoid[t0:t1]
                    res[arm][w]["slip_phys"].append(float(sl[t0:t1].mean()))
                    res[arm][w]["RE_mid"].append(float(((F[t0:t1][av] - fmid[t0:t1][av]) / fmid[t0:t1][av]).mean()))
        S = {"physical_feedback": {}, "D_RE": {}}
        for arm in B.ARMS:
            S["physical_feedback"][arm] = {w: {k: {"mean": float(np.mean(v)), "CI95": boot_ci(v), "min": float(np.min(v)),
                                                   "max": float(np.max(v))} for k, v in d.items()}
                                           for w, d in res[arm].items()}
        rng = np.random.default_rng(1011)
        for w in WINDOWS3:
            rc, r1 = np.array(res["CertGrip"][w]["RE_mid"]), np.array(res["CSF1"][w]["RE_mid"])
            bs = []
            for _ in range(2000):
                i = rng.integers(0, len(rc), len(rc))
                bs.append(1 - rc[i].mean() / r1[i].mean())
            S["D_RE"][w] = {"point": float(1 - rc.mean() / r1.mean()),
                            "CI95": [float(np.percentile(bs, 2.5)), float(np.percentile(bs, 97.5))]}
        out["shifts"][s] = S
    h3 = json.load(open(os.path.join(ROOT, "v1/h3_analysis.json")))
    out["reference_08d_label_route"] = {s: h3["shifts"][s].get("arms") for s in SHIFTS3}
    os.makedirs(os.path.join(ROOT, "v3"), exist_ok=True)
    json.dump(out, open(os.path.join(ROOT, "v3/b3_analysis.json"), "w"), indent=1)
    print("wrote results/v3/b3_analysis.json")


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    r = sub.add_parser("run")
    r.add_argument("--shift", required=True, choices=SHIFTS3)
    r.add_argument("--ordering", type=int, required=True, choices=ORDS3)
    r.add_argument("--arm", required=True, choices=list(B.ARMS))
    r.add_argument("--steps", type=int, default=H.T_PRE + H.T_SHIFT)
    r.add_argument("--out", required=True)
    sub.add_parser("analyse")
    a = ap.parse_args()
    cmd_run(a) if a.cmd == "run" else cmd_analyse(a)


if __name__ == "__main__":
    main()
