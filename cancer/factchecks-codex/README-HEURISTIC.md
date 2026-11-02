# Read this first: the Codex pass is heuristic triage, not fact-checking

`generate_codex_verdicts.py` assigns every row from regexes over the claim text. It never consulted a source.

| Field | Value across all 3,165 rows |
|---|---|
| `url` | empty |
| `verbatim` (quoted passage) | empty |
| `source` | `model-knowledge` (2,607) or `not-located` (558) |
| `tier` | `low` |

- **PLAUSIBLE** (was CONFIRMED, 2,562 rows): the sentence matched no suspicious pattern. It is *not* evidence the claim is true.
- **NOT CHECKED** (was UNVERIFIED, 603 rows): statistics, guidelines, approvals, named evidence or specialist claims that still need a database lookup.
- The rules never produce CONTRADICTED or OUTDATED.
- 2,010 rows share one canned sentence as their "finding".
- About 31% of the PLAUSIBLE rows are not assertions at all (see `../../assertion-triage/SUMMARY.md`).

The data file was renamed `verdicts-codex.jsonl` -> `heuristic-triage-codex.jsonl` (no longer matched by `merge_verdicts.py`'s `factchecks-*/verdicts-*.jsonl` glob), so these rows cannot be counted as a checker's vote or recorded into the shared dictionary. The old verdict is kept in each row as `original_verdict`.

Re-running `generate_codex_verdicts.py` regenerates the old labels; run `relabel_as_heuristic.py` afterwards.
