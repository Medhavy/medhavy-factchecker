#!/usr/bin/env python3
"""10_check_changes.py — validate the wording changes, apply the reviewer's decisions, write the review sheet.

A change is a proposed rewording of a book claim, with the reason and the database quotes behind it. The book's own
sentence is never edited: `canonical` and `claim_origin` in facts.json stay exactly as extracted, and the rewording
lives only in changes/ (and, via step 7, in a claim's `revisions` list).

Reads   changes/changes.jsonl     proposals, written by a model. Every row stays `proposed` here; never edited by a reviewer.
        changes/decisions/*.jsonl one file per reviewer: {change_id, decision, reviewer, date, note, edited}
        changes/decisions.jsonl   (optional) the adjudicator's final calls, same row shape; overrides the reviewers
Writes  changes/resolved.jsonl    each proposal + priority + derived status + the final wording (regenerable; steps 7 and 11 read it)
        changes/CHANGES.md        the review sheet, in priority order: what the book said, what is proposed, why, the quote

Priority (what a reviewer sees first): 1 = a database record points against the claim (`conflicting_evidence`);
2 = a time-bound claim a record shows has moved on (`dated_evidence`); 3 = everything else. Within a tier, more
refuting records first, then book order. The tier comes from the claim's status, so it changes when the evidence does.

Proposal row: {change_id, fact_id, module, original, proposed, kind, why, evidence: [{record_id, url, quote}],
               status: "proposed", proposed_by, proposed_date}

Checks (any failure stops the run):
  - fact_id exists and `original` equals the claim's canonical sentence, character for character
  - kind is on the list in changes_vocab.py; `proposed` is non-empty and differs from `original`
  - every evidence quote is an exact substring (whitespace-collapsed) of a database quote already stored on that claim
  - a decision names a real change, uses an allowed answer, has a reviewer and a date;
    `accept_edited` also needs an `edited` wording that differs from the proposal
The final wording: proposal for `accept`, the reviewer's text for `accept_edited`, none for `reject` or no decision yet.
A reviewer's own wording is NOT machine-checked against the quotes; the sheet says so.

Usage: python3 pipeline/10_check_changes.py     (then 07_merge_into_facts.py)
"""
import json, sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))
from changes_vocab import ANSWERS, KINDS, STATUSES  # noqa: E402


def norm(s):
    return " ".join((s or "").split())


def jl(p):
    p = Path(p)
    return [json.loads(l) for l in p.read_text(encoding="utf-8").splitlines() if l.strip()] if p.exists() else []


facts = {f["fact_id"]: f for f in json.loads((REPO / "data/cancer/facts.json").read_text(encoding="utf-8"))}
props = jl(REPO / "changes/changes.jsonl")
by_id = {}
for r in props:
    cid = r["change_id"]
    assert cid not in by_id, f"duplicate change_id {cid}"; by_id[cid] = r
    f = facts.get(r["fact_id"]); assert f, f"{cid}: unknown claim"
    assert r["status"] == "proposed", f"{cid}: changes.jsonl rows stay 'proposed'; decisions go in changes/decisions/"
    assert r["original"] == f["canonical"], f"{cid}: original is not the book's sentence"
    assert norm(r["proposed"]) and r["proposed"] != r["original"], f"{cid}: proposed wording is empty or unchanged"
    assert r["kind"] in KINDS, f"{cid}: kind '{r['kind']}' not allowed"
    assert r["why"].strip(), f"{cid}: a change needs a reason"
    assert r["evidence"], f"{cid}: a change needs at least one database quote"
    for e in r["evidence"]:
        assert any(x["record_id"] == e["record_id"] and norm(e["quote"]) in norm(x["verbatim"]) for x in f["evidence"]), \
            f"{cid}: quote from {e['record_id']} is not in this claim's stored evidence"

# decisions: one file per reviewer (changes/decisions/<name>.jsonl, only the changes that reviewer has answered),
# plus changes/decisions.jsonl for the adjudicator's final calls. Filled-in answers are never touched by this script.
def check_decision(d, who):
    cid = d["change_id"]
    assert cid in by_id, f"{who}: decision for an unknown change {cid[:40]}"
    assert d["decision"] in ANSWERS, f"{who}: '{d['decision']}' is not an allowed answer"
    assert d.get("reviewer") and d.get("date"), f"{who}: a decision needs a reviewer and a date ({cid[:40]})"
    if d["decision"] == "accept_edited":
        assert norm(d.get("edited")) and d["edited"] != by_id[cid]["proposed"], f"{cid[:40]}: accept_edited needs your own wording in `edited`"


reviewers = {}
for dp in sorted((REPO / "changes/decisions").glob("*.jsonl")):
    for d in jl(dp):
        if d.get("decision"):
            check_decision(d, dp.name)
            reviewers.setdefault(d["change_id"], {})[d["reviewer"]] = d
final_call = {}
adj = REPO / "changes/decisions.jsonl"
for d in jl(adj):
    if d.get("decision"):
        check_decision(d, adj.name)
        final_call[d["change_id"]] = d


def priority(r):
    f = facts[r["fact_id"]]
    tier = {"conflicting_evidence": 1, "dated_evidence": 2}.get(f["status"], 3)
    n_ref = sum(1 for x in f["evidence"] if x["stance"] == "refutes")
    why = {1: "a record points against the claim", 2: "a record shows a time-bound claim has moved on",
           3: "the claim is only partly supported"}[tier]
    return (tier, -n_ref, r["module"], r["change_id"]), tier, why


def same(a, b):
    return a["decision"] == b["decision"] and (a["decision"] != "accept_edited" or norm(a["edited"]) == norm(b["edited"]))


order = sorted(by_id, key=lambda c: priority(by_id[c])[0])
policy = json.loads((REPO / "changes/policy.json").read_text(encoding="utf-8")) if (REPO / "changes/policy.json").exists() else {}
MIN = int(policy.get("min_reviewers", 1))
assert MIN >= 1, "changes/policy.json: min_reviewers must be at least 1"
ent = {r["change_id"]: r for r in jl(REPO / "changes/entailment.jsonl")}
resolved = []
for cid in order:
    r = by_id[cid]
    _, tier, tier_why = priority(r)
    out = dict(r)
    ds = list(reviewers.get(cid, {}).values())
    out.update(priority=tier, priority_reason=tier_why, status="proposed", final=None, decided_by=None, decided_date=None,
               review_note=None, quote_check=(ent.get(cid) or {}).get("verdict"), quote_check_extra=(ent.get(cid) or {}).get("extra"), reviewers=sorted(reviewers.get(cid, {})), decision_source=None)
    d = None
    if cid in final_call:
        d, out["decision_source"] = final_call[cid], "adjudicator"
    elif len(ds) >= 1 and len(ds) < MIN and all(same(ds[0], x) for x in ds[1:]):
        out.update(status="needs_more_reviewers", decision_source=f"{len(ds)} of {MIN} reviewers so far")
    elif len(ds) >= 1:
        if all(same(ds[0], x) for x in ds[1:]):
            d, out["decision_source"] = ds[0], ("one reviewer" if len(ds) == 1 else f"{len(ds)} reviewers agree")
        else:
            out.update(status="disputed", decision_source="reviewers disagree",
                       review_note=" | ".join(f"{x['reviewer']}: {x['decision']}" + (f" ({x['note']})" if x.get("note") else "") for x in ds))
    if d:
        out.update(status={"accept": "accepted", "accept_edited": "accepted_edited", "reject": "rejected"}[d["decision"]],
                   final=r["proposed"] if d["decision"] == "accept" else (d["edited"] if d["decision"] == "accept_edited" else None),
                   decided_by=d["reviewer"], decided_date=d["date"], review_note=d.get("note"))
    resolved.append(out)
(REPO / "changes/resolved.jsonl").write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in resolved), encoding="utf-8")

n = {s: sum(1 for r in resolved if r["status"] == s) for s in STATUSES}
left = n["proposed"] + n["disputed"] + n["needs_more_reviewers"]
L = ["# Wording changes — review sheet\n", "## Summary\n"]
L.append(f"**{len(resolved)} proposed rewordings** of the book's sentences: {n['proposed']} waiting for a reviewer, {n['needs_more_reviewers']} waiting for more reviewers (policy: {MIN} needed), {n['disputed']} disputed between reviewers, "
         f"{n['accepted'] + n['accepted_edited']} accepted, {n['rejected']} rejected. They are listed in priority order; work from the top. A model wrote every proposal. "
         "The book's own sentence is never edited; each change records what it said, what is proposed, why, and the database quote behind it.\n")
L.append("### How to review\n")
L.append("1. Read the book's sentence, the proposal, the reason and the quote. Open the record link if the quote is not enough.")
L.append("2. Use the review dashboard (`streamlit run review_app.py`), or write a row in `changes/decisions/<your-name>.jsonl` with `decision` one of: " + "; ".join(f"`{a}` ({t})" for a, t in ANSWERS.items()) + ".")
L.append("3. A row needs `change_id`, `decision`, your name as `reviewer`, the `date`, and optionally `note` and `edited`. Two reviewers who disagree make the change `disputed`; a row in `changes/decisions.jsonl` is the final call.")
L.append("4. Run `python3 pipeline/10_check_changes.py`. When you are through, run `python3 pipeline/11_implement_changes.py` to apply the accepted ones.\n")
L.append("A proposal is checked against the stored quotes by the pipeline. Wording you write yourself (`accept_edited`) is not; you are the check on it.\n")
L.append("---\n")
for i, r in enumerate(resolved, 1):
    L.append(f"### {i} of {len(resolved)}. {r['module']} · {r['kind']} · priority {r['priority']} · `{r['status']}`\n")
    L.append(f"- **Why this position:** {r['priority_reason']}")
    L.append(f"- **Change id:** `{r['change_id']}`")
    L.append(f"- **Book:** {r['original']}")
    L.append(f"- **Proposed:** {r['proposed']}")
    L.append(f"- **Why:** {r['why']}")
    for e in r["evidence"]:
        L.append(f"- **Record:** [{e['record_id']}]({e['url']}) “{e['quote']}”")
    if r.get("quote_check") == "over_reach":
        L.append(f"- **Second reader's warning:** the sentence says something the quotes do not: {r['quote_check_extra']}")
    L.append(f"- **Proposed by:** {r['proposed_by']} on {r['proposed_date']}")
    if r["decided_by"]:
        L.append(f"- **Decision:** `{r['status']}` by {r['decided_by']} on {r['decided_date']}" + (f" — {r['review_note']}" if r["review_note"] else ""))
        if r["status"] == "accepted_edited":
            L.append(f"- **Final wording (reviewer's own):** {r['final']}")
    L.append("")
(REPO / "changes/CHANGES.md").write_text("\n".join(L) + "\n", encoding="utf-8")
print(f"{left} still to review; next up: " + (", ".join(r["change_id"][:50] for r in resolved if r["status"] == "proposed")[:200] or "none"))
print(f"{len(resolved)} changes valid -> changes/resolved.jsonl, changes/CHANGES.md  {n}")
