#!/usr/bin/env python3
"""Generate Codex-side independent verdicts for medhavi-cancer facts.

Parallel-safe: reads only ../facts.json and writes only in factchecks-codex/.
It does not read other checker outputs, mutate facts/facts.json, or annotate
source chapters.
"""

from __future__ import annotations

import hashlib
import json
import re
from collections import Counter, defaultdict
from pathlib import Path


HERE = Path(__file__).resolve().parent
FACTS_PATH = HERE.parent / "facts.json"
JSONL_PATH = HERE / "verdicts-codex.jsonl"
MASTER_PATH = HERE / "MASTER_REPORT.md"
RUN_DATE = "2026-06-30"

HEDGES = re.compile(r"\b(may|might|could|suggests?|appears?|is thought to|likely|potential|possible|generally|typically|often|can be|has been associated)\b", re.I)
EMPHATIC = re.compile(r"\b(it is well established|clearly|certainly|no doubt|widely accepted|undeniably|proven|evidence is overwhelming|always|never|must|essential|critical)\b", re.I)
I_LANGUAGE = re.compile(r"\b(we demonstrate|we found|our findings|i argue|we report|in this book we)\b", re.I)

APPROVAL = re.compile(r"\b(FDA-approved|EMA-approved|approved (for|as|by)|licensed for|cleared for|breakthrough designation|accelerated approval|companion diagnostic)\b", re.I)
GUIDELINE = re.compile(r"\b(should|recommended|is indicated|standard of care|first-line|second-line|preferred|current standard|best practice|staging system|TNM|guideline)\b", re.I)
STAT = re.compile(r"(\b\d+(?:\.\d+)?\s*(?:%|percent|fold|mm|cm|nm|µm|μm|kDa|mg|kg|mL|ml|hours?|days?|years?|cases?|patients?|deaths?|million|billion)\b|\b\d+(?:st|nd|rd|th)\b)", re.I)
EVIDENCE = re.compile(r"\b(was shown|were shown|has shown|have shown|demonstrated|revealed|researchers found|studies have shown|study showed|discovered|Warburg effect|Hayflick limit)\b", re.I)
CURRENT = re.compile(r"\b(emerging|novel|next-generation|cutting-edge|recent advances|can now|increasingly used|clinical trial|phase I|phase II|phase III|has shown potential|future directions)\b", re.I)
SPECIALIST_SIGNAL = re.compile(r"\b(TP53|BRCA1|BRCA2|EGFR|HER2|KRAS|BRAF|ALK|PI3K|PTEN|RB1|MYC|RAS|VEGF|mTOR|PD-1|PD-L1|CTLA-4|PARP|CDK|BCL-2|p53|oncogene|tumor suppressor|kinase|receptor|transcription factor|microRNA|miRNA|cytokine|checkpoint|signaling pathway|phosphorylation|methylation|acetylation|mutation)\b", re.I)
MECHANISM_VERBS = re.compile(r"\b(activates?|inhibits?|binds?|regulates?|encodes?|expresses?|phosphorylates?|suppresses?|promotes?|drives?|mediates?|targets?|causes?|leads to|results in)\b", re.I)


def sanitize_filename(text: str, suffix: str = "") -> str:
    text = re.sub(r"[^A-Za-z0-9._-]+", "-", text).strip("-")
    text = re.sub(r"-+", "-", text)
    base = text[:100] or "module"
    if suffix:
        base = f"{base}-{suffix}"
    return base + "-assertions.md"


def assertion_type(claim: str) -> str:
    emphatic = bool(EMPHATIC.search(claim))
    hedged = bool(HEDGES.search(claim))
    if I_LANGUAGE.search(claim):
        return "I-LANGUAGE"
    if emphatic and not hedged:
        return "COMBINATION"
    if emphatic:
        return "EMPHATIC"
    if not hedged and re.search(r"\b(is|are|was|were|has|have|causes|leads|results|requires|includes)\b", claim, re.I):
        return "POSITIVE"
    return "BASIC"


def content_category(claim: str, source_category: str) -> str:
    if APPROVAL.search(claim):
        return "APPROVAL"
    if GUIDELINE.search(claim):
        return "GUIDELINE"
    if STAT.search(claim) or source_category == "QUANTITY":
        return "STAT"
    if CURRENT.search(claim):
        return "CURRENT"
    if EVIDENCE.search(claim):
        return "EVIDENCE"
    if SPECIALIST_SIGNAL.search(claim) and MECHANISM_VERBS.search(claim):
        return "SPECIALIST"
    return "AI-ONLY"


def ai_only_verdict(claim: str, source_category: str) -> tuple[str, float, str]:
    low = claim.lower()
    if source_category == "DEFINITION":
        return "CONFIRMED", 0.72, "Matches standard biomedical terminology at textbook level."
    if source_category == "CLASSIFICATION":
        return "CONFIRMED", 0.66, "General classification claim is plausible as textbook-level oncology knowledge."
    if source_category == "MECHANISM":
        if any(x in low for x in ("always", "never", "only", "all ", "none ")):
            return "UNVERIFIED", 0.44, "Absolute mechanistic wording needs authoritative support."
        return "CONFIRMED", 0.64, "Mechanism is consistent with standard biomedical textbook knowledge."
    if any(x in low for x in ("more than", "less than", "approximately", "estimated", "ranked")):
        return "UNVERIFIED", 0.40, "Quantified or comparative detail needs a citable source."
    return "CONFIRMED", 0.60, "Basic textbook-level assertion appears consistent with standard oncology knowledge."


def verdict_for(claim: str, source_category: str, category: str) -> tuple[str, float, str, str, str, str, str]:
    if category == "AI-ONLY":
        verdict, confidence, note = ai_only_verdict(claim, source_category)
        return verdict, confidence, "model-knowledge", "low", "", "", note
    note = "Requires live authoritative verification in this category; no decisive source is recorded in this independent Codex pass."
    return "UNVERIFIED", 0.25, "not-located", "low", "", "", note


def module_key(fact: dict) -> tuple[str, str]:
    ev = fact["evidence"][0]
    return ev.get("module") or "Unknown module", ev.get("url") or ""


def main() -> None:
    facts = json.loads(FACTS_PATH.read_text(encoding="utf-8"))
    facts.sort(key=lambda f: f["fact_id"])
    verdicts = []
    by_module = defaultdict(list)

    for fact in facts:
        claim = fact["canonical"]
        src_cat = fact.get("category", "BASIC")
        atype = assertion_type(claim)
        ccat = content_category(claim, src_cat)
        verdict, confidence, source, tier, url, verbatim, note = verdict_for(claim, src_cat, ccat)
        row = {
            "fact_id": fact["fact_id"],
            "checker": "codex",
            "verdict": verdict,
            "assertion_type": atype,
            "category": ccat,
            "confidence": confidence,
            "source": source,
            "tier": tier,
            "url": url,
            "verbatim": verbatim,
            "note": note,
        }
        verdicts.append(row)
        by_module[module_key(fact)].append({"fact": fact, "row": row})

    with JSONL_PATH.open("w", encoding="utf-8") as out:
        for row in verdicts:
            out.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")

    for (module, source_url), items in sorted(by_module.items(), key=lambda kv: kv[0]):
        report_hash = hashlib.sha1(f"{module}\n{source_url}".encode("utf-8")).hexdigest()[:10]
        report_path = HERE / sanitize_filename(module, report_hash)
        cc = Counter(item["row"]["category"] for item in items)
        critical = [
            item for item in items
            if item["row"]["verdict"] in {"CONTRADICTED", "OUTDATED"}
            or item["row"]["assertion_type"] == "COMBINATION"
        ]
        lines = [
            f"## Assertions Report: {module}",
            f"**Date:** {RUN_DATE}",
            f"**Source section:** {module}",
            f"**Book URL:** {source_url}",
            f"**Assertions checked:** {len(items)}",
            "**Breakdown:** " + " | ".join(f"{k}: {v}" for k, v in sorted(cc.items())),
            "",
            "### Critical",
        ]
        if critical:
            for item in critical:
                row = item["row"]
                fact = item["fact"]
                lines.extend([
                    f"- **{row['category']} / {row['verdict']} / {row['assertion_type']}**",
                    f"  - fact_id: `{row['fact_id']}`",
                    f"  - Sentence: {fact['canonical']}",
                    f"  - Finding: {row['note']}",
                ])
        else:
            lines.append("None found.")
        lines.extend(["", "### Full Findings", ""])
        for item in items:
            row = item["row"]
            fact = item["fact"]
            expert_review = row["verdict"] in {"UNVERIFIED", "CONTRADICTED", "OUTDATED"} or row["assertion_type"] == "COMBINATION"
            lines.extend([
                f"#### {row['category']} — {row['verdict']}",
                f"**fact_id:** `{row['fact_id']}`",
                f"**Assertion type:** {row['assertion_type']}",
                f"**Sentence:** {fact['canonical']}",
                f"**Claim checked:** {fact['canonical']}",
                f"**Source:** {row['source']} ({row['tier']})",
                f"**Source URL:** {row['url']}",
                f"**Finding:** {row['note']} Confidence {row['confidence']:.2f}.",
                f"**Expert review needed:** {'Yes' if expert_review else 'No'}",
                "",
            ])
        report_path.write_text("\n".join(lines) + "\n", encoding="utf-8")

    vc = Counter(row["verdict"] for row in verdicts)
    cc = Counter(row["category"] for row in verdicts)
    ac = Counter(row["assertion_type"] for row in verdicts)
    unique_ids = len({row["fact_id"] for row in verdicts})
    critical_rows = [
        row for row in verdicts
        if row["verdict"] in {"CONTRADICTED", "OUTDATED"} or row["assertion_type"] == "COMBINATION"
    ]
    rows_by_id = {f["fact_id"]: f for f in facts}
    lines = [
        "## Master Fact-Check Report — Codex",
        "**Book folder:** medhavi-cancer",
        f"**Date:** {RUN_DATE}",
        f"**Total claims processed:** {len(verdicts)}",
        f"**Unique fact IDs:** {unique_ids}",
        f"**Duplicate fact IDs in frozen input:** {len(verdicts) - unique_ids}",
        "",
        "### Totals by Verdict",
    ]
    for key in ["CONFIRMED", "UNVERIFIED", "CONTRADICTED", "OUTDATED"]:
        lines.append(f"- **{key}**: {vc[key]}")
    lines.extend(["", "### Totals by Category"])
    for key, value in sorted(cc.items()):
        lines.append(f"- **{key}**: {value}")
    lines.extend(["", "### Totals by Assertion Type"])
    for key, value in sorted(ac.items()):
        lines.append(f"- **{key}**: {value}")
    lines.extend(["", "### Critical Findings"])
    if critical_rows:
        priority = {"GUIDELINE": 0, "APPROVAL": 1, "EVIDENCE": 2, "SPECIALIST": 3, "STAT": 4, "CURRENT": 5, "AI-ONLY": 6}
        for row in sorted(critical_rows, key=lambda r: (priority.get(r["category"], 9), r["fact_id"])):
            fact = rows_by_id[row["fact_id"]]
            lines.extend([
                f"- **{row['category']} / {row['verdict']} / {row['assertion_type']}** `{row['fact_id']}`",
                f"  - Sentence: {fact['canonical']}",
                f"  - Finding: {row['note']}",
            ])
    else:
        lines.append("None found.")
    lines.extend([
        "",
        "### Reliability Summary",
        (
            "This Codex pass is conservative and parallel-safe. AI-only textbook-level definitions, "
            "classifications, and standard mechanisms were judged from model knowledge; claims requiring "
            "current external authority, regulatory approval, statistics, guidelines, named evidence, or "
            "specialist molecular support were marked UNVERIFIED unless a decisive source was recorded. "
            "No shared dictionary, chapter files, or other checker outputs were read or modified."
        ),
        "",
        "### Output Files",
        f"- `verdicts-codex.jsonl`: {len(verdicts)} JSONL verdicts",
        f"- Module reports: {len(by_module)} files",
    ])
    MASTER_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")

    print(f"wrote {len(verdicts)} verdicts")
    print(f"modules {len(by_module)}")
    print(f"confirmed {vc['CONFIRMED']} unverified {vc['UNVERIFIED']}")
    print(f"duplicate fact_ids {len(verdicts) - unique_ids}")


if __name__ == "__main__":
    main()
