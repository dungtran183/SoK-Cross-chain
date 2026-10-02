import re
p = r"C:\Users\dungt\Downloads\PhD\ACIIDS2027-SoK\main.tex"
s = open(p, encoding="utf-8").read()
drop = ['tsai2023ibc', 'mercury2026', 'tran2024chainsniper', 'gazi2019pos']


def fix(m):
    keys = [k.strip() for k in m.group(1).split(',') if k.strip() not in drop]
    return '\\cite{' + ','.join(keys) + '}'


s = re.sub(r'\\cite\{([^}]*)\}', fix, s)
R = [
 ("committee hardening uses threshold cryptography, economic security or trusted execution~\\cite{xiong2022trustboost};",
  "committee hardening uses threshold cryptography or economic security~\\cite{xiong2022trustboost};"),
 ("Learning-based auditors learn cross-chain vulnerability patterns from few labelled contracts~\\cite{tran2026crossguard}.",
  "Learning-based auditors learn cross-chain vulnerability patterns from few labelled contracts~\\cite{tran2026crossguard}."),
 ("How should a deployed bridge be monitored when evidence is incomplete and intermediaries change behavior? CrossSentry (in preparation) compiles Part II invariants into online rules for pairing, conservation, nonce reuse, quorum and privileged calls; it fuses rule and graph-model evidence with an explicit evidence-sufficiency score that permits abstention (ECA); it tracks per-actor, per-corridor risk with a jump-diffusion trust process (CRS), building on ChronosRep~\\cite{tran2026chronosrep} and CrossTrust-IoT~\\cite{tran2026crosstrust}; and it bounds the concentration of response actions on a few entities with a Gini-based constraint (G-surv).",
  "How should a deployed bridge be monitored when evidence is incomplete and intermediaries change behavior? CrossSentry (in preparation) compiles Part II invariants into online rules for pairing, conservation, nonce reuse, quorum and privileged calls; scores whether the fused rule and graph evidence suffices for a decision, abstaining otherwise (evidence competence assessment, ECA); tracks per-actor, per-corridor risk with a jump-diffusion trust process (corridor risk score, CRS)~\\cite{tran2026chronosrep,tran2026crosstrust}; and bounds the concentration of response actions with a Gini-based constraint (G-surv)."),
 ("The research community has responded with surveys, systematizations of knowledge (SoKs), protocols, analysers and monitors. Existing SoKs, however, answer different questions from the one a bridge engineer or auditor faces.",
  "Existing systematizations of knowledge (SoKs) answer different questions from the one a bridge engineer or auditor faces."),
 ("Detectors depend on pairing source and destination transactions, which bridges do not publish; ConneX, ABCTracer and XChainDataGen reconstruct these pairs and release datasets~",
  "Detectors depend on pairing source and destination transactions, which tools such as ConneX, ABCTracer and XChainDataGen reconstruct~"),
 ("\\subsubsection{G6, new architectures.} Intent-based bridges, chain abstraction and ZK-verified bridges move trust to solvers, settlement layers and proof circuits; their attack surfaces are only beginning to be measured~",
  "\\subsubsection{G6, new architectures.} Intent-based and ZK-verified bridges move trust to solvers, settlement layers and proof circuits, whose attack surfaces are only beginning to be measured~"),
]
for a, b in R:
    assert a in s, a[:80]
    s = s.replace(a, b, 1)
open(p, 'w', encoding='utf-8').write(s)
print("ok")
