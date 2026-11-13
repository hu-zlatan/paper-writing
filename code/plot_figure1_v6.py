"""Render Figure 1 panels B-F of paper/mypaper/sections/draft_v6.md (accuracy-latency frontier, test5 episodes 0-499).

Every plotted value is read from the results JSONs under the keys named in the draft's FIGURE 1 PROMPT; nothing is typed
in. EXPECTED below is the prompt's copied data table and is only an assertion guard against the two drifting apart.
Panel A is a schematic (image-generator prompt in the draft) and is not drawn here.
Usage (repo root or code/): python code/plot_figure1_v6.py -> paper/mypaper/figures/figure1_v6_panelsBF.{pdf,png}
"""
import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.lines import Line2D  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "paper/mypaper/figures/figure1_v6_panelsBF"
BLUE, GREY, BLACK, PURPLE, DARK = "#1F6FB4", "#777777", "#222222", "#7A4FA3", "#555555"
CELLS = [("S2", "S2, κ = 2"), ("S4", "S4, κ = 4"), ("S8", "S8, κ = 8"), ("S12", "S12, κ = 12"),
         ("A16-2", "A16-2, κ = 2")]
METHODS = {"gstar": "gstar", "r500": "g500_512_4", "r125": "g125_512_16", "student": "student"}

# Prompt table: x = G*/R-500/R-125/student; y = G* r1, G* r2, R-500, R-125, student, seed min, seed max; H*, RL.
EXPECTED = {
    "S2": ((4.880, 0.194, 0.116, 0.000500), (0.518, 0.532, 0.462, 0.406, 0.4988, 0.464, 0.526), (0.432, 0.4132)),
    "S4": ((3.375, 0.141, 0.080, 0.000494), (0.496, 0.494, 0.390, 0.402, 0.4576, 0.432, 0.482), (0.368, 0.3964)),
    "S8": ((1.234, 0.061, 0.030, 0.000358), (0.432, 0.464, 0.372, 0.356, 0.4188, 0.408, 0.436), (0.344, 0.3932)),
    "S12": ((0.910, 0.048, 0.022, 0.000358), (0.434, 0.434, 0.390, 0.358, 0.4144, 0.398, 0.428), (0.358, 0.3576)),
    "A16-2": ((2.702, 0.098, 0.058, 0.000326), (0.474, 0.498, 0.374, 0.330, 0.4832, 0.464, 0.496), (0.312, 0.2144)),
}
EXPECTED_STARS = {"S2": {"r125"}, "S4": {"r125", "r500"}, "S8": {"r125"}, "S12": {"r125"}, "A16-2": {"r125", "r500"}}


def load(p):
    return json.loads((ROOT / p).read_text())


def read():
    A, D = load("results/v6/14_v6_analysis.json")["cells"], load("results/v6/15_derived_v6.json")["cells"]
    out = {}
    for cell, _ in CELLS:
        fr, w = A[cell]["frontier"], A[cell]["0-499"]
        seeds = [w["means"][f"student_s70{i}"]["success"] for i in range(1, 6)]
        out[cell] = dict(
            x={m: fr["latency_median_s"][k] for m, k in METHODS.items()},
            y={m: fr["success_0_499"][k] for m, k in METHODS.items()},
            g2=w["means"]["gstar2"]["success"],
            seed_rng=(min(seeds), max(seeds)),
            hstar=w["means"][w["v5_row_updates"]["H_star"]]["success"],
            rl=D[cell]["0-499"]["rl_mean"],
            stars={m for m in ("r125", "r500") if w["holm"][f"H6b_{METHODS[m]}"]},
        )
    return out


def check(d):
    for cell, (xs, ys, (hs, rl)) in EXPECTED.items():
        r = d[cell]
        for m, want in zip(METHODS, xs):  # prompt rounds latency to 3 decimals (6 for the student)
            got = r["x"][m]
            assert abs(got - want) <= (5e-7 if m == "student" else 5e-4), (cell, m, got, want)
        got_y = (r["y"]["gstar"], r["g2"], r["y"]["r500"], r["y"]["r125"], r["y"]["student"], *r["seed_rng"])
        assert all(abs(a - b) < 6e-5 for a, b in zip(got_y, ys)), (cell, got_y, ys)
        assert abs(r["hstar"] - hs) < 6e-5 and abs(r["rl"] - rl) < 6e-5, (cell, r["hstar"], r["rl"])
        assert r["stars"] == EXPECTED_STARS[cell], (cell, r["stars"])


def plot(d):
    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 8, "axes.edgecolor": "#999999",
                         "axes.labelcolor": BLACK, "xtick.color": DARK, "ytick.color": DARK})
    fig, axes = plt.subplots(1, 5, figsize=(11.0, 2.9), sharex=True, sharey=True)
    for i, (ax, (cell, title)) in enumerate(zip(axes, CELLS)):
        r = d[cell]
        x, y = r["x"], r["y"]
        ax.set_xscale("log")
        ax.set_xlim(1e-4, 1e1)
        ax.set_ylim(0.20, 0.56)
        ax.grid(True, which="major", color="#E6E6E6", lw=0.6)
        ax.set_axisbelow(True)
        ax.axhline(r["hstar"], color=DARK, ls="--", lw=1.0)
        ax.axhline(r["rl"], color=BLACK, ls="-.", lw=1.0)
        for m in ("r125", "r500"):  # arrow reduced planner -> student, star where Holm rejects on 0-499
            ax.annotate("", xy=(x["student"], y["student"]), xytext=(x[m], y[m]),
                        arrowprops=dict(arrowstyle="-|>", color="#AAAAAA", lw=0.8, shrinkA=5, shrinkB=6))
        stars = r["stars"]
        if stars:
            ax.text(x["student"] * 1.9, y["student"] + 0.012, "★" * len(stars), color=BLACK, fontsize=7,
                    ha="left", va="bottom")
        ax.plot([x["gstar"]] * 2, [y["gstar"], r["g2"]], color=BLACK, lw=1.0, zorder=3)
        # run 2 (hollow, larger) drawn first so run 1 (filled, smaller) stays visible when the two coincide
        ax.plot(x["gstar"], r["g2"], "o", mfc="white", mec=BLACK, ms=8, mew=1.2, zorder=4)
        ax.plot(x["gstar"], y["gstar"], "o", color=BLACK, ms=4.5, zorder=5)
        ax.plot(x["r500"], y["r500"], "s", color=GREY, ms=6, mec="white", mew=1.0, zorder=4)
        ax.plot(x["r125"], y["r125"], "^", color=GREY, ms=6.5, mec="white", mew=1.0, zorder=4)
        lo, hi = r["seed_rng"]
        ax.plot([x["student"]] * 2, [lo, hi], color=BLUE, lw=1.4, zorder=3)
        ax.plot(x["student"], y["student"], "D", color=BLUE, ms=6, mec="white", mew=1.0, zorder=4)
        ax.set_title(title, color=PURPLE if cell == "A16-2" else BLACK, fontsize=8.5)
        ax.text(0.03, 0.97, "BCDEF"[i], transform=ax.transAxes, fontweight="bold", va="top", fontsize=9)
        if i == 0:
            ax.set_ylabel("success (episodes 0-499)")
            ax.annotate("teacher run-to-run", xy=(x["gstar"], (y["gstar"] + r["g2"]) / 2),
                        xytext=(x["gstar"] / 5, 0.545), fontsize=6.5, color=DARK, ha="right", va="center",
                        arrowprops=dict(arrowstyle="-", color="#AAAAAA", lw=0.6))
        if i == 2:
            ax.set_xlabel("median latency per decision (s, log scale; phase-1 timings)")
        ax.set_xticks([1e-4, 1e-2, 1e0])
    handles = [
        Line2D([], [], marker="o", color=BLACK, ls="", ms=4.5, label="G* run 1"),
        Line2D([], [], marker="o", mfc="white", mec=BLACK, ls="", ms=8, label="G* run 2"),
        Line2D([], [], marker="s", color=GREY, ls="", ms=6, label="R-500"),
        Line2D([], [], marker="^", color=GREY, ls="", ms=6, label="R-125"),
        Line2D([], [], marker="D", color=BLUE, ls="-", ms=6, label="student (5-seed mean, seed range)"),
        Line2D([], [], color=DARK, ls="--", label="H* (latency not timed)"),
        Line2D([], [], color=BLACK, ls="-.", label="RL (latency not timed)"),
        Line2D([], [], marker="$★$", color=BLACK, ls="", ms=7, label="Holm-confirmed vs reduced planner"),
    ]
    fig.legend(handles=handles, loc="lower center", ncol=8, frameon=False, fontsize=6.8, bbox_to_anchor=(0.5, -0.01))
    fig.tight_layout(rect=(0, 0.08, 1, 1))
    fig.savefig(f"{OUT}.pdf")
    fig.savefig(f"{OUT}.png", dpi=200)


if __name__ == "__main__":
    data = read()
    check(data)
    plot(data)
    print("ok", OUT)
