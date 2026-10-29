"""Collect every v3 analysis output (results/v3/12_*.json, 14_*.json) into results/v3/results_v3.json, the data
context of stage 14. Values are copied unchanged; nothing is recomputed here."""
import glob
import json
import os

base = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "results", "v3")
out = {}
for f in sorted(glob.glob(os.path.join(base, "1[24]_*.json"))):
    out[os.path.basename(f)[:-5]] = json.load(open(f))
json.dump(out, open(os.path.join(base, "results_v3.json"), "w"), indent=1)
print(len(out), "files:", ", ".join(out))
