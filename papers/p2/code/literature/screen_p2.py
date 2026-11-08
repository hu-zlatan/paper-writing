"""p2 stage 5 LITERATURE_SCREEN helpers (adapted from paper 1's code/literature/screen.py; same filter and merge rules,
paper-2 paths and keyword terms).

prefilter: year/ID/abstract filter + transparent keyword score used only to ORDER candidates for reading.
merge:     join docs/04_screen_decisions.json (written by the screening reviewer) with the original candidate records,
           preserving every original field verbatim -> docs/04_shortlist.jsonl.
usage (from papers/p2): python code/literature/screen_p2.py prefilter|merge
"""
import json
import re
import sys

CAND = "docs/03_candidates.jsonl"
TERMS = {  # weight, regex
    "conformal|distribution-free|coverage guarantee|risk control": 3, "slip": 3,
    "grip force|grasp force|grasping force|normal force|force regulation": 3,
    "tactile|touch|haptic|visuotactile": 2, "grasp": 1, "friction": 1,
    "guarantee|certif|safety|risk|chance constrain": 1, "uncertainty|calibrat|quantile": 1,
    "distribution shift|online|adaptive": 1, "robot|manipulat": 1,
}


def load():
    return [json.loads(line) for line in open(CAND, encoding="utf-8")]


def score(r):
    txt = (r["title"] + " " + (r.get("abstract") or "")).lower()
    return sum(w for pat, w in TERMS.items() if re.search(pat, txt)) + sum(
        2 * w for pat, w in TERMS.items() if re.search(pat, r["title"].lower()))


def prefilter():
    recs = load()
    keep = []
    for r in recs:
        has_id = r.get("doi") or r.get("arxiv_id") or r.get("openalex_id")
        old_ok = (r.get("year") or 0) >= 2018 or r.get("strategy") == "seminal"
        if has_id and old_ok and (r.get("abstract") or r.get("strategy") == "seminal"):
            r["_kw"] = score(r)
            keep.append(r)
    keep.sort(key=lambda r: -r["_kw"])
    with open("docs/04_prefiltered.tsv", "w", encoding="utf-8") as f:
        f.write("kw\tcite_key\tyear\tcitations\tvenue\ttitle\n")
        for r in keep:
            f.write(f"{r['_kw']}\t{r['cite_key']}\t{r.get('year')}\t{r.get('citation_count')}\t{(r.get('venue') or '')[:40]}\t{r['title']}\n")
    print(len(recs), "candidates ->", len(keep), "after year/ID/abstract filter")


def merge():
    recs = {r["cite_key"]: r for r in load()}
    dec = json.load(open("docs/04_screen_decisions.json", encoding="utf-8"))
    out = []
    for d in dec["shortlist"]:
        r = recs[d["cite_key"]]  # KeyError = a hallucinated cite_key -> fail loudly
        assert d["title"] == r["title"], d["cite_key"]
        row = dict(r)
        row.update({k: d[k] for k in ("relevance_score", "quality_score", "keep_reason")})
        row["paper_id"] = r["id"]
        out.append(row)
    with open("docs/04_shortlist.jsonl", "w", encoding="utf-8") as f:
        for row in out:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")
    print(len(out), "shortlisted")


if __name__ == "__main__":
    {"prefilter": prefilter, "merge": merge}[sys.argv[1]]()
