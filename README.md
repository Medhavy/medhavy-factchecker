# medhavy-factchecker

Fact checking by **evidence**, not verdicts. Each claim in a textbook is matched to a public database that could confirm or refute it, and the database record (its name, URL and exact passage) is stored as the evidence. A claim's status comes from that evidence. Nobody votes.

This started as a copy of `Medhavy/medhavy-facts` and is being reworked for a paper and a sounder pipeline. It is not connected to that repo.

## Where it stands

Steps 1 to 3 are done for one book (medhavi-cancer). Steps 4 to 6 are not built yet.

| Step | What | State |
|---|---|---|
| 1. Extract | Pull candidate claims (verbatim sentences) out of the book | done: 3,165 claims in `data/cancer/facts.json` |
| 2. Triage | Decide which claims are real assertions and which database could check each | done: `triage/triage.jsonl` (one model-labeler pass, a first filter) |
| 3. Map and query | Rewrite each assertion as a query for its database | done: `data/cancer/queries.jsonl`, 1,399 queries (model-written, smoke-tested on a sample) |
| 4. Retrieve | Look it up; keep the record | not built |
| 5. Store evidence | Database name as `source`, `url`, exact `verbatim`, the query in its own field | not built |
| 6. Derive status | Status computed from the evidence records | not built |

Nothing here is verified. Every claim has `evidence: []` and `status: "no_evidence"`.

## Step 3 in numbers

One query row for each of the 1,481 strict assertions (`data/cancer/queries.jsonl`, joined on `fact_id`). The rules the writers followed are in `notes/query-spec.md`; `pipeline/03_check_queries.py` checks ids and shapes (it passes).

| | Rows |
|---|---:|
| usable query | 1,399 |
| not queryable: needs context (a "this tumor" with no referent) | 44 |
| not queryable: no record type fits | 34 |
| not queryable: too vague | 4 |

Where the queries go (`database_final`): PubMed 972, NCBI Gene / UniProt / Ensembl 151, guideline bodies 148, SEER / GLOBOCAN 97, FDA 57, ClinicalTrials.gov 20, none 36.

- **The query writers disagreed with the triage on 113 rows (7.6%).** The biggest moves: 29 SEER/GLOBOCAN to PubMed, 27 FDA to none (mostly descriptions of the approval process, not records), 18 gene to PubMed (relations and frequencies no gene record holds), 14 FDA to PubMed. So the triage over-labelled FDA and SEER; the triage's database label is a first guess, not a fact.
- **Smoke test** (`pipeline/03b_probe_queries.py`; counts only, nothing stored): of 60 sampled PubMed queries, 39 returned 10 to 2,000 hits, 13 returned 1 to 9, 6 returned over 2,000, and 2 returned none. ClinicalTrials.gov: 18 of 20 returned hits. openFDA: 17 of 20. NCBI Gene symbol lookup: 19 of 20. Samples are small, so read these as rough rates, not measurements.
- **Known weak spots for step 4.** Some PubMed queries have too many AND terms and return 0 (relax and retry). openFDA generic names with a salt or qualifier ("sorafenib tosylate", "BCG live") returned 0. A gene "symbol" that is really a family ("CDK family") returns 0. 44 rows have a number from the `check` sentence also in the query; a few queries carry a name or direction from the claim (for example an author's name), which tilts the search toward confirming. 
- **Not independent.** The queries were written by model agents in one pass and I read about a dozen. The same caveat as the triage applies.

## The triage in one paragraph

Of the 3,165 candidates, **885 (28%) are not assertions** (framing, evaluation, vagueness no source could support or refute), **799 (25%) are real claims only a general textbook could confirm**, and **1,481 (47%) map to a real database**: PubMed, SEER/GLOBOCAN, FDA, gene and protein databases, guideline bodies, ClinicalTrials.gov. Only the 1,481 go to step 3. PubMed takes 902 of them and is the weakest label, so real query terms are needed before any of it counts as evidence. See `triage/SUMMARY.md`.

## Layout

```
README.md
pipeline/
  01_extract.py              step 1: textbook -> terms.json, graph.json, facts.json (deterministic, no AI)
  03_check_queries.py        step 3: validates queries.jsonl (ids, shapes, one row per strict assertion)
  03b_probe_queries.py       step 3: smoke test, counts hits per query on a sample (network; stores nothing)
  legacy_migrate_facts.py    one-off: June 2026 medhavy-facts schema -> this schema
data/cancer/
  facts.json                 3,165 candidate claims
  queries.jsonl              step 3: one database query per strict assertion (1,481 rows)
  terms.json  graph.json     glossary (10,055 terms) and concept graph (24,347 edges)
triage/
  SUMMARY.md  triage.jsonl   which claims are real assertions, and which database fits
notes/
  query-spec.md              the rules the query writers followed (query shape per database)
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
