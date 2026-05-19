import json
from pathlib import Path
from typing import Any, Dict, List

def sandbox_output_root(data_root: Path) -> Path:
    return data_root / "release_sandbox" / "outputs"

def sandbox_output_dir(data_root: Path, sandbox_id: str) -> Path:
    return sandbox_output_root(data_root) / sandbox_id

def validate_sandbox_output_path(path: Path, data_root: Path) -> List[str]:
    root = sandbox_output_root(data_root).resolve()
    if not path.resolve().is_relative_to(root):
        return ["Path traversal detected or path outside output root."]
    return []

def write_sandbox_output_json(path: Path, payload: Dict[str, Any]) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload))
    return path

def write_sandbox_output_text(path: Path, text: str) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text)
    return path

def output_isolation_summary(output_path: Path) -> Dict[str, Any]:
    return {"path": str(output_path)}
