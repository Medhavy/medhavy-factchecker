# The earlier Codex pass was heuristic triage, not fact-checking

This repo started as a copy of `Medhavy/medhavy-facts`. That repo held a "Codex fact-check" of all 3,165 candidate claims. It has been removed from the working tree. This note says why, and where to find it.

## What it was

`generate_codex_verdicts.py` assigned every row from regexes over the claim text. It never consulted a source.

| Field | Value across all 3,165 rows |
|---|---|
| `url` | empty |
| `verbatim` (quoted passage) | empty |
| `source` | `model-knowledge` (2,607) or `not-located` (558) |
| `tier` | `low` |

- **CONFIRMED** (2,562 rows) meant the sentence matched no suspicious pattern. It was not evidence the claim is true.
- **UNVERIFIED** (603 rows) meant a statistic, guideline, approval, named study or specialist claim that still needed a database lookup.
- The rules never produced CONTRADICTED or OUTDATED.
- 2,010 rows shared one canned sentence as their "finding".
- About 31% of the CONFIRMED rows were not assertions at all (see `triage/SUMMARY.md`).

## Why it was dropped

This project judges a claim by evidence: a database record, its URL, the exact passage. The Codex pass produced none, and its labels would have been read as verdicts. The same goes for the Claude and Codex fact-check prompts and for `merge_verdicts.py`, which counted checker votes. The new pipeline has no checkers voting; a claim's status comes from the evidence records attached to it.

## Where it is

Nothing was lost. It is in this repo's git history:

| Commit | What it holds |
|---|---|
| `2a61bb2` | the repo exactly as `medhavy-facts` left it (verdict files, prompts, `merge_verdicts.py`) |
| `0e2158d` | the same output relabelled as heuristic triage (`PLAUSIBLE` / `NOT_CHECKED`), with `heuristic-triage-codex.jsonl`, a banner on each report, and `relabel_as_heuristic.py` |

To read it: `git show 0e2158d:cancer/factchecks-codex/MASTER_REPORT.md`.

The per-claim comparison of Codex's labels against the assertion triage is still in `triage/triage.jsonl` (the `codex_verdict` column).
