from typing import Any
from usa_signal_bot.paper_readiness_board_dossier.board_dossier_models import (
    BoardDossierEvidenceItem,
    AcceptanceBoardSeal,
    ShadowLaunchBlockerRule,
    ShadowLaunchBlockerEvent,
    PaperReadinessBoardDossier,
    BoardDossierAuditEntry,
    BoardDossierFullReview
)
from usa_signal_bot.paper_readiness_board_dossier.board_dossier_report import (
    board_dossier_full_review_to_text as _full_review_to_text,
    board_dossier_limitations_text as _limitations_text
)
from usa_signal_bot.paper_readiness_board_dossier.board_dossier import board_dossier_to_text as _dossier_to_text
from usa_signal_bot.paper_readiness_board_dossier.acceptance_board_seal import acceptance_board_seal_to_text as _seal_to_text
from usa_signal_bot.paper_readiness_board_dossier.shadow_launch_blocker_rules import shadow_launch_blocker_rules_to_text as _rules_to_text
from usa_signal_bot.paper_readiness_board_dossier.shadow_launch_attempt_simulator import shadow_launch_attempt_simulator_to_text as _events_to_text
from usa_signal_bot.paper_readiness_board_dossier.board_dossier_audit import board_dossier_audit_to_text as _audit_to_text

def board_dossier_evidence_item_to_text(item: BoardDossierEvidenceItem) -> str:
    return f"Evidence: {item.evidence_type} [{item.status.name}] (Available: {item.available})"

def acceptance_board_seal_to_text(item: AcceptanceBoardSeal) -> str:
    return _seal_to_text(item)

def shadow_launch_blocker_rule_to_text(item: ShadowLaunchBlockerRule) -> str:
    return f"Rule: {item.attempt_type.name} -> {item.action.name}"

def shadow_launch_blocker_event_to_text(item: ShadowLaunchBlockerEvent) -> str:
    return f"Event: {item.attempt_type.name} -> Blocked: {item.blocked}"

def paper_readiness_board_dossier_to_text(item: PaperReadinessBoardDossier, limit: int = 100) -> str:
    return _dossier_to_text(item, limit)

def board_dossier_audit_entry_to_text(item: BoardDossierAuditEntry) -> str:
    return f"Audit: {item.entity_type} {item.action} -> {item.decision}"

def board_dossier_full_review_to_text(item: BoardDossierFullReview, limit: int = 100) -> str:
    return _full_review_to_text(item, limit)

def board_dossier_store_summary_to_text(summary: dict[str, Any]) -> str:
    return f"Store Summary:\n  Dossiers: {summary.get('dossiers', 0)}\n  Acceptance Seals: {summary.get('acceptance_seals', 0)}\n  Full Reviews: {summary.get('full_reviews', 0)}"

def board_dossier_limitations_text() -> str:
    return _limitations_text()
