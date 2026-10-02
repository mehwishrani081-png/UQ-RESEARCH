# CoBra Lab Notes

## 2026-10-03
Project started: CoBra, repo skeleton created.

### Phase-0 inspection note
The supplied UQ source repository was inspected before creating this skeleton. Existing implementations are intended for reuse where they satisfy the new ground rules; Phase 0 deliberately does not copy model or scientific data-processing logic into CoBra.

Important discrepancy found: the supplied ZIP does not contain the claimed results/lidc_full_real/checkpoints/ directory or seven trained checkpoint files, and its data/processed/ directory contains no processed scientific artifacts. This is documented rather than papered over.

Important compatibility issue found: the existing repository contains src/data/annotation_parser.py, a custom raw LIDC XML parser. This conflicts with the new ground rule requiring pylidc for LIDC-IDRI ingestion. The parser is therefore not treated as reusable for the CoBra LIDC ingestion path unless the rule is explicitly revised.
