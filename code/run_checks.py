"""T3 manipulation checks (docs/07_hypotheses.md §1.2): writes results/v1/checks/{confusability,myopia}_<set>.json."""
import json
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from touchbed.checks import confusability, myopia_bank  # noqa: E402

out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "results", "v1", "checks")
os.makedirs(out, exist_ok=True)
which = sys.argv[1] if len(sys.argv) > 1 else "all"
for s in ("S", "A"):
    if which in ("all", "myopia"):
        t = time.time()
        rows = myopia_bank(s, 0, 100)
        json.dump({"set": s, "params": {"n_particles": 1000, "C1": 16, "Y1": 8, "C2": 16, "M": 16,
                                        "fresh_reestimate": "selected a1 re-estimated with 2*Y1 outcomes, 4*M samples"},
                   "rows": rows, "wall_s": time.time() - t}, open(os.path.join(out, f"myopia_{s}.json"), "w"), indent=1)
        print("myopia", s, time.time() - t, flush=True)
    if which in ("all", "conf"):
        t = time.time()
        r = confusability(s)
        r["wall_s"] = time.time() - t
        json.dump(r, open(os.path.join(out, f"confusability_{s}.json"), "w"), indent=1)
        print("conf", s, r["C"], time.time() - t, flush=True)
