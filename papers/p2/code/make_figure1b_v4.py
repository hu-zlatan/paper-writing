"""Render Figure 1(b) (confirmatory forest plot) of draft_v4 from results/v4/v4_analysis.json.

Every plotted value is read from the JSON; nothing is typed in. EXPECTED is the FIGURE 1 PROMPT's copied numbers and
only guards against the two drifting apart. Panel (a) is a schematic timeline (image-generator prompt) and is not drawn.
Keys: C1-C3 f4/rows/C{1,2,3}; C4-C5 c4/rows/C{4,5}; CRC ticks f4/rows/S5_C{1,2}_crc, c4/rows/S5_C{4,5}_crc.
Usage (from papers/p2/code): python make_figure1b_v4.py -> ../paper/mypaper/figures/figure1b_v4.{pdf,png}
"""
import json
import os

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "..", "results", "v4", "v4_analysis.json")
OUT = os.path.join(HERE, "..", "paper", "mypaper", "figures", "figure1b_v4")
INK, MUTED = "#222222", "#777777"

EXPECTED = {  # point, lo, hi, crc tick (None for C3)
    "C1": (0.4314, 0.3824, 0.4835, 0.4482),
    "C2": (0.01117, -0.05552, 0.05686, -0.06291),
    "C3": (0.4135, 0.3578, 0.4903, None),
    "C4": (-0.5814, -0.7208, -0.4563, -0.5166),
    "C5": (-0.5461, -0.6590, -0.4290, -0.4733),
}
LABELS = {
    "C1": "C1  probe plug-in vs CSF-1",
    "C2": "C2  learned model vs plug-in",
    "C3": "C3  learned model vs CSF-1",
    "C4": "C4  plug-in vs CSF-fam",
    "C5": "C5  learned model vs CSF-fam",
}


def read():
    d = json.load(open(SRC))
    f4, c4 = d["f4"]["rows"], d["c4"]["rows"]
    rows = {k: f4[k] for k in ("C1", "C2", "C3")} | {k: c4[k] for k in ("C4", "C5")}
    crc = {"C1": f4["S5_C1_crc"], "C2": f4["S5_C2_crc"], "C4": c4["S5_C4_crc"], "C5": c4["S5_C5_crc"]}
    out = {}
    for k, r in rows.items():
        out[k] = (r["point"], r["CI**"][0], r["CI**"][1], crc[k]["point"] if k in crc else None)
    assert rows["C3"]["kind"] == "crc" and all(rows[k]["kind"] == "match" for k in ("C1", "C2", "C4", "C5"))
    return out


def check(data):
    for k, want in EXPECTED.items():
        for got, w in zip(data[k], want):
            if w is None:
                assert got is None, k
            else:  # prompt rounds to 4 significant figures
                assert abs(got - w) <= 5e-5 * max(1.0, abs(w) * 10), (k, got, w)


def plot(data):
    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 8})
    fig, ax = plt.subplots(figsize=(6.4, 3.2))
    ypos = {"C1": 6, "C2": 5, "C3": 4, "C4": 1.5, "C5": 0.5}
    ax.fill_between([-0.10, 0.10], ypos["C2"] - 0.35, ypos["C2"] + 0.35, color="#DDDDDD", lw=0)
    ax.axvline(0, color=INK, lw=0.9)
    for xv in (-0.10, 0.10):
        ax.axvline(xv, color=MUTED, lw=0.8, ls="--")
    for k, (pt, lo, hi, crc) in data.items():
        y = ypos[k]
        filled = k in ("C1", "C2", "C3")  # registered prediction met (C1-C3); none registered for C4/C5
        ax.plot([lo, hi], [y, y], color=INK, lw=1.4, solid_capstyle="butt")
        ax.plot(pt, y, "o", ms=6.5, mfc=INK if filled else "white", mec=INK, mew=1.3, zorder=4)
        if crc is not None:
            ax.plot(crc, y, "|", ms=9, mew=1.4, color=MUTED, zorder=3)
        ax.text(1.02, y, f"{pt:.3g} [{lo:.3g}, {hi:.3g}]", va="center", fontsize=6.8, color=INK,
                transform=ax.get_yaxis_transform(), clip_on=False)
    ax.set_yticks([ypos[k] for k in LABELS], list(LABELS.values()))
    for yh, txt in ((6.75, "fresh pool (friction independent of appearance)"),
                    (2.25, "friction-correlated pool, vs family prior")):
        ax.text(-0.02, yh, txt, fontsize=7.2, fontweight="bold", va="bottom", ha="right", color=INK,
                transform=ax.get_yaxis_transform(), clip_on=False)
    ax.set_xlim(-0.8, 0.6)
    ax.set_ylim(-0.2, 7.3)
    ax.set_xlabel("D = 1 − RE(a) / RE(b)")
    for s in ("top", "right", "left"):
        ax.spines[s].set_visible(False)
    ax.tick_params(axis="y", length=0)
    ax.set_title("(b) Confirmatory contrasts", loc="left", fontsize=8.5)
    handles = [
        plt.Line2D([], [], marker="o", color=INK, ls="", label="registered prediction met"),
        plt.Line2D([], [], marker="o", mfc="white", mec=INK, ls="", label="no prediction registered"),
        plt.Line2D([], [], marker="|", color=MUTED, ls="", ms=9, mew=1.4, label="CRC-route value"),
    ]
    fig.legend(handles=handles, loc="lower center", ncol=3, frameon=False, fontsize=6.8)
    fig.tight_layout(rect=(0, 0.07, 1, 1))
    fig.savefig(OUT + ".pdf")
    fig.savefig(OUT + ".png", dpi=200)


if __name__ == "__main__":
    d = read()
    check(d)
    plot(d)
    print("ok", OUT)
