"""Figure 1 panel D inset: test3 0-299 success (sub-8) and the H3 headroom bound.

All values are read from the results JSONs; nothing is typed by hand. The expected values below are the ones printed in
paper/mypaper/figures/figure1_prompt.txt and only guard against the two drifting apart.
"""
import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "paper/mypaper/figures"
GREY, BLUE, AQUA, YELLOW = "#555555", "#2a78d6", "#1baf7a", "#eda100"
INK, MUTED = "#222222", "#666666"


def load(p):
    return json.loads((ROOT / p).read_text())


def rows():
    """Return {regime: [(label, success, ci_lo, ci_hi), ...]}; ci is relative to G* (None for G*)."""
    m4 = load("results/v3/14_m4_analysis.json")
    s2 = load("results/v4/14_s2_analysis.json")["test3_sub8"]
    bf = m4["exploratory_b_fan"]
    flip = lambda ci: [-ci[1], -ci[0]]  # gstar-rl -> rl-gstar
    return {
        "S12": [
            ("G*", m4["rows"]["gstar"]["success"], None),
            ("student", m4["rows"]["student"]["success"], m4["diffs"]["student-gstar:success"]["ci95"]),
            ("RL", m4["rows"]["rl"]["success"], flip(m4["diffs"]["gstar-rl:success"]["ci95"])),
            ("B-fan", bf["success"], bf["b_fan-gstar:success"]["ci95"]),
        ],
        "S2": [
            ("G*", s2["rows"]["gstar"]["success"], None),
            ("student", s2["rows"]["student"]["success"], s2["diffs"]["student-gstar:success"]["ci95"]),
            ("RL", s2["rows"]["rl"]["success"], flip(s2["diffs"]["gstar-rl:success"]["ci95"])),
            ("B-fan", s2["rows"]["b_fan"]["success"], s2["diffs"]["b_fan-gstar:success"]["ci95"]),
        ],
    }


EXPECTED = {
    "S12": [(0.4267, None), (0.3822, (-0.0933, 0.0056)), (0.3567, (-0.1367, -0.0022)), (0.36, (-0.12, -0.01))],
    "S2": [(0.5533, None), (0.4511, (-0.1656, -0.0433)), (0.4233, (-0.1944, -0.0644)), (0.37, (-0.2467, -0.12))],
}


def check(data, ub):
    for regime, want in EXPECTED.items():
        for (_, s, ci), (ws, wci) in zip(data[regime], want):
            assert abs(s - ws) < 6e-5, (regime, s, ws)
            if wci:
                assert all(abs(a - b) < 6e-5 for a, b in zip(ci, wci)), (regime, ci, wci)
    assert abs(ub[12] - 0.0221) < 6e-5 and abs(ub[2] - 0.0197) < 6e-5, ub


def main():
    data = rows()
    g2 = load("results/v3/12_g2_analysis.json")
    ub = {12: g2["k12"]["ub95"], 2: g2["k2"]["ub95"]}
    check(data, ub)

    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 5.5, "axes.linewidth": 0.4, "hatch.linewidth": 0.5,
                         "pdf.fonttype": 42, "text.color": INK, "axes.labelcolor": INK, "xtick.color": INK,
                         "ytick.color": MUTED})
    fig = plt.figure(figsize=(4.5 / 2.54, 5.4 / 2.54))  # inset frame of the 17 cm wide Figure 1
    ax = fig.add_axes([0.20, 0.13, 0.50, 0.68])
    st = fig.add_axes([0.82, 0.13, 0.16, 0.68])
    colour = {"G*": GREY, "student": BLUE, "RL": AQUA, "B-fan": YELLOW}
    w = 0.19
    for gi, (regime, rs) in enumerate(data.items()):
        g_val = rs[0][1]
        for i, (lab, s, ci) in enumerate(rs):
            x = gi + (i - 1.5) * (w + 0.02)
            ax.bar(x, s, w, color=colour[lab] if lab != "B-fan" else "white", edgecolor=colour[lab], linewidth=0.5,
                   hatch="/////" if lab == "B-fan" else None, label=(lab + (" (exploratory)" if lab == "B-fan" else "")) if gi == 0 else None)
            if ci:
                ax.plot([x, x], [g_val + ci[0], g_val + ci[1]], color=INK, lw=0.7, solid_capstyle="butt")
    ax.set_xticks([0, 1], list(data))
    ax.set_xlim(-0.55, 1.55)
    ax.set_ylim(0, 0.65)
    ax.set_yticks([0, 0.2, 0.4, 0.6])
    ax.set_ylabel("test success")
    ax.tick_params(length=2, width=0.4)
    ax.grid(axis="y", color="#E6E6E6", lw=0.4)
    ax.set_axisbelow(True)
    ax.spines[["top", "right"]].set_visible(False)
    fig.legend(*ax.get_legend_handles_labels(), ncol=2, frameon=False, loc="upper left", bbox_to_anchor=(0.03, 1.0),
               fontsize=4.8, handlelength=1.1, handletextpad=0.4, columnspacing=0.8, borderpad=0)

    st.scatter([0, 1], [ub[12], ub[2]], s=9, color=GREY, zorder=3)
    st.axhline(0.03, color=INK, lw=0.6, ls=(0, (3, 2)))
    st.text(0.5, 0.0308, "Hold", ha="center", va="bottom", fontsize=4.8)
    st.set_xticks([0, 1], ["12", "2"])
    st.set_xlim(-0.6, 1.6)
    st.set_xlabel("κ")
    st.set_ylim(0, 0.04)
    st.set_yticks([0, 0.02, 0.04], ["0", ".02", ".04"])
    st.set_title("H3 UB", fontsize=5.5, pad=2)
    st.tick_params(length=2, width=0.4)
    st.spines[["top", "right"]].set_visible(False)

    OUT.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT / "figure1_panelD.pdf")
    fig.savefig(OUT / "figure1_panelD.png", dpi=400)


if __name__ == "__main__":
    main()
