#!/usr/bin/env python3
"""11_implement_changes.py — apply the accepted wording changes. Run this once a reviewer has been through the sheet.

Reads   changes/resolved.jsonl (written by 10_check_changes.py), data/cancer/facts.json
Writes  data/cancer/claims_current.jsonl   every claim with the wording we now stand behind:
            {fact_id, module, text, revised, change_id, original}
            `text` is the accepted wording where a change was accepted, otherwise the book's own sentence unchanged.
        changes/book_patch.jsonl           the accepted changes only, as edits for whoever maintains the book text:
            {change_id, module, original, revised, kind, why, reviewed_by, reviewed_on}

Implemented means: accepted rewordings become the current wording in the claim set and are listed as a patch.
It never edits the book's source files, `canonical` or `claim_origin`, and it never applies a change that is
`proposed` or `rejected`. Safe to re-run; the outputs are rebuilt from the decisions every time.

Usage: python3 pipeline/11_implement_changes.py
"""
import collections, json
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]


def jl(p):
    p = Path(p)
    return [json.loads(l) for l in p.read_text(encoding="utf-8").splitlines() if l.strip()] if p.exists() else []


facts = json.loads((REPO / "data/cancer/facts.json").read_text(encoding="utf-8"))
res = jl(REPO / "changes/resolved.jsonl")
pending = [r for r in res if r["status"] in ("proposed", "disputed")]
acc = {}
for r in res:
    if r["status"] in ("accepted", "accepted_edited"):
        assert r["final"] and r["decided_by"] and r["decided_date"], r["change_id"]
        assert r["fact_id"] not in acc, f"two accepted changes for one claim: {r['fact_id']}"
        acc[r["fact_id"]] = r

rows = []
for f in facts:
    c = acc.get(f["fact_id"])
    rows.append({"fact_id": f["fact_id"], "module": f["claim_origin"]["module"],
                 "text": c["final"] if c else f["canonical"], "revised": bool(c),
                 "change_id": c["change_id"] if c else None, "original": f["canonical"]})
(REPO / "data/cancer/claims_current.jsonl").write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows), encoding="utf-8")
(REPO / "changes/book_patch.jsonl").write_text("".join(json.dumps(
    {"change_id": r["change_id"], "module": r["module"], "original": r["original"], "revised": r["final"], "kind": r["kind"],
     "why": r["why"], "reviewed_by": r["decided_by"], "reviewed_on": r["decided_date"]}, ensure_ascii=False) + "\n"
    for r in acc.values()), encoding="utf-8")
c = collections.Counter(r["status"] for r in res)
print(f"{len(rows)} claims -> data/cancer/claims_current.jsonl ({len(acc)} reworded); {len(acc)} edits -> changes/book_patch.jsonl")
print(f"  decided: {len(res) - len(pending)} of {len(res)} ({dict(c)})")
if pending:
    print(f"  NOTE: {len(pending)} changes still undecided and NOT applied")
