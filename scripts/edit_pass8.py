p = r"C:\Users\dungt\Downloads\PhD\ACIIDS2027-SoK\main.tex"
s = open(p, encoding="utf-8").read()
R = [
 ("\\newcommand{\\no}{--}\n", "\\newcommand{\\no}{--}\n\\newcolumntype{L}[1]{>{\\raggedright\\arraybackslash}p{#1}}\n\\raggedbottom\n"),
 ("\\begin{tabular}{@{}llrp{4.9cm}cc@{}}", "\\begin{tabular}{@{}llrL{4.9cm}cc@{}}"),
 ("\\begin{tabular}{@{}lp{4.6cm}p{5.3cm}@{}}", "\\begin{tabular}{@{}lL{4.6cm}L{5.3cm}@{}}"),
]
for a, b in R:
    assert a in s, a[:80]
    s = s.replace(a, b, 1)
open(p, 'w', encoding='utf-8').write(s)
print("ok")
