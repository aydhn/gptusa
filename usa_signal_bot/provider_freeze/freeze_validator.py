from typing import Any, Dict, List
from usa_signal_bot.provider_freeze.phase114_models import ProviderExpansionFreezeBundle

def validate_provider_freeze_bundle_safety(bundle: ProviderExpansionFreezeBundle) -> List[str]:
    errors = []
    if not bundle.frozen:
        errors.append("Bundle is not marked frozen.")
    if not bundle.immutable:
        errors.append("Bundle is not marked immutable.")
    if bundle.phase_start != 106 or bundle.phase_end != 114:
        errors.append("Bundle phase range invalid (must be 106-114).")

    if bundle.missing_items > 0:
        errors.append(f"Bundle is missing {bundle.missing_items} evidence items.")
    if bundle.stale_items > 0:
        errors.append(f"Bundle contains {bundle.stale_items} stale evidence items.")

    if bundle.secret_violation_count > 0:
        errors.append(f"Bundle contains {bundle.secret_violation_count} secret violations.")
    if bundle.execution_violation_count > 0:
        errors.append(f"Bundle contains {bundle.execution_violation_count} execution language violations.")
    if bundle.trade_signal_violation_count > 0:
        errors.append(f"Bundle contains {bundle.trade_signal_violation_count} trade signal language violations.")
    if bundle.order_decision_violation_count > 0:
        errors.append(f"Bundle contains {bundle.order_decision_violation_count} order decision language violations.")

    return errors

def provider_freeze_bundle_is_complete(bundle: ProviderExpansionFreezeBundle) -> bool:
    return bundle.missing_items == 0 and bundle.invalid_items == 0

def provider_freeze_bundle_blocks_phase115(bundle: ProviderExpansionFreezeBundle) -> bool:
    return len(validate_provider_freeze_bundle_safety(bundle)) > 0 or not provider_freeze_bundle_is_complete(bundle)

def provider_freeze_validator_summary(errors: List[str]) -> Dict[str, Any]:
    return {
        "valid": len(errors) == 0,
        "error_count": len(errors),
        "errors": errors
    }

def provider_freeze_validator_to_text(errors: List[str]) -> str:
    if not errors:
        return "Provider Freeze Bundle is safe and valid."

    lines = ["Provider Freeze Bundle Validation Errors:"]
    for e in errors:
        lines.append(f" - {e}")
    return "\n".join(lines)
