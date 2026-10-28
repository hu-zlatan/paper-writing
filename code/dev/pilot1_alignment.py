"""Dev pilot 1: is total information about the full state aligned with the success criterion? (random policy)"""
import os, sys, json
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
import numpy as np
from touchbed.evaluate import make_states, run_episode
from touchbed.likelihood import ObsModel
from touchbed.policies import RandomPolicy
om = ObsModel()
out = {}
for setname in ("S", "A"):
    for T in (3, 5, 10):
        lib, prior, states = make_states(setname, "pilot", 40)
        res = [run_episode(RandomPolicy, lib, prior, om, s0, T, (setname, "pilot1", T, i), n_eval=4000, needs_belief=False)[0]
               for i, s0 in enumerate(states)]
        row = {m: float(np.mean([r[m] for r in res])) for m in ("success", "identity_ok", "ig", "trans_err_mm", "rot_err_deg")}
        row["median_trans_err_mm"] = float(np.median([r["trans_err_mm"] for r in res]))
        row["median_rot_err_deg"] = float(np.median([r["rot_err_deg"] for r in res]))
        out[f"{setname}_T{T}"] = row
        print(setname, T, json.dumps({k: round(v, 3) for k, v in row.items()}), flush=True)
json.dump(out, open(os.path.join(os.path.dirname(__file__), '..', '..', 'results', 'v1', 'dev', 'pilot1_alignment.json'), 'w'), indent=1)
