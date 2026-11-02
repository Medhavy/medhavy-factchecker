<!-- heuristic-triage-banner -->
> **Heuristic triage, not fact-checking.** These labels came from word-pattern rules in `generate_codex_verdicts.py`. No source was consulted: no URL, no quoted passage. PLAUSIBLE means the sentence matched no suspicious pattern. It does not mean a source supports it. NOT CHECKED means a database lookup is still needed. See `README-HEURISTIC.md`.

## Assertions Report: Introduction
**Date:** 2026-06-30
**Source section:** Introduction
**Book URL:** /docs/Chapter24/1_Introduction
**Assertions checked:** 3
**Breakdown:** AI-ONLY: 2 | SPECIALIST: 1

### Flagged by the rules (emphatic wording with no hedge; not an error finding)
None found.

### Full Findings

#### SPECIALIST — NOT CHECKED (needs a database)
**fact_id:** `cancer-in-like-manner-their-toxicity-often-relates-to-off-target-activity-either`
**Assertion type:** BASIC
**Sentence:** In like manner, their toxicity often relates to off-target activity, either to the unmutated kinase or to closely related, normal kinases.
**Claim checked:** In like manner, their toxicity often relates to off-target activity, either to the unmutated kinase or to closely related, normal kinases.
**Source:** not-located (low)
**Source URL:** 
**Finding:** Requires live authoritative verification in this category; no decisive source is recorded in this independent Codex pass. Confidence 0.25.
**Expert review needed:** Yes

#### AI-ONLY — PLAUSIBLE (rule-based, no source)
**fact_id:** `cancer-targeted-therapies-represent-a-revolutionary-approach-in-cancer-treatment`
**Assertion type:** BASIC
**Sentence:** Targeted therapies represent a revolutionary approach in cancer treatment, moving away from broadly cytotoxic agents toward drugs that specifically target the molecular abnormalities of cancer cells.
**Claim checked:** Targeted therapies represent a revolutionary approach in cancer treatment, moving away from broadly cytotoxic agents toward drugs that specifically target the molecular abnormalities of cancer cells.
**Source:** model-knowledge (low)
**Source URL:** 
**Finding:** Basic textbook-level assertion appears consistent with standard oncology knowledge. Confidence 0.60.
**Expert review needed:** No

#### AI-ONLY — PLAUSIBLE (rule-based, no source)
**fact_id:** `cancer-the-concept-of-targeted-therapy-is-based-on-the-understanding-that-cancer`
**Assertion type:** POSITIVE
**Sentence:** The concept of targeted therapy is based on the understanding that cancer cells harbor specific genetic alterations, protein overexpression, or pathway dysregulation that distinguish them from normal cells.
**Claim checked:** The concept of targeted therapy is based on the understanding that cancer cells harbor specific genetic alterations, protein overexpression, or pathway dysregulation that distinguish them from normal cells.
**Source:** model-knowledge (low)
**Source URL:** 
**Finding:** Basic textbook-level assertion appears consistent with standard oncology knowledge. Confidence 0.60.
**Expert review needed:** No

