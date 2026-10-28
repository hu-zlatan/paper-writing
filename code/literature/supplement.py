"""Targeted OpenAlex title lookups (stdlib only + PyYAML). Appends new records to docs/03_supplement.jsonl with cite_keys
that never collide with docs/03_candidates.jsonl. Runs on GitHub Actions (the sandbox shell cannot reach OpenAlex)."""
import json
import os
import sys
import urllib.parse

import yaml

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from collect import NOW, get, make_key, norm_title  # noqa: E402

plan = yaml.safe_load(open("docs/03_supplement_queries.yaml"))
existing = {json.loads(l)["cite_key"] for l in open("docs/03_candidates.jsonl")}
seen_titles = {norm_title(json.loads(l)["title"]) for l in open("docs/03_candidates.jsonl")}
out_path = "docs/03_supplement.jsonl"
if os.path.exists(out_path):
    for l in open(out_path):
        r = json.loads(l)
        existing.add(r["cite_key"])
        seen_titles.add(norm_title(r["title"]))
new = []
for item in plan["queries"]:
    url = ("https://api.openalex.org/works?search=" + urllib.parse.quote(item["q"]) + "&per_page=5"
           + f"&filter=publication_year:>{item['year_min'] - 1}&mailto=mr.huguangjun@gmail.com")
    try:
        data = json.loads(get(url))
    except Exception as e:  # logged; continue with the next query
        print("ERROR", item["q"], e)
        continue
    for w in data.get("results", [])[:3]:
        title = w.get("title") or ""
        if not title or norm_title(title) in seen_titles:
            continue
        inv = w.get("abstract_inverted_index") or {}
        pos = {i: word for word, idxs in inv.items() for i in idxs}
        authors = [a["author"]["display_name"] for a in (w.get("authorships") or []) if a.get("author")]
        key = make_key(authors, w.get("publication_year"), title)
        base, n = key, 0
        while key in existing:
            n += 1
            key = base + "abcdefghijklmnopqrstuvwxyz"[n - 1]
        existing.add(key)
        seen_titles.add(norm_title(title))
        new.append({"id": "openalex:" + w["id"].rsplit("/", 1)[-1], "title": title, "source": "openalex",
                    "url": w.get("doi") or w["id"], "year": w.get("publication_year"),
                    "abstract": " ".join(pos[i] for i in sorted(pos)), "authors": authors,
                    "doi": (w.get("doi") or "").replace("https://doi.org/", "") or None,
                    "openalex_id": w["id"].rsplit("/", 1)[-1], "citation_count": w.get("cited_by_count"),
                    "venue": ((w.get("primary_location") or {}).get("source") or {}).get("display_name"),
                    "cite_key": key, "query": item["q"], "collected_at": NOW})
        print("ADD", key, title)
with open(out_path, "a", encoding="utf-8") as f:
    for r in new:
        f.write(json.dumps(r, ensure_ascii=False) + "\n")
print("added", len(new))
