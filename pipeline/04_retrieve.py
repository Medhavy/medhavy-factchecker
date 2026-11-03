#!/usr/bin/env python3
"""04_retrieve.py — step 4: run each claim's query against its public database and cache what comes back.

Retrieval only. It does not judge anything and does not touch facts.json. For each claim it stores the
records the database returned (id, url, title, text fields) plus the exact request used, so a later step can
pick passages and the whole chain stays auditable.

Databases with an open API are supported: pubmed, clinicaltrials, fda (openFDA), gene-protein-db
(NCBI Gene and UniProt). seer-globocan, guideline-body and ensembl rows are skipped (no clean open API).

A PubMed query that returns nothing is relaxed by dropping its last AND-group, up to 2 times; the number of
relaxations is recorded (`relaxed`) so a loosened query is never mistaken for the original.

Usage:
  python3 pipeline/04_retrieve.py --pilot 60          # pick a seeded, stratified sample and retrieve it
  python3 pipeline/04_retrieve.py --ids FILE.json --dir full [--resume]
                                                      # retrieve the fact_ids in a JSON array into data/cancer/full/
Writes <dir>/pilot_ids.json (when --pilot) and <dir>/cache/retrieved.jsonl (default dir: pilot).
The cache holds third-party record text, so it is git-ignored and can be regenerated.
--resume keeps the rows already in the cache and retrieves only the claims not yet in it.
Needs network. ~2.5 requests/s (NCBI allows 3/s without a key).
"""
import argparse, datetime, json, random, re, sys, time, urllib.error, urllib.parse, urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
TODAY = datetime.date.today().isoformat()
UA = {"User-Agent": "medhavy-factchecker/0.1 (research; contact via github.com/Medhavy)"}
EUT = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"
SUPPORTED = {"pubmed", "clinicaltrials", "fda", "gene-protein-db"}
MAX_RECORDS = 5


def get(url, raw=False):
    time.sleep(0.4)
    req = urllib.request.Request(url, headers=UA)
    try:
        with urllib.request.urlopen(req, timeout=30) as f:
            body = f.read()
    except urllib.error.HTTPError as e:
        if e.code == 404: return None            # openFDA answers 404 for "no matches"
        raise
    return body if raw else json.loads(body)


def clean(s):
    return re.sub(r"\s+", " ", s or "").strip()


# ───────────────────────── PubMed ─────────────────────────
def split_and(term):
    """Split on top-level ' AND ' (outside parentheses and quotes)."""
    parts, depth, quote, cur, i = [], 0, False, "", 0
    while i < len(term):
        c = term[i]
        if c == '"': quote = not quote
        elif not quote and c == "(": depth += 1
        elif not quote and c == ")": depth -= 1
        if not quote and depth == 0 and term[i:i + 5] == " AND ":
            parts.append(cur); cur = ""; i += 5; continue
        cur += c; i += 1
    parts.append(cur)
    return [p.strip() for p in parts if p.strip()]


def pubmed(q):
    term = q["term"]
    groups = split_and(term)
    relaxed = 0
    while True:
        t = " AND ".join(groups)
        url = EUT + "esearch.fcgi?" + urllib.parse.urlencode(
            {"db": "pubmed", "term": t, "retmax": MAX_RECORDS, "sort": "relevance", "retmode": "json"})
        res = get(url)["esearchresult"]
        ids, count = res.get("idlist", []), int(res.get("count", 0))
        if ids or relaxed >= 2 or len(groups) <= 1:
            break
        groups = groups[:-1]; relaxed += 1
    recs = []
    if ids:
        xml = get(EUT + "efetch.fcgi?" + urllib.parse.urlencode(
            {"db": "pubmed", "id": ",".join(ids), "retmode": "xml"}), raw=True)
        root = ET.fromstring(xml)
        for art in root.findall(".//PubmedArticle"):
            pmid = art.findtext(".//MedlineCitation/PMID")
            title = clean("".join(art.find(".//ArticleTitle").itertext())) if art.find(".//ArticleTitle") is not None else ""
            abs_parts = []
            for a in art.findall(".//Abstract/AbstractText"):
                lab = a.get("Label"); txt = clean("".join(a.itertext()))
                if txt: abs_parts.append(f"{lab}: {txt}" if lab else txt)
            year = art.findtext(".//JournalIssue/PubDate/Year") or (art.findtext(".//JournalIssue/PubDate/MedlineDate") or "")[:4]
            recs.append({"record_id": f"PMID:{pmid}", "url": f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/",
                         "title": title, "year": year, "journal": clean(art.findtext(".//Journal/Title")),
                         "pub_types": [clean(p.text) for p in art.findall(".//PublicationType")],
                         "fields": {"title": title, "abstract": " ".join(abs_parts)}})
    return {"request": url, "effective_query": " AND ".join(groups), "relaxed": relaxed, "total_hits": count, "records": recs}


# ───────────────────────── ClinicalTrials.gov ─────────────────────────
def clinicaltrials(q):
    p = {k: v for k, v in q.items() if v}
    p.update({"pageSize": MAX_RECORDS, "countTotal": "true",
              "fields": "NCTId|BriefTitle|OfficialTitle|BriefSummary|OverallStatus|Phase|StartDate|Condition|InterventionName"})
    url = "https://clinicaltrials.gov/api/v2/studies?" + urllib.parse.urlencode(p)
    d = get(url) or {}
    recs = []
    for s in d.get("studies", []):
        ps = s["protocolSection"]; idm = ps.get("identificationModule", {})
        nct = idm.get("nctId")
        recs.append({"record_id": nct, "url": f"https://clinicaltrials.gov/study/{nct}",
                     "title": idm.get("briefTitle", ""),
                     "fields": {"brief_title": idm.get("briefTitle", ""), "official_title": idm.get("officialTitle", ""),
                                "brief_summary": clean(ps.get("descriptionModule", {}).get("briefSummary")),
                                "status": ps.get("statusModule", {}).get("overallStatus", ""),
                                "phase": ", ".join(ps.get("designModule", {}).get("phases", [])),
                                "start_date": ps.get("statusModule", {}).get("startDateStruct", {}).get("date", ""),
                                "conditions": ", ".join(ps.get("conditionsModule", {}).get("conditions", [])),
                                "interventions": ", ".join(i.get("name", "") for i in ps.get("armsInterventionsModule", {}).get("interventions", []))}})
    return {"request": url, "effective_query": json.dumps(p), "relaxed": 0, "total_hits": d.get("totalCount", 0), "records": recs}


# ───────────────────────── openFDA ─────────────────────────
def fda(q):
    url = f"https://api.fda.gov/{q['endpoint']}.json?" + urllib.parse.urlencode({"search": q["search"], "limit": 3}, safe=':"+()')
    d = get(url) or {}
    recs = []
    for r in d.get("results", []):
        of = r.get("openfda", {})
        if q["endpoint"] == "drug/label":
            rid = (r.get("set_id") or r.get("id")); f = {}
            for k in ("indications_and_usage", "boxed_warning", "mechanism_of_action", "dosage_and_administration"):
                if r.get(k): f[k] = clean(" ".join(r[k]))
            ftr = q.get("field_to_read")
            if ftr and r.get(ftr) and ftr not in f: f[ftr] = clean(" ".join(r[ftr]) if isinstance(r[ftr], list) else str(r[ftr]))
            title = ", ".join(of.get("brand_name", [])[:2] + of.get("generic_name", [])[:1])
            f["label_effective_time"] = str(r.get("effective_time", ""))
            url_r = f"https://api.fda.gov/drug/label.json?search=set_id:{rid}"
        elif q["endpoint"] == "drug/drugsfda":
            rid = r.get("application_number"); title = ", ".join(sorted({p.get("brand_name", "") for p in r.get("products", [])}))
            subs = "; ".join(f"{s.get('submission_type')} {s.get('submission_number')} {s.get('submission_status')} {s.get('submission_status_date')}"
                             for s in r.get("submissions", [])[:30])
            f = {"application": f"{rid} sponsor {r.get('sponsor_name')}", "products": title, "submissions": subs}
            url_r = f"https://api.fda.gov/drug/drugsfda.json?search=application_number:{rid}"
        else:
            rid = next((r[k] for k in ("k_number", "pma_number", "recall_number") if r.get(k)), "")
            f = {k: clean(str(v)) for k, v in r.items() if isinstance(v, (str, int)) and v != ""}
            title = of.get("device_name", rid); url_r = url
        recs.append({"record_id": rid, "url": url_r, "title": title, "fields": f})
    return {"request": url, "effective_query": q["search"], "relaxed": 0,
            "total_hits": d.get("meta", {}).get("results", {}).get("total", 0), "records": recs}


# ───────────────────────── NCBI Gene / UniProt ─────────────────────────
def gene(q):
    sym = q["symbol"]
    if q["database"] == "ensembl":
        return {"request": None, "skipped": "ensembl not supported", "records": []}
    if q["database"] == "uniprot":
        qs = f'(gene_exact:"{sym}" OR protein_name:"{sym}") AND organism_id:9606 AND reviewed:true'
        url = "https://rest.uniprot.org/uniprotkb/search?" + urllib.parse.urlencode(
            {"query": qs, "size": 2, "fields": "accession,gene_names,protein_name,cc_function,cc_subcellular_location,cc_subunit,cc_disease,length"})
        d = get(url) or {}
        recs = []
        for r in d.get("results", []):
            f = {"protein": r.get("proteinDescription", {}).get("recommendedName", {}).get("fullName", {}).get("value", ""),
                 "length": str(r.get("sequence", {}).get("length", ""))}
            for c in r.get("comments", []):
                txt = clean(" ".join(t.get("value", "") for t in c.get("texts", [])))
                if c.get("commentType") == "SUBCELLULAR LOCATION":
                    txt = ", ".join(l.get("location", {}).get("value", "") for l in c.get("subcellularLocations", []))
                if c.get("commentType") == "DISEASE":
                    txt = clean(c.get("disease", {}).get("description", ""))
                if txt: f[c["commentType"].lower().replace(" ", "_")] = txt
            acc = r["primaryAccession"]
            recs.append({"record_id": f"UniProt:{acc}", "url": f"https://rest.uniprot.org/uniprotkb/{acc}", "title": f["protein"], "fields": f})
        return {"request": url, "effective_query": qs, "relaxed": 0, "total_hits": len(recs), "records": recs}
    # ncbi-gene
    for term in (f'{sym}[sym] AND "Homo sapiens"[orgn]', f'{sym}[All Fields] AND "Homo sapiens"[orgn]'):
        url = EUT + "esearch.fcgi?" + urllib.parse.urlencode({"db": "gene", "term": term, "retmax": 2, "retmode": "json"})
        ids = get(url)["esearchresult"].get("idlist", [])
        if ids: break
    recs = []
    if ids:
        s = get(EUT + "esummary.fcgi?" + urllib.parse.urlencode({"db": "gene", "id": ",".join(ids), "retmode": "json"}))["result"]
        for gid in ids:
            r = s[gid]
            recs.append({"record_id": f"GeneID:{gid}", "url": f"https://www.ncbi.nlm.nih.gov/gene/{gid}", "title": f"{r.get('name')} - {r.get('description')}",
                         "fields": {"description": r.get("description", ""), "summary": clean(r.get("summary")),
                                    "location": f"chromosome {r.get('chromosome')} {r.get('maplocation')}".strip(),
                                    "aliases": r.get("otheraliases", "")}})
    return {"request": url, "effective_query": term, "relaxed": 0, "total_hits": len(ids), "records": recs}


RUN = {"pubmed": pubmed, "clinicaltrials": clinicaltrials, "fda": fda, "gene-protein-db": gene}


def pilot_ids(rows, n, seed=20261102):
    """Seeded sample of queryable rows, stratified by database: ~half PubMed, the rest spread over the others."""
    rng = random.Random(seed)
    by = {}
    for r in rows:
        if r["queryable"] and r["database_final"] in SUPPORTED: by.setdefault(r["database_final"], []).append(r)
    share = {"pubmed": 0.5, "gene-protein-db": 0.23, "clinicaltrials": 0.135, "fda": 0.135}
    ids = []
    for db, frac in share.items():
        k = min(round(n * frac), len(by[db]))
        ids += [r["fact_id"] for r in rng.sample(by[db], k)]
    return ids


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pilot", type=int); ap.add_argument("--ids")
    ap.add_argument("--dir", default="pilot"); ap.add_argument("--resume", action="store_true")
    a = ap.parse_args()
    rows = [json.loads(l) for l in (REPO / "data/cancer/queries.jsonl").read_text(encoding="utf-8").splitlines() if l.strip()]
    by_id = {r["fact_id"]: r for r in rows}
    out_dir = REPO / "data/cancer" / a.dir
    if a.pilot:
        ids = pilot_ids(rows, a.pilot)
        out_dir.mkdir(parents=True, exist_ok=True)
        (out_dir / "pilot_ids.json").write_text(json.dumps(ids, indent=1), encoding="utf-8")
    elif a.ids:
        ids = json.loads(Path(a.ids).read_text(encoding="utf-8"))
    else:
        sys.exit("give --pilot N or --ids FILE")
    cache = out_dir / "cache"; cache.mkdir(parents=True, exist_ok=True)
    path = cache / "retrieved.jsonl"
    done_ids = set()
    if a.resume and path.exists():
        done_ids = {json.loads(l)["fact_id"] for l in path.read_text(encoding="utf-8").splitlines() if l.strip()}
    n_err = 0
    with open(path, "a" if a.resume else "w", encoding="utf-8") as out:
        for i, fid in enumerate(ids, 1):
            if fid in done_ids: continue
            r = by_id[fid]; db = r["database_final"]; q = dict(r["query"])
            if db == "gene-protein-db": q["database"] = q.get("database", "ncbi-gene")
            row = {"fact_id": fid, "database": db, "retrieved": TODAY}
            try:
                row.update(RUN[db](q))
            except Exception as e:                       # keep going; record the failure
                row.update({"error": f"{type(e).__name__}: {e}"[:200], "records": []}); n_err += 1
            out.write(json.dumps(row, ensure_ascii=False) + "\n"); out.flush()
            print(f"{i:>3}/{len(ids)} {db:<16} records={len(row['records'])} relaxed={row.get('relaxed', '-')}", flush=True)
    print(f"done: {len(ids)} claims ({len(done_ids)} already cached), {n_err} errors -> {path}")


if __name__ == "__main__":
    main()
