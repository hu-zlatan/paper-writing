"""Dev pilot 2: does the evaluation PF converge? Same episodes (random policy, set A, T=10), N in {4000, 40000}."""
import os, sys, json, time
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
import numpy as np
from touchbed.evaluate import make_states, run_episode
from touchbed.likelihood import ObsModel
from touchbed.policies import RandomPolicy
om = ObsModel(); out = {}
lib, prior, states = make_states("A", "pilot", 20)
for N in (2000, 8000, 32000):
    t = time.time()
    res = [run_episode(RandomPolicy, lib, prior, om, s0, 10, ("A", "pilot1", 10, i), n_eval=N, needs_belief=False)[0]
           for i, s0 in enumerate(states)]
    row = {m: float(np.mean([r[m] for r in res])) for m in ("success", "identity_ok", "ig", "ball_info")}
    row["sec_per_episode"] = (time.time() - t) / len(states)
    out[N] = row
    print(N, json.dumps({k: round(v, 3) for k, v in row.items()}), flush=True)
json.dump(out, open(os.path.join(os.path.dirname(__file__), '..', '..', 'results', 'v1', 'dev', 'pilot2b_pf_convergence_contactq.json'), 'w'), indent=1)
