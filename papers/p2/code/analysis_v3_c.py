"""Amendment 10 A3: Holm as registered (07 §4) for the v1 secondary rows with a CI**.
Re-runs the v1 secondary parts in memory with their recorded seeds / draws, capturing each bootstrap vector given to
secondaries_08f.ci; a vector is used only when its interval equals the stored one exactly (else: not adjusted).
p = min(1, 2 * min(share <= 0, share >= 0)); Holm at 5 % within each 07 family; sensitivity: Holm over all rows
(v1 secondaries here plus the v2 rows listed in V2_ROWS when their draws are captured the same way -- none are, see note).
Writes results/v3/a3_holm.json.  usage (from papers/p2/code): python analysis_v3_c.py
"""
import json
import os

import numpy as np

import secondaries_08f as s8f
import secondaries_08g as s8g
import secondaries_08h as s8h
from certgrip.io import ROOT

CAPT = []
_orig = s8f.ci


def _cap(v):
    out = _orig(v)
    CAPT.append((out, np.asarray(v, dtype=float)))
    return out


for m in (s8f, s8g, s8h):
    m.ci = _cap

# (stored file, callable, recorded draws)
RUNS = [("sec08f_tail.json", lambda: s8f.part_tail(2000)),
        ("sec08f_label.json", lambda: s8f.part_label(2000)),
        ("sec08g.json", lambda: dict(s8g.main(2000), H2n=s8g.h2n(2000))),
        ("sec08h_h1c.json", lambda: s8h.part_h1c(2000)),
        ("sec08h_h3s.json", lambda: s8h.part_h3s(2000)),
        ("sec08h_h4b.json", lambda: s8h.part_h4b(2000)),
        ("sec08h_massnoise.json", lambda: s8h.part_massnoise(2000))]

NONZERO_NULL = ("sec08f_tail", "H4c_", "oracle_decomposition")


def family(path):
    p = path
    if "sec08h_h1c" in p:
        return "H1c"
    if "sec08h_h3s" in p:
        return "H3-x"
    if "H4c" in p or "H4d" in p or "sec08h_h4b" in p:
        return "H4-x"
    if "oracle_decomposition" in p:
        return None
    return "H2-x"


def intervals(o, path):
    if isinstance(o, dict):
        for k, v in o.items():
            q = f"{path}/{k}"
            if k in ("CI**", "interval") and isinstance(v, list) and len(v) == 2:
                yield q, v
            else:
                yield from intervals(v, q)


def pval(v):
    return float(min(1.0, 2 * min(np.mean(v <= 0), np.mean(v >= 0))))


def holm(ps):
    order = np.argsort(ps); m = len(ps); adj = np.empty(m); run = 0.0
    for r, i in enumerate(order):
        run = max(run, min(1.0, (m - r) * ps[i])); adj[i] = run
    return adj


def main():
    rows = []
    for fn, fun in RUNS:
        CAPT.clear()
        fun()
        stored = json.load(open(os.path.join(ROOT, "v1", fn)))
        for path, iv in intervals(stored, fn[:-5]):
            hit = [v for out, v in CAPT if out[0] == iv[0] and out[1] == iv[1]]
            r = {"row": path, "family": family(path), "CI": iv,
                 "null_not_registered_threshold": any(t in path for t in NONZERO_NULL)}
            if hit:
                r["p"] = pval(hit[0]); r["draws"] = int(len(hit[0]))
            else:
                r["p"] = None; r["status"] = "not adjusted (interval not reproduced exactly)"
            rows.append(r)
        print(fn, "rows", sum(1 for r in rows if r["row"].startswith(fn[:-5])),
              "reproduced", sum(1 for r in rows if r["row"].startswith(fn[:-5]) and r["p"] is not None), flush=True)
    fams = {}
    for f in ("H1c", "H2-x", "H3-x", "H4-x"):
        idx = [i for i, r in enumerate(rows) if r["family"] == f and r["p"] is not None]
        if idx:
            adj = holm(np.array([rows[i]["p"] for i in idx]))
            for i, a in zip(idx, adj):
                rows[i]["p_holm_family"] = float(a); rows[i]["reject_family_5pct"] = bool(a <= 0.05)
            fams[f] = {"m": len(idx), "rejected": int(sum(a <= 0.05 for a in adj))}
    idx = [i for i, r in enumerate(rows) if r["p"] is not None]
    adj = holm(np.array([rows[i]["p"] for i in idx]))
    for i, a in zip(idx, adj):
        rows[i]["p_holm_all"] = float(a); rows[i]["reject_all_5pct"] = bool(a <= 0.05)
    out = {"note": "Amendment 10 A3. p two-sided vs 0 from the re-drawn bootstrap (recorded seeds / draws); Holm 5 % "
                   "within 07 §4 families and over all v1 secondary CI** rows. v2 rows: their bootstraps are not "
                   "re-drawn here (sensitivity over v1 rows only; stated).",
           "families": fams, "all": {"m": len(idx), "rejected": int(sum(a <= 0.05 for a in adj))}, "rows": rows}
    json.dump(out, open(os.path.join(ROOT, "v3", "a3_holm.json"), "w"), indent=1)
    print(json.dumps({"families": fams, "all": out["all"]}, indent=1))


if __name__ == "__main__":
    main()
