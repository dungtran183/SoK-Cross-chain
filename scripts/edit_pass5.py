p = r"C:\Users\dungt\Downloads\PhD\ACIIDS2027-SoK\main.tex"
s = open(p, encoding="utf-8").read()
R = [
 # abstract acronyms
 ("the costliest attack surface of decentralized finance:", "the costliest attack surface of decentralized finance (DeFi):"),
 ("We report a PRISMA 2020 systematic review of 2,369 records",
  "We report a systematic review following the PRISMA 2020 guideline (Preferred Reporting Items for Systematic Reviews and Meta-Analyses) of 2,369 records"),
 # intro acronyms + paper map
 ("The research community has responded with surveys, systematizations of knowledge (SoKs), protocols,",
  "The research community has responded with surveys, systematizations of knowledge (SoKs), protocols,"),
 ("\\item A doctoral research roadmap that instantiates the lifecycle with three connected thesis parts and reports their preliminary results.\n\\end{enumerate}\n",
  "\\item A doctoral research roadmap that instantiates the lifecycle with three connected thesis parts and reports their preliminary results.\n\\end{enumerate}\nSections~\\ref{sec:background} and~\\ref{sec:method} give the background and protocol, Sections~\\ref{sec:taxonomy} to~\\ref{sec:gaps} answer RQ1 to RQ3, Section~\\ref{sec:roadmap} presents the roadmap, and Sections~\\ref{sec:validity} and~\\ref{sec:conclusion} discuss validity and conclude.\n"),
 ("We followed the PRISMA 2020 statement~\\cite{page2021prisma};", "We followed the Preferred Reporting Items for Systematic Reviews and Meta-Analyses (PRISMA) 2020 statement~\\cite{page2021prisma};"),
 ("Off-chain relayers, oracles and RPC nodes observe $e$ (2).", "Off-chain relayers, oracles and remote procedure call (RPC) nodes observe $e$ (2)."),
 ("a multisignature or threshold signature of a committee,", "a multisignature or threshold signature of a committee that may use multi-party computation (MPC),"),
 ("as in the IBC light-client jamming attack~", "as in the light-client jamming attack on the Inter-Blockchain Communication (IBC) protocol~"),
 ("\\subsubsection{T6, economic and user-level attacks} (violate P6). Transparent source-chain events enable cross-chain sandwiching~",
  "\\subsubsection{T6, economic and user-level attacks} (violate P6). Transparent source-chain events enable maximal-extractable-value (MEV) strategies such as cross-chain sandwiching~"),
 # calibrated causal claim
 ("First, Part II improves on the strongest static baseline only modestly, which supports G3: gains are bounded by data, not by model capacity.",
  "First, Part II improves on the strongest static baseline only modestly; with 91 labelled traces, this is consistent with G3, which identifies data rather than model capacity as the likely bottleneck."),
 # split threats / conclusion (two-paragraph conclusion: synthesis + future work)
 ("\\section{Threats to Validity and Conclusion}\\label{sec:validity}", "\\section{Threats to Validity}\\label{sec:validity}"),
 ("Incident figures are nominal and come from grey literature, which we mitigated with two-source confirmation.\n\nThis review systematized",
  "Incident figures are nominal and come from grey literature, which we mitigated with two-source confirmation.\n\n%=====================================================================\n\\section{Conclusion}\\label{sec:conclusion}\n%=====================================================================\nThis review systematized"),
 ("The doctoral roadmap addresses these gaps by connecting the three stages through typed hand-offs.",
  "The doctoral roadmap addresses these gaps by connecting the three stages through typed hand-offs.\n\nFuture work will maintain the corpus as a living review, build a leakage-free benchmark that spans design, pre-deployment and runtime evidence, and develop monitors that check source-event authenticity across independently operated observers while preserving the privacy guarantees of design-time protocols."),
]
for a, b in R:
    assert a in s, a[:80]
    s = s.replace(a, b, 1)
open(p, 'w', encoding='utf-8').write(s)
print("ok")
