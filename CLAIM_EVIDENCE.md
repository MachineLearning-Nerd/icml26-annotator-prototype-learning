# PTBCC claim-to-evidence map

This document explains how a paper statement becomes a result in this
repository. A verdict applies only to the scope and contract recorded in
[claims.json](claims.json).

## Evidence layers

1. **Paper layer.** The arXiv v1 PDF, source archive, and the source anchors in
   [SOURCE_AUDIT.md](SOURCE_AUDIT.md) define the statements and reported
   numbers.
2. **Input layer.** Public data files are downloaded from commit-pinned URLs
   and checked against [repro/audit/public_data_manifest.json](repro/audit/public_data_manifest.json).
3. **Implementation layer.** [repro/src/run_ptbcc.py](repro/src/run_ptbcc.py)
   reconstructs PTBCC from the paper; [repro/src/reference_baselines.py](repro/src/reference_baselines.py)
   contains the comparison implementations.
4. **Output layer.** CSV, JSON, and PNG artifacts record predictions,
   distributions, timings, and summary statistics.
5. **Audit layer.** [repro/src/claim_verifier.py](repro/src/claim_verifier.py)
   reads evidence files without importing the implementations, recomputes the
   contracts, and runs one negative control per claim.

## C1: prototype architecture

**Paper statement.** Annotators are represented by distributions over shared
prototype confusion matrices.

**Production path.**

- fit_ptbcc learns a prototype tensor with semantics
  (prototype, truth class, observed class) and a worker-weight tensor with
  semantics (worker, prototype).
- synthetic_trial creates 40 exact-model datasets with seeds 73000 through
  73039 and compares PTBCC with majority vote.
- The run exports learned_prototypes.csv, annotator_weights.csv, and
  synthetic_recovery_trials.csv.
- The independent checker verifies finite normalized rows, exactly two
  prototypes per dataset, Table 3 worker counts, all 40 wins, and mean
  matched-prototype MAE below 0.08.

**Result.** VERIFIED within the reconstruction scope: 40/40 wins and mean
matched-prototype MAE 0.0417523140. The negative control removes one required
seed and must be rejected.

## C2: Val5 headline result

**Paper statement.** PTBCC improves the Val5 result by 15 percentage points
over the best reported baseline.

**Production path.**

- The exact Val5 label/truth files are loaded from the FGBCC authors' pinned
  release and checked as 100 tasks, 38 workers, 100 truths, 5 classes, and
  1000 labels.
- The released DS reference implementation produces 0.41.
- PTBCC produces 0.56 in the cumulative evidence run.
- The checker verifies the domain, baseline identity, PTBCC value, and the
  rounded difference.

**Result.** VERIFIED: 0.56 minus 0.41 equals 0.15. This contract does not
pretend that the paper's missing PTBCC code has been recovered.

## C3: Table 4 macro accuracy

**Paper statement.** The unweighted 11-dataset macro values are MV 0.6986,
BWA 0.7132, FGBCC 0.7175, and PTBCC 0.7472.

**Production path.**

- load_paper_datasets reads the 11 Table 3 domains from the commit-pinned
  FGBCC release.
- BWA, DS, FGBCC, and PTBCC are run per dataset.
- Accuracy uses fractional credit for tied maximum predictions.
- The checker averages the per-dataset results and independently checks the
  Aircr FGBCC golden output.

**Result.** BLOCKED. The observed values are MV 0.6986047829, BWA 0.7131502844,
FGBCC 0.7175816744, and PTBCC 0.7471525427. The FGBCC result rounds to 0.7176,
not 0.7175. The exact implementation and numerical environment used for the
paper are unavailable, so the small discrepancy is recorded rather than
called a paper falsification.

## C4: prototype-count ablation

**Paper statement.** The macro peaks at S=2 with printed values for S=3 and
S=4.

**Production path.**

- S=2 reuses the deterministic main fit.
- S=3 includes the separate 3-Ran all-entries-uniform initialization.
- S=3 and S=4 Dirichlet(1) initializations are run for seeds 20260715,
  20260716, and 20260717 over all 11 datasets.
- The checker verifies the complete dataset-by-seed grid and keeps 3-Ran
  distinct from a Dirichlet draw.

**Result.** BLOCKED. S=2 is the peak in every tested seed, but no tested seed
reproduces both stochastic printed values and the paper does not disclose the
seed. The negative control must reject a mislabeled 3-Ran row.

## C5: runtime and average-accuracy claim

**Paper statement.** PTBCC is about three percentage points more accurate and
uses less than 10% of the runtime of confusion-matrix methods.

**Production path.**

- The all-11-dataset cumulative result establishes the accuracy difference of
  2.9570868254 percentage points versus FGBCC.
- process_isolated_benchmark runs five clean-process repetitions with rotated
  method order and records wall and process clocks.
- The checker recomputes per-comparator ratios and bootstrap intervals and
  rejects zero-time injection.

**Result.** BLOCKED. The local PTBCC/FGBCC process-time median is 0.2258383
with a 95% bootstrap interval [0.2007075, 0.2294063]. The paper's raw timing
table and aggregate denominator are not available, and the local FGBCC
implementation and hardware differ from the paper's setup.

## Catalog-only corrections

The attached catalog wording is audited separately from paper claims. The
source probes show that “CPBCC” and the 26% number do not occur in the pinned
paper, while PTBCC and 15% do. The catalog's 10-dataset 68.73-to-74.11 values
also do not occur; Table 4 says 11 datasets and 69.86-to-74.72. These are
FALSIFIED catalog statements, not new claims about the authors.
