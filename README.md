# medhavy-factchecker

Fact checking by **evidence**, not verdicts. Each claim in a textbook is matched to a public database that could confirm or refute it, and the database record (its name, URL and exact passage) is stored as the evidence. A claim's status comes from that evidence. Nobody votes.

This started as a copy of `Medhavy/medhavy-facts` and is being reworked for a paper and a sounder pipeline. It is not connected to that repo.

## Where it stands

All six steps have run for one book (medhavi-cancer), on the 1,170 queryable claims whose database has an open API (PubMed, ClinicalTrials.gov, openFDA, NCBI Gene, UniProt). 229 queryable claims (SEER/GLOBOCAN, guideline bodies, Ensembl) have no open API and are not checked. Nothing is human-reviewed.

| Step | What | State |
|---|---|---|
| 1. Extract | Pull candidate claims (verbatim sentences) out of the book | done: 3,165 claims in `data/cancer/facts.json` |
| 2. Triage | Decide which claims are real assertions and which database could check each | done: `triage/triage.jsonl` (one model-labeler pass, a first filter) |
| 3. Map and query | Rewrite each assertion as a query for its database | done: `data/cancer/queries.jsonl`, 1,399 queries (model-written, smoke-tested on a sample) |
| 4. Retrieve | Look it up; keep the record | done for 1,172 claims: a 60-claim pilot, then the other 1,112 (`pipeline/04_retrieve.py`); SEER/GLOBOCAN, guideline bodies and Ensembl have no open API and are skipped |
| 5. Store evidence | Database name as `source`, `url`, exact `verbatim`, the query in its own field | done: `data/cancer/pilot/evidence.pilot.jsonl` (77) and `data/cancer/full/evidence.jsonl` (1,386 records); merged into `facts.json` by `pipeline/07_merge_into_facts.py` |
| 6. Derive status | Status computed from the evidence records | done: `data/cancer/status.jsonl`, all 3,165 claims |

Nothing here is human-reviewed. In `data/cancer/facts.json` each claim carries the database records found for it (`evidence`) and a `status` derived from them; 2,206 claims have no evidence yet because they are not assertions, have no record type, have no stand-alone query, have no open API, or nothing returned bears on them.

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

## Full run: steps 4 and 5 on the other 1,112 claims

Same method as the pilot, with the two fixes in place. `04_retrieve.py` fetched the top 5 records for each query (0 errors), and 36 model passes picked quoted passages under `notes/passage-spec.md`. `05_build_evidence.py` kept a passage only if it is an exact substring of the record field it cites. All 1,386 offered passages passed; none were dropped.

Together with the pilot (1,172 claims attempted; 1,170 with an open API):

| Database | Claims | Records returned | Supported | Partial | Related only | Conflicting / dated | None found |
|---|---:|---:|---:|---:|---:|---:|---:|
| PubMed | 950 | 945 | 107 | 601 | 83 | 10 | 149 |
| Gene / protein | 146 | 121 | 4 | 76 | 16 | 1 | 49 |
| ClinicalTrials.gov | 20 | 18 | 0 | 13 | 0 | 1 | 6 |
| openFDA | 54 | 47 | 6 | 36 | 4 | 1 | 7 |
| **All** | **1,170** | **1,131** | **117 (10%)** | **726 (62%)** | **103 (9%)** | **13 (1%)** | **211 (18%)** |

These counts are after the strict re-read below. Before it, 339 (29%) were `supported` and 504 (43%) `partially_supported`.

**What it shows**
- **Most claims are only partly confirmed.** One in ten reaches `supported`. Textbook sentences bundle several claims, and a record states one piece of one.
- **Genes and proteins are the weak spot.** 4 of 146 supported, 49 with nothing. Short summaries rarely state the relations the book claims.
- **No database is clean.** Even openFDA, the best, has 6 of 54 that pass the strict reading.
- **"No evidence found" is not "no evidence exists".** It means none of the top-5 records returned bears on the claim. A claim can be well supported in a paper that ranked sixth.
- **"Supported" can be a lucky top-5.** It means a passage that a model read as stating the claim, in a record the database ranked highly. It is not a systematic review.
- **The review queue is now 17 claims** (it was 30 before the strict re-read, which turned 13 of the plural cases into plain `partially_supported`): 12 `conflicting_evidence`, 1 `dated_evidence`, and 4 plural claims where one record shows one instance. See `review/QUEUE.md`. I read all of the conflicts. Each is one study or record pointing the other way, usually in a narrower setting (one cell line, one glioma series, one New York study), with a few opposite-direction findings (Hedgehog inhibition inducing autophagy, gamma-secretase inhibition reducing oxaliplatin-induced apoptosis). So `conflicting_evidence` means "a person should look", not "the book is wrong"; several should have been `partial`.
- **Audit, first look.** I read 8 random `supported` rows and 6 that a crude number check flagged. They held up on numbers, but that sample was too small to catch the bigger problem below.

### Strict re-read (step 5b)

A second hand check of 24 random `supports` quotes found 9 where the quote covered only one clause of a multi-part claim (e.g. "adverse effects that *restrict clinical application*" matched by "adverse effects have been reported"). So `pipeline/05b_strict_recheck.py` re-read all 496 `supports` quotes under a strict rule: keep only if the quote, read by itself, states every substantive part of the claim. Five model readers, each given about 100 quotes, could only keep or downgrade to `partial`. **361 were downgraded, 135 kept.**

- The original label stays on every row as `stance_original`; the missing part is added to `stance_note`; all 496 verdicts are in `data/cancer/strict_recheck.jsonl`. Nothing is lost and it can be reversed.
- Calibration on my 24: the strict readers downgraded all 9 I had called loose, and also 7 of the 15 I had called clean. Several of those 7 are nitpicks (e.g. a quote about CDK4/6 that never writes the name "CDK6"). So the strict pass errs on the cautious side. `supported` now means "the quote states all of it"; `partially_supported` includes many claims that are fine in substance.
- It is still a model reading and unreviewed by a person.

Evidence for these claims is in `data/cancer/full/evidence.jsonl`, with `attempts.jsonl` (one row per retrieval, no third-party text) and `ids.json`. The raw record text (9 MB) is cached in `data/cancer/full/cache/` and is git-ignored.

## Step 6: status for every claim

`pipeline/06_derive_status.py` writes `data/cancer/status.jsonl`, one row per claim, from the triage, the queries and the evidence. It never says "true". Every row has `human_reviewed: false`.

| Status | Claims | Meaning |
|---|---:|---|
| `not_an_assertion` | 885 | framing, evaluation or vagueness; no record could confirm or refute it |
| `no_record_type` | 799 | a real claim, but no database record type fits |
| `not_queryable` | 82 | a database fits but no stand-alone query could be written |
| `no_open_api` | 229 | queryable, but SEER/GLOBOCAN, a guideline body or Ensembl has no open API |
| `no_evidence_found` | 211 | retrieved; nothing returned bears on the claim |
| `related_only` | 103 | same topic, no passage states the claim's relation or value |
| `partially_supported` | 726 | a passage supports part of it, a different number or scope, or one record for a plural claim |
| `supported` | 117 | a passage states the claim's relation or value |
| `conflicting_evidence` | 12 | a passage states a conflicting value or relation (needs a human) |
| `dated_evidence` | 1 | a record differs only through today's state of a time-bound claim (needs a human) |

`supported` means a retrieved record contains a passage a model read as stating the claim. It is not a verification and it is not human-reviewed.

`facts.json` is the single record of a claim: where the book said it, the evidence found, and the status. `pipeline/07_merge_into_facts.py` rebuilds its `evidence`, `status` and `status_detail` from the evidence files and `status.jsonl` on every run (it never changes `fact_id`, `canonical`, `claim_origin` or the other claim fields, and asserts so). `status.jsonl` stays as a flat table of the same statuses, easy to count and filter.

## Human review

The 17 claims step 6 flagged are in `review/QUEUE.md`: each shows the book's claim and where it appears, the quoted evidence with a link to each record, and one question with a fixed set of answers (`pipeline/review_vocab.py`). A reviewer records an answer in `review/decisions.jsonl` (`decision`, `reviewer`, `date`, optional `note`), then runs `06_derive_status.py` and `07_merge_into_facts.py`.

A decision is attached to the claim as `status_detail.human_review` and sets `human_reviewed: true`. **It does not change the evidence or the derived status**: the status says what the records show, and the decision says what a person made of it. That keeps "a model read this" and "a person checked this" countable separately. `06` rejects an answer that is not on the list, and a decision without a reviewer and date. Rebuilding the queue (`08_build_review_queue.py`) never overwrites a decision.

Nobody has reviewed anything yet: 0 of 17 decided.

## Wording changes

Where a book sentence is stronger than its evidence ("binds *exclusively* to...", "is apparently..."), the fix is usually looser wording, not a verdict. `changes/changes.jsonl` holds one row per proposed rewording: the book's sentence, the proposed one, the kind (`remove_absolute`, `hedge`, `scope`, `attribute`, `update`; `pipeline/changes_vocab.py`), the reason, the database quotes behind it, and who proposed and who decided. `pipeline/10_check_changes.py` checks that the original is the book's sentence character for character and that every quote is already stored on the claim, then writes `changes/CHANGES.md`. Step 7 adds them to the claim as `revisions`.

The book's own sentence is never edited. A change starts as `proposed` (a model's suggestion) and only becomes `approved` when a person says so. Four are proposed so far (the first four conflicts); none is approved. A rewording is a separate record from a review decision (`review/decisions.jsonl`): the decision says how the evidence relates to the claim as written; the change says what we would write instead.

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
  07_merge_into_facts.py     step 7: write evidence and status into facts.json (idempotent)
  08_build_review_queue.py   builds review/QUEUE.md and review/decisions.jsonl for the claims step 6 flagged
  review_vocab.py            the three kinds of review case and the answers allowed for each
  05_build_evidence.py       step 5: keep only quoted passages that are exact substrings of the record; write evidence rows
  05b_strict_recheck.py      step 5b: apply the strict re-read (supports -> partial only); keeps stance_original
  10_check_changes.py        validates changes/changes.jsonl, writes changes/CHANGES.md; step 7 attaches them as `revisions`
  09_build_report.py         writes REPORT.md, the plain-words summary, from facts.json
  legacy_migrate_facts.py    one-off: June 2026 medhavy-facts schema -> this schema
data/cancer/
  facts.json                 3,165 claims: claim_origin + evidence + status (step 7 merges the last two in)
  queries.jsonl              step 3: one database query per strict assertion (1,481 rows)
  pilot/                     steps 4-5 on 60 claims: pilot_ids.json, attempts.jsonl, evidence.pilot.jsonl (cache/ is git-ignored)
  full/                      steps 4-5 on the other 1,112: ids.json, attempts.jsonl, evidence.jsonl (cache/ is git-ignored)
  strict_recheck.jsonl      step 5b: the 496 strict verdicts (keep / partial + what was missing)
  status.jsonl               step 6: the derived status of all 3,165 claims (regenerable)
  terms.json  graph.json     glossary (10,055 terms) and concept graph (24,347 edges)
review/
  QUEUE.md                   the 17 flagged claims: book's claim, quoted evidence, record links, the question to answer
  decisions.jsonl            one row per queued claim; a reviewer fills in decision / reviewer / date / note
triage/
  SUMMARY.md  triage.jsonl   which claims are real assertions, and which database fits
notes/
  query-spec.md              the rules the query writers followed (query shape per database)
  passage-spec.md            the rules for picking a quoted passage and its stance
  heuristic-codex-pass.md    why the earlier Codex "fact-check" was removed, and where it is in git
  slice-stats-2026-06.md     counts for the June extraction (terms, graph, claims by chapter, images)
```

## A claim record

A real record from `data/cancer/facts.json` (the `query` URL is shortened here, and a second evidence row is omitted):

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
  "evidence": [
    {
      "source": "PubMed", "database": "pubmed", "record_id": "PMID:8400344",
      "url": "https://pubmed.ncbi.nlm.nih.gov/8400344/",
      "title": "Immunological quantitation of thymidylate synthase-FdUMP-5,10-methylenetetrahydrofolate ternary complex with the monoclonal antibody TS 106.",
      "field": "abstract",
      "verbatim": "One of the principal mechanisms of action of 5-fluorouracil (5-FU) is the inhibition of TS by formation of a ternary covalent complex consisting of TS-5-fluorodeoxyuridylate-5,10-methylenetetrahydrofolate.",
      "retrieved": "2026-11-02",
      "query": "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term=...&retmax=5&sort=relevance&retmode=json",
      "effective_query": "(\"Fluorouracil\"[MeSH Terms] OR 5-FU[tiab]) AND (\"Thymidylate Synthase\"[MeSH Terms] OR \"thymidine synthetase\"[tiab]) AND (FdUMP[tiab] OR metabolite[tiab])",
      "relaxed": 0,
      "stance": "supports",
      "stance_note": "States covalent ternary complex of TS with FdUMP and folate forms during 5-FU action.",
      "stance_by": "model, unreviewed"
    }
  ],
  "status": "supported",
  "status_detail": {
    "database": "pubmed", "n_records": 1, "n_supports": 1, "n_partial": 0, "n_related": 0,
    "n_refutes": 0, "n_dated": 0, "sources": ["PubMed"],
    "flags": {"time_sensitive": false, "plural": false},
    "needs_review": false, "review_reasons": [], "human_reviewed": false
  }
}
```

- `claim_origin` is where the **book** made the claim. It is provenance of the claim, not evidence for it: a book cannot vouch for itself. (The old schema stored this as `evidence[0]` with `verdict: SUPPORTS` and tier `trusted`; that was circular and is gone.)
- `evidence` holds database records only. Each row has the database name as `source`, the record's `url`, the exact `verbatim` passage (always a character-for-character copy of the cited record field), the request that found it (`query`, `effective_query`, `relaxed`), and a `stance`.
- `stance` (supports / partial / related / refutes) is a model's reading of how the passage relates to the claim, stored as `stance_by: "model, unreviewed"`. The record, URL and quote are the evidence; the stance is not.
- `status` is derived from the evidence rows (step 6). It never says "true".
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
