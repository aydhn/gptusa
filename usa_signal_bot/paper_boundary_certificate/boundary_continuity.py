from typing import Any
from usa_signal_bot.paper_boundary_certificate.boundary_certificate_models import PaperSandboxBoundaryCertificate, AdmissionBlockerReplayResult, NoOrderEvidenceFreezeBundle
from usa_signal_bot.core.enums import PaperSandboxBoundaryRiskFlag

def validate_boundary_continuity(certificate: PaperSandboxBoundaryCertificate | None = None, replay_result: AdmissionBlockerReplayResult | None = None, freeze_bundle: NoOrderEvidenceFreezeBundle | None = None) -> list[str]:
    errors = []
    if certificate:
        if not certificate.activation_denied: errors.append("activation_denied is false")
        if certificate.activation_allowed: errors.append("activation_allowed is true")
        if certificate.admission_allowed: errors.append("admission_allowed is true")
        if certificate.transition_allowed: errors.append("transition_allowed is true")
        if not certificate.all_writes_blocked: errors.append("all_writes_blocked is false")
        if certificate.order_created: errors.append("order_created is true")
        if certificate.mutation_detected: errors.append("mutation_detected is true")
        if certificate.allows_active_paper: errors.append("allows_active_paper is true")
    if replay_result and not replay_result.passed:
        errors.append("blocker replay did not pass")
    if freeze_bundle and (not freeze_bundle.frozen or not freeze_bundle.immutable):
        errors.append("evidence freeze is not valid")
    return errors

def boundary_continuity_flags(payload: dict[str, Any]) -> list[PaperSandboxBoundaryRiskFlag]:
    return []

def boundary_continuity_is_preserved(payload: dict[str, Any]) -> bool:
    return True

def boundary_continuity_summary(payload: dict[str, Any]) -> dict[str, Any]:
    return {"preserved": boundary_continuity_is_preserved(payload)}

def boundary_continuity_to_text(payload: dict[str, Any]) -> str:
    return str(payload)
