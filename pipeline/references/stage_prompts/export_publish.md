# Stage 22 — EXPORT_PUBLISH  (LaTeX)

## Purpose
Convert the markdown sections into LaTeX matching the conference template, build the PDF, and verify it fits the page limit.

## Mode
- LLM: strongest model (latex needs care with math + citations).
- json_mode: false.
- **max_tokens: 16384.**

## Prompt template

**System:**
```
You are a publication formatting editor.
```

**User:**
```
Format revised paper into clean final markdown for publication export.

Preserve content quality and readability.

Input paper:

{revised}
```

The original prompt asks for *markdown* output — that's a leftover from earlier in the pipeline. For an actual conference submission, you want LaTeX. Use this revised user prompt instead:

```
Convert the revised markdown paper into LaTeX matching the conference template.

REQUIREMENTS:
1. Use the conference's LaTeX class (loaded via `\documentclass{<conference_template>}`).
2. Each section becomes its own `paper/mypaper/sections/<name>.tex` file, included from `main.tex` via `\input{}`.
3. Inline math `$...$` stays as-is. Display math becomes `\begin{equation} ... \end{equation}` (numbered) or `\begin{align} ... \end{align}` (multi-line).
4. Tables use `\begin{table}[t] \centering \begin{tabular}{...} ... \end{tabular} \caption{...} \label{tab:...} \end{table}`.
5. Figures use `\begin{figure}[t] \centering \includegraphics[width=0.9\linewidth]{figures/<name>} \caption{...} \label{fig:...} \end{figure}`.
6. Every `\cite{cite_key}` must use the exact cite_keys from the bibliography. Do NOT invent new cite_keys.
7. Preserve every numerical value EXACTLY as it appears in the revised markdown — no rounding changes, no reformatting.

Conference template name: {conference_template}

Bibliography cite_keys available: {available_cite_keys}

Revised paper (markdown):

{revised}

Return one LaTeX block per section, formatted as ```latex:sections/<name>.tex ... ``` plus the main.tex skeleton.
```

## Placeholders

- `{conference_template}` — e.g. `neurips_2024`, `icml2024`, `iclr2024_conference`.
- `{available_cite_keys}` — list of cite_keys from the bibliography (extract from `paper/mypaper/references.bib`).
- `{revised}` — the revised markdown paper.

## Hard rules — page limit enforcement

After building the PDF (`pdflatex` × 2 + `bibtex` + `pdflatex` × 2), check:

1. **Page count of the body.** Conclusion's last line must end on or before the conference's main-page limit (NeurIPS=9, ICML=8 for camera-ready / 8 for submission, ICLR=10, etc.). References can spill onto extra pages. Appendix is unlimited but reviewers don't need to read it.
2. **If over the limit:** move non-critical content to the appendix (`sections/appendix.tex`, included after the bibliography). Candidates: detailed derivations, hyperparameter tables, additional ablations, qualitative examples.
3. **If under the limit by more than half a page:** consider whether you missed depth. Don't pad — but if Method or Experiments is short, that's a sign to flesh them out.

## Build commands

```bash
cd paper/mypaper/
pdflatex main.tex
bibtex main
pdflatex main.tex
pdflatex main.tex
```

## Output

- `paper/mypaper/sections/*.tex` — section files.
- `paper/mypaper/main.tex` — top-level (the template's main.tex with `\input{sections/...}` calls).
- `paper/mypaper/main.pdf` — built PDF.
