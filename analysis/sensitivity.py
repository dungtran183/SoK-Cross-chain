"""Sensitivity of the stage distribution to the evidence thresholds EC4/EC5.

The 132 records excluded under EC4 or EC5 are coded by title for their stage (default D,
because almost all are protocol proposals; exceptions listed below) and flagged when the title
targets authentication or access control (policy-type T3). Indices refer to prisma/eligibility.csv.
"""
import csv, json, os
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
STAGE = {  # non-design exceptions, coded from the title
    31: "-", 77: "-", 169: "-", 269: "-",          # analyses and reviews
    51: "R", 60: "R", 66: "R", 152: "R",          # reputation or credit management of notaries
    220: "R", 226: "R", 229: "R",                 # anomaly detection
}
T3_POLICY = {61, 62, 68, 74, 78, 80, 120, 197, 199, 201, 215, 222, 223, 224, 234, 241, 290, 293, 296, 303, 315}
T3_IMPL = set()  # no excluded record targets implementation flaws by title

elig = list(csv.DictReader(open(os.path.join(HERE, "data/prisma/eligibility.csv"), encoding="utf-8")))
exc = [r for r in elig if r["reason"] in ("EC4", "EC5")]
assert len(exc) == 132
stage = Counter(STAGE.get(int(r["idx"]), "D") for r in exc)
rec = list(csv.DictReader(open(os.path.join(HERE, "recoded_studies.csv"), encoding="utf-8")))
inc_stage = Counter("survey" if r["survey"] == "1" else r["stage_new"] for r in rec)
n_inc, n_all = len(rec), len(rec) + len(exc)
out = dict(excluded=len(exc), by_reason=dict(Counter(r["reason"] for r in exc)), excluded_stage=dict(stage),
           included_stage=dict(inc_stage), design_share_included=round(inc_stage["D"] / n_inc, 3),
           design_share_with_excluded=round((inc_stage["D"] + stage["D"]) / n_all, 3),
           t3_policy_excluded=len(T3_POLICY), t3_impl_excluded=len(T3_IMPL),
           runtime_with_excluded=inc_stage["R"] + stage["R"])
json.dump(out, open(os.path.join(HERE, "sensitivity.json"), "w"), indent=1)
print(json.dumps(out, indent=1))
