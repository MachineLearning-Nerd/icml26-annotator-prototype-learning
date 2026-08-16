# PTBCC reproduction status

**Audit date:** 2026-08-16
**Collection status:** VERIFIED_SCOPED_WITH_LIMITATIONS
**Repository target:** https://github.com/MachineLearning-Nerd/icml26-annotator-prototype-learning

## Paper identity

- arXiv v1: *Understanding the Essence: Delving into Annotator Prototype
  Learning for Multi-Class Annotation Aggregation*
- Challenge/OpenReview index: *Let the Prototype Guide You: Robust
  Aggregation of Sparse Multi-Class Annotations via Annotator Prototype
  Learning*
- Authors: Ju Chen, Jun Feng, and Shenyu Zhang
- Identifiers: arXiv 2508.02123v1 and OpenReview KJq0iScNM6

## Claims

| Claim | Verdict | Short reason |
|---|---|---|
| C1 architecture and synthetic recovery | VERIFIED | 40/40 exact-model trials improve over majority vote; prototype and worker distributions satisfy the tensor contracts. |
| C2 Val5 headline gain | VERIFIED | PTBCC 0.56 versus DS 0.41, a 15.0 percentage-point difference. |
| C3 Table 4 | BLOCKED | FGBCC reconstructs as 0.7175816744, which rounds to 0.7176 rather than 0.7175. |
| C4 prototype ablation | BLOCKED | S=2 remains the peak in tested seeds; exact stochastic S=3/S=4 attribution is unavailable without the paper seed. |
| C5 efficiency | BLOCKED | Controlled local PTBCC/FGBCC process-time ratio is 0.2258; paper timing inputs and denominator are not published. |

## Catalog corrections

The catalog text attached to this repository is not treated as paper evidence:

1. “CPBCC yields up to 26%” is falsified by the paper source: the method is
   PTBCC and the best-case statement is 15%.
2. “Boosts average accuracy from 68.73% to 74.11% across 10 datasets” is
   falsified by the source: Table 4 reports MV 0.6986, PTBCC 0.7472, over 11
   datasets.
3. The description of class-specific prototype matrices and annotator-specific
   prototype weights is supported by the paper's generative process and
   equations (7)--(14).

## Evidence and rerun note

The durable claim evidence is in .openresearch/artifacts/claim_1 through
claim_5. The first runnable outputs/full snapshot contains six public
datasets; the cumulative claim-verifier run recovered the exact 11-dataset
corpus and preserved its raw evidence and provenance. See
[CLAIM_EVIDENCE.md](CLAIM_EVIDENCE.md) for the distinction.

The fixed rerun command and environment are in
[ENVIRONMENT.md](ENVIRONMENT.md). The final publication-state verifier is
[verify_final.py](verify_final.py).
