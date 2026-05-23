from typing import Any
from usa_signal_bot.core.enums import (
    NoWriteTransitionDecision,
    NoWriteTransitionDossierStatus,
    NoWriteTransitionRiskFlag
)
from usa_signal_bot.paper_no_write_transition.admission_ingestion import (
    admission_review_supports_no_write_transition,
    extract_final_no_write_transition_checkpoint,
    extract_admission_evidence_seal,
    extract_paper_mode_admission_review
)

def no_write_transition_safety_flags_from_admission(payload: dict[str, Any]) -> list[NoWriteTransitionRiskFlag]:
    flags = []

    if payload.get("activation_allowed") is True:
        flags.append(NoWriteTransitionRiskFlag.ACTIVATION_ALLOWED_RISK)
    if payload.get("transition_allowed") is True:
        flags.append(NoWriteTransitionRiskFlag.TRANSITION_ALLOWED_RISK)

    supports, _ = admission_review_supports_no_write_transition(payload)
    if not supports:
        flags.append(NoWriteTransitionRiskFlag.TRANSITION_DOSSIER_INVALID)

    seal = extract_admission_evidence_seal(payload)
    if not seal:
        flags.append(NoWriteTransitionRiskFlag.EVIDENCE_SEAL_MISSING)

    # Check for blocking keys
    for k, v in payload.items():
         if v is True:
             if k in ["allows_active_paper", "real_order_executed", "sent_to_broker"]:
                 flags.append(NoWriteTransitionRiskFlag.ACTIVE_PAPER_ENABLE_RISK)
             if k in ["broker_order_created"]:
                 flags.append(NoWriteTransitionRiskFlag.BROKER_ORDER_RISK)
             if k in ["telegram_real_send"]:
                 flags.append(NoWriteTransitionRiskFlag.TELEGRAM_REAL_SEND_RISK)
             if k in ["config_patched"]:
                 flags.append(NoWriteTransitionRiskFlag.PRODUCTION_CONFIG_WRITE_RISK)
             if k in ["paper_state_mutated"]:
                 flags.append(NoWriteTransitionRiskFlag.PAPER_STATE_MUTATION_RISK)

    return flags

def no_write_transition_eligibility_reasons(admission_payload: dict[str, Any]) -> list[str]:
    reasons = []
    flags = no_write_transition_safety_flags_from_admission(admission_payload)

    if NoWriteTransitionRiskFlag.ACTIVATION_ALLOWED_RISK in flags:
        reasons.append("activation_allowed is true")
    if NoWriteTransitionRiskFlag.TRANSITION_ALLOWED_RISK in flags:
        reasons.append("transition_allowed is true")

    if not extract_paper_mode_admission_review(admission_payload):
        reasons.append("Missing paper_mode_admission_review")

    if not extract_final_no_write_transition_checkpoint(admission_payload):
        reasons.append("Missing final_no_write_transition_checkpoint")

    if not extract_admission_evidence_seal(admission_payload):
        reasons.append("Missing admission_evidence_seal")

    if admission_payload.get("status") in ["STALE", "FAILED"]:
        reasons.append(f"Admission review status is {admission_payload.get('status')}")

    seal = extract_admission_evidence_seal(admission_payload)
    if seal and seal.get("status") in ["STALE", "FAILED", "MISSING"]:
        reasons.append(f"Evidence seal status is {seal.get('status')}")

    return reasons

def evaluate_no_write_transition_eligibility(admission_payload: dict[str, Any]) -> NoWriteTransitionDecision:
    flags = no_write_transition_safety_flags_from_admission(admission_payload)
    reasons = no_write_transition_eligibility_reasons(admission_payload)

    # Block immediately if safety flags related to execution
    block_flags = [
        NoWriteTransitionRiskFlag.ACTIVATION_ALLOWED_RISK,
        NoWriteTransitionRiskFlag.TRANSITION_ALLOWED_RISK,
        NoWriteTransitionRiskFlag.ACTIVE_PAPER_ENABLE_RISK,
        NoWriteTransitionRiskFlag.BROKER_ORDER_RISK,
        NoWriteTransitionRiskFlag.TELEGRAM_REAL_SEND_RISK,
        NoWriteTransitionRiskFlag.PRODUCTION_CONFIG_WRITE_RISK,
        NoWriteTransitionRiskFlag.PAPER_STATE_MUTATION_RISK
    ]
    if any(f in flags for f in block_flags):
        return NoWriteTransitionDecision.BLOCK

    status = admission_payload.get("status")
    if status in ["STALE", "FAILED"]:
        return NoWriteTransitionDecision.REQUEST_ADMISSION_REVIEW_REFRESH

    seal = extract_admission_evidence_seal(admission_payload)
    if not seal or seal.get("status") in ["STALE", "FAILED", "MISSING"]:
        return NoWriteTransitionDecision.REQUEST_EVIDENCE_SEAL_REFRESH

    if "Missing dry admission" in reasons: # Simplification for mock
        return NoWriteTransitionDecision.REQUEST_DRY_ADMISSION_REFRESH

    if "Missing manual review" in reasons:
        return NoWriteTransitionDecision.REQUEST_MANUAL_REVIEW

    if not reasons and not flags:
        return NoWriteTransitionDecision.CREATE_NO_WRITE_TRANSITION_DOSSIER

    return NoWriteTransitionDecision.INCONCLUSIVE

def transition_dossier_status_from_decision(decision: NoWriteTransitionDecision) -> NoWriteTransitionDossierStatus:
    if decision == NoWriteTransitionDecision.CREATE_NO_WRITE_TRANSITION_DOSSIER:
        return NoWriteTransitionDossierStatus.CREATED
    if decision in [NoWriteTransitionDecision.REQUEST_ADMISSION_REVIEW_REFRESH,
                    NoWriteTransitionDecision.REQUEST_EVIDENCE_SEAL_REFRESH,
                    NoWriteTransitionDecision.REQUEST_DRY_ADMISSION_REFRESH,
                    NoWriteTransitionDecision.REQUEST_MANUAL_REVIEW]:
        return NoWriteTransitionDossierStatus.REQUEST_CHANGES
    if decision == NoWriteTransitionDecision.BLOCK:
        return NoWriteTransitionDossierStatus.BLOCKED
    if decision == NoWriteTransitionDecision.REJECT:
        return NoWriteTransitionDossierStatus.REJECTED
    return NoWriteTransitionDossierStatus.UNKNOWN

def eligibility_checker_to_text(payload: dict[str, Any]) -> str:
    decision = evaluate_no_write_transition_eligibility(payload)
    reasons = no_write_transition_eligibility_reasons(payload)
    text = f"Eligibility Check:\nDecision: {decision.value}\n"
    if reasons:
        text += f"Reasons: {', '.join(reasons)}\n"
    return text
