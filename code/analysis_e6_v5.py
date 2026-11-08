"""v5 E6 latency (amendment v5.0 E6, addendum v5.1f) on results/v5/lat/*.jsonl (latency3, Lat' protocol, pilot3).
Per cell, job 1 (<tag>_s701_gstar): median L_dec with a bootstrap 95 % CI over decisions (B = 2,000, as
analysis_lat_v3) for the student, full G* (g2000_512_64) and the reduced G* configs g125_512_16 / g500_512_4, all timed
on the same decision states on one runner; the per-decision ratio full G* / student (median, CI) and median L_final.
Job 2 (<tag>_s70x, students 702-705): median student L_dec per seed (seed spread; another runner). Protocol complete
iff every CI half-width <= 10 % of its median (the v3 Lat' criterion). Writes results/v5/14_e6_analysis.json."""
import glob
import json
import os

import numpy as np

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "results", "v5")
CELLS = {"S2": "S_k2", "S4": "S_k4", "S8": "S_k8", "S12": "S_k12", "A16-2": "A16_k2"}
B = 2000


def rows(path):
    if not os.path.exists(path):
        return None, None
    r = [json.loads(l) for l in open(path)]
    return [x for x in r if "timers" in x], [x for x in r if x.get("final")]


def med_ci(v, rng):
    v = np.asarray(v, float)
    bs = np.median(rng.choice(v, (B, len(v))), axis=1)
    m = float(np.median(v))
    lo, hi = float(np.quantile(bs, 0.025)), float(np.quantile(bs, 0.975))
    return {"median": m, "ci95": [lo, hi], "n": len(v), "half_width_ok": bool(max(m - lo, hi - m) <= 0.1 * m)}


def main():
    rng = np.random.default_rng(0)
    out = {}
    for c, tag in CELLS.items():
        res = {}
        # addendum v5.1g: a cell whose 500-decision job 1 failed the 10 % half-width rule is re-timed with 1,000
        # decisions on one runner (v3 Lat' "500 more decisions"); that record, when present, is the job-1 record.
        p1000 = os.path.join(ROOT, "lat", f"{tag}_s701_gstar_d1000.jsonl")
        res["job1_source"] = os.path.basename(p1000) if os.path.exists(p1000) else f"{tag}_s701_gstar.jsonl"
        recs, fin = rows(os.path.join(ROOT, "lat", res["job1_source"]))
        if recs:
            ms = list(recs[0]["timers"])
            res["job1"] = {m: med_ci([x["timers"][m]["L_dec"] for x in recs], rng) for m in ms}
            res["job1"]["ratio_full_gstar_over_student"] = med_ci(
                [x["timers"]["g2000_512_64"]["L_dec"] / x["timers"]["student"]["L_dec"] for x in recs], rng)
            res["job1"]["L_final_median_s"] = float(np.median([f["L_final_s"] for f in fin]))
            res["job1_complete"] = all(v["half_width_ok"] for k, v in res["job1"].items() if isinstance(v, dict))
        res["job2"] = {}
        for sd in (702, 703, 704, 705):
            r2, _ = rows(os.path.join(ROOT, "lat", f"{tag}_s{sd}.jsonl"))
            if r2:
                res["job2"][str(sd)] = med_ci([x["timers"]["student"]["L_dec"] for x in r2], rng)
        out[c] = res
    json.dump(out, open(os.path.join(ROOT, "14_e6_analysis.json"), "w"), indent=1)
    print({c: ("job1" in r, len(r["job2"])) for c, r in out.items()})


if __name__ == "__main__":
    main()
