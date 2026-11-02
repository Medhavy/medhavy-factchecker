<!-- heuristic-triage-banner -->
> **Heuristic triage, not fact-checking.** These labels came from word-pattern rules in `generate_codex_verdicts.py`. No source was consulted: no URL, no quoted passage. PLAUSIBLE means the sentence matched no suspicious pattern. It does not mean a source supports it. NOT CHECKED means a database lookup is still needed. See `README-HEURISTIC.md`.

## Assertions Report: Introduction
**Date:** 2026-06-30
**Source section:** Introduction
**Book URL:** /docs/Chapter9/1_Introduction
**Assertions checked:** 3
**Breakdown:** AI-ONLY: 2 | SPECIALIST: 1

### Flagged by the rules (emphatic wording with no hedge; not an error finding)
- **AI-ONLY / PLAUSIBLE / COMBINATION**
  - fact_id: `cancer-the-precise-control-of-cell-cycle-progression-is-essential-for-normal-dev`
  - Sentence: The precise control of cell cycle progression is essential for normal development, tissue homeostasis, and prevention of diseases such as cancer.
  - Finding: Basic textbook-level assertion appears consistent with standard oncology knowledge.

### Full Findings

#### AI-ONLY — PLAUSIBLE (rule-based, no source)
**fact_id:** `cancer-at-the-heart-of-the-cell-cycle-control-system-is-a-family-of-protein-kina`
**Assertion type:** POSITIVE
**Sentence:** At the heart of the cell-cycle control system is a family of protein kinases known as cyclin-dependent kinases (Cdks).
**Claim checked:** At the heart of the cell-cycle control system is a family of protein kinases known as cyclin-dependent kinases (Cdks).
**Source:** model-knowledge (low)
**Source URL:** 
**Finding:** Matches standard biomedical terminology at textbook level. Confidence 0.72.
**Expert review needed:** No

#### SPECIALIST — NOT CHECKED (needs a database)
**fact_id:** `cancer-the-oscillations-lead-directly-to-cyclical-changes-in-the-phosphorylation`
**Assertion type:** BASIC
**Sentence:** The oscillations lead directly to cyclical changes in the phosphorylation of intracellular proteins that initiate or regulate the major events of the cell cycle—DNA replication, mitosis, and cytokinesis.
**Claim checked:** The oscillations lead directly to cyclical changes in the phosphorylation of intracellular proteins that initiate or regulate the major events of the cell cycle—DNA replication, mitosis, and cytokinesis.
**Source:** not-located (low)
**Source URL:** 
**Finding:** Requires live authoritative verification in this category; no decisive source is recorded in this independent Codex pass. Confidence 0.25.
**Expert review needed:** Yes

#### AI-ONLY — PLAUSIBLE (rule-based, no source)
**fact_id:** `cancer-the-precise-control-of-cell-cycle-progression-is-essential-for-normal-dev`
**Assertion type:** COMBINATION
**Sentence:** The precise control of cell cycle progression is essential for normal development, tissue homeostasis, and prevention of diseases such as cancer.
**Claim checked:** The precise control of cell cycle progression is essential for normal development, tissue homeostasis, and prevention of diseases such as cancer.
**Source:** model-knowledge (low)
**Source URL:** 
**Finding:** Basic textbook-level assertion appears consistent with standard oncology knowledge. Confidence 0.60.
**Expert review needed:** Yes

