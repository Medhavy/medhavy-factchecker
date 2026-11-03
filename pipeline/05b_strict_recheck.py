#!/usr/bin/env python3
"""05b_strict_recheck.py — apply a strict second reading to every evidence row labelled `supports`.

Why: a hand check of 24 random `supports` rows found about a third were too generous (the quote covers one clause
of a multi-part claim, or one study in a narrower setting). A second model pass re-read every `supports` quote with
a strict rule: keep only if the quote by itself states every substantive component of the claim.

The pass can only KEEP or DOWNGRADE (supports -> partial). It never upgrades and never edits a quote. The original
label stays on the row as `stance_original`, the missing component is added to `stance_note`, and the verdicts are
saved in data/cancer/strict_recheck.jsonl so the change can be audited.

Inputs   one or more verdict files, JSON Lines: {"id": "<fact_id>|<record_id>", "quote": "<the quote judged>",
         "verdict": "keep"|"partial", "missing": "..."}. A record can be quoted twice for one claim, so a verdict is
         matched on id AND the quote text.
Edits    data/cancer/**/evidence*.jsonl (in place; idempotent: a row that already has `stance_original` is skipped)
Writes   data/cancer/strict_recheck.jsonl (all verdicts, merged)
Then run 06_derive_status.py and 07_merge_into_facts.py.

Usage: python3 pipeline/05b_strict_recheck.py out_0.jsonl out_1.jsonl ...
"""
import collections, glob, hashlib, json, sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]


def key(i, quote):
    return i + "|" + hashlib.sha1(" ".join((quote or "").split()).encode()).hexdigest()[:10]


verd = {}
for p in sys.argv[1:]:
    for l in Path(p).read_text(encoding="utf-8").splitlines():
        if l.strip():
            r = json.loads(l)
            assert r["verdict"] in ("keep", "partial"), r
            k = key(r["id"], r["quote"])
            assert k not in verd, f"duplicate verdict {r['id']}"
            verd[k] = r
assert verd, "no verdicts given"

c = collections.Counter()
seen = set()
for p in sorted(glob.glob(str(REPO / "data/cancer/**/evidence*.jsonl"), recursive=True)):
    rows = [json.loads(l) for l in Path(p).read_text(encoding="utf-8").splitlines() if l.strip()]
    for e in rows:
        k = key(f"{e['fact_id']}|{e['record_id']}", e["verbatim"])
        v = verd.get(k)
        if not v:
            continue
        seen.add(k)
        if "stance_original" in e:
            c["already applied"] += 1; continue
        assert e["stance"] == "supports", f"{k}: verdict for a row that is {e['stance']}"
        e["stance_original"] = "supports"
        c["kept"] += v["verdict"] == "keep"
        if v["verdict"] == "partial":
            e["stance"] = "partial"
            e["stance_note"] = (e["stance_note"] + " " if e["stance_note"] else "") + "Strict re-read: the quote does not state " + v["missing"].rstrip(". ") + "."
            c["downgraded"] += 1
        e["stance_by"] = "model, unreviewed; strict re-read"
    Path(p).write_text("".join(json.dumps(e, ensure_ascii=False) + "\n" for e in rows), encoding="utf-8")

missing = set(verd) - seen
assert not missing, f"{len(missing)} verdicts match no evidence row, e.g. {sorted(missing)[:2]}"
out = REPO / "data/cancer/strict_recheck.jsonl"
out.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in verd.values()), encoding="utf-8")
print(f"{len(verd)} verdicts -> {out}")
for k, v in c.items(): print(f"  {k}: {v}")
