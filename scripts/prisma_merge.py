"""PRISMA: merge raw source CSVs, de-duplicate, and apply the automated
relevance screen.  Writes prisma/records_dedup.csv and prisma/screen_auto.csv
and appends counts to prisma/counts.json.

Automated screen (reported in PRISMA as "records marked ineligible by automation tools"):
  R1  title present and record is a research item (not erratum/retraction/editorial/front matter/thesis)
  R2  a cross-chain term occurs in the TITLE, or >=2 times in the abstract
  R3  a security term occurs in title or abstract
  R4  not a domain where "cross-chain" has a non-blockchain meaning (polymer chemistry etc.)
"""
import csv, json, os, re, glob

KB = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P = os.path.join(KB, "prisma")

XC = re.compile(r"cross[- ]?chain|crosschain|cross[- ]blockchain|inter[- ]blockchain|blockchain bridge|"
                r"token bridge|bridge protocol|bridges?\b|interoperab|atomic swap|htlc|hash[- ]?time[- ]?lock|"
                r"relay chain|sidechain|side[- ]chain|ibc\b|layerzero|wormhole|ccip", re.I)
XC_STRONG = re.compile(r"cross[- ]?chain|crosschain|cross[- ]blockchain|inter[- ]blockchain|bridge|interoperab|"
                       r"atomic swap|htlc|sidechain|side[- ]chain|relay chain|\bpegs?\b|pegged|multi-?chain", re.I)
SEC = re.compile(r"attack|exploit|vulnerab|secur|anomal|hack|threat|malicious|fraud|adversar|"
                 r"detect|audit|verif|trust|risk|incident|theft|steal|launder|authenticat|privacy|reputation|"
                 r"integrity|consisten|signature|safety|robust|resilien|censor|double[- ]spend|replay|collu", re.I)
NONPAPER = re.compile(r"^(erratum|corrigendum|retraction|editorial|front matter|back matter|preface|"
                      r"table of contents|index|author index|proceedings)\b", re.I)
OFFDOMAIN = re.compile(r"polymer|cross-linked|hydrogel|crosslink|protein|peptide|cellulose|elastomer", re.I)


def norm(t):
    return re.sub(r"[^a-z0-9]", "", (t or "").lower())


def load():
    rows = []
    for f in sorted(glob.glob(os.path.join(P, "raw_*.csv"))):
        rows += list(csv.DictReader(open(f, encoding="utf-8")))
    return rows


def dedup(rows):
    pri = {"semanticscholar": 0, "openalex": 1, "dblp": 2, "arxiv": 3, "citation": 4}
    by = {}
    for r in sorted(rows, key=lambda r: pri.get(r["source"], 9)):
        keys = [k for k in (("doi:" + r["doi"]) if r["doi"] else None,
                            ("arx:" + r["arxiv"]) if r["arxiv"] else None,
                            "t:" + norm(r["title"])[:90]) if k]
        hit = next((by[k] for k in keys if k in by), None)
        if hit is None:
            hit = dict(r); hit["sources"] = r["source"]
        else:
            hit["sources"] = ";".join(sorted(set(hit["sources"].split(";") + [r["source"]])))
            for f in ("abstract", "doi", "arxiv", "venue", "citations", "authors", "year"):
                if not hit.get(f) and r.get(f): hit[f] = r[f]
            if r["source"] != "arxiv" and r["venue"] and hit.get("venue") in ("arXiv", "", "ArXiv"):
                hit["venue"] = r["venue"]
        for k in keys: by[k] = hit
    uniq = {id(v): v for v in by.values()}
    return list(uniq.values())


def auto_screen(r):
    t, a = r["title"] or "", r["abstract"] or ""
    if not t or NONPAPER.search(t): return "R1"
    if not (XC_STRONG.search(t) or len(XC.findall(a)) >= 2): return "R2"
    if not (SEC.search(t) or SEC.search(a)): return "R3"
    if OFFDOMAIN.search(t + " " + a) and not re.search(r"blockchain|ledger|defi", t + a, re.I): return "R4"
    return ""


if __name__ == "__main__":
    rows = load()
    per = {}
    for r in rows: per[r["source"]] = per.get(r["source"], 0) + 1
    d = dedup(rows)
    for r in d: r["auto"] = auto_screen(r)
    fields = ["id", "sources", "title", "year", "venue", "doi", "arxiv", "citations", "authors", "url", "auto", "abstract"]
    d.sort(key=lambda r: (r["auto"] != "", str(r["year"]), r["title"]))
    for i, r in enumerate(d): r["id"] = f"R{i+1:04d}"
    with open(os.path.join(P, "records_dedup.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore"); w.writeheader(); w.writerows(d)
    kept = [r for r in d if not r["auto"]]
    with open(os.path.join(P, "screen_auto.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore"); w.writeheader(); w.writerows(kept)
    reasons = {}
    for r in d:
        if r["auto"]: reasons[r["auto"]] = reasons.get(r["auto"], 0) + 1
    c = dict(identified_per_source=per, identified_total=len(rows), duplicates_removed=len(rows) - len(d),
             after_dedup=len(d), auto_excluded=reasons, auto_excluded_total=sum(reasons.values()),
             to_title_abstract_screening=len(kept))
    json.dump(c, open(os.path.join(P, "counts_stage1.json"), "w"), indent=2)
    print(json.dumps(c, indent=2))
