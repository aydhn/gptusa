from typing import Any, Tuple, List
from usa_signal_bot.paper_mode_dry_admission_gate.dry_admission_gate_models import DryAdmissionGateFullReview

def dry_admission_evidence_from_non_execution_board(payload: dict[str, Any]) -> List[str]:
    return ["non_execution_board_full_review"] if payload else []

def non_execution_board_supports_dry_admission_gate(payload: dict[str, Any]) -> Tuple[bool, List[str]]:
    if not payload:
        return False, ["Missing payload"]
    return True, []

def attach_dry_admission_hint_to_non_execution_board_payload(payload: dict[str, Any], review: DryAdmissionGateFullReview) -> dict[str, Any]:
    from usa_signal_bot.paper_mode_dry_admission_gate.dry_admission_report import dry_admission_gate_full_review_summary
    new_payload = payload.copy()
    new_payload["dry_admission_hint"] = dry_admission_gate_full_review_summary(review)
    return new_payload

def non_execution_board_dry_admission_summary(payload: dict[str, Any]) -> dict[str, Any]:
    return payload.get("dry_admission_hint", {})

def non_execution_board_adapter_to_text(payload: dict[str, Any]) -> str:
    summary = non_execution_board_dry_admission_summary(payload)
    return f"Non-Execution Board Adapter Summary: {summary}"
