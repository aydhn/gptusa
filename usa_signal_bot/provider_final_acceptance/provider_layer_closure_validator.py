from typing import Any
from usa_signal_bot.provider_final_acceptance.phase115_models import ProviderLayerClosureBundle

def validate_provider_layer_closure_safety(bundle: ProviderLayerClosureBundle) -> list[str]:
    errors = []
    if not bundle.closed:
        errors.append("Closure bundle is not marked as closed.")
    if not bundle.frozen:
        errors.append("Closure bundle is not marked as frozen.")
    if not bundle.immutable:
        errors.append("Closure bundle is not marked as immutable.")
    if bundle.phase_start != 106 or bundle.phase_end != 115:
        errors.append("Closure bundle phase range is invalid (expected 106-115).")
    if not bundle.metadata_only:
        errors.append("Closure bundle is not metadata_only.")
    if not bundle.research_data_only:
        errors.append("Closure bundle is not research_data_only.")

    for item in bundle.items:
        if not item.closed:
            errors.append(f"Closure item '{item.closure_name}' is not closed.")

    return errors

def provider_layer_closure_is_complete(bundle: ProviderLayerClosureBundle) -> bool:
    return len(validate_provider_layer_closure_safety(bundle)) == 0

def provider_layer_closure_blocks_phase116(bundle: ProviderLayerClosureBundle) -> bool:
    return not provider_layer_closure_is_complete(bundle)

def provider_layer_closure_validator_summary(errors: list[str]) -> dict[str, Any]:
    return {"valid": len(errors) == 0, "errors": errors}

def provider_layer_closure_validator_to_text(errors: list[str]) -> str:
    if not errors:
        return "Closure Validator: PASS"
    return f"Closure Validator: FAIL ({len(errors)} errors)"
