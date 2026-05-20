import hashlib
import json
from typing import Any, List, Optional

def load_read_only_paper_snapshot(snapshot_payload: Optional[dict[str, Any]] = None) -> dict[str, Any]:
    if snapshot_payload is None:
        return {
            "snapshot_id": "mock_snapshot",
            "timestamp": "2023-01-01T00:00:00Z",
            "paper_state_committed": False,
            "portfolio": {},
            "orders": []
        }

    snapshot = snapshot_payload.copy()
    snapshot["paper_state_committed"] = False
    return snapshot

def redact_paper_snapshot_sensitive_fields(snapshot: dict[str, Any]) -> dict[str, Any]:
    redacted = snapshot.copy()
    sensitive_keys = ["api_key", "secret", "token", "password"]

    def _redact(d: dict):
        for k, v in d.items():
            if any(s in k.lower() for s in sensitive_keys):
                d[k] = "[REDACTED]"
            elif isinstance(v, dict):
                _redact(v)
            elif isinstance(v, list):
                for item in v:
                    if isinstance(item, dict):
                        _redact(item)

    _redact(redacted)
    return redacted

def paper_snapshot_hash(snapshot: dict[str, Any]) -> str:
    snapshot_str = json.dumps(snapshot, sort_keys=True)
    return hashlib.sha256(snapshot_str.encode("utf-8")).hexdigest()

def validate_paper_snapshot_read_only(snapshot: dict[str, Any]) -> List[str]:
    errors = []
    if snapshot.get("paper_state_committed", False):
        errors.append("Snapshot has paper_state_committed=True. Must be read-only.")
    if snapshot.get("paper_order_executed", False):
        errors.append("Snapshot has paper_order_executed=True. Must be read-only.")
    if snapshot.get("portfolio_state_mutated", False):
        errors.append("Snapshot has portfolio_state_mutated=True. Must be read-only.")
    return errors

def paper_snapshot_loader_summary(snapshot: dict[str, Any]) -> dict[str, Any]:
    return {
        "hash": paper_snapshot_hash(snapshot),
        "keys_count": len(snapshot.keys()),
        "read_only": not snapshot.get("paper_state_committed", False)
    }

def paper_snapshot_loader_to_text(payload: dict[str, Any]) -> str:
    summary = paper_snapshot_loader_summary(payload)
    return f"Paper Snapshot: Hash {summary['hash']}, Read-Only: {summary['read_only']}"
