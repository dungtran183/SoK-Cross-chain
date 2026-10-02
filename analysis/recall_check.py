"""Known-item recall of the database search (before citation searching).

Benchmark A (independent): peer-reviewed cross-chain security works published 2019-2026 that are
cited by the Zhang et al. SoK (RAID 2024; reference list of arXiv:2312.12573), plus CONNECTOR
(IEEE TIFS 2025), a peer-reviewed tool found during reviewer verification.
Benchmark B (dependent, upper bound): peer-reviewed 2019-2026 cross-chain works in the authors'
reference library refs.bib. B was assembled partly from the search, so its recall is optimistic.
A work counts as retrieved if a record with the same normalized title prefix is among the
1,392 de-duplicated records (prisma/records_dedup.csv).
"""
import csv, json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
csv.field_size_limit(10**9)
norm = lambda t: re.sub(r"[^a-z0-9]", "", t.lower())
recs = list(csv.DictReader(open(os.path.join(HERE, "data/prisma/records_dedup.csv"), encoding="utf-8")))
keys = {norm(r["title"])[:60] for r in recs}

A = [
    "Xscope: Hunting for Cross-Chain Bridge Attacks",
    "Universal Atomic Swaps: Secure Exchange of Coins Across All Blockchains",
    "A Survey on Blockchain Interoperability: Past, Present, and Future Trends",
    "SoK: Communication Across Distributed Ledgers",
    "Cross-chain Transactions",
    "A Privacy Protection Scheme for Cross-Chain Transactions Based on Group Signature and Relay Chain",
    "Proof-of-Work Sidechains",
    "Proof-of-Stake Sidechains",
    "SoK: Not Quite Water Under the Bridge: Review of Cross-Chain Bridge Hacks",
    "Cross-chain exchange by transaction dependence with conditional transaction method",
    "CONNECTOR: Enhancing the Traceability of Decentralized Bridge Applications via Automatic Cross-chain Transaction Association",
]
sys.path.insert(0, "/Users/zungtran/.claude/skills/review_paper/scripts")
from audit_citations import parse_bib
bib = parse_bib(open(os.path.join(HERE, "..", "refs.bib"), encoding="utf-8").read())
NOT_CROSS_CHAIN = {"page2021prisma", "zhou2023sok", "tran2026fedvuln", "tran2026chronosrep", "wu2026tracing", "bentov2019tesseract"}
B = []
for k, e in bib.items():
    peer = e.get("doi") and e["__type__"] in ("article", "inproceedings")
    yr = int(e.get("year", "0") or 0)
    if peer and 2019 <= yr <= 2026 and k not in NOT_CROSS_CHAIN:
        B.append((k, re.sub(r"[{}]", "", e["title"])))


def check(titles):
    hits = [(t, norm(t)[:60] in keys or any(norm(t)[:40] == k[:40] for k in keys)) for t in titles]
    return sum(h for _, h in hits), len(hits), [t for t, h in hits if not h]


a_hit, a_n, a_miss = check(A)
b_hit, b_n, b_miss = check([t for _, t in B])
out = dict(A_retrieved=a_hit, A_size=a_n, A_missed=a_miss, B_retrieved=b_hit, B_size=b_n, B_missed=b_miss)
json.dump(out, open(os.path.join(HERE, "recall_check.json"), "w"), indent=1)
print(json.dumps(out, indent=1))
