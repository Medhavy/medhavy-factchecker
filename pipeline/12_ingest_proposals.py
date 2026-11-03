#!/usr/bin/env python3
"""12_ingest_proposals.py — turn a proposer run (model-written rewordings) into rows in changes/.

A proposer run is a folder of paired files:
  in_N.jsonl   one row per claim: {change_id, module, claim, evidence: [{i, source, record_id, stance, quote, note}]}
  out_N.jsonl  one row per claim, from a model: {change_id, action: "propose"|"no_change", proposed, kind, why, uses: [i, ...]}
The model chose which evidence quotes (`uses`) its wording rests on. This script does NOT trust the wording or the quotes:
it takes each quote from the claim's own stored evidence in facts.json by index, so a quote can never be invented,
and rejects a row whose `uses` points at nothing.

  propose    -> appended to changes/changes.jsonl as a `proposed` change (checked later by 10_check_changes.py)
  no_change  -> appended to changes/no_change.jsonl: the model judged the book's sentence already within what the records say.
                These are logged, not hidden, so the paper can report how often it happened.

Already-present change_ids are skipped, so re-running is safe. The run's raw files are copied to changes/proposer_runs/<name>/.

Usage: python3 pipeline/12_ingest_proposals.py RUN_FOLDER [--name 2026-11-03-partial]
"""
import argparse, json, shutil, sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))
from changes_vocab import KINDS  # noqa: E402

ap = argparse.ArgumentParser()
ap.add_argument("run")
ap.add_argument("--name", default="run")
ap.add_argument("--date", default="2026-11-03")
a = ap.parse_args()
run = Path(a.run)


def jl(p):
    p = Path(p)
    return [json.loads(l) for l in p.read_text(encoding="utf-8").splitlines() if l.strip()] if p.exists() else []


facts = {f["fact_id"]: f for f in json.loads((REPO / "data/cancer/facts.json").read_text(encoding="utf-8"))}
have = {r["change_id"] for r in jl(REPO / "changes/changes.jsonl")} | {r["change_id"] for r in jl(REPO / "changes/no_change.jsonl")}
new_props, new_none, bad = [], [], []
for inp in sorted(run.glob("in_*.jsonl")):
    out = run / inp.name.replace("in_", "out_")
    ins, outs = jl(inp), jl(out)
    if [r["change_id"] for r in ins] != [r["change_id"] for r in outs]:
        sys.exit(f"{out.name}: rows do not match {inp.name}")
    for i, o in zip(ins, outs):
        cid = o["change_id"]
        if cid in have:
            continue
        fid = cid.rsplit("#", 1)[0]
        f = facts[fid]
        if o["action"] == "no_change":
            if not o.get("why", "").strip():
                bad.append((cid, "no_change without a reason")); continue
            new_none.append({"change_id": cid, "fact_id": fid, "module": f["claim_origin"]["module"], "original": f["canonical"],
                             "why": o["why"], "proposed_by": "model", "proposed_date": a.date})
            continue
        stored = {e["record_id"] + "\x00" + e["verbatim"]: e for e in f["evidence"]}
        ev = []
        for k in o.get("uses", []):
            if not isinstance(k, int) or not 0 <= k < len(i["evidence"]):
                bad.append((cid, f"uses index {k} not in evidence")); ev = []; break
            q = i["evidence"][k]
            e = stored.get(q["record_id"] + "\x00" + q["quote"])
            if not e:
                bad.append((cid, f"quote {k} is not in the claim's stored evidence")); ev = []; break
            ev.append({"record_id": e["record_id"], "url": e["url"], "quote": e["verbatim"]})
        if not ev:
            if not any(b[0] == cid for b in bad): bad.append((cid, "no evidence quotes used"))
            continue
        if o["kind"] not in KINDS or not o["proposed"].strip() or o["proposed"] == f["canonical"] or not o["why"].strip():
            bad.append((cid, "bad kind, empty/unchanged wording, or no reason")); continue
        new_props.append({"change_id": cid, "fact_id": fid, "module": f["claim_origin"]["module"], "original": f["canonical"],
                          "proposed": o["proposed"].strip(), "kind": o["kind"], "why": o["why"].strip(), "evidence": ev,
                          "status": "proposed", "proposed_by": "model", "proposed_date": a.date})

with open(REPO / "changes/changes.jsonl", "a", encoding="utf-8") as fh:
    for r in new_props: fh.write(json.dumps(r, ensure_ascii=False) + "\n")
with open(REPO / "changes/no_change.jsonl", "a", encoding="utf-8") as fh:
    for r in new_none: fh.write(json.dumps(r, ensure_ascii=False) + "\n")
dest = REPO / "changes/proposer_runs" / a.name
dest.mkdir(parents=True, exist_ok=True)
for p in list(run.glob("in_*.jsonl")) + list(run.glob("out_*.jsonl")):
    shutil.copy(p, dest / p.name)
print(f"{len(new_props)} proposals -> changes/changes.jsonl; {len(new_none)} no_change -> changes/no_change.jsonl; {len(bad)} rejected")
for b in bad[:10]: print("  rejected:", b)
