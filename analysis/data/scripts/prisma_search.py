"""PRISMA 2020 identification stage: run the documented search string against
OpenAlex, Semantic Scholar, arXiv and DBLP, store every hit in records.csv and
log per-source counts in search_log.md.

Search string (title/abstract), years 2019-2026:
  (blockchain OR "distributed ledger" OR DeFi)
  AND ("cross-chain" OR crosschain OR "cross-blockchain" OR "inter-blockchain" OR "blockchain bridge"
       OR "token bridge" OR "bridge protocol" OR "blockchain interoperability" OR "interoperability protocol")
  AND (attack OR exploit OR vulnerability OR security OR anomaly OR hack)
"""
import csv, json, os, re, sys, time, urllib.parse, xml.etree.ElementTree as ET
from datetime import date
import requests

KB = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(KB, "prisma")
os.makedirs(OUT, exist_ok=True)
Y0, Y1 = 2019, 2026
S = requests.Session()
S.headers["User-Agent"] = "prisma-review-script/1.0 (academic literature review)"

CTX = ["blockchain", "distributed ledger", "defi"]
XC = ["cross-chain", "crosschain", "bridge", "interoperability", "inter-blockchain"]
SEC = ["attack", "exploit", "vulnerab", "security", "anomal", "hack"]


def get(url, params=None, tries=6, **kw):
    for i in range(tries):
        try:
            r = S.get(url, params=params, timeout=60, **kw)
            if r.status_code == 429 or r.status_code >= 500:
                time.sleep(3 * (i + 1)); continue
            r.raise_for_status(); return r
        except requests.RequestException as e:
            print("  retry", i, e, file=sys.stderr); time.sleep(3 * (i + 1))
    return None


def rec(src, title, year, venue, doi, arxiv, abstract, authors, url, cites=None):
    return dict(source=src, title=(title or "").strip(), year=year or "", venue=venue or "",
                doi=(doi or "").lower().replace("https://doi.org/", ""), arxiv=arxiv or "",
                abstract=(abstract or "").replace("\n", " ").strip(), authors=authors or "",
                url=url or "", citations=cites if cites is not None else "")


def openalex():
    out = []
    q = ('(blockchain OR "distributed ledger" OR DeFi) AND ("cross-chain" OR crosschain OR "cross-blockchain" '
         'OR "inter-blockchain" OR "blockchain bridge" OR "token bridge" OR "bridge protocol" '
         'OR "blockchain interoperability" OR "interoperability protocol") AND (attack OR exploit OR vulnerability OR '
         'security OR anomaly OR hack)')
    cursor = "*"
    while cursor:
        r = get("https://api.openalex.org/works", {
            "filter": f"title_and_abstract.search:{q},publication_year:{Y0}-{Y1}",
            "per-page": 200, "cursor": cursor,
            "select": "id,doi,title,publication_year,primary_location,abstract_inverted_index,authorships,cited_by_count,ids,type"})
        if r is None: break
        d = r.json()
        for w in d.get("results", []):
            ab = ""
            inv = w.get("abstract_inverted_index") or {}
            if inv:
                pos = sorted((p, t) for t, ps in inv.items() for p in ps)
                ab = " ".join(t for _, t in pos)
            loc = (w.get("primary_location") or {}).get("source") or {}
            au = "; ".join(a["author"]["display_name"] for a in (w.get("authorships") or [])[:8])
            out.append(rec("openalex", w.get("title"), w.get("publication_year"), loc.get("display_name"),
                           w.get("doi"), "", ab, au, w.get("id"), w.get("cited_by_count")))
        cursor = d.get("meta", {}).get("next_cursor")
        print(f"  openalex {len(out)}/{d.get('meta',{}).get('count')}")
        if not d.get("results"): break
    return out


def s2():
    out = []
    q = ('(blockchain | "distributed ledger" | DeFi) + ("cross-chain" | crosschain | "cross-blockchain" | '
         '"inter-blockchain" | "blockchain bridge" | "token bridge" | "bridge protocol" | '
         '"blockchain interoperability" | "interoperability protocol") + (attack | exploit | vulnerability | security | anomaly | hack)')
    token = None
    while True:
        p = {"query": q, "year": f"{Y0}-{Y1}",
             "fields": "title,year,venue,externalIds,abstract,authors,citationCount,url"}
        if token: p["token"] = token
        r = get("https://api.semanticscholar.org/graph/v1/paper/search/bulk", p)
        if r is None: break
        d = r.json()
        for w in d.get("data", []):
            ex = w.get("externalIds") or {}
            au = "; ".join(a.get("name", "") for a in (w.get("authors") or [])[:8])
            out.append(rec("semanticscholar", w.get("title"), w.get("year"), w.get("venue"), ex.get("DOI"),
                           ex.get("ArXiv"), w.get("abstract"), au, w.get("url"), w.get("citationCount")))
        print(f"  s2 {len(out)}/{d.get('total')}")
        token = d.get("token")
        if not token: break
        time.sleep(1.5)
    return out


def arxiv():
    out = []
    ctx = "(" + " OR ".join(f'abs:"{c}"' if " " in c else f"abs:{c}" for c in ["blockchain", "distributed ledger", "DeFi"]) + ")"
    xc = "(" + " OR ".join(f'abs:"{c}"' for c in ["cross-chain", "crosschain", "bridge", "interoperability", "inter-blockchain"]) + ")"
    sec = "(" + " OR ".join(f"abs:{c}" for c in ["attack", "exploit", "vulnerability", "security", "anomaly", "hack"]) + ")"
    q = f"{ctx} AND {xc} AND {sec}"
    ns = {"a": "http://www.w3.org/2005/Atom"}
    start = 0
    while True:
        r = get("http://export.arxiv.org/api/query", {"search_query": q, "start": start, "max_results": 200})
        if r is None: break
        root = ET.fromstring(r.content)
        total = int(root.find("{http://a9.com/-/spec/opensearch/1.1/}totalResults").text)
        ents = root.findall("a:entry", ns)
        for e in ents:
            yr = int(e.find("a:published", ns).text[:4])
            if not (Y0 <= yr <= Y1): continue
            aid = e.find("a:id", ns).text.rsplit("/abs/", 1)[-1]
            aid = re.sub(r"v\d+$", "", aid)
            doi_el = e.find("{http://arxiv.org/schemas/atom}doi")
            au = "; ".join(x.find("a:name", ns).text for x in e.findall("a:author", ns)[:8])
            out.append(rec("arxiv", " ".join(e.find("a:title", ns).text.split()), yr, "arXiv",
                           doi_el.text if doi_el is not None else "", aid,
                           " ".join(e.find("a:summary", ns).text.split()), au, f"https://arxiv.org/abs/{aid}"))
        start += len(ents)
        print(f"  arxiv {start}/{total}")
        if not ents or start >= total: break
        time.sleep(3.5)
    return out


def dblp():
    # DBLP indexes titles only; run the cross-product of short title queries.
    out, seen = [], set()
    for xc in ["cross-chain", "crosschain", "cross-blockchain", "inter-blockchain", "blockchain bridge", "token bridge", "bridge protocol", "blockchain interoperability"]:
        for sec in ["attack", "exploit", "vulnerab", "secur", "anomal", "hack"]:
            r = get("https://dblp.org/search/publ/api", {"q": f"{xc} {sec}", "format": "json", "h": 1000})
            if r is None: continue
            try:
                js = r.json()
            except ValueError:
                time.sleep(20); r = get("https://dblp.org/search/publ/api", {"q": f"{xc} {sec}", "format": "json", "h": 1000})
                try: js = r.json()
                except Exception: print("  dblp fail", xc, sec); continue
            hits = (js.get("result", {}).get("hits", {}) or {}).get("hit", []) or []
            for h in hits:
                i = h["info"]
                if h.get("@id") in seen: continue
                yr = int(i.get("year", 0) or 0)
                if not (Y0 <= yr <= Y1): continue
                seen.add(h.get("@id"))
                a = i.get("authors", {}).get("author", [])
                a = a if isinstance(a, list) else [a]
                au = "; ".join((x.get("text") if isinstance(x, dict) else str(x)) for x in a[:8])
                out.append(rec("dblp", re.sub(r"\.$", "", i.get("title", "")), yr, i.get("venue"),
                               i.get("doi"), "", "", au, i.get("ee") or i.get("url")))
            print(f"  dblp q='{xc} {sec}' total={len(out)}", flush=True)
            time.sleep(4)
    print(f"  dblp {len(out)}")
    return out


if __name__ == "__main__":
    srcs = sys.argv[1:] or ["openalex", "s2", "arxiv", "dblp"]
    fn = {"openalex": openalex, "s2": s2, "arxiv": arxiv, "dblp": dblp}
    for s in srcs:
        print("==", s)
        rows = fn[s]()
        with open(os.path.join(OUT, f"raw_{s}.csv"), "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=list(rec("", "", "", "", "", "", "", "", "").keys()))
            w.writeheader(); w.writerows(rows)
        with open(os.path.join(OUT, "search_log.md"), "a", encoding="utf-8") as f:
            f.write(f"- {date.today()} | {s} | {len(rows)} records | years {Y0}-{Y1}\n")
