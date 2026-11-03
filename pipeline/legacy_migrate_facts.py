#!/usr/bin/env python3
"""One-off: convert the June 2026 medhavy-facts `facts.json` (vote/verdict schema) to the
evidence-first schema used here. Kept so the conversion can be audited and repeated.

  old: evidence[0] = the book citing itself, verdict SUPPORTS, tier "trusted",
       plus consensus / votes / same_publisher / needs_review / verified* / books / expires
  new: claim_origin = that same citation (module, url, verbatim, retrieved) — provenance of the claim
       evidence     = []   (database records only, added by later steps)
       status       = "no_evidence"

Dropped on purpose: verdict (a textbook cannot support itself), tier (set per database, not per book),
and the vote/consensus fields (status is derived from evidence records, not counted votes).
fact_id, canonical, domain, stable and category are copied unchanged.

WARNING: the default output is data/cancer/facts.json, which now also holds merged evidence and status. This script
writes EMPTY evidence; if you overwrite facts.json, run 06_derive_status.py and 07_merge_into_facts.py afterwards.

Usage:  python3 pipeline/legacy_migrate_facts.py OLD_FACTS.json [OUT.json]
        old file: git show 2a61bb2:cancer/facts.json   (the last medhavy-facts commit)
"""
import json, sys
from pathlib import Path

src = Path(sys.argv[1])
out = Path(sys.argv[2]) if len(sys.argv) > 2 else Path(__file__).resolve().parents[1] / "data/cancer/facts.json"
old = json.loads(src.read_text(encoding="utf-8"))

new = []
for f in old:
    assert len(f["evidence"]) == 1 and f["evidence"][0].get("source") == "medhavi-cancer", f["fact_id"]
    e = f["evidence"][0]
    new.append({
        "fact_id": f["fact_id"],
        "canonical": f["canonical"],
        "domain": f["domain"],
        "stable": f["stable"],
        "category": f["category"],
        "claim_origin": {"source": e["source"], "publisher": e["publisher"], "book": e["book"],
                         "module": e["module"], "url": e["url"],
                         "verbatim": e["verbatim"], "retrieved": e["retrieved"]},
        "evidence": [],
        "status": "no_evidence",
    })
assert len({f["fact_id"] for f in new}) == len(new) == len(old)
out.write_text(json.dumps(new, indent=2, ensure_ascii=False), encoding="utf-8")
print(f"{len(new)} claims -> {out}")
