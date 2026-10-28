import time, numpy as np, sys
sys.path.insert(0, __import__('os').path.join(__import__('os').path.dirname(__file__), '..'))
from touchbed.evaluate import make_states, run_episode
from touchbed.likelihood import ObsModel
from touchbed.policies import RandomPolicy, CoveragePolicy, GreedyEIGPolicy
om = ObsModel()
for setname in ("S", "A"):
    lib, prior, states = make_states(setname, "pilot", 6)
    for name, fac, nb in (("random", RandomPolicy, False), ("coverage", CoveragePolicy, True), ("greedy", GreedyEIGPolicy, True)):
        t0 = time.time(); res = []
        for i, s0 in enumerate(states):
            r, lat = run_episode(fac, lib, prior, om, s0, 5, (setname, "pilot", 5, i), n_eval=10000)
            res.append(r)
        print(setname, name, "succ", np.mean([r["success"] for r in res]), "id", np.mean([r["identity_ok"] for r in res]),
              "ig", round(np.mean([r["ig"] for r in res]), 2), "lat_ms", round(1000*np.median([r["latency_median_s"] for r in res]), 2),
              "ep_s", round((time.time()-t0)/len(states), 2), flush=True)
