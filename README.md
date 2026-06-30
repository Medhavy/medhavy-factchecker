# medhavi-facts — knowledge slice for *medhavi-cancer*

A deterministically extracted knowledge slice for the **medhavi-cancer** textbook,
in the same four-file format as the shared dictionary's other domains (`facts/biology/`,
`facts/anatomy/`, …): `terms.json`, `graph.json`, `facts.json`, `preview.md`.

No language model is in the loop. Same inputs in → byte-identical files out. Definitions
are the book's own glossary entries, verbatim; candidate facts are verbatim chapter
sentences. Everything here is **unverified candidate material for expert review** — nothing
is asserted as true.

```
medhavi-facts/
├── README.md                  ← this file
├── extract-medhavi-facts.py   ← the reproducible extractor (re-run to rebuild)
└── cancer/
    ├── terms.json             ← glossary: one entry per term (7.81 MB)
    ├── graph.json             ← concept graph: nodes + edges (3.10 MB)
    ├── facts.json             ← candidate facts scoured from chapters (3.85 MB)
    ├── preview.md             ← human-readable summary
    └── match-report.md        ← reconciliation against the shared dictionary
```

## Sources

| Output | Source in the book | Method |
|---|---|---|
| `terms.json`, `graph.json` | `data/keywords.json` (curated glossary) | term dictionary + concept co-mention graph |
| `facts.json` | `content/docs/**/*.mdx` (38 chapters + 4 appendices) | atomic sentence extraction |
| `match-report.md` | the above vs `facts/facts.json` | deterministic wording-similarity match |

---

## terms.json — 10,055 terms

Every term carries a verbatim `definition`, a `category`, a within-book `url`
(`/glossary/<slug>`), `related` terms (concept links), and a `media` list.

- **10,055** terms, **all with a definition** (0 missing)
- **8,227** terms (81.8%) link to at least one other term
- **22** categories:

| Count | Category | Count | Category |
|---:|---|---:|---|
| 4,103 | Biomedical Science | 209 | Toxicology |
| 1,687 | Biochemistry | 180 | Genomics |
| 946 | Oncology | 151 | Pharmacology |
| 464 | Cell Biology | 49 | Immunology |
| 457 | Genetics | 44 | Pharmaceutical |
| 443 | Biotechnology | 30 | Chemotherapy |
| 394 | Molecular Biology | 23 | Biomarkers |
| 337 | Nanotechnology | 17 | Diagnostics |
| 244 | Pathology | 16 | Immunotherapy |
| 230 | Medical Imaging | 12 | Surgery |
| | | 11 | Drug Delivery |
| | | 8 | Biosensing |

---

## graph.json — 10,055 nodes · 24,347 edges

An edge `A → B` means term **B** is mentioned inside term **A**'s definition. A term's
`in_degree` (how many other definitions reference it) is a prerequisite/foundation signal.

- **24,347** edges, **2.42** edges per term on average
- **7,659** isolated nodes (in_degree 0) — the graph's value is in its high-in-degree core, not the long tail
- in_degree: **max 1,618**, mean 2.42, median 0

**Top 25 most-connected concepts**

| In-degree | Concept | In-degree | Concept |
|---:|---|---:|---|
| 1,618 | Protein | 211 | Translation |
| 1,053 | Gene | 209 | Virus |
| 897 | Cancer | 206 | Chromosome |
| 426 | Genome | 206 | Metabolism |
| 421 | Bacteria | 197 | Amino acid |
| 410 | Molecular biology | 177 | Sequencing |
| 316 | Enzyme | 167 | Biochemistry |
| 298 | Receptor | 159 | Bioinformatics |
| 244 | Transcription | 139 | Carcinoma |
| 230 | MicroRNA | 138 | Breast cancer |
| 224 | Therapy | 135 | Biotechnology |
| 213 | Gene expression | 133 | Lipid |
| | | 133 | Mass spectrometry |

---

## facts.json — 3,165 candidate facts

Scoured from the chapter prose: **15,844** raw sentences were segmented and filtered
(declarative, decontextualized, factual-verb-bearing, length 40–300 chars, no discourse-marker
or attribution openers, no truncated abbreviations) down to **3,165** candidate facts — a
**~20% yield**. Each is cited to its source section with the same fact schema as the rest
of the dictionary.

- **243** distinct source sections (of 320) produced facts
- canonical length: min 40 · mean 157 · max 300 chars
- consensus: **3,165 unverified** (single-source candidates); **0** need review

**By category**

| Count | Category |
|---:|---|
| 2,192 | BASIC |
| 557 | MECHANISM |
| 267 | QUANTITY |
| 107 | CLASSIFICATION |
| 42 | DEFINITION |

**By chapter** (facts extracted per chapter)

| # | Chapter | Facts |
|---:|---|---:|
| 1 | The Building Blocks of Life: Normal Cell Biology | 83 |
| 2 | Introduction to Cancer: A Disease of Deregulation | 152 |
| 3 | Cancer Epidemiology and Risk Factors | 92 |
| 4 | Genetics and Genomic Instability in Cancer | 133 |
| 5 | Oncogenes | 67 |
| 6 | Tumor Suppressor Genes | 108 |
| 7 | Epigenetics in Cancer | 83 |
| 8 | Cancer Etiology | 87 |
| 9 | Cell Cycle Control and Cancer | 79 |
| 10 | Apoptosis and Programmed Cell Death in Cancer | 52 |
| 11 | Cancer Metabolism — The Warburg Effect and Beyond | 83 |
| 12 | Angiogenesis | 105 |
| 13 | Invasion and Metastasis — The Spread of Cancer | 124 |
| 14 | The Tumor Microenvironment | 66 |
| 15 | Cancer Stem Cells and Tumor Heterogeneity | 278 |
| 16 | Tumor Immunology | 118 |
| 17 | Cancer Prevention and Screening | 67 |
| 18 | Cancer Detection and Diagnosis | 67 |
| 19 | Principles of Cancer Therapy | 34 |
| 20 | Surgical Oncology | 76 |
| 21 | Radiation Oncology | 88 |
| 22 | Chemotherapy | 57 |
| 23 | Hormonal Therapies | 61 |
| 24 | Targeted Therapies | 113 |
| 25 | Cancer Immunotherapy | 29 |
| 26 | Gene Therapy and Oncolytic Virotherapy | 54 |
| 27 | Nanotechnology in Cancer | 92 |
| 28 | Clinical Trials and Regulatory Pathways | 37 |
| 29 | Future Directions in Cancer Treatment Research | 67 |
| 30 | Principles of Cancer Classification | 32 |
| 31 | Solid Tumors by Organ/System | 50 |
| 32 | Central Nervous System Tumors | 57 |
| 33 | Hematologic Malignancies | 105 |
| 34 | Pediatric Cancers | 41 |
| 35 | Rare and Orphan Cancers | 100 |
| 36 | Supportive Care and Palliative Care in Oncology | 46 |
| 37 | Cancer Survivorship | 59 |
| 38 | Health Economics and Access to Cancer Care | 59 |
| A | Experimental Models in Cancer Research | 14 |
| B | Essential Techniques and Assays in Cancer Research | 7 |
| C | Advanced Imaging and Photodynamic Therapy | 17 |
| D | Molecular Biology Techniques | 23 |
| — | index | 3 |

---

## Reconciliation with the shared dictionary

Every candidate fact was matched against the shared dictionary `facts/facts.json` using the
same deterministic logic as `extract-facts.py` (difflib token-sort ratio + Jaccard, with a
numeric guard), at the standard thresholds: **0.82** to merge, **0.70** for a near-duplicate
flag. The master dictionary was **not** modified.

**Result: 0 corroborations, 0 conflicts — all 3,165 facts are new to the dictionary.**

This is an honest outcome, not a failure of the matcher. The shared dictionary currently
holds only **253** facts, all from a single OpenStax anatomy book. The highest similarity any
cancer sentence reached was **0.55** — the two books cover overlapping topics (cell cycle,
CNS, apoptosis) but phrase them as genuinely different atomic claims. As more books enter the
dictionary, these candidates will start corroborating and reaching `agreement` (two
independent publishers). See `cancer/match-report.md` for the 25 closest sub-threshold pairs.

---

## Provenance & trust

- **Publisher:** `medhavi` · **Source:** `medhavi-cancer` · **Tier:** `solid`
  (an authored textbook — below OpenStax `trusted`, above general `web`). To treat it as a
  vetted textbook, set its tier to `trusted` in `facts/facts-sources.yaml`.
- **Status:** every fact is `source-attested`, `verified: false`, `consensus: unverified`.
  Human sign-off is the only path to `verified` — by design, not policy.

## Reproducing

```bash
python3 medhavi-facts/extract-medhavi-facts.py
```

Reads `data/keywords.json` and `content/docs/**/*.mdx`, matches against `facts/facts.json`,
and rewrites everything under `medhavi-facts/cancer/`. Deterministic: same inputs produce
identical outputs.

*Generated 2026-06-29.*
