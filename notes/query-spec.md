# Step 3 spec — turn each assertion into a database query

Project principle: we are collecting EVIDENCE, not verdicts. You are NOT judging whether a claim is true.
You are preparing a lookup that a program will run later against a public database. The lookup must be able
to surface records that CONFIRM or REFUTE the claim, so it must not be worded to favour either outcome.

Each input line (JSONL): fact_id, sentence (verbatim from a cancer textbook), section, chapter, database
(the database type chosen in an earlier triage pass), why (a short topic note), needs_context (true if the
sentence leans on surrounding text, e.g. "this", "these", a fragment).

For EVERY input line write exactly ONE output line (JSONL) with these keys:

  fact_id          copy EXACTLY from the input. Do not number, renumber, reorder, skip or add rows.
  database         copy the input's database.
  database_final   one of: pubmed | clinicaltrials | fda | gene-protein-db | seer-globocan | guideline-body | none.
                   Normally equal to `database`. Change it ONLY if the claim clearly belongs elsewhere
                   (then query for the new one), or "none" if no public database record could confirm it.
  claim_standalone one self-contained sentence stating the single assertion to be checked. Resolve "this/these/it"
                   using the section title. If the sentence holds several claims, choose the most checkable one
                   and say so in notes. Never add facts that are not in the sentence or section title.
  queryable        true | false. false when you cannot build a lookup that stands alone
                   (fragment whose referent is unknowable, pure definition of a word, no record type fits).
  unqueryable_reason  null if queryable, else one of: needs_context | no_record_type | too_vague.
  entities         list of 1-5 specific things the lookup is about (genes, drugs, trials, cancer sites, measures,
                   organisms). Use standard names (HGNC symbols, generic drug names, MeSH-style disease names).
  check            ONE neutral sentence: what a retrieved record must state for it to bear on this claim
                   (the value, relation, date or property to compare). Do NOT say "confirm that ..." or
                   "verify that ..."; say "the record states the value of X for Y".
  query            an object in the shape for database_final (below). null if not queryable.
  query_text       the same query flattened to the one string a person would type in that database's search box.
                   null if not queryable.
  notes            "" or a short remark (multiple claims in sentence; number is a rounded figure; etc.)

## query shapes

pubmed:
  {"term": "<Entrez syntax>", "article_types": []}
  - 2 to 4 concepts joined with AND; synonyms joined with OR inside parentheses.
  - Use field tags: [tiab] for title/abstract words, [MeSH Terms] where a MeSH heading exists.
  - Put the ENTITIES and the RELATION'S NOUN in the query (e.g. "thymidylate synthase" AND fluorouracil),
    never the whole sentence, never the asserted direction or value ("increases", "90%").
  - article_types: optional subset of ["Review","Meta-Analysis","Clinical Trial","Randomized Controlled Trial",
    "Systematic Review","Guideline"] when the claim is about trial evidence; else [].
clinicaltrials:  (ClinicalTrials.gov API v2 parameters)
  {"query.term": "", "query.cond": "", "query.intr": "", "query.titles": ""}   leave unused keys as "".
fda:  (openFDA)
  {"endpoint": "drug/label" | "drug/drugsfda" | "drug/enforcement" | "device/510k" | "device/pma",
   "search": "<openFDA search string, e.g. openfda.generic_name:\"imatinib\">",
   "field_to_read": "<e.g. indications_and_usage, boxed_warning, approval date field>"}
gene-protein-db:
  {"database": "ncbi-gene" | "uniprot" | "ensembl", "symbol": "<HGNC symbol or protein name>",
   "organism": "Homo sapiens", "field_to_read": "<e.g. function, domains, subcellular location, chromosome, pathway>"}
seer-globocan:
  {"dataset": "seer-cancer-stat-facts" | "globocan" | "acs-cancer-statistics" | "who-ihme-gbd",
   "cancer_site": "", "measure": "incidence | mortality | 5-year relative survival | prevalence | lifetime risk | survivors",
   "population": "<US | world | region | age group>", "year": "<year or range if stated, else ''>"}
guideline-body:
  {"body": "NCCN" | "ASCO" | "WHO" | "ESMO" | "AJCC" | "NCI-PDQ" | "CAP", "topic": "", "cancer_site": "",
   "access": "open | paywalled | unknown"}
  Pick the body that actually issues the thing the claim describes (staging system -> AJCC; classification -> WHO;
  treatment recommendation -> NCCN/ASCO/ESMO; physician summary -> NCI-PDQ).

## rules
- Never invent a number, trial name, gene or drug that is not in the sentence or its section title.
- Do not put the claim's asserted value in `query` / `query_text` (it goes in `check`).
- If you change database_final, `query` must follow the NEW shape.
- Output file: JSON Lines only, UTF-8, one object per line, no markdown fences, no commentary.
- The output must have exactly as many lines as the input, with the same fact_ids in the same order.
