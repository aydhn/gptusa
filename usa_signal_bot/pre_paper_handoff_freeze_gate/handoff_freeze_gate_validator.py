from typing import Any, List
from usa_signal_bot.pre_paper_handoff_freeze_gate.handoff_freeze_models import FinalPrePaperHandoffFreezeGate
from usa_signal_bot.core.enums import HandoffFreezeRuleStatus, HandoffFreezeAssertionStatus

def validate_final_handoff_freeze_gate_safety(gate: FinalPrePaperHandoffFreezeGate) -> List[str]:
    errors = []
    if not gate.sealed:
        errors.append("Gate must be sealed")
    if not gate.immutable:
        errors.append("Gate must be immutable")
    if not gate.frozen:
        errors.append("Gate must be frozen")
    if not gate.handoff_is_metadata_only:
        errors.append("Gate handoff must be metadata-only")
    if not gate.activation_denied:
        errors.append("activation_denied must be True")
    if gate.activation_allowed:
        errors.append("activation_allowed must be False")
    if gate.admission_allowed:
        errors.append("admission_allowed must be False")
    if gate.transition_allowed:
        errors.append("transition_allowed must be False")
    if gate.sandbox_runtime_admission_allowed:
        errors.append("sandbox_runtime_admission_allowed must be False")
    if gate.paper_sandbox_runtime_allowed:
        errors.append("paper_sandbox_runtime_allowed must be False")
    if gate.simulator_admission_allowed:
        errors.append("simulator_admission_allowed must be False")
    if gate.local_paper_simulator_allowed:
        errors.append("local_paper_simulator_allowed must be False")
    if gate.active_paper_enabled:
        errors.append("active_paper_enabled must be False")
    if not gate.all_writes_blocked:
        errors.append("all_writes_blocked must be True")
    if gate.order_created:
        errors.append("order_created must be False")
    if gate.mutation_detected:
        errors.append("mutation_detected must be False")
    if gate.allows_active_paper:
        errors.append("allows_active_paper must be False")
    if gate.allows_broker_execution:
        errors.append("allows_broker_execution must be False")
    if gate.allows_paper_state_mutation:
        errors.append("allows_paper_state_mutation must be False")
    if gate.allows_config_patch:
        errors.append("allows_config_patch must be False")
    if gate.allows_telegram_real_send:
        errors.append("allows_telegram_real_send must be False")

    for rule in gate.rules:
        if rule.status in [HandoffFreezeRuleStatus.FAIL, HandoffFreezeRuleStatus.BLOCKED]:
            errors.append(f"Rule failed/blocked: {rule.rule_name}")

    for assertion in gate.assertions:
        if assertion.status in [HandoffFreezeAssertionStatus.FAIL, HandoffFreezeAssertionStatus.BLOCKED]:
            errors.append(f"Assertion failed/blocked: {assertion.assertion_name}")

    if gate.sandbox_replay_result and not gate.sandbox_replay_result.passed:
        errors.append("Sandbox replay failed")

    if gate.evidence_freeze and gate.evidence_freeze.missing_evidence_count > 0:
        errors.append("Evidence freeze failed or is incomplete")

    return errors

def final_handoff_freeze_gate_allows_sandbox_runtime_admission(gate: FinalPrePaperHandoffFreezeGate) -> bool:
    return gate.sandbox_runtime_admission_allowed

def final_handoff_freeze_gate_allows_paper_admission(gate: FinalPrePaperHandoffFreezeGate) -> bool:
    return gate.admission_allowed

def final_handoff_freeze_gate_allows_activation(gate: FinalPrePaperHandoffFreezeGate) -> bool:
    return gate.activation_allowed

def final_handoff_freeze_gate_requires_followup(gate: FinalPrePaperHandoffFreezeGate) -> bool:
    return len(gate.required_followups) > 0 or len(validate_final_handoff_freeze_gate_safety(gate)) > 0

def final_handoff_freeze_gate_blocks_next_stage(gate: FinalPrePaperHandoffFreezeGate) -> bool:
    return final_handoff_freeze_gate_requires_followup(gate)

def final_handoff_freeze_gate_validator_summary(gate: FinalPrePaperHandoffFreezeGate) -> dict[str, Any]:
    errors = validate_final_handoff_freeze_gate_safety(gate)
    return {
        "valid": len(errors) == 0,
        "errors": errors
    }

def final_handoff_freeze_gate_validator_to_text(payload: dict[str, Any]) -> str:
    res = f"Final Handoff Freeze Gate Validation\nValid: {payload.get('valid')}\n"
    if payload.get("errors"):
        res += "Errors:\n"
        for e in payload.get("errors", []):
            res += f"- {e}\n"
    return res
