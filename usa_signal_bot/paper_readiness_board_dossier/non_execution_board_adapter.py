from typing import Any
from usa_signal_bot.paper_readiness_board_dossier.board_dossier_models import (
    PaperReadinessBoardDossier,
    AcceptanceBoardSeal,
    ShadowLaunchBlockerEvent,
    BoardDossierFullReview
)
from usa_signal_bot.paper_readiness_board_dossier.board_dossier import build_paper_readiness_board_dossier
from usa_signal_bot.paper_readiness_board_dossier.acceptance_board_seal import build_acceptance_board_seal
from usa_signal_bot.paper_readiness_board_dossier.shadow_launch_attempt_simulator import simulate_shadow_launch_attempts
from usa_signal_bot.paper_readiness_board_dossier.board_dossier_report import build_board_dossier_review_from_parts

def board_dossier_from_non_execution_board(payload: dict[str, Any]) -> PaperReadinessBoardDossier:
    return build_paper_readiness_board_dossier(payload)

def acceptance_board_seal_from_non_execution_board(payload: dict[str, Any]) -> AcceptanceBoardSeal:
    return build_acceptance_board_seal(payload)

def shadow_launch_blocker_events_from_non_execution_board(payload: dict[str, Any]) -> list[ShadowLaunchBlockerEvent]:
    # Regardless of payload, the simulator does not use it as it's purely metadata based
    return simulate_shadow_launch_attempts()

def board_dossier_full_review_from_non_execution_board(payload: dict[str, Any]) -> BoardDossierFullReview:
    dossier = board_dossier_from_non_execution_board(payload)
    seal = acceptance_board_seal_from_non_execution_board(payload)
    events = shadow_launch_blocker_events_from_non_execution_board(payload)
    return build_board_dossier_review_from_parts(dossier, seal, events)

def attach_board_dossier_metadata_to_non_execution_board_payload(payload: dict[str, Any], review: BoardDossierFullReview) -> dict[str, Any]:
    new_payload = dict(payload)
    new_payload["board_dossier_metadata"] = {
        "review_id": review.review_id,
        "dossiers_created": len(review.dossiers),
        "seals_created": len(review.acceptance_board_seals),
        "shadow_launch_blocked_all": all(e.blocked for e in review.shadow_launch_blocker_events) if review.shadow_launch_blocker_events else False
    }
    return new_payload

def non_execution_board_dossier_summary(payload: dict[str, Any]) -> dict[str, Any]:
    return payload.get("board_dossier_metadata", {})

def non_execution_board_adapter_to_text(payload: dict[str, Any]) -> str:
    summary = non_execution_board_dossier_summary(payload)
    if not summary:
        return "No Board Dossier metadata attached."
    lines = ["Non-Execution Board Adapter Metadata:"]
    for k, v in summary.items():
        lines.append(f"  {k}: {v}")
    return "\n".join(lines)
