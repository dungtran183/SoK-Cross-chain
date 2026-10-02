p = r"C:\Users\dungt\Downloads\PhD\ACIIDS2027-SoK\main.tex"
s = open(p, encoding="utf-8").read()
R = [
 ("\\includegraphics[width=0.74\\linewidth]{figures/fig_prisma.pdf}", "\\includegraphics[width=98mm]{figures/fig_prisma.pdf}"),
 ("\\includegraphics[width=0.9\\linewidth]{figures/fig_roadmap.pdf}", "\\includegraphics[width=\\linewidth]{figures/fig_roadmap.pdf}"),
]
for a, b in R:
    assert a in s, a
    s = s.replace(a, b)
open(p, 'w', encoding='utf-8').write(s)
print("ok")
