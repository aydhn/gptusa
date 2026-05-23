from typing import Any
from usa_signal_bot.core.enums import PaperSandboxBoundaryDecision, PaperSandboxBoundaryCertificateStatus, PaperSandboxBoundaryRiskFlag
from usa_signal_bot.paper_boundary_certificate.no_order_ingestion import no_order_supports_boundary_certificate

def evaluate_boundary_certificate_eligibility(no_order_payload: dict[str, Any]) -> PaperSandboxBoundaryDecision:
    supports, warnings = no_order_supports_boundary_certificate(no_order_payload)
    if not supports:
        return PaperSandboxBoundaryDecision.BLOCK
    return PaperSandboxBoundaryDecision.CREATE_BOUNDARY_CERTIFICATE

def boundary_certificate_eligibility_reasons(no_order_payload: dict[str, Any]) -> list[str]:
    _, warnings = no_order_supports_boundary_certificate(no_order_payload)
    return warnings

def boundary_safety_flags_from_no_order(payload: dict[str, Any]) -> list[PaperSandboxBoundaryRiskFlag]:
    flags = []
    if payload.get("activation_allowed", False):
        flags.append(PaperSandboxBoundaryRiskFlag.ACTIVATION_ALLOWED_RISK)
    if payload.get("admission_allowed", False):
        flags.append(PaperSandboxBoundaryRiskFlag.ADMISSION_ALLOWED_RISK)
    if payload.get("transition_allowed", False):
        flags.append(PaperSandboxBoundaryRiskFlag.TRANSITION_ALLOWED_RISK)
    if payload.get("order_created", False):
        flags.append(PaperSandboxBoundaryRiskFlag.ORDER_CREATED_RISK)
    if payload.get("mutation_detected", False):
        flags.append(PaperSandboxBoundaryRiskFlag.MUTATION_DETECTED_RISK)
    return flags

def boundary_certificate_status_from_decision(decision: PaperSandboxBoundaryDecision) -> PaperSandboxBoundaryCertificateStatus:
    if decision == PaperSandboxBoundaryDecision.CREATE_BOUNDARY_CERTIFICATE:
        return PaperSandboxBoundaryCertificateStatus.CREATED
    elif decision == PaperSandboxBoundaryDecision.BLOCK:
        return PaperSandboxBoundaryCertificateStatus.BLOCKED
    return PaperSandboxBoundaryCertificateStatus.DRAFT

def eligibility_checker_to_text(payload: dict[str, Any]) -> str:
    return f"Decision: {evaluate_boundary_certificate_eligibility(payload).value}"
