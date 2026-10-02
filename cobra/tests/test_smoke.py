"""Controlled software smoke test; not a scientific result."""
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

def test_imports_work():
    import reproducibility
    assert callable(reproducibility.set_global_seed)
    assert callable(reproducibility.save_run_metadata)
