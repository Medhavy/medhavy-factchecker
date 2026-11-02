<!-- heuristic-triage-banner -->
> **Heuristic triage, not fact-checking.** These labels came from word-pattern rules in `generate_codex_verdicts.py`. No source was consulted: no URL, no quoted passage. PLAUSIBLE means the sentence matched no suspicious pattern. It does not mean a source supports it. NOT CHECKED means a database lookup is still needed. See `README-HEURISTIC.md`.

## Assertions Report: Introduction
**Date:** 2026-06-30
**Source section:** Introduction
**Book URL:** /docs/Chapter22/0_Introduction
**Assertions checked:** 3
**Breakdown:** AI-ONLY: 2 | STAT: 1

### Flagged by the rules (emphatic wording with no hedge; not an error finding)
None found.

### Full Findings

#### AI-ONLY — PLAUSIBLE (rule-based, no source)
**fact_id:** `cancer-historical-documents-indicate-that-arsenicals-were-employed-in-cancer-tre`
**Assertion type:** POSITIVE
**Sentence:** Historical documents indicate that arsenicals were employed in cancer treatment starting in the 1900s.
**Claim checked:** Historical documents indicate that arsenicals were employed in cancer treatment starting in the 1900s.
**Source:** model-knowledge (low)
**Source URL:** 
**Finding:** Basic textbook-level assertion appears consistent with standard oncology knowledge. Confidence 0.60.
**Expert review needed:** No

#### STAT — NOT CHECKED (needs a database)
**fact_id:** `cancer-the-field-of-cancer-chemotherapy-originated-at-the-beginning-of-the-20th-`
**Assertion type:** BASIC
**Sentence:** The field of cancer chemotherapy originated at the beginning of the 20th century with attempts to identify chemicals that might affect disease through screening using transplantable tumors in rodents.
**Claim checked:** The field of cancer chemotherapy originated at the beginning of the 20th century with attempts to identify chemicals that might affect disease through screening using transplantable tumors in rodents.
**Source:** not-located (low)
**Source URL:** 
**Finding:** Requires live authoritative verification in this category; no decisive source is recorded in this independent Codex pass. Confidence 0.25.
**Expert review needed:** Yes

#### AI-ONLY — PLAUSIBLE (rule-based, no source)
**fact_id:** `cancer-the-term-chemotherapy-was-coined-by-german-chemist-paul-ehrlich-who-inves`
**Assertion type:** BASIC
**Sentence:** The term "chemotherapy" was coined by German chemist Paul Ehrlich, who investigated the use of drugs to treat infectious diseases and pioneered the use of animal models to screen chemicals for potential therapeutic activity.
**Claim checked:** The term "chemotherapy" was coined by German chemist Paul Ehrlich, who investigated the use of drugs to treat infectious diseases and pioneered the use of animal models to screen chemicals for potential therapeutic activity.
**Source:** model-knowledge (low)
**Source URL:** 
**Finding:** Basic textbook-level assertion appears consistent with standard oncology knowledge. Confidence 0.60.
**Expert review needed:** No

