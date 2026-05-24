from typing import Any, List
from usa_signal_bot.paper_mode_dry_admission_gate.dry_admission_gate_models import FinalPaperModeDryAdmissionGate
from usa_signal_bot.core.enums import DryAdmissionGateRuleStatus, DryAdmissionGateAssertionStatus

def validate_final_dry_admission_gate_safety(gate: FinalPaperModeDryAdmissionGate) -> List[str]:
    errors = []
    if not gate.sealed: errors.append("Gate must be sealed")
    if not gate.immutable: errors.append("Gate must be immutable")
    if not gate.activation_denied: errors.append("activation_denied must be True")
    if gate.activation_allowed: errors.append("activation_allowed must be False")
    if gate.admission_allowed: errors.append("admission_allowed must be False")
    if gate.transition_allowed: errors.append("transition_allowed must be False")
    if gate.shadow_launch_allowed: errors.append("shadow_launch_allowed must be False")
    if gate.paper_mode_launch_allowed: errors.append("paper_mode_launch_allowed must be False")
    if not gate.all_writes_blocked: errors.append("all_writes_blocked must be True")
    if gate.order_created: errors.append("order_created must be False")
    if gate.mutation_detected: errors.append("mutation_detected must be False")
    if gate.allows_active_paper: errors.append("allows_active_paper must be False")
    if gate.allows_broker_execution: errors.append("allows_broker_execution must be False")
    if gate.allows_paper_state_mutation: errors.append("allows_paper_state_mutation must be False")
    if gate.allows_config_patch: errors.append("allows_config_patch must be False")
    if gate.allows_telegram_real_send: errors.append("allows_telegram_real_send must be False")

    for rule in gate.rules:
        if rule.status in [DryAdmissionGateRuleStatus.FAIL, DryAdmissionGateRuleStatus.BLOCKED]:
            errors.append(f"Rule failed: {rule.rule_name}")

    for assertion in gate.assertions:
        if assertion.status in [DryAdmissionGateAssertionStatus.FAIL, DryAdmissionGateAssertionStatus.BLOCKED]:
            errors.append(f"Assertion failed: {assertion.assertion_name}")

    return errors

def final_dry_admission_gate_allows_shadow_launch(gate: FinalPaperModeDryAdmissionGate) -> bool:
    return gate.shadow_launch_allowed

def final_dry_admission_gate_allows_admission(gate: FinalPaperModeDryAdmissionGate) -> bool:
    return gate.admission_allowed

def final_dry_admission_gate_allows_activation(gate: FinalPaperModeDryAdmissionGate) -> bool:
    return gate.activation_allowed

def final_dry_admission_gate_requires_followup(gate: FinalPaperModeDryAdmissionGate) -> bool:
    return not gate.dry_admission_gate_passed or len(validate_final_dry_admission_gate_safety(gate)) > 0

def final_dry_admission_gate_blocks_next_stage(gate: FinalPaperModeDryAdmissionGate) -> bool:
    return not gate.dry_admission_gate_passed or len(validate_final_dry_admission_gate_safety(gate)) > 0

def final_dry_admission_gate_validator_summary(gate: FinalPaperModeDryAdmissionGate) -> dict[str, Any]:
    errors = validate_final_dry_admission_gate_safety(gate)
    return {
        "valid": len(errors) == 0,
        "errors": errors,
        "blocks_next_stage": final_dry_admission_gate_blocks_next_stage(gate)
    }

def final_dry_admission_gate_validator_to_text(payload: dict[str, Any]) -> str:
    valid = payload.get("valid", False)
    return f"Gate Validator - Valid: {valid}"
