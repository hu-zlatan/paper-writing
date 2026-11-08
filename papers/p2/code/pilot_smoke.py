"""Stage-10 pilot smoke test (paper 2): replay cost, determinism, tactile channels and a small monotonicity look.

Slip metric fixed BEFORE this look at the 07_hypotheses assumption: delta_t = 2 mm tangential, 3 deg rotation, contact
loss. Not a paper result; it informs the pre-registration freeze (07_hypotheses §8 items 1, 2, 4).
usage (from papers/p2/code): python pilot_smoke.py [--n 16] [--seed 1] [--out ../results/pilot/pilot_smoke.json]
"""
import argparse
import hashlib
import json
import os
import platform
import time

import mujoco
import numpy as np

from certgrip.sim import Sim, preload_force, sample_instance


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=16)
    ap.add_argument("--seed", type=int, default=1)
    ap.add_argument("--grid", type=int, default=25)
    ap.add_argument("--out", default="../results/pilot/pilot_smoke.json")
    a = ap.parse_args()
    rng = np.random.default_rng(a.seed)
    F0 = preload_force()
    fams, dists = ["F1", "F2", "F3", "F4"], ["D1", "D2", "D3", "D4"]
    grid = np.exp(np.linspace(np.log(0.3), np.log(100.0), a.grid))
    rows, times = [], []
    for i in range(a.n):
        inst = sample_instance(rng, fams[i % 4], dists[(i // 4) % 4])
        sim = Sim(inst, F0)
        t0 = time.perf_counter()
        r = sim.run(30.0, record=True)
        times.append(time.perf_counter() - t0)
        tp = r["features"]["touch_preload"].reshape(2, 3, 8, 8)
        out = []
        for f in grid:
            t0 = time.perf_counter()
            out.append(bool(sim.run(float(f))["slip"]))
            times.append(time.perf_counter() - t0)
        first_ok = next((k for k, o in enumerate(out) if not o), None)
        nonmono = first_ok is not None and any(out[first_ok:])
        # determinism: same instance, same force, twice -> identical final state hash
        h = []
        for _ in range(2):
            sim.run(float(grid[a.grid // 2]))
            h.append(hashlib.sha256(np.concatenate([sim.d.qpos, sim.d.qvel]).tobytes()).hexdigest())
        rows.append({"instance": inst.__dict__, "slip_grid": out, "non_monotone": nonmono,
                     "first_no_slip_force": float(grid[first_ok]) if first_ok is not None else None,
                     "deterministic": h[0] == h[1],
                     "touch_channel_sums": [float(np.abs(tp[p, c]).sum()) for p in range(2) for c in range(3)]})
    res = {"purpose": "p2 stage-10 pilot smoke (not a paper result)", "mujoco": mujoco.__version__,
           "machine": platform.machine(), "python": platform.python_version(), "F0": F0,
           "slip_metric": {"delta_t_m": 0.002, "rot_deg": 3.0, "contact_loss": True},
           "force_grid": grid.tolist(), "replay_seconds_median": float(np.median(times)),
           "replay_seconds_p95": float(np.percentile(times, 95)), "n_replays_timed": len(times),
           "n_instances": a.n, "n_non_monotone": int(sum(r["non_monotone"] for r in rows)),
           "all_deterministic": all(r["deterministic"] for r in rows), "rows": rows}
    os.makedirs(os.path.dirname(a.out), exist_ok=True)
    json.dump(res, open(a.out, "w"), indent=1)
    print(f"replay_seconds_median: {res['replay_seconds_median']:.4f}")
    print(f"n_non_monotone: {res['n_non_monotone']} / {a.n}")
    print(f"all_deterministic: {res['all_deterministic']}")


if __name__ == "__main__":
    main()
