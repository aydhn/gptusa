from typing import Any
from usa_signal_bot.paper_no_write_transition.no_write_transition_models import (
    TransitionDossierEvidenceItem,
    AdmissionEvidenceSealValidation,
    AdmissionEvidenceSealRefresh,
    PaperSandboxBridgeRoute,
    PaperSandboxBridgeEnvelope,
    NoWriteTransitionDossier,
    NoWriteTransitionAuditEntry,
    NoWriteTransitionFullReview
)
from usa_signal_bot.paper_no_write_transition.transition_report import no_write_transition_limitations_text

def transition_dossier_evidence_item_to_text(item: TransitionDossierEvidenceItem) -> str:
    return f"Evidence: {item.evidence_type} [{item.status.value}]"

def admission_evidence_seal_validation_to_text(item: AdmissionEvidenceSealValidation) -> str:
    return f"Seal Validation: {item.status.value}"

def admission_evidence_seal_refresh_to_text(item: AdmissionEvidenceSealRefresh) -> str:
    return f"Seal Refresh: {item.status.value}"

def paper_sandbox_bridge_route_to_text(item: PaperSandboxBridgeRoute) -> str:
    return f"Route: {item.route_type.value} [{item.status.value}]"

def paper_sandbox_bridge_envelope_to_text(item: PaperSandboxBridgeEnvelope, limit: int = 100) -> str:
    return f"Bridge Envelope: {item.status.value}"

def no_write_transition_dossier_to_text(item: NoWriteTransitionDossier, limit: int = 100) -> str:
    return f"Dossier: {item.status.value}"

def no_write_transition_audit_entry_to_text(item: NoWriteTransitionAuditEntry) -> str:
    return f"Audit: {item.action}"

def no_write_transition_full_review_to_text(item: NoWriteTransitionFullReview, limit: int = 100) -> str:
    return f"Full Review: {item.report_type.value}\n{no_write_transition_limitations_text()}"

def no_write_transition_store_summary_to_text(summary: dict[str, Any]) -> str:
    return f"Store Summary: {summary}"
