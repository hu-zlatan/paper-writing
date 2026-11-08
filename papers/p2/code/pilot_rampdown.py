"""Re-pilot of the candidate incipient-slip ramp-down probe (pilot pool only; not a paper result).
Question: does the onset force reveal friction? Estimate log mu_hat = log(m g / (2 F_onset)) on D4 instances
(static load before the disturbance) and compare with the true log mu. Also counts instances whose onset is not found
above the floor. usage: python pilot_rampdown.py [--floor 0.02] [--objects 25] [--out ../results/pilot/pilot_rampdown]
"""
import argparse
import json
import math

import numpy as np

import certgrip.sim as simmod
from certgrip.data import FAMILIES, make_instance
from certgrip.sim import Sim, preload_force


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--floor", type=float, default=0.02)
    ap.add_argument("--objects", type=int, default=25)
    ap.add_argument("--out", default="../results/pilot/pilot_rampdown")
    a = ap.parse_args()
    simmod.RD_FLOOR = a.floor
    rows = []
    for fam in FAMILIES + ("F5",):
        for o in range(a.objects):
            inst = make_instance("pilot", fam, o, "D4")
            s = Sim(inst, preload_force(), rampdown=True)
            rd = s.run(30.0, record=True)["features"]["rampdown"]
            est = math.log(inst.mass * 9.81 / (2 * rd["onset_force"])) if rd["found"] else None
            rows.append({"family": fam, "obj": o, "mu": inst.mu, "mass": inst.mass, "found": rd["found"],
                         "onset_force": rd["onset_force"], "log_mu_hat": est})
    ok = [r for r in rows if r["found"]]
    err = np.array([r["log_mu_hat"] - math.log(r["mu"]) for r in ok])
    res = {"purpose": "p2 re-pilot: ramp-down probe friction information (pilot pool, D4 instances)",
           "floor_frac_F0": a.floor, "n": len(rows), "not_found": len(rows) - len(ok),
           "corr_logmu_hat_logmu": float(np.corrcoef([r["log_mu_hat"] for r in ok], [math.log(r["mu"]) for r in ok])[0, 1]),
           "err_mean": float(err.mean()), "err_sd": float(err.std()), "rows": rows}
    json.dump(res, open(a.out + f"_floor{a.floor}.json", "w"), indent=1)
    print({k: v for k, v in res.items() if k != "rows"})


if __name__ == "__main__":
    main()
