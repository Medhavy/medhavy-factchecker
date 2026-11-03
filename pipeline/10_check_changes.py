#!/usr/bin/env python3
"""10_check_changes.py — validate changes/changes.jsonl and build changes/CHANGES.md.

A change is a proposed rewording of a book claim, with the reason and the database quotes behind it. The book's own
sentence is never edited: `canonical` and `claim_origin` in facts.json stay exactly as extracted, and the rewording
lives only here (and, via step 7, in a claim's `revisions` list). So every claim can show: what the book said, what we
would say instead, why, and who agreed.

Row: {change_id, fact_id, module, original, proposed, kind, why,
      evidence: [{record_id, url, quote}],
      status, proposed_by, proposed_date, decided_by, decided_date, note}

Checks (any failure stops the run):
  - fact_id exists and `original` equals the claim's canonical sentence, character for character
  - kind and status are on the lists in changes_vocab.py
  - every evidence quote is an exact substring (whitespace-collapsed) of a database quote already stored on that claim
  - a change that is not `proposed` has decided_by and decided_date
  - `proposed` differs from `original`

Usage: python3 pipeline/10_check_changes.py     (then run 07_merge_into_facts.py)
"""
import json, sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))
from changes_vocab import KINDS, STATUSES  # noqa: E402


def norm(s):
    return " ".join((s or "").split())


facts = {f["fact_id"]: f for f in json.loads((REPO / "data/cancer/facts.json").read_text(encoding="utf-8"))}
path = REPO / "changes/changes.jsonl"
rows = [json.loads(l) for l in path.read_text(encoding="utf-8").splitlines() if l.strip()] if path.exists() else []
seen = set()
for r in rows:
    cid = r["change_id"]
    assert cid not in seen, f"duplicate change_id {cid}"; seen.add(cid)
    f = facts.get(r["fact_id"]); assert f, f"{cid}: unknown claim"
    assert r["original"] == f["canonical"], f"{cid}: original is not the book's sentence"
    assert norm(r["proposed"]) and r["proposed"] != r["original"], f"{cid}: proposed wording is empty or unchanged"
    assert r["kind"] in KINDS, f"{cid}: kind '{r['kind']}' not allowed"
    assert r["status"] in STATUSES, f"{cid}: status '{r['status']}' not allowed"
    assert r["why"].strip(), f"{cid}: a change needs a reason"
    assert r["evidence"], f"{cid}: a change needs at least one database quote"
    for e in r["evidence"]:
        ok = any(x["record_id"] == e["record_id"] and norm(e["quote"]) in norm(x["verbatim"]) for x in f["evidence"])
        assert ok, f"{cid}: quote from {e['record_id']} is not in this claim's stored evidence"
    if r["status"] != "proposed":
        assert r.get("decided_by") and r.get("decided_date"), f"{cid}: a decided change needs decided_by and decided_date"

L = ["# Wording changes\n", "## Summary\n"]
n = {s: sum(1 for r in rows if r["status"] == s) for s in STATUSES}
L.append(f"**{len(rows)} proposed rewordings** of the book's sentences: {n['proposed']} proposed, {n['approved']} approved, "
         f"{n['rejected']} rejected. The book's own sentence is never edited; each change records what it said, what we would say, "
         "why, and the database quote behind it.\n")
for r in rows:
    L.append(f"### {r['module']} — {KINDS[r['kind']].split(' (')[0]} · `{r['status']}`\n")
    L.append(f"- **Book:** {r['original']}")
    L.append(f"- **Proposed:** {r['proposed']}")
    L.append(f"- **Why:** {r['why']}")
    for e in r["evidence"]:
        L.append(f"- **Record:** [{e['record_id']}]({e['url']}) “{e['quote']}”")
    L.append(f"- **By:** {r['proposed_by']} on {r['proposed_date']}" + (f"; {r['status']} by {r['decided_by']} on {r['decided_date']}" if r.get("decided_by") else ""))
    if r.get("note"): L.append(f"- **Note:** {r['note']}")
    L.append("")
(REPO / "changes/CHANGES.md").write_text("\n".join(L) + "\n", encoding="utf-8")
print(f"{len(rows)} changes valid -> {REPO / 'changes/CHANGES.md'}  {n}")
