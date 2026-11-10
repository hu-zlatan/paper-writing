"""Collect every p2 v2 analysis JSON unchanged into results/v2/results_v2.json (v2 evidence index for stages 16-20).
Grid dumps (crc_grids_09*.json) and the sha256 freeze are referenced by name only."""
import json
import os

here = os.path.dirname(os.path.abspath(__file__))
b = os.path.join(here, "..", "results", "v2")
SKIP = {"crc_grids_09.json", "crc_grids_09e.json", "13_freeze.json", "results_v2.json"}
out = {"note": "p2 v2 (docs/09_amendment_v2.md, all rows secondary); every block is the unchanged content of the named "
               "file; crc_grids_09*.json and 13_freeze.json are referenced, not inlined"}
for name in sorted(os.listdir(b)):
    if name.endswith(".json") and name not in SKIP:
        out[name] = json.load(open(os.path.join(b, name)))
json.dump(out, open(os.path.join(b, "results_v2.json"), "w"), indent=1)
print(sorted(k for k in out if k != "note"))
