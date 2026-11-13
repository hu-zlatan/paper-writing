# Run 52 plan — render Figure 1 panels B–F of draft_v6 from JSON (paper 1, paper-level only)

- **Why now:** both papers wait for the owner's stage-20 decision (OWNER_TODO run 50 / p2 run 48); the default is
  paper-level work only. The remaining paper-level gate item for paper 1 is "figures unrendered" — Figure 1 panels B–F
  are specified as data panels in the FIGURE 1 PROMPT of `paper/mypaper/sections/draft_v6.md` but were never plotted.
- **What:** `code/plot_figure1_v6.py` reads every plotted value from `results/v6/14_v6_analysis.json` (A) and
  `results/v6/15_derived_v6.json` (D) under exactly the keys listed in the prompt; the prompt's copied data table is
  used only as an assertion guard (fail if JSON and prompt drift apart; nothing typed in).
- **Output:** `paper/mypaper/figures/figure1_v6_panelsBF.{pdf,png}`. Panel A stays a schematic (image-generator prompt).
- **Not done:** no new experiment, no change to any number or table of the draft, no gate rerun, no LaTeX export.
- **Checks:** the script's asserts; visual inspection of the PNG; `tools_number_audit.py` unaffected (draft unchanged).
