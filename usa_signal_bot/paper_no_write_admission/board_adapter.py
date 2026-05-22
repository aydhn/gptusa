from typing import Any
from usa_signal_bot.paper_no_write_admission.no_write_admission_models import NoWritePaperAdmissionContract, ActivationReplayResult, PaperModePreflightRun, NoWriteAdmissionFullReview

def no_write_contract_from_board(payload: dict[str, Any]) -> NoWritePaperAdmissionContract:
    pass

def activation_replay_result_from_board(payload: dict[str, Any]) -> ActivationReplayResult:
    pass

def paper_mode_preflight_from_board(payload: dict[str, Any]) -> PaperModePreflightRun:
    pass

def no_write_full_review_from_board(payload: dict[str, Any]) -> NoWriteAdmissionFullReview:
    pass

def attach_no_write_metadata_to_board_payload(payload: dict[str, Any], review: NoWriteAdmissionFullReview) -> dict[str, Any]:
    payload["no_write_admission_review"] = review.review_id
    return payload

def board_no_write_summary(payload: dict[str, Any]) -> dict[str, Any]:
    return {}

def board_adapter_to_text(payload: dict[str, Any]) -> str:
    return "Board Adapter"
