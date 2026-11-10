"""Amendment 11: Actions manifests for the v4 W-grid replays (workflow input workdir: papers/p2/code).
f4: 8 arms, 25 objects per job; c4: 4 arms, cal + test objects 50-349, 50 per job; np: CSF-1 noprobe, 150 per job.
Writes ../../../experiments/p2_crc_v4_{f4,c4,np}.json.  usage: python tools_v4_manifests.py"""
import json
import os

H = os.path.dirname(os.path.abspath(__file__))
EXP = os.path.join(H, "..", "..", "..", "experiments")
FAMS = ("F1", "F2", "F3", "F4")
SPEC = {"f4": (0, 300, 25, ""), "c4": (50, 350, 50, ""), "np": (0, 300, 150, " --rep-protocol noprobe")}
for name, (a, b, step, extra) in SPEC.items():
    pool = "c4" if name == "c4" else "f4"
    jobs = [{"id": f"p2v4_{name}_{f}_{s:03d}",
             "cmd": f"python main.py crc --grids ../v4/crc_grids_11_{name}.json --pool {pool}{extra} --family {f} "
                    f"--start {s} --count {min(step, b - s)} --budget-minutes 60 --out ../results/v4/crc_{name}/{f}_{s:03d}"}
            for f in FAMS for s in range(a, b, step)]
    json.dump({"purpose": f"p2 amendment 11 W-grid replays ({name})", "jobs": jobs},
              open(os.path.join(EXP, f"p2_crc_v4_{name}.json"), "w"), indent=1)
    print(name, len(jobs))
