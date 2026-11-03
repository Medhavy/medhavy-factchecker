#!/usr/bin/env python3
"""09_build_report.py — write REPORT.md: what the fact checker found, in plain words, summary first.

Reads   data/cancer/facts.json (merged by step 7), data/cancer/strict_recheck.jsonl (if present), review/decisions.jsonl
Writes  REPORT.md   (every number is computed here; nothing is typed in by hand except the hand-check note)

Usage: python3 pipeline/09_build_report.py
"""
import collections, datetime, json, random
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]


def jl(p):
    p = Path(p)
    return [json.loads(l) for l in p.read_text(encoding="utf-8").splitlines() if l.strip()] if p.exists() else []


facts = json.loads((REPO / "data/cancer/facts.json").read_text(encoding="utf-8"))
strict = jl(REPO / "data/cancer/strict_recheck.jsonl")
dec = jl(REPO / "review/decisions.jsonl")
N = len(facts)
st = collections.Counter(f["status"] for f in facts)
checked = sum(st[s] for s in ("no_evidence_found", "related_only", "partially_supported", "supported",
                               "conflicting_evidence", "dated_evidence"))
real = N - st["not_an_assertion"]
n_ev = sum(len(f["evidence"]) for f in facts)
n_dec = sum(1 for d in dec if d.get("decision"))
pct = lambda a, b: f"{100 * a / b:.0f}%"

L = []
A = L.append
A("# Medhavy fact checker — what it found\n")
A(f"Built {datetime.date.today().isoformat()} from `data/cancer/facts.json`. The book is the Medhavy cancer textbook.\n")
A("## Summary\n")
A(f"- **{N:,} statements** were pulled from the book. **{real:,}** are real assertions; the other {st['not_an_assertion']} are framing, "
  "opinion or vague, and no database record could confirm or refute them.")
A(f"- **{checked:,} statements** were looked up in a public database (PubMed, UniProt, openFDA, ClinicalTrials.gov, NCBI Gene). "
  f"That produced **{n_ev:,} pieces of evidence**: each is an exact quote from a database record, with a link to it.")
A(f"- **{st['supported']} are supported** ({pct(st['supported'], checked)} of those looked up): a record states the claim. "
  f"**{st['partially_supported']} are partly supported** ({pct(st['partially_supported'], checked)}): records back part of it, or a narrower version. "
  f"**{st['related_only']}** only found records on the same topic. **{st['no_evidence_found']}** found nothing in the top results.")
A(f"- **{st['conflicting_evidence'] + st['dated_evidence']} need a person.** A record points against the book, or against a "
  "time-bound claim (\"currently\", \"ongoing\"). Most are one study in a narrower setting, so this means \"look\", not \"the book is wrong\".")
A(f"- **Human check so far: {n_dec} of {len(dec)} flagged cases decided.** Every \"supports\" or \"conflicts\" label is a model's reading of the "
  "quote. The quote is real and exact; the reading is not yet checked by a person.\n")
A("**\"Supported\" never means \"true\".** It means a database record says so. A record can be wrong, narrow or out of date.\n")

A("## Where all the statements went\n")
A("| Status | Statements | What it means |\n|---|---:|---|")
rows = [("not_an_assertion", "Framing, opinion or vague. Nothing to check."),
        ("no_record_type", "A real claim, but no public record type fits (general textbook knowledge)."),
        ("not_queryable", "A database fits, but no stand-alone question could be written."),
        ("no_open_api", "A database fits (SEER, GLOBOCAN, guideline bodies) but it has no open API. **Not checked.**"),
        ("no_evidence_found", "Searched; nothing in the top 5 records bore on the claim. Not the same as \"no evidence exists\"."),
        ("related_only", "Records on the same topic; none states the claim."),
        ("partially_supported", "A record backs part of the claim, a narrower version, or one instance of a plural claim."),
        ("supported", "A record states the claim (a plural claim needs two records)."),
        ("conflicting_evidence", "A record states something that points against the claim. Needs a person."),
        ("dated_evidence", "A record differs only because it shows today's state of a time-bound claim. Needs a person.")]
for s, t in rows:
    A(f"| `{s}` | {st[s]:,} | {t} |")
A("")

A("## How far to trust \"supported\"\n")
A("The first pass was too generous. A hand check of 24 random \"supports\" quotes found 15 clean and 9 that covered only one clause "
  "of a multi-part claim (for example, a claim about \"adverse effects *that restrict clinical application*\" matched a quote about adverse effects alone).\n")
if strict:
    k = sum(1 for r in strict if r["verdict"] == "keep")
    d = len(strict) - k
    A(f"So every \"supports\" quote was re-read under a strict rule: keep it only if the quote by itself states every substantive part of the claim. "
      f"**{d} of {len(strict)} were downgraded to partial; {k} kept** ({pct(k, len(strict))}). The pass can only downgrade, never upgrade. "
      "The original label is kept on each row as `stance_original`, and all verdicts are in `data/cancer/strict_recheck.jsonl`. "
      "This is a second model reading, still unreviewed by a person.\n")
else:
    A("A strict second reading has not been applied yet.\n")

A("## Five examples that came out supported\n")
random.seed(11)
sup = [f for f in facts if f["status"] == "supported"]
for f in random.sample(sup, min(5, len(sup))):
    e = next(x for x in f["evidence"] if x["stance"] == "supports")
    A(f"**Book ({f['claim_origin']['module']}):** {f['canonical']}  ")
    A(f"> “{e['verbatim']}”  ")
    A(f"> — {e['source']}, [{e['record_id']}]({e['url']}): {e['title']}\n")

A("## The conflicts\n")
A("These are the cases where a record points against the book. Each is in `review/QUEUE.md` with the full quote and a link.\n")
for f in facts:
    if f["status"] in ("conflicting_evidence", "dated_evidence"):
        A(f"- {f['canonical']} _({f['claim_origin']['module']})_")
A("")

A("## What is not covered\n")
A(f"- **{st['no_open_api']} statements** that need SEER/GLOBOCAN cancer statistics, clinical guidelines or Ensembl. Their databases have no open API; they are listed, not checked.")
A(f"- **{st['no_record_type']} statements** that are real but general (mechanisms, definitions, history). No public record type holds them.")
A(f"- **{st['not_queryable']} statements** that could not be turned into a stand-alone question.")
A("- Only the top 5 records per question were read, so \"no evidence found\" is a limit of the search, not a finding about the world.")
A("- Only the cancer book has been run. The pipeline is built to take other Medhavy books.\n")
A("## Files\n")
A("- `data/cancer/facts.json` — every statement with its evidence and status.")
A("- `review/QUEUE.md` and `review/decisions.jsonl` — the cases for a person to decide.")
A("- `README.md` — how the pipeline works, step by step.")

(REPO / "REPORT.md").write_text("\n".join(L) + "\n", encoding="utf-8")
print("REPORT.md written;", dict(st))
