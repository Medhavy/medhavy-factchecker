# medhavy-factchecker

Fact checking by **evidence**, not verdicts. Each claim in a textbook is matched to a public database that could confirm or refute it, and the database record (its name, URL and exact passage) is stored as the evidence. A claim's status comes from that evidence. Nobody votes.

This started as a copy of `Medhavy/medhavy-facts` and is being reworked for a paper and a sounder pipeline. It is not connected to that repo.

## Where it stands

Steps 1 and 2 are done for one book (medhavi-cancer). Steps 3 to 6 are not built yet.

| Step | What | State |
|---|---|---|
| 1. Extract | Pull candidate claims (verbatim sentences) out of the book | done: 3,165 claims in `data/cancer/facts.json` |
| 2. Triage | Decide which claims are real assertions and which database could check each | done: `triage/triage.jsonl` (one model-labeler pass, a first filter) |
| 3. Map and query | Rewrite each assertion as a query for its database | not built |
| 4. Retrieve | Look it up; keep the record | not built |
| 5. Store evidence | Database name as `source`, `url`, exact `verbatim`, the query in its own field | not built |
| 6. Derive status | Status computed from the evidence records | not built |

Nothing here is verified. Every claim has `evidence: []` and `status: "no_evidence"`.

## The triage in one paragraph

Of the 3,165 candidates, **885 (28%) are not assertions** (framing, evaluation, vagueness no source could support or refute), **799 (25%) are real claims only a general textbook could confirm**, and **1,481 (47%) map to a real database**: PubMed, SEER/GLOBOCAN, FDA, gene and protein databases, guideline bodies, ClinicalTrials.gov. Only the 1,481 go to step 3. PubMed takes 902 of them and is the weakest label, so real query terms are needed before any of it counts as evidence. See `triage/SUMMARY.md`.

## Layout

```
README.md
pipeline/
  01_extract.py              step 1: textbook -> terms.json, graph.json, facts.json (deterministic, no AI)
  legacy_migrate_facts.py    one-off: June 2026 medhavy-facts schema -> this schema
data/cancer/
  facts.json                 3,165 candidate claims
  terms.json  graph.json     glossary (10,055 terms) and concept graph (24,347 edges)
triage/
  SUMMARY.md  triage.jsonl   which claims are real assertions, and which database fits
notes/
  heuristic-codex-pass.md    why the earlier Codex "fact-check" was removed, and where it is in git
  slice-stats-2026-06.md     counts for the June extraction (terms, graph, claims by chapter, images)
```

## A claim record

```json
{
  "fact_id": "cancer-5-fus-active-metabolite-forms-a-stable-covalent-complex-with-thymidine-sy",
  "canonical": "5-FU's active metabolite forms a stable covalent complex with thymidine synthetase.",
  "domain": ["cancer", "chapter22"],
  "stable": true,
  "category": "BASIC",
  "claim_origin": {
    "source": "medhavi-cancer", "publisher": "medhavi", "book": "medhavi-cancer",
    "module": "22.2 Classes of Chemotherapeutic Agents", "url": "/docs/Chapter22/2_Classes_of_Chemotherapeutic_Agents",
    "verbatim": "5-FU's active metabolite forms a stable covalent complex with thymidine synthetase.",
    "retrieved": "2026-06-30"
  },
  "evidence": [],
  "status": "no_evidence"
}
```

- `claim_origin` is where the **book** made the claim. It is provenance of the claim, not evidence for it: a book cannot vouch for itself. (The old schema stored this as `evidence[0]` with `verdict: SUPPORTS` and tier `trusted`; that was circular and is gone.)
- `evidence` holds database records only. Each will carry the database name as `source`, a `url`, the exact `verbatim` passage, and the rewritten query in a separate field.
- `fact_id` and `canonical` never change. Everything else joins to them.
- `triage/triage.jsonl` joins to `facts.json` on `fact_id`.

## Running step 1

```bash
python3 pipeline/01_extract.py ../medhavi-cancer
```

It needs a `medhavi-cancer` checkout (`content/docs/**/*.mdx` and `data/keywords.json`) and nothing else. **Do not expect it to reproduce `data/cancer/` today.** The local book has changed since June (its glossary lost its definitions), so a fresh run gives different numbers. The committed data is the June extraction, converted with `legacy_migrate_facts.py`.

## What changed from medhavy-facts

| Kept | Why |
|---|---|
| the extractor, `facts.json`, `terms.json`, `graph.json` | the candidate pool, with stable ids and the book's own wording |
| the triage | decides what is worth sending to a database |
| the textbook citation, as `claim_origin` | provenance of the claim, kept apart from evidence |

| Dropped | Why |
|---|---|
| the Codex output (287 section reports, master report, data file) | rule-based labels with no sources; see `notes/heuristic-codex-pass.md` |
| the Claude and Codex fact-check prompts | they ask each checker for a verdict |
| `merge_verdicts.py` and the consensus / vote fields | they count checker votes; status is now derived from evidence |
| matching against the shared 253-fact dictionary | 0 matches; it belonged to the vote model |
| `tier: trusted` on the book's own citation | a book's tier says nothing about a database |

Git history keeps all of it: `git show 2a61bb2` is the repo as it was inherited.
