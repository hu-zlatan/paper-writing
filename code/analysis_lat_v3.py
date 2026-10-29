"""Gate Lat' (07_hypotheses_v3 §1.8, §4; amendment v3.0 C11) on results/v3/lat/S_k12_pilot.jsonl.
Per method: median L_dec (and components) with a bootstrap 95 % CI over decisions (B = 2,000); protocol complete iff
every CI half-width <= 10 % of its median. Q = greedy configurations with median L_dec <= 100 x median L_dec(student);
R_b candidates = maximal elements of Q under the componentwise order on (N, C, M). H1-fb active iff
median L_dec(G* full = g2000_512_64) / median L_dec(pruned16) >= 10. Also the per-decision ratio of G* full to the
student (report-only here; the claim is tested on test decisions after the main runs) and L_final.
Writes results/v3/12_lat_analysis.json."""
import json
import os

import numpy as np

base = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "results", "v3")
files = [f for f in ("S_k12_pilot.jsonl", "S_k12_pilot_more.jsonl") if os.path.exists(os.path.join(base, "lat", f))]
rows = [json.loads(l) for f in files for l in open(os.path.join(base, "lat", f))]
recs = [r for r in rows if "timers" in r]
finals = [r for r in rows if r.get("final")]
rng = np.random.default_rng(0)
B = 2000
methods = list(recs[0]["timers"].keys())


def med_ci(x):
    x = np.asarray(x)
    bs = np.array([np.median(x[rng.integers(0, len(x), len(x))]) for _ in range(B)])
    lo, hi = np.quantile(bs, [0.025, 0.975])
    m = float(np.median(x))
    return {"median": m, "ci": [float(lo), float(hi)], "half_width_rel": float((hi - lo) / 2 / m) if m > 0 else None}


out = {"files": files, "n_decisions": len(recs), "n_episodes": len({r["episode"] for r in recs}), "methods": {}}
for m in methods:
    L = [r["timers"][m]["L_dec"] for r in recs]
    comp = {k: float(np.median([r["timers"][m][k] for r in recs])) for k in recs[0]["timers"][m] if k != "L_dec"}
    out["methods"][m] = {**med_ci(L), "component_medians": comp}
out["protocol_complete"] = bool(all(v["half_width_rel"] is not None and v["half_width_rel"] <= 0.10
                                    for v in out["methods"].values()))
out["ci_too_wide"] = [m for m, v in out["methods"].items() if v["half_width_rel"] is None or v["half_width_rel"] > 0.10]
st = out["methods"]["student"]["median"]
cfg = {m: tuple(int(v) for v in m[1:].split("_")) for m in methods if m.startswith("g") and m.count("_") == 2}
Q = [m for m in cfg if out["methods"][m]["median"] <= 100 * st]
maximal = [m for m in Q if not any(o != m and all(a >= b for a, b in zip(cfg[o], cfg[m])) for o in Q)]
out["student_median_s"] = st
out["Q"] = sorted(Q, key=lambda m: cfg[m])
out["R_b_candidates"] = sorted(maximal, key=lambda m: cfg[m])
out["Q_empty"] = not Q
full = out["methods"]["g2000_512_64"]["median"]
out["ratio_full_over_student"] = full / st
out["ratio_full_over_pruned16"] = full / out["methods"]["pruned16"]["median"]
out["H1_fb_active"] = bool(out["ratio_full_over_pruned16"] >= 10)
out["L_final"] = med_ci([r["L_final_s"] for r in finals])
print(json.dumps({k: v for k, v in out.items() if k != "methods"}, indent=1))
json.dump(out, open(os.path.join(base, "12_lat_analysis.json"), "w"), indent=1)
