p = r"C:\Users\dungt\Downloads\PhD\ACIIDS2027-SoK\main.tex"
s = open(p, encoding="utf-8").read()
R = [
 # abstract acronym form
 ("We report a systematic review following the PRISMA 2020 guideline (Preferred Reporting Items for Systematic Reviews and Meta-Analyses) of 2,369 records",
  "Following the Preferred Reporting Items for Systematic Reviews and Meta-Analyses (PRISMA) 2020 guideline, we review 2,369 records"),
 # paper map wording
 ("Sections~\\ref{sec:background} and~\\ref{sec:method} give the background and protocol,",
  "The remainder of this paper is organized as follows. Sections~\\ref{sec:background} and~\\ref{sec:method} give the background and protocol,"),
 # float proximity for Fig. 2: move first reference next to the figure
 ("statement~\\cite{page2021prisma}; Fig.~\\ref{fig:prisma} reports the flow.", "statement~\\cite{page2021prisma}."),
 ("Titles and abstracts of the remaining 911 records were then screened",
  "Fig.~\\ref{fig:prisma} reports the resulting flow. Titles and abstracts of the remaining 911 records were then screened"),
 # acronyms
 ("a light-client or zero-knowledge proof of $C_s$ consensus", "a light-client or zero-knowledge (ZK) proof of $C_s$ consensus"),
 ("design-time proposals neither in a CORE A*/A venue or Q1 journal",
  "design-time proposals neither in a venue ranked A* or A by the Computing Research and Education Association of Australasia (CORE) or a first-quartile (Q1) journal"),
 ("the Semantic Scholar bulk search API and the arXiv API", "the Semantic Scholar bulk search interface and the arXiv interface"),
 ("but its search API returned an anti-bot challenge", "but its search interface returned an anti-bot challenge"),
 ("\\caption{Comparison with prior reviews (\\yes{} covered, \\partly{} partly, \\no{} not covered).}",
  "\\caption{Comparison with prior reviews (\\yes{} covered, \\partly{} partly, \\no{} not covered; MLR: multivocal literature review; SLR: systematic literature review).}"),
 ("the query omits terms such as sidechain, relay, HTLC and light client", "the query omits terms such as sidechain, relay, hash time-locked contract and light client"),
 ("performed by a single reviewer with LLM assistance under the documented criteria", "performed by a single reviewer assisted by a large language model under the documented criteria"),
 ("Cross-chain credential lifecycle on three EVM chains~", "Cross-chain credential lifecycle on three Ethereum-compatible chains~"),
 # conclusion: move data availability + disclosure into LNCS credits block
 ("\\subsubsection{Data availability.} Search scripts, raw records, screening decisions and the coded corpus are available at [SUPPLEMENT-URL].\n",
  "\\begin{credits}\n\\subsubsection{Data availability.} Search scripts, raw records, screening decisions and the coded corpus are available at [SUPPLEMENT-URL].\n\n\\subsubsection{\\discintname} [DISCLOSURE: The authors have no competing interests to declare that are relevant to the content of this article.]\n\\end{credits}\n"),
]
for a, b in R:
    assert a in s, a[:80]
    s = s.replace(a, b, 1)
open(p, 'w', encoding='utf-8').write(s)
print("ok")
