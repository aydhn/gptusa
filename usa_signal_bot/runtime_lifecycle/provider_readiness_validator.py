from typing import List, Dict, Any, Optional
from usa_signal_bot.runtime_lifecycle.phase104_models import ServiceReadinessMatrix

def validate_provider_readiness(matrix: Optional[ServiceReadinessMatrix] = None) -> List[str]:
    # Placeholder for logic ensuring no provider network/paid/scraping API is active
    errors = []
    if matrix:
        for item in matrix.items:
            # We enforce all interface checks locally
            if not item.provider_interface_ready:
                errors.append(f"Service {item.service_id} provider interface not ready.")
    return errors

def provider_readiness_summary(errors: List[str]) -> Dict[str, Any]:
    return {"errors": errors}

def provider_readiness_validator_to_text(errors: List[str]) -> str:
    if not errors:
        return "Provider interfaces ready (no network/paid/scraping allowed)."
    return "Provider readiness errors:\n" + "\n".join([f"- {e}" for e in errors])
