#!/usr/bin/env python3
"""06_derive_status.py — step 6: derive each claim's status from its evidence. No votes, no verdict words.

Reads   data/cancer/facts.json, triage/triage.jsonl, data/cancer/queries.jsonl,
        data/cancer/pilot/attempts.jsonl, every data/cancer/**/evidence*.jsonl, review/decisions.jsonl (if filled in)
Writes  data/cancer/status.jsonl  (one row per claim, same order as facts.json; always regenerable)

The status says how far a claim has got and what the evidence found. It never says "true".
`supported` means: a retrieved database record contains a passage that a model read as stating the claim's
relation or value. Every stance is a model's unreviewed reading (`human_reviewed` is false on every row).

Statuses, in the order a claim can fall out of the pipeline:
  not_an_assertion     triage: framing, evaluation or vagueness; no record could confirm or refute it
  no_record_type       triage: a real claim, but no database record type fits (general textbook knowledge)
  not_queryable        a database fits, but no stand-alone query could be written (needs context, too vague)
  no_open_api          queryable, but its database (SEER/GLOBOCAN, guideline bodies) has no open API
  not_yet_checked      queryable with an open API, not retrieved yet
  retrieval_failed     the request errored
  no_evidence_found    retrieved; nothing returned, or nothing returned bears on the claim
  related_only         passages on the same topic, none states the claim's relation or value
  partially_supported  passages support part of it, or a different number/scope, or one record for a plural claim
  supported            at least one passage states the claim's relation or value (plural claims need 2 records)
  conflicting_evidence a passage states a conflicting value/relation (needs a human)
  dated_evidence       a record differs only because it shows today's state of a time-bound claim (needs a human)

Two wording flags (pipeline/claim_flags.py) adjust the reading:
  time_sensitive  "refutes" is counted as a dated difference, not a conflict
  plural          "supports" from a single record is counted as partial

Usage: python3 pipeline/06_derive_status.py
"""
import collections, glob, json, sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))
import claim_flags as cf  # noqa: E402
from review_vocab import KINDS  # noqa: E402

NO_API = {"seer-globocan", "guideline-body"}


def jl(p):
    return [json.loads(l) for l in Path(p).read_text(encoding="utf-8").splitlines() if l.strip()]


facts = json.loads((REPO / "data/cancer/facts.json").read_text(encoding="utf-8"))
tri = {r["fact_id"]: r for r in jl(REPO / "triage/triage.jsonl")}
qry = {r["fact_id"]: r for r in jl(REPO / "data/cancer/queries.jsonl")}
att = {}
for p in sorted(glob.glob(str(REPO / "data/cancer/**/attempts*.jsonl"), recursive=True)):
    for r in jl(p): att[r["fact_id"]] = r
ev = collections.defaultdict(list)
for p in sorted(glob.glob(str(REPO / "data/cancer/**/evidence*.jsonl"), recursive=True)):
    for r in jl(p): ev[r["fact_id"]].append(r)

assert set(tri) == {f["fact_id"] for f in facts}, "triage ids differ from facts.json"
assert set(ev) <= set(qry), "evidence for a claim with no query"

rows = []
for f in facts:
    fid = f["fact_id"]; t = tri[fid]; q = qry.get(fid); a = att.get(fid); e = ev.get(fid, [])
    flags = {"time_sensitive": cf.time_sensitive(f["canonical"], q and q["claim_standalone"]),
             "plural": cf.plural(f["canonical"], q and q["claim_standalone"])}
    row = {"fact_id": fid, "status": None, "reason": None, "database": q and q["database_final"],
           "n_records": 0, "n_supports": 0, "n_partial": 0, "n_related": 0, "n_refutes": 0, "n_dated": 0,
           "sources": [], "flags": flags, "needs_review": False, "review_reasons": [], "human_reviewed": False}

    def done(status, reason=None):
        row["status"], row["reason"] = status, reason
        rows.append(row)

    if not t["real_assertion"]:
        done("not_an_assertion", t["label"]); continue
    if not t["strict_assertion"]:
        done("no_record_type", t["database"]); continue
    if not q["queryable"]:
        done("not_queryable", q["unqueryable_reason"]); continue
    if not a:
        done("no_open_api" if q["database_final"] in NO_API else "not_yet_checked", q["database_final"]); continue
    if a.get("skipped"):
        done("no_open_api", a["skipped"]); continue
    if a.get("error"):
        done("retrieval_failed", a["error"][:80]); continue
    if not e:
        done("no_evidence_found", "no records returned" if not a["records_returned"] else "records returned, none bears on the claim"); continue

    rec_ids = {x["record_id"] for x in e}
    row["n_records"] = len(rec_ids); row["sources"] = sorted({x["source"] for x in e})
    sup = {x["record_id"] for x in e if x["stance"] == "supports"}
    n_sup = len(sup)
    n_par = sum(1 for x in e if x["stance"] == "partial")
    n_rel = sum(1 for x in e if x["stance"] == "related")
    n_ref = sum(1 for x in e if x["stance"] == "refutes")
    if flags["time_sensitive"] and n_ref:
        row["n_dated"], n_ref = n_ref, 0
        row["review_reasons"].append("time-bound claim: record shows today's state, which differs")
    if flags["plural"] and 0 < n_sup < 2:
        n_par += n_sup; n_sup = 0
        row["review_reasons"].append("plural claim: only one record supports one instance")
    row.update(n_supports=n_sup, n_partial=n_par, n_related=n_rel, n_refutes=n_ref)

    if n_ref:
        status = "conflicting_evidence"
        row["review_reasons"].append("a passage conflicts with the claim" + ("; another supports it" if n_sup else ""))
    elif row["n_dated"] and not n_sup:
        status = "dated_evidence"
    elif n_sup:
        status = "supported"
    elif n_par:
        status = "partially_supported"
    else:
        status = "related_only"
    row["needs_review"] = status in ("conflicting_evidence", "dated_evidence") or bool(row["review_reasons"])
    done(status)

# human decisions (review/decisions.jsonl): attached to the claim, never used to change evidence or status
dec_path = REPO / "review/decisions.jsonl"
n_dec = 0
if dec_path.exists():
    by_id = {r["fact_id"]: r for r in rows}
    for d in jl(dec_path):
        if not d.get("decision"): continue
        assert d["fact_id"] in by_id, f"decision for unknown claim {d['fact_id']}"
        assert d["decision"] in KINDS[d["review_type"]]["answers"], \
            f"{d['fact_id']}: '{d['decision']}' is not an allowed answer for a {d['review_type']} case"
        assert d.get("reviewer") and d.get("date"), f"{d['fact_id']}: a decision needs a reviewer and a date"
        r = by_id[d["fact_id"]]
        r["human_reviewed"] = True
        r["human_review"] = {k: d.get(k) for k in ("review_type", "decision", "reviewer", "date", "note")}
        n_dec += 1

out = REPO / "data/cancer/status.jsonl"
out.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows), encoding="utf-8")

order = ["not_an_assertion", "no_record_type", "not_queryable", "no_open_api", "not_yet_checked", "retrieval_failed",
         "no_evidence_found", "related_only", "partially_supported", "supported", "conflicting_evidence", "dated_evidence"]
c = collections.Counter(r["status"] for r in rows)
assert sum(c.values()) == len(facts) and set(c) <= set(order)
print(f"{len(rows)} claims -> {out}")
for s in order:
    if c[s]: print(f"  {s:<22}{c[s]:>5}")
print(f"  needs_review: {sum(r['needs_review'] for r in rows)} | human decisions attached: {n_dec}")
