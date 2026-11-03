#!/usr/bin/env python3
"""03_check_queries.py — check data/cancer/queries.jsonl before anything is sent to a database.

Checks (exit 1 on any failure):
  - exactly one row per strict assertion in triage/triage.jsonl, same fact_ids, none extra, none twice
  - every fact_id exists in data/cancer/facts.json
  - required keys present; database / database_final from the allowed set
  - queryable rows have a `query` object with the keys its database needs, a non-empty query_text,
    1-5 entities, and a `check` sentence; unqueryable rows have a reason and query null
  - the query does not contain a number that appears in the claim's `check` only (the asserted value
    belongs in `check`, never in the lookup)  -- reported as a warning count, not a failure

Usage:  python3 pipeline/03_check_queries.py [queries.jsonl]
"""
import json, re, sys
from collections import Counter
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
Q = Path(sys.argv[1]) if len(sys.argv) > 1 else REPO / "data/cancer/queries.jsonl"
DBS = {"pubmed", "clinicaltrials", "fda", "gene-protein-db", "seer-globocan", "guideline-body"}
FINAL = DBS | {"none"}
REQ = {"fact_id", "database", "database_final", "claim_standalone", "queryable", "unqueryable_reason",
       "entities", "check", "query", "query_text", "notes"}
SHAPE = {
    "pubmed": {"term", "article_types"},
    "clinicaltrials": {"query.term", "query.cond", "query.intr", "query.titles"},
    "fda": {"endpoint", "search", "field_to_read"},
    "gene-protein-db": {"database", "symbol", "organism", "field_to_read"},
    "seer-globocan": {"dataset", "cancer_site", "measure", "population", "year"},
    "guideline-body": {"body", "topic", "cancer_site", "access"},
}
REASONS = {"needs_context", "no_record_type", "too_vague"}

rows = [json.loads(l) for l in Q.read_text(encoding="utf-8").splitlines() if l.strip()]
strict = [json.loads(l)["fact_id"] for l in (REPO / "triage/triage.jsonl").read_text(encoding="utf-8").splitlines()
          if l.strip() and json.loads(l)["strict_assertion"]]
facts = {f["fact_id"] for f in json.load(open(REPO / "data/cancer/facts.json", encoding="utf-8"))}

errs = []
ids = [r.get("fact_id") for r in rows]
if len(ids) != len(set(ids)): errs.append(f"duplicate fact_ids: {len(ids) - len(set(ids))}")
if set(ids) != set(strict): errs.append(f"ids differ from strict set: missing {len(set(strict) - set(ids))}, extra {len(set(ids) - set(strict))}")
if not set(ids) <= facts: errs.append("fact_ids not in facts.json")
warn = Counter()
for r in rows:
    i = r.get("fact_id", "?")
    miss = REQ - set(r)
    if miss: errs.append(f"{i}: missing keys {sorted(miss)}"); continue
    if r["database"] not in DBS: errs.append(f"{i}: bad database {r['database']}")
    if r["database_final"] not in FINAL: errs.append(f"{i}: bad database_final {r['database_final']}")
    if not isinstance(r["queryable"], bool): errs.append(f"{i}: queryable not bool"); continue
    if r["queryable"]:
        if r["database_final"] == "none": errs.append(f"{i}: queryable but database_final none")
        elif not isinstance(r["query"], dict) or set(r["query"]) != SHAPE[r["database_final"]]:
            errs.append(f"{i}: query keys {sorted(r['query'] or [])} != {sorted(SHAPE[r['database_final']])}")
        if not (isinstance(r["query_text"], str) and r["query_text"].strip()): errs.append(f"{i}: empty query_text")
        if not (isinstance(r["entities"], list) and 1 <= len(r["entities"]) <= 5): errs.append(f"{i}: entities not 1-5")
        if not (isinstance(r["check"], str) and r["check"].strip()): errs.append(f"{i}: empty check")
        if r["unqueryable_reason"] is not None: errs.append(f"{i}: reason set on queryable row")
        # asserted numbers belong in `check`, not in the lookup
        qt = json.dumps(r["query"]) if r["query"] else ""
        nums = set(re.findall(r"\d+(?:\.\d+)?", r["check"]))
        if any(re.search(rf"(?<![\w.]){re.escape(n)}(?![\w.])", qt) for n in nums if len(n) > 1):
            warn["number from `check` also in query"] += 1
    else:
        if r["unqueryable_reason"] not in REASONS: errs.append(f"{i}: bad reason {r['unqueryable_reason']}")
        if r["query"] is not None or r["query_text"] is not None: errs.append(f"{i}: unqueryable row has a query")

print(f"{len(rows)} rows | queryable {sum(r['queryable'] for r in rows)} | "
      f"database changed {sum(r['database'] != r['database_final'] for r in rows)}")
print("by database_final:", dict(Counter(r["database_final"] for r in rows)))
print("unqueryable reasons:", dict(Counter(r["unqueryable_reason"] for r in rows if not r["queryable"])))
for k, v in warn.items(): print(f"warning: {v} rows — {k}")
if errs:
    print(f"\n{len(errs)} ERRORS"); print("\n".join(errs[:30])); sys.exit(1)
print("OK")
