#!/usr/bin/env python3
"""07_merge_into_facts.py — put each claim's evidence and derived status into data/cancer/facts.json.

After this, facts.json holds the claim, where the book said it, the evidence found, and the status — one record each.

Run order:  05_build_evidence.py  ->  05b_strict_recheck.py  ->  06_derive_status.py  ->  07_merge_into_facts.py
(re-running 05 rebuilds the evidence rows and drops the strict re-read; re-apply 05b from data/cancer/strict_recheck.jsonl)

Rebuilt from scratch on every run (never appended), so it is idempotent. It touches ONLY these three keys of a claim:
  evidence       the evidence rows for this claim from every data/cancer/**/evidence*.jsonl (the fact_id inside each
                 row is dropped; it is the parent's)
  status         copied from data/cancer/status.jsonl
  status_detail  the rest of that status row: reason, database, counts, sources, flags, needs_review,
                 review_reasons, human_reviewed
fact_id, canonical, domain, stable, category and claim_origin are never changed; the script asserts this.

status.jsonl stays as a flat table of the same statuses (easy to count and filter). Its contents are derived
from the evidence, so the two cannot disagree after a run.

Usage: python3 pipeline/07_merge_into_facts.py
"""
import collections, glob, json
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
FACTS = REPO / "data/cancer/facts.json"
KEEP = ("fact_id", "canonical", "domain", "stable", "category", "claim_origin")


def jl(p):
    return [json.loads(l) for l in Path(p).read_text(encoding="utf-8").splitlines() if l.strip()]


facts = json.loads(FACTS.read_text(encoding="utf-8"))
status = {r["fact_id"]: r for r in jl(REPO / "data/cancer/status.jsonl")}
ev = collections.defaultdict(list)
for p in sorted(glob.glob(str(REPO / "data/cancer/**/evidence*.jsonl"), recursive=True)):
    for r in jl(p):
        ev[r["fact_id"]].append({k: v for k, v in r.items() if k != "fact_id"})

assert set(status) == {f["fact_id"] for f in facts}, "status.jsonl and facts.json disagree on claims; run 06 first"
assert set(ev) <= set(status), "evidence for an unknown claim"

merged = []
for f in facts:
    fid = f["fact_id"]
    s = status[fid]
    g = {k: f[k] for k in KEEP}                       # untouched fields, in their original order
    g["evidence"] = ev.get(fid, [])
    g["status"] = s["status"]
    g["status_detail"] = {k: v for k, v in s.items() if k not in ("fact_id", "status")}
    merged.append(g)

# nothing but evidence / status / status_detail may differ from what was there
for a, b in zip(facts, merged):
    assert all(a[k] == b[k] for k in KEEP), f"changed a protected field on {a['fact_id']}"
assert [f["fact_id"] for f in facts] == [g["fact_id"] for g in merged]

FACTS.write_text(json.dumps(merged, indent=2, ensure_ascii=False), encoding="utf-8")
n_ev = sum(len(g["evidence"]) for g in merged)
print(f"{len(merged)} claims; {n_ev} evidence rows on {sum(1 for g in merged if g['evidence'])} claims -> {FACTS}")
for s, n in collections.Counter(g["status"] for g in merged).most_common(): print(f"  {s:<22}{n:>5}")
