"""Data extraction: code every included study by lifecycle stage and attack classes
(T1 attestation-key compromise, T2 verification flaw, T3 contract logic/access control,
T4 off-chain observation/relay, T5 protocol consistency/atomicity, T6 economic/user-level,
T7 privacy/linkability). Defaults by category, explicit overrides by study id."""
import csv, json, os
from collections import Counter, defaultdict
KB = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TAG2T = {"atk-key-validator-compromise": "T1", "atk-verification-flaw": "T2", "atk-contract-logic": "T3",
         "atk-offchain-relay": "T4", "atk-protocol-level": "T5", "atk-economic-user": "T6"}
DEF = {"C.1": ("D", "T1 T2"), "C.2": ("D", "T1 T4"), "C.3": ("D", "T5"), "C.4": ("D", "T7"),
       "D.1": ("P", "T3"), "D.2": ("P", "T2 T3"), "D.3": ("P", "T3"),
       "E.1": ("R", "T1 T2 T3"), "E.2": ("R", "T1 T2 T3"), "E.3": ("R", "T1 T4"),
       "F.1": ("X", "T1 T2 T3"), "F.2": ("R", "")}
OVR = {  # sid: (stage, classes)
    "S071": ("-", "T1 T2 T3"), "S084": ("-", "T4 T5"), "S109": ("-", "T2 T3"), "S117": ("-", "T6"),
    "S123": ("-", "T6"), "S072": ("-", "T6"), "S082": ("-", "T1 T2 T3 T6"), "S091": ("-", "T1 T2 T3"),
    "S101": ("-", "T1 T2 T3"), "S156": ("-", "T6"), "S130": ("-", "T6"),
    "S075": ("P", "T2 T3"), "S088": ("P", "T3"), "S137": ("P", "T2 T4"), "S095": ("P", "T3"), "S100": ("P", "T5"),
    "S027": ("R", "T2 T3"), "S059": ("R", "T1 T2 T3"), "S078": ("R", "T1 T2 T3 T5"), "S040": ("R", "T3"),
    "S021": ("R", "T5"), "S079": ("P", "T3 T5"), "S135": ("R", "T6"), "S118": ("R", "T6"), "S093": ("R", "T6"),
    "S080": ("R", "T6"), "S132": ("X", "T6"), "S157": ("X", "T6"), "S124": ("R", ""), "S062": ("R", "T2"),
    "S087": ("R", "T1 T2 T3"), "S108": ("-", "T2 T4"),
}
rows = list(csv.DictReader(open(os.path.join(KB, "included.csv"), encoding="utf-8")))
for r in rows:
    cat = r["category"]
    if r["sid"] in OVR: st, cl = OVR[r["sid"]]
    elif cat in DEF: st, cl = DEF[cat]
    elif cat.startswith("B"):
        st = "-"; cl = " ".join(sorted({TAG2T[t] for t in r["tags"].split(";") if t in TAG2T}))
    else: st, cl = "-", ""
    if "privacy" in r["title"].lower() and "T7" not in cl and cat.startswith("C"): cl += " T7"
    if "linkab" in r["title"].lower(): cl += " T7"
    r["stage"], r["classes"] = st, " ".join(sorted(set(cl.split())))
f = list(rows[0].keys())
with open(os.path.join(KB, "coded_studies.csv"), "w", newline="", encoding="utf-8") as h:
    w = csv.DictWriter(h, fieldnames=f); w.writeheader(); w.writerows(rows)
M = defaultdict(Counter)
for r in rows:
    for c in r["classes"].split(): M[r["stage"]][c] += 1
print("stage counts", Counter(r["stage"] for r in rows))
for st in ["-", "D", "P", "R", "X"]:
    print(st, {c: M[st][c] for c in ["T1", "T2", "T3", "T4", "T5", "T6", "T7"]})
json.dump({k: dict(v) for k, v in M.items()}, open(os.path.join(KB, "prisma/coverage_matrix.json"), "w"), indent=1)
