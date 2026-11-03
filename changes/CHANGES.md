# Wording changes — review sheet

## Summary

**4 proposed rewordings** of the book's sentences: 4 waiting for a reviewer, 0 accepted, 0 rejected. They are listed in priority order; work from the top. A model wrote every proposal. The book's own sentence is never edited; each change records what it said, what is proposed, why, and the database quote behind it.

### How to review

1. Read the book's sentence, the proposal, the reason and the quote. Open the record link if the quote is not enough.
2. In `changes/decisions.jsonl`, set `decision` to one of: `accept` (use the proposed wording as written); `accept_edited` (use my wording instead (put it in `edited`)); `reject` (keep the book's sentence; do not reword).
3. Add your name as `reviewer`, today's date as `date`, and a `note` if you want to say why.
4. Run `python3 pipeline/10_check_changes.py`. When you are through, run `python3 pipeline/11_implement_changes.py` to apply the accepted ones.

A proposal is checked against the stored quotes by the pipeline. Wording you write yourself (`accept_edited`) is not; you are the check on it.

---

### 1 of 4. 12.2 Key Angiogenic Factors · remove_absolute · priority 1 · `proposed`

- **Why this position:** a record points against the claim
- **Change id:** `cancer-plgf-is-predominantly-expressed-in-placenta-and-binds-exclusively-to-vegf#1`
- **Book:** PlGF is predominantly expressed in placenta and binds exclusively to VEGFR-1.
- **Proposed:** PlGF is predominantly expressed in placenta and binds to VEGFR-1.
- **Why:** UniProt records that the PlGF-2 isoform also binds neuropilin-1 and neuropilin-2, so "exclusively" is not carried by the record. "Binds to VEGFR-1" is stated by the same record. The placenta half is unchanged and was not checked.
- **Record:** [UniProt:P49763](https://rest.uniprot.org/uniprotkb/P49763) “It binds to the receptor FLT1/VEGFR-1. Isoform PlGF-2 binds NRP1/neuropilin-1 and NRP2/neuropilin-2 in a heparin-dependent manner.”
- **Proposed by:** model on 2026-11-03

### 2 of 4. 12.6 Anti-Angiogenic Therapy · hedge · priority 1 · `proposed`

- **Why this position:** a record points against the claim
- **Change id:** `cancer-the-authors-concluded-that-the-use-of-bevacizumab-was-significantly-assoc#1`
- **Book:** The authors concluded that the use of bevacizumab was significantly associated with an increased risk of developing venous thromboembolism in cancer patients receiving this drug.
- **Proposed:** Some studies have found that bevacizumab is associated with an increased risk of venous thromboembolism in cancer patients receiving it, but the evidence is mixed.
- **Why:** One SEER-Medicare colorectal cohort found bevacizumab protective (HR 0.68), and a review calls the venous literature conflicting. The book reports what its authors concluded; the softer wording keeps that finding without presenting it as settled. The same claim also appears in 24.6 with different wording and was not changed here.
- **Record:** [PMID:35129311](https://pubmed.ncbi.nlm.nih.gov/35129311/) “After adjustment, any therapy and bevacizumab (HR 0.68, 0.58-0.78) in particular were protective.”
- **Record:** [PMID:31317482](https://pubmed.ncbi.nlm.nih.gov/31317482/) “Bevacizumab, an inhibitor of vascular endothelial growth factor, increases arterial and possibly venous thrombotic risk, although the literature is conflicting about the latter.”
- **Proposed by:** model on 2026-11-03

### 3 of 4. 13.2 Epithelial-Mesenchymal Transition (EMT) · scope · priority 1 · `proposed`

- **Why this position:** a record points against the claim
- **Change id:** `cancer-aberrant-de-novo-expression-of-n-cadherin-has-been-noted-in-carcinomas-fr#1`
- **Book:** Aberrant de novo expression of N-cadherin has been noted in carcinomas from the breast, prostate, bladder and the head and neck region, where it parallels a downregulation of E-cadherin and a decrease in tumor differentiation.
- **Proposed:** Aberrant de novo expression of N-cadherin has been noted in some carcinomas, including breast, prostate, bladder and head and neck, where it has been reported to parallel a downregulation of E-cadherin and a decrease in tumor differentiation; one breast carcinoma study found no such correlation.
- **Why:** A breast carcinoma study found no correlation between E/N-cadherin and size, grade, node status or receptors, so the parallel with E-cadherin loss is not universal. The wording now says "some" and "has been reported" and notes the one study.
- **Record:** [PMID:14645693](https://pubmed.ncbi.nlm.nih.gov/14645693/) “There were no correlations between E/N-cadherin and size, grade, node status, or receptors.”
- **Proposed by:** model on 2026-11-03

### 4 of 4. 15.3 Implications for Treatment Resistance · attribute · priority 1 · `proposed`

- **Why this position:** a record points against the claim
- **Change id:** `cancer-gamma-secretase-inhibitors-that-target-notch-signaling-sensitize-colon-ca#1`
- **Book:** Gamma-secretase inhibitors that target Notch signaling sensitize colon cancer cells to chemotherapy by inhibiting oxaliplatin-induced Notch-1 receptor and Hes-1 activity.
- **Proposed:** In some colon cancer models, gamma-secretase inhibitors that target Notch signaling have been reported to blunt oxaliplatin-induced Notch-1 and Hes-1 activity; one study found that gamma-secretase inhibition reduced oxaliplatin-induced apoptosis instead.
- **Why:** One record supports the Hes-1 finding (GSI34 blunted Hes-1 activation). Another found gamma-secretase inhibition reduced oxaliplatin-induced apoptosis, the opposite of sensitizing. "Sensitize ... to chemotherapy" is therefore not carried by the evidence; the rewording keeps the supported part and states the conflict.
- **Record:** [PMID:19147571](https://pubmed.ncbi.nlm.nih.gov/19147571/) “Subsequent inhibition of Notch-1 signaling with a sulfonamide GSI (GSI34) prevented the induction of NICD by chemotherapy and blunted Hes-1 activation. Blocking the activation of Notch signaling with GSI34 sensitized cells to chemotherapy and was synergistic with oxaliplatin, 5-FU, and SN-38.”
- **Record:** [PMID:23887890](https://pubmed.ncbi.nlm.nih.gov/23887890/) “Unexpectedly, gamma-secretase inhibition reduced oxaliplatin-induced apoptosis”
- **Proposed by:** model on 2026-11-03

