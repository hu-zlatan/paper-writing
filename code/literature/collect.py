"""Stage 4 LITERATURE_COLLECT: query OpenAlex, arXiv and Semantic Scholar for every query in
docs/02_search_plan.yaml and write normalized, deduplicated candidates to docs/03_candidates.jsonl.

Stdlib only (plus PyYAML for the plan). Network access is required, so this runs on GitHub Actions.
Usage: python code/literature/collect.py [--plan docs/02_search_plan.yaml] [--out docs/03_candidates.jsonl]
"""
import argparse
import datetime as dt
import json
import re
import time
import unicodedata
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET

import yaml

UA = "paper-writing-literature-bot/1.0 (https://github.com/hu-zlatan/paper-writing; mailto:mr.huguangjun@gmail.com)"
STOP = {"a", "an", "the", "on", "of", "for", "in", "to", "and", "with", "via", "from", "by", "at", "is", "are",
        "towards", "toward", "using", "learning"}
NOW = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def get(url, tries=4, accept="application/json"):
    last = None
    for k in range(tries):
        req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": accept})
        try:
            with urllib.request.urlopen(req, timeout=60) as r:
                return r.read().decode("utf-8")
        except urllib.error.HTTPError as e:
            last = f"HTTP {e.code}"
            if e.code in (429, 500, 502, 503, 504):
                time.sleep(3 * (2 ** k))
                continue
            break
        except Exception as e:  # network error: retry with backoff, then report
            last = repr(e)
            time.sleep(3 * (2 ** k))
    raise RuntimeError(f"{url} failed: {last}")


def ascii_fold(s):
    return unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode("ascii")


def norm_title(t):
    return re.sub(r"[^a-z0-9]+", " ", ascii_fold(t or "").lower()).strip()


def make_key(authors, year, title):
    last = "anon"
    if authors:
        parts = ascii_fold(authors[0]).replace(",", " ").split()
        if parts:
            last = re.sub(r"[^a-z]", "", parts[-1].lower()) or "anon"
    word = "paper"
    for w in norm_title(title).split():
        if w not in STOP and len(w) > 2:
            word = w
            break
    return f"{last}{year or 'nd'}{word}"


def openalex(q, limit, year_cutoff):
    flt = f"&filter=publication_year:>{year_cutoff - 1}" if year_cutoff else ""
    url = ("https://api.openalex.org/works?search=" + urllib.parse.quote(q) + f"&per_page={limit}" + flt +
           "&mailto=mr.huguangjun@gmail.com")
    data = json.loads(get(url))
    out = []
    for w in data.get("results", []):
        inv = w.get("abstract_inverted_index") or {}
        pos = {}
        for word, idxs in inv.items():
            for i in idxs:
                pos[i] = word
        abstract = " ".join(pos[i] for i in sorted(pos))
        doi = (w.get("doi") or "").replace("https://doi.org/", "") or None
        ids = w.get("ids") or {}
        arx = None
        for loc in (w.get("locations") or []):
            lu = (loc.get("landing_page_url") or "")
            m = re.search(r"arxiv\.org/abs/([0-9]{4}\.[0-9]{4,5})", lu)
            if m:
                arx = m.group(1)
        if doi and doi.lower().startswith("10.48550/arxiv."):
            arx = arx or doi.split("arxiv.", 1)[1]
        venue = ((w.get("primary_location") or {}).get("source") or {}).get("display_name")
        out.append({
            "id": "openalex:" + w["id"].rsplit("/", 1)[-1],
            "title": w.get("title") or w.get("display_name") or "",
            "source": "openalex",
            "url": w.get("doi") or w["id"],
            "year": w.get("publication_year"),
            "abstract": abstract,
            "authors": [a["author"]["display_name"] for a in (w.get("authorships") or []) if a.get("author")],
            "doi": doi,
            "arxiv_id": arx,
            "openalex_id": w["id"].rsplit("/", 1)[-1],
            "citation_count": w.get("cited_by_count"),
            "venue": venue,
            "type": w.get("type"),
        })
    return out


def arxiv(q, limit):
    url = ("https://export.arxiv.org/api/query?search_query=" + urllib.parse.quote(f'all:"{q}"' if len(q.split()) <= 3 else
           " AND ".join(f"all:{t}" for t in q.split())) + f"&max_results={limit}&sortBy=relevance")
    root = ET.fromstring(get(url, accept="application/atom+xml"))
    ns = {"a": "http://www.w3.org/2005/Atom", "x": "http://arxiv.org/schemas/atom"}
    out = []
    for e in root.findall("a:entry", ns):
        aid = e.find("a:id", ns).text.rsplit("/abs/", 1)[-1]
        aid_nov = re.sub(r"v\d+$", "", aid)
        doi_el = e.find("x:doi", ns)
        out.append({
            "id": "arxiv:" + aid_nov,
            "title": " ".join(e.find("a:title", ns).text.split()),
            "source": "arxiv",
            "url": "https://arxiv.org/abs/" + aid_nov,
            "year": int(e.find("a:published", ns).text[:4]),
            "abstract": " ".join(e.find("a:summary", ns).text.split()),
            "authors": [a.find("a:name", ns).text for a in e.findall("a:author", ns)],
            "doi": doi_el.text if doi_el is not None else None,
            "arxiv_id": aid_nov,
            "openalex_id": None,
            "citation_count": None,
            "venue": "arXiv",
            "type": "preprint",
        })
    time.sleep(3.5)  # arXiv API etiquette
    return out


def s2(q, limit):
    url = ("https://api.semanticscholar.org/graph/v1/paper/search?query=" + urllib.parse.quote(q) + f"&limit={limit}"
           "&fields=title,abstract,year,authors,externalIds,citationCount,venue,url")
    data = json.loads(get(url, tries=3))
    out = []
    for p in data.get("data", []) or []:
        ext = p.get("externalIds") or {}
        out.append({
            "id": "s2:" + p["paperId"],
            "title": p.get("title") or "",
            "source": "semanticscholar",
            "url": p.get("url") or f"https://www.semanticscholar.org/paper/{p['paperId']}",
            "year": p.get("year"),
            "abstract": p.get("abstract") or "",
            "authors": [a.get("name") for a in (p.get("authors") or [])],
            "doi": ext.get("DOI"),
            "arxiv_id": ext.get("ArXiv"),
            "openalex_id": None,
            "citation_count": p.get("citationCount"),
            "venue": p.get("venue"),
            "type": None,
        })
    time.sleep(1.5)
    return out


def merge(dst, src):
    for k, v in src.items():
        if k in ("queries", "sources"):
            continue
        if dst.get(k) in (None, "", []) and v not in (None, "", []):
            dst[k] = v
    dst["sources"] = sorted(set(dst["sources"]) | set(src["sources"]))
    dst["queries"] = sorted(set(dst["queries"]) | set(src["queries"]))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--plan", default="docs/02_search_plan.yaml")
    ap.add_argument("--out", default="docs/03_candidates.jsonl")
    ap.add_argument("--log", default="docs/03_collect_log.json")
    args = ap.parse_args()
    plan = yaml.safe_load(open(args.plan, encoding="utf-8"))
    limit = int(plan.get("per_query_limit", 25))
    cutoff = int(plan.get("year_cutoff", 2018))
    jobs = [(st["name"], q, cutoff) for st in plan["search_strategies"] for q in st["queries"]]
    jobs += [("seminal", q, None) for q in plan.get("seminal", {}).get("queries", [])]

    records, log = [], {"generated": NOW, "queries": []}
    for strat, q, yc in jobs:
        for name, fn in (("openalex", lambda: openalex(q, limit, yc)), ("arxiv", lambda: arxiv(q, limit)),
                         ("semanticscholar", lambda: s2(q, limit))):
            entry = {"strategy": strat, "query": q, "source": name}
            try:
                got = fn()
                entry["hits"] = len(got)
                for r in got:
                    r["queries"] = [q]
                    r["sources"] = [name]
                    r["strategy"] = strat
                records.extend(got)
            except Exception as e:  # logged per query; the run continues with the other sources
                entry["error"] = str(e)[:300]
            log["queries"].append(entry)
            print(json.dumps(entry), flush=True)

    # dedupe by DOI, arXiv id, normalized title
    merged, by_key = [], {}
    for r in records:
        keys = [k for k in (("doi:" + r["doi"].lower()) if r.get("doi") else None,
                            ("arxiv:" + r["arxiv_id"]) if r.get("arxiv_id") else None,
                            "title:" + norm_title(r["title"])) if k]
        hit = next((by_key[k] for k in keys if k in by_key), None)
        if hit is None:
            hit = dict(r)
            merged.append(hit)
        else:
            merge(hit, r)
        for k in keys:
            by_key[k] = hit
    merged = [m for m in merged if m["title"] and len(norm_title(m["title"])) > 5]

    used = {}
    for m in merged:
        base = make_key(m.get("authors"), m.get("year"), m["title"])
        n = used.get(base, 0)
        used[base] = n + 1
        m["cite_key"] = base if n == 0 else base + "abcdefghijklmnopqrstuvwxyz"[n - 1]
        m["collected_at"] = NOW
    with open(args.out, "w", encoding="utf-8") as f:
        for m in merged:
            f.write(json.dumps(m, ensure_ascii=False) + "\n")
    log["raw_records"] = len(records)
    log["unique_candidates"] = len(merged)
    json.dump(log, open(args.log, "w", encoding="utf-8"), indent=1)
    print(f"raw={len(records)} unique={len(merged)}")


if __name__ == "__main__":
    main()
