from typing import Any
from usa_signal_bot.paper_no_order_dossier.no_order_dossier_models import (
    NoOrderPaperSessionDossier,
    BridgeReplayAuditSeal,
    PaperAdmissionBlockerRule,
    PaperAdmissionBlockerEvent,
    NoOrderDossierAuditEntry,
    NoOrderDossierFullReview
)
from usa_signal_bot.paper_no_order_dossier.no_order_session_dossier import no_order_dossier_to_text
from usa_signal_bot.paper_no_order_dossier.bridge_replay_audit_seal import bridge_replay_audit_seal_to_text
from usa_signal_bot.paper_no_order_dossier.admission_blocker_rules import paper_admission_blocker_rules_to_text
from usa_signal_bot.paper_no_order_dossier.admission_attempt_simulator import paper_admission_attempt_simulator_to_text
from usa_signal_bot.paper_no_order_dossier.no_order_dossier_audit import no_order_dossier_audit_to_text
from usa_signal_bot.paper_no_order_dossier.no_order_dossier_report import no_order_dossier_full_review_to_text, no_order_dossier_limitations_text

def no_order_dossier_evidence_item_to_text(item: Any) -> str:
    # Uses the list one mainly in dossier_evidence
    return str(item)

def paper_admission_blocker_rule_to_text(item: PaperAdmissionBlockerRule) -> str:
    return paper_admission_blocker_rules_to_text([item])

def paper_admission_blocker_event_to_text(item: PaperAdmissionBlockerEvent) -> str:
    return paper_admission_attempt_simulator_to_text([item])

def no_order_paper_session_dossier_to_text(item: NoOrderPaperSessionDossier, limit: int = 100) -> str:
    return no_order_dossier_to_text(item, limit)

def no_order_dossier_audit_entry_to_text(item: NoOrderDossierAuditEntry) -> str:
    return no_order_dossier_audit_to_text([item])

def no_order_dossier_store_summary_to_text(summary: dict[str, Any]) -> str:
    import json
    return json.dumps(summary, indent=2)
