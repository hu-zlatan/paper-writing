# Run 51 · paper 1 paper-level item: resolve the 3 [CITE-MISSING] markers (owner decision still pending)

- Why: OWNER_TODO run-50 default ("你不回复时") allows only paper-level text work; stage-20 gate listed the 3 markers.
- How: WebFetch is not available in this run and the sandbox shell cannot reach OpenAlex / Crossref, so dispatch the
  existing `literature-supplement` Actions workflow with three title queries (docs/03_supplement_queries.yaml).
  Records land in docs/03_supplement.jsonl with OpenAlex IDs / DOIs.
- Acceptance: a marker is replaced only when the returned record's title, first author and year match the intended work
  (Zaheer et al. 2017; Efron 1979; Holm 1979) and carries a DOI or OpenAlex ID. Otherwise the marker stays.
- No new experiments, no number changes, no LaTeX export.
