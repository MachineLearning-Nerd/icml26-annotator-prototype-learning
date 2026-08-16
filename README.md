# PTBCC: annotator prototype learning

This repository is the paper-first reproduction and claim audit for
*Understanding the Essence: Delving into Annotator Prototype Learning for
Multi-Class Annotation Aggregation*.

The repository is published as
MachineLearning-Nerd/icml26-annotator-prototype-learning. The paper is also
listed in the ICML 2026 challenge index under the title *Let the Prototype
Guide You: Robust Aggregation of Sparse Multi-Class Annotations via Annotator
Prototype Learning*.

## Paper

- Authors: Ju Chen, Jun Feng, and Shenyu Zhang.
- arXiv: [2508.02123v1](https://arxiv.org/abs/2508.02123v1).
- Challenge record: [OpenReview KJq0iScNM6](https://openreview.net/forum?id=KJq0iScNM6).
- Pinned paper files: [paper_2508.02123.pdf](paper_2508.02123.pdf) and
  [source/arxiv/2508.02123.tar](source/arxiv/2508.02123.tar).
- The paper proposes PTBCC, which represents annotators as distributions over
  a small set of shared prototype confusion matrices.

The arXiv title and the challenge title are recorded separately because they
identify the same paper through different indexes. The arXiv source is the
primary source for the claims below.

## Current verdict

This is a scoped reproduction, not a claim that the authors' unpublished
implementation has been recovered.

| Claim | Reproduction verdict | What the evidence establishes |
|---|---|---|
| C1: shared prototype confusion matrices and annotator mixtures | VERIFIED | The reconstruction has the stated tensor semantics, normalized distributions, and 40/40 deterministic synthetic recovery wins. |
| C2: 15 percentage-point Val5 gain | VERIFIED | PTBCC is 0.56 versus released DS at 0.41 on the exact Val5 domain. |
| C3: exact 11-dataset Table 4 macro | BLOCKED | MV, BWA, and PTBCC match the printed values to four decimals; reconstructed FGBCC is 0.7176 rather than 0.7175. |
| C4: exact prototype-count ablation | BLOCKED | S=2 is the peak in every tested seed, but the paper does not disclose the stochastic seed needed to attribute the exact S=3 and S=4 values. |
| C5: about 3 points at less than 10% of confusion-matrix runtime | BLOCKED | The controlled local PTBCC/FGBCC ratio is 0.2258, while the paper does not publish raw timings or a single denominator. |

Claims C1 and C2 are verified against explicit contracts and committed
evidence. BLOCKED means that the experiment is informative but the exact
paper-level statement cannot be attributed from the available source. It does
not mean that a proxy result has been silently substituted.

## What the paper is doing

The reconstruction follows the paper's generative process and equations
(7)--(14):

1. Learn a small shared tensor of prototype confusion matrices, one matrix per
   prototype and truth class.
2. Model each annotator with a normalized mixture over those prototypes rather
   than an independently learned full confusion matrix.
3. Infer latent truths, prototype assignments, prototype matrices, and
   annotator weights with the variational updates implemented in
   repro/src/run_ptbcc.py.
4. Compare the inferred truth distribution with majority vote, BWA, DS, and
   FGBCC using fractional credit for tied maxima.

The paper reports 11 real-world datasets, a best-case improvement of up to
15%, an average improvement of about 3%, and a runtime below 10% of
confusion-matrix methods. Each of those statements has a separate claim
contract in [claims.json](claims.json).

## How each claim is produced

The durable evidence path is:

paper source and data manifests
  -> reconstruction and reference baselines
  -> machine-readable CSV/JSON outputs
  -> independent file-only checker and negative controls
  -> claim verdicts and technical report

| Claim | Production path | Evidence surface |
|---|---|---|
| C1 | fit_ptbcc and synthetic_trial generate 40 exact-model trials; learned prototypes and worker mixtures are exported; the checker recomputes normalization, shape, worker-count, and recovery invariants. | [.openresearch/artifacts/claim_1](.openresearch/artifacts/claim_1), [outputs/full/synthetic_recovery_trials.csv](outputs/full/synthetic_recovery_trials.csv), [repro/src/claim_verifier.py](repro/src/claim_verifier.py) |
| C2 | The exact Val5 release is loaded, the published DS baseline and PTBCC are run, and the difference is evaluated against the 0.15 contract. | [.openresearch/artifacts/claim_2](.openresearch/artifacts/claim_2), [repro/audit/public_data_manifest.json](repro/audit/public_data_manifest.json) |
| C3 | All 11 released dataset files are loaded; MV, BWA, FGBCC, and PTBCC are averaged without dataset-size weighting; Aircr is checked against the FGBCC authors' golden output. | [.openresearch/artifacts/claim_3](.openresearch/artifacts/claim_3), [repro/src/reference_baselines.py](repro/src/reference_baselines.py) |
| C4 | S=2, S=3, and S=4 are evaluated with the disclosed initialization distinction and seeds 20260715--20260717; the checker separates the 3-Ran uniform matrix from a Dirichlet draw. | [.openresearch/artifacts/claim_4](.openresearch/artifacts/claim_4), [outputs/full/prototype_count_ablation.csv](outputs/full/prototype_count_ablation.csv) |
| C5 | Five process-isolated CPU repetitions are compared per method; wall and process clocks, ratios, and bootstrap intervals are recorded. | [.openresearch/artifacts/claim_5](.openresearch/artifacts/claim_5), [reports/ptbcc-claim-by-claim-2026-07-23/report.md](reports/ptbcc-claim-by-claim-2026-07-23/report.md) |

The independent checker is intentionally file-only: it does not import the
model or baseline implementations while evaluating the exported evidence.
Each claim has a deliberate corruption test in
[negative_control.json](.openresearch/artifacts/claim_1/negative_control.json)
and its corresponding claim directory.

## Reproduce

The fixed command inherited by the historical experiment branches is:

~~~bash
uv sync --frozen
uv run python repro/src/run_ptbcc.py --output-dir outputs/full
uv run python -m unittest -v repro.tests.test_ptbcc
~~~

The command obtains the commit-pinned public inputs described by
[repro/audit/public_data_manifest.json](repro/audit/public_data_manifest.json),
rebuilds the outputs and figures, runs the independent checker, and validates
the release artifacts. It is CPU-only and can take substantially longer than
the small synthetic checks.

The committed outputs/full directory is the original six-dataset runnable
baseline from the early branch. The complete 11-dataset evidence used for
Claims C2--C5 is preserved in the cumulative
.openresearch/artifacts/claim_2 through claim_5 bundle and its report. A fresh
fixed-command run downloads the full manifest and overwrites outputs/full with
the complete surface.

For a lightweight publication-state check after cloning, run:

~~~bash
python verify_final.py
~~~

## Branches

The final branch names describe their role:

- main: cumulative publication surface.
- baseline/validated-six-datasets: first validated data and environment
  baseline.
- baseline/frozen-runtime: runnable frozen baseline.
- audit/exact-11-dataset-corpus: recovered the exact Table 3 corpus and
  reference baselines.
- audit/exact-baselines-ablation: added exact DS/FGBCC evidence and the
  prototype-count ablation.
- audit/legacy-fgbcc-semantics: matched legacy FGBCC exponentiation semantics.
- benchmark/cpu-runtime: added process-isolated runtime measurements.
- audit/claim-verifier: added independent claim contracts and controls.

The former release-candidate branch pointed at the same commit as main and is
collapsed into main. The old orx/* names are documented in
[BRANCH_AUDIT.md](BRANCH_AUDIT.md) and are not part of the final public branch
inventory.

## Reproduction boundaries

- No author-linked PTBCC implementation was found in the pinned arXiv source,
  its metadata, or the repository search performed for the exact title and
  arXiv identifier. This repository therefore reconstructs the method from the
  paper and uses public reference implementations only for baselines.
- Five exact public releases were not present in the initial six-dataset
  baseline. The cumulative evidence bundle records the later recovery of the
  exact 11-dataset files from the FGBCC authors' pinned release.
- The paper does not disclose the random seed for the prototype ablation.
- The paper does not publish raw runtime values or a named aggregate
  denominator.
- Timing results are hardware- and implementation-specific. The controlled
  local result is evidence about this stack, not a faithful reproduction of
  the paper's reference machine.

See [SOURCE_AUDIT.md](SOURCE_AUDIT.md), [ENVIRONMENT.md](ENVIRONMENT.md), and
[CLAIM_EVIDENCE.md](CLAIM_EVIDENCE.md) for the full provenance and limitations.

## Citation

~~~bibtex
@article{chen2025understanding,
  title   = {Understanding the Essence: Delving into Annotator Prototype Learning for Multi-Class Annotation Aggregation},
  author  = {Chen, Ju and Feng, Jun and Zhang, Shenyu},
  journal = {arXiv preprint arXiv:2508.02123},
  year    = {2025},
  url     = {https://arxiv.org/abs/2508.02123}
}
~~~

Machine-readable citation metadata is in
[CITATION.cff](CITATION.cff). Please cite the paper and this reproduction
separately when reusing the code or evidence.

## Thank you

Thank you to Ju Chen, Jun Feng, and Shenyu Zhang for making the paper and its
method description available. The equations, dataset table, baselines, and
reported values gave this audit a concrete basis for reconstruction. Thank you
also to the authors of the pinned FGBCC and BWA reference repositories and the
public truth-inference data releases that make the comparison checks possible.

All publication commits in this repository are attributed to
MachineLearning-Nerd, with the paper authors credited for the research being
reproduced.
