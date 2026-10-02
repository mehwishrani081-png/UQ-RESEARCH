"""Patient-level split utilities. Never split at slice/sample level."""
from __future__ import annotations
from pathlib import Path
import numpy as np

class SplitError(RuntimeError):
    pass

def patient_split(patient_ids, *, seed: int, train_fraction=.50,
                   validation_fraction=.10, pool_fraction=.40):
    if not np.isclose(train_fraction + validation_fraction + pool_fraction, 1.0):
        raise SplitError("train/validation/pool fractions must sum to 1")
    ids = sorted({str(x) for x in patient_ids})
    if len(ids) < 3:
        raise SplitError("At least three patients are required")
    rng = np.random.default_rng(int(seed))
    ids = list(np.asarray(ids, dtype=object)[rng.permutation(len(ids))])
    n = len(ids)
    n_train = int(np.floor(n * train_fraction))
    n_val = int(np.floor(n * validation_fraction))
    if n_train < 1 or n_val < 1 or n_train + n_val >= n:
        raise SplitError("Fractions produce an invalid patient split")
    return {
        "TRAIN": tuple(sorted(ids[:n_train])),
        "VALIDATION": tuple(sorted(ids[n_train:n_train+n_val])),
        "POOL": tuple(sorted(ids[n_train+n_val:])),
    }

def assert_disjoint(split_map):
    sets = [set(v) for v in split_map.values()]
    if any(a & b for i,a in enumerate(sets) for b in sets[i+1:]):
        raise SplitError("Patient leakage detected")

def save_split_lists(split_map, output_dir):
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)
    assert_disjoint(split_map)
    for name, ids in split_map.items():
        (out / f"{name.lower()}_patients.txt").write_text("\n".join(ids) + "\n", encoding="utf-8")
