from typing import Any, Dict, Optional, List
import copy
import hashlib
import json

def load_observer_read_only_paper_snapshot(paper_payload: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    if not paper_payload:
        return {"_metadata": {"status": "empty_snapshot"}}
    return copy.deepcopy(paper_payload)

def redact_observer_snapshot_sensitive_fields(snapshot: Dict[str, Any]) -> Dict[str, Any]:
    redacted = copy.deepcopy(snapshot)
    if "secrets" in redacted:
        redacted["secrets"] = "***REDACTED***"
    if "api_keys" in redacted:
        redacted["api_keys"] = "***REDACTED***"
    if "tokens" in redacted:
        redacted["tokens"] = "***REDACTED***"
    return redacted

def observer_snapshot_hash(snapshot: Dict[str, Any]) -> str:
    serialized = json.dumps(snapshot, sort_keys=True, default=str)
    return hashlib.sha256(serialized.encode('utf-8')).hexdigest()

def validate_observer_snapshot_read_only(snapshot: Dict[str, Any]) -> List[str]:
    errors = []
    if snapshot.get("paper_state_committed"):
        errors.append("Snapshot has paper_state_committed=True")
    if snapshot.get("paper_order_executed"):
        errors.append("Snapshot has paper_order_executed=True")
    if snapshot.get("portfolio_state_mutated"):
        errors.append("Snapshot has portfolio_state_mutated=True")
    return errors

def observer_snapshot_summary(snapshot: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "keys": list(snapshot.keys()),
        "hash": observer_snapshot_hash(snapshot)
    }

def observer_snapshot_to_text(snapshot: Dict[str, Any]) -> str:
    return f"ReadOnlyPaperSnapshot hash: {observer_snapshot_hash(snapshot)}"
