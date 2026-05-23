from typing import Any, Dict
from usa_signal_bot.paper_readiness_non_execution_board.non_execution_board_models import (
    PaperReadinessNonExecutionBoard,
    RuntimeMapReplayResult,
    NonExecutionSealIntegrityAudit,
    NonExecutionBoardFullReview
)

def non_execution_board_from_dossier(payload: Dict[str, Any]) -> PaperReadinessNonExecutionBoard:
    # Dummy read logic from dossier payload
    # A real implementation would parse the json payload
    pass

def runtime_map_replay_from_dossier(payload: Dict[str, Any]) -> RuntimeMapReplayResult:
    pass

def seal_integrity_audit_from_dossier(payload: Dict[str, Any]) -> NonExecutionSealIntegrityAudit:
    pass

def non_execution_board_full_review_from_dossier(payload: Dict[str, Any]) -> NonExecutionBoardFullReview:
    pass

def attach_non_execution_board_metadata_to_dossier_payload(payload: Dict[str, Any], review: NonExecutionBoardFullReview) -> Dict[str, Any]:
    from usa_signal_bot.paper_readiness_non_execution_board.non_execution_board_models import non_execution_board_full_review_to_dict
    payload["non_execution_board_reviews"] = payload.get("non_execution_board_reviews", [])
    payload["non_execution_board_reviews"].append(non_execution_board_full_review_to_dict(review))
    return payload

def dossier_non_execution_board_summary(payload: Dict[str, Any]) -> Dict[str, Any]:
    reviews = payload.get("non_execution_board_reviews", [])
    return {
        "review_count": len(reviews),
        "latest_decision": reviews[-1].get("boards", [{}])[0].get("decision") if reviews else None
    }

def dossier_adapter_to_text(payload: Dict[str, Any]) -> str:
    summary = dossier_non_execution_board_summary(payload)
    return f"--- DOSSIER ADAPTER ---\nReview Count: {summary['review_count']}\nLatest Decision: {summary['latest_decision']}"
