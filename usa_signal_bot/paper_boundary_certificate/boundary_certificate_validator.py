from typing import Any
from usa_signal_bot.paper_boundary_certificate.boundary_certificate_models import PaperSandboxBoundaryCertificate
from usa_signal_bot.core.enums import BoundaryRuleStatus, BoundaryAssertionStatus

def validate_boundary_certificate_safety(certificate: PaperSandboxBoundaryCertificate) -> list[str]:
    errors = []
    if not certificate.sealed:
        errors.append("Certificate is not sealed")
    if not certificate.immutable:
        errors.append("Certificate is not immutable")
    if not certificate.activation_denied:
        errors.append("Activation is not denied")
    if certificate.activation_allowed:
        errors.append("Activation is allowed")
    if certificate.admission_allowed:
        errors.append("Admission is allowed")
    if certificate.transition_allowed:
        errors.append("Transition is allowed")
    if not certificate.all_writes_blocked:
        errors.append("All writes are not blocked")
    if certificate.order_created:
        errors.append("Order was created")
    if certificate.mutation_detected:
        errors.append("Mutation detected")
    if certificate.allows_active_paper:
        errors.append("Active paper is allowed")
    if certificate.allows_broker_execution:
        errors.append("Broker execution is allowed")
    if certificate.allows_paper_state_mutation:
        errors.append("Paper state mutation is allowed")
    if certificate.allows_config_patch:
        errors.append("Config patch is allowed")
    if certificate.allows_telegram_real_send:
        errors.append("Telegram real send is allowed")

    for r in certificate.boundary_rules:
        if r.status in [BoundaryRuleStatus.FAIL, BoundaryRuleStatus.BLOCKED]:
            errors.append(f"Boundary rule failed: {r.rule_name}")

    for a in certificate.boundary_assertions:
        if a.status in [BoundaryAssertionStatus.FAIL, BoundaryAssertionStatus.BLOCKED]:
            errors.append(f"Boundary assertion failed: {a.assertion_name}")

    return errors

def boundary_certificate_allows_activation(certificate: PaperSandboxBoundaryCertificate) -> bool:
    return certificate.activation_allowed

def boundary_certificate_allows_admission(certificate: PaperSandboxBoundaryCertificate) -> bool:
    return certificate.admission_allowed

def boundary_certificate_requires_followup(certificate: PaperSandboxBoundaryCertificate) -> bool:
    return len(validate_boundary_certificate_safety(certificate)) > 0

def boundary_certificate_blocks_next_stage(certificate: PaperSandboxBoundaryCertificate) -> bool:
    return boundary_certificate_requires_followup(certificate)

def boundary_certificate_validator_summary(certificate: PaperSandboxBoundaryCertificate) -> dict[str, Any]:
    return {"safe": not boundary_certificate_requires_followup(certificate), "errors": validate_boundary_certificate_safety(certificate)}

def boundary_certificate_validator_to_text(payload: dict[str, Any]) -> str:
    return str(payload)
