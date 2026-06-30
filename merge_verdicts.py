#!/usr/bin/env python3
"""merge_verdicts.py — ensemble fact-check reconciliation for medhavi-cancer.

Joins the independent checkers' verdict logs on `fact_id`, scores agreement, records
findings back into the shared dictionary (facts/facts.json) via the canonical
facts_store, and emits the human review queue.

Design (matches the project's consensus model):
  - Each checker is an INDEPENDENT voter. Two runs of the same model are NOT two votes
    (correlated error); independence is enforced by `checker` identity + a publisher map.
  - WIDE AGREEMENT = less suspect, never "verified". Only a human signs off.
  - The human queue = every CONFLICT and SPLIT, PLUS a random sample of the CLEAN pile
    (calibration — to catch correlated errors that agree and are still wrong).

Inputs (one JSONL line per claim, schema in the *-factcheck-prompt.md files):
  factchecks-claude/verdicts-claude.jsonl
  factchecks-codex/verdicts-codex.jsonl
  ...any number of factchecks-*/verdicts-*.jsonl

Verdict vocab: CONFIRMED | CONTRADICTED | OUTDATED | UNVERIFIED.

Outputs (under medhavi-facts/cancer/):
  triage/ensemble.jsonl       — per claim: all checker verdicts + agreement + bucket
  triage/HUMAN_QUEUE.md       — what a person should look at, highest priority first
  triage/ENSEMBLE_REPORT.md   — rollup: bucket counts, agreement stats, source-tier weighting
  (optional) records into facts/facts.json via facts_store when --record is passed

Usage:
  python merge_verdicts.py                 # join + triage + reports (no dictionary writes)
  python merge_verdicts.py --record        # also record agreed verdicts into facts/facts.json
  python merge_verdicts.py --sample 0.10   # clean-pile audit sample fraction (default 0.05)
"""
import argparse, glob, json, os, random, re, sys, datetime
from collections import defaultdict, Counter

HERE = os.path.dirname(os.path.abspath(__file__))
CANCER = os.path.join(HERE, "cancer")
CLAIMS = os.path.join(CANCER, "facts.json")
TRIAGE = os.path.join(CANCER, "triage")
TODAY = datetime.date.today().isoformat()

# Map a checker -> the "publisher" whose errors are correlated with it. Two checkers that
# share a publisher do NOT count as independent votes (same_publisher guard for checkers).
CHECKER_PUBLISHER = {"claude": "anthropic", "codex": "openai", "gemini": "google",
                     "deterministic": "rule-based", "human": "human"}
TIER_WEIGHT = {"trusted": 3.0, "solid": 2.0, "low": 1.0, "": 1.0, None: 1.0}
AGREE = {"CONFIRMED": +1, "OUTDATED": -1, "CONTRADICTED": -1, "UNVERIFIED": 0}

# ---- locate the canonical fact store (ai1-cli/facts) so we can record back ----
def find_facts_store():
    root = HERE
    for _ in range(8):
        cand = os.path.join(root, "books", "ai1-cli", "facts")
        if os.path.exists(os.path.join(cand, "facts_store.py")):
            return cand
        root = os.path.dirname(root)
    # also try a sibling top-level facts/ with facts_store
    for _ in range(8):
        if os.path.exists(os.path.join(HERE, "..", "..", "..", "facts", "facts_store.py")):
            return os.path.abspath(os.path.join(HERE, "..", "..", "..", "facts"))
    return None

# ---------- load verdict logs ----------
def load_verdicts():
    rows = []
    for path in sorted(glob.glob(os.path.join(CANCER, "factchecks-*", "verdicts-*.jsonl"))):
        with open(path, encoding="utf-8") as fh:
            for ln, line in enumerate(fh, 1):
                line = line.strip()
                if not line:
                    continue
                try:
                    r = json.loads(line)
                except json.JSONDecodeError as e:
                    print(f"  WARN {os.path.basename(path)}:{ln} bad JSON ({e}) — skipped", file=sys.stderr)
                    continue
                if not r.get("fact_id") or not r.get("verdict"):
                    continue
                r["_file"] = os.path.basename(path)
                rows.append(r)
    return rows

def independent_checkers(verdicts):
    """Collapse checkers sharing a publisher to one vote (keep the highest-tier/confidence)."""
    by_pub = {}
    for v in verdicts:
        pub = CHECKER_PUBLISHER.get(v.get("checker"), v.get("checker"))
        key = pub
        score = (TIER_WEIGHT.get(v.get("tier"), 1.0), v.get("confidence", 0) or 0)
        if key not in by_pub or score > by_pub[key][0]:
            by_pub[key] = (score, v)
    return [v for _, v in by_pub.values()]

# ---------- agreement / bucket ----------
def classify(verdicts):
    """Given the independent verdicts for one claim, return (bucket, agreement_ratio, signed_score)."""
    ind = independent_checkers(verdicts)
    n = len(ind)
    if n == 0:
        return "unchecked", 0.0, 0.0, ind
    any_refute = any(v["verdict"] in ("CONTRADICTED", "OUTDATED") for v in ind)
    # tier-weighted signed score: an FDA REFUTES outweighs several low-tier SUPPORTS
    signed = sum(AGREE[v["verdict"]] * TIER_WEIGHT.get(v.get("tier"), 1.0) for v in ind)
    # agreement ratio over checkers that took a position (exclude UNVERIFIED)
    positioned = [v for v in ind if v["verdict"] != "UNVERIFIED"]
    if positioned:
        top = Counter(v["verdict"] for v in positioned).most_common(1)[0][1]
        agreement = top / len(positioned)
    else:
        agreement = 0.0
    distinct = {v["verdict"] for v in positioned}

    if any_refute and len(distinct) > 1:
        bucket = "conflict"          # someone refutes AND someone supports -> hard human review
    elif any_refute:
        bucket = "refuted"           # all positioned checkers refute/outdate -> likely real error
    elif not positioned:
        bucket = "unverified"        # nobody could verify -> stays candidate
    elif len(distinct) == 1 and len(positioned) >= 2:
        bucket = "clean"             # 2+ independent checkers, same verdict, no refute
    elif len(distinct) > 1:
        bucket = "split"             # checkers disagree (e.g. CONFIRMED vs UNVERIFIED-but-positioned)
    else:
        bucket = "thin"              # only one positioned checker -> weak signal
    return bucket, round(agreement, 3), round(signed, 2), ind

# priority for the human queue (higher = look first)
BUCKET_PRIORITY = {"conflict": 5, "refuted": 4, "split": 3, "thin": 1,
                   "unverified": 1, "clean": 0, "unchecked": 2}

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--record", action="store_true", help="record agreed verdicts into facts/facts.json")
    ap.add_argument("--sample", type=float, default=0.05, help="fraction of CLEAN claims to audit (default 0.05)")
    ap.add_argument("--seed", type=int, default=0)
    args = ap.parse_args()
    random.seed(args.seed)
    os.makedirs(TRIAGE, exist_ok=True)

    claims = {c["fact_id"]: c for c in json.load(open(CLAIMS, encoding="utf-8"))}
    verdicts = load_verdicts()
    if not verdicts:
        sys.exit(f"No verdict logs found under {CANCER}/factchecks-*/verdicts-*.jsonl . "
                 "Run the Claude and Codex prompts first.")
    by_claim = defaultdict(list)
    for v in verdicts:
        by_claim[v["fact_id"]].append(v)

    checkers = sorted({v.get("checker") for v in verdicts})
    rows, buckets = [], Counter()
    coverage = {c: len({v.get("checker") for v in by_claim.get(c, [])}) for c in claims}

    for fid, claim in claims.items():
        vs = by_claim.get(fid, [])
        bucket, agreement, signed, ind = classify(vs)
        buckets[bucket] += 1
        rows.append({
            "fact_id": fid,
            "canonical": claim["canonical"],
            "module": claim.get("evidence", [{}])[0].get("module", ""),
            "n_checkers": len({v.get("checker") for v in vs}),
            "n_independent": len(ind),
            "bucket": bucket,
            "agreement": agreement,
            "signed_score": signed,
            "verdicts": [{"checker": v.get("checker"), "verdict": v["verdict"],
                          "tier": v.get("tier"), "source": v.get("source"),
                          "url": v.get("url", ""), "confidence": v.get("confidence")} for v in vs],
        })

    # audit sample from the clean pile (calibration for correlated errors)
    clean_ids = [r["fact_id"] for r in rows if r["bucket"] == "clean"]
    audit = set(random.sample(clean_ids, max(0, round(len(clean_ids) * args.sample)))) if clean_ids else set()
    for r in rows:
        r["audit_sample"] = r["fact_id"] in audit

    # ---- write ensemble.jsonl ----
    with open(os.path.join(TRIAGE, "ensemble.jsonl"), "w", encoding="utf-8") as fh:
        for r in rows:
            fh.write(json.dumps(r, ensure_ascii=False) + "\n")

    # ---- human queue: conflict + refuted + split + audit sample, by priority ----
    queue = [r for r in rows if r["bucket"] in ("conflict", "refuted", "split") or r["audit_sample"]]
    queue.sort(key=lambda r: (BUCKET_PRIORITY[r["bucket"]], r["n_independent"]), reverse=True)
    ql = [f"# Human review queue — medhavi-cancer ensemble fact-check\n",
          f"_{TODAY} · checkers: {', '.join(checkers)} · {len(claims)} claims · "
          f"{len(queue)} need a human ({len(audit)} of them are clean-pile audit spot-checks)._\n",
          "Reason a person is needed, highest priority first. **Agreement lowers suspicion; it never "
          "certifies truth — only your sign-off does.**\n"]
    reason = {"conflict": "CONFLICT — checkers refute *and* support; do not pick a side blindly",
              "refuted": "REFUTED — every positioned checker says wrong/outdated; likely a real error",
              "split": "SPLIT — checkers disagree",
              "clean": "AUDIT — checkers agreed; spot-check for correlated error"}
    for r in queue:
        tag = "clean" if (r["bucket"] == "clean" or (r["audit_sample"] and r["bucket"] not in reason)) else r["bucket"]
        ql.append(f"### [{r['bucket'].upper()}] {r['fact_id']}")
        ql.append(f"*{r['canonical']}*  \n— {r['module']} · {reason.get(tag, reason.get(r['bucket'],''))}"
                  f" · agreement {r['agreement']} · signed {r['signed_score']}")
        for v in r["verdicts"]:
            ql.append(f"  - **{v['checker']}** → {v['verdict']} "
                      f"({v.get('tier') or '—'}; {v.get('source') or '—'}; {v.get('url') or 'no url'})")
        ql.append("")
    open(os.path.join(TRIAGE, "HUMAN_QUEUE.md"), "w", encoding="utf-8").write("\n".join(ql))

    # ---- ensemble report ----
    cov = Counter(coverage.values())
    rl = [f"# Ensemble fact-check report — medhavi-cancer\n",
          f"_{TODAY} · checkers: {', '.join(checkers)}_\n",
          f"**{len(claims)} claims** in the frozen set. Each claim's verdicts were joined on "
          "`fact_id`, collapsed to independent voters (checkers sharing a publisher count once), "
          "and bucketed.\n",
          "## Coverage\n"]
    for k in sorted(cov):
        rl.append(f"- {cov[k]} claims checked by {k} of {len(checkers)} checkers")
    rl.append("\n## Triage buckets\n")
    order = ["conflict", "refuted", "split", "thin", "unverified", "clean", "unchecked"]
    desc = {"conflict": "refute + support (hard review)", "refuted": "all checkers say wrong/outdated",
            "split": "checkers disagree", "thin": "only one positioned checker",
            "unverified": "nobody could verify", "clean": "2+ independent agree, no refute",
            "unchecked": "no verdicts"}
    for b in order:
        if buckets.get(b):
            rl.append(f"- **{buckets[b]}** {b} — {desc[b]}")
    human = sum(buckets.get(b, 0) for b in ("conflict", "refuted", "split"))
    rl.append(f"\n**{human} claims go to a human on disagreement alone** "
              f"(+{len(audit)} clean-pile audit spot-checks = {human + len(audit)} total in the queue). "
              f"The remaining {buckets.get('clean',0)} clean claims are *less suspect*, not verified.\n")
    rl.append("## Notes on method\n")
    rl.append("- Independence: two runs of the same model are collapsed to one vote (correlated error).")
    rl.append("- Tier weighting: a `trusted` (FDA/NCCN/WHO) verdict outweighs `solid` (PubMed) outweighs `low` (web).")
    rl.append("- A refutation with no source is rejected upstream (the prompts require a url/verbatim).")
    rl.append("- Agreement never sets `verified`; only a human sign-off does (facts/scripts/verify.py).")
    open(os.path.join(TRIAGE, "ENSEMBLE_REPORT.md"), "w", encoding="utf-8").write("\n".join(rl))

    print(f"claims: {len(claims)} · checkers: {', '.join(checkers)}")
    print("buckets: " + ", ".join(f"{b}={buckets[b]}" for b in order if buckets.get(b)))
    print(f"human queue: {human} (+{len(audit)} audit) → {TRIAGE}/HUMAN_QUEUE.md")

    # ---- optional: record agreed verdicts into the shared dictionary ----
    if args.record:
        store_dir = find_facts_store()
        if not store_dir:
            print("  --record: could not locate facts_store.py; skipped.", file=sys.stderr)
            return
        sys.path.insert(0, store_dir)
        import facts_store as fs  # noqa
        facts = fs.load_facts()
        sources = fs.load_sources()
        recorded = 0
        for r in rows:
            if r["bucket"] not in ("clean", "refuted", "conflict"):
                continue
            for v in r["verdicts"]:
                verdict = {"CONFIRMED": "SUPPORTS", "CONTRADICTED": "REFUTES",
                           "OUTDATED": "REFUTES", "UNVERIFIED": None}[v["verdict"]]
                if verdict is None:
                    continue
                if verdict in ("REFUTES",) and not v.get("url"):
                    continue  # unsourced refutation rejected
                ev = {"source": f"{v['checker']}-factcheck", "verdict": verdict,
                      "verbatim": "", "url": v.get("url", ""),
                      "publisher": CHECKER_PUBLISHER.get(v["checker"], v["checker"]),
                      "tier": v.get("tier") or "low"}
                fs.record_evidence(facts, r["canonical"], ev, sources,
                                   canonical=r["canonical"], category="BASIC")
                recorded += 1
        fs.save_facts(facts)
        print(f"  --record: wrote {recorded} evidence items into {store_dir}/facts.json")

if __name__ == "__main__":
    main()
