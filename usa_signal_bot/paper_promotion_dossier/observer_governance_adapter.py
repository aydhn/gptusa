from typing import Any, Dict
from .dossier_builder import build_promotion_dossier_from_observer_governance
from .safety_board_gates import default_final_safety_board_gates
from .risk_register import build_promotion_risk_register
from .safety_board_decision import FinalSafetyBoardDecisionEngine
from .readiness_package import build_staged_paper_readiness_package
from .dossier_report import build_promotion_dossier_review

def promotion_dossier_from_observer_governance_review(payload: Dict[str, Any]) -> Any:
    return build_promotion_dossier_from_observer_governance(payload)

def safety_board_from_observer_governance_review(payload: Dict[str, Any]) -> Any:
    dossier = promotion_dossier_from_observer_governance_review(payload)
    gates = default_final_safety_board_gates(dossier)
    risks = build_promotion_risk_register(dossier, gates)
    engine = FinalSafetyBoardDecisionEngine()
    return engine.decide(dossier, gates, risks)

def readiness_package_from_observer_governance_review(payload: Dict[str, Any]) -> Any:
    dossier = promotion_dossier_from_observer_governance_review(payload)
    board = safety_board_from_observer_governance_review(payload)
    return build_staged_paper_readiness_package(dossier, board)

def promotion_review_from_observer_governance_review(payload: Dict[str, Any]) -> Any:
    dossier = promotion_dossier_from_observer_governance_review(payload)
    board = safety_board_from_observer_governance_review(payload)
    package = build_staged_paper_readiness_package(dossier, board)
    return build_promotion_dossier_review(dossier, board, package)

def attach_promotion_dossier_metadata_to_observer_governance(payload: Dict[str, Any], review: Any) -> Dict[str, Any]:
    payload["promotion_dossier_review_id"] = getattr(review, "review_id", None)
    return payload

def observer_governance_promotion_dossier_summary(payload: Dict[str, Any]) -> Dict[str, Any]:
    return {"promotion_dossier_attached": "promotion_dossier_review_id" in payload}

def observer_governance_adapter_to_text(payload: Dict[str, Any]) -> str:
    return f"Governance Adapter Output. Attached: {'promotion_dossier_review_id' in payload}."
