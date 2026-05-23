from typing import Any
import json
from usa_signal_bot.paper_no_order_dossier.no_order_dossier_models import (
    NoOrderPaperSessionDossier,
    BridgeReplayAuditSeal,
    PaperAdmissionBlockerEvent,
    NoOrderDossierFullReview
)
from usa_signal_bot.paper_no_order_dossier.no_order_session_dossier import build_no_order_paper_session_dossier
from usa_signal_bot.paper_no_order_dossier.bridge_replay_audit_seal import build_bridge_replay_audit_seal
from usa_signal_bot.paper_no_order_dossier.admission_attempt_simulator import simulate_paper_admission_attempts
from usa_signal_bot.paper_no_order_dossier.no_order_dossier_report import build_no_order_dossier_full_review

def no_order_dossier_from_bridge(payload: dict[str, Any]) -> NoOrderPaperSessionDossier:
    return build_no_order_paper_session_dossier(payload)

def bridge_replay_audit_seal_from_bridge(payload: dict[str, Any]) -> BridgeReplayAuditSeal:
    return build_bridge_replay_audit_seal(payload)

def admission_blocker_events_from_bridge(payload: dict[str, Any]) -> list[PaperAdmissionBlockerEvent]:
    return simulate_paper_admission_attempts()

def no_order_dossier_full_review_from_bridge(payload: dict[str, Any]) -> NoOrderDossierFullReview:
    return build_no_order_dossier_full_review(payload)

def attach_no_order_dossier_metadata_to_bridge_payload(payload: dict[str, Any], review: NoOrderDossierFullReview) -> dict[str, Any]:
    out = payload.copy()
    out["no_order_dossier_review_id"] = review.review_id
    dossier = review.dossiers[0] if review.dossiers else None
    if dossier:
        out["no_order_dossier_status"] = dossier.status.value
    return out

def bridge_no_order_dossier_summary(payload: dict[str, Any]) -> dict[str, Any]:
    return {
        "review_id": payload.get("review_id"),
        "no_order_dossier_review_id": payload.get("no_order_dossier_review_id"),
        "no_order_dossier_status": payload.get("no_order_dossier_status")
    }

def bridge_adapter_to_text(payload: dict[str, Any]) -> str:
    return json.dumps(payload, indent=2)
