from typing import Any, Dict
from usa_signal_bot.paper_safe_dossier.paper_safe_dossier_models import (
    PaperSafeDossierEvidenceItem, NonExecutionAcceptanceSeal, RuntimeComponentMapItem,
    RuntimeRouteMapItem, PrePaperLocalRuntimeMap, PaperSafeGateDossier,
    PaperSafeDossierAuditEntry, PaperSafeDossierFullReview
)
from usa_signal_bot.paper_safe_dossier.dossier_evidence import paper_safe_dossier_evidence_to_text
from usa_signal_bot.paper_safe_dossier.non_execution_acceptance_seal import non_execution_acceptance_seal_to_text
from usa_signal_bot.paper_safe_dossier.local_runtime_map import pre_paper_local_runtime_map_to_text
from usa_signal_bot.paper_safe_dossier.runtime_route_map import runtime_route_map_to_text
from usa_signal_bot.paper_safe_dossier.paper_safe_gate_dossier import paper_safe_dossier_to_text
from usa_signal_bot.paper_safe_dossier.dossier_audit import paper_safe_dossier_audit_to_text
from usa_signal_bot.paper_safe_dossier.dossier_report import paper_safe_dossier_full_review_to_text, paper_safe_dossier_limitations_text

def paper_safe_dossier_evidence_item_to_text(item: PaperSafeDossierEvidenceItem) -> str:
    return paper_safe_dossier_evidence_to_text([item])

def runtime_component_map_item_to_text(item: RuntimeComponentMapItem) -> str:
    return f"Component: {item.component_name} | Mode: {item.mode.value}"

def paper_safe_dossier_audit_entry_to_text(item: PaperSafeDossierAuditEntry) -> str:
    return paper_safe_dossier_audit_to_text([item])

def paper_safe_dossier_store_summary_to_text(summary: Dict[str, Any]) -> str:
    return f"Dossier Store Summary: {summary}"
