import json
from pathlib import Path
from typing import Any, Dict, List

def load_bundle_for_sandbox(bundle_path: Path) -> Dict[str, Any]:
    if not bundle_path.exists():
        return {}
    return {"id": "mock_bundle", "version": "1.0.0"}

def load_bundle_manifest_for_sandbox(bundle_path: Path) -> Dict[str, Any]:
    return {"manifest": "mock"}

def load_bundle_artifacts_for_sandbox(bundle_path: Path) -> List[Dict[str, Any]]:
    return [{"type": "config", "content": "mock"}]

def load_bundle_validation_for_sandbox(bundle_path: Path) -> Dict[str, Any]:
    return {"status": "PASS"}

def bundle_loader_summary(bundle_payload: Dict[str, Any]) -> Dict[str, Any]:
    return {"loaded": True, "keys": list(bundle_payload.keys())}

def bundle_loader_to_text(payload: Dict[str, Any]) -> str:
    return "Bundle Loader: Loaded mock bundle for preview."
