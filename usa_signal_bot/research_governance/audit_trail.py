from typing import Optional, Any
from datetime import datetime
from usa_signal_bot.research_governance.governance_models import GovernanceAuditTrail, create_governance_audit_trail_id

def create_governance_audit_event(event_type: str, entity_id: str, payload: Optional[dict[str, Any]] = None) -> dict[str, Any]:
    # Redact sensitive info if needed
    safe_payload = payload.copy() if payload else {}
    for k in ["api_key", "secret", "token"]:
        if k in safe_payload:
            safe_payload[k] = "***REDACTED***"

    return {
        "timestamp": datetime.utcnow().isoformat(),
        "event_type": event_type,
        "entity_id": entity_id,
        "payload": safe_payload
    }

def build_governance_audit_trail(entity_type: str, entity_id: str, events: list[dict[str, Any]]) -> GovernanceAuditTrail:
    return GovernanceAuditTrail(
        audit_id=create_governance_audit_trail_id(),
        created_at_utc=datetime.utcnow().isoformat(),
        entity_type=entity_type,
        entity_id=entity_id,
        events=events,
        warning_count=0, error_count=0, blocked_count=0,
        warnings=[], errors=[]
    )

def append_governance_audit_event(trail: GovernanceAuditTrail, event: dict[str, Any]) -> GovernanceAuditTrail:
    trail.events.append(event)
    return trail

def audit_trail_summary(trail: GovernanceAuditTrail) -> dict[str, Any]:
    return {"event_count": len(trail.events)}

def audit_trail_to_text(trail: GovernanceAuditTrail, limit: int = 100) -> str:
    return "Audit Trail"
