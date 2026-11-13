"""Render Figure 2 (boundary map, fresh pool) of draft_v4 from results/v4/v4_analysis.json.

Every plotted value is read from the JSON (keys as named in the FIGURE 2 PROMPT of draft_v4.md); nothing is typed in.
Usage (from papers/p2/code): python make_figure2_v4.py  -> ../paper/mypaper/figures/figure2_v4.{pdf,png}
"""
import json, os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "..", "results", "v4", "v4_analysis.json")
OUT = os.path.join(HERE, "..", "paper", "mypaper", "figures", "figure2_v4")
BLUE, TEAL, ORANGE, GREY = "#1f3b8c", "#1a9a8f", "#e07b21", "#7a7a7a"

d = json.load(open(SRC))
f4 = d["f4"]; arms, rows = f4["arms"], f4["rows"]
sig = ["0.1", "0.2", "0.4"]
plug = [arms[f"CSF-muhat@{s}"]["RE_match"] for s in sig]
lrn = [arms[f"full_rd@{s}#0"]["RE_match"] for s in sig]
csf1 = arms["CSF-1"]["RE_match"]
def row(name_by_sigma):
    return [rows[name_by_sigma(s)]["point"] for s in sig]
d_c1 = row(lambda s: "C1" if s == "0.2" else f"S1_C1@{s}")
d_c2 = row(lambda s: "C2" if s == "0.2" else f"S1_C2@{s}")
d_c3 = row(lambda s: "C3" if s == "0.2" else f"S1_C3@{s}")

fig, ax = plt.subplots(1, 3, figsize=(13.5, 4.0))
fig.suptitle("Boundary map (fresh pool, simulation; secondary rows)", fontsize=11)
def tag(a, t):
    a.text(0.02, 0.98, t, transform=a.transAxes, va="top", fontsize=7.5,
           bbox=dict(boxstyle="round,pad=0.2", fc="white", ec="0.7"))

# (a) matched RE vs sigma
a = ax[0]; x = [0, 1, 2]
a.plot(x, plug, "o-", color=TEAL, label="probe plug-in")
a.plot(x, lrn, "o-", color=BLUE, label="learned probe model")
a.axhline(csf1, color=ORANGE, label="CSF-1 (no probe info)")
a.set_ylim(0, 1.05); a.set_ylabel("matched relative excess RE")
a.set_xticks(x, [f"σ {s}\nD plug-in vs CSF-1 {d_c1[i]:.3g}\nD learned vs plug-in {d_c2[i]:.3g}"
                 for i, s in enumerate(sig)], fontsize=7)
a2 = a.twinx(); a2.plot(x, d_c3, linestyle="none", marker="x", markersize=7, color=GREY,
                        label="CRC route, learned vs CSF-1 D")
a2.set_ylabel("D (CRC route)", color=GREY, fontsize=8); a2.set_ylim(-1.05, 1.05); a2.tick_params(colors=GREY)
h1, l1 = a.get_legend_handles_labels(); h2, l2 = a2.get_legend_handles_labels()
a.legend(h1 + h2, l1 + l2, fontsize=6.5, loc="upper left", bbox_to_anchor=(0.0, 0.9)); tag(a, "test-slip-matched route")
a.set_title("(a) onset noise", fontsize=9)

# (b) width sweep
b = ax[1]; ws = ["1.0", "0.75", "0.5", "0.25"]; sw = d["S3_width_sweep"]; xb = list(range(len(ws)))
pm = [sw[w]["rows"]["D_muhat_vs_CSF1"] for w in ws]
pf = [sw[w]["rows"]["D_full_vs_CSF1"]["point"] for w in ws]
pts = [r["point"] for r in pm]
err = [[p - r["CI**"][0] for p, r in zip(pts, pm)], [r["CI**"][1] - p for p, r in zip(pts, pm)]]
b.errorbar(xb, pts, yerr=err, fmt="o", color=TEAL, capsize=3, label="probe plug-in (97.5 % CI)")
b.plot(xb, pf, "s", color=BLUE, label="learned probe model")
b.axhline(0, color="k", lw=0.8)
labels = []
for w in ws:
    lo, hi = sw[w]["mu_window"]
    labels.append(f"w {w}\nμ [{lo:.4g}, {hi:.4g}]")
b.set_xticks(xb, labels, fontsize=7); b.set_ylim(-1.0, 0.6); b.set_ylabel("D vs CSF-1")
last = sw[ws[-1]]
b.text(0.5, -0.30, f"w {ws[-1]}: {last['n_cal_objects']} cal / {last['n_test_objects']} test objects",
       transform=b.transAxes, ha="center", fontsize=7)
b.legend(fontsize=6.5, loc="lower left"); tag(b, "test-slip-matched route, σ 0.2")
b.set_title("(b) friction-range width", fontsize=9)

# (c) force-time accounting (linear in T: shared phases + hold force x T, so straight segments are exact)
c = ax[2]; s6 = d["S6_noprobe"]["arms"]; T = ["1", "5", "30"]; Tf = [float(t) for t in T]
c.axvspan(0.6, 40, color="0.93", zorder=0)
c.text(0.98, 0.03, "holds beyond the 0.6 s disturbance window:\nslip not simulated", transform=c.transAxes,
       ha="right", fontsize=6.5, color="0.35")
c.plot(Tf, [s6["full_rd@0.2#0"]["noprobe_integrated_Ns"][t] for t in T], "o--", color=GREY, label="no-probe grasp")
for k, col, lab in [("full_rd@0.2#0", BLUE, "learned"), ("CSF-muhat@0.2", TEAL, "plug-in"),
                    ("CSF-1", ORANGE, "CSF-1 with probe")]:
    c.plot(Tf, [s6[k]["integrated_Ns"][t] for t in T], "o-", color=col, label=lab)
    be = s6[k]["break_even_T_s"]
    if be is not None:
        c.axvline(be, color=col, ls=":", lw=1); c.text(be, 120, f"{be:.4g} s",
                                                       color=col, fontsize=6.5, rotation=90, va="bottom")
c.set_xticks(Tf, T); c.set_xlim(0, 32)
c.set_xlabel("hold time T (s)"); c.set_ylabel("integrated grip force (N·s)")
c.legend(fontsize=6.5, loc="upper left", bbox_to_anchor=(0.0, 0.9))
tag(c, "CRC point, force-time accounting (not a slip measurement)")
c.set_title("(c) closed-form accounting, no interval", fontsize=9)

fig.tight_layout()
os.makedirs(os.path.dirname(OUT), exist_ok=True)
fig.savefig(OUT + ".pdf"); fig.savefig(OUT + ".png", dpi=200)
print("wrote", OUT + ".pdf/.png")
