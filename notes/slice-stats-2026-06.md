# The medhavi-cancer slice in numbers (June 2026 extraction)

Counts for the data in `data/cancer/`, copied from the original `medhavy-facts` README. They describe the book as it was on 2026-06-29 (10,055 glossary terms, 320 sections). The local `medhavi-cancer` checkout has since changed: its `data/keywords.json` now has no definitions, so re-running `pipeline/01_extract.py` today gives different numbers.

The original README's "reconciliation with the shared dictionary" (0 matches against 253 facts) and its provenance tier (`solid`) described the vote/consensus model and are not carried over.

---

## Images and media links

There **are** image links in the textbook, but they are chapter-level MDX links rather
than glossary-term media records. In the current slice:

- `terms.json` contains **0** media entries; every term has `"media": []`.
- `content/docs/**/*.mdx` contains **149** image references, all local `/images/...` links.
- `public/images/` contains **150** image files totaling **88.1 MB**.
- **141** image references resolve to existing files.
- **141** unique image files are referenced by chapters.
- **8** chapter references are broken because the MDX points to a `.jpg` while the
  corresponding asset exists with another extension.
- **9** files in `public/images/` are currently unreferenced by the chapter MDX.

**Files by extension**

| Extension | Files in `public/images/` | Resolved chapter references |
|---:|---:|---:|
| `.jpg` | 124 | 124 |
| `.png` | 22 | 14 |
| `.gif` | 2 | 1 |
| `.svg` | 2 | 2 |

**Broken chapter image references**

| Source section | Referenced path | Matching asset present |
|---|---|---|
| `Chapter11/4_Mitochondrial_Function_in_Cancer.mdx` | `/images/11-3-2-1.jpg` | `11-3-2-1.png` |
| `Chapter2/3_Hallmarks_of_Cancer.mdx` | `/images/2-3-1-1.jpg` | `2-3-1-1.png` |
| `Chapter24/4_Monoclonal_Antibodies.mdx` | `/images/24-3-1.jpg` | `24-3-1.gif` |
| `Chapter4/2_Mutations_Types_and_Consequences.mdx` | `/images/4-2-2-4.jpg` | `4-2-2-4.png` |
| `Chapter4/4_DNA_Repair_Mechanisms_and_Their_Failure_in_Cancer.mdx` | `/images/4-4-2-1.jpg` | `4-4-2-1.png` |
| `Chapter4/4_DNA_Repair_Mechanisms_and_Their_Failure_in_Cancer.mdx` | `/images/4-4-2-2.jpg` | `4-4-2-2.png` |
| `Chapter6/3_Key_Tumor_Suppressor_Genes.mdx` | `/images/6-3-4-1.jpg` | `6-3-4-1.png` |
| `Chapter6/3_Key_Tumor_Suppressor_Genes.mdx` | `/images/6-3-5-1.jpg` | `6-3-5-1.png` |

**Unreferenced files in `public/images/`**

`11-3-2-1.png`, `2-3-1-1.png`, `24-3-1.gif`, `27-1-1.png`,
`4-2-2-4.png`, `4-4-2-1.png`, `4-4-2-2.png`, `6-3-4-1.png`,
`6-3-5-1.png`.

So the answer is: yes, the textbook has image links; they are currently recoverable from
the chapter MDX, not from the glossary-derived `terms.json` media field. A future extractor
pass could add a separate `images.json` or attach chapter image references to fact evidence.

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

## facts.json — 3,165 candidate claims

Scoured from the chapter prose: **15,844** raw sentences were segmented and filtered
(declarative, decontextualized, factual-verb-bearing, length 40–300 chars, no discourse-marker
or attribution openers, no truncated abbreviations) down to **3,165** candidate facts — a
**~20% yield**. Each is cited to its source section with the same fact schema as the rest
of the dictionary.

- **243** distinct source sections (of 320) produced facts
- canonical length: min 40 · mean 157 · max 300 chars
- status: all 3,165 have `no_evidence`

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
