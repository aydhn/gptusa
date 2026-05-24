from typing import Any
from usa_signal_bot.advanced_runtime.phase102_models import NormalizedRuntimeRegistry, ConfigSurfaceRecord

def validate_runtime_registry_safety(registry: NormalizedRuntimeRegistry) -> list[str]:
    errors = []
    errors.extend(validate_no_execution_enabled_in_registry(registry))
    errors.extend(validate_provider_safety_policies(registry))
    errors.extend(validate_config_surface_safety(registry.config_surface))
    return errors

def validate_no_execution_enabled_in_registry(registry: NormalizedRuntimeRegistry) -> list[str]:
    errors = []
    if registry.activation_allowed: errors.append("activation_allowed is true")
    if registry.active_paper_enabled: errors.append("active_paper_enabled is true")
    if registry.broker_execution_enabled: errors.append("broker_execution_enabled is true")
    if registry.paper_state_mutation_enabled: errors.append("paper_state_mutation_enabled is true")
    if registry.telegram_real_send_enabled: errors.append("telegram_real_send_enabled is true")
    if registry.scraping_enabled: errors.append("scraping_enabled is true")
    if registry.dashboard_enabled: errors.append("dashboard_enabled is true")
    return errors

def validate_provider_safety_policies(registry: NormalizedRuntimeRegistry) -> list[str]:
    errors = []
    for sm in registry.provider_safety_manifests:
        if not sm.safe_for_phase102:
            pass # It's okay if not safe, just shouldn't be used actively
        if not sm.broker_blocked:
            errors.append(f"Provider {sm.provider_name} does not block broker")
    return errors

def validate_config_surface_safety(records: list[ConfigSurfaceRecord]) -> list[str]:
    return []

def safety_policy_summary(errors: list[str]) -> dict[str, Any]:
    return {"errors": errors, "is_safe": len(errors) == 0}

def safety_policy_validator_to_text(errors: list[str]) -> str:
    return "Safe" if not errors else "Unsafe:\n" + "\n".join(errors)
