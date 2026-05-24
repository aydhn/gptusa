from typing import Dict, Any, List
from usa_signal_bot.core_runtime_acceptance.phase105_models import DataProviderExpansionKickoffGate

def validate_provider_kickoff_gate_safety(gate: DataProviderExpansionKickoffGate) -> List[str]:
    errors = []
    if not gate.ready_for_phase106:
        errors.append("not ready_for_phase106")
    if not gate.sealed or not gate.immutable or not gate.frozen:
        errors.append("not sealed/immutable/frozen")
    if not gate.metadata_only:
        errors.append("not metadata_only")
    if gate.activation_allowed:
        errors.append("activation_allowed is true")
    if gate.active_paper_enabled:
        errors.append("active_paper_enabled is true")
    if gate.broker_execution_enabled:
        errors.append("broker_execution_enabled is true")
    if gate.paper_state_mutation_enabled:
        errors.append("paper_state_mutation_enabled is true")
    if gate.telegram_real_send_enabled:
        errors.append("telegram_real_send_enabled is true")
    if gate.scraping_enabled:
        errors.append("scraping_enabled is true")
    if gate.html_parse_enabled:
        errors.append("html_parse_enabled is true")
    if gate.dashboard_enabled:
        errors.append("dashboard_enabled is true")
    if gate.paid_api_enabled:
        errors.append("paid_api_enabled is true")
    if gate.provider_network_fetch_required:
        errors.append("provider_network_fetch_required is true")
    return errors

def provider_kickoff_gate_allows_phase106(gate: DataProviderExpansionKickoffGate) -> bool:
    return gate.phase106_scope_allowed

def provider_kickoff_gate_allows_activation(gate: DataProviderExpansionKickoffGate) -> bool:
    return gate.activation_allowed

def provider_kickoff_gate_allows_network_fetch(gate: DataProviderExpansionKickoffGate) -> bool:
    return gate.network_used

def provider_kickoff_gate_requires_followup(gate: DataProviderExpansionKickoffGate) -> bool:
    return len(validate_provider_kickoff_gate_safety(gate)) > 0

def provider_kickoff_gate_blocks_phase106(gate: DataProviderExpansionKickoffGate) -> bool:
    return not gate.ready_for_phase106

def provider_kickoff_gate_validator_summary(gate: DataProviderExpansionKickoffGate) -> Dict[str, Any]:
    return {"valid": len(validate_provider_kickoff_gate_safety(gate)) == 0}

def provider_kickoff_gate_validator_to_text(gate: DataProviderExpansionKickoffGate) -> str:
    return f"Kickoff Gate Validator: {'Valid' if len(validate_provider_kickoff_gate_safety(gate)) == 0 else 'Invalid'}"
