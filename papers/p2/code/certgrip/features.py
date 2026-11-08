"""Compact tactile / proprioceptive records from one replay with record=True (stored per instance in label JSONL).

touch_grid layout (checked in the stage-10 pilot): per pad 3 channels x 8 x 8, channel-first; channel 0 = normal
(sums to the grip force), channels 1-2 = tangential. Per frame and pad we keep 7 statistics:
normal sum, tangential-1 sum, tangential-2 sum, normal-weighted centroid (row, col), normal-weighted spread
(row var + col var), active-cell count. Frames: the preload frame and all 10 probe frames.
The learning feature sets (P / S / full) are built from these records at training time (increment 3).
"""
from __future__ import annotations

import numpy as np

GRID = 8
PROBE_KEEP = tuple(range(10))   # probe frames: every 15 steps (0.03 s) over the 0.3 s squeeze -> 10 frames, all kept


def pad_stats(frame: np.ndarray) -> list:
    a = np.asarray(frame, dtype=float).reshape(2, 3, GRID, GRID)
    out = []
    rr, cc = np.meshgrid(np.arange(GRID), np.arange(GRID), indexing="ij")
    for p in range(2):
        n = np.clip(a[p, 0], 0, None)
        s = n.sum()
        if s > 1e-12:
            r, c = (n * rr).sum() / s, (n * cc).sum() / s
            spread = (n * ((rr - r) ** 2 + (cc - c) ** 2)).sum() / s
        else:
            r = c = spread = float("nan")
        out += [s, a[p, 1].sum(), a[p, 2].sum(), r, c, spread, int((n > 1e-9).sum())]
    return [float(round(x, 6)) if isinstance(x, float) or isinstance(x, np.floating) else int(x) for x in out]


def record(feats: dict) -> dict:
    probe = feats["touch_probe"]
    out = {
        "aperture": round(feats["aperture"], 7),
        "aperture_probe": round(feats["aperture_probe"], 7),
        "touch_preload": pad_stats(feats["touch_preload"]),
        "touch_probe": [pad_stats(probe[k]) for k in PROBE_KEEP if k < len(probe)],
        "probe_frames": [k for k in PROBE_KEEP if k < len(probe)],
    }
    if "onset" in feats:   # amendment 08a ramp-down probe (protocol "rd"); eps = the instance's onset-noise draw
        o = feats["onset"]
        out["onset"] = {"found": bool(o["found"]), "F_onset": round(float(o["F_onset"]), 7), "frames": int(o["frames"]),
                        "eps": round(float(o["eps"]), 7), "disp_at_onset_mm": round(float(o["disp_at_onset_mm"]), 5)}
    return out
