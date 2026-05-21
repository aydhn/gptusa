from typing import Any
from .observer_governance_models import ObserverGovernanceAuditEntry, ObserverGovernanceDecisionResult, create_observer_governance_audit_id
from usa_signal_bot.core.enums import ObserverGovernanceRiskFlag
from datetime import datetime, timezone

def create_observer_governance_audit_entry(entity_type: str, entity_id: str, action: str, rationale: str, evidence_refs: list[str] | None = None, risk_flags: list[ObserverGovernanceRiskFlag] | None = None) -> ObserverGovernanceAuditEntry:
    return ObserverGovernanceAuditEntry(
        audit_id=create_observer_governance_audit_id(), created_at_utc=datetime.now(timezone.utc).isoformat(),
        entity_type=entity_type, entity_id=entity_id, action=action, rationale=rationale, evidence_refs=evidence_refs or [],
        risk_flags=risk_flags or [], warnings=[], errors=[]
    )

def audit_entry_from_observer_governance_decision(result: ObserverGovernanceDecisionResult) -> ObserverGovernanceAuditEntry:
    return create_observer_governance_audit_entry("Decision", result.decision_id, result.decision.value, result.rationale, risk_flags=result.risk_flags)

def append_observer_governance_audit_entry(entries: list[ObserverGovernanceAuditEntry], entry: ObserverGovernanceAuditEntry) -> list[ObserverGovernanceAuditEntry]:
    return entries + [entry]

def observer_governance_audit_summary(entries: list[ObserverGovernanceAuditEntry]) -> dict[str, Any]:
    return {"total": len(entries)}

def observer_governance_audit_to_text(entries: list[ObserverGovernanceAuditEntry], limit: int = 100) -> str:
    return str(observer_governance_audit_summary(entries))
