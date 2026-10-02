p = r"C:\Users\dungt\Downloads\PhD\ACIIDS2027-SoK\main.tex"
s = open(p, encoding="utf-8").read()
R = [
 ("\\includegraphics[width=0.8\\linewidth]{figures/fig_prisma.pdf}", "\\includegraphics[width=0.74\\linewidth]{figures/fig_prisma.pdf}"),
 ("\\includegraphics[width=\\linewidth]{figures/fig_roadmap.pdf}", "\\includegraphics[width=0.9\\linewidth]{figures/fig_roadmap.pdf}"),
 ("Section~\\ref{sec:background} introduces the reference model and related reviews, Section~\\ref{sec:method} the review protocol, Sections~\\ref{sec:taxonomy} to~\\ref{sec:gaps} answer RQ1 to RQ3, Section~\\ref{sec:roadmap} presents the doctoral roadmap, and Section~\\ref{sec:validity} discusses validity and concludes.\n", ""),
 ("The remaining work (2026 to 2027) integrates the typed hand-off between Parts II and III, evaluates the three parts end to end on independently generated cross-chain datasets, and extends Part III to observation-layer checks (G1).",
  "The remaining work (2026 to 2027) integrates the hand-off between Parts II and III, evaluates all parts end to end on independently generated datasets, and adds observation-layer checks (G1)."),
 ("These techniques remove T1 by construction only when the verifier itself is correct, which shifts risk to proof systems and verifier code (T2). No design-time study addresses T3, because contract logic is an implementation property.",
  "They remove T1 only if the verifier itself is correct, shifting risk to proof systems and verifier code (T2); no design-time study addresses T3, an implementation property."),
 ("A taxonomy is only useful if its classes can be decided unambiguously. We therefore define classes by the security property they violate rather than by the exploited code pattern.",
  "To make classes decidable, we define them by the violated security property rather than by the exploited code pattern."),
]
for a, b in R:
    assert a in s, a[:60]
    s = s.replace(a, b)
open(p, 'w', encoding='utf-8').write(s)
print("ok")
