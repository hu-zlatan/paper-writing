"""Collect every p2 v3 analysis JSON unchanged into results/v3/results_v3.json (v3 evidence index for stages 16-20).
Grid dumps (crc_grids_10*.json) are referenced by name only."""
import json
import os

here = os.path.dirname(os.path.abspath(__file__))
b = os.path.join(here, "..", "results", "v3")
SKIP = {"crc_grids_10.json", "crc_grids_10e.json", "results_v3.json"}
out = {"note": "p2 v3 (docs/10_amendment_v3.md, all rows secondary); every block is the unchanged content of the named "
               "file; crc_grids_10*.json are referenced, not inlined"}
for name in sorted(os.listdir(b)):
    if name.endswith(".json") and name not in SKIP:
        out[name] = json.load(open(os.path.join(b, name)))
json.dump(out, open(os.path.join(b, "results_v3.json"), "w"), indent=1)
print(sorted(k for k in out if k != "note"))
