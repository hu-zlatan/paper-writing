"""Collect every p2 v1 analysis JSON unchanged into results/v1/results_v1.json (evidence index for stages 16-20).
Large per-grid dumps (crc_grids*.json) and the sha256 freeze are referenced by name only, not inlined."""
import json
import os

here = os.path.dirname(os.path.abspath(__file__))
b = os.path.join(here, "..", "results", "v1")
SKIP = {"crc_grids.json", "crc_grids_v2.json", "13_freeze.json", "results_v1.json"}
out = {"note": "p2 v1 (docs/08b_preregistration.md + 08c-08h); every block is the unchanged content of the named file; "
               "crc_grids*.json and 13_freeze.json are referenced, not inlined"}
for name in sorted(os.listdir(b)):
    if name.endswith(".json") and name not in SKIP:
        out[name] = json.load(open(os.path.join(b, name)))
json.dump(out, open(os.path.join(b, "results_v1.json"), "w"), indent=1)
print(sorted(k for k in out if k != "note"))
