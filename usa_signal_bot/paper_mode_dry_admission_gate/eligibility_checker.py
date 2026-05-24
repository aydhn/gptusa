from typing import Any, List
from usa_signal_bot.core.enums import (
    PaperModeDryAdmissionGateDecision,
    PaperModeDryAdmissionGateStatus,
    DryAdmissionGateRiskFlag
)
from usa_signal_bot.paper_mode_dry_admission_gate.board_dossier_ingestion import board_dossier_supports_dry_admission_gate

def evaluate_dry_admission_gate_eligibility(board_payload: dict[str, Any]) -> PaperModeDryAdmissionGateDecision:
    supported, reasons = board_dossier_supports_dry_admission_gate(board_payload)
    if supported:
        return PaperModeDryAdmissionGateDecision.PASS_TO_DRY_ADMISSION_GATE_DOSSIER

    if any("Missing board dossier" in r for r in reasons) or any("Board dossier decision" in r for r in reasons):
        return PaperModeDryAdmissionGateDecision.REQUEST_BOARD_DOSSIER_REFRESH

    if any("Missing shadow-launch blocker events" in r for r in reasons):
        return PaperModeDryAdmissionGateDecision.REQUEST_SHADOW_REPLAY

    if any("Missing acceptance board seal" in r for r in reasons) or any("Acceptance board seal status" in r for r in reasons):
        return PaperModeDryAdmissionGateDecision.REQUEST_BOARD_EVIDENCE_FREEZE

    return PaperModeDryAdmissionGateDecision.BLOCK

def dry_admission_gate_eligibility_reasons(board_payload: dict[str, Any]) -> List[str]:
    _, reasons = board_dossier_supports_dry_admission_gate(board_payload)
    return reasons

def dry_admission_safety_flags_from_payload(payload: dict[str, Any]) -> List[DryAdmissionGateRiskFlag]:
    flags = []
    supported, reasons = board_dossier_supports_dry_admission_gate(payload)
    if not supported:
        flags.append(DryAdmissionGateRiskFlag.DRY_ADMISSION_GATE_INVALID)

    if payload.get("shadow_launch_allowed"):
        flags.append(DryAdmissionGateRiskFlag.SHADOW_LAUNCH_RISK)

    if payload.get("paper_mode_launch_allowed"):
        flags.append(DryAdmissionGateRiskFlag.PAPER_MODE_LAUNCH_RISK)

    if payload.get("activation_allowed"):
        flags.append(DryAdmissionGateRiskFlag.ACTIVATION_ALLOWED_RISK)

    if payload.get("admission_allowed"):
        flags.append(DryAdmissionGateRiskFlag.ADMISSION_ALLOWED_RISK)

    if payload.get("transition_allowed"):
        flags.append(DryAdmissionGateRiskFlag.TRANSITION_ALLOWED_RISK)

    if payload.get("order_created"):
        flags.append(DryAdmissionGateRiskFlag.ORDER_CREATED_RISK)

    if payload.get("mutation_detected"):
        flags.append(DryAdmissionGateRiskFlag.MUTATION_DETECTED_RISK)

    return flags

def dry_admission_gate_status_from_decision(decision: PaperModeDryAdmissionGateDecision) -> PaperModeDryAdmissionGateStatus:
    if decision == PaperModeDryAdmissionGateDecision.PASS_TO_DRY_ADMISSION_GATE_DOSSIER:
        return PaperModeDryAdmissionGateStatus.VALIDATED_DRY_ADMISSION_SAFE
    elif decision in [
        PaperModeDryAdmissionGateDecision.REQUEST_SHADOW_REPLAY,
        PaperModeDryAdmissionGateDecision.REQUEST_BOARD_EVIDENCE_FREEZE,
        PaperModeDryAdmissionGateDecision.REQUEST_BOARD_DOSSIER_REFRESH,
        PaperModeDryAdmissionGateDecision.REQUEST_MANUAL_REVIEW
    ]:
        return PaperModeDryAdmissionGateStatus.REQUEST_CHANGES
    elif decision == PaperModeDryAdmissionGateDecision.REJECT:
        return PaperModeDryAdmissionGateStatus.REJECTED
    elif decision == PaperModeDryAdmissionGateDecision.BLOCK:
        return PaperModeDryAdmissionGateStatus.BLOCKED
    return PaperModeDryAdmissionGateStatus.UNKNOWN

def eligibility_checker_to_text(payload: dict[str, Any]) -> str:
    decision = evaluate_dry_admission_gate_eligibility(payload)
    status = dry_admission_gate_status_from_decision(decision)
    reasons = dry_admission_gate_eligibility_reasons(payload)
    flags = dry_admission_safety_flags_from_payload(payload)

    text = f"Decision: {decision.value}\nStatus: {status.value}\n"
    if reasons:
        text += "Reasons:\n" + "\n".join(f"- {r}" for r in reasons) + "\n"
    if flags:
        text += "Risk Flags:\n" + "\n".join(f"- {f.value}" for f in flags) + "\n"
    return text
