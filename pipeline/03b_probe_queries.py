#!/usr/bin/env python3
"""03b_probe_queries.py — does each kind of query run, and does it return a sensible number of hits?

A smoke test, NOT retrieval: it asks each public API only for the NUMBER of matches (PubMed retmax=0,
ClinicalTrials.gov pageSize=1, openFDA limit=1, NCBI Gene count) and stores nothing from the answers.
Samples: 60 PubMed, 20 ClinicalTrials.gov, 20 openFDA, 20 NCBI Gene symbol lookups (seeded, so repeatable).
Needs network. Rate-limited to ~2.5 requests/s (NCBI allows 3/s without a key).

Buckets: 0 = too narrow or broken; 1-9 = narrow; 10-2000 = usable; >2000 = broad, needs filters.

Usage:  python3 pipeline/03b_probe_queries.py [save_counts.json]
"""
import json, random, time, urllib.parse, urllib.request, collections, sys
from pathlib import Path
R=str(Path(__file__).resolve().parents[1])+"/"
rows=[json.loads(l) for l in open(R+"data/cancer/queries.jsonl")]
q=[r for r in rows if r["queryable"]]
random.seed(11)
def get(url):
    time.sleep(0.4)
    try:
        with urllib.request.urlopen(urllib.request.Request(url,headers={"User-Agent":"medhavy-factchecker-querytest"}),timeout=20) as f:
            return json.load(f)
    except urllib.error.HTTPError as e:
        return {"_http":e.code}
    except Exception as e:
        return {"_err":str(e)[:80]}
out=[]
# PubMed
pm=[r for r in q if r["database_final"]=="pubmed"]
for r in random.sample(pm,60):
    d=get("https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&retmode=json&retmax=0&term="+urllib.parse.quote(r["query"]["term"]))
    es=d.get("esearchresult",{}); n=int(es["count"]) if "count" in es else None
    bad = bool(es.get("errorlist")) or "ERROR" in es or n is None
    out.append(("pubmed",r["fact_id"],n,bad,r["query"]["term"][:90]))
# ClinicalTrials
for r in [r for r in q if r["database_final"]=="clinicaltrials"][:20]:
    p={k:v for k,v in r["query"].items() if v}
    p.update({"pageSize":1,"countTotal":"true"})
    d=get("https://clinicaltrials.gov/api/v2/studies?"+urllib.parse.urlencode(p))
    out.append(("ctgov",r["fact_id"],d.get("totalCount"),"_http" in d or "_err" in d,json.dumps(r["query"])[:90]))
# openFDA
for r in random.sample([r for r in q if r["database_final"]=="fda"],min(20,sum(1 for r in q if r["database_final"]=="fda"))):
    d=get("https://api.fda.gov/"+r["query"]["endpoint"]+".json?limit=1&search="+urllib.parse.quote(r["query"]["search"],safe=':"+'))
    n=d.get("meta",{}).get("results",{}).get("total")
    out.append(("openfda",r["fact_id"],n if n is not None else 0,("_err" in d) or (d.get("_http") not in (None,404)),r["query"]["search"][:90]))
# NCBI Gene
for r in random.sample([r for r in q if r["database_final"]=="gene-protein-db"],20):
    sym=r["query"]["symbol"]
    d=get("https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=gene&retmode=json&retmax=0&term="+urllib.parse.quote(f'{sym}[sym] AND "Homo sapiens"[orgn]'))
    es=d.get("esearchresult",{}); n=int(es["count"]) if "count" in es else None
    out.append(("gene-symbol",r["fact_id"],n,n is None,sym))
if len(sys.argv)>1: json.dump(out,open(sys.argv[1],"w"))   # optional: save per-query counts
def bucket(n):
    return "error" if n is None else "0" if n==0 else "1-9" if n<10 else "10-2000" if n<=2000 else ">2000"
for src in ("pubmed","ctgov","openfda","gene-symbol"):
    rs=[o for o in out if o[0]==src]
    print(src,len(rs),dict(collections.Counter("ERR" if o[3] and o[2] is None else bucket(o[2]) for o in rs)))
