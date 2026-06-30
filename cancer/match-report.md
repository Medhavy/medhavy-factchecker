# medhavi-cancer ↔ shared dictionary — match report

Scoured **3165 candidate facts** from 320 chapter sections (out of 15844 raw sentences), then matched each against the shared dictionary `facts/facts.json` (253 facts) using deterministic wording-similarity (difflib + Jaccard, numeric guard). The master dictionary was **not** modified.

## Outcome

- **3165** — new to dictionary

## Candidate facts by category

- BASIC: 2192
- MECHANISM: 557
- QUANTITY: 267
- CLASSIFICATION: 107
- DEFINITION: 42

## Note

No candidate reached the merge threshold (0.82) or near-duplicate threshold (0.7). The shared dictionary currently holds only 253 facts from one OpenStax anatomy book, so genuine overlap is small and the two books phrase shared topics differently. The closest sub-threshold pairs are listed below so an expert can judge whether any are in fact the same claim (and the dictionary would grow as more books are added).

## Closest sub-threshold pairs (topically related, not auto-merged)

- **0.55** cancer: *Central nervous system (CNS) tumors represent a diverse group of neoplasms that originate within the brain and spinal cord.*
  - dictionary: *The central nervous system (CNS) consists of the brain and the spinal cord.*
- **0.53** cancer: *M phase consists of mitosis, which is usually followed by cytokinesis.*
  - dictionary: *One cell cycle consists of interphase followed by mitosis and cytokinesis.*
- **0.50** cancer: *The M phase of the cycle corresponds to mitosis, which is usually followed by cytokinesis.*
  - dictionary: *One cell cycle consists of interphase followed by mitosis and cytokinesis.*
- **0.50** cancer: *Meningioma is a known benign central nervous system tumor commonly arising from the meninges of the brain and spinal cord.*
  - dictionary: *The central nervous system (CNS) consists of the brain and the spinal cord.*
- **0.47** cancer: *In their normal forms, these genes control the cell cycle, the sequence of events by which cells enlarge and divide.*
  - dictionary: *The cell cycle is the sequence of events from a cell's creation until it divides into two new cells.*
- **0.46** cancer: *Within the cell, the protoplasm consists of both the cytoplasm and the nucleus.*
  - dictionary: *A cell's cytoplasm consists of the organelles together with the cytosol.*
- **0.45** cancer: *Within the cytoplasm is an abundance of rough endoplasmic reticulum (rER) and a large Golgi apparatus.*
  - dictionary: *The endomembrane system includes the endoplasmic reticulum, the Golgi apparatus, and vesicles.*
- **0.42** cancer: *As viewed in the microscope, the cell cycle is divided into two basic parts: mitosis and interphase.*
  - dictionary: *One cell cycle consists of interphase followed by mitosis and cytokinesis.*
- **0.42** cancer: *In antibody responses, B cells are activated to secrete antibodies, which are proteins called immunoglobulins.*
  - dictionary: *An antibody, also called an immunoglobulin, is essentially a secreted form of a B cell receptor.*
- **0.42** cancer: *Each cell is enclosed by a delicate plasma membrane that separates its internal contents from the external environment.*
  - dictionary: *The cell membrane, also called the plasma membrane, separates a cell's interior from its exterior environment and regulates which materials pass in and out.*
- **0.41** cancer: *GBM is the most common primary brain tumor in adults, accounting for 45.2% of primary malignant brain and central nervous system (CNS) tumors.*
  - dictionary: *The central nervous system (CNS) consists of the brain and the spinal cord.*
- **0.40** cancer: *During S-phase, the DNAs of the 100,000 genes located on 23 pairs (in humans) of chromosomes are replicated, each in a timely fashion.*
  - dictionary: *Humans are diploid, having 23 pairs of chromosomes in each somatic cell.*
- **0.39** cancer: *Platelets, red blood cells (RBCs), white blood cells (WBCs), plasma (fluid), and blast cells are labeled, illustrating the key differences between healthy blood composition and leukemic blood.*
  - dictionary: *The formed elements of blood are red blood cells, white blood cells, and platelets.*
- **0.38** cancer: *Cells in multicellular organisms are organized into tissues, which combine to form organs and organ systems.*
  - dictionary: *The levels of structural organization of the human body, from simplest to most complex, are subatomic particles, atoms, molecules, organelles, cells, tissues, organs, organ systems, organisms, and the biosphere.*
- **0.38** cancer: *The other type of cell death, necrosis, is a pathological death caused by external factors such as inflammation or toxic injury.*
  - dictionary: *Necrosis is accidental cell death and causes inflammation.*
- **0.38** cancer: *Fibroblasts are the most common cell type represented in connective tissue.*
  - dictionary: *Synovial joints are the most common type of joint in the body.*
- **0.38** cancer: *For the most part, tumor stroma is formed by elements that are derived from the circulating blood and from adjacent host connective tissues.*
  - dictionary: *Blood is a connective tissue made up of formed elements (cells) and a fluid extracellular matrix called plasma.*
- **0.37** cancer: *In eukaryotes, however, the cell cycle is more complex and consists of four discrete phases.*
  - dictionary: *One cell cycle consists of interphase followed by mitosis and cytokinesis.*
- **0.37** cancer: *In simple terms, cancer is a group of more than 100 diseases that develop across time and involve the uncontrolled division of the body's cells.*
  - dictionary: *Cancer is a broad term for diseases caused by abnormal cells in the body dividing uncontrollably.*
- **0.37** cancer: *In 2018, cancer of the brain and central nervous system was the 17th most common cancer type, with an estimated 297,000 new cases worldwide.*
  - dictionary: *The central nervous system (CNS) consists of the brain and the spinal cord.*
- **0.37** cancer: *Cells are composed of water, inorganic ions, and carbon-containing (organic) molecules.*
  - dictionary: *An inorganic compound is a substance that does not contain both carbon and hydrogen.*
- **0.36** cancer: *Non-Hodgkin's lymphoma (NHL) is the 6th most common type of cancer in the UK.*
  - dictionary: *Synovial joints are the most common type of joint in the body.*
- **0.36** cancer: *Somatic cells are the best known for this cell cycle and go through 2 main phases called interphase and mitosis.*
  - dictionary: *One cell cycle consists of interphase followed by mitosis and cytokinesis.*
- **0.36** cancer: *Osteosarcoma can occur in any bone of the body.*
  - dictionary: *The femur (thigh bone) is the longest and strongest bone of the body.*
- **0.36** cancer: *Sarcomas, which are rare in humans, are solid tumors of connective tissues, such as muscle, bone, cartilage, and fibrous tissue.*
  - dictionary: *The four broad categories of human tissue are epithelial, connective, muscle, and nervous.*
