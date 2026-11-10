"""Amendment 11: apply the frozen v1 seed-0 learned arms (full_rd at sigma 0.1 / 0.2 / 0.4) to the v4 pools.
The v1 fits stored predictions, not models, so each model is re-fitted with its stored best config on the same id
train rows (deterministic, random_state = seed) and accepted only if it reproduces the stored v1 log-predictions on
every v1 row (max |diff| <= 1e-5, the stored rounding is 1e-6); then it predicts every v4 label row.
Writes results/v4/preds/<arm>.json.  usage (from papers/p2/code): python predict_v4.py [--check-only]"""
import hashlib
import json
import os
import sys

import numpy as np
from sklearn.ensemble import HistGradientBoostingRegressor

from certgrip.featsets import matrix
from certgrip.io import ROOT, key, load_rows

SIGMAS = (0.1, 0.2, 0.4)


def main():
    rows = load_rows("v1/labels/*.jsonl")
    tr = [r for r in rows if r["pool"] == "id" and r["shift"] is None and r["split"] == "train" and not r["unavoidable"]]
    y = np.log([r["F_hi"] for r in tr])
    new = None if "--check-only" in sys.argv else load_rows("v4/labels/*.jsonl")
    os.makedirs(os.path.join(ROOT, "v4/preds"), exist_ok=True)
    for s in SIGMAS:
        p = json.load(open(os.path.join(ROOT, "v1/preds", f"a010_full_rd_s{s}_seed0.json")))
        m = HistGradientBoostingRegressor(loss="quantile", quantile=1 - p["alpha"], random_state=p["seed"], **p["best"])
        m.fit(matrix(tr, "full_rd", False, s), y)
        diff = float(np.max(np.abs(m.predict(matrix(rows, "full_rd", False, s)) - np.asarray(p["log_pred"]))))
        print(f"sigma {s}: max |refit - stored| on {len(rows)} v1 rows = {diff:.2e}", flush=True)
        assert diff <= 1e-5, "refit does not reproduce the stored v1 predictions"
        if new is None:
            continue
        out = {"arm": f"full_rd@{s}#0", "source": f"v1/preds/a010_full_rd_s{s}_seed0.json (refit, check {diff:.2e})",
               "keys": [list(key(r)) for r in new],
               "keys_sha256": hashlib.sha256(json.dumps([list(key(r)) for r in new]).encode()).hexdigest(),
               "log_pred": [round(float(v), 6) for v in m.predict(matrix(new, "full_rd", False, s))]}
        json.dump(out, open(os.path.join(ROOT, "v4/preds", f"full_rd_s{s}_seed0.json"), "w"))


if __name__ == "__main__":
    main()
