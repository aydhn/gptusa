from typing import Any, Optional
from usa_signal_bot.paper_no_write_transition.no_write_transition_models import PaperSandboxBridgeEnvelope
from usa_signal_bot.paper_no_write_transition.bridge_route_guard import bridge_route_allows_dangerous_operation

def validate_bridge_against_no_write_contract(
    envelope: PaperSandboxBridgeEnvelope,
    admission_payload: Optional[dict[str, Any]] = None
) -> list[str]:
    errors = []
    if not envelope.bridge_is_no_write:
        errors.append("Contract violation: Bridge is not no-write")
    if not envelope.activation_denied:
        errors.append("Contract violation: Activation is not denied")
    if envelope.activation_allowed:
        errors.append("Contract violation: Activation is allowed")
    for r in envelope.routes:
        if bridge_route_allows_dangerous_operation(r):
            errors.append(f"Contract violation: Route {r.route_type.value} allows dangerous operation")
    return errors

def bridge_contract_allows_activation(envelope: PaperSandboxBridgeEnvelope) -> bool:
    return envelope.activation_allowed

def bridge_contract_allows_write(envelope: PaperSandboxBridgeEnvelope) -> bool:
    return any(r.write_allowed for r in envelope.routes) or not envelope.all_writes_blocked

def bridge_contract_requires_followup(envelope: PaperSandboxBridgeEnvelope) -> bool:
    return len(envelope.required_followups) > 0

def bridge_contract_validator_summary(envelope: PaperSandboxBridgeEnvelope) -> dict[str, Any]:
    errors = validate_bridge_against_no_write_contract(envelope)
    return {
        "is_valid": len(errors) == 0,
        "violations": errors
    }

def bridge_contract_validator_to_text(payload: dict[str, Any]) -> str:
    return f"Contract Valid: {payload.get('is_valid')} Violations: {len(payload.get('violations', []))}"
