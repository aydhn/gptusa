import json
from pathlib import Path
from typing import Any, Dict, List
from usa_signal_bot.core.exceptions import SandboxOutputIsolationError

def sandbox_output_root(data_root: Path) -> Path:
    root = data_root / "release_sandbox" / "outputs"
    root.mkdir(parents=True, exist_ok=True)
    return root

def sandbox_output_dir(data_root: Path, sandbox_id: str) -> Path:
    out_dir = sandbox_output_root(data_root) / sandbox_id
    out_dir.mkdir(parents=True, exist_ok=True)
    return out_dir

def validate_sandbox_output_path(path: Path, data_root: Path) -> List[str]:
    warnings = []
    try:
        resolved_path = path.resolve()
        resolved_root = sandbox_output_root(data_root).resolve()
        # Verify path traversal (path must be under root)
        if resolved_root not in resolved_path.parents and resolved_path != resolved_root:
            warnings.append(f"Path traversal detected: {path} is not under {resolved_root}")
    except Exception as e:
        warnings.append(f"Failed to resolve paths: {e}")
    return warnings

def write_sandbox_output_json(path: Path, payload: Dict[str, Any]) -> Path:
    if "release_sandbox/outputs" not in str(path):
        raise SandboxOutputIsolationError(f"Refusing to write JSON to unsafe path: {path}")
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(payload, f, indent=2)
    return path

def write_sandbox_output_text(path: Path, text: str) -> Path:
    if "release_sandbox/outputs" not in str(path):
        raise SandboxOutputIsolationError(f"Refusing to write text to unsafe path: {path}")
    with open(path, 'w', encoding='utf-8') as f:
        f.write(text)
    return path

def output_isolation_summary(output_path: Path) -> Dict[str, Any]:
    return {
        "path": str(output_path),
        "is_safe": "release_sandbox/outputs" in str(output_path)
    }
