"""v6 g_T for the v6 test5 records (amendment v6.0 step 3; same gt3 command and file rule as tools_v5_gt.py): run `main.py gt3` (J 16, L 4095) in the sandbox on every committed test5 eval3 file
of G*, students, RL and rl_success that has no g_T output yet. One output per source file:
results/v6/test5/<name>.jsonl -> results/v6/test5_gt/<name>.jsonl. Source files are final once committed (each runner
job commits once at its end; follow-up shards get new names). Prints counts only.
usage: python tools_v6_gt.py [--workers 2]"""
import glob
import os
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor

HERE = os.path.dirname(os.path.abspath(__file__))
SRC, DST = os.path.join(HERE, "..", "results/v6/test5"), os.path.join(HERE, "..", "results/v6/test5_gt")
KEEP = ("_gstar_", "_student_s", "_rl_s", "_rlsucc_s")


def todo():
    out = []
    for f in sorted(glob.glob(os.path.join(SRC, "*.jsonl"))):
        n = os.path.basename(f)
        if any(k in n for k in KEEP) and not os.path.exists(os.path.join(DST, n)):
            out.append(f)
    return out


def run(f):
    n = os.path.basename(f)[:-6]
    env = dict(os.environ, OMP_NUM_THREADS="1", OPENBLAS_NUM_THREADS="1", MKL_NUM_THREADS="1")
    tmp = os.path.join(DST, "." + n)
    r = subprocess.run([sys.executable, "main.py", "gt3", "--src", f, "--out", tmp], cwd=HERE, env=env,
                       capture_output=True, text=True)
    if r.returncode == 0:
        os.replace(tmp + ".jsonl", os.path.join(DST, n + ".jsonl"))   # only complete outputs get the final name
    return r.returncode


if __name__ == "__main__":
    w = int(sys.argv[sys.argv.index("--workers") + 1]) if "--workers" in sys.argv else 2
    os.makedirs(DST, exist_ok=True)
    fs = todo()
    with ThreadPoolExecutor(w) as ex:
        codes = list(ex.map(run, fs))
    print(f"gt3 files: {len(fs)}, failed: {sum(c != 0 for c in codes)}")
