# Assertion triage — medhavi-cancer candidate facts

Date: 2026-11-02 · Input: `data/cancer/facts.json` (3,165 candidate claims) · Output: `triage/triage.jsonl`

## Executive summary

Of the 3,165 "candidate facts", **885 (28%) are not assertions at all**: framing, evaluation, prediction or vagueness that no source could support or refute. Another **799 (25%) are real claims but only a general textbook could confirm them**, so no database record type fits. That leaves **1,481 (47%) assertions that map to a real database** (PubMed, SEER/GLOBOCAN, FDA, gene/protein databases, guideline bodies, ClinicalTrials.gov).

The earlier Codex pass marked 2,562 facts CONFIRMED. **797 of those (31%) are not assertions**, and only **1,029 (40%)** are strict assertions. Codex's verdicts came from word patterns and carry no source or quote, so none of its CONFIRMED rows is evidence.

The example that prompted this ("Understanding normal cellular biology provides the essential foundation for comprehending the aberrant changes that occur in cancer") is labeled NOT_ASSERTION, database `none`.

## The definition used

An assertion is a claim with an entity, a relation and a value (or a definite statement), where some kind of database record could confirm or refute it. If no record type fits, it is not an assertion. This ties "what is an assertion" to "which database can reflect it".

| Label | Meaning | Count | Share |
|---|---|---:|---:|
| SPECIFIC | Falsifiable, with a concrete findable source: numbers, dates, "first/only/predominant", a named drug/trial/study/approval, a named gene or pathway with a precise claim | 878 | 27.7% |
| STANDARD | Falsifiable textbook-level fact (definition, established mechanism, anatomy, classification) | 1,402 | 44.3% |
| NOT_ASSERTION | Framing, evaluative or emphatic wording, prediction, hedged vagueness, tautology, or a fragment that cannot be understood alone | 885 | 28.0% |

Two counts of "real assertion":
- **Loose** (SPECIFIC + STANDARD): 2,280 (72.0%).
- **Strict** (loose, and mapped to a real database type, not the general `reference-text` fallback): **1,481 (46.8%)**.

## Strict assertions by database to query

| Database type | Facts |
|---|---:|
| PubMed (literature) | 902 |
| Gene/protein databases (NCBI Gene, UniProt, Ensembl) | 169 |
| Guideline bodies (NCCN, ASCO, WHO) | 159 |
| SEER / GLOBOCAN (statistics) | 127 |
| FDA (approvals, labels) | 97 |
| ClinicalTrials.gov | 27 |

Caution: PubMed is the label for "some paper states this", and it takes 902 of 1,481 rows. It is the weakest of the database labels. The next step needs real query terms before any of these counts as evidence.

## Against the Codex pass

| Codex group | Rows | Not assertions | Strict assertions |
|---|---:|---:|---:|
| CONFIRMED | 2,562 | 797 (31%) | 1,029 (40%) |
| UNVERIFIED | 603 | 88 | 452 |
| COMBINATION (flagged "highest priority for review") | 157 | 83 (53%) | — |

Codex's UNVERIFIED rows were mostly real assertions it could not check. Its CONFIRMED rows were mostly everything else.

## Other findings

- **291 facts depend on surrounding text to be understood** (fragments, unresolved "the/these"). 163 of them are otherwise real assertions and would need their context before any lookup.
- **Chapters differ a lot.** Strict share is lowest in chapter 1 (basic cell biology): 4 of 83 (5%). It is highest in chapter 28 (clinical trials and regulatory): 30 of 37 (81%), and chapter 12 (angiogenesis): 79 of 105 (75%). Chapters 19 (18%), 20 (22%) and 18 (28%) are also low.

## How reliable these labels are

- Eight model agents labeled the facts in parallel from one written rubric (`SPECIFIC` / `STANDARD` / `NOT_ASSERTION`, plus database and context flag). One pass, no second labeler.
- Two agents numbered their rows 1–396 instead of using the real ids. I remapped them by position and confirmed alignment by comparing each label's reason text with its sentence (word overlap 0.67–0.73, against 0.02 for a shifted control).
- I read 45 random labels myself. I would change 3 (all borderline), about 93% agreement. I wrote the rubric and I am one reviewer, so this is a sanity check, not validation.
- An earlier hand-sort of 30 facts gave a similar split (about a third vague), so the 28% is plausible. The labels are a first filter. Borderline calls should be reviewed by a person before anything is dropped.

## Files

- `triage/triage.jsonl`: one row per claim with label, database, reason, context flag, loose/strict flags, and the earlier Codex label (`codex_verdict`, see `notes/heuristic-codex-pass.md`). Join to `data/cancer/facts.json` on `fact_id`.
