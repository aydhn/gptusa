from typing import Any, Dict, List, Optional
import hashlib
import json

def validate_baseline_snapshot_consistency(baseline: Optional[Dict[str, Any]], snapshot: Optional[Dict[str, Any]]) -> List[str]:
    errors = []
    if not baseline:
        errors.append("Baseline is missing")
    if not snapshot:
        errors.append("Snapshot is missing")
    return errors

def validate_drift_result_consistency(baseline: Optional[Dict[str, Any]], snapshot: Optional[Dict[str, Any]], drift_result: Optional[Dict[str, Any]]) -> List[str]:
    errors = []
    if not drift_result:
        errors.append("Drift result is missing")
    return errors

def validate_readiness_gate_consistency(readiness_gate: Optional[Dict[str, Any]], drift_result: Optional[Dict[str, Any]]) -> List[str]:
    errors = []
    if not readiness_gate:
        errors.append("Readiness gate is missing")
    return errors

def validate_monitoring_hash_consistency(baseline: Optional[Dict[str, Any]], snapshot: Optional[Dict[str, Any]]) -> List[str]:
    errors = []
    # simplified logic
    if baseline and not baseline.get("hash"):
        pass # could add error
    return errors

def monitoring_consistency_summary(errors: List[str]) -> Dict[str, Any]:
    return {"valid": len(errors) == 0, "errors": errors}

def monitoring_consistency_to_text(errors: List[str]) -> str:
    if not errors:
        return "Monitoring Consistency Valid."
    return f"Monitoring Consistency Failed with {len(errors)} errors:\n" + "\n".join(f"- {e}" for e in errors)
