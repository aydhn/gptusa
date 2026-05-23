from typing import Any, Dict, List, Optional
import json

from usa_signal_bot.core.enums import AdmissionReviewRiskFlag
from .admission_review_models import LedgerReconciliationReport

def admission_no_write_continuity_flags(payload: Dict[str, Any]) -> List[AdmissionReviewRiskFlag]:
    flags = []
    if not payload.get("activation_denied", False):
        flags.append(AdmissionReviewRiskFlag.ACTIVE_PAPER_ENABLE_RISK)
    if payload.get("activation_allowed", True):
        flags.append(AdmissionReviewRiskFlag.ACTIVATION_ALLOWED_RISK)
    if not payload.get("all_writes_blocked", False):
        flags.append(AdmissionReviewRiskFlag.PRODUCTION_CONFIG_WRITE_RISK)
    if payload.get("mutation_detected", True):
        flags.append(AdmissionReviewRiskFlag.PAPER_STATE_MUTATION_RISK)
    if payload.get("allows_active_paper", True):
        flags.append(AdmissionReviewRiskFlag.ACTIVE_PAPER_ENABLE_RISK)
    if payload.get("allows_broker_execution", True):
        flags.append(AdmissionReviewRiskFlag.BROKER_ORDER_RISK)
    if payload.get("allows_paper_state_mutation", True):
        flags.append(AdmissionReviewRiskFlag.PAPER_STATE_MUTATION_RISK)
    if payload.get("allows_config_patch", True):
        flags.append(AdmissionReviewRiskFlag.PRODUCTION_CONFIG_WRITE_RISK)
    if payload.get("allows_telegram_real_send", True):
        flags.append(AdmissionReviewRiskFlag.TELEGRAM_REAL_SEND_RISK)
    return flags

def validate_admission_no_write_continuity(dry_admission_payload: Optional[Dict[str, Any]] = None, reconciliation: Optional[LedgerReconciliationReport] = None) -> List[str]:
    errors = []
    if not dry_admission_payload:
        return ["Payload missing"]

    flags = admission_no_write_continuity_flags(dry_admission_payload)
    for flag in flags:
        errors.append(f"Continuity violation: {flag.value}")

    if reconciliation and not reconciliation.acknowledged_not_activation:
        errors.append("Continuity violation: Ledger does not acknowledge 'not activation'")

    return errors

def admission_no_write_continuity_is_preserved(payload: Dict[str, Any]) -> bool:
    return len(admission_no_write_continuity_flags(payload)) == 0

def admission_no_write_continuity_summary(payload: Dict[str, Any]) -> Dict[str, Any]:
    flags = admission_no_write_continuity_flags(payload)
    return {
        "preserved": len(flags) == 0,
        "violations": [f.value for f in flags]
    }

def admission_no_write_continuity_to_text(payload: Dict[str, Any]) -> str:
    return json.dumps(admission_no_write_continuity_summary(payload), indent=2)
