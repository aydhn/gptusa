import hashlib
import json
from typing import Any, Dict, List

def redact_paper_baseline_sensitive_fields(snapshot: Dict[str, Any]) -> Dict[str, Any]:
    redacted = snapshot.copy()
    keys_to_redact = ["api_key", "secret", "token", "password", "broker_order_id", "live_order_id"]
    for key in keys_to_redact:
        if key in redacted:
            redacted[key] = "[REDACTED]"
    return redacted

def load_read_only_paper_baseline_for_pre_rehearsal(paper_payload: Dict[str, Any] | None = None) -> Dict[str, Any]:
    baseline = {}
    if paper_payload:
        baseline = redact_paper_baseline_sensitive_fields(paper_payload.copy())

    baseline["paper_state_committed"] = False
    baseline["paper_order_executed"] = False
    baseline["portfolio_state_mutated"] = False
    return baseline

def paper_baseline_hash(snapshot: Dict[str, Any]) -> str:
    snapshot_str = json.dumps(snapshot, sort_keys=True)
    return hashlib.sha256(snapshot_str.encode("utf-8")).hexdigest()

def validate_paper_baseline_read_only(snapshot: Dict[str, Any]) -> List[str]:
    violations = []
    if snapshot.get("paper_state_committed", False):
        violations.append("paper_state_committed is True, must be False")
    if snapshot.get("paper_order_executed", False):
        violations.append("paper_order_executed is True, must be False")
    if snapshot.get("portfolio_state_mutated", False):
        violations.append("portfolio_state_mutated is True, must be False")
    return violations

def paper_baseline_summary(snapshot: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "hash": paper_baseline_hash(snapshot),
        "read_only": len(validate_paper_baseline_read_only(snapshot)) == 0
    }

def paper_baseline_to_text(snapshot: Dict[str, Any]) -> str:
    s = paper_baseline_summary(snapshot)
    return f"Paper Baseline: Hash={s['hash']}, Read-Only={s['read_only']}"
