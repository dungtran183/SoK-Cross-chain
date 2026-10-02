"""Record title/abstract screening decisions (keyed by normalised title) from a batch
of indices into prisma/screen_auto.csv order. Usage: ta_record.py <start> <end> <comma-list-of-included-idx>"""
import csv, json, os, re, sys
KB = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
rows = list(csv.DictReader(open(os.path.join(KB, "prisma/screen_auto.csv"), encoding="utf-8")))
start, end = int(sys.argv[1]), int(sys.argv[2])
inc = {int(x) for x in sys.argv[3].split(",") if x.strip()}
f = os.path.join(KB, "prisma/ta_decisions.json")
d = json.load(open(f)) if os.path.exists(f) else {}
norm = lambda t: re.sub(r"[^a-z0-9]", "", t.lower())[:90]
for i in range(start, min(end, len(rows))):
    d[norm(rows[i]["title"])] = "include" if i in inc else "exclude"
json.dump(d, open(f, "w"), indent=0)
print(len(d), "decisions;", sum(v == "include" for v in d.values()), "included")
