# medhavy-factchecker

Fact checking by **evidence**, not verdicts. Each claim in a textbook is matched to a public database that could confirm or refute it, and the database record (its name, URL and exact passage) is stored as the evidence. A claim's status comes from that evidence. Nobody votes.

This started as a copy of `Medhavy/medhavy-facts` and is being reworked for a paper and a sounder pipeline. It is not connected to that repo.

## Where it stands

Steps 1 to 3 are done for one book (medhavi-cancer). Steps 4 and 5 have run on a 60-claim pilot only. Step 6 (status) is built and runs on whatever evidence exists.

| Step | What | State |
|---|---|---|
| 1. Extract | Pull candidate claims (verbatim sentences) out of the book | done: 3,165 claims in `data/cancer/facts.json` |
| 2. Triage | Decide which claims are real assertions and which database could check each | done: `triage/triage.jsonl` (one model-labeler pass, a first filter) |
| 3. Map and query | Rewrite each assertion as a query for its database | done: `data/cancer/queries.jsonl`, 1,399 queries (model-written, smoke-tested on a sample) |
| 4. Retrieve | Look it up; keep the record | pilot: 60 claims retrieved (`pipeline/04_retrieve.py`); SEER/GLOBOCAN and guideline bodies have no open API and are not in it |
| 5. Store evidence | Database name as `source`, `url`, exact `verbatim`, the query in its own field | pilot: `data/cancer/pilot/evidence.pilot.jsonl`, 77 records; NOT merged into `facts.json` yet |
| 6. Derive status | Status computed from the evidence records | done: `data/cancer/status.jsonl`, all 3,165 claims (only the 60 pilot claims have evidence so far) |

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

## Pilot: steps 4 and 5 on 60 claims

A seeded, stratified sample (`data/cancer/pilot/pilot_ids.json`): 30 PubMed, 14 gene/protein, 8 ClinicalTrials.gov, 8 openFDA. `04_retrieve.py` ran each query and cached the records. Model agents then picked up to two quoted passages per claim (rules: `notes/passage-spec.md`), and `05_build_evidence.py` kept a passage **only if it is an exact substring of the record field it cites**. All 77 offered passages passed; none were fabricated or altered.

| | Claims | Records returned | Got evidence | Status `supported` |
|---|---:|---:|---:|---:|
| PubMed | 30 | 29 | 24 | 8 |
| Gene / protein | 14 | 13 | 10 | 0 |
| ClinicalTrials.gov | 8 | 8 | 6 | 0 |
| openFDA | 8 | 6 | 6 | 3 |
| **All** | **60** | **56** | **46** | **11** |

Result per claim: supported 11, partially supported 29, related only 5, conflicting 1, no evidence found 14 (4 had no records; in 10 the records never state the specific number or relation).

**What the pilot shows**
- **Most evidence is partial, not confirming.** 29 of 46 claims got at best a partial match. Textbook sentences bundle several claims; a database record states one piece of one. A "supported" outcome will be the minority, and the pipeline should say so plainly.
- **Gene records confirm little.** None of 14. NCBI Gene and UniProt summaries are short, and the claims routed there are mostly relations, not properties.
- **One real discrepancy worth a human look:** the book says no dose adjustment is needed with liver impairment for aromatase inhibitors; the letrozole label says to reduce the dose 50% in cirrhosis with severe hepatic dysfunction. It is the pilot's one `conflicting_evidence`.
- **`stance` is a model's reading, not a finding.** It is stored as `stance_by: "model, unreviewed"`. I read about a dozen; two overreached.
- **Not independent.** One pass of model agents; no second reader.

**Two fixes made after the first pilot.** The first pass marked a trial "refuted" because its record now says `COMPLETED` while the book said "is currently being tested", and marked "several trials are underway" as supported by a single trial. Both are wording problems, not evidence problems, so:
1. **Time-bound claims** ("currently", "now approved", "ongoing"): a record that differs only because it shows today's state is `partial` with a "dated:" note, never `refutes`. A claim flagged by `pipeline/claim_flags.py` also has any `refutes` counted as a dated difference in step 6.
2. **Plural claims** ("several", "many", "a number of", "the majority"): one record showing one instance is `partial`. Such a claim needs two different records to reach `supported`.

I re-ran the 12 pilot claims these rules touch: 6 passages across 5 claims changed stance (the AZD3965 "refutes" became partial, "several trials" lost its single-trial "supports"). Both rules are word patterns (129 and 273 of the 3,165 claims are flagged); they miss some claims and over-flag a few. That is the safe direction.

Evidence rows live in `data/cancer/pilot/evidence.pilot.jsonl`; `attempts.jsonl` records every retrieval attempt without third-party text. The raw record text is cached in `data/cancer/pilot/cache/` and is git-ignored (regenerate with `04_retrieve.py`).

## Step 6: status for every claim

`pipeline/06_derive_status.py` writes `data/cancer/status.jsonl`, one row per claim, from the triage, the queries and the evidence. It never says "true". Every row has `human_reviewed: false`.

| Status | Claims | Meaning |
|---|---:|---|
| `not_an_assertion` | 885 | framing, evaluation or vagueness; no record could confirm or refute it |
| `no_record_type` | 799 | a real claim, but no database record type fits |
| `not_queryable` | 82 | a database fits but no stand-alone query could be written |
| `no_open_api` | 227 | queryable, but SEER/GLOBOCAN or a guideline body has no open API |
| `not_yet_checked` | 1,112 | queryable with an open API, not retrieved yet |
| `no_evidence_found` | 14 | retrieved; nothing returned bears on the claim |
| `related_only` | 5 | same topic, no passage states the claim's relation or value |
| `partially_supported` | 29 | a passage supports part of it, a different number or scope, or one record for a plural claim |
| `supported` | 11 | a passage states the claim's relation or value |
| `conflicting_evidence` | 1 | a passage states a conflicting value or relation (needs a human) |
| `dated_evidence` | 0 | a record differs only through today's state of a time-bound claim (needs a human) |

`supported` means a retrieved record contains a passage a model read as stating the claim. It is not a verification and it is not human-reviewed.

`facts.json` is the claim pool as extracted. Its `evidence: []` and `status: "no_evidence"` are extraction-time defaults and are **not updated**; `status.jsonl` and the evidence files are the authoritative state. (Merging evidence back into `facts.json` is still open.)

## The triage in one paragraph

Of the 3,165 candidates, **885 (28%) are not assertions** (framing, evaluation, vagueness no source could support or refute), **799 (25%) are real claims only a general textbook could confirm**, and **1,481 (47%) map to a real database**: PubMed, SEER/GLOBOCAN, FDA, gene and protein databases, guideline bodies, ClinicalTrials.gov. Only the 1,481 go to step 3. PubMed takes 902 of them and is the weakest label, so real query terms are needed before any of it counts as evidence. See `triage/SUMMARY.md`.

## Layout

```
README.md
pipeline/
  01_extract.py              step 1: textbook -> terms.json, graph.json, facts.json (deterministic, no AI)
  03_check_queries.py        step 3: validates queries.jsonl (ids, shapes, one row per strict assertion)
  03b_probe_queries.py       step 3: smoke test, counts hits per query on a sample (network; stores nothing)
  04_retrieve.py             step 4: run queries against PubMed / ClinicalTrials.gov / openFDA / NCBI Gene / UniProt, cache records
  claim_flags.py             two word-pattern flags: time-bound and plural claims
  06_derive_status.py        step 6: status for every claim, derived from the evidence
  05_build_evidence.py       step 5: keep only quoted passages that are exact substrings of the record; write evidence rows
  legacy_migrate_facts.py    one-off: June 2026 medhavy-facts schema -> this schema
data/cancer/
  facts.json                 3,165 candidate claims
  queries.jsonl              step 3: one database query per strict assertion (1,481 rows)
  pilot/                     steps 4-5 on 60 claims: pilot_ids.json, attempts.jsonl, evidence.pilot.jsonl (cache/ is git-ignored)
  status.jsonl               step 6: the derived status of all 3,165 claims (regenerable)
  terms.json  graph.json     glossary (10,055 terms) and concept graph (24,347 edges)
triage/
  SUMMARY.md  triage.jsonl   which claims are real assertions, and which database fits
notes/
  query-spec.md              the rules the query writers followed (query shape per database)
  passage-spec.md            the rules for picking a quoted passage and its stance
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
