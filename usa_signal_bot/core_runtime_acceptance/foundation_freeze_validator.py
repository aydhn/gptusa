from typing import Dict, Any, List
from usa_signal_bot.core_runtime_acceptance.phase105_models import AdvancedFoundationFreezeBundle

def validate_advanced_foundation_freeze_safety(bundle: AdvancedFoundationFreezeBundle) -> List[str]:
    errors = []
    if not bundle.frozen:
        errors.append("frozen is false")
    if not bundle.immutable:
        errors.append("immutable is false")
    if not bundle.freeze_is_metadata_only:
        errors.append("freeze_is_metadata_only is false")
    if bundle.missing_evidence_count > 0:
        errors.append("missing evidence")
    if bundle.stale_evidence_count > 0:
        errors.append("stale evidence")
    if bundle.next_phase != 106:
        errors.append("next_phase is not 106")
    if bundle.final_phase != 160:
        errors.append("final_phase is not 160")
    return errors

def foundation_freeze_is_complete(bundle: AdvancedFoundationFreezeBundle) -> bool:
    return len(validate_advanced_foundation_freeze_safety(bundle)) == 0

def foundation_freeze_requires_followup(bundle: AdvancedFoundationFreezeBundle) -> bool:
    return bundle.missing_evidence_count > 0 or bundle.stale_evidence_count > 0

def foundation_freeze_blocks_phase106(bundle: AdvancedFoundationFreezeBundle) -> bool:
    return not foundation_freeze_is_complete(bundle)

def foundation_freeze_validator_summary(bundle: AdvancedFoundationFreezeBundle) -> Dict[str, Any]:
    return {
        "valid": foundation_freeze_is_complete(bundle),
        "errors": len(validate_advanced_foundation_freeze_safety(bundle))
    }

def foundation_freeze_validator_to_text(bundle: AdvancedFoundationFreezeBundle) -> str:
    return f"Foundation Freeze Validator: {'Valid' if foundation_freeze_is_complete(bundle) else 'Invalid'}"
