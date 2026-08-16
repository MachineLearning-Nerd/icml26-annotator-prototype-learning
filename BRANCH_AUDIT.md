# Branch and experiment audit

The original branch names were generated experiment labels. The final names
describe the evidence role while preserving the linear history. The commit
identifiers below are the pre-normalization identifiers from the original
remote; history normalization changes their hashes while preserving their
tree content and ancestry.

| Original branch | Final branch | Historical role | Pre-normalization tip |
|---|---|---|---|
| main | main | Cumulative publication surface | 6c21d5eea44d0cd4bc781f5c2a7ffef828646747 |
| orx/validated-six-dataset-ptbcc-baseline | baseline/validated-six-datasets | Pin the first runnable environment and public-data baseline | 06c98ae5413fea1271f2fd4d3881a6a9758cb5b7 |
| orx/runnable-frozen-ptbcc-baseline | baseline/frozen-runtime | Repair baseline bootstrap and freeze the runnable path | 6c3a1b4e5cc5aa2b0d6992964d04044b78201d6c |
| orx/official-11-dataset-corpus-and-reference-baselin | audit/exact-11-dataset-corpus | Recover the exact Table 3 corpus and reference baselines | 602e1ce62868ac11d9ce566795b4237255829fed |
| orx/exact-ds-full-fgbcc-and-logged-ablation | audit/exact-baselines-ablation | Add exact DS/FGBCC evidence and the seeded ablation | 7d32700c46660155447baa921d235b6f53d968b3 |
| orx/legacy-exact-fgbcc-numerical-semantics | audit/legacy-fgbcc-semantics | Match legacy FGBCC exponentiation semantics | 4efc1592cf044c5aeb8d0df096b3139994b3e282 |
| orx/process-isolated-cpu-runtime-benchmark | benchmark/cpu-runtime | Add clean-process timing and bootstrap intervals | c0fa15c12bb1e16592d2993e5921cd79196c1f28 |
| orx/cumulative-claim-verifier-and-evidence-bundle | audit/claim-verifier | Add independent claim contracts, evidence, and negative controls | dc8d5eba7a9cf92fe64a0e75473df740146a191f |
| orx/release-candidate-report-and-additive-logbook | main | Same tip and tree as main; collapsed to avoid a duplicate publication branch | 6c21d5eea44d0cd4bc781f5c2a7ffef828646747 |

## Final public inventory

The intended final public branches are exactly:

~~~text
main
baseline/validated-six-datasets
baseline/frozen-runtime
audit/exact-11-dataset-corpus
audit/exact-baselines-ablation
audit/legacy-fgbcc-semantics
benchmark/cpu-runtime
audit/claim-verifier
~~~

No orx/*, master, or duplicate release-candidate ref belongs in the final
inventory. main contains the cumulative publication surface; the other
branches are historical checkpoints and are not claims of separate papers.
