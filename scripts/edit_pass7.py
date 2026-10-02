p = r"C:\Users\dungt\Downloads\PhD\ACIIDS2027-SoK\main.tex"
s = open(p, encoding="utf-8").read()
R = [
 ("The thresholds of EC4 and EC5 keep the large and heterogeneous body of protocol proposals tractable while retaining all peer-reviewed attack and detection studies.",
  "EC4 and EC5 keep the large body of protocol proposals tractable while retaining all peer-reviewed attack and detection studies."),
 ("Two observations shape the remaining work. First,", "First,"),
]
for a, b in R:
    assert a in s, a[:80]
    s = s.replace(a, b, 1)
open(p, 'w', encoding='utf-8').write(s)
print("ok")
