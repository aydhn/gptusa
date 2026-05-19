import json
from pathlib import Path
from typing import Any, Dict, List

def read_bundle_manifest(path: Path) -> Dict[str, Any]:
    if not path.exists():
        return {}
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def read_bundle_json(path: Path) -> Dict[str, Any]:
    if not path.exists():
        return {}
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def read_bundle_validation(path: Path) -> Dict[str, Any]:
    if not path.exists():
        return {}
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def read_bundle_artifacts(path: Path) -> List[Dict[str, Any]]:
    if not path.exists():
        return []
    artifacts = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                artifacts.append(json.loads(line))
    return artifacts

def read_versioned_candidate_bundle(bundle_path: Path) -> Dict[str, Any]:
    if bundle_path.is_dir():
        bundle_path = bundle_path / "bundle.json"
    return read_bundle_json(bundle_path)

def bundle_reader_summary(bundle_path: Path) -> Dict[str, Any]:
    if bundle_path.is_dir():
        bundle_path = bundle_path / "bundle.json"
    if not bundle_path.exists():
        return {"error": "not found"}
    return {"path": str(bundle_path)}

def bundle_reader_to_text(payload: Dict[str, Any]) -> str:
    return f"Reader: {payload}"
