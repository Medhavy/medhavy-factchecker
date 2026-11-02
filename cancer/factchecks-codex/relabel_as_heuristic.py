#!/usr/bin/env python3
"""Relabel the Codex pass as HEURISTIC TRIAGE, not fact-checking.

Why: generate_codex_verdicts.py assigns every verdict from regexes over the claim text.
No source was consulted: every row has url "" and verbatim "". "CONFIRMED" therefore means
"matched no suspicious pattern", not "an authoritative source supports this".

What this does (idempotent, nothing is lost):
  verdicts-codex.jsonl  ->  heuristic-triage-codex.jsonl
      checker   codex            -> codex-heuristic
      verdict   CONFIRMED        -> heuristic_result PLAUSIBLE   (original kept as original_verdict)
                UNVERIFIED       -> heuristic_result NOT_CHECKED (original kept as original_verdict)
      adds kind="heuristic-triage", evidence_found=false
      The new name no longer matches merge_verdicts.py's  factchecks-*/verdicts-*.jsonl  glob,
      so the merge step cannot count these rows as a checker's vote.
  *-assertions.md and MASTER_REPORT.md: headings relabelled and a banner added.

Restore everything with:  git checkout -- . && rm heuristic-triage-codex.jsonl  (inside this folder).
"""
import glob, json, os, re
from pathlib import Path

HERE = Path(__file__).resolve().parent
OLD, NEW = HERE / "verdicts-codex.jsonl", HERE / "heuristic-triage-codex.jsonl"
MAP = {"CONFIRMED": "PLAUSIBLE", "UNVERIFIED": "NOT_CHECKED",
       "CONTRADICTED": "CONTRADICTED", "OUTDATED": "OUTDATED"}
LABEL = {"PLAUSIBLE": "PLAUSIBLE (rule-based, no source)",
         "NOT_CHECKED": "NOT CHECKED (needs a database)"}
BANNER_MARK = "<!-- heuristic-triage-banner -->"
BANNER = (f"{BANNER_MARK}\n"
          "> **Heuristic triage, not fact-checking.** These labels came from word-pattern rules in "
          "`generate_codex_verdicts.py`. No source was consulted: no URL, no quoted passage. "
          "PLAUSIBLE means the sentence matched no suspicious pattern. It does not mean a source "
          "supports it. NOT CHECKED means a database lookup is still needed. See `README-HEURISTIC.md`.\n\n")

# ---- 1. jsonl ----
if OLD.exists():
    rows = [json.loads(l) for l in OLD.read_text(encoding="utf-8").splitlines() if l.strip()]
    out = []
    for r in rows:
        v = r.pop("verdict")
        r["checker"] = "codex-heuristic"
        r["original_verdict"] = v
        r["heuristic_result"] = MAP[v]
        r["kind"] = "heuristic-triage"
        r["evidence_found"] = bool(r.get("url") or r.get("verbatim"))
        out.append(r)
    NEW.write_text("".join(json.dumps(r, ensure_ascii=False, sort_keys=True) + "\n" for r in out),
                   encoding="utf-8")
    back = [json.loads(l) for l in NEW.read_text(encoding="utf-8").splitlines() if l.strip()]
    assert len(back) == len(rows) and {r["fact_id"] for r in back} == {r["fact_id"] for r in rows}
    OLD.unlink()   # content fully preserved in NEW (original_verdict + every other field)
    print(f"jsonl: {len(rows)} rows -> {NEW.name}")
else:
    print("jsonl: already relabelled")

# ---- 2. markdown reports ----
def relabel_text(t):
    for src, dst in (("CONFIRMED", "PLAUSIBLE"), ("UNVERIFIED", "NOT_CHECKED")):
        t = re.sub(rf"^(#### .+? — ){src}$", lambda m: m.group(1) + LABEL[dst], t, flags=re.M)
        t = re.sub(rf"^(- \*\*[A-Z-]+ / ){src}( / [A-Z-]+\*\*)", lambda m: m.group(1) + dst + m.group(2), t, flags=re.M)
    return t

n = 0
for p in sorted(glob.glob(str(HERE / "*-assertions.md"))):
    t = Path(p).read_text(encoding="utf-8")
    t2 = relabel_text(t)
    t2 = t2.replace("\n### Critical\n", "\n### Flagged by the rules (emphatic wording with no hedge; not an error finding)\n")
    if BANNER_MARK not in t2:
        t2 = BANNER + t2
    if t2 != t:
        Path(p).write_text(t2, encoding="utf-8"); n += 1
print(f"assertion reports touched: {n}")

mp = HERE / "MASTER_REPORT.md"
t = mp.read_text(encoding="utf-8")
t2 = relabel_text(t)
t2 = t2.replace("## Master Fact-Check Report — Codex", "## Heuristic Triage Report — Codex pass (rule-based, not fact-checking)")
t2 = t2.replace("### Totals by Verdict", "### Totals by Rule Result")
t2 = t2.replace("- **CONFIRMED**:", "- **PLAUSIBLE (rule-based, no source)**:")
t2 = t2.replace("- **UNVERIFIED**:", "- **NOT CHECKED (needs a database)**:")
t2 = t2.replace("- **CONTRADICTED**:", "- **CONTRADICTED** (the rules never assign this):")
t2 = t2.replace("- **OUTDATED**:", "- **OUTDATED** (the rules never assign this):")
t2 = t2.replace("`verdicts-codex.jsonl`", "`heuristic-triage-codex.jsonl`")
t2 = t2.replace("### Critical Findings", "### Flagged by the rules (COMBINATION = emphatic wording with no hedge; not an error finding)")
if BANNER_MARK not in t2:
    t2 = BANNER + t2
if t2 != t:
    mp.write_text(t2, encoding="utf-8"); print("MASTER_REPORT.md relabelled")

# ---- 3. README ----
rd = HERE / "README-HEURISTIC.md"
if not rd.exists():
    rd.write_text("""# Read this first: the Codex pass is heuristic triage, not fact-checking

`generate_codex_verdicts.py` assigns every row from regexes over the claim text. It never consulted a source.

| Field | Value across all 3,165 rows |
|---|---|
| `url` | empty |
| `verbatim` (quoted passage) | empty |
| `source` | `model-knowledge` (2,607) or `not-located` (558) |
| `tier` | `low` |

- **PLAUSIBLE** (was CONFIRMED, 2,562 rows): the sentence matched no suspicious pattern. It is *not* evidence the claim is true.
- **NOT CHECKED** (was UNVERIFIED, 603 rows): statistics, guidelines, approvals, named evidence or specialist claims that still need a database lookup.
- The rules never produce CONTRADICTED or OUTDATED.
- 2,010 rows share one canned sentence as their "finding".
- About 31% of the PLAUSIBLE rows are not assertions at all (see `../../assertion-triage/SUMMARY.md`).

The data file was renamed `verdicts-codex.jsonl` -> `heuristic-triage-codex.jsonl` (no longer matched by `merge_verdicts.py`'s `factchecks-*/verdicts-*.jsonl` glob), so these rows cannot be counted as a checker's vote or recorded into the shared dictionary. The old verdict is kept in each row as `original_verdict`.

Re-running `generate_codex_verdicts.py` regenerates the old labels; run `relabel_as_heuristic.py` afterwards.
""", encoding="utf-8")
    print("wrote README-HEURISTIC.md")
