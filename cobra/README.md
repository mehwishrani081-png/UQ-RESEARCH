# CoBra

Phase-0 repository skeleton for the revised CoBra project.

## Ground rules

1. One repository across local development, Kaggle, and university GPU; only YAML configuration changes between environments.
2. Every reported paper number must be produced by a re-runnable script.
3. Expert masks remain separate (R,H,W); fusion is outside the loader.
4. Patient-level splitting is mandatory everywhere.
5. Existing correct implementations are reused after inspection; no disconnected duplicates.
6. LIDC-IDRI ingestion must use pylidc, not a custom raw XML parser or filename/folder matching.
7. Surprises/failures are documented plainly; no silent fallback or fabricated output.
8. Algorithmic logic receives unit tests before scientific trust.
9. No synthetic/fabricated scientific results. Controlled fixtures may exist only in tests/ and must be clearly labeled.
10. Phases are sequential and fail-closed.
11. No placeholder scientific methods.

## Phase 0 status

- Repository layout: created.
- Exact dependency baseline: declared in requirements.txt.
- Reproducibility helper: reproducibility.py.
- Smoke test: tests/test_smoke.py.
- Initial notes: NOTES.md.
- Scientific/model/data-processing logic: intentionally not implemented in Phase 0.

## Reproduction command

```bash
pytest -q
```

Phase 0 does not claim scientific execution or model results.

## Reuse audit

See REUSE_AUDIT.md for the inspected prior implementation and the explicit reuse/new decisions.

## Environment

The exact Python pin is in environment.yml; package pins are also mirrored in requirements.txt. The current inspection runtime is intentionally not treated as the target scientific environment.
