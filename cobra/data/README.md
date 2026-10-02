# Phase 2 data pipelines

Common contract:
- image: float32 [H,W], scaled to [0,1]
- masks: uint8 [R,H,W], one mask per rater; empty masks preserved
- meta: patient_id, sample_id, n_raters, n_marked, source_site, spacing_mm

No annotation fusion occurs in data adapters.

LIDC uses pylidc Scan/Annotation APIs only. No custom XML parser and no filename/folder matching. The adapter uses cluster_annotations(), to_volume(), Annotation.bbox()/boolean_mask(), and DICOM metadata for Manufacturer.

## Verification status

Phase 2 is **IN PROGRESS**. The LIDC adapter is code-complete enough for a genuine-data verification pass, but no scientific export is accepted until it is executed against the genuine LIDC DICOM/XML collection and its cross-check/tests pass.

RIGA and QUBIQ are intentionally **BLOCKED**, not stubbed: their genuine source trees are not present in this repository. Source-specific file assumptions will not be invented. RIGA's original release uses six ophthalmologist annotations drawn onto image copies; QUBIQ's official documentation describes 2D NIfTI slices with individual expert segmentations. The actual downloaded trees must be inspected before implementing those readers.

No result, sample count, split count, or overlay is being reported as a scientific result from this phase yet.
