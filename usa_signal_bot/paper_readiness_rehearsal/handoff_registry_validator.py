from typing import Any, Dict, List
from usa_signal_bot.paper_readiness_rehearsal.readiness_rehearsal_models import GuardedHandoffRegistryEntry
from usa_signal_bot.core.enums import GuardedHandoffDecision

def validate_handoff_entry_safety(entry: GuardedHandoffRegistryEntry) -> List[str]:
    errors = []
    if entry.allows_active_paper:
        errors.append("Registry entry unexpectedly allows active paper")
    if entry.allows_broker_execution:
        errors.append("Registry entry unexpectedly allows broker execution")
    if entry.allows_paper_state_mutation:
        errors.append("Registry entry unexpectedly allows paper state mutation")
    if entry.allows_config_patch:
        errors.append("Registry entry unexpectedly allows config patch")
    return errors

def validate_handoff_entry_evidence(entry: GuardedHandoffRegistryEntry) -> List[str]:
    errors = []
    if not entry.evidence_refs:
        errors.append("Missing evidence refs in registry entry")
    return errors

def handoff_entry_allows_activation(entry: GuardedHandoffRegistryEntry) -> bool:
    # Handoff entry is metadata only, NEVER allows activation
    return False

def handoff_entry_blocks_next_review(entry: GuardedHandoffRegistryEntry) -> bool:
    if entry.decision != GuardedHandoffDecision.REGISTER_FOR_FINAL_NON_EXECUTING_HANDOFF_REVIEW:
        return True
    if validate_handoff_entry_safety(entry) or validate_handoff_entry_evidence(entry):
        return True
    return False

def handoff_registry_validator_summary(entry: GuardedHandoffRegistryEntry) -> Dict[str, Any]:
    return {
        "is_safe": not bool(validate_handoff_entry_safety(entry)),
        "blocks_next_review": handoff_entry_blocks_next_review(entry)
    }

def handoff_registry_validator_to_text(payload: Dict[str, Any]) -> str:
    return f"Registry Validator: safe={payload.get('is_safe', False)}, blocks_next={payload.get('blocks_next_review', True)}"
