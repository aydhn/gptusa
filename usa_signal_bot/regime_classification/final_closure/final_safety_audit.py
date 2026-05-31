from typing import Any, Dict, List
from usa_signal_bot.regime_classification.final_closure.phase135_models import (
    RegimeResearchFreezeIngestionResult,
    RegimeFinalClosureResult,
    RegimeFreezeSeal,
    RegimeFinalSafetyAudit,
    RegimeFinalClosureQuality,
    create_regime_final_safety_audit_id
)
from datetime import datetime, timezone

def run_final_safety_audit(ingestion: RegimeResearchFreezeIngestionResult, closure_result: RegimeFinalClosureResult, seal: RegimeFreezeSeal) -> RegimeFinalSafetyAudit:
    passed = closure_result.closure_passed

    return RegimeFinalSafetyAudit(
        audit_id=create_regime_final_safety_audit_id(),
        created_at_utc=datetime.now(timezone.utc).isoformat(),
        source_closure_result_id=closure_result.closure_result_id,
        source_seal_id=seal.seal_id,
        safety_passed=passed,
        quality=RegimeFinalClosureQuality.HIGH if passed else RegimeFinalClosureQuality.LOW
    )

def validate_final_safety_audit(audit: RegimeFinalSafetyAudit) -> List[str]:
    return []

def final_safety_audit_passed(audit: RegimeFinalSafetyAudit) -> bool:
    return audit.safety_passed

def final_safety_audit_summary(audit: RegimeFinalSafetyAudit) -> Dict[str, Any]:
    return {"passed": audit.safety_passed}

def final_safety_audit_to_text(audit: RegimeFinalSafetyAudit, limit: int = 300) -> str:
    return f"Audit Passed: {audit.safety_passed}"
