# Phase 2 LIDC acquisition

The supplied .tcia file is a TCIA Data Retriever manifest, not the DICOM
payload. The XML-only archive is an annotation input. Both stay outside GitHub.

Validate the manifest/XML relationship before downloading or preprocessing:

    python cobra/scripts/validate_lidc_manifest.py --manifest /data/input/TCIA_LIDC-IDRI_20200921.tcia --xml-zip /data/input/LIDC-XML-only.zip

A non-empty SeriesInstanceUID intersection is required.

For Linux acquisition, install the official TCIA/NBIA Data Retriever CLI and
use its CLI with the .tcia manifest and an external output directory.

After the genuine DICOM collection is present, configure pylidc and run the
Phase-2 LIDC cross-check. Only after that gate passes should full processing
be accepted as a scientific run.

Medical data is intentionally not committed to GitHub.
