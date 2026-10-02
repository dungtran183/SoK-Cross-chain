import shutil
p = r"C:\Users\dungt\Downloads\PhD\ACIIDS2027-SoK\main.tex"
shutil.copy(p, p.replace("main.tex", "paper_before_improve.tex"))
s = open(p, encoding="utf-8").read()
R = [
 # M2 count consistency
 ("The 168 included studies comprise 16 surveys, 26 attack or measurement studies, 85 design-time proposals, 11 pre-deployment analysers, 25 runtime monitors or detectors and 5 response or data studies.",
  "Coded by lifecycle stage, the 168 included studies comprise 16 surveys, 25 attack or measurement studies, 85 design-time proposals, 12 pre-deployment analysers, 26 runtime monitors, detectors or datasets, and 4 response studies."),
 # M3 overreach
 ("First, every one of these incidents violated P1 or P3, the two end-to-end properties, so a runtime check of source-event existence and value conservation would have flagged all of them; Liu et al.\\ confirm this retrospectively on 10 million transactions~\\cite{liu2024monte}.",
  "First, every one of these incidents is observable as a violation of P1 or P3, the two end-to-end properties. For the 2021 to 2023 subset, Liu et al.\\ confirm on 10 million transactions that a conservation invariant identifies every known attack~\\cite{liu2024monte}; turning such detection into prevention additionally requires a response mechanism (Section~\\ref{sec:defenses})."),
 # M4 stage coding
 ("BNB token hub & 2022-10 & 586 & forged IAVL Merkle proof accepted & T2 & D \\\\",
  "BNB token hub & 2022-10 & 586 & forged IAVL Merkle proof accepted & T2 & P \\\\"),
 ("Loss in million USD (nominal); stage = earliest stage that could have stopped the attack.}",
  "Loss in million USD (nominal). Stage is the earliest stage that could have stopped the attack: D if the root cause is a trust-model or key-custody choice, P if it is a defect in bridge or verifier code. Per-incident sources are listed in the supplement.}"),
 # minors
 ("venues on a pre-registered list of mega-journals", "venues on a predefined list of mega-journals"),
 ("DBLP-indexed venues are covered through OpenAlex and Semantic Scholar.", "DBLP-indexed venues are largely indexed by OpenAlex and Semantic Scholar."),
 ("and none covers the 2024 to 2026 work on", "and none systematically covers the 2024 to 2026 work on"),
 ("Zhang et al.~\\cite{zhang2024security} & SoK & $\\le$2023 & \\yes & \\no & \\partly & \\partly \\\\",
  "Zhang et al.~\\cite{zhang2024security} & SoK & $\\le$2023 & \\yes & \\no & \\partly & \\no \\\\"),
 ("Automated pre-screening may exclude relevant records whose abstracts use unusual vocabulary.",
  "Automated pre-screening may exclude relevant records whose abstracts use unusual vocabulary, and the query omits terms such as sidechain, relay, HTLC and light client, so such studies entered only when they also used a cross-chain term."),
 ("III & 78 incidents, 12 anomaly classes, temporal split (in preparation) &", "III & 78 incidents, 12 anomaly classes, temporal split (preliminary, unpublished) &"),
 ("III & Agent simulation, 1,000 agents, sleeper relayers &", "III & Agent simulation, 1,000 agents, sleeper relayers (preliminary) &"),
]
for a, b in R:
    assert a in s, a[:70]
    s = s.replace(a, b)
open(p, 'w', encoding='utf-8').write(s)
print("ok")
