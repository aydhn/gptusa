from typing import Any
from datetime import datetime, timezone
from usa_signal_bot.core.enums import BoardDossierRiskFlag
from usa_signal_bot.paper_readiness_board_dossier.board_dossier_models import (
    BoardDossierAuditEntry,
    PaperReadinessBoardDossier,
    AcceptanceBoardSeal,
    ShadowLaunchBlockerEvent,
    create_board_dossier_audit_id
)

def create_board_dossier_audit_entry(entity_type: str, entity_id: str, action: str, rationale: str, decision: str | None = None, evidence_refs: list[str] | None = None, risk_flags: list[BoardDossierRiskFlag] | None = None) -> BoardDossierAuditEntry:
    return BoardDossierAuditEntry(
        audit_id=create_board_dossier_audit_id(),
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
        metadata={"redacted_secrets": True, "local_only": True}
    )

def audit_entry_from_board_dossier(dossier: PaperReadinessBoardDossier) -> BoardDossierAuditEntry:
    return create_board_dossier_audit_entry(
        entity_type="PaperReadinessBoardDossier",
        entity_id=dossier.dossier_id,
        action="BUILD_BOARD_DOSSIER",
        rationale="Built metadata-only dossier from non-execution board outputs.",
        decision=dossier.decision.name,
        evidence_refs=dossier.evidence_refs,
        risk_flags=dossier.safety_flags
    )

def audit_entry_from_acceptance_board_seal(seal: AcceptanceBoardSeal) -> BoardDossierAuditEntry:
    return create_board_dossier_audit_entry(
        entity_type="AcceptanceBoardSeal",
        entity_id=seal.seal_id,
        action="BUILD_ACCEPTANCE_BOARD_SEAL",
        rationale="Built metadata-only seal confirming boundaries without execution permissions.",
        decision=seal.decision.name,
        evidence_refs=[],
        risk_flags=seal.risk_flags
    )

def audit_entry_from_shadow_launch_blocker_events(events: list[ShadowLaunchBlockerEvent]) -> BoardDossierAuditEntry:
    all_blocked = all(e.blocked for e in events)
    return create_board_dossier_audit_entry(
        entity_type="ShadowLaunchBlocker",
        entity_id="shadow_launch_blocker_simulator",
        action="SIMULATE_SHADOW_LAUNCH_ATTEMPTS",
        rationale=f"Simulated {len(events)} shadow launch attempts. All blocked: {all_blocked}.",
        decision="BLOCK_SHADOW_LAUNCH" if all_blocked else "REQUIRE_MANUAL_REVIEW",
        evidence_refs=[e.event_id for e in events],
        risk_flags=[]
    )

def append_board_dossier_audit_entry(entries: list[BoardDossierAuditEntry], entry: BoardDossierAuditEntry) -> list[BoardDossierAuditEntry]:
    # Ensure immutability by creating a new list
    new_entries = list(entries)
    new_entries.append(entry)
    return new_entries

def board_dossier_audit_summary(entries: list[BoardDossierAuditEntry]) -> dict[str, Any]:
    return {
        "total_entries": len(entries),
        "entities_audited": list(set(e.entity_type for e in entries)),
        "decisions": list(set(e.decision for e in entries if e.decision))
    }

def board_dossier_audit_to_text(entries: list[BoardDossierAuditEntry], limit: int = 100) -> str:
    lines = [f"Board Audit Trail ({len(entries)} entries):"]
    for i, entry in enumerate(entries[:limit]):
        lines.append(f"  {i+1}. [{entry.created_at_utc}] {entry.entity_type} - {entry.action} -> {entry.decision or 'N/A'}")
    if len(entries) > limit:
        lines.append(f"  ... and {len(entries) - limit} more")
    return "\n".join(lines)
