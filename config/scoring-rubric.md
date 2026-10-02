# Scoring Rubric — Cross-Chain Bridge Attacks

How papers are vetted, scored, and classified for this knowledge base. Two
independent systems: a **venue-quality gate** (keep/exclude), a **discovery
relevance score** (0–10, what to chase first), and a **novelty classification**
(assigned to every integrated card).

---

## 1. Venue-quality gate (hard filter)

Applied during discovery. A candidate is **kept** only if its venue is reputable.

**Reputable (keep):**
- CORE 2023 **A\*** / **A** conferences.
- Flagship journals: IEEE Transactions on *, IEEE Internet of Things Journal (IOT-J),
  ACM Transactions on *, and other Q1 journals with **IF ≥ 5** that are **Q1 in both
  WoS and Scopus**.
- Tier is assigned by `scripts/kblib.py:classify_venue()` against `assets/venues.json`.

**Excluded (never auto-accept):**
- MDPI, Hindawi, Frontiers, IEEE Access, Scientific Reports, PLOS ONE, Heliyon,
  and other mega-journals / predatory publishers.

**Preprints / arXiv:**
- Excluded **unless** authored by a widely recognized researcher / group (heavily
  cited, foundational). These get `novelty: foundational` or are flagged for review.

---

## 2. Discovery relevance score (0–10)

Sum of four components. Used to triage candidates into accept / review / discard.

| Component         | Points | Encoding |
|-------------------|--------|----------|
| Query match       | 0–3    | 0 tangential · 1 related field · 2 same sub-domain · 3 exact topic |
| Citation overlap  | 0–3    | 0 none · 1 (1–2 shared refs with KB) · 2 (3–5) · 3 (6+ shared) |
| Recency           | 0–2    | 0 (>3 yr) · 1 (1–3 yr) · 2 (<1 yr) |
| Venue quality     | 0–2    | 0 unknown/preprint · 1 reputable · 2 top-tier (CORE A*/flagship) |

**Thresholds**
- **≥ 5** → auto-accept (queue for download + extraction)
- **3–4** → human review (`candidates/pending-review.md`)
- **< 3** → discard

---

## 3. Novelty classification (per card)

| Class           | When |
|-----------------|------|
| `sota`          | >10% improvement on a tracked benchmark, a fundamentally new capability, a widely-adopted new benchmark, or a strong open-source system. |
| `incremental`   | Builds directly on a SoTA method; minor extension; <10% improvement. |
| `complementary` | Different sub-problem / methodology in the same domain; not directly comparable. |
| `derivative`    | Applies well-known methods unmodified to a new domain; no new benchmark. |
| `survey`        | Review / survey paper. |
| `foundational`  | Architectural/algorithmic/conceptual ancestor that multiple SoTA cards depend on (paradigm-defining, broad lineage, temporal priority). Carries a `descendants:` list; descendant cards may set `ancestors: [...]`. |

`sota` and `foundational` papers get the **full** card write-up (Problem Statement,
Method Summary, Key Results, Baselines, Limitations, Novelty Claims, Key References).
Incremental / derivative / complementary papers get a concise 3-section stub.
