"""Amendment 10 §B2 / addendum 10a (p2 v3): reactive slip-tightening controllers on the id cal + test instances.
Arms: REACT-blind@c (r_safe = 0.8 * 0.3, F0 = c * CSF-1 nominal) and REACT-probe@c (r_safe = 0.8 * mu_hat, F0 = c *
CSF-mu-hat sigma 0.2 force), c in {0.5, 0.75}. Base forces from results/v1/crc_grids.json (log_g of CSF-1 and
CSF-muhat@0.2); mu_hat from the recorded onset (robot-observable) in the label rows; no F* label is read.
Detector: noisy taxel ratio T / N every 10 ms (08a taxel model; channel gain as 08a, noise stream seeded "react"),
mean of the last 6 frames > r_safe on 2 consecutive frames, 30 ms refractory; action F <- min(F_max, 1.25 F) ramped
over 20 ms, at most 4 steps. Slip = the v1 criterion over ramp + settle + disturbance.

  python react_run.py run --family F1 --start 200 --count 100 --out ../results/v3/react/F1_200
  python react_run.py analyse  -> ../results/v3/b2_analysis.json"""
import argparse
import glob
import json
import math
import os
import time
from collections import deque

import numpy as np

from certgrip.baselines import mu_hat
from certgrip.data import DISTS, make_instance, split_of
from certgrip.featsets import onset_log_force
from certgrip.io import ROOT, key, load_rows
from certgrip.sim import TAXEL_NOISE, Sim, instance_seed, preload_force
from main import SLIP

MU_MIN, SAFE, FACTOR, MAX_STEPS, W, CONSEC, REFRACT = 0.3, 0.8, 1.25, 4, 6, 2, 3
CS = (0.5, 0.75)
F_MAX = 100.0


class React:
    def __init__(self, inst, F_start, r_safe):
        g = np.random.default_rng(instance_seed(inst, "taxel"))
        self.gain = np.exp(TAXEL_NOISE["gain"] * g.standard_normal(3))
        self.gain[2] = self.gain[1]
        self.rng = np.random.default_rng(instance_seed(inst, "react"))
        self.F, self.r_safe = F_start, r_safe
        self.buf, self.consec, self.refr, self.n_steps = deque(maxlen=W), 0, 0, 0

    def step(self, sim):
        N, T = sim._noisy_ratio(self.rng, self.gain)
        self.buf.append(T / max(N, 1e-9))
        if self.refr > 0:
            self.refr -= 1
            return None
        self.consec = self.consec + 1 if np.mean(self.buf) > self.r_safe else 0
        if self.consec >= CONSEC and self.n_steps < MAX_STEPS:
            self.n_steps += 1
            self.consec, self.refr = 0, REFRACT
            self.F = min(F_MAX, FACTOR * self.F)
            return self.F
        return None


def arms_for(i, G, lab_row):
    g1 = math.exp(G["arms"]["CSF-1"]["log_g"][i])
    gm = math.exp(G["arms"]["CSF-muhat@0.2"]["log_g"][i])
    muh = mu_hat(lab_row["inst"]["mass"], math.exp(onset_log_force(lab_row, 0.2)))
    out = {}
    for c in CS:
        out[f"REACT-blind@{c}"] = (c * g1, SAFE * MU_MIN)
        out[f"REACT-probe@{c}"] = (c * gm, SAFE * muh)
    return out


def cmd_run(a):
    G = json.load(open(os.path.join(ROOT, "v1/crc_grids.json")))
    index = {tuple(k): i for i, k in enumerate(G["instances"])}
    labs = {key(r): r for r in load_rows("v1/labels/*.jsonl")}
    os.makedirs(os.path.dirname(os.path.abspath(a.out)), exist_ok=True)
    t0, n = time.time(), 0
    with open(a.out + ".jsonl", "w") as f:
        f.write(json.dumps({"header": True, "cmd": "react", "argv": vars(a), "params": {
            "mu_min": MU_MIN, "safe": SAFE, "factor": FACTOR, "max_steps": MAX_STEPS, "w": W, "consec": CONSEC,
            "refractory_frames": REFRACT, "cs": CS}}) + "\n")
        for obj in range(a.start, a.start + a.count):
            if time.time() - t0 > 0.8 * a.budget_minutes * 60:
                f.write(json.dumps({"EARLY_STOP_AT_80_PCT_BUDGET": True, "next_index": obj}) + "\n")
                break
            for d in DISTS:
                k = ("id", a.family, obj, d, None)
                if k not in index:
                    continue
                inst = make_instance("id", a.family, obj, d, None)
                sim = Sim(inst, preload_force(), delta_t=SLIP["delta_t"], rot_t_deg=SLIP["rot_t_deg"], protocol="rd")
                res = {}
                for arm, (F_start, r_safe) in arms_for(index[k], G, labs[k]).items():
                    F_start = min(F_MAX, F_start)
                    ctl = React(inst, F_start, r_safe)
                    o = sim.run(F_start, controller=ctl)
                    res[arm] = {"slip": bool(o["slip"]), "F_start": round(F_start, 6), "F_end": round(o["F_end"], 6),
                                "n_steps": o["n_steps"]}
                f.write(json.dumps({"key": list(k), "split": split_of("id", obj), "arms": res}) + "\n")
                f.flush()
                n += 1
    print(f"instances: {n}")
    print(f"seconds: {time.time() - t0:.1f}")


def cmd_analyse(a):
    G = json.load(open(os.path.join(ROOT, "v1/crc_grids.json")))
    keys = [tuple(k) for k in G["instances"]]
    rep = {}
    for p in sorted(glob.glob(os.path.join(ROOT, "v3/react/*.jsonl"))):
        for line in open(p):
            r = json.loads(line)
            if "key" in r:
                rep.setdefault(tuple(r["key"]), []).append(r)
    missing = [k for k in keys if k not in rep]
    print(f"instances {len(keys)}, with runs {len(keys) - len(missing)}")
    if missing:
        raise SystemExit("incomplete: refusing to analyse")
    labs = {key(r): r for r in load_rows("v1/labels/*.jsonl")}
    test = [k for k in keys if labs[k]["split"] == "test"]
    arms = list(rep[test[0]][-1]["arms"])
    out = {"purpose": "p2 amendment 10 B2 / 10a reactive controllers (descriptive, test split)", "arms": {}}
    for arm in arms:
        def summ(ks):
            sl = [labs[k]["unavoidable"] or rep[k][-1]["arms"][arm]["slip"] for k in ks]
            av = [k for k in ks if not labs[k]["unavoidable"]]
            re_ = [(rep[k][-1]["arms"][arm]["F_end"] - labs[k]["F_mid"]) / labs[k]["F_mid"] for k in av]
            st = [rep[k][-1]["arms"][arm]["n_steps"] for k in ks]
            return {"n": len(ks), "slip_phys": float(np.mean(sl)), "RE_mid": float(np.mean(re_)),
                    "mean_steps": float(np.mean(st)), "share_at_cap": float(np.mean([s >= MAX_STEPS for s in st])),
                    "F_end_N_mean": float(np.mean([rep[k][-1]["arms"][arm]["F_end"] for k in av]))}
        out["arms"][arm] = {"overall": summ(test), "stratum": {d: summ([k for k in test if k[3] == d]) for d in DISTS}}
    json.dump(out, open(os.path.join(ROOT, "v3/b2_analysis.json"), "w"), indent=1)
    for arm, r in out["arms"].items():
        print(arm, {k: round(v, 4) for k, v in r["overall"].items()})


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    r = sub.add_parser("run")
    r.add_argument("--family", required=True)
    r.add_argument("--start", type=int, required=True)
    r.add_argument("--count", type=int, required=True)
    r.add_argument("--budget-minutes", type=float, default=150)
    r.add_argument("--out", required=True)
    sub.add_parser("analyse")
    a = ap.parse_args()
    cmd_run(a) if a.cmd == "run" else cmd_analyse(a)


if __name__ == "__main__":
    main()
