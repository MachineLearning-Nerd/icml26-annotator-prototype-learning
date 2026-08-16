# Primary-source and provenance audit

## Paper identity

- Primary identifier: arXiv 2508.02123v1.
- Primary title: *Understanding the Essence: Delving into Annotator Prototype
  Learning for Multi-Class Annotation Aggregation*.
- Challenge/OpenReview title: *Let the Prototype Guide You: Robust Aggregation
  of Sparse Multi-Class Annotations via Annotator Prototype Learning*.
- Authors: Ju Chen, Jun Feng, and Shenyu Zhang.
- Primary URL: https://arxiv.org/abs/2508.02123v1.
- Challenge URL: https://openreview.net/forum?id=KJq0iScNM6.

The title difference is an index distinction, not a claim that two papers were
reproduced. The arXiv v1 source is the authority for the method and numerical
claims in this repository.

## Pinned paper files

| File | Retrieval or source | SHA-256 |
|---|---|---|
| paper_2508.02123.pdf | arXiv v1 PDF, retrieved 2026-08-16 | dd828f554eeb1f5c8b36d0bcc4efbba1d99ecde9a8dfbc029babbcf0ec609b2c |
| source/arxiv/2508.02123.tar | arXiv v1 e-print source, retrieved 2026-08-16 | 6af318fa7f16a8dc711b041ca828ddaa1964dd7b935303bfccaf5e940f8f2108 |
| source/Formatting-Instructions-LaTeX-2026.tex | source file in the e-print archive | 2b1b3d6f44c74ed16172b5e473fb75078be33e568b5c39b0d49befa25f8d3c4b |

The ar5iv text audit was retrieved on 2026-07-23 at
https://ar5iv.labs.arxiv.org/html/2508.02123. Its SHA-256 was
1910a8d019a88a17bc2c17441a41850645cf29d99bec84c19bc61f50cc5d500b.

## Paper anchors used by the claims

- Architecture: Method, generative process, and equations (7)--(14).
- Domain: Table 3 and Experimental Setup; 11 datasets, accuracy metric,
  |S|=2, e=1, f=5, m=1.35, and xi=0.001.
- C2: Table 2 and the Val5 case study. The source states the 15% improvement;
  the released DS baseline is 0.41 and the contract evaluates PTBCC at 0.56.
- C3: Table 4, whose printed macro values are MV 0.6986, BWA 0.7132, FGBCC
  0.7175, and PTBCC 0.7472.
- C4: Table 5 and the Number of Prototypes subsection. The source distinguishes
  Dirichlet initialization from the 3-Ran all-entries-uniform matrix.
- C5: Efficiency subsection and Figure 5. The source says less than 10% of
  confusion-matrix runtime but does not publish raw timing values or one named
  aggregate denominator.

## Data and reference implementations

- The exact 11-dataset cleaned files are pinned to
  JuJuCHEN-HHU/CodeForFGBCC at commit
  e2ca2b8a876bf9cceb871e8cec9081870a30aab4. The data manifest records every
  downloaded file hash.
- The FGBCC reference source is code/FGBCC/method.py at that commit, with
  SHA-256 6e8e1545c950c4895165eb1aa3bc37e06097e6fa7887fe9d387e1a9e7b091979.
  Its Aircr output is used as a golden equivalence check.
- BWA is pinned to yuan-li/truth-inference-at-scale at commit
  621789b2d57324d3559dc973b2613d2296d73f55. The reference code hash is
  96cd391294664de983e8c8af340f4dec9cfca322f35bb0562ab086cef5985151.
- The DS reference is the public truth-inference survey bundle, whose hash is
  fcb72da704bf06701ebec5f47e3d85b583354a098e4410a29750abdaaa59d9a2.

## Author-code search boundary

The pinned arXiv source and metadata do not provide a PTBCC code or data
repository link. Searches performed for the exact paper title, arXiv
identifier, and author-linked repository names found no author PTBCC
implementation. The FGBCC repository is used only for its public data and
reference baseline; it is not labeled as PTBCC author code. This is a
reproducibility boundary, not proof that no unindexed implementation exists.

## Catalog audit

The source contains PTBCC, 11 datasets, and 15%/about-3% claims. It does not
contain the catalog's CPBCC/26% or 10-dataset 68.73-to-74.11 wording. Those
catalog statements are recorded as falsified in [claims.json](claims.json).
