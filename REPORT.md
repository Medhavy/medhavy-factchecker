# Medhavy fact checker — what it found

Built 2026-11-03 from `data/cancer/facts.json`. The book is the Medhavy cancer textbook.

## Summary

- **3,165 statements** were pulled from the book. **2,280** are real assertions; the other 885 are framing, opinion or vague, and no database record could confirm or refute them.
- **1,170 statements** were looked up in a public database (PubMed, UniProt, openFDA, ClinicalTrials.gov, NCBI Gene). That produced **1,463 pieces of evidence**: each is an exact quote from a database record, with a link to it.
- **117 are supported** (10% of those looked up): a record states the claim. **726 are partly supported** (62%): records back part of it, or a narrower version. **103** only found records on the same topic. **211** found nothing in the top results.
- **13 need a person.** A record points against the book, or against a time-bound claim ("currently", "ongoing"). Most are one study in a narrower setting, so this means "look", not "the book is wrong".
- **Human check so far: 0 of 17 flagged cases decided.** Every "supports" or "conflicts" label is a model's reading of the quote. The quote is real and exact; the reading is not yet checked by a person.

**"Supported" never means "true".** It means a database record says so. A record can be wrong, narrow or out of date.

## Where all the statements went

| Status | Statements | What it means |
|---|---:|---|
| `not_an_assertion` | 885 | Framing, opinion or vague. Nothing to check. |
| `no_record_type` | 799 | A real claim, but no public record type fits (general textbook knowledge). |
| `not_queryable` | 82 | A database fits, but no stand-alone question could be written. |
| `no_open_api` | 229 | A database fits (SEER, GLOBOCAN, guideline bodies) but it has no open API. **Not checked.** |
| `no_evidence_found` | 211 | Searched; nothing in the top 5 records bore on the claim. Not the same as "no evidence exists". |
| `related_only` | 103 | Records on the same topic; none states the claim. |
| `partially_supported` | 726 | A record backs part of the claim, a narrower version, or one instance of a plural claim. |
| `supported` | 117 | A record states the claim (a plural claim needs two records). |
| `conflicting_evidence` | 12 | A record states something that points against the claim. Needs a person. |
| `dated_evidence` | 1 | A record differs only because it shows today's state of a time-bound claim. Needs a person. |

## How far to trust "supported"

The first pass was too generous. A hand check of 24 random "supports" quotes found 15 clean and 9 that covered only one clause of a multi-part claim (for example, a claim about "adverse effects *that restrict clinical application*" matched a quote about adverse effects alone).

So every "supports" quote was re-read under a strict rule: keep it only if the quote by itself states every substantive part of the claim. **361 of 496 were downgraded to partial; 135 kept** (27%). The pass can only downgrade, never upgrade. The original label is kept on each row as `stance_original`, and all verdicts are in `data/cancer/strict_recheck.jsonl`. This is a second model reading, still unreviewed by a person.

## Five examples that came out supported

**Book (24.6 Angiogenesis Inhibitors):** Angiogenesis—the formation of new blood vessels—is central to the growth of cancer.  
> “Various preclinical in vivo experiments have proven that most tumours need new vessel formation in order to grow and to form metastases.”  
> — PubMed, [PMID:14694516](https://pubmed.ncbi.nlm.nih.gov/14694516/): Are tumours angiogenesis-dependent?

**Book (7.7: Epigenetic Therapy):** Genome-wide analysis of the BETi-induced transcriptional response identified the immune checkpoint ligand Cd274 (Pd-l1) as a Myc-independent, BETi target-gene.  
> “Genome-wide analysis of the BETi-induced transcriptional response identified the immune checkpoint ligand Cd274 (Pd-l1) as a Myc-independent, BETi target-gene.”  
> — PubMed, [PMID:28249162](https://pubmed.ncbi.nlm.nih.gov/28249162/): BET-Bromodomain Inhibitors Engage the Host Immune System and Regulate Expression of the Immune Checkpoint Ligand PD-L1.

**Book (27.1 Nanoparticles for Drug Delivery):** Solid and malignant tumours are highly heterogenous resulting in disparate tumour permeability, unfavourable for passive targeting.  
> “However, the EPR effect is compromised in some tumors due to the heterogeneity of tumor structures.”  
> — PubMed, [PMID:36581260](https://pubmed.ncbi.nlm.nih.gov/36581260/): Polysaccharide-based nanocarriers for efficient transvascular drug delivery.

**Book (7.7: Epigenetic Therapy):** Transcriptional silencing mediated by DNA methylation is also related to the recruitment of co-repressors and deacetylation or methylation of histone marks at promoters and enhancers.  
> “MeCP2 is shown to interact with the Sin3/histone deacetylase co-repressor complex. Thus, this interaction can provide a mechanistic explanation for the long-known relationship between DNA methylation and chromatin structure.”  
> — PubMed, [PMID:10322130](https://pubmed.ncbi.nlm.nih.gov/10322130/): DNA methylation and chromatin modification.

**Book (5.3 Mechanisms of Oncogene Activation):** Much of the interest in ras stems from the fact that this gene is involved in a high fraction of human cancers.  
> “RAS mutation is the most frequent oncogenic alteration in human cancers.”  
> — PubMed, [PMID:32725342](https://pubmed.ncbi.nlm.nih.gov/32725342/): Molecular epidemiology and diagnostics of KRAS mutations in human cancer.

## The conflicts

These are the cases where a record points against the book. Each is in `review/QUEUE.md` with the full quote and a link.

- PlGF is predominantly expressed in placenta and binds exclusively to VEGFR-1. _(12.2 Key Angiogenic Factors)_
- The authors concluded that the use of bevacizumab was significantly associated with an increased risk of developing venous thromboembolism in cancer patients receiving this drug. _(12.6 Anti-Angiogenic Therapy)_
- Aberrant de novo expression of N-cadherin has been noted in carcinomas from the breast, prostate, bladder and the head and neck region, where it parallels a downregulation of E-cadherin and a decrease in tumor differentiation. _(13.2 Epithelial-Mesenchymal Transition (EMT))_
- The mutant aberrant activation of the Wnt pathway is a major factor driving most types of tissue stem cells and contributes to DTP cell development and stemness maintenance. _(15.3 Implications for Treatment Resistance)_
- The Hedgehog pathway regulates autophagy in cancer cells, and inhibition of this pathway augments the efficacy of chemotherapeutic agents through suppression of autophagy. _(15.3 Implications for Treatment Resistance)_
- Gamma-secretase inhibitors that target Notch signaling sensitize colon cancer cells to chemotherapy by inhibiting oxaliplatin-induced Notch-1 receptor and Hes-1 activity. _(15.3 Implications for Treatment Resistance)_
- Regorafenib, an oral multikinase inhibitor blocking activity of protein kinases involved in angiogenesis, oncogenesis, metastasis, and tumor immunity, decreases stemness phenotypes including tumor sphere formation and side population fraction in colorectal cancer cells. _(15.3 Implications for Treatment Resistance)_
- IMRT has higher integral radiation dose and increases the total volume of tissues exposed to low-dose radiation compared to conventional radiotherapy. _(21.2 Types of Radiation Therapy)_
- No dose adjustment is necessary for patients with renal or liver impairment or elderly patients. _(23.4 Aromatase Inhibitors)_
- Socioeconomic factors and physician supply are key predictors of CRC screening. _(3.5 Cancer Health Disparities and Social Determinants)_
- Mechanistically, up-regulation of HELLS confers transcription factor SP1 hyperactivation, leading to epigenetic silencing of multiple tumor suppressor genes through altered chromatin accessibility and nucleosome positioning. _(6.2 Mechanisms of Tumor Suppressor Inactivation)_
- Gene specificity of the epigenetic silencing was observed in each of these tumor types, as hypermethylation of MSH2 was not detected in any of several studies. _(6.2 Mechanisms of Tumor Suppressor Inactivation)_
- As of January 2022, RNK05047 has entered clinical trials to treat advanced solid tumors and lymphomas. _(7.7: Epigenetic Therapy)_

## What is not covered

- **229 statements** that need SEER/GLOBOCAN cancer statistics, clinical guidelines or Ensembl. Their databases have no open API; they are listed, not checked.
- **799 statements** that are real but general (mechanisms, definitions, history). No public record type holds them.
- **82 statements** that could not be turned into a stand-alone question.
- Only the top 5 records per question were read, so "no evidence found" is a limit of the search, not a finding about the world.
- Only the cancer book has been run. The pipeline is built to take other Medhavy books.

## Files

- `data/cancer/facts.json` — every statement with its evidence and status.
- `review/QUEUE.md` and `review/decisions.jsonl` — the cases for a person to decide.
- `README.md` — how the pipeline works, step by step.
