from typing import Any
from usa_signal_bot.provider_final_acceptance.phase115_models import FeatureFactorEngineKickoffGate

def validate_feature_factor_kickoff_gate_safety(gate: FeatureFactorEngineKickoffGate) -> list[str]:
    errors = []
    if gate.activation_allowed:
        errors.append("activation_allowed is true.")
    if gate.produces_trade_signal:
        errors.append("produces_trade_signal is true.")
    if gate.produces_order_decision:
        errors.append("produces_order_decision is true.")
    if not gate.sealed:
        errors.append("Gate is not sealed.")
    return errors

def feature_factor_kickoff_gate_allows_phase116(gate: FeatureFactorEngineKickoffGate) -> bool:
    return gate.phase116_scope_allowed and gate.ready_for_phase116 and gate.sealed

def feature_factor_kickoff_gate_allows_activation(gate: FeatureFactorEngineKickoffGate) -> bool:
    return gate.activation_allowed

def feature_factor_kickoff_gate_blocks_phase116(gate: FeatureFactorEngineKickoffGate) -> bool:
    return not feature_factor_kickoff_gate_allows_phase116(gate)

def feature_factor_kickoff_gate_requires_followup(gate: FeatureFactorEngineKickoffGate) -> bool:
    return feature_factor_kickoff_gate_blocks_phase116(gate)

def feature_factor_kickoff_gate_validator_summary(errors: list[str]) -> dict[str, Any]:
    return {"valid": len(errors) == 0, "errors": errors}

def feature_factor_kickoff_gate_validator_to_text(errors: list[str]) -> str:
    if not errors:
        return "Kickoff Gate Validator: PASS"
    return f"Kickoff Gate Validator: FAIL ({len(errors)} errors)"
