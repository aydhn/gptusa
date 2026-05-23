from typing import Any, Dict, List
import json

def required_admission_evidence_types() -> List[str]:
    return [
        "dry_admission_full_review",
        "dry_admission_run",
        "no_write_contract",
        "write_lock_refresh",
        "human_approval_ledger",
        "activation_replay_result",
        "no_write_continuity_report",
        "runtime_write_lock_assertion",
        "validation_reports",
        "audit_trails"
    ]

def collect_admission_evidence_refs(dry_admission_payload: Dict[str, Any]) -> List[str]:
    refs = dry_admission_payload.get("evidence_refs", [])
    if isinstance(refs, list):
        return refs
    return []

def missing_admission_evidence_types(dry_admission_payload: Dict[str, Any]) -> List[str]:
    evidence = dry_admission_payload.get("evidence", {})
    if not isinstance(evidence, dict):
        return required_admission_evidence_types()

    return [t for t in required_admission_evidence_types() if t not in evidence]

def stale_admission_evidence_types(dry_admission_payload: Dict[str, Any]) -> List[str]:
    # Placeholder heuristic for staleness
    stale = []
    evidence = dry_admission_payload.get("evidence", {})
    if isinstance(evidence, dict):
        for k, v in evidence.items():
            if isinstance(v, dict) and v.get("status") in ["STALE", "EXPIRED"]:
                stale.append(k)
    return stale

def evaluate_admission_evidence_completeness(dry_admission_payload: Dict[str, Any]) -> Dict[str, Any]:
    missing = missing_admission_evidence_types(dry_admission_payload)
    stale = stale_admission_evidence_types(dry_admission_payload)
    return {
        "complete": len(missing) == 0 and len(stale) == 0,
        "missing_types": missing,
        "stale_types": stale,
        "refs_count": len(collect_admission_evidence_refs(dry_admission_payload))
    }

def dry_admission_evidence_to_text(payload: Dict[str, Any]) -> str:
    return json.dumps(evaluate_admission_evidence_completeness(payload), indent=2)
