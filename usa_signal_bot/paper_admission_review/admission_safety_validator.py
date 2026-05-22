from typing import Any, Dict, List, Optional
import json
from usa_signal_bot.core.enums import AdmissionReviewRiskFlag
from .admission_review_models import PaperModeAdmissionReview, LedgerReconciliationReport, FinalNoWriteTransitionCheckpoint

def collect_admission_safety_flags(
    admission_review: Optional[PaperModeAdmissionReview] = None,
    reconciliation: Optional[LedgerReconciliationReport] = None,
    checkpoint: Optional[FinalNoWriteTransitionCheckpoint] = None
) -> List[AdmissionReviewRiskFlag]:
    flags = []
    if admission_review:
        flags.extend(admission_review.safety_flags)
        if admission_review.activation_allowed:
            flags.append(AdmissionReviewRiskFlag.ACTIVATION_ALLOWED_RISK)
        if not admission_review.activation_denied:
            flags.append(AdmissionReviewRiskFlag.ACTIVE_PAPER_ENABLE_RISK)
        if admission_review.transition_allowed:
             flags.append(AdmissionReviewRiskFlag.TRANSITION_CHECKPOINT_INVALID)
        if not admission_review.all_writes_blocked:
             flags.append(AdmissionReviewRiskFlag.PRODUCTION_CONFIG_WRITE_RISK)
        if admission_review.mutation_detected:
             flags.append(AdmissionReviewRiskFlag.PAPER_STATE_MUTATION_RISK)
        for attr in ["allows_active_paper", "allows_broker_execution", "allows_paper_state_mutation", "allows_config_patch", "allows_telegram_real_send"]:
             if getattr(admission_review, attr, True):
                 if "broker" in attr: flags.append(AdmissionReviewRiskFlag.BROKER_ORDER_RISK)
                 elif "telegram" in attr: flags.append(AdmissionReviewRiskFlag.TELEGRAM_REAL_SEND_RISK)
                 elif "config" in attr: flags.append(AdmissionReviewRiskFlag.PRODUCTION_CONFIG_WRITE_RISK)
                 elif "mutation" in attr: flags.append(AdmissionReviewRiskFlag.PAPER_STATE_MUTATION_RISK)
                 else: flags.append(AdmissionReviewRiskFlag.ACTIVE_PAPER_ENABLE_RISK)

    if reconciliation:
        flags.extend(reconciliation.safety_flags)
    if checkpoint:
        flags.extend(checkpoint.safety_flags)

    return list(set(flags))

def admission_has_blocking_flags(flags: List[AdmissionReviewRiskFlag]) -> bool:
    blocking_flags = [
        AdmissionReviewRiskFlag.REAL_ORDER_RISK,
        AdmissionReviewRiskFlag.PAPER_ORDER_RISK,
        AdmissionReviewRiskFlag.BROKER_ORDER_RISK,
        AdmissionReviewRiskFlag.PAPER_STATE_MUTATION_RISK,
        AdmissionReviewRiskFlag.TELEGRAM_REAL_SEND_RISK,
        AdmissionReviewRiskFlag.PRODUCTION_CONFIG_WRITE_RISK,
        AdmissionReviewRiskFlag.ACTIVE_PAPER_ENABLE_RISK,
        AdmissionReviewRiskFlag.ACTIVATION_ALLOWED_RISK,
        AdmissionReviewRiskFlag.TRANSITION_CHECKPOINT_INVALID,
        AdmissionReviewRiskFlag.LEDGER_ACTIVATION_RISK,
        AdmissionReviewRiskFlag.SECRET_RISK
    ]
    return any(f in blocking_flags for f in flags)

def validate_admission_safety(
    admission_review: Optional[PaperModeAdmissionReview] = None,
    reconciliation: Optional[LedgerReconciliationReport] = None,
    checkpoint: Optional[FinalNoWriteTransitionCheckpoint] = None
) -> List[str]:
    flags = collect_admission_safety_flags(admission_review, reconciliation, checkpoint)
    errors = []
    if admission_has_blocking_flags(flags):
        for flag in flags:
             if flag in [
                AdmissionReviewRiskFlag.REAL_ORDER_RISK,
                AdmissionReviewRiskFlag.PAPER_ORDER_RISK,
                AdmissionReviewRiskFlag.BROKER_ORDER_RISK,
                AdmissionReviewRiskFlag.PAPER_STATE_MUTATION_RISK,
                AdmissionReviewRiskFlag.TELEGRAM_REAL_SEND_RISK,
                AdmissionReviewRiskFlag.PRODUCTION_CONFIG_WRITE_RISK,
                AdmissionReviewRiskFlag.ACTIVE_PAPER_ENABLE_RISK,
                AdmissionReviewRiskFlag.ACTIVATION_ALLOWED_RISK,
                AdmissionReviewRiskFlag.TRANSITION_CHECKPOINT_INVALID,
                AdmissionReviewRiskFlag.LEDGER_ACTIVATION_RISK,
                AdmissionReviewRiskFlag.SECRET_RISK
             ]:
                  errors.append(f"Blocking safety risk detected: {flag.value}")
    return errors

def admission_safety_summary(flags: List[AdmissionReviewRiskFlag]) -> Dict[str, Any]:
    return {
        "safe": not admission_has_blocking_flags(flags),
        "blocking_flags": [f.value for f in flags if f in [
            AdmissionReviewRiskFlag.REAL_ORDER_RISK, AdmissionReviewRiskFlag.PAPER_ORDER_RISK,
            AdmissionReviewRiskFlag.BROKER_ORDER_RISK, AdmissionReviewRiskFlag.PAPER_STATE_MUTATION_RISK,
            AdmissionReviewRiskFlag.TELEGRAM_REAL_SEND_RISK, AdmissionReviewRiskFlag.PRODUCTION_CONFIG_WRITE_RISK,
            AdmissionReviewRiskFlag.ACTIVE_PAPER_ENABLE_RISK, AdmissionReviewRiskFlag.ACTIVATION_ALLOWED_RISK,
            AdmissionReviewRiskFlag.TRANSITION_CHECKPOINT_INVALID, AdmissionReviewRiskFlag.LEDGER_ACTIVATION_RISK,
            AdmissionReviewRiskFlag.SECRET_RISK]],
        "all_flags": [f.value for f in flags]
    }

def admission_safety_validator_to_text(payload: Dict[str, Any]) -> str:
    return json.dumps(payload, indent=2)
