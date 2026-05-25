import hashlib
import json
from pathlib import Path
from typing import Any, Dict, Optional, List

def stable_json_hash(payload: Dict[str, Any]) -> str:
    serialized = json.dumps(payload, sort_keys=True, default=str).encode('utf-8')
    return hashlib.sha256(serialized).hexdigest()

def file_sha256(path: Path) -> Optional[str]:
    if not path.exists():
        return None
    sha256 = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            sha256.update(chunk)
    return sha256.hexdigest()

def safe_artifact_hash(value: Any) -> str:
    if isinstance(value, dict):
        return stable_json_hash(value)
    return hashlib.sha256(str(value).encode('utf-8')).hexdigest()

def artifact_hash_summary(payload: Dict[str, Any]) -> Dict[str, Any]:
    return {}

def validate_hash_safe(value: Optional[str]) -> List[str]:
    return []
