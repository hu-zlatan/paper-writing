"""H1-V (07_hypotheses §3, reported as secondary after the H1-M failure, 08c §1): label-rule split conformal per
disturbance stratum (cal split, n = 500, label scores log F*_hi - log g), forces for every id test instance, a direct
replay (protocol rd) at that force, and the paired net disagreement Delta = mean(slip_direct - 1{F < F*_hi}).
Arms: CertGrip (full_rd, sigma 0.2, seed 0) at alpha 0.10 (primary H1-V) and 0.05; COMP = CSF-1 at 0.10 and 0.05
(H1-x secondary). Object-cluster bootstrap (2,000 draws, test objects within family; q-hat held fixed — the audit
is conditional on the calibration draw, as in 07). Pass iff CI** upper <= 0.02; failure iff lower > 0.02.
  python h1v.py replay   -> results/v1/h1v/replays.jsonl (direct replays only; nothing printed but counts)
  python h1v.py analyse  -> results/v1/h1v_analysis.json
"""
import hashlib
import json
import math
import os
import sys

import numpy as np

from certgrip.baselines import f_nom
from certgrip.conformal import qhat
from certgrip.data import make_instance
from certgrip.io import ROOT, key, load_rows

ALPHAS, F_MAX, TAU = (0.10, 0.05), 100.0, 0.02
OUT = os.path.join(ROOT, "v1/h1v")


def setup():
    rows = load_rows("v1/labels/*.jsonl")
    p = json.load(open(os.path.join(ROOT, "v1/preds/a010_full_rd_s0.2_seed0.json")))
    assert p["keys_sha256"] == hashlib.sha256(json.dumps([list(key(r)) for r in rows]).encode()).hexdigest()
    lg = {"CertGrip": np.asarray(p["log_pred"]),
          "CSF-1": np.log([f_nom(r["inst"]["mass"], r["dist"], r["inst"]["amp"], r["inst"]["freq"]) for r in rows])}
    base = [r["pool"] == "id" and r["shift"] is None for r in rows]
    cal = np.array([b and r["split"] == "cal" and not r["unavoidable"] for b, r in zip(base, rows)])
    test = [i for i, (b, r) in enumerate(zip(base, rows)) if b and r["split"] == "test"]
    dist = np.array([r["dist"] for r in rows])
    sched = []
    for arm, g in lg.items():
        sc = np.log([r["F_hi"] if r["F_hi"] else np.nan for r in rows]) - g
        for a in ALPHAS:
            q = {d: qhat(sc[cal & (dist == d)], a) for d in ("D1", "D2", "D3", "D4")}
            for i in test:
                F = min(F_MAX, math.exp(g[i] + q[dist[i]]))
                sched.append({"arm": arm, "alpha": a, "i": i, "key": list(key(rows[i])), "F": F, "q": q[dist[i]]})
    return rows, sched


def cmd_replay():
    from main import SLIP
    from certgrip.sim import Sim, preload_force
    rows, sched = setup()
    os.makedirs(OUT, exist_ok=True)
    cache = {}
    with open(os.path.join(OUT, "replays.jsonl"), "w") as f:
        for s in sched:
            k = (tuple(s["key"]), round(s["F"], 9))
            if k not in cache:
                pool, fam, obj, d, sh = s["key"]
                sim = Sim(make_instance(pool, fam, obj, d, sh), preload_force(), delta_t=SLIP["delta_t"],
                          rot_t_deg=SLIP["rot_t_deg"], protocol="rd")
                cache[k] = bool(sim.run(s["F"])["slip"])
            f.write(json.dumps({"arm": s["arm"], "alpha": s["alpha"], "key": s["key"], "F": s["F"],
                                "slip_direct": cache[k]}) + "\n")
    print(f"scheduled: {len(sched)}, distinct replays: {len(cache)}")


def cmd_analyse(draws=2000, seed=31):
    rows, sched = setup()
    rep = {(r["arm"], r["alpha"], tuple(r["key"])): r for r in map(json.loads, open(os.path.join(OUT, "replays.jsonl")))}
    out = {"purpose": "p2 H1-V direct-replay audit (secondary after the H1-M failure)", "tau": TAU, "draws": draws}
    rng = np.random.default_rng(seed)
    for arm in ("CertGrip", "CSF-1"):
        for a in ALPHAS:
            ss = [s for s in sched if s["arm"] == arm and s["alpha"] == a]
            r_ = [rows[s["i"]] for s in ss]
            d = np.array([rep[(arm, a, tuple(s["key"]))]["slip_direct"] for s in ss], float)
            lab = np.array([1.0 if r["unavoidable"] else float(s["F"] < r["F_hi"]) for s, r in zip(ss, r_)])
            objs = {}
            for j, r in enumerate(r_):
                objs.setdefault((r["family"], r["obj"]), []).append(j)
            fams = sorted({k[0] for k in objs})
            byf = {fm: [k for k in objs if k[0] == fm] for fm in fams}
            boot_D, boot_d = [], []
            for _ in range(draws):
                idx = [j for fm in fams for t in rng.integers(0, len(byf[fm]), len(byf[fm])) for j in objs[byf[fm][t]]]
                boot_D.append((d[idx] - lab[idx]).mean()); boot_d.append(d[idx].mean())
            ci = [float(np.percentile(boot_D, 1.25)), float(np.percentile(boot_D, 98.75))]
            out[f"{arm}@{a}"] = {"n": len(ss), "slip_direct": float(d.mean()), "slip_label": float(lab.mean()),
                                 "Delta": float((d - lab).mean()), "Delta_CI**": ci,
                                 "slip_direct_CI**": [float(np.percentile(boot_d, 1.25)), float(np.percentile(boot_d, 98.75))],
                                 "disagree_up": int(((d == 1) & (lab == 0)).sum()), "disagree_down": int(((d == 0) & (lab == 1)).sum()),
                                 "decision": "pass" if ci[1] <= TAU else "failure" if ci[0] > TAU else "inconclusive"}
            print(f"{arm}@{a}: Delta {out[f'{arm}@{a}']['Delta']:.4f} CI** {ci} -> {out[f'{arm}@{a}']['decision']}")
    json.dump(out, open(os.path.join(ROOT, "v1/h1v_analysis.json"), "w"), indent=1)


if __name__ == "__main__":
    {"replay": cmd_replay, "analyse": cmd_analyse}[sys.argv[1]]()
