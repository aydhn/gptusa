from typing import Any, Dict, List
import json
from usa_signal_bot.core.enums import (
    PaperModeAdmissionReviewDecision,
    PaperModeAdmissionReviewStatus,
    AdmissionReviewRiskFlag
)
from .dry_admission_ingestion import (
    extract_dry_admission_run,
    extract_write_lock_refresh,
    extract_human_approval_ledger
)

def evaluate_admission_review_eligibility(dry_admission_payload: Dict[str, Any]) -> PaperModeAdmissionReviewDecision:
    flags = admission_review_safety_flags_from_dry_admission(dry_admission_payload)

    if PaperModeAdmissionReviewDecision.BLOCK in flags or AdmissionReviewRiskFlag.ACTIVATION_ALLOWED_RISK in flags:
        return PaperModeAdmissionReviewDecision.BLOCK

    run = extract_dry_admission_run(dry_admission_payload)
    if not run or run.get("status") in ["FAILED", "STALE"]:
        return PaperModeAdmissionReviewDecision.REQUEST_DRY_ADMISSION_REFRESH

    ledger = extract_human_approval_ledger(dry_admission_payload)
    if not ledger or ledger.get("missing_scopes"):
        return PaperModeAdmissionReviewDecision.REQUEST_LEDGER_RECONCILIATION

    write_lock = extract_write_lock_refresh(dry_admission_payload)
    if not write_lock or write_lock.get("status") == "FAILED":
        return PaperModeAdmissionReviewDecision.REQUEST_WRITE_LOCK_REFRESH

    if "manual_review_required" in dry_admission_payload and dry_admission_payload.get("manual_review_required"):
        if not ledger or not ledger.get("manual_review_completed"):
             return PaperModeAdmissionReviewDecision.REQUEST_MANUAL_REVIEW

    if "reject" in dry_admission_payload and dry_admission_payload.get("reject"):
        return PaperModeAdmissionReviewDecision.REJECT

    if len(flags) > 0 and AdmissionReviewRiskFlag.UNKNOWN in flags:
        return PaperModeAdmissionReviewDecision.INCONCLUSIVE

    return PaperModeAdmissionReviewDecision.PASS_TO_NO_WRITE_TRANSITION_CHECKPOINT

def admission_review_eligibility_reasons(dry_admission_payload: Dict[str, Any]) -> List[str]:
    reasons = []
    flags = admission_review_safety_flags_from_dry_admission(dry_admission_payload)
    if AdmissionReviewRiskFlag.ACTIVATION_ALLOWED_RISK in flags:
        reasons.append("activation_allowed is true")
    run = extract_dry_admission_run(dry_admission_payload)
    if not run:
        reasons.append("Missing dry_admission_run")
    ledger = extract_human_approval_ledger(dry_admission_payload)
    if not ledger:
        reasons.append("Missing human_approval_ledger")
    write_lock = extract_write_lock_refresh(dry_admission_payload)
    if not write_lock:
        reasons.append("Missing write_lock_refresh")
    return reasons

def admission_review_safety_flags_from_dry_admission(payload: Dict[str, Any]) -> List[AdmissionReviewRiskFlag]:
    flags = []
    if payload.get("activation_allowed"):
        flags.append(AdmissionReviewRiskFlag.ACTIVATION_ALLOWED_RISK)
    if not payload.get("all_writes_blocked", True):
         flags.append(AdmissionReviewRiskFlag.PRODUCTION_CONFIG_WRITE_RISK)
    if payload.get("mutation_detected"):
         flags.append(AdmissionReviewRiskFlag.PAPER_STATE_MUTATION_RISK)
    return flags

def admission_review_status_from_decision(decision: PaperModeAdmissionReviewDecision) -> PaperModeAdmissionReviewStatus:
    mapping = {
        PaperModeAdmissionReviewDecision.PASS_TO_NO_WRITE_TRANSITION_CHECKPOINT: PaperModeAdmissionReviewStatus.READY,
        PaperModeAdmissionReviewDecision.REQUEST_DRY_ADMISSION_REFRESH: PaperModeAdmissionReviewStatus.REQUEST_CHANGES,
        PaperModeAdmissionReviewDecision.REQUEST_LEDGER_RECONCILIATION: PaperModeAdmissionReviewStatus.REQUEST_CHANGES,
        PaperModeAdmissionReviewDecision.REQUEST_WRITE_LOCK_REFRESH: PaperModeAdmissionReviewStatus.REQUEST_CHANGES,
        PaperModeAdmissionReviewDecision.REQUEST_MANUAL_REVIEW: PaperModeAdmissionReviewStatus.REQUEST_CHANGES,
        PaperModeAdmissionReviewDecision.REJECT: PaperModeAdmissionReviewStatus.REJECTED,
        PaperModeAdmissionReviewDecision.BLOCK: PaperModeAdmissionReviewStatus.BLOCKED,
        PaperModeAdmissionReviewDecision.INCONCLUSIVE: PaperModeAdmissionReviewStatus.UNKNOWN,
        PaperModeAdmissionReviewDecision.UNKNOWN: PaperModeAdmissionReviewStatus.UNKNOWN
    }
    return mapping.get(decision, PaperModeAdmissionReviewStatus.UNKNOWN)

def eligibility_checker_to_text(payload: Dict[str, Any]) -> str:
    return json.dumps(payload, indent=2)
