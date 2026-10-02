"""Common Phase-2 data contract. No scientific fusion occurs here."""
from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
from typing import Any
import json
import numpy as np

class DataContractError(RuntimeError):
    pass

@dataclass(frozen=True)
class SampleMeta:
    patient_id: str
    sample_id: str
    n_raters: int
    n_marked: int
    source_site: str
    spacing_mm: tuple[float, float]

@dataclass(frozen=True)
class CommonSample:
    image: np.ndarray
    masks: np.ndarray
    meta: SampleMeta

def validate_common_sample(sample: CommonSample) -> None:
    image, masks, meta = sample.image, sample.masks, sample.meta
    if image.dtype != np.float32 or image.ndim != 2:
        raise DataContractError("image must be float32 [H,W]")
    if masks.dtype != np.uint8 or masks.ndim != 3:
        raise DataContractError("masks must be uint8 [R,H,W]")
    if masks.shape[0] != meta.n_raters:
        raise DataContractError("mask/rater count mismatch")
    if not np.isin(masks, [0, 1]).all():
        raise DataContractError("masks must contain only 0/1")
    if not np.isfinite(image).all() or image.min() < 0 or image.max() > 1:
        raise DataContractError("image must be finite and scaled to [0,1]")
    marked = int(np.any(masks.astype(bool), axis=(1, 2)).sum())
    if marked != meta.n_marked:
        raise DataContractError("n_marked does not match mask content")

def save_sample(path: str | Path, sample: CommonSample) -> None:
    validate_common_sample(sample)
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    np.savez_compressed(path, image=sample.image, masks=sample.masks,
        meta_json=json.dumps({
            "patient_id": sample.meta.patient_id,
            "sample_id": sample.meta.sample_id,
            "n_raters": sample.meta.n_raters,
            "n_marked": sample.meta.n_marked,
            "source_site": sample.meta.source_site,
            "spacing_mm": list(sample.meta.spacing_mm),
        }))
