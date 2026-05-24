from typing import Any
from usa_signal_bot.paper_readiness_board_dossier.board_dossier_models import BoardDossierFullReview

def board_dossier_evidence_from_paper_safe_dossier(payload: dict[str, Any]) -> list[str]:
    evidence = []
    if payload.get("review_id"):
        evidence.append("paper_safe_dossier_full_review")
    if payload.get("paper_safe_dossier"):
        evidence.append("paper_safe_dossier")
    return evidence

def paper_safe_dossier_supports_board_dossier(payload: dict[str, Any]) -> tuple[bool, list[str]]:
    evidence = board_dossier_evidence_from_paper_safe_dossier(payload)
    if "paper_safe_dossier_full_review" in evidence:
        return True, evidence
    return False, ["Missing paper_safe_dossier_full_review"]

def attach_board_dossier_hint_to_paper_safe_dossier_payload(payload: dict[str, Any], review: BoardDossierFullReview) -> dict[str, Any]:
    new_payload = dict(payload)
    new_payload["board_dossier_hint"] = {
        "review_id": review.review_id,
        "status": "VALIDATED_NON_EXECUTION" if review.dossiers and review.dossiers[0].status.name == "VALIDATED_NON_EXECUTION" else "BLOCKED",
        "requires_refresh": False
    }
    return new_payload

def paper_safe_dossier_board_summary(payload: dict[str, Any]) -> dict[str, Any]:
    return payload.get("board_dossier_hint", {})

def paper_safe_dossier_adapter_to_text(payload: dict[str, Any]) -> str:
    summary = paper_safe_dossier_board_summary(payload)
    if not summary:
        return "No Board Dossier hint attached."
    lines = ["Paper Safe Dossier Adapter Hint:"]
    for k, v in summary.items():
        lines.append(f"  {k}: {v}")
    return "\n".join(lines)
