<!-- heuristic-triage-banner -->
> **Heuristic triage, not fact-checking.** These labels came from word-pattern rules in `generate_codex_verdicts.py`. No source was consulted: no URL, no quoted passage. PLAUSIBLE means the sentence matched no suspicious pattern. It does not mean a source supports it. NOT CHECKED means a database lookup is still needed. See `README-HEURISTIC.md`.

## Assertions Report: Conclusion
**Date:** 2026-06-30
**Source section:** Conclusion
**Book URL:** /docs/Chapter24/12_Conclusion
**Assertions checked:** 3
**Breakdown:** AI-ONLY: 2 | CURRENT: 1

### Flagged by the rules (emphatic wording with no hedge; not an error finding)
- **AI-ONLY / PLAUSIBLE / COMBINATION**
  - fact_id: `cancer-the-integration-of-precision-medicine-approaches-including-comprehensive-`
  - Sentence: The integration of precision medicine approaches, including comprehensive tumor profiling and resistance monitoring, is essential for optimizing the use of targeted therapies.
  - Finding: Basic textbook-level assertion appears consistent with standard oncology knowledge.
- **AI-ONLY / PLAUSIBLE / COMBINATION**
  - fact_id: `cancer-the-success-of-targeted-therapies-has-proven-that-understanding-the-molec`
  - Sentence: The success of targeted therapies has proven that understanding the molecular basis of cancer can lead to more effective and less toxic treatments.
  - Finding: Mechanism is consistent with standard biomedical textbook knowledge.

### Full Findings

#### CURRENT — NOT CHECKED (needs a database)
**fact_id:** `cancer-the-field-continues-to-evolve-rapidly-with-new-targets-being-identified-n`
**Assertion type:** BASIC
**Sentence:** The field continues to evolve rapidly, with new targets being identified, novel drug classes being developed, and innovative combination strategies being explored.
**Claim checked:** The field continues to evolve rapidly, with new targets being identified, novel drug classes being developed, and innovative combination strategies being explored.
**Source:** not-located (low)
**Source URL:** 
**Finding:** Requires live authoritative verification in this category; no decisive source is recorded in this independent Codex pass. Confidence 0.25.
**Expert review needed:** Yes

#### AI-ONLY — PLAUSIBLE (rule-based, no source)
**fact_id:** `cancer-the-integration-of-precision-medicine-approaches-including-comprehensive-`
**Assertion type:** COMBINATION
**Sentence:** The integration of precision medicine approaches, including comprehensive tumor profiling and resistance monitoring, is essential for optimizing the use of targeted therapies.
**Claim checked:** The integration of precision medicine approaches, including comprehensive tumor profiling and resistance monitoring, is essential for optimizing the use of targeted therapies.
**Source:** model-knowledge (low)
**Source URL:** 
**Finding:** Basic textbook-level assertion appears consistent with standard oncology knowledge. Confidence 0.60.
**Expert review needed:** Yes

#### AI-ONLY — PLAUSIBLE (rule-based, no source)
**fact_id:** `cancer-the-success-of-targeted-therapies-has-proven-that-understanding-the-molec`
**Assertion type:** COMBINATION
**Sentence:** The success of targeted therapies has proven that understanding the molecular basis of cancer can lead to more effective and less toxic treatments.
**Claim checked:** The success of targeted therapies has proven that understanding the molecular basis of cancer can lead to more effective and less toxic treatments.
**Source:** model-knowledge (low)
**Source URL:** 
**Finding:** Mechanism is consistent with standard biomedical textbook knowledge. Confidence 0.64.
**Expert review needed:** Yes

