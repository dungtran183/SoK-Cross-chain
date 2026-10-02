# Supplementary Material: Attacking the Bridge (ACIIDS 2027)

This folder can be published as is (e.g., as a Zenodo or GitHub release) and cited in the paper's Data availability statement.

| Path | Content |
|---|---|
| `scripts/prisma_search.py` | Identification: OpenAlex, Semantic Scholar and arXiv queries (search date 2026-10-02) |
| `prisma/raw_*.csv` | All raw records per source (2,369) |
| `scripts/prisma_merge.py` | De-duplication and automated rules R1–R4 |
| `prisma/records_dedup.csv`, `prisma/screen_auto.csv` | 1,392 unique records and the 911 records left after the automated rules |
| `prisma/ta_decisions.json` | Title/abstract screening decisions |
| `scripts/eligibility.py`, `prisma/eligibility.csv` | Eligibility decisions with exclusion codes EC1–EC5 |
| `included.csv` | The 168 included studies (S001–S168) with category and tags |
| `scripts/code_studies.py`, `coded_studies.csv`, `prisma/coverage_matrix.json` | Stage and attack-class coding (Table 3) |
| `incidents.csv` | 16 incidents, each with two sources (Table 2) |
| `prisma/counts_*.json` | PRISMA flow counts (Fig. 2) |
| `scripts/fetch_bib.py`, `prisma/reference_audit.log` | DOI-based reference verification |
| `papers/`, `registry.json`, `exports/dashboard.html` | Knowledge-base cards and the interactive dashboard |

Before publishing, remove or ignore `_logs/` and `pdf/`. Do not redistribute PDFs of copyrighted papers.
