#!/usr/bin/env python3
"""08_build_review_queue.py — build the human review queue from the claims step 6 flagged.

Reads   data/cancer/facts.json   (claims whose status_detail.needs_review is true)
        review/decisions.jsonl   (existing decisions, if any; never overwritten)
Writes  review/QUEUE.md          what a reviewer reads: each case with the book's claim, the quoted evidence, a link
                                 to each record, and the one question to answer
        review/decisions.jsonl   one row per queued claim; a reviewer fills `decision`, `reviewer`, `date`, `note`.
                                 Rows that already hold a decision are kept exactly as they are.

A decision never changes a claim's evidence or its derived status. 06_derive_status.py attaches it as `human_review`
and sets `human_reviewed: true`, so a count can separate "a model read this" from "a person checked it".

Usage: python3 pipeline/08_build_review_queue.py      (then edit review/decisions.jsonl, then run 06 and 07)
"""
import collections, datetime, json, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from review_vocab import KINDS  # noqa: E402

REPO = Path(__file__).resolve().parents[1]
OUT = REPO / "review"
TODAY = datetime.date.today().isoformat()

def jl(p):
    p = Path(p)
    return [json.loads(l) for l in p.read_text(encoding="utf-8").splitlines() if l.strip()] if p.exists() else []


def kind(f):
    d = f["status_detail"]
    if f["status"] == "dated_evidence": return "dated"
    if f["status"] == "conflicting_evidence": return "conflict"
    return "plural"


facts = json.loads((REPO / "data/cancer/facts.json").read_text(encoding="utf-8"))
queue = [f for f in facts if f["status_detail"]["needs_review"]]
order = {"conflict": 0, "dated": 1, "plural": 2}
queue.sort(key=lambda f: (order[kind(f)], f["claim_origin"]["module"], f["fact_id"]))

old = {r["fact_id"]: r for r in jl(OUT / "decisions.jsonl")}
OUT.mkdir(exist_ok=True)
rows = []
for f in queue:
    k = kind(f)
    r = old.get(f["fact_id"]) or {"fact_id": f["fact_id"], "review_type": k, "decision": None,
                                  "reviewer": None, "date": None, "note": None}
    r["review_type"] = k
    rows.append(r)
(OUT / "decisions.jsonl").write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows), encoding="utf-8")

n = collections.Counter(kind(f) for f in queue)
done = sum(1 for r in rows if r["decision"])

L = []
L.append("# Human review queue\n")
L.append("## Summary\n")
L.append(f"**{len(queue)} claims need a person to look.** {done} decided, {len(queue) - done} to go. "
         f"Built {TODAY} from `data/cancer/facts.json`.\n")
L.append(f"- **{n['conflict']} conflicts:** a retrieved record says something that points against the book's claim. "
         "Most are one study in a narrower setting, so this is \"a person should look\", not \"the book is wrong\".")
L.append(f"- **{n['dated']} dated difference:** a record differs from a time-bound claim only because it shows today's state.")
L.append(f"- **{n['plural']} plural claims:** the book says \"several\" or \"many\" and only one record was found.\n")
L.append("Everything the evidence says here is a model's reading of a quoted passage. The quote is an exact copy of the "
         "record; the stance (`supports`, `partial`, `refutes`, `related`) is not reviewed. You are the first human check.\n")
L.append("### How to review\n")
L.append("1. Read the case. Open the record link if the quote is not enough.")
L.append("2. Pick one answer for the question under the case.")
L.append("3. Write it in `review/decisions.jsonl`: set `decision` to the answer key, add your name as `reviewer`, today's "
         "date, and a `note` if you want to say why.")
L.append("4. Run `python3 pipeline/06_derive_status.py` then `python3 pipeline/07_merge_into_facts.py`. The decision is "
         "attached to the claim as `human_review` and `human_reviewed` becomes true. The evidence and status are not changed.\n")
L.append("Do not edit the quotes or stances. If a stance is wrong, say so in `note`.\n")
L.append("---\n")

cur = None
i = 0
for f in queue:
    k = kind(f)
    if k != cur:
        cur = k
        L.append(f"## {KINDS[k]['title']} ({n[k]})\n")
        L.append(f"**Question:** {KINDS[k]['ask']}\n")
        L.append("Answers: " + "; ".join(f"`{a}` = {t}" for a, t in KINDS[k]["answers"].items()) + "\n")
    i += 1
    co = f["claim_origin"]
    d = f["status_detail"]
    L.append(f"### {i}. {f['canonical']}\n")
    L.append(f"- **Book:** {co['module']} (`{co['url']}`)")
    L.append(f"- **Fact id:** `{f['fact_id']}`")
    L.append(f"- **Status:** `{f['status']}` · looked up in {d['database']} · {d['n_records']} record(s)")
    L.append(f"- **Why flagged:** {'; '.join(d['review_reasons'])}")
    r = next(x for x in rows if x["fact_id"] == f["fact_id"])
    if r["decision"]:
        L.append(f"- **Decided:** `{r['decision']}` by {r['reviewer']} on {r['date']}" + (f" — {r['note']}" if r["note"] else ""))
    L.append("")
    shown = sorted(f["evidence"], key=lambda e: {"refutes": 0, "supports": 1, "partial": 2, "related": 3}[e["stance"]])
    for e in shown:
        L.append(f"> **{e['stance']}** · {e['source']} · [{e['record_id']}]({e['url']})  ")
        L.append(f"> {e['title']}  ")
        L.append(f"> “{e['verbatim']}”  ")
        L.append(f"> _model's note: {e['stance_note']}_")
        L.append(">")
    L.append("")
    L.append("---\n")

(OUT / "QUEUE.md").write_text("\n".join(L), encoding="utf-8")
print(f"{len(queue)} queued ({dict(n)}), {done} decided -> {OUT / 'QUEUE.md'}, {OUT / 'decisions.jsonl'}")
