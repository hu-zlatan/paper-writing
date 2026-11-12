"""Build the p2 stage-18 [v4] prompt: build_stage18.py (verbatim template) on paper/mypaper/draft_v4.md, then insert
results/v4/v4_analysis.json (confirmatory C1-C5 + S1-S7, docs/11_amendment_v4.md) and the v3 force-time file
results/v3/a7_integrated.json into the evidence block. Usage: python build_stage18_v4.py [suffix] (default _v4;
"_v4_pass2" for the second pass on the revised draft)."""
import os
import runpy
import sys

SUF = sys.argv[1] if len(sys.argv) > 1 else "_v4"
d = os.path.dirname(os.path.abspath(__file__))
P2 = os.path.join(d, "..", "..", "..")
sys.argv = ["build_stage18.py", "paper/mypaper/draft_v4.md", SUF]
runpy.run_path(os.path.join(d, "build_stage18.py"), run_name="__main__")
p = os.path.join(d, f"stage18{SUF}_user.txt")
u = open(p).read()
anchor = "\n\n(b) First 200 lines of the longest run log"
assert u.count(anchor) == 1
add = ("\n\n(a4) results/v4/v4_analysis.json (full; the v4 confirmatory read-out C1-C5 with Holm and secondaries S1-S7 "
       "of docs/11_amendment_v4.md, produced once by code/analysis_v4.py, committed before any v4 replay; raw replays in "
       "results/v4/ (labels/, preds/, crc/ and the grid files crc_grids_11_{f4,c4,np}.json); stage-14 record "
       "results/14_analysis_v4.md):\n" + open(os.path.join(P2, "results/v4/v4_analysis.json")).read()
       + "\n\n(a5) results/v3/a7_integrated.json (full; the force-time accounting incl. the probe's return to F0 and "
       "re-hold; code/ a7 script): \n" + open(os.path.join(P2, "results/v3/a7_integrated.json")).read()
       + "\n\n(a6) Earlier rounds, open as needed: results/v2/results_v2.json, results/v3/results_v3.json "
       "(docs/09_amendment_v2.md, docs/10_amendment_v3.md).")
open(p, "w").write(u.replace(anchor, add + anchor))
print(len(open(p).read().split()), "words")
