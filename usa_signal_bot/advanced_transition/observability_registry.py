from typing import Dict, List

def build_phase101_observability_registry() -> Dict[str, str]:
    return {
        "latest_advanced_transition_context_count": "Count",
        "latest_handoff_ingestion_valid_count": "Count",
        "latest_module_inventory_count": "Count",
        "latest_runtime_boundary_blocked_capability_count": "Count",
        "latest_config_consolidation_issue_count": "Count",
        "latest_phase101_validation_issue_count": "Count",
        "latest_advanced_transition_ready_count": "Count",
        "latest_execution_capability_violation_count": "Count"
    }

def validate_observability_registry(registry: Dict[str, str]) -> List[str]:
    errors = []
    if "latest_advanced_transition_context_count" not in registry:
        errors.append("Missing metric")
    return errors

def observability_registry_to_text(registry: Dict[str, str]) -> str:
    return "\n".join([f"{k}: {v}" for k, v in registry.items()])
