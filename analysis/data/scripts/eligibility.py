"""PRISMA eligibility stage. Indices refer to prisma/ta_included.json order
(the title/abstract-included records). Writes prisma/eligibility.csv,
included.csv (database + other methods) and prisma/counts_final.json.

Exclusion reasons
  EC1 duplicate / superseded version of an included report
  EC2 out of scope on reading: no security treatment of cross-chain communication
  EC3 outlet not peer reviewed (SSRN, Research Square, Zenodo, Figshare, theses) or on the
      excluded mega-journal list (MDPI, Hindawi, Heliyon, Scientific Reports, IEEE Access, PLoS ONE)
  EC4 evidence threshold for design-time proposals: not CORE A*/A or Q1 venue and <10 citations
  EC5 evidence threshold for preprints: <10 citations, no empirical/formal evaluation (pre-2025)
      or no identifiable outlet
"""
import csv, json, os

KB = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
recs = json.load(open(os.path.join(KB, "prisma/ta_included.json"), encoding="utf-8"))

INC = {
    # A surveys / SoKs
    5: "A.2|survey-interoperability;sok-bridge-security", 45: "A.1|sok-bridge-security", 47: "A.1|sok-bridge-security;incident-measurement",
    64: "A.2|survey-interoperability", 73: "A.1|sok-bridge-security", 98: "A.2|survey-interoperability",
    135: "A.1|sok-bridge-security", 170: "A.1|sok-bridge-security", 173: "A.1|sok-bridge-security",
    174: "A.1|sok-bridge-security", 272: "A.1|sok-bridge-security;incident-measurement",
    # B attacks / empirical
    2: "B.6|atk-economic-user", 19: "B.6|atk-economic-user", 14: "B.5|atk-protocol-level", 35: "B.4|atk-offchain-relay;atk-protocol-level",
    133: "B.6|atk-economic-user;incident-measurement", 147: "B.2|atk-verification-flaw;rt-graph-ml", 166: "B.7|incident-measurement;rt-graph-ml",
    167: "B.7|incident-measurement", 191: "B.7|incident-measurement", 198: "B.7|incident-measurement;atk-protocol-level",
    216: "B.7|incident-measurement", 239: "B.5|atk-protocol-level", 245: "B.7|incident-measurement",
    259: "B.2|atk-verification-flaw", 260: "B.7|incident-measurement", 273: "B.6|atk-economic-user",
    276: "B.7|incident-measurement", 287: "B.6|atk-economic-user", 288: "B.7|incident-measurement",
    307: "B.6|atk-economic-user;incident-measurement", 308: "B.6|atk-economic-user", 320: "B.6|atk-economic-user;atk-offchain-relay",
    331: "B.6|atk-economic-user", 345: "B.6|atk-economic-user;atk-offchain-relay", 346: "B.4|atk-offchain-relay;incident-measurement",
    348: "B.7|incident-measurement;atk-economic-user",
    # C design-time defenses
    1: "C.3|def-formal-protocol", 3: "C.1|def-lightclient-zk", 6: "C.3|def-formal-protocol", 7: "C.3|def-formal-protocol",
    8: "C.3|def-formal-protocol", 9: "C.3|def-formal-protocol", 15: "C.1|def-lightclient-zk", 17: "C.2|def-threshold-committee",
    22: "C.1|def-lightclient-zk;def-privacy-auth", 25: "C.2|def-threshold-committee", 26: "C.2|def-threshold-committee",
    29: "C.3|def-formal-protocol", 33: "C.3|def-formal-protocol", 36: "C.2|def-threshold-committee", 37: "C.3|def-formal-protocol",
    44: "C.2|def-threshold-committee", 46: "C.1|def-lightclient-zk", 52: "C.2|def-threshold-committee", 56: "C.4|def-privacy-auth",
    57: "C.1|def-lightclient-zk", 72: "C.4|def-privacy-auth", 76: "C.2|def-threshold-committee", 82: "C.3|def-formal-protocol",
    83: "C.4|def-privacy-auth", 90: "C.3|def-formal-protocol", 91: "C.3|def-formal-protocol", 92: "C.1|def-lightclient-zk",
    93: "C.1|def-lightclient-zk", 96: "C.3|def-formal-protocol", 97: "C.2|def-threshold-committee", 100: "C.3|def-formal-protocol",
    101: "C.4|def-privacy-auth", 116: "E.3|rt-trust-reputation;def-threshold-committee", 124: "C.4|def-privacy-auth",
    125: "C.3|def-formal-protocol", 127: "C.1|def-lightclient-zk", 128: "C.3|def-formal-protocol", 130: "C.3|def-formal-protocol",
    132: "C.4|def-privacy-auth", 136: "E.3|rt-trust-reputation;def-threshold-committee", 145: "C.2|def-threshold-committee",
    156: "C.3|def-formal-protocol", 158: "C.4|def-privacy-auth", 160: "C.4|def-privacy-auth", 161: "C.1|def-lightclient-zk",
    162: "C.1|def-lightclient-zk", 163: "C.4|def-privacy-auth", 164: "C.2|def-threshold-committee", 171: "C.1|def-lightclient-zk",
    187: "C.3|def-formal-protocol", 203: "C.2|def-threshold-committee", 217: "C.4|def-privacy-auth", 228: "C.4|def-privacy-auth",
    233: "C.3|def-formal-protocol", 237: "C.2|def-threshold-committee", 240: "C.3|def-formal-protocol", 247: "C.4|def-privacy-auth",
    250: "C.4|def-privacy-auth", 254: "C.1|def-lightclient-zk", 256: "C.4|def-privacy-auth", 258: "C.3|def-formal-protocol;def-privacy-auth",
    262: "C.4|def-privacy-auth;def-threshold-committee", 266: "C.2|def-threshold-committee", 267: "C.4|def-privacy-auth",
    271: "C.3|def-formal-protocol", 275: "C.2|def-threshold-committee", 279: "C.1|def-lightclient-zk", 286: "C.3|def-formal-protocol",
    295: "C.4|def-privacy-auth", 302: "C.4|def-privacy-auth", 304: "C.4|def-privacy-auth", 313: "C.4|def-privacy-auth",
    317: "C.2|def-threshold-committee", 323: "C.3|def-formal-protocol", 324: "C.2|def-threshold-committee", 327: "C.4|def-privacy-auth",
    330: "C.2|def-threshold-committee", 333: "C.1|def-lightclient-zk", 339: "C.4|def-privacy-auth", 340: "C.3|def-formal-protocol",
    342: "C.3|def-formal-protocol", 344: "C.4|def-privacy-auth", 352: "C.4|def-privacy-auth", 354: "C.3|def-formal-protocol",
    356: "C.3|def-formal-protocol;def-privacy-auth",
    # D pre-deployment
    110: "D.2|pre-fuzzing-testing", 138: "D.3|pre-ml-llm-audit", 172: "D.1|pre-static-symbolic", 209: "D.1|pre-static-symbolic",
    231: "D.1|pre-static-symbolic", 243: "D.1|def-formal-protocol;pre-static-symbolic", 314: "D.3|pre-ml-llm-audit",
    319: "D.2|pre-fuzzing-testing", 322: "D.2|pre-fuzzing-testing", 325: "D.2|pre-fuzzing-testing", 318: "D.1|pre-static-symbolic;atk-verification-flaw",
    # E runtime
    38: "E.1|rt-rule-invariant", 55: "E.1|rt-rule-invariant;incident-measurement", 95: "E.1|rt-rule-invariant", 139: "E.1|rt-rule-invariant",
    142: "E.2|rt-graph-ml", 157: "E.2|rt-graph-ml", 179: "E.1|rt-rule-invariant;data-benchmark", 181: "E.1|rt-rule-invariant",
    183: "E.2|rt-graph-ml", 205: "E.2|rt-graph-ml", 210: "E.2|rt-graph-ml", 214: "E.2|rt-graph-ml", 218: "E.2|rt-graph-ml;data-benchmark",
    248: "E.2|rt-graph-ml", 277: "E.2|rt-graph-ml;resp-mitigation", 285: "E.2|rt-graph-ml", 289: "F.2|data-benchmark",
    291: "E.1|rt-rule-invariant;resp-mitigation", 298: "E.2|rt-graph-ml", 311: "F.1|resp-mitigation", 316: "E.2|rt-graph-ml",
    351: "F.1|resp-mitigation", 137: "E.3|rt-trust-reputation", 194: "E.3|rt-trust-reputation", 337: "E.3|rt-trust-reputation",
    # F response
    204: "F.1|resp-mitigation", 328: "F.1|resp-mitigation",
}
EC1 = {11: 19, 12: 19, 16: 247, 21: 44, 53: 44, 54: 44, 94: 156, 99: 17, 107: 170, 159: 330, 175: 174, 180: 179, 211: 210}
EC2 = {18, 58, 106, 192, 196, 200, 207, 219, 225, 227, 230, 265, 268, 270, 299, 306, 310, 305, 343, 347, 300, 185}
EC3_OUTLETS = ("ssrn", "research square", "zenodo", "figshare", "mspace", "symmetry", "electronics", "ieee access", "heliyon",
               "scientific reports", "doaj", "int. j. distributed sens", "journal of big data and comput", "american journal of ai",
               "american scientific research", "darpan", "journal of physics, conference")

OTHER = [  # identified through citation searching (seed bibliographies + backward snowballing of included SoKs)
    dict(title="XCLAIM: Trustless, Interoperable, Cryptocurrency-Backed Assets", year=2019, venue="IEEE S&P", doi="10.1109/SP.2019.00085", tags="C.1|def-lightclient-zk", via="snowball:Zamyatin SoK"),
    dict(title="SoK: Decentralized Finance (DeFi) Attacks", year=2023, venue="IEEE S&P", doi="10.1109/SP46215.2023.10179435", tags="A.3|survey-defi-smart-contract", via="snowball:Augusto SoK"),
    dict(title="SoK: Decentralized Finance (DeFi)", year=2022, venue="ACM AFT", doi="10.1145/3558535.3559780", tags="A.3|survey-defi-smart-contract", via="seed:CD3 bib"),
    dict(title="A Survey on Blockchain Interoperability: Past, Present, and Future Trends", year=2021, venue="ACM Computing Surveys", doi="10.1145/3471140", tags="A.2|survey-interoperability", via="seed:CD1/CD3 bib"),
    dict(title="Exploring Blockchains Interoperability: A Systematic Survey", year=2023, venue="ACM Computing Surveys", doi="10.1145/3573897", tags="A.2|survey-interoperability", via="seed:CD1 bib"),
    dict(title="An overview on cross-chain: Mechanism, platforms, challenges and advances", year=2022, venue="Computer Networks", doi="10.1016/j.comnet.2022.109378", tags="A.2|survey-interoperability", via="seed:CD1 bib"),
    dict(title="CrossTrust-IoT: An adaptive reinforcement learning framework for cross-chain trust in resource-constrained IoT networks", year=2026, venue="IEEE Internet of Things Journal", doi="", tags="E.3|rt-trust-reputation", via="seed:CD3 bib"),
    dict(title="DAVE-CC: A decentralized, access-controlled, verifiable ecosystem for cross-chain academic credential management", year=2025, venue="Journal of Information Security and Applications", doi="", tags="C.4|def-privacy-auth", via="seed:CD1 publications"),
]

if __name__ == "__main__":
    elig, inc = [], []
    for i, r in enumerate(recs):
        v = (r["venue"] or "").lower()
        if i in INC:
            dec, why = "include", ""
            cat, tags = INC[i].split("|")
        elif i in EC1:
            dec, why, cat, tags = "exclude", f"EC1 (duplicate of {EC1[i]})", "", ""
        elif i in EC2:
            dec, why, cat, tags = "exclude", "EC2", "", ""
        elif any(o in v for o in EC3_OUTLETS):
            dec, why, cat, tags = "exclude", "EC3", "", ""
        elif r["tier"] == 3 or not v or "eprint" in v:
            dec, why, cat, tags = "exclude", "EC5", "", ""
        else:
            dec, why, cat, tags = "exclude", "EC4", "", ""
        row = dict(idx=i, title=r["title"], year=r["year"], venue=r["venue"], doi=r["doi"], arxiv=r["arxiv"],
                   citations=r["citations"], decision=dec, reason=why, category=cat, tags=tags, via="database")
        elig.append(row)
        if dec == "include": inc.append(row)
    for o in OTHER:
        cat, tags = o["tags"].split("|")
        inc.append(dict(idx="O", title=o["title"], year=o["year"], venue=o["venue"], doi=o["doi"], arxiv="", citations="",
                        decision="include", reason="", category=cat, tags=tags, via=o["via"]))
    for k, r in enumerate(inc): r["sid"] = f"S{k+1:03d}"
    f = ["sid", "idx", "title", "year", "venue", "doi", "arxiv", "citations", "decision", "reason", "category", "tags", "via"]
    with open(os.path.join(KB, "prisma/eligibility.csv"), "w", newline="", encoding="utf-8") as h:
        w = csv.DictWriter(h, fieldnames=f, extrasaction="ignore"); w.writeheader(); w.writerows(elig)
    with open(os.path.join(KB, "included.csv"), "w", newline="", encoding="utf-8") as h:
        w = csv.DictWriter(h, fieldnames=f, extrasaction="ignore"); w.writeheader(); w.writerows(inc)
    from collections import Counter
    s1 = json.load(open(os.path.join(KB, "prisma/counts_stage1.json")))
    ta_total = s1["to_title_abstract_screening"]
    c = dict(stage1=s1, ta_screened=ta_total, ta_excluded=ta_total - len(recs), reports_assessed=len(recs),
             excluded_by_reason=dict(Counter(r["reason"].split(" ")[0] for r in elig if r["decision"] == "exclude")),
             included_from_databases=sum(1 for r in elig if r["decision"] == "include"),
             included_other_methods=len(OTHER), included_total=len(inc),
             by_category=dict(Counter(r["category"][0] for r in inc)),
             by_year=dict(sorted(Counter(str(r["year"]) for r in inc).items())))
    json.dump(c, open(os.path.join(KB, "prisma/counts_final.json"), "w"), indent=2)
    print(json.dumps(c, indent=2))
