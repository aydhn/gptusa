from typing import Any
from usa_signal_bot.paper_no_write_admission.no_write_admission_models import NoWriteAdmissionFullReview

def no_write_evidence_from_confirmation(payload: dict[str, Any]) -> list[str]:
    return []

def confirmation_supports_no_write_admission(payload: dict[str, Any]) -> tuple[bool, list[str]]:
    return True, []

def attach_no_write_hint_to_confirmation_payload(payload: dict[str, Any], review: NoWriteAdmissionFullReview) -> dict[str, Any]:
    return payload

def confirmation_no_write_summary(payload: dict[str, Any]) -> dict[str, Any]:
    return {}

def confirmation_adapter_to_text(payload: dict[str, Any]) -> str:
    return "Confirmation Adapter"
