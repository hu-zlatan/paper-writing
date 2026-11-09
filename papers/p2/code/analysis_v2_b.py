"""Amendment 09 part B read-out (p2 v2, secondary).
B1 / H5: D(CertGrip-full sigma 0.2 vs CSF-proxy@sp) on the 08c CRC route, sp in 0.2 / 0.4 / 0.8, CI** as in
   code/analysis_crc.py (object-cluster bootstrap within family, lambda-hat refitted, 2,000 draws, seed 2026); grid-edge
   flags (lambda-hat index 0 or 19) reported per stratum. CertGrip-full replays: results/v1/crc (08c).
B2: probe + fixed margin (no calibration): test (and cal) physical slip and RE per margin m and stratum.
Inputs: results/v2/crc_grids_09.json, results/v2/crc09/*.jsonl. Refuses to analyse an incomplete set.
Writes results/v2/b_analysis.json.  usage (from papers/p2/code): python analysis_v2_b.py [--draws 2000]"""
import argparse
import glob
import json
import os

import numpy as np

import analysis_crc as A

TARGET, SP = "full_rd@0.2#0", (0.2, 0.4, 0.8)
MARGINS = (0.0, 0.25, 0.5, 1.0)


def load09(tag="09"):
    G = json.load(open(os.path.join(A.ROOT, f"v2/crc_grids_{tag}.json")))
    keys = [tuple(k) for k in G["instances"]]
    rep = {}
    for f in sorted(glob.glob(os.path.join(A.ROOT, f"v2/crc{tag}/*.jsonl"))):
        for line in open(f):
            r = json.loads(line)
            if "key" in r:
                rep.setdefault(tuple(r["key"]), []).append(r)
    return G, keys, rep, [k for k in keys if k not in rep]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--draws", type=int, default=2000)
    ap.add_argument("--edge", action="store_true", help="B1 edge rule: CSF-proxy@0.2 on 08e-recipe grids vs CertGrip-full 08e")
    a = ap.parse_args()
    if a.edge:
        return b1_edge(a.draws)
    G9, k9, rep9, missing = load09()
    print(f"instances {len(k9)}, missing {len(missing)}")
    if missing:
        print("incomplete: refusing to analyse")
        return
    G1, k1, _, rep1, miss1, _ = A.load_real()
    assert k1 == k9 and not miss1
    D1 = A.build(G1, k1, rep1)
    D = A.build(G9, k9, rep9)
    D["L"][TARGET], D["F"][TARGET] = D1["L"][TARGET], D1["F"][TARGET]
    marg = {"L": D["L"].pop("margin@0.2"), "F": D["F"].pop("margin@0.2")}
    # B1 via the registered CRC machinery
    old = A.contrasts
    A.contrasts = lambda: {f"H5@{sp}": (TARGET, f"CSF-proxy@{sp}") for sp in SP}
    res = A.analyse(D, draws=a.draws)
    A.contrasts = old
    for k, c in res["contrasts"].items():
        lo, hi = c["CI**"]["mid"]
        c["decision_09"] = "superiority" if lo > 0 else ("inferiority" if hi < 0 else "not shown")
    edge = {arm: {s: j for s, j in v["lam_idx"].items() if j in (0, 19)} for arm, v in res["arms"].items()}
    # B2 descriptive
    split = np.array(D["split"])
    st = D["strata"]
    b2 = {}
    for j, m in enumerate(MARGINS):
        row = {}
        for part in ("cal", "test"):
            idx = np.where(split == part)[0]
            av = D["avoid"][idx]
            F = marg["F"][idx, j]
            ref = D["ref"]["mid"][idx]
            row[part] = {"slip_phys": float(marg["L"][idx, j].mean()),
                         "RE_mid": float(np.mean((F[av] - ref[av]) / ref[av])),
                         "by_stratum_slip": {s: float(marg["L"][idx[st[idx] == s], j].mean()) for s in ("D1", "D2", "D3", "D4")}}
        b2[str(m)] = row
    out = {"purpose": "p2 v2 amendment 09 part B (H5 CSF-proxy, probe + fixed margin); secondary", "draws": a.draws,
           "H5": res["contrasts"], "arms": res["arms"], "grid_edge_lam_idx": edge, "B2_margin": b2,
           "n_cal_instances": res["n_cal_instances"], "n_test_instances": res["n_test_instances"]}
    json.dump(out, open(os.path.join(A.ROOT, "v2/b_analysis.json"), "w"), indent=1)
    for k, c in res["contrasts"].items():
        print(k, round(c["D"]["mid"], 4), [round(x, 4) for x in c["CI**"]["mid"]], c["decision_09"])
    print("edge", edge)
    for m, r in b2.items():
        print("margin", m, round(r["test"]["slip_phys"], 4), round(r["test"]["RE_mid"], 4))


def b1_edge(draws):
    G9, k9, rep9, missing = load09("09e")
    print(f"instances {len(k9)}, missing {len(missing)}")
    if missing:
        print("incomplete: refusing to analyse")
        return
    A.V2 = True
    G1, k1, _, rep1, miss1, _ = A.load_real()
    assert k1 == k9 and not miss1
    D1 = A.build(G1, k1, rep1)
    D = A.build(G9, k9, rep9)
    D["L"][TARGET], D["F"][TARGET] = D1["L"][TARGET], D1["F"][TARGET]
    old = A.contrasts
    A.contrasts = lambda: {"H5@0.2_08e": (TARGET, "CSF-proxy@0.2")}
    res = A.analyse(D, draws=draws)
    A.contrasts = old
    c = res["contrasts"]["H5@0.2_08e"]
    lo, hi = c["CI**"]["mid"]
    c["decision_09"] = "superiority" if lo > 0 else ("inferiority" if hi < 0 else "not shown")
    out = {"purpose": "p2 v2 amendment 09 B1 edge rule (08e-recipe grids, 41 points)", "draws": draws,
           "H5": res["contrasts"], "arms": res["arms"],
           "grid_edge_lam_idx": {arm: {s: j for s, j in v["lam_idx"].items() if j in (0, 40)} for arm, v in res["arms"].items()}}
    json.dump(out, open(os.path.join(A.ROOT, "v2/b_analysis_edge.json"), "w"), indent=1)
    print(round(c["D"]["mid"], 4), [round(x, 4) for x in c["CI**"]["mid"]], c["decision_09"], out["grid_edge_lam_idx"])


if __name__ == "__main__":
    main()
