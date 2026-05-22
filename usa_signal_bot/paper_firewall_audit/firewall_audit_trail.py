from typing import Any, List, Optional
from datetime import datetime, timezone
from usa_signal_bot.paper_firewall_audit.firewall_audit_models import (
    FirewallAuditTrailEntry, FirewallReplayResult, ZeroMutationAuditReport, ReadinessAuditCheckpoint,
    create_firewall_audit_trail_entry_id
)
from usa_signal_bot.core.enums import FirewallAuditRiskFlag

def create_firewall_audit_trail_entry(
    entity_type: str, entity_id: str, action: str, rationale: str,
    decision: Optional[str] = None, evidence_refs: Optional[List[str]] = None,
    risk_flags: Optional[List[FirewallAuditRiskFlag]] = None
) -> FirewallAuditTrailEntry:
    return FirewallAuditTrailEntry(
        audit_entry_id=create_firewall_audit_trail_entry_id(),
        created_at_utc=datetime.now(timezone.utc).isoformat(),
        entity_type=entity_type,
        entity_id=entity_id,
        action=action,
        decision=decision,
        rationale=rationale,
        evidence_refs=evidence_refs or [],
        risk_flags=risk_flags or [],
        warnings=[],
        errors=[],
        metadata={}
    )

def audit_entry_from_firewall_replay_result(result: FirewallReplayResult) -> FirewallAuditTrailEntry:
    return create_firewall_audit_trail_entry(
        entity_type="FirewallReplayResult",
        entity_id=result.replay_result_id,
        action="FIREWALL_REPLAY",
        rationale=f"Outcome: {result.outcome.value}",
        decision=result.status.value,
        evidence_refs=[],
        risk_flags=result.risk_flags
    )

def audit_entry_from_zero_mutation_audit(report: ZeroMutationAuditReport) -> FirewallAuditTrailEntry:
    return create_firewall_audit_trail_entry(
        entity_type="ZeroMutationAuditReport",
        entity_id=report.audit_id,
        action="ZERO_MUTATION_AUDIT",
        rationale=f"Passed: {report.passed}",
        decision=report.decision.value,
        evidence_refs=[],
        risk_flags=report.risk_flags
    )

def audit_entry_from_readiness_audit_checkpoint(checkpoint: ReadinessAuditCheckpoint) -> FirewallAuditTrailEntry:
    return create_firewall_audit_trail_entry(
        entity_type="ReadinessAuditCheckpoint",
        entity_id=checkpoint.checkpoint_id,
        action="READINESS_AUDIT",
        rationale=f"Decision: {checkpoint.decision.value}",
        decision=checkpoint.decision.value,
        evidence_refs=[],
        risk_flags=checkpoint.risk_flags
    )

def append_firewall_audit_trail_entry(entries: List[FirewallAuditTrailEntry], entry: FirewallAuditTrailEntry) -> List[FirewallAuditTrailEntry]:
    entries.append(entry)
    return entries

def firewall_audit_trail_summary(entries: List[FirewallAuditTrailEntry]) -> dict[str, Any]:
    return {"count": len(entries)}

def firewall_audit_trail_to_text(entries: List[FirewallAuditTrailEntry], limit: int = 100) -> str:
    return f"Audit trail entries: {len(entries)}"
