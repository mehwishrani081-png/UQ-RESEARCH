"""Phase-0 reproducibility helper: seeds and run metadata only."""
from __future__ import annotations

import importlib.metadata
import json
import os
import platform
import random
import shutil
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

def set_global_seed(seed: int, deterministic: bool = True) -> dict[str, Any]:
    if isinstance(seed, bool) or not isinstance(seed, int):
        raise TypeError("seed must be an integer")
    random.seed(seed)
    os.environ["PYTHONHASHSEED"] = str(seed)
    info = {"seed": seed, "python": True, "numpy": False, "torch": False}
    try:
        import numpy as np
        np.random.seed(seed)
        info["numpy"] = True
    except ImportError:
        pass
    try:
        import torch
        torch.manual_seed(seed)
        if torch.cuda.is_available():
            torch.cuda.manual_seed_all(seed)
        if deterministic:
            torch.use_deterministic_algorithms(True, warn_only=True)
            if hasattr(torch.backends, "cudnn"):
                torch.backends.cudnn.deterministic = True
                torch.backends.cudnn.benchmark = False
        info["torch"] = True
    except ImportError:
        pass
    return info

def git_commit(project_root: str | Path) -> str:
    try:
        p = subprocess.run(
            ["git", "rev-parse", "HEAD"], cwd=Path(project_root),
            check=True, capture_output=True, text=True, timeout=5
        )
        return p.stdout.strip() or "NOT_AVAILABLE"
    except (FileNotFoundError, subprocess.CalledProcessError, subprocess.TimeoutExpired):
        return "NOT_AVAILABLE"

def package_versions() -> dict[str, str]:
    names = ["torch", "numpy", "scipy", "pandas", "scikit-image",
             "pydicom", "pylidc", "matplotlib", "PyYAML", "pytest", "Pillow"]
    out = {"python": platform.python_version()}
    for name in names:
        try:
            out[name] = importlib.metadata.version(name)
        except importlib.metadata.PackageNotFoundError:
            out[name] = "NOT_INSTALLED"
    return out

def save_run_metadata(
    output_dir: str | Path,
    config: dict[str, Any],
    project_root: str | Path,
    config_path: str | Path | None = None,
) -> Path:
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)
    seed = int(config["reproducibility"]["seed"])
    deterministic = bool(config["reproducibility"]["deterministic"])
    seed_info = set_global_seed(seed, deterministic)
    metadata = {
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "seed_info": seed_info,
        "git_commit": git_commit(project_root),
        "package_versions": package_versions(),
        "config": config,
    }
    path = out / "run_metadata.json"
    path.write_text(json.dumps(metadata, indent=2, sort_keys=True), encoding="utf-8")
    if bool(config.get("reproducibility", {}).get("save_config_copy", True)):
        if config_path is not None and Path(config_path).is_file():
            shutil.copy2(config_path, out / "config_used.yaml")
        else:
            import yaml
            (out / "config_used.yaml").write_text(
                yaml.safe_dump(config, sort_keys=False), encoding="utf-8"
            )
    return path
