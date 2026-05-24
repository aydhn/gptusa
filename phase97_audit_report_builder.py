import os

path1 = "usa_signal_bot/paper_mode_dry_admission_dossier/dry_admission_dossier_audit.py"
content1 = """from typing import Any
import datetime
from usa_signal_bot.core.enums import DryAdmissionDossierRiskFlag
from usa_signal_bot.paper_mode_dry_admission_dossier.dry_admission_dossier_models import (
    DryAdmissionDossierAuditEntry,
    DryAdmissionGateDossier,
    DryAdmissionAcceptanceSeal,
    PaperModeRehearsalBlockerEvent,
    create_dry_admission_dossier_audit_id
)

def create_dry_admission_dossier_audit_entry(
    entity_type: str,
    entity_id: str,
    action: str,
    rationale: str,
    decision: str | None = None,
    evidence_refs: list[str] | None = None,
    risk_flags: list[DryAdmissionDossierRiskFlag] | None = None
) -> DryAdmissionDossierAuditEntry:
    now = datetime.datetime.utcnow().isoformat() + "Z"
    return DryAdmissionDossierAuditEntry(
        audit_id=create_dry_admission_dossier_audit_id(),
        created_at_utc=now,
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

def audit_entry_from_dry_admission_dossier(dossier: DryAdmissionGateDossier) -> DryAdmissionDossierAuditEntry:
    return create_dry_admission_dossier_audit_entry(
        entity_type="DryAdmissionGateDossier",
        entity_id=dossier.dossier_id,
        action="CREATE_DOSSIER",
        rationale=f"Dossier status: {dossier.status.value}",
        decision=dossier.decision.value,
        evidence_refs=dossier.evidence_refs,
        risk_flags=dossier.safety_flags
    )

def audit_entry_from_dry_admission_acceptance_seal(seal: DryAdmissionAcceptanceSeal) -> DryAdmissionDossierAuditEntry:
    return create_dry_admission_dossier_audit_entry(
        entity_type="DryAdmissionAcceptanceSeal",
        entity_id=seal.seal_id,
        action="CREATE_SEAL",
        rationale=f"Seal status: {seal.status.value}",
        decision=seal.decision.value,
        evidence_refs=[],
        risk_flags=seal.risk_flags
    )

def audit_entry_from_rehearsal_blocker_events(events: list[PaperModeRehearsalBlockerEvent]) -> DryAdmissionDossierAuditEntry:
    return create_dry_admission_dossier_audit_entry(
        entity_type="RehearsalBlockerEventBatch",
        entity_id="batch",
        action="EVALUATE_EVENTS",
        rationale=f"Evaluated {len(events)} events",
        decision="BLOCK" if all(e.blocked for e in events) else "FAIL",
        evidence_refs=[e.event_id for e in events],
        risk_flags=[]
    )

def append_dry_admission_dossier_audit_entry(entries: list[DryAdmissionDossierAuditEntry], entry: DryAdmissionDossierAuditEntry) -> list[DryAdmissionDossierAuditEntry]:
    entries.append(entry)
    return entries

def dry_admission_dossier_audit_summary(entries: list[DryAdmissionDossierAuditEntry]) -> dict[str, Any]:
    return {
        "total_entries": len(entries),
        "actions": [e.action for e in entries]
    }

def dry_admission_dossier_audit_to_text(entries: list[DryAdmissionDossierAuditEntry], limit: int = 100) -> str:
    summary = dry_admission_dossier_audit_summary(entries)
    return f"Audit Trails: {summary['total_entries']} entries"
"""

path2 = "usa_signal_bot/paper_mode_dry_admission_dossier/dry_admission_dossier_report.py"
content2 = """from typing import Any
import datetime

from usa_signal_bot.core.enums import DryAdmissionDossierReportType
from usa_signal_bot.paper_mode_dry_admission_dossier.dry_admission_dossier_models import (
    DryAdmissionDossierFullReview,
    DryAdmissionGateDossier,
    DryAdmissionAcceptanceSeal,
    PaperModeRehearsalBlockerEvent,
    create_dry_admission_dossier_full_review_id
)
from usa_signal_bot.paper_mode_dry_admission_dossier.dry_admission_dossier import build_dry_admission_gate_dossier
from usa_signal_bot.paper_mode_dry_admission_dossier.dry_admission_dossier_audit import audit_entry_from_dry_admission_dossier, audit_entry_from_dry_admission_acceptance_seal, audit_entry_from_rehearsal_blocker_events

def dry_admission_dossier_limitations_text() -> str:
    return (
        "Dry-Admission Dossier Limitations:\n"
        "- No broker/live/demo order.\n"
        "- No active paper enable.\n"
        "- No paper admission.\n"
        "- No shadow launch.\n"
        "- No paper-mode launch.\n"
        "- No rehearsal.\n"
        "- No real paper mutation.\n"
        "- No paper order.\n"
        "- No Telegram real send.\n"
        "- No production config patch.\n"
        "- Dry-admission dossier is not activation.\n"
        "- Dry-admission acceptance seal is metadata-only.\n"
        "- Rehearsal blocker denies rehearsal.\n"
        "- Not investment advice.\n"
    )

def build_dry_admission_dossier_full_review(payload: dict[str, Any]) -> DryAdmissionDossierFullReview:
    dossier = build_dry_admission_gate_dossier(payload)
    return build_dry_admission_dossier_review_from_parts(
        dossier=dossier,
        seal=dossier.acceptance_seal,
        blocker_events=dossier.rehearsal_blocker_events
    )

def build_dry_admission_dossier_review_from_parts(
    dossier: DryAdmissionGateDossier,
    seal: DryAdmissionAcceptanceSeal | None = None,
    blocker_events: list[PaperModeRehearsalBlockerEvent] | None = None
) -> DryAdmissionDossierFullReview:
    now = datetime.datetime.utcnow().isoformat() + "Z"

    audits = [audit_entry_from_dry_admission_dossier(dossier)]
    if seal:
        audits.append(audit_entry_from_dry_admission_acceptance_seal(seal))
    if blocker_events:
        audits.append(audit_entry_from_rehearsal_blocker_events(blocker_events))

    return DryAdmissionDossierFullReview(
        review_id=create_dry_admission_dossier_full_review_id(),
        created_at_utc=now,
        report_type=DryAdmissionDossierReportType.FULL_DRY_ADMISSION_DOSSIER_REVIEW,
        dossiers=[dossier],
        evidence_items=dossier.evidence_items,
        acceptance_seals=[seal] if seal else [],
        rehearsal_blocker_rules=[],
        rehearsal_blocker_events=blocker_events or [],
        audit_entries=audits,
        output_paths={},
        warnings=[],
        errors=[]
    )

def dry_admission_dossier_full_review_summary(review: DryAdmissionDossierFullReview) -> dict[str, Any]:
    return {
        "review_id": review.review_id,
        "dossiers": len(review.dossiers),
        "seals": len(review.acceptance_seals),
        "blocker_events": len(review.rehearsal_blocker_events),
        "audits": len(review.audit_entries)
    }

def dry_admission_dossier_full_review_to_text(review: DryAdmissionDossierFullReview, limit: int = 100) -> str:
    summary = dry_admission_dossier_full_review_summary(review)
    return f"Dry-Admission Full Review [{review.review_id}]: Dossiers={summary['dossiers']}, Seals={summary['seals']}, Events={summary['blocker_events']}"
"""

with open(path1, "w") as f:
    f.write(content1)
with open(path2, "w") as f:
    f.write(content2)

print("Audit and report builder created")
