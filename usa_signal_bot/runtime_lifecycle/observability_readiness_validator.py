from typing import List, Dict, Any, Optional
from usa_signal_bot.runtime_lifecycle.phase104_models import ServiceReadinessMatrix

def validate_observability_readiness(matrix: Optional[ServiceReadinessMatrix] = None) -> List[str]:
    errors = []
    if matrix:
        for item in matrix.items:
            if not item.observability_ready:
                errors.append(f"Service {item.service_id} observability not ready.")
    return errors

def observability_readiness_summary(errors: List[str]) -> Dict[str, Any]:
    return {"errors": errors}

def observability_readiness_validator_to_text(errors: List[str]) -> str:
    if not errors:
        return "Observability ready (local metrics only)."
    return "Observability readiness errors:\n" + "\n".join([f"- {e}" for e in errors])
