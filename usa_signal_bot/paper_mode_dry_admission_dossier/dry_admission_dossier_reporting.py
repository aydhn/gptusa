from typing import Any
from usa_signal_bot.paper_mode_dry_admission_dossier.dry_admission_dossier_models import (
    DryAdmissionGateDossier,
    DryAdmissionDossierEvidenceItem,
    DryAdmissionAcceptanceSeal,
    PaperModeRehearsalBlockerRule,
    PaperModeRehearsalBlockerEvent,
    DryAdmissionDossierAuditEntry,
    DryAdmissionDossierFullReview
)
from usa_signal_bot.paper_mode_dry_admission_dossier.dossier_evidence import dry_admission_dossier_evidence_to_text
from usa_signal_bot.paper_mode_dry_admission_dossier.dry_admission_acceptance_seal import dry_admission_acceptance_seal_to_text
from usa_signal_bot.paper_mode_dry_admission_dossier.rehearsal_blocker_rules import rehearsal_blocker_rules_to_text
from usa_signal_bot.paper_mode_dry_admission_dossier.dry_admission_dossier import dry_admission_dossier_to_text
from usa_signal_bot.paper_mode_dry_admission_dossier.dry_admission_dossier_audit import dry_admission_dossier_audit_to_text
from usa_signal_bot.paper_mode_dry_admission_dossier.dry_admission_dossier_report import dry_admission_dossier_full_review_to_text, dry_admission_dossier_limitations_text

def dry_admission_dossier_evidence_item_to_text(item: DryAdmissionDossierEvidenceItem) -> str:
    return f"Evidence [{item.evidence_type}]: {item.status.value}"

def rehearsal_blocker_rule_to_text(item: PaperModeRehearsalBlockerRule) -> str:
    return f"Rule [{item.attempt_type.value}]: Blocking={item.blocking}"

def rehearsal_blocker_event_to_text(item: PaperModeRehearsalBlockerEvent) -> str:
    return f"Event [{item.attempt_type.value}]: Blocked={item.blocked}"

def dry_admission_gate_dossier_to_text(item: DryAdmissionGateDossier, limit: int = 100) -> str:
    return dry_admission_dossier_to_text(item, limit)

def dry_admission_dossier_audit_entry_to_text(item: DryAdmissionDossierAuditEntry) -> str:
    return f"Audit [{item.entity_type} - {item.action}]: {item.decision}"

def dry_admission_dossier_store_summary_to_text(summary: dict[str, Any]) -> str:
    return f"Dossier Store: {summary['reviews']} reviews, {summary['dossiers']} dossiers, {summary['seals']} seals"
