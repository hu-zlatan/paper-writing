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
    """H1-M. --design grid (pilot): --grid log points on [f_min_grid, f_max]. --design h1m (frozen, 07_hypotheses H1-M):
    25 log points on [f_min, f_max] + the 11 bisection replays + 10 log points on [F*_hi, 1.5 F*_hi]; non-monotone =
    any F_a < F_b with slip(F_a) = 0 and slip(F_b) = 1 among all simulated forces."""
    if a.design == "grid":
        grid = np.exp(np.linspace(math.log(a.f_min_grid), math.log(a.f_max), a.grid))

        def body(sim):
            t0 = time.perf_counter()
            out = [bool(sim.run(float(F))["slip"]) for F in grid]
            first_ok = next((k for k, o in enumerate(out) if not o), None)
            nonmono = first_ok is not None and any(out[first_ok:])
            return {"grid": grid.round(6).tolist(), "slip_grid": out, "non_monotone": bool(nonmono),
                    "seconds": time.perf_counter() - t0}
    else:
        def body(sim):
            t0 = time.perf_counter()
            pts = {}
            for F in np.exp(np.linspace(math.log(a.f_min), math.log(a.f_max), 25)):
                pts[float(F)] = bool(sim.run(float(F))["slip"])
            lo, hi = math.log(a.f_min), math.log(a.f_max)
            pts[a.f_max] = bool(sim.run(a.f_max)["slip"])
            F_hi = None
            if not pts[a.f_max]:
                for _ in range(a.halvings):
                    mid = 0.5 * (lo + hi)
                    sl = bool(sim.run(math.exp(mid))["slip"])
                    pts[math.exp(mid)] = sl
                    lo, hi = (mid, hi) if sl else (lo, mid)
                F_hi = math.exp(hi)
                for F in np.exp(np.linspace(math.log(F_hi), math.log(1.5 * F_hi), 10)):
                    pts[float(F)] = bool(sim.run(float(F))["slip"])
            Fs = sorted(pts)
            sl = [pts[F] for F in Fs]
            first_ok = next((k for k, o in enumerate(sl) if not o), None)
            nonmono = first_ok is not None and any(sl[first_ok:])
            return {"forces": [round(F, 6) for F in Fs], "slip": sl, "F_hi": F_hi, "non_monotone": bool(nonmono),
                    "n_forces": len(Fs), "seconds": time.perf_counter() - t0}
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


def cmd_fit(a):
    """Equal 30-config grouped-CV search on the id train objects (avoidable instances), tau = 1 - alpha, refit, then
    log-predictions for every labelled row (id select / cal / test, shift pools). Cal / test labels are never read
    here except to write the row keys; only train rows enter the fit."""
    from certgrip.featsets import matrix
    from certgrip.io import key, load_rows
    from certgrip.models import fit_quantile
    rows = load_rows(a.labels)
    tr = [r for r in rows if r["pool"] == a.train_pool and r["shift"] is None and r["split"] == a.train_split and not r["unavoidable"]]
    y = np.log([r["F_hi"] for r in tr])
    g = np.array([f"{r['family']}_{r['obj']}" for r in tr])
    t0 = time.time()
    m, info = fit_quantile(matrix(tr, a.fset, a.no_mass, a.sigma), y, g, 1 - a.alpha, seed=a.seed, n_configs=a.configs)
    pred = m.predict(matrix(rows, a.fset, a.no_mass, a.sigma))
    os.makedirs(os.path.dirname(os.path.abspath(a.out)), exist_ok=True)
    res = header(a, "fit")
    res.update({"fset": a.fset, "sigma": a.sigma, "no_mass": a.no_mass, "alpha": a.alpha, "seed": a.seed,
                "configs": a.configs, "n_train_rows": len(tr), "best": info["best"], "cv_pinball": info["cv_pinball"],
                "n_rows": len(rows), "keys_sha256": hashlib.sha256(json.dumps([list(key(r)) for r in rows]).encode()).hexdigest(),
                "log_pred": [round(float(p), 6) for p in pred],
                "seconds": time.time() - t0})
    with open(a.out + ".json", "w") as f:
        json.dump(res, f)
    print(f"n_train_rows: {len(tr)}")
    print(f"cv_pinball: {info['cv_pinball']:.5f}")


def cmd_fitg(a):
    """Addendum 08h §1 (H1c RAW-G): GaussianModel on the id train objects with a given config (the best config of an
    existing quantile fit, no new search); writes mu and sigma log-predictions for every labelled row."""
    from certgrip.featsets import matrix
    from certgrip.io import key, load_rows
    from certgrip.models import GaussianModel
    rows = load_rows(a.labels)
    tr = [r for r in rows if r["pool"] == "id" and r["shift"] is None and r["split"] == "train" and not r["unavoidable"]]
    cfg = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "results", a.config_from)))["best"]
    m = GaussianModel(seed=a.seed, **cfg).fit(matrix(tr, a.fset, False, a.sigma), np.log([r["F_hi"] for r in tr]))
    X = matrix(rows, a.fset, False, a.sigma)
    mu = m.mu.predict(X); sd = np.sqrt(np.pi / 2) * np.maximum(m.sd.predict(X), 1e-6)
    res = header(a, "fitg")
    res.update({"fset": a.fset, "sigma": a.sigma, "seed": a.seed, "config": cfg, "config_from": a.config_from,
                "keys_sha256": hashlib.sha256(json.dumps([list(key(r)) for r in rows]).encode()).hexdigest(),
                "mu": [round(float(v), 6) for v in mu], "sigma_hat": [round(float(v), 6) for v in sd]})
    with open(a.out + ".json", "w") as f:
        json.dump(res, f)
    print(f"n_train_rows: {len(tr)}")


def cmd_crc(a):
    """08c §2: direct replays of one shard of id cal / test instances (protocol rd) at every arm's 20 grid forces
    F = min(F_max, g e^lambda) from results/v1/crc_grids.json; one line per instance with slip[arm] (20 booleans).
    Identical forces within an instance are replayed once. No label value is read."""
    a.protocol = "rd"
    G = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "results", "v1", a.grids)))
    index = {tuple(k): i for i, k in enumerate(G["instances"])}
    f_max = G["F_max"]
    os.makedirs(os.path.dirname(os.path.abspath(a.out)), exist_ok=True)
    t0, n, n_rep = time.time(), 0, 0
    with open(a.out + ".jsonl", "w") as f:
        h = header(a, "crc")
        h.update({"grids_keys_sha256": G["keys_sha256"], "arms": list(G["arms"])})
        f.write(json.dumps(h) + "\n")
        for obj in range(a.start, a.start + a.count):
            if time.time() - t0 > 0.8 * a.budget_minutes * 60:
                f.write(json.dumps({"EARLY_STOP_AT_80_PCT_BUDGET": True, "next_index": obj}) + "\n")
                print("EARLY_STOP_AT_80_PCT_BUDGET", flush=True)
                break
            for d in DISTS:
                k = ("id", a.family, obj, d, None)
                if k not in index:
                    continue
                i = index[k]
                inst = make_instance("id", a.family, obj, d, None)
                sim = Sim(inst, preload_force(), delta_t=SLIP["delta_t"], rot_t_deg=SLIP["rot_t_deg"], protocol="rd")
                cache, slips, forces = {}, {}, {}
                for arm, A in G["arms"].items():
                    grid = A["grids"][d] if "grids" in A else A["grid"]
                    Fs = [min(f_max, math.exp(A["log_g"][i] + lam)) for lam in grid]
                    out = []
                    for F in Fs:
                        fk = round(F, 9)
                        if fk not in cache:
                            cache[fk] = bool(sim.run(F)["slip"])
                        out.append(cache[fk])
                    slips[arm] = out
                    forces[arm] = [round(F, 6) for F in Fs]
                n += 1
                n_rep += len(cache)
                f.write(json.dumps({"key": list(k), "split": split_of("id", obj), "slip": slips, "F": forces,
                                    "n_replays": len(cache)}) + "\n")
                f.flush()
    print(f"instances: {n}")
    print(f"replays: {n_rep}")
    print(f"seconds: {time.time() - t0:.1f}")


def cmd_replay(a):
    """08d §3: direct replays (protocol rd) of rows start..start+count of results/v1/h3/schedule_<shift>.json at the
    scheduled force; one line per row with the physical slip outcome. No label value is read."""
    a.protocol = "rd"
    S = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "results", "v1", "h3",
                                    f"schedule_{a.shift}.json")))
    rows = S["rows"][a.start:a.start + a.count]
    os.makedirs(os.path.dirname(os.path.abspath(a.out)), exist_ok=True)
    t0 = time.time()
    with open(a.out + ".jsonl", "w") as f:
        f.write(json.dumps(header(a, "replay") | {"shift_schedule": a.shift}) + "\n")
        for r in rows:
            pool, fam, obj, d, sh = r["key"]
            inst = make_instance(pool, fam, obj, d, sh)
            sim = Sim(inst, preload_force(), delta_t=SLIP["delta_t"], rot_t_deg=SLIP["rot_t_deg"], protocol="rd")
            out = sim.run(r["F"])
            f.write(json.dumps({"shift": a.shift, "arm": r["arm"], "step": r["step"], "key": r["key"], "F": r["F"],
                                "slip": bool(out["slip"]), "reason": out.get("reason")}) + "\n")
    print(f"replays: {len(rows)}")
    print(f"seconds: {time.time() - t0:.1f}")


def main(argv=None):
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    for name in ("label", "mono", "timing"):
        p = sub.add_parser(name)
        p.add_argument("--pool", default="pilot", choices=["id", "s2", "pilot", "f4", "c4"])
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
        p.add_argument("--design", default="grid", choices=["grid", "h1m"], help="mono only: pilot grid or frozen H1-M design")
        p.add_argument("--budget-minutes", type=float, default=25.0)
        p.add_argument("--protocol", default="squeeze", choices=["squeeze", "rd", "noprobe"],
                       help="squeeze = stage-9 design; rd = amendment 08a ramp-down probe (the frozen study uses rd)")
        p.add_argument("--out", required=True)
    fi = sub.add_parser("fit", help="stage 12: train one arm on the id train objects; predict log F for every row")
    fi.add_argument("--fset", required=True)
    fi.add_argument("--sigma", type=float, default=0.2)
    fi.add_argument("--no-mass", action="store_true")
    fi.add_argument("--alpha", type=float, default=0.10)
    fi.add_argument("--seed", type=int, default=0)
    fi.add_argument("--configs", type=int, default=30)
    fi.add_argument("--labels", default="v1/labels/*.jsonl", help="glob under results/")
    fi.add_argument("--train-pool", default="id", help="smoke tests only: pilot")
    fi.add_argument("--train-split", default="train", help="smoke tests only: pilot")
    fi.add_argument("--out", required=True)
    fg = sub.add_parser("fitg", help="08h: RAW-G Gaussian model with a fixed config")
    fg.add_argument("--fset", default="full_rd")
    fg.add_argument("--sigma", type=float, default=0.2)
    fg.add_argument("--seed", type=int, default=0)
    fg.add_argument("--config-from", default="v1/preds/a010_full_rd_s0.2_seed0.json")
    fg.add_argument("--labels", default="v1/labels/*.jsonl")
    fg.add_argument("--out", required=True)
    po = sub.add_parser("pilotoof", help="re-pilot (08a): one arm's cross-fitted OOF predictions on the pilot labels")
    po.add_argument("--fset", required=True)
    po.add_argument("--sigma", type=float, default=0.0)
    po.add_argument("--configs", type=int, default=30)
    po.add_argument("--out", required=True)
    cr = sub.add_parser("crc", help="08c: CRC grid replays for one family x object range (id cal / test instances)")
    cr.add_argument("--family", required=True, choices=["F1", "F2", "F3", "F4"])
    cr.add_argument("--start", type=int, required=True)
    cr.add_argument("--count", type=int, required=True)
    cr.add_argument("--budget-minutes", type=float, default=25.0)
    cr.add_argument("--grids", default="crc_grids.json", help="crc_grids_v2.json for addendum 08e")
    cr.add_argument("--out", required=True)
    rp = sub.add_parser("replay", help="08d: H3 stream-audit direct replays from a schedule file")
    rp.add_argument("--shift", required=True, choices=["S1", "S2", "S3", "S1m"])
    rp.add_argument("--start", type=int, required=True)
    rp.add_argument("--count", type=int, required=True)
    rp.add_argument("--out", required=True)
    a = ap.parse_args(argv)
    if a.cmd == "replay":
        cmd_replay(a)
        return
    if a.cmd == "crc":
        cmd_crc(a)
        return
    if a.cmd == "fit":
        cmd_fit(a)
        return
    if a.cmd == "fitg":
        cmd_fitg(a)
        return
    if a.cmd == "pilotoof":
        import pilot_analysis_rd
        pilot_analysis_rd.run_arm(a.fset, a.sigma, a.configs, a.out)
        return
    {"label": cmd_label, "mono": cmd_mono, "timing": cmd_timing}[a.cmd](a)


if __name__ == "__main__":
    main()
