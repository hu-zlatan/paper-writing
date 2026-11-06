"""Manifest generator for the v5 student pipeline (amendment v5.0 E2 / v5.1). One recipe in every cell:
round 0 = distill on label3 0-2,999 minus held-out 1,200-1,499; DAgger r1 (beta 0.5) / r2 (beta 0), 800 episodes in
shards of 40; every distill = fixed 200 epochs, best held-out R-bar checkpoint, init = previous round's best weights,
training data = all label shards + every DAgger shard of earlier rounds (the v4 pattern, results/v4/d4/*_r1.json).

usage: python tools_v5_manifests.py <step> <cell> [<cell> ...]
  step: r0 | distill1 | dag2 | distill2      cell: S2 | S4 | S8 | S12 | A16-2
Checks that every input file exists (refuses to write a manifest that would fail on the runner)."""
import json
import os
import sys

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
SEEDS = range(701, 706)
CELLS = {"S2": ("S", 2, 4.7), "S4": ("S", 4, 4.8), "S8": ("S", 8, 4.8), "S12": ("S", 12, 4.9)}
A16_TAU = None  # filled from results/v5/12_cal_analysis.json once A16-2 is kept


def cell(c):
    if c == "A16-2":
        cal = json.load(open(os.path.join(ROOT, "results/v5/12_cal_analysis.json")))
        k = cal.get("keep", {}).get("A16", {})
        assert k.get("keep") is True and "A16_k2" in cal["tau"], "A16-2 not kept / not calibrated"
        return "A16", 2, cal["tau"]["A16_k2"]["tau"]
    return CELLS[c]


def label_shards(s, k):
    """(train, held-out) label shard paths relative to code/."""
    if (s, k) == ("S", 2):
        f = [f"../results/v4/labels/S_k2_r0_s{i:04d}.npz" for i in range(0, 3000, 50)]
        held = [p for p in f if 1200 <= int(p[-8:-4]) < 1500]
    elif (s, k) == ("S", 12):
        # v3 S12 labels: the exact lists of the v5 round-0 manifest (experiments/v5_d5_r0_S2_S12.json)
        m = json.load(open(os.path.join(ROOT, "experiments/v5_d5_r0_S2_S12.json")))
        cmd = next(j["cmd"] for j in m["jobs"] if "--kappa 12" in j["cmd"]).split()
        i, v = cmd.index("--shards"), cmd.index("--val-shards")
        tr = cmd[i + 1:v]
        held = []
        for t in cmd[v + 1:]:
            if t.startswith("--"):
                break
            held.append(t)
        return tr, held
    else:
        f = [f"../results/v5/labels/{s}_k{k}_r0_s{i:04d}.npz" for i in range(0, 3000, 50)]
        held = [p for p in f if 1200 <= int(p[-8:-4]) < 1500]
    return [p for p in f if p not in held], held


def dag_shards(s, k, sd, r):
    return [f"../results/v5/d5/{s}_k{k}_s{sd}_r{r}_{st:03d}.npz" for st in range(0, 800, 40)]


def check(paths):
    miss = [p for p in paths if not os.path.exists(os.path.join(ROOT, "code", p))]
    assert not miss, f"{len(miss)} missing, e.g. {miss[:3]}"


def jobs_for(step, c):
    s, k, tau = cell(c)
    tr, held = label_shards(s, k)
    out = []
    for sd in SEEDS:
        if step in ("r0", "distill1", "distill2"):
            r = {"r0": 0, "distill1": 1, "distill2": 2}[step]
            shards = list(tr) + [p for q in range(1, r + 1) for p in dag_shards(s, k, sd, q)]
            need = shards + held + ([f"../results/v5/d5/{s}_k{k}_s{sd}_r{r - 1}.npz"] if r else [])
            check(need)
            init = f" --init ../results/v5/d5/{s}_k{k}_s{sd}_r{r - 1}.npz" if r else ""
            out.append({"id": f"v5_d5_{c}_s{sd}_r{r}", "cmd": f"python main.py distill3 --set {s} --kappa {k} --tau {tau} --hp 0 "
                        f"--seed {sd} --round {r} --shards {' '.join(shards)} --val-shards {' '.join(held)}{init} "
                        f"--fixed-epochs 200 --keep best --budget-minutes 330 --out ../results/v5/d5/{s}_k{k}_s{sd}_r{r}"})
        elif step == "dag2":
            w = f"../results/v5/d5/{s}_k{k}_s{sd}_r1.npz"
            check([w])
            for st in range(0, 800, 40):
                out.append({"id": f"v5_dag_{c}_s{sd}_r2_{st:03d}", "cmd": f"python main.py dagger3 --set {s} --kappa {k} --tau {tau} "
                            f"--weights {w} --seed {sd} --round 2 --beta 0 --start {st} --count 40 --budget-minutes 25 "
                            f"--out ../results/v5/d5/{s}_k{k}_s{sd}_r2_{st:03d}"})
    return out


if __name__ == "__main__":
    step, cells = sys.argv[1], sys.argv[2:]
    jobs = [j for c in cells for j in jobs_for(step, c)]
    name = f"v5_{step}_{'_'.join(c.replace('-', '') for c in cells)}"
    json.dump({"purpose": f"v5 E2 {step} for {', '.join(cells)} (code/tools_v5_manifests.py; amendment v5.0/v5.1)", "jobs": jobs},
              open(os.path.join(ROOT, "experiments", name + ".json"), "w"), indent=1)
    print(name, len(jobs))
