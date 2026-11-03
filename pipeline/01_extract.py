#!/usr/bin/env python3
"""01_extract.py — step 1 of the evidence-first pipeline: pull candidate claims out of a textbook.

Deterministic (no language model in the loop). Reads the medhavi-cancer book and writes:

  data/cancer/terms.json    one entry per glossary term           (from data/keywords.json)
  data/cancer/graph.json    concept graph from term co-mention in definitions
  data/cancer/facts.json    CANDIDATE CLAIMS scoured from the chapter prose (content/docs/**/*.mdx)
  data/cancer/preview.md    human-readable summary

Each candidate carries:
  claim_origin   where the BOOK made the claim (module, url, the verbatim sentence). This is
                 provenance of the claim, NOT evidence for it: a book cannot vouch for itself.
  evidence       [] — filled later, by database lookups only (see README.md).
  status         "no_evidence" until evidence records exist.

Usage:  python3 pipeline/01_extract.py [path/to/medhavi-cancer]
        (default: ../medhavi-cancer next to this repo, or $MEDHAVI_CANCER)
"""
import json, os, re, glob, datetime, sys
from collections import defaultdict, Counter
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
BOOK = Path(sys.argv[1] if len(sys.argv) > 1
            else os.environ.get("MEDHAVI_CANCER") or REPO.parent / "medhavi-cancer").resolve()
DOCS = BOOK / "content" / "docs"
KEYWORDS = BOOK / "data" / "keywords.json"
OUT = REPO / "data" / "cancer"
TODAY = datetime.date.today().isoformat()
SLICE, PUBLISHER, SOURCE = "cancer", "medhavi", "medhavi-cancer"
URL_BASE = "/glossary/"
if not (DOCS.is_dir() and KEYWORDS.is_file()):
    sys.exit(f"not a medhavi-cancer checkout: {BOOK}\n(expected content/docs and data/keywords.json)")
OUT.mkdir(parents=True, exist_ok=True)

# ───────────────────────── helpers ─────────────────────────
def slugify(s):
    s = re.sub(r"[^\w\s-]", "", s.lower())
    return re.sub(r"[\s_-]+", "-", s).strip("-")[:80] or "x"

def normalize(s):
    return re.sub(r"\s+", " ", re.sub(r"[^\w\s]", "", s.lower())).strip()

# ───────────────────────── terms + graph (glossary) ─────────────────────────
kw = json.load(open(KEYWORDS, encoding="utf-8"))
records = []
for slug, v in kw.items():
    term = (v.get("term") or "").strip()
    if not term: continue
    records.append({"slug": slug, "term": term,
                    "definition": (v.get("definition") or "").strip(),
                    "category": (v.get("category") or "").strip() or "Uncategorized"})
records.sort(key=lambda r: r["term"].lower())
def url_for(slug): return URL_BASE + slug

term_by_lower = {}
for r in records:
    lt = r["term"].lower()
    if len(lt) >= 4 and not lt.isdigit():
        term_by_lower.setdefault(lt, r["term"])
MAXN = 4
word_re = re.compile(r"[A-Za-z0-9][A-Za-z0-9\-']*")
def mentions(definition, self_term):
    found, seen = [], set()
    toks = word_re.findall(definition.lower()); n = len(toks)
    for i in range(n):
        for k in range(MAXN, 0, -1):
            if i + k > n: continue
            canon = term_by_lower.get(" ".join(toks[i:i+k]))
            if canon and canon.lower() != self_term.lower() and canon not in seen:
                seen.add(canon); found.append(canon); break
    return found

related_map, edges, indeg = {}, [], defaultdict(int)
for r in records:
    rel = mentions(r["definition"], r["term"])
    related_map[r["term"]] = rel
    for tgt in rel:
        edges.append([r["term"], tgt]); indeg[tgt] += 1

terms = [{"term": r["term"], "page": r["term"], "url": url_for(r["slug"]),
          "definition": r["definition"] or None, "categories": [r["category"]],
          "related": related_map[r["term"]], "media": []} for r in records]
json.dump(terms, open(f"{OUT}/terms.json", "w", encoding="utf-8"), indent=2, ensure_ascii=False)
nodes = [{"term": r["term"], "page": r["term"], "url": url_for(r["slug"]),
          "in_degree": indeg.get(r["term"], 0)} for r in records]
json.dump({"nodes": nodes, "edges": edges},
          open(f"{OUT}/graph.json", "w", encoding="utf-8"), indent=2, ensure_ascii=False)

# ───────────────────────── scour chapter prose for candidate claims ─────────────────────────
def strip_mdx(t):
    t = re.sub(r"^---.*?---\s*", "", t, flags=re.S)
    t = re.sub(r"```.*?```", " ", t, flags=re.S)
    t = re.sub(r"`[^`]*`", " ", t)
    t = re.sub(r"!\[[^\]]*\]\([^)]*\)", " ", t)
    t = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", t)
    t = re.sub(r"<[^>]+>", " ", t)
    t = re.sub(r"[*_>#|]", " ", t)
    return t
def frontmatter_title(raw, fallback):
    m = re.search(r'^title:\s*"?(.+?)"?\s*$', raw, flags=re.M)
    return (m.group(1).strip() if m else fallback)

SENT = re.compile(r'(?<=[.!?])\s+(?=[A-Z0-9"(])')
SKIP_START = re.compile(r'^(This|These|Those|It|They|Such|Here|We|I|In this|For example|For instance|'
                        r'However|According|As (noted|described|shown|discussed|mentioned)|In contrast|'
                        r'Although|Though|Thus|Therefore|Moreover|Furthermore|Additionally|Also|'
                        r'Both|Other|One|Some|Many|Their|His|Her|Its|First|Second|Third|Finally|'
                        r'Notably|Importantly|Interestingly|Recent|Currently|Today|Figure|Table|Chapter|'
                        r'Example|Examples|Unlike|Despite|While|When|If|Once|After|Before|Because)\b')
# sentences truncated at an abbreviation period (e.g. "...physician Dr.") or an initial
ABBR_END = re.compile(r'\b(Dr|Mr|Mrs|Ms|Prof|St|vs|cf|e\.g|i\.e|Fig|No|al|Inc|Ltd|approx|[A-Z])\.\s*$')
FACT_VERB = re.compile(r'\b(is|are|was|were|consists?|contains?|includes?|comprises?|causes?|caused|'
                       r'results?|leads?|leading|binds?|regul=?ates?|regulates?|encodes?|produces?|'
                       r'inhibits?|activates?|requires?|occurs?|involves?|refers?|represents?|forms?|'
                       r'enables?|prevents?|increases?|decreases?|expresses?|associated|characterized|'
                       r'defined|derived|known as|composed|mediated|responsible|plays?|functions?|'
                       r'develops?|arises?|promotes?|suppress(es|ed)?|targets?|treats?|affects?)\b', re.I)
ATTRIB = re.compile(r'\b(according to|as noted|as described|as shown|et al\.?|in this (chapter|section)|'
                    r'this (chapter|section|figure|table))\b', re.I)

def categorize(s):
    if re.search(r'\d', s) and re.search(r'(%|percent|mm|cm|µm|nm|kDa|mg|kg|ml|μL|hours?|days?|years?|fold|°)', s):
        return "QUANTITY"
    if re.search(r'\b(causes?|results? in|leads? to|activates?|inhibits?|binds?|regulates?|mediated|'
                 r'promotes?|suppress)', s, re.I):
        return "MECHANISM"
    if re.search(r'\b(is|are)\b.+\b(defined|known as|type of|class of|form of|refers? to|a process|'
                 r'a (group|family|category))', s, re.I):
        return "DEFINITION"
    if re.search(r'\b(classified|categories|subtypes?|grades?|stages?|types? of)\b', s, re.I):
        return "CLASSIFICATION"
    return "BASIC"

files = sorted(glob.glob(str(DOCS / "**" / "*.mdx"), recursive=True))
candidates, seen_norm = [], set()
raw_count = 0
for path in files:
    rel = os.path.relpath(path, DOCS)                  # e.g. Chapter1/1_Introduction_to_Cells.mdx
    chap = rel.split(os.sep)[0]
    raw = open(path, encoding="utf-8").read()
    title = frontmatter_title(raw, rel)
    route = "/docs/" + rel[:-4]                          # strip .mdx
    body = strip_mdx(raw)
    for para in body.split("\n"):
        para = para.strip()
        if len(para) < 40: continue
        for s in SENT.split(para):
            s = re.sub(r"\s+", " ", s).strip().strip('"')
            if not s: continue
            raw_count += 1
            if not (40 <= len(s) <= 300): continue
            if not re.match(r'^[A-Z0-9]', s): continue   # must start with a letter/digit, not punctuation
            if not s.endswith(('.', '!')): continue
            if s.endswith(':'): continue
            if ABBR_END.search(s): continue              # truncated at an abbreviation/initial
            if SKIP_START.match(s): continue
            if ATTRIB.search(s): continue
            if not FACT_VERB.search(s): continue
            if s.count(',') > 6: continue                # over-long compound — skip
            if s.count(')') != s.count('('): continue    # unbalanced parens = mid-sentence fragment
            if re.search(r'\b(we|our|you|they|these|this)\b', s[:25], re.I): continue
            nm = normalize(s)
            if len(nm) < 20: continue
            if nm in seen_norm: continue                 # same claim repeated in the book
            seen_norm.add(nm)
            candidates.append({
                "fact_id": slugify(SLICE + "-" + s),
                "canonical": s,
                "domain": [SLICE, chap.lower()],
                "stable": True,
                "category": categorize(s),
                "claim_origin": {                         # where the book said it — NOT evidence
                    "source": SOURCE, "publisher": PUBLISHER, "book": SOURCE,
                    "module": title, "url": route,
                    "verbatim": s, "retrieved": TODAY,
                },
                "evidence": [],                           # database records only, added by later steps
                "status": "no_evidence",
            })

# guarantee unique fact_ids (the join key for every later step)
seen_ids = {}
for fact in candidates:
    fid = fact["fact_id"]
    if fid in seen_ids:
        seen_ids[fid] += 1
        fact["fact_id"] = f"{fid}-{seen_ids[fid]}"
    else:
        seen_ids[fid] = 0
assert len({f["fact_id"] for f in candidates}) == len(candidates), "fact_id collision remains"

json.dump(candidates, open(f"{OUT}/facts.json", "w", encoding="utf-8"), indent=2, ensure_ascii=False)

# ───────────────────────── preview.md ─────────────────────────
top = sorted(nodes, key=lambda x: x["in_degree"], reverse=True)[:20]
pl = []
pl.append("# Cancer / Oncology — candidate claims from medhavi-cancer\n")
pl.append("Extracted deterministically (no AI) from the medhavi-cancer book:")
pl.append("- **terms & concept graph** from the book's curated keyword glossary (`data/keywords.json`)")
pl.append("- **candidate claims** scoured from the chapter prose (`content/docs/**/*.mdx`)\n")
pl.append(f"**{len(terms)} terms · {len(edges)} concept links · {len(candidates)} candidate claims.** "
          "Definitions are the book's glossary entries, verbatim; candidate claims are verbatim chapter "
          "sentences. A candidate is not a fact: `evidence` is empty until a database record is attached.\n")
pl.append("## Most-connected concepts (a prerequisite/foundation signal)\n")
for t in top:
    pl.append(f"- **{t['term']}** — mentioned in {t['in_degree']} other term definitions · {t['url']}")
pl.append("")
pl.append("## Candidate-claim sample (first 25 scoured from chapters)\n")
for f in candidates[:25]:
    pl.append(f"- *{f['canonical']}*  \n  — {f['claim_origin']['module']} · `{f['category']}` · {f['status']}")
pl.append("")
pl.append("## Glossary sample (alphabetical, first 20)\n")
for t in terms[:20]:
    pl.append(f"### {t['term']}")
    pl.append(t["definition"] or "*(no definition)*")
    pl.append("")
    pl.append(f"- page: {t['url']} · category: {', '.join(t['categories'])}")
    if t["related"]:
        pl.append(f"- related: {', '.join(t['related'][:10])}")
    pl.append("")
open(f"{OUT}/preview.md", "w", encoding="utf-8").write("\n".join(pl))

print(f"terms.json : {len(terms)} terms")
print(f"graph.json : {len(nodes)} nodes, {len(edges)} edges")
print(f"facts.json : {len(candidates)} candidate claims (from {raw_count} raw sentences)")
print(f"written to : {OUT}")
