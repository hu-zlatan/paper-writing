"""Behaviour diagnostics on test3 (stage 18 v3 review items; report-only, no test): per method, finger travel per
episode (degrees), probe-count distribution, fraction of decisions that move the finger by more than one phi grid step,
g_T saturation at log(L+1); RL final policy entropy; teacher tie fraction in the distillation logs; training epochs and
wall time per student round. Inputs: results/v3/test3 (no-grid, 0-499), test3_sub8 (B-fan, 0-299), h2, rl, d3, d3rem.
Writes results/v3/14_behaviour.json."""
import glob
import json
import math
import os
import re
from collections import Counter

b = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "results", "v3")
N_PHI, N_PSI = 64, 8
STEP = 2 * math.pi / N_PHI


def rows(pattern):
    r = {}
    for f in sorted(glob.glob(os.path.join(b, pattern))):
        for line in open(f):
            d = json.loads(line)
            if "episode" in d and "header" not in d:
                r[d["episode"]] = d
    return r


def phi_moves(actions, phi0_idx=None):
    """Grid-step moves between consecutive probes (the first probe's start angle is not logged -> skipped)."""
    idx = [a // N_PSI for a in actions]
    out = []
    for i in range(1, len(idx)):
        d = abs(idx[i] - idx[i - 1]) % N_PHI
        out.append(min(d, N_PHI - d))
    return out


groups = {"gstar": "test3/S_k12_gstar_*.jsonl", "random": "test3/S_k12_random_*.jsonl",
          "student_rem_s501": "test3/S_k12_student_rem_s501_*.jsonl",
          "student_rem_s502": "test3/S_k12_student_rem_s502_*.jsonl",
          "student_rem_s503": "test3/S_k12_student_rem_s503_*.jsonl",
          "rl_s511": "test3/S_k12_rl_s511_*.jsonl", "rl_s512": "test3/S_k12_rl_s512_*.jsonl",
          "rl_s513": "test3/S_k12_rl_s513_*.jsonl", "b_fan": "test3_sub8/S_k12_b_fan_*.jsonl"}
out = {"note": "report-only diagnostics; travel_rad is the logged total finger travel per episode",
       "grid_step_deg": 360 / N_PHI, "methods": {}}
for name, pat in groups.items():
    r = rows(pat)
    if not r:
        continue
    eps = sorted(r)
    if name == "b_fan":
        eps = [e for e in eps if e < 300]
    trav = [math.degrees(r[e]["travel_rad"]) for e in eps]
    probes = Counter(r[e]["n_probes"] for e in eps)
    mv = [m for e in eps for m in phi_moves(r[e]["actions"])]
    m = {"n_episodes": len(eps), "travel_deg_mean": sum(trav) / len(trav),
         "travel_deg_median": sorted(trav)[len(trav) // 2], "travel_deg_max": max(trav),
         "probes_mean": sum(r[e]["n_probes"] for e in eps) / len(eps),
         "probes_hist": {str(k): v for k, v in sorted(probes.items())},
         "frac_between_probe_moves_gt_1_step": (sum(1 for x in mv if x > 1) / len(mv)) if mv else None,
         "frac_between_probe_moves_eq_0": (sum(1 for x in mv if x == 0) / len(mv)) if mv else None}
    h = os.path.join(b, "h2", f"S_k12_{name}.jsonl")
    if os.path.exists(h):
        g = [json.loads(l) for l in open(h)]
        g = [x for x in g if "g_T" in x]
        cap = math.log(g[0]["L"] + 1)
        m["gT_n"] = len(g)
        m["gT_cap_log_L_plus_1"] = cap
        m["gT_saturated_frac"] = sum(1 for x in g if x["g_T"] >= cap - 1e-6) / len(g)
    out["methods"][name] = m
for f in sorted(glob.glob(os.path.join(b, "rl", "S_k12_rel_cfg2_sd51?.json"))):
    d = json.load(open(f))
    last = d["history"][-1]
    out.setdefault("rl_final", {})[os.path.basename(f)[:-5]] = {k: last[k] for k in ("episodes", "entropy", "probes_mean", "sat_frac")}
ties, rounds = [], {}
for f in sorted(glob.glob(os.path.join(b, "d3*", "*.json"))):
    s = open(f).read()
    ties += [float(x) for x in re.findall(r'"val_tie_fraction": ([0-9.eE-]+)', s)]
    d = json.loads(s)
    if isinstance(d, dict) and isinstance(d.get("log"), list) and d["log"]:
        rounds[os.path.relpath(f, b)] = {"epochs": len(d["log"]), "wall_s": d.get("wall_s"),
                                         "train_loss_last": d["log"][-1].get("train_loss"),
                                         "train_loss_prev": d["log"][-2].get("train_loss") if len(d["log"]) > 1 else None,
                                         "status": d.get("status")}
out["teacher_tie_fraction"] = {"n_logged": len(ties), "max": max(ties) if ties else None}
out["student_rounds"] = rounds
ep = [v["epochs"] for v in rounds.values()]; ws = [v["wall_s"] for v in rounds.values() if v["wall_s"]]
out["student_rounds_summary"] = {"n_rounds": len(ep), "epochs_min": min(ep), "epochs_max": max(ep),
                                 "wall_s_min": min(ws), "wall_s_max": max(ws)}
json.dump(out, open(os.path.join(b, "14_behaviour.json"), "w"), indent=1)
print(json.dumps({k: {kk: (vv if not isinstance(vv, dict) else "…") for kk, vv in v.items()} if isinstance(v, dict) else v for k, v in out["methods"].items()}, indent=1))
print(json.dumps(out.get("rl_final"), indent=1), out["teacher_tie_fraction"], len(rounds))
