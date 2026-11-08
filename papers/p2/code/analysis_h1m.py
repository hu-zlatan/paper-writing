"""H1-M read-out (07_hypotheses H1-M as frozen in docs/08b §4: one-sided 98.75 % Clopper-Pearson upper limit of the
non-monotone rate <= 2 %, i.e. <= 7 of 800 id instances). Also: per-family and per-disturbance counts (descriptive),
shift pools (descriptive), and where the violations sit relative to F*_hi. Writes results/v1/h1m_analysis.json."""
import glob
import json
import os

import numpy as np
from scipy.stats import beta

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "results", "v1")


def rows(pattern):
    out = []
    for f in sorted(glob.glob(os.path.join(ROOT, "mono", pattern))):
        out += [json.loads(l) for l in open(f) if l.strip() and '"inst"' in l]
    return out


def cp_upper(k, n, level=0.9875):
    return float(beta.ppf(level, k + 1, n - k)) if k < n else 1.0


def main():
    idr = rows("id_F[1-4].jsonl")
    k = sum(r["non_monotone"] for r in idr)
    viol = []
    for r in idr + rows("id_F1_S*.jsonl") + rows("s2_*.jsonl"):
        if r["non_monotone"]:
            F, s = r["forces"], r["slip"]
            j = next(i for i, o in enumerate(s) if not o)
            top = max(F[i] for i in range(j, len(s)) if s[i])
            viol.append({"pool": r["pool"], "shift": r["shift"], "family": r["family"], "obj": r["obj"], "dist": r["dist"],
                         "F_hi": r["F_hi"], "first_no_slip": F[j], "max_slip_above": top,
                         "rel_above_F_hi": top / r["F_hi"] - 1 if r["F_hi"] else None})
    out = {"n": len(idr), "non_monotone": k, "cp_upper_98.75": cp_upper(k, len(idr)), "threshold_count": 7,
           "gate_pass": k <= 7,
           "by_family": {f: int(sum(r["non_monotone"] for r in idr if r["family"] == f)) for f in ("F1", "F2", "F3", "F4")},
           "by_dist": {d: int(sum(r["non_monotone"] for r in idr if r["dist"] == d)) for d in ("D1", "D2", "D3", "D4")},
           "shift_pools": {n: {"n": len(rows(p)), "non_monotone": int(sum(r["non_monotone"] for r in rows(p)))}
                           for n, p in (("S1", "id_F1_S1.jsonl"), ("S3", "id_F1_S3.jsonl"), ("S2", "s2_*.jsonl"))},
           "violations": viol,
           "max_rel_above_F_hi": float(max(v["rel_above_F_hi"] for v in viol if v["rel_above_F_hi"] is not None)) if viol else None}
    json.dump(out, open(os.path.join(ROOT, "h1m_analysis.json"), "w"), indent=1)
    print({k2: v for k2, v in out.items() if k2 != "violations"})


if __name__ == "__main__":
    main()
