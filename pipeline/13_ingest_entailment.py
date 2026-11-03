#!/usr/bin/env python3
"""13_ingest_entailment.py — record the blind second reading of each proposed rewording.

A second model sees ONLY a proposed sentence and the database quotes it rests on (no claim, no notes) and answers: does
everything the sentence says follow from those quotes alone? `ok`, or `over_reach` with what the quotes do not state.
This catches a proposer that borrowed a setting or a name from the unreviewed notes instead of from the quotes.
The result is shown to the reviewer beside each proposal; it never changes a proposal.

Input   a folder of out_N.jsonl files: {"change_id", "verdict": "ok"|"over_reach", "extra"}
Writes  changes/entailment.jsonl  (merged; 10_check_changes.py attaches it to each change)
Usage   python3 pipeline/13_ingest_entailment.py RUN_FOLDER
"""
import json, sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
run = Path(sys.argv[1])
ids = {json.loads(l)["change_id"] for l in (REPO / "changes/changes.jsonl").read_text(encoding="utf-8").splitlines() if l.strip()}
rows = {}
for p in sorted(run.glob("out_*.jsonl")):
    for l in p.read_text(encoding="utf-8").splitlines():
        if l.strip():
            r = json.loads(l)
            assert r["verdict"] in ("ok", "over_reach"), r
            assert r["change_id"] in ids, f"unknown change {r['change_id'][:40]}"
            assert r["verdict"] == "ok" or r["extra"].strip(), f"over_reach without a reason: {r['change_id'][:40]}"
            rows[r["change_id"]] = {"change_id": r["change_id"], "verdict": r["verdict"], "extra": r["extra"].strip(), "checked_by": "model, blind, unreviewed"}
(REPO / "changes/entailment.jsonl").write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows.values()), encoding="utf-8")
n_over = sum(1 for r in rows.values() if r["verdict"] == "over_reach")
print(f"{len(rows)} of {len(ids)} proposals checked: {len(rows) - n_over} ok, {n_over} over_reach -> changes/entailment.jsonl")
