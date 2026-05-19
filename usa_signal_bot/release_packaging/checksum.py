import hashlib
import json
from pathlib import Path
from typing import Any, Dict, List, Optional

def stable_payload_json(payload: Dict[str, Any]) -> str:
    return json.dumps(payload, sort_keys=True, separators=(',', ':'))

def stable_payload_hash(payload: Dict[str, Any]) -> str:
    text = stable_payload_json(payload)
    return text_sha256(text)

def file_sha256(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            h.update(chunk)
    return h.hexdigest()

def text_sha256(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()

def verify_payload_hash(payload: Dict[str, Any], expected_hash: Optional[str]) -> bool:
    if not expected_hash:
        return False
    return stable_payload_hash(payload) == expected_hash

def verify_file_hash(path: Path, expected_hash: Optional[str]) -> bool:
    if not expected_hash:
        return False
    return file_sha256(path) == expected_hash

def checksum_summary(payloads: List[Dict[str, Any]]) -> Dict[str, Any]:
    hashes = [stable_payload_hash(p) for p in payloads]
    return {"count": len(payloads), "hashes": hashes}
