from typing import Any
import json
from datetime import datetime, timezone
from usa_signal_bot.core.enums import NoOrderDossierRiskFlag
from usa_signal_bot.paper_no_order_dossier.no_order_dossier_models import (
    NoOrderDossierAuditEntry,
    create_no_order_dossier_audit_id,
    NoOrderPaperSessionDossier,
    BridgeReplayAuditSeal,
    PaperAdmissionBlockerEvent,
    no_order_dossier_audit_entry_to_dict
)

def create_no_order_dossier_audit_entry(
    entity_type: str,
    entity_id: str,
    action: str,
    rationale: str,
    decision: str | None = None,
    evidence_refs: list[str] | None = None,
    risk_flags: list[NoOrderDossierRiskFlag] | None = None
) -> NoOrderDossierAuditEntry:
    return NoOrderDossierAuditEntry(
        audit_id=create_no_order_dossier_audit_id(),
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

def audit_entry_from_no_order_dossier(dossier: NoOrderPaperSessionDossier) -> NoOrderDossierAuditEntry:
    return create_no_order_dossier_audit_entry(
        entity_type="NoOrderPaperSessionDossier",
        entity_id=dossier.dossier_id,
        action="DOSSIER_CREATION",
        rationale=f"Created No-Order Dossier for candidate {dossier.candidate_id}",
        decision=dossier.decision.value,
        evidence_refs=dossier.evidence_refs,
        risk_flags=dossier.safety_flags
    )

def audit_entry_from_bridge_replay_audit_seal(seal: BridgeReplayAuditSeal) -> NoOrderDossierAuditEntry:
    return create_no_order_dossier_audit_entry(
        entity_type="BridgeReplayAuditSeal",
        entity_id=seal.seal_id,
        action="REPLAY_SEAL_CREATION",
        rationale=f"Created Bridge Replay Audit Seal for candidate {seal.candidate_id}",
        decision=seal.decision.value,
        evidence_refs=seal.evidence_refs,
        risk_flags=seal.risk_flags
    )

def audit_entry_from_admission_blocker_events(events: list[PaperAdmissionBlockerEvent]) -> NoOrderDossierAuditEntry:
    blocked_count = len([e for e in events if e.blocked])
    all_blocked = (blocked_count == len(events)) and len(events) > 0
    return create_no_order_dossier_audit_entry(
        entity_type="PaperAdmissionBlockerEvent",
        entity_id="bulk_events",
        action="ADMISSION_BLOCKER_SIMULATION",
        rationale=f"Simulated {len(events)} admission attempts. All blocked: {all_blocked}",
        decision="BLOCK" if all_blocked else "FAILED",
        evidence_refs=[e.event_id for e in events],
        risk_flags=[]
    )

def append_no_order_dossier_audit_entry(entries: list[NoOrderDossierAuditEntry], entry: NoOrderDossierAuditEntry) -> list[NoOrderDossierAuditEntry]:
    return entries + [entry]

def no_order_dossier_audit_summary(entries: list[NoOrderDossierAuditEntry]) -> dict[str, Any]:
    return {
        "total_entries": len(entries),
        "actions": list(set(e.action for e in entries)),
        "decisions": list(set(e.decision for e in entries if e.decision))
    }

def no_order_dossier_audit_to_text(entries: list[NoOrderDossierAuditEntry], limit: int = 100) -> str:
    return json.dumps([no_order_dossier_audit_entry_to_dict(e) for e in entries[:limit]], indent=2)
