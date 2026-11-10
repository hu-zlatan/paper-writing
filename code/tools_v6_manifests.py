"""Amendment v6.0 / addendum v6.1: build the E8-E12 manifests (no outcome is read; per-episode times come from the v5
test5 wall_s means and the P6 pilot). Commands are the v5 test5 commands (experiments/v5_test5*.json) with new episode
ranges / methods / output paths. Each manifest has <= 250 jobs (GitHub matrix limit 256).
usage: python code/tools_v6_manifests.py   (from the repo root) -> experiments/v6_<row>_p<k>.json"""
import glob
import json
import os
import re

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
SEC = {"A16_k2": dict(b_cov=313.7, b_fan=79, b_spread=184.7, gstar=81.4, rl=161.9, student=67),
       "S_k12": dict(b_cov=78.8, b_fan=43.5, b_spread=142, gstar=41.8, rl=66.3, student=45.5),
       "S_k2": dict(b_cov=73.7, b_fan=44.2, b_spread=148.4, gstar=36.2, rl=38.9, student=30.3),
       "S_k4": dict(b_cov=79.1, b_fan=45.1, b_spread=149.3, gstar=36.9, rl=54.9, student=37.2),
       "S_k8": dict(b_cov=80.1, b_fan=46.9, b_spread=152.3, gstar=44.4, rl=56.8, student=41.9)}
SUB16_S = 245.0
TARGET_S = 1000.0          # ~17 min of work per job; the 25-min eval3 time guard stops a slow job at 20 min
BASE = " --sub 8 --budget-minutes 25"


def v5_specs():
    spec = {}
    for f in sorted(glob.glob(os.path.join(ROOT, "experiments", "v5_test5*.json"))):
        for j in json.load(open(f))["jobs"]:
            m = re.search(r"--out \.\./results/v5/test5/(\S+)_(\d+)(_\S+)?$", j["cmd"])
            if m:
                spec.setdefault(m.group(1), re.sub(r" --start \d+ --count \d+.*", "", j["cmd"]))
    return spec


def kind(name):
    for k in ("b_cov", "b_fan", "b_spread", "gstar", "student", "rlsucc", "rl"):
        if f"_{k}" in name:
            return "rl" if k == "rlsucc" else k
    raise ValueError(name)


def chunks(prefix, out, lo, hi, sec):
    n = max(1, int(TARGET_S // sec))
    return [{"id": f"{os.path.basename(out)}_{s:03d}", "cmd": f"{prefix} --start {s} --count {min(n, hi - s)}{BASE} "
             f"--out ../results/v6/test5/{out}_{s:03d}"} for s in range(lo, hi, n)]


def main():
    spec = v5_specs()
    assert len(spec) == 85, len(spec)
    rows = {"e8": [], "e9": [], "e10": [], "e11": [], "e12": []}
    for name, pre in sorted(spec.items()):
        if "_random" in name:
            continue                                                   # v6.0 E8: random is not extended
        tag = name.split("_gstar")[0].split("_student")[0].split("_rl")[0].split("_b_")[0]
        rows["e8"] += chunks(pre, name, 300, 500, SEC[tag][kind(name)])
    for tag in SEC:
        g = spec[f"{tag}_gstar"]
        for cfg in ("g125_512_16", "g500_512_4"):
            rows["e9"] += chunks(g.replace("--method gstar", f"--method {cfg}"), f"{tag}_{cfg}", 0, 500, SEC[tag]["gstar"])
        rows["e10"] += chunks(g + " --run-salt r1", f"{tag}_gstar2", 0, 500, SEC[tag]["gstar"])
        for s in range(701, 706):
            st = spec[f"{tag}_student_s{s}"]
            assert st.endswith("--split test5") and f"_s{s}_r2.npz" in st
            rows["e11"] += chunks(st.replace(f"_s{s}_r2.npz", f"_s{s}_r0.npz"), f"{tag}_r0student_s{s}", 0, 500,
                                  SEC[tag]["student"])
        for m in ["gstar"] + [f"student_s{s}" for s in range(701, 706)]:
            if tag in ("S_k2", "S_k12") and m in ("gstar", "student_s701"):
                continue                                               # v5 E5 already re-read 0-199 at sub 16
            src = " ".join(sorted(os.path.relpath(p, os.path.join(ROOT, "code"))
                                  for p in glob.glob(os.path.join(ROOT, "results", "v5", "test5", f"{tag}_{m}_*.jsonl"))))
            n = max(1, int(TARGET_S // SUB16_S))
            for s in range(0, 100, n):
                eps = " ".join(str(e) for e in range(s, min(100, s + n)))
                rows["e12"].append({"id": f"{tag}_{m}_sub16_{s:03d}",
                                    "cmd": f"python main.py regrid3 --src {src} --episodes {eps} --sub 16 "
                                           f"--budget-minutes 25 --out ../results/v6/e12/{tag}_{m}_sub16_{s:03d}"})
    for r, jobs in rows.items():
        for k in range(0, len(jobs), 250):
            part = jobs[k:k + 250]
            p = os.path.join(ROOT, "experiments", f"v6_{r}_p{k // 250}.json")
            json.dump({"purpose": f"v6 {r.upper()} (docs/07c_amendment_v6_0.md, addendum v6.1), part {k // 250}",
                       "jobs": part}, open(p, "w"), indent=1)
        print(r, len(jobs), "jobs")


if __name__ == "__main__":
    main()
