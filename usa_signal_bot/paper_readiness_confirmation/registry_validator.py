from typing import Any
from usa_signal_bot.paper_readiness_confirmation.confirmation_models import ActivationStillDeniedRegistryEntry

def validate_activation_denied_registry_entry_safety(entry: ActivationStillDeniedRegistryEntry) -> list[str]:
    errors = []
    if not entry.activation_denied:
         errors.append("activation_denied must be True")
    if entry.activation_allowed:
         errors.append("activation_allowed must be False")
    if entry.allows_active_paper:
         errors.append("allows_active_paper must be False")
    if entry.allows_broker_execution:
         errors.append("allows_broker_execution must be False")
    if entry.allows_paper_state_mutation:
         errors.append("allows_paper_state_mutation must be False")
    if entry.allows_config_patch:
         errors.append("allows_config_patch must be False")
    if entry.allows_telegram_real_send:
         errors.append("allows_telegram_real_send must be False")
    return errors

def registry_entry_allows_activation(entry: ActivationStillDeniedRegistryEntry) -> bool:
    return entry.activation_allowed

def registry_entry_requires_followup(entry: ActivationStillDeniedRegistryEntry) -> bool:
    return len(entry.required_followups) > 0

def registry_entry_blocks_next_stage(entry: ActivationStillDeniedRegistryEntry) -> bool:
    return len(validate_activation_denied_registry_entry_safety(entry)) > 0

def registry_validator_summary(entry: ActivationStillDeniedRegistryEntry) -> dict[str, Any]:
    return {
        "is_safe": not registry_entry_blocks_next_stage(entry),
        "errors": validate_activation_denied_registry_entry_safety(entry)
    }

def registry_validator_to_text(payload: dict[str, Any]) -> str:
    return f"Registry Valid: {payload.get('is_safe', False)}"
