from typing import Any, List
from usa_signal_bot.core.enums import (
    PaperModeDryAdmissionDecision,
    PaperModeDryAdmissionStatus,
    DryAdmissionRiskFlag
)
from usa_signal_bot.paper_dry_admission.no_write_ingestion import (
    extract_no_write_contract,
    extract_activation_replay_result,
    extract_paper_mode_preflight,
    no_write_supports_dry_admission
)

def evaluate_dry_admission_eligibility(no_write_payload: dict[str, Any]) -> PaperModeDryAdmissionDecision:
    supported, reasons = no_write_supports_dry_admission(no_write_payload)
    if supported:
        return PaperModeDryAdmissionDecision.RUN_DRY_ADMISSION_REHEARSAL

    if "Missing no-write contract" in reasons or "No-write contract" in "".join(reasons):
        return PaperModeDryAdmissionDecision.REQUEST_NO_WRITE_CONTRACT_REFRESH
    if "Missing activation replay" in reasons:
        return PaperModeDryAdmissionDecision.REQUEST_ACTIVATION_REPLAY_REFRESH
    if "Missing paper mode preflight" in reasons:
        return PaperModeDryAdmissionDecision.REQUEST_MANUAL_REVIEW

    return PaperModeDryAdmissionDecision.BLOCK

def dry_admission_eligibility_reasons(no_write_payload: dict[str, Any]) -> List[str]:
    _, reasons = no_write_supports_dry_admission(no_write_payload)
    return reasons

def dry_admission_safety_flags_from_no_write(payload: dict[str, Any]) -> List[DryAdmissionRiskFlag]:
    flags = []
    contract = extract_no_write_contract(payload)
    preflight = extract_paper_mode_preflight(payload)

    if not contract or not contract.get("activation_denied", False):
        flags.append(DryAdmissionRiskFlag.NO_WRITE_CONTRACT_INVALID)
    if contract and contract.get("activation_allowed", True):
        flags.append(DryAdmissionRiskFlag.ACTIVATION_ALLOWED_RISK)

    if preflight:
        if preflight.get("mutation_detected", False):
            flags.append(DryAdmissionRiskFlag.PAPER_STATE_MUTATION_RISK)
        if not preflight.get("all_writes_blocked", True):
            flags.append(DryAdmissionRiskFlag.DRY_ADMISSION_WRITE_ATTEMPT)
        if preflight.get("activation_allowed", True):
            flags.append(DryAdmissionRiskFlag.ACTIVE_PAPER_ENABLE_RISK)

    return flags

def dry_admission_status_from_decision(decision: PaperModeDryAdmissionDecision) -> PaperModeDryAdmissionStatus:
    if decision == PaperModeDryAdmissionDecision.RUN_DRY_ADMISSION_REHEARSAL:
        return PaperModeDryAdmissionStatus.READY
    elif decision in [PaperModeDryAdmissionDecision.REJECT, PaperModeDryAdmissionDecision.BLOCK]:
        return PaperModeDryAdmissionStatus.BLOCKED
    else:
        return PaperModeDryAdmissionStatus.WARNING

def eligibility_checker_to_text(payload: dict[str, Any]) -> str:
    decision = evaluate_dry_admission_eligibility(payload)
    reasons = dry_admission_eligibility_reasons(payload)
    flags = dry_admission_safety_flags_from_no_write(payload)

    lines = [
        f"Decision: {decision.value}",
        f"Status: {dry_admission_status_from_decision(decision).value}"
    ]
    if reasons:
        lines.append("Reasons:")
        for r in reasons: lines.append(f"  - {r}")
    if flags:
        lines.append("Risk Flags:")
        for f in flags: lines.append(f"  - {f.value}")
    return "\n".join(lines)
