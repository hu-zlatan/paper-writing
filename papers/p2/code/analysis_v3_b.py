"""Amendment 10 B1 read-out (p2 v3): shrunk plug-in (CSF-shrunk@sigma, sigma 0.2 / 0.4) on the CRC route.
Arms: CSF-shrunk@s from results/v3/crc10/*.jsonl (grids results/v3/crc_grids_10.json); full_rd@s#0 and CSF-1 from the
v1 08c replays (results/v1/crc/*.jsonl). Same instances, same v1 cal / test split.
Registered read-out: D(full_rd@s#0 vs CSF-shrunk@s) with CI** (s 0.2, 0.4); also D(CSF-shrunk@s vs CSF-1) and arm
slip / RE / lambda-hat index (edge flag if a stratum's lambda-hat is on grid index 0 or 19 -> 08e recipe per the
amendment, reported). Refuses to compute unless every instance has exactly one v3 replay line.
CI** as code/analysis_crc.py.  Writes results/v3/b1_analysis.json.  usage: python analysis_v3_b.py [--check]"""
import argparse
import glob
import json
import os

import numpy as np

import analysis_crc as A
import analysis_v3_a as V

SIG = (0.2, 0.4)


EDGE = False   # --edge: CSF-shrunk@0.2 on the 08e-recipe grids (results/v3/crc_grids_10e.json, replays v3/crc10e/)


def load_v3():
    G = json.load(open(os.path.join(A.ROOT, "v3/crc_grids_10e.json" if EDGE else "v3/crc_grids_10.json")))
    keys = [tuple(k) for k in G["instances"]]
    rep = {}
    for f in sorted(glob.glob(os.path.join(A.ROOT, "v3/crc10e/*.jsonl" if EDGE else "v3/crc10/*.jsonl"))):
        for line in open(f):
            r = json.loads(line)
            if "key" in r:
                rep.setdefault(tuple(r["key"]), []).append(r)
    missing = [k for k in keys if k not in rep]
    dup = sum(1 for k in keys if len(rep.get(k, [])) > 1)
    return G, keys, rep, missing, dup


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--draws", type=int, default=2000)
    ap.add_argument("--edge", action="store_true")
    a = ap.parse_args()
    global EDGE
    EDGE = a.edge
    G3, keys3, rep3, missing, dup = load_v3()
    print(f"v3 instances {len(keys3)}, with replays {len(keys3) - len(missing)}, duplicates {dup}")
    if a.check or missing or dup:
        if (missing or dup) and not a.check:
            print("incomplete: refusing to analyse")
        return
    A.V2 = False
    G, keys, idx, rep, miss1, _ = A.load_real()
    assert not miss1 and keys == keys3
    D = A.build(G, keys, rep)
    keep = [f"full_rd@{s}#0" for s in SIG] + ["CSF-1"]
    D["L"] = {k: D["L"][k] for k in keep}
    D["F"] = {k: D["F"][k] for k in keep}
    for arm in G3["arms"]:
        D["L"][arm] = np.array([rep3[k][-1]["slip"][arm] for k in keys], dtype=bool)
        D["F"][arm] = np.array([rep3[k][-1]["F"][arm] for k in keys], dtype=float)
        D["L"][arm][~D["avoid"]] = True
    D["by_obj"] = {}
    for i, o in enumerate(D["obj"]):
        D["by_obj"].setdefault(o, []).append(i)
    cal_objs, test_objs = V.groups_of(D)
    ci0, ti0 = V.split_idx(D, cal_objs), V.split_idx(D, test_objs)

    def stats(ci, ti):
        m = {arm: V.metrics(D, arm, ci, ti, "crc") for arm in D["L"]}
        v = {}
        for s in SIG:
            if f"CSF-shrunk@{s}" not in m:
                continue
            sh, fu = f"CSF-shrunk@{s}", f"full_rd@{s}#0"
            v[f"D:{fu}_vs_{sh}"] = 1 - m[fu]["RE_mid"] / m[sh]["RE_mid"]
            v[f"D:{sh}_vs_CSF-1"] = 1 - m[sh]["RE_mid"] / m["CSF-1"]["RE_mid"]
        for arm in m:
            v[f"RE:{arm}"] = m[arm]["RE_mid"]
            v[f"slip:{arm}"] = m[arm]["slip_phys"]
        return v

    point = stats(ci0, ti0)
    boot = {k: [] for k in point}
    for ci, ti in V.boot_draws(D, cal_objs, test_objs, a.draws):
        v = stats(ci, ti)
        for k in point:
            boot[k].append(v[k])
    lam = {}
    st_c = D["strata"][ci0]
    for arm in G3["arms"]:
        lam[arm] = {}
        for s in np.unique(D["strata"]):
            j, at_max = A.lam_index(D["L"][arm][ci0[st_c == s]])
            lam[arm][str(s)] = {"idx": int(j), "at_max": bool(at_max), "edge": j in (0, D["L"][arm].shape[1] - 1)}
    res = {"purpose": "p2 amendment 10 B1 shrunk plug-in read-out (secondary)", "draws": a.draws,
           "ols": {arm: G3["arms"][arm]["ols"] for arm in G3["arms"]}, "lam_idx": lam,
           "rows": {k: {"point": point[k], "CI**": V.ci_of(boot[k]),
                        **({"decision": V.label(V.ci_of(boot[k]))} if k.startswith("D:") else {})} for k in point}}
    os.makedirs(os.path.join(A.ROOT, "v3"), exist_ok=True)
    name = "b1_analysis_edge.json" if EDGE else "b1_analysis.json"
    json.dump(res, open(os.path.join(A.ROOT, "v3", name), "w"), indent=1)
    print("wrote results/v3/" + name)


if __name__ == "__main__":
    main()
