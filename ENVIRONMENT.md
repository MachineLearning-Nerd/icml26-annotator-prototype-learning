# Reproduction environment

## Fixed command

~~~bash
uv sync --frozen
uv run python repro/src/run_ptbcc.py --output-dir outputs/full
uv run python -m unittest -v repro.tests.test_ptbcc
~~~

The runner then invokes the independent claim verifier and the release-artifact
checks. Data are downloaded only from the URLs and hashes in
[repro/audit/public_data_manifest.json](repro/audit/public_data_manifest.json).

## Recorded cumulative run

The committed claim evidence was produced by the cumulative verifier run with:

| Input | Recorded value |
|---|---|
| Python | 3.12.11 |
| Python constraint | 3.12 from .python-version |
| Platform | macOS-26.5.2-arm64-arm-64bit |
| Processor | arm |
| Compute | local CPU only; no GPU or cloud job |
| pyproject.toml SHA-256 | 167cb8af474e19d484804a62d39f1bc172564e7be99b807889824e61566cd56e |
| uv.lock SHA-256 | efcd9120fe50fc91b3f6fa4f71ec8923f35527317db5a909560700655dbd37c6 |
| Synthetic seeds | 73000 through 73039 |
| Ablation seeds | 20260715, 20260716, 20260717 |
| Runtime repetitions | 5 clean processes per comparison |
| Bootstrap seed | 20260723 |

The evidence provenance is stored in each
.openresearch/artifacts/claim_N/run_provenance.json. Timing is not expected to
be portable across processors or Python implementations; the exact runtime
claim remains BLOCKED for that reason and because the paper omits its raw
timing denominator.

## Input storage

The public datasets are intentionally not committed to this repository. The
bootstrap code downloads them into the ignored external/ directory and checks
the manifest before use. The committed outputs and cumulative raw evidence
remain inspectable without redistributing the source datasets.
