import re, sys
p = sys.argv[1]
s = open(p, encoding="utf-8").read()
s = re.sub(r"&amp;(?:amp;)*", "&", s)          # undo HTML entities from Crossref
s = re.sub(r"(?<!\\)&", r"\\&", s)               # escape bare ampersands for LaTeX
open(p, "w", encoding="utf-8").write(s)
print("escaped", s.count("\\&"))
