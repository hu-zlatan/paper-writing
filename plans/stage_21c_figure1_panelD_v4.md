# Stage 21c (low-risk follow-up) — Figure 1 panel D inset [v4]

Owner's stage-20 decision is still pending, so only low-risk work runs (OWNER_TODO default). No new experiment, no
LaTeX export, no claim or number changes, no DONE mark.

**Goal.** Plot the data inset that `paper/mypaper/figures/figure1_prompt.txt` specifies. Needed under every owner option
that keeps this paper ((a), (b), (c)).

**Steps.** `code/plot_figure1_panelD.py` reads every value directly from `results/v3/14_m4_analysis.json`,
`results/v4/14_s2_analysis.json`, `results/v3/12_g2_analysis.json` (nothing typed by hand), asserts they equal the spec
to its printed precision, and writes `paper/mypaper/figures/figure1_panelD.{pdf,png}`. Whiskers: the paired diff ci95
added to G*'s success, so a whisker reaching the G* bar top means "not shown different from G*".

**Output.** See PROGRESS.md (run 13).
