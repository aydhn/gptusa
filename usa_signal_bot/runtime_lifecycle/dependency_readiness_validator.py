from typing import List, Dict, Any
from usa_signal_bot.runtime_lifecycle.phase104_models import ServiceReadinessMatrix

def validate_dependency_readiness(matrix: ServiceReadinessMatrix) -> List[str]:
    errors = []
    for item in matrix.items:
        if not item.dependency_ready:
            errors.append(f"Service {item.service_id} has unresolved dependencies.")
    return errors

def dependency_readiness_summary(matrix: ServiceReadinessMatrix) -> Dict[str, Any]:
    return {"errors": validate_dependency_readiness(matrix)}

def dependency_readiness_validator_to_text(errors: List[str]) -> str:
    if not errors:
        return "Dependencies are ready."
    return "Dependency errors:\n" + "\n".join([f"- {e}" for e in errors])
