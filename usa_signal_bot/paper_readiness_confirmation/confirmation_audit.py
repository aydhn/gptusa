from typing import Any
import datetime

from usa_signal_bot.paper_readiness_confirmation.confirmation_models import (
    ReadinessConfirmationAuditEntry,
    ReadinessConfirmationQueueItem,
    HumanReviewBundle,
    ActivationStillDeniedRegistryEntry,
    create_readiness_confirmation_audit_id
)
from usa_signal_bot.core.enums import ReadinessConfirmationRiskFlag

def create_readiness_confirmation_audit_entry(
    entity_type: str,
    entity_id: str,
    action: str,
    rationale: str,
    decision: str | None = None,
    evidence_refs: list[str] | None = None,
    risk_flags: list[ReadinessConfirmationRiskFlag] | None = None
) -> ReadinessConfirmationAuditEntry:
    return ReadinessConfirmationAuditEntry(
        audit_id=create_readiness_confirmation_audit_id(),
        created_at_utc=datetime.datetime.utcnow().isoformat() + "Z",
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

def audit_entry_from_confirmation_queue_item(item: ReadinessConfirmationQueueItem) -> ReadinessConfirmationAuditEntry:
    return create_readiness_confirmation_audit_entry(
        entity_type="QUEUE_ITEM",
        entity_id=item.queue_item_id,
        action="CREATE_QUEUE_ITEM",
        rationale=f"Queue item created for candidate {item.candidate_id}",
        decision=item.decision.value,
        evidence_refs=item.evidence_refs,
        risk_flags=item.safety_flags
    )

def audit_entry_from_human_review_bundle(bundle: HumanReviewBundle) -> ReadinessConfirmationAuditEntry:
    return create_readiness_confirmation_audit_entry(
        entity_type="HUMAN_REVIEW_BUNDLE",
        entity_id=bundle.bundle_id,
        action="CREATE_HUMAN_REVIEW_BUNDLE",
        rationale=f"Bundle created for candidate {bundle.candidate_id}",
        decision=None,
        evidence_refs=bundle.evidence_refs,
        risk_flags=bundle.safety_flags
    )

def audit_entry_from_activation_denied_registry_entry(entry: ActivationStillDeniedRegistryEntry) -> ReadinessConfirmationAuditEntry:
    return create_readiness_confirmation_audit_entry(
        entity_type="REGISTRY_ENTRY",
        entity_id=entry.registry_entry_id,
        action="CREATE_REGISTRY_ENTRY",
        rationale=entry.denial_reason,
        decision=entry.decision.value,
        evidence_refs=[],
        risk_flags=entry.safety_flags
    )

def append_readiness_confirmation_audit_entry(
    entries: list[ReadinessConfirmationAuditEntry],
    entry: ReadinessConfirmationAuditEntry
) -> list[ReadinessConfirmationAuditEntry]:
    entries.append(entry)
    return entries

def readiness_confirmation_audit_summary(entries: list[ReadinessConfirmationAuditEntry]) -> dict[str, Any]:
    return {
        "total_entries": len(entries),
        "actions": list(set(e.action for e in entries))
    }

def readiness_confirmation_audit_to_text(entries: list[ReadinessConfirmationAuditEntry], limit: int = 100) -> str:
    summary = readiness_confirmation_audit_summary(entries)
    return f"Audit Entries: {summary['total_entries']}"
