# Human review queue

## Summary

**30 claims need a person to look.** 0 decided, 30 to go. Built 2026-11-02 from `data/cancer/facts.json`.

- **12 conflicts:** a retrieved record says something that points against the book's claim. Most are one study in a narrower setting, so this is "a person should look", not "the book is wrong".
- **1 dated difference:** a record differs from a time-bound claim only because it shows today's state.
- **17 plural claims:** the book says "several" or "many" and only one record was found.

Everything the evidence says here is a model's reading of a quoted passage. The quote is an exact copy of the record; the stance (`supports`, `partial`, `refutes`, `related`) is not reviewed. You are the first human check.

### How to review

1. Read the case. Open the record link if the quote is not enough.
2. Pick one answer for the question under the case.
3. Write it in `review/decisions.jsonl`: set `decision` to the answer key, add your name as `reviewer`, today's date, and a `note` if you want to say why.
4. Run `python3 pipeline/06_derive_status.py` then `python3 pipeline/07_merge_into_facts.py`. The decision is attached to the claim as `human_review` and `human_reviewed` becomes true. The evidence and status are not changed.

Do not edit the quotes or stances. If a stance is wrong, say so in `note`.

---

## A record points the other way (12)

**Question:** Does the quoted passage contradict the book's claim as the book states it?

Answers: `contradicts` = yes, it contradicts the claim as written; `narrower` = it points the other way, but only in a narrower setting; the claim as written is not refuted; `misread` = it does not actually conflict (the model misread it); `cannot_tell` = I cannot tell from the passage and the record

### 1. PlGF is predominantly expressed in placenta and binds exclusively to VEGFR-1.

- **Book:** 12.2 Key Angiogenic Factors (`/docs/Chapter12/2_Key_Angiogenic_Factors`)
- **Fact id:** `cancer-plgf-is-predominantly-expressed-in-placenta-and-binds-exclusively-to-vegf`
- **Status:** `conflicting_evidence` · looked up in gene-protein-db · 1 record(s)
- **Why flagged:** a passage conflicts with the claim

> **refutes** · UniProt · [UniProt:P49763](https://rest.uniprot.org/uniprotkb/P49763)  
> Placenta growth factor  
> “It binds to the receptor FLT1/VEGFR-1. Isoform PlGF-2 binds NRP1/neuropilin-1 and NRP2/neuropilin-2 in a heparin-dependent manner.”  
> _model's note: Confirms VEGFR-1 binding but PlGF-2 also binds neuropilins, conflicting with exclusively; no placenta expression stated._
>

---

### 2. The authors concluded that the use of bevacizumab was significantly associated with an increased risk of developing venous thromboembolism in cancer patients receiving this drug.

- **Book:** 12.6 Anti-Angiogenic Therapy (`/docs/Chapter12/6_Anti_Angiogenic_Therapy`)
- **Fact id:** `cancer-the-authors-concluded-that-the-use-of-bevacizumab-was-significantly-assoc`
- **Status:** `conflicting_evidence` · looked up in pubmed · 2 record(s)
- **Why flagged:** a passage conflicts with the claim

> **refutes** · PubMed · [PMID:35129311](https://pubmed.ncbi.nlm.nih.gov/35129311/)  
> Risk factors for venous thromboembolism in metastatic colorectal cancer with contemporary treatment: A SEER-Medicare analysis.  
> “After adjustment, any therapy and bevacizumab (HR 0.68, 0.58-0.78) in particular were protective.”  
> _model's note: In a metastatic colorectal SEER cohort, bevacizumab was associated with lower VTE risk; narrower scope than claim._
>
> **partial** · PubMed · [PMID:31317482](https://pubmed.ncbi.nlm.nih.gov/31317482/)  
> Thrombotic Risk from Chemotherapy and Other Cancer Therapies.  
> “Bevacizumab, an inhibitor of vascular endothelial growth factor, increases arterial and possibly venous thrombotic risk, although the literature is conflicting about the latter.”  
> _model's note: Says bevacizumab possibly increases venous thrombotic risk; literature conflicting, no relative risk given._
>

---

### 3. Aberrant de novo expression of N-cadherin has been noted in carcinomas from the breast, prostate, bladder and the head and neck region, where it parallels a downregulation of E-cadherin and a decrease in tumor differentiation.

- **Book:** 13.2 Epithelial-Mesenchymal Transition (EMT) (`/docs/Chapter13/2_Epithelial_Mesenchymal_Transition_EMT`)
- **Fact id:** `cancer-aberrant-de-novo-expression-of-n-cadherin-has-been-noted-in-carcinomas-fr`
- **Status:** `conflicting_evidence` · looked up in pubmed · 2 record(s)
- **Why flagged:** a passage conflicts with the claim

> **refutes** · PubMed · [PMID:14645693](https://pubmed.ncbi.nlm.nih.gov/14645693/)  
> Expression of P-cadherin, but not E-cadherin or N-cadherin, relates to pathological and functional differentiation of breast carcinomas.  
> “There were no correlations between E/N-cadherin and size, grade, node status, or receptors.”  
> _model's note: In breast carcinomas, N-cadherin and E-cadherin showed no correlation with grade, unlike the claim._
>
> **partial** · PubMed · [PMID:24503792](https://pubmed.ncbi.nlm.nih.gov/24503792/)  
> Increased expression of EphA2 and E-N cadherin switch in primary hepatocellular carcinoma.  
> “Increased expressions of ephrin type-A receptor 2 and N-cadherin and reduced expression of E-cadherin were significantly detected in hepatocellular carcinoma compared with normal liver tissues.”  
> _model's note: N-cadherin up with E-cadherin down, but in hepatocellular carcinoma, not the listed tumor types._
>

---

### 4. Gamma-secretase inhibitors that target Notch signaling sensitize colon cancer cells to chemotherapy by inhibiting oxaliplatin-induced Notch-1 receptor and Hes-1 activity.

- **Book:** 15.3 Implications for Treatment Resistance (`/docs/Chapter15/3_Implications_for_Treatment_Resistance`)
- **Fact id:** `cancer-gamma-secretase-inhibitors-that-target-notch-signaling-sensitize-colon-ca`
- **Status:** `conflicting_evidence` · looked up in pubmed · 2 record(s)
- **Why flagged:** a passage conflicts with the claim; another supports it

> **refutes** · PubMed · [PMID:23887890](https://pubmed.ncbi.nlm.nih.gov/23887890/)  
> Gamma-secretase inhibition attenuates oxaliplatin-induced apoptosis through increased Mcl-1 and/or Bcl-xL in human colon cancer cells.  
> “Unexpectedly, gamma-secretase inhibition reduced oxaliplatin-induced apoptosis”  
> _model's note: GSI reduced oxaliplatin-induced apoptosis in colon cancer cells, opposite to sensitization._
>
> **supports** · PubMed · [PMID:19147571](https://pubmed.ncbi.nlm.nih.gov/19147571/)  
> gamma-Secretase inhibitors abrogate oxaliplatin-induced activation of the Notch-1 signaling pathway in colon cancer cells resulting in enhanced chemosensitivity.  
> “Subsequent inhibition of Notch-1 signaling with a sulfonamide GSI (GSI34) prevented the induction of NICD by chemotherapy and blunted Hes-1 activation. Blocking the activation of Notch signaling with GSI34 sensitized cells to chemotherapy and was synergistic with oxaliplatin, 5-FU, and SN-38.”  
> _model's note: GSI blocked oxaliplatin-induced NICD and Hes-1 activation and sensitized colon cancer cells to chemotherapy._
>

---

### 5. Regorafenib, an oral multikinase inhibitor blocking activity of protein kinases involved in angiogenesis, oncogenesis, metastasis, and tumor immunity, decreases stemness phenotypes including tumor sphere formation and side population fraction in colorectal cancer cells.

- **Book:** 15.3 Implications for Treatment Resistance (`/docs/Chapter15/3_Implications_for_Treatment_Resistance`)
- **Fact id:** `cancer-regorafenib-an-oral-multikinase-inhibitor-blocking-activity-of-protein-ki`
- **Status:** `conflicting_evidence` · looked up in pubmed · 2 record(s)
- **Why flagged:** a passage conflicts with the claim; another supports it

> **refutes** · PubMed · [PMID:33023006](https://pubmed.ncbi.nlm.nih.gov/33023006/)  
> STAT3 Mediated miR-30a-5p Inhibition Enhances Proliferation and Inhibits Apoptosis in Colorectal Cancer Cells.  
> “The formation of colorectal cancer stem-like tumorspheres was inhibited by BBI608, a STAT3 inhibitor, but not by regorafenib.”  
> _model's note: In HT29-derived tumorspheres, regorafenib did not inhibit sphere formation; side population not addressed._
>
> **supports** · PubMed · [PMID:30005681](https://pubmed.ncbi.nlm.nih.gov/30005681/)  
> Regorafenib suppresses colon tumorigenesis and the generation of drug resistant cancer stem-like cells via modulation of miR-34a associated signaling.  
> “We showed that regorafenib treatment decreased the stemness phenotypes including tumor sphere formation, and side-population, of both HCT-116R and DLD-1R cells.”  
> _model's note: Regorafenib decreased tumor sphere formation and side-population in 5-FU-resistant colorectal cell lines._
>

---

### 6. The Hedgehog pathway regulates autophagy in cancer cells, and inhibition of this pathway augments the efficacy of chemotherapeutic agents through suppression of autophagy.

- **Book:** 15.3 Implications for Treatment Resistance (`/docs/Chapter15/3_Implications_for_Treatment_Resistance`)
- **Fact id:** `cancer-the-hedgehog-pathway-regulates-autophagy-in-cancer-cells-and-inhibition-o`
- **Status:** `conflicting_evidence` · looked up in pubmed · 2 record(s)
- **Why flagged:** a passage conflicts with the claim

> **refutes** · PubMed · [PMID:25701353](https://pubmed.ncbi.nlm.nih.gov/25701353/)  
> Targeting Hedgehog signaling pathway and autophagy overcomes drug resistance of BCR-ABL-positive chronic myeloid leukemia.  
> “Our results indicated that pharmacological or genetic inhibition of Hh pathway could markedly induce autophagy in BCR-ABL(+) CML cells.”  
> _model's note: Hh inhibition induced (not suppressed) autophagy in CML cells; combined Hh and autophagy inhibition enhanced cell death. Opposite direction._
>
> **partial** · PubMed · [PMID:30081498](https://pubmed.ncbi.nlm.nih.gov/30081498/)  
> Hedgehog Signaling Pathway and Autophagy in Cancer.  
> “Recent evidence demonstrated that Hh signaling interplays with autophagy in multiple cancers.”  
> _model's note: Supports Hh-autophagy crosstalk in cancers; does not state that Hh inhibition acts through autophagy suppression._
>

---

### 7. The mutant aberrant activation of the Wnt pathway is a major factor driving most types of tissue stem cells and contributes to DTP cell development and stemness maintenance.

- **Book:** 15.3 Implications for Treatment Resistance (`/docs/Chapter15/3_Implications_for_Treatment_Resistance`)
- **Fact id:** `cancer-the-mutant-aberrant-activation-of-the-wnt-pathway-is-a-major-factor-drivi`
- **Status:** `conflicting_evidence` · looked up in pubmed · 2 record(s)
- **Why flagged:** a passage conflicts with the claim

> **refutes** · PubMed · [PMID:35773527](https://pubmed.ncbi.nlm.nih.gov/35773527/)  
> Mex3a marks drug-tolerant persister colorectal cancer cells that mediate relapse after chemotherapy.  
> “Lineage-tracing analysis showed that persister Mex3a+ cells downregulate the WNT/stem cell gene program immediately after chemotherapy and adopt a transient state reminiscent to that of YAP+ fetal intestinal progenitors.”  
> _model's note: Persister cells downregulate the WNT program after chemotherapy, conflicting with Wnt activation driving persister development._
>
> **related** · PubMed · [PMID:42882474](https://pubmed.ncbi.nlm.nih.gov/42882474/)  
> Acquired Chemoresistance in Colorectal Cancer: Therapy-Induced Signalling Adaptation, Cellular Plasticity and Mechanism-Guided Therapeutic Strategies.  
> “Evidence linking chemoresistance with Wnt/β-catenin, Notch and Hippo/Yes-associated protein 1 (YAP1) signalling is predominantly preclinical and varies according to treatment context, with stronger direct pathway-specific evidence for 5-FU and oxaliplatin than for irinotecan.”  
> _model's note: Links Wnt signalling to chemoresistance, but only as preclinical, context-dependent evidence; no persister-specific Wnt role stated._
>

---

### 8. IMRT has higher integral radiation dose and increases the total volume of tissues exposed to low-dose radiation compared to conventional radiotherapy.

- **Book:** 21.2 Types of Radiation Therapy (`/docs/Chapter21/2_Types_of_Radiation_Therapy`)
- **Fact id:** `cancer-imrt-has-higher-integral-radiation-dose-and-increases-the-total-volume-of`
- **Status:** `conflicting_evidence` · looked up in pubmed · 2 record(s)
- **Why flagged:** a passage conflicts with the claim

> **refutes** · PubMed · [PMID:17208388](https://pubmed.ncbi.nlm.nih.gov/17208388/)  
> Intensity-modulated radiotherapy (IMRT) and conventional three-dimensional conformal radiotherapy for high-grade gliomas: does IMRT increase the integral dose to normal brain?  
> “Overall, total integral dose was reduced by 7-10% with IMRT, p < 0.001, without significantly increasing the 0.5-5 Gy low-dose volume.”  
> _model's note: In high-grade gliomas IMRT reduced integral dose versus 3D-CRT and did not raise low-dose volume; one tumor site._
>
> **related** · PubMed · [PMID:33472549](https://pubmed.ncbi.nlm.nih.gov/33472549/)  
> Comparison of Intensity Modulated Radiotherapy Treatment Plans Between 1.5T MR-Linac and Conventional Linac.  
> “However, MRL-IMRT plans had higher dose to skin and larger low dose region of normal tissues.”  
> _model's note: Larger low-dose region for MR-linac IMRT versus conventional-linac IMRT, not versus conventional radiotherapy._
>

---

### 9. No dose adjustment is necessary for patients with renal or liver impairment or elderly patients.

- **Book:** 23.4 Aromatase Inhibitors (`/docs/Chapter23/5_Aromatase_Inhibitors`)
- **Fact id:** `cancer-no-dose-adjustment-is-necessary-for-patients-with-renal-or-liver-impairme`
- **Status:** `conflicting_evidence` · looked up in fda · 2 record(s)
- **Why flagged:** a passage conflicts with the claim

> **refutes** · openFDA · [065cc89f-3a3f-4d78-b9f6-1c32a77ceb1c](https://api.fda.gov/drug/label.json?search=set_id:065cc89f-3a3f-4d78-b9f6-1c32a77ceb1c)  
> Letrozole, LETROZOLE  
> “The dose of letrozole tablets in patients with cirrhosis and severe hepatic dysfunction should be reduced by 50% [see Warnings and Precautions ( 5.3 )].”  
> _model's note: Letrozole label requires dose reduction in cirrhosis with severe hepatic dysfunction._
>
> **partial** · openFDA · [03586c40-eb32-45c5-beb7-6762a6b78790](https://api.fda.gov/drug/label.json?search=set_id:03586c40-eb32-45c5-beb7-6762a6b78790)  
> Anastrozole, ANASTROZOLE  
> “No dosage adjustment is necessary for patients with renal impairment or for elderly patients [see Use in Specific Populations ( 8.6 )].”  
> _model's note: Anastrozole label: no adjustment for renal impairment or elderly; hepatic addressed only separately, one drug._
>

---

### 10. Socioeconomic factors and physician supply are key predictors of CRC screening.

- **Book:** 3.5 Cancer Health Disparities and Social Determinants (`/docs/Chapter3/5_Cancer_Health_Disparities_and_Social_Determinants`)
- **Fact id:** `cancer-socioeconomic-factors-and-physician-supply-are-key-predictors-of-crc-scre`
- **Status:** `conflicting_evidence` · looked up in pubmed · 2 record(s)
- **Why flagged:** a passage conflicts with the claim; another supports it

> **refutes** · PubMed · [PMID:39029926](https://pubmed.ncbi.nlm.nih.gov/39029926/)  
> Individual and geospatial factors associated with receipt of colorectal cancer screening: a state-wide mixed-level analysis.  
> “In this state-wide representative analysis, physician density was completely unassociated with CRC screening, although health insurance status remains strongly related.”  
> _model's note: New York study found physician density unassociated with CRC screening, conflicting on physician supply._
>
> **supports** · PubMed · [PMID:23277775](https://pubmed.ncbi.nlm.nih.gov/23277775/)  
> Socioeconomic and physician supply determinants of racial disparities in colorectal cancer screening.  
> “Socioeconomic factors and physician supply are key predictors of CRC screening.”  
> _model's note: Conclusion states exactly that socioeconomic factors and physician supply are key predictors of CRC screening._
>

---

### 11. Gene specificity of the epigenetic silencing was observed in each of these tumor types, as hypermethylation of MSH2 was not detected in any of several studies.

- **Book:** 6.2 Mechanisms of Tumor Suppressor Inactivation (`/docs/Chapter6/2_Mechanisms_of_Tumor_Suppressor_Inactivation`)
- **Fact id:** `cancer-gene-specificity-of-the-epigenetic-silencing-was-observed-in-each-of-thes`
- **Status:** `conflicting_evidence` · looked up in pubmed · 1 record(s)
- **Why flagged:** a passage conflicts with the claim

> **refutes** · PubMed · [PMID:30784122](https://pubmed.ncbi.nlm.nih.gov/30784122/)  
> Methylation and expression analysis of mismatch repair genes in extramammary Paget's disease.  
> “Hypermethylation also was found in the promoter of MSH2 but not in other MMR genes.”  
> _model's note: MSH2 promoter hypermethylation was detected in extramammary Paget's disease tumors, against the claim._
>

---

### 12. Mechanistically, up-regulation of HELLS confers transcription factor SP1 hyperactivation, leading to epigenetic silencing of multiple tumor suppressor genes through altered chromatin accessibility and nucleosome positioning.

- **Book:** 6.2 Mechanisms of Tumor Suppressor Inactivation (`/docs/Chapter6/2_Mechanisms_of_Tumor_Suppressor_Inactivation`)
- **Fact id:** `cancer-mechanistically-up-regulation-of-hells-confers-transcription-factor-sp1-h`
- **Status:** `conflicting_evidence` · looked up in pubmed · 1 record(s)
- **Why flagged:** plural claim: only one record supports one instance; a passage conflicts with the claim

> **refutes** · PubMed · [PMID:30516846](https://pubmed.ncbi.nlm.nih.gov/30516846/)  
> HELLS Regulates Chromatin Remodeling and Epigenetic Silencing of Multiple Tumor Suppressor Genes in Human Hepatocellular Carcinoma.  
> “We further showed that up-regulation of HELLS in HCC was conferred by hyperactivation of transcription factor specificity protein 1 (SP1).”  
> _model's note: SP1 hyperactivation drives HELLS up-regulation, the reverse direction of the claim._
>
> **supports** · PubMed · [PMID:30516846](https://pubmed.ncbi.nlm.nih.gov/30516846/)  
> HELLS Regulates Chromatin Remodeling and Epigenetic Silencing of Multiple Tumor Suppressor Genes in Human Hepatocellular Carcinoma.  
> “Though this mechanism, up-regulation of HELLS mediated epigenetic silencing of multiple tumor suppressor genes including E-cadherin, FBP1, IGFBP3, XAF1 and CREB3L3 in HCC.”  
> _model's note: HELLS up-regulation mediates epigenetic silencing of tumor suppressor genes._
>

---

## The record differs only by date (1)

**Question:** Was the book's time-bound claim right when it was written?

Answers: `right_then` = yes, the claim was right at the time; `wrong` = no, it was already wrong when written; `cannot_tell` = I cannot tell

### 13. As of January 2022, RNK05047 has entered clinical trials to treat advanced solid tumors and lymphomas.

- **Book:** 7.7: Epigenetic Therapy (`/docs/Chapter7/7_Epigenetic_Therapy`)
- **Fact id:** `cancer-as-of-january-2022-rnk05047-has-entered-clinical-trials-to-treat-advanced`
- **Status:** `dated_evidence` · looked up in clinicaltrials · 1 record(s)
- **Why flagged:** time-bound claim: record shows today's state, which differs

> **refutes** · ClinicalTrials.gov · [NCT05487170](https://clinicaltrials.gov/study/NCT05487170)  
> A Study of RNK05047 in Subjects With Advanced Solid Tumors/Diffuse Large B-cell Lymphoma (CHAMP-1)  
> “2022-07-12”  
> _model's note: Registered RNK05047 trial started July 2022, after January 2022._
>
> **partial** · ClinicalTrials.gov · [NCT05487170](https://clinicaltrials.gov/study/NCT05487170)  
> A Study of RNK05047 in Subjects With Advanced Solid Tumors/Diffuse Large B-cell Lymphoma (CHAMP-1)  
> “Advanced Solid Tumor, DLBCL”  
> _model's note: Trial conditions are advanced solid tumors and DLBCL, matching the claimed indications but not the date._
>

---

## One record, but the claim is about several (17)

**Question:** Does this single record carry the claim, or does a claim like 'several' / 'many' need more records?

Answers: `one_is_enough` = one record is enough for this claim; `needs_more` = the claim needs more than one record; leave it partially supported; `cannot_tell` = I cannot tell

### 14. For Warburg, several questions remained unanswered, including why cancer cells would inefficiently shunt glucose-derived pyruvate to lactate production instead of to the TCA cycle, which would result in significantly higher ATP production.

- **Book:** 11.1 The Warburg Effect: Historical Discovery and Modern Understanding (`/docs/Chapter11/2_The_Warburg_Effect_Historical_Discovery_and_Modern_Understanding`)
- **Fact id:** `cancer-for-warburg-several-questions-remained-unanswered-including-why-cancer-ce`
- **Status:** `partially_supported` · looked up in pubmed · 2 record(s)
- **Why flagged:** plural claim: only one record supports one instance

> **supports** · PubMed · [PMID:39082678](https://pubmed.ncbi.nlm.nih.gov/39082678/)  
> The Warburg Effect Revisited through Blood and Electron Flow.  
> “The benefit of the Warburg effect on cancer cells remains enigmatic, particularly because extracellular disposal of incompletely oxidized lactate is wasteful.”  
> _model's note: States the benefit of lactate production over oxidation remains enigmatic._
>
> **related** · PubMed · [PMID:26942675](https://pubmed.ncbi.nlm.nih.gov/26942675/)  
> Mitochondria-Translocated PGK1 Functions as a Protein Kinase to Coordinate Glycolysis and the TCA Cycle in Tumorigenesis.  
> “This reduces mitochondrial pyruvate utilization, suppresses reactive oxygen species production, increases lactate production, and promotes brain tumorigenesis.”  
> _model's note: Proposes a mechanism (PGK1-PDHK1-PDH inhibition) diverting pyruvate to lactate; not a statement of Warburg's gap._
>

---

### 15. The tyrosine kinase receptor Tie2 was initially identified as a specific vascular growth factor that governed several properties of endothelial cells under both physiological and pathological conditions.

- **Book:** 12.2 Key Angiogenic Factors (`/docs/Chapter12/2_Key_Angiogenic_Factors`)
- **Fact id:** `cancer-the-tyrosine-kinase-receptor-tie2-was-initially-identified-as-a-specific-`
- **Status:** `partially_supported` · looked up in gene-protein-db · 1 record(s)
- **Why flagged:** plural claim: only one record supports one instance

> **supports** · UniProt · [UniProt:Q02763](https://rest.uniprot.org/uniprotkb/Q02763)  
> Angiopoietin-1 receptor  
> “Tyrosine-protein kinase that acts as a cell-surface receptor for ANGPT1, ANGPT2 and ANGPT4 and regulates angiogenesis, endothelial cell survival, proliferation, migration, adhesion and cell spreading, reorganization of the actin cytoskeleton, but also maintenance of vascular quiescence.”  
> _model's note: Receptor tyrosine kinase regulating several endothelial cell properties._
>

---

### 16. Tumor hypoxia is associated with more aggressive malignant behavior and reduced survival across multiple cancer types.

- **Book:** 12.3 Role of Hypoxia in Angiogenesis (`/docs/Chapter12/3_Role_of_Hypoxia_in_Angiogenesis`)
- **Fact id:** `cancer-tumor-hypoxia-is-associated-with-more-aggressive-malignant-behavior-and-r`
- **Status:** `partially_supported` · looked up in pubmed · 2 record(s)
- **Why flagged:** plural claim: only one record supports one instance

> **supports** · PubMed · [PMID:39875616](https://pubmed.ncbi.nlm.nih.gov/39875616/)  
> Tumour hypoxia in driving genomic instability and tumour evolution.  
> “Intratumour hypoxia is a feature of all heterogenous solid tumours. Increased levels or subregions of tumour hypoxia are associated with an adverse clinical prognosis, particularly when this co-occurs with genomic instability.”  
> _model's note: States hypoxia in all heterogeneous solid tumours is associated with adverse clinical prognosis._
>
> **partial** · PubMed · [PMID:40312969](https://pubmed.ncbi.nlm.nih.gov/40312969/)  
> Charting the single-cell and spatial landscape of IDH-wild-type glioblastoma with GBmap.  
> “The TSS demonstrated that highly organized tumors, characterized by well-defined vasculature and hypoxic niches, correlated with worse survival outcomes.”  
> _model's note: one instance: glioblastoma hypoxic niches correlated with worse survival._
>

---

### 17. Research and development of drugs in this area have so far begun to yield positive results with therapies such as Bevacizumab being implemented in the treatment of several cancer types.

- **Book:** 12.7 Clinical Implications and Future Directions (`/docs/Chapter12/7_Clinical_Implications_and_Future_Directions`)
- **Fact id:** `cancer-research-and-development-of-drugs-in-this-area-have-so-far-begun-to-yield`
- **Status:** `partially_supported` · looked up in fda · 1 record(s)
- **Why flagged:** plural claim: only one record supports one instance

> **supports** · openFDA · [0a562b4e-67ce-4bab-852c-d9ee71e55fb8](https://api.fda.gov/drug/label.json?search=set_id:0a562b4e-67ce-4bab-852c-d9ee71e55fb8)  
> MVASI, BEVACIZUMAB-AWWB  
> “Recurrent glioblastoma in adults. ( 1.3 ) Metastatic renal cell carcinoma in combination with interferon-alfa. ( 1.4 ) Persistent, recurrent, or metastatic cervical cancer, in combination with paclitaxel and cisplatin, or paclitaxel and topotecan. ( 1.5 )”  
> _model's note: Label lists glioblastoma, renal cell and cervical cancer among bevacizumab indications._
>

---

### 18. Several studies indicate that tumor-associated macrophages (TAMs) usually have a pro-tumoral action, since they can stimulate angiogenesis, increase tumor cell invasion and motility, and have an immunosuppressive action.

- **Book:** 14.1 Components of the Tumor Microenvironment (`/docs/Chapter14/1_Components_of_the_Tumor_Microenvironment`)
- **Fact id:** `cancer-several-studies-indicate-that-tumor-associated-macrophages-tams-usually-h`
- **Status:** `partially_supported` · looked up in pubmed · 2 record(s)
- **Why flagged:** plural claim: only one record supports one instance

> **supports** · PubMed · [PMID:35844605](https://pubmed.ncbi.nlm.nih.gov/35844605/)  
> Shaping Polarization Of Tumor-Associated Macrophages In Cancer Immunotherapy.  
> “TAMs predominantly play a M2-like tumor-promoting role in the TME and regulate various malignant effects, such as angiogenesis, immune suppression, and tumor metastasis; hence, TAMs have emerged as a hot topic of research in cancer therapy.”  
> _model's note: TAMs predominantly tumor-promoting, regulating angiogenesis, immune suppression and metastasis._
>
> **partial** · PubMed · [PMID:38035101](https://pubmed.ncbi.nlm.nih.gov/38035101/)  
> Tumor-associated macrophages: an effective player of the tumor microenvironment.  
> “This M2-TAM bias in the TME promotes cancer cell proliferation, neoangiogenesis, lymphangiogenesis, epithelial-to-mesenchymal transition, matrix remodeling for metastatic support, and TME manipulation to an immunosuppressive state.”  
> _model's note: Pro-tumor M2-TAM promotes angiogenesis, metastasis support and immunosuppression; 'usually' is framed via M2 bias._
>

---

### 19. Boolean logic circuits implemented in CAR-T cells enable AND-gate activation requiring multiple antigens or NOT-gate inhibition by normal tissue markers, reducing on-target off-tumor toxicity.

- **Book:** 15.5 Future Directions (`/docs/Chapter15/5_Future_Directions`)
- **Fact id:** `cancer-boolean-logic-circuits-implemented-in-car-t-cells-enable-and-gate-activat`
- **Status:** `partially_supported` · looked up in pubmed · 2 record(s)
- **Why flagged:** plural claim: only one record supports one instance

> **supports** · PubMed · [PMID:36890224](https://pubmed.ncbi.nlm.nih.gov/36890224/)  
> Co-opting signalling molecules enables logic-gated control of CAR T cells.  
> “We exploited the cooperative role of LAT and SLP-76 to engineer logic-gated intracellular network (LINK) CAR, a rapid and reversible Boolean-logic AND-gated CAR T cell platform that outperforms other systems in both efficacy and prevention of on-target, off-tumour toxicity.”  
> _model's note: AND-gated LINK CAR outperforms others in preventing on-target off-tumour toxicity; AND-gate only, no NOT-gate._
>
> **partial** · PubMed · [PMID:41176533](https://pubmed.ncbi.nlm.nih.gov/41176533/)  
> On-target off-tumor toxicity of claudin18.2-directed CAR-T cells in preclinical models.  
> “Additionally, we demonstrate the utility of this model in testing strategies to mitigate on-target toxicity, such as Boolean-logic AND-gate approaches.”  
> _model's note: Tests Boolean-logic AND-gate strategies to mitigate on-target toxicity; model use, no outcome stated._
>

---

### 20. The molecular basis of T-cell exhaustion involves persistent antigen exposure driving hyperactivation of T cells, which ultimately leads to sustained co-expression of multiple inhibitory receptors including PD-1, LAG-3, TIM-3, 2B4, CD160, and TIGIT.

- **Book:** 16.1 Immune Surveillance and Escape (`/docs/Chapter16/1_Immune_Surveillance_and_Escape`)
- **Fact id:** `cancer-the-molecular-basis-of-t-cell-exhaustion-involves-persistent-antigen-expo`
- **Status:** `partially_supported` · looked up in pubmed · 2 record(s)
- **Why flagged:** plural claim: only one record supports one instance

> **supports** · PubMed · [PMID:37503045](https://pubmed.ncbi.nlm.nih.gov/37503045/)  
> Five inhibitory receptors display distinct vesicular distributions in T cells.  
> “Upon induction of T cell exhaustion in response to persistent antigen, prominently in the anti-tumor immune response, many are expressed simultaneously. Key inhibitory receptors are CTLA-4, PD-1, LAG3, TIM3 and TIGIT, as investigated here.”  
> _model's note: Persistent antigen induces exhaustion with simultaneous inhibitory receptors, naming CTLA-4, PD-1, LAG3, TIM3, TIGIT; 2B4/CD160 not named._
>
> **related** · PubMed · [PMID:31207604](https://pubmed.ncbi.nlm.nih.gov/31207604/)  
> TOX is a critical regulator of tumour-specific T cell differentiation.  
> “Tox-deleted TST cells did not upregulate genes for inhibitory receptors (such as Pdcd1, Entpd1, Havcr2, Cd244 and Tigit)”  
> _model's note: Names exhaustion-associated inhibitory receptor genes including Cd244 (2B4) and Tigit; does not describe co-expression or hyperactivation._
>

---

### 21. Over the past decade, a number of reports have provided data indicating that tumor cells can either directly produce PGs or induce macrophages in the tumor microenvironment to secrete PGs.

- **Book:** 16.4 Tumor-Induced Immune Suppression (`/docs/Chapter16/4_Tumor_Induced_Immune_Suppression`)
- **Fact id:** `cancer-over-the-past-decade-a-number-of-reports-have-provided-data-indicating-th`
- **Status:** `partially_supported` · looked up in pubmed · 2 record(s)
- **Why flagged:** plural claim: only one record supports one instance

> **supports** · PubMed · [PMID:40425576](https://pubmed.ncbi.nlm.nih.gov/40425576/)  
> Soft matrix promotes immunosuppression in tumor-resident immune cells via COX-FGF2 signaling.  
> “These immunosuppressive events are mediated by tumor cell derived fibroblast growth factor 2 (FGF2) and prostaglandin E2 (PGE2).”  
> _model's note: Tumor cells are a source of PGE2 in the microenvironment._
>
> **partial** · PubMed · [PMID:41196020](https://pubmed.ncbi.nlm.nih.gov/41196020/)  
> Tumor-Associated Macrophages Produce PGE2 to Promote CD8+ T-cell Exhaustion and Drive Resistance to PD-L1 Blockade in Microsatellite-Stable Colorectal Cancer.  
> “Transcriptomic analysis revealed elevated COX1/2 expression in TAMs in MSS tumors compared with MSI tumors.”  
> _model's note: Tumor-associated macrophages express COX1/2 and drive PGE2 signalling; macrophage induction by tumor cells not stated._
>

---

### 22. Synergistic Benefits Across Disease Categories: An important advantage of lifestyle-based prevention strategies is that they address risk factors common to multiple chronic diseases.

- **Book:** 17.4 Integration of Prevention Strategies (`/docs/Chapter17/5_Integration_of_Prevention_Strategies`)
- **Fact id:** `cancer-synergistic-benefits-across-disease-categories-an-important-advantage-of-`
- **Status:** `partially_supported` · looked up in pubmed · 2 record(s)
- **Why flagged:** plural claim: only one record supports one instance

> **supports** · PubMed · [PMID:24969415](https://pubmed.ncbi.nlm.nih.gov/24969415/)  
> Prevention of diseases after menopause.  
> “Evidence-based prevention for the diseases noted above include lifestyle management, cessation of smoking, curtailing excessive alcohol consumption, a healthy diet and moderate exercise, as well as mentally stimulating activities.”  
> _model's note: Lifestyle measures are proposed to prevent several chronic diseases including cancer, obesity, diabetes and cardiovascular disease._
>
> **partial** · PubMed · [PMID:31806905](https://pubmed.ncbi.nlm.nih.gov/31806905/)  
> Chronic inflammation in the etiology of disease across the life span.  
> “In the present Perspective we describe the multi-level mechanisms underlying SCI and several risk factors that promote this health-damaging phenotype, including infections, physical inactivity, poor diet, environmental and industrial toxicants and psychological stress.”  
> _model's note: Lists shared lifestyle risk factors for chronic inflammation underlying cancer and other diseases; interventions not detailed here._
>

---

### 23. The complete surgical cytoreduction possible is decisive for the prognosis, which requires multiple organ resections in addition to a partial to subtotal parietal peritonectomy.

- **Book:** 20.2 Types of Surgical Procedures (`/docs/Chapter20/3_Types_of_Surgical_Procedures`)
- **Fact id:** `cancer-the-complete-surgical-cytoreduction-possible-is-decisive-for-the-prognosi`
- **Status:** `partially_supported` · looked up in pubmed · 1 record(s)
- **Why flagged:** plural claim: only one record supports one instance

> **supports** · PubMed · [PMID:21424289](https://pubmed.ncbi.nlm.nih.gov/21424289/)  
> [Peritoneal carcinomatosis].  
> “Decisive for the prognosis is a complete cytoreduction, which in most cases necessitates multi-organ resection in addition to a partial or subtotal parietal peritonectomy (PE).”  
> _model's note: States complete cytoreduction is decisive for prognosis and needs multi-organ resection plus partial/subtotal peritonectomy._
>

---

### 24. Doxil was the first nanotherapeutic approved to treat cancer and is used for treating ovarian cancer, AIDS-related Kaposi's sarcoma, and multiple myeloma.

- **Book:** 27.1 Nanoparticles for Drug Delivery (`/docs/Chapter27/1_Nanoparticles_for_Drug_Delivery`)
- **Fact id:** `cancer-doxil-was-the-first-nanotherapeutic-approved-to-treat-cancer-and-is-used-`
- **Status:** `partially_supported` · looked up in fda · 1 record(s)
- **Why flagged:** plural claim: only one record supports one instance

> **supports** · openFDA · [917eddf9-1d3f-4abe-8c81-d33b066e5bae](https://api.fda.gov/drug/label.json?search=set_id:917eddf9-1d3f-4abe-8c81-d33b066e5bae)  
> DOXIL, DOXORUBICIN HYDROCHLORIDE  
> “Ovarian cancer: After failure of platinum-based chemotherapy ( 1.1 ) • AIDS-related Kaposi’s Sarcoma: After failure of prior systemic chemotherapy or intolerance to such therapy ( 1.2 ) • Multiple Myeloma: In combination with bortezomib in patients who have not previously received bortezomib and have received at least one prior therapy ( 1.3 )”  
> _model's note: label lists ovarian cancer, AIDS-related Kaposi's sarcoma and multiple myeloma indications_
>

---

### 25. Patients with multiple myeloma and other monoclonal gammopathies often have kidney dysfunction due to a wide range of associated pathologies.

- **Book:** 33.7 Special Populations (`/docs/Chapter33/8_Special_Populations`)
- **Fact id:** `cancer-patients-with-multiple-myeloma-and-other-monoclonal-gammopathies-often-ha`
- **Status:** `partially_supported` · looked up in pubmed · 1 record(s)
- **Why flagged:** plural claim: only one record supports one instance

> **supports** · PubMed · [PMID:33440212](https://pubmed.ncbi.nlm.nih.gov/33440212/)  
> Management of acute kidney injury in symptomatic multiple myeloma.  
> “Symptomatic multiple myeloma is commonly complicated by acute kidney injury through various mechanisms.”  
> _model's note: States acute kidney injury commonly complicates symptomatic myeloma; other gammopathies and exact frequency not given._
>

---

### 26. Symptoms are usually present for several months before the diagnosis is made, with an average duration of approximately 3 months.

- **Book:** 35.1 Sarcomas (`/docs/Chapter35/2_Sarcomas`)
- **Fact id:** `cancer-symptoms-are-usually-present-for-several-months-before-the-diagnosis-is-m`
- **Status:** `partially_supported` · looked up in pubmed · 2 record(s)
- **Why flagged:** plural claim: only one record supports one instance

> **supports** · PubMed · [PMID:37567167](https://pubmed.ncbi.nlm.nih.gov/37567167/)  
> Assessment of the Interval to Diagnosis in Pediatric Bone Sarcoma.  
> “Average symptom duration was 5.4 ± 13.9 months (range, 0.1-84).”  
> _model's note: Pediatric bone sarcoma (osteosarcoma and Ewing) average symptom duration of 5.4 months._
>
> **partial** · PubMed · [PMID:3475157](https://pubmed.ncbi.nlm.nih.gov/3475157/)  
> Extraskeletal osteosarcoma.  
> “The preoperative duration of symptoms ranged from 2 weeks to 25 years (median, 6 months).”  
> _model's note: Median 6 months for extraskeletal osteosarcoma; a median, not an average, and a single subtype._
>

---

### 27. The ATM kinase plays an early, pivotal role in the signaling process by detecting DSBs and relaying this information to numerous downstream transducer and effector proteins.

- **Book:** 4.4 DNA Repair Mechanisms and Their Failure in Cancer (`/docs/Chapter4/4_DNA_Repair_Mechanisms_and_Their_Failure_in_Cancer`)
- **Fact id:** `cancer-the-atm-kinase-plays-an-early-pivotal-role-in-the-signaling-process-by-de`
- **Status:** `partially_supported` · looked up in gene-protein-db · 1 record(s)
- **Why flagged:** plural claim: only one record supports one instance

> **supports** · UniProt · [UniProt:Q13315](https://rest.uniprot.org/uniprotkb/Q13315)  
> Serine-protein kinase ATM  
> “Serine/threonine protein kinase which activates checkpoint signaling upon double strand breaks (DSBs), apoptosis and genotoxic stresses such as ionizing ultraviolet A light (UVA), thereby acting as a DNA damage sensor”  
> _model's note: ATM described as DNA damage sensor activating checkpoint signaling upon double strand breaks._
>
> **supports** · UniProt · [UniProt:Q13315](https://rest.uniprot.org/uniprotkb/Q13315)  
> Serine-protein kinase ATM  
> “Phosphorylates DYRK2, CHEK2, p53/TP53, FBXW7, FANCD2, NFKBIA, BRCA1, CREBBP/CBP, RBBP8/CTIP, FBXO46, MRE11, nibrin (NBN), RAD50, RAD17, PELI1, TERF1, UFL1, RAD9, UBQLN4, UCHL3 and DCLRE1C”  
> _model's note: Lists many downstream proteins ATM phosphorylates, matching relay to downstream effectors._
>

---

### 28. The list of recurrently mutated cancer genes is relatively short, but there are many rarely mutated genes.

- **Book:** 4.5 Genomic Instability (`/docs/Chapter4/5_Genomic_Instability`)
- **Fact id:** `cancer-the-list-of-recurrently-mutated-cancer-genes-is-relatively-short-but-ther`
- **Status:** `partially_supported` · looked up in pubmed · 1 record(s)
- **Why flagged:** plural claim: only one record supports one instance

> **supports** · PubMed · [PMID:23539594](https://pubmed.ncbi.nlm.nih.gov/23539594/)  
> Cancer genome landscapes.  
> “For most cancer types, this landscape consists of a small number of "mountains" (genes altered in a high percentage of tumors) and a much larger number of "hills" (genes altered infrequently).”  
> _model's note: Few frequently altered genes versus many infrequently altered genes, matching the claim._
>

---

### 29. Mutations in histone genes or chromatin modifier proteins are frequently detected in many cancer types, resulting in impairments in gene expression programs and genomic integrity.

- **Book:** 7.3 Histone Modifications in Cancer (`/docs/Chapter7/3_Histone_Modifications_in_Cancer`)
- **Fact id:** `cancer-mutations-in-histone-genes-or-chromatin-modifier-proteins-are-frequently-`
- **Status:** `partially_supported` · looked up in pubmed · 2 record(s)
- **Why flagged:** plural claim: only one record supports one instance

> **supports** · PubMed · [PMID:34619527](https://pubmed.ncbi.nlm.nih.gov/34619527/)  
> Targeting ARID1A mutations in cancer.  
> “Genes encoding SWI/SNF chromatin remodeling complex subunits are collectively mutated in approximately 20% of human cancers.”  
> _model's note: Gives frequency (~20% of human cancers) of mutations in chromatin remodeler genes; impairment of expression not in this sentence._
>
> **partial** · PubMed · [PMID:22286061](https://pubmed.ncbi.nlm.nih.gov/22286061/)  
> Driver mutations in histone H3.3 and chromatin remodelling genes in paediatric glioblastoma.  
> “Somatic mutations in the H3.3-ATRX-DAXX chromatin remodelling pathway were identified in 44% of tumours (21/48).”  
> _model's note: one instance: chromatin remodelling and histone H3.3 pathway mutations in 44% of paediatric glioblastomas._
>

---

### 30. Cancer is also a disease of transcriptional mis-regulation and, given the role of chromatin in this process, it is not surprising to realize that many mutations in chromatin-controlling factors have been observed in human cancers.

- **Book:** 7.6 Epigenetic Reprogramming in Cancer (`/docs/Chapter7/6_Epigenetic_Reprogramming_in_Cancer`)
- **Fact id:** `cancer-cancer-is-also-a-disease-of-transcriptional-mis-regulation-and-given-the-`
- **Status:** `partially_supported` · looked up in pubmed · 2 record(s)
- **Why flagged:** plural claim: only one record supports one instance

> **supports** · PubMed · [PMID:27194046](https://pubmed.ncbi.nlm.nih.gov/27194046/)  
> Epigenetic Determinants of Cancer.  
> “Cancer genetics and epigenetics are inextricably linked in generating the malignant phenotype; epigenetic changes can cause mutations in genes, and, conversely, mutations are frequently observed in genes that modify the epigenome.”  
> _model's note: States mutations are frequently observed in epigenome-modifying genes in cancer; no numeric frequency._
>
> **partial** · PubMed · [PMID:28199314](https://pubmed.ncbi.nlm.nih.gov/28199314/)  
> Whole-genome landscape of pancreatic neuroendocrine tumours.  
> “Somatic mutations, including point mutations and gene fusions, were commonly found in genes involved in four main pathways: chromatin remodelling, DNA damage repair, activation of mTOR signalling (including previously undescribed EWSR1 gene fusions), and telomere maintenance.”  
> _model's note: one instance: chromatin remodelling genes commonly mutated in pancreatic neuroendocrine tumours._
>

---
