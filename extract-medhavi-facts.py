#!/usr/bin/env python3
"""scour_and_match.py — build the medhavi-cancer knowledge slice AND reconcile it
with the shared facts dictionary.

Two jobs, both deterministic (no language model in the loop):

  A) Build the 4-file slice (schema-compatible with facts/biology/):
       terms.json  — one entry per glossary term  (from data/keywords.json)
       graph.json  — concept graph from term co-mention in definitions
       facts.json  — CANDIDATE FACTS scoured from the chapter PROSE (content/docs/**/*.mdx)
       preview.md  — human-readable summary for expert review

  B) Match every scoured candidate against the shared dictionary facts/facts.json
     using the same deterministic merge/consensus logic as extract-facts.py
     (difflib wording-similarity + numeric guard). The master file is NOT mutated;
     corroborations/conflicts are recorded into the slice and a match-report.md.

     1 source                -> consensus "unverified" (candidate)
     2+ independent sources   -> consensus "agreement"   (corroborated)
     same wording, diff number-> kept separate, needs_review (numeric conflict)
     a refuting source        -> consensus "conflict"     (human queue)
"""
import json, os, re, glob, datetime, difflib, sys
from collections import defaultdict, Counter
from pathlib import Path

BOOK  = Path(__file__).resolve().parents[1]
ROOT  = BOOK.parents[1]
FACT_STORE_DIR = ROOT / "books" / "ai1-cli" / "facts"
sys.path.insert(0, str(FACT_STORE_DIR))
import facts_store as fs  # noqa: E402

BOOK  = str(BOOK)
ROOT  = str(ROOT)
DOCS  = os.path.join(BOOK, "content/docs")
KEYWORDS = os.path.join(BOOK, "data/keywords.json")
MASTER   = os.path.join(ROOT, "facts/facts.json")          # shared dictionary (read-only)
OUT   = os.path.join(BOOK, "medhavi-facts/cancer")
TODAY = datetime.date.today().isoformat()
SLICE, PUBLISHER, SOURCE = "cancer", "medhavi", "medhavi-cancer"
SOURCES = fs.load_sources(str(FACT_STORE_DIR / "facts-sources.yaml"))
TIER, _ = fs.source_meta("textbook", SOURCES)
URL_BASE = "/glossary/"
os.makedirs(OUT, exist_ok=True)

# ───────────────────────── shared helpers ─────────────────────────
def slugify(s):
    s = re.sub(r"[^\w\s-]", "", s.lower())
    return re.sub(r"[\s_-]+", "-", s).strip("-")[:80] or "x"

def normalize(s):
    return re.sub(r"\s+", " ", re.sub(r"[^\w\s]", "", s.lower())).strip()

_STOP = set("a an the is are was were be been being of to in on at by for with as that this these "
            "those it its and or not from into within can may will which who whose".split())
def _tokens(s):
    return [t for t in re.findall(r"[a-z]+", s.lower()) if t not in _STOP]
def numbers(s):
    return set(re.findall(r"\d+(?:\.\d+)?", s))
def _strip_numbers(s):
    return re.sub(r"\d+(?:\.\d+)?", "", s)
def wording_similarity(a, b):
    ta, tb = _tokens(_strip_numbers(a)), _tokens(_strip_numbers(b))
    if not ta or not tb: return 0.0
    seq = difflib.SequenceMatcher(None, " ".join(sorted(ta)), " ".join(sorted(tb))).ratio()
    A, B = set(ta), set(tb)
    jac = len(A & B) / len(A | B)
    return 0.5 * seq + 0.5 * jac
MERGE_THRESHOLD, NEAR_THRESHOLD = fs.MERGE_THRESHOLD, fs.NEAR_THRESHOLD

def recompute_consensus(fact):
    ev = fact["evidence"]
    supporters = {e["source"] for e in ev if e.get("verdict") == "SUPPORTS"}
    publishers = {(e.get("publisher") or e["source"]) for e in ev if e.get("verdict") == "SUPPORTS"}
    has_refute  = any(e.get("verdict") == "REFUTES"  for e in ev)
    has_partial = any(e.get("verdict") == "PARTIAL"  for e in ev)
    votes = len(supporters)
    if has_refute:                       c = "conflict"
    elif votes >= 2:                     c = "agreement"
    elif has_partial and votes >= 1:     c = "partial"
    else:                                c = "unverified"
    fact["votes"] = votes
    fact["consensus"] = c
    fact["same_publisher"] = (len(publishers) <= 1)
    fact["needs_review"] = (c == "conflict")
    return fact

# ───────────────────────── A1: terms + graph (glossary) ─────────────────────────
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

# ───────────────────────── A2: scour chapter prose for candidate facts ─────────────────────────
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

files = sorted(glob.glob(os.path.join(DOCS, "**/*.mdx"), recursive=True))
candidates, seen_norm = [], {}
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
            if nm in seen_norm:                          # same claim repeated in the book
                ev = seen_norm[nm]["evidence"][0]
                continue
            fact = fs.make_fact(
                {
                    "canonical": s,
                    "verbatim": s,
                    "domain": [SLICE, chap.lower()],
                    "stable": True,
                    "category": categorize(s),
                },
                {
                    "source": SOURCE,
                    "publisher": PUBLISHER,
                    "book": SOURCE,
                    "repo": None,
                    "module": title,
                    "url": route,
                },
                TIER,
                SOURCES,
            )
            fact["fact_id"] = slugify(SLICE + "-" + s)
            candidates.append(fact)
            seen_norm[nm] = fact

# ───────────────────────── B: match candidates against the shared dictionary ─────────────────────────
master = json.load(open(MASTER, encoding="utf-8"))
master_norm = [(normalize(f["canonical"]), f) for f in master]
# inverted index: content token -> set of master indices, to avoid all-pairs comparison
m_tokens = [set(_tokens(_strip_numbers(f["canonical"]))) for f in master]
inv = defaultdict(set)
for i, toks in enumerate(m_tokens):
    for t in toks:
        inv[t].add(i)

actions = Counter()
corroborations = []   # (cancer_fact, master_fact)
conflicts = []
near_misses = []      # (sim, cancer_canonical, master_canonical) below NEAR_THRESHOLD
for fact in candidates:
    can = fact["canonical"]
    cn = normalize(can)
    cand_toks = set(_tokens(_strip_numbers(can)))
    # only consider master facts sharing >=2 content tokens (or exact normalized match)
    shortlist = Counter()
    for t in cand_toks:
        for i in inv.get(t, ()):
            shortlist[i] += 1
    cand_idx = [i for i, c in shortlist.items() if c >= 2]
    best_sim, best = 0.0, None
    for i in cand_idx:
        mn, mf = master_norm[i]
        sim = 1.0 if mn == cn else wording_similarity(can, mf["canonical"])
        if sim > best_sim:
            best_sim, best = sim, mf
    if best is not None and best_sim >= MERGE_THRESHOLD:
        if numbers(can) == numbers(best["canonical"]):
            # corroboration: import the master's supporting evidence -> 2 publishers -> agreement
            sig = {(e["source"], e.get("module")) for e in fact["evidence"]}
            for e in best["evidence"]:
                if (e["source"], e.get("module")) not in sig:
                    fact["evidence"].append(dict(e))
            fact["matched_dictionary_fact"] = best["fact_id"]
            recompute_consensus(fact)
            actions["corroborated (agreement)"] += 1
            corroborations.append((fact, best))
        else:
            fact["needs_review"] = True
            fact["numeric_conflict_with"] = best["fact_id"]
            actions["numeric-conflict (review)"] += 1
            conflicts.append((fact, best))
    elif best is not None and best_sim >= NEAR_THRESHOLD:
        fact["needs_review"] = True
        fact["possible_duplicate_of"] = best["fact_id"]
        fact["match_similarity"] = round(best_sim, 3)
        actions["near-duplicate (review)"] += 1
    else:
        actions["new to dictionary"] += 1
        if best is not None:
            near_misses.append((best_sim, can, best["canonical"]))

near_misses.sort(reverse=True)

# guarantee unique fact_ids (the join key for the ensemble fact-checkers)
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

# ───────────────────────── match-report.md ─────────────────────────
rl = []
rl.append("# medhavi-cancer ↔ shared dictionary — match report\n")
rl.append(f"Scoured **{len(candidates)} candidate facts** from {len(files)} chapter sections "
          f"(out of {raw_count} raw sentences), then matched each against the shared dictionary "
          f"`facts/facts.json` ({len(master)} facts) using deterministic wording-similarity "
          "(difflib + Jaccard, numeric guard). The master dictionary was **not** modified.\n")
rl.append("## Outcome\n")
for k, v in actions.most_common():
    rl.append(f"- **{v}** — {k}")
rl.append("")
cat = Counter(f["category"] for f in candidates)
rl.append("## Candidate facts by category\n")
for k, v in cat.most_common():
    rl.append(f"- {k}: {v}")
rl.append("")
if corroborations:
    rl.append("## Corroborations (cancer fact ↔ existing dictionary fact → agreement)\n")
    for cf, mf in corroborations[:40]:
        rl.append(f"- cancer: *{cf['canonical']}*")
        rl.append(f"  - dictionary [{mf['evidence'][0]['source']}]: *{mf['canonical']}*")
    rl.append("")
if conflicts:
    rl.append("## Numeric conflicts (same wording, different number → human review)\n")
    for cf, mf in conflicts[:40]:
        rl.append(f"- cancer: *{cf['canonical']}*")
        rl.append(f"  - dictionary: *{mf['canonical']}*")
    rl.append("")
if not corroborations and not conflicts:
    rl.append("## Note\n")
    rl.append(f"No candidate reached the merge threshold ({MERGE_THRESHOLD}) or near-duplicate "
              f"threshold ({NEAR_THRESHOLD}). The shared dictionary currently holds only "
              f"{len(master)} facts from one OpenStax anatomy book, so genuine overlap is small and "
              "the two books phrase shared topics differently. The closest sub-threshold pairs are "
              "listed below so an expert can judge whether any are in fact the same claim (and the "
              "dictionary would grow as more books are added).\n")
if near_misses:
    rl.append("## Closest sub-threshold pairs (topically related, not auto-merged)\n")
    for s, c, m in near_misses[:25]:
        rl.append(f"- **{s:.2f}** cancer: *{c}*")
        rl.append(f"  - dictionary: *{m}*")
    rl.append("")
open(f"{OUT}/match-report.md", "w", encoding="utf-8").write("\n".join(rl))

# ───────────────────────── preview.md ─────────────────────────
n_media = 0
top = sorted(nodes, key=lambda x: x["in_degree"], reverse=True)[:20]
pl = []
pl.append("# Cancer / Oncology — medhavi-cancer knowledge slice (for expert review)\n")
pl.append("Auto-extracted, deterministically (no AI), from the medhavi-cancer book:")
pl.append("- **terms & concept graph** from the book's curated keyword glossary (`data/keywords.json`)")
pl.append("- **facts** scoured from the chapter prose (`content/docs/**/*.mdx`) and matched against the "
          "shared dictionary (`facts/facts.json`)\n")
pl.append(f"**{len(terms)} terms · {len(edges)} concept links · {len(candidates)} candidate facts · "
          f"{n_media} media refs.** Definitions are the book's glossary entries, verbatim; candidate "
          "facts are verbatim chapter sentences. Please flag anything wrong.\n")
agree = sum(1 for f in candidates if f["consensus"] == "agreement")
review = sum(1 for f in candidates if f.get("needs_review"))
pl.append("## Reconciliation with the shared dictionary\n")
pl.append(f"- {agree} candidate facts corroborate an existing dictionary fact (→ consensus *agreement*, "
          "two independent publishers)")
pl.append(f"- {review} flagged for human review (numeric conflict or possible duplicate)")
pl.append(f"- {len(candidates) - agree - review} are new single-source candidates (consensus *unverified*)")
pl.append("- See `match-report.md` for the itemized matches.\n")
pl.append("## Most-connected concepts (a prerequisite/foundation signal)\n")
for t in top:
    pl.append(f"- **{t['term']}** — mentioned in {t['in_degree']} other term definitions · {t['url']}")
pl.append("")
pl.append("## Candidate-fact sample (first 25 scoured from chapters)\n")
for f in candidates[:25]:
    pl.append(f"- *{f['canonical']}*  \n  — {f['evidence'][0]['module']} · `{f['category']}` · {f['consensus']}")
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
print(f"facts.json : {len(candidates)} candidate facts (from {raw_count} raw sentences)")
print("matching   : " + ", ".join(f"{k}={v}" for k, v in actions.most_common()))
print(f"written to : {OUT}")
