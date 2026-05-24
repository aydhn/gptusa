from typing import List, Dict, Any, Optional
from usa_signal_bot.runtime_lifecycle.phase104_models import ServiceReadinessMatrix

def validate_notification_readiness(matrix: Optional[ServiceReadinessMatrix] = None) -> List[str]:
    errors = []
    if matrix:
        for item in matrix.items:
            if not item.notification_boundary_ready:
                errors.append(f"Service {item.service_id} notification boundary not ready.")
    return errors

def notification_readiness_summary(errors: List[str]) -> Dict[str, Any]:
    return {"errors": errors}

def notification_readiness_validator_to_text(errors: List[str]) -> str:
    if not errors:
        return "Notification boundary ready (no real sends)."
    return "Notification readiness errors:\n" + "\n".join([f"- {e}" for e in errors])
