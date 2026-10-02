# Prior Repository Reuse Audit — Phase 0

Inspected source: supplied UQ_Project_COMPLETE_SOURCE_CODE.zip.

## Existing work identified

| Existing capability | Existing location | CoBra decision |
|---|---|---|
| Majority-vote U-Net | src/models/unet_majority.py, scripts/train_majority.py | REUSE CANDIDATE |
| Soft-label U-Net | src/models/unet_softlabel.py, scripts/train_softlabel.py | REUSE CANDIDATE |
| Rater-aware U-Net | src/models/rater_aware_unet.py, scripts/train_rateraware.py | REUSE CANDIDATE |
| Probabilistic U-Net | src/models/probabilistic_unet.py, scripts/train_probunet.py | REUSE CANDIDATE |
| MC Dropout | src/uq/mc_dropout.py, scripts/run_mc_dropout.py | REUSE CANDIDATE |
| Deep Ensemble | src/uq/deep_ensemble.py, scripts/run_ensemble.py | REUSE CANDIDATE |
| Probabilistic sampling | src/uq/probabilistic_sampling.py, scripts/run_probabilistic_sampling.py | REUSE CANDIDATE |
| Core–Shell / LTT | src/conformal/*, scripts/run_core_shell.py | REUSE CANDIDATE |
| Reproducibility utilities | src/utils/reproducibility.py | REUSE/ADAPT CANDIDATE |
| Extensive unit tests | tests/ | REUSE/ADAPT CANDIDATE |

## New Phase-0 work

- CoBra repository skeleton.
- Single phase-0 configuration pattern.
- Explicit reuse audit.
- New ground-rule documentation.
- Minimal reproducibility helper sufficient for Phase 0.
- Minimal smoke test.

## Do not silently reuse

The prior repository contains src/data/annotation_parser.py, which implements raw XML parsing. The new ground rules explicitly require pylidc for LIDC-IDRI and prohibit a custom raw XML parser for that path. Therefore this component is not accepted as the CoBra LIDC loader under the current rules.

The prior repository also has data/processed/ but the supplied archive contains no processed scientific artifacts there.

The prior repository documentation repeatedly states that genuine LIDC execution and scientific validation were not completed in the supplied runtime.

## Missing artifact discrepancy

The Phase-0 request refers to seven trained checkpoints in results/lidc_full_real/checkpoints/. The supplied ZIP was inspected and contains no checkpoint files under results/. This must be resolved before any training-dependent CoBra phase can consume those checkpoints.

## Phase-0 principle

No model/data-processing code is copied into CoBra yet. Reuse decisions are recorded first so later implementation can reuse verified components without creating disconnected duplicates.
