<!-- heuristic-triage-banner -->
> **Heuristic triage, not fact-checking.** These labels came from word-pattern rules in `generate_codex_verdicts.py`. No source was consulted: no URL, no quoted passage. PLAUSIBLE means the sentence matched no suspicious pattern. It does not mean a source supports it. NOT CHECKED means a database lookup is still needed. See `README-HEURISTIC.md`.

## Assertions Report: Introduction
**Date:** 2026-06-30
**Source section:** Introduction
**Book URL:** /docs/Chapter10/1_Introduction
**Assertions checked:** 3
**Breakdown:** AI-ONLY: 3

### Flagged by the rules (emphatic wording with no hedge; not an error finding)
- **AI-ONLY / PLAUSIBLE / COMBINATION**
  - fact_id: `cancer-programmed-cell-death-plays-critical-roles-in-a-wide-variety-of-physiolog`
  - Sentence: Programmed cell death plays critical roles in a wide variety of physiologic processes during fetal development and in adult tissues.
  - Finding: Basic textbook-level assertion appears consistent with standard oncology knowledge.
- **AI-ONLY / PLAUSIBLE / COMBINATION**
  - fact_id: `cancer-the-ability-of-cancer-cells-to-evade-apoptosis-represents-one-of-the-fund`
  - Sentence: The ability of cancer cells to evade apoptosis represents one of the fundamental hallmarks of malignancy and constitutes a critical step in tumor development and therapeutic resistance.
  - Finding: Basic textbook-level assertion appears consistent with standard oncology knowledge.

### Full Findings

#### AI-ONLY — PLAUSIBLE (rule-based, no source)
**fact_id:** `cancer-in-most-cases-physiologic-cell-death-occurs-by-a-process-known-as-apoptos`
**Assertion type:** BASIC
**Sentence:** In most cases, physiologic cell death occurs by a process known as "apoptosis." Defects in apoptotic cell death contribute to neoplastic diseases, by preventing or delaying normal cell turnover, thus promoting cell accumulation.
**Claim checked:** In most cases, physiologic cell death occurs by a process known as "apoptosis." Defects in apoptotic cell death contribute to neoplastic diseases, by preventing or delaying normal cell turnover, thus promoting cell accumulation.
**Source:** model-knowledge (low)
**Source URL:** 
**Finding:** Basic textbook-level assertion appears consistent with standard oncology knowledge. Confidence 0.60.
**Expert review needed:** No

#### AI-ONLY — PLAUSIBLE (rule-based, no source)
**fact_id:** `cancer-programmed-cell-death-plays-critical-roles-in-a-wide-variety-of-physiolog`
**Assertion type:** COMBINATION
**Sentence:** Programmed cell death plays critical roles in a wide variety of physiologic processes during fetal development and in adult tissues.
**Claim checked:** Programmed cell death plays critical roles in a wide variety of physiologic processes during fetal development and in adult tissues.
**Source:** model-knowledge (low)
**Source URL:** 
**Finding:** Basic textbook-level assertion appears consistent with standard oncology knowledge. Confidence 0.60.
**Expert review needed:** Yes

#### AI-ONLY — PLAUSIBLE (rule-based, no source)
**fact_id:** `cancer-the-ability-of-cancer-cells-to-evade-apoptosis-represents-one-of-the-fund`
**Assertion type:** COMBINATION
**Sentence:** The ability of cancer cells to evade apoptosis represents one of the fundamental hallmarks of malignancy and constitutes a critical step in tumor development and therapeutic resistance.
**Claim checked:** The ability of cancer cells to evade apoptosis represents one of the fundamental hallmarks of malignancy and constitutes a critical step in tumor development and therapeutic resistance.
**Source:** model-knowledge (low)
**Source URL:** 
**Finding:** Basic textbook-level assertion appears consistent with standard oncology knowledge. Confidence 0.60.
**Expert review needed:** Yes

