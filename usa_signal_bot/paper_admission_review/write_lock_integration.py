from typing import Any, Dict, List
import json
from usa_signal_bot.core.enums import AdmissionReviewRiskFlag
from .dry_admission_ingestion import extract_write_lock_refresh

def extract_write_lock_refresh_summary(dry_admission_payload: Dict[str, Any]) -> Dict[str, Any]:
    refresh = extract_write_lock_refresh(dry_admission_payload)
    if not refresh:
        return {"status": "MISSING"}
    return {
        "status": refresh.get("status", "UNKNOWN"),
        "all_writes_blocked": refresh.get("all_writes_blocked", False),
        "mutation_detected": refresh.get("mutation_detected", True),
        "unblocked_write_attempt_count": refresh.get("unblocked_write_attempt_count", 1),
        "hash_unchanged": refresh.get("hash_unchanged", False)
    }

def validate_write_lock_refresh_for_admission_review(dry_admission_payload: Dict[str, Any]) -> List[str]:
    errors = []
    refresh = extract_write_lock_refresh(dry_admission_payload)
    if not refresh:
        return ["Write lock refresh missing"]

    if not refresh.get("all_writes_blocked", False):
        errors.append("all_writes_blocked is false in write lock refresh")
    if refresh.get("mutation_detected", True):
        errors.append("mutation_detected is true in write lock refresh")
    if refresh.get("unblocked_write_attempt_count", 1) > 0:
        errors.append("unblocked_write_attempt_count > 0 in write lock refresh")
    if not refresh.get("hash_unchanged", False):
        errors.append("hash_unchanged is false in write lock refresh")
    for allow_key in ["allows_active_paper", "allows_broker_execution", "allows_paper_state_mutation", "allows_config_patch", "allows_telegram_real_send"]:
         if refresh.get(allow_key, True):
             errors.append(f"{allow_key} is true in write lock refresh")

    return errors

def write_lock_refresh_is_valid_for_admission(dry_admission_payload: Dict[str, Any]) -> bool:
    return len(validate_write_lock_refresh_for_admission_review(dry_admission_payload)) == 0

def write_lock_integration_risk_flags(dry_admission_payload: Dict[str, Any]) -> List[AdmissionReviewRiskFlag]:
    flags = []
    errors = validate_write_lock_refresh_for_admission_review(dry_admission_payload)
    if errors:
        flags.append(AdmissionReviewRiskFlag.WRITE_LOCK_REFRESH_FAILED)
    return flags

def write_lock_integration_to_text(payload: Dict[str, Any]) -> str:
    return json.dumps(extract_write_lock_refresh_summary(payload), indent=2)
