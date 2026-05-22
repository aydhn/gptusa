from typing import Any, Dict, List
from usa_signal_bot.core.enums import FinalHandoffDecision, FinalHandoffReviewStatus, FinalHandoffRiskFlag
from usa_signal_bot.paper_final_handoff.readiness_rehearsal_ingestion import (
    readiness_rehearsal_supports_final_handoff,
    extract_final_review_lock,
    extract_guarded_handoff_entry
)
from usa_signal_bot.paper_final_handoff.handoff_registry_ingestion import validate_handoff_registry_entry_for_final_review

def evaluate_final_handoff_eligibility(readiness_payload: Dict[str, Any]) -> FinalHandoffDecision:
    supports, warnings = readiness_rehearsal_supports_final_handoff(readiness_payload)
    if "Rehearsal status is BLOCKED or REJECTED." in warnings:
        return FinalHandoffDecision.BLOCK

    lock = extract_final_review_lock(readiness_payload)
    if not lock:
        return FinalHandoffDecision.REQUEST_HANDOFF_REHEARSAL_RERUN

    registry = extract_guarded_handoff_entry(readiness_payload)
    if not registry:
        return FinalHandoffDecision.REQUEST_DOSSIER_REFRESH

    registry_errors = validate_handoff_registry_entry_for_final_review(registry)
    if registry_errors:
        return FinalHandoffDecision.BLOCK

    if not readiness_payload.get("manual_review_completed"):
        return FinalHandoffDecision.REQUEST_MANUAL_REVIEW

    if not readiness_payload.get("evidence_valid", True):
        return FinalHandoffDecision.REQUEST_EVIDENCE_REFRESH

    if supports:
        return FinalHandoffDecision.CREATE_SEALED_READINESS_ARCHIVE

    return FinalHandoffDecision.INCONCLUSIVE

def final_handoff_eligibility_reasons(readiness_payload: Dict[str, Any]) -> List[str]:
    reasons = []
    dec = evaluate_final_handoff_eligibility(readiness_payload)
    reasons.append(f"Decision: {dec.value}")
    return reasons

def final_handoff_safety_flags_from_readiness(payload: Dict[str, Any]) -> List[FinalHandoffRiskFlag]:
    flags = []
    if not extract_final_review_lock(payload):
        flags.append(FinalHandoffRiskFlag.FINAL_LOCK_INVALID)
    registry = extract_guarded_handoff_entry(payload)
    if not registry or validate_handoff_registry_entry_for_final_review(registry):
        flags.append(FinalHandoffRiskFlag.HANDOFF_REGISTRY_INVALID)
    if not payload.get("manual_review_completed"):
        flags.append(FinalHandoffRiskFlag.MANUAL_REVIEW_MISSING)
    if not payload.get("evidence_valid", True):
        flags.append(FinalHandoffRiskFlag.EVIDENCE_STALE)
    return flags

def final_handoff_status_from_decision(decision: FinalHandoffDecision) -> FinalHandoffReviewStatus:
    mapping = {
        FinalHandoffDecision.CREATE_SEALED_READINESS_ARCHIVE: FinalHandoffReviewStatus.COMPLETED,
        FinalHandoffDecision.REQUEST_HANDOFF_REHEARSAL_RERUN: FinalHandoffReviewStatus.REVIEWING,
        FinalHandoffDecision.REQUEST_DOSSIER_REFRESH: FinalHandoffReviewStatus.REVIEWING,
        FinalHandoffDecision.REQUEST_EVIDENCE_REFRESH: FinalHandoffReviewStatus.REVIEWING,
        FinalHandoffDecision.REQUEST_MANUAL_REVIEW: FinalHandoffReviewStatus.REVIEWING,
        FinalHandoffDecision.REJECT: FinalHandoffReviewStatus.REJECTED,
        FinalHandoffDecision.BLOCK: FinalHandoffReviewStatus.BLOCKED,
        FinalHandoffDecision.INCONCLUSIVE: FinalHandoffReviewStatus.REVIEWING,
        FinalHandoffDecision.UNKNOWN: FinalHandoffReviewStatus.UNKNOWN
    }
    return mapping.get(decision, FinalHandoffReviewStatus.UNKNOWN)

def eligibility_checker_to_text(payload: Dict[str, Any]) -> str:
    dec = evaluate_final_handoff_eligibility(payload)
    return f"Eligibility Check -> {dec.value}"
