"""Build the p2 stage-18 [v3] prompt: build_stage18.py (verbatim template) on paper/mypaper/draft_v3.md with suffix
_v3, then insert results/v2 + v3 results JSON and the amendment pointers into the evidence block."""
import os
import runpy
import sys

SUF = sys.argv[1] if len(sys.argv) > 1 else "_v3"  # "_v3_pass2" for the second pass on the revised draft_v2.md
d = os.path.dirname(os.path.abspath(__file__))
P2 = os.path.join(d, "..", "..", "..")
sys.argv = ["build_stage18.py", "paper/mypaper/draft_v3.md", SUF]
runpy.run_path(os.path.join(d, "build_stage18.py"), run_name="__main__")
p = os.path.join(d, f"stage18{SUF}_user.txt")
u = open(p).read()
anchor = "\n\n(b) First 200 lines of the longest run log"
assert u.count(anchor) == 1
v2 = ("\n\n(a2) results/v2/results_v2.json (full; second-round SECONDARY rows of docs/09_amendment_v2.md; every block is "
      "an unchanged analysis file of results/v2/; compute in results/v2/compute_v2.json; raw replays in "
      "results/v2/crc09/, crc09e/, b3/; B3 plan plans/stage_13_v2_b3_online_physical.md):\n"
      + open(os.path.join(P2, "results/v2/results_v2.json")).read()
      + "\n\n(a3) results/v3/results_v3.json (full; third-round SECONDARY rows of docs/10_amendment_v3.md + addendum "
      "10a; every block is an unchanged analysis file of results/v3/; raw replays in results/v3/crc10/, crc10e/, react/, "
      "b3/; analysis code code/analysis_v3_a.py, _b.py, _c.py, _d.py, b3v3_online.py, react_run.py):\n"
      + open(os.path.join(P2, "results/v3/results_v3.json")).read())
open(p, "w").write(u.replace(anchor, v2 + anchor))
print(len(open(p).read().split()), "words")
