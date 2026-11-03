# Wording changes — review sheet

## Summary

**13 proposed rewordings** of the book's sentences: 13 waiting for a reviewer, 0 disputed between reviewers, 0 accepted, 0 rejected. They are listed in priority order; work from the top. A model wrote every proposal. The book's own sentence is never edited; each change records what it said, what is proposed, why, and the database quote behind it.

### How to review

1. Read the book's sentence, the proposal, the reason and the quote. Open the record link if the quote is not enough.
2. Use the review dashboard (`streamlit run review_app.py`), or write a row in `changes/decisions/<your-name>.jsonl` with `decision` one of: `accept` (use the proposed wording as written); `accept_edited` (use my wording instead (put it in `edited`)); `reject` (keep the book's sentence; do not reword).
3. A row needs `change_id`, `decision`, your name as `reviewer`, the `date`, and optionally `note` and `edited`. Two reviewers who disagree make the change `disputed`; a row in `changes/decisions.jsonl` is the final call.
4. Run `python3 pipeline/10_check_changes.py`. When you are through, run `python3 pipeline/11_implement_changes.py` to apply the accepted ones.

A proposal is checked against the stored quotes by the pipeline. Wording you write yourself (`accept_edited`) is not; you are the check on it.

---

### 1 of 13. 12.2 Key Angiogenic Factors · remove_absolute · priority 1 · `proposed`

- **Why this position:** a record points against the claim
- **Change id:** `cancer-plgf-is-predominantly-expressed-in-placenta-and-binds-exclusively-to-vegf#1`
- **Book:** PlGF is predominantly expressed in placenta and binds exclusively to VEGFR-1.
- **Proposed:** PlGF is predominantly expressed in placenta and binds to VEGFR-1.
- **Why:** UniProt records that the PlGF-2 isoform also binds neuropilin-1 and neuropilin-2, so "exclusively" is not carried by the record. "Binds to VEGFR-1" is stated by the same record. The placenta half is unchanged and was not checked.
- **Record:** [UniProt:P49763](https://rest.uniprot.org/uniprotkb/P49763) “It binds to the receptor FLT1/VEGFR-1. Isoform PlGF-2 binds NRP1/neuropilin-1 and NRP2/neuropilin-2 in a heparin-dependent manner.”
- **Proposed by:** model on 2026-11-03

### 2 of 13. 12.6 Anti-Angiogenic Therapy · hedge · priority 1 · `proposed`

- **Why this position:** a record points against the claim
- **Change id:** `cancer-the-authors-concluded-that-the-use-of-bevacizumab-was-significantly-assoc#1`
- **Book:** The authors concluded that the use of bevacizumab was significantly associated with an increased risk of developing venous thromboembolism in cancer patients receiving this drug.
- **Proposed:** Some studies have found that bevacizumab is associated with an increased risk of venous thromboembolism in cancer patients receiving it, but the evidence is mixed.
- **Why:** One SEER-Medicare colorectal cohort found bevacizumab protective (HR 0.68), and a review calls the venous literature conflicting. The book reports what its authors concluded; the softer wording keeps that finding without presenting it as settled. The same claim also appears in 24.6 with different wording and was not changed here.
- **Record:** [PMID:35129311](https://pubmed.ncbi.nlm.nih.gov/35129311/) “After adjustment, any therapy and bevacizumab (HR 0.68, 0.58-0.78) in particular were protective.”
- **Record:** [PMID:31317482](https://pubmed.ncbi.nlm.nih.gov/31317482/) “Bevacizumab, an inhibitor of vascular endothelial growth factor, increases arterial and possibly venous thrombotic risk, although the literature is conflicting about the latter.”
- **Proposed by:** model on 2026-11-03

### 3 of 13. 13.2 Epithelial-Mesenchymal Transition (EMT) · scope · priority 1 · `proposed`

- **Why this position:** a record points against the claim
- **Change id:** `cancer-aberrant-de-novo-expression-of-n-cadherin-has-been-noted-in-carcinomas-fr#1`
- **Book:** Aberrant de novo expression of N-cadherin has been noted in carcinomas from the breast, prostate, bladder and the head and neck region, where it parallels a downregulation of E-cadherin and a decrease in tumor differentiation.
- **Proposed:** Aberrant de novo expression of N-cadherin has been noted in some carcinomas, including breast, prostate, bladder and head and neck, where it has been reported to parallel a downregulation of E-cadherin and a decrease in tumor differentiation; one breast carcinoma study found no such correlation.
- **Why:** A breast carcinoma study found no correlation between E/N-cadherin and size, grade, node status or receptors, so the parallel with E-cadherin loss is not universal. The wording now says "some" and "has been reported" and notes the one study.
- **Record:** [PMID:14645693](https://pubmed.ncbi.nlm.nih.gov/14645693/) “There were no correlations between E/N-cadherin and size, grade, node status, or receptors.”
- **Proposed by:** model on 2026-11-03

### 4 of 13. 15.3 Implications for Treatment Resistance · attribute · priority 1 · `proposed`

- **Why this position:** a record points against the claim
- **Change id:** `cancer-gamma-secretase-inhibitors-that-target-notch-signaling-sensitize-colon-ca#1`
- **Book:** Gamma-secretase inhibitors that target Notch signaling sensitize colon cancer cells to chemotherapy by inhibiting oxaliplatin-induced Notch-1 receptor and Hes-1 activity.
- **Proposed:** In some colon cancer models, gamma-secretase inhibitors that target Notch signaling have been reported to blunt oxaliplatin-induced Notch-1 and Hes-1 activity; one study found that gamma-secretase inhibition reduced oxaliplatin-induced apoptosis instead.
- **Why:** One record supports the Hes-1 finding (GSI34 blunted Hes-1 activation). Another found gamma-secretase inhibition reduced oxaliplatin-induced apoptosis, the opposite of sensitizing. "Sensitize ... to chemotherapy" is therefore not carried by the evidence; the rewording keeps the supported part and states the conflict.
- **Record:** [PMID:19147571](https://pubmed.ncbi.nlm.nih.gov/19147571/) “Subsequent inhibition of Notch-1 signaling with a sulfonamide GSI (GSI34) prevented the induction of NICD by chemotherapy and blunted Hes-1 activation. Blocking the activation of Notch signaling with GSI34 sensitized cells to chemotherapy and was synergistic with oxaliplatin, 5-FU, and SN-38.”
- **Record:** [PMID:23887890](https://pubmed.ncbi.nlm.nih.gov/23887890/) “Unexpectedly, gamma-secretase inhibition reduced oxaliplatin-induced apoptosis”
- **Proposed by:** model on 2026-11-03

### 5 of 13. 15.3 Implications for Treatment Resistance · scope · priority 1 · `proposed`

- **Why this position:** a record points against the claim
- **Change id:** `cancer-regorafenib-an-oral-multikinase-inhibitor-blocking-activity-of-protein-ki#1`
- **Book:** Regorafenib, an oral multikinase inhibitor blocking activity of protein kinases involved in angiogenesis, oncogenesis, metastasis, and tumor immunity, decreases stemness phenotypes including tumor sphere formation and side population fraction in colorectal cancer cells.
- **Proposed:** Regorafenib, an oral multikinase inhibitor blocking activity of protein kinases involved in angiogenesis, oncogenesis, metastasis, and tumor immunity, decreased stemness phenotypes including tumor sphere formation and side-population in HCT-116R and DLD-1R colorectal cancer cells; another study found that colorectal cancer tumorsphere formation was not inhibited by regorafenib.
- **Why:** One study supports the decrease in two colorectal cell lines (HCT-116R and DLD-1R; the quote does not say what the R stands for); a second found tumorsphere formation was inhibited by BBI608 but not by regorafenib. The wording now names the cells and states both. The descriptive clause about the drug was left as the book wrote it and was not checked.
- **Record:** [PMID:30005681](https://pubmed.ncbi.nlm.nih.gov/30005681/) “We showed that regorafenib treatment decreased the stemness phenotypes including tumor sphere formation, and side-population, of both HCT-116R and DLD-1R cells.”
- **Record:** [PMID:33023006](https://pubmed.ncbi.nlm.nih.gov/33023006/) “The formation of colorectal cancer stem-like tumorspheres was inhibited by BBI608, a STAT3 inhibitor, but not by regorafenib.”
- **Proposed by:** model on 2026-11-03

### 6 of 13. 15.3 Implications for Treatment Resistance · scope · priority 1 · `proposed`

- **Why this position:** a record points against the claim
- **Change id:** `cancer-the-hedgehog-pathway-regulates-autophagy-in-cancer-cells-and-inhibition-o#1`
- **Book:** The Hedgehog pathway regulates autophagy in cancer cells, and inhibition of this pathway augments the efficacy of chemotherapeutic agents through suppression of autophagy.
- **Proposed:** The Hedgehog pathway interplays with autophagy in multiple cancers; in BCR-ABL-positive CML cells, pharmacological or genetic inhibition of the pathway markedly induced autophagy.
- **Why:** The CML study found the opposite direction from the book (inhibiting Hh induced autophagy rather than suppressing it), and a review supports only that Hh and autophagy interact. The book's claim that inhibition augments chemotherapy by suppressing autophagy has no supporting record here, so it is dropped.
- **Record:** [PMID:30081498](https://pubmed.ncbi.nlm.nih.gov/30081498/) “Recent evidence demonstrated that Hh signaling interplays with autophagy in multiple cancers.”
- **Record:** [PMID:25701353](https://pubmed.ncbi.nlm.nih.gov/25701353/) “Our results indicated that pharmacological or genetic inhibition of Hh pathway could markedly induce autophagy in BCR-ABL(+) CML cells.”
- **Proposed by:** model on 2026-11-03

### 7 of 13. 15.3 Implications for Treatment Resistance · hedge · priority 1 · `proposed`

- **Why this position:** a record points against the claim
- **Change id:** `cancer-the-mutant-aberrant-activation-of-the-wnt-pathway-is-a-major-factor-drivi#1`
- **Book:** The mutant aberrant activation of the Wnt pathway is a major factor driving most types of tissue stem cells and contributes to DTP cell development and stemness maintenance.
- **Proposed:** Wnt/β-catenin signalling has been linked to chemoresistance, but the evidence is predominantly preclinical and varies with treatment context; in one lineage-tracing study, persister Mex3a+ cells downregulated the WNT/stem cell gene program immediately after chemotherapy.
- **Why:** A review says the Wnt-chemoresistance evidence is mostly preclinical and context-dependent, and a lineage-tracing study found the WNT program downregulated in persister cells after chemotherapy. The book's "major factor driving most types of tissue stem cells" has no record behind it, so that part is dropped, not softened.
- **Record:** [PMID:42882474](https://pubmed.ncbi.nlm.nih.gov/42882474/) “Evidence linking chemoresistance with Wnt/β-catenin, Notch and Hippo/Yes-associated protein 1 (YAP1) signalling is predominantly preclinical and varies according to treatment context, with stronger direct pathway-specific evidence for 5-FU and oxaliplatin than for irinotecan.”
- **Record:** [PMID:35773527](https://pubmed.ncbi.nlm.nih.gov/35773527/) “Lineage-tracing analysis showed that persister Mex3a+ cells downregulate the WNT/stem cell gene program immediately after chemotherapy and adopt a transient state reminiscent to that of YAP+ fetal intestinal progenitors.”
- **Proposed by:** model on 2026-11-03

### 8 of 13. 21.2 Types of Radiation Therapy · scope · priority 1 · `proposed`

- **Why this position:** a record points against the claim
- **Change id:** `cancer-imrt-has-higher-integral-radiation-dose-and-increases-the-total-volume-of#1`
- **Book:** IMRT has higher integral radiation dose and increases the total volume of tissues exposed to low-dose radiation compared to conventional radiotherapy.
- **Proposed:** Higher dose to skin and a larger low-dose region of normal tissue have been reported for MR-linac IMRT plans; another planning study found total integral dose reduced by 7-10% with IMRT without a significant increase in the 0.5-5 Gy low-dose volume.
- **Why:** The two records point in opposite directions and concern different comparisons (an MR-linac against a conventional linac, and IMRT against three-dimensional conformal radiotherapy in one planning study). The book's general statement that IMRT has a higher integral dose is not carried by either; the rewording states each finding for its own setting.
- **Record:** [PMID:33472549](https://pubmed.ncbi.nlm.nih.gov/33472549/) “However, MRL-IMRT plans had higher dose to skin and larger low dose region of normal tissues.”
- **Record:** [PMID:17208388](https://pubmed.ncbi.nlm.nih.gov/17208388/) “Overall, total integral dose was reduced by 7-10% with IMRT, p < 0.001, without significantly increasing the 0.5-5 Gy low-dose volume.”
- **Proposed by:** model on 2026-11-03

### 9 of 13. 23.4 Aromatase Inhibitors · scope · priority 1 · `proposed`

- **Why this position:** a record points against the claim
- **Change id:** `cancer-no-dose-adjustment-is-necessary-for-patients-with-renal-or-liver-impairme#1`
- **Book:** No dose adjustment is necessary for patients with renal or liver impairment or elderly patients.
- **Proposed:** For anastrozole, no dosage adjustment is necessary for patients with renal impairment or for elderly patients; for letrozole, the dose in patients with cirrhosis and severe hepatic dysfunction should be reduced by 50%.
- **Why:** The two drug labels differ: the anastrozole label gives no adjustment for renal impairment or age, and the letrozole label says to reduce the dose by 50% in cirrhosis with severe hepatic dysfunction. The book's blanket statement for patients with liver impairment is therefore not carried. Other aromatase inhibitors were not checked.
- **Record:** [03586c40-eb32-45c5-beb7-6762a6b78790](https://api.fda.gov/drug/label.json?search=set_id:03586c40-eb32-45c5-beb7-6762a6b78790) “No dosage adjustment is necessary for patients with renal impairment or for elderly patients [see Use in Specific Populations ( 8.6 )].”
- **Record:** [065cc89f-3a3f-4d78-b9f6-1c32a77ceb1c](https://api.fda.gov/drug/label.json?search=set_id:065cc89f-3a3f-4d78-b9f6-1c32a77ceb1c) “The dose of letrozole tablets in patients with cirrhosis and severe hepatic dysfunction should be reduced by 50% [see Warnings and Precautions ( 5.3 )].”
- **Proposed by:** model on 2026-11-03

### 10 of 13. 3.5 Cancer Health Disparities and Social Determinants · hedge · priority 1 · `proposed`

- **Why this position:** a record points against the claim
- **Change id:** `cancer-socioeconomic-factors-and-physician-supply-are-key-predictors-of-crc-scre#1`
- **Book:** Socioeconomic factors and physician supply are key predictors of CRC screening.
- **Proposed:** Socioeconomic factors and physician supply have been reported as key predictors of colorectal cancer screening; one state-wide analysis found physician density completely unassociated with screening, while health insurance status remained strongly related.
- **Why:** One record states the book's sentence as a finding; a state-wide analysis found physician density unassociated with screening. The wording attributes the original finding and states the contrary one.
- **Record:** [PMID:23277775](https://pubmed.ncbi.nlm.nih.gov/23277775/) “Socioeconomic factors and physician supply are key predictors of CRC screening.”
- **Record:** [PMID:39029926](https://pubmed.ncbi.nlm.nih.gov/39029926/) “In this state-wide representative analysis, physician density was completely unassociated with CRC screening, although health insurance status remains strongly related.”
- **Proposed by:** model on 2026-11-03

### 11 of 13. 6.2 Mechanisms of Tumor Suppressor Inactivation · scope · priority 1 · `proposed`

- **Why this position:** a record points against the claim
- **Change id:** `cancer-gene-specificity-of-the-epigenetic-silencing-was-observed-in-each-of-thes#1`
- **Book:** Gene specificity of the epigenetic silencing was observed in each of these tumor types, as hypermethylation of MSH2 was not detected in any of several studies.
- **Proposed:** Hypermethylation of the MSH2 promoter has been found in at least one study, in which other mismatch repair genes were not hypermethylated.
- **Why:** The book says MSH2 hypermethylation was not detected in any of several studies; the record found it in the promoter, while other mismatch repair genes were not. The book's "gene specificity in each of these tumor types" has no record checked here and is dropped.
- **Record:** [PMID:30784122](https://pubmed.ncbi.nlm.nih.gov/30784122/) “Hypermethylation also was found in the promoter of MSH2 but not in other MMR genes.”
- **Proposed by:** model on 2026-11-03

### 12 of 13. 6.2 Mechanisms of Tumor Suppressor Inactivation · scope · priority 1 · `proposed`

- **Why this position:** a record points against the claim
- **Change id:** `cancer-mechanistically-up-regulation-of-hells-confers-transcription-factor-sp1-h#1`
- **Book:** Mechanistically, up-regulation of HELLS confers transcription factor SP1 hyperactivation, leading to epigenetic silencing of multiple tumor suppressor genes through altered chromatin accessibility and nucleosome positioning.
- **Proposed:** Mechanistically, hyperactivation of the transcription factor SP1 confers up-regulation of HELLS in hepatocellular carcinoma, and up-regulated HELLS mediates epigenetic silencing of multiple tumor suppressor genes, including E-cadherin, FBP1, IGFBP3, XAF1 and CREB3L3.
- **Why:** The record reverses the direction of the first step: SP1 hyperactivation confers HELLS up-regulation, not the other way round. The silencing step is supported by the same record, which names the genes and the cancer (HCC). The book's "altered chromatin accessibility and nucleosome positioning" is not in the quotes and is dropped.
- **Record:** [PMID:30516846](https://pubmed.ncbi.nlm.nih.gov/30516846/) “We further showed that up-regulation of HELLS in HCC was conferred by hyperactivation of transcription factor specificity protein 1 (SP1).”
- **Record:** [PMID:30516846](https://pubmed.ncbi.nlm.nih.gov/30516846/) “Though this mechanism, up-regulation of HELLS mediated epigenetic silencing of multiple tumor suppressor genes including E-cadherin, FBP1, IGFBP3, XAF1 and CREB3L3 in HCC.”
- **Proposed by:** model on 2026-11-03

### 13 of 13. 7.7: Epigenetic Therapy · update · priority 2 · `proposed`

- **Why this position:** a record shows a time-bound claim has moved on
- **Change id:** `cancer-as-of-january-2022-rnk05047-has-entered-clinical-trials-to-treat-advanced#1`
- **Book:** As of January 2022, RNK05047 has entered clinical trials to treat advanced solid tumors and lymphomas.
- **Proposed:** RNK05047 is in a registered clinical trial (CHAMP-1, NCT05487170) in advanced solid tumors and diffuse large B-cell lymphoma, with a start date of 12 July 2022.
- **Why:** The registry gives a start date of 2022-07-12, after the book's "as of January 2022", and lists advanced solid tumor and DLBCL as the conditions. Lymphomas other than DLBCL were not found. The wording states the registered start date instead.
- **Record:** [NCT05487170](https://clinicaltrials.gov/study/NCT05487170) “2022-07-12”
- **Record:** [NCT05487170](https://clinicaltrials.gov/study/NCT05487170) “Advanced Solid Tumor, DLBCL”
- **Proposed by:** model on 2026-11-03

