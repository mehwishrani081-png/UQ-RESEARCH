# CoBra Lab Notes

## 2026-10-07 — Phase 1 completed

Project: CoBra / UQ Research.

Phase 1 (Novelty/Baseline Extraction) was completed from accessible primary/full-text sources for the nine references specified in the proposal.

Deliverable:
- `docs/reading_table.md`

Key novelty conclusion:
ValUES already provides systematic empirical validation of segmentation uncertainty, including ambiguity, distribution shift, score aggregation and a four-rater LIDC-IDRI setup. Christensen et al. (2026) further study LIDC with four annotations per image and analyze uncertainty entanglement and disagreement structure. Therefore, a contribution framed only as a faithfulness/uncertainty audit against expert disagreement on LIDC would not be sufficiently differentiated. The defensible direction is to move from empirical audit/association toward finite-sample prediction/risk guarantees for spatial segmentation while explicitly retaining multiple expert annotations.

Phase-1 gate:
- [x] All 9 specified papers reviewed from accessible primary/full-text sources
- [x] Exact requested table columns populated
- [x] Accessible-source limitations documented
- [x] Novelty/saturation paragraph documented
- [x] No scientific results or fabricated numerical results generated

Important implementation constraint:
Do not begin Phase 2 until the Phase-2 data requirements and existing repository implementation have been audited. No method is to be implemented merely from the novelty table; exact mathematical definitions must be verified from the source paper when implementation begins.
