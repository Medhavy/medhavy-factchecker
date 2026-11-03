#!/usr/bin/env python3
"""05_build_evidence.py — turn retrieved records + selected passages into evidence records.

Inputs
  data/cancer/pilot/cache/retrieved.jsonl   step 4 output (record text, exact request, date)
  a passages file (JSON Lines): per claim, up to 2 passages chosen by a model from the retrieved text
      {"fact_id", "passages": [{"record_id","field","verbatim","stance","note"}], "none_reason"}

The guard: a passage becomes evidence ONLY if its `verbatim` is an exact substring of the named field of the
named record (whitespace-collapsed). Anything else is discarded and counted. So every quoted passage can be found,
character for character, in the database record it cites.

Output  data/cancer/pilot/evidence.pilot.jsonl — one row per evidence record:
  fact_id, source (database name), database, record_id, url, title, field, verbatim, retrieved,
  query (exact request URL), effective_query, relaxed, stance, stance_note, stance_by
`stance` is a MODEL's reading of how the passage relates to the claim (supports / refutes / partial / related).
It is not a verdict on the claim and it is unreviewed; the record, url and verbatim are the evidence.
facts.json is NOT modified here (the pilot is kept apart until the shape is agreed).

Also writes data/cancer/pilot/attempts.jsonl (one row per retrieval attempt, no third-party text).
Usage:  python3 pipeline/05_build_evidence.py [--dir full] PASSAGES.jsonl [PASSAGES2.jsonl ...]
        If a claim appears in more than one file, the LAST file wins (use this to re-run a few claims).
"""
import json, re, sys, collections
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
import argparse
_ap = argparse.ArgumentParser()
_ap.add_argument("--dir", default="pilot", help="batch folder under data/cancer/ (default: pilot)")
_ap.add_argument("passages", nargs="+")
_a = _ap.parse_args()
PILOT = REPO / "data/cancer" / _a.dir
STANCES = {"supports", "refutes", "partial", "related"}
NAMES = {"pubmed": "PubMed", "clinicaltrials": "ClinicalTrials.gov", "fda": "openFDA"}


def norm(s):
    return re.sub(r"\s+", " ", s or "").strip()


def source_name(db, record_id):
    if db == "gene-protein-db":
        return "UniProt" if str(record_id).startswith("UniProt") else "NCBI Gene"
    return NAMES[db]


ret = {}
for l in (PILOT / "cache/retrieved.jsonl").read_text(encoding="utf-8").splitlines():
    if l.strip():
        r = json.loads(l); ret[r["fact_id"]] = r

sel = {}
for p in _a.passages:
    for l in Path(p).read_text(encoding="utf-8").splitlines():
        if l.strip():
            r = json.loads(l); sel[r["fact_id"]] = r      # a later file overrides an earlier one (re-runs)

stats = collections.Counter()
rows = []
if set(sel) != set(ret):
    sys.exit(f"claims differ: retrieved {len(ret)}, selected {len(sel)}, missing {len(set(ret) - set(sel))}")
for fid, s in sel.items():
    r = ret[fid]
    recs = {x["record_id"]: x for x in r["records"]}
    kept = 0
    for ps in s.get("passages", []):
        stats["passages offered"] += 1
        rec = recs.get(ps.get("record_id"))
        text = norm(rec["fields"].get(ps.get("field"), "")) if rec else ""
        v = norm(ps.get("verbatim"))
        if not rec: stats["dropped: record not in retrieved set"] += 1; continue
        if not v or v not in text: stats["dropped: not an exact substring"] += 1; continue
        if ps.get("stance") not in STANCES: stats["dropped: bad stance"] += 1; continue
        rows.append({"fact_id": fid, "source": source_name(r["database"], rec["record_id"]), "database": r["database"],
                     "record_id": rec["record_id"], "url": rec["url"], "title": rec["title"], "field": ps["field"],
                     "verbatim": v, "retrieved": r["retrieved"], "query": r.get("request"),
                     "effective_query": r.get("effective_query"), "relaxed": r.get("relaxed", 0),
                     "stance": ps["stance"], "stance_note": norm(ps.get("note")), "stance_by": "model, unreviewed"})
        kept += 1
    stats["claims with evidence" if kept else "claims without evidence"] += 1

# attempts.jsonl: one row per retrieval attempt, no third-party text (safe to commit). Step 6 uses it to tell
# "searched, nothing bore on the claim" from "never searched".
with open(PILOT / "attempts.jsonl", "w", encoding="utf-8") as f:
    for fid, r in ret.items():
        f.write(json.dumps({"fact_id": fid, "database": r["database"], "retrieved": r["retrieved"],
                            "request": r.get("request"), "effective_query": r.get("effective_query"),
                            "relaxed": r.get("relaxed", 0), "total_hits": r.get("total_hits"),
                            "records_returned": len(r["records"]), "error": r.get("error"), "skipped": r.get("skipped")}, ensure_ascii=False) + "\n")

out = PILOT / ("evidence.pilot.jsonl" if _a.dir == "pilot" else "evidence.jsonl")
out.write_text("".join(json.dumps(x, ensure_ascii=False) + "\n" for x in rows), encoding="utf-8")
print(f"{len(rows)} evidence records for {stats['claims with evidence']} of {len(sel)} claims -> {out}")
for k, v in stats.items(): print(f"  {k}: {v}")
print("  stance:", dict(collections.Counter(x["stance"] for x in rows)))
print("  by source:", dict(collections.Counter(x["source"] for x in rows)))
