<!-- heuristic-triage-banner -->
> **Heuristic triage, not fact-checking.** These labels came from word-pattern rules in `generate_codex_verdicts.py`. No source was consulted: no URL, no quoted passage. PLAUSIBLE means the sentence matched no suspicious pattern. It does not mean a source supports it. NOT CHECKED means a database lookup is still needed. See `README-HEURISTIC.md`.

## Assertions Report: Introduction
**Date:** 2026-06-30
**Source section:** Introduction
**Book URL:** /docs/Chapter16/0_Introduction
**Assertions checked:** 2
**Breakdown:** AI-ONLY: 2

### Flagged by the rules (emphatic wording with no hedge; not an error finding)
- **AI-ONLY / PLAUSIBLE / COMBINATION**
  - fact_id: `cancer-understanding-the-molecular-and-cellular-mechanisms-underlying-tumor-immu`
  - Sentence: Understanding the molecular and cellular mechanisms underlying tumor-immune interactions is now essential for developing more effective therapeutic strategies, predicting treatment responses, and overcoming resistance mechanisms that limit the efficacy of current immunotherapies.
  - Finding: Basic textbook-level assertion appears consistent with standard oncology knowledge.

### Full Findings

#### AI-ONLY — PLAUSIBLE (rule-based, no source)
**fact_id:** `cancer-the-dynamic-interplay-between-malignant-cells-and-the-immune-system-repre`
**Assertion type:** BASIC
**Sentence:** The dynamic interplay between malignant cells and the immune system represents one of the most complex and therapeutically promising areas in modern oncology.
**Claim checked:** The dynamic interplay between malignant cells and the immune system represents one of the most complex and therapeutically promising areas in modern oncology.
**Source:** model-knowledge (low)
**Source URL:** 
**Finding:** Basic textbook-level assertion appears consistent with standard oncology knowledge. Confidence 0.60.
**Expert review needed:** No

#### AI-ONLY — PLAUSIBLE (rule-based, no source)
**fact_id:** `cancer-understanding-the-molecular-and-cellular-mechanisms-underlying-tumor-immu`
**Assertion type:** COMBINATION
**Sentence:** Understanding the molecular and cellular mechanisms underlying tumor-immune interactions is now essential for developing more effective therapeutic strategies, predicting treatment responses, and overcoming resistance mechanisms that limit the efficacy of current immunotherapies.
**Claim checked:** Understanding the molecular and cellular mechanisms underlying tumor-immune interactions is now essential for developing more effective therapeutic strategies, predicting treatment responses, and overcoming resistance mechanisms that limit the efficacy of current immunotherapies.
**Source:** model-knowledge (low)
**Source URL:** 
**Finding:** Basic textbook-level assertion appears consistent with standard oncology knowledge. Confidence 0.60.
**Expert review needed:** Yes

