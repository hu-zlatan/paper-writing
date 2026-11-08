"""CertGrip (paper 2) experiment entry point. Every number in the paper comes from outputs of these commands.

Commands (run from papers/p2/code; Actions: experiments.yml with workdir papers/p2/code):
  label  --pool id|s2|pilot --family F1 --start 0 --count 25 [--shift S1|S1m|S3] --out ../results/...
         F* bracket by log-space bisection (1 replay at F_max + 10 halvings) for each object x disturbance, plus the
         tactile/proprio record of the F_max replay (features precede the force, so they do not depend on F).
  mono   same selection, 35-point log force grid per instance -> slip outcome per grid point (H1-M).
  timing replay a fixed pilot set twice -> per-replay time and sha256 of the final state (replay cost c, UT6).
Each command writes <out>.jsonl: a header line, one line per instance, and on time-out an EARLY_STOP line with
next_index (time guard at 80 % of --budget-minutes); a metric summary is printed as `name: value`.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import platform
import sys
import time

import mujoco
import numpy as np

from certgrip.data import DISTS, N_OBJ, make_instance, split_of
from certgrip.features import record
from certgrip.sim import RD2, TAXEL_NOISE, Sim, preload_force

SLIP = {"delta_t": 0.002, "rot_t_deg": 3.0}   # fixed before any monotonicity data (run 37; 07_hypotheses §1.1)


def header(a, cmd):
    return {"header": True, "cmd": cmd, "argv": sys.argv[1:], "mujoco": mujoco.__version__,
            "numpy": np.__version__, "python": platform.python_version(), "machine": platform.machine(),
            "processor": platform.processor(), "F0": preload_force(), "slip_metric": SLIP,
            "protocol": getattr(a, "protocol", "squeeze"), "rd_detector": RD2 if getattr(a, "protocol", "") == "rd" else None,
            "taxel_noise": TAXEL_NOISE if getattr(a, "protocol", "") == "rd" else None}


def items(a):
    dists = a.dists.split(",") if a.dists else DISTS
    for obj in range(a.start, a.start + a.count):
        if obj >= N_OBJ[a.pool]:
            break
        for d in dists:
            yield obj, d


def inst_row(a, obj, d, inst):
    return {"pool": a.pool, "family": a.family, "obj": obj, "dist": d, "shift": a.shift, "split": split_of(a.pool, obj),
            "inst": {k: (list(v) if isinstance(v, tuple) else v) for k, v in inst.__dict__.items()}}


def label_one(sim, f_min, f_max, halvings):
    t0 = time.perf_counter()
    top = sim.run(f_max, record=True)
    n = 1
    if top["slip"]:
        return {"F_lo": f_max, "F_hi": None, "F_mid": None, "unavoidable": True, "n_replays": n,
                "slip_reason_fmax": top["reason"], "preload_slip": top["preload_slip"],
                "rec": record(top["features"]), "seconds": time.perf_counter() - t0}
    lo, hi = math.log(f_min), math.log(f_max)
    for _ in range(halvings):
        mid = 0.5 * (lo + hi)
        n += 1
        if sim.run(math.exp(mid))["slip"]:
            lo = mid
        else:
            hi = mid
    return {"F_lo": math.exp(lo), "F_hi": math.exp(hi), "F_mid": math.exp(0.5 * (lo + hi)), "unavoidable": False,
            "n_replays": n, "preload_slip": top["preload_slip"], "rec": record(top["features"]),
            "seconds": time.perf_counter() - t0}


def run_loop(a, cmd, body):
    os.makedirs(os.path.dirname(os.path.abspath(a.out)), exist_ok=True)
    t0, rows = time.time(), []
    with open(a.out + ".jsonl", "w") as f:
        f.write(json.dumps(header(a, cmd)) + "\n")
        for obj, d in items(a):
            first = d == (a.dists.split(",")[0] if a.dists else DISTS[0])   # stop only at object boundaries
            if first and time.time() - t0 > 0.8 * a.budget_minutes * 60:
                f.write(json.dumps({"EARLY_STOP_AT_80_PCT_BUDGET": True, "next_index": obj}) + "\n")
                print("EARLY_STOP_AT_80_PCT_BUDGET", flush=True)
                break
            inst = make_instance(a.pool, a.family, obj, d, a.shift)
            sim = Sim(inst, preload_force(), delta_t=SLIP["delta_t"], rot_t_deg=SLIP["rot_t_deg"], protocol=a.protocol)
            r = inst_row(a, obj, d, inst)
            r.update(body(sim))
            rows.append(r)
            f.write(json.dumps(r) + "\n")
            f.flush()
    return rows


def cmd_label(a):
    rows = run_loop(a, "label", lambda sim: label_one(sim, a.f_min, a.f_max, a.halvings))
    if rows:
        per = [r["seconds"] / r["n_replays"] for r in rows]
        print(f"instances: {len(rows)}")
        print(f"unavoidable: {sum(r['unavoidable'] for r in rows)}")
        print(f"preload_slips: {sum(r['preload_slip'] for r in rows)}")
        print(f"replay_seconds_mean: {float(np.mean(per)):.4f}")


def cmd_mono(a):
    grid = np.exp(np.linspace(math.log(a.f_min_grid), math.log(a.f_max), a.grid))

    def body(sim):
        t0 = time.perf_counter()
        out = [bool(sim.run(float(F))["slip"]) for F in grid]
        first_ok = next((k for k, o in enumerate(out) if not o), None)
        nonmono = first_ok is not None and any(out[first_ok:])
        return {"grid": grid.round(6).tolist(), "slip_grid": out, "non_monotone": bool(nonmono),
                "seconds": time.perf_counter() - t0}
    rows = run_loop(a, "mono", body)
    if rows:
        print(f"instances: {len(rows)}")
        print(f"non_monotone: {sum(r['non_monotone'] for r in rows)}")


def cmd_timing(a):
    """Fixed pilot instances (pool pilot, objects start..start+count, all families x disturbances), each replayed
    at three forces, twice; sha256 of (qpos, qvel) after each replay -> bit-identity within and across machines."""
    os.makedirs(os.path.dirname(os.path.abspath(a.out)), exist_ok=True)
    rows, times = [], []
    for fam in ("F1", "F2", "F3", "F4"):
        for obj in range(a.start, a.start + a.count):
            for d in DISTS:
                inst = make_instance("pilot", fam, obj, d)
                sim = Sim(inst, preload_force(), delta_t=SLIP["delta_t"], rot_t_deg=SLIP["rot_t_deg"],
                          protocol=a.protocol)
                hs = []
                for F in (3.0, 15.0, 60.0):
                    for _ in range(2):
                        t0 = time.perf_counter()
                        r = sim.run(F)
                        times.append(time.perf_counter() - t0)
                        hs.append(hashlib.sha256(np.concatenate([sim.d.qpos, sim.d.qvel]).tobytes()).hexdigest())
                rows.append({"family": fam, "obj": obj, "dist": d, "hashes": hs,
                             "within_identical": all(hs[2 * k] == hs[2 * k + 1] for k in range(3))})
    res = header(a, "timing")
    res.update({"replay_seconds_median": float(np.median(times)), "replay_seconds_mean": float(np.mean(times)),
                "replay_seconds_p95": float(np.percentile(times, 95)), "n_replays": len(times),
                "all_within_identical": all(r["within_identical"] for r in rows),
                "digest": hashlib.sha256("".join(h for r in rows for h in r["hashes"]).encode()).hexdigest(),
                "rows": rows})
    with open(a.out + ".json", "w") as f:
        json.dump(res, f, indent=1)
    print(f"replay_seconds_median: {res['replay_seconds_median']:.4f}")
    print(f"all_within_identical: {res['all_within_identical']}")
    print(f"digest: {res['digest']}")


def main(argv=None):
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    for name in ("label", "mono", "timing"):
        p = sub.add_parser(name)
        p.add_argument("--pool", default="pilot", choices=["id", "s2", "pilot"])
        p.add_argument("--family", default="F1", choices=["F1", "F2", "F3", "F4", "F5"])
        p.add_argument("--start", type=int, default=0)
        p.add_argument("--count", type=int, default=1)
        p.add_argument("--dists", default="", help="comma list, default all four")
        p.add_argument("--shift", default=None, choices=["S1", "S1m", "S3"])
        p.add_argument("--f-min", type=float, default=0.1)
        p.add_argument("--f-max", type=float, default=100.0)
        p.add_argument("--halvings", type=int, default=10)
        p.add_argument("--f-min-grid", type=float, default=0.3)
        p.add_argument("--grid", type=int, default=35)
        p.add_argument("--budget-minutes", type=float, default=25.0)
        p.add_argument("--protocol", default="squeeze", choices=["squeeze", "rd"],
                       help="squeeze = stage-9 design; rd = amendment 08a ramp-down probe (the frozen study uses rd)")
        p.add_argument("--out", required=True)
    a = ap.parse_args(argv)
    {"label": cmd_label, "mono": cmd_mono, "timing": cmd_timing}[a.cmd](a)


if __name__ == "__main__":
    main()
