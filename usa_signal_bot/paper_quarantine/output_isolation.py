import json
from pathlib import Path
from typing import Any

from usa_signal_bot.core.exceptions import QuarantineOutputIsolationError

def quarantine_output_root(data_root: Path) -> Path:
    return data_root / "paper_quarantine" / "outputs"

def quarantine_output_dir(data_root: Path, candidate_id: str) -> Path:
    return quarantine_output_root(data_root) / candidate_id

def validate_quarantine_output_path(path: Path, data_root: Path) -> list[str]:
    errors = []
    root = quarantine_output_root(data_root).resolve()
    target = path.resolve()

    if root not in target.parents and target != root:
        errors.append(f"Path traversal detected. Target {target} is not under quarantine root {root}")

    paper_store_path = (data_root / "paper").resolve()
    if paper_store_path in target.parents or target == paper_store_path:
        errors.append("Output path is inside paper store path.")

    config_path = (data_root.parent / "config").resolve()
    if config_path in target.parents or target == config_path:
         errors.append("Output path is inside production config path.")

    return errors

def write_quarantine_output_json(path: Path, payload: dict[str, Any], data_root: Path) -> Path:
    errors = validate_quarantine_output_path(path, data_root)
    if errors:
        raise QuarantineOutputIsolationError(f"Invalid output path: {errors}")

    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w") as f:
        json.dump(payload, f, indent=2)
    return path

def write_quarantine_output_text(path: Path, text: str, data_root: Path) -> Path:
    errors = validate_quarantine_output_path(path, data_root)
    if errors:
        raise QuarantineOutputIsolationError(f"Invalid output path: {errors}")

    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w") as f:
        f.write(text)
    return path

def quarantine_output_summary(output_path: Path) -> dict[str, Any]:
    return {
        "output_path": str(output_path),
        "exists": output_path.exists(),
        "is_file": output_path.is_file(),
    }
